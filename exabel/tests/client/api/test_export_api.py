import io
import json
import pickle
import re
import warnings
from typing import Sequence
from unittest.mock import MagicMock

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
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

    def test_run_query_bytes_warns_on_pickle(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b""
        export_api._session.post = MagicMock(return_value=mock_response)

        with pytest.warns(DeprecationWarning, match="file_format='pickle' is deprecated"):
            export_api.run_query_bytes("SELECT 1", file_format="pickle")

        assert export_api._session.post.call_args[1]["data"]["format"] == "pickle"

    def test_run_query_bytes_normalizes_pickle_casing(self):
        """Case-insensitive detection also normalizes the wire value so the server,
        which expects lowercase format keys, still accepts the request."""
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b""
        export_api._session.post = MagicMock(return_value=mock_response)

        with pytest.warns(DeprecationWarning):
            export_api.run_query_bytes("SELECT 1", file_format="PICKLE")

        assert export_api._session.post.call_args[1]["data"]["format"] == "pickle"

    def test_run_query_uses_pickle_silently(self):
        """``run_query`` requests pickle internally so v1 callers don't need
        ``pyarrow`` installed, and it must not emit ``DeprecationWarning`` —
        only the public ``run_query_bytes`` does that for explicit opt-in."""
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        frame = pd.DataFrame({"time": [pd.Timestamp("2024-03-31")], "Sales": [100]})
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = pickle.dumps(frame)
        export_api._session.post = MagicMock(return_value=mock_response)

        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)
            result = export_api.run_query("SELECT time, Sales FROM signals")

        call_args = export_api._session.post.call_args
        assert call_args[1]["data"]["format"] == "pickle"
        pd.testing.assert_frame_equal(result, frame)


def _make_v2_response_df(
    time_values: list,
    columns: list[tuple],
    data: list[list],
    level_names: tuple[str, ...] = ("Signal", "Entity", "Bloomberg ticker", "Time series"),
) -> pd.DataFrame:
    """Build a DataFrame matching the v2 export response format.

    The first column contains timestamps with a tuple of level names as header.
    Remaining columns are a MultiIndex with the given `level_names` — defaults to
    the 4-level shape, override to exercise 3-level (no Entity), 5-level, or
    Currency-present layouts.
    """
    time_col_name = level_names
    all_columns = pd.MultiIndex.from_tuples([time_col_name] + columns, names=level_names)
    all_data = {time_col_name: time_values, **dict(zip(columns, data))}
    return pd.DataFrame(all_data, columns=all_columns)


def _df_to_parquet_bytes(
    df: pd.DataFrame,
    multi_ts_signals: Sequence[str] = (),
) -> bytes:
    """Serialize a test DataFrame to parquet bytes, matching the server's wire format.

    Always embeds ``exabel_multi_ts_signals`` under the schema metadata key —
    the real server guarantees the key is present (empty list when no multi-ts
    signals participated), and the SDK treats an absent key as a contract
    violation.
    """
    table = pa.Table.from_pandas(df)
    metadata = {
        **(table.schema.metadata or {}),
        b"exabel_multi_ts_signals": json.dumps(sorted(multi_ts_signals)).encode("utf-8"),
    }
    table = table.replace_schema_metadata(metadata)
    buffer = io.BytesIO()
    pq.write_table(table, buffer)
    return buffer.getvalue()


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
        signal = DerivedSignal(name=None, label="brand_sales", expression="data('sales')")
        result = ExportApi._build_v2_signals(signal)
        assert result == [{"label": "brand_sales", "expression": "data('sales')"}]

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
        mock_response.content = _df_to_parquet_bytes(pd.DataFrame({"x": [1]}))
        export_api._session.post = MagicMock(return_value=mock_response)

        export_api._post_v2_signals(
            [{"label": "Pop", "expression": "graph_signal('ns.popularity')"}],
            entities=["entityTypes/company/entities/abc"],
            tags=["tags/user:123"],
            start_time="2024-01-01",
            end_time="2024-12-31",
            version="2024-06-01",
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
        assert body["outputFormat"] == "parquet"

    def test_post_v2_signals_error(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.content = b'"INTERNAL: Failed call"'
        export_api._session.post = MagicMock(return_value=mock_response)

        with pytest.raises(ValueError, match="Got 500: INTERNAL: Failed call"):
            export_api._post_v2_signals([{"label": "sig"}])

    def test_post_v2_signals_rejects_pickle(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        export_api._session.post = MagicMock()

        with pytest.raises(ValueError, match="pickle is not supported on the v2 export endpoint"):
            export_api._post_v2_signals([{"label": "sig"}], output_format="pickle")

        export_api._session.post.assert_not_called()

    def test_reshape_v2_response_single_entity_single_signal(self):
        times = [pd.Timestamp("2024-03-31"), pd.Timestamp("2024-06-30")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("Popularity", "Company A", "COMP US", "Company A")],
            data=[[100, 200]],
        )

        result = ExportApi._reshape_v2_response(
            raw_df, multi_entity=False, multi_ts_signals=frozenset()
        )

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

        result = ExportApi._reshape_v2_response(
            raw_df, multi_entity=True, multi_ts_signals=frozenset()
        )

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

        result = ExportApi._reshape_v2_response(
            raw_df, multi_entity=True, multi_ts_signals=frozenset()
        )

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

        result = ExportApi._reshape_v2_response(
            raw_df, multi_entity=False, multi_ts_signals=frozenset({"Visits"})
        )

        assert "Visits/domain1.com" in result.columns
        assert "Visits/domain2.com" in result.columns
        assert result["Visits/domain1.com"].iloc[0] == 100
        assert result["Visits/domain2.com"].iloc[0] == 200

    def test_reshape_v2_response_no_entity_level(self):
        """3-level shape: (Signal, Time series, Currency) — dataset-scoped query with no entity."""
        times = [pd.Timestamp("2024-03-31"), pd.Timestamp("2024-06-30")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("GDP", "USA", "")],
            data=[[25000, 25500]],
            level_names=("Signal", "Time series", "Currency"),
        )

        result = ExportApi._reshape_v2_response(
            raw_df, multi_entity=False, multi_ts_signals=frozenset()
        )

        assert list(result.columns) == ["GDP"]
        assert list(result.index) == times
        assert list(result["GDP"]) == [25000, 25500]

    def test_reshape_v2_response_with_currency_level_single_entity(self):
        """4-level (Signal, Entity, Time series, Currency). Time series must not be
        mis-read as Currency — the positional fallback 'last level' pointed at
        Currency before the name-based refactor."""
        times = [pd.Timestamp("2024-03-31")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("Revenue", "Company A", "Company A", "USD")],
            data=[[1000]],
            level_names=("Signal", "Entity", "Time series", "Currency"),
        )

        result = ExportApi._reshape_v2_response(
            raw_df, multi_entity=False, multi_ts_signals=frozenset()
        )

        assert list(result.columns) == ["Revenue"]
        assert result["Revenue"].iloc[0] == 1000

    def test_reshape_v2_response_multi_ts_single_entity_match(self):
        """When a multi-ts signal matches exactly one sub-entity for a given
        entity, the SDK must still produce a "signal/sub_entity" column name
        so the caller can tell which sub-entity the value belongs to —
        multi-ts signals get the suffix for *every* entity, not just those
        with multiple sub-entities in the result."""
        times = [pd.Timestamp("2024-03-31")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[
                ("Visits", "Company A", "COMP US", "domain1.com"),
                ("Visits", "Company A", "COMP US", "domain2.com"),
                ("Visits", "Company B", "ANOT US", "domain1.com"),
            ],
            data=[[100], [200], [50]],
        )

        result = ExportApi._reshape_v2_response(
            raw_df, multi_entity=True, multi_ts_signals=frozenset({"Visits"})
        )

        assert result.index.names == ["name", "time"]
        assert result.loc["Company A", times[0]]["Visits/domain1.com"] == 100
        assert result.loc["Company A", times[0]]["Visits/domain2.com"] == 200
        assert result.loc["Company B", times[0]]["Visits/domain1.com"] == 50
        assert "Visits" not in result.columns

    def test_reshape_v2_response_with_currency_level_multi_entity_multi_ts(self):
        """5-level shape with Currency present, multi-entity, multi-timeseries —
        the most stress-testing shape for the name-based reshape."""
        times = [pd.Timestamp("2024-03-31")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[
                ("Visits", "Company A", "COMP US", "domain1.com", ""),
                ("Visits", "Company A", "COMP US", "domain2.com", ""),
                ("Visits", "Company B", "ANOT US", "domain3.com", ""),
                ("Visits", "Company B", "ANOT US", "domain4.com", ""),
            ],
            data=[[100], [200], [50], [75]],
            level_names=("Signal", "Entity", "Bloomberg ticker", "Time series", "Currency"),
        )

        result = ExportApi._reshape_v2_response(
            raw_df, multi_entity=True, multi_ts_signals=frozenset({"Visits"})
        )

        assert result.index.names == ["name", "time"]
        assert result.loc["Company A", times[0]]["Visits/domain1.com"] == 100
        assert result.loc["Company A", times[0]]["Visits/domain2.com"] == 200
        assert result.loc["Company B", times[0]]["Visits/domain3.com"] == 50
        assert result.loc["Company B", times[0]]["Visits/domain4.com"] == 75

    def test_reshape_v2_response_multi_ts_with_name_collision(self):
        """Regression for the review concern on #15390: a sub-entity whose
        display name happens to equal its parent entity's display name (e.g.
        a brand named "Nike Inc" under company "Nike Inc"). With server
        metadata driving classification, the sub-entity still gets its
        "BrandValue/Nike Inc" column — previous name-based heuristics
        collapsed this to a bare "BrandValue".
        """
        times = [pd.Timestamp("2024-03-31")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("BrandValue", "Nike Inc", "NKE US", "Nike Inc")],
            data=[[42]],
        )

        result = ExportApi._reshape_v2_response(
            raw_df, multi_entity=False, multi_ts_signals=frozenset({"BrandValue"})
        )

        assert list(result.columns) == ["BrandValue/Nike Inc"]

    def test_export_signals_v2_raises_on_missing_metadata(self):
        """The SDK treats a response without ``exabel_multi_ts_signals`` as a
        server contract violation — no silent fallback to heuristics."""
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        raw_df = pd.DataFrame({"time": [pd.Timestamp("2024-03-31")], "Sales": [100]})
        buffer = io.BytesIO()
        raw_df.to_parquet(buffer)
        export_api._post_v2_signals = MagicMock(return_value=buffer.getvalue())

        with pytest.raises(ValueError, match="exabel_multi_ts_signals"):
            export_api.export_signals_v2("Sales", resource_name="entityTypes/company/entities/abc")

    def test_export_signals_v2_reads_multi_ts_from_metadata(self):
        """End-to-end: when the server embeds the metadata, the caller sees
        ``{signal}/{ts_name}`` columns even in the name-collision case."""
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        times = [pd.Timestamp("2024-03-31")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("BrandValue", "Nike Inc", "NKE US", "Nike Inc")],
            data=[[42]],
        )
        export_api._post_v2_signals = MagicMock(
            return_value=_df_to_parquet_bytes(raw_df, multi_ts_signals=["BrandValue"])
        )

        result = export_api.export_signals_v2(
            "BrandValue", resource_name="entityTypes/company/entities/nke"
        )

        assert isinstance(result, pd.Series)
        assert result.name == "BrandValue/Nike Inc"

    def test_export_signals_v2_single_entity(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        times = [pd.Timestamp("2024-03-31"), pd.Timestamp("2024-06-30")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("Sales", "Company A", "COMP US", "Company A")],
            data=[[100, 200]],
        )
        mock_post = MagicMock(return_value=_df_to_parquet_bytes(raw_df))
        export_api._post_v2_signals = mock_post

        result = export_api.export_signals_v2(
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

    def test_export_signals_v2_multi_entity(self):
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
        export_api._post_v2_signals = MagicMock(return_value=_df_to_parquet_bytes(raw_df))

        result = export_api.export_signals_v2(
            "Sales",
            resource_name=["entityTypes/company/entities/abc", "entityTypes/company/entities/def"],
        )

        assert isinstance(result, pd.Series)
        assert result.index.names == ["name", "time"]

    def test_export_signals_v2_with_tag(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        times = [pd.Timestamp("2024-03-31")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("Sales", "Company A", "COMP US", "Company A")],
            data=[[100]],
        )
        mock_post = MagicMock(return_value=_df_to_parquet_bytes(raw_df))
        export_api._post_v2_signals = mock_post

        export_api.export_signals_v2("Sales", tag="tags/user:123")

        assert mock_post.call_args[1]["tags"] == ["tags/user:123"]

    def test_export_signals_v2_with_derived_signal(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        times = [pd.Timestamp("2024-03-31")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("brand_sales", "Company A", "COMP US", "Company A")],
            data=[[42]],
        )
        export_api._post_v2_signals = MagicMock(return_value=_df_to_parquet_bytes(raw_df))

        signal = DerivedSignal(
            name=None,
            label="brand_sales",
            expression="data('sales').for_type('brand')",
        )
        result = export_api.export_signals_v2(
            signal, resource_name="entityTypes/company/entities/abc"
        )

        call_args = export_api._post_v2_signals.call_args[0][0]
        assert call_args == [
            {
                "label": "brand_sales",
                "expression": "data('sales').for_type('brand')",
            }
        ]

    def test_export_signals_v2_empty_signal_raises(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        with pytest.raises(ValueError, match="Must specify signal to retrieve"):
            export_api.export_signals_v2([], resource_name="entityTypes/company/entities/abc")

    def test_run_export_signals_v2(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        times = [pd.Timestamp("2024-03-31"), pd.Timestamp("2024-06-30")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("Sales", "Company A", "COMP US", "Company A")],
            data=[[100, 200]],
        )
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = _df_to_parquet_bytes(raw_df)
        export_api._session.post = MagicMock(return_value=mock_response)

        result_df = export_api.run_export_signals_v2(
            [{"label": "Sales"}],
            entities=["entityTypes/company/entities/abc"],
            start_time="2024-01-01",
            end_time="2024-12-31",
        )

        assert isinstance(result_df, pd.DataFrame)
        # Raw response: MultiIndex columns, first column is timestamps
        assert isinstance(result_df.columns, pd.MultiIndex)
        assert result_df.shape == (2, 2)  # time column + 1 data column

    def test_export_signals_v2_bytes_returns_raw_response(self):
        """``export_signals_v2_bytes`` posts the v2 request in the requested format
        and returns the server's raw bytes unchanged — no pyarrow parsing."""
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        wire_bytes = b"time,Sales\n2024-03-31,100\n"
        mock_post = MagicMock(return_value=wire_bytes)
        export_api._post_v2_signals = mock_post

        result = export_api.export_signals_v2_bytes(
            "Sales",
            file_format="csv",
            resource_name="entityTypes/company/entities/abc",
            start_time="2024-01-01",
            end_time="2024-12-31",
        )

        assert result == wire_bytes
        assert mock_post.call_args[1]["output_format"] == "csv"
        assert mock_post.call_args[1]["entities"] == ["entityTypes/company/entities/abc"]

    def test_export_signals_v2_bytes_empty_signal_raises(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        with pytest.raises(ValueError, match="Must specify signal to retrieve"):
            export_api.export_signals_v2_bytes([], resource_name="entityTypes/company/entities/abc")

    def test_export_signals_v2_bytes_rejects_pickle(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        export_api._session.post = MagicMock()

        with pytest.raises(ValueError, match="pickle is not supported on the v2 export endpoint"):
            export_api.export_signals_v2_bytes(
                "Sales",
                file_format="pickle",
                resource_name="entityTypes/company/entities/abc",
            )

        export_api._session.post.assert_not_called()

    def test_signal_query_v2_emits_deprecation_warning(self):
        """The old name remains a thin wrapper that delegates to
        ``export_signals_v2`` with a ``DeprecationWarning``."""
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        times = [pd.Timestamp("2024-03-31")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("Sales", "Company A", "COMP US", "Company A")],
            data=[[100]],
        )
        export_api._post_v2_signals = MagicMock(return_value=_df_to_parquet_bytes(raw_df))

        with pytest.warns(DeprecationWarning, match="signal_query_v2 is deprecated"):
            result = export_api.signal_query_v2(
                "Sales", resource_name="entityTypes/company/entities/abc"
            )
        assert isinstance(result, pd.Series)

    def test_run_signal_query_v2_emits_deprecation_warning(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        times = [pd.Timestamp("2024-03-31")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("Sales", "Company A", "COMP US", "Company A")],
            data=[[100]],
        )
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = _df_to_parquet_bytes(raw_df)
        export_api._session.post = MagicMock(return_value=mock_response)

        with pytest.warns(DeprecationWarning, match="run_signal_query_v2 is deprecated"):
            result = export_api.run_signal_query_v2(
                [{"label": "Sales"}], entities=["entityTypes/company/entities/abc"]
            )
        assert isinstance(result, pd.DataFrame)

    def test_reshape_v2_response_non_multiindex(self):
        flat_df = pd.DataFrame({"time": [pd.Timestamp("2024-03-31")], "Sales": [100]})

        result = ExportApi._reshape_v2_response(
            flat_df, multi_entity=False, multi_ts_signals=frozenset()
        )

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
