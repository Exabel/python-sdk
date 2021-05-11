import unittest

import pandas as pd

from exabel_data_sdk.query.column import Column
from exabel_data_sdk.query.dashboard import Dashboard
from exabel_data_sdk.query.literal import to_sql
from exabel_data_sdk.query.signals import Signals


class TestQuery(unittest.TestCase):
    def test_escape(self):
        self.assertEqual("123", to_sql(123))
        self.assertEqual("'foo'", to_sql("foo"))
        self.assertEqual("'foo'", to_sql("foo"))
        self.assertEqual("''''", to_sql("'"))
        self.assertEqual("'\"'", to_sql('"'))
        self.assertEqual("'\\\"'", to_sql('\\"'))
        self.assertEqual("'''\\'''''", to_sql("'\\''"))

    def test_dashboard_queries(self):
        self.assertEqual(
            "SELECT * FROM dashboard WHERE dashboard_id = 123", Dashboard.query(123).sql()
        )
        self.assertEqual(
            "SELECT foo, bar FROM dashboard WHERE dashboard_id = 'dash:123' "
            "AND widget_id = 'widget:123'",
            Dashboard.query("dash:123", ["foo", "bar"], "widget:123").sql(),
        )
        self.assertEqual(
            "SELECT foo, bar FROM dashboard WHERE dashboard_id = 'dash''123' "
            "AND widget_id = 'widget\"123'",
            Dashboard.query("dash'123", ["foo", "bar"], 'widget"123').sql(),
        )

    def test_signals_queries(self):
        self.assertEqual("SELECT my_signal FROM signals", Signals.query(["my_signal"]).sql())
        self.assertEqual(
            "SELECT a, b FROM signals WHERE factset_id IN ('FA', 'FB') "
            "AND time >= '2020-01-01' AND time <= '2020-12-31'",
            Signals.query(
                ["a", "b"],
                start_time="2020-01-01",
                end_time=pd.Timestamp("2020-12-31"),
                predicates=[Signals.FACTSET_ID.in_list("FA", "FB")],
            ).sql(),
        )
        self.assertEqual(
            "SELECT 'a+b' AS total, 'get(''foo'')' AS myget FROM signals "
            "WHERE has_tag('signal:dynamicTag:367') AND time >= '2020-01-01'",
            Signals.query(
                [Column("total", "a+b"), Column("myget", "get('foo')")],
                "signal:dynamicTag:367",
                "2020-01-01",
            ).sql(),
        )
