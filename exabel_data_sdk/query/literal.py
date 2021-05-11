from typing import Union

import pandas as pd

Literal = Union[str, int, float, pd.Timestamp]


def to_sql(literal: Literal) -> str:
    """Returns the SQL representation of the given term."""
    if isinstance(literal, str):
        return escape(literal)
    if isinstance(literal, (int, float)):
        return str(literal)
    if isinstance(literal, pd.Timestamp):
        return f"'{literal.date()}'"
    raise ValueError(f"Unknown object type {type(literal)} for {literal}")


def escape(string: str) -> str:
    """
    Returns the SQL representation of the given string,
    by escaping all single-quotes with two single-quotes
    and surrounding the string with single-quotes.
    """
    return f"""'{string.replace("'", "''")}'"""
