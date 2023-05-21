from typing import Generator, Optional
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlmodel import Session
from app.core import security
from fastapi import Depends, HTTPException, Path, status
from app.core.config import settings
from app.db.session import engine
from fastapi.security import OAuth2PasswordBearer
from app import crud
from app import models
from app.models.user import User


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
    auto_error=False,
)


def get_db():
    with Session(engine) as session:
        yield session


def get_user_from_path(identifier: str = Path(), db: Session = Depends(get_db)):
    user: User = crud.user.get(db, identifier)

    if not user:
        raise HTTPException(
            status_code=404, detail="User with such identifier does not exist!"
        )
    return user


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = models.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, user=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
