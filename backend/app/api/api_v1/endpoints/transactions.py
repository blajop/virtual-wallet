from datetime import datetime, timedelta
from typing import Union
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session

from app import crud, deps, utils
from app.error_models import TransactionError
from app.error_models.transaction_errors import TransactionPermissionError
from app.models import User, Transaction, TransactionCreate
from app.models.msg import Msg
from fastapi_pagination import Page, Params

router = APIRouter()


@router.get("", response_model=Page[Transaction])
def get_transactions(
    params: Params = Depends(),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
    from_date: datetime = datetime.now() - timedelta(weeks=4.0),
    to_date: datetime = datetime.now(),
    recipient: str = None,
    status: str = None,
    direction: str = "all",
    sort_by: str = "date",
    sort: str = "desc",
):
    return crud.transaction.get_multi(
        db,
        user=logged_user,
        from_date=from_date,
        to_date=to_date,
        recipient=recipient,
        direction=direction,
        sort_by=sort_by,
        sort=sort,
        status=status,
    )


@router.get("/confirm_balance")
def confirm_balance(
    wallet_id: str,
    amount: float,
    currency: str,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    user_wallets_ids = [
        w.id for w in crud.wallet.get_multi_by_owner(db, logged_user)
    ] + [w.id for w in logged_user.wallets]
    if wallet_id not in user_wallets_ids and not crud.user.is_admin(logged_user):
        raise HTTPException(
            status_code=403, detail="Wallet passed is not associated with you"
        )
    wallet = crud.wallet.get(db, logged_user, wallet_id)
    if crud.transaction.confirm_balance(db, wallet, logged_user, amount, currency):
        return Msg(msg="You have enough balance")
    else:
        raise HTTPException(status_code=400, detail="Insufficient balance")


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
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    recipient_user = crud.user.get(db, new_transaction.receiving_user)
    try:
        created_transaction = crud.transaction.create(
            db,
            new_transaction=new_transaction,
            user=logged_user,
            recipient_user=recipient_user,
        )
    except TransactionError as err:
        raise HTTPException(status_code=400, detail=err.args[0])

    background_tasks.add_task(
        utils.util_mail.send_confirm_transaction_email,
        recipient_user.email,
        created_transaction,
        logged_user,
        recipient_user,
    )

    return created_transaction


@router.get("/{token_transaction}/confirm/{token_recipient}", response_model=Msg)
def confirm_transaction(
    token_transaction: str,
    token_recipient: str,
    db: Session = Depends(deps.get_db),
):
    transaction_id = utils.util_mail.verify_email_link_token(token_transaction)
    recipient_id = utils.util_mail.verify_email_link_token(token_recipient)

    recipient_user = crud.user.get(db, recipient_id)
    transaction = crud.transaction.get(db, transaction_id, recipient_user)

    if not transaction:
        raise HTTPException(status_code=404)

    try:
        try:
            return crud.transaction.accept(
                db=db, transaction=transaction, user=recipient_user
            )
        except TransactionPermissionError as err:
            raise HTTPException(status_code=403, detail=err.args[0])
    except TransactionError as err:
        raise HTTPException(status_code=400, detail=err.args[0])


@router.get("/{token_transaction}/decline/{token_recipient}", response_model=Msg)
def decline_transaction(
    token_transaction: str,
    token_recipient: str,
    db: Session = Depends(deps.get_db),
):
    transaction_id = utils.util_mail.verify_email_link_token(token_transaction)
    recipient_id = utils.util_mail.verify_email_link_token(token_recipient)

    recipient_user = crud.user.get(db, recipient_id)
    transaction = crud.transaction.get(db, transaction_id, recipient_user)

    if not transaction:
        raise HTTPException(status_code=404)

    try:
        try:
            return crud.transaction.decline(
                db=db, transaction=transaction, user=recipient_user
            )
        except TransactionPermissionError as err:
            raise HTTPException(status_code=403, detail=err.args[0])
    except TransactionError as err:
        raise HTTPException(status_code=400, detail=err.args[0])
