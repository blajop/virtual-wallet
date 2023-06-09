from datetime import datetime, timedelta
from typing import List, Optional, Union
from sqlmodel import Session, String, cast, or_, select, desc, func, DateTime, asc
from sqlalchemy import exc as sqlExc
from fastapi_pagination.ext.sqlmodel import paginate

from app import crud
from app.crud.base import CRUDBase
from app.error_models import TransactionError
from app.error_models.transaction_errors import TransactionPermissionError
from app.models import (
    Card,
    UserCardLink,
    Transaction,
    TransactionBase,
    TransactionCreate,
    User,
    Msg,
    Wallet,
    UserWalletLink,
    Currency,
)
from app.utils import util_id, util_crypt


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionBase]):
    def get(
        self, db: Session, id: str, user: User, *, admin_r: bool = False
    ) -> Transaction:
        found_transaction: Transaction = super().get(db, id)

        if not found_transaction:
            return None

        receiver_wallet = found_transaction.wallet_rec_obj

        if (
            admin_r
            or (found_transaction.sending_user == user.id)
            or (user in receiver_wallet)
        ):
            return found_transaction

        return None

    def get_multi(
        self,
        db: Session,
        *,
        user: Optional[User],
        from_date: datetime = datetime.now() - timedelta(weeks=4.0),
        to_date: datetime = datetime.now(),
        recipient: str = None,
        direction: str = "all",
        sort_by: str = "date",
        sort: str = "asc",
        status: str = None,
        recurring: bool | None = None,
    ) -> List[Transaction]:
        if status not in [None, "finished", "active"]:
            status = None

        if user:
            user_wallets_ids = [
                w.id for w in crud.wallet.get_multi_by_owner(db, user)
            ] + [w.id for w in user.wallets]

        selectable = (
            select(Transaction)
            .filter(
                or_(
                    (Transaction.sending_user == user.id) if user else True,
                    (Transaction.wallet_receiver.in_(user_wallets_ids))
                    if user
                    else True,
                )
            )
            .filter(
                Transaction.created > from_date,
                Transaction.created < to_date,
                (Transaction.receiving_user == recipient) if recipient else True,
                (Transaction.sending_user == user.id)
                if ((direction == "out") and user)
                else True,
                (Transaction.sending_user != user.id)
                if ((direction == "in") and user)
                else True,
                (Transaction.status != "pending")
                if status and status == "finished"
                else True,
                (Transaction.status == "pending")
                if status and status == "active"
                else True,
                (Transaction.recurring != None) if recurring == True else True,
                (Transaction.recurring == None) if recurring == False else True,
            )
        )
        return paginate(
            db,
            selectable.order_by(
                (desc if (sort == "desc") else asc)(
                    Transaction.amount if sort_by == "amount" else Transaction.created
                )
            ),
        )

    def get_recurring(self, db: Session):
        transactions = (
            db.exec(select(Transaction).where(Transaction.recurring != None))
            .unique()
            .all()
        )

        return transactions

    def create(
        self,
        db: Session,
        *,
        new_transaction: TransactionCreate,
        user: User,
        recipient_user: User,
    ) -> Transaction:
        """
        Creates a transaction.
        - Option 1: Transfers money Card -> Wallet (depositing from card to a wallet -
        ONLY card registered on the user's account to wallet), according to the transaction data
        - Option 2: Wallet -> Wallet transer from a wallet in which the user is the owner | user,
        according to the transaction data

        If different currencies arise, they are exchanged on cross-USD rate.

        Arguments:
            db: Session
            new_transaction: TransactionCreate model
            user: User model
        Returns:
            Transaction : the created transaction.
        """
        user_wallets = crud.wallet.get_multi_by_owner(db, user) + user.wallets
        recipient_user_wallets = (
            crud.wallet.get_multi_by_owner(db, recipient_user) + recipient_user.wallets
        )
        if new_transaction.wallet_receiver not in [
            w.id for w in recipient_user_wallets
        ]:
            raise TransactionError(
                "The wallet receiver passed is not associated with the recipient user."
            )

        # If the sender is a wallet
        if (
            sender_item_id := new_transaction.wallet_sender
        ) and not new_transaction.card_sender:
            if sender_item_id not in [w.id for w in user_wallets]:
                raise TransactionError(
                    "The wallet sender passed is not in your associated wallets"
                )
            sender_item_obj: Wallet = crud.wallet.get(db, user, sender_item_id)
            new_transaction.card_sender = None

            if new_transaction.currency == sender_item_obj.currency:
                sender_currency_amount = new_transaction.amount
            else:
                sender_curr = self.get_currency(db, sender_item_obj.currency)
                transaction_curr = self.get_currency(db, new_transaction.currency)
                sender_currency_amount = self.currency_exchange(
                    base=transaction_curr,
                    to=sender_curr,
                    amount=new_transaction.amount,
                )
            if sender_item_obj.balance < sender_currency_amount:
                raise TransactionError(
                    "You do not have enough balance in the sender Wallet in order to make the transfer"
                )
            # block the sender_currency_amount within the transaction until acceptance/decline
            sender_item_obj.balance -= sender_currency_amount

        # Card -> Wallet (depositing) - only from user's registered card to
        # wallet connected with the user

        # If the sender is a card
        elif (
            sender_item_id := new_transaction.card_sender
        ) and not new_transaction.wallet_sender:
            if sender_item_id not in [c.id for c in user.cards]:
                raise TransactionError(
                    "The card sender passed is not in your registered cards"
                )
            if new_transaction.wallet_receiver not in (w.id for w in user_wallets):
                raise TransactionError(
                    "You can't deposit money to a wallet not connected with your acoount"
                )
            # the obtained Card is with the number and cvc deciphered, so we cipher them back straight away
            sender_item_obj: Card = crud.card.get(db, sender_item_id)
            sender_item_obj.number = util_crypt.encrypt(sender_item_obj.number)
            sender_item_obj.cvc = util_crypt.encrypt(sender_item_obj.cvc)
            new_transaction.wallet_sender = None

        else:
            raise TransactionError(
                "You should pass either valid wallet or valid card sender"
            )

        if sender_item_id == new_transaction.wallet_receiver:
            raise TransactionError("The sender and receiver wallets are the same")

        transaction = super().create(
            db, obj_in=new_transaction, generated_id=util_id.generate_id()
        )
        transaction.sending_user = user.id
        transaction.blocked_sender_amt = sender_currency_amount
        transaction.created = transaction.updated = datetime.now()

        db.commit()
        return transaction

    def accept(
        self, *, db: Session, transaction: Transaction, user: User
    ) -> Msg | TransactionError | TransactionPermissionError:
        if user.id != transaction.receiving_user:
            raise TransactionPermissionError(
                "You are not the receiver of the transaction and cannot confirm it"
            )

        if transaction.status == "success":
            raise TransactionError("Already accepted")

        if transaction.status != "pending":
            raise TransactionError("Transaction is not with status pending ")

        msg = self._finalise(db=db, transaction=transaction)
        transaction.status = "success"
        transaction.updated = datetime.now()

        db.commit()

        return msg

    def _finalise(self, db: Session, *, transaction: Transaction) -> Msg:
        """
        Finalises a transaction, adding the amount to the receiver durring acceptance.
        """
        receiver: Wallet = transaction.wallet_rec_obj

        transaction_curr: Currency = self.get_currency(db, transaction.currency)
        receiver_curr: Currency = self.get_currency(db, receiver.currency)

        amount: float = transaction.amount

        if transaction_curr == receiver_curr:
            receiver_currency_amount = amount
        else:
            receiver_currency_amount = self.currency_exchange(
                base=transaction_curr, to=receiver_curr, amount=amount
            )

        receiver.balance += receiver_currency_amount
        transaction.blocked_sender_amt = 0

        db.commit()

        return Msg(msg="Successfully executed transaction")

    def get_currency(self, db: Session, currency_str: str) -> Currency:
        return db.exec(
            select(Currency).filter(Currency.currency == currency_str.upper())
        ).first()

    def currency_exchange(
        self, *, base: Currency, to: Currency, amount: float
    ) -> float:
        in_USD = amount / base.rate
        in_output = in_USD * to.rate

        return in_output

    def decline(
        self, *, db: Session, transaction: Transaction, user: User
    ) -> Msg | TransactionError | TransactionPermissionError:
        if user.id != transaction.receiving_user:
            raise TransactionPermissionError(
                "You are not the receiver of the transaction and cannot decline it"
            )

        if transaction.status != "pending":
            raise TransactionError("Transaction is not with status pending")

        transaction.status = "declined"
        if transaction.wallet_sen_obj:
            transaction.wallet_sen_obj.balance += transaction.blocked_sender_amt
            transaction.blocked_sender_amt = 0
        transaction.updated = datetime.now()

        db.commit()

        return Msg(msg="Transaction declined")


transaction = CRUDTransaction(Transaction)
