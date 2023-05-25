from typing import Optional
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
    """
    Add a leech to a wallet.

    Args:
        wallet_id: id of the wallet
        leech: username/email/phone number to add to the wallet
    Returns:
        wallet info
    Raises:
        403 if trying to access another user's wallet
        404 if leech user or wallet not found

    """
    if user != logged_user:
        raise HTTPException(
            status_code=403, detail="Cannot invite to wallets that you don't own"
        )

    wallet = crud.wallet.get_by_owner(db, user, wallet_id)
    leech_user = crud.user.get(db, leech)

    if not all([leech_user, wallet]):
        raise HTTPException(status_code=404)

    return crud.wallet.invite_user(db, wallet, leech_user).__dict__


### CODE BELLOW TO BE REMOVED
#
# @router.post("/{wallet_id}/deposit")
# def deposit_to_wallet(
#     wallet_id: str,
#     amount: float,
#     source: str,
#     user: User = Depends(deps.get_user_from_path),
#     db: Session = Depends(deps.get_db),
#     logged_user: User = Depends(deps.get_current_user),
# ):
#     if user != logged_user:
#         raise HTTPException(
#             status_code=403, detail="Cannot deposit to wallets that you don't own"
#         )

#     from_card = crud.card.get(db, source)
#     if not from_card:
#         raise HTTPException(status_code=404, detail="No such card added")

#     wallet = crud.wallet.get_by_owner(db, user, wallet_id)
#     if not wallet:
#         raise HTTPException(status_code=404, detail="No wallet found")

#     return crud.wallet.deposit(db=db, wallet=wallet, amount=amount, card=from_card)


# @router.post("/{wallet_id}/tansfer")
# def transfer_to_wallet(
#     wallet_id: str,
#     amount: float,
#     target: str,
#     fcurr: Optional[str],
#     tcurr: Optional[str],
#     confirm: Optional[bool],
#     interval: Optional[str],
#     user: User = Depends(deps.get_user_from_path),
#     db: Session = Depends(deps.get_db),
#     logged_user: User = Depends(deps.get_current_user),
# ):
#     """
#     Transfer an amount from a wallet to another.

#     Args:
#         wallet_id - wallet to send from
#         amount - amount for the transfer
#         target - id of the wallet to receive
#         fcurr - sending wallet currency (BGN | EUR | USD ...)
#         tcurr - receiving wallet currency (BGN | EUR | USD ...)
#         confirm - confirm currency exchange (True | False)
#         user - sending user
#         interval - the interval of a recurring transaction (month | year)
#     """

#     if user != logged_user:
#         raise HTTPException(
#             status_code=403, detail="Cannot transfer from wallets that you don't own"
#         )

#     to_wallet = crud.card.get(db, target)
#     if not to_wallet:
#         raise HTTPException(status_code=404, detail="No target wallet found")

#     from_wallet = crud.wallet.get_by_owner(db, user, wallet_id)
#     if not from_wallet:
#         raise HTTPException(status_code=404, detail="No wallet found")

#     # create transaction object

#     if not fcurr != tcurr and not confirm:
#         raise HTTPException(status_code=400)

#     # use exchange util to exchange the amount

#     if interval:
#         pass

#     return crud.wallet.transfer(
#         db=db, from_wallet=from_wallet, amount=amount, to_wallet=to_wallet
#     )
#
#
### CODE ABOVE TO BE REMOVED
