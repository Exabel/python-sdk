from typing import Sequence, Union

import pandas as pd

from exabel_data_sdk.query.column import Column
from exabel_data_sdk.query.predicate import Predicate
from exabel_data_sdk.query.query import Query
from exabel_data_sdk.query.table import Table


class Signals:
    """
    The signals table allows evaluating and retrieving any signals from the user's library
    or arbitrary DSL expressions.
    """

    TABLE = Table("signals")

    TIME = Column("time")
    EXABEL_ID = Column("exabel_id")
    FACTSET_ID = Column("factset_id")

    @staticmethod
    def query(
        columns: Sequence[Union[str, Column]],
        filters: Sequence[Predicate],
        start_time: Union[str, pd.Timestamp] = None,
        end_time: Union[str, pd.Timestamp] = None,
    ) -> Query:
        cols = [Column(column) if isinstance(column, str) else column for column in columns]
        filters = list(filters)
        if start_time:
            filters.append(Signals.TIME.greater_eq(start_time))
        if end_time:
            filters.append(Signals.TIME.less_eq(end_time))
        return Query(Signals.TABLE, cols, filters)
