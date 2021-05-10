from typing import Sequence, Union

from exabel_data_sdk.query.column import Column
from exabel_data_sdk.query.query import Query
from exabel_data_sdk.query.table import Table


class Dashboard:
    """
    Allows retrieving the contents of any dashboard widget the user has access to.

    If the widget ID is not specified, then the first widget in the dashboard is retrieved.
    """

    TABLE = Table("dashboard")

    DASHBOARD_ID = Column("dashboard_id")
    WIDGET_ID = Column("widget_id")

    @staticmethod
    def query(
        dashboard: Union[str, int], columns: Sequence[str] = None, widget: Union[str, int] = None
    ) -> Query:
        if columns is None:
            columns = ["*"]
        cols = [Column(column) for column in columns]
        filters = [Dashboard.DASHBOARD_ID.eq(dashboard)]
        if widget is not None:
            filters.append(Dashboard.WIDGET_ID.eq(widget))
        return Query(Dashboard.TABLE, cols, filters)
