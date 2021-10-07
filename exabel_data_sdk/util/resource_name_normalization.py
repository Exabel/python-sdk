import re

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


def to_entity_resource_names(
    entity_api: EntityApi, identifiers: pd.Series, namespace: str = None
) -> pd.Series:
    """
    Turns the given identifiers into entity resource names.

    The name of the given series is used to determine what kind of identifier it is.
    These are the legal series names, and how each case is handled:

     - entity (or entity_from or entity_to):
        The given identifiers are the entity resource names.
        The identifiers are returned unaltered.

     - isin:
        The given identifiers are ISIN numbers.
        The ISIN numbers are looked up with the Exabel API, and the Exabel resource identifiers
        for the associated companies are returned.

     - factset_identifier:
        The given identifiers are FactSet IDs.
        The identifiers are looked up with the Exabel API, and the Exabel resource identifiers
        are returned.

     - bloomberg_ticker:
        The given identifiers are Bloomberg tickers.
        The tickers are looked up with the Exabel API, and the Exabel resource identifiers
        are returned.

     - any known entity type, e.g. "brand" or "product_type":
        The given identifiers are customer provided names.
        The names are first normalized (using the normalize_resource_name method)
        and then a full resource identifier is constructed on this form:
            entityTypes/{entityType}/entity/{namespace}.{normalized_name}
        for example:
            entityTypes/brand/entity/acme.Spring_Vine

    Returns:
        a Series with the same index as the input Series
          Any identifier that could not be mapped, will be set to None.
    """
    name = identifiers.name
    if name in ("entity", "entity_from", "entity_to"):
        # Already resource identifiers, nothing to be done
        return identifiers

    unique_ids = identifiers.unique()

    if name in ("isin", "factset_identifier", "bloomberg_ticker"):
        # A company identifier
        print(f"Looking up {len(unique_ids)} {name}s...")
        mapping = {}
        for identifier in unique_ids:
            if not identifier:
                # Skip empty identifiers
                continue
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
        if not entity_type:
            message = f"Failure: Did not find entity type {entity_type_name}"
            print(message)
            print("Available entity types are:")
            print(entity_api.list_entity_types())
            raise ValueError(message)

        if namespace is None:
            prefix = ""
        else:
            if "." in namespace:
                raise ValueError(f"Namespace cannot contain periods (.), got {namespace}")
            prefix = f"{namespace}."

        mapping = {
            identifier: f"{entity_type_name}/entities/{prefix}{normalize_resource_name(identifier)}"
            for identifier in unique_ids
            if identifier
        }

    result = identifiers.map(mapping)
    result.name = "entity"
    return result
