import abc
import logging
from typing import Iterable, Iterator, NewType, Optional, Union

import pandas as pd

from exabel_data_sdk.services.file_writer import FileWritingResult
from exabel_data_sdk.services.file_writer_provider import FileWriterProvider

logger = logging.getLogger(__name__)

Query = NewType("Query", str)
OutputFile = NewType("OutputFile", str)
OutputFilePrefix = NewType("OutputFilePrefix", str)
BatchSize = NewType("BatchSize", int)
FileFormat = NewType("FileFormat", str)


class SqlReader(abc.ABC):
    """
    Abstract class for readers of SQL queries.
    """

    @staticmethod
    def get_data_frame(df: Union[pd.DataFrame, Iterable[pd.DataFrame]]) -> pd.DataFrame:
        """Return the first `DataFrame` if given an iterable, or the given `DataFrame`."""
        if isinstance(df, pd.DataFrame):
            return df
        for chunk in df:
            return chunk
        return pd.DataFrame()

    @abc.abstractmethod
    def read_sql_query(self, query: Query) -> pd.DataFrame:
        """Execute the given query and return the content as a pandas DataFrame."""

    @abc.abstractmethod
    def read_sql_query_in_batches(
        self, query: Query, batch_size: BatchSize
    ) -> Iterator[pd.DataFrame]:
        """
        Execute the given query and return the content as a pandas DataFrame in chunks of the given
        batch size.
        """

    def read_sql_query_and_write_result(
        self,
        query: Query,
        output_file: Optional[OutputFile] = None,
        *,
        batch_size: Optional[BatchSize] = None,
    ) -> Optional[FileWritingResult]:
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
            return None
        return FileWriterProvider.get_file_writer(output_file).write_file(df, output_file)
