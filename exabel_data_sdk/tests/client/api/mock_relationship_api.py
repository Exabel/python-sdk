from typing import Optional

from google.protobuf.field_mask_pb2 import FieldMask

from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.data_classes.relationship_type import RelationshipType
from exabel_data_sdk.client.api.relationship_api import RelationshipApi
from exabel_data_sdk.tests.client.api.mock_resource_store import MockResourceStore


# pylint: disable=super-init-not-called
class MockRelationshipApi(RelationshipApi):
    """
    Mock of the RelationshipApi class for CRUD operations on relationships and relationship types.
    """

    def __init__(self):
        self.relationships = MockResourceStore()
        self.types = MockResourceStore()
        self._insert_standard_relationship_types()

    def _insert_standard_relationship_types(self):
        for rel_type in ("LOCATED_IN", "WEB_DOMAIN_OWNED_BY", "test.HAS_BRAND", "acme.PART_OF"):
            self.types.create(RelationshipType("relationshipTypes/" + rel_type, rel_type, ""))

    @staticmethod
    def _key(relationship: Relationship) -> object:
        return (relationship.relationship_type, relationship.from_entity, relationship.to_entity)

    def list_relationship_types(
        self, page_size: int = 1000, page_token: str = None
    ) -> PagingResult[RelationshipType]:
        return self.types.list()

    def get_relationship_type(self, name: str) -> Optional[RelationshipType]:
        return self.types.get(name)

    def create_relationship_type(self, relationship_type: RelationshipType) -> RelationshipType:
        return self.types.create(relationship_type)

    def update_relationship_type(
        self,
        relationship_type: RelationshipType,
        update_mask: FieldMask = None,
        allow_missing: bool = None,
    ) -> RelationshipType:
        raise NotImplementedError()

    def delete_relationship_type(self, relationship_type: str) -> None:
        self.types.delete(relationship_type)

    def get_relationships_from_entity(
        self,
        relationship_type: str,
        from_entity: str,
        page_size: int = 1000,
        page_token: str = None,
    ) -> PagingResult[Relationship]:
        raise NotImplementedError()

    def get_relationships_to_entity(
        self,
        relationship_type: str,
        to_entity: str,
        page_size: int = 1000,
        page_token: str = None,
    ) -> PagingResult[Relationship]:
        raise NotImplementedError()

    def get_relationship(
        self, relationship_type: str, from_entity: str, to_entity: str
    ) -> Optional[Relationship]:
        return self.relationships.get((relationship_type, from_entity, to_entity))

    def create_relationship(self, relationship: Relationship) -> Relationship:
        return self.relationships.create(relationship, self._key(relationship))

    def update_relationship(
        self, relationship: Relationship, update_mask: FieldMask = None, allow_missing: bool = None
    ) -> Relationship:
        # Note: The mock implementation ignores update_mask
        return self.relationships.update(relationship, self._key(relationship), allow_missing)

    def delete_relationship(self, relationship_type: str, from_entity: str, to_entity: str) -> None:
        self.relationships.delete((relationship_type, from_entity, to_entity))

    def list_relationships(self) -> PagingResult[Relationship]:
        """
        Returns all relationships.
        Note that this method is only available in the mock API, not the real API.
        """
        return self.relationships.list()
