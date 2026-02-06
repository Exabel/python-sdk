import pytest

from exabel.services.entity_mapping_file_reader import EntityMappingFileReader
from exabel.services.file_loading_exception import FileLoadingException


class TestEntityMappingFileReader:
    def test_read_entity_mapping_file_json(self):
        expected_entity_mapping = {
            "isin": {"do_not_search_for": "entityTypes/company/entities/was_not_searched_for"}
        }
        assert expected_entity_mapping == EntityMappingFileReader.read_entity_mapping_file(
            "./exabel/tests/resources/data/entity_mapping.json"
        )

    def test_read_entity_mapping_file_csv(self):
        expected_entity_mapping = {
            "isin": {"do_not_search_for": "entityTypes/company/entities/was_not_searched_for"}
        }
        assert expected_entity_mapping == EntityMappingFileReader.read_entity_mapping_file(
            "./exabel/tests/resources/data/entity_mapping.csv"
        )

    def test_should_fail_read_entity_mapping_file_invalid_csv(self):
        with pytest.raises(FileLoadingException) as context:
            EntityMappingFileReader.read_entity_mapping_file(
                "./exabel/tests/resources/data/entity_mapping_invalid.csv"
            )
        assert (
            "The entity mapping CSV file is missing one or more entity columns: "
            "['extra_col_entity']" == str(context.value)
        )

    def test_should_fail_read_entity_mapping_file_invalid_json(self):
        files = [
            "./exabel/tests/resources/data/entity_mapping_invalid_0.json",
            "./exabel/tests/resources/data/entity_mapping_invalid_1.json",
        ]
        expected_errors = [
            "Expected all values of the JSON object to be objects as well, "
            "but got: ['entityTypes/company/entities/was_not_searched_for']",
            "Expected entity mapping file to be a JSON key-value object, but got: "
            "[{'do_not_search_for_0': 'entityTypes/company/entities/was_not_searched_for_0'}, "
            "{'do_not_search_for_1': 'entityTypes/company/entities/was_not_searched_for_1'}]",
        ]

        for file, expected in zip(files, expected_errors):
            with pytest.raises(FileLoadingException) as context:
                EntityMappingFileReader.read_entity_mapping_file(file)
            assert expected == str(context.value)

    def test_should_fail_read_entity_mapping_file_invalid_extension(self):
        files = [
            "./file/does/not/exist/entity_mapping",
            "./file/does/not/exist/entity_mapping.txt",
            "./file/does/not/exist/entity_mapping.xlsx",
        ]
        for file in files:
            with pytest.raises(FileLoadingException) as context:
                EntityMappingFileReader.read_entity_mapping_file(file)
            assert (
                "Expected the entity mapping file to be a *.json or *.csv file, "
                f"but got: '{file}'." == str(context.value)
            )
