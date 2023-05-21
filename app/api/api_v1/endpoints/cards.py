from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Response,
)
from sqlmodel import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app import crud
import app
from app import utils
from app.api import deps
from app.error_models.card_errors import CardDataError
from app.error_models.user_errors import DataTakenError
from app.models.card import Card, CardCreate, CardShow
from app.models.msg import Msg
from app.models.user import User, UserBase, UserCreate
from app.utils import util_mail

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
