from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Response,
    Security,
)
from app.crud import crud_wallet


wallets_router = APIRouter(prefix="/wallets", tags=["02. API / Wallets"])


@wallets_router.get("/")
def get_wallets():
    return crud_wallet.get_wallets()
