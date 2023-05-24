from unittest.mock import Mock
from fastapi import HTTPException
import pytest
from app.api.api_v1.endpoints import cards
from app.models.card import Card, CardCreate, CardExpiry
from sqlmodel import Session, select
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app import utils
from fastapi.encoders import jsonable_encoder
from app import deps
from app.tests.utils.utils import random_user, random_card
from main import app

from app.models.user import User


@pytest.fixture(name="card")
def card_fixture(session: Session):
    curr_year = datetime.now().year
    yield CardCreate(
        number="1234567890123456",
        expiry=jsonable_encoder(CardExpiry(mm="09", yyyy=str(curr_year + 1))),
        holder="User Userov",
        cvc="345",
    )


# card_2 = CardCreate(
#     number=6543210987654321,
#     expiry=jsonable_encoder(CardExpiry(mm="10", yyyy=str(curr_year + 1))),
#     holder="User Userov",
#     cvc=345,
# )

# TEST POST ------------------------------------


def test_add_card_succeeds_when_userAndValidData(
    client: TestClient, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = user

    response = client.post("/api/v1/cards", json=jsonable_encoder(card))
    data = response.json()

    assert response.status_code == 200
    assert data["number"] == card.number
    app.dependency_overrides.clear()


def test_add_card_raises401_when_NotLoggedUser(
    client: TestClient, guest, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = guest

    response = client.post("/api/v1/cards", json=jsonable_encoder(card))
    data = response.json()

    assert response.status_code == 401
    # assert data["detail"] == "You should login first"

    app.dependency_overrides.clear()


def test_add_card_raises400_when_sameCardNumberWithDiffData(
    client: TestClient, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = user

    client.post("/api/v1/cards", json=jsonable_encoder(card))

    card.cvc = "111"

    response = client.post("/api/v1/cards", json=jsonable_encoder(card))
    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "This card # already exists with different credentials"
    app.dependency_overrides.clear()


def test_add_card_raises400_when_userAlreadyHasTheCard(
    client: TestClient, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = user

    client.post("/api/v1/cards", json=jsonable_encoder(card))

    response = client.post("/api/v1/cards", json=jsonable_encoder(card))
    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "You already have this card"
    app.dependency_overrides.clear()


def test_add_card_raises400_when_cardIsExpired(
    client: TestClient, user, card: CardCreate
):
    curr_year = datetime.now().year
    app.dependency_overrides[deps.get_current_user] = user

    card.expiry = jsonable_encoder(CardExpiry(mm="09", yyyy=str(curr_year - 1)))

    response = client.post("/api/v1/cards", json=jsonable_encoder(card))
    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "Your card is expired"
    app.dependency_overrides.clear()


def test_add_card_succeeds_when_sameCardAlreadyReggdWithAnotherUser(
    session: Session, client: TestClient, user, admin, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = admin
    client.post("/api/v1/cards", json=jsonable_encoder(card))

    app.dependency_overrides[deps.get_current_user] = user
    response = client.post("/api/v1/cards", json=jsonable_encoder(card))

    # what it returns
    data = response.json()
    assert response.status_code == 200
    assert data["number"] == card.number

    # how it registers the new user associated with the card
    card_inDB: Card = session.exec(
        select(Card).filter(Card.number == utils.util_crypt.encrypt(card.number))
    ).first()
    assert user() in card_inDB.users
    assert admin() in card_inDB.users
    app.dependency_overrides.clear()


# TEST GET ONE ------------------------------------


def test_get_card_raises404_when_cardExistsNotLoggedUser(
    client: TestClient, guest, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = user
    client.post("/api/v1/cards", json=jsonable_encoder(card))

    app.dependency_overrides[deps.get_current_user] = guest

    response = client.get(f"/api/v1/cards/{card.number}")
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "You should be logged in"
    app.dependency_overrides.clear()


def test_get_card_returnsCard_when_cardExistsAsssociatedWithUser(
    client: TestClient, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = user

    client.post("/api/v1/cards", json=jsonable_encoder(card))

    response = client.get(f"/api/v1/cards/{card.number}")
    data = response.json()

    assert response.status_code == 200

    found_card = Card(
        number=data["number"],
        expiry=data["expiry"],
        holder=data["holder"],
        cvc=data["cvc"],
    )
    assert found_card.number == card.number
    assert found_card.expiry == card.expiry.datetime_
    assert found_card.holder == card.holder
    assert found_card.cvc == card.cvc
    app.dependency_overrides.clear()


def test_get_card_returnsCard_when_userAdminCardExistsNotAsssociatedWithUser(
    client: TestClient, admin, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = user
    client.post("/api/v1/cards", json=jsonable_encoder(card))

    app.dependency_overrides[deps.get_current_user] = admin
    response = client.get(f"/api/v1/cards/{card.number}")
    data = response.json()

    assert response.status_code == 200

    found_card = Card(
        number=data["number"],
        expiry=data["expiry"],
        holder=data["holder"],
        cvc=data["cvc"],
    )
    assert found_card.number == card.number
    assert found_card.expiry == card.expiry.datetime_
    assert found_card.holder == card.holder
    assert found_card.cvc == card.cvc
    app.dependency_overrides.clear()


def test_get_card_returns404_when_CardExistsNotAsssociatedWithUser(
    client: TestClient, admin, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = admin
    client.post("/api/v1/cards", json=jsonable_encoder(card))

    app.dependency_overrides[deps.get_current_user] = user
    response = client.get(f"/api/v1/cards/{card.number}")
    data = response.json()

    assert response.status_code == 404
    app.dependency_overrides.clear()
