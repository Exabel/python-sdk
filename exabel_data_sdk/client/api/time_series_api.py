from typing import Optional, Sequence

import pandas as pd
from dateutil import tz
from google.protobuf import timestamp_pb2
from google.protobuf.wrappers_pb2 import DoubleValue

from exabel_data_sdk.client.api.api_client.grpc.time_series_grpc_client import TimeSeriesGrpcClient
from exabel_data_sdk.client.api.api_client.http.time_series_http_client import TimeSeriesHttpClient
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    BatchDeleteTimeSeriesPointsRequest,
    CreateTimeSeriesRequest,
    DeleteTimeSeriesRequest,
    GetTimeSeriesRequest,
    ListTimeSeriesRequest,
)
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import TimeSeries as ProtoTimeSeries
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    TimeSeriesPoint,
    TimeSeriesView,
    UpdateTimeSeriesRequest,
)
from exabel_data_sdk.stubs.exabel.api.time.time_range_pb2 import TimeRange


class TimeSeriesApi:
    """
    API class for time series CRUD operations.
    """

    def __init__(self, config: ClientConfig, use_json: bool):
        self.client = (TimeSeriesHttpClient if use_json else TimeSeriesGrpcClient)(config)

    def get_signal_time_series(
        self, signal: str, page_size: int = 1000, page_token: str = None
    ) -> PagingResult[str]:
        """
        Get the resource names of all time series for one signal.

        Args:
            signal:     The signal to get time series for, for example "signal/ns.signal1".
            page_size:  The maximum number of results to return. Defaults to 1000, which is also
                        the maximum size of this field.
            page_token: The page token to resume the results from.
        """
        response = self.client.list_time_series(
            ListTimeSeriesRequest(parent=signal, page_size=page_size, page_token=page_token)
        )
        return PagingResult(
            [t.name for t in response.time_series],
            response.next_page_token,
            response.total_size,
        )

    def get_entity_time_series(
        self, entity: str, page_size: int = 1000, page_token: str = None
    ) -> PagingResult[str]:
        """
        Get the resource names of all time series for one entity.

        Args:
            entity:     The entity to get time series for, for example
                        "entityTypes/ns.type1/entities/ns.entity1".
            page_size:  The maximum number of results to return. Defaults to 1000, which is also
                        the maximum size of this field.
            page_token: The page token to resume the results from.
        """
        response = self.client.list_time_series(
            ListTimeSeriesRequest(parent=entity, page_size=page_size, page_token=page_token),
        )
        return PagingResult(
            [t.name for t in response.time_series],
            response.next_page_token,
            response.total_size,
        )

    def get_time_series(
        self, name: str, start: pd.Timestamp = None, end: pd.Timestamp = None
    ) -> Optional[pd.Series]:
        """
        Get one time series.

        If start and end are not specified, all data points will be returned.
        If start or end is specified, both must be specified.

        If time series does not exist, None is returned.

        Args:
            name:   The resource name of the requested time series, for example
                    "entityTypes/ns.type1/entities/ns.entity1/signals/ns.signal1" or
                    "signals/ns.signal1/entityTypes/ns.type1/entities/ns.entity1".
            start:  Start of the period to get data for.
            end:    End of the period to get data for.
        """
        if bool(start) != bool(end):
            raise ValueError("Either specify both 'start' and 'end' or none of them.")
        time_range = self._get_time_range(start, end)

        try:
            time_series = self.client.get_time_series(
                GetTimeSeriesRequest(name=name, view=TimeSeriesView(time_range=time_range)),
            )
        except RequestError as error:
            if error.error_type == ErrorType.NOT_FOUND:
                return None
            raise

        return self._time_series_points_to_series(time_series.points, time_series.name)

    def create_time_series(self, name: str, series: pd.Series, create_tag: bool = False) -> None:
        """
        Create a time series.

        A time series has one entity and one signal as its parents. As such, it can be
        referred to as both "{entity_name}/{signal_name}" and "{signal_name}/{entity_name}". The
        first version is the canonical form. The signal must be associated with the entity's type.

        Args:
            name:       The resource name of the time series, for example
                        "entityTypes/ns1.type/entities/ns2.entities/signals/ns3.signal".
                        An alternative name for the same time series is
                        "signals/ns3.signal/entityTypes/ns1.type/entities/ns2.entity". The
                        namespaces must be empty (being global) or one of the predetermined
                        namespaces the customer has access to. If ns2 is not empty, it must be
                        equals to ns3, and if ns1 is not empty, all three namespaces must be equal.
            series:     The time series data
            create_tag: Set to true to create a tag for every entity type a signal has time series
                        for. If a tag already exists, it will be updated when time series are
                        created (or deleted) regardless of the value of this flag.
        """
        time_series_points = self._series_to_time_series_points(series)
        self.client.create_time_series(
            CreateTimeSeriesRequest(
                time_series=ProtoTimeSeries(name=name, points=time_series_points),
                create_tag=create_tag,
            ),
        )

    def upsert_time_series(self, name: str, series: pd.Series, create_tag: bool = False) -> None:
        """
        Create or update a time series.

        Args:
            name:       The resource name of the time series, for example
                        "entityTypes/ns1.type/entities/ns2.entities/signals/ns3.signal".
                        An alternative name for the same time series is
                        "signals/ns3.signal/entityTypes/ns1.type/entities/ns2.entity".
                        The namespaces must be empty (being global) or one of the predetermined
                        namespaces the customer has access to. If ns2 is not empty, it must be
                        equals to ns3, and if ns1 is not empty, all three namespaces must be equal.
            series:     The time series data
            create_tag: Set to true to create a tag for every entity type a signal has time series
                        for. If a tag already exists, it will be updated when time series are
                        created (or deleted) regardless of the value of this flag.

        """
        if self.time_series_exists(name):
            self.append_time_series_data(name, series)
        else:
            self.create_time_series(name, series, create_tag)

    def clear_time_series_data(self, name: str, start: pd.Timestamp, end: pd.Timestamp) -> None:
        """
        Delete data points in the given interval for the given time series.

        Args:
            name:   The resource name of the time series.
            start:  Start of the period to delete data for.
            end:    End of the period to delete data for.
        """
        time_range = self._get_time_range(start, end)
        self.client.batch_delete_time_series_points(
            BatchDeleteTimeSeriesPointsRequest(name=name, time_ranges=[time_range]),
        )

    def append_time_series_data(self, name: str, series: pd.Series) -> pd.Series:
        """
        Append data to the given time series.

        If the given series contains data points that already exist, these data points will be
        overwritten.

        Args:
            name:   The resource name of the time series.
            series: Series with data to append.

        Returns:
            A series with all data for the given time series.
        """
        proto_time_series = ProtoTimeSeries(
            name=name, points=self._series_to_time_series_points(series)
        )

        # Set empty TimeRange() in request to get back entire time series.
        time_series = self.client.update_time_series(
            UpdateTimeSeriesRequest(
                time_series=proto_time_series,
                view=TimeSeriesView(time_range=TimeRange()),
            ),
        )
        return self._time_series_points_to_series(time_series.points, time_series.name)

    def delete_time_series(self, name: str) -> None:
        """
        Delete a time series.

        Args:
            name:   The resource name of the time series to be deleted, for example
                    "entityTypes/ns.type1/entities/ns.entity1/signals/ns.signal1" or
                    "signals/ns.signal1/entityTypes/ns.type1/entities/ns.entity1".
        """
        self.client.delete_time_series(DeleteTimeSeriesRequest(name=name))

    def time_series_exists(self, name: str) -> bool:
        """
        Determine whether a time series with the given name already exists.

        Args:
            name:   The resource name of the time series, for example
                    "entityTypes/ns.type1/entities/ns.entity1/signals/ns.signal1".
        """
        return self.get_time_series(name) is not None

    @staticmethod
    def _series_to_time_series_points(series: pd.Series) -> Sequence[TimeSeriesPoint]:
        """Convert a pandas Series to a sequence of TimeSeriesPoint."""
        points = []
        for timestamp, value in series.iteritems():
            proto_timestamp = timestamp_pb2.Timestamp()
            if not timestamp.tz:
                timestamp = timestamp.tz_localize(tz=tz.tzutc())
            proto_timestamp.FromJsonString(timestamp.isoformat())
            proto_value = DoubleValue(value=value)
            points.append(TimeSeriesPoint(time=proto_timestamp, value=proto_value))
        return points

    @staticmethod
    def _time_series_points_to_series(
        points: Sequence[TimeSeriesPoint], name: str = None
    ) -> pd.Series:
        """Convert a sequence of TimeSeriesPoint to a pandas Series."""
        return pd.Series(
            map(lambda x: x.value.value, points),
            index=map(lambda x: TimeSeriesApi._proto_timestamp_to_pandas_time(x.time), points),
            name=name,
        )

    @staticmethod
    def _get_time_range(
        start: Optional[pd.Timestamp],
        end: Optional[pd.Timestamp],
        include_start: bool = True,
        include_end: bool = True,
    ) -> TimeRange:
        """
        Get a TimeRange given start and end dates.

        Args:
            start:          Start timestamp.
            end:            End timestamp.
            include_start:  Whether to include the start timestamp.
            include_end:    Whether to include the end timestamp.
        """
        if start is None:
            return TimeRange()

        start_timestamp = timestamp_pb2.Timestamp()
        start_timestamp.FromJsonString(TimeSeriesApi._convert_utc(start).isoformat())

        end_timestamp = timestamp_pb2.Timestamp()
        end_timestamp.FromJsonString(TimeSeriesApi._convert_utc(end).isoformat())

        return TimeRange(
            from_time=start_timestamp,
            to_time=end_timestamp,
            exclude_from=not include_start,
            include_to=include_end,
        )

    @staticmethod
    def _proto_timestamp_to_pandas_time(
        timestamp: timestamp_pb2.Timestamp,
    ) -> pd.Timestamp:
        """Convert a protobuf Timestamp to a pandas Timestamp."""
        pts = pd.Timestamp(timestamp.ToJsonString())
        return TimeSeriesApi._convert_utc(pts)

    @staticmethod
    def _convert_utc(timestamp: pd.Timestamp) -> pd.Timestamp:
        """Return the given timestamp with the UTC time zone."""
        if timestamp.tz:
            return timestamp.tz_convert(tz.tzutc())
        return timestamp.tz_localize(tz.tzutc())
