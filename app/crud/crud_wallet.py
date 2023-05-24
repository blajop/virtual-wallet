from typing import List
from fastapi import HTTPException, Response
from sqlmodel import Session, select

from app import utils
from app.crud.base import CRUDBase
from app.models import Card, User, Wallet, WalletCreate, WalletUpdate


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

    ### CODE BELLOW TO BE REMOVED
    #
    # def deposit(self, db: Session, wallet: Wallet, amount: float, card: Card):
    #     # if not card.confirm_balance(amount): bank logic
    #     #    return Response(status_code=400, detail='nema pari :(')
    #     wallet.balance += amount
    #     db.add(wallet)
    #     db.commit()
    #     db.refresh(wallet)
    #     return wallet

    # def transfer(
    #     self, db: Session, from_wallet: Wallet, amount: float, to_wallet: Wallet
    # ):
    #     if from_wallet.balance < amount:
    #         return Response(
    #             status_code=400, content="Insufficient amount in your wallet."
    #         )
    #     to_wallet.balance += amount
    #     from_wallet.balance -= amount
    #     db.add(from_wallet)
    #     db.commit()
    #     db.refresh(from_wallet)
    #     return from_wallet
    #
    #
    ### CODE BELLOW TO BE REMOVED


wallet = CRUDWallet(Wallet)
