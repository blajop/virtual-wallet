import requests


def get_all_rates() -> dict:
    """
    Gets the rates of all supported currencies.

    Returns:
        dict: keys of which are the currencies - 'USD', 'BGN' etc.
    """

    data = requests.get(
        f"https://api.freecurrencyapi.com/v1/latest?apikey=CaObycAixuF3GJJl9IVBdOQZNeTL2MmM3TamraI7&currencies=USD%2CEUR%2CBGN%2CCAD%2CAUD%2CCHF%2CCNY%2CJPY%2CGBP%2CNOK"
    )

    data = data.json().get("data")
    return data


def get_rate(data: dict, base_curr: str, to_curr: str) -> float:
    rate = data[to_curr] / data[base_curr]
    return rate


def exchange(rate: float, amount: float):
    return amount * rate
