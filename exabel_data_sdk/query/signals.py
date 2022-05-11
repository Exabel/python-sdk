from typing import Sequence, Union

import pandas as pd

from exabel_data_sdk.query.column import Column
from exabel_data_sdk.query.predicate import FunctionPredicate, Predicate
from exabel_data_sdk.query.query import Query
from exabel_data_sdk.query.table import Table


class Signals:
    """
    The signals table allows evaluating and retrieving any signals from the user's library
    or arbitrary DSL expressions.
    """

    TABLE = Table("signals")

    # Special columns. Refer to online documentation for descriptions:
    # https://help.exabel.com/docs/exporting-via-exabel-sdk
    TIME = Column("time")
    VERSION = Column("version")
    LABEL = Column("label")
    NAME = Column("name")
    BLOOMBERG_TICKER = Column("bloomberg_ticker")
    FACTSET_ID = Column("factset_id")
    ISIN = Column("isin")
    MIC = Column("mic")
    TICKER = Column("ticker")
    EXABEL_ID = Column("exabel_id")
    RESOURCE_NAME = Column("resource_name")

    @staticmethod
    def query(
        columns: Sequence[Union[str, Column]],
        tag: Union[str, Sequence[str]] = None,
        start_time: Union[str, pd.Timestamp] = None,
        end_time: Union[str, pd.Timestamp] = None,
        predicates: Sequence[Predicate] = (),
    ) -> Query:
        """
        Build a query for the signals table.
        All signals are time series.

        There are four types of columns:
         - The 'time' column which contains the date of a data point in a time series.
         - Entity identifiers (such as Exabel ID or FactSet ID) for the entity the time series
           applies to. The entity would typically be a company, but could also be e.g. a brand
           or a sector.
         - A signal from the user's signal library
         - A DSL expression provided as part of the query, using the following syntax:
              'expression' AS name

        Most of the time, one would want to specify predicates for the entity IDs to limit
        the scope of which entities the signals are evaluated for. Many signals will require
        such a limitation.

        Args:
            columns:    the columns to retrieve, as string identifiers or Column objects.
                        At least one column must be requested.
            tag:        retrieve data for the entities with this tag,
                        or with any of the provided tags if several.
            start_time: the first date to retrieve data for
            end_time:   the last date to retrieve data for
            predicates: any additional conditions for what data to include
        """
        if len(columns) == 0:
            raise ValueError("Need to query for at least one column")
        cols = [Column(column) if isinstance(column, str) else column for column in columns]
        predicates = list(predicates)
        if tag:
            if isinstance(tag, str):
                tag = [tag]
            predicates.append(Signals.has_tag(*tag))
        if start_time:
            predicates.append(Signals.TIME.greater_eq(start_time))
        if end_time:
            predicates.append(Signals.TIME.less_eq(end_time))
        return Query(Signals.TABLE, cols, predicates)

    @staticmethod
    def has_tag(*tags: str) -> FunctionPredicate:
        """Returns a predicate for entities having at least one of the provided tags."""
        return FunctionPredicate("has_tag", tags)
