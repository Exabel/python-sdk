import unittest
from unittest import mock

import pandas as pd

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.util.resource_name_normalization import (
    normalize_resource_name,
    to_entity_resource_names,
)


class TestResourceNameNormalization(unittest.TestCase):
    def test_basic(self):
        self.assertEqual("abc_Inc_", normalize_resource_name("abc, Inc."))
        self.assertEqual("abcXYZ0189-_", normalize_resource_name("abcXYZ0189-_"))
        self.assertEqual("_l_", normalize_resource_name("-Øl?."))
        long_name = "".join(str(i) for i in range(50))
        self.assertEqual(long_name[:64], normalize_resource_name(long_name))
        self.assertRaises(ValueError, normalize_resource_name, "")

    def test_entity_type_mapping(self):
        data = pd.Series(["abc, Inc.", "abcXYZ0189-_", "", "-Øl?."], name="brand")
        expected = pd.Series(
            [
                "entityTypes/brand/entities/acme.abc_Inc_",
                "entityTypes/brand/entities/acme.abcXYZ0189-_",
                None,
                "entityTypes/brand/entities/acme._l_",
            ],
            name="entity",
        )
        entity_api = mock.create_autospec(EntityApi(ClientConfig(api_key="123"), use_json=True))
        result = to_entity_resource_names(entity_api, data, namespace="acme")
        pd.testing.assert_series_equal(expected, result)

    def test_isin_mapping(self):
        data = pd.Series(["US87612E1064", "DE000A1EWWW0", "US87612E1064"], name="isin")
        expected = pd.Series(
            [
                "entityTypes/company/entities/target_inc",
                "entityTypes/company/entities/adidas_ag",
                "entityTypes/company/entities/target_inc",
            ],
            name="entity",
        )
        entity_api = mock.create_autospec(EntityApi(ClientConfig(api_key="123"), use_json=True))
        entity_api.search_for_entities.side_effect = [
            [Entity("entityTypes/company/entities/target_inc", "Target, Inc.")],
            [Entity("entityTypes/company/entities/adidas_ag", "Adidas Ag")],
        ]
        result = to_entity_resource_names(entity_api, data, namespace="acme")
        call_args_list = entity_api.search_for_entities.call_args_list
        self.assertEqual(2, len(call_args_list))
        self.assertEqual(
            {"entity_type": "entityTypes/company", "isin": "US87612E1064"},
            call_args_list[0][1],
            "Arguments not as expected",
        )
        self.assertEqual(
            {"entity_type": "entityTypes/company", "isin": "DE000A1EWWW0"},
            call_args_list[1][1],
            "Arguments not as expected",
        )
        pd.testing.assert_series_equal(expected, result)
