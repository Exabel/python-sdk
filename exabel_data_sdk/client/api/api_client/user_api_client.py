from abc import ABC, abstractmethod

from exabel_data_sdk.stubs.exabel.api.management.v1.all_pb2 import (
    ListGroupsRequest,
    ListGroupsResponse,
    ListUsersRequest,
    ListUsersResponse,
)


class UserApiClient(ABC):
    """
    Superclass for clients that send user requests to the Exabel Management API.
    """

    @abstractmethod
    def list_users(self, request: ListUsersRequest) -> ListUsersResponse:
        """List all users."""

    @abstractmethod
    def list_groups(self, request: ListGroupsRequest) -> ListGroupsResponse:
        """List all groups."""
