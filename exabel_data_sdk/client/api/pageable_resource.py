from typing import Callable, Iterator, Optional, TypeVar

from exabel_data_sdk.client.api.data_classes.data_set import DataSet
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.data_classes.relationship_type import RelationshipType
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.client.api.data_classes.tag import Tag

PageableResourceT = TypeVar(
    "PageableResourceT",
    DataSet,
    Entity,
    EntityType,
    Relationship,
    RelationshipType,
    Signal,
    Tag,
    str,  # for paging through time series
)


class PageableResourceMixin:
    """Mixin class for APIs that contain methods with pageable resources."""

    @staticmethod
    def _get_resource_iterator(
        pageable_func: Callable[..., PagingResult[PageableResourceT]],
        page_size: int = 1000,
        **kwargs: str,
    ) -> Iterator[PageableResourceT]:
        """
        Return an iterator with all the resources returnable by function, paging through the
        results.
        """
        page_token: Optional[str] = None
        while True:
            result = pageable_func(**kwargs, page_token=page_token, page_size=page_size)
            yield from result.results
            page_token = result.next_page_token
            if len(result.results) < page_size:
                break
