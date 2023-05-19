from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Response,
    Security,
)
from app.crud import crud_transaction


transactions_router = APIRouter(prefix="/transactions", tags=["03. API / Transactions"])


@transactions_router.get("/")
def get_transactions():
    return crud_transaction.get_transactions()
