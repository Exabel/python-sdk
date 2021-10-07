import sys
from collections import Counter
from enum import Enum
from typing import Generic, List, TypeVar

import pandas as pd

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.data_classes.request_error import RequestError

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


class ResourceCreationResult(Generic[TResource]):
    """
    The status of the creation of a particular resource.
    """

    def __init__(
        self, status: ResourceCreationStatus, resource: TResource, error: RequestError = None
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

    def __init__(self) -> None:
        self.results: List[ResourceCreationResult[TResource]] = []
        self.counter: Counter = Counter()

    def add(self, result: ResourceCreationResult[TResource]) -> None:
        """Add the result for a resource."""
        self.results.append(result)
        self.counter.update([result.status])

    def count(self, status: ResourceCreationStatus = None) -> int:
        """
        Number of results with the given status,
        or total number of results if no status is specified.
        """
        return len(self.results) if status is None else self.counter[status]

    def print_summary(self) -> None:
        """Prints a human legible summary of the resource creation results to screen."""
        print(self.counter[ResourceCreationStatus.CREATED], "new resources created")
        print(self.counter[ResourceCreationStatus.EXISTS], "resources already existed")
        if self.counter[ResourceCreationStatus.FAILED]:
            print(self.counter[ResourceCreationStatus.FAILED], "resources failed:")
            for result in self.results:
                if result.status == ResourceCreationStatus.FAILED:
                    print("   ", result.resource, ":\n      ", result.error)


def status_callback(results: ResourceCreationResults, total_count: int) -> None:
    """
    Prints a status update on the progress of the data loading, showing the percentage complete
    and how many objects were created, already existed or failed.

    Note that the previous status message is overwritten (by writing '\r'),
    but this only works if nothing else has been printed to stdout since the last update.
    """
    fraction_complete = results.count() / total_count
    sys.stdout.write(
        f"\r{fraction_complete:.0%} - "
        f"{results.count(ResourceCreationStatus.CREATED)} created, "
        f"{results.count(ResourceCreationStatus.EXISTS)} exists, "
        f"{results.count(ResourceCreationStatus.FAILED)} failed"
    )
    if fraction_complete == 1:
        sys.stdout.write("\n")
    fraction_error = results.count(ResourceCreationStatus.FAILED) / results.count()
    if fraction_error > 0.5:
        sys.stdout.write("\nAborting - more than half the requests are failing.\n")
        results.print_summary()
        sys.exit(-1)
    sys.stdout.flush()
