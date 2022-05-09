import unittest
from unittest.mock import MagicMock

from exabel_data_sdk.client.api.export_api import ExportApi
from exabel_data_sdk.query.column import Column


class TestExportApi(unittest.TestCase):
    def test_signal_query(self):
        export_api = ExportApi(auth_headers={})
        mock = MagicMock(name="run_query")
        export_api.run_query = mock

        export_api.signal_query(Column("EURUSD", "fx('EUR', 'USD')"))
        mock.assert_called_with("SELECT time, 'fx(''EUR'', ''USD'')' AS EURUSD FROM signals")

        export_api.signal_query("Sales_Actual", factset_id="QLGSL2-R")
        mock.assert_called_with(
            "SELECT time, Sales_Actual FROM signals WHERE factset_id = 'QLGSL2-R'"
        )

        export_api.signal_query("Sales_Actual", bloomberg_ticker=["AAPL US", "TSLA US"])
        mock.assert_called_with(
            "SELECT name, time, Sales_Actual FROM signals "
            "WHERE bloomberg_ticker IN ('AAPL US', 'TSLA US')"
        )

        export_api.signal_query("Sales_Actual", tag="graph:tag:user:xyz-123")
        mock.assert_called_with(
            "SELECT name, time, Sales_Actual FROM signals WHERE has_tag('graph:tag:user:xyz-123')"
        )

        column = Column("Q", "sales_actual(alignment='afp')")
        export_api.signal_query(["Sales_Actual_fiscal", column], "AAPL US")
        mock.assert_called_with(
            "SELECT time, Sales_Actual_fiscal, 'sales_actual(alignment=''afp'')' AS Q "
            "FROM signals WHERE bloomberg_ticker = 'AAPL US'"
        )
