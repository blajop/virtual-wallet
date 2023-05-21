from unittest.mock import Mock
from fastapi import HTTPException
import pytest
from sqlmodel import Session
from app.api.api_v1.endpoints import users
from app.models.user import User, UserCreate
from fastapi import BackgroundTasks
from app.utils import util_mail
from app.core.config import settings

BACKGROUND_TASKS = Mock(spec=BackgroundTasks)
BACKGROUND_TASKS.add_task = lambda a, b, c: None


def test_get_users(db: Session) -> None:
    all_users = users.get_users(db)

    assert len(all_users) > 1
    assert isinstance(all_users, list)
    for item in all_users:
        assert isinstance(item, User)


def test_get_profile(db: Session):
    # test get_user endpoint
    test_user = users.get_user(settings.ADMIN_TEST_USERNAME, db)

    with pytest.raises(HTTPException) as exc_info:
        users.get_user("doesntexist", db)

    # test get_profile endpoint
    profile_info = users.profile_info(logged_user=test_user)

    assert test_user
    assert exc_info.value.status_code == 404
    assert profile_info
    assert profile_info.username == settings.ADMIN_TEST_USERNAME


def test_get_profile_raise_when_not_logged():
    with pytest.raises(HTTPException) as exc_info:
        users.profile_info(logged_user=None)

    assert exc_info.value.status_code == 401


def test_register_user(db: Session):
    new_user = UserCreate(
        username="New",
        email="test_user@example.com",
        phone="0888888888",
        f_name="Created",
        l_name="User",
        password="Asdfghjkl_1",
    )

    new_user_with_taken_data = UserCreate(
        username="New",
        email="test_user@example.com",
        phone="0888888888",
        f_name="Created2",
        l_name="User2",
        password="Asdfghjkl_1",
    )

    user = users.sign_up_user(
        db=db, background_tasks=BACKGROUND_TASKS, new_user=new_user, logged_user=None
    )
    # test if a user is logged in and tries to access register endpoint
    with pytest.raises(HTTPException) as exc_info:
        users.sign_up_user(
            db=db,
            background_tasks=BACKGROUND_TASKS,
            new_user=new_user,
            logged_user=new_user,
        )
    # test if user data is taken
    with pytest.raises(HTTPException) as data_info:
        users.sign_up_user(
            db=db,
            background_tasks=BACKGROUND_TASKS,
            new_user=new_user_with_taken_data,
            logged_user=None,
        )

    assert user
    assert isinstance(user, User)
    assert user.username == "New"
    assert exc_info.value.status_code == 403
    assert data_info.value.status_code == 409


# def test_admin_user_inDB(db: Session):
#     all_users = users.get_users(db)
#     admin = users.get_user("admin_id", db)
#     user = users.get_user("user_id", db)
#     assert admin.username == "adminTest"
#     assert "user" in [sc.scope for sc in admin.scopes]
#     assert "admin" in [sc.scope for sc in admin.scopes]
#     assert user.username == "userTest"
#     assert "user" in [sc.scope for sc in user.scopes]
#     assert "admin" not in [sc.scope for sc in user.scopes]


def test_verify_email(db: Session):
    # generate a token
    new_user = UserCreate(
        username="verifyMail",
        email="verify_test@example.com",
        phone="0888822222",
        f_name="Created",
        l_name="User",
        password="Asdfghjkl_1",
    )

    token = util_mail.generate_email_link_token(new_user.email)

    user = users.sign_up_user(
        db=db, background_tasks=BACKGROUND_TASKS, new_user=new_user, logged_user=None
    )

    users.verify_email(token, db=db)
    # Test corrupted token
    with pytest.raises(HTTPException) as exc_info:
        users.verify_email("fake_token", db=db)

    assert user
    assert user.email_confirmed == True
    assert exc_info.value.status_code == 404
