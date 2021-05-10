import unittest

from exabel_data_sdk.query.column import Column
from exabel_data_sdk.query.dashboard import Dashboard
from exabel_data_sdk.query.filter import to_sql


class TestQuery(unittest.TestCase):

    def test_escape(self):
        self.assertEqual("123", to_sql(123))
        self.assertEqual("foo", to_sql(Column("foo")))
        self.assertEqual("'foo'", to_sql("foo"))
        self.assertEqual("'foo'", to_sql("foo"))
        self.assertEqual("''''", to_sql("'"))
        self.assertEqual('\'"\'', to_sql('"'))
        self.assertEqual('\'\\"\'', to_sql('\\"'))
        self.assertEqual("'''\\'''''", to_sql("'\\''"))

    def test_dashboard_queries(self):
        self.assertEqual("SELECT * FROM dashboard WHERE dashboard_id = 123",
                         Dashboard.query(123).sql())
        self.assertEqual(
            "SELECT foo, bar FROM dashboard WHERE dashboard_id = 'dash:123' "
            "AND widget_id = 'widget:123'",
            Dashboard.query('dash:123', ["foo", "bar"], "widget:123").sql())
        self.assertEqual(
            "SELECT foo, bar FROM dashboard WHERE dashboard_id = 'dash''123' "
            "AND widget_id = 'widget\"123'",
            Dashboard.query("dash'123", ["foo", "bar"], "widget\"123").sql())
