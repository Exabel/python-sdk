from abc import ABC, abstractmethod

from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    CreateEntityRequest,
    DeleteEntityRequest,
    Entity,
    EntityType,
    GetEntityRequest,
    GetEntityTypeRequest,
    ListEntitiesRequest,
    ListEntitiesResponse,
    ListEntityTypesRequest,
    ListEntityTypesResponse,
    SearchEntitiesRequest,
    SearchEntitiesResponse,
)


class EntityApiClient(ABC):
    """
    Superclass for clients that send entity requests to the Exabel Data API.
    """

    @abstractmethod
    def list_entity_types(self, request: ListEntityTypesRequest) -> ListEntityTypesResponse:
        """List all known entity types."""

    @abstractmethod
    def get_entity_type(self, request: GetEntityTypeRequest) -> EntityType:
        """Get an entity type."""

    @abstractmethod
    def list_entities(self, request: ListEntitiesRequest) -> ListEntitiesResponse:
        """List all entities of a given entity type."""

    @abstractmethod
    def get_entity(self, request: GetEntityRequest) -> Entity:
        """Get an entity."""

    @abstractmethod
    def create_entity(self, request: CreateEntityRequest) -> Entity:
        """Create an entity."""

    @abstractmethod
    def delete_entity(self, request: DeleteEntityRequest) -> None:
        """Delete an entity."""

    @abstractmethod
    def search_entities(self, request: SearchEntitiesRequest) -> SearchEntitiesResponse:
        """Search for entities."""
