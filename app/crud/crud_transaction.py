from sqlmodel import Session
from sqlalchemy import select

# from sqlalchemy import select
from app.models.transaction import Transaction


# def get_transactions():
#     with Session(engine) as session:
#         result = session.exec(select(Transaction))
#         return [el.__dict__ for el in result.unique().scalars().all()]
