from sqlmodel import select, Session
from app.models import Wallet, User
from app.data import engine


def get_wallets():
    with Session(engine) as session:
        final = []
        result = session.exec(select(Wallet))
        for wallet in result:
            wallet.owner
            final.append(wallet.__dict__)
        return final


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
