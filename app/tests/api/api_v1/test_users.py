from unittest.mock import Mock
from fastapi.testclient import TestClient
from app.api import deps
from app.models.user import User, UserBase
from fastapi import BackgroundTasks
from main import app


def test_get_users(client: TestClient, user) -> None:
    app.dependency_overrides[deps.get_current_user] = user

    response = client.get("/api/v1/users")
    content = response.json()

    assert response.status_code == 200
    assert len(content) > 1
    for u in content:
        assert isinstance(User(**u), User)


def test_get_one_user(client: TestClient, user) -> None:
    app.dependency_overrides[deps.get_current_user] = user
    user: User = user()

    response = client.get(f"/api/v1/users/{user.id}")
    content = response.json()

    assert response.status_code == 200
    assert len([content]) == 1
    assert UserBase(**content) == UserBase.from_orm(user)

    # If user not found
    response = client.get(f"/api/v1/users/fakeUser")
    assert response.status_code == 404


def test_get_profile(client: TestClient, user):
    app.dependency_overrides[deps.get_current_user] = user
    user: User = user()

    response = client.get(f"/api/v1/users/profile")
    content = response.json()

    assert response.status_code == 200
    assert len([content]) == 1
    assert User(**content) == user
