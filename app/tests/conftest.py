from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, select, create_engine
from main import app
from sqlmodel.pool import StaticPool

from app import crud, deps

from app.core.config import settings
from app.models.scope import Scope
from app.models.user import User, UserCreate
from app.core.security import get_password_hash


from app.tests.utils.utils import random_user, random_admin
from app.utils import util_id


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session_init:
        fill_scopes(session_init)
        fill_basic_users(session_init)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="guest")
def guest_fixture():
    def get_guest_override():
        return None

    return get_guest_override


@pytest.fixture(name="user")
def user_fixture(session: Session):
    user = session.exec(
        select(User).filter(User.username == settings.USER_TEST_USERNAME)
    ).first()

    def get_user_override():
        return user

    return get_user_override


@pytest.fixture(name="admin")
def admin_fixture(session: Session):
    admin = session.exec(
        select(User).filter(User.username == settings.ADMIN_TEST_USERNAME)
    ).first()

    def get_admin_override():
        return admin

    return get_admin_override


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[deps.get_db] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def fill_scopes(session: Session):
    with session:
        scopes = [
            Scope(id=1, scope="guest"),
            Scope(id=2, scope="user"),
            Scope(id=3, scope="admin"),
        ]

        session.add_all(scopes)
        session.commit()


def fill_basic_users(session: Session):
    with session:
        scope_a = session.exec(select(Scope).filter(Scope.id == 3)).first()
        scope_u = session.exec(select(Scope).filter(Scope.id == 2)).first()

        admin = User(
            username=settings.ADMIN_TEST_USERNAME,
            email=settings.ADMIN_TEST_EMAIL,
            phone=settings.ADMIN_TEST_PHONE,
            f_name=settings.ADMIN_TEST_FNAME,
            l_name=settings.ADMIN_TEST_LNAME,
            id=util_id.generate_id(),
            password=get_password_hash(settings.ADMIN_TEST_PASSWORD),
        )
        admin.scopes.append(scope_u)
        admin.scopes.append(scope_a)

        user = User(
            username=settings.USER_TEST_USERNAME,
            email=settings.USER_TEST_EMAIL,
            phone=settings.USER_TEST_PHONE,
            f_name=settings.USER_TEST_FNAME,
            l_name=settings.USER_TEST_LNAME,
            id=util_id.generate_id(),
            password=get_password_hash(settings.USER_TEST_PASSWORD),
        )
        user.scopes.append(scope_u)

        session.add_all([admin, user])
        session.commit()


# @pytest.fixture(scope="session")
# def db() -> Generator:
#     with Session(engine) as session:
#         create_tables()
#         fill_scopes(session)
#         fill_basic_users(session)
#         yield session


# @pytest.fixture(scope="module")
# def client() -> Generator:
#     with TestClient(app) as c:
#         yield c


# @pytest.fixture(scope="module")
# def user(db: Session) -> User:
#     return random_user(db)


# @pytest.fixture(scope="module")
# def superuser_token_headers(client: TestClient) -> Dict[str, str]:
#     return get_superuser_token_headers(client)


# @pytest.fixture(scope="module")
# def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
#     return authentication_token_from_email(
#         client=client, email=settings.EMAIL_TEST_USER, db=db
#     )
