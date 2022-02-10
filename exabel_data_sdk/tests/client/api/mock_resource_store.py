from random import random
from typing import Callable, Dict, Generic, Optional, TypeVar

from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError

TResource = TypeVar("TResource")


def failure_prone(func):
    """
    Decorator for class methods that make them raise an exception every now and then,
    depending on the 'failure_rate' attribute of the object.
    """

    def unreliable(self, *args, **kwargs):
        if self.failure_rate and random() < self.failure_rate:
            raise RequestError(ErrorType.UNAVAILABLE, "This is a random failure")
        return func(self, *args, **kwargs)

    return unreliable


class MockResourceStore(Generic[TResource]):
    """In-memory resource store. Only intended for tests."""

    def __init__(self):
        self.resources: Dict[object, TResource] = {}
        # The failure rate, as a fraction (0.0-1.0) of calls that should fail
        self.failure_rate = 0.0

    def get(self, key: object) -> Optional[TResource]:
        """Get the resource with the given key if present, otherwise returns None."""
        return self.resources.get(key, None)

    def list(self, predicate: Callable[[TResource], bool] = None) -> PagingResult[TResource]:
        """List all resources in the store."""
        resources = list(self.resources.values())
        if predicate:
            resources = list(filter(predicate, resources))
        return PagingResult(
            results=resources,
            next_page_token="next_page_token",
            total_size=len(resources),
        )

    @failure_prone
    def create(self, resource: TResource, key: object = None) -> TResource:
        """
        Create the given resource in the store.

        Typically, resources have a resource name, which should be used as the key.
        In this case, the key parameter should not be set.
        If not, as in the case of Relationship resources, an explicit key must be provided.

        Args:
            resource: the resource to create in the store
            key:      the key of the resource. Defaults to the resource's name.
        """
        if key is None:
            key = resource.name  # type: ignore[attr-defined]
        if key in self.resources:
            raise RequestError(ErrorType.ALREADY_EXISTS, f"Already exists: {key}")
        self.resources[key] = resource
        return resource

    @failure_prone
    def update(
        self, resource: TResource, key: object = None, allow_missing: bool = None
    ) -> TResource:
        """
        Update the given resource in the store.

        Typically, resources have a resource name, which should be used as the key.
        In this case, the key parameter should not be set.
        If not, as in the case of Relationship resources, an explicit key must be provided.

        Args:
            resource: the resource to create in the store
            key:      the key of the resource. Defaults to the resource's name.
        """
        if key is None:
            key = resource.name  # type: ignore[attr-defined]
        if not allow_missing and key not in self.resources:
            raise RequestError(ErrorType.NOT_FOUND, f"Does not exist: {key}")
        self.resources[key] = resource
        return resource

    def delete(self, key: object):
        """Delete the resource with the given key."""
        if key in self.resources:
            del self.resources[key]
        raise ValueError(f"Trying to delete non-existent resource: {key}")
