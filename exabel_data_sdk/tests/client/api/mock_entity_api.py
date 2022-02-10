from typing import Optional, Sequence

from google.protobuf.field_mask_pb2 import FieldMask

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.tests.client.api.mock_resource_store import MockResourceStore


# pylint: disable=super-init-not-called
class MockEntityApi(EntityApi):
    """
    Mock of the EntityApi class for CRUD operations on entities and entity types.
    """

    def __init__(self):
        self.entities = MockResourceStore()
        self.types = MockResourceStore()
        self._insert_standard_entity_types()

    def _insert_standard_entity_types(self):
        for entity_type in ("brand", "business_segment", "company", "country", "region"):
            self.types.create(EntityType("entityTypes/" + entity_type, entity_type, ""))

    def list_entity_types(
        self, page_size: int = 1000, page_token: str = None
    ) -> PagingResult[EntityType]:
        return self.types.list()

    def get_entity_type(self, name: str) -> Optional[EntityType]:
        return self.types.get(name)

    def list_entities(
        self, entity_type: str, page_size: int = 1000, page_token: str = None
    ) -> PagingResult[Entity]:
        return self.entities.list(lambda x: x.get_entity_type() == entity_type)

    def get_entity(self, name: str) -> Optional[Entity]:
        return self.entities.get(name)

    def create_entity(self, entity: Entity, entity_type: str) -> Entity:
        return self.entities.create(entity)

    def update_entity(
        self, entity: Entity, update_mask: FieldMask = None, allow_missing: bool = False
    ) -> Entity:
        # Note: The mock implementation ignores update_mask
        return self.entities.update(entity, allow_missing=allow_missing)

    def delete_entity(self, name: str) -> None:
        # Note: The mock implementation does not delete associated time series and relationships
        self.entities.delete(name)

    def search_for_entities(self, entity_type: str, **search_terms: str) -> Sequence[Entity]:
        raise NotImplementedError()
