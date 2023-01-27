from typing import Callable, Iterator, Optional, TypeVar

from exabel_data_sdk.client.api.data_classes.data_set import DataSet
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.data_classes.relationship_type import RelationshipType
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.client.api.data_classes.tag import Tag

PagableResourceT = TypeVar(
    "PagableResourceT",
    DataSet,
    Entity,
    EntityType,
    Relationship,
    RelationshipType,
    Signal,
    Tag,
    str,  # for paging through time series
)


class PagableResourceMixin:
    """Mixin class for APIs that contain methods with pagable resources."""

    @staticmethod
    def _get_resource_iterator(
        pagable_func: Callable[..., PagingResult[PagableResourceT]],
        **kwargs: str,
    ) -> Iterator[PagableResourceT]:
        """
        Return an iterator with all the resources returnable by function, paging through the
        results.
        """
        page_token: Optional[str] = None
        resource_count = 0
        while True:
            result = pagable_func(**kwargs, page_token=page_token)
            for resource in result.results:
                yield resource
            page_token = result.next_page_token
            resource_count += len(result.results)
            if resource_count >= result.total_size:
                break
