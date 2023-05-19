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


class UserRegistration(BaseModel):
    username: constr(min_length=2, max_length=20)
    email: EmailStr
    phone: constr(regex="^\d{10}$")
    f_name: str
    l_name: str
    password: constr(regex="^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+*&^_]).{8,}$")


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
