import logging
import pickle
from time import time
from typing import List, Mapping, Optional, Sequence, Union

import pandas as pd
import requests

from exabel_data_sdk.client.user_login import UserLogin
from exabel_data_sdk.query.column import Column
from exabel_data_sdk.query.predicate import Predicate
from exabel_data_sdk.query.query import Query
from exabel_data_sdk.query.signals import Signals


class ExportApi:
    """
    API class for data export operations.

    If authentication headers are not provided, this method will attempt to obtain them by logging
    in with the UserLogin script.

    Args:
        auth_headers:   authentication headers for the HTTPS requests to the backend server
        backend:        the address of the backend server. This field is only for internal use at
                        Exabel and should never be set by customers or partners.
        reauthenticate: if True, the user will be prompted to log in again.
        user:           the Exabel user to log in as, e.g. `my_user@enterprise.com`. If not
                        provided, the default user will be logged in.
    """

    def __init__(
        self,
        auth_headers: Optional[Mapping[str, str]] = None,
        *,
        backend: str = "endpoints.exabel.com",
        reauthenticate: bool = False,
        user: Optional[str] = None,
    ):
        if auth_headers is None:
            # Attempt to log in
            auth_headers = UserLogin(reauthenticate=reauthenticate, user=user).get_auth_headers()
        self._auth_headers = auth_headers
        self._backend = backend

    @staticmethod
    def from_api_key(api_key: str, use_test_backend: bool = False) -> "ExportApi":
        """Create an `ExportApi` from an API key."""
        backend = "export.api-test.exabel.com" if use_test_backend else "export.api.exabel.com"
        return ExportApi(auth_headers={"x-api-key": api_key}, backend=backend)

    def run_query_bytes(self, query: Union[str, Query], file_format: str) -> bytes:
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
        response = requests.post(url, headers=self._auth_headers, data=data, timeout=600)
        spent_time = time() - start_time
        logging.getLogger(__name__).info(
            "Query completed in %.1f seconds, received %d bytes: %s",
            spent_time,
            len(response.content),
            query,
        )
        if response.status_code == 200:
            return response.content
        error_message = response.content.decode()
        if error_message.startswith('"') and error_message.endswith('"'):
            error_message = error_message[1:-1]
        error_message = f"{response.status_code}: {error_message}"
        raise Exception(error_message)

    def run_query(self, query: Union[str, Query]) -> pd.DataFrame:
        """
        Run an export data query, and returns a DataFrame with the results.
        Raises an exception if the status code is not 200.
        """
        content = self.run_query_bytes(query, file_format="pickle")
        content = pickle.loads(content)
        assert isinstance(content, pd.DataFrame)
        return content

    def signal_query(
        self,
        signal: Union[str, Column, Sequence[Union[str, Column]]],
        bloomberg_ticker: Optional[Union[str, Sequence[str]]] = None,
        *,
        factset_id: Optional[Union[str, Sequence[str]]] = None,
        resource_name: Optional[Union[str, Sequence[str]]] = None,
        tag: Optional[Union[str, Sequence[str]]] = None,
        start_time: Optional[Union[str, pd.Timestamp]] = None,
        end_time: Optional[Union[str, pd.Timestamp]] = None,
        identifier: Optional[Union[Column, Sequence[Column]]] = None,
        version: Optional[Union[str, pd.Timestamp, Sequence[str], Sequence[pd.Timestamp]]] = None,
    ) -> Union[pd.Series, pd.DataFrame]:
        """
        Run a query for one or more signals.

        The entity or entities to retrieve data for can be specified using either
        bloomberg_ticker, factset_id, resource name or tag, but these methods cannot be combined.
        Alternatively, specify none of these parameters for signals that are not
        related to any entity.

        Args:
            signal:     the signal(s) to retrieve, as string identifiers or Column objects.
                        At least one signal must be requested.
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
        predicates: List[Predicate] = []
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
        index: List[Column] = []
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
        columns: List[Union[str, Column]] = list(index)
        if isinstance(signal, (str, Column)):
            columns.append(signal)
        else:
            columns.extend(signal)

        # Execute the query
        query = Signals.query(
            columns, start_time=start_time, end_time=end_time, predicates=predicates
        )
        df = self.run_query(query.sql())

        # Set the row index
        df.set_index([col.name for col in index], inplace=True)
        # Squeeze to a Series if a single time series was returned,
        # and fix the data type (the backend returns a DataFrame with dtype=object)
        return df.squeeze(axis=1).infer_objects()

    def batched_signal_query(
        self,
        batch_size: int,
        signal: Union[str, Column, Sequence[Union[str, Column]]],
        *,
        bloomberg_ticker: Optional[Sequence[str]] = None,
        factset_id: Optional[Sequence[str]] = None,
        resource_name: Optional[Sequence[str]] = None,
        start_time: Optional[Union[str, pd.Timestamp]] = None,
        end_time: Optional[Union[str, pd.Timestamp]] = None,
        identifier: Optional[Union[Column, Sequence[Column]]] = None,
        version: Optional[Union[str, pd.Timestamp, Sequence[str], Sequence[pd.Timestamp]]] = None,
    ) -> Union[pd.Series, pd.DataFrame]:
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
        entity_identifiers: List[str] = []
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
            for i in range(0, len(entities), batch_size)
        ]
        return pd.concat(results)
