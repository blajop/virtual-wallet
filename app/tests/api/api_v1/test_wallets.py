import pytest
import copy
from fastapi import HTTPException, Response
from sqlmodel import Session, select
from app.api import deps
from app.api.api_v1.endpoints import wallets
from app.models.scope import Scope
from app.models.user import User, UserCreate
from app import crud
from app.models.wallet import Wallet, WalletCreate
from app.tests.utils.utils import random_user, random_wallet
from fastapi.testclient import TestClient
from main import app
from fastapi.encoders import jsonable_encoder as js
from app.utils import util_id


# CREATE AND GET WALLETS
def test_create_wallets(client: TestClient, user, admin, session: Session):
    app.dependency_overrides[deps.get_current_user] = user
    user1: User = user()
    user2: User = User.from_orm(random_user())

    # Add another user for testing purposes
    user2.id = util_id.generate_id()
    scope = session.exec(select(Scope).where(Scope.id == 2)).first()
    user2.scopes.append(scope)
    session.add(user2)
    session.commit()
    session.refresh(user2)

    # Create the wallets to be added
    wallet1 = WalletCreate(currency="USD")
    wallet2 = WalletCreate(currency="BGN")

    # Successfully create 2 wallets
    response = client.post(f"/api/v1/users/{user1.username}/wallets", json=js(wallet1))
    response = client.post(f"/api/v1/users/{user1.username}/wallets", json=js(wallet2))
    assert response.status_code == 200

    # Get the added wallets
    response = client.get(f"/api/v1/users/{user1.username}/wallets")
    content = response.json()
    assert response.status_code == 200
    assert len(content) == 2
    for w in content:
        assert w["currency"] in (wallet1.currency, wallet2.currency)

    # Try to create wallets for another user
    response = client.post(f"/api/v1/users/{user2.username}/wallets", json=js(wallet1))
    assert response.status_code == 403

    # Try to get other users wallets
    app.dependency_overrides[deps.get_current_user] = lambda: user2
    response = client.get(f"/api/v1/users/{user1.username}/wallets")
    assert response.status_code == 403


# INVITE AND GET WALLET LEECHES
def test_create_get_wallet_leech(client: TestClient, user, session: Session):
    app.dependency_overrides[deps.get_current_user] = user
    user1: User = user()
    wallet: Wallet = random_wallet(user1, "BGN", db=session)

    leech: User = User.from_orm(random_user())

    # Create leech user
    leech.id = util_id.generate_id()
    scope = session.exec(select(Scope).where(Scope.id == 2)).first()
    leech.scopes.append(scope)
    session.add(leech)
    session.commit()
    session.refresh(leech)

    # Add leech to wallet
    response = client.post(
        f"/api/v1/users/{user1.username}/wallets/{wallet.id}/leeches?leech={leech.username}"
    )
    assert response.status_code == 200
    assert leech.username in [
        obj.get("username") for obj in response.json().get("users")
    ]

    # Get wallet leeches
    response = client.get(f"/api/v1/users/{user1.username}/wallets/{wallet.id}/leeches")
    content = response.json()
    assert response.status_code == 200
    assert leech in [User(**o) for o in content]
