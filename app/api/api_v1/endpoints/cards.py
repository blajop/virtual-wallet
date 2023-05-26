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
    result = crud.card.get(db, card_identifier, logged_user)

    if not result:
        raise HTTPException(
            status_code=404, detail="There is no such card within your access"
        )
    return result


@router.get("", response_model=list[Card])
def get_cards(
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    return crud.card.get_multi(db, skip=skip, limit=limit, user=logged_user)


@router.post("", response_model=CardShow)
def add_card(
    new_card: CardCreate,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    try:
        return crud.card.add_card(db, logged_user, new_card)
    except CardDataError as err:
        raise HTTPException(status_code=400, detail=err.args[0])


@router.delete("/{card_identifier}", status_code=204)
def deregister_card(
    card_identifier,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    try:
        crud.card.deregister_card(db, card_identifier, logged_user)
    except CardNotFoundError as err:
        raise HTTPException(status_code=404, detail=err.args[0])
