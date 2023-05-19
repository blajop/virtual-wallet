from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class UserWalletLink(SQLModel, table=True):
    __tablename__ = "shared_wallets"
    user_id: str = Field(foreign_key="users.id", primary_key=True)
    wallet_id: str = Field(foreign_key="wallets.id", primary_key=True)


class Wallet(SQLModel, table=True):
    __tablename__ = "wallets"
    id: Optional[str] = Field(primary_key=True)
    owner_id: Optional[str] = Field(default=None, foreign_key="users.id")
    currency: str  # Currency
    balance: float = Field(default=0)

    users: User = Relationship(back_populates="wallets", link_model=UserWalletLink)

    owner: User = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="User.id==Wallet.owner_id")
    )  # lazy="joined" can be added here
