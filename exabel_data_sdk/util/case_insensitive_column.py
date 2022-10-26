from typing import Sequence, Union


def get_case_insensitive_column(column: Union[str, int], columns: Sequence[str]) -> Union[str, int]:
    """
    Search for a column name in a sequence of column names and if found, return the
    lexicographically first case-insensitive match among the column names. If no match is found
    or the input column is an integer, the input column name is returned unchanged.
    """
    if isinstance(column, int):
        return column
    lowered_column = column.lower()
    lowered_columns = {c.lower(): c for c in reversed(columns)}
    return lowered_columns.get(lowered_column, column)
