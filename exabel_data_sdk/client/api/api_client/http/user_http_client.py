from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.http.base_http_client import BaseHttpClient
from exabel_data_sdk.client.api.api_client.user_api_client import UserApiClient
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.management.v1.all_pb2 import (
    ListGroupsRequest,
    ListGroupsResponse,
    ListUsersRequest,
    ListUsersResponse,
)


class UserHttpClient(UserApiClient, BaseHttpClient):
    """
    Client which sends user requests to the Exabel Management API with JSON over HTTP.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.MANAGEMENT_API)

    def list_users(self, request: ListUsersRequest) -> ListUsersResponse:
        return self._request("GET", "users", ListUsersResponse())

    def list_groups(self, request: ListGroupsRequest) -> ListGroupsResponse:
        return self._request("GET", "groups", ListGroupsResponse())
