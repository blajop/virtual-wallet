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
from app.models.transaction import Transaction
from app.models.user import User


router = APIRouter()


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
