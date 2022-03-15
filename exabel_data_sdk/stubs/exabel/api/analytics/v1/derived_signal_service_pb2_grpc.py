"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....exabel.api.analytics.v1 import derived_signal_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2
from .....exabel.api.analytics.v1 import derived_signal_service_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

class DerivedSignalServiceStub(object):
    """Service to manage derived signals.

    A derived signal is a DSL expression with a unique label. The label must be unique to the
    customer.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetDerivedSignal = channel.unary_unary('/exabel.api.analytics.v1.DerivedSignalService/GetDerivedSignal', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.GetDerivedSignalRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.FromString)
        self.CreateDerivedSignal = channel.unary_unary('/exabel.api.analytics.v1.DerivedSignalService/CreateDerivedSignal', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.CreateDerivedSignalRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.FromString)
        self.UpdateDerivedSignal = channel.unary_unary('/exabel.api.analytics.v1.DerivedSignalService/UpdateDerivedSignal', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.UpdateDerivedSignalRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.FromString)
        self.DeleteDerivedSignal = channel.unary_unary('/exabel.api.analytics.v1.DerivedSignalService/DeleteDerivedSignal', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.DeleteDerivedSignalRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)

class DerivedSignalServiceServicer(object):
    """Service to manage derived signals.

    A derived signal is a DSL expression with a unique label. The label must be unique to the
    customer.
    """

    def GetDerivedSignal(self, request, context):
        """Get a derived signal.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateDerivedSignal(self, request, context):
        """Create a derived signal.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateDerivedSignal(self, request, context):
        """Update a derived signal.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteDerivedSignal(self, request, context):
        """Delete a derived signal.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_DerivedSignalServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'GetDerivedSignal': grpc.unary_unary_rpc_method_handler(servicer.GetDerivedSignal, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.GetDerivedSignalRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.SerializeToString), 'CreateDerivedSignal': grpc.unary_unary_rpc_method_handler(servicer.CreateDerivedSignal, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.CreateDerivedSignalRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.SerializeToString), 'UpdateDerivedSignal': grpc.unary_unary_rpc_method_handler(servicer.UpdateDerivedSignal, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.UpdateDerivedSignalRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.SerializeToString), 'DeleteDerivedSignal': grpc.unary_unary_rpc_method_handler(servicer.DeleteDerivedSignal, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.DeleteDerivedSignalRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.analytics.v1.DerivedSignalService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class DerivedSignalService(object):
    """Service to manage derived signals.

    A derived signal is a DSL expression with a unique label. The label must be unique to the
    customer.
    """

    @staticmethod
    def GetDerivedSignal(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.DerivedSignalService/GetDerivedSignal', exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.GetDerivedSignalRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateDerivedSignal(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.DerivedSignalService/CreateDerivedSignal', exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.CreateDerivedSignalRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateDerivedSignal(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.DerivedSignalService/UpdateDerivedSignal', exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.UpdateDerivedSignalRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteDerivedSignal(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.DerivedSignalService/DeleteDerivedSignal', exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.DeleteDerivedSignalRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)