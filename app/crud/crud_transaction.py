from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlmodel import Session, or_, select
from app import crud
from app.crud.base import CRUDBase
from app.error_models.transaction_errors import TransactionError
from app.models.card import Card, UserCardLink
from app.models.transaction import Transaction, TransactionBase, TransactionCreate
from app.models.user import User
from app.models.msg import Msg
from app.models.wallet import Wallet, UserWalletLink
from app.utils import util_id, util_crypt
from sqlalchemy import exc as sqlExc


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionBase]):
    def get(self, db: Session, id: str, user: User) -> Transaction:
        """
        Returns a transaction by id.

        Arguments:
            db: Session
            id: str
            user: User model
            Takes skip and limit pagination args which have default values.
        Returns:
            Transaction model | None
        """
        found_transaction = super().get(db, id)

        if not found_transaction:
            return None

        sender_item: Wallet | Card = (
            found_transaction.wallet_sen_obj
            if found_transaction.wallet_sen_obj
            else found_transaction.card_sen_obj
        )
        receiver_wallet = found_transaction.wallet_rec_obj

        if (
            crud.user.is_admin(user)
            or (user in sender_item)
            or (user in receiver_wallet)
        ):
            return found_transaction
        return None

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, user: User
    ) -> List[Transaction]:
        """
        Returns all transactions accessible to the passed user.
        If the user is admin, he can see all transactions in the app.
        If the user is a normal user, he can see all transactions with cards/wallets
        which he owns or uses.

        Arguments:
            db: Session
            user: User model
            Takes skip and limit pagination args which have default values.
        Returns:
            list[Transaction]
        """
        if crud.user.is_admin(user):
            return super().get_multi(db, skip=skip, limit=limit)

        else:
            user_wallets_ids = (
                db.exec(
                    select(UserWalletLink.wallet_id).filter(
                        user.id == UserWalletLink.user_id
                    )
                )
                .unique()
                .all()
            )
            user_wallets_ids.extend(
                db.exec(select(Wallet.id).filter(user.id == Wallet.owner_id))
                .unique()
                .all()
            )
            user_cards_ids = (
                db.exec(
                    select(UserCardLink.card_id).filter(user.id == UserCardLink.user_id)
                )
                .unique()
                .all()
            )

            return (
                db.exec(
                    select(Transaction)
                    .filter(
                        or_(
                            Transaction.card_sender.in_(user_cards_ids),
                            Transaction.wallet_sender.in_(user_wallets_ids),
                            Transaction.wallet_receiver.in_(user_wallets_ids),
                        )
                    )
                    .offset(skip)
                    .limit(limit)
                )
                .unique()
                .all()
            )

    def create(
        self, db: Session, *, new_transaction: TransactionCreate, user: User
    ) -> Transaction:
        """
        Creates a transaction.

        Arguments:
            db: Session
            new_transaction: User model
            Takes skip and limit pagination args which have default values.
        Returns:
            list[Transaction]
        """
        user_wallets = crud.wallet.get_multi_by_owner(db, user) + user.wallets

        if (
            sender_item := new_transaction.wallet_sender
        ) and not new_transaction.card_sender:
            if sender_item not in [w.id for w in user_wallets]:
                raise TransactionError(
                    "The sender item passed is not in your wallets/cards"
                )
            new_transaction.card_sender = None

        elif (
            sender_item := new_transaction.card_sender
        ) and not new_transaction.wallet_sender:
            if sender_item not in [c.id for c in user.cards]:
                raise TransactionError(
                    "The sender item passed is not in your wallets/cards"
                )
            new_transaction.wallet_sender = None

        else:
            raise TransactionError(
                "You should pass either valid wallet or valid card sender"
            )
        try:
            return super().create(
                db, obj_in=new_transaction, generated_id=util_id.generate_id()
            )
        except sqlExc.IntegrityError:
            raise TransactionError("The sender and receiver wallets are the same")


transaction = CRUDTransaction(Transaction)
