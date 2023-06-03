from datetime import timedelta
from typing import Annotated, Any, Optional

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, deps
from app.core import security, settings
from app.core.security import get_password_hash
from app.error_models import DataTakenError
from app.models import User, UserBase, UserCreate, UserResetPass
from app.utils import util_mail

router = APIRouter()


@router.post("/login/access-token", response_model=models.Token)
def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(deps.get_db),
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
        "user_id": user.id,
        "access_token": security.create_access_token(
            user.username, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/refer")
def refer_friend(
    email: str,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    return crud.user.refer_friend(user=logged_user, email=email, db=db)


@router.post("/signup", response_model=UserBase)
def sign_up(
    new_user: UserCreate,
    background_tasks: BackgroundTasks,
    referrer: Optional[str] = None,
    db: Session = Depends(deps.get_db),
):
    # referrer should lose a refer spot in his UserSettings
    if referrer:
        referrer_mail = util_mail.verify_email_link_token(referrer)
        referrer = crud.user.get(db, identifier=referrer_mail)
    # if not more spots, dont give them money
    try:
        registered_user = crud.user.create(db, new_user, referrer)
    except DataTakenError as err:
        raise HTTPException(status_code=409, detail=err.args[0])

    background_tasks.add_task(
        util_mail.send_new_account_email,
        registered_user.email,
        registered_user.username,
    )

    return registered_user


@router.get("/username-unique/{username}")
def verify_data_not_taken(
    username: str,
    db: Session = Depends(deps.get_db),
):
    try:
        return crud.user.username_taken(db, username=username)
    except DataTakenError as err:
        raise HTTPException(status_code=409, detail=err.args[0])


@router.get("/email-unique/{email}")
def verify_data_not_taken(
    email: str,
    db: Session = Depends(deps.get_db),
):
    try:
        return crud.user.email_taken(db, email=email)
    except DataTakenError as err:
        raise HTTPException(status_code=409, detail=err.args[0])


@router.get("/phone-unique/{phone}")
def verify_data_not_taken(
    phone: str,
    db: Session = Depends(deps.get_db),
):
    try:
        return crud.user.phone_taken(db, phone=phone)
    except DataTakenError as err:
        raise HTTPException(status_code=409, detail=err.args[0])


@router.get("/verify/{token}")
def verify_email(token, db: Session = Depends(deps.get_db)):
    user_email = util_mail.verify_email_link_token(token)
    user = crud.user.get(db, user_email)

    if not user:
        raise HTTPException(status_code=404, detail="Token user not found")

    return crud.user.confirm_email(db, db_obj=user)


@router.post("/password-recovery/{email}", response_model=models.Msg)
def recover_password(
    email: str, background: BackgroundTasks, db: Session = Depends(deps.get_db)
) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get(db, identifier=email)

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
@router.put("/reset-password", response_model=models.Msg)
def reset_password(
    info: UserResetPass,
    token: str = ...,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    if info.new_password != info.verify_password:
        raise HTTPException(status_code=400, detail="Passwords don't match")

    email = util_mail.verify_email_link_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get(db, identifier=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )

    user.password = get_password_hash(info.new_password)
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}
