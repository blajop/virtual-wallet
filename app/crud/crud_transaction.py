from datetime import datetime, timedelta
from typing import List, Optional, Union
from sqlmodel import Session, String, cast, or_, select, desc, func, DateTime, asc
from sqlalchemy import exc as sqlExc


from app import crud
from app.crud.base import CRUDBase
from app.error_models import TransactionError
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
        skip: int = 0,
        limit: int = 100,
        user: Optional[User],
        from_date: datetime = datetime.now() - timedelta(weeks=4.0),
        to_date: datetime = datetime.now(),
        recipient: str = None,
        direction: str = "all",
        sort_by: str = "date",
        sort: str = "asc",
        admin_r: bool = False,
    ) -> List[Transaction]:
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
                (Transaction.wallet_receiver == recipient) if recipient else True,
                (Transaction.sending_user == user.id)
                if ((direction == "out") and user)
                else True,
                (Transaction.sending_user != user.id)
                if ((direction == "in") and user)
                else True,
            )
        )
        return (
            db.exec(
                selectable.order_by(
                    (desc if (sort == "desc") else asc)(
                        Transaction.amount
                        if sort_by == "amount"
                        else Transaction.created
                    )
                )
                .offset(skip)
                .limit(limit)
            )
            .unique()
            .all()
        )

    def get_recurring(self, db: Session):
        transactions = (
            db.exec(select(Transaction).where(Transaction.recurring != None))
            .unique()
            .all()
        )

        return transactions

    def create(
        self, db: Session, *, new_transaction: TransactionCreate, user: User
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

        # If the sender is a wallet
        if (
            sender_item_id := new_transaction.wallet_sender
        ) and not new_transaction.card_sender:
            if sender_item_id not in [w.id for w in user_wallets]:
                raise TransactionError(
                    "The wallet sender passed is not in your associated wallets"
                )
            sender_item_obj: Wallet = crud.wallet.get(db, sender_item_id)
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
        transaction.created = transaction.updated = datetime.now()
        db.commit()
        return transaction

    def accept(
        self, *, db: Session, transaction: Transaction
    ) -> Msg | TransactionError:
        if transaction.status == "success":
            raise TransactionError("Already accepted")

        msg = self._finalise(db=db, transaction=transaction)
        transaction.status = "success"

        db.commit()

        return msg

    def _finalise(
        self, db: Session, *, transaction: Transaction
    ) -> Msg | TransactionError:
        """
        Finalises a transaction, exchanging the amount between the wallets.
        """
        sender: Wallet | Card = transaction.card_sen_obj or transaction.wallet_sen_obj
        receiver: Wallet = transaction.wallet_rec_obj

        transaction_curr: Currency = self.get_currency(db, transaction.currency)
        sender_curr: Currency = self.get_currency(db, sender.currency)
        receiver_curr: Currency = self.get_currency(db, receiver.currency)

        amount: float = transaction.amount

        if transaction_curr == receiver_curr:
            receiver_currency_amount = amount
        else:
            receiver_currency_amount = self.currency_exchange(
                base=transaction_curr, to=receiver_curr, amount=amount
            )

        if isinstance(sender, Card):
            receiver.balance += receiver_currency_amount
            db.commit()
            # Return when a card deposit
            return Msg(msg="Successfully executed transaction")

        # Transfer between wallets
        if transaction_curr == sender_curr:
            sender_currency_amount = amount
        else:
            sender_currency_amount = self.currency_exchange(
                base=transaction_curr, to=sender_curr, amount=amount
            )

        sender.balance -= sender_currency_amount
        receiver.balance += receiver_currency_amount

        db.commit()

        return Msg(msg="Successfully executed transaction")

        # backup code bellow

        ##
        ##
        ##

        # if isinstance(sender, Wallet):
        #     if transaction.currency == sender.currency:
        #         sender_currency_amount = amount
        #     else:
        #         sender_currency_amount = self.currency_exchange(
        #             db,
        #             fro=transaction_curr,
        #             to=sender_curr,
        #             amount=amount,
        #         )
        #         if sender.balance < sender_currency_amount:
        #             raise TransactionError(
        #                 "You do not have enough balance in the sender Wallet in order to make the transfer"
        #             )

        #     if transaction_curr == receiver_curr:
        #         receiver_currency_amount = amount
        #     else:
        #         receiver_currency_amount = self.currency_exchange(
        #             db, fro=transaction_curr, to=receiver_curr, amount=amount
        #         )

        #     sender.balance -= sender_currency_amount
        #     receiver_wallet.balance += receiver_currency_amount

        #     db.commit()

        #     return Msg(msg="Successfully executed transaction")

        # # if the sender is a Card
        # else:
        #     if transaction_curr == receiver_curr:
        #         receiver_currency_amount = amount
        #     else:
        #         receiver_currency_amount = self.currency_exchange(
        #             db, fro=transaction_curr, to=receiver_curr, amount=amount
        #         )

        #     # logic for confirmation by the recipient

        #     receiver_wallet.balance += receiver_currency_amount
        #     db.commit()

        #     return Msg(msg="Successfully executed transaction")

        ##
        ##
        ##

        # backup code above

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


transaction = CRUDTransaction(Transaction)
