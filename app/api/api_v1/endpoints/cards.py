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
        raise HTTPException(status_code=404)
    return result


@router.post("", response_model=CardShow | Msg)
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


@router.delete("/{card_identifier}", status_code=204)
def remove_card(
    card_identifier,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    try:
        crud.card.remove(db, card_identifier, logged_user)
    except CardNotFoundError as err:
        raise HTTPException(status_code=404, detail=err.args[0])
