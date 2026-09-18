"""Argument types for the dashboard table export.

These build the JSON body of `POST /v1/export/dashboardTable` rather than a protobuf
message: the SDK ships no stubs for `exabel.export`, and the endpoint is proto3 JSON
over HTTP, so the wire form is the only contract there is. Field names below are the
proto-JSON spellings of `ExportDashboardTableRequest`, and unset fields are left out
rather than sent as nulls, which is what proto3 JSON parsing expects.
"""

from dataclasses import dataclass

# How one column of a dashboard table is named: by its identifier or display name, or by
# its position in the table, counting the entity column as 0.
#
# Identifiers come from the Management API's "List dashboard table columns" method and
# name a column precisely. They are content hashes of the column definition, so editing
# a column — renaming it included — gives it a new one: list the columns again rather
# than storing an identifier between sessions. Display names need not be unique, and are
# matched ignoring case and surrounding whitespace; a filter or an ordering naming a
# column that occurs twice is an error, since each applies to one column.
ColumnRef = str | int


def column_ref_to_json(column: ColumnRef) -> dict[str, str | int]:
    """Convert a column reference to the TableColumnRef JSON form."""
    if isinstance(column, bool) or not isinstance(column, (str, int)):
        raise ValueError(
            f"A column must be named by its identifier or display name, or by its position "
            f"as an integer, but got {column!r}"
        )
    if isinstance(column, str):
        if not column:
            raise ValueError("A column name must not be empty")
        return {"column": column}
    if column < 0:
        raise ValueError(f"A column position must not be negative, but got {column}")
    return {"index": column}


@dataclass(frozen=True)
class Interval:
    """A one- or two-sided interval, used by both the numeric and the date filters.

    Serializes to the same JSON in both cases, since the protobuf wrappers the two
    intervals use render as plain numbers. A bound left unset is unbounded, so
    `Interval(start=5)` means "at least 5". The `open_at_*` flags exclude a bound, which
    is the only way to express a strict comparison: `above=5` keeps a value of exactly 5,
    while `Interval(start=5, open_at_start=True)` does not.
    """

    start: float | None = None
    end: float | None = None
    open_at_start: bool = False
    open_at_end: bool = False

    def to_json(self) -> dict[str, float | bool]:
        """Convert to the interval JSON form, omitting unset bounds and false flags."""
        if self.start is None and self.end is None:
            raise ValueError("An interval must have at least one of start and end set")
        body: dict[str, float | bool] = {}
        if self.start is not None:
            body["start"] = self.start
            if self.open_at_start:
                body["openAtStart"] = True
        if self.end is not None:
            body["end"] = self.end
            if self.open_at_end:
                body["openAtEnd"] = True
        return body


@dataclass(frozen=True)
class TableColumnFilter:
    """A filter on the values of one dashboard table column.

    Exactly one of the expressions must be given. A row is exported only if it passes
    every filter in the request, and a cell holding no value of the filter's kind never
    passes: a numeric filter drops rows whose cell is empty or textual, and a date filter
    drops rows whose cell carries no timestamp.

    Args:
        column:               the column whose values are filtered.
        above:                keep values greater than or equal to this.
        below:                keep values less than or equal to this.
        between:              keep values inside this interval.
        outside:              keep values outside this interval.
        inside_relative_days: keep dates inside this interval, counted in days from today
                              and signed: -30 is thirty days ago, 30 is thirty days ahead.

    Example::

        TableColumnFilter("Market cap", above=1e9)
        TableColumnFilter("Next report", inside_relative_days=Interval(start=0, end=30))
    """

    column: ColumnRef
    above: float | None = None
    below: float | None = None
    between: Interval | None = None
    outside: Interval | None = None
    inside_relative_days: Interval | None = None

    def to_json(self) -> dict[str, object]:
        """Convert to the TableColumnFilter JSON form."""
        expressions: dict[str, dict[str, float | Interval | None]] = {
            "numericFilter": {
                "above": self.above,
                "below": self.below,
                "between": self.between,
                "outside": self.outside,
            },
            "dateFilter": {"insideRelativeDays": self.inside_relative_days},
        }
        given = {
            (filter_type, name): value
            for filter_type, expression in expressions.items()
            for name, value in expression.items()
            if value is not None
        }
        if len(given) != 1:
            raise ValueError(
                f"A filter on column {self.column!r} must give exactly one of above, below, "
                f"between, outside and inside_relative_days, but "
                f"{sorted(name for _, name in given) or 'none'} was given"
            )
        (filter_type, name), value = next(iter(given.items()))
        return {
            "column": column_ref_to_json(self.column),
            filter_type: {name: value.to_json() if isinstance(value, Interval) else value},
        }


@dataclass(frozen=True)
class TableColumnOrdering:
    """Orders the rows of a dashboard table by the values of one of its columns.

    Rows whose cell in the column has no value are placed last in both directions.

    Args:
        column:     the column whose values the rows are ordered by.
        descending: sort descending rather than ascending.
        use_ticker: order companies by their Bloomberg ticker rather than by their
                    displayed name. Applies only to the entity column, at position 0;
                    setting it on any other column is an error rather than a flag that
                    does nothing. Note that the Bloomberg ticker is not necessarily the
                    ticker the table displays.
    """

    column: ColumnRef
    descending: bool = False
    use_ticker: bool = False

    def to_json(self) -> dict[str, object]:
        """Convert to the TableColumnOrdering JSON form."""
        body: dict[str, object] = {"column": column_ref_to_json(self.column)}
        if self.descending:
            body["direction"] = "DESCENDING"
        if self.use_ticker:
            body["useTicker"] = True
        return body
