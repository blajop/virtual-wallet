from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    user_id: str
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    scopes: list[int] = []
