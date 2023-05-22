from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
)
from sqlmodel import Session
from app import crud
from app.api import deps
from app.crud import crud_transaction
from app.error_models.transaction_errors import TransactionError
from app.models.transaction import Transaction, TransactionCreate
from app.models.user import User


router = APIRouter()


@router.get("", response_model=list[Transaction])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if not logged_user:
        raise HTTPException(status_code=401, detail="You should be logged in")

    return crud.transaction.get_multi(db, skip=skip, limit=limit, user=logged_user)


@router.get("/{id}", response_model=Transaction)
def get_transaction(
    id: str,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if not logged_user:
        raise HTTPException(status_code=401, detail="You should be logged in")
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
    if not logged_user:
        raise HTTPException(status_code=401, detail="You should be logged in")
    try:
        return crud.transaction.create(
            db, new_transaction=new_transaction, user=logged_user
        )
    except TransactionError as err:
        raise HTTPException(status_code=400, detail=err.args[0])
