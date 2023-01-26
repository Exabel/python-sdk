from typing import Iterator, List, Optional

from exabel_data_sdk.client.api.api_client.grpc.tag_grpc_client import TagGrpcClient
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.api.data_classes.tag import Tag
from exabel_data_sdk.client.api.pagable_resource import PagableResourceMixin
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    AddEntitiesRequest,
    CreateTagRequest,
    DeleteTagRequest,
    GetTagRequest,
    ListTagEntitiesRequest,
    ListTagsRequest,
    RemoveEntitiesRequest,
    UpdateTagRequest,
)


class TagApi(PagableResourceMixin):
    """
    API class for tag operations.
    """

    def __init__(self, config: ClientConfig):
        self.client = TagGrpcClient(config)

    def create_tag(self, tag: Tag, folder: Optional[str] = None) -> Tag:
        """
        Create a tag.

        Args:
            tag:    The tag to create.
            folder: The resource name of the folder to put the tag in. Example: "folders/123".
                    If not provided, the tag will be put in the default analytics API folder.
        """
        response = self.client.create_tag(CreateTagRequest(tag=tag.to_proto(), folder=folder))
        return Tag.from_proto(response)

    def get_tag(self, name: str) -> Optional[Tag]:
        """
        Get a tag.

        Return None if the tag does not exist.

        Args:
            name:   The resource name of the tag, for example "tags/user:123".
        """
        try:
            response = self.client.get_tag(GetTagRequest(name=name))
        except RequestError as error:
            if error.error_type == ErrorType.NOT_FOUND:
                return None
            raise
        return Tag.from_proto(response)

    def update_tag(self, tag: Tag) -> Tag:
        """
        Update a tag.

        Args:
            tag: The tag to update.
        """
        response = self.client.update_tag(UpdateTagRequest(tag=tag.to_proto()))
        return Tag.from_proto(response)

    def delete_tag(self, name: str) -> None:
        """
        Delete a tag.

        Args:
            name:   The resource name of the tag, for example "tags/user:123".
        """
        self.client.delete_tag(DeleteTagRequest(name=name))

    def list_tags(
        self, page_size: int = 1000, page_token: Optional[str] = None
    ) -> PagingResult[Tag]:
        """
        List tags accesible to the user.

        Args:
            page_size:  The maximum number of results to return. Defaults to 1000, which is also
                        the maximum size of this field.
            page_token: The page token to resume the results from.
        """

        response = self.client.list_tags(
            ListTagsRequest(page_size=page_size, page_token=page_token)
        )

        return PagingResult(
            results=[Tag.from_proto(t) for t in response.tags],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    def get_tag_iterator(self) -> Iterator[Tag]:
        """Return an iterator with all tags."""
        return self._get_resource_iterator(self.list_tags)

    def add_entities(self, name: str, entity_names: List[str]) -> None:
        """
        Add entities to a tag.

        Args:
            name:         The resource name of the tag, for example "tags/user:123".
            entity_names: A list of resource names for entities to be added to the tag.
        """
        self.client.add_entities(AddEntitiesRequest(name=name, entity_names=entity_names))

    def remove_entities(self, name: str, entity_names: List[str]) -> None:
        """
        Remove entities from a tag.

        Args:
            name:         The resource name of the tag, for example "tags/user:123".
            entity_names: A list of resource names for entities to be removed from the tag.
        """
        self.client.remove_entities(RemoveEntitiesRequest(name=name, entity_names=entity_names))

    def list_entities(
        self, parent: str, page_size: int = 1000, page_token: Optional[str] = None
    ) -> PagingResult[str]:
        """
        List resource names of the entities in the parent tag.

        Args:
            parent:     The parent tag to get entities for, for example "tags/user:123".
            page_size:  The maximum number of results to return. Defaults to 1000, which is also
                        the maximum size of this field.
            page_token: The page token to resume the results from.
        """

        response = self.client.list_entities(
            ListTagEntitiesRequest(parent=parent, page_size=page_size, page_token=page_token)
        )

        return PagingResult(
            results=response.entity_names,
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    def get_entity_iterator(self, parent: str) -> Iterator[str]:
        """Return an iterator with all resource names of the entities in a tag."""
        return self._get_resource_iterator(self.list_entities, parent=parent)
