from typing import TYPE_CHECKING, List

from fastapi import Body

if TYPE_CHECKING:
    from app.models.card import Card
    from app.models.scope import Scope
    from app.models.wallet import Wallet

from app.models.card import UserCardLink
from app.models.wallet import UserWalletLink
from app.models.scope import UserScopeLink

from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class UserLogin(BaseModel):
    username: str
    password: str


class UserBase(SQLModel):
    username: str = Field(min_length=2, max_length=20, unique=True)
    email: EmailStr = Field(unique=True)
    phone: str = Field(regex="^\d{10}$", unique=True)
    f_name: str
    l_name: str


class UserCreate(UserBase):
    password: str = Field(regex="^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+*&^_]).{8,}$")


class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, regex="^\d{10}$")
    f_name: Optional[str] = None
    l_name: Optional[str] = None
    password: Optional[str] = Field(
        default=None, regex="^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+*&^_]).{8,}$"
    )


class UserResetPass(SQLModel):
    new_password: str = Body(
        regex="^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+*&^_]).{8,}$"
    )
    verify_password: str = Body(
        regex="^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+*&^_]).{8,}$"
    )


class FriendLink(SQLModel, table=True):
    __tablename__ = "friends"
    user_id: str = Field(foreign_key="users.id", primary_key=True)
    friend_id: str = Field(foreign_key="users.id", primary_key=True)


class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[str] = Field(primary_key=True)
    password: str
    email_confirmed: bool = Field(default=False)

    scopes: Optional[List["Scope"]] = Relationship(
        back_populates="users",
        link_model=UserScopeLink,
        sa_relationship_kwargs=dict(lazy="joined"),
    )

    cards: List["Card"] = Relationship(
        back_populates="users",
        link_model=UserCardLink,
    )

    wallets: List["Wallet"] = Relationship(
        back_populates="users",
        link_model=UserWalletLink,
    )

    friends: List["User"] = Relationship(
        back_populates="friends",
        link_model=FriendLink,
        sa_relationship_kwargs={
            "primaryjoin": "User.id==FriendLink.user_id",
            "secondaryjoin": "User.id==FriendLink.friend_id",
        },
    )

    # 'lazy':"joined" can be added here
    # avatar: Optional[str] = None