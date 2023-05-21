from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
)
from sqlmodel import Session
from app.api import deps
from app import crud
from app.models.user import User
from app.models.wallet import Wallet, WalletCreate

router = APIRouter()


@router.get("")
def get_wallets(
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if not user:
        raise HTTPException(status_code=404)

    if user != logged_user and not crud.user.is_admin(logged_user):
        # admin can look up whoever
        raise HTTPException(status_code=403)

    return crud.wallet.get_multi_by_owner(db, user)


@router.post("")
def create_wallet(
    new_wallet: WalletCreate,
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if not user:
        raise HTTPException(status_code=404)

    if user != logged_user:
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
    if not user:
        raise HTTPException(status_code=404)

    if user != logged_user and not crud.user.is_admin(logged_user):
        # admin can look up whoever
        raise HTTPException(status_code=403)

    wallet = crud.wallet.get(db, wallet_id)
    if not wallet:
        raise HTTPException(status_code=404)

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

    if wallet.owner != logged_user:
        raise HTTPException(
            status_code=403, detail="Cannot invite to wallets you don't own"
        )

    return crud.wallet.invite_user(db, wallet, leech_user).__dict__


@router.delete("/{wallet_id}")
def delete_wallet(
    wallet_id: str,
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    wallet = crud.wallet.get(db=db, id=wallet_id)

    if not wallet:
        raise HTTPException(status_code=404, detail="No such wallet!")

    if user != logged_user or logged_user != wallet.owner:
        raise HTTPException(status_code=403, detail="Can only delete your own wallets!")

    crud.wallet.remove(db=db, id=wallet_id)

    return Response(status_code=204)
