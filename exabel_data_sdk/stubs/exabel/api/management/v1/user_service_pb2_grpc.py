"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....exabel.api.management.v1 import user_service_pb2 as exabel_dot_api_dot_management_dot_v1_dot_user__service__pb2

class UserServiceStub(object):
    """Service to manage users and groups.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListGroups = channel.unary_unary('/exabel.api.management.v1.UserService/ListGroups', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_user__service__pb2.ListGroupsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_management_dot_v1_dot_user__service__pb2.ListGroupsResponse.FromString)
        self.ListUsers = channel.unary_unary('/exabel.api.management.v1.UserService/ListUsers', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_user__service__pb2.ListUsersRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_management_dot_v1_dot_user__service__pb2.ListUsersResponse.FromString)

class UserServiceServicer(object):
    """Service to manage users and groups.
    """

    def ListGroups(self, request, context):
        """List all groups. Only groups for the current customer is returned.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListUsers(self, request, context):
        """List all users in the current customer.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_UserServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListGroups': grpc.unary_unary_rpc_method_handler(servicer.ListGroups, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_user__service__pb2.ListGroupsRequest.FromString, response_serializer=exabel_dot_api_dot_management_dot_v1_dot_user__service__pb2.ListGroupsResponse.SerializeToString), 'ListUsers': grpc.unary_unary_rpc_method_handler(servicer.ListUsers, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_user__service__pb2.ListUsersRequest.FromString, response_serializer=exabel_dot_api_dot_management_dot_v1_dot_user__service__pb2.ListUsersResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.management.v1.UserService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class UserService(object):
    """Service to manage users and groups.
    """

    @staticmethod
    def ListGroups(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.UserService/ListGroups', exabel_dot_api_dot_management_dot_v1_dot_user__service__pb2.ListGroupsRequest.SerializeToString, exabel_dot_api_dot_management_dot_v1_dot_user__service__pb2.ListGroupsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListUsers(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.UserService/ListUsers', exabel_dot_api_dot_management_dot_v1_dot_user__service__pb2.ListUsersRequest.SerializeToString, exabel_dot_api_dot_management_dot_v1_dot_user__service__pb2.ListUsersResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)