import logging
from concurrent.futures import ThreadPoolExecutor
from time import sleep, time
from typing import Callable, Optional, Sequence

from exabel_data_sdk.client.api.bulk_insert import (
    BulkInsertFailedError,
    _bulk_insert,
    _get_backoff,
    _raise_error,
)
from exabel_data_sdk.client.api.data_classes.request_error import RequestError
from exabel_data_sdk.client.api.resource_creation_result import (
    ResourceCreationResult,
    ResourceCreationResults,
    ResourceCreationStatus,
    TResource,
)

logger = logging.getLogger(__name__)


def _bulk_insert_with_retry(
    resources: Sequence[TResource],
    results: ResourceCreationResults[TResource],
    insert_func: Callable[[TResource], ResourceCreationStatus],
    retries: int,
    threads: int,
) -> None:
    """Insert a batch of resources divided from a sequence of resources.

    Calls the provided insert function with each of the provided resources,
    while catching errors and tracking progress.
    Values of arguments are inherited from function bulk_insert(...)
    """
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


def _process_batch_import(
    results: ResourceCreationResults[TResource],
    resources_batch: Sequence[TResource],
    import_func: Callable[[Sequence[TResource]], Sequence[ResourceCreationStatus]],
    insert_func: Callable[[TResource], ResourceCreationStatus],
    threads_for_insert_func: int,
    retries: int,
    abort: Callable,
) -> None:
    """Import batch of resources.

    If failed, the batch will be managed by function bulk_insert(...).

    Args:
        results:     The result set to append to.
        resources_batch:
                     The batch of resources to be imported.
        insert_func: The function to use to import the batch.
        abort:       The function to call when the insert is aborted.
    """
    if results.abort:
        abort()
        return
    try:
        statuses_batch = import_func(resources_batch)
        for resource, status in zip(resources_batch, statuses_batch):
            results.add(ResourceCreationResult(status, resource))
    except (RequestError, TypeError):
        _bulk_insert_with_retry(
            resources=resources_batch,
            results=results,
            insert_func=insert_func,
            retries=retries,
            threads=threads_for_insert_func,
        )


def bulk_import(
    resources_batches: Sequence[Sequence[TResource]],
    import_func: Callable[[Sequence[TResource]], Sequence[ResourceCreationStatus]],
    insert_func: Callable[[TResource], ResourceCreationStatus],
    threads_for_import_func: int = 4,
    threads_for_insert_func: int = 4,
    retries: int = 5,
    abort_threshold: Optional[float] = 0.5,
) -> ResourceCreationResults[TResource]:
    """Import a series of batches of resources.

    For each batch, the provided import_func is called to import its resources.

    If a batch fails, the provided insert_func will be called to insert the resources,
    while catching errors and tracking progress.

    Raises a BulkInsertFailedError if more than 50% of the resources fail to insert.

    Args:
        resources_batches:  The batches of resources to be inserted.
        import_func:        The function to call for each import.
        insert_func:        The function to call for each insert.
        threads_for_import_func:
                            The number of parallel import threads to use.
        threads_for_insert_func:
                            The number of parallel upload threads to use.
        retries:            The maximum number of retries to run the provided insert_func for each
                            failed batch. The import_func will never be retried.
        abort_threshold:    The threshold for the proportion of failed requests that will cause the
                            upload to be aborted; if it is `None`, the upload is never aborted.


    Returns:
        The result set showing the current status for each insert.
    """
    start_time: float
    start_time = time()
    results: ResourceCreationResults[TResource] = ResourceCreationResults(
        total_count=sum(len(batch) for batch in resources_batches),
        abort_threshold=abort_threshold,
    )
    _bulk_import(
        results,
        resources_batches,
        import_func,
        insert_func,
        threads_for_import_func,
        threads_for_insert_func,
        retries,
    )
    spent_time = int(time() - start_time)
    logger.info(
        "Spent %d seconds loading %d resources (%d threads)",
        spent_time,
        sum([len(rb) for rb in resources_batches]),
        threads_for_import_func,
    )
    results.print_summary()
    return results


def _bulk_import(
    results: ResourceCreationResults[TResource],
    resources_batches: Sequence[Sequence[TResource]],
    import_func: Callable[[Sequence[TResource]], Sequence[ResourceCreationStatus]],
    insert_func: Callable[[TResource], ResourceCreationStatus],
    threads_for_import_func: int,
    threads_for_insert_func: int,
    retries: int,
) -> None:
    if threads_for_import_func == 1:
        for r_b in resources_batches:
            _process_batch_import(
                results,
                r_b,
                import_func,
                insert_func,
                threads_for_insert_func,
                retries,
                _raise_error,
            )

    else:
        with ThreadPoolExecutor(max_workers=threads_for_import_func) as executor:
            for r_b in resources_batches:
                if not results.abort:
                    executor.submit(
                        _process_batch_import,
                        results,  # type: ignore[arg-type]
                        r_b,  # type: ignore[arg-type]
                        import_func,  # type: ignore[arg-type]
                        insert_func,  # type: ignore[arg-type]
                        threads_for_insert_func,
                        retries,
                        # Python 3.9 added support for the shutdown argument 'cancel_futures'.
                        # We should set this argument to True once we have moved to this python
                        # version.
                        lambda: executor.shutdown(wait=False),
                    )
        if results.abort:
            raise BulkInsertFailedError()
