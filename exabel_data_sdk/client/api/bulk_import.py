import logging
from collections.abc import Sequence as SequenceABC
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from itertools import chain
from time import sleep, time
from typing import Callable, Generic, Mapping, Optional, Sequence

import pandas as pd

from exabel_data_sdk.client.api.bulk_insert import BulkInsertFailedError, _get_backoff, _raise_error
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError, Violation
from exabel_data_sdk.client.api.data_classes.time_series import TimeSeriesResourceName
from exabel_data_sdk.client.api.resource_creation_result import (
    ResourceCreationResult,
    ResourceCreationResults,
    ResourceCreationStatus,
    ResourceT,
)
from exabel_data_sdk.services.csv_loading_constants import MAX_THREADS_FOR_IMPORT
from exabel_data_sdk.util.deprecate_arguments import deprecate_arguments
from exabel_data_sdk.util.import_ import get_batches_for_import

logger = logging.getLogger(__name__)


@dataclass
class ResourceFailureHandler(Generic[ResourceT]):
    """Handles resource failures."""

    request_error: RequestError

    def __post_init__(self) -> None:
        precondition_failure = self.request_error.precondition_failure
        self._violations = {}
        if precondition_failure and precondition_failure.violations:
            self._violations = {
                violation.subject: violation for violation in precondition_failure.violations
            }

    @staticmethod
    def get_time_series_result_from_violations(
        resource: pd.Series, violations: Mapping[str, Violation]
    ) -> ResourceCreationResult[pd.Series]:
        """Get a time series creation result from precondition failure violations."""
        resource_name = TimeSeriesResourceName.from_string(resource.name)
        entity_name = resource_name.entity_name
        signal_name = resource_name.signal_name
        if entity_name not in violations and signal_name not in violations:
            retryable_error = RequestError(ErrorType.INTERNAL)
            return ResourceCreationResult(ResourceCreationStatus.FAILED, resource, retryable_error)

        violation = violations.get(entity_name) or violations.get(signal_name)
        assert violation is not None, "Violation subject is neither an entity nor a signal"
        error_type = ErrorType.from_precondition_failure_violation_type(violation.type)
        non_retryable_error = RequestError(error_type, violation.description)
        return ResourceCreationResult(
            ResourceCreationStatus.FAILED,
            resource,
            non_retryable_error,
        )

    @classmethod
    def get_result_from_violations(
        cls, resource: ResourceT, violations: Mapping[str, Violation]
    ) -> ResourceCreationResult[ResourceT]:
        """Get a resource creation result from precondition failure violations."""
        if isinstance(resource, pd.Series):
            return cls.get_time_series_result_from_violations(resource, violations)
        raise NotImplementedError(
            f"Handling precondition failure violations for resource type {resource.__class__} is "
            "not implemented."
        )

    def get_resource_creation_result(
        self,
        resource: ResourceT,
    ) -> ResourceCreationResult[ResourceT]:
        """Get the creation result for a resource."""
        if self._violations:
            return self.get_result_from_violations(resource, self._violations)
        if self.request_error.error_type == ErrorType.ALREADY_EXISTS:
            return ResourceCreationResult(ResourceCreationStatus.EXISTS, None, self.request_error)
        return ResourceCreationResult(ResourceCreationStatus.FAILED, resource, self.request_error)


def _process(
    results: ResourceCreationResults[ResourceT],
    resources: Sequence[ResourceT],
    import_func: Callable[[Sequence[ResourceT]], Sequence[ResourceCreationStatus]],
    abort: Callable,
) -> None:
    """
    Import a sequence of resources using the provided function. Catches and handles RequestErrors.

    Args:
        results:     The result set to append to.
        resources:
                     The batch of resources to be imported.
        import_func: The function to call to import the resources.
        abort:       The function to call when the insert is aborted.
    """
    if results.abort:
        abort()
        return
    try:
        statuses_batch = import_func(resources)
        for resource, status in zip(resources, statuses_batch):
            results.add(ResourceCreationResult(status, resource))
    except RequestError as error:
        failure_handler = ResourceFailureHandler(error)
        for resource in resources:
            results.add(failure_handler.get_resource_creation_result(resource))
    except TypeError as error:
        # Raised when proto message is not constructable (as a result of invalid argument types).
        for resource in resources:
            request_error = RequestError(ErrorType.INVALID_ARGUMENT, message=str(error))
            results.add(
                ResourceCreationResult(ResourceCreationStatus.FAILED, resource, request_error)
            )


@deprecate_arguments(
    resources_batches="resources",
    threads_for_import_func="threads",
    threads_for_insert_func=None,
    insert_func=None,
)
def bulk_import(
    resources: Sequence[ResourceT],
    import_func: Callable[[Sequence[ResourceT]], Sequence[ResourceCreationStatus]],
    threads: int = 4,
    retries: int = 5,
    abort_threshold: Optional[float] = 0.5,
    # Deprecated arguments
    resources_batches: Optional[  # pylint: disable=unused-argument
        Sequence[Sequence[ResourceT]]
    ] = None,
    threads_for_import_func: Optional[int] = None,  # pylint: disable=unused-argument
    threads_for_insert_func: Optional[int] = None,  # pylint: disable=unused-argument
    insert_func: Optional[  # pylint: disable=unused-argument
        Callable[[ResourceT], ResourceCreationStatus]
    ] = None,
) -> ResourceCreationResults[ResourceT]:
    """
    Call the provided import function with batches of the provided resources, while catching errors
    and tracking progress.

    Raise a BulkInsertFailedError if more than 50% of the resources fail to insert.

    Args:
        resources:          The resources to be imported.
        import_func:        The function to call for each import.
        threads:            The number of parallel import threads to use.
        retries:            The maximum number of retries to make for each failed request.
        abort_threshold:    The threshold for the proportion of failed requests that will cause the
                            upload to be aborted; if it is `None`, the upload is never aborted.

    Returns:
        The result set showing the current status for each insert.
    """
    if threads > MAX_THREADS_FOR_IMPORT:
        logger.info(
            "Maximum number of threads for time series upload is %d. Using %d threads.",
            MAX_THREADS_FOR_IMPORT,
            MAX_THREADS_FOR_IMPORT,
        )
        threads = MAX_THREADS_FOR_IMPORT
    # For backwards compatibility, in case resources are pre-batched.
    if resources and isinstance(resources[0], SequenceABC):
        resources = list(chain.from_iterable(resources))  # type: ignore[arg-type]
    start_time: float
    start_time = time()
    results: ResourceCreationResults[ResourceT] = ResourceCreationResults(
        total_count=len(resources),
        abort_threshold=abort_threshold,
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
                resources = [result.resource for result in failures if result.resource is not None]
                logger.info("Retry #%d with %d resources:", trial, len(resources))
            _bulk_import(results, resources, import_func, threads=threads)
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


def _bulk_import(
    results: ResourceCreationResults[ResourceT],
    resources: Sequence[ResourceT],
    import_func: Callable[[Sequence[ResourceT]], Sequence[ResourceCreationStatus]],
    threads: int,
) -> None:
    """
    Call the provided import function with batches of the provided resources, while catching errors
    and tracking progress.

    Args:
        results:        Add the results to this result set.
        resources:      The resources to be imported.
        import_func:    The function to call for each batch of resources.
        threads:        The number of parallel upload threads to use.
    """
    resource_batches = get_batches_for_import(resources)
    if threads == 1:
        for resource_batch in resource_batches:
            _process(
                results,
                resource_batch,
                import_func,
                _raise_error,
            )

    else:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for resource_batch in resource_batches:
                if not results.abort:
                    # The generic type hints do not guarantee that TResource refers to the same
                    # class for each of the three parameters. This leads to mypy warnings for the
                    # following function call.
                    executor.submit(
                        _process,
                        results,  # type: ignore[arg-type]
                        resource_batch,
                        import_func,  # type: ignore[arg-type]
                        # Python 3.9 added support for the shutdown argument 'cancel_futures'.
                        # We should set this argument to True once we have moved to this python
                        # version.
                        lambda: executor.shutdown(wait=False),
                    )
        if results.abort:
            raise BulkInsertFailedError()
