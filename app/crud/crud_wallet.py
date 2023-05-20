from sqlmodel import Session
from sqlalchemy import select
from app import utils
from app.data import engine
from app.models.user import User
from app.models.wallet import Wallet


def get_wallets():
    with Session(engine) as session:
        final = []
        result = session.exec(select(Wallet))
        return [el.__dict__ for el in result.unique().scalars().all()]


def create_wallet(user: User, currency: str):
    generated_id = utils.util_id.generate_id()
    new_wallet = Wallet(id=generated_id, owner_id=user.id, currency=currency, balance=0)

    with Session(engine) as session:
        session.add(Wallet(new_wallet))
        session.commit()
        session.refresh(new_wallet)

    return new_wallet


def add_user_to_wallet(wallet: Wallet, user: User):
    with Session(engine) as session:
        wallet.users.append(user)
        session.refresh(wallet)
    return wallet
