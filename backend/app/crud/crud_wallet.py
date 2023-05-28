from typing import List
from fastapi import HTTPException, Response
from sqlmodel import Session, select

from app import crud, utils
from app.crud.base import CRUDBase
from app.models import Card, User, Wallet, WalletCreate, WalletUpdate
from app.models.wallet import UserWalletLink


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
        """

        wallet_orm = Wallet.from_orm(new_wallet)
        wallet_orm.id = utils.util_id.generate_id()
        wallet_orm.owner = user

        db.add(wallet_orm)
        db.commit()
        db.refresh(wallet_orm)

        return wallet_orm

    def get_by_owner(self, db: Session, owner: User, wallet_id: str) -> Wallet:
        return db.exec(
            select(self.model).filter(
                self.model.owner_id == owner.id, self.model.id == wallet_id
            )
        ).first()

    def get_multi_by_owner(self, db: Session, owner: User) -> List[Wallet]:
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

    def kick_user(self, db: Session, wallet: Wallet, user_to_remove: str):
        user_to_remove = crud.user.get(db=db, identifier=user_to_remove)
        wallet.users.remove(user_to_remove)

        db.add(wallet)
        db.commit()
        db.refresh(wallet)

        return wallet

    def toggle_deposit(self, db: Session, wallet: Wallet, leech: User):
        link_model: UserWalletLink = db.exec(
            select(UserWalletLink).where(
                UserWalletLink.user_id == leech.id,
                UserWalletLink.wallet_id == wallet.id,
            )
        ).first()
        link_model.can_deposit = not link_model.can_deposit
        db.add(link_model)
        db.commit()
        db.refresh(link_model)

        return link_model

    def toggle_send(self, db: Session, wallet: Wallet, leech: User):
        link_model: UserWalletLink = db.exec(
            select(UserWalletLink).where(
                UserWalletLink.user_id == leech.id,
                UserWalletLink.wallet_id == wallet.id,
            )
        ).first()
        link_model.can_send = not link_model.can_send
        db.add(link_model)
        db.commit()
        db.refresh(link_model)

        return link_model


wallet = CRUDWallet(Wallet)