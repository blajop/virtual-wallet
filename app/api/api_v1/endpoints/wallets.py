from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session

from app import crud, deps
from app.models import User, WalletCreate

router = APIRouter()


@router.get("")
def get_wallets(
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
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
    if user != logged_user:
        raise HTTPException(
            status_code=403, detail="Cannot add wallets to other users!"
        )

    return crud.wallet.create(db, user, new_wallet)


@router.delete("/{wallet_id}", status_code=204)
def remove_wallet(
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


@router.get("/{wallet_id}/leeches")
def get_wallet_leeches(
    wallet_id: str,
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if user != logged_user and not crud.user.is_admin(logged_user):
        # admin can look up whoever
        raise HTTPException(status_code=403)

    wallet = crud.wallet.get_by_owner(db, user, wallet_id)
    if not wallet:
        raise HTTPException(status_code=404)

    return wallet.users


@router.post("/{wallet_id}/leeches")
def invite_wallet_leeches(
    wallet_id: str,
    leech: str,
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if user != logged_user:
        raise HTTPException(
            status_code=403, detail="Cannot invite to wallets that you don't own"
        )

    wallet = crud.wallet.get_by_owner(db, user, wallet_id)
    leech_user = crud.user.get(db, leech)

    if not all([leech_user, wallet]):
        raise HTTPException(status_code=404)

    return crud.wallet.invite_user(db, wallet, leech_user).__dict__


@router.delete("/{wallet_id}/leeches/{user_to_kick}", status_code=204)
def kick_wallet_leech(
    wallet_id: str,
    user_to_kick: str,
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if user != logged_user:
        raise HTTPException(
            status_code=403, detail="Cannot kick users from wallets that you don't own"
        )

    wallet = crud.wallet.get_by_owner(db, user, wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="No such wallet owned")

    return crud.wallet.kick_user(db=db, wallet=wallet, user_to_remove=user_to_kick)
