from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
)
from app.crud import crud_transaction


router = APIRouter()


@router.get("/")
def get_transactions():
    return crud_transaction.get_transactions()
