import random
import unittest

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.scripts.load_entities_from_csv import LoadEntitiesFromCsv
from exabel_data_sdk.tests.scripts.common_utils import load_test_data_from_csv

common_args = [
    "script-name",
    "--namespace",
    "test",
    "--api-key",
    "123",
]


class TestLoadEntities(unittest.TestCase):
    def test_read_file(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/entities.csv",
            "--description-col",
            "description",
        ]
        client = load_test_data_from_csv(LoadEntitiesFromCsv, args)
        expected_entities = [
            Entity(
                name="entityTypes/brand/entities/test.Spring_Vine",
                display_name="Spring & Vine",
                description="Shampoo bars",
            ),
            Entity(
                name="entityTypes/brand/entities/test.The_Coconut_Tree",
                display_name="The Coconut Tree",
                description="Sri Lankan street food",
            ),
        ]
        self.check_entities(client, expected_entities)

    def test_read_file_with_integer_identifier(self):
        file_args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/entities_with_integer_identifiers.csv",
        ]
        extra_args = [[], ["--name-column", "brand"]]
        expected_entities = [
            Entity(name="entityTypes/brand/entities/test.0001", display_name="0001"),
            Entity(name="entityTypes/brand/entities/test.0002", display_name="0002"),
        ]
        for e_args in extra_args:
            args = file_args + e_args
            client = load_test_data_from_csv(LoadEntitiesFromCsv, args)
            self.check_entities(client, expected_entities)

    def check_entities(self, client, expected_entities):
        """Check expected entities against actual entities retrieved from the client"""
        all_entities = client.entity_api.list_entities("entityTypes/brand").results
        self.assertListEqual(sorted(expected_entities), sorted(all_entities))
        for expected_entity in expected_entities:
            entity = client.entity_api.get_entity(expected_entity.name)
            self.assertEqual(expected_entity, entity)

    def test_read_file_random_errors(self):
        random.seed(1)
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/entities2.csv",
        ]
        client = load_test_data_from_csv(LoadEntitiesFromCsv, args)
        client.entity_api.entities.failure_rate = 0.3
        expected_entities = [
            Entity(
                name=f"entityTypes/brand/entities/test.Brand_{letter}",
                display_name=f"Brand {letter}",
            )
            for letter in "ABCDEFGHIJ"
        ]
        self.check_entities(client, expected_entities)

    def test_read_file_with_upsert(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/entities.csv",
            "--description-col",
            "description",
            "--upsert",
        ]
        client = load_test_data_from_csv(LoadEntitiesFromCsv, args)
        expected_entities = [
            Entity(
                name="entityTypes/brand/entities/test.Spring_Vine",
                display_name="Spring & Vine",
                description="This entry might be ignored because it's a duplicate",
            ),
            Entity(
                name="entityTypes/brand/entities/test.The_Coconut_Tree",
                display_name="The Coconut Tree",
                description="Sri Lankan street food",
            ),
        ]
        self.check_entities(client, expected_entities)
        client = load_test_data_from_csv(LoadEntitiesFromCsv, args, client)
        self.check_entities(client, expected_entities)
