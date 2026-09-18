import pytest

from exabel.client.api.data_classes.dashboard_table import (
    Interval,
    TableColumnFilter,
    TableColumnOrdering,
    column_ref_to_json,
)


class TestColumnRef:
    def test_name_becomes_the_column_field(self):
        assert column_ref_to_json("Revenue") == {"column": "Revenue"}

    def test_position_becomes_the_index_field(self):
        assert column_ref_to_json(0) == {"index": 0}

    def test_empty_name_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            column_ref_to_json("")

    def test_negative_position_raises(self):
        with pytest.raises(ValueError, match="must not be negative"):
            column_ref_to_json(-1)

    def test_other_type_raises(self):
        with pytest.raises(ValueError, match="identifier or display name"):
            column_ref_to_json(1.5)

    def test_boolean_is_not_a_position(self):
        with pytest.raises(ValueError, match="identifier or display name"):
            column_ref_to_json(True)


class TestInterval:
    def test_both_bounds(self):
        assert Interval(start=1, end=2).to_json() == {"start": 1, "end": 2}

    def test_one_bound_is_unbounded_on_the_other_side(self):
        assert Interval(start=-30).to_json() == {"start": -30}

    def test_open_bounds(self):
        assert Interval(start=1, end=2, open_at_start=True, open_at_end=True).to_json() == {
            "start": 1,
            "openAtStart": True,
            "end": 2,
            "openAtEnd": True,
        }

    def test_open_flag_without_its_bound_is_dropped(self):
        assert Interval(end=2, open_at_start=True).to_json() == {"end": 2}

    def test_no_bounds_raises(self):
        with pytest.raises(ValueError, match="at least one of start and end"):
            Interval().to_json()


class TestTableColumnFilter:
    def test_numeric_bound(self):
        assert TableColumnFilter("Market cap", above=1e9).to_json() == {
            "column": {"column": "Market cap"},
            "numericFilter": {"above": 1e9},
        }

    def test_numeric_interval_by_position(self):
        assert TableColumnFilter(3, between=Interval(start=5, open_at_start=True)).to_json() == {
            "column": {"index": 3},
            "numericFilter": {"between": {"start": 5, "openAtStart": True}},
        }

    def test_date_filter(self):
        assert TableColumnFilter(
            "Next report", inside_relative_days=Interval(start=0, end=30)
        ).to_json() == {
            "column": {"column": "Next report"},
            "dateFilter": {"insideRelativeDays": {"start": 0, "end": 30}},
        }

    def test_zero_is_a_bound_rather_than_an_unset_field(self):
        assert TableColumnFilter("Change", below=0).to_json() == {
            "column": {"column": "Change"},
            "numericFilter": {"below": 0},
        }

    def test_no_expression_raises(self):
        with pytest.raises(ValueError, match="exactly one of above, below"):
            TableColumnFilter("Revenue").to_json()

    def test_two_expressions_raise(self):
        with pytest.raises(ValueError, match="exactly one of above, below"):
            TableColumnFilter("Revenue", above=1, below=2).to_json()

    def test_a_numeric_and_a_date_expression_raise(self):
        with pytest.raises(ValueError, match="exactly one of above, below"):
            TableColumnFilter("Revenue", above=1, inside_relative_days=Interval(start=0)).to_json()


class TestTableColumnOrdering:
    def test_ascending_is_the_default_and_is_not_sent(self):
        assert TableColumnOrdering("Revenue").to_json() == {"column": {"column": "Revenue"}}

    def test_descending(self):
        assert TableColumnOrdering("Revenue", descending=True).to_json() == {
            "column": {"column": "Revenue"},
            "direction": "DESCENDING",
        }

    def test_use_ticker_on_the_entity_column(self):
        assert TableColumnOrdering(0, use_ticker=True).to_json() == {
            "column": {"index": 0},
            "useTicker": True,
        }
