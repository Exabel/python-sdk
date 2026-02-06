from exabel.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel.client.api.api_client.user_api_client import UserApiClient
from exabel.client.api.error_handler import handle_grpc_error
from exabel.client.client_config import ClientConfig
from exabel.stubs.exabel.api.management.v1.all_pb2 import (
    ListGroupsRequest,
    ListGroupsResponse,
    ListUsersRequest,
    ListUsersResponse,
)
from exabel.stubs.exabel.api.management.v1.all_pb2_grpc import UserServiceStub


class UserGrpcClient(UserApiClient, BaseGrpcClient):
    """
    Client which sends user requests to the Exabel Management API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.MANAGEMENT_API)
        self.stub = UserServiceStub(self.channel)

    @handle_grpc_error
    def list_users(self, request: ListUsersRequest) -> ListUsersResponse:
        return self.stub.ListUsers(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def list_groups(self, request: ListGroupsRequest) -> ListGroupsResponse:
        return self.stub.ListGroups(request, metadata=self.metadata, timeout=self.config.timeout)
