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

# Default time range for v2 export tests where the actual dates don't matter
# (calls are mocked); spread into kwargs to satisfy the required parameters.
_V2_TIME_RANGE = {"start_time": "2024-01-01", "end_time": "2024-12-31"}


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

    def test_build_v2_signals_derived_signal(self):
        signal = DerivedSignal(name=None, label="brand_sales", expression="data('sales')")
        result = ExportApi._build_v2_signals(signal)
        assert result == [{"label": "brand_sales", "expression": "data('sales')"}]

    def test_build_v2_signals_sequence(self):
        signals = [
            "Sales_Actual",
            DerivedSignal(name=None, label="derived", expression="expr()"),
        ]
        result = ExportApi._build_v2_signals(signals)
        assert result == [
            {"label": "Sales_Actual"},
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
            **_V2_TIME_RANGE,
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

        result = ExportApi._reshape_v2_response(raw_df, multi_ts_signals=frozenset())

        # Single-entity responses now also pivot to (name, time) so the row-index
        # shape is uniform with multi-entity responses.
        assert list(result.columns) == ["Popularity"]
        assert result.index.names == ["name", "time"]
        assert list(result.index.get_level_values("name").unique()) == ["Company A"]
        assert list(result.loc["Company A"]["Popularity"]) == [100, 200]

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

        result = ExportApi._reshape_v2_response(raw_df, multi_ts_signals=frozenset())

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

        result = ExportApi._reshape_v2_response(raw_df, multi_ts_signals=frozenset())

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

        result = ExportApi._reshape_v2_response(raw_df, multi_ts_signals=frozenset({"Visits"}))

        assert result.index.names == ["name", "time"]
        assert "Visits/domain1.com" in result.columns
        assert "Visits/domain2.com" in result.columns
        assert result.loc["Company A", times[0]]["Visits/domain1.com"] == 100
        assert result.loc["Company A", times[0]]["Visits/domain2.com"] == 200

    def test_reshape_v2_response_no_entity_level(self):
        """3-level shape: (Signal, Time series, Currency) — query with no entity."""
        times = [pd.Timestamp("2024-03-31"), pd.Timestamp("2024-06-30")]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[("GDP", "USA", "")],
            data=[[25000, 25500]],
            level_names=("Signal", "Time series", "Currency"),
        )

        result = ExportApi._reshape_v2_response(raw_df, multi_ts_signals=frozenset())

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

        result = ExportApi._reshape_v2_response(raw_df, multi_ts_signals=frozenset())

        assert result.index.names == ["name", "time"]
        assert list(result.columns) == ["Revenue"]
        assert result.loc["Company A", times[0]]["Revenue"] == 1000

    def test_reshape_v2_response_multi_ts_single_entity_match(self):
        """When a multi-ts signal matches exactly one sub-entity for a given
        entity, the SDK must still produce a {signal_label}/{ts_name} column name
        so the caller can tell which sub-entity the value belongs to —
        multi-ts signals get the suffix for every entity, not just those
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

        result = ExportApi._reshape_v2_response(raw_df, multi_ts_signals=frozenset({"Visits"}))

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

        result = ExportApi._reshape_v2_response(raw_df, multi_ts_signals=frozenset({"Visits"}))

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

        result = ExportApi._reshape_v2_response(raw_df, multi_ts_signals=frozenset({"BrandValue"}))

        assert result.index.names == ["name", "time"]
        assert list(result.columns) == ["BrandValue/Nike Inc"]

    def test_reshape_v2_response_no_performance_warning_with_many_columns(self):
        """Regression: assembling the result column-by-column tripped pandas'
        BlockManager fragmentation heuristic past ~100 columns, emitting a
        PerformanceWarning per assignment. Real ``for_type()`` queries (e.g.
        ~360 Similarweb domains per company) hit this on every call. The
        reshape must stay warning-free regardless of column count."""
        times = [pd.Timestamp("2024-03-31")]
        columns = [("Visits", "Company A", "COMP US", f"domain{i}.com") for i in range(200)]
        data = [[i] for i in range(200)]
        raw_df = _make_v2_response_df(time_values=times, columns=columns, data=data)

        with warnings.catch_warnings():
            warnings.simplefilter("error", pd.errors.PerformanceWarning)
            ExportApi._reshape_v2_response(raw_df, multi_ts_signals=frozenset({"Visits"}))

    def test_reshape_v2_response_no_performance_warning_multi_entity(self):
        """Same fragmentation guard for the multi-entity branch — it used to
        build each entity's frame column-by-column too, so a watchlist of N
        companies × M sub-entities tripped the same warning per entity."""
        times = [pd.Timestamp("2024-03-31")]
        columns = [
            ("Visits", entity, ticker, f"domain{i}.com")
            for entity, ticker in [("Company A", "COMP US"), ("Company B", "ANOT US")]
            for i in range(200)
        ]
        data = [[i] for i in range(len(columns))]
        raw_df = _make_v2_response_df(time_values=times, columns=columns, data=data)

        with warnings.catch_warnings():
            warnings.simplefilter("error", pd.errors.PerformanceWarning)
            ExportApi._reshape_v2_response(raw_df, multi_ts_signals=frozenset({"Visits"}))

    def test_export_signals_v2_raises_on_missing_metadata(self):
        """The SDK treats a response without ``exabel_multi_ts_signals`` as a
        server contract violation — no silent fallback to heuristics."""
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        raw_df = pd.DataFrame({"time": [pd.Timestamp("2024-03-31")], "Sales": [100]})
        buffer = io.BytesIO()
        raw_df.to_parquet(buffer)
        export_api._post_v2_signals = MagicMock(return_value=buffer.getvalue())

        with pytest.raises(ValueError, match="exabel_multi_ts_signals"):
            export_api.export_signals_v2(
                "Sales",
                entities="entityTypes/company/entities/abc",
                **_V2_TIME_RANGE,
            )

    def test_export_signals_v2_reads_multi_ts_from_metadata(self):
        """End-to-end: when the server embeds the metadata, the caller sees
        {signal_label}/{ts_name} columns even in the name-collision case."""
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
            "BrandValue",
            entities="entityTypes/company/entities/nke",
            **_V2_TIME_RANGE,
        )

        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["BrandValue/Nike Inc"]
        assert result.index.names == ["name", "time"]

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
            entities="entityTypes/company/entities/abc",
            **_V2_TIME_RANGE,
        )

        # Single signal, single entity -> DataFrame with MultiIndex (uniform shape).
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["Sales"]
        assert result.index.names == ["name", "time"]
        assert list(result.index.get_level_values("time")) == times
        assert list(result.index.get_level_values("name").unique()) == ["Company A"]
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        assert call_kwargs[0][0] == [{"label": "Sales"}]
        assert call_kwargs[1]["entities"] == ("entityTypes/company/entities/abc",)

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
            entities=["entityTypes/company/entities/abc", "entityTypes/company/entities/def"],
            **_V2_TIME_RANGE,
        )

        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["Sales"]
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

        export_api.export_signals_v2("Sales", tags="tags/user:123", **_V2_TIME_RANGE)

        assert mock_post.call_args[1]["tags"] == ("tags/user:123",)

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
            signal,
            entities="entityTypes/company/entities/abc",
            **_V2_TIME_RANGE,
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
        with pytest.raises(ValueError, match="Must specify signals to retrieve"):
            export_api.export_signals_v2(
                [],
                entities="entityTypes/company/entities/abc",
                **_V2_TIME_RANGE,
            )

    def test_export_signals_v2_drops_all_nan_rows_keeps_partial_nan(self):
        """All-NaN rows from sparse signals are dropped; rows with any value survive.

        Critical for the common case: a quarterly signal (e.g. Visible Alpha
        actuals) exported across a daily range otherwise produces an output
        padded with empty rows for every non-period day.
        """
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        times = [
            pd.Timestamp("2024-03-31"),
            pd.Timestamp("2024-04-01"),  # all-NaN — should be dropped
            pd.Timestamp("2024-06-30"),
            pd.Timestamp("2024-07-01"),  # partial-NaN — should survive
        ]
        raw_df = _make_v2_response_df(
            time_values=times,
            columns=[
                ("actual", "Company A", "COMP US", "Company A"),
                ("consensus", "Company A", "COMP US", "Company A"),
            ],
            data=[
                [100, float("nan"), 200, float("nan")],
                [110, float("nan"), 210, 220],
            ],
        )
        export_api._post_v2_signals = MagicMock(return_value=_df_to_parquet_bytes(raw_df))

        result = export_api.export_signals_v2(
            ["actual", "consensus"],
            entities="entityTypes/company/entities/abc",
            **_V2_TIME_RANGE,
        )

        result_times = list(result.index.get_level_values("time"))
        assert pd.Timestamp("2024-04-01") not in result_times, "all-NaN row was not dropped"
        assert pd.Timestamp("2024-07-01") in result_times, "partial-NaN row was incorrectly dropped"
        assert pd.Timestamp("2024-03-31") in result_times
        assert pd.Timestamp("2024-06-30") in result_times

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
            **_V2_TIME_RANGE,
        )

        assert isinstance(result_df, pd.DataFrame)
        # Raw response: MultiIndex columns, first column is timestamps
        assert isinstance(result_df.columns, pd.MultiIndex)
        assert result_df.shape == (2, 2)  # time column + 1 data column

    def test_export_signals_v2_bytes_returns_raw_response(self):
        """export_signals_v2_bytes posts the v2 request in the requested format
        and returns the server's raw bytes unchanged — no pyarrow parsing."""
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        wire_bytes = b"time,Sales\n2024-03-31,100\n"
        mock_post = MagicMock(return_value=wire_bytes)
        export_api._post_v2_signals = mock_post

        result = export_api.export_signals_v2_bytes(
            "Sales",
            file_format="csv",
            entities="entityTypes/company/entities/abc",
            **_V2_TIME_RANGE,
        )

        assert result == wire_bytes
        assert mock_post.call_args[1]["output_format"] == "csv"
        assert mock_post.call_args[1]["entities"] == ("entityTypes/company/entities/abc",)

    def test_export_signals_v2_bytes_empty_signal_raises(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        with pytest.raises(ValueError, match="Must specify signals to retrieve"):
            export_api.export_signals_v2_bytes(
                [],
                entities="entityTypes/company/entities/abc",
                **_V2_TIME_RANGE,
            )

    def test_export_signals_v2_bytes_rejects_pickle(self):
        export_api = ExportApi(ClientConfig(api_key="api-key"))
        export_api._session.post = MagicMock()

        with pytest.raises(ValueError, match="pickle is not supported on the v2 export endpoint"):
            export_api.export_signals_v2_bytes(
                "Sales",
                file_format="pickle",
                entities="entityTypes/company/entities/abc",
                **_V2_TIME_RANGE,
            )

        export_api._session.post.assert_not_called()

    def test_reshape_v2_response_non_multiindex(self):
        flat_df = pd.DataFrame({"time": [pd.Timestamp("2024-03-31")], "Sales": [100]})

        result = ExportApi._reshape_v2_response(flat_df, multi_ts_signals=frozenset())

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
