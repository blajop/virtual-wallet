import datetime
from snowflake import SnowflakeGenerator, Snowflake


def generate_id(instance: int = 1) -> str:
    """Generates a unique identifier.

    Args:
        instance: int between 0 and 1023; the seed for generation
    Returns:
        19 digits in a str format
    """
    return str(next(SnowflakeGenerator(instance)))


def datetime_from_id(id: str) -> datetime:
    """Parses a snowflake ID and retrieves the datetime from it in UTC"""
    return Snowflake.parse(int(id)).datetime
