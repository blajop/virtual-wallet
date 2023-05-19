from typing import Optional
from pydantic import constr
from sqlmodel import Field, Relationship, SQLModel


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"
    id: Optional[str] = Field(primary_key=True)
    wallet_sender: Optional[str] = Field(default=None, foreign_key="wallets.id")
    card_sender: Optional[str] = Field(default=None, foreign_key="cards.id")
    wallet_receiver: str = Field(foreign_key="wallets.id")
    currency: str  # Currency
    amount: float
    status: constr(regex="^pending|success|cancelled$")

    card_sen_obj: Optional[Card] = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="Card.id==Transaction.card_sender")
    )  # lazy="joined" can be added here

    wallet_sen_obj: Optional[Wallet] = Relationship(
        sa_relationship_kwargs=dict(primaryjoin="Wallet.id==Transaction.wallet_sender")
    )  # lazy="joined" can be added here

    wallet_rec_obj: Optional[Wallet] = Relationship(
        sa_relationship_kwargs=dict(
            primaryjoin="Wallet.id==Transaction.wallet_receiver"
        )
    )  # lazy="joined" can be added here
