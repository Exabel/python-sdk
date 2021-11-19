import argparse
import unittest

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.csv_script_with_entity_mapping import CsvScriptWithEntityMapping

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


class TestCsvScriptWithEntitySearch(unittest.TestCase):
    def test_read_entity_mapping_file_json(self):
        args = common_args + [
            "--entity_mapping_filename",
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
            "--entity_mapping_filename",
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
            "--entity_mapping_filename",
            "./exabel_data_sdk/tests/resources/data/entity_mapping_invalid.csv",
        ]

        loader = ConcreteCsvScriptWithEntitySearch(args, "Load")
        with self.assertRaises(SystemExit):
            loader.read_entity_mapping_file(loader.parse_arguments())

    def test_should_fail_read_entity_mapping_file_invalid_json(self):
        files = [
            "./exabel_data_sdk/tests/resources/data/entity_mapping_invalid_0.json",
            "./exabel_data_sdk/tests/resources/data/entity_mapping_invalid_1.json",
        ]

        for file in files:
            args = common_args + ["--entity_mapping_filename", file]
            loader = ConcreteCsvScriptWithEntitySearch(args, "Load")
            with self.assertRaises(SystemExit):
                loader.read_entity_mapping_file(loader.parse_arguments())

    def test_should_fail_read_entity_mapping_file_invalid_extension(self):
        files = [
            "./file/does/not/exist/entity_mapping",
            "./file/does/not/exist/entity_mapping.txt",
            "./file/does/not/exist/entity_mapping.xlsx",
        ]

        for file in files:
            args = common_args + ["--entity_mapping_filename", file]
            loader = ConcreteCsvScriptWithEntitySearch(args, "Load")
            with self.assertRaises(SystemExit):
                loader.read_entity_mapping_file(loader.parse_arguments())
