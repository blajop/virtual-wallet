from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlmodel import Session
from app.api import deps
from app import crud
from app.models.user import User
from app.models.wallet import Wallet, WalletCreate
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("")
def get_wallets(
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if not logged_user:
        raise HTTPException(status_code=401)

    if not user:
        raise HTTPException(status_code=404)

    if user.id != logged_user.id and not crud.user.is_admin(logged_user):
        # admin can look up whoever
        raise HTTPException(status_code=401)

    return crud.wallet.get_multi_by_owner(db, user)


@router.post("")
def create_wallet(
    new_wallet: WalletCreate,
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    user: User = crud.user.get(db, user)

    if not logged_user:
        raise HTTPException(status_code=401)

    if not user:
        raise HTTPException(status_code=404)

    if user.id != logged_user.id:
        raise HTTPException(
            status_code=403, detail="Cannot add wallets to other users!"
        )

    return crud.wallet.create(db, user, new_wallet)


@router.get("/{wallet_id}/leeches")
def get_wallet_leeches(
    wallet_id: str,
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if not logged_user:
        raise HTTPException(status_code=401)

    if not user:
        raise HTTPException(status_code=404)

    if user.id != logged_user.id and not crud.user.is_admin(logged_user):
        # admin can look up whoever
        raise HTTPException(status_code=401)

    wallet = crud.wallet.get(db, wallet_id)

    return wallet.users


@router.post("/{wallet_id}/leeches")
def invite_wallet_leeches(
    wallet_id: str,
    leech: str,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    """
    Add a leech to a wallet.

    Args:
        wallet_id: id of the wallet
        leech: username/email/phone number to add to the wallet
    Returns:
        wallet info
    Raises:
        404 if leech user is not found

    """

    wallet = crud.wallet.get(db, wallet_id)
    leech_user = crud.user.get(db, leech)

    if not all([leech_user, wallet]):
        raise HTTPException(status_code=404)

    if wallet.owner.id != logged_user.id:
        raise HTTPException(
            status_code=403, detail="Cannot invite to wallets you don't own"
        )

    return crud.wallet.invite_user(db, wallet, leech_user).__dict__
