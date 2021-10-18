import unittest
from unittest import mock

import pandas as pd

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.util.resource_name_normalization import (
    _assert_no_collision,
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

    def test_micticker_mapping(self):
        # Note that "NO?COLON" and "TOO:MANY:COLONS" are illegal mic:ticker identifiers,
        # since any legal identifier must contain exactly one colon.
        # The to_entity_resource_names function will print a warning for such illegal identifiers,
        # and they will not result in any searches towards the Exabel API.
        data = pd.Series(
            [
                "XOSL:TEL",
                "XNAS:AAPL",
                "NO?COLON",
                "TOO:MANY:COLONS",
                "XOSL:ORK",
                "MANY:HITS",
                "NO:HITS",
            ],
            name="mic:ticker",
        )
        expected = pd.Series(
            [
                "entityTypes/company/entities/telenor_asa",
                "entityTypes/company/entities/apple_inc",
                None,
                None,
                "entityTypes/company/entities/orkla_asa",
                None,
                None,
            ],
            name="entity",
        )
        entity_api = mock.create_autospec(EntityApi(ClientConfig(api_key="123"), use_json=True))
        entity_api.search_for_entities.side_effect = [
            [Entity("entityTypes/company/entities/telenor_asa", "Telenor ASA")],
            [Entity("entityTypes/company/entities/apple_inc", "Apple, Inc.")],
            [Entity("entityTypes/company/entities/orkla_asa", "Orkla ASA")],
            # Result for "MANY:HITS"
            [
                Entity("entityTypes/company/entities/orkla_asa", "Orkla ASA"),
                Entity("entityTypes/company/entities/telenor_asa", "Telenor ASA"),
            ],
            # Result for "NO:HITS"
            [],
        ]
        result = to_entity_resource_names(entity_api, data, namespace="acme")
        pd.testing.assert_series_equal(expected, result)

        # Check that the expected searches were performed
        call_args_list = entity_api.search_for_entities.call_args_list
        expected_searches = ["XOSL:TEL", "XNAS:AAPL", "XOSL:ORK", "MANY:HITS", "NO:HITS"]
        self.assertEqual(len(expected_searches), len(call_args_list))
        for i, identifier in enumerate(expected_searches):
            mic, ticker = identifier.split(":")
            self.assertEqual(
                {"entity_type": "entityTypes/company", "mic": mic, "ticker": ticker},
                call_args_list[i][1],
                "Arguments not as expected",
            )

    def test_name_collision(self):
        bad_mapping = {"Abc!": "Abc_", "Abcd": "Abcd", "Abc?": "Abc_"}
        self.assertRaises(SystemExit, _assert_no_collision, bad_mapping)
        good_mapping = {"Abc!": "Abc_1", "Abcd": "Abcd", "Abc?": "Abc_2"}
        _assert_no_collision(good_mapping)
