from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from app.models import User

from sqlmodel import Field, Relationship, SQLModel


class UserScopeLink(SQLModel, table=True):
    __tablename__ = "users_scopes"
    user_id: Optional[str] = Field(foreign_key="users.id", primary_key=True)
    scope_id: Optional[int] = Field(foreign_key="scopes.id", primary_key=True)


class Scope(SQLModel, table=True):
    __tablename__ = "scopes"
    id: Optional[int] = Field(primary_key=True)
    scope: str
    users: List["User"] = Relationship(
        back_populates="scopes", link_model=UserScopeLink
    )
