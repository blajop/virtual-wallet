from typing import Optional
from pydantic import constr
from sqlmodel import Field, Relationship, SQLModel
from app.models.card import Card
from app.models.wallet import Wallet


class TransactionBase(SQLModel):
    wallet_sender: Optional[str] = Field(default=None, foreign_key="wallets.id")
    card_sender: Optional[str] = Field(default=None, foreign_key="cards.id")
    wallet_receiver: str = Field(foreign_key="wallets.id")
    currency: str  # Currency
    amount: float
    status: constr(regex="^pending|success|cancelled$")
    recurring: Optional[constr(regex="^month|year")] = Field(default=None)


class Transaction(TransactionBase, table=True):
    __tablename__ = "transactions"
    id: Optional[str] = Field(primary_key=True)

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
