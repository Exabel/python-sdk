from abc import ABC, abstractmethod

from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    CreateEntityRequest,
    CreateEntityTypeRequest,
    DeleteEntitiesRequest,
    DeleteEntityRequest,
    DeleteEntityTypeRequest,
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
    UpdateEntityRequest,
    UpdateEntityTypeRequest,
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
    def create_entity_type(self, request: CreateEntityTypeRequest) -> EntityType:
        """Create an entity type."""

    @abstractmethod
    def update_entity_type(self, request: UpdateEntityTypeRequest) -> EntityType:
        """Update an entity type."""

    @abstractmethod
    def delete_entity_type(self, request: DeleteEntityTypeRequest) -> None:
        """Delete an entity type."""

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
    def update_entity(self, request: UpdateEntityRequest) -> Entity:
        """Update an entity."""

    @abstractmethod
    def delete_entity(self, request: DeleteEntityRequest) -> None:
        """Delete an entity."""

    @abstractmethod
    def delete_entities(self, request: DeleteEntitiesRequest) -> None:
        """Delete all entities of a given entity type."""

    @abstractmethod
    def search_entities(self, request: SearchEntitiesRequest) -> SearchEntitiesResponse:
        """Search for entities."""
