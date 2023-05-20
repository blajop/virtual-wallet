from typing import Annotated
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Response,
    Security,
)
from app.api import deps
from app.crud import crud_wallet
from app.models.user import User
from app.models.wallet import WalletCreate


router = APIRouter()


@router.get("/")
def get_wallets():
    return crud_wallet.get_wallets()


@router.post("/")
def create_wallet(
    new_wallet: WalletCreate,
    current_user: Annotated[User, Depends(deps.get_current_user)],
):
    if not current_user:
        raise HTTPException(status_code=401)
    return crud_wallet.create_wallet(current_user, new_wallet)
