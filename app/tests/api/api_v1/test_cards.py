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


curr_year = datetime.now().year

card_1 = CardCreate(
    number=1234567890123456,
    expiry=jsonable_encoder(CardExpiry(mm="09", yyyy=str(curr_year + 1))),
    holder="User Userov",
    cvc=345,
)

card_2 = CardCreate(
    number=6543210987654321,
    expiry=CardExpiry(mm="10", yyyy=str(curr_year + 1)),
    holder="User Userov",
    cvc=345,
)


def test_add_card(client: TestClient):
    response = client.post("/api/v1/cards", json=jsonable_encoder(card_1))
    data = response.json()

    assert response.status_code == 200
    assert data["number"] == card_1.number


def test_get_card(session: Session, client: TestClient):
    # session.add(card_3)
    # session.commit()

    # plain_num = utils.util_crypt.decrypt(card_3.number)

    response = client.get(f"/api/v1/cards/{card_1.number}")
    data = response.json()

    assert response.status_code == 200
    # assert data["id"] == card_3.id
    # assert data["number"] == card_3.number
    # assert data["expiry"] == card_3.expiry
    # assert data["holder"] == card_3.holder
    # assert data["cvc"] == card_3.cvc
