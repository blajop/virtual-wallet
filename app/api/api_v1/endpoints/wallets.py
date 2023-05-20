from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Response,
    Security,
)
from app.crud import crud_wallet


router = APIRouter()


@router.get("/")
def get_wallets():
    return crud_wallet.get_wallets()
