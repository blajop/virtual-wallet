from __future__ import annotations
from fastapi import HTTPException
from sqlmodel import Session, or_
from app.data import engine
from app.core import security
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from operator import itemgetter
from app import utils
from app import models_temp
import app


def get_users():
    with Session(engine) as session:
        result = session.exec(
            select(models_temp.User).options(
                selectinload(models_temp.User.scopes),
                selectinload(models_temp.User.wallets),
                selectinload(models_temp.User.friends),
                selectinload(models_temp.User.cards),
            ),
        )
        users = result.unique().scalars().all()
        attribute_names = models_temp.User.__table__.columns.keys() + [
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


def register_user(new_user: models_temp.UserRegistration):
    if not user_data_taken(new_user):
        user_orm = models_temp.User.from_orm(new_user)
        user_orm.id = utils.util_id.generate_id()
        user_orm.password = app.core.security.get_password_hash(user_orm.password)
        with Session(engine) as session:
            session.add(user_orm)
            default_scopes = session.scalar(
                select(models_temp.Scope).filter(models_temp.Scope.id == 2)
            )
            user_orm.scopes.append(default_scopes)
            # session.add(user_orm)
            session.commit()
            session.refresh(user_orm)
        return user_orm


def search_by_unique(param: str | None = None):
    with Session(engine) as session:
        if param:
            result = session.scalar(
                select(models_temp.User).filter(
                    or_(
                        models_temp.User.username == param,
                        models_temp.User.email == param,
                        models_temp.User.phone == param,
                    )
                )
            )
        else:
            result = session.scalar(select(models_temp.User))
        return result


def user_data_taken(user: models_temp.UserRegistration):
    with Session(engine) as session:
        result = session.scalar(
            select(models_temp.User).filter(models_temp.User.username == user.username)
        )
        if result:
            raise HTTPException(status_code=409, detail="Username is already taken")

        result = session.scalar(
            select(models_temp.User).filter(models_temp.User.email == user.email)
        )
        if result:
            raise HTTPException(status_code=409, detail="Email is already taken")

        result = session.scalar(
            select(models_temp.User).filter(models_temp.User.phone == user.phone)
        )
        if result:
            raise HTTPException(status_code=409, detail="Phone number is already taken")

    return False
