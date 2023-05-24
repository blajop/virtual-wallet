from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.error_models import CardDataError, CardNotFoundError
from app.models import Card, CardCreate, CardShow, Msg, User
from app import crud, deps

router = APIRouter()


@router.get("/{card_identifier}", response_model=Card)
def get_card(
    card_identifier: str,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if not logged_user:
        raise HTTPException(status_code=401, detail="You should be logged in")

    result = crud.card.get(db, card_identifier, logged_user)

    if not result:
        raise HTTPException(
            status_code=404, detail="There is no such card within your access"
        )
    return result


@router.post("", response_model=CardShow)
def add_card(
    new_card: CardCreate,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if not logged_user:
        raise HTTPException(status_code=401, detail="You should login first")
    try:
        return crud.card.add_card(db, logged_user, new_card)
    except CardDataError as err:
        raise HTTPException(status_code=400, detail=err.args[0])


@router.delete("/admin-del/{card_identifier}", status_code=204)
def admin_delete_card(
    card_identifier,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if not logged_user:
        raise HTTPException(status_code=401, detail="You should login")
    if not crud.user.is_admin(logged_user):
        raise HTTPException(status_code=403, detail="Admin endpoint")

    try:
        crud.card.remove(db, card_identifier)
    except CardNotFoundError as err:
        raise HTTPException(status_code=404, detail=err.args[0])


@router.delete("/{card_identifier}", status_code=204)
def deregister_card(
    card_identifier,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if not logged_user:
        raise HTTPException(status_code=401, detail="You should login")

    try:
        crud.card.deregister_card(db, card_identifier, logged_user)
    except CardNotFoundError as err:
        raise HTTPException(status_code=404, detail=err.args[0])
