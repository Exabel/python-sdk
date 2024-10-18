import argparse
from typing import Iterable, Sequence, Union

from tqdm import tqdm

PAGE_SIZE = 1000
MAX_WORKERS = 10
SUCCESS = 0
ERROR = 1
TQDM_BAR_FORMAT = (
    "{l_bar}{bar} | Pages: {n_fmt}/{total_fmt} [Time - Remaining: {remaining} Elapsed: {elapsed}]"
)
NCOLS = 100

ID_EXAMPLE_MAP = {
    "entityTypes": "brand",
    "dataSets": "transactions",
    "signals": "spend",
    "relationshipTypes": "HAS_BRAND",
}


def conditional_progress_bar(
    iterable: Iterable, show_progress: bool = False, **kwargs: Union[str, int]
) -> Iterable:
    """
    Returns a tqdm progress bar if show_progress is True, otherwise returns the iterable unchanged.
    """
    if show_progress:
        return tqdm(iterable, ncols=NCOLS, bar_format=TQDM_BAR_FORMAT, **kwargs)
    return iterable


def parse_resource_name(argument: str, resource_type: str) -> str:
    """
    Parses a resource name argument for a given resource type.

    Args:
        argument: The input argument to parse.
        resource_type: The type of resource (e.g., 'dataSets', 'signals').
    """
    if argument.startswith(f"{resource_type}/"):
        return argument
    if "/" in argument:
        id_example = ID_EXAMPLE_MAP[resource_type]
        raise argparse.ArgumentTypeError(
            f"Invalid {resource_type[:-1]} resource name '{argument}', "
            f"valid formats: '{resource_type}/ns.{id_example}' or 'ns.{id_example}'"
        )
    return f"{resource_type}/{argument}"


def data_set_resource_name(argument: str) -> str:
    """
    Parses a data set resource name argument. E.g., 'dataSets/ns.dataset1'.
    """
    return parse_resource_name(argument, "dataSets")


def relationship_type_resource_name(argument: str) -> str:
    """
    Parses a relationship type resource name argument. E.g., 'relationshipTypes/ns.HAS_BRAND'.
    """
    return parse_resource_name(argument, "relationshipTypes")


def entity_type_resource_name(argument: str) -> str:
    """
    Parses an entity type resource name argument. E.g., 'entityTypes/ns.brand'.
    """
    return parse_resource_name(argument, "entityTypes")


def entity_resource_name(argument: str) -> str:
    """
    Parses an entity resource name argument. E.g., 'entityTypes/ns.brand/entities/ns.brand1'.
    """
    elements = argument.split("/")
    if len(elements) != 4 or elements[0] != "entityTypes" or elements[2] != "entities":
        if not argument.startswith("entityTypes/") and len(elements) == 3:
            return entity_resource_name(f"entityTypes/{argument}")
        raise ValueError(f"Invalid resource name: {argument}")

    return argument


def signal_resource_name(argument: str) -> str:
    """
    Parses a signal resource name argument. E.g., 'signals/ns.signal1'.
    """
    return parse_resource_name(argument, "signals")


def time_series_resource_name(argument: str) -> str:
    """
    Parses a time series resource name argument.
    E.g., 'entityTypes/ns.brand/entities/ns.brand1/signals/ns.signal1'.
    """
    elements = argument.split("/")
    if (
        len(elements) != 6
        or elements[0] != "entityTypes"
        or elements[2] != "entities"
        or elements[4] != "signals"
    ):
        raise ValueError(f"Invalid resource name: {argument}")
    return argument


def read_signals_from_file(file_name: str) -> Sequence[str]:
    """
    Reads a list of signal resource name from a file which has one per line.
    """
    signals = []
    with open(file_name, "r", encoding="utf-8") as signals_file:
        for line in signals_file:
            if line.strip():
                signals.append(signal_resource_name(line.strip()))
    return signals
