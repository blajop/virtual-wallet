import random
import string
from typing import Dict

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.models.scope import Scope
from app.models.user import User, UserCreate
from app.models.wallet import Wallet, WalletCreate
from app.utils import util_id


def random_lower_string(k) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=k))


def random_phone() -> str:
    return "".join(random.choices(string.digits, k=10))


def random_email() -> str:
    return f"{random_lower_string(10)}@{random_lower_string(6)}.com"


def random_user(db: Session) -> User:
    user = UserCreate(
        username=random_lower_string(8),
        email=random_email(),
        phone=random_phone(),
        f_name=random_lower_string(8),
        l_name=random_lower_string(8),
        password="Passw0rd_1",
    )

    user = User.from_orm(user)
    user.id = util_id.generate_id()
    scope = db.exec(select(Scope).where(Scope.id == 2)).first()
    user.scopes.append(scope)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def random_wallet(
    owner: User, currency: str, balance: int = 200, *, db: Session
) -> Wallet:
    wallet = WalletCreate(
        currency=currency,
    )
    wallet = Wallet.from_orm(wallet)
    wallet.id = util_id.generate_id()
    wallet.owner = owner
    wallet.owner_id = owner.id

    db.add(wallet)
    db.commit()
    db.refresh(wallet)
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
