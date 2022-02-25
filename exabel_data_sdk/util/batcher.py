import itertools
from typing import Iterable, Iterator, Sequence, TypeVar

T = TypeVar("T")  # pylint: disable=invalid-name


def batcher(iterable: Iterable[T], n: int = 1000) -> Iterator[Sequence[T]]:
    """
    Batches the iterable into chunks of size n.
    """
    iterator = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(iterator, n))
        if not chunk:
            return
        yield chunk
