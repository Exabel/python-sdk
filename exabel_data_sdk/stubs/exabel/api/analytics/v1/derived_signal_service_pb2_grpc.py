"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from .....exabel.api.analytics.v1 import derived_signal_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2
from .....exabel.api.analytics.v1 import derived_signal_service_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2
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
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in exabel/api/analytics/v1/derived_signal_service_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class DerivedSignalServiceStub(object):
    """Service to manage derived signals.

    A derived signal is a DSL expression with a unique label. The label must be unique to the
    customer.

    Derived signals are stored in Library folders and shared across users through folder sharing.

    Requests to the DerivedSignalService are executed in the context of the customer's service
    account (SA). The SA is a special user that is a member of the customer user group, giving
    it access to all folders that are shared with this user group, but not to private folders.
    Hence, only derived signals that are in folders shared to the SA, via the customer user group,
    will be accessible via the DerivedSignalService.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetDerivedSignal = channel.unary_unary('/exabel.api.analytics.v1.DerivedSignalService/GetDerivedSignal', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.GetDerivedSignalRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.FromString, _registered_method=True)
        self.CreateDerivedSignal = channel.unary_unary('/exabel.api.analytics.v1.DerivedSignalService/CreateDerivedSignal', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.CreateDerivedSignalRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.FromString, _registered_method=True)
        self.UpdateDerivedSignal = channel.unary_unary('/exabel.api.analytics.v1.DerivedSignalService/UpdateDerivedSignal', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.UpdateDerivedSignalRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.FromString, _registered_method=True)
        self.DeleteDerivedSignal = channel.unary_unary('/exabel.api.analytics.v1.DerivedSignalService/DeleteDerivedSignal', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.DeleteDerivedSignalRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, _registered_method=True)

class DerivedSignalServiceServicer(object):
    """Service to manage derived signals.

    A derived signal is a DSL expression with a unique label. The label must be unique to the
    customer.

    Derived signals are stored in Library folders and shared across users through folder sharing.

    Requests to the DerivedSignalService are executed in the context of the customer's service
    account (SA). The SA is a special user that is a member of the customer user group, giving
    it access to all folders that are shared with this user group, but not to private folders.
    Hence, only derived signals that are in folders shared to the SA, via the customer user group,
    will be accessible via the DerivedSignalService.
    """

    def GetDerivedSignal(self, request, context):
        """Gets a derived signal.

        The derived signal must be in a folder that is shared to your service account (which is always
        in your main customer user group).
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateDerivedSignal(self, request, context):
        """Creates a derived signal.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateDerivedSignal(self, request, context):
        """Updates a derived signal.

        Note that this method will update all fields unless `update_mask` is set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteDerivedSignal(self, request, context):
        """Deletes a derived signal.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_DerivedSignalServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'GetDerivedSignal': grpc.unary_unary_rpc_method_handler(servicer.GetDerivedSignal, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.GetDerivedSignalRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.SerializeToString), 'CreateDerivedSignal': grpc.unary_unary_rpc_method_handler(servicer.CreateDerivedSignal, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.CreateDerivedSignalRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.SerializeToString), 'UpdateDerivedSignal': grpc.unary_unary_rpc_method_handler(servicer.UpdateDerivedSignal, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.UpdateDerivedSignalRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.SerializeToString), 'DeleteDerivedSignal': grpc.unary_unary_rpc_method_handler(servicer.DeleteDerivedSignal, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.DeleteDerivedSignalRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.analytics.v1.DerivedSignalService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('exabel.api.analytics.v1.DerivedSignalService', rpc_method_handlers)

class DerivedSignalService(object):
    """Service to manage derived signals.

    A derived signal is a DSL expression with a unique label. The label must be unique to the
    customer.

    Derived signals are stored in Library folders and shared across users through folder sharing.

    Requests to the DerivedSignalService are executed in the context of the customer's service
    account (SA). The SA is a special user that is a member of the customer user group, giving
    it access to all folders that are shared with this user group, but not to private folders.
    Hence, only derived signals that are in folders shared to the SA, via the customer user group,
    will be accessible via the DerivedSignalService.
    """

    @staticmethod
    def GetDerivedSignal(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.DerivedSignalService/GetDerivedSignal', exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.GetDerivedSignalRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def CreateDerivedSignal(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.DerivedSignalService/CreateDerivedSignal', exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.CreateDerivedSignalRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def UpdateDerivedSignal(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.DerivedSignalService/UpdateDerivedSignal', exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.UpdateDerivedSignalRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2.DerivedSignal.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def DeleteDerivedSignal(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.DerivedSignalService/DeleteDerivedSignal', exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__service__pb2.DeleteDerivedSignalRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)