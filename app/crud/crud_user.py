from __future__ import annotations
from fastapi import HTTPException
from sqlmodel import Session, or_
from app.crud.base import CRUDBase
from app.data import engine
from app.core import security
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from operator import itemgetter
from app import utils
from app.core import security
from app.models.scope import Scope
from app.models.user import User, UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, new_user: UserCreate):
        if not self.user_data_taken(new_user):
            user_orm = User.from_orm(new_user)
            user_orm.id = utils.util_id.generate_id()
            user_orm.password = security.get_password_hash(user_orm.password)

            db.add(user_orm)
            db.commit()
            db.refresh(user_orm)

            return user_orm

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in

        if update_data["password"]:
            hashed_password = security.get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def user_data_taken(self, db: Session, user: UserCreate):
        with Session(engine) as session:
            result = session.scalar(select(User).filter(User.username == user.username))
            if result:
                raise HTTPException(status_code=409, detail="Username is already taken")

            result = session.scalar(select(User).filter(User.email == user.email))
            if result:
                raise HTTPException(status_code=409, detail="Email is already taken")

            result = session.scalar(select(User).filter(User.phone == user.phone))
            if result:
                raise HTTPException(
                    status_code=409, detail="Phone number is already taken"
                )

        return False
