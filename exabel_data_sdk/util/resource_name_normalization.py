import logging
import re
import warnings
from collections import deque
from dataclasses import dataclass
from typing import Iterator, Mapping, MutableMapping, MutableSequence, Optional, Sequence, Tuple

import pandas as pd

from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.client.api.search_service import COMPANY_SEARCH_TERM_FIELDS
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import SearchTerm
from exabel_data_sdk.util.batcher import batcher
from exabel_data_sdk.util.warnings import ExabelDeprecationWarning

logger = logging.getLogger(__name__)

MAX_SEARCH_TERMS = 1000
# Matches anything but letters, numbers, underscore, and dash, except for the first character
ILLEGAL_RESOURCE_NAME_CHARACTER_PATTERN = re.compile(r"(^-|[^a-zA-Z0-9_\-])")
# Matches two or more consecutive underscores
MULTIPLE_UNDERSCORE_PATTERN = re.compile(r"__+")
# Matches namespace prefixes
NAMESPACE_PREFIX_PATTERN = re.compile(r"^[a-zA-Z0-9_\-]+(?=\.)")


def normalize_resource_name(name: str, *, preserve_namespace: bool = False) -> str:
    """
    Turn a non-empty string into a legal resource name by applying the following steps:
     - Replace all illegal characters with an underscore
     - Turn multiple consecutive underscores into one
     - Cut at length at most 64 characters
     - If `preserve_namespace` is set then the name can contain a namespace prefix, which is
        preserved from normalization.
    """
    # Cannot be empty
    if not name or pd.isna(name):
        raise ValueError("Cannot have an empty resource name.")
    namespace = None
    if preserve_namespace and NAMESPACE_PREFIX_PATTERN.match(name):
        name_parts = name.split(".", 2)
        if len(name_parts) == 2:
            namespace, name = name_parts
    name = ILLEGAL_RESOURCE_NAME_CHARACTER_PATTERN.sub("_", name)
    name = MULTIPLE_UNDERSCORE_PATTERN.sub("_", name)
    # Truncate to 64 characters
    name = name[:64]
    return f"{namespace}.{name}" if namespace else name


def remove_prefix(name: str, prefix: str) -> str:
    """
    Remove the given prefix from the identifier, if it is there.
    """
    if name.startswith(prefix):
        return name[len(prefix) :]
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
    pd.set_option("max_colwidth", 1000)
    logger.error(
        "The normalization of identifiers have introduced resource name collisions. "
        "The collisions are shown below. "
        "Please fix these duplicates, and then re-run the script.\n%s",
        duplicates.sort_values().to_string(),
    )
    raise ValueError("Resource name collisions detected")


@dataclass
class EntitySearchResultWarning:
    """A warning that is generated when searching for an entity."""

    field: str
    query: str
    matched_entity_names: Sequence[str]

    @property
    def _pretty_terms(self) -> str:
        return f"{{'{self.field}': '{self.query}'}}"

    def __str__(self) -> str:
        if not self.matched_entity_names:
            return f"Did not find any match for {self._pretty_terms}"
        if len(self.matched_entity_names) > 1:
            return (
                f"Found {len(self.matched_entity_names)} matches for {self._pretty_terms}:\n"
                f"\t{self.matched_entity_names}"
            )
        return f"Unknown LookupWarning for search term: {self._pretty_terms}"


@dataclass
class EntityResourceNames:
    """
    Identified resource names along with warnings regarding entities that could not be uniquely
    identified.
    """

    names: pd.Series
    warnings: Sequence[EntitySearchResultWarning]
    mapping: Mapping[str, str]
    identifier_type: str


def get_namespace_from_resource_identifier(resource_identifier: str) -> Optional[str]:
    """Get the namespace from a resource identifier."""
    resource_identifier_parts = resource_identifier.split(".")
    if len(resource_identifier_parts) == 1:
        return None
    if len(resource_identifier_parts) == 2:
        return resource_identifier_parts[0]
    raise ValueError(f"Expected 1 or less '.' in the resource identifier: '{resource_identifier}'.")


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


def _search_entities(
    *,
    entity_api: EntityApi,
    identifier_type: str,
    identifiers: Sequence[str],
    entity_type: str,
) -> Tuple[Mapping[str, str], Sequence[EntitySearchResultWarning]]:
    logger.info("Looking up %d %ss...", len(identifiers), identifier_type)
    # Skip empty identifiers
    non_empty_identifiers: Iterator[str] = (
        identifier for identifier in identifiers if identifier and not pd.isna(identifier)
    )
    no_search_terms = MAX_SEARCH_TERMS
    if identifier_type == "mic:ticker":
        # mic and ticker takes up to two search terms
        no_search_terms = no_search_terms // 2
        non_empty_identifiers = filter(_validate_mic_ticker, non_empty_identifiers)
    mapping: MutableMapping[str, str] = {}
    search_result_warnings: MutableSequence[EntitySearchResultWarning] = []
    for identifier_batch in batcher(non_empty_identifiers, no_search_terms):
        search_terms: MutableSequence[SearchTerm] = deque()
        for identifier in identifier_batch:
            if identifier_type == "mic:ticker":
                parts = identifier.split(":")
                search_terms.extend(
                    [
                        SearchTerm(field="mic", query=parts[0]),
                        SearchTerm(field="ticker", query=parts[1]),
                    ]
                )
            else:
                search_terms.append(SearchTerm(field=identifier_type, query=identifier))
        search_results = entity_api.search.entities_by_terms(
            entity_type=f"entityTypes/{entity_type}", terms=search_terms
        )
        for identifier, search_result in zip(identifier_batch, search_results):
            entities = search_result.entities
            if not entities or len(entities) > 1:
                warning = EntitySearchResultWarning(
                    field=identifier_type,
                    query=identifier,
                    matched_entity_names=[entity.name for entity in entities],
                )
                logger.warning(warning)
                search_result_warnings.append(warning)
            else:
                mapping[identifier] = entities[0].name
    logger.info("Found a match for %d %ss.", len(mapping), identifier_type)

    return mapping, search_result_warnings


def _get_resource_names(
    *,
    entity_api: EntityApi,
    identifiers: Sequence[str],
    entity_type: str,
    namespace: Optional[str] = None,
    check_entity_types: bool = True,
    preserve_namespace: bool = False,
) -> Mapping[str, str]:
    # Should be a known entity type (case insensitive matching)
    entity_type_name = f"entityTypes/{entity_type}"
    entity_type_name_lower = entity_type_name.lower()
    entity_type_name_lower_map: MutableMapping[str, EntityType] = {}
    read_only_entity_type_lower_names = set()
    # Entity types are reversed because we want to match the first entity type returned by the
    # API lexicographically.
    for et in reversed(list(entity_api.get_entity_type_iterator())):
        lower_case_entity_type_name = et.name.lower()
        entity_type_name_lower_map[lower_case_entity_type_name] = et
        if et.read_only:
            read_only_entity_type_lower_names.add(lower_case_entity_type_name)

    try:
        entity_type_name = entity_type_name_lower_map[entity_type_name_lower].name
    except KeyError as e:
        if check_entity_types:
            raise ValueError(f"Did not find entity type {entity_type_name}") from e

    if entity_type_name_lower in read_only_entity_type_lower_names or preserve_namespace:
        namespace = None
    prefix = ""

    entity_type_namespace = get_namespace_from_resource_identifier(entity_type)
    if entity_type_namespace or namespace:
        prefix = f"{entity_type_namespace or namespace}."

    mapping: MutableMapping[str, str] = {}
    for identifier in filter(None, identifiers):
        if preserve_namespace:
            _identifier = identifier
            if entity_type_namespace:
                # Remove prefix in order to support mixing explicit and implicit namespaces for
                # entities
                _identifier = remove_prefix(identifier, prefix)
            normalized_name = normalize_resource_name(
                _identifier, preserve_namespace=preserve_namespace
            )
        else:
            normalized_name = normalize_resource_name(remove_prefix(identifier, prefix))
        mapping[identifier] = f"{entity_type_name}/entities/{prefix}{normalized_name}"

    _assert_no_collision(mapping)

    return mapping


def to_entity_resource_names(
    entity_api: EntityApi,
    identifiers: pd.Series,
    namespace: Optional[str] = None,
    entity_mapping: Optional[Mapping[str, Mapping[str, str]]] = None,
    check_entity_types: bool = True,
    preserve_namespace: bool = False,
) -> EntityResourceNames:
    """
    Turns the given identifiers into entity resource names.

    If `preserve_namespace` is set, it is assumed that the identifiers can contain a namespace
    prefix which should be preserved. The name of the given series is used to determine what kind
    of identifier it is. These are the legal series names, and how each case is handled:

     - entity
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
    entity_type = identifiers.name
    if entity_type in ("entity", "entity_from", "entity_to"):
        # Already resource identifiers, nothing to be done
        if entity_type in ("entity_from", "entity_to"):
            warnings.warn(
                "The 'entity_from' and 'entity_to' columns with full resource names are "
                "deprecated. Please specify the entity types explicitly and use resource "
                "identifiers instead.",
                ExabelDeprecationWarning,
            )
        return EntityResourceNames(identifiers, [], {}, entity_type)

    search_result_warnings: MutableSequence[EntitySearchResultWarning] = []
    unique_ids = identifiers.unique().tolist()
    mapping: MutableMapping[str, str] = {}
    if entity_mapping and entity_mapping.get(entity_type):
        mapping.update(entity_mapping[entity_type])
        unique_ids = [unique_id for unique_id in unique_ids if unique_id not in mapping]

    if entity_type in COMPANY_SEARCH_TERM_FIELDS:
        _mapping, _search_result_warnings = _search_entities(
            entity_api=entity_api,
            identifiers=unique_ids,
            identifier_type=entity_type,
            entity_type="company",
        )
        mapping.update(_mapping)
        search_result_warnings.extend(_search_result_warnings)
    else:
        _mapping = _get_resource_names(
            entity_api=entity_api,
            identifiers=unique_ids,
            entity_type=entity_type,
            namespace=namespace,
            check_entity_types=check_entity_types,
            preserve_namespace=preserve_namespace,
        )
        mapping.update(_mapping)

    result = identifiers.map(mapping)
    result.name = "entity"
    return EntityResourceNames(result, search_result_warnings, mapping, entity_type)


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
