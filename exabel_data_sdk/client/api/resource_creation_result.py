from __future__ import annotations

import logging
from collections import Counter
from enum import Enum
from typing import Generic, MutableSequence, Optional, Sequence, Set, TypeVar

import numpy as np
import pandas as pd

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.data_classes.request_error import RequestError
from exabel_data_sdk.services.csv_loading_constants import DEFAULT_BULK_LOAD_CHECKPOINTS

logger = logging.getLogger(__name__)

ResourceT = TypeVar("ResourceT", Entity, Relationship, pd.Series)


def get_resource_name(resource: ResourceT) -> str:
    """Get the name of a resource."""
    if isinstance(resource, Entity):
        return resource.name
    if isinstance(resource, Relationship):
        return f"{resource.relationship_type}/{resource.from_entity}/{resource.to_entity}"
    if isinstance(resource, pd.Series):
        return resource.name
    raise TypeError(f"Unknown resource type: {type(resource)}")


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


class ResourceCreationResult(Generic[ResourceT]):
    """
    The status of the creation of a particular resource.
    """

    def __init__(
        self,
        status: ResourceCreationStatus,
        resource: ResourceT,
        error: Optional[RequestError] = None,
    ):
        self.status = status
        self.resource: Optional[ResourceT] = (
            None if status != ResourceCreationStatus.FAILED else resource
        )
        self.resource_name = get_resource_name(resource)
        self.error = error

    def __repr__(self) -> str:
        return f"ResourceCreationResult{self.status.name, self.resource}"

    def get_printable_resource(self) -> str:
        """
        Return a printable resource representation string. Return only the name of the series for
        ResourceCreationResult of type pd.Series
        """
        return self.resource.name if isinstance(self.resource, pd.Series) else self.resource

    def get_printable_error(self) -> str:
        """
        Return a printable request error message if it is set, otherwise return the string
        representation of the error
        """
        return self.error.message if self.error and self.error.message else str(self.error)


class ResourceCreationResults(Generic[ResourceT]):
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
        self.results: MutableSequence[ResourceCreationResult[ResourceT]] = []
        self.counter: Counter = Counter()
        self.total_count = total_count
        self.do_print_status = print_status
        self.abort_threshold = abort_threshold if abort_threshold is not None else 2
        self.abort = False
        self.progress_checkpoints = self._get_progress_checkpoints(
            total_count, DEFAULT_BULK_LOAD_CHECKPOINTS
        )

    @staticmethod
    def _get_progress_checkpoints(total: int, checkpoints: int) -> Set[int]:
        """
        Return a list of progress checkpoints.
        """
        start = total // checkpoints
        return set(np.linspace(start, total, checkpoints, dtype=int))

    def update(self, other: ResourceCreationResults[ResourceT]) -> None:
        """
        Update this result set with the results from another result set.
        """
        self.results.extend(other.results)
        self.counter.update(other.counter)
        self.total_count += other.total_count

    def add(self, result: ResourceCreationResult[ResourceT]) -> None:
        """Add the result for a resource."""
        self.results.append(result)
        self.counter.update([result.status])
        count = self.count()
        if count in self.progress_checkpoints:
            if self.do_print_status:
                self.print_status()
            # For very small uploads, we don't want to abort too early if there are a few errors.
            if count > 20 and count != self.total_count:
                self.check_failures()

    def count(self, status: Optional[ResourceCreationStatus] = None) -> int:
        """
        Number of results with the given status,
        or total number of results if no status is specified.
        """
        return len(self.results) if status is None else self.counter[status]

    def has_failure(self) -> bool:
        """Whether this result contains failures."""
        return self.count(ResourceCreationStatus.FAILED) > 0

    def get_failures(self) -> Sequence[ResourceCreationResult[ResourceT]]:
        """Return all the failed results."""
        return list(filter(lambda r: r.status == ResourceCreationStatus.FAILED, self.results))

    def extract_retryable_failures(self) -> Sequence[ResourceCreationResult[ResourceT]]:
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
                    logger.warning(
                        "   %s\n      %s",
                        result.get_printable_resource(),
                        result.get_printable_error(),
                    )

    def print_status(self) -> None:
        """
        Prints a status update on the progress of the data loading, showing the percentage complete
        and how many objects were created, already existed or failed.
        """
        message_parts = []
        fraction_complete = self.count() / self.total_count
        message_parts.append(f"{fraction_complete:.0%} - ")
        if self.counter[ResourceCreationStatus.CREATED]:
            message_parts.append(f"{self.count(ResourceCreationStatus.CREATED)} created, ")
        if self.counter[ResourceCreationStatus.UPSERTED]:
            message_parts.append(f"{self.count(ResourceCreationStatus.UPSERTED)} upserted, ")
        if self.counter[ResourceCreationStatus.EXISTS]:
            message_parts.append(f"{self.count(ResourceCreationStatus.EXISTS)} exists, ")
        message_parts.append(f"{self.count(ResourceCreationStatus.FAILED)} failed")
        logger.info("".join(message_parts))
