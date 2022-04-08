"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....exabel.api.analytics.v1 import prediction_model_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__messages__pb2
from .....exabel.api.analytics.v1 import prediction_model_service_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__service__pb2

class PredictionModelServiceStub(object):
    """Service to manage prediction models.

    The only current supported operation is to request to run a given prediction model.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreatePredictionModelRun = channel.unary_unary('/exabel.api.analytics.v1.PredictionModelService/CreatePredictionModelRun', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__service__pb2.CreatePredictionModelRunRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__messages__pb2.PredictionModelRun.FromString)

class PredictionModelServiceServicer(object):
    """Service to manage prediction models.

    The only current supported operation is to request to run a given prediction model.
    """

    def CreatePredictionModelRun(self, request, context):
        """Create a model run.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_PredictionModelServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'CreatePredictionModelRun': grpc.unary_unary_rpc_method_handler(servicer.CreatePredictionModelRun, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__service__pb2.CreatePredictionModelRunRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__messages__pb2.PredictionModelRun.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.analytics.v1.PredictionModelService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class PredictionModelService(object):
    """Service to manage prediction models.

    The only current supported operation is to request to run a given prediction model.
    """

    @staticmethod
    def CreatePredictionModelRun(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.PredictionModelService/CreatePredictionModelRun', exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__service__pb2.CreatePredictionModelRunRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__messages__pb2.PredictionModelRun.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)