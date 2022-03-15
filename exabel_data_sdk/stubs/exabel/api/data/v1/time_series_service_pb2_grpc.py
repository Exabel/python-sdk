"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....exabel.api.data.v1 import time_series_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2
from .....exabel.api.data.v1 import time_series_service_pb2 as exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

class TimeSeriesServiceStub(object):
    """Manages time series in the Data API.
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
        self.DeleteTimeSeries = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/DeleteTimeSeries', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.DeleteTimeSeriesRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.BatchDeleteTimeSeriesPoints = channel.unary_unary('/exabel.api.data.v1.TimeSeriesService/BatchDeleteTimeSeriesPoints', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.BatchDeleteTimeSeriesPointsRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)

class TimeSeriesServiceServicer(object):
    """Manages time series in the Data API.
    """

    def ListTimeSeries(self, request, context):
        """Lists all time series for one entity or for one signal. Only the names are returned.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTimeSeries(self, request, context):
        """Gets one time series. The known_time (of present) must be formatted
        according to RFC3339, as specified by
        https://developers.google.com/protocol-buffers/docs/proto3#json.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateTimeSeries(self, request, context):
        """Creates one time series and returns it.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateTimeSeries(self, request, context):
        """Updates one time series and returns it. The data in this request and the
        existing data will be merged together.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteTimeSeries(self, request, context):
        """Deletes one time series. The time series and all its points will be deleted.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BatchDeleteTimeSeriesPoints(self, request, context):
        """Deletes part(s) of one time series. The requested points will be deleted, but the time series
        will not. With this request, it is possible to delete all points from a time series, but not
        the time series itself.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_TimeSeriesServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.ListTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ListTimeSeriesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.ListTimeSeriesResponse.SerializeToString), 'GetTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.GetTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.GetTimeSeriesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.SerializeToString), 'CreateTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.CreateTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.CreateTimeSeriesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.SerializeToString), 'UpdateTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.UpdateTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.UpdateTimeSeriesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__messages__pb2.TimeSeries.SerializeToString), 'DeleteTimeSeries': grpc.unary_unary_rpc_method_handler(servicer.DeleteTimeSeries, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.DeleteTimeSeriesRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'BatchDeleteTimeSeriesPoints': grpc.unary_unary_rpc_method_handler(servicer.BatchDeleteTimeSeriesPoints, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.BatchDeleteTimeSeriesPointsRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.data.v1.TimeSeriesService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class TimeSeriesService(object):
    """Manages time series in the Data API.
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
    def DeleteTimeSeries(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/DeleteTimeSeries', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.DeleteTimeSeriesRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BatchDeleteTimeSeriesPoints(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.TimeSeriesService/BatchDeleteTimeSeriesPoints', exabel_dot_api_dot_data_dot_v1_dot_time__series__service__pb2.BatchDeleteTimeSeriesPointsRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)