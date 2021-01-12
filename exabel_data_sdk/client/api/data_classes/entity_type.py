from __future__ import annotations

from dataclasses import dataclass

from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import EntityType as ProtoEntityType


@dataclass
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

    name: str

    display_name: str

    description: str

    read_only: bool = False

    @staticmethod
    def from_proto(entity_type: ProtoEntityType) -> EntityType:
        """Create an EntityType from a protobuf EntityType."""
        return EntityType(
            name=entity_type.name,
            display_name=entity_type.display_name,
            description=entity_type.description,
            read_only=entity_type.read_only,
        )
