from sqlmodel import Session
from sqlalchemy import select
from app.data import engine


def get_wallets():
    with Session(engine) as session:
        final = []
        result = session.exec(select(Wallet))
        return [el.__dict__ for el in result.unique().scalars().all()]


# def create_wallet(user: UserExtended, currency: str):
#     wallet_id = sf.generate_id()
#     new_wallet = Wallet(
#         id=wallet_id,
#         owner=user,
#         currency=currency,
#     )

#     with Session(engine) as session:
#         session.add(WalletORM(**new_wallet.__dict__))
#         session.commit()

#     return new_wallet


# def add_leech(wallet: Wallet, leech: UserExtended):
#     pass
