from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, constr, confloat
from sqlmodel import Field, Relationship, SQLModel
from app.models.card import Card
from app.models.wallet import Wallet
from app.models.user import User


class TransactionBase(SQLModel):
    wallet_sender: Optional[str] = Field(default=None, foreign_key="wallets.id")
    blocked_sender_amt: Optional[float] = Field(default=None)
    card_sender: Optional[str] = Field(default=None, foreign_key="cards.id")
    receiving_user: Optional[str] = Field(default=None)
    wallet_receiver: str = Field(foreign_key="wallets.id")
    currency: constr(regex="^(USD|EUR|BGN|CAD|AUD|CHF|CNY|JPY|GBP|NOK)$")
    amount: confloat(gt=0)
    recurring: Optional[constr(regex="^Monthly|Annually")] = Field(default=None)
    detail: Optional[str] = Field(default=None)
    spending_category_id: Optional[int] = Field(
        default=3, foreign_key="spending_categories.id"
    )
    link_accept: Optional[str] = Field(default=None)
    link_decline: Optional[str] = Field(default=None)


class Transaction(TransactionBase, table=True):
    __tablename__ = "transactions"
    sending_user: Optional[str] = Field(default=None, foreign_key="users.id")
    receiving_user: Optional[str] = Field(default=None, foreign_key="users.id")
    id: Optional[str] = Field(primary_key=True)
    status: Optional[constr(regex="^pending|success|cancelled|declined$")] = Field(
        default="pending"
    )
    created: Optional[datetime] = Field(default=None)
    updated: Optional[datetime] = Field(default=None)

    spending_category_obj: "SpendingCategory" = Relationship(
        back_populates="transactions",
        sa_relationship_kwargs=dict(
            primaryjoin="Transaction.spending_category_id==SpendingCategory.id"
        ),
    )

    sending_user_obj: "User" = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="User.id==Transaction.sending_user")
    )

    receiving_user_obj: "User" = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="User.id==Transaction.receiving_user")
    )

    card_sen_obj: Optional["Card"] = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="Card.id==Transaction.card_sender")
    )  # lazy="joined" can be added here

    wallet_sen_obj: Optional["Wallet"] = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="Wallet.id==Transaction.wallet_sender")
    )  # lazy="joined" can be added here

    wallet_rec_obj: Optional["Wallet"] = Relationship(
        sa_relationship_kwargs=dict(
            primaryjoin="Wallet.id==Transaction.wallet_receiver"
        )
    )  # lazy="joined" can be added here


class TransactionCreate(TransactionBase):
    pass


class SpendingCategory(SQLModel, table=True):
    __tablename__ = "spending_categories"
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(unique=True)

    transactions: List["Transaction"] = Relationship(
        sa_relationship_kwargs=dict(
            primaryjoin="Transaction.spending_category_id==SpendingCategory.id"
        )
    )
