from fastapi import HTTPException
from sqlmodel import Session
from sqlalchemy import select
from app import utils
from app.core import security
from app.crud.base import CRUDBase
from app.data import engine
from app.models.card import Card
from app.models.user import User
from app.models.wallet import Wallet, WalletCreate, WalletUpdate


class CRUDWallet(CRUDBase[Wallet, WalletCreate, WalletUpdate]):
    def create(
        self, db: Session, user: User, new_wallet: WalletCreate
    ) -> Wallet | HTTPException:
        """
        Creates a new wallet for the logged user.

        Arguments:
            db: Session
            user: User model to create wallet for
            new_wallet: WalletCreate model
        Returns:
            Wallet model
        Raises:
            HTTPException with status code 400: Username/Email/Phone number already taken
        """

        wallet_orm = Wallet.from_orm(new_wallet)
        wallet_orm.id = utils.util_id.generate_id()
        wallet_orm.owner = user

        db.add(wallet_orm)
        db.commit()
        db.refresh(wallet_orm)

        return wallet_orm

    def get_multi_by_owner(self, db: Session, owner: User):
        return (
            db.exec(select(self.model).filter(self.model.owner_id == owner.id))
            .unique()
            .all()
        )

    def invite_user(self, db: Session, wallet: Wallet, user: User):
        wallet.users.append(user)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
        return wallet

    def deposit(self, db: Session, wallet: Wallet, card: Card):
        pass


wallet = CRUDWallet(Wallet)
