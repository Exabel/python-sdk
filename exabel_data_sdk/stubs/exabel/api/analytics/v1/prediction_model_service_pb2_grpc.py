"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from .....exabel.api.analytics.v1 import prediction_model_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__messages__pb2
from .....exabel.api.analytics.v1 import prediction_model_service_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__service__pb2
GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in exabel/api/analytics/v1/prediction_model_service_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class PredictionModelServiceStub(object):
    """Service to manage prediction models.

    The only current supported operation is to request to run a given prediction model.

    Requests to the PredictionModelService are executed in the context of the customer's service
    account (SA). The SA is a special user that is a member of the customer user group, giving
    it access to all folders that are shared with this user group, but not to private folders.
    Hence, only prediction models that are in folders shared to the SA, via the customer user group,
    will be accessible via the PredictionModelService.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreatePredictionModelRun = channel.unary_unary('/exabel.api.analytics.v1.PredictionModelService/CreatePredictionModelRun', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__service__pb2.CreatePredictionModelRunRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__messages__pb2.PredictionModelRun.FromString, _registered_method=True)

class PredictionModelServiceServicer(object):
    """Service to manage prediction models.

    The only current supported operation is to request to run a given prediction model.

    Requests to the PredictionModelService are executed in the context of the customer's service
    account (SA). The SA is a special user that is a member of the customer user group, giving
    it access to all folders that are shared with this user group, but not to private folders.
    Hence, only prediction models that are in folders shared to the SA, via the customer user group,
    will be accessible via the PredictionModelService.
    """

    def CreatePredictionModelRun(self, request, context):
        """Runs a prediction model.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_PredictionModelServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'CreatePredictionModelRun': grpc.unary_unary_rpc_method_handler(servicer.CreatePredictionModelRun, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__service__pb2.CreatePredictionModelRunRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__messages__pb2.PredictionModelRun.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.analytics.v1.PredictionModelService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('exabel.api.analytics.v1.PredictionModelService', rpc_method_handlers)

class PredictionModelService(object):
    """Service to manage prediction models.

    The only current supported operation is to request to run a given prediction model.

    Requests to the PredictionModelService are executed in the context of the customer's service
    account (SA). The SA is a special user that is a member of the customer user group, giving
    it access to all folders that are shared with this user group, but not to private folders.
    Hence, only prediction models that are in folders shared to the SA, via the customer user group,
    will be accessible via the PredictionModelService.
    """

    @staticmethod
    def CreatePredictionModelRun(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.PredictionModelService/CreatePredictionModelRun', exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__service__pb2.CreatePredictionModelRunRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_prediction__model__messages__pb2.PredictionModelRun.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)