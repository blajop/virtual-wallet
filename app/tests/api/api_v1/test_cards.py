from unittest.mock import Mock
from fastapi import HTTPException
import pytest
from app.api.api_v1.endpoints import cards
from app.models.card import Card, CardCreate, CardExpiry
from sqlmodel import Session
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


# def test_add_card_succeeds_when_userAndValidData(client: TestClient):
#     response = client.post("/api/v1/cards", json=jsonable_encoder(card_1))
#     data = response.json()

#     assert response.status_code == 200
#     assert data["number"] == card_1.number


# def test_add_card_raises400_when_sameCardNumberWithDiffData(client: TestClient):
#     client.post("/api/v1/cards", json=jsonable_encoder(card_1))
#     card_1.cvc = "111"

#     response = client.post("/api/v1/cards", json=jsonable_encoder(card_1))
#     data = response.json()

#     assert response.status_code == 400


# def test_add_card_succeeds_when_sameCardAlreadyReggdWithAnotherUser(client: TestClient):
#     client.post("/api/v1/cards", json=jsonable_encoder(card_1))
#     card_1.cvc = "111"

#     response = client.post("/api/v1/cards", json=jsonable_encoder(card_1))
#     data = response.json()

#     assert response.status_code == 400


# def test_get_card_raises404_when_cardExistsButNotAsssociatedWithUser(
#     client: TestClient, user
# ):
#     app.dependency_overrides[deps.get_current_user] = user

#     client.post("/api/v1/cards", json=jsonable_encoder(card_1))

#     user.cards.clear()

#     response = client.get(f"/api/v1/cards/{card_1.number}")
#     assert response.status_code == 404


# def test_get_card_raises404_when_cardDoesNotExist(client: TestClient):
#     response = client.get(f"/api/v1/cards/{card_1.number}")
#     assert response.status_code == 404


def test_get_card_findsCard_when_cardExistsAsssociatedWithUser(
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


def test_get_card_raises404_when_cardExistsNotLoggedUser(
    client: TestClient, guest, user
):
    app.dependency_overrides[deps.get_current_user] = user
    client.post("/api/v1/cards", json=jsonable_encoder(card_1))

    app.dependency_overrides[deps.get_current_user] = guest

    response = client.get(f"/api/v1/cards/{card_1.number}")
    assert response.status_code == 401
    app.dependency_overrides.clear()
