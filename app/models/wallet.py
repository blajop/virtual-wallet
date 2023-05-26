from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from app.models.user import User

from sqlmodel import Field, Relationship, SQLModel
from pydantic import constr


class UserWalletLink(SQLModel, table=True):
    __tablename__ = "shared_wallets"
    user_id: str = Field(foreign_key="users.id", primary_key=True)
    wallet_id: str = Field(foreign_key="wallets.id", primary_key=True)
    can_deposit: bool = Field(default=True)
    can_send: bool = Field(default=True)


class WalletCreate(SQLModel):
    currency: constr(regex="^(USD|EUR|BGN|CAD|AUD|CHF|CNY|JPY|GBP|NOK)$")


class WalletBase(WalletCreate):
    owner_id: Optional[str] = Field(default=None, foreign_key="users.id")
    balance: Optional[float] = Field(default=0)


class Wallet(WalletBase, table=True):
    __tablename__ = "wallets"
    id: Optional[str] = Field(primary_key=True)

    users: List["User"] = Relationship(
        back_populates="wallets",
        link_model=UserWalletLink,
        sa_relationship_kwargs=dict(lazy="joined"),
    )

    owner: "User" = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="User.id==Wallet.owner_id")
    )  # lazy="joined" can be added here

    def __contains__(self, item: "User") -> bool:
        return item in self.users or item == self.owner


class WalletUpdate(Wallet):
    # manages balance?
    pass
