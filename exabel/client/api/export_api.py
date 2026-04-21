import json
import logging
import pickle
from time import time
from typing import Sequence

import pandas as pd
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from exabel.client.api.data_classes.derived_signal import DerivedSignal
from exabel.client.client_config import ClientConfig
from exabel.query.column import Column
from exabel.query.predicate import Predicate
from exabel.query.query import Query
from exabel.query.signals import Signals
from exabel.scripts.utils import conditional_progress_bar

logger = logging.getLogger(__name__)


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
        if client_config.retries:
            retry = Retry(
                total=client_config.retries,
                backoff_factor=1.0,
                allowed_methods=["POST"],
                status_forcelist=[500, 502, 503, 504],
            )
            session.mount("https://", HTTPAdapter(max_retries=retry))
        self._session = session
        self._backend = (
            client_config.export_api_host
            if not client_config.export_api_host or client_config.export_api_port == 443
            else f"{client_config.export_api_host}:{client_config.export_api_port}"
        )

    def run_query_bytes(self, query: str | Query, file_format: str) -> bytes:
        """
        Run an export data query, and returns a byte string with the file in the requested format.
        Raises an exception if the status code is not 200.

        file_format is one of:
         * csv
         * excel (.xlsx format)
         * pickle (pickled pandas DataFrame)
         * json
         * feather
         * parquet
        """
        if isinstance(query, Query):
            query = query.sql()
        data = {"format": file_format, "query": query}
        url = f"https://{self._backend}/v1/export/file"
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

    def run_query(self, query: str | Query) -> pd.DataFrame:
        """
        Run an export data query, and returns a DataFrame with the results.
        Raises an exception if the status code is not 200.
        """
        content = self.run_query_bytes(query, file_format="pickle")
        content = pickle.loads(content)
        assert isinstance(content, pd.DataFrame)
        return content

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
        signal: str | Column | DerivedSignal | Sequence[str | Column | DerivedSignal],
    ) -> list[dict[str, str]]:
        """Convert signal arguments to the v2 JSON format."""
        items = [signal] if isinstance(signal, (str, Column, DerivedSignal)) else signal
        result: list[dict[str, str]] = []
        for item in items:
            if isinstance(item, DerivedSignal):
                if not item.label or not item.expression:
                    raise ValueError(
                        f"DerivedSignal must have both label and expression, "
                        f"got label={item.label!r}, expression={item.expression!r}"
                    )
                result.append({"label": item.label, "expression": item.expression})
            elif isinstance(item, Column):
                entry: dict[str, str] = {"label": item.name}
                if item.expression:
                    entry["expression"] = item.expression
                result.append(entry)
            else:
                result.append({"label": item})
        return result

    def _post_v2_signals(
        self,
        signals: list[dict[str, str]],
        *,
        entities: list[str] | None = None,
        tags: list[str] | None = None,
        start_time: str | pd.Timestamp | None = None,
        end_time: str | pd.Timestamp | None = None,
        version: str | pd.Timestamp | None = None,
        output_format: str = "pickle",
    ) -> bytes:
        """POST a structured JSON request to the v2 export signals endpoint.

        Returns the raw response bytes in the requested format.
        """
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

        url = f"https://{self._backend}/v2/export/signals"
        start = time()
        logger.info("Sending v2 signal query: %s", body)
        response = self._session.post(
            url, data=json.dumps(body), headers={"Content-Type": "application/json"}, timeout=600
        )
        spent_time = time() - start
        logger.info(
            "v2 query completed in %.1f seconds, received %d bytes, status %d",
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

    def run_signal_query_v2(
        self,
        signals: list[dict[str, str]],
        *,
        entities: list[str] | None = None,
        tags: list[str] | None = None,
        start_time: str | pd.Timestamp | None = None,
        end_time: str | pd.Timestamp | None = None,
        version: str | pd.Timestamp | None = None,
    ) -> pd.DataFrame:
        """Run a v2 signal export query, returning the unprocessed server response as a DataFrame.

        Use this when you need the full multi-level column structure from the server, for
        example to access Bloomberg tickers or time series labels embedded in the column
        headers. For a simpler interface that returns flat columns, use signal_query_v2().

        The returned DataFrame has:
        - A RangeIndex (integer rows).
        - The first column contains timestamps (column header is a tuple of level names).
        - Remaining columns are a MultiIndex with levels
          (Signal, Entity, Bloomberg ticker, Time series), where each column represents
          one (signal, entity, time series) combination.

        Example::

            df = export_api.run_signal_query_v2(
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
            output_format="pickle",
        )
        result_df = pickle.loads(content)
        assert isinstance(result_df, pd.DataFrame)
        return result_df

    @staticmethod
    def _reshape_v2_response(
        df: pd.DataFrame,
        multi_entity: bool,
    ) -> pd.DataFrame:
        """Reshape a v2 response DataFrame to the signal_query format.

        The v2 response has MultiIndex columns (Signal, Entity, Bloomberg ticker, Time series)
        with the first column containing timestamps and a RangeIndex for rows.
        """
        time_values = pd.DatetimeIndex(df.iloc[:, 0])
        data_df = df.iloc[:, 1:]

        if not isinstance(data_df.columns, pd.MultiIndex):
            data_df = data_df.copy()
            data_df.index = time_values
            data_df.index.name = "time"
            return data_df

        signal_labels = data_df.columns.get_level_values(0)
        has_entity_level = data_df.columns.nlevels >= 4

        if has_entity_level and multi_entity:
            entity_names = data_df.columns.get_level_values(1)
            unique_entities = list(dict.fromkeys(entity_names))
            unique_signals = list(dict.fromkeys(signal_labels))
            ts_level = data_df.columns.nlevels - 1

            pieces = []
            for entity in unique_entities:
                entity_mask = entity_names == entity
                entity_data = data_df.loc[:, entity_mask]
                entity_signal_labels = signal_labels[entity_mask]

                entity_df = pd.DataFrame(index=time_values)
                for sig in unique_signals:
                    sig_mask = entity_signal_labels == sig
                    sig_cols = entity_data.loc[:, sig_mask]
                    if sig_cols.shape[1] == 0:
                        continue
                    if sig_cols.shape[1] == 1:
                        entity_df[sig] = sig_cols.iloc[:, 0].values
                    else:
                        ts_names = data_df.columns.get_level_values(ts_level)[entity_mask][sig_mask]
                        for i, ts_name in enumerate(ts_names):
                            entity_df[f"{sig}/{ts_name}"] = sig_cols.iloc[:, i].values

                entity_df["__entity__"] = entity
                pieces.append(entity_df)

            result = pd.concat(pieces)
            result.index.name = "time"
            result = result.reset_index().set_index(["__entity__", "time"])
            result.index.names = ["name", "time"]
            return result

        # Single entity or no entity level
        result = pd.DataFrame(index=time_values)
        result.index.name = "time"
        unique_signals = list(dict.fromkeys(signal_labels))
        ts_level = data_df.columns.nlevels - 1

        for sig in unique_signals:
            sig_mask = signal_labels == sig
            sig_cols = data_df.loc[:, sig_mask]
            if sig_cols.shape[1] == 1:
                result[sig] = sig_cols.iloc[:, 0].values
            else:
                ts_names = data_df.columns.get_level_values(ts_level)[sig_mask]
                for i, ts_name in enumerate(ts_names):
                    result[f"{sig}/{ts_name}"] = sig_cols.iloc[:, i].values

        return result

    def signal_query_v2(
        self,
        signal: str | Column | DerivedSignal | Sequence[str | Column | DerivedSignal],
        *,
        resource_name: str | Sequence[str] | None = None,
        tag: str | Sequence[str] | None = None,
        start_time: str | pd.Timestamp | None = None,
        end_time: str | pd.Timestamp | None = None,
        version: str | pd.Timestamp | None = None,
    ) -> pd.Series | pd.DataFrame:
        """Run a query for one or more signals using the v2 export endpoint.

        Unlike signal_query(), this method uses the v2 export API which supports
        multi-timeseries signals (e.g., expressions using for_type() that return one time
        series per sub-entity). Entities must be specified by resource_name or tag rather
        than bloomberg_ticker or factset_id.

        For multi-timeseries signals, each time series becomes a separate column named
        ``"{signal_label}/{time_series_name}"`` (e.g., ``"Visits/domain1.com"``).

        For access to the full server response with multi-level column headers (including
        Bloomberg tickers and entity names), use run_signal_query_v2() instead.

        Example::

            result = export_api.signal_query_v2(
                DerivedSignal(
                    name=None,
                    label="sweb_visits",
                    expression="data('similarweb.all_visits').for_type('similarweb.domain')",
                ),
                resource_name="entityTypes/company/entities/F_000C7F-E",
                start_time="2024-01-01",
                end_time="2024-12-31",
            )

        Args:
            signal:     the signal(s) to retrieve. A string is interpreted as a signal label
                        from the library. Column and DerivedSignal objects allow specifying
                        a DSL expression with a label. At least one signal must be requested.
            resource_name: an Exabel resource name such as
                        "entityTypes/company/entities/F_000C7F-E", or a list of such names.
            tag:        an Exabel tag resource name such as "tags/user:123",
                        or a list of such names.
            start_time: the first date to retrieve data for.
            end_time:   the last date to retrieve data for.
            version:    the point-in-time at which to evaluate the signals.

        Returns:
            A pandas Series if the result is a single time series,
            or a pandas DataFrame if there are multiple time series in the result.
            If a single entity was specified, the index is a DatetimeIndex.
            If multiple entities or a tag was given, the index is a MultiIndex with
            entity on the first level and time on the second level.
        """
        if not signal:
            raise ValueError("Must specify signal to retrieve")

        v2_signals = self._build_v2_signals(signal)

        entities: list[str] | None = None
        tags: list[str] | None = None
        multi_entity = False

        if resource_name is not None:
            entities = [resource_name] if isinstance(resource_name, str) else list(resource_name)
            multi_entity = len(entities) > 1
        if tag is not None:
            tags = [tag] if isinstance(tag, str) else list(tag)
            multi_entity = True

        content = self._post_v2_signals(
            v2_signals,
            entities=entities,
            tags=tags,
            start_time=start_time,
            end_time=end_time,
            version=version,
            output_format="pickle",
        )
        raw_df = pickle.loads(content)
        assert isinstance(raw_df, pd.DataFrame)
        df = self._reshape_v2_response(raw_df, multi_entity=multi_entity)
        return df.squeeze(axis=1).infer_objects()

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
