from __future__ import annotations
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Any, Optional, List
from sqlalchemy.orm import relationship
from sqlmodel import (
    SQLModel,
    Field,
    Session,
    create_engine,
    ForeignKey,
    Relationship,
    select,
)
from fastapi.encoders import jsonable_encoder
from app.data import engine


class UserScopeLink(SQLModel, table=True):
    __tablename__ = "users_scopes"
    user_id: str = Field(foreign_key="users.id", primary_key=True)
    scope_id: int = Field(foreign_key="scopes.id", primary_key=True)


class Scope(SQLModel, table=True):
    __tablename__ = "scopes"
    id: Optional[int] = Field(primary_key=True)
    scope: str
    users: User = Relationship(back_populates="scopes", link_model=UserScopeLink)


class UserCardLink(SQLModel, table=True):
    __tablename__ = "cards_users"
    user_id: str = Field(foreign_key="users.id", primary_key=True)
    card_id: str = Field(foreign_key="cards.id", primary_key=True)


class Card(SQLModel, table=True):
    __tablename__ = "cards"
    id: Optional[str] = Field(primary_key=True)
    number: constr(regex="^\d{16}$") = Field(unique=True)
    expiry: datetime
    holder: constr(min_length=2, max_length=30)
    cvc: constr(regex="^\d{3}$")
    users: User = Relationship(back_populates="cards", link_model=UserCardLink)


class UserWalletLink(SQLModel, table=True):
    __tablename__ = "shared_wallets"
    user_id: str = Field(foreign_key="users.id", primary_key=True)
    wallet_id: str = Field(foreign_key="wallets.id", primary_key=True)


class Wallet(SQLModel, table=True):
    __tablename__ = "wallets"
    id: Optional[str] = Field(primary_key=True)
    owner_id: Optional[str] = Field(default=None, foreign_key="users.id")
    currency: str  # Currency
    balance: float = Field(default=0)

    users: User = Relationship(back_populates="wallets", link_model=UserWalletLink)

    owner: User = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="User.id==Wallet.owner_id")
    )  # lazy="joined" can be added here


class FriendLink(SQLModel, table=True):
    __tablename__ = "friends"
    user_id: str = Field(foreign_key="users.id", primary_key=True)
    friend_id: str = Field(foreign_key="users.id", primary_key=True)


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[str] = Field(primary_key=True)
    username: constr(min_length=2, max_length=20) = Field(unique=True)
    password: str
    email: EmailStr = Field(unique=True)
    phone: constr(regex="^\d{10}$") = Field(unique=True)
    f_name: str
    l_name: str
    email_confirmed: bool = Field(default=False)

    scopes: Scope = Relationship(
        back_populates="users",
        link_model=UserScopeLink,
        sa_relationship_kwargs=dict(lazy="joined"),
    )
    cards: Card = Relationship(back_populates="users", link_model=UserCardLink)
    wallets: Wallet = Relationship(back_populates="users", link_model=UserWalletLink)
    friends: User = Relationship(
        back_populates="friends",
        link_model=FriendLink,
        sa_relationship_kwargs=dict(
            primaryjoin="User.id==FriendLink.user_id",
            secondaryjoin="User.id==FriendLink.friend_id",
        ),
    )  # lazy="joined" can be added here
    # avatar: Optional[str] = None


class UserRegistration(BaseModel):
    username: constr(min_length=2, max_length=20)
    email: EmailStr
    phone: constr(regex="^\d{10}$")
    f_name: str
    l_name: str
    password: constr(regex="^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+*&^_]).{8,}$")


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"
    id: Optional[str] = Field(primary_key=True)
    wallet_sender: Optional[str] = Field(default=None, foreign_key="wallets.id")
    card_sender: Optional[str] = Field(default=None, foreign_key="cards.id")
    wallet_receiver: str = Field(foreign_key="wallets.id")
    currency: str  # Currency
    amount: float
    status: constr(regex="^pending|success|cancelled$")

    card_sen_obj: Optional[Card] = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="Card.id==Transaction.card_sender")
    )  # lazy="joined" can be added here

    wallet_sen_obj: Optional[Wallet] = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="Wallet.id==Transaction.wallet_sender")
    )  # lazy="joined" can be added here

    wallet_rec_obj: Optional[Wallet] = Relationship(
        sa_relationship_kwargs=dict(
            primaryjoin="Wallet.id==Transaction.wallet_receiver"
        )
    )  # lazy="joined" can be added here


class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: User


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[int] = []


class PasswordUpdateModel(BaseModel):
    old_password: str
    new_password: str


class UserLogin(BaseModel):
    username: constr(min_length=2, max_length=20)
    password: str
