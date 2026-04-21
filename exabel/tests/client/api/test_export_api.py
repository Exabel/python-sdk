import json
import pickle
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


def _make_v2_response_df(
    time_values: list,
    columns: list[tuple],
    data: list[list],
) -> pd.DataFrame:
    """Build a DataFrame matching the v2 export response format.

    The first column contains timestamps with a tuple of level names as header.
    Remaining columns are MultiIndex tuples of (Signal, Entity, Bloomberg ticker, Time series).
    """
    level_names = ("Signal", "Entity", "Bloomberg ticker", "Time series")
    time_col_name = level_names
    all_columns = pd.MultiIndex.from_tuples([time_col_name] + columns, names=level_names)
    all_data = {time_col_name: time_values, **dict(zip(columns, data))}
    return pd.DataFrame(all_data, columns=all_columns)


class TestExportApiV2:
    def test_build_v2_signals_string(self):
        result = ExportApi._build_v2_signals("Sales_Actual")
        assert result == [{"label": "Sales_Actual"}]

    def test_build_v2_signals_column(self):
        result = ExportApi._build_v2_signals(Column("Q", "sales_actual(alignment='afp')"))
        assert result == [{"label": "Q", "expression": "sales_actual(alignment='afp')"}]

    def test_build_v2_signals_column_without_expression(self):
        result = ExportApi._build_v2_signals(Column("Sales_Actual"))
        assert result == [{"label": "Sales_Actual"}]

    def test_build_v2_signals_derived_signal(self):
        signal = DerivedSignal(name=None, label="sweb", expression="data('similarweb.visits')")
        result = ExportApi._build_v2_signals(signal)
        assert result == [{"label": "sweb", "expression": "data('similarweb.visits')"}]

    def test_build_v2_signals_sequence(self):
        signals = [
            "Sales_Actual",
            Column("Q", "sales_actual(alignment='afp')"),
            DerivedSignal(name=None, label="derived", expression="expr()"),
        ]
        result = ExportApi._build_v2_signals(signals)
        assert result == [
            {"label": "Sales_Actual"},
            {"label": "Q", "expression": "sales_actual(alignment='afp')"},
            {"label": "derived", "expression": "expr()"},
        ]

    def test_build_v2_signals_invalid_derived_signal(self):
        with pytest.raises(ValueError, match="DerivedSignal must have both label and expression"):
            ExportApi._build_v2_signals(DerivedSignal(name=None, label="", expression="expr()"))

    def test_to_timestamp_string_date_string(self):
        assert ExportApi._to_timestamp_string("2024-01-01") == "2024-01-01T00:00:00Z"

    def test_to_timestamp_string_iso_string(self):
        assert ExportApi._to_timestamp_string("2024-01-01T12:00:00Z") == "2024-01-01T12:00:00Z"

    def test_to_timestamp_string_naive_timestamp(self):
        ts = pd.Timestamp("2024-06-15 10:30:00")
        assert ExportApi._to_timestamp_string(ts) == "2024-06-15T10:30:00Z"

    def test_to_timestamp_string_tz_aware_timestamp(self):
        ts = pd.Timestamp("2024-06-15 10:30:00", tz="US/Eastern")
        result = ExportApi._to_timestamp_string(ts)
        assert result == "2024-06-15T14:30:00Z"

    def test_post_v2_signals_request_format(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = pickle.dumps(pd.DataFrame())
        export_api._session.post = MagicMock(return_value=mock_response)

        export_api._post_v2_signals(
            [{"label": "Pop", "expression": "graph_signal('ns.popularity')"}],
            entities=["entityTypes/company/entities/abc"],
            tags=["tags/user:123"],
            start_time="2024-01-01",
            end_time="2024-12-31",
            version="2024-06-01",
            output_format="pickle",
        )

        call_args = export_api._session.post.call_args
        assert "/v2/export/signals" in call_args[0][0]
        body = json.loads(call_args[1]["data"])
        assert body["signals"] == [{"label": "Pop", "expression": "graph_signal('ns.popularity')"}]
        assert body["entities"] == ["entityTypes/company/entities/abc"]
        assert body["tags"] == ["tags/user:123"]
        assert body["timeRange"] == {
            "from": "2024-01-01T00:00:00Z",
            "to": "2024-12-31T00:00:00Z",
        }
        assert body["version"] == "2024-06-01T00:00:00Z"
        assert body["outputFormat"] == "pickle"

    def test_post_v2_signals_error(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.content = b'"INTERNAL: Failed call"'
        export_api._session.post = MagicMock(return_value=mock_response)

        with pytest.raises(ValueError, match="Got 500: INTERNAL: Failed call"):
            export_api._post_v2_signals(
                [{"label": "sig"}],
                output_format="pickle",
            )

    def test_reshape_v2_response_single_entity_single_signal(self):
        times = [pd.Timestamp("2024-03-31"), pd.Timestamp("2024-06-30")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("Popularity", "Company A", "COMP US", "Company A")],
            data=[[100, 200]],
        )

        result = ExportApi._reshape_v2_response(raw_df, multi_entity=False)

        assert list(result.columns) == ["Popularity"]
        assert list(result.index) == times
        assert result.index.name == "time"
        assert list(result["Popularity"]) == [100, 200]

    def test_reshape_v2_response_multi_entity_single_signal(self):
        times = [pd.Timestamp("2024-03-31"), pd.Timestamp("2024-06-30")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[
                ("Popularity", "Company A", "COMP US", "Company A"),
                ("Popularity", "Company B", "ANOT US", "Company B"),
            ],
            data=[[100, 200], [400, 300]],
        )

        result = ExportApi._reshape_v2_response(raw_df, multi_entity=True)

        assert result.index.names == ["name", "time"]
        assert list(result.columns) == ["Popularity"]
        assert result.loc["Company A", times[0]]["Popularity"] == 100
        assert result.loc["Company B", times[0]]["Popularity"] == 400

    def test_reshape_v2_response_multi_entity_multi_signal(self):
        times = [pd.Timestamp("2024-03-31"), pd.Timestamp("2024-06-30")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[
                ("Popularity", "Company A", "COMP US", "Company A"),
                ("Popularity", "Company B", "ANOT US", "Company B"),
                ("Reputation", "Company A", "COMP US", "Company A"),
            ],
            data=[[100, 200], [400, 300], [1, 2]],
        )

        result = ExportApi._reshape_v2_response(raw_df, multi_entity=True)

        assert result.index.names == ["name", "time"]
        assert sorted(result.columns) == ["Popularity", "Reputation"]
        assert result.loc["Company A", times[0]]["Popularity"] == 100
        assert result.loc["Company A", times[0]]["Reputation"] == 1
        # Company B has no Reputation signal
        assert pd.isna(result.loc["Company B", times[0]]["Reputation"])

    def test_reshape_v2_response_multi_timeseries(self):
        times = [pd.Timestamp("2024-03-31")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[
                ("Visits", "Company A", "COMP US", "domain1.com"),
                ("Visits", "Company A", "COMP US", "domain2.com"),
            ],
            data=[[100], [200]],
        )

        result = ExportApi._reshape_v2_response(raw_df, multi_entity=False)

        assert "Visits/domain1.com" in result.columns
        assert "Visits/domain2.com" in result.columns
        assert result["Visits/domain1.com"].iloc[0] == 100
        assert result["Visits/domain2.com"].iloc[0] == 200

    def test_signal_query_v2_single_entity(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        times = [pd.Timestamp("2024-03-31"), pd.Timestamp("2024-06-30")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("Sales", "Company A", "COMP US", "Company A")],
            data=[[100, 200]],
        )
        mock_post = MagicMock(return_value=pickle.dumps(raw_df))
        export_api._post_v2_signals = mock_post

        result = export_api.signal_query_v2(
            "Sales",
            resource_name="entityTypes/company/entities/abc",
            start_time="2024-01-01",
            end_time="2024-12-31",
        )

        # Single signal, single entity -> Series
        assert isinstance(result, pd.Series)
        assert result.name == "Sales"
        assert list(result.index) == times
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        assert call_kwargs[0][0] == [{"label": "Sales"}]
        assert call_kwargs[1]["entities"] == ["entityTypes/company/entities/abc"]

    def test_signal_query_v2_multi_entity(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        times = [pd.Timestamp("2024-03-31"), pd.Timestamp("2024-06-30")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[
                ("Sales", "Company A", "COMP US", "Company A"),
                ("Sales", "Company B", "ANOT US", "Company B"),
            ],
            data=[[100, 200], [400, 300]],
        )
        export_api._post_v2_signals = MagicMock(return_value=pickle.dumps(raw_df))

        result = export_api.signal_query_v2(
            "Sales",
            resource_name=["entityTypes/company/entities/abc", "entityTypes/company/entities/def"],
        )

        assert isinstance(result, pd.Series)
        assert result.index.names == ["name", "time"]

    def test_signal_query_v2_with_tag(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        times = [pd.Timestamp("2024-03-31")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("Sales", "Company A", "COMP US", "Company A")],
            data=[[100]],
        )
        mock_post = MagicMock(return_value=pickle.dumps(raw_df))
        export_api._post_v2_signals = mock_post

        export_api.signal_query_v2("Sales", tag="tags/user:123")

        assert mock_post.call_args[1]["tags"] == ["tags/user:123"]

    def test_signal_query_v2_with_derived_signal(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        times = [pd.Timestamp("2024-03-31")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("sweb", "Company A", "COMP US", "Company A")],
            data=[[42]],
        )
        export_api._post_v2_signals = MagicMock(return_value=pickle.dumps(raw_df))

        signal = DerivedSignal(
            name=None,
            label="sweb",
            expression="data('similarweb.all_visits').for_type('similarweb.domain')",
        )
        result = export_api.signal_query_v2(
            signal, resource_name="entityTypes/company/entities/abc"
        )

        call_args = export_api._post_v2_signals.call_args[0][0]
        assert call_args == [
            {
                "label": "sweb",
                "expression": "data('similarweb.all_visits').for_type('similarweb.domain')",
            }
        ]

    def test_signal_query_v2_empty_signal_raises(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        with pytest.raises(ValueError, match="Must specify signal to retrieve"):
            export_api.signal_query_v2([], resource_name="entityTypes/company/entities/abc")

    def test_run_signal_query_v2(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        times = [pd.Timestamp("2024-03-31"), pd.Timestamp("2024-06-30")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("Sales", "Company A", "COMP US", "Company A")],
            data=[[100, 200]],
        )
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = pickle.dumps(raw_df)
        export_api._session.post = MagicMock(return_value=mock_response)

        result_df = export_api.run_signal_query_v2(
            [{"label": "Sales"}],
            entities=["entityTypes/company/entities/abc"],
            start_time="2024-01-01",
            end_time="2024-12-31",
        )

        assert isinstance(result_df, pd.DataFrame)
        # Raw response: MultiIndex columns, first column is timestamps
        assert isinstance(result_df.columns, pd.MultiIndex)
        assert result_df.shape == (2, 2)  # time column + 1 data column

    def test_reshape_v2_response_non_multiindex(self):
        flat_df = pd.DataFrame({"time": [pd.Timestamp("2024-03-31")], "Sales": [100]})

        result = ExportApi._reshape_v2_response(flat_df, multi_entity=False)

        assert result.index.name == "time"
        assert list(result.columns) == ["Sales"]
        assert result["Sales"].iloc[0] == 100

    def test_signal_query_unchanged(self):
        """Verify signal_query still uses the v1 SQL path."""
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        mock = MagicMock(name="run_query")
        export_api.run_query = mock

        export_api.signal_query("Sales_Actual", factset_id="QLGSL2-R")
        mock.assert_called_with(
            "SELECT time, Sales_Actual FROM signals WHERE factset_id = 'QLGSL2-R'"
        )

        export_api.signal_query("Sales_Actual", resource_name="entityTypes/company/entities/A1-E")
        mock.assert_called_with(
            "SELECT time, Sales_Actual FROM signals "
            "WHERE resource_name = 'entityTypes/company/entities/A1-E'"
        )
