import re
import sys
from typing import Mapping, MutableMapping

import pandas as pd

from exabel_data_sdk.client.api.entity_api import EntityApi


def normalize_resource_name(name: str) -> str:
    """
    Turn a non-empty string into a legal resource name by applying the following steps:
     - Replace all illegal characters with an underscore
     - Turn multiple consecutive underscores into one
     - Cut at length at most 64 characters
    """
    # Cannot be empty
    if not name:
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
    print("The normalization of identifiers have introduced resource name collisions.")
    print("The collisions are shown below.")
    print("Please fix these duplicates, and then re-run the script.")
    pd.set_option("max_colwidth", 1000)
    print(duplicates.sort_values().to_string())
    sys.exit(1)


def to_entity_resource_names(
    entity_api: EntityApi,
    identifiers: pd.Series,
    namespace: str = None,
    entity_mapping: Mapping[str, Mapping[str, str]] = None,
) -> pd.Series:
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

     - bloomberg_ticker
        The given identifiers are Bloomberg tickers.
        The tickers are looked up with the Exabel API, and the Exabel resource identifiers
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
        a Series with the same index as the input Series
          Any identifier that could not be mapped, will be set to None.
    """
    name = identifiers.name
    if name in ("entity", "entity_from", "entity_to"):
        # Already resource identifiers, nothing to be done
        return identifiers

    unique_ids = identifiers.unique().tolist()
    mapping: MutableMapping[str, str] = {}
    if entity_mapping and entity_mapping.get(name):
        mapping.update(entity_mapping[name])
        unique_ids = [unique_id for unique_id in unique_ids if unique_id not in mapping]

    if name in ("isin", "factset_identifier", "bloomberg_ticker", "mic:ticker"):
        # A company identifier
        print(f"Looking up {len(unique_ids)} {name}s...")
        for identifier in unique_ids:
            if not identifier:
                # Skip empty identifiers
                continue
            if name == "mic:ticker":
                parts = identifier.split(":")
                if len(parts) != 2:
                    print("mic:ticker must contain exactly one colon (:), but got:", identifier)
                    continue
                search_terms = {"mic": parts[0], "ticker": parts[1]}
            else:
                search_terms = {name: identifier}
            entities = entity_api.search_for_entities(
                entity_type="entityTypes/company", **search_terms
            )
            if not entities:
                print("Did not find any match for", search_terms)
            elif len(entities) > 1:
                print(f"Found {len(entities)} matches for {search_terms}:\n  {entities}")
            else:
                mapping[identifier] = entities[0].name
        print(f"Found a match for {len(mapping)} {name}s.")

    else:
        # Should be a known entity type
        entity_type_name = f"entityTypes/{name}"
        entity_type = entity_api.get_entity_type(entity_type_name)
        entity_types = entity_api.list_entity_types()
        read_only_entity_type_names = [
            entity_type.name for entity_type in entity_types if entity_type.read_only
        ]
        if not entity_type:
            message = f"Failure: Did not find entity type {entity_type_name}"
            print(message)
            print("Available entity types are:")
            print(entity_api.list_entity_types())
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
    return result


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
