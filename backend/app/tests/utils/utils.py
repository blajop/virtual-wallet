from datetime import datetime
import random
import string
from typing import Dict

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.models.card import CardCreate, CardExpiry
from app.models.scope import Scope
from app.models.user import User, UserCreate
from app.models.wallet import Wallet, WalletCreate
from app.utils import util_id
from fastapi.encoders import jsonable_encoder
from app.core.security import get_password_hash


def random_lower_string(k) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=k))


def random_phone() -> str:
    return "".join(random.choices(string.digits, k=10))


def random_cardnum() -> str:
    return "".join(random.choices(string.digits, k=16))


def random_email() -> str:
    return f"{random_lower_string(10)}@{random_lower_string(6)}.com"


def random_card() -> CardCreate:
    curr_year = datetime.now().year

    card = CardCreate(
        number=random_cardnum(),
        expiry=jsonable_encoder(CardExpiry(mm="09", yyyy=str(curr_year + 1))),
        holder="User Userov",
        cvc="345",
    )
    return card


def random_usercreate() -> UserCreate:
    user = UserCreate(
        username=random_lower_string(8),
        email=random_email(),
        phone=random_phone(),
        f_name=random_lower_string(8),
        l_name=random_lower_string(8),
        password="Passw0rd_1",
    )

    return user


def random_usermodel() -> User:
    user = User(
        id=util_id.generate_id(),
        username=random_lower_string(8),
        email=random_email(),
        phone=random_phone(),
        f_name=random_lower_string(8),
        l_name=random_lower_string(8),
        password=get_password_hash("Passw0rd_1"),
    )

    return user


def random_admin() -> UserCreate:
    user = UserCreate(
        username=random_lower_string(8),
        email=random_email(),
        phone=random_phone(),
        f_name=random_lower_string(8),
        l_name=random_lower_string(8),
        password="Passw0rd_1",
    )

    return user


def random_wallet(owner: User, currency: str, balance: int = 200) -> Wallet:
    wallet = WalletCreate(
        currency=currency,
    )
    wallet = Wallet.from_orm(wallet)
    wallet.id = util_id.generate_id()
    wallet.owner = owner
    wallet.balance = balance
    # wallet.owner_id = owner.id

    return wallet


# def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
#     login_data = {
#         "username": "stanim",
#         "password": "Stanislav_1",
#     }
#     r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
#     tokens = r.json()
#     a_token = tokens["access_token"]
#     headers = {"Authorization": f"Bearer {a_token}"}
#     return headers
