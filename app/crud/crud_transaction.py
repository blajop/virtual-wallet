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
)
from app.utils import util_id, util_crypt


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
            # user_wallets_ids = (
            #     db.exec(
            #         select(UserWalletLink.wallet_id).filter(
            #             user.id == UserWalletLink.user_id
            #         )
            #     )
            #     .unique()
            #     .all()
            # )
            # user_wallets_ids.extend(
            #     db.exec(select(Wallet.id).filter(user.id == Wallet.owner_id))
            #     .unique()
            #     .all()
            # )
            # user_cards_ids = (
            #     db.exec(
            #         select(UserCardLink.card_id).filter(user.id == UserCardLink.user_id)
            #     )
            #     .unique()
            #     .all()
            # )
            user_wallets_ids = crud.wallet.get_multi_by_owner(db, user) + user.wallets
            print(user.wallets)
            print(user.cards)
            return (
                db.exec(
                    select(Transaction)
                    .filter(
                        or_(
                            Transaction.card_sender.in_(c.id for c in user.cards),
                            Transaction.wallet_sender.in_(
                                w.id for w in user_wallets_ids
                            ),
                            Transaction.wallet_receiver.in_(
                                w.id for w in user_wallets_ids
                            ),
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
        receiver_wallet_obj = crud.wallet.get(db, new_transaction.wallet_receiver)

        # Here the money transfer between the items happens
        self.money_transfer(
            db,
            sender_item=sender_item_obj,
            receiver_wallet=receiver_wallet_obj,
            currency=self.get_currency(db, currency_str=new_transaction.currency),
            amount=new_transaction.amount,
        )

        try:
            return super().create(
                db, obj_in=new_transaction, generated_id=util_id.generate_id()
            )
        except sqlExc.IntegrityError:
            # the other sql error is prevented by the above code (a single sender item)
            raise TransactionError("The sender and receiver wallets are the same")

    def money_transfer(
        self,
        db: Session,
        *,
        sender_item: Wallet | Card,
        receiver_wallet: Wallet,
        currency: Currency,
        amount: float,
    ) -> Msg:
        """
        Transfers money in the following way Wallet | Card -> Wallet.
        If the sender is a card, no change occurs with the card.
        If the sender is a wallet, the amount passed is taken from their balance (exchanged if necessary).
        The wallet receiver receives the amount passed added to their balance (exchanged if necessary).

        The currencies table ignores the buy/sell exchange rate margin - same rate in all directions is used.

        If different currencies arise between sender and receiver(not their currencies or non_USD),
        they are exchanged on cross-USD rate.

        Arguments:
            db: Session
            new_transaction: TransactionCreate model
            user: User model
        Returns:
            Transaction : the created transaction.
        """
        # if the sender is a Wallet
        if isinstance(sender_item, Wallet):
            if not currency.currency == sender_item.currency:
                sender_currency_amount = self.currency_exchange(
                    db,
                    fro=currency,
                    to=self.get_currency(db, currency_str=sender_item.currency),
                    amount=amount,
                )
                if sender_item.balance < sender_currency_amount:
                    raise TransactionError(
                        "You do not have enough balance in the sender Wallet in order to make the transfer"
                    )
            else:
                sender_currency_amount = amount

            if not currency.currency == receiver_wallet.currency:
                receiver_currency_amount = self.currency_exchange(
                    db,
                    fro=currency,
                    to=self.get_currency(db, currency_str=receiver_wallet.currency),
                    amount=amount,
                )
            else:
                receiver_currency_amount = amount

            sender_item.balance -= sender_currency_amount

            # logic for confirmation by the recipient

            receiver_wallet.balance += receiver_currency_amount
            db.commit()
            return Msg(msg="Successfully executed transaction")

        # if the sender is a Card
        else:
            if not currency.currency == receiver_wallet.currency:
                receiver_currency_amount = self.currency_exchange(
                    db,
                    fro=currency,
                    to=self.get_currency(db, currency_str=receiver_wallet.currency),
                    amount=amount,
                )

            else:
                receiver_currency_amount = amount

                # logic for confirmation by the recipient

            receiver_wallet.balance += receiver_currency_amount
            db.commit()

            return Msg(msg="Successfully executed transaction")

    def get_currency(self, db: Session, *, currency_str: str):
        """
        Gets a Currency object from the DB.

        Arguments:
            db: Session
            currency_str: str : representing the sought currency
        Returns:
            Currency model
        """
        currency_obj = db.exec(
            select(Currency).filter(Currency.currency == currency_str.upper())
        ).first()
        return currency_obj

    def currency_exchange(
        self, db: Session, *, fro: Currency, to: Currency, amount: float
    ) -> float:
        """
        Exchanges amount from one currency to another.
        If the currencies are USD and some other the exchange rate is direct.
        If the currencies are both different from USD, they are exchanged via cross-USD rate.

        Arguments:
            db: Session
            fro: Currency model : the currency of the passed amount
            to: Currency model : the output amount in the "to" currency
        Returns:
            float
        """
        in_USD = amount / fro.rate
        in_output = in_USD * to.rate

        return in_output


transaction = CRUDTransaction(Transaction)
