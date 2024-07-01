import unittest
from typing import Iterator, Optional, Sequence

from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.pageable_resource import PageableResourceMixin


class _PageableApiMock(PageableResourceMixin):
    def __init__(self, resources: Sequence[str], total_sizes: Optional[Sequence[int]] = None):
        self.resources = resources
        if total_sizes is not None:
            self.total_sizes = total_sizes
        else:
            self.total_sizes = [len(resources)] * len(resources)

    def get_resource_page(
        self, page_size: Optional[int] = None, page_token: Optional[str] = None
    ) -> PagingResult[str]:
        """Return a page of resources."""
        assert page_size == 1
        if page_token == "~~~":
            page_idx = len(self.resources)
        else:
            page_idx = int(page_token) if page_token else 0
        if page_idx >= len(self.resources):
            return PagingResult([], next_page_token="~~~", total_size=self.total_sizes[-1])
        return PagingResult(
            [self.resources[page_idx]] if page_idx < len(self.resources) else [],
            next_page_token=str(page_idx + 1),
            total_size=self.total_sizes[page_idx],
        )

    def get_resource_iterator(self) -> Iterator[str]:
        """Return an iterator with all resources."""
        return self._get_resource_iterator(self.get_resource_page, page_size=1)


class TestPageableResourceMixin(unittest.TestCase):
    def test_get_resource_iterator(self):
        resources = ["a", "b", "c"]
        api = _PageableApiMock(resources)
        self.assertListEqual(list(api.get_resource_iterator()), resources)

    def test_get_resource_iterator__with_varying_total_sizes(self):
        """Avoid infinite iteration if the item set is modified while iterating."""
        resources = ["a", "b", "c"]
        total_sizes = [3, 4, 4]
        api = _PageableApiMock(resources, total_sizes)
        self.assertListEqual(list(api.get_resource_iterator()), resources)
