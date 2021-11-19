import argparse
import json
import sys
from typing import Mapping, Optional, Sequence

import pandas as pd

from exabel_data_sdk.scripts.csv_script import CsvScript


class CsvScriptWithEntityMapping(CsvScript):
    """
    Base class for scripts that process a CSV files with data to be loaded into the Exabel API,
    with the addition of also providing an option to override normalising or looking up given
    identifiers in the Exabel API.

    The entity mapping file is either a CSV file with the following columns and headers:
        <identifier>: The identifier of the entity.
        <identifier>_entity: The full resource name of the entity to map this identifier to.

        E.g.
            isin,isin_entity
            US0000001,entityTypes/company/entities/company_1
            US0000002,entityTypes/company/entities/company_2
            ...

    Or, the entity mapping file is a JSON file with the following format:
        {
            <identifier>: {
                "identifier": "entity"
            }
        }

        E.g.
            {
                "isin": {
                    "US0000001": "entityTypes/company/entities/company_1",
                    "US0000002": "entityTypes/company/entities/company_2",
                    ...
                }
            }
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        help_text = (
            "The URL of the entity mapping file to use. "
            "Supports *.json and *.csv extensions only."
        )
        self.parser.add_argument(
            "--entity_mapping_filename", required=False, type=str, help=help_text
        )

    def read_entity_mapping_file(
        self, args: argparse.Namespace
    ) -> Optional[Mapping[str, Mapping[str, str]]]:
        """
        Read the entity mapping file from disk with the filename specified by command line
        argument. Only supports *.json and *.csv file extensions.
        """
        if args.entity_mapping_filename is None:
            return None
        if args.entity_mapping_filename.endswith(".json"):
            with open(args.entity_mapping_filename, "r", encoding="utf-8") as f:
                mappings = json.load(f)
            # validate the mapping is a dictionary (and not a list)
            if not isinstance(mappings, dict):
                print(
                    "Expected entity mapping file to be a JSON key-value object, "
                    f"but got: {mappings}"
                )
                sys.exit(1)
            else:
                for value in mappings.values():
                    if not isinstance(value, dict):
                        print(
                            "Expected all values of the JSON object to be objects as well, "
                            f"but got: {value}"
                        )
                        sys.exit(1)
            # validate each sub-dictionary are string-string mappings
            for mapping in mappings.values():
                for key, value in mapping.items():
                    if not isinstance(key, str) or not isinstance(value, str):
                        print(
                            "Expected the key-value pairs in the entity mapping JSON file to be "
                            f"str-str mappings, but got:\n"
                            f"Key ({type(key)}): {key}\n"
                            f"Value ({type(value)}): {value}"
                        )
                        sys.exit(1)
            return mappings

        if args.entity_mapping_filename.endswith(".csv"):
            csv_data_frame = pd.read_csv(
                args.entity_mapping_filename, header=0, sep=args.sep, dtype="str"
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
                print(
                    "The entity mapping CSV file is missing one or more entity columns: "
                    f"{[identifier + '_entity' for identifier in invalid_identifiers]}"
                )
                sys.exit(1)
            invalid_entities = [
                entity
                for entity in entity_columns
                if entity[: -len("_entity")] not in identifier_columns
            ]
            if invalid_entities:
                print(
                    "The entity mapping CSV file is missing one or more identifier columns: "
                    f"{[entity[:-len('_entity')] for entity in invalid_entities]}"
                )
                sys.exit(1)

            mappings = {}
            for identifier in identifier_columns:
                mappings[identifier] = {
                    getattr(row, identifier): getattr(row, f"{identifier}_entity")
                    for row in csv_data_frame[~csv_data_frame[identifier].isna()].itertuples()
                }
            return mappings

        # If the file extension is not supported or set, exit.
        print(
            "Expected the entity mapping file to be a *.json or *.csv file, "
            f"but got: '{args.entity_mapping_filename}'."
        )
        sys.exit(1)
