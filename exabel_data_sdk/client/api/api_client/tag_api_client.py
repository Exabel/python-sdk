from abc import ABC, abstractmethod

from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    AddEntitiesRequest,
    AddEntitiesResponse,
    CreateTagRequest,
    DeleteTagRequest,
    GetTagRequest,
    ListTagEntitiesRequest,
    ListTagEntitiesResponse,
    ListTagsRequest,
    ListTagsResponse,
    RemoveEntitiesRequest,
    RemoveEntitiesResponse,
    Tag,
    UpdateTagRequest,
)


class TagApiClient(ABC):
    """
    Superclass for clients that send tag requests to the Exabel Analytics API.
    """

    @abstractmethod
    def create_tag(self, request: CreateTagRequest) -> Tag:
        """Create a tag."""

    @abstractmethod
    def get_tag(self, request: GetTagRequest) -> Tag:
        """Get a tag."""

    @abstractmethod
    def update_tag(self, request: UpdateTagRequest) -> Tag:
        """Update a tag."""

    @abstractmethod
    def delete_tag(self, request: DeleteTagRequest) -> None:
        """Delete a tag."""

    @abstractmethod
    def list_tags(self, request: ListTagsRequest) -> ListTagsResponse:
        """List all tags accessible to user."""

    @abstractmethod
    def add_entities(self, request: AddEntitiesRequest) -> AddEntitiesResponse:
        """Add entities to a tag."""

    @abstractmethod
    def remove_entities(self, request: RemoveEntitiesRequest) -> RemoveEntitiesResponse:
        """Remove entities from a tag."""

    @abstractmethod
    def list_entities(self, request: ListTagEntitiesRequest) -> ListTagEntitiesResponse:
        """List entities in a tag."""
