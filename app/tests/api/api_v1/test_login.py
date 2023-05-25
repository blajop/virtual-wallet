from typing import Callable
from unittest.mock import Mock
from fastapi import Depends, HTTPException
from pydantic import parse_obj_as
import pytest
from sqlmodel import Session, select
from app import crud
from app.api import deps
from app.tests.utils.utils import random_usercreate
from main import app
from app.models.user import User, UserCreate, UserResetPass
from app.api.api_v1.endpoints import users, login
from fastapi import BackgroundTasks
from app.utils import util_mail
from app.core.config import settings
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import get_password_hash
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder as js

BACKGROUND_TASKS = Mock(spec=BackgroundTasks)
BACKGROUND_TASKS.add_task = lambda func, email_to, email, token: None


def override_oauth2_form():
    form_data = OAuth2PasswordRequestForm(
        username=settings.USER_TEST_USERNAME,
        password=settings.USER_TEST_PASSWORD,
        scope="",
    )

    return form_data


def override_oauth2_wrong_form():
    form_data = OAuth2PasswordRequestForm(
        username=settings.USER_TEST_USERNAME,
        password="greshka",
        scope="",
    )

    return form_data


def test_get_access_token(client: TestClient):
    app.dependency_overrides[OAuth2PasswordRequestForm] = override_oauth2_form
    response = client.post("/api/v1/login/access-token")

    assert response.status_code == 200
    assert b"access_token" in response.content

    app.dependency_overrides[OAuth2PasswordRequestForm] = override_oauth2_wrong_form
    bad_login = client.post("/api/v1/login/access-token")

    assert bad_login.status_code == 400
    assert b"access_token" not in bad_login.content


def test_refer_friend(client: TestClient, user):
    app.dependency_overrides[deps.get_current_user] = user
    new_email = "testrefermail@gmail.com"
    existing_email = settings.USER_TEST_EMAIL
    # success
    response = client.post(f"/api/v1/refer?email={new_email}")
    assert response.status_code == 200
    #
    response = client.post(f"/api/v1/refer?email={existing_email}")
    assert response.status_code == 400


def test_register_user(client: TestClient):
    new_user = random_usercreate()

    another_user = random_usercreate()
    another_user.username = new_user.username
    # success
    response = client.post(f"/api/v1/signup", json=js(new_user))
    assert response.status_code == 200
    # data taken
    taken_user = client.post(f"/api/v1/signup", json=js(new_user))
    assert taken_user.status_code == 409
    # if referrer
    referrer_mail = settings.ADMIN_TEST_EMAIL
    referrer_token = util_mail.generate_email_link_token(referrer_mail)

    taken_user = client.post(
        f"/api/v1/signup?referrer={referrer_token}", json=js(new_user)
    )
    # referrer logic needs to be implemented


def test_verify_mail(client: TestClient, user):
    user: User = user()
    verify_token = util_mail.generate_email_link_token(user.email)
    assert user.email_confirmed == False
    response = client.get(f"/api/v1/verify/{verify_token}")

    assert response.status_code == 200
    assert user.email_confirmed == True

    response = client.get(f"/api/v1/verify/fake_token")
    assert response.status_code == 404


def test_recover_password(client: TestClient):
    response = client.post(f"/api/v1/password-recovery/{settings.USER_TEST_EMAIL}")
    assert response.status_code == 200

    no_user = client.post(f"/api/v1/password-recovery/fake_email")
    assert no_user.status_code == 404


def test_reset_password(client: TestClient, session: Session):
    user = session.exec(
        select(User).where(User.username == settings.ADMIN_TEST_USERNAME)
    ).first()
    old_password = user.password

    new_pass = UserResetPass(
        new_password="new_passw0rD", verify_password="new_passw0rD"
    )

    token = util_mail.generate_email_link_token(email=user.email)

    # success
    response = client.put(f"/api/v1/reset-password?token={token}", json=js(new_pass))
    user_after = session.exec(
        select(User).where(User.username == settings.ADMIN_TEST_USERNAME)
    ).first()
    assert response.status_code == 200
    assert old_password != user_after.password

    # user with such email not found
    token_for_non_existent_user = util_mail.generate_email_link_token(
        email="notRegistered@example.com"
    )
    response_for_non_registered = client.put(
        f"/api/v1/reset-password?token={token_for_non_existent_user}", json=js(new_pass)
    )
    assert response_for_non_registered.status_code == 404

    # broken token
    response_broken_token = client.put(
        f"/api/v1/reset-password?token=as324fdsaa", json=js(new_pass)
    )
    assert response_broken_token.status_code == 400

    # passwords dont match
    not_match = UserResetPass(
        new_password="new_passw0rD", verify_password="N0t_matching"
    )
    response_broken_token = client.put(
        f"/api/v1/reset-password?token=as324fdsaa", json=js(not_match)
    )
    assert response_broken_token.status_code == 400
