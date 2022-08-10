import logging
from collections import Counter
from enum import Enum
from typing import Generic, List, Optional, Sequence, TypeVar

import pandas as pd

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.data_classes.request_error import RequestError

logger = logging.getLogger(__name__)

TResource = TypeVar("TResource", Entity, Relationship, pd.Series)


class ResourceCreationStatus(Enum):
    """
    Status values for resource creation.
    """

    # Denotes that a resource was created.
    CREATED = 1

    # Denotes that a resource already existed.
    EXISTS = 2

    # Denotes that creation failed.
    FAILED = 3

    # Denotes that a resource was upserted.
    UPSERTED = 4


class ResourceCreationResult(Generic[TResource]):
    """
    The status of the creation of a particular resource.
    """

    def __init__(
        self,
        status: ResourceCreationStatus,
        resource: TResource,
        error: RequestError = None,
    ):
        self.status = status
        self.resource: TResource = resource
        self.error = error

    def __repr__(self) -> str:
        return f"ResourceCreationResult{self.status.name, self.resource}"


class ResourceCreationResults(Generic[TResource]):
    """
    Class for returning resource creation results.
    """

    def __init__(
        self, total_count: int, print_status: bool = True, abort_threshold: Optional[float] = 0.5
    ) -> None:
        """
        Args:
            total_count:     The total number of resources expected to be loaded.
            print_status:    Whether to print status of the upload during processing.
            abort_threshold: If the fraction of failed requests exceeds this threshold,
                             the upload is aborted; if it is `None`, the upload is not aborted,
                             regardless of how many errors there are.
        """
        self.results: List[ResourceCreationResult[TResource]] = []
        self.counter: Counter = Counter()
        self.total_count = total_count
        self.do_print_status = print_status
        self.abort_threshold = abort_threshold if abort_threshold is not None else 2
        self.abort = False

    def add(self, result: ResourceCreationResult[TResource]) -> None:
        """Add the result for a resource."""
        self.results.append(result)
        self.counter.update([result.status])
        if self.do_print_status and (
            self.count() % 10_000 == 0 or self.count() == self.total_count
        ):
            self.print_status()
        if self.count() % 20 == 0 and self.count() != self.total_count:
            self.check_failures()

    def count(self, status: ResourceCreationStatus = None) -> int:
        """
        Number of results with the given status,
        or total number of results if no status is specified.
        """
        return len(self.results) if status is None else self.counter[status]

    def has_failure(self) -> bool:
        """Whether this result contains failures."""
        return self.count(ResourceCreationStatus.FAILED) > 0

    def get_failures(self) -> Sequence[ResourceCreationResult[TResource]]:
        """Return all the failed results."""
        return list(filter(lambda r: r.status == ResourceCreationStatus.FAILED, self.results))

    def extract_retryable_failures(self) -> List[ResourceCreationResult[TResource]]:
        """
        Remove all retryable failures from this result set,
        and return them.
        """
        failed = []
        rest = []
        for result in self.results:
            if (
                result.status == ResourceCreationStatus.FAILED
                and result.error
                and result.error.error_type.retryable()
            ):
                failed.append(result)
            else:
                rest.append(result)
        self.counter.subtract([result.status for result in failed])
        self.results = rest
        return failed

    def check_failures(self) -> None:
        """
        Set the member field 'abort' to True if the fraction of errors exceeds the abort threshold.
        """
        fraction_error = self.count(ResourceCreationStatus.FAILED) / self.count()
        if fraction_error > self.abort_threshold and not self.abort:
            self.abort = True
            if self.do_print_status:
                logger.error(
                    "Aborting - more than %.0f of the requests are failing.", self.abort_threshold
                )

    def print_summary(self) -> None:
        """Prints a human legible summary of the resource creation results to screen."""
        if self.counter[ResourceCreationStatus.CREATED]:
            logger.info("%s new resources created", self.counter[ResourceCreationStatus.CREATED])
        if self.counter[ResourceCreationStatus.EXISTS]:
            logger.info("%s resources already existed", self.counter[ResourceCreationStatus.EXISTS])
        if self.counter[ResourceCreationStatus.UPSERTED]:
            logger.info("%s resources upserted", self.counter[ResourceCreationStatus.UPSERTED])
        if self.counter[ResourceCreationStatus.FAILED]:
            logger.warning("%s resources failed", self.counter[ResourceCreationStatus.FAILED])
            for result in self.results:
                if result.status == ResourceCreationStatus.FAILED:
                    logger.warning("   %s\n      %s", result.resource, result.error)

    def print_status(self) -> None:
        """
        Prints a status update on the progress of the data loading, showing the percentage complete
        and how many objects were created, already existed or failed.
        """
        message_parts = []
        fraction_complete = self.count() / self.total_count
        message_parts.append(f"\r{fraction_complete:.0%} - ")
        if self.counter[ResourceCreationStatus.CREATED]:
            message_parts.append(f"{self.count(ResourceCreationStatus.CREATED)} created, ")
        if self.counter[ResourceCreationStatus.UPSERTED]:
            message_parts.append(f"{self.count(ResourceCreationStatus.UPSERTED)} upserted, ")
        if self.counter[ResourceCreationStatus.EXISTS]:
            message_parts.append(f"{self.count(ResourceCreationStatus.EXISTS)} exists, ")
        message_parts.append(f"{self.count(ResourceCreationStatus.FAILED)} failed")
        logger.info("".join(message_parts))
