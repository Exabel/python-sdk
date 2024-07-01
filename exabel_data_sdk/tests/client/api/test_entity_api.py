import unittest
from unittest import mock

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.client.client_config import ClientConfig
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

    def test_get_entity_type_iterator(self):
        entity_api = EntityApi(ClientConfig("api-key"))
        entity_type = mock.create_autospec(EntityType)
        entity_api.list_entity_types = mock.MagicMock()
        entity_api.list_entity_types.side_effect = [
            PagingResult([entity_type] * 1000, next_page_token="1000", total_size=2555),
            PagingResult([entity_type] * 1000, next_page_token="2000", total_size=2555),
            PagingResult([entity_type] * 555, next_page_token="~~~", total_size=2555),
            AssertionError("Should not be called"),
        ]
        entity_types = list(entity_api.get_entity_type_iterator())
        self.assertEqual(2555, len(entity_types))
        self.assertSequenceEqual([entity_type] * 2555, entity_types)
        entity_api.list_entity_types.assert_has_calls(
            [
                mock.call(page_token=None, page_size=1000),
                mock.call(page_token="1000", page_size=1000),
                mock.call(page_token="2000", page_size=1000),
            ]
        )

    def test_get_entities_iterator(self):
        entity_api = EntityApi(ClientConfig("api-key"))
        entity = mock.create_autospec(Entity)
        entity_api.list_entities = mock.MagicMock()
        entity_api.list_entities.side_effect = [
            PagingResult([entity] * 1000, next_page_token="1000", total_size=1100),
            PagingResult([entity] * 100, next_page_token="~~~", total_size=1100),
            AssertionError("Should not be called"),
        ]
        entities = list(entity_api.get_entities_iterator("entity_type"))
        self.assertEqual(1100, len(entities))
        self.assertSequenceEqual([entity] * 1100, entities)
        entity_api.list_entities.assert_has_calls(
            [
                mock.call(entity_type="entity_type", page_token=None, page_size=1000),
                mock.call(entity_type="entity_type", page_token="1000", page_size=1000),
            ]
        )
