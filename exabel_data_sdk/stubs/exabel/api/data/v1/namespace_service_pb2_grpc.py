"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from .....exabel.api.data.v1 import namespace_service_pb2 as exabel_dot_api_dot_data_dot_v1_dot_namespace__service__pb2
GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in exabel/api/data/v1/namespace_service_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class NamespaceServiceStub(object):
    """Service for managing namespaces. Namespaces allow Exabel to keep customer data segregated and
    private to users of that customer.

    If you have an Exabel full platform license, you will have your own private namespace. All data
    that you import will be created in that namespace, and therefore kept private.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListNamespaces = channel.unary_unary('/exabel.api.data.v1.NamespaceService/ListNamespaces', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_namespace__service__pb2.ListNamespacesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_namespace__service__pb2.ListNamespacesResponse.FromString, _registered_method=True)

class NamespaceServiceServicer(object):
    """Service for managing namespaces. Namespaces allow Exabel to keep customer data segregated and
    private to users of that customer.

    If you have an Exabel full platform license, you will have your own private namespace. All data
    that you import will be created in that namespace, and therefore kept private.
    """

    def ListNamespaces(self, request, context):
        """Lists namespaces.

        Lists all namespaces accessible to your customer. If you have your own namespace, it will
        listed as writeable. You may also have read access to other namespaces, depending on your
        subscriptions.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_NamespaceServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListNamespaces': grpc.unary_unary_rpc_method_handler(servicer.ListNamespaces, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_namespace__service__pb2.ListNamespacesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_namespace__service__pb2.ListNamespacesResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.data.v1.NamespaceService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('exabel.api.data.v1.NamespaceService', rpc_method_handlers)

class NamespaceService(object):
    """Service for managing namespaces. Namespaces allow Exabel to keep customer data segregated and
    private to users of that customer.

    If you have an Exabel full platform license, you will have your own private namespace. All data
    that you import will be created in that namespace, and therefore kept private.
    """

    @staticmethod
    def ListNamespaces(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.NamespaceService/ListNamespaces', exabel_dot_api_dot_data_dot_v1_dot_namespace__service__pb2.ListNamespacesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_namespace__service__pb2.ListNamespacesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)