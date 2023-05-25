from typing import List
from sqlmodel import Session, or_, select
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
    def get(self, db: Session, id: str, user: User) -> Transaction:
        """
        Returns a transaction by id.
        Admin can get any transaction.
        A normal user can get only a transaction he is the sender of,
        or such that transfers money to a wallet he is owner or user of.

        Arguments:
            db: Session
            id: str
            user: User model
        Returns:
            Transaction model | None
        """
        found_transaction: Transaction = super().get(db, id)

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
            or (found_transaction.sending_user == user.id)
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
        If the user is a normal user, he can see all transactions to wallets
        which he owns or uses, and transactions he is the sender of.

        Arguments:
            db: Session
            user: User model
            Takes skip and limit pagination args which have default values.
        Returns:
            list[Transaction]
        """
        # TBD : Search to be implemented with filtering
        if crud.user.is_admin(user):
            return super().get_multi(db, skip=skip, limit=limit)

        # TBD : Search to be implemented with filtering
        else:
            user_wallets_ids = [
                w.id for w in crud.wallet.get_multi_by_owner(db, user)
            ] + [w.id for w in user.wallets]

            return (
                db.exec(
                    select(Transaction)
                    .filter(
                        or_(
                            Transaction.card_sender.in_(c.id for c in user.cards),
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
            if sender.balance < sender_currency_amount:
                raise TransactionError(
                    "You do not have enough balance in the sender Wallet in order to make the transfer"
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
