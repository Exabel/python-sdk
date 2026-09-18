"""The dashboard resources the Management API reports.

All three are output only: the Management API inspects dashboards and does not create
them, so these are read from protos and never written back to one. That is why there is
no `to_proto` here, unlike most data classes in this package.
"""

from dataclasses import dataclass
from enum import Enum

from exabel.stubs.exabel.api.management.v1.all_pb2 import (
    DashboardWidget as ProtoDashboardWidget,
)
from exabel.stubs.exabel.api.management.v1.all_pb2 import TableColumn as ProtoTableColumn
from exabel.stubs.exabel.api.management.v1.all_pb2 import WidgetType as ProtoWidgetType


class WidgetType(Enum):
    """Enum representing the type of a dashboard widget."""

    # A widget whose type this SDK could not determine, either because the server could not
    # either or because the server knows a type this version does not. In a request, every type.
    UNSPECIFIED = ProtoWidgetType.WIDGET_TYPE_UNSPECIFIED
    # A chart. Only these can be rendered with the Export API, and not all of them: a chart
    # widget in the older format reports as a chart but the export rejects it, saying so.
    CHART = ProtoWidgetType.WIDGET_TYPE_CHART
    # A table of cells consisting of signal data.
    SIGNALS_TABLE = ProtoWidgetType.WIDGET_TYPE_SIGNALS_TABLE
    # A financial model.
    FINANCIAL_MODEL = ProtoWidgetType.WIDGET_TYPE_FINANCIAL_MODEL
    # Text.
    TEXT = ProtoWidgetType.WIDGET_TYPE_TEXT
    # A table of cells consisting of portfolio data.
    PORTFOLIO = ProtoWidgetType.WIDGET_TYPE_PORTFOLIO

    @classmethod
    def _missing_(cls, value: object) -> "WidgetType | None":
        """
        Report a widget type this version does not know as UNSPECIFIED.

        Proto3 enums are open, so a server that has gained a widget type sends its number to an
        SDK released before it, and the number survives the wire as a plain int. Raising here
        would cost the caller the whole listing — every chart and table in the dashboard — over
        one widget of a type they were not asking about.
        """
        return cls.UNSPECIFIED if isinstance(value, int) else None


@dataclass(frozen=True)
class DashboardWidget:
    """A widget in a dashboard.

    Attributes:
        name:            Widget resource name, e.g. "dashboards/1234/widgets/1". Widget ids
                         are unique only within their dashboard, so a widget is always named
                         relative to the dashboard holding it. This is the name the Export
                         API's chart export accepts for a chart widget — except for a chart
                         widget in the older format, which reports as `CHART` here but which
                         the export rejects as not renderable.
        display_name:    The widget heading shown in the Exabel web app.
        description:     The text under the widget heading in the Exabel web app.
        widget_type:     The widget type.
        chart:           For a chart widget showing a saved chart, that chart's resource
                         name, e.g. "charts/123". None for a chart defined in the dashboard
                         itself, for a chart widget in the older format, and for every other
                         widget type. A widget that has one can be exported by either name.
        chart_not_found: Whether the chart named by `chart` can no longer be read, because it
                         was deleted or is no longer shared with you. The widget still
                         appears in the dashboard but cannot be exported.
    """

    name: str
    display_name: str
    description: str
    widget_type: WidgetType
    chart: str | None = None
    chart_not_found: bool = False

    @classmethod
    def from_proto(cls, widget: ProtoDashboardWidget) -> "DashboardWidget":
        """Create a DashboardWidget from the given protobuf DashboardWidget."""
        return cls(
            name=widget.name,
            display_name=widget.display_name,
            description=widget.description,
            widget_type=WidgetType(widget.widget_type),
            chart=widget.chart or None,
            chart_not_found=widget.chart_not_found,
        )


@dataclass(frozen=True)
class TableColumn:
    """A column of a dashboard table widget.

    Attributes:
        identifier:   Names this column when exporting the table with the Export API.
                      Derived from the column's definition, so editing the column — renaming
                      it included — gives it a new identifier. List the columns again rather
                      than storing one between sessions. A table may hold the same column
                      twice, and both copies then carry this identifier; use `index` where a
                      reference has to name exactly one of them.
        display_name: The column heading shown in the Exabel web app. Not necessarily
                      unique: a table may hold two columns with the same heading.
        index:        The position of this column in the table, counting from 0, where
                      position 0 holds the entity each row is about and is the column to sort
                      by when ordering rows by company name or ticker. A position names
                      exactly one column, but changes whenever columns to its left are added,
                      removed or reordered. None only for a column the server did not report
                      a position for, which the API says it always does — so treat it as a
                      column that cannot be named by position rather than as position 0.
    """

    identifier: str
    display_name: str
    index: int | None = None

    @classmethod
    def from_proto(cls, column: ProtoTableColumn) -> "TableColumn":
        """Create a TableColumn from the given protobuf TableColumn."""
        return cls(
            identifier=column.identifier,
            display_name=column.display_name,
            # The proto field has explicit presence, so an unset position is distinguishable
            # from position 0 — and conflating the two would silently point a caller at the
            # entity column.
            index=column.index if column.HasField("index") else None,
        )
