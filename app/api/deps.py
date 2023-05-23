from fastapi import Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from app.models import User, TokenPayload
from app.core import settings
from app.db import engine
from app import crud

from sqlmodel import Session
from jose import jwt


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
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
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, identifier=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
