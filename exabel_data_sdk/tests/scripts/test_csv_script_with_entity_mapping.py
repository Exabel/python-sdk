import argparse
import unittest
from typing import Mapping, Optional

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.csv_script_with_entity_mapping import CsvScriptWithEntityMapping
from exabel_data_sdk.services.csv_exception import CsvLoadingException
from exabel_data_sdk.services.csv_loader_with_entity_mapping import CsvLoaderWithEntityMapping

common_args = [
    "script-name",
    "--namespace",
    "test",
    "--api-key",
    "123",
    "--filename",
    "./this_file_does_not_exist",
]


class ConcreteCsvScriptWithEntitySearch(CsvScriptWithEntityMapping):
    """Dummy implementation used for testing"""

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        raise NotImplementedError

    def read_entity_mapping_file(
        self, args: argparse.Namespace
    ) -> Optional[Mapping[str, Mapping[str, str]]]:
        """Read an entity mapping file."""
        return CsvLoaderWithEntityMapping().read_entity_mapping_file(
            entity_mapping_filename=args.entity_mapping_filename
        )


class TestCsvScriptWithEntitySearch(unittest.TestCase):
    def test_read_entity_mapping_file_json(self):
        args = common_args + [
            "--entity-mapping-filename",
            "./exabel_data_sdk/tests/resources/data/entity_mapping.json",
        ]

        loader = ConcreteCsvScriptWithEntitySearch(args, "Load")
        expected_entity_mapping = {
            "isin": {"do_not_search_for": "entityTypes/company/entities/was_not_searched_for"}
        }
        self.assertDictEqual(
            loader.read_entity_mapping_file(loader.parse_arguments()), expected_entity_mapping
        )

    def test_read_entity_mapping_file_csv(self):
        args = common_args + [
            "--entity-mapping-filename",
            "./exabel_data_sdk/tests/resources/data/entity_mapping.csv",
        ]

        loader = ConcreteCsvScriptWithEntitySearch(args, "Load")
        expected_entity_mapping = {
            "isin": {"do_not_search_for": "entityTypes/company/entities/was_not_searched_for"}
        }
        self.assertDictEqual(
            loader.read_entity_mapping_file(loader.parse_arguments()), expected_entity_mapping
        )

    def test_should_fail_read_entity_mapping_file_invalid_csv(self):
        args = common_args + [
            "--entity-mapping-filename",
            "./exabel_data_sdk/tests/resources/data/entity_mapping_invalid.csv",
        ]

        loader = ConcreteCsvScriptWithEntitySearch(args, "Load")
        with self.assertRaises(CsvLoadingException) as context:
            loader.read_entity_mapping_file(loader.parse_arguments())
        self.assertEqual(
            "The entity mapping CSV file is missing one or more entity columns: "
            "['extra_col_entity']",
            str(context.exception),
        )

    def test_should_fail_read_entity_mapping_file_invalid_json(self):
        files = [
            "./exabel_data_sdk/tests/resources/data/entity_mapping_invalid_0.json",
            "./exabel_data_sdk/tests/resources/data/entity_mapping_invalid_1.json",
        ]
        expected_errors = [
            "Expected all values of the JSON object to be objects as well, "
            "but got: ['entityTypes/company/entities/was_not_searched_for']",
            "Expected entity mapping file to be a JSON key-value object, but got: "
            "[{'do_not_search_for_0': 'entityTypes/company/entities/was_not_searched_for_0'}, "
            "{'do_not_search_for_1': 'entityTypes/company/entities/was_not_searched_for_1'}]",
        ]

        for file, expected in zip(files, expected_errors):
            args = common_args + ["--entity-mapping-filename", file]
            loader = ConcreteCsvScriptWithEntitySearch(args, "Load")
            with self.assertRaises(CsvLoadingException) as context:
                loader.read_entity_mapping_file(loader.parse_arguments())
            self.assertEqual(expected, str(context.exception))

    def test_should_fail_read_entity_mapping_file_invalid_extension(self):
        files = [
            "./file/does/not/exist/entity_mapping",
            "./file/does/not/exist/entity_mapping.txt",
            "./file/does/not/exist/entity_mapping.xlsx",
        ]

        for file in files:
            args = common_args + ["--entity-mapping-filename", file]
            loader = ConcreteCsvScriptWithEntitySearch(args, "Load")
            with self.assertRaises(CsvLoadingException) as context:
                loader.read_entity_mapping_file(loader.parse_arguments())
            self.assertEqual(
                "Expected the entity mapping file to be a *.json or *.csv file, "
                f"but got: '{file}'.",
                str(context.exception),
            )
