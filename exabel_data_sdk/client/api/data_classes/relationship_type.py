from typing import Mapping, Union

from exabel_data_sdk.client.api.proto_utils import from_struct, to_struct
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    RelationshipType as ProtoRelationshipType,
)


class RelationshipType:
    """
    A relationship type resource in the Data API.

    Attributes:
        name (str):             The resource name of the relationship type, for example
                                "relationshipTypes/namespace.relationshipTypeIdentifier".
                                The namespace must be empty (being global) or one of the
                                predetermined namespaces the customer has access to. The
                                relationship type identifier must match the regex
                                [A-Z][A-Z0-9_]{0,63}.
        description (str):      One or more paragraphs of text description.
        properties (dict):      The properties of this entity.
        read_only (bool):       Whether this resource is read only.
        is_ownership (bool):    Whether this relationship type is a data set ownership.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        properties: Mapping[str, Union[str, bool, int, float]] = None,
        read_only: bool = False,
        is_ownership: bool = False,
    ):
        """
        Create a relationship type resource in the Data API.

        Args:
            name:        The resource name of the relationship type, for example
                         "relationshipTypes/namespace.relationshipTypeIdentifier". The namespace
                         must be empty (being global) or one of the predetermined namespaces the
                         customer has access to. The relationship type identifier must match the
                         regex [A-Z][A-Z0-9_]{0,63}.
            description: One or more paragraphs of text description.
            properties:  The properties of this entity.
            read_only:   Whether this resource is read only.
            read_only:   Whether this relationship type is a data set ownership.
        """
        self.name = name
        self.description = description
        self.properties = {} if properties is None else properties
        self.read_only = read_only
        self.is_ownership = is_ownership

    @staticmethod
    def from_proto(relationship_type: ProtoRelationshipType) -> "RelationshipType":
        """Create a RelationshipType from the given protobuf RelationshipType."""
        return RelationshipType(
            name=relationship_type.name,
            description=relationship_type.description,
            properties=from_struct(relationship_type.properties),
            read_only=relationship_type.read_only,
            is_ownership=relationship_type.is_ownership,
        )

    def to_proto(self) -> ProtoRelationshipType:
        """Create a protobuf RelationshipType from this RelationshipType."""
        return ProtoRelationshipType(
            name=self.name,
            description=self.description,
            properties=to_struct(self.properties),
            is_ownership=self.is_ownership,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RelationshipType):
            return False
        return (
            self.name == other.name
            and self.description == other.description
            and self.properties == other.properties
            and self.read_only == other.read_only
            and self.is_ownership == other.is_ownership
        )

    def __repr__(self) -> str:
        return (
            f"RelationshipType(name='{self.name}', description='{self.description}', "
            f"properties={self.properties}, read_only={self.read_only}, "
            f"is_ownership={self.is_ownership})"
        )
