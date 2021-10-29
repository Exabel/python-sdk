from concurrent.futures.thread import ThreadPoolExecutor
from time import time
from typing import Callable, Sequence

from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.api.resource_creation_result import (
    ResourceCreationResult,
    ResourceCreationResults,
    ResourceCreationStatus,
    TResource,
)


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


def bulk_insert(
    resources: Sequence[TResource],
    insert_func: Callable[[TResource], ResourceCreationStatus],
    retries: int = 2,
    threads: int = 40,
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

    Returns:
        the result set showing the current status for each insert
    """
    start_time = time()
    results: ResourceCreationResults[TResource] = ResourceCreationResults(len(resources))
    try:
        for trial in range(retries + 1):
            if trial > 0:
                failures = results.extract_retryable_failures()
                if not failures:
                    break
                resources = [result.resource for result in failures]
                print(f"Retry #{trial} with {len(resources)} resources:")
            _bulk_insert(results, resources, insert_func, threads=threads)
    finally:
        spent_time = int(time() - start_time)
        print(f"Spent {spent_time} seconds loading {len(resources)} resources ({threads} threads)")
        results.print_summary()
    return results
