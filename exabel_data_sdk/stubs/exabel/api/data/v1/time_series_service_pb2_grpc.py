"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....exabel.api.data.v1 import time_series_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2
from .....exabel.api.data.v1 import time_series_service_pb2 as exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

class TimeSeriesServiceStub(object):
    """Service for managing time series. See the User Guide for more information about time series.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListTimeSeries = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/ListTimeSeries', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ListTimeSeriesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ListTimeSeriesResponse.FromString)
        self.GetTimeSeries = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/GetTimeSeries', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.GetTimeSeriesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.FromString)
        self.CreateTimeSeries = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/CreateTimeSeries', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.CreateTimeSeriesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.FromString)
        self.UpdateTimeSeries = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/UpdateTimeSeries', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.UpdateTimeSeriesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.FromString)
        self.ImportTimeSeries = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/ImportTimeSeries', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ImportTimeSeriesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ImportTimeSeriesResponse.FromString)
        self.DeleteTimeSeries = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/DeleteTimeSeries', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.DeleteTimeSeriesRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.BatchDeleteTimeSeriesPoints = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/BatchDeleteTimeSeriesPoints', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.BatchDeleteTimeSeriesPointsRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)

class TimeSeriesServiceServicer(object):
    """Service for managing time series. See the User Guide for more information about time series.
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

        The optional `view` argument lets you request for time series data points to be returned
        within a date range. If this is not set, no values are returned.
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
        as the `signalId` path parameter. (Signal IDs are part of each time series' resource name,
        so your time series will still be assigned to their corresponding signals.)

        *Note*: Exabel only supports processing time series with daily or lower resolution. Timestamps
        must be RFC 3339 timestamps, normalised to **midnight UTC**, e.g. `2020-01-01T00:00:00Z`.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteTimeSeries(self, request, context):
        """Deletes one time series.

        This will delete the time series and ***all*** its data points.

        If you have a "coverage" tag from the Create, Update or Import time series endpoints (by
        setting `create_tag` to `true`), this will remove this entity from that tag.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BatchDeleteTimeSeriesPoints(self, request, context):
        """Deletes part(s) of one time series.

        Delete data points within a time series by specifying time ranges. This does not delete the
        time series.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_TimeSeriesServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.ListTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ListTimeSeriesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ListTimeSeriesResponse.SerializeToString), 'GetTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.GetTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.GetTimeSeriesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.SerializeToString), 'CreateTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.CreateTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.CreateTimeSeriesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.SerializeToString), 'UpdateTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.UpdateTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.UpdateTimeSeriesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.SerializeToString), 'ImportTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.ImportTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ImportTimeSeriesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ImportTimeSeriesResponse.SerializeToString), 'DeleteTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.DeleteTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.DeleteTimeSeriesRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'BatchDeleteTimeSeriesPoints': grpc.unary_unary_rpc_method_handler(servicer.BatchDeleteTimeSeriesPoints, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.BatchDeleteTimeSeriesPointsRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.data.v1.TimeSeriesService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class TimeSeriesService(object):
    """Service for managing time series. See the User Guide for more information about time series.
    """

    @staticmethod
    def ListTimeSeries(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/ListTimeSeries', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ListTimeSeriesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ListTimeSeriesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTimeSeries(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/GetTimeSeries', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.GetTimeSeriesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateTimeSeries(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/CreateTimeSeries', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.CreateTimeSeriesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateTimeSeries(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/UpdateTimeSeries', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.UpdateTimeSeriesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ImportTimeSeries(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/ImportTimeSeries', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ImportTimeSeriesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ImportTimeSeriesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteTimeSeries(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/DeleteTimeSeries', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.DeleteTimeSeriesRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BatchDeleteTimeSeriesPoints(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/BatchDeleteTimeSeriesPoints', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.BatchDeleteTimeSeriesPointsRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)