from typing import Sequence

from exabel_data_sdk.scripts.csv_script import CsvScript


class CsvScriptWithEntityMapping(CsvScript):
    """
    Base class for scripts that process CSV files with data to be loaded into the Exabel API,
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
        self.parser.add_argument(
            "--entity-mapping-filename",
            required=False,
            type=str,
            help=(
                "The URL of the entity mapping file to use. "
                "Supports *.json and *.csv extensions only."
            ),
        )
