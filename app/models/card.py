from typing import TYPE_CHECKING, List
import calendar

from app.error_models.card_errors import CardDataError

if TYPE_CHECKING:
    from app.models.user import User
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, conint, constr, validator
from sqlmodel import Field, Relationship, SQLModel


class UserCardLink(SQLModel, table=True):
    __tablename__ = "cards_users"
    user_id: str = Field(foreign_key="users.id", primary_key=True)
    card_id: str = Field(foreign_key="cards.id", primary_key=True)


class CardBase(SQLModel):
    number: constr(regex="^\d{16}$") = Field(unique=True)
    expiry: datetime
    holder: constr(min_length=2, max_length=30)
    cvc: constr(regex="^\d{3}$")


class Card(CardBase, table=True):
    __tablename__ = "cards"
    id: Optional[str] = Field(default=None, primary_key=True)
    number: str
    cvc: str
    users: List["User"] = Relationship(
        back_populates="cards",
        link_model=UserCardLink,
    )

    def __contains__(self, item: "User") -> bool:
        return item in self.users


class CardShow(SQLModel):
    number: constr(regex="^\d{16}$") = Field(unique=True)
    expiry: str
    holder: constr(min_length=2, max_length=30)


class CardExpiry(BaseModel):
    mm: str
    yyyy: str

    @property
    def datetime_(self):
        datetime_obj = datetime(
            month=int(self.mm),
            year=int(self.yyyy),
            day=calendar.monthrange(int(self.yyyy), int(self.mm))[1],
            hour=23,
            minute=59,
            second=59,
        )
        if datetime_obj < datetime.utcnow():
            raise CardDataError("Your card is expired")
        return datetime_obj

    @validator("mm")
    def validate_mm(cls, val: str):
        val = val.strip("0")
        if 1 > int(val) > 12:
            raise ValueError("Invalid month entered")
        return val


class CardCreate(CardBase):
    expiry: CardExpiry
