from datetime import datetime, timedelta
from typing import Union
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import crud, deps
from app.error_models import TransactionError
from app.error_models.card_errors import CardNotFoundError
from app.models import User, Transaction, TransactionCreate
from app.models.card import Card
from app.models.msg import Msg
from app.models.user import UserUpdate
from app.models.wallet import Wallet


admin_router = APIRouter()


#  USER
@admin_router.get("/admin/{identifier}", response_model=User)
def get_user(
    identifier: str,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_admin),
):
    user = crud.user.get(db, identifier)

    if not user:
        raise HTTPException(status_code=404)
    return user


@admin_router.put("/admin/{identifier}", response_model=UserUpdate)
def get_user(
    updated_info: UserUpdate,
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_admin),
):
    return crud.user.update(db=db, db_obj=user, obj_in=updated_info)


# TRANSACTIONS
@admin_router.get("/transactions/{id}", response_model=Transaction)
def get_transaction(
    id: str,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_admin),
):
    result = crud.transaction.get(db, id, logged_user, admin_r=True)

    if not result:
        raise HTTPException(status_code=404, detail="There is no such transaction")

    return result


@admin_router.get("/transactions", response_model=list[Transaction])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_admin),
    from_date: datetime = datetime.now() - timedelta(weeks=4.0),
    to_date: datetime = datetime.now(),
    recipient: str = None,
    direction: str = "all",
    sort_by: str = "date",
    sort: str = "asc",
    user: str | None = None,
):
    if user:
        user = crud.user.get(db, user)

    return crud.transaction.get_multi(
        db,
        skip=skip,
        limit=limit,
        user=user,
        from_date=from_date,
        to_date=to_date,
        recipient=recipient,
        direction=direction,
        sort_by=sort_by,
        sort=sort,
    )


# CARDS
@admin_router.get("/cards/{card_identifier}", response_model=Card)
def get_card(
    card_identifier: str,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_admin),
):
    result = crud.card.get(db, card_identifier, admin_r=True)

    if not result:
        raise HTTPException(status_code=404, detail="There is no such card")
    return result


@admin_router.get("/cards", response_model=list[Card])
def get_cards(
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_admin),
    skip: int = 0,
    limit: int = 100,
):
    return crud.card.get_multi(db, skip=skip, limit=limit, admin_r=True)


@admin_router.delete("/cards/{card_identifier}", status_code=204)
def admin_delete_card(
    card_identifier,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_admin),
):
    try:
        crud.card.remove(db, card_identifier)
    except CardNotFoundError as err:
        raise HTTPException(status_code=404, detail=err.args[0])


# WALLETS
@admin_router.get("/wallets", response_model=list[Wallet])
def get_wallets(
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_admin),
    skip: int = 0,
    limit: int = 100,
):
    return crud.wallet.get_multi(db, skip=skip, limit=limit)


@admin_router.get("/wallets/{identifier}", response_model=list[Wallet])
def get_wallets_for_user(
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_admin),
):
    return crud.wallet.get_multi_by_owner(db, user)
