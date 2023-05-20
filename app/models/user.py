from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.card import Card
    from app.models.scope import Scope
    from app.models.wallet import Wallet
from app.models.card import UserCardLink
from app.models.wallet import UserWalletLink
from app.models.scope import UserScopeLink

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


class UserBase(SQLModel):
    pass


class UserLogin(BaseModel):
    username: constr(min_length=2, max_length=20)
    password: str


class UserCreate:
    pass


class UserUpdate:
    pass


class UserPassChange:
    pass


class UserCollections:
    pass


class FriendLink(SQLModel, table=True):
    __tablename__ = "friends"
    user_id: str = Field(foreign_key="users.id", primary_key=True)
    friend_id: str = Field(foreign_key="users.id", primary_key=True)


class UserBase(SQLModel):
    username: constr(min_length=2, max_length=20) = Field(unique=True)
    email: EmailStr = Field(unique=True)
    phone: constr(regex="^\d{10}$") = Field(unique=True)
    f_name: str
    l_name: str


class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[str] = Field(primary_key=True)
    password: str
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


class UserCreate(UserBase):
    password: constr(regex="^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+*&^_]).{8,}$")
