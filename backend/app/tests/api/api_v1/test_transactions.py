from unittest.mock import Mock
from fastapi import HTTPException
from fastapi_pagination import Params, add_pagination
import fastapi_pagination
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


def datetime_to_str(time: datetime):
    return time.strftime("%Y-%m-%dT%H:%M:%S.000000")


# TEST POST ------------------------------------


def test_post_transaction_returns400_when_senderWalletNotInUsersWalls(
    session: Session, client: TestClient, admin, user
):
    # Arrange
    wallet_s = random_wallet(user(), "BGN")
    wallet_r = random_wallet(admin(), "BGN")
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
        receiving_user=admin().id,
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
        receiving_user=admin().id,
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
    wallet_r = random_wallet(admin(), "BGN")
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
        receiving_user=admin().id,
        wallet_receiver=wallet_r.id,
        currency="BGN",
        amount=120,
    )


def test_post_transaction_returns400_when_senderCardInUsersCardsButWalletReceiverNotUsers(
    session: Session, client: TestClient, admin, user
):
    # Arrange
    card_s = random_card()
    wallet_r = random_wallet(admin(), "BGN")
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
        receiving_user=admin().id,
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
        receiving_user=admin().id,
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

    # Should fail neither of the params passed
    transaction_2 = TransactionCreate(
        wallet_receiver=wallet_r.id,
        receiving_user=admin().id,
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

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        receiving_user=admin().id,
        currency="USD",
        amount=50,
    )

    # Create the transaction
    app.dependency_overrides[deps.get_current_user] = user
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
    token_transaction = utils.util_mail.generate_id_link_token(transaction_id)
    token_recipient = utils.util_mail.generate_id_link_token(admin().id)
    confirmation_link = (
        f"/api/v1/transactions/{token_transaction}/confirm/{token_recipient}"
    )

    app.dependency_overrides[deps.get_current_user] = admin
    response = client.get(confirmation_link)
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

    transaction_id = utils.util_id.generate_id()

    # Act - confirm the transaction
    response = client.put(f"/api/v1/transactions/{transaction_id}/confirm")

    assert response.status_code == 404


def test_confirm_transaction_returns400_when_transactionAlreadyConfirmed(
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

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        receiving_user=admin().id,
        currency="BGN",
        amount=50,
    )

    # Create the transaction
    response = client.post(
        f"/api/v1/transactions", json=jsonable_encoder(transaction_1)
    )
    transaction_id = response.json()["id"]

    app.dependency_overrides[deps.get_current_user] = admin
    # Confirm it once and update the status to 'success'
    token_transaction = utils.util_mail.generate_id_link_token(transaction_id)
    token_recipient = utils.util_mail.generate_id_link_token(admin().id)
    confirmation_link = (
        f"/api/v1/transactions/{token_transaction}/confirm/{token_recipient}"
    )
    response = client.get(confirmation_link)
    data = response.json()
    assert response.status_code == 200

    # Confirm it again and 400 should be returned
    response = client.get(confirmation_link)
    data = response.json()
    assert response.status_code == 400
    assert data["detail"] == "Already accepted"


def test_confirm_transaction_returns403_when_confirmationIsAttemptedByNonReceiverUser(
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

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        receiving_user=admin().id,
        currency="BGN",
        amount=50,
    )

    # Create the transaction
    response = client.post(
        f"/api/v1/transactions", json=jsonable_encoder(transaction_1)
    )
    transaction_id = response.json()["id"]

    # Confirm it by non-receiving user and 403 should be returned
    token_transaction = utils.util_mail.generate_id_link_token(transaction_id)
    token_recipient = utils.util_mail.generate_id_link_token(user().id)
    confirmation_link = (
        f"/api/v1/transactions/{token_transaction}/confirm/{token_recipient}"
    )
    response = client.get(confirmation_link)
    data = response.json()
    assert response.status_code == 403
    assert (
        data["detail"]
        == "You are not the receiver of the transaction and cannot confirm it"
    )


def test_decline_transaction_works_when_allOk(
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

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        receiving_user=admin().id,
        currency="BGN",
        amount=50,
    )

    # Create the transaction
    response = client.post(
        f"/api/v1/transactions", json=jsonable_encoder(transaction_1)
    )
    transaction_id = response.json()["id"]

    # Act
    token_transaction = utils.util_mail.generate_id_link_token(transaction_id)
    token_recipient = utils.util_mail.generate_id_link_token(admin().id)
    confirmation_link = (
        f"/api/v1/transactions/{token_transaction}/decline/{token_recipient}"
    )
    response = client.get(confirmation_link)
    data = response.json()
    assert response.status_code == 200

    transaction_inDB: Transaction = session.exec(
        select(Transaction).filter(Transaction.id == transaction_id)
    ).first()
    assert transaction_inDB.status == "declined"


def test_decline_transaction_returns403_when_AttemptedByNonReceiverUser(
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

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        receiving_user=admin().id,
        currency="BGN",
        amount=50,
    )

    # Create the transaction
    response = client.post(
        f"/api/v1/transactions", json=jsonable_encoder(transaction_1)
    )
    transaction_id = response.json()["id"]

    # Confirm it by non-receiving user and 403 should be returned
    token_transaction = utils.util_mail.generate_id_link_token(transaction_id)
    token_recipient = utils.util_mail.generate_id_link_token(user().id)
    confirmation_link = (
        f"/api/v1/transactions/{token_transaction}/decline/{token_recipient}"
    )
    response = client.get(confirmation_link)
    data = response.json()
    assert response.status_code == 403
    assert (
        data["detail"]
        == "You are not the receiver of the transaction and cannot decline it"
    )


# TEST GET-ONE ------------------------------------


def test_get_transaction_returns404_when_notExistingTransaction(
    client: TestClient, user
):
    app.dependency_overrides[deps.get_current_user] = user

    transaction_id = utils.util_id.generate_id()
    response = client.get(f"/api/v1/transactions/{transaction_id}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "There is no such transaction within your access"


def test_get_transaction_returnsTransaction_when_existingAndUserIsSender(
    session: Session, client: TestClient, user, admin
):
    # Arrange
    wallet_s = random_wallet(user(), "BGN")
    wallet_r = random_wallet(admin(), "BGN")
    session.add_all([wallet_s, wallet_r])

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        receiving_user=admin().id,
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
    assert data["sending_user"] == user().id
    assert data["wallet_sender"] == wallet_s.id
    assert data["wallet_receiver"] == wallet_r.id
    assert data["currency"] == "BGN"
    assert data["amount"] == 120
    assert data["recurring"] == None
    assert data["status"] == "pending"


def test_get_transaction_returnsTransaction_when_existingAndUserIsOwnerReceiverWallet(
    session: Session, client: TestClient, user, admin
):
    # Arrange
    wallet_s = random_wallet(admin(), "BGN")
    wallet_r = random_wallet(user(), "BGN")
    session.add_all([wallet_s, wallet_r])

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        receiving_user=user().id,
        currency="BGN",
        amount=120,
    )

    app.dependency_overrides[deps.get_current_user] = admin
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_1))
    data = response.json()
    transaction_1_id = data["id"]

    # Act
    app.dependency_overrides[deps.get_current_user] = user
    response = client.get(f"/api/v1/transactions/{transaction_1_id}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["id"] == transaction_1_id


def test_get_transaction_returnsTransaction_when_existingAndUserIsParticipantInReceiverWallet(
    session: Session, client: TestClient, user, admin
):
    # Arrange
    wallet_s = random_wallet(admin(), "BGN")
    wallet_r = random_wallet(user(), "BGN")
    user_3 = random_usermodel()
    session.add_all([wallet_s, wallet_r, user_3])

    app.dependency_overrides[deps.get_current_user] = user
    client.post(
        f"/api/v1/users/{user().id}/wallets/{wallet_r.id}/leeches?leech={user_3.id}"
    )
    assert len(wallet_r.users) == 1

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        receiving_user=user().id,
        currency="BGN",
        amount=120,
    )

    app.dependency_overrides[deps.get_current_user] = admin
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_1))

    data = response.json()
    transaction_1_id = data["id"]

    # Act
    app.dependency_overrides[deps.get_current_user] = lambda: user_3
    response = client.get(f"/api/v1/transactions/{transaction_1_id}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["id"] == transaction_1_id


def test_get_transaction_returns404_when_existingAndUserNotAssociated(
    session: Session, client: TestClient, user, admin
):
    # Arrange
    user_3 = random_usermodel()
    wallet_s = random_wallet(user(), "BGN")
    wallet_r = random_wallet(user_3, "BGN")
    session.add_all([wallet_s, wallet_r, user_3])

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        receiving_user=user_3.id,
        currency="BGN",
        amount=120,
    )

    app.dependency_overrides[deps.get_current_user] = user
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_1))
    data = response.json()
    transaction_1_id = data["id"]

    # Act
    app.dependency_overrides[deps.get_current_user] = admin
    response = client.get(f"/api/v1/transactions/{transaction_1_id}")
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == "There is no such transaction within your access"


def test_get_transaction_returnsTransaction_when_notAssociatedAndViaAdminPanel(
    session: Session, client: TestClient, user, admin
):
    # Arrange
    user_3 = random_usermodel()
    wallet_s = random_wallet(user(), "BGN")
    wallet_r = random_wallet(user_3, "BGN")
    session.add_all([wallet_s, wallet_r, user_3])

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_s.id,
        wallet_receiver=wallet_r.id,
        receiving_user=user_3.id,
        currency="BGN",
        amount=120,
    )

    app.dependency_overrides[deps.get_current_user] = user
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_1))
    data = response.json()
    transaction_1_id = data["id"]

    # Act
    app.dependency_overrides[deps.get_admin] = admin
    response = client.get(f"/api/v1/admin/transactions/{transaction_1_id}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["id"] == transaction_1_id


def test_get_transaction_returns404_when_notExistingTransactionViaAdminPanel(
    session: Session, client: TestClient, user, admin
):
    # Arrange
    user_3 = random_usermodel()
    wallet_s = random_wallet(user(), "BGN")
    wallet_r = random_wallet(user_3, "BGN")
    session.add_all([wallet_s, wallet_r, user_3])

    transaction_1_id = utils.util_id.generate_id()

    # Act
    app.dependency_overrides[deps.get_admin] = admin
    response = client.get(f"/api/v1/admin/transactions/{transaction_1_id}")
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == "There is no such transaction"


# TEST GET-MULTI ------------------------------------

# VIA ADMIN PANEL


def test_get_transactions_showsCorrectly_when_viaAdminPanelSortAmount(
    session: Session, client: TestClient, user, admin
):
    # Arrange
    user_3 = random_usermodel()
    wallet_1 = random_wallet(user(), "BGN")
    wallet_2 = random_wallet(admin(), "BGN")
    wallet_3 = random_wallet(user_3, "BGN")
    session.add_all([wallet_1, wallet_2, wallet_3, user_3])

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_1.id,
        wallet_receiver=wallet_2.id,
        receiving_user=admin().id,
        currency="BGN",
        amount=5,
    )
    app.dependency_overrides[deps.get_current_user] = user
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_1))
    data = response.json()
    transaction_1_id = data["id"]

    transaction_2 = TransactionCreate(
        wallet_sender=wallet_2.id,
        wallet_receiver=wallet_1.id,
        receiving_user=user().id,
        currency="BGN",
        amount=10,
    )
    app.dependency_overrides[deps.get_current_user] = admin
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_2))
    data = response.json()
    transaction_2_id = data["id"]

    transaction_3 = TransactionCreate(
        wallet_sender=wallet_3.id,
        wallet_receiver=wallet_2.id,
        receiving_user=admin().id,
        currency="BGN",
        amount=20,
    )
    app.dependency_overrides[deps.get_current_user] = lambda: user_3
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_3))
    data = response.json()
    transaction_3_id = data["id"]

    transaction_4 = TransactionCreate(
        wallet_sender=wallet_1.id,
        wallet_receiver=wallet_3.id,
        receiving_user=user_3.id,
        currency="BGN",
        amount=30,
    )
    app.dependency_overrides[deps.get_current_user] = user
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_4))
    data = response.json()
    transaction_4_id = data["id"]

    # TEST THE SORT_BY AMOUNT AND ASC & DESC
    # Act 1
    app.dependency_overrides[deps.get_admin] = admin
    params = Params(page=1, size=100)
    app.dependency_overrides[Params] = lambda: params

    response = client.get(
        "/api/v1/admin/transactions",
        params=QueryParams(
            {
                "from_date": datetime_to_str(datetime.now() - timedelta(minutes=1)),
                "to_date": datetime_to_str(datetime.now() + timedelta(minutes=1)),
                "sort_by": "amount",
            }
        ),
    )
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) == 4
    assert data[0]["id"] == transaction_1_id
    assert data[1]["id"] == transaction_2_id
    assert data[2]["id"] == transaction_3_id
    assert data[3]["id"] == transaction_4_id

    # Act 2
    app.dependency_overrides[deps.get_admin] = admin
    app.dependency_overrides[add_pagination] = add_pagination

    response = client.get(
        "/api/v1/admin/transactions",
        params=QueryParams(
            {
                "from_date": datetime_to_str(datetime.now() - timedelta(minutes=1)),
                "to_date": datetime_to_str(datetime.now() + timedelta(minutes=1)),
                "sort_by": "amount",
                "sort": "desc",
                "page": 1,
                "size": 100,
            }
        ),
    )
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) == 4
    assert data[0]["id"] == transaction_4_id
    assert data[1]["id"] == transaction_3_id
    assert data[2]["id"] == transaction_2_id
    assert data[3]["id"] == transaction_1_id


def test_get_transactions_showsCorrectly_when_viaAdminPanelRecipientFilter(
    session: Session, client: TestClient, user, admin, monkeypatch
):
    # Arrange
    user_3 = random_usermodel()
    wallet_1 = random_wallet(user(), "BGN")
    wallet_2 = random_wallet(admin(), "BGN")
    wallet_3 = random_wallet(user_3, "BGN")
    session.add_all([wallet_1, wallet_2, wallet_3, user_3])

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_1.id,
        wallet_receiver=wallet_2.id,
        receiving_user=admin().id,
        currency="BGN",
        amount=5,
    )
    app.dependency_overrides[deps.get_current_user] = user
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_1))
    data = response.json()
    transaction_1_id = data["id"]

    transaction_2 = TransactionCreate(
        wallet_sender=wallet_2.id,
        wallet_receiver=wallet_1.id,
        receiving_user=user().id,
        currency="BGN",
        amount=10,
    )
    app.dependency_overrides[deps.get_current_user] = admin
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_2))
    data = response.json()
    transaction_2_id = data["id"]

    transaction_3 = TransactionCreate(
        wallet_sender=wallet_3.id,
        wallet_receiver=wallet_2.id,
        receiving_user=admin().id,
        currency="BGN",
        amount=20,
    )
    app.dependency_overrides[deps.get_current_user] = lambda: user_3
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_3))
    data = response.json()
    transaction_3_id = data["id"]

    transaction_4 = TransactionCreate(
        wallet_sender=wallet_1.id,
        wallet_receiver=wallet_3.id,
        receiving_user=user_3.id,
        currency="BGN",
        amount=30,
    )
    app.dependency_overrides[deps.get_current_user] = user
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_4))
    data = response.json()
    transaction_4_id = data["id"]

    # TEST THE SORT_BY AMOUNT AND ASC & DESC
    # Act
    app.dependency_overrides[deps.get_admin] = admin

    monkeypatch.setattr("fastapi_pagination.Params", lambda: Params(page=1, size=100))

    response = client.get(
        "/api/v1/admin/transactions",
        params={
            "from_date": datetime_to_str(datetime.now() - timedelta(minutes=1)),
            "to_date": datetime_to_str(datetime.now() + timedelta(minutes=1)),
            "sort_by": "amount",
            "recipient": admin().id,
        },
    )
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["id"] == transaction_1_id
    assert data[1]["id"] == transaction_3_id


# VIA ADMIN PANEL WITH USER PARAM


def test_get_transactions_showsCorrectly_when_viaAdminPanelWithUserParam(
    session: Session, client: TestClient, user, admin
):
    # Arrange
    user_3 = random_usermodel()
    wallet_1 = random_wallet(user(), "BGN")
    wallet_2 = random_wallet(admin(), "BGN")
    wallet_3 = random_wallet(user_3, "BGN")
    session.add_all([wallet_1, wallet_2, wallet_3, user_3])

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_1.id,
        wallet_receiver=wallet_2.id,
        receiving_user=admin().id,
        currency="BGN",
        amount=5,
    )
    app.dependency_overrides[deps.get_current_user] = user
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_1))
    data = response.json()
    transaction_1_id = data["id"]

    transaction_2 = TransactionCreate(
        wallet_sender=wallet_2.id,
        wallet_receiver=wallet_1.id,
        receiving_user=user().id,
        currency="BGN",
        amount=10,
    )
    app.dependency_overrides[deps.get_current_user] = admin
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_2))
    data = response.json()
    transaction_2_id = data["id"]

    transaction_3 = TransactionCreate(
        wallet_sender=wallet_3.id,
        wallet_receiver=wallet_2.id,
        receiving_user=admin().id,
        currency="BGN",
        amount=20,
    )
    app.dependency_overrides[deps.get_current_user] = lambda: user_3
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_3))
    data = response.json()
    transaction_3_id = data["id"]

    transaction_4 = TransactionCreate(
        wallet_sender=wallet_1.id,
        wallet_receiver=wallet_3.id,
        receiving_user=user_3.id,
        currency="BGN",
        amount=30,
    )
    app.dependency_overrides[deps.get_current_user] = user
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_4))
    data = response.json()
    transaction_4_id = data["id"]

    # Act
    app.dependency_overrides[deps.get_admin] = admin

    response = client.get(
        "/api/v1/admin/transactions",
        params=QueryParams(
            {
                "from_date": datetime_to_str(datetime.now() - timedelta(minutes=1)),
                "to_date": datetime_to_str(datetime.now() + timedelta(minutes=1)),
                "sort_by": "amount",
                "user": user_3.id,
                "params": Params(page=1, size=100),
            }
        ),
    )
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["id"] == transaction_3_id
    assert data[1]["id"] == transaction_4_id


# VIA USER PANEL


def test_get_transactions_showsCorrectly_when_viaUserPanel(
    session: Session, client: TestClient, user, admin
):
    # Arrange
    user_3 = random_usermodel()
    wallet_1 = random_wallet(user(), "BGN")
    wallet_2 = random_wallet(admin(), "BGN")
    wallet_3 = random_wallet(user_3, "BGN")
    session.add_all([wallet_1, wallet_2, wallet_3, user_3])

    transaction_1 = TransactionCreate(
        wallet_sender=wallet_1.id,
        wallet_receiver=wallet_2.id,
        receiving_user=admin().id,
        currency="BGN",
        amount=5,
    )
    app.dependency_overrides[deps.get_current_user] = user
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_1))
    data = response.json()
    transaction_1_id = data["id"]

    transaction_2 = TransactionCreate(
        wallet_sender=wallet_2.id,
        wallet_receiver=wallet_1.id,
        receiving_user=user().id,
        currency="BGN",
        amount=10,
    )
    app.dependency_overrides[deps.get_current_user] = admin
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_2))
    data = response.json()
    transaction_2_id = data["id"]

    transaction_3 = TransactionCreate(
        wallet_sender=wallet_3.id,
        wallet_receiver=wallet_2.id,
        receiving_user=admin().id,
        currency="BGN",
        amount=20,
    )
    app.dependency_overrides[deps.get_current_user] = lambda: user_3
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_3))
    data = response.json()
    transaction_3_id = data["id"]

    transaction_4 = TransactionCreate(
        wallet_sender=wallet_1.id,
        wallet_receiver=wallet_3.id,
        receiving_user=user_3.id,
        currency="BGN",
        amount=30,
    )
    app.dependency_overrides[deps.get_current_user] = user
    response = client.post("/api/v1/transactions", json=jsonable_encoder(transaction_4))
    data = response.json()
    transaction_4_id = data["id"]

    # Act 1 - USER
    app.dependency_overrides[deps.get_current_user] = user
    params = Params(page=1, size=100)
    app.dependency_overrides[Params] = lambda: params

    response = client.get(
        "/api/v1/transactions",
        params=QueryParams(
            {
                "from_date": datetime_to_str(datetime.now() - timedelta(minutes=1)),
                "to_date": datetime_to_str(datetime.now() + timedelta(minutes=1)),
            }
        ),
    )
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) == 3
    for el in data:
        assert el["id"] in (
            transaction_1_id,
            transaction_2_id,
            transaction_4_id,
        )

    # Add user_3 as leech to wallet_1
    app.dependency_overrides[deps.get_user_from_path] = user
    client.post(
        f"/api/v1/users/{user().id}/wallets/{wallet_1.id}/leeches?leech={user_3.id}"
    )
    assert len(wallet_1.users) == 1

    # Act 2 USER_3
    app.dependency_overrides[deps.get_current_user] = lambda: user_3
    params = Params(page=1, size=100)
    app.dependency_overrides[Params] = add_pagination
    response = client.get(
        "/api/v1/transactions",
        params=QueryParams(
            {
                "from_date": datetime_to_str(datetime.now() - timedelta(minutes=1)),
                "to_date": datetime_to_str(datetime.now() + timedelta(minutes=1)),
                "params": params,
            }
        ),
    )
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) == 3
    for el in data:
        assert el["id"] in (
            transaction_2_id,
            transaction_3_id,
            transaction_4_id,
        )

    # Act 3 - USER_3 OUT
    app.dependency_overrides[deps.get_current_user] = lambda: user_3
    params = Params(page=1, size=100)
    app.dependency_overrides[Params] = add_pagination

    response = client.get(
        "/api/v1/transactions",
        params=QueryParams(
            {
                "from_date": datetime_to_str(datetime.now() - timedelta(minutes=1)),
                "to_date": datetime_to_str(datetime.now() + timedelta(minutes=1)),
                "direction": "out",
                "params": params,
            }
        ),
    )
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) == 1
    for el in data:
        assert el["id"] in (transaction_3_id,)

    # Act 4 - USER_3 IN
    app.dependency_overrides[deps.get_current_user] = lambda: user_3
    params = Params(page=1, size=100)
    app.dependency_overrides[Params] = add_pagination

    response = client.get(
        "/api/v1/transactions",
        params=QueryParams(
            {
                "from_date": datetime_to_str(datetime.now() - timedelta(minutes=1)),
                "to_date": datetime_to_str(datetime.now() + timedelta(minutes=1)),
                "direction": "in",
            }
        ),
    )
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) == 2
    for el in data:
        assert el["id"] in (transaction_2_id, transaction_4_id)
