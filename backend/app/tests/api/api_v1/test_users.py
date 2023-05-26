from fastapi.testclient import TestClient
from app.models.user import User, UserBase, UserUpdate
from app.api import deps
from main import app
from fastapi.encoders import jsonable_encoder


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


def test_update_profile(client: TestClient, user):
    app.dependency_overrides[deps.get_current_user] = user
    user: User = user()

    new_data = UserUpdate(
        email="newmail@asd.dd",
        phone="0888664853",
        f_name="NewName",
        l_name="NewLast",
        password="N3w_passW",
    )

    old_user_info = client.get(f"/api/v1/users/profile")
    old_data = old_user_info.json()

    updated_info = client.put(f"/api/v1/users/profile", json=jsonable_encoder(new_data))

    assert updated_info.status_code == 200
    assert old_user_info != updated_info
    assert updated_info.json().get("email") != old_data.get("email")
    assert updated_info.json().get("phone") != old_data.get("phone")
    assert updated_info.json().get("f_name") != old_data.get("f_name")
    assert updated_info.json().get("l_name") != old_data.get("l_name")
    assert updated_info.json().get("password") != old_data.get("password")


def test_friend(client: TestClient, user, admin):
    app.dependency_overrides[deps.get_current_user] = user

    main_user: User = user()
    friend: User = admin()
    assert main_user.friends == []

    # Add successfully
    response = client.post(f"/api/v1/users/{main_user.username}/friends?id={friend.id}")
    assert response.status_code == 200
    assert main_user.friends == [friend]

    # Get successfully
    response = client.get(f"/api/v1/users/{main_user.username}/friends")
    assert response.status_code == 200
    assert main_user.friends == [friend]

    # Raise 403 if tryint to get/add other user's friends
    response_add = client.post(
        f"/api/v1/users/{friend.username}/friends?id={friend.id}"
    )
    response_get = client.get(f"/api/v1/users/{friend.username}/friends")

    assert response_add.status_code == 403
    assert response_get.status_code == 403

    # Raise 409 if user is already in you contact list
    response = client.post(f"/api/v1/users/{main_user.username}/friends?id={friend.id}")
    assert response.status_code == 409

    # Raise 403 if trying to remove other user's friends
    app.dependency_overrides[deps.get_current_user] = admin
    response = client.delete(
        f"/api/v1/users/{main_user.username}/friends?id={friend.id}"
    )
    assert response.status_code == 403

    app.dependency_overrides[deps.get_current_user] = user
    # Remove friend successfully
    assert main_user.friends == [friend]
    response = client.delete(
        f"/api/v1/users/{main_user.username}/friends?id={friend.id}"
    )
    assert main_user.friends == []
    assert response.status_code == 204

    # Raise 404 if no such user in friend list
    response = client.delete(
        f"/api/v1/users/{main_user.username}/friends?id={friend.id}"
    )
    assert response.status_code == 404
