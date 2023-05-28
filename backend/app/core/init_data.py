from datetime import datetime
from sqlmodel import Session

from app.models import Transaction
from app.utils import util_exchange, util_id
from app.api.deps import get_db
from app import crud


db: Session = next(get_db())


def _init_data():
    # update daily exchange rates
    util_exchange._write_rates_to_db(db)
    # check recurring payments
    _check_recurring_payments()


def _check_recurring_payments():
    recurring = crud.transaction.get_recurring(db)

    for transaction in recurring:
        date: datetime = util_id.datetime_from_id(transaction.id)
        period: str = transaction.recurring

        if _check_passed(date, period):
            # check if wallet has sufficient funds
            wallet_sender = transaction.wallet_sen_obj
            if wallet_sender.balance < transaction.amount:
                continue
            # generate a new transaction
            new_transaction = Transaction.from_orm(transaction)
            new_transaction.id = util_id.generate_id()
            # change new_transaction dates

            transaction.recurring = None

            db.add_all([transaction, new_transaction])
            db.commit()

            # move money between the wallets
            # call endpoint?


def _check_passed(date: datetime, period: str):
    # period (month | year)
    now = datetime.now()
    day = date.day
    month = date.month
    year = date.year

    difference_months = (now.year - year) * 12 + (now.month - month)

    if period == "month" and difference_months >= 1 and now.day >= day:
        return True
    elif period == "year" and difference_months >= 12 and now.day >= day:
        return True
    return False
