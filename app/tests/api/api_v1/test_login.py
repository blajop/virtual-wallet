from unittest.mock import Mock
from fastapi import HTTPException
import pytest
from sqlmodel import Session
from app import crud
from app.models.user import User, UserCreate, UserResetPass
from app.api.api_v1.endpoints import users, login
from fastapi import BackgroundTasks
from app.utils import util_mail
from app.core.config import settings
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import get_password_hash

BACKGROUND_TASKS = Mock(spec=BackgroundTasks)
BACKGROUND_TASKS.add_task = lambda func, email_to, email, token: None


def test_get_access_token(db: Session):
    form_data = Mock(spec=OAuth2PasswordRequestForm)
    form_data.username = settings.ADMIN_TEST_USERNAME
    form_data.password = settings.ADMIN_TEST_PASSWORD

    token_dict = login.login_access_token(db=db, form_data=form_data)

    # Raise if login info not correct
    form_data.password = "wrong_password"
    with pytest.raises(HTTPException) as exc_info:
        login.login_access_token(db=db, form_data=form_data)

    assert exc_info.value.status_code == 400
    assert token_dict
    assert token_dict.get("access_token")
    assert token_dict.get("token_type")


def test_recover_password(db: Session):
    msg = login.recover_password(
        email=settings.ADMIN_TEST_EMAIL,
        background=BACKGROUND_TASKS,
        db=db,
    )

    with pytest.raises(HTTPException) as exc_info:
        login.recover_password(
            email="wrongMail@example.com",
            background=BACKGROUND_TASKS,
            db=db,
        )

    assert msg["msg"]
    assert exc_info.value.status_code == 404


def test_reset_password(db: Session):
    old_password = get_password_hash(settings.ADMIN_TEST_PASSWORD)

    new_pass = UserResetPass(
        new_password="new_passw0rD", verify_password="new_passw0rD"
    )

    token = util_mail.generate_email_link_token(email=settings.ADMIN_TEST_EMAIL)
    login.reset_password(info=new_pass, token=token, db=db)

    user_in_db = users.get_user(settings.ADMIN_TEST_USERNAME, db=db)

    # RAISES
    non_matching_pass = UserResetPass(
        new_password="new_passw0rD", verify_password="different_P4ssword"
    )
    with pytest.raises(HTTPException) as non_matching:
        login.reset_password(info=non_matching_pass, token=token, db=db)

    with pytest.raises(HTTPException) as invalid_mail:
        login.reset_password(info=new_pass, token="Invalid token", db=db)

    token_for_non_existent_user = util_mail.generate_email_link_token(
        email="notRegistered@example.com"
    )

    with pytest.raises(HTTPException) as non_registered:
        login.reset_password(info=new_pass, token=token_for_non_existent_user, db=db)

    assert user_in_db.password != old_password
    assert non_matching.value.status_code == 400
    assert invalid_mail.value.status_code == 400
    assert non_registered.value.status_code == 404
