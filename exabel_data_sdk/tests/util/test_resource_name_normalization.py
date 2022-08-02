import unittest
from unittest import mock

import pandas as pd

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import SearchEntitiesResponse, SearchTerm
from exabel_data_sdk.util.resource_name_normalization import (
    _assert_no_collision,
    _validate_mic_ticker,
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
        result, _ = to_entity_resource_names(entity_api, data, namespace="acme")
        pd.testing.assert_series_equal(expected, result)

    def test_global_entity_type_mapping(self):
        data = pd.Series(["I_DE", "I_US", "", "abcXYZ0189"], name="country")
        expected = pd.Series(
            [
                "entityTypes/country/entities/I_DE",
                "entityTypes/country/entities/I_US",
                None,
                "entityTypes/country/entities/abcXYZ0189",
            ],
            name="entity",
        )
        entity_api = mock.create_autospec(EntityApi(ClientConfig(api_key="123"), use_json=True))
        entity_api.list_entity_types.side_effect = [
            [EntityType("entityTypes/country", "Countries", "Countries", True)]
        ]
        result, _ = to_entity_resource_names(entity_api, data, namespace="acme")
        pd.testing.assert_series_equal(expected, result)

    def test_validate_mic_ticker(self):
        self.assertTrue(_validate_mic_ticker("A:A"))

        self.assertFalse(_validate_mic_ticker(":A"))
        self.assertFalse(_validate_mic_ticker("A:"))
        self.assertFalse(_validate_mic_ticker("A:A:A"))
        self.assertFalse(_validate_mic_ticker("A::A"))
        self.assertFalse(_validate_mic_ticker("A"))

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
        search_terms = [
            SearchTerm(field="isin", query="US87612E1064"),
            SearchTerm(field="isin", query="DE000A1EWWW0"),
        ]
        entity_api = mock.create_autospec(EntityApi(ClientConfig(api_key="123"), use_json=True))
        entity_api.search.entities_by_terms.return_value = [
            SearchEntitiesResponse.SearchResult(
                terms=[search_terms[0]],
                entities=[
                    Entity("entityTypes/company/entities/target_inc", "Target, Inc.").to_proto(),
                ],
            ),
            SearchEntitiesResponse.SearchResult(
                terms=[search_terms[1]],
                entities=[
                    Entity("entityTypes/company/entities/adidas_ag", "Adidas Ag").to_proto(),
                ],
            ),
        ]
        result, _ = to_entity_resource_names(entity_api, data, namespace="acme")
        call_args_list = entity_api.search.entities_by_terms.call_args_list
        self.assertEqual(1, len(call_args_list))

        self.assertEqual(
            "entityTypes/company",
            call_args_list[0][1]["entity_type"],
            "Arguments not as expected",
        )
        self.assertSequenceEqual(
            search_terms,
            call_args_list[0][1]["terms"],
            "Arguments not as expected",
        )
        pd.testing.assert_series_equal(expected, result)

    def test_isin_mapping_with_entity_mapping(self):
        data = pd.Series(["US87612E1064", "do_not_search_for"], name="isin")
        entity_mapping = {
            "isin": {"do_not_search_for": "entityTypes/company/entities/was_not_searched_for"}
        }
        expected = pd.Series(
            [
                "entityTypes/company/entities/target_inc",
                "entityTypes/company/entities/was_not_searched_for",
            ],
            name="entity",
        )
        search_terms = [
            SearchTerm(field="isin", query="US87612E1064"),
        ]
        entity_api = mock.create_autospec(EntityApi(ClientConfig(api_key="123"), use_json=True))
        entity_api.search.entities_by_terms.return_value = [
            SearchEntitiesResponse.SearchResult(
                terms=[search_terms[0]],
                entities=[
                    Entity("entityTypes/company/entities/target_inc", "Target, Inc.").to_proto(),
                ],
            ),
        ]
        result, _ = to_entity_resource_names(
            entity_api, data, namespace="acme", entity_mapping=entity_mapping
        )
        call_args_list = entity_api.search.entities_by_terms.call_args_list
        self.assertEqual(1, len(call_args_list))
        self.assertEqual(
            "entityTypes/company",
            call_args_list[0][1]["entity_type"],
            "Arguments not as expected",
        )
        self.assertSequenceEqual(
            search_terms,
            call_args_list[0][1]["terms"],
            "Arguments not as expected",
        )
        pd.testing.assert_series_equal(expected, result)

    def test_entity_mapping(self):
        company_data = pd.Series(["TGT US", "ADI GE"], name="bloomberg_ticker")
        brand_data = pd.Series(
            [
                "should_be_mapped_not_normalized",
                "should be mapped not normalized",
                "should#be#mapped#not#normalized",
            ],
            name="brand",
        )
        entity_mapping = {
            "bloomberg_ticker": {
                "TGT US": "entityTypes/company/entities/target_inc",
                "ADI GE": "entityTypes/company/entities/adidas_ag",
            },
            "brand": {
                "should_be_mapped_not_normalized": "entityTypes/company/entities/brand",
                "should be mapped not normalized": "entityTypes/company/entities/other_brand",
                "should#be#mapped#not#normalized": "entityTypes/company/entities/another_brand",
            },
        }
        expected_companies = pd.Series(
            ["entityTypes/company/entities/target_inc", "entityTypes/company/entities/adidas_ag"],
            name="entity",
        )
        expected_brands = pd.Series(
            [
                "entityTypes/company/entities/brand",
                "entityTypes/company/entities/other_brand",
                "entityTypes/company/entities/another_brand",
            ],
            name="entity",
        )
        entity_api = mock.create_autospec(EntityApi(ClientConfig(api_key="123"), use_json=True))
        company_result, _ = to_entity_resource_names(
            entity_api, company_data, namespace="acme", entity_mapping=entity_mapping
        )
        self.assertFalse(entity_api.search_for_entities.called)
        pd.testing.assert_series_equal(expected_companies, company_result)

        brand_result, _ = to_entity_resource_names(
            entity_api, brand_data, namespace="acme", entity_mapping=entity_mapping
        )
        pd.testing.assert_series_equal(expected_brands, brand_result)

    def test_micticker_mapping(self):
        # Note that "NO?COLON" and "TOO:MANY:COLONS" are illegal mic:ticker identifiers,
        # since any legal identifier must contain exactly one colon.
        # The to_entity_resource_names function will print a warning for such illegal identifiers,
        # and they will not result in any searches towards the Exabel API.
        mic_tickers = [
            "XOSL:TEL",
            "XNAS:AAPL",
            "NO?COLON",
            "TOO:MANY:COLONS",
            "XOSL:ORK",
            "MANY:HITS",
            "NO:HITS",
        ]
        data = pd.Series(
            mic_tickers,
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
        search_terms = []
        for mic, ticker in map(lambda x: x.split(":"), mic_tickers[:2] + mic_tickers[4:]):
            search_terms.append(SearchTerm(field="mic", query=mic))
            search_terms.append(SearchTerm(field="ticker", query=ticker))
        entity_api = mock.create_autospec(EntityApi(ClientConfig(api_key="123"), use_json=True))
        entity_api.search.entities_by_terms.return_value = [
            SearchEntitiesResponse.SearchResult(
                terms=[search_terms[0]],
                entities=[
                    Entity("entityTypes/company/entities/telenor_asa", "Telenor ASA").to_proto(),
                ],
            ),
            SearchEntitiesResponse.SearchResult(
                terms=[search_terms[1]],
                entities=[
                    Entity("entityTypes/company/entities/apple_inc", "Apple, Inc.").to_proto(),
                ],
            ),
            SearchEntitiesResponse.SearchResult(
                terms=[search_terms[4]],
                entities=[
                    Entity("entityTypes/company/entities/orkla_asa", "Orkla ASA").to_proto(),
                ],
            ),
            # Result for "MANY:HITS"
            SearchEntitiesResponse.SearchResult(
                terms=[search_terms[5]],
                entities=[
                    Entity("entityTypes/company/entities/orkla_asa", "Orkla ASA").to_proto(),
                    Entity("entityTypes/company/entities/telenor_asa", "Telenor ASA").to_proto(),
                ],
            ),
            # Result for "NO:HITS"
            SearchEntitiesResponse.SearchResult(
                terms=[search_terms[6]],
                entities=[],
            ),
        ]
        result, _ = to_entity_resource_names(entity_api, data, namespace="acme")
        pd.testing.assert_series_equal(expected, result)

        # Check that the expected searches were performed
        call_args_list = entity_api.search.entities_by_terms.call_args_list
        self.assertEqual(1, len(call_args_list))
        self.assertEqual(
            "entityTypes/company",
            call_args_list[0][1]["entity_type"],
            "Arguments not as expected",
        )
        self.assertSequenceEqual(
            search_terms,
            call_args_list[0][1]["terms"],
            "Arguments not as expected",
        )

    def test_name_collision(self):
        bad_mapping = {"Abc!": "Abc_", "Abcd": "Abcd", "Abc?": "Abc_"}
        self.assertRaises(ValueError, _assert_no_collision, bad_mapping)
        good_mapping = {"Abc!": "Abc_1", "Abcd": "Abcd", "Abc?": "Abc_2"}
        _assert_no_collision(good_mapping)

    def test_mapping_with_duplicated_entity_identifiers_should_not_fail(self):
        search_terms = [
            SearchTerm(field="bloomberg_ticker", query="TGT US"),
            SearchTerm(field="bloomberg_ticker", query="TGT UK"),
        ]
        entity_api = mock.create_autospec(EntityApi(ClientConfig(api_key="123"), use_json=True))
        entity_api.search.entities_by_terms.return_value = [
            SearchEntitiesResponse.SearchResult(
                terms=[search_terms[0]],
                entities=[
                    Entity("entityTypes/company/entities/F_000C7F-E", "Target, Inc.").to_proto(),
                ],
            ),
            SearchEntitiesResponse.SearchResult(
                terms=[search_terms[1]],
                entities=[
                    Entity("entityTypes/company/entities/F_000C7F-E", "Target, Inc.").to_proto(),
                ],
            ),
        ]
