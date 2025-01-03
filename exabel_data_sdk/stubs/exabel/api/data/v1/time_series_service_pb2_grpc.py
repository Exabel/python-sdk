"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from .....exabel.api.data.v1 import time_series_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2
from .....exabel.api.data.v1 import time_series_service_pb2 as exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in exabel/api/data/v1/time_series_service_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class TimeSeriesServiceStub(object):
    """Service for managing time series. See the User Guide for more information about time series:
    https://help.exabel.com/docs/time-series
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListTimeSeries = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/ListTimeSeries', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ListTimeSeriesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ListTimeSeriesResponse.FromString, _registered_method=True)
        self.GetTimeSeries = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/GetTimeSeries', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.GetTimeSeriesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.FromString, _registered_method=True)
        self.CreateTimeSeries = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/CreateTimeSeries', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.CreateTimeSeriesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.FromString, _registered_method=True)
        self.UpdateTimeSeries = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/UpdateTimeSeries', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.UpdateTimeSeriesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.FromString, _registered_method=True)
        self.ImportTimeSeries = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/ImportTimeSeries', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ImportTimeSeriesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ImportTimeSeriesResponse.FromString, _registered_method=True)
        self.BatchDeleteTimeSeriesPoints = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/BatchDeleteTimeSeriesPoints', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.BatchDeleteTimeSeriesPointsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.BatchDeleteTimeSeriesPointsResponse.FromString, _registered_method=True)
        self.DeleteTimeSeries = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/DeleteTimeSeries', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.DeleteTimeSeriesRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, _registered_method=True)

class TimeSeriesServiceServicer(object):
    """Service for managing time series. See the User Guide for more information about time series:
    https://help.exabel.com/docs/time-series
    """

    def ListTimeSeries(self, request, context):
        """Lists time series.

        Lists all time series for one entity or for one signal. Only the names are returned.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTimeSeries(self, request, context):
        """Gets one time series.

        Use this method to get time series data points.

        *Note*: Exabel only supports processing time series with daily or lower resolution. Timestamps
        must be RFC 3339 timestamps, normalised to **midnight UTC**, e.g. `2020-01-01T00:00:00Z`.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateTimeSeries(self, request, context):
        """Creates one time series.

        *Note*: Exabel only supports processing time series with daily or lower resolution. Timestamps
        must be RFC 3339 timestamps, normalised to **midnight UTC**, e.g. `2020-01-01T00:00:00Z`.

        The default `known_time` for a data point is insertion time, i.e. same as setting
        `current_time` to `true`. To override the default behaviour, set one of the
        `default_known_time` fields.

        The optional `view` argument lets you request for time series data points to be returned
        within a date range. If this is not set, no values are returned.

        It is also possible to create a time series by calling `UpdateTimeSeries`
        with `allow_missing` set to `true`.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateTimeSeries(self, request, context):
        """Updates one time series.

        This can also be used to create a time series by setting `allow_missing` to `true`.

        Updating a time series will usually create a new version of the time series. However, by
        explicitly setting a known time, any version may be changed or updated. If a value already
        exists with exactly the same timestamp *and* known time, it will be updated. Otherwise a new
        point will be created.

        If a timestamp that is previously known is not included, its value is *not* deleted, even
        though it is within the range of this update. The old value will simply continue to exist at
        the new version. Data points without values are cleared from this version, meaning that the
        old value will continue to exist up until the new version, then cease to exist.

        Time series storage is optimized by discarding values which haven't changed from the previous
        versions. Note that this optimization may cause surprising behavior when updating older
        versions. When older versions are updated, it is therefore recommended to perform a full
        backload from this version on.

        The default `known_time` for a data point is insertion time, i.e. same as setting
        `current_time` to `true`. To override the default behaviour, set one of the
        `default_known_time` fields.

        *Note*: Exabel only supports processing time series with daily or lower resolution. Timestamps
        must be RFC 3339 timestamps, normalised to **midnight UTC**, e.g. `2020-01-01T00:00:00Z`.

        The optional `view` argument lets you request for time series data points to be returned
        within a date range. If this is not set, no values are returned.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ImportTimeSeries(self, request, context):
        """Creates or update multiple time series.

        Import multiple time series in bulk, by creating new time series or updating existing time
        series.

        If you would like to import multiple time series belonging to different signals, specify `-`
        as the signal identifier. (Signal identifiers are part of each time series' resource name, so
        your time series will still be assigned to their corresponding signals.)

        The default `known_time` for a data point is insertion time, i.e. same as setting
        `current_time` to `true`. To override the default behaviour, set one of the
        `default_known_time` fields.

        *Note*: Exabel only supports processing time series with daily or lower resolution. Timestamps
        must be RFC 3339 timestamps, normalised to **midnight UTC**, e.g. `2020-01-01T00:00:00Z`.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BatchDeleteTimeSeriesPoints(self, request, context):
        """Deletes specific time series points for multiple time series.

        Delete multiple time series points in bulk, by erasing the points from the storage. Use with
        care: Time series storage is optimized by discarding values which haven't changed from the
        previous versions. Note that this optimization may cause surprising behavior when updating
        older versions. When older versions are deleted, it is therefore recommended to perform a full
        backload from this version on.

        Deleting a value is both different from inserting NaN values, or inserting _no_ value.

        If you would like to delete multiple time series points belonging to different signals,
        specify `-` as the signal identifier. (Signal identifiers are part of each time series'
        resource name, so your time series will still be assigned to their corresponding signals.)

        *Note*: Exabel only supports processing time series with daily or lower resolution. Timestamps
        must be RFC 3339 timestamps, normalised to **midnight UTC**, e.g. `2020-01-01T00:00:00Z`.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteTimeSeries(self, request, context):
        """Deletes one time series.

        This will delete the time series and ***all*** its data points.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_TimeSeriesServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.ListTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ListTimeSeriesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ListTimeSeriesResponse.SerializeToString), 'GetTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.GetTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.GetTimeSeriesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.SerializeToString), 'CreateTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.CreateTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.CreateTimeSeriesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.SerializeToString), 'UpdateTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.UpdateTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.UpdateTimeSeriesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.SerializeToString), 'ImportTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.ImportTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ImportTimeSeriesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ImportTimeSeriesResponse.SerializeToString), 'BatchDeleteTimeSeriesPoints': grpc.unary_unary_rpc_method_handler(servicer.BatchDeleteTimeSeriesPoints, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.BatchDeleteTimeSeriesPointsRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.BatchDeleteTimeSeriesPointsResponse.SerializeToString), 'DeleteTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.DeleteTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.DeleteTimeSeriesRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.data.v1.TimeSeriesService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('exabel.api.data.v1.TimeSeriesService', rpc_method_handlers)

class TimeSeriesService(object):
    """Service for managing time series. See the User Guide for more information about time series:
    https://help.exabel.com/docs/time-series
    """

    @staticmethod
    def ListTimeSeries(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/ListTimeSeries', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ListTimeSeriesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ListTimeSeriesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GetTimeSeries(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/GetTimeSeries', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.GetTimeSeriesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def CreateTimeSeries(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/CreateTimeSeries', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.CreateTimeSeriesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def UpdateTimeSeries(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/UpdateTimeSeries', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.UpdateTimeSeriesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def ImportTimeSeries(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/ImportTimeSeries', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ImportTimeSeriesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ImportTimeSeriesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def BatchDeleteTimeSeriesPoints(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/BatchDeleteTimeSeriesPoints', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.BatchDeleteTimeSeriesPointsRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.BatchDeleteTimeSeriesPointsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def DeleteTimeSeries(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/DeleteTimeSeries', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.DeleteTimeSeriesRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)