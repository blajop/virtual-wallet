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


from app.tests.utils.utils import random_user
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


@pytest.fixture(name="user")
def user_fixture(session: Session):
    yield random_user(session)


@pytest.fixture(name="client")
def client_fixture(session: Session, user: User):
    def get_session_override():
        return session

    def get_user_override():
        return user

    app.dependency_overrides[deps.get_db] = get_session_override
    app.dependency_overrides[deps.get_current_user] = get_user_override

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

        admin = random_user(session)
        admin.scopes.append(scope_u)
        admin.scopes.append(scope_a)

        user = random_user(session)
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
