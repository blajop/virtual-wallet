from __future__ import annotations
from fastapi import HTTPException
from app.models import User, UserRegistration
from sqlmodel import Session
from sqlalchemy import or_, select
from app.data import engine
from app.auth import auth
from app.helpers import snowflake_ids as sf
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import selectinload, joinedload, contains_eager


def get_users():
    with Session(engine) as session:
        result = session.exec(select(User).options(contains_eager(User.scopes)))
        # find the right option
        return result.all()


# def register_user(new_user: UserRegistration):
#     if not user_data_taken(new_user):
#         new_user.id = sf.generate_id()
#         new_user.password = auth.get_password_hash(new_user.password)
#         with Session(engine) as session:
#             session.add(UserORM(**new_user.__dict__))
#             session.commit()
#         return new_user


# def search(param: str | None = None):
#     with Session(engine) as session:
#         result = session.scalar(
#             select(UserORM).filter(
#                 or_(
#                     UserORM.username == param,
#                     UserORM.email == param,
#                     UserORM.phone == param,
#                 )
#             )
#         )
#         return UserExtended.from_orm(result)


# def user_data_taken(user: UserRegistration):
#     with Session(engine) as session:
#         result = session.scalar(
#             select(UserORM).filter(UserORM.username == user.username)
#         )
#         if result:
#             raise HTTPException(status_code=409, detail="Username is already taken")

#         result = session.scalar(select(UserORM).filter(UserORM.email == user.email))
#         if result:
#             raise HTTPException(status_code=409, detail="Email is already taken")

#         result = session.scalar(select(UserORM).filter(UserORM.phone == user.phone))
#         if result:
#             raise HTTPException(status_code=409, detail="Phone number is already taken")

#     return False
