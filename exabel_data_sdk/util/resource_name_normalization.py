import logging
import re
from collections import deque
from typing import Deque, Iterator, List, Mapping, MutableMapping, NamedTuple, Sequence

import pandas as pd

from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import SearchTerm
from exabel_data_sdk.util.batcher import batcher

logger = logging.getLogger(__name__)

MAX_SEARCH_TERMS = 1000


def normalize_resource_name(name: str) -> str:
    """
    Turn a non-empty string into a legal resource name by applying the following steps:
     - Replace all illegal characters with an underscore
     - Turn multiple consecutive underscores into one
     - Cut at length at most 64 characters
    """
    # Cannot be empty
    if not name or pd.isna(name):
        raise ValueError("Cannot have an empty resource name.")
    # Only letters, numbers, underscore, and dash
    p = re.compile(r"[^a-zA-Z0-9_\-]")
    name = p.sub("_", name)
    # Cannot start with a dash
    if name[0] == "-":
        name = "_" + name[1:]
    # Prettify by turning multiple consecutive underscores into one
    name = re.compile(r"__+").sub("_", name)
    # At most 64 characters
    name = name[:64]
    return name


def _assert_no_collision(mapping: Mapping[str, str]) -> None:
    """
    Verify that the normalization of identifiers hasn't introduced any name collisions.
    If there are collisions, a message is printed informing about the collisions,
    and the script exits with an error code of 1.

    Args:
        mapping: a map from external identifier to a normalized resource name

    Raises:
        SystemExit if there are two identifiers that map to the same resource name
    """
    series = pd.Series(mapping)
    duplicates = series[series.duplicated(keep=False)]
    if duplicates.empty:
        # No duplicates, all good
        return
    logger.error("The normalization of identifiers have introduced resource name collisions.")
    logger.error("The collisions are shown below.")
    logger.error("Please fix these duplicates, and then re-run the script.")
    pd.set_option("max_colwidth", 1000)
    logger.error(duplicates.sort_values().to_string())
    raise ValueError("Resource name collisions detected")


class EntityResourceNames(NamedTuple):
    """
    Identified resource names along with warnings regarding entities that could not be uniquely
    identified.
    """

    names: pd.Series
    warnings: Sequence[str]


def _validate_mic_ticker(mic_ticker: str) -> bool:
    """
    Validate MIC and ticker by the presence of a single colon (:) character.

    Returns:
        `True` if the given MIC and ticker are valid, `False` otherwise
    """
    valid = len(mic_ticker) >= 3 and mic_ticker[1:-1].count(":") == 1
    if not valid:
        logger.warning(
            "mic:ticker must contain exactly one colon (:), and both 'mic' and 'ticker' must "
            "contain at least one character, but got: %s",
            mic_ticker,
        )
    return valid


def to_entity_resource_names(
    entity_api: EntityApi,
    identifiers: pd.Series,
    namespace: str = None,
    entity_mapping: Mapping[str, Mapping[str, str]] = None,
    check_entity_types: bool = True,
) -> EntityResourceNames:
    """
    Turns the given identifiers into entity resource names.

    The name of the given series is used to determine what kind of identifier it is.
    These are the legal series names, and how each case is handled:

     - entity (or entity_from or entity_to)
        The given identifiers are the entity resource names.
        The identifiers are returned unaltered.

     - isin
        The given identifiers are ISIN numbers.
        The ISIN numbers are looked up with the Exabel API, and the Exabel resource identifiers
        for the associated companies are returned.

     - factset_identifier
        The given identifiers are FactSet IDs.
        The identifiers are looked up with the Exabel API, and the Exabel resource identifiers
        are returned.

     - bloomberg_symbol
        The given identifiers are Bloomberg symbols.
        The tickers are looked up with the Exabel API, and the Exabel resource identifiers
        are returned.

     - bloomberg_ticker
        The given identifiers are Bloomberg tickers.
        The tickers are looked up with the Exabel API, and the Exabel resource identifiers
        are returned.

     - figi
        The given identifiers are FIGIs (Financial Instrument Global Identifiers).
        The FIGIs are looked up with the Exabel API, and the Exabel resource identifiers
        are returned.

     - mic:ticker
        The given identifiers are the combination of MIC and stock ticker, separated by a colon.
        MIC is the Market Identifier Code of the stock exchange where the stock is traded under
        the given ticker.
        The MIC/ticker combinations are looked up with the Exabel API, and the Exabel resource
        identifiers are returned.
        Examples:
            XNAS:AAPL refers to Apple, Inc. on NASDAQ
            XNYS:GE refers to General Electric Co. on the New York Stock Exchange
            XOSL:TEL refers to Telenor ASA on the Oslo Stock Exchange

     - any known entity type, e.g. "brand" or "product_type":
        The given identifiers are customer provided names.
        The names are first normalized (using the normalize_resource_name method)
        and then a full resource identifier is constructed on this form:
            entityTypes/{entityType}/entities/{namespace}.{normalized_name}
        for example:
            entityTypes/brand/entities/acme.Spring_Vine
        If the entity type is read-only, e.g. "country" or "currency", the namespace is
        not added to the resource identifier.
        For example:
            entityTypes/country/entities/I_DE

    It is also possible to override the normalisation and search with the provided
    `entity_mapping`. This is useful when the Exabel API is not able to find the corresponding
    entity for an identifier, or one wants to hard map an identifier to a specific entity.

    Returns:
        a tuple containing:
            * a Series with the same index as the input Series, where any identifier that could not
              be mapped is set to None
            * a sequence of warnings for entities that could not be uniquely identified
    """
    warnings: List[str] = []
    name = identifiers.name
    if name in ("entity", "entity_from", "entity_to"):
        # Already resource identifiers, nothing to be done
        return EntityResourceNames(identifiers, warnings)

    unique_ids = identifiers.unique().tolist()
    mapping: MutableMapping[str, str] = {}
    if entity_mapping and entity_mapping.get(name):
        mapping.update(entity_mapping[name])
        unique_ids = [unique_id for unique_id in unique_ids if unique_id not in mapping]

    if name in (
        "isin",
        "factset_identifier",
        "bloomberg_symbol",
        "bloomberg_ticker",
        "mic:ticker",
        "figi",
    ):
        # A company identifier
        logger.info("Looking up %d %ss...", len(unique_ids), name)
        # Skip empty identifiers
        non_empty_identifiers: Iterator[str] = (
            identifier for identifier in unique_ids if identifier and not pd.isna(identifier)
        )
        no_search_terms = MAX_SEARCH_TERMS
        if name == "mic:ticker":
            # mic and ticker takes up to two search terms
            no_search_terms = no_search_terms // 2
            non_empty_identifiers = filter(_validate_mic_ticker, non_empty_identifiers)
        for identifier_batch in batcher(non_empty_identifiers, no_search_terms):
            search_terms: Deque[SearchTerm] = deque()
            for identifier in identifier_batch:
                if name == "mic:ticker":
                    parts = identifier.split(":")
                    search_terms.extend(
                        [
                            SearchTerm(field="mic", query=parts[0]),
                            SearchTerm(field="ticker", query=parts[1]),
                        ]
                    )
                else:
                    search_terms.append(SearchTerm(field=name, query=identifier))
            search_results = entity_api.search.entities_by_terms(
                entity_type="entityTypes/company", terms=search_terms
            )
            for identifier, search_result in zip(identifier_batch, search_results):
                entities = search_result.entities
                pretty_terms = {
                    search_term.field: search_term.query for search_term in search_result.terms
                }
                if not entities:
                    warning = f"Did not find any match for {pretty_terms}"
                    logger.warning(warning)
                    warnings.append(warning)
                elif len(entities) > 1:
                    warning = f"Found {len(entities)} matches for {pretty_terms}:\n  {entities}"
                    logger.warning(warning)
                    warnings.append(warning)
                else:
                    mapping[identifier] = entities[0].name
        logger.info("Found a match for %d %ss.", len(mapping), name)

    else:
        # Should be a known entity type
        entity_type_name = f"entityTypes/{name}"
        entity_type = entity_api.get_entity_type(entity_type_name)
        entity_types = entity_api.list_entity_types()
        read_only_entity_type_names = [
            entity_type.name for entity_type in entity_types if entity_type.read_only
        ]
        if check_entity_types and not entity_type:
            message = f"Failure: Did not find entity type {entity_type_name}"
            logger.error(message)
            logger.error("Available entity types are:")
            logger.error(entity_api.list_entity_types())
            raise ValueError(message)

        if namespace is None:
            prefix = ""
        elif entity_type_name in read_only_entity_type_names:
            prefix = ""
        else:
            if "." in namespace:
                raise ValueError(f"Namespace cannot contain periods (.), got {namespace}")
            prefix = f"{namespace}."

        mapping.update(
            {
                identifier: (
                    f"{entity_type_name}/entities/{prefix}{normalize_resource_name(identifier)}"
                )
                for identifier in unique_ids
                if identifier
            }
        )
        _assert_no_collision(mapping)

    result = identifiers.map(mapping)
    result.name = "entity"
    return EntityResourceNames(result, warnings)


def validate_signal_name(name: str) -> None:
    """
    Validate that the given signal name is a legal signal name. A signal name is a string that
    starts with a letter, and can contain letters, numbers, and underscores.
    """
    if not name:
        raise ValueError("Signal name cannot be empty")
    if len(name) > 64:
        raise ValueError(f'Signal name cannot be longer than 64 characters, but got "{name}"')
    if not re.match(r"^[a-zA-Z]\w{0,63}$", name):
        raise ValueError(
            f"Signal name must start with a letter, contain only letters, "
            f'numbers, and underscores, but got "{name}"'
        )
