from typing import Iterable, Union

from tqdm import tqdm

PAGE_SIZE = 1000
MAX_WORKERS = 10
SUCCESS = 0
ERROR = 1
TQDM_BAR_FORMAT = (
    "{l_bar}{bar} | Pages: {n_fmt}/{total_fmt} [Time - Remaining: {remaining} Elapsed: {elapsed}]"
)
NCOLS = 100


def conditional_progress_bar(
    iterable: Iterable, show_progress: bool = False, **kwargs: Union[str, int]
) -> Iterable:
    """
    Returns a tqdm progress bar if show_progress is True, otherwise returns the iterable unchanged.
    """
    if show_progress:
        return tqdm(iterable, ncols=NCOLS, bar_format=TQDM_BAR_FORMAT, **kwargs)
    return iterable
