from typing import Dict
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.core.config import settings
from app import crud
from app.models.user import User, UserCreate
from app.api.api_v1.endpoints import users


def test_get_users(db: Session) -> None:
    username = "testuser123"
    email = "testuser123@example.com"
    phone = "0123456789"
    f_name = "testuser123"
    l_name = "testuser123"
    password = "Testuser123_"

    user_in = UserCreate(
        username=username,
        email=email,
        phone=phone,
        f_name=f_name,
        l_name=l_name,
        password=password,
    )

    crud.user.create(db, new_user=user_in)

    username2 = "testuser124"
    email2 = "testuser124@example.com"
    phone2 = "0124456789"
    f_name2 = "testuser123"
    l_name2 = "testuser123"
    password2 = "Testuser123_"

    user_in2 = UserCreate(
        username=username2,
        email=email2,
        phone=phone2,
        f_name=f_name2,
        l_name=l_name2,
        password=password2,
    )

    crud.user.create(db, new_user=user_in2)

    # r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)

    all_users = users.get_users(db)

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item.__dict__


def test_admin_user_inDB(db: Session):
    all_users = users.get_users(db)
    admin = users.get_user("admin_id", db)
    user = users.get_user("user_id", db)
    assert admin.username == "adminTest"
    assert "user" in [sc.scope for sc in admin.scopes]
    assert "admin" in [sc.scope for sc in admin.scopes]
    assert user.username == "userTest"
    assert "user" in [sc.scope for sc in user.scopes]
    assert "admin" not in [sc.scope for sc in user.scopes]


# def test_get_profile(
#     client: TestClient,
#     superuser_token_headers: dict,
# ):
#     r = client.get(
#         f"{settings.API_V1_STR}/users/profile", headers=superuser_token_headers
#     )
#     info = r.json()

#     user = User(
#         id=info.get("id"),
#         username=info.get("username"),
#         email=info.get("email"),
#         phone=info.get("phone"),
#         f_name=info.get("f_name"),
#         l_name=info.get("l_name"),
#         password=info.get("password"),
#     )

#     assert user
#     assert info.get("username") == "stanim"


def test_get_profile_raise_when_not_logged(
    client: TestClient,
):
    r = client.get(f"{settings.API_V1_STR}/users/profile")

    assert r.status_code == 401
