from exabel_data_sdk.stubs.exabel.api.management.v1.all_pb2 import User as ProtoUser


class User:
    """
    A user resource in the Management API.

    Attributes:
        name (str):     The resource name of the user, for example "users/123".
        email (str):    The email of the user.
        blocked (bool): Whether the user is blocked.
    """

    def __init__(self, name: str, email: str, blocked: bool):
        """
        Create a user.

        Args:
            name (str):     The resource name of the user, for example "users/123".
            email (str):    The email of the user.
            blocked (bool): Whether the user is blocked.
        """
        self.name = name
        self.email = email
        self.blocked = blocked

    @staticmethod
    def from_proto(user: ProtoUser) -> "User":
        """Create a User from the given protobuf User."""
        return User(name=user.name, email=user.email, blocked=user.blocked)

    def to_proto(self) -> ProtoUser:
        """Create a protobuf User from this User."""
        return ProtoUser(name=self.name, email=self.email, blocked=self.blocked)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return (
            self.name == other.name and self.email == other.email and self.blocked == other.blocked
        )

    def __repr__(self) -> str:
        return f"User(name='{self.name}', email='{self.email}', blocked={self.blocked})"

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, User):
            raise ValueError(f"Cannot compare User to non-User: {other}")
        return self.name < other.name
