import re
import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from exabel_data_sdk.client.api.export_api import ExportApi
from exabel_data_sdk.query.column import Column
from exabel_data_sdk.query.signals import Signals


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

        export_api.signal_query("Sales_Actual", resource_name="entityTypes/company/entities/A1-E")
        mock.assert_called_with(
            "SELECT time, Sales_Actual FROM signals "
            "WHERE resource_name = 'entityTypes/company/entities/A1-E'"
        )

        export_api.signal_query("Sales_Actual", resource_name=["A", "B"])
        mock.assert_called_with(
            "SELECT name, time, Sales_Actual FROM signals WHERE resource_name IN ('A', 'B')"
        )

        export_api.signal_query("Sales_Actual", ["AAPL US", "TSLA US"])
        mock.assert_called_with(
            "SELECT name, time, Sales_Actual FROM signals "
            "WHERE bloomberg_ticker IN ('AAPL US', 'TSLA US')"
        )

        export_api.signal_query(
            "Sales_Actual", ["AAPL US", "TSLA US"], identifier=Signals.EXABEL_ID
        )
        mock.assert_called_with(
            "SELECT exabel_id, time, Sales_Actual FROM signals "
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

        export_api.signal_query(
            Column("Prediction", "allocations(analysis=7)"), identifier=Signals.NAME
        )
        mock.assert_called_with(
            "SELECT name, time, 'allocations(analysis=7)' AS Prediction FROM signals"
        )

        export_api.signal_query("Sales_Actual", factset_id="QLGSL2-R", version="2019-02-03")
        mock.assert_called_with(
            "SELECT time, Sales_Actual FROM signals WHERE factset_id = 'QLGSL2-R'"
            " AND version = '2019-02-03'"
        )

        export_api.signal_query(
            "Sales_Actual",
            factset_id=["QLGSL2-R", "FOOBAR"],
            version=[pd.Timestamp("2019-01-01"), pd.Timestamp("2019-02-02")],
        )
        mock.assert_called_with(
            "SELECT version, name, time, Sales_Actual FROM signals "
            "WHERE factset_id IN ('QLGSL2-R', 'FOOBAR') AND version IN ('2019-01-01', '2019-02-02')"
        )

    def test_batched_signal_query(self):
        resource_name = list("ABCDEFGHIJ")
        data = pd.concat(
            [
                pd.Series(resource_name, name="name"),
                pd.Series(pd.date_range("2023-01-01", periods=10, name="time")),
                pd.Series(range(10)),
            ],
            axis=1,
        )
        series = data.set_index(["name", "time"]).squeeze()

        def side_effect(query: str):
            exp_query = "SELECT name, time, Sales_Actual FROM signals WHERE resource_name IN (.*)"
            m = re.fullmatch(exp_query, query)
            assert m
            names = m.group(1)
            length = len(names.split(","))
            self.assertLessEqual(length, batch_size)
            return data.query(f"name in {names}")

        export_api = ExportApi(auth_headers={})
        export_api.run_query = MagicMock(name="run_query", side_effect=side_effect)
        for batch_size in range(1, 12):
            result = export_api.batched_signal_query(
                batch_size, "Sales_Actual", resource_name=resource_name
            )
            pd.testing.assert_series_equal(series, result)

    def test_batched_signal_query_error(self):
        export_api = ExportApi(auth_headers={})
        self.assertRaisesRegex(
            ValueError,
            "Need to specify an identification method",
            export_api.batched_signal_query,
            3,
            "Sales_Actual",
        )
        self.assertRaisesRegex(
            ValueError,
            "At most one entity identification method",
            export_api.batched_signal_query,
            3,
            "Sales_Actual",
            bloomberg_ticker=["A", "B"],
            factset_id=["C", "D"],
        )

    @patch("exabel_data_sdk.client.api.export_api.ExportApi")
    def test_from_api_key(self, mock_api):
        mock_api.return_value = None
        api_key = "api-key"
        ExportApi.from_api_key(api_key=api_key)
        mock_api.assert_called_with(
            auth_headers={"x-api-key": api_key}, backend="export.api.exabel.com"
        )
        ExportApi.from_api_key(api_key=api_key, use_test_backend=True)
        mock_api.assert_called_with(
            auth_headers={"x-api-key": api_key}, backend="export.api-test.exabel.com"
        )
