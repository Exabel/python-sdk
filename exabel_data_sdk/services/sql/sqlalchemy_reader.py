import logging
import time
from typing import Any, Iterator, Mapping, Optional

import pandas as pd

from exabel_data_sdk.services.sql.sql_reader import BatchSize, Query, SqlReader
from exabel_data_sdk.services.sql.sql_reader_configuration import ConnectionString
from exabel_data_sdk.util.handle_missing_imports import handle_missing_imports

with handle_missing_imports():
    from sqlalchemy import create_engine

logger = logging.getLogger(__name__)


class SQLAlchemyReader(SqlReader):
    """Reader of SQL queries using SQLAlchemy."""

    def __init__(
        self, connection_string: ConnectionString, *, kwargs: Optional[Mapping[str, Any]] = None
    ) -> None:
        kwargs = kwargs or {}
        self.engine = create_engine(connection_string, **kwargs)

    def read_sql_query(self, query: Query) -> pd.DataFrame:
        """Execute the given query and return the content as a pandas DataFrame."""
        try:
            return pd.read_sql_query(query, self.engine)
        except Exception as e:
            logger.error("An error occurred while executing the query: %s", str(e))
            raise

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
            current_time = time.time()
            for batch_no, chunk in enumerate(reader, 1):
                logger.info(
                    "Reading batch no: %d Row count: %d Time spent: %.1fs",
                    batch_no,
                    len(chunk),
                    round(time.time() - current_time, 1),
                )
                current_time = time.time()
                yield chunk
        except Exception as e:
            logger.error(
                "An error occurred in batch number %d while executing the query: %s",
                batch_no,
                str(e),
            )
            raise
        logger.info("Finished reading %d batches", batch_no)
