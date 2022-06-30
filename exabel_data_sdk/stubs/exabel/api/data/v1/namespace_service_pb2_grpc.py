"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....exabel.api.data.v1 import namespace_service_pb2 as exabel_dot_api_dot_data_dot_v1_dot_namespace__service__pb2

class NamespaceServiceStub(object):
    """Retrieves namespace info from the Data API.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListNamespaces = channel.unary_unary('/exabel.api.data.v1.NamespaceService/ListNamespaces', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_namespace__service__pb2.ListNamespacesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_namespace__service__pb2.ListNamespacesResponse.FromString)

class NamespaceServiceServicer(object):
    """Retrieves namespace info from the Data API.
    """

    def ListNamespaces(self, request, context):
        """Lists namespaces.

        Lists the namespaces available to the client.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_NamespaceServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListNamespaces': grpc.unary_unary_rpc_method_handler(servicer.ListNamespaces, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_namespace__service__pb2.ListNamespacesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_namespace__service__pb2.ListNamespacesResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.data.v1.NamespaceService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class NamespaceService(object):
    """Retrieves namespace info from the Data API.
    """

    @staticmethod
    def ListNamespaces(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.NamespaceService/ListNamespaces', exabel_dot_api_dot_data_dot_v1_dot_namespace__service__pb2.ListNamespacesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_namespace__service__pb2.ListNamespacesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)