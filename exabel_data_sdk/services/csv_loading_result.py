from typing import Generic, Optional, Sequence, TypeVar

import pandas as pd

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.resource_creation_result import ResourceCreationResults

TResource = TypeVar("TResource", Entity, Relationship, pd.Series)


class CsvLoadingResult(Generic[TResource]):
    """
    Contains a summary of the results of uploading data from a CSV file.

    Attributes:
        results: the individual uploading results for all the resources; `None` if uploading was
            aborted or it was a dry run
        warnings: a list of warnings
        aborted: whether uploading was aborted
    """

    def __init__(
        self,
        results: ResourceCreationResults[TResource] = None,
        *,
        warnings: Sequence[str] = None,
        aborted: bool = False,
    ):
        self.results: Optional[ResourceCreationResults[TResource]] = results
        self.warnings = warnings or []
        self.aborted = aborted
