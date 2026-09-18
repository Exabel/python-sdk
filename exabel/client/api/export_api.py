import io
import json
import logging
import pickle
import warnings
from time import time
from typing import Sequence, TypeVar

import pandas as pd
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from exabel.client.api.data_classes.dashboard_table import (
    ColumnRef,
    TableColumnFilter,
    TableColumnOrdering,
    column_ref_to_json,
)
from exabel.client.api.data_classes.derived_signal import DerivedSignal
from exabel.client.client_config import ClientConfig
from exabel.query.column import Column
from exabel.query.predicate import Predicate
from exabel.query.query import Query
from exabel.query.signals import Signals
from exabel.scripts.utils import conditional_progress_bar
from exabel.util.handle_missing_imports import handle_missing_imports

logger = logging.getLogger(__name__)

_PICKLE_DEPRECATED_MESSAGE = (
    "{parameter}='pickle' is deprecated and will be removed in a future release. "
    "Use 'parquet' (default), 'feather', 'csv', or 'json' instead."
)

_MULTI_TS_METADATA_KEY = b"exabel_multi_ts_signals"


# One item or a sequence of them: a string, a filter and an ordering are all things a
# caller naturally passes one of, and a bare string is one item rather than a sequence of
# characters.
_Item = TypeVar("_Item", str, TableColumnFilter, TableColumnOrdering)


def _to_list(value: _Item | Sequence[_Item] | None) -> list[_Item]:
    """Accept a single item or a sequence of them, and return a list either way."""
    if value is None:
        return []
    if isinstance(value, (str, TableColumnFilter, TableColumnOrdering)):
        return [value]
    return list(value)


def _to_column_refs(value: ColumnRef | Sequence[ColumnRef] | None) -> list[ColumnRef]:
    """Accept a single column reference or a sequence of them, and return a list either way.

    Separate from _to_list because a column reference is itself a union, which a value
    restricted type variable cannot express.
    """
    if value is None:
        return []
    if isinstance(value, (str, int)):
        return [value]
    return list(value)


_DEFAULT_PORTS = {"https": 443, "http": 80}


def _merge_headers(extra_headers: Sequence[tuple[str, str]]) -> dict[str, str]:
    """
    Collect the configured extra headers into the form a requests Session takes.

    A header given more than once is comma-joined rather than overwritten, which is how HTTP
    carries a repeated field in one line, and keeps every value the caller asked for: the gRPC
    clients append each pair to their metadata, so dropping all but the last here would make the
    same configuration mean different things on the two transports.
    """
    headers: dict[str, str] = {}
    for name, value in extra_headers:
        name = name.lower()
        headers[name] = f"{headers[name]}, {value}" if name in headers else value
    return headers


def _read_parquet(content: bytes) -> pd.DataFrame:
    """
    Read a parquet response into a DataFrame.

    Guards the engine import so that a caller without pyarrow is told which extra to install,
    rather than getting pandas' own "Unable to find a usable engine". The ``_bytes`` variants
    write the same response straight to disk and need no engine at all.
    """
    with handle_missing_imports(
        warning=(
            "'pyarrow' must be installed to read an export response as a DataFrame. "
            "Install it with: pip install 'exabel[export]'"
        ),
        reraise=True,
    ):
        import pyarrow  # noqa: F401

    return pd.read_parquet(io.BytesIO(content))


def _read_v2_parquet(content: bytes) -> tuple[pd.DataFrame, frozenset[str]]:
    """Read a v2 parquet response and extract the multi-ts signal set.

    The server emits exabel_multi_ts_signals (UTF-8 JSON list of labels)
    into the parquet schema metadata — always present, empty list when no
    multi-ts signals participated. A missing key indicates a contract
    violation (e.g. an unexpected non-server parquet).
    """
    with handle_missing_imports(
        warning=(
            "'pyarrow' must be installed to use the v2 export endpoints. "
            "Install it with: pip install 'exabel[export]'"
        ),
        reraise=True,
    ):
        import pyarrow.parquet as pq

    table = pq.read_table(io.BytesIO(content))
    raw = (table.schema.metadata or {}).get(_MULTI_TS_METADATA_KEY)
    if raw is None:
        raise ValueError(
            f"Parquet response is missing the {_MULTI_TS_METADATA_KEY.decode()!r} schema "
            "metadata key — server did not emit a v2-compatible response."
        )
    return table.to_pandas(), frozenset(json.loads(raw.decode("utf-8")))


class ExportApi:
    """
    API class for data export operations.
    """

    def __init__(self, client_config: ClientConfig):
        auth_headers = {}
        if client_config.access_token:
            auth_headers["Authorization"] = f"Bearer {client_config.access_token}"
        elif client_config.api_key:
            auth_headers["x-api-key"] = client_config.api_key
        session = Session()
        session.headers.update(auth_headers)
        # The headers ClientConfig documents as "included in the request", which the gRPC clients
        # apply and this one did not. They carry the GCP consumer identity that a project-number
        # caller authenticates with, and are the only way to add a header the SDK does not model.
        session.headers.update(_merge_headers(client_config.extra_headers))
        # The port is dropped only when it is the default for the scheme in use. Dropping 443
        # unconditionally would silently turn an http request on 443 into one on port 80.
        default_port = _DEFAULT_PORTS[client_config.export_api_scheme]
        backend = (
            client_config.export_api_host
            if not client_config.export_api_host or client_config.export_api_port == default_port
            else f"{client_config.export_api_host}:{client_config.export_api_port}"
        )
        # Held whole rather than assembled per request, so that every endpoint is reached the same
        # way and the scheme is decided once.
        self._base_url = f"{client_config.export_api_scheme}://{backend}"
        if client_config.retries:
            retry = Retry(
                total=client_config.retries,
                backoff_factor=1.0,
                allowed_methods=["POST"],
                status_forcelist=[500, 502, 503, 504],
            )
            session.mount(f"{client_config.export_api_scheme}://", HTTPAdapter(max_retries=retry))
        self._session = session

    def run_query_bytes(self, query: str | Query, file_format: str) -> bytes:
        """
        Run an export data query, and returns a byte string with the file in the requested format.
        Raises an exception if the status code is not 200.

        file_format is one of:
         * csv
         * excel (.xlsx format)
         * pickle (pickled pandas DataFrame  - deprecated — to be removed)
         * json
         * feather
         * parquet
        """
        if file_format.lower() == "pickle":
            warnings.warn(
                _PICKLE_DEPRECATED_MESSAGE.format(parameter="file_format"),
                DeprecationWarning,
                stacklevel=2,
            )
            file_format = "pickle"
        return self._run_query_bytes(query, file_format)

    def run_query(self, query: str | Query) -> pd.DataFrame:
        """
        Run an export data query, and returns a DataFrame with the results.
        Raises an exception if the status code is not 200.
        """
        content = self._run_query_bytes(query, file_format="pickle")
        return pickle.loads(content)

    def _run_query_bytes(self, query: str | Query, file_format: str) -> bytes:
        if isinstance(query, Query):
            query = query.sql()
        data = {"format": file_format, "query": query}
        url = f"{self._base_url}/v1/export/file"
        start_time = time()
        logger.info("Sending query: %s", query)
        response = self._session.post(url, data=data, timeout=600)
        spent_time = time() - start_time
        logger.info(
            "Query completed in %.1f seconds, received %d bytes, status %d: %s",
            spent_time,
            len(response.content),
            response.status_code,
            query,
        )
        if response.status_code == 200:
            return response.content
        error_message = response.content.decode()
        if error_message.startswith('"') and error_message.endswith('"'):
            error_message = error_message[1:-1]
        error_message = f"Got {response.status_code}: {error_message} for query {query}"
        raise ValueError(error_message)

    @staticmethod
    def _to_column(item: str | Column | DerivedSignal) -> str | Column:
        """Convert a signal specification to a Column for query building."""
        if isinstance(item, DerivedSignal):
            if not item.label or not item.expression:
                raise ValueError(
                    f"DerivedSignal must have both label and expression, "
                    f"got label={item.label!r}, expression={item.expression!r}"
                )
            return Column(name=item.label, expression=item.expression)
        return item  # str or Column pass through unchanged

    @staticmethod
    def _to_timestamp_string(value: str | pd.Timestamp) -> str:
        """Convert a timestamp value to an ISO 8601 string suitable for the v2 JSON request."""
        if isinstance(value, pd.Timestamp):
            if value.tzinfo is None:
                return value.isoformat() + "Z"
            return value.tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ")
        return value if "T" in value else value + "T00:00:00Z"

    @staticmethod
    def _build_v2_signals(
        signal: str | DerivedSignal | Sequence[str | DerivedSignal],
    ) -> list[dict[str, str]]:
        """Convert signal arguments to the v2 JSON format."""
        items = [signal] if isinstance(signal, (str, DerivedSignal)) else signal
        result: list[dict[str, str]] = []
        for item in items:
            if isinstance(item, DerivedSignal):
                if not item.label or not item.expression:
                    raise ValueError(
                        f"DerivedSignal must have both label and expression, "
                        f"got label={item.label!r}, expression={item.expression!r}"
                    )
                result.append({"label": item.label, "expression": item.expression})
            else:
                result.append({"label": item})
        return result

    def _post_v2_signals(
        self,
        signals: list[dict[str, str]],
        *,
        entities: Sequence[str] | None = None,
        tags: Sequence[str] | None = None,
        start_time: str | pd.Timestamp | None = None,
        end_time: str | pd.Timestamp | None = None,
        version: str | pd.Timestamp | None = None,
        output_format: str = "parquet",
    ) -> bytes:
        """POST a structured JSON request to the v2 export signals endpoint.

        Returns the raw response bytes in the requested format.
        """
        if output_format.lower() == "pickle":
            raise ValueError(
                "pickle is not supported on the v2 export endpoint; "
                "use parquet, feather, csv, excel, or json"
            )
        body: dict = {
            "signals": signals,
            "outputFormat": output_format,
        }
        if entities:
            body["entities"] = entities
        if tags:
            body["tags"] = tags
        time_range: dict[str, str] = {}
        if start_time:
            time_range["from"] = self._to_timestamp_string(start_time)
        if end_time:
            time_range["to"] = self._to_timestamp_string(end_time)
        if time_range:
            body["timeRange"] = time_range
        if version is not None:
            body["version"] = self._to_timestamp_string(version)

        return self._post_json("/v2/export/signals", body, description="v2 signal export")

    def _post_json(self, path: str, body: dict[str, object], *, description: str) -> bytes:
        """POST a JSON body to an export endpoint, and return the response bytes.

        Shared by every structured export method. They differ in the body they build and
        the path they post it to; the timeout, the logging and the error shape — a failure
        body that is a JSON string, whose quotes are stripped so the message reads as a
        sentence — are the same for all of them.
        """
        url = f"{self._base_url}{path}"
        start = time()
        logger.info("Sending %s request: %s", description, body)
        response = self._session.post(
            url, data=json.dumps(body), headers={"Content-Type": "application/json"}, timeout=600
        )
        spent_time = time() - start
        logger.info(
            "%s completed in %.1f seconds, received %d bytes, status %d",
            description,
            spent_time,
            len(response.content),
            response.status_code,
        )
        if response.status_code == 200:
            return response.content
        error_message = response.content.decode()
        if error_message.startswith('"') and error_message.endswith('"'):
            error_message = error_message[1:-1]
        raise ValueError(f"Got {response.status_code}: {error_message}")

    def run_export_signals_v2(
        self,
        signals: list[dict[str, str]],
        *,
        start_time: str | pd.Timestamp,
        end_time: str | pd.Timestamp,
        entities: Sequence[str] | None = None,
        tags: Sequence[str] | None = None,
        version: str | pd.Timestamp | None = None,
    ) -> pd.DataFrame:
        """Run a v2 signal export, returning the unprocessed server response as a DataFrame.

        Use this when you need the full multi-level column headers from the server, for
        example to access Bloomberg tickers or time series labels embedded in the column
        headers. For a simpler interface that returns flat columns, use export_signals_v2().

        Unlike export_signals_v2, this method does NOT drop all-NaN rows — the response is
        returned in the exact shape the server emitted, so sparse signals retain their
        empty rows. Use export_signals_v2 if you want sparse rows stripped.

        The returned DataFrame has:
        - A RangeIndex (integer rows).
        - The first column contains timestamps (column header is a tuple of level names).
        - Remaining columns are a MultiIndex. The levels present depend on the query
          shape — Signal and a time-series level are always present; Entity,
          Bloomberg ticker, and Currency levels may be present or absent depending on
          whether the query targets entities and whether any signals carry currency
          metadata. Index levels by name (e.g. get_level_values("Signal")) rather
          than by position when consuming this frame.

        Example::

            df = export_api.run_export_signals_v2(
                signals=[
                    {"label": "Popularity", "expression": "graph_signal('ns.popularity')"},
                    {"label": "Revenue"},
                ],
                entities=["entityTypes/company/entities/F_000C7F-E"],
                start_time="2024-01-01",
                end_time="2024-12-31",
            )

        Args:
            signals:    list of signal specifications, each a dict with 'label' and optionally
                        'expression'. If only 'label' is provided, it must refer to a derived
                        signal in the library. If 'expression' is provided, it is evaluated as
                        a DSL expression and 'label' is used as the column header.
            entities:   entity resource names
                        (e.g., ["entityTypes/company/entities/F_000C7F-E"]).
            tags:       tag resource names (e.g., ["tags/user:123"]).
            start_time: the start of the time range.
            end_time:   the end of the time range.
            version:    point-in-time version at which to evaluate the signals.
        """
        content = self._post_v2_signals(
            signals,
            entities=entities,
            tags=tags,
            start_time=start_time,
            end_time=end_time,
            version=version,
            output_format="parquet",
        )
        return pd.read_parquet(io.BytesIO(content))

    @staticmethod
    def _reshape_v2_response(
        df: pd.DataFrame,
        multi_ts_signals: frozenset[str],
    ) -> pd.DataFrame:
        """Reshape a v2 response DataFrame to the signal_query format.

        The v2 response has MultiIndex columns whose level names always include
        "Signal" and "Time series", and may include "Entity", "Bloomberg ticker",
        and "Currency" depending on the query shape. The first column holds
        timestamps under a tuple of level names as header, and the row index is a
        RangeIndex. Levels are addressed by name so server-side level reordering
        or the addition of new levels does not silently mis-route columns.

        Whenever the response carries an Entity level, the result is pivoted to a
        (name, time) MultiIndex regardless of how many distinct entities are
        present — single- and multi-entity calls return the same row-index shape
        so callers don't branch on entity count.

        Multi-ts signals keep the {signal_label}/{ts_name} column naming for
        every entity, even one whose query happens to match a single sub-entity
        — otherwise callers cannot tell which sub-entity that value belongs to.

        multi_ts_signals is the authoritative set emitted by the server in
        the parquet schema metadata (see _read_v2_parquet).
        """
        time_values = pd.DatetimeIndex(df.iloc[:, 0])
        data_df = df.iloc[:, 1:]

        if not isinstance(data_df.columns, pd.MultiIndex):
            data_df = data_df.copy()
            data_df.index = time_values
            data_df.index.name = "time"
            return data_df

        level_names = data_df.columns.names
        signal_labels = data_df.columns.get_level_values("Signal")
        time_series_labels = data_df.columns.get_level_values("Time series")
        has_entity_level = "Entity" in level_names
        entity_labels = data_df.columns.get_level_values("Entity") if has_entity_level else None

        def _column_name(sig: str, ts_name: str) -> str:
            return f"{sig}/{ts_name}" if sig in multi_ts_signals else sig

        data_df = data_df.set_axis(time_values, axis=0)

        if has_entity_level:
            assert entity_labels is not None  # narrowed by has_entity_level
            unique_entities = list(dict.fromkeys(entity_labels))

            pieces = []
            for entity in unique_entities:
                entity_mask = entity_labels == entity
                entity_slice = data_df.loc[:, entity_mask].copy()
                entity_slice.columns = [
                    _column_name(sig, ts_name)
                    for sig, ts_name in zip(
                        signal_labels[entity_mask], time_series_labels[entity_mask]
                    )
                ]
                pieces.append(entity_slice)

            return pd.concat(pieces, keys=unique_entities, names=["name", "time"])

        # No entity level — keep the flat DatetimeIndex.
        data_df.index.name = "time"
        data_df.columns = [
            _column_name(sig, ts_name) for sig, ts_name in zip(signal_labels, time_series_labels)
        ]
        return data_df

    def export_signals_v2(
        self,
        signals: str | DerivedSignal | Sequence[str | DerivedSignal],
        *,
        start_time: str | pd.Timestamp,
        end_time: str | pd.Timestamp,
        entities: str | Sequence[str] | None = None,
        tags: str | Sequence[str] | None = None,
        version: str | pd.Timestamp | None = None,
    ) -> pd.DataFrame:
        """Export one or more signals using the v2 export endpoint.

        Parameter names align with the wire contract on
        ExportSignalsV2Request (proto exabel/export/export_service.proto):
        signals, entities, tags. Pass both entities and tags in the same
        call to evaluate against the union of the two sets.

        Unlike signal_query(), this method uses the v2 export API which supports
        multi-timeseries signals (e.g., expressions using for_type() that return one time
        series per sub-entity). Entities must be specified by entities or tags rather
        than bloomberg_ticker or factset_id.

        For multi-timeseries signals, each time series becomes a separate column named
        {signal_label}/{ts_name} (e.g., Visits/domain1.com).

        For access to multi-level column headers (including Bloomberg tickers
        and entity names), use run_export_signals_v2() instead.

        Example::

            result = export_api.export_signals_v2(
                DerivedSignal(
                    name=None,
                    label="brand_sales",
                    expression="data('sales').for_type('brand')",
                ),
                entities="entityTypes/company/entities/F_000C7F-E",
                start_time="2024-01-01",
                end_time="2024-12-31",
            )

        Args:
            signals:    the signal(s) to retrieve. A string is sent to the server as a
                        label and resolved there — either as a saved library signal
                        (e.g. "close") or as a DSL expression
                        (e.g. "data('similarweb.all_visits')"). A DerivedSignal lets
                        you pass a DSL expression with an explicit label that becomes
                        the column header. At least one signal must be requested.
            entities:   one Exabel resource name such as
                        "entityTypes/company/entities/F_000C7F-E", or a sequence of
                        such names.
            tags:       one Exabel tag resource name such as "tags/user:123", or a
                        sequence of such names. Signals are exported for the union of
                        the entities given by entities and tags.
            start_time: the first date to retrieve data for.
            end_time:   the last date to retrieve data for.
            version:    the point-in-time at which to evaluate the signals.

        Returns:
            A DataFrame. Rows are a MultiIndex (name, time) whenever entities
            or tags is set (the response carries an Entity level); otherwise the
            rows are a DatetimeIndex. One flat column per signal, or per
            {signal_label}/{ts_name} for multi-timeseries signals. All-NaN rows are dropped.
        """
        if not signals:
            raise ValueError("Must specify signals to retrieve")

        if isinstance(entities, str):
            entities = (entities,)
        if isinstance(tags, str):
            tags = (tags,)
        content = self._post_v2_signals(
            self._build_v2_signals(signals),
            entities=entities,
            tags=tags,
            start_time=start_time,
            end_time=end_time,
            version=version,
            output_format="parquet",
        )
        raw_df, multi_ts_signals = _read_v2_parquet(content)
        df = self._reshape_v2_response(raw_df, multi_ts_signals=multi_ts_signals)
        # Drop rows where every value is NaN so sparse signals don't pad the result.
        return df.dropna(how="all").infer_objects()

    def export_signals_v2_bytes(
        self,
        signals: str | DerivedSignal | Sequence[str | DerivedSignal],
        *,
        start_time: str | pd.Timestamp,
        end_time: str | pd.Timestamp,
        file_format: str = "parquet",
        entities: str | Sequence[str] | None = None,
        tags: str | Sequence[str] | None = None,
        version: str | pd.Timestamp | None = None,
    ) -> bytes:
        """Run a v2 signal export and return the raw response bytes.

        Use this when you need the exported file bytes directly — e.g. to
        persist to disk or forward to another system — without parsing them
        into a DataFrame. This is the only v2 method that works without
        pyarrow installed when file_format is csv, excel, or json; parquet
        and feather bytes come back fine but reading them back as a
        DataFrame still requires pyarrow.

        Args:
            signals:     the signal(s) to retrieve, same semantics as in
                         export_signals_v2.
            file_format: one of parquet, feather, csv, excel, json.
            entities:    entity resource name(s) to evaluate for.
            tags:        tag resource name(s) to evaluate for. Signals are exported for
                         the union of the entities given by entities and tags.
            start_time:  first date to retrieve data for.
            end_time:    last date to retrieve data for.
            version:     point-in-time at which to evaluate the signals.
        """
        if not signals:
            raise ValueError("Must specify signals to retrieve")
        if isinstance(entities, str):
            entities = (entities,)
        if isinstance(tags, str):
            tags = (tags,)
        return self._post_v2_signals(
            self._build_v2_signals(signals),
            entities=entities,
            tags=tags,
            start_time=start_time,
            end_time=end_time,
            version=version,
            output_format=file_format,
        )

    def export_chart(
        self,
        chart: str,
        *,
        entities: str | Sequence[str] | None = None,
        start_time: str | pd.Timestamp | None = None,
        end_time: str | pd.Timestamp | None = None,
        version: str | pd.Timestamp | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> bytes:
        """Render a saved chart as a PNG image, and return the image bytes.

        The chart is rendered as the web app draws it, so nothing here describes what to
        plot: the saved chart carries its signals, its entities and its time range, and
        the arguments below only override the last two.

        Example::

            image = export_api.export_chart("dashboards/1234/widgets/1")
            Path("chart.png").write_bytes(image)

        Args:
            chart:      the chart to render, either a saved chart, "charts/123", or a chart
                        widget in a dashboard, "dashboards/1234/widgets/1". The second form
                        is the only way to reach a chart built inside a dashboard, since
                        such a chart is stored in the dashboard and has no name of its own;
                        list a dashboard's widgets with the Management API to find them.
            entities:   entity resource name(s) to render for, replacing the entities saved
                        with the chart. At most 100 may be given. If empty, the chart's own
                        entities are used.
            start_time: the start of the time range to render over. If neither bound is
                        given, the chart's saved range is used, which is resolved at
                        request time when it is relative.
            end_time:   the end of the time range to render over.
            version:    the point-in-time at which to evaluate the chart's signals.
            width:      image width in pixels, between 100 and 4000. Defaults to 1600, the
                        width the web app's own chart download produces.
            height:     image height in pixels, between 100 and 4000. Defaults to 800.

        Returns:
            The PNG image bytes.
        """
        if not chart:
            raise ValueError("Must specify the chart to render")
        body: dict[str, object] = {"chart": chart}
        chart_entities = _to_list(entities)
        if chart_entities:
            body["entities"] = chart_entities
        time_range: dict[str, str] = {}
        if start_time:
            time_range["from"] = self._to_timestamp_string(start_time)
        if end_time:
            time_range["to"] = self._to_timestamp_string(end_time)
        if time_range:
            body["timeRange"] = time_range
        if version is not None:
            body["version"] = self._to_timestamp_string(version)
        if width is not None:
            body["width"] = width
        if height is not None:
            body["height"] = height
        return self._post_json("/v1/export/chart", body, description="chart export")

    def export_dashboard_table(
        self,
        table: str,
        *,
        columns: ColumnRef | Sequence[ColumnRef] | None = None,
        entities: str | Sequence[str] | None = None,
        included_tags: str | Sequence[str] | None = None,
        any_of_tags: str | Sequence[str] | None = None,
        excluded_tags: str | Sequence[str] | None = None,
        column_filters: TableColumnFilter | Sequence[TableColumnFilter] | None = None,
        column_orderings: TableColumnOrdering | Sequence[TableColumnOrdering] | None = None,
    ) -> pd.DataFrame:
        """Export one dashboard table widget, and return it as a DataFrame.

        The structured counterpart to exporting a dashboard with run_query(): it reaches
        filters that have no SQL syntax, and reports an unknown column as an error rather
        than failing inside the query interpreter. The table is exported as the dashboard
        computed it — this evaluates nothing itself, so a column's own settings, formatting
        and time period are whatever the dashboard says they are.

        Example::

            df = export_api.export_dashboard_table(
                "dashboards/1234/widgets/2",
                columns=["Revenue", "Close price"],
                column_filters=TableColumnFilter("Market cap", above=1e9),
                column_orderings=TableColumnOrdering(0, use_ticker=True),
            )

        Args:
            columns:          the column(s) to export, in the order they should appear,
                              named by identifier, display name or position. If empty,
                              every column is exported in the order the table shows them.
                              The entity columns on the left of the table — the entity
                              name, and for companies also MIC, ticker, FactSet id and
                              Bloomberg ticker — are always included, so naming position 0
                              here adds nothing.
            entities:         entity resource name(s), "entityTypes/company/entities/...",
                              or semantic entity id(s), "graph:entity:...", whose rows are
                              exported. Combined with the tag arguments as a union.
            included_tags:    a row is exported only if its entity has *all* of these tags.
            any_of_tags:      a row is exported only if its entity has *at least one* of
                              these tags. Tags are given either as resource names,
                              "tags/...", or as semantic tag ids, "graph:tag:...".
            excluded_tags:    a row is not exported if its entity has *any* of these tags.
                              This has no equivalent in the SQL export.
            column_filters:   filter(s) on column values. A row is exported only if it
                              passes every one of them.
            column_orderings: the sort order of the rows. At most one is supported; giving
                              more is an error rather than a silent choice of one of them.
                              If empty, rows are sorted by the entity column, ascending.

        Returns:
            A DataFrame with one row per entity and one column per exported table column.
        """
        content = self.export_dashboard_table_bytes(
            table,
            columns=columns,
            entities=entities,
            included_tags=included_tags,
            any_of_tags=any_of_tags,
            excluded_tags=excluded_tags,
            column_filters=column_filters,
            column_orderings=column_orderings,
            file_format="parquet",
        )
        return _read_parquet(content)

    def export_dashboard_table_bytes(
        self,
        table: str,
        *,
        columns: ColumnRef | Sequence[ColumnRef] | None = None,
        entities: str | Sequence[str] | None = None,
        included_tags: str | Sequence[str] | None = None,
        any_of_tags: str | Sequence[str] | None = None,
        excluded_tags: str | Sequence[str] | None = None,
        column_filters: TableColumnFilter | Sequence[TableColumnFilter] | None = None,
        column_orderings: TableColumnOrdering | Sequence[TableColumnOrdering] | None = None,
        file_format: str = "parquet",
    ) -> bytes:
        """Export one dashboard table widget, and return the raw response bytes.

        Use this when you need the exported file bytes directly — to write an Excel file to
        disk, say — without parsing them into a DataFrame. Excel is the one format that
        carries the table's own formatting and its sub-row grouping, both of which a
        DataFrame flattens away.

        Args:
            file_format: one of parquet, csv, excel, json, feather. Note that this defaults
                         to parquet, while the endpoint itself defaults to csv. Unlike the
                         other export methods here, pickle is not accepted.

        See export_dashboard_table for the remaining arguments.
        """
        if file_format.lower() == "pickle":
            raise ValueError(
                "pickle is not supported by the dashboard table export; "
                "use parquet, csv, excel, json or feather"
            )
        body = self._build_dashboard_table_body(
            table,
            columns=columns,
            entities=entities,
            included_tags=included_tags,
            any_of_tags=any_of_tags,
            excluded_tags=excluded_tags,
            column_filters=column_filters,
            column_orderings=column_orderings,
            output_format=file_format,
        )
        return self._post_json(
            "/v1/export/dashboardTable", body, description="dashboard table export"
        )

    @staticmethod
    def _build_dashboard_table_body(
        table: str,
        *,
        columns: ColumnRef | Sequence[ColumnRef] | None = None,
        entities: str | Sequence[str] | None = None,
        included_tags: str | Sequence[str] | None = None,
        any_of_tags: str | Sequence[str] | None = None,
        excluded_tags: str | Sequence[str] | None = None,
        column_filters: TableColumnFilter | Sequence[TableColumnFilter] | None = None,
        column_orderings: TableColumnOrdering | Sequence[TableColumnOrdering] | None = None,
        output_format: str = "csv",
    ) -> dict[str, object]:
        """Build the JSON body of a dashboard table export request.

        The three tag arguments are separate parameters rather than one filter object
        because they are combined with AND, so a caller passing two of them is asking for
        one filter, not two.
        """
        if not table or not table.startswith("dashboards/") or "/widgets/" not in table:
            raise ValueError(
                f"The table must be named as 'dashboards/{{dashboard}}/widgets/{{widget}}', "
                f"but got {table!r}"
            )
        body: dict[str, object] = {"table": table, "outputFormat": output_format}
        # Each argument is normalised before it is tested, rather than testing the argument
        # itself: position 0 is a column reference and not an unset field, and a falsy check
        # on the argument would drop it.
        selected_columns = _to_column_refs(columns)
        if selected_columns:
            body["columns"] = [column_ref_to_json(column) for column in selected_columns]
        selected_entities = _to_list(entities)
        if selected_entities:
            body["entities"] = selected_entities
        tag_filter = {
            field: tags
            for field, tags in (
                ("includedTags", _to_list(included_tags)),
                ("anyOfTags", _to_list(any_of_tags)),
                ("excludedTags", _to_list(excluded_tags)),
            )
            if tags
        }
        if tag_filter:
            body["tagFilter"] = tag_filter
        filters = _to_list(column_filters)
        if filters:
            body["columnFilters"] = [column_filter.to_json() for column_filter in filters]
        orderings = _to_list(column_orderings)
        if orderings:
            body["columnOrderings"] = [ordering.to_json() for ordering in orderings]
        return body

    def signal_query(
        self,
        signal: str | Column | DerivedSignal | Sequence[str | Column | DerivedSignal],
        bloomberg_ticker: str | Sequence[str] | None = None,
        *,
        factset_id: str | Sequence[str] | None = None,
        resource_name: str | Sequence[str] | None = None,
        tag: str | Sequence[str] | None = None,
        start_time: str | pd.Timestamp | None = None,
        end_time: str | pd.Timestamp | None = None,
        identifier: Column | Sequence[Column] | None = None,
        version: str | pd.Timestamp | Sequence[str] | Sequence[pd.Timestamp] | None = None,
    ) -> pd.Series | pd.DataFrame:
        """
        Run a query for one or more signals.

        The entity or entities to retrieve data for can be specified using either
        bloomberg_ticker, factset_id, resource name or tag, but these methods cannot be combined.
        Alternatively, specify none of these parameters for signals that are not
        related to any entity.

        Args:
            signal:     the signal(s) to retrieve, as string identifiers, Column objects,
                        or DerivedSignal objects. At least one signal must be requested.
            bloomberg_ticker: a Bloomberg ticker such as "AAPL US", or a list of such tickers.
            factset_id: a FactSet id such as "QLGSL2-R", or a list of such identifiers.
            resource_name: an Exabel resource name such as "entityTypes/company/entities/F_000C7F-E"
                        or a list of such identifiers.
            tag:        retrieve data for the entities with this Exabel tag ID,
                        or with any of the provided tags if several.
            start_time: the first date to retrieve data for
            end_time:   the last date to retrieve data for
            identifier: the identifier(s) to return to identify the entities in the result.
                        By default, will use Signals.NAME if multiple identifiers
                        or a tag are given, or else no identifier.
            version:    the Point-in-Time at which to evaluate the signals,
                        or a list of such dates at which to evaluate the signals.
                        If a list of dates is provided, 'version' will be included as a column
                        in the result.
                        If no version is specified, then the signals will be evaluated with the
                        latest available data (the default).

        Returns:
            A pandas Series if the result is a single time series per entity,
            or a pandas DataFrame if there are multiple time series in the result.
            If a single entity identifier was specified, the index is a DatetimeIndex.
            If a list of entity identifiers or a tag was given, the index is a MultiIndex with
            entity on the first level and time on the second level.
        """
        if not signal:
            raise ValueError("Must specify signal to retrieve")

        # Specify entity filter
        multi_entity = False
        predicates: list[Predicate] = []
        if factset_id:
            if isinstance(factset_id, str):
                predicates.append(Signals.FACTSET_ID.equal(factset_id))
            else:
                predicates.append(Signals.FACTSET_ID.in_list(*factset_id))
                multi_entity = True
        if bloomberg_ticker:
            if isinstance(bloomberg_ticker, str):
                predicates.append(Signals.BLOOMBERG_TICKER.equal(bloomberg_ticker))
            else:
                predicates.append(Signals.BLOOMBERG_TICKER.in_list(*bloomberg_ticker))
                multi_entity = True
        if resource_name:
            if isinstance(resource_name, str):
                predicates.append(Signals.RESOURCE_NAME.equal(resource_name))
            else:
                predicates.append(Signals.RESOURCE_NAME.in_list(*resource_name))
                multi_entity = True
        if tag:
            if isinstance(tag, str):
                predicates.append(Signals.has_tag(tag))
            else:
                predicates.append(Signals.has_tag(*tag))
            multi_entity = True
        if len(predicates) > 1:
            raise ValueError("At most one entity identification method can be specified")

        # Specify the identifier(s)
        index: list[Column] = []
        if identifier is None:
            if multi_entity:
                index.append(Signals.NAME)
        elif isinstance(identifier, Column):
            index.append(identifier)
        else:
            index.extend(identifier)
        index.append(Signals.TIME)

        # Specify version(s), if provided
        if version:
            if isinstance(version, (str, pd.Timestamp)):
                predicates.append(Signals.VERSION.equal(version))
            else:
                predicates.append(Signals.VERSION.in_list(*version))
                index.insert(0, Signals.VERSION)

        # The columns to query for
        columns: list[str | Column] = list(index)
        if isinstance(signal, (str, Column, DerivedSignal)):
            columns.append(self._to_column(signal))
        else:
            columns.extend(self._to_column(s) for s in signal)

        # Execute the query
        query = Signals.query(
            columns, start_time=start_time, end_time=end_time, predicates=predicates
        )
        df = self.run_query(query.sql())

        # Set the row index
        df = df.set_index([col.name for col in index])
        # Squeeze to a Series if a single time series was returned,
        # and fix the data type (the backend returns a DataFrame with dtype=object)
        return df.squeeze(axis=1).infer_objects()

    def batched_signal_query(
        self,
        batch_size: int,
        signal: str | Column | DerivedSignal | Sequence[str | Column | DerivedSignal],
        *,
        bloomberg_ticker: Sequence[str] | None = None,
        factset_id: Sequence[str] | None = None,
        resource_name: Sequence[str] | None = None,
        start_time: str | pd.Timestamp | None = None,
        end_time: str | pd.Timestamp | None = None,
        identifier: Column | Sequence[Column] | None = None,
        version: str | pd.Timestamp | Sequence[str] | Sequence[pd.Timestamp] | None = None,
        show_progress: bool = False,
    ) -> pd.Series | pd.DataFrame:
        """
        Run a query for one or more signals.

        The entity or entities to retrieve data for can be specified using either
        bloomberg_ticker, factset_id or resource name, but these methods cannot be combined.

        Args:
            batch_size:  the number of entities to include in each API call.

        Other arguments are the same as for the signal_query method.
        (Note that 'tag' cannot be used to specify entities in this batched version)

        Returns:
            A pandas Series if the result is a single time series per entity,
            or a pandas DataFrame if there are multiple time series in the result.
            The index is a MultiIndex with entity on the first level and time on the second level.
        """
        entity_identifiers: list[str] = []
        entities: Sequence[str] = []
        if factset_id:
            entity_identifiers.append("factset_id")
            entities = factset_id
        if bloomberg_ticker:
            entity_identifiers.append("bloomberg_ticker")
            entities = bloomberg_ticker
        if resource_name:
            entity_identifiers.append("resource_name")
            entities = resource_name
        if not entity_identifiers:
            raise ValueError("Need to specify an identification method")
        if len(entity_identifiers) > 1:
            raise ValueError(
                "At most one entity identification method can be specified"
                + f", but got {entity_identifiers}"
            )
        entity_identifier = entity_identifiers[0]
        results = [
            self.signal_query(
                signal=signal,
                start_time=start_time,
                end_time=end_time,
                identifier=identifier,
                version=version,
                **{entity_identifier: entities[i : i + batch_size]},
            )
            for i in conditional_progress_bar(
                range(0, len(entities), batch_size), show_progress=show_progress
            )
        ]
        return pd.concat(results)
