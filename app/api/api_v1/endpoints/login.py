from datetime import timedelta
from typing import Any

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import UserResetPass
from app.utils import util_mail

router = APIRouter()


@router.post("/login/access-token", response_model=models.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.username, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=models.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=models.Msg)
def recover_password(
    email: str, background: BackgroundTasks, db: Session = Depends(deps.get_db)
) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get(db, user=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User with this email does not exist in the system.",
        )
    password_reset_token = util_mail.generate_email_link_token(email=email)

    background.add_task(
        util_mail.send_reset_password_email,
        email_to=user.email,
        email=email,
        token=password_reset_token,
    )
    return {"msg": "Password recovery email sent"}


# the frontend needs to come here
@router.post("/reset-password/", response_model=models.Msg)
def reset_password(
    info: UserResetPass,
    token: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    if info.new_password != info.verify_password:
        raise HTTPException(status_code=400, detail="Passwords don't match")

    email = util_mail.verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get(db, user=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )

    user.password = get_password_hash(info.new_password)
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}
