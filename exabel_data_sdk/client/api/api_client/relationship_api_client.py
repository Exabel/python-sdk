from abc import ABC, abstractmethod

from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    CreateRelationshipRequest,
    CreateRelationshipTypeRequest,
    DeleteRelationshipRequest,
    DeleteRelationshipTypeRequest,
    GetRelationshipRequest,
    GetRelationshipTypeRequest,
    ListRelationshipsRequest,
    ListRelationshipsResponse,
    ListRelationshipTypesRequest,
    ListRelationshipTypesResponse,
    Relationship,
    RelationshipType,
)


class RelationshipApiClient(ABC):
    """
    Superclass for clients that send relationship requests to the Exabel Data API.
    """

    @abstractmethod
    def list_relationship_types(
        self, request: ListRelationshipTypesRequest
    ) -> ListRelationshipTypesResponse:
        """List all relationship types."""

    @abstractmethod
    def get_relationship_type(self, request: GetRelationshipTypeRequest) -> RelationshipType:
        """Get a relationship type."""

    @abstractmethod
    def create_relationship_type(self, request: CreateRelationshipTypeRequest) -> RelationshipType:
        """Create a relationship type."""

    @abstractmethod
    def delete_relationship_type(self, request: DeleteRelationshipTypeRequest) -> None:
        """Delete a relationship type."""

    @abstractmethod
    def list_relationships(self, request: ListRelationshipsRequest) -> ListRelationshipsResponse:
        """List the relationships for a given entity."""

    @abstractmethod
    def get_relationship(self, request: GetRelationshipRequest) -> Relationship:
        """Get a relationship."""

    @abstractmethod
    def create_relationship(self, request: CreateRelationshipRequest) -> Relationship:
        """Create a relationship."""

    @abstractmethod
    def delete_relationship(self, request: DeleteRelationshipRequest) -> None:
        """Delete a relationship."""
