from __future__ import annotations
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, create_engine, ForeignKey, Relationship
from fastapi.encoders import jsonable_encoder


class UserScopeLink(SQLModel, table=True):
    __tablename__ = "users_scopes"
    user_id: Optional[str] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    scope_id: Optional[str] = Field(
        default=None, foreign_key="scopes.id", primary_key=True
    )


class Scope(SQLModel, table=True):
    __tablename__ = "scopes"
    id: Optional[str] = Field(primary_key=True)
    scope: str
    users: User = Relationship(back_populates="scopes", link_model=UserScopeLink)


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

    scopes: Scope = Relationship(back_populates="users", link_model=UserScopeLink)
    wallets: list[Wallet] = Field(default=[], foreign_key="shared_wallets.user_id")
    cards: list[Card] = Field(default=[], foreign_key="cards_users.user_id")
    # friends: list[User] = Field(default=[], foreign_key="friends.user_id")
    # avatar: Optional[str] = None

    # @property
    # def is_admin(self):
    #     if "admin" in self.scopes:
    #         return True
    #     return False


class UserRegistration(BaseModel):
    id: str | None
    username: constr(min_length=2, max_length=20)
    email: EmailStr
    phone: constr(regex="^\d{10}$")
    f_name: str
    l_name: str
    password: constr(regex="^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+*&^_]).{8,}$")


class Wallet(SQLModel, table=True):
    __tablename__ = "wallets"
    id: Optional[str] = Field(primary_key=True)
    owner: Optional[str] = Field(default=None, foreign_key="users.id")
    currency: str  # Currency
    balance: float = Field(default=0)
    users: list[str] = Field(default=[], foreign_key="shared_wallets.wallet_id")


class Card(SQLModel, table=True):
    __tablename__ = "cards"
    id: Optional[str] = Field(primary_key=True)
    number: constr(regex="^\d{16}$") = Field(unique=True)
    expiry: datetime
    holder: constr(min_length=2, max_length=30)
    cvc: constr(regex="^\d{3}$")


class Transaction(BaseModel):
    __tablename__ = "transactions"
    id: Optional[str] = Field(primary_key=True)
    wallet_sender: Optional[str]
    card_sender: Optional[str]
    wallet_receiver: str
    currency: str  # Currency
    amount: float
    status: constr(regex="^pending|success|cancelled$")


class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: User


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class PasswordUpdateModel(BaseModel):
    old_password: str
    new_password: str


class UserLogin(BaseModel):
    username: constr(min_length=2, max_length=20)
    password: str
