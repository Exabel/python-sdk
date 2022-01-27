import json
from abc import ABC
from typing import Mapping, Optional

import pandas as pd

from exabel_data_sdk.services.csv_exception import CsvLoadingException
from exabel_data_sdk.services.csv_loader import CsvLoader


class CsvLoaderWithEntityMapping(CsvLoader, ABC):
    """
    Base class for CSV loaders optionally can make use of an entity mapping file.
    """

    def read_entity_mapping_file(
        self, *, entity_mapping_filename: Optional[str], separator: str = ","
    ) -> Optional[Mapping[str, Mapping[str, str]]]:
        """
        Read the entity mapping file from disk with the filename specified by command line
        argument. Only supports *.json and *.csv file extensions.
        """
        if entity_mapping_filename is None:
            return None
        if entity_mapping_filename.endswith(".json"):
            with open(entity_mapping_filename, "r", encoding="utf-8") as f:
                mappings = json.load(f)
            # validate the mapping is a dictionary (and not a list)
            if not isinstance(mappings, dict):
                raise CsvLoadingException(
                    "Expected entity mapping file to be a JSON key-value object, "
                    f"but got: {mappings}"
                )
            for value in mappings.values():
                if not isinstance(value, dict):
                    raise CsvLoadingException(
                        "Expected all values of the JSON object to be objects as well, "
                        f"but got: {value}"
                    )
            # validate each sub-dictionary are string-string mappings
            for mapping in mappings.values():
                for key, value in mapping.items():
                    if not isinstance(key, str) or not isinstance(value, str):
                        raise CsvLoadingException(
                            "Expected the key-value pairs in the entity mapping JSON file to be "
                            f"str-str mappings, but got:\n"
                            f"Key ({type(key)}): {key}\n"
                            f"Value ({type(value)}): {value}"
                        )
            return mappings

        if entity_mapping_filename.endswith(".csv"):
            csv_data_frame = pd.read_csv(
                entity_mapping_filename, header=0, sep=separator, dtype="str"
            )
            identifier_columns = [
                col for col in csv_data_frame.columns if not col.endswith("_entity")
            ]
            entity_columns = [col for col in csv_data_frame.columns if col.endswith("_entity")]
            invalid_identifiers = [
                identifier
                for identifier in identifier_columns
                if f"{identifier}_entity" not in entity_columns
            ]
            if invalid_identifiers:
                raise CsvLoadingException(
                    "The entity mapping CSV file is missing one or more entity columns: "
                    f"{[identifier + '_entity' for identifier in invalid_identifiers]}"
                )
            invalid_entities = [
                entity
                for entity in entity_columns
                if entity[: -len("_entity")] not in identifier_columns
            ]
            if invalid_entities:
                raise CsvLoadingException(
                    "The entity mapping CSV file is missing one or more identifier columns: "
                    f"{[entity[:-len('_entity')] for entity in invalid_entities]}"
                )

            mappings = {}
            for identifier in identifier_columns:
                mappings[identifier] = {
                    getattr(row, identifier): getattr(row, f"{identifier}_entity")
                    for row in csv_data_frame[~csv_data_frame[identifier].isna()].itertuples()
                }
            return mappings

        # If the file extension is not supported or set, exit.
        raise CsvLoadingException(
            "Expected the entity mapping file to be a *.json or *.csv file, "
            f"but got: '{entity_mapping_filename}'."
        )
