from __future__ import annotations
from fastapi import HTTPException
from app.models import Scope, User, UserRegistration
from sqlmodel import Session, or_
from app.data import engine
from app.core import security
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from operator import itemgetter


def get_users():
    with Session(engine) as session:
        result = session.exec(
            select(User).options(
                selectinload(User.scopes),
                selectinload(User.wallets),
                selectinload(User.friends),
                selectinload(User.cards),
            ),
        )
        users = result.unique().scalars().all()
        attribute_names = User.__table__.columns.keys() + [
            "scopes",
            "wallets",
            "cards",
            "friends",
        ]

        user_dicts = [
            dict(zip(attribute_names, itemgetter(*attribute_names)(user.__dict__)))
            for user in users
        ]

        return user_dicts


def register_user(new_user: UserRegistration):
    if not user_data_taken(new_user):
        user_orm = User.from_orm(new_user)
        user_orm.id = sf.generate_id()
        user_orm.password = auth.get_password_hash(user_orm.password)
        with Session(engine) as session:
            session.add(user_orm)
            default_scopes = session.scalar(select(Scope).filter(Scope.id == 2))
            user_orm.scopes.append(default_scopes)
            # session.add(user_orm)
            session.commit()
            session.refresh(user_orm)
        return user_orm


def search_by_unique(param: str | None = None):
    with Session(engine) as session:
        if param:
            result = session.scalar(
                select(User).filter(
                    or_(
                        User.username == param,
                        User.email == param,
                        User.phone == param,
                    )
                )
            )
        else:
            result = session.scalar(select(User))
        return result


def user_data_taken(user: UserRegistration):
    with Session(engine) as session:
        result = session.scalar(select(User).filter(User.username == user.username))
        if result:
            raise HTTPException(status_code=409, detail="Username is already taken")

        result = session.scalar(select(User).filter(User.email == user.email))
        if result:
            raise HTTPException(status_code=409, detail="Email is already taken")

        result = session.scalar(select(User).filter(User.phone == user.phone))
        if result:
            raise HTTPException(status_code=409, detail="Phone number is already taken")

    return False
