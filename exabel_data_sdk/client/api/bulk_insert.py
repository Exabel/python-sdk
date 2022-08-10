import logging
from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep, time
from typing import Callable, Optional, Sequence

from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.api.resource_creation_result import (
    ResourceCreationResult,
    ResourceCreationResults,
    ResourceCreationStatus,
    TResource,
)

logger = logging.getLogger(__name__)


class BulkInsertFailedError(Exception):
    """Error indicating that the bulk insert failed."""


def _process(
    results: ResourceCreationResults[TResource],
    resource: TResource,
    insert_func: Callable[[TResource], ResourceCreationStatus],
    abort: Callable,
) -> None:
    """
    Insert the given resource using the provided function.
    Catches and handles RequestErrors.

    Args:
        results:     the result set to append to
        resource:    the resource to be inserted
        insert_func: the function to use to insert the resource
        abort:       the function to call when the insert is aborted
    """
    if results.abort:
        abort()
        return

    try:
        status = insert_func(resource)
        results.add(ResourceCreationResult(status, resource))
    except RequestError as error:
        status = (
            ResourceCreationStatus.EXISTS
            if error.error_type == ErrorType.ALREADY_EXISTS
            else ResourceCreationStatus.FAILED
        )
        results.add(ResourceCreationResult(status, resource, error))
    except TypeError as error:
        # Raised when proto message is not constructable (as a result of invalid argument types).
        request_error = RequestError(ErrorType.INVALID_ARGUMENT, message=str(error))
        results.add(ResourceCreationResult(ResourceCreationStatus.FAILED, resource, request_error))


def _raise_error() -> None:
    """Raise a BulkInsertFailedError."""
    raise BulkInsertFailedError()


def _bulk_insert(
    results: ResourceCreationResults[TResource],
    resources: Sequence[TResource],
    insert_func: Callable[[TResource], ResourceCreationStatus],
    threads: int = 40,
) -> None:
    """
    Calls the provided insert function with each of the provided resources,
    while catching errors and tracking progress.

    Args:
        results:         add the results to this result set
        resources:       the resources to be inserted
        insert_func:     the function to call for each insert.
        threads:         the number of parallel upload threads to use
    """
    if threads == 1:
        for resource in resources:
            _process(results, resource, insert_func, _raise_error)

    else:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for resource in resources:
                if not results.abort:
                    executor.submit(
                        _process,
                        results,
                        resource,
                        insert_func,
                        # Python 3.9 added support for the shutdown argument 'cancel_futures'.
                        # We should set this argument to True once we have moved to this python
                        # version.
                        lambda: executor.shutdown(wait=False),
                    )
        if results.abort:
            raise BulkInsertFailedError()


def _get_backoff(trial: int, min_sleep: float = 1.0, max_sleep: float = 60.0) -> float:
    """Return the backoff in seconds for the given trial."""
    return min(min_sleep * 2**trial, max_sleep)


def bulk_insert(
    resources: Sequence[TResource],
    insert_func: Callable[[TResource], ResourceCreationStatus],
    retries: int = 5,
    threads: int = 40,
    abort_threshold: Optional[float] = 0.5,
) -> ResourceCreationResults[TResource]:
    """
    Calls the provided insert function with each of the provided resources,
    while catching errors and tracking progress.

    Raises a BulkInsertFailedError if more than 50% of the resources fail to insert.

    Args:
        resources:       the resources to be inserted
        insert_func:     the function to call for each insert.
        retries:         the maximum number of retries to make for each failed request
        threads:         the number of parallel upload threads to use
        abort_threshold: the threshold for the proportion of failed requests that will cause the
                         upload to be aborted; if it is `None`, the upload is never aborted

    Returns:
        the result set showing the current status for each insert
    """
    start_time = time()
    results: ResourceCreationResults[TResource] = ResourceCreationResults(
        len(resources), abort_threshold=abort_threshold
    )
    try:
        for trial in range(retries + 1):
            if trial > 0:
                failures = results.extract_retryable_failures()
                if not failures:
                    break
                backoff = _get_backoff(trial)
                logger.info("Sleeping %.2f seconds before retrying failed requests...", backoff)
                sleep(backoff)
                resources = [result.resource for result in failures]
                logger.info("Retry #%d with %d resources:", trial, len(resources))
            _bulk_insert(results, resources, insert_func, threads=threads)
    finally:
        spent_time = int(time() - start_time)
        logger.info(
            "Spent %d seconds loading %d resources (%d threads)",
            spent_time,
            len(resources),
            threads,
        )
        results.print_summary()
    return results
