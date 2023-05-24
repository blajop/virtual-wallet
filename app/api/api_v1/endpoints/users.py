from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import crud, deps
from app.models import User, UserBase

router = APIRouter()


@router.get("", response_model=list[User])
def get_users(
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    return crud.user.get_multi(db)


@router.get("/profile", response_model=User)
def profile_info(logged_user: User = Depends(deps.get_current_user)):
    return logged_user


@router.get("/{identifier}", response_model=UserBase)
def get_user(
    identifier: str,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    """
    Returns a User model from username, email or id search
    """
    user = crud.user.get(db, identifier)

    if not user:
        raise HTTPException(status_code=404)
    return user
