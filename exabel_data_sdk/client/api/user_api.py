from typing import Sequence

from exabel_data_sdk.client.api.api_client.grpc.user_grpc_client import UserGrpcClient
from exabel_data_sdk.client.api.api_client.http.user_http_client import UserHttpClient
from exabel_data_sdk.client.api.data_classes.group import Group
from exabel_data_sdk.client.api.data_classes.user import User
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.management.v1.user_service_pb2 import (
    ListGroupsRequest,
    ListUsersRequest,
)


class UserApi:
    """
    API class for user operations.
    """

    def __init__(self, config: ClientConfig, use_json: bool = False):
        self.client = (UserHttpClient if use_json else UserGrpcClient)(config)

    def list_users(self) -> Sequence[User]:
        """
        List all users.
        """
        response = self.client.list_users(ListUsersRequest())
        return [User.from_proto(user) for user in response.users]

    def list_groups(self) -> Sequence[Group]:
        """
        List all groups.
        """
        response = self.client.list_groups(ListGroupsRequest())
        return [Group.from_proto(group) for group in response.groups]
