import unittest
from unittest.mock import MagicMock

from exabel_data_sdk.client.api.export_api import ExportApi
from exabel_data_sdk.query.column import Column


class TestExportApi(unittest.TestCase):
    def test_signal_query(self):
        export_api = ExportApi(auth_headers={})
        mock = MagicMock(name="run_query")
        export_api.run_query = mock

        def check_query(sql: str) -> None:
            query = mock.call_args.args[0]
            self.assertEqual(sql, query.sql())

        export_api.signal_query(Column("EURUSD", "fx('EUR', 'USD')"))
        check_query("SELECT time, 'fx(''EUR'', ''USD'')' AS EURUSD FROM signals")

        export_api.signal_query("Sales_Actual", factset_id="QLGSL2-R")
        check_query("SELECT time, Sales_Actual FROM signals WHERE factset_id = 'QLGSL2-R'")

        export_api.signal_query("Sales_Actual", bloomberg_ticker=["AAPL US", "TSLA US"])
        check_query(
            "SELECT name, time, Sales_Actual FROM signals "
            "WHERE bloomberg_ticker IN ('AAPL US', 'TSLA US')"
        )

        export_api.signal_query("Sales_Actual", tag="graph:tag:user:xyz-123")
        check_query(
            "SELECT name, time, Sales_Actual FROM signals WHERE has_tag('graph:tag:user:xyz-123')"
        )

        column = Column("Q", "sales_actual(alignment='afp')")
        export_api.signal_query(["Sales_Actual_fiscal", column], "AAPL US")
        check_query(
            "SELECT time, Sales_Actual_fiscal, 'sales_actual(alignment=''afp'')' AS Q "
            "FROM signals WHERE bloomberg_ticker = 'AAPL US'"
        )
