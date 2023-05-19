from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Response,
    Security,
)
from app.services import transaction_services


transactions_router = APIRouter(prefix="/transactions", tags=["03. API / Transactions"])


@transactions_router.get("/")
def get_transactions():
    return transaction_services.get_transactions()
