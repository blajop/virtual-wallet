import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_all_rates() -> dict:
    """
    Gets the rates of all supported currencies.

    Returns:
        dict: keys of which are the currencies - 'USD', 'BGN' etc.
    """

    data = requests.get(os.getenv("CURRENCY_REQUEST_URL"))

    data = data.json().get("data")
    return data


def get_rate(data: dict, base_curr: str, to_curr: str) -> float:
    rate = data[to_curr] / data[base_curr]
    return rate


def exchange(rate: float, amount: float):
    return amount * rate
