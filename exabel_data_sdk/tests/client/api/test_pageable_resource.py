import unittest
from typing import Iterator, Optional, Sequence

from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.pageable_resource import PageableResourceMixin


class _PageableApiMock(PageableResourceMixin):
    def __init__(self, resources: Sequence[str]):
        self.resources = resources

    def get_resource_page(self, page_token: Optional[str] = None) -> PagingResult[str]:
        """Return a page of resources."""
        page_idx = int(page_token) if page_token else 0
        return PagingResult(
            self.resources[page_idx],
            next_page_token=str(page_idx + 1),
            total_size=len(self.resources),
        )

    def get_resource_iterator(self) -> Iterator[str]:
        """Return an iterator with all resources."""
        return self._get_resource_iterator(self.get_resource_page)


class TestPageableResourceMixin(unittest.TestCase):
    def test_get_resource_iterator(self):
        resources = ["a", "b", "c"]
        api = _PageableApiMock(resources)
        self.assertListEqual(list(api.get_resource_iterator()), resources)
