from datetime import datetime, timedelta
from typing import Union
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import crud, deps
from app.error_models import TransactionError
from app.models import User, Transaction, TransactionCreate
from app.models.msg import Msg


router = APIRouter()


@router.get("", response_model=list[Transaction])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
    f_start_datetime: datetime = datetime.now() - timedelta(weeks=4.0),
    f_end_datetime: datetime = datetime.now(),
    f_recipient: str = None,
    f_direction: str = "all",
    sort_by: str = "date",
    sort: str = "asc",
):
    # transactions filtered by period, recipient,
    # and direction (incoming or outgoing) and sort them by amount and date.

    return crud.transaction.get_multi(db, skip=skip, limit=limit, user=logged_user)


@router.get("/{id}", response_model=Transaction)
def get_transaction(
    id: str,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    result = crud.transaction.get(db, id, logged_user)
    if not result:
        raise HTTPException(
            status_code=404, detail="There is no such transaction within your access"
        )
    return result


@router.post("", response_model=Transaction, status_code=201)
def create_transaction(
    new_transaction: TransactionCreate,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    """
    Used to create a new transaction.
    One of the two wallet_sender | card_sender should be passed in the body
    of the request, and the other removed/null.
    If the transaction is not recurring, the recurring field should be
    removed/null.
    If the spending category should be default, the field should be removed from the body.

    Arguments:
        new_transaction: TransactionCreate model
        db: Session
        logged_user: User model

    Returns:
        Transaction
    """

    try:
        return crud.transaction.create(
            db, new_transaction=new_transaction, user=logged_user
        )
    except TransactionError as err:
        raise HTTPException(status_code=400, detail=err.args[0])


@router.put("/{id}/confirm")
def confirm_transaction(
    id: str,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    transaction = crud.transaction.get(db, id, logged_user)

    if not transaction:
        raise HTTPException(status_code=404)

    try:
        crud.transaction.accept(db=db, transaction=transaction)
    except TransactionError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
