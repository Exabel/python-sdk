import pytest

from exabel.client.api.data_classes.dashboard import (
    DashboardWidget,
    TableColumn,
    WidgetType,
)
from exabel.stubs.exabel.api.management.v1.all_pb2 import (
    WIDGET_TYPE_CHART,
    WIDGET_TYPE_SIGNALS_TABLE,
    WIDGET_TYPE_UNSPECIFIED,
)
from exabel.stubs.exabel.api.management.v1.all_pb2 import (
    DashboardWidget as ProtoDashboardWidget,
)
from exabel.stubs.exabel.api.management.v1.all_pb2 import TableColumn as ProtoTableColumn
from exabel.stubs.exabel.api.management.v1.all_pb2 import WidgetType as ProtoWidgetType


class TestDashboardWidget:
    def test_from_proto(self):
        widget = DashboardWidget.from_proto(
            ProtoDashboardWidget(
                name="dashboards/1234/widgets/1",
                display_name="Revenue",
                description="Quarterly revenue",
                widget_type=WIDGET_TYPE_CHART,
                chart="charts/123",
            )
        )
        assert (
            DashboardWidget(
                name="dashboards/1234/widgets/1",
                display_name="Revenue",
                description="Quarterly revenue",
                widget_type=WidgetType.CHART,
                chart="charts/123",
                chart_not_found=False,
            )
            == widget
        )

    def test_from_proto__chart_defined_in_the_dashboard_has_no_chart_name(self):
        widget = DashboardWidget.from_proto(
            ProtoDashboardWidget(
                name="dashboards/1234/widgets/1", widget_type=WIDGET_TYPE_CHART, chart=""
            )
        )
        assert widget.chart is None

    def test_from_proto__missing_chart(self):
        widget = DashboardWidget.from_proto(
            ProtoDashboardWidget(
                name="dashboards/1234/widgets/1",
                widget_type=WIDGET_TYPE_CHART,
                chart="charts/123",
                chart_not_found=True,
            )
        )
        assert widget.chart_not_found

    def test_from_proto__undeterminable_type(self):
        widget = DashboardWidget.from_proto(
            ProtoDashboardWidget(
                name="dashboards/1234/widgets/1", widget_type=WIDGET_TYPE_UNSPECIFIED
            )
        )
        assert WidgetType.UNSPECIFIED == widget.widget_type

    def test_equals(self):
        widget = ProtoDashboardWidget(
            name="dashboards/1234/widgets/2",
            display_name="Table",
            widget_type=WIDGET_TYPE_SIGNALS_TABLE,
        )
        other = ProtoDashboardWidget(
            name="dashboards/1234/widgets/3",
            display_name="Table",
            widget_type=WIDGET_TYPE_SIGNALS_TABLE,
        )
        assert DashboardWidget.from_proto(widget) == DashboardWidget.from_proto(widget)
        assert DashboardWidget.from_proto(widget) != DashboardWidget.from_proto(other)


class TestTableColumn:
    def test_from_proto(self):
        column = TableColumn.from_proto(
            ProtoTableColumn(identifier="a1b2c3", display_name="Revenue", index=3)
        )
        assert TableColumn(identifier="a1b2c3", display_name="Revenue", index=3) == column

    def test_from_proto__entity_column(self):
        """
        Position 0 is the entity column, and 0 must not come back as None. Its identifier is the
        server's own literal, since every column reaching the SDK has one — the service drops the
        columns whose identifier is empty.
        """
        column = TableColumn.from_proto(
            ProtoTableColumn(identifier="entity_column_identifier", display_name="Company", index=0)
        )
        assert 0 == column.index
        assert "entity_column_identifier" == column.identifier

    def test_from_proto__position_left_unset_is_not_position_zero(self):
        column = TableColumn.from_proto(ProtoTableColumn(identifier="a1b2c3", display_name="Sales"))
        assert column.index is None

    def test_from_proto__the_same_column_twice_carries_one_identifier(self):
        first = ProtoTableColumn(identifier="a1b2c3", display_name="Sales", index=1)
        second = ProtoTableColumn(identifier="a1b2c3", display_name="Sales", index=2)
        columns = [TableColumn.from_proto(first), TableColumn.from_proto(second)]
        assert {"a1b2c3"} == {column.identifier for column in columns}
        assert [1, 2] == [column.index for column in columns]


class TestWidgetType:
    def test_a_value_this_version_does_not_know_is_unspecified(self):
        """
        Proto3 enums are open, so a server that gains a widget type sends its number to an SDK
        released before it. UNSPECIFIED already means "a widget whose type could not be
        determined", and raising instead would take the whole dashboard listing down.
        """
        assert WidgetType.UNSPECIFIED is WidgetType(99)

    def test_a_value_that_is_not_a_number_is_still_rejected(self):
        """The fallback is for unknown enum numbers, not for anything at all."""
        with pytest.raises(ValueError):
            WidgetType("WIDGET_TYPE_CHART")

    def test_every_proto_widget_type_is_mapped(self):
        """
        A widget type added to the proto and not here makes list_widgets raise, and takes the whole
        dashboard listing down with it rather than the one widget of the new type.
        """
        assert set(ProtoWidgetType.values()) == {widget_type.value for widget_type in WidgetType}
