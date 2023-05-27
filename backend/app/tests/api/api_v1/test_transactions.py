from unittest.mock import Mock
from fastapi import HTTPException
from httpx import QueryParams
import pytest
from app.api.api_v1.endpoints import cards
from app.models.card import Card
from app.models.currency import Currency
from app.models.transaction import Transaction, TransactionCreate
from sqlmodel import Session, select
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app import utils
from fastapi.encoders import jsonable_encoder
from app import deps
from app.tests.utils.utils import random_usermodel, random_wallet, random_card
from main import app

from app.models.user import User

# TEST POST ------------------------------------


def test_post_transaction_returns400_when_senderWalletNotInUsersWalls(
    session: Session, client: TestClient, admin, user
):
    # Arrange
    wallet_s = random_wallet(user(), "BGN")
    wallet_r = random_wallet(admin(), "EUR")
    user_3 = random_usermodel()
    user_4 = random_usermodel()
    session.add_all([wallet_s, wallet_r, user_3, user_4])

    app.dependency_overrides[deps.get_current_user] = user
    app.dependency_overrides[deps.get_user_from_path] = user

    client.post(
        f"/api/v1/users/{user().id}/wallets/{wallet_s.id}/leeches?leech={user_3.id}"
    )
    assert len(wallet_s.users) == 1

    app.dependency_overrides[deps.get_current_user] = lambda: user_4
    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        currency="BGN",
        amount=120,
    )

    # Act
    response = client.post(
        f"/api/v1/transactions", json=jsonable_encoder(transaction_1)
    )
    data = response.json()
    assert response.status_code == 400
    assert (
        data["detail"] == "The wallet sender passed is not in your associated wallets"
    )


def test_post_transaction_returns400_when_notEnoughAmountSameCurr(
    session: Session, client: TestClient, admin, user
):
    # Arrange
    wallet_s = random_wallet(user(), "BGN", balance=100)
    wallet_r = random_wallet(admin(), "BGN")

    session.add_all([wallet_s, wallet_r])

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        currency="BGN",
        amount=120,
    )

    app.dependency_overrides[deps.get_current_user] = user
    # Act
    response = client.post(
        f"/api/v1/transactions", json=jsonable_encoder(transaction_1)
    )
    data = response.json()
    assert response.status_code == 400
    assert (
        data["detail"]
        == "You do not have enough balance in the sender Wallet in order to make the transfer"
    )


def test_post_transaction_returns400_when_senderCardNotInUsersCards(
    session: Session, client: TestClient, admin, user
):
    # Arrange
    card_s = random_card()
    wallet_r = random_wallet(admin(), "EUR")
    session.add(wallet_r)

    app.dependency_overrides[deps.get_current_user] = admin
    client.post("/api/v1/cards", json=jsonable_encoder(card_s))

    card_inDB: Card = session.exec(
        select(Card).filter(Card.number == utils.util_crypt.encrypt(card_s.number))
    ).first()
    assert len(card_inDB.users) == 1
    card_db_id = card_inDB.id

    app.dependency_overrides[deps.get_current_user] = user
    transaction_1 = TransactionCreate(
        card_sender=card_db_id,
        wallet_receiver=wallet_r.id,
        currency="BGN",
        amount=120,
    )


def test_post_transaction_returns400_when_senderCardInUsersCardsButWallerReceiverNotUsers(
    session: Session, client: TestClient, admin, user
):
    # Arrange
    card_s = random_card()
    wallet_r = random_wallet(admin(), "EUR")
    session.add(wallet_r)

    app.dependency_overrides[deps.get_current_user] = user
    client.post("/api/v1/cards", json=jsonable_encoder(card_s))

    card_inDB: Card = session.exec(
        select(Card).filter(Card.number == utils.util_crypt.encrypt(card_s.number))
    ).first()
    assert len(card_inDB.users) == 1
    card_db_id = card_inDB.id

    transaction_1 = TransactionCreate(
        card_sender=card_db_id,
        wallet_receiver=wallet_r.id,
        currency="BGN",
        amount=120,
    )
    # Act
    response = client.post(
        f"/api/v1/transactions", json=jsonable_encoder(transaction_1)
    )
    data = response.json()
    assert response.status_code == 400
    assert (
        data["detail"]
        == "You can't deposit money to a wallet not connected with your acoount"
    )


def test_post_transaction_returns400_when_senRecItemsPassedIncorrectly(
    session: Session, client: TestClient, user, admin
):
    # Arrange
    card_s = random_card()
    wallet_s = random_wallet(user(), "BGN")
    wallet_r = random_wallet(admin(), "BGN")
    session.add_all([wallet_s, wallet_r])

    app.dependency_overrides[deps.get_current_user] = user
    client.post("/api/v1/cards", json=jsonable_encoder(card_s))

    card_inDB: Card = session.exec(
        select(Card).filter(Card.number == utils.util_crypt.encrypt(card_s.number))
    ).first()
    card_db_id = card_inDB.id

    # Should fail with both params passed
    transaction_1 = TransactionCreate(
        card_sender=card_db_id,
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        currency="BGN",
        amount=120,
    )

    # Act
    response = client.post(
        f"/api/v1/transactions", json=jsonable_encoder(transaction_1)
    )
    data = response.json()
    assert response.status_code == 400
    assert data["detail"] == "You should pass either valid wallet or valid card sender"

    # Should fail with both params passed
    transaction_2 = TransactionCreate(
        wallet_receiver=wallet_r.id,
        currency="BGN",
        amount=120,
    )
    # Act
    response = client.post(
        f"/api/v1/transactions", json=jsonable_encoder(transaction_2)
    )
    data = response.json()
    assert response.status_code == 400
    assert data["detail"] == "You should pass either valid wallet or valid card sender"

    # Should fail with same wallet_s & wallet_r passed
    transaction_3 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_s.id,
        currency="BGN",
        amount=120,
    )
    # Act
    response = client.post(
        f"/api/v1/transactions", json=jsonable_encoder(transaction_3)
    )
    data = response.json()
    assert response.status_code == 400
    assert data["detail"] == "The sender and receiver wallets are the same"


# TRANSACTION ACCEPT & FINALIZATION - WALLET TO WALLET WITH EXCHANGE


def test_postAndConfirm_transaction_work_when_allOkWithCrossExchange(
    session: Session, client: TestClient, user, admin
):
    # Arrange
    currency_EUR = Currency(currency="EUR", rate=0.9)
    currency_BGN = Currency(currency="BGN", rate=1.8)
    currency_USD = Currency(currency="USD", rate=1)
    wallet_s = random_wallet(user(), "BGN", balance=100)
    wallet_r = random_wallet(admin(), "EUR", balance=100)
    session.add_all([wallet_s, wallet_r, currency_EUR, currency_BGN, currency_USD])

    app.dependency_overrides[deps.get_current_user] = user

    # Should fail with both params passed
    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        currency="USD",
        amount=50,
    )

    # Create the transaction
    response = client.post(
        f"/api/v1/transactions", json=jsonable_encoder(transaction_1)
    )
    data = response.json()
    assert data["sending_user"] == user().id
    assert data["wallet_sender"] == wallet_s.id
    assert data["wallet_receiver"] == wallet_r.id
    assert data["currency"] == transaction_1.currency
    assert data["amount"] == transaction_1.amount
    assert data["recurring"] == None
    assert data["detail"] == None
    assert data["status"] == "pending"
    transaction_id = data["id"]

    transaction_inDB: Transaction = session.exec(
        select(Transaction).filter(Transaction.id == transaction_id)
    ).first()
    assert transaction_inDB.id != None
    assert transaction_inDB.status == "pending"

    # Act - confirm the transaction
    response = client.put(f"/api/v1/transactions/{transaction_id}/confirm")
    data = response.json()
    assert response.status_code == 200

    transaction_inDB: Transaction = session.exec(
        select(Transaction).filter(Transaction.id == transaction_id)
    ).first()
    assert transaction_inDB.status == "success"

    assert wallet_s.balance == 10.0
    assert wallet_r.balance == 145.0


def test_confirm_transaction_returns404_when_noSuchTransaction(
    client: TestClient, user
):
    app.dependency_overrides[deps.get_current_user] = user

    # Act - confirm the transaction
    response = client.put("/api/v1/transactions/7067750323622031361/confirm")

    assert response.status_code == 404


# TEST GET ------------------------------------


def test_get_transaction_returns404_when_notExistingTransaction(
    session: Session, client: TestClient, admin, user
):
    app.dependency_overrides[deps.get_current_user] = user

    transaction_id = utils.util_id.generate_id()
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
        sending_user=wallet_s.owner.id,
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
    assert data["sending_user"] == wallet_s.owner.id
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
        sending_user=wallet_s.owner.id,
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
    assert data["sending_user"] == wallet_s.owner.id
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
        sending_user=wallet_s.owner.id,
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
    assert data["sending_user"] == wallet_s.owner.id
    assert data["wallet_sender"] == wallet_s.id
    assert data["wallet_receiver"] == wallet_r.id
    assert data["currency"] == "BGN"
    assert data["amount"] == 120
    assert data["recurring"] == None
    assert data["status"] == "pending"
