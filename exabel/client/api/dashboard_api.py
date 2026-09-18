from typing import Sequence

from exabel.client.api.api_client.dashboard_api_client import DashboardApiClient
from exabel.client.api.api_client.grpc.dashboard_grpc_client import DashboardGrpcClient
from exabel.client.api.data_classes.dashboard import (
    DashboardWidget,
    TableColumn,
    WidgetType,
)
from exabel.client.client_config import ClientConfig
from exabel.stubs.exabel.api.management.v1.dashboard_service_pb2 import (
    ListTableColumnsRequest,
    ListWidgetsRequest,
)


class DashboardApi:
    """
    API class for inspecting dashboards.

    This is the discovery half of the dashboard exports: it hands out the widget names and
    column identifiers that `ExportApi.export_chart` and `ExportApi.export_dashboard_table`
    take as input. Find the dashboards themselves with `LibraryApi`, where they are folder
    items of type `DASHBOARD`.

    Dashboards are visible according to the authenticated caller. A customer's service
    account, authenticating with an API key, is a member of the customer user group and so
    sees dashboards shared with that group but not private ones; a personal access token
    additionally sees the user's own.
    """

    def __init__(self, config: ClientConfig):
        # Typed as the abstraction rather than the gRPC implementation, so a test can stand a
        # different client in without the type checker objecting.
        self.client: DashboardApiClient = DashboardGrpcClient(config)

    def list_widgets(
        self, dashboard: str, widget_type: WidgetType | None = None
    ) -> Sequence[DashboardWidget]:
        """
        List the widgets in a dashboard, in the order they appear in it.

        Args:
            dashboard:   Resource name of the dashboard, for example "dashboards/1234".
            widget_type: Only list widgets of this type. If not given, every type is listed.

        Returns:
            The dashboard's widgets. A chart widget's name is what `ExportApi.export_chart`
            renders, and a `SIGNALS_TABLE` widget's name is what
            `ExportApi.export_dashboard_table` exports.

            One `CHART` widget cannot be rendered: a chart widget in the older format reports
            as a chart, because that is what it is, but the export rejects it and says so. So
            iterating the `CHART` widgets of a dashboard and exporting each is not guaranteed
            to succeed for every one of them.
        """
        response = self.client.list_widgets(
            ListWidgetsRequest(
                parent=dashboard,
                widget_type=widget_type.value if widget_type is not None else None,
            )
        )
        return [DashboardWidget.from_proto(widget) for widget in response.widgets]

    def list_table_columns(self, table: str) -> Sequence[TableColumn]:
        """
        List the columns of one dashboard table widget, in the order they appear in it.

        The identifiers returned here are the only way to name a column precisely in an
        export, and they are computed when the table is calculated. Three consequences worth
        knowing before calling:

        - A table that has never been calculated, or whose last calculation failed, has no
          columns to report, and raises rather than returning an empty list. Calculation is a
          background job, so this one is worth retrying.
        - A company page dashboard's tables are calculated per entity when asked for rather than
          in the background, so their columns cannot be listed at all. This is permanent for that
          dashboard type, not something to retry, and it is reported as an invalid argument — the
          same error as naming a widget that is not a table.
        - A column added since the last calculation has no identifier yet and is not listed.
          Positions are absolute, so a gap in them is what reports such a column.

        Args:
            table: Resource name of the table widget, for example
                   "dashboards/1234/widgets/2". The widget must be a signals table; listing
                   the columns of any other kind of widget is an error. Find widget names
                   with `list_widgets`.

        Returns:
            The table's columns.
        """
        response = self.client.list_table_columns(ListTableColumnsRequest(parent=table))
        return [TableColumn.from_proto(column) for column in response.columns]
