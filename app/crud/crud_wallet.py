from sqlmodel import Session
from sqlalchemy import select
from app import utils
from app.data import engine
from app.models.user import User
from app.models.wallet import Wallet, WalletCreate


def get_wallets():
    with Session(engine) as session:
        final = []
        result = session.exec(select(Wallet))
        return [el.__dict__ for el in result.unique().scalars().all()]


def create_wallet(user: User, new_wallet: WalletCreate):
    generated_id = utils.util_id.generate_id()
    wallet_orm = Wallet(
        id=generated_id, owner_id=user.id, currency=new_wallet.currency, balance=0
    )

    with Session(engine) as session:
        session.add(wallet_orm)
        wallet_orm.users.append(user)
        session.commit()
        session.refresh(wallet_orm)

    return wallet_orm


def add_user_to_wallet(wallet: Wallet, user: User):
    with Session(engine) as session:
        wallet.users.append(user)
        session.refresh(wallet)
    return wallet
