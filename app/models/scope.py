# from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.user import User
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class UserScopeLink(SQLModel, table=True):
    __tablename__ = "users_scopes"
    user_id: str = Field(foreign_key="users.id", primary_key=True)
    scope_id: int = Field(foreign_key="scopes.id", primary_key=True)


class Scope(SQLModel, table=True):
    __tablename__ = "scopes"
    id: Optional[int] = Field(primary_key=True)
    scope: str
    users: List["User"] = Relationship(
        back_populates="scopes", link_model=UserScopeLink
    )
