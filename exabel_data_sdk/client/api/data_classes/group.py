from typing import Sequence

from exabel_data_sdk.client.api.data_classes.user import User
from exabel_data_sdk.stubs.exabel.api.management.v1.all_pb2 import Group as ProtoGroup


class Group:
    """
    A group resource in the Management API.

    Attributes:
        name (str):         The resource name of the group, for example "groups/123".
        display_name (str): The display name of the group.
        users (list):       The users in this group.
    """

    def __init__(self, name: str, display_name: str, users: Sequence[User]):
        """
        Create a user.

        Args:
            name (str):         The resource name of the group, for example "groups/123".
            display_name (str): The display name of the group.
            users (list):       The users in this group.
        """
        self.name = name
        self.display_name = display_name
        self.users = users

    @staticmethod
    def from_proto(group: ProtoGroup) -> "Group":
        """Create a Group from the given protobuf Group."""
        return Group(
            name=group.name,
            display_name=group.display_name,
            users=[User.from_proto(user) for user in group.users],
        )

    def to_proto(self) -> ProtoGroup:
        """Create a protobuf Group from this Group."""
        return ProtoGroup(
            name=self.name,
            display_name=self.display_name,
            users=[user.to_proto() for user in self.users],
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Group):
            return False
        return (
            self.name == other.name
            and self.display_name == other.display_name
            and sorted(self.users) == sorted(other.users)
        )

    def __repr__(self) -> str:
        return f"Group(name='{self.name}', display_name='{self.display_name}', users={self.users})"
