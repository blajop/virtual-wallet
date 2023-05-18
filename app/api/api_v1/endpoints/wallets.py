from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Response,
    Security,
)
from app.services import wallet_services


wallets_router = APIRouter(prefix="/wallets", tags=["02. API / Wallets"])


@wallets_router.get("/")
def get_wallets():
    return wallet_services.get_wallets()
