from typing import MutableSequence, Sequence

import pandas as pd

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.resource_creation_result import ResourceT


def get_batches_for_import(resources: Sequence[ResourceT]) -> Sequence[Sequence[ResourceT]]:
    """
    Split the given sequence of resources into batches of resources where each batch can be sent in
    a single import request.

    The goal is to create batches such that the size of the request for each batch does not exceed
    1MB.
    """
    all_batches = []
    current_batch: MutableSequence[pd.Series] = []
    current_size = 0
    one_mb = 2**20
    for s in resources:
        size = estimate_size(s)
        if current_size + size > one_mb and current_size > 0:
            all_batches.append(current_batch)
            current_batch = [s]
            current_size = size
        else:
            current_size += size
            current_batch.append(s)
    all_batches.append(current_batch)
    return all_batches


def estimate_size(resource: ResourceT) -> int:
    """
    Estimate how many bytes the given resource will add to an import request.
    """
    if isinstance(resource, (Entity, Relationship)):
        raise NotImplementedError("Cannot estimate size for entities and relationships.")

    # 1 byte for each character in the time series name
    # + 27/19 bytes for each data point (depends on whether known-time is specified)
    # + 7 bytes overhead.
    has_known_time = isinstance(resource.index, pd.MultiIndex)
    return len(str(resource.name)) + (27 if has_known_time else 19) * len(resource) + 7
