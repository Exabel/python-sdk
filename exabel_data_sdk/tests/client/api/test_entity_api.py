import unittest

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.tests.client.api.mock_entity_api import MockEntityApi


class TestEntityApi(unittest.TestCase):
    def test_upsert(self):
        entity_api: EntityApi = MockEntityApi()
        expected = Entity(
            name="entityTypes/company/entities/Amazon",
            display_name="Amazon",
        )
        created_entity = entity_api.upsert_entity(expected)
        self.assertEqual(expected, created_entity)
        updated_entity = entity_api.upsert_entity(expected)
        self.assertEqual(expected, updated_entity)

    def test_upsert_replaces_resource(self):
        entity_api: EntityApi = MockEntityApi()
        old_entity = Entity(
            name="entityTypes/company/entities/Amazon",
            display_name="Amazon's old display name",
            description="Amazon's old description",
            properties={"old_property": "old_value"},
        )
        expected = Entity(
            name="entityTypes/company/entities/Amazon",
            display_name="Amazon",
            description="Amazon's new description",
        )
        entity_api.create_entity(old_entity, old_entity.get_entity_type())
        entity_api.upsert_entity(expected)
        actual_entity = entity_api.get_entity(expected.name)
        self.assertEqual(expected, actual_entity)
