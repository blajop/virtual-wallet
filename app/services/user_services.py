from fastapi import HTTPException
from app.models import UserRegistration, UserORM
from sqlalchemy.orm import Session
from sqlalchemy import insert
from sqlalchemy import exc
from app.data import engine
from app.auth import auth


def register_user(new_user: UserRegistration):
    new_user.id = "asdASD"
    new_user.password = auth.get_password_hash(new_user.password)
    try:
        with Session(engine) as session:
            session.add(UserORM(**new_user.__dict__))
            session.commit()
        return new_user
    except exc.IntegrityError:
        raise HTTPException(status_code=409, detail="Username, phone or email taken")
