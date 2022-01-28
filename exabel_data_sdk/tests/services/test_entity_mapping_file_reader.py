import unittest

from exabel_data_sdk.services.csv_exception import CsvLoadingException
from exabel_data_sdk.services.entity_mapping_file_reader import EntityMappingFileReader


class TestEntityMappingFileReader(unittest.TestCase):
    def test_read_entity_mapping_file_json(self):
        expected_entity_mapping = {
            "isin": {"do_not_search_for": "entityTypes/company/entities/was_not_searched_for"}
        }
        self.assertDictEqual(
            EntityMappingFileReader.read_entity_mapping_file(
                "./exabel_data_sdk/tests/resources/data/entity_mapping.json"
            ),
            expected_entity_mapping,
        )

    def test_read_entity_mapping_file_csv(self):
        expected_entity_mapping = {
            "isin": {"do_not_search_for": "entityTypes/company/entities/was_not_searched_for"}
        }
        self.assertDictEqual(
            EntityMappingFileReader.read_entity_mapping_file(
                "./exabel_data_sdk/tests/resources/data/entity_mapping.csv"
            ),
            expected_entity_mapping,
        )

    def test_should_fail_read_entity_mapping_file_invalid_csv(self):
        with self.assertRaises(CsvLoadingException) as context:
            EntityMappingFileReader.read_entity_mapping_file(
                "./exabel_data_sdk/tests/resources/data/entity_mapping_invalid.csv"
            )
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
            with self.assertRaises(CsvLoadingException) as context:
                EntityMappingFileReader.read_entity_mapping_file(file)
            self.assertEqual(expected, str(context.exception))

    def test_should_fail_read_entity_mapping_file_invalid_extension(self):
        files = [
            "./file/does/not/exist/entity_mapping",
            "./file/does/not/exist/entity_mapping.txt",
            "./file/does/not/exist/entity_mapping.xlsx",
        ]
        for file in files:
            with self.assertRaises(CsvLoadingException) as context:
                EntityMappingFileReader.read_entity_mapping_file(file)
            self.assertEqual(
                "Expected the entity mapping file to be a *.json or *.csv file, "
                f"but got: '{file}'.",
                str(context.exception),
            )
