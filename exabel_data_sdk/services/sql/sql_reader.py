import logging
from typing import Iterable, Iterator, NewType, Optional, Union

import pandas as pd

from exabel_data_sdk.services.file_writer_provider import FileWriterProvider
from exabel_data_sdk.services.sql.sql_reader_configuration import ConnectionString
from exabel_data_sdk.util.handle_missing_imports import handle_missing_imports

with handle_missing_imports():
    from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

BatchSize = NewType("BatchSize", int)
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

    @staticmethod
    def get_data_frame(df: Union[pd.DataFrame, Iterable[pd.DataFrame]]) -> pd.DataFrame:
        """Return the first `DataFrame` if given an iterable, or the given `DataFrame`."""
        if isinstance(df, pd.DataFrame):
            return df
        for chunk in df:
            return chunk
        return pd.DataFrame()

    def read_sql_query_in_batches(
        self, query: Query, batch_size: BatchSize
    ) -> Iterator[pd.DataFrame]:
        """
        Execute the given query and return the content as a pandas DataFrame in chunks of the given
        batch size.
        """
        batch_no = 0
        try:
            reader = pd.read_sql_query(query, self.engine, chunksize=batch_size)
            for batch_no, chunk in enumerate(reader):
                yield chunk
        except Exception as e:
            logger.exception(
                "An error occurred in batch number %d while executing the query: %s",
                batch_no,
                str(e),
            )
            raise

    def read_sql_query_and_write_result(
        self,
        query: Query,
        output_file: OutputFile = None,
        *,
        batch_size: Optional[BatchSize] = None,
    ) -> None:
        """
        Execute the given query and write the result to the given output file. If no output file is
        given, print a sample instead.
        """
        if batch_size is None:
            df = self.read_sql_query(query)
        else:
            df = self.read_sql_query_in_batches(query, batch_size)
        if not output_file:
            logger.info("No output file specified. Printing sample.")
            logger.info(self.get_data_frame(df))
            return
        FileWriterProvider.get_file_writer(output_file).write_file(df, output_file)
