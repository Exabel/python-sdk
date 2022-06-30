import logging
from typing import NewType

import pandas as pd

from exabel_data_sdk.services.file_writer_provider import FileWriterProvider
from exabel_data_sdk.services.sql.sql_reader_configuration import ConnectionString
from exabel_data_sdk.util.handle_missing_imports import handle_missing_imports

with handle_missing_imports():
    from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

Query = NewType("Query", str)
OutputFile = NewType("OutputFile", str)


class SqlReader:
    """Reader of SQL queries."""

    def __init__(self, connection_string: ConnectionString) -> None:
        self.engine = create_engine(connection_string)

    def read_sql_query(self, query: Query) -> pd.DataFrame:
        """Execute the given query and return the content as a pandas DataFrame."""
        try:
            return pd.read_sql_query(query, self.engine)
        except Exception as e:
            logger.error("An error occurred while executing the query: %s", str(e))
            raise

    def read_sql_query_and_write_result(self, query: Query, output_file: OutputFile = None) -> None:
        """
        Execute the given query and write the result to the given output file. If no output file is
        given, print a sample instead.
        """
        df = self.read_sql_query(query)
        if not output_file:
            logger.info("No output file specified. Printing sample.")
            logger.info(df)
            return
        FileWriterProvider.get_file_writer(output_file).write_file(df, output_file)
