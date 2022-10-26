from typing import List, Optional, Sequence

import pandas as pd
from dateutil import tz
from google.protobuf import timestamp_pb2
from google.protobuf.wrappers_pb2 import DoubleValue

from exabel_data_sdk.client.api.api_client.grpc.time_series_grpc_client import TimeSeriesGrpcClient
from exabel_data_sdk.client.api.bulk_import import bulk_import
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.api.resource_creation_result import (
    ResourceCreationResults,
    ResourceCreationStatus,
)
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    BatchDeleteTimeSeriesPointsRequest,
    CreateTimeSeriesRequest,
    DefaultKnownTime,
    DeleteTimeSeriesRequest,
    GetTimeSeriesRequest,
    ImportTimeSeriesRequest,
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

    def __init__(self, config: ClientConfig):
        self.client = TimeSeriesGrpcClient(config)

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
        self,
        name: str,
        start: pd.Timestamp = None,
        end: pd.Timestamp = None,
        known_time: pd.Timestamp = None,
    ) -> Optional[pd.Series]:
        """
        Get one time series.

        If start and end are not specified, all data points will be returned.
        If start or end is specified, both must be specified.

        If known_time is specified, the data will be returned as if it was requested at the given
        time (in the past). Values inserted after this known time are disregarded.
        If not set, the newest values are returned.

        If time series does not exist, None is returned.

        Args:
            name:       The resource name of the requested time series, for example
                        "entityTypes/ns.type1/entities/ns.entity1/signals/ns.signal1" or
                        "signals/ns.signal1/entityTypes/ns.type1/entities/ns.entity1".
            start:      Start of the period to get data for.
            end:        End of the period to get data for.
            known_time: The point-in-time at which to request the time series.
        """
        time_range = self._get_time_range(start, end)

        try:
            time_series = self.client.get_time_series(
                GetTimeSeriesRequest(
                    name=name,
                    view=TimeSeriesView(
                        time_range=time_range,
                        known_time=TimeSeriesApi._pandas_timestamp_to_proto(known_time),
                    ),
                ),
            )
        except RequestError as error:
            if error.error_type == ErrorType.NOT_FOUND:
                return None
            raise

        return self._time_series_points_to_series(time_series.points, time_series.name)

    def create_time_series(
        self,
        name: str,
        series: pd.Series,
        create_tag: bool = False,
        default_known_time: DefaultKnownTime = None,
    ) -> None:
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
            default_known_time:
                        Specify a default known time policy. This is used to determine
                        the Known Time for data points where a specific known time timestamp
                        has not been given. If not provided, the Exabel API defaults to the
                        current time (upload time) as the Known Time.
        """
        time_series_points = self._series_to_time_series_points(series)
        self.client.create_time_series(
            CreateTimeSeriesRequest(
                time_series=ProtoTimeSeries(name=name, points=time_series_points),
                create_tag=create_tag,
                default_known_time=default_known_time,
            ),
        )

    def upsert_time_series(
        self,
        name: str,
        series: pd.Series,
        create_tag: bool = False,
        default_known_time: DefaultKnownTime = None,
    ) -> None:
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
            default_known_time:
                        Specify a default known time policy. This is used to determine
                        the Known Time for data points where a specific known time timestamp
                        has not been given. If not provided, the Exabel API defaults to the
                        current time (upload time) as the Known Time.
        """
        self.append_time_series_data(
            name, series, default_known_time, allow_missing=True, create_tag=create_tag
        )

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

    def append_time_series_data(
        self,
        name: str,
        series: pd.Series,
        default_known_time: DefaultKnownTime = None,
        allow_missing: bool = False,
        create_tag: bool = False,
    ) -> None:
        """
        Append data to the given time series.

        If the given series contains data points that already exist, these data points will be
        overwritten.

        Args:
            name:           The resource name of the time series.
            series:         Series with data to append.
            default_known_time:
                            Specify a default known time policy. This is used to determine
                            the Known Time for data points where a specific known time timestamp
                            has not been given. If not provided, the Exabel API defaults to the
                            current time (upload time) as the Known Time.
            allow_missing:  If set to true, and the resource is not found, a new resource will be
                            created. In this situation, the "update_mask" is ignored.
            create_tag:     If allow_missing is set to true and the time series does not exist, also
                            create a tag for every entity type the signal has time series for.
        """
        self.client.update_time_series(
            UpdateTimeSeriesRequest(
                time_series=ProtoTimeSeries(
                    name=name, points=self._series_to_time_series_points(series)
                ),
                default_known_time=default_known_time,
                allow_missing=allow_missing,
                create_tag=create_tag,
            ),
        )

    def import_time_series(
        self,
        parent: str,
        series: Sequence[pd.Series],
        default_known_time: DefaultKnownTime = None,
        allow_missing: bool = False,
        create_tag: bool = False,
    ) -> None:
        """
        Import multiple time series.

        If the time series contains data points that already exist, these data points will be
        overwritten.

        Args:
            parent:         The common parent of all time series to import. May include `-` as a
                            wild card.
            series:         One or more time series to import.
            default_known_time:
                            The specification of the default known time to use for points that don't
                            explicitly have a known time set. If not set, the time of insertion is
                            used as the default known time (`current_time = true`).
            allow_missing:  If set to true, and a time series is not found, a new time series will
                            be created.
            create_tag:     Set to true to create a tag for every entity type a signal has time
                            series for. If a tag already exists, it will be updated when time series
                            are created (or deleted) regardless of the value of this flag.
        """
        self.client.import_time_series(
            ImportTimeSeriesRequest(
                parent=parent,
                time_series=[
                    ProtoTimeSeries(name=ts.name, points=self._series_to_time_series_points(ts))
                    for ts in series
                ],
                default_known_time=default_known_time,
                allow_missing=allow_missing,
                create_tag=create_tag,
            ),
        )

    def append_time_series_data_and_return(
        self,
        name: str,
        series: pd.Series,
        default_known_time: DefaultKnownTime = None,
        allow_missing: Optional[bool] = False,
        create_tag: Optional[bool] = False,
    ) -> pd.Series:
        """
        Append data to the given time series, and return the full series.

        If the given series contains data points that already exist, these data points will be
        overwritten.

        Args:
            name:           The resource name of the time series.
            series:         Series with data to append.
            default_known_time:
                            Specify a default known time policy. This is used to determine
                            the Known Time for data points where a specific known time timestamp
                            has not been given. If not provided, the Exabel API defaults to the
                            current time (upload time) as the Known Time.
            allow_missing:  If set to true, and the resource is not found, a new resource will be
                            created. In this situation, the "update_mask" is ignored.
            create_tag:     If allow_missing is set to true and the time series does not exist, also
                            create a tag for every entity type the signal has time series for.

        Returns:
            A series with all data for the given time series.
        """
        # Set empty TimeRange() in request to get back entire time series.
        time_series = self.client.update_time_series(
            UpdateTimeSeriesRequest(
                time_series=ProtoTimeSeries(
                    name=name, points=self._series_to_time_series_points(series)
                ),
                view=TimeSeriesView(time_range=TimeRange()),
                default_known_time=default_known_time,
                allow_missing=allow_missing,
                create_tag=create_tag,
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

    def bulk_upsert_time_series(
        self,
        series: Sequence[pd.Series],
        create_tag: bool = False,
        threads: int = 4,
        default_known_time: DefaultKnownTime = None,
        retries: int = 5,
        abort_threshold: Optional[float] = 0.5,
        threads_for_import: int = 4,
    ) -> ResourceCreationResults[pd.Series]:
        """Import the provided time series in batches.

        Calls import_time_series for each of the provided time series in batches, while catching
        errors and tracking progress. If any error occurs while importing a time series, the time
        series will be retried individually.

        The name attribute of each time series is taken to be the resource name. See the docstring
        of upsert_time_series regarding required format for this resource name.

        Args:
            series:         The time series to be imported.
            create_tag:     Set to true to create a tag for every entity type a signal has time
                            series for. If a tag already exists, it will be updated when time
                            series are created (or deleted) regardless of the value of this flag.
            threads:        The number of parallel upload threads to use, when falling back to
                            uploading time series individually.
            default_known_time:
                            Specify a default known time policy. This is used to determine
                            the Known Time for data points where a specific known time timestamp
                            has not been given. If not provided, the Exabel API defaults to the
                            current time (upload time) as the Known Time.
            retries:        Maximum number of retries to make for each failed request.
            abort_threshold:
                            The threshold for the proportion of failed requests that will cause the
                            upload to be aborted; if it is `None`, the upload is never aborted.
            threads_for_import:
                            The number of parallel threads to use, when using the import endpoint.
        """

        return self._bulk_import_time_series(
            series=series,
            create_tag=create_tag,
            threads_for_import=threads_for_import,
            threads_for_insert=threads,
            default_known_time=default_known_time,
            retries=retries,
            abort_threshold=abort_threshold,
        )

    def _bulk_import_time_series(
        self,
        series: Sequence[pd.Series],
        create_tag: bool = False,
        threads_for_import: int = 4,
        threads_for_insert: int = 4,
        default_known_time: DefaultKnownTime = None,
        retries: int = 5,
        abort_threshold: Optional[float] = 0.5,
    ) -> ResourceCreationResults[pd.Series]:
        """Split the given series into batches and call import_time_series for each batch.

        If a batch is not imported successfully by import_time_series,
        append_time_series_data will be called for it, while catching errors and tracking progress.

        The name attribute of each time series is taken to be the resource name.
        See the docstring of append_time_series_data regarding required format
        for this resource name.

        Args:
            series:     The time series to be imported.
            create_tag: Set to true to create a tag for every entity type a signal has time
                        series for. If a tag already exists, it will be updated when time
                        series are created (or deleted) regardless of the value of this flag.
            threads_for_import:
                        The number of parallel threads to run function using time series import API.
            threads_for_insert:
                        The number of parallel threads to run function using time series append API.
            default_known_time:
                        Specify a default known time policy. This is used to determine
                        the Known Time for data points where a specific known time timestamp
                        has not been given. If not provided, the Exabel API defaults to the
                        current time (upload time) as the Known Time.
            retries:    Maximum number of retries to run the insert function using time series
                        append API make for each failed batch in the request.
            abort_threshold:
                        The threshold for the proportion of failed requests that will cause the
                        upload to be aborted; if it is `None`, the upload is never aborted.
        """
        series_batches = self._get_batches_for_import(series)

        def import_func(ts_sequence: Sequence[pd.Series]) -> Sequence[ResourceCreationStatus]:
            self.import_time_series(
                parent="signals/-",
                series=ts_sequence,
                default_known_time=default_known_time,
                allow_missing=True,
                create_tag=create_tag,
            )
            return [ResourceCreationStatus.UPSERTED] * len(ts_sequence)

        def insert_func(ts: pd.Series) -> ResourceCreationStatus:
            self.append_time_series_data(
                name=str(ts.name),
                series=ts,
                default_known_time=default_known_time,
                allow_missing=True,
                create_tag=create_tag,
            )
            return ResourceCreationStatus.UPSERTED

        return bulk_import(
            series_batches,
            import_func,
            insert_func,
            threads_for_import,
            threads_for_insert,
            retries,
            abort_threshold,
        )

    @staticmethod
    def _get_batches_for_import(series: Sequence[pd.Series]) -> Sequence[Sequence[pd.Series]]:
        """
        Split the given sequence of series into batches of series where each batch can be sent
        in a single ImportTimeSeriesRequest.

        The goal is to create batches such that the size of the ImportTimeSeriesRequest for each
        batch does not exceed 1MB.
        """
        all_batches = []
        current_batch: List[pd.Series] = []
        current_size = 0
        one_mb = 2**20
        for s in series:
            size = TimeSeriesApi._estimate_size(s)
            if current_size + size > one_mb and current_size > 0:
                all_batches.append(current_batch)
                current_batch = [s]
                current_size = size
            else:
                current_size += size
                current_batch.append(s)
        all_batches.append(current_batch)
        return all_batches

    @staticmethod
    def _estimate_size(series: pd.Series) -> int:
        """
        Estimate how many bytes the given series will add to an ImportTimeSeriesRequest.
        """

        # 1 byte for each character in the time series name
        # + 27/19 bytes for each data point (depends on whether known-time is specified)
        # + 7 bytes overhead.
        has_known_time = isinstance(series.index, pd.MultiIndex)
        return len(str(series.name)) + (27 if has_known_time else 19) * len(series) + 7

    @staticmethod
    def _series_to_time_series_points(series: pd.Series) -> Sequence[TimeSeriesPoint]:
        """Convert a pandas Series to a sequence of TimeSeriesPoint."""
        points = []
        for index, value in series.iteritems():
            if isinstance(index, tuple):
                # (timestamp, known_time)
                if len(index) != 2:
                    raise ValueError(
                        "A time series with a MultiIndex is expected to have exactly "
                        f"two elements: (timestamp, known_time), but got {index}"
                    )
                timestamp = index[0]
                known_time = index[1]
            else:
                timestamp = index
                known_time = None
            points.append(
                TimeSeriesPoint(
                    time=TimeSeriesApi._pandas_timestamp_to_proto(timestamp),
                    value=DoubleValue(value=value),
                    known_time=TimeSeriesApi._pandas_timestamp_to_proto(known_time),
                )
            )
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
        if bool(start) != bool(end):
            raise ValueError("Either specify both 'start' and 'end' or none of them.")
        if start is None:
            return TimeRange()

        return TimeRange(
            from_time=TimeSeriesApi._pandas_timestamp_to_proto(start),
            to_time=TimeSeriesApi._pandas_timestamp_to_proto(end),
            exclude_from=not include_start,
            include_to=include_end,
        )

    @staticmethod
    def _pandas_timestamp_to_proto(
        timestamp: Optional[pd.Timestamp],
    ) -> Optional[timestamp_pb2.Timestamp]:
        """
        Convert a pandas Timestamp to a protobuf Timestamp.
        Note that second time resolution is used, and any fraction of a second is discarded.
        If the input is None, the result is None.
        """
        if timestamp is None:
            return None
        return timestamp_pb2.Timestamp(seconds=timestamp.value // 1000000000)

    @staticmethod
    def _proto_timestamp_to_pandas_time(timestamp: timestamp_pb2.Timestamp) -> pd.Timestamp:
        """Convert a protobuf Timestamp to a pandas Timestamp."""
        pts = pd.Timestamp(timestamp.ToJsonString())
        return TimeSeriesApi._convert_utc(pts)

    @staticmethod
    def _convert_utc(timestamp: pd.Timestamp) -> pd.Timestamp:
        """Return the given timestamp with the UTC time zone."""
        if timestamp.tz:
            return timestamp.tz_convert(tz.tzutc())
        return timestamp.tz_localize(tz.tzutc())
