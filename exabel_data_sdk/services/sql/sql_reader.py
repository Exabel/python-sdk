import pandas as pd

from exabel_data_sdk.util.handle_missing_imports import handle_missing_imports

with handle_missing_imports():
    from sqlalchemy import create_engine


class SqlReader:
    """Reader of SQL queries."""

    def __init__(self, connection_string: str) -> None:
        self.engine = create_engine(connection_string)

    def read_sql_query(self, query: str) -> pd.DataFrame:
        """Execute the given query and return the content as a pandas DataFrame."""
        return pd.read_sql_query(query, self.engine)
