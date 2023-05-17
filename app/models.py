from __future__ import annotations
from pydantic import BaseModel, EmailStr, constr
from currencies import Currency
from datetime import datetime
from sqlalchemy import Column, DateTime, Float, String, Integer, select, ForeignKey
from sqlalchemy.orm import Session, declarative_base


base_orm = declarative_base()


class UserORM(base_orm):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    f_name = Column(String)
    l_name = Column(String)


class User(BaseModel):
    id: str | None
    username: constr(min_length=2, max_length=20)
    email: EmailStr
    phone: constr(regex="^\d{10}$")
    f_name: str
    l_name: str
    wallets: list[Wallet] = []
    cards: list[Card] = []
    contacts: list[UserPermission] = []
    avatar: str | None = None

    class Config:
        orm_mode = True


class UserRegistration(User):
    password: constr(regex="^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+*&^_]).{8,}$")


class UserPermission(User):
    password: str
    scopes: list[str] = ["user"]
    email_confirmed: bool = False

    @property
    def is_admin(self):
        if "admin" in self.scopes:
            return True
        return False

    class Config:
        orm_mode = True


class WalletORM(base_orm):
    __tablename__ = "wallets"
    id = Column(String, primary_key=True)
    owner_id = Column(String)
    currency = Column(String)
    balance = Column(Float)


class Wallet(BaseModel):
    id: str | None
    owner: UserPermission | None
    currency: str  # Currency
    balance: float

    class Config:
        orm_mode = True


class JointWallet(Wallet):
    users: list[UserPermission] = []


class CardORM(base_orm):
    __tablename__ = "cards"
    id = Column(String, primary_key=True)
    number = Column(String, unique=True)
    expiry = Column(DateTime)
    holder = Column(String)
    cvc = Column(String)


class Card(BaseModel):
    id: str | None
    number: constr(regex="^\d{16}$")
    expiry: datetime
    holder: constr(min_length=2, max_length=30)
    cvc: constr(regex="^\d{3}$")

    class Config:
        orm_mode = True


class TransactionORM(base_orm):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True)
    wallet_sender = Column(String)
    card_sender = Column(String)
    wallet_receiver = Column(String)
    currency = Column(String)
    amount = Column(Float)
    status = Column(String)


class Transaction(BaseModel):
    id: str | None
    wallet_sender: str | None
    card_sender: str | None
    wallet_receiver: str
    currency: str  # Currency
    amount: float
    status: constr(regex="^pending|success|cancelled$")

    class Config:
        orm_mode = True
