from typing import Generator

from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlmodel import Session
from app import models
from app.core import security
from fastapi import Depends, HTTPException, status
from app.core.config import settings
from app.db.session import SessionLocal
from fastapi.security import OAuth2PasswordBearer
import crud

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = models.token.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(
        db, id=token_data.sub
    )  # refactor when we add the crud operation
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
