from unittest.mock import Mock
from fastapi import HTTPException
import pytest
from app.api.api_v1.endpoints import cards
from app.models.card import Card, CardCreate, CardExpiry, UserCardLink
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
    yield random_card(session)


# TEST POST ------------------------------------


def test_add_card_succeeds_when_userAndValidData(
    client: TestClient, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = user

    response = client.post("/api/v1/cards", json=jsonable_encoder(card))
    data = response.json()

    assert response.status_code == 200
    assert data["number"] == card.number


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


def test_add_card_raises400_when_userAlreadyHasTheCard(
    client: TestClient, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = user

    client.post("/api/v1/cards", json=jsonable_encoder(card))

    response = client.post("/api/v1/cards", json=jsonable_encoder(card))
    data = response.json()

    assert response.status_code == 400
    assert data["detail"] == "You already have this card"


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


# TEST GET ONE ------------------------------------


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


def test_get_card_returns404_when_CardExistsNotAsssociatedWithUser(
    client: TestClient, admin, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = admin
    client.post("/api/v1/cards", json=jsonable_encoder(card))

    app.dependency_overrides[deps.get_current_user] = user
    response = client.get(f"/api/v1/cards/{card.number}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "There is no such card within your access"


# TEST GET ALL ------------------------------------


def test_get_cards_returnsEmptyList_when_NoCards(client: TestClient, admin, user):
    app.dependency_overrides[deps.get_current_user] = admin
    response = client.get(f"/api/v1/cards")
    data = response.json()
    assert data == []

    app.dependency_overrides[deps.get_current_user] = user
    response = client.get(f"/api/v1/cards")
    data = response.json()
    assert data == []


def test_get_cards_showsAllCards_when_user(
    session: Session, client: TestClient, admin, user
):
    card_1 = random_card(session)
    card_2 = random_card(session)
    card_3 = random_card(session)

    app.dependency_overrides[deps.get_current_user] = admin
    client.post("/api/v1/cards", json=jsonable_encoder(card_1))

    app.dependency_overrides[deps.get_current_user] = user
    client.post("/api/v1/cards", json=jsonable_encoder(card_2))
    client.post("/api/v1/cards", json=jsonable_encoder(card_3))

    # Act - user
    response = client.get(f"/api/v1/cards")
    data = response.json()
    assert len(data) == 2
    for obj in data:
        assert obj["number"] in [card_2.number, card_3.number]


def test_get_cards_showsAllCards_when_Admin(
    session: Session, client: TestClient, admin, user
):
    card_1 = random_card(session)
    card_2 = random_card(session)
    card_3 = random_card(session)

    app.dependency_overrides[deps.get_current_user] = user
    client.post("/api/v1/cards", json=jsonable_encoder(card_2))
    client.post("/api/v1/cards", json=jsonable_encoder(card_3))

    app.dependency_overrides[deps.get_current_user] = admin
    client.post("/api/v1/cards", json=jsonable_encoder(card_1))

    # Act - admin
    response = client.get(f"/api/v1/cards")
    data = response.json()
    assert len(data) == 3
    for obj in data:
        assert obj["number"] in [card_1.number, card_2.number, card_3.number]


# TEST DELETE ------------------------------------


def test_adminDelete_card_returns403_when_userNotAdmin(
    client: TestClient, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = user
    client.post("/api/v1/cards", json=jsonable_encoder(card))

    response = client.delete(f"/api/v1/cards/admin-del/{card.number}")
    data = response.json()

    assert response.status_code == 403
    assert data["detail"] == "Admin endpoint"


def test_adminDelete_card_returns404_when_cardNotExisting(
    client: TestClient, admin, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = admin

    response = client.delete(f"/api/v1/cards/admin-del/{card.number}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "There is no such card"


def test_adminDelete_card_works_when_allOk(
    session: Session, client: TestClient, admin, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = user
    client.post("/api/v1/cards", json=jsonable_encoder(card))

    app.dependency_overrides[deps.get_current_user] = admin
    client.post("/api/v1/cards", json=jsonable_encoder(card))

    card_inDB: Card = session.exec(
        select(Card).filter(Card.number == utils.util_crypt.encrypt(card.number))
    ).first()

    assert len(card_inDB.users) == 2

    card_db_id = card_inDB.id

    # Act
    response = client.delete(f"/api/v1/cards/admin-del/{card.number}")

    assert response.status_code == 204

    user_card_link = (
        session.exec(select(UserCardLink).filter(UserCardLink.card_id == card_db_id))
        .unique()
        .all()
    )
    assert len(user_card_link) == 0

    response = client.get(f"/api/v1/cards/{card.number}")
    assert response.status_code == 404


def test_deregister_card_returns404_when_cardDoeNotExist(
    client: TestClient, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = user

    response = client.delete(f"/api/v1/cards/{card.number}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "There is no such card"


def test_deregister_card_returns404_when_cardNotAssociatedToUser(
    client: TestClient, admin, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = admin
    client.post("/api/v1/cards", json=jsonable_encoder(card))

    app.dependency_overrides[deps.get_current_user] = user
    response = client.delete(f"/api/v1/cards/{card.number}")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "There is no such card within your access"


def test_deregister_card_works_when_cardHasMoreThanOneUser(
    session: Session, client: TestClient, admin, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = user
    client.post("/api/v1/cards", json=jsonable_encoder(card))

    app.dependency_overrides[deps.get_current_user] = admin
    client.post("/api/v1/cards", json=jsonable_encoder(card))

    card_inDB: Card = session.exec(
        select(Card).filter(Card.number == utils.util_crypt.encrypt(card.number))
    ).first()
    assert len(card_inDB.users) == 2

    # Act - admin deletes
    response = client.delete(f"/api/v1/cards/{card.number}")

    assert response.status_code == 204

    card_inDB: Card = session.exec(
        select(Card).filter(Card.number == utils.util_crypt.encrypt(card.number))
    ).first()
    assert len(card_inDB.users) == 1

    # Prepare for user delete
    client.post("/api/v1/cards", json=jsonable_encoder(card))

    app.dependency_overrides[deps.get_current_user] = user

    # Act - user deletes
    response = client.delete(f"/api/v1/cards/{card.number}")

    card_inDB: Card = session.exec(
        select(Card).filter(Card.number == utils.util_crypt.encrypt(card.number))
    ).first()

    assert response.status_code == 204
    assert len(card_inDB.users) == 1

    app.dependency_overrides[deps.get_current_user] = admin

    response = client.get(f"/api/v1/cards/{card.number}")
    assert response.status_code == 200


def test_deregister_card_works_when_cardHasOneUser(
    session: Session, client: TestClient, admin, user, card: CardCreate
):
    app.dependency_overrides[deps.get_current_user] = user
    client.post("/api/v1/cards", json=jsonable_encoder(card))

    card_inDB: Card = session.exec(
        select(Card).filter(Card.number == utils.util_crypt.encrypt(card.number))
    ).first()
    assert len(card_inDB.users) == 1
    card_db_id = card_inDB.id

    # Act
    response = client.delete(f"/api/v1/cards/{card.number}")

    assert response.status_code == 204

    user_card_link = (
        session.exec(select(UserCardLink).filter(UserCardLink.card_id == card_db_id))
        .unique()
        .all()
    )
    assert len(user_card_link) == 0

    app.dependency_overrides[deps.get_current_user] = admin

    response = client.get(f"/api/v1/cards/{card.number}")
    assert response.status_code == 404
