from typing import Mapping, Union

from exabel_data_sdk.client.api.proto_utils import from_struct, to_struct
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import Relationship as ProtoRelationship


class Relationship:
    """
    A relationship resource in the Data API.

    Attributes:
        relationship_type: The resource name of the relationship type, for example
                           "relationshipTypes/namespace.relationshipTypeIdentifier". The namespace
                           must be empty (being global) or one of the predetermined namespaces the
                           customer has access to. The relationship type identifier must match the
                           regex [A-Z][A-Z0-9_]{0,63}.
        from_entity:       The resource name of the start point of the relationship, for example
                           "entityTypes/ns.type1/entities/ns.entity1".
        to_entity:         The resource name of the end point of the relationship, for example
                           "entityTypes/ns.type2/entities/ns.entity2".
        description:       One or more paragraphs of text description.
        properties:        The properties of this entity.
        read_only:         Whether this resource is read only.
    """

    def __init__(
        self,
        relationship_type: str,
        from_entity: str,
        to_entity: str,
        description: str,
        properties: Mapping[str, Union[str, bool, int, float]],
        read_only: bool = False,
    ):
        self.relationship_type = relationship_type
        self.from_entity = from_entity
        self.to_entity = to_entity
        self.description = description
        self.properties = properties
        self.read_only = read_only

    @staticmethod
    def from_proto(relationship: ProtoRelationship) -> "Relationship":
        """Create a Relationship from the given protobuf Relationship."""
        return Relationship(
            relationship_type=relationship.parent,
            from_entity=relationship.from_entity,
            to_entity=relationship.to_entity,
            description=relationship.description,
            properties=from_struct(relationship.properties),
            read_only=relationship.read_only,
        )

    def to_proto(self) -> ProtoRelationship:
        """Create a protobuf Relationship from this Relationship."""
        return ProtoRelationship(
            parent=self.relationship_type,
            from_entity=self.from_entity,
            to_entity=self.to_entity,
            description=self.description,
            properties=to_struct(self.properties),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Relationship):
            return False
        return (
            self.relationship_type == other.relationship_type
            and self.from_entity == other.from_entity
            and self.to_entity == other.to_entity
            and self.description == other.description
            and self.properties == other.properties
            and self.read_only == other.read_only
        )

    def __repr__(self) -> str:
        return (
            f"Relationship(relationship_type='{self.relationship_type}', "
            f"from_entity='{self.from_entity}', to_entity='{self.to_entity}', "
            f"description='{self.description}', properties={self.properties}, "
            f"read_only={self.read_only})"
        )
