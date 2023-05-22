from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from app.core.config import settings
from app.models.scope import Scope
from app.models.user import User, UserCreate
from main import app
from app.core.security import get_password_hash

from app.tests.utils.utils import random_user
from app.utils import util_id


engine = create_engine("sqlite:///:memory:", echo=True)


def create_tables():
    SQLModel.metadata.create_all(bind=engine)


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
            id="admin_id",
            username=settings.ADMIN_TEST_USERNAME,
            email=settings.ADMIN_TEST_EMAIL,
            phone="0987654321",
            f_name="Admin",
            l_name="Adminov",
            password=get_password_hash(settings.ADMIN_TEST_PASSWORD),
        )
        admin.scopes.append(scope_u)
        admin.scopes.append(scope_a)

        user = User(
            id="user_id",
            username=settings.USER_TEST_USERNAME,
            email=settings.USER_TEST_EMAIL,
            phone="1234567890",
            f_name="User",
            l_name="Userov",
            password=get_password_hash(settings.USER_TEST_PASSWORD),
        )
        user.scopes.append(scope_u)

        session.add_all([admin, user])
        session.commit()


@pytest.fixture(scope="session")
def db() -> Generator:
    with Session(engine) as session:
        create_tables()
        fill_scopes(session)
        fill_basic_users(session)
        yield session


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def user(db: Session) -> User:
    return random_user(db)


# @pytest.fixture(scope="module")
# def superuser_token_headers(client: TestClient) -> Dict[str, str]:
#     return get_superuser_token_headers(client)


# @pytest.fixture(scope="module")
# def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
#     return authentication_token_from_email(
#         client=client, email=settings.EMAIL_TEST_USER, db=db
#     )
