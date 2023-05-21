import pytest
import copy
from fastapi import HTTPException, Response
from sqlmodel import Session
from app.api.api_v1.endpoints import wallets
from app.models.user import User
from app import crud
from app.models.wallet import WalletCreate
from app.tests.utils.utils import random_user, random_wallet


# GET WALLETS


def test_get_wallets_404_when_no_user_found(db: Session, user: User):
    with pytest.raises(HTTPException) as exc_info:
        wallets.get_wallets(user=None, db=db, logged_user=user)

    assert exc_info.value.status_code == 404


def test_get_wallets_403_when_trying_to_view_another_user_wallet(
    db: Session, user: User
):
    user2 = copy.deepcopy(user)
    user2.username = "anotherUser"

    with pytest.raises(HTTPException) as exc_info:
        wallets.get_wallets(user=user2, db=db, logged_user=user)

    assert exc_info.value.status_code == 403


def test_get_wallets_by_owner_successfully(db: Session, user: User):
    wallet1 = random_wallet(user, "USD", db=db)
    wallet2 = random_wallet(user, "BGN", db=db)

    wallets_from_db_user = wallets.get_wallets(user=user, db=db, logged_user=user)

    assert len(wallets_from_db_user) > 1
    assert set([wallet1.currency, wallet2.currency]) == set(
        [wl.currency for wl in wallets_from_db_user]
    )


# CREATE WALLET


def test_create_wallet_404_when_no_user_found(db: Session, user: User):
    with pytest.raises(HTTPException) as exc_info:
        wallets.create_wallet(new_wallet="wallet", user=None, db=db, logged_user=user)

    assert exc_info.value.status_code == 404


def test_create_wallet_403_when_trying_to_create_for_another_user(
    db: Session, user: User
):
    user2 = copy.deepcopy(user)
    user2.username = "anotherUser"

    with pytest.raises(HTTPException) as exc_info:
        wallets.create_wallet(new_wallet="wallet", user=user2, db=db, logged_user=user)

    assert exc_info.value.status_code == 403


def test_create_wallet_successfully(db: Session, user: User):
    wallet = WalletCreate(currency="BGN")
    wallet = wallets.create_wallet(
        new_wallet=wallet, user=user, db=db, logged_user=user
    )

    assert wallet
    assert wallet.owner == user


# GET WALLET LEECHES


def test_get_wallet_leeches_404_when_no_user_found(db: Session, user: User):
    with pytest.raises(HTTPException) as exc_info:
        wallets.get_wallet_leeches(
            wallet_id="wallet.id", user=None, db=db, logged_user=user
        )

    assert exc_info.value.status_code == 404


def test_get_wallet_leeches_403_when_trying_to_get_for_another_users_wallet(
    db: Session, user: User
):
    user2 = copy.deepcopy(user)
    user2.username = "anotherUser"

    with pytest.raises(HTTPException) as exc_info:
        wallets.get_wallet_leeches(
            wallet_id="wallet.id", user=user2, db=db, logged_user=user
        )

    assert exc_info.value.status_code == 403


def test_get_wallet_leeches_404_when_no_wallet_found(db: Session, user: User):
    with pytest.raises(HTTPException) as exc_info:
        wallets.get_wallet_leeches(
            wallet_id="wallet.id", user=user, db=db, logged_user=user
        )

    assert exc_info.value.status_code == 404


def test_get_wallet_leeches_successfully(db: Session, user: User):
    wallet = random_wallet(user, "USD", db=db)
    leech1 = random_user(db)
    leech2 = random_user(db)
    wallet.users.extend([leech1, leech2])

    db.add_all([wallet, leech1, leech2])
    db.commit()
    db.refresh(wallet)

    wallet_leeches = wallets.get_wallet_leeches(
        wallet_id=wallet.id, user=user, db=db, logged_user=user
    )

    assert len(wallet_leeches) > 1
    assert set([leech1.username, leech2.username]) == set(
        [us.username for us in wallet_leeches]
    )


# INVITE WALLET LEECHES


def test_invite_wallet_leeches_404_when_no_user_found(db: Session, user: User):
    with pytest.raises(HTTPException) as exc_info:
        wallets.invite_wallet_leeches(
            wallet_id="wallet.id", leech=None, db=db, logged_user=user
        )

    assert exc_info.value.status_code == 404


def test_invite_wallet_leeches_403_when_trying_to_invite_for_another_users_wallet(
    db: Session, user: User
):
    user2 = random_user(db)
    user3 = random_user(db)
    wallet = random_wallet(user3, "USD", db=db)

    with pytest.raises(HTTPException) as exc_info:
        wallets.invite_wallet_leeches(
            wallet_id=wallet.id, leech=user2.username, db=db, logged_user=user
        )

    assert exc_info.value.status_code == 403


def test_invite_wallet_leeches_404_when_no_wallet_found(db: Session, user: User):
    with pytest.raises(HTTPException) as exc_info:
        wallets.invite_wallet_leeches(
            wallet_id="noWallet", leech=user.id, db=db, logged_user=user
        )

    assert exc_info.value.status_code == 404


def test_invite_wallet_leeches_successfully(db: Session, user: User):
    wallet = random_wallet(user, "USD", db=db)
    leech1 = random_user(db)
    leech2 = random_user(db)

    wallets.invite_wallet_leeches(
        wallet_id=wallet.id, leech=leech1.id, db=db, logged_user=user
    )
    wallet_leeches = wallets.invite_wallet_leeches(
        wallet_id=wallet.id, leech=leech2.id, db=db, logged_user=user
    )

    assert len(wallet_leeches) > 1
    assert set([leech1.username, leech2.username]) == set(
        [us.username for us in wallet_leeches.get("users")]
    )


# DELETE WALLET


def test_delete_wallet_404_when_no_such_wallet(db: Session, user: User):
    with pytest.raises(HTTPException) as exc_info:
        wallets.delete_wallet(wallet_id="wallet.id", user=user, db=db, logged_user=user)

    assert exc_info.value.status_code == 404


def test_delete_wallet_403_when_not_matching_user(db: Session, user: User):
    wallet = random_wallet(user, "USD", db=db)

    with pytest.raises(HTTPException) as exc_info:
        wallets.delete_wallet(wallet_id=wallet.id, user=None, db=db, logged_user=user)

    assert exc_info.value.status_code == 403


def test_delete_wallet_403_when_not_owner(db: Session, user: User):
    not_owner = random_user(db)
    wallet = random_wallet(not_owner, "USD", db=db)

    with pytest.raises(HTTPException) as exc_info:
        wallets.delete_wallet(wallet_id=wallet.id, user=user, db=db, logged_user=user)

    assert exc_info.value.status_code == 403


def test_delete_wallet_successfully(db: Session, user: User):
    wallet = random_wallet(user, "USD", db=db)

    response: Response = wallets.delete_wallet(
        wallet_id=wallet.id, user=user, db=db, logged_user=user
    )
    no_wallet = crud.wallet.get(db, wallet.id)

    assert not no_wallet
    assert response.status_code == 204
