import unittest

import pandas as pd

from exabel.query.column import Column
from exabel.query.dashboard import Dashboard
from exabel.query.literal import to_sql
from exabel.query.signals import Signals


class TestQuery(unittest.TestCase):
    def test_escape(self):
        assert "123" == to_sql(123)
        assert "'foo'" == to_sql("foo")
        assert "'foo'" == to_sql("foo")
        assert "''''" == to_sql("'")
        assert "'\"'" == to_sql('"')
        assert "'\\\"'" == to_sql('\\"')
        assert "'''\\'''''" == to_sql("'\\''")

    def test_dashboard_queries(self):
        assert "SELECT * FROM dashboard WHERE dashboard_id = 123" == Dashboard.query(123).sql()
        assert (
            "SELECT foo, bar FROM dashboard WHERE dashboard_id = 'dash:123' "
            "AND widget_id = 'widget:123'"
            == Dashboard.query("dash:123", ["foo", "bar"], "widget:123").sql()
        )
        assert (
            "SELECT foo, bar FROM dashboard WHERE dashboard_id = 'dash''123' "
            "AND widget_id = 'widget\"123'"
            == Dashboard.query("dash'123", ["foo", "bar"], 'widget"123').sql()
        )

    def test_signals_queries(self):
        assert "SELECT my_signal FROM signals" == Signals.query(["my_signal"]).sql()
        assert (
            "SELECT a, b FROM signals WHERE factset_id IN ('FA', 'FB') "
            "AND time >= '2020-01-01' AND time <= '2020-12-31'"
            == Signals.query(
                ["a", "b"],
                start_time="2020-01-01",
                end_time=pd.Timestamp("2020-12-31"),
                predicates=[Signals.FACTSET_ID.in_list("FA", "FB")],
            ).sql()
        )
        assert (
            "SELECT 'a+b' AS total, 'get(''foo'')' AS myget FROM signals "
            "WHERE has_tag('signal:dynamicTag:367') AND time >= '2020-01-01'"
            == Signals.query(
                [Column("total", "a+b"), Column("myget", "get('foo')")],
                "signal:dynamicTag:367",
                "2020-01-01",
            ).sql()
        )
