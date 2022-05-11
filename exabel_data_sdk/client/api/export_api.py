import logging
import pickle
from time import time
from typing import List, Mapping, Sequence, Union

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
    """

    def __init__(
        self, auth_headers: Mapping[str, str] = None, *, backend: str = "endpoints.exabel.com"
    ):
        """
        If authentication headers are not provided, this method will attempt to obtain them
        by logging in with the UserLogin script.

        Args:
            auth_headers: authentication headers for the HTTPS requests to the backend server
            backend:      the address of the backend server. This field is only for internal
                          use at Exabel and should never be set by customers or partners.
        """
        if auth_headers is None:
            # Attempt to log in
            auth_headers = UserLogin().get_auth_headers()
        self._auth_headers = auth_headers
        self._backend = backend

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
        response = requests.post(url, headers=self._auth_headers, data=data)
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
        bloomberg_ticker: Union[str, Sequence[str]] = None,
        *,
        factset_id: Union[str, Sequence[str]] = None,
        tag: Union[str, Sequence[str]] = None,
        start_time: Union[str, pd.Timestamp] = None,
        end_time: Union[str, pd.Timestamp] = None,
        identifier: Union[Column, Sequence[Column]] = None,
        version: Union[str, pd.Timestamp, Sequence[str], Sequence[pd.Timestamp]] = None,
    ) -> Union[pd.Series, pd.DataFrame]:
        """
        Run a query for one or more signals.

        The company or companies to retrieve data for can be specified using either
        bloomberg_ticker, factset_id or tag, but these methods cannot be combined.
        Alternatively, specify none of these parameters for signals that are not
        related to any entity.

        Args:
            signal:     the signal(s) to retrieve, as string identifiers or Column objects.
                        At least one signal must be requested.
            bloomberg_ticker: a Bloomberg ticker such as "AAPL US", or a list of such tickers.
            factset_id: a FactSet id such as "QLGSL2-R", or a list of such identifiers.
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
            A pandas Series if the result is a single time series,
            or a pandas DataFrame if there are multiple time series in the result.
            If a single company identifier was specified, the index is a DatetimeIndex.
            If a list of company identifiers or a tag was given, the index is a MultiIndex with
            company on the first level and time on the second level.
        """
        if not signal:
            raise ValueError("Must specify signal to retrieve")

        # Specify entity filter
        multi_company = False
        predicates: List[Predicate] = []
        if factset_id:
            if isinstance(factset_id, str):
                predicates.append(Signals.FACTSET_ID.equal(factset_id))
            else:
                predicates.append(Signals.FACTSET_ID.in_list(*factset_id))
                multi_company = True
        if bloomberg_ticker:
            if isinstance(bloomberg_ticker, str):
                predicates.append(Signals.BLOOMBERG_TICKER.equal(bloomberg_ticker))
            else:
                predicates.append(Signals.BLOOMBERG_TICKER.in_list(*bloomberg_ticker))
                multi_company = True
        if tag:
            if isinstance(tag, str):
                predicates.append(Signals.has_tag(tag))
            else:
                predicates.append(Signals.has_tag(*tag))
            multi_company = True
        if len(predicates) > 1:
            raise ValueError("At most one company identification method can be specified")

        # Specify the identifier(s)
        index: List[Column] = []
        if identifier is None:
            if multi_company:
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
