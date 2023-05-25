from unittest.mock import Mock
from fastapi import HTTPException
import pytest
from app.api.api_v1.endpoints import cards
from app.models.transaction import Transaction, TransactionCreate
from sqlmodel import Session, select
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app import utils
from fastapi.encoders import jsonable_encoder
from app import deps
from app.tests.utils.utils import random_usermodel, random_wallet
from main import app

from app.models.user import User

# TEST POST ------------------------------------


# TEST GET ------------------------------------


def test_get_transaction_returns404_when_notExistingTransaction(
    client: TestClient, user
):
    transaction_id = utils.util_id.generate_id()
    app.dependency_overrides[deps.get_current_user] = user
    response = client.get(f"/api/v1/transactions/{transaction_id}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "There is no such transaction within your access"


def test_get_transaction_returnsTransaction_when_existingAndUserIsSenderWalletOwner(
    session: Session, client: TestClient, user, admin
):
    # Arrange
    wallet_s = random_wallet(user(), "BGN")
    wallet_r = random_wallet(admin(), "EUR")
    session.add_all([wallet_s, wallet_r])

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        currency="BGN",
        amount=120,
    )

    app.dependency_overrides[deps.get_current_user] = user
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_1))
    data = response.json()
    transaction_1_id = data["id"]

    # Act
    response = client.get(f"/api/v1/transactions/{transaction_1_id}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["id"] == transaction_1_id
    assert data["wallet_sender"] == wallet_s.id
    assert data["wallet_receiver"] == wallet_r.id
    assert data["currency"] == "BGN"
    assert data["amount"] == 120
    assert data["recurring"] == None
    assert data["status"] == "pending"


def test_get_transaction_returnsTransaction_when_existingAndUserIsReceiverWalletOwner(
    session: Session, client: TestClient, user, admin
):
    # Arrange
    wallet_s = random_wallet(admin(), "BGN")
    wallet_r = random_wallet(user(), "EUR")
    session.add_all([wallet_s, wallet_r])

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        currency="BGN",
        amount=120,
    )

    app.dependency_overrides[deps.get_current_user] = admin
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_1))
    data = response.json()
    transaction_1_id = data["id"]

    app.dependency_overrides[deps.get_current_user] = user
    # Act
    response = client.get(f"/api/v1/transactions/{transaction_1_id}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["id"] == transaction_1_id
    assert data["wallet_sender"] == wallet_s.id
    assert data["wallet_receiver"] == wallet_r.id
    assert data["currency"] == "BGN"
    assert data["amount"] == 120
    assert data["recurring"] == None
    assert data["status"] == "pending"


def test_get_transaction_returnsTransaction_when_existingAndUserIsReceiverWalletParticipant(
    session: Session, client: TestClient, user, admin
):
    # Arrange
    owner_wallet_2 = random_usermodel()
    session.add(owner_wallet_2)

    wallet_s = random_wallet(admin(), "BGN")
    wallet_r = random_wallet(owner_wallet_2, "EUR")
    wallet_r.users.append(user())

    session.add_all([wallet_s, wallet_r])

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        currency="BGN",
        amount=120,
    )

    app.dependency_overrides[deps.get_current_user] = admin
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_1))
    data = response.json()
    transaction_1_id = data["id"]

    app.dependency_overrides[deps.get_current_user] = user
    # Act
    response = client.get(f"/api/v1/transactions/{transaction_1_id}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["id"] == transaction_1_id
    assert data["wallet_sender"] == wallet_s.id
    assert data["wallet_receiver"] == wallet_r.id
    assert data["currency"] == "BGN"
    assert data["amount"] == 120
    assert data["recurring"] == None
    assert data["status"] == "pending"
