import re
from unittest.mock import MagicMock

import pandas as pd
import pytest

from exabel.client.api.data_classes.derived_signal import DerivedSignal
from exabel.client.api.export_api import ExportApi
from exabel.client.client_config import ClientConfig
from exabel.query.column import Column
from exabel.query.signals import Signals


class TestExportApi:
    def test_signal_query(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
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

    def test_signal_query_with_derived_signal(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        mock = MagicMock(name="run_query")
        export_api.run_query = mock

        # Test single DerivedSignal
        export_api.signal_query(
            DerivedSignal(name=None, label="EURUSD", expression="fx('EUR', 'USD')")
        )
        mock.assert_called_with("SELECT time, 'fx(''EUR'', ''USD'')' AS EURUSD FROM signals")

        # Test DerivedSignal with entity filter
        export_api.signal_query(
            DerivedSignal(name=None, label="Sales", expression="sales_actual()"),
            factset_id="QLGSL2-R",
        )
        mock.assert_called_with(
            "SELECT time, 'sales_actual()' AS Sales FROM signals WHERE factset_id = 'QLGSL2-R'"
        )

        # Test sequence of DerivedSignals
        signals = [
            DerivedSignal(name=None, label="sig1", expression="expr1()"),
            DerivedSignal(name=None, label="sig2", expression="expr2()"),
        ]
        export_api.signal_query(signals, factset_id="QLGSL2-R")
        mock.assert_called_with(
            "SELECT time, 'expr1()' AS sig1, 'expr2()' AS sig2 FROM signals "
            "WHERE factset_id = 'QLGSL2-R'"
        )

        # Test mixed sequence of DerivedSignal and Column
        mixed_signals = [
            DerivedSignal(name=None, label="derived", expression="derived_expr()"),
            Column("col", "col_expr()"),
        ]
        export_api.signal_query(mixed_signals, factset_id="QLGSL2-R")
        mock.assert_called_with(
            "SELECT time, 'derived_expr()' AS derived, 'col_expr()' AS col FROM signals "
            "WHERE factset_id = 'QLGSL2-R'"
        )

    def test_signal_query_with_invalid_derived_signal(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        with pytest.raises(ValueError, match="DerivedSignal must have both label and expression"):
            export_api.signal_query(DerivedSignal(name=None, label="", expression="expr()"))
        with pytest.raises(ValueError, match="DerivedSignal must have both label and expression"):
            export_api.signal_query(DerivedSignal(name=None, label="label", expression=""))

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
            assert length <= batch_size
            return data.query(f"name in {names}")

        export_api = ExportApi(ClientConfig(api_key="api-key"))
        export_api.run_query = MagicMock(name="run_query", side_effect=side_effect)
        for batch_size in range(1, 12):
            result = export_api.batched_signal_query(
                batch_size, "Sales_Actual", resource_name=resource_name
            )
            pd.testing.assert_series_equal(series, result)

    def test_batched_signal_query_error(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        with pytest.raises(ValueError, match="Need to specify an identification method"):
            export_api.batched_signal_query(3, "Sales_Actual")
        with pytest.raises(ValueError, match="At most one entity identification method"):
            export_api.batched_signal_query(
                3,
                "Sales_Actual",
                bloomberg_ticker=["A", "B"],
                factset_id=["C", "D"],
            )
