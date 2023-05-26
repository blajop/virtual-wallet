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


admin_router = APIRouter()


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
        admin_r=True,
    )


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


@admin_router.delete("/cards/admin-del/{card_identifier}", status_code=204)
def admin_delete_card(
    card_identifier,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_admin),
):
    try:
        crud.card.remove(db, card_identifier)
    except CardNotFoundError as err:
        raise HTTPException(status_code=404, detail=err.args[0])
