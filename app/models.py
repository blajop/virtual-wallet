from __future__ import annotations
from pydantic import BaseModel, EmailStr, constr
from currencies import Currency
from datetime import datetime


class UserSchema(BaseModel):
    id: int | None
    first_name: str
    last_name: str
    username: constr(min_length=2, max_length=20)
    email: EmailStr
    phone_num: constr(regex='^\d{10}$')
    wallets: list[Wallet] = []
    cards: list[Card] = []
    contacts: list[UserPermissionsSchema] = []
    avatar: str | None = None

    @classmethod
    def from_query_result(cls, id, first_name, last_name, username, email, password, 
                          phone_num, wallets, cards, contacts, avatar):
        return cls(id=id, first_name=first_name, last_name=last_name, username=username, email=email,
                   phone_num=phone_num, wallets=wallets, cards=cards, contacts=contacts, avatar=avatar)

class RegisterSchema(UserSchema):
    password: constr(regex='^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+*&^_]).{8,}$')

class UserPermissionsSchema(UserSchema):
    password: str                 
    scopes: list[str] = ['user']
    email_confirmed: bool = False

    @classmethod
    def from_query_result(cls, id, first_name, last_name, username, email, scopes, password):
        pass

    @property
    def is_admin(self):
        if 'admin' in self.scopes:
            return True
        return False
    


class Wallet(BaseModel):
    id: int | None
    owner: UserPermissionsSchema
    currency: Currency
    balance: float


class JointWallet(Wallet):
    users: list[UserPermissionsSchema]


class Card(BaseModel):
    id: int | None
    number: constr(regex='^\d{16}$')
    expiry: datetime    # ??
    holder: constr(min_length=2, max_length=30)
    cvc: constr(regex='^\d{3}$')
    