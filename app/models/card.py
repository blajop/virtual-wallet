import datetime
from typing import Optional
from pydantic import constr
from sqlmodel import Field, Relationship, SQLModel


class UserCardLink(SQLModel, table=True):
    __tablename__ = "cards_users"
    user_id: str = Field(foreign_key="users.id", primary_key=True)
    card_id: str = Field(foreign_key="cards.id", primary_key=True)


class Card(SQLModel, table=True):
    __tablename__ = "cards"
    id: Optional[str] = Field(primary_key=True)
    number: constr(regex="^\d{16}$") = Field(unique=True)
    expiry: datetime
    holder: constr(min_length=2, max_length=30)
    cvc: constr(regex="^\d{3}$")
    users: User = Relationship(back_populates="cards", link_model=UserCardLink)
