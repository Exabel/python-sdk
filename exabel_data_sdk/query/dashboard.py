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
        """
        Build a query for the dashboard table.

        Args:
            dashboard: the ID of the dashboard to request, as "dashboard:dashboard:123" or just 123
            columns:   the specific columns to retrieve. Defaults to retrieving all columns.
            widget:    the widget to retrieve, as "dashboard:widget:1" or just 1.
                       Defaults to retrieving the first widget in the dashboard.
        """
        if columns is None:
            columns = ["*"]
        cols = [Column(column) for column in columns]
        filters = [Dashboard.DASHBOARD_ID.equal(dashboard)]
        if widget is not None:
            filters.append(Dashboard.WIDGET_ID.equal(widget))
        return Query(Dashboard.TABLE, cols, filters)
