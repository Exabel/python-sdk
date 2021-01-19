from typing import Generic, Iterator, Sequence, TypeVar

TValue = TypeVar("TValue")


class PagingResult(Generic[TValue]):
    """
    A sequence of results from the Exabel API that can be be retrieved with paging.

    Attributes:
        results:         The results of a single request.
        next_page_token: The page token where the list continues. Can be sent to a subsequent query.
        total_size:      The total number of results, irrespective of paging.
    """

    def __init__(self, results: Sequence[TValue], next_page_token: str, total_size: int):
        self.results = results
        self.next_page_token = next_page_token
        self.total_size = total_size

    def __iter__(self) -> Iterator[TValue]:
        return self.results.__iter__()

    def __str__(self) -> str:
        results = "\n   ".join([str(result) for result in self.results])
        return (
            f"total_size: {self.total_size}\nnext_page_token: {self.next_page_token}\nresults:\n   "
            f"{results}"
        )
