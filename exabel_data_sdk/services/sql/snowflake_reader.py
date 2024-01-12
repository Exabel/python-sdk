import logging
from typing import Any, Iterator, Mapping, Optional

import pandas as pd

from exabel_data_sdk.services.sql.sql_reader import BatchSize, Query, SqlReader
from exabel_data_sdk.util.handle_missing_imports import handle_missing_imports

with handle_missing_imports():
    from snowflake.connector import connect

logger = logging.getLogger(__name__)

SNOWFLAKE_MIN_ROWCOUNT_FOR_BATCHING = 500_000


class SnowflakeReader(SqlReader):
    """Reader of SQL queries from Snowflake."""

    def __init__(
        self, connection_args: Mapping[str, Any], *, kwargs: Optional[Mapping[str, Any]] = None
    ) -> None:
        self.kwargs = kwargs or {}
        self.connection_args = connection_args

    def read_sql_query(self, query: Query) -> pd.DataFrame:
        """Execute the given query and return the content as a pandas DataFrame."""
        try:
            with connect(**self.connection_args, **self.kwargs) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    logger.info("Query returned %d rows", cursor.rowcount)
                    return cursor.fetch_pandas_all()
        except Exception as e:
            logger.error("An error occurred while executing the query: %s", str(e))
            raise

    def read_sql_query_in_batches(
        self, query: Query, batch_size: BatchSize
    ) -> Iterator[pd.DataFrame]:
        """
        Execute the given query and return the content as a pandas DataFrame in chunks.
        """
        logger.info(
            "Reading query in batches from Snowflake. batch_size = %d "
            "will be ignored and will instead be calculated dynamically.",
            batch_size,
        )

        batch_no = 0
        try:
            with connect(**self.connection_args, **self.kwargs) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    logger.info("Query returned %d rows", cursor.rowcount)
                    if (
                        cursor.rowcount is not None
                        and cursor.rowcount <= SNOWFLAKE_MIN_ROWCOUNT_FOR_BATCHING
                    ):
                        batch_no += 1
                        yield cursor.fetch_pandas_all()
                    else:
                        for chunk in cursor.fetch_pandas_batches():
                            batch_no += 1
                            logger.info("Reading batch no: %d Row count: %d", batch_no, len(chunk))
                            yield chunk
        except Exception as e:
            logger.error(
                "An error occurred in batch number %d while executing the query: %s",
                batch_no,
                str(e),
            )
            raise
        logger.info("Finished reading %d batches", batch_no)
