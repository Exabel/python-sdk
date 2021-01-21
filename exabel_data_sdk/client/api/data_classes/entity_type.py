from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import EntityType as ProtoEntityType


class EntityType:
    r"""
    An entity type resource in the Data API.

    Attributes:
        name (str):         The resource name of the entity type, for example
                            "entityTypes/entityTypeIdentifier" or
                            "entityTypes/namespace.entityTypeIdentifier". The namespace must be
                            empty (being global) or one of the predetermined namespaces the customer
                            has access to. The entity type identifier must match the regex
                            [a-zA-Z][\w-]{0,63}.
        display_name (str): The display name of the entity type.
        description (str):  One or more paragraphs of text description.
        read_only (bool):   Whether this resource is read only.
    """

    def __init__(
        self,
        name: str,
        display_name: str,
        description: str,
        read_only: bool = False,
    ):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.read_only = read_only

    @staticmethod
    def from_proto(entity_type: ProtoEntityType) -> "EntityType":
        """Create an EntityType from a protobuf EntityType."""
        return EntityType(
            name=entity_type.name,
            display_name=entity_type.display_name,
            description=entity_type.description,
            read_only=entity_type.read_only,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EntityType):
            return False
        return (
            self.name == other.name
            and self.display_name == other.display_name
            and self.description == other.description
            and self.read_only == other.read_only
        )

    def __repr__(self) -> str:
        return (
            f"EntityType(name='{self.name}', display_name='{self.display_name}', "
            f"description='{self.description}', read_only={self.read_only})"
        )
