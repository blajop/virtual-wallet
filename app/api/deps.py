from typing import Generator, Optional
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError
from sqlmodel import Session
from app.core import security, security_copy
from fastapi import Depends, HTTPException, status
from app.core.config import settings
from app.db.session import engine
from fastapi.security import OAuth2PasswordBearer
from app import crud
from app import models


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login/access-token",
    auto_error=False,
)


def get_db():
    with Session(engine) as session:
        yield session


def get_current_user(
    db: Session = Depends(get_db), token: Optional[str] = Depends(reusable_oauth2)
) -> Optional[models.User]:
    if not token:
        return None
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
    user = security_copy.get_user(token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
