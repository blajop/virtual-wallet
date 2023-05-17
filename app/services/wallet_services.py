from app.models import WalletORM, Wallet, User, UserExtended
from app.helpers import snowflake_ids as sf
from sqlalchemy.orm import Session
from app.data import engine


def create_wallet(user: UserExtended, currency: str):
    wallet_id = sf.generate_id()
    new_wallet = Wallet(
        id=wallet_id,
        owner=user,
        currency=currency,
    )

    with Session(engine) as session:
        session.add(WalletORM(**new_wallet.__dict__))
        session.commit()

    return new_wallet


def add_leech(wallet: Wallet, leech: UserExtended):
    pass
