from typing import Sequence

from exabel.client.api.api_client.dashboard_api_client import DashboardApiClient
from exabel.client.api.dashboard_api import DashboardApi
from exabel.client.api.data_classes.dashboard import (
    DashboardWidget,
    TableColumn,
    WidgetType,
)
from exabel.client.client_config import ClientConfig
from exabel.stubs.exabel.api.management.v1.all_pb2 import (
    WIDGET_TYPE_CHART,
    WIDGET_TYPE_SIGNALS_TABLE,
    WIDGET_TYPE_UNSPECIFIED,
    ListTableColumnsRequest,
    ListTableColumnsResponse,
    ListWidgetsRequest,
    ListWidgetsResponse,
)
from exabel.stubs.exabel.api.management.v1.all_pb2 import (
    DashboardWidget as ProtoDashboardWidget,
)
from exabel.stubs.exabel.api.management.v1.all_pb2 import TableColumn as ProtoTableColumn

# What the server calls the column holding the entity of each row, verbatim: the export
# service's own error message lists it as "Company (entity_column_identifier)". Every column
# reaching the SDK has an identifier, since the service drops the ones without.
ENTITY_COLUMN = "entity_column_identifier"

# The field number of DashboardWidget.widget_type, for hand-encoding a value the generated
# enum refuses to hold.
_WIDGET_TYPE_FIELD = ProtoDashboardWidget.DESCRIPTOR.fields_by_name["widget_type"].number


class _FakeDashboardApiClient(DashboardApiClient):
    """Records the requests it is given, so the request the API builds can be asserted on."""

    def __init__(
        self,
        widgets: Sequence[ProtoDashboardWidget] = (),
        columns: Sequence[ProtoTableColumn] = (),
    ):
        self._widgets = widgets
        self._columns = columns
        self.widgets_request: ListWidgetsRequest | None = None
        self.columns_request: ListTableColumnsRequest | None = None

    def list_widgets(self, request: ListWidgetsRequest) -> ListWidgetsResponse:
        self.widgets_request = request
        return ListWidgetsResponse(widgets=self._widgets)

    def list_table_columns(self, request: ListTableColumnsRequest) -> ListTableColumnsResponse:
        self.columns_request = request
        return ListTableColumnsResponse(columns=self._columns)


def _dashboard_api(client: _FakeDashboardApiClient) -> DashboardApi:
    """A real DashboardApi with its gRPC client swapped out.

    The API's own __init__ runs, so the channel it builds is covered; gRPC channels connect
    lazily, so nothing reaches the network.
    """
    api = DashboardApi(ClientConfig(api_key="api-key"))
    api.client = client
    return api


class TestDashboardApi:
    def test_list_widgets(self):
        client = _FakeDashboardApiClient(
            widgets=[
                ProtoDashboardWidget(
                    name="dashboards/1234/widgets/1",
                    display_name="Revenue chart",
                    widget_type=WIDGET_TYPE_CHART,
                    chart="charts/123",
                ),
                ProtoDashboardWidget(
                    name="dashboards/1234/widgets/2",
                    display_name="Peers",
                    widget_type=WIDGET_TYPE_SIGNALS_TABLE,
                ),
            ]
        )

        widgets = _dashboard_api(client).list_widgets("dashboards/1234")

        assert ListWidgetsRequest(parent="dashboards/1234") == client.widgets_request
        assert [
            DashboardWidget(
                name="dashboards/1234/widgets/1",
                display_name="Revenue chart",
                description="",
                widget_type=WidgetType.CHART,
                chart="charts/123",
            ),
            DashboardWidget(
                name="dashboards/1234/widgets/2",
                display_name="Peers",
                description="",
                widget_type=WidgetType.SIGNALS_TABLE,
            ),
        ] == list(widgets)

    def test_list_widgets__no_type_given_does_not_filter(self):
        """An unset widget type is what the service reads as "every type"."""
        client = _FakeDashboardApiClient()

        _dashboard_api(client).list_widgets("dashboards/1234")

        assert WIDGET_TYPE_UNSPECIFIED == client.widgets_request.widget_type

    def test_list_widgets__a_widget_type_this_version_does_not_know_keeps_the_listing(self):
        """
        Proto3 enums are open, so a newer server can report a widget type this SDK has no member
        for. Losing that one widget's type is acceptable; losing the chart and the table next to
        it, which is what raising would do, is not.
        """
        future_widget = ProtoDashboardWidget(name="dashboards/1234/widgets/1")
        # Written as bytes because the generated enum will not hold a value it does not know,
        # which is exactly the position a released SDK is in.
        future_widget.MergeFromString(bytes([_WIDGET_TYPE_FIELD << 3, 99]))
        assert 99 == future_widget.widget_type, "the unknown value must survive the parse"
        client = _FakeDashboardApiClient(
            widgets=[
                future_widget,
                ProtoDashboardWidget(
                    name="dashboards/1234/widgets/2", widget_type=WIDGET_TYPE_CHART
                ),
            ]
        )

        widgets = _dashboard_api(client).list_widgets("dashboards/1234")

        assert [WidgetType.UNSPECIFIED, WidgetType.CHART] == [
            widget.widget_type for widget in widgets
        ]

    def test_list_widgets__filters_on_type(self):
        client = _FakeDashboardApiClient()

        _dashboard_api(client).list_widgets("dashboards/1234", WidgetType.SIGNALS_TABLE)

        assert (
            ListWidgetsRequest(parent="dashboards/1234", widget_type=WIDGET_TYPE_SIGNALS_TABLE)
            == client.widgets_request
        )

    def test_list_widgets__empty_dashboard(self):
        assert [] == list(_dashboard_api(_FakeDashboardApiClient()).list_widgets("dashboards/1"))

    def test_list_table_columns(self):
        client = _FakeDashboardApiClient(
            columns=[
                ProtoTableColumn(identifier=ENTITY_COLUMN, display_name="Company", index=0),
                ProtoTableColumn(identifier="a1b2c3", display_name="Revenue", index=1),
            ]
        )

        columns = _dashboard_api(client).list_table_columns("dashboards/1234/widgets/2")

        assert ListTableColumnsRequest(parent="dashboards/1234/widgets/2") == client.columns_request
        assert [
            TableColumn(identifier=ENTITY_COLUMN, display_name="Company", index=0),
            TableColumn(identifier="a1b2c3", display_name="Revenue", index=1),
        ] == list(columns)

    def test_list_table_columns__a_gap_in_the_positions_reports_an_uncalculated_column(self):
        client = _FakeDashboardApiClient(
            columns=[
                ProtoTableColumn(identifier=ENTITY_COLUMN, display_name="Company", index=0),
                ProtoTableColumn(identifier="a1b2c3", display_name="Revenue", index=2),
            ]
        )

        columns = _dashboard_api(client).list_table_columns("dashboards/1234/widgets/2")

        assert [0, 2] == [column.index for column in columns]
