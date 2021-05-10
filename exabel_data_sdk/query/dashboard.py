from typing import Union, Sequence

from exabel_data_sdk.query.column import Column
from exabel_data_sdk.query.filter import Filter
from exabel_data_sdk.query.query import Query
from exabel_data_sdk.query.table import Table


class Dashboard:

    TABLE = Table("dashboard")
    DASHBOARD_ID = Column("dashboard_id")
    WIDGET_ID = Column("widget_id")

    @staticmethod
    def query(dashboard: Union[str, int], columns: Sequence[str] = None, widget: Union[str, int] = None) -> Query:
        if columns is None:
            columns = ["*"]
        cols = [Column(column) for column in columns]
        filters = [Filter.eq(Dashboard.DASHBOARD_ID, dashboard)]
        if widget is not None:
            filters.append(Filter.eq(Dashboard.WIDGET_ID, widget))
        return Query(Dashboard.TABLE, cols, filters)
