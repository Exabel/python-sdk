"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....exabel.api.analytics.v1 import model_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_model__messages__pb2
from .....exabel.api.analytics.v1 import model_service_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_model__service__pb2

class ModelServiceStub(object):
    """Service to manage models.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateModelRun = channel.unary_unary('/exabel.api.analytics.v1.ModelService/CreateModelRun', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_model__service__pb2.CreateModelRunRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_model__messages__pb2.ModelRun.FromString)

class ModelServiceServicer(object):
    """Service to manage models.
    """

    def CreateModelRun(self, request, context):
        """Create a model run.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_ModelServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'CreateModelRun': grpc.unary_unary_rpc_method_handler(servicer.CreateModelRun, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_model__service__pb2.CreateModelRunRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_model__messages__pb2.ModelRun.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.analytics.v1.ModelService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class ModelService(object):
    """Service to manage models.
    """

    @staticmethod
    def CreateModelRun(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.ModelService/CreateModelRun', exabel_dot_api_dot_analytics_dot_v1_dot_model__service__pb2.CreateModelRunRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_model__messages__pb2.ModelRun.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)