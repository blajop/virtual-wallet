import datetime
import random
from snowflake import SnowflakeGenerator, Snowflake


def generate_id() -> str:
    """Generates a unique identifier.

    Returns:
        str: 19 digits in a str format
    """
    instance = random.choice(range(1, 1024))
    return str(next(SnowflakeGenerator(instance)))


def datetime_from_id(id: str) -> datetime:
    """Parses a snowflake ID and retrieves the datetime from it in UTC

    Args:
        id: str
    Returns:
        datetime: when the ID was issued
    """
    return Snowflake.parse(int(id)).datetime
