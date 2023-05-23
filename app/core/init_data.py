from app.utils import util_exchange
from app.api.deps import get_db


def _init_data():
    util_exchange.write_rates_to_db(next(get_db()))
    pass
    # check recurring payments
