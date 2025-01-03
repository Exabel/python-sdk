from typing import Iterator, Optional, Sequence, Union

import numpy as np
import pandas as pd
from dateutil import tz
from google.protobuf import timestamp_pb2
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
from google.rpc.code_pb2 import Code as CodeProto
from grpc import StatusCode

from exabel_data_sdk.client.api.api_client.grpc.time_series_grpc_client import TimeSeriesGrpcClient
from exabel_data_sdk.client.api.bulk_import import bulk_import
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.api.data_classes.time_series import TimeSeries
from exabel_data_sdk.client.api.error_handler import grpc_status_to_error_type
from exabel_data_sdk.client.api.pageable_resource import PageableResourceMixin
from exabel_data_sdk.client.api.resource_creation_result import (
    ResourceCreationResult,
    ResourceCreationResults,
    ResourceCreationStatus,
)
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.services.csv_loading_constants import (
    DEFAULT_ABORT_THRESHOLD,
    DEFAULT_NUMBER_OF_RETRIES,
    DEFAULT_NUMBER_OF_THREADS_FOR_IMPORT,
)
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    BatchDeleteTimeSeriesPointsRequest,
    CreateTimeSeriesRequest,
    DefaultKnownTime,
    DeleteTimeSeriesRequest,
    GetTimeSeriesRequest,
    ImportTimeSeriesRequest,
    InsertOptions,
    ListTimeSeriesRequest,
    TimeSeriesView,
    UpdateOptions,
    UpdateTimeSeriesRequest,
)
from exabel_data_sdk.stubs.exabel.api.time.time_range_pb2 import TimeRange
from exabel_data_sdk.util.deprecate_arguments import deprecate_arguments


class TimeSeriesApi(PageableResourceMixin):
    """
    API class for time series CRUD operations.
    """

    def __init__(self, config: ClientConfig):
        self.client = TimeSeriesGrpcClient(config)

    def get_signal_time_series(
        self, signal: str, page_size: int = 1000, page_token: Optional[str] = None
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

    def get_signal_time_series_iterator(self, signal: str) -> Iterator[str]:
        """
        Return an iterator with all the resource names of all time series for one signal.
        """
        return self._get_resource_iterator(self.get_signal_time_series, signal=signal)

    def get_entity_time_series(
        self, entity: str, page_size: int = 1000, page_token: Optional[str] = None
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

    def get_entity_time_series_iterator(self, entity: str) -> Iterator[str]:
        """
        Return an iterator with all the resource names of all time series for one entity.
        """
        return self._get_resource_iterator(self.get_entity_time_series, entity=entity)

    def get_time_series(
        self,
        name: str,
        start: Optional[pd.Timestamp] = None,
        end: Optional[pd.Timestamp] = None,
        known_time: Optional[pd.Timestamp] = None,
        include_metadata: bool = False,
    ) -> Optional[Union[pd.Series, TimeSeries]]:
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
            include_metadata:
                        Whether to include the metadata of the time series in the response.
                        Returns a TimeSeries object if set to True, otherwise a pandas Series.
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

        result = TimeSeries.from_proto(time_series)
        if not include_metadata:
            return (
                result.series.droplevel(level=1)
                if result.series.index.nlevels > 1
                else result.series
            )
        return result

    @deprecate_arguments(create_tag=None)
    def create_time_series(
        self,
        name: str,
        series: Union[pd.Series, TimeSeries],
        create_tag: Optional[bool] = None,  # pylint: disable=unused-argument
        default_known_time: Optional[DefaultKnownTime] = None,
        should_optimise: Optional[bool] = None,
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
            create_tag: Deprecated.
            default_known_time:
                        Specify a default known time policy. This is used to determine
                        the Known Time for data points where a specific known time timestamp
                        has not been given. If not provided, the Exabel API defaults to the
                        current time (upload time) as the Known Time.
            should_optimise:
                        Whether time series storage optimisation should be enabled or not. If not
                        set, optimisation is at the discretion of the server.
        """
        series = self._handle_time_series(name, series)

        self.client.create_time_series(
            CreateTimeSeriesRequest(
                time_series=series.to_proto(),
                default_known_time=default_known_time,
                insert_options=InsertOptions(should_optimise=should_optimise),
            ),
        )

    @deprecate_arguments(create_tag=None)
    def upsert_time_series(
        self,
        name: str,
        series: pd.Series,
        create_tag: Optional[bool] = None,  # pylint: disable=unused-argument
        default_known_time: Optional[DefaultKnownTime] = None,
        should_optimise: Optional[bool] = None,
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
            create_tag: Deprecated.
            default_known_time:
                        Specify a default known time policy. This is used to determine
                        the Known Time for data points where a specific known time timestamp
                        has not been given. If not provided, the Exabel API defaults to the
                        current time (upload time) as the Known Time.
            should_optimise:
                        Whether time series storage optimisation should be enabled or not. If not
                        set, optimisation is at the discretion of the server.
        """
        self.append_time_series_data(
            name,
            series,
            default_known_time,
            allow_missing=True,
            should_optimise=should_optimise,
        )

    @deprecate_arguments(create_tag=None)
    def append_time_series_data(
        self,
        name: str,
        series: Union[pd.Series, TimeSeries],
        default_known_time: Optional[DefaultKnownTime] = None,
        allow_missing: bool = False,
        create_tag: bool = False,  # pylint: disable=unused-argument
        should_optimise: Optional[bool] = None,
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
            create_tag:     Deprecated.
            should_optimise:
                        Whether time series storage optimisation should be enabled or not. If not
                        set, optimisation is at the discretion of the server.
        """
        series = self._handle_time_series(name, series)

        self.client.update_time_series(
            UpdateTimeSeriesRequest(
                time_series=series.to_proto(),
                insert_options=InsertOptions(
                    default_known_time=default_known_time,
                    should_optimise=should_optimise,
                ),
                update_options=UpdateOptions(
                    allow_missing=allow_missing,
                ),
            ),
        )

    @deprecate_arguments(create_tag=None)
    def import_time_series(
        self,
        parent: str,
        series: Sequence[Union[pd.Series, TimeSeries]],
        default_known_time: Optional[DefaultKnownTime] = None,
        allow_missing: bool = False,
        create_tag: Optional[bool] = None,  # pylint: disable=unused-argument
        status_in_response: bool = False,
        replace_existing_time_series: bool = False,
        replace_existing_data_points: bool = False,
        should_optimise: Optional[bool] = None,
    ) -> Optional[Sequence[ResourceCreationResult]]:
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
            create_tag:     Deprecated.
            status_in_response:
                            If set to true, the status of each time series will be reported as a
                            ResourceCreationResult.
                            If set to false, a failure for one time series will fail the entire
                            request, and a sample of the failures will be reported in the exception.
            replace_existing_time_series:
                            Set to true to first delete all data from existing time series. This
                            means that all historical and point-in-time data for the time series
                            will be destroyed and replaced with the data in this call.
                            Use with care! For instance: If this flag is set, and an import job
                            splits one time series over multiple calls, only the data in the last
                            call will be kept. Only one of replace_existing_time_series or
                            replace_existing_data_points can be set to true.
            replace_existing_data_points:
                            Set to true to remove all existing known_time data point versions of the
                            inserted time series points. Data points at times not present in the
                            request will be left untouched. Only one of replace_existing_data_points
                            or replace_existing_time_series can be set to true.
            should_optimise:
                            Whether time series storage optimisation should be enabled or not. If
                            not set, optimisation is at the discretion of the server.
        Returns:
            If status_in_response is set to true, a list of ResourceCreationResult will be returned.
            Otherwise, None is returned.
        """
        if replace_existing_time_series and replace_existing_data_points:
            raise ValueError(
                "Only one of replace_existing_time_series or replace_existing_data_points can be "
                "true"
            )
        update_options = UpdateOptions(allow_missing=allow_missing)
        if replace_existing_time_series:
            update_options.replace_existing_time_series = replace_existing_time_series
        elif replace_existing_data_points:
            update_options.replace_existing_data_points = replace_existing_data_points
        request = ImportTimeSeriesRequest(
            parent=parent,
            time_series=[
                TimeSeries(ts).to_proto() if isinstance(ts, pd.Series) else ts.to_proto()
                for ts in series
            ],
            status_in_response=status_in_response,
            insert_options=InsertOptions(
                default_known_time=default_known_time,
                should_optimise=should_optimise,
            ),
            update_options=update_options,
        )
        response = self.client.import_time_series(request)

        if status_in_response:
            return self._handle_time_series_response(response.responses, series)

        return None

    @deprecate_arguments(create_tag=None)
    def append_time_series_data_and_return(
        self,
        name: str,
        series: Union[pd.Series, TimeSeries],
        default_known_time: Optional[DefaultKnownTime] = None,
        allow_missing: Optional[bool] = False,
        create_tag: Optional[bool] = None,  # pylint: disable=unused-argument
        include_metadata: Optional[bool] = False,
        should_optimise: Optional[bool] = None,
    ) -> Union[pd.Series, TimeSeries]:
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
            create_tag:     Deprecated.
            include_metadata:
                            Whether to include the metadata of the time series in the response.
                            Returns a TimeSeries object if set to True, otherwise a pandas Series.
            should_optimise:
                        Whether time series storage optimisation should be enabled or not. If not
                        set, optimisation is at the discretion of the server.

        Returns:
            A series with all data for the given time series.
        """
        series = self._handle_time_series(name, series)

        # Set empty TimeRange() in request to get back entire time series.
        time_series = self.client.update_time_series(
            UpdateTimeSeriesRequest(
                time_series=series.to_proto(),
                view=TimeSeriesView(time_range=TimeRange()),
                insert_options=InsertOptions(
                    default_known_time=default_known_time,
                    should_optimise=should_optimise,
                ),
                update_options=UpdateOptions(
                    allow_missing=allow_missing,
                ),
            ),
        )
        if include_metadata:
            return TimeSeries.from_proto(time_series)
        return TimeSeries.from_proto(time_series).series

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

    @deprecate_arguments(threads_for_import=None, create_tag=None)
    def bulk_upsert_time_series(
        self,
        series: Sequence[Union[pd.Series, TimeSeries]],
        create_tag: Optional[bool] = None,  # pylint: disable=unused-argument
        threads: int = DEFAULT_NUMBER_OF_THREADS_FOR_IMPORT,
        default_known_time: Optional[DefaultKnownTime] = None,
        replace_existing_time_series: bool = False,
        replace_existing_data_points: bool = False,
        should_optimise: Optional[bool] = None,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
        abort_threshold: Optional[float] = DEFAULT_ABORT_THRESHOLD,
        # Deprecated arguments
        threads_for_import: int = 4,  # pylint: disable=unused-argument
    ) -> ResourceCreationResults[pd.Series]:
        """Import the provided time series in batches.

        Calls import_time_series for each of the provided time series in batches, while catching
        errors and tracking progress. If any error occurs while importing a time series, the time
        series will be retried individually.

        The name attribute of each time series is taken to be the resource name. See the docstring
        of upsert_time_series regarding required format for this resource name.

        Args:
            series:         The time series to be imported.
            create_tag:     Deprecated.
            threads:        The number of parallel upload threads to use, when falling back to
                            uploading time series individually.
            default_known_time:
                            Specify a default known time policy. This is used to determine
                            the Known Time for data points where a specific known time timestamp
                            has not been given. If not provided, the Exabel API defaults to the
                            current time (upload time) as the Known Time.
            replace_existing_time_series:
                            Set to true to first delete all data from existing time series. This
                            means that all historical and point-in-time data for the time series
                            will be destroyed and replaced with the data in this call.
                            Use with care! For instance: If this flag is set, and an import job
                            splits one time series over multiple calls, only the data in the last
                            call will be kept.
            replace_existing_data_points:
                            Set to true to remove all existing known_time data point versions of the
                            inserted time series points. Data points at times not present in the
                            request will be left untouched. Only one of replace_existing_data_points
                            or replace_existing_time_series can be set to true.
            should_optimise:
                            Whether time series storage optimisation should be enabled or not. If
                            not set, optimisation is at the discretion of the server.
            retries:        Maximum number of retries to make for each failed request.
            abort_threshold:
                            The threshold for the proportion of failed requests that will cause the
                            upload to be aborted; if it is `None`, the upload is never aborted.

        Returns:
            ResourceCreationResults containing the status for each time series that was imported.
        """

        def import_func(
            ts_sequence: Sequence[Union[pd.Series, TimeSeries]]
        ) -> Sequence[ResourceCreationResult]:
            result = self.import_time_series(
                parent="signals/-",
                series=ts_sequence,
                default_known_time=default_known_time,
                allow_missing=True,
                status_in_response=True,
                replace_existing_time_series=replace_existing_time_series,
                replace_existing_data_points=replace_existing_data_points,
                should_optimise=should_optimise,
            )
            assert result is not None
            return result

        return bulk_import(
            series,
            import_func,
            threads,
            retries,
            abort_threshold,
        )

    def delete_time_series_points(
        self,
        series: Sequence[pd.Series],
    ) -> Optional[Sequence[ResourceCreationResult]]:
        """
        Delete data points from time series. A data point that is deleted will be removed from the
        time series at the given date and known_time if it exists with a value or NaN.

        Args:
            series: The data points to be deleted. The series must have date and known-time. Values
                    are ignored.
        """
        response = self.client.batch_delete_time_series_points(
            BatchDeleteTimeSeriesPointsRequest(
                parent="signals/-",
                time_series=[TimeSeries(ts).to_proto() for ts in series],
                status_in_response=True,
            )
        )

        return self._handle_time_series_response(response.responses, series)

    def batch_delete_time_series_points(
        self,
        series: Sequence[pd.Series],
        threads: int = DEFAULT_NUMBER_OF_THREADS_FOR_IMPORT,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
        abort_threshold: Optional[float] = DEFAULT_ABORT_THRESHOLD,
    ) -> ResourceCreationResults[pd.Series]:
        """Delete the provided time series data points in batches.

        Calls batch_delete_time_series_points for each of the provided time series in batches,
        while catching errors and tracking progress. If any error occurs while deleting a time
        series point, the time series will be retried individually.

        The name attribute of each time series is taken to be the resource name.

        Args:
            series:         The time series to be imported.
            threads:        The number of parallel upload threads to use, when falling back to
                            uploading time series individually.
            retries:        Maximum number of retries to make for each failed request.
            abort_threshold:
                            The threshold for the proportion of failed requests that will cause the
                            upload to be aborted; if it is `None`, the upload is never aborted.

        Returns:
            ResourceCreationResults containing the status for each time series that was deleted.
        """

        def import_func(ts_sequence: Sequence[pd.Series]) -> Sequence[ResourceCreationResult]:
            result = self.delete_time_series_points(
                series=ts_sequence,
            )
            assert result is not None
            return result

        return bulk_import(
            series,
            import_func,
            threads,
            retries,
            abort_threshold,
        )

    @staticmethod
    def _datetime_index(nanoseconds: Sequence[int]) -> pd.DatetimeIndex:
        return pd.DatetimeIndex(np.array(nanoseconds).astype("datetime64[ns]"), tz=tz.tzutc())

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
    def _handle_time_series_response(
        responses: RepeatedCompositeFieldContainer, series: Sequence[pd.Series]
    ) -> Sequence[ResourceCreationResult]:
        time_series_results = []
        for single_time_series_response, single_time_series in zip(responses, series):
            # The code (integer) given in the response corresponds to google.rpc.Code enum.
            status_code = StatusCode[CodeProto.Name(single_time_series_response.status.code)]
            if status_code == StatusCode.OK:
                # We treat a delete of data point(s) as an update of the time series.
                time_series_results.append(
                    ResourceCreationResult(ResourceCreationStatus.UPSERTED, single_time_series)
                )
            else:
                error = RequestError(
                    error_type=grpc_status_to_error_type(status_code),
                    message=single_time_series_response.status.message,
                )
                time_series_results.append(
                    ResourceCreationResult(ResourceCreationStatus.FAILED, single_time_series, error)
                )

        return time_series_results

    @staticmethod
    def _handle_time_series(name: str, series: Union[pd.Series, TimeSeries]) -> TimeSeries:
        """
        Helper function to convert to TimeSeries if necessary,
        and set the name equal to the given name.
        """
        if isinstance(series, pd.Series):
            series = TimeSeries(series)
            series.name = name
        if isinstance(series, TimeSeries) and series.name != name:
            series = TimeSeries(series.series, series.units)
            series.name = name
        return series
