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
from app.tests.utils.utils import random_user
from main import app

from app.models.user import User


curr_year = datetime.now().year

card_1 = CardCreate(
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


def test_add_card_succeeds_when_userAndValidData(client: TestClient, user):
    app.dependency_overrides[deps.get_current_user] = user

    response = client.post("/api/v1/cards", json=jsonable_encoder(card_1))
    data = response.json()

    assert response.status_code == 200
    assert data["number"] == card_1.number
    app.dependency_overrides.clear()


def test_add_card_raises401_when_NotLoggedUser(client: TestClient, guest):
    app.dependency_overrides[deps.get_current_user] = guest

    response = client.post("/api/v1/cards", json=jsonable_encoder(card_1))
    data = response.json()

    assert response.status_code == 401
    # assert data["detail"] == "You should login first"

    app.dependency_overrides.clear()


def test_add_card_raises400_when_sameCardNumberWithDiffData(client: TestClient, user):
    app.dependency_overrides[deps.get_current_user] = user

    client.post("/api/v1/cards", json=jsonable_encoder(card_1))

    card_1.cvc = "111"

    response = client.post("/api/v1/cards", json=jsonable_encoder(card_1))
    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "This card # already exists with different credentials"

    card_1.cvc = "345"
    app.dependency_overrides.clear()


def test_add_card_raises400_when_userAlreadyHasTheCard(client: TestClient, user):
    app.dependency_overrides[deps.get_current_user] = user

    client.post("/api/v1/cards", json=jsonable_encoder(card_1))

    response = client.post("/api/v1/cards", json=jsonable_encoder(card_1))
    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "You already have this card"
    app.dependency_overrides.clear()


def test_add_card_raises400_when_cardIsExpired(client: TestClient, user):
    app.dependency_overrides[deps.get_current_user] = user

    card_1.expiry = jsonable_encoder(CardExpiry(mm="09", yyyy=str(curr_year - 1)))

    response = client.post("/api/v1/cards", json=jsonable_encoder(card_1))
    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "Your card is expired"

    card_1.expiry = jsonable_encoder(CardExpiry(mm="09", yyyy=str(curr_year + 1)))
    app.dependency_overrides.clear()


def test_add_card_succeeds_when_sameCardAlreadyReggdWithAnotherUser(
    session: Session, client: TestClient, user, admin
):
    app.dependency_overrides[deps.get_current_user] = admin
    client.post("/api/v1/cards", json=jsonable_encoder(card_1))

    app.dependency_overrides[deps.get_current_user] = user
    response = client.post("/api/v1/cards", json=jsonable_encoder(card_1))

    # what it returns
    data = response.json()
    assert response.status_code == 200
    assert data["number"] == card_1.number

    # how it registers the new user associated with the card
    card_inDB: Card = session.exec(
        select(Card).filter(Card.number == utils.util_crypt.encrypt(card_1.number))
    ).first()
    assert user() in card_inDB.users
    assert admin() in card_inDB.users
    app.dependency_overrides.clear()


# TEST GET ONE ------------------------------------


def test_get_card_raises404_when_cardExistsNotLoggedUser(
    client: TestClient, guest, user
):
    app.dependency_overrides[deps.get_current_user] = user
    client.post("/api/v1/cards", json=jsonable_encoder(card_1))

    app.dependency_overrides[deps.get_current_user] = guest

    response = client.get(f"/api/v1/cards/{card_1.number}")
    data = response.json()
    assert response.status_code == 401
    assert data["detail"] == "You should be logged in"
    app.dependency_overrides.clear()


def test_get_card_returnsCard_when_cardExistsAsssociatedWithUser(
    client: TestClient, user
):
    app.dependency_overrides[deps.get_current_user] = user

    client.post("/api/v1/cards", json=jsonable_encoder(card_1))

    response = client.get(f"/api/v1/cards/{card_1.number}")
    data = response.json()

    assert response.status_code == 200

    found_card = Card(
        number=data["number"],
        expiry=data["expiry"],
        holder=data["holder"],
        cvc=data["cvc"],
    )
    assert found_card.number == card_1.number
    assert found_card.expiry == card_1.expiry.datetime_
    assert found_card.holder == card_1.holder
    assert found_card.cvc == card_1.cvc
    app.dependency_overrides.clear()


def test_get_card_returnsCard_when_userAdminCardExistsNotAsssociatedWithUser(
    client: TestClient, admin, user
):
    app.dependency_overrides[deps.get_current_user] = user
    client.post("/api/v1/cards", json=jsonable_encoder(card_1))

    app.dependency_overrides[deps.get_current_user] = admin
    response = client.get(f"/api/v1/cards/{card_1.number}")
    data = response.json()

    assert response.status_code == 200

    found_card = Card(
        number=data["number"],
        expiry=data["expiry"],
        holder=data["holder"],
        cvc=data["cvc"],
    )
    assert found_card.number == card_1.number
    assert found_card.expiry == card_1.expiry.datetime_
    assert found_card.holder == card_1.holder
    assert found_card.cvc == card_1.cvc
    app.dependency_overrides.clear()


def test_get_card_returns404_when_CardExistsNotAsssociatedWithUser(
    client: TestClient, admin, user
):
    app.dependency_overrides[deps.get_current_user] = admin
    client.post("/api/v1/cards", json=jsonable_encoder(card_1))

    app.dependency_overrides[deps.get_current_user] = user
    response = client.get(f"/api/v1/cards/{card_1.number}")
    data = response.json()

    assert response.status_code == 404
    app.dependency_overrides.clear()
