from dataclasses import dataclass
from typing import Generic, Mapping, Optional, Sequence, TypeVar

import pandas as pd

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.resource_creation_result import ResourceCreationResults

TResource = TypeVar("TResource", Entity, Relationship, pd.Series)


@dataclass
class EntityMappingResult:
    """
    Contains results of mapping entities in an input file to entities in the platform.

    Attributes:
        mapping:         a mapping from the input identifier to a platform entity resource name
        identifier_type: the type of the identifiers found in the input file
        entity_names:    the entity names, after any mapping is applied
    """

    mapping: Mapping[str, str]
    identifier_type: str
    entity_names: Sequence[str]
    unmapped_entity_queries: Sequence[str]


class FileLoadingResult(Generic[TResource]):
    """
    Contains a summary of the results of uploading data from a data file.

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


class TimeSeriesFileLoadingResult(FileLoadingResult[pd.Series]):
    """
    Contains a summary of the results of uploading data from a data file.

    Attributes:
        results:                the individual uploading results for all the resources; `None` if
                                uploading was aborted or it was a dry run
        warnings:               a list of warnings
        aborted:                whether uploading was aborted
        entity_mapping_result:  results of mapping entities in the input file
        created_data_signals:   resource names of data API signals which did not exist from before
        dry_run_results:        resource names of resources which would be created in case of a dry
                                run
        sheet_name:             the name of the sheet, when applicable
        has_known_time:         whether the file contained a column specifying the known time
    """

    def __init__(
        self,
        results: ResourceCreationResults[pd.Series] = None,
        *,
        warnings: Sequence[str] = None,
        aborted: bool = False,
        entity_mapping_result: EntityMappingResult = None,
        created_data_signals: Sequence[str] = None,
        dry_run_results: Sequence[str] = None,
        sheet_name: str = None,
        has_known_time: bool = False,
    ):
        super().__init__(results, warnings=warnings, aborted=aborted)
        if entity_mapping_result is None:
            raise ValueError("Entity mapping result must be set.")
        self.entity_mapping_result = entity_mapping_result
        if created_data_signals is None:
            raise ValueError("List of created data API signals must be set.")
        self.created_data_signals = created_data_signals
        self.dry_run_results = dry_run_results
        self.sheet_name = sheet_name
        self.has_known_time = has_known_time
