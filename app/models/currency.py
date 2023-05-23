from sqlmodel import SQLModel, Field


class Currency(SQLModel, table=True):
    __tablename__ = "currencies"
    currency: str = Field(
        primary_key=True,
        regex="^(USD|EUR|BGN|CAD|AUD|CHF|CNY|JPY|GBP|NOK)$",
    )
    rate: float
