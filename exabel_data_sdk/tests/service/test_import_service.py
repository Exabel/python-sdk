import unittest
from unittest import mock

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.service.import_service import CsvImportService, ResourceCreationStatus

ENTITY_WITH_DESCRIPTION = Entity(
    name="entityTypes/brand/entities/test.BRAND_X",
    display_name="BRAND_X",
    description="BRAND_X description",
    properties={},
)

ENTITY_WITHOUT_DESCRIPTION = Entity(
    name="entityTypes/brand/entities/test.BRAND_X",
    display_name="BRAND_X",
    description="",
    properties={},
)

RELATIONSHIP = Relationship(
    relationship_type="relationshipTypes/test.HAS_BRAND",
    from_entity="entityTypes/company/company_x",
    to_entity="entityTypes/brand/test.brand_x",
    description="",
    properties={},
)


class TestCsvImportService(unittest.TestCase):
    def test_create_entities(self):
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        client.entity_api.get_entity.return_value = None
        client.entity_api.create_entity.return_value = ENTITY_WITH_DESCRIPTION
        service = CsvImportService(client)
        result = service.create_entities_from_csv(
            filename_input="./exabel_data_sdk/tests/resources/data/entities_with_description.csv",
            separator=";",
        )

        # first row
        # entityTypes/brand/test.brand_y;brand_y;brand_y description
        # fails with ValueError
        self.assertEqual(
            result["entityTypes/brand/test.brand_y"].status,
            ResourceCreationStatus.FAILED,
            "FAIL status expected",
        )
        self.assertEqual(
            result["entityTypes/brand/test.brand_y"].resource, None, "No entity expected"
        )

        # second row
        # entityTypes/brand/entities/test.BRAND_X;BRAND_X;BRAND_X description
        call_args = client.entity_api.create_entity.call_args_list[0]
        _, kwargs = call_args
        self.assertEqual(
            {
                "entity": ENTITY_WITH_DESCRIPTION,
                "entity_type": "entityTypes/brand",
            },
            kwargs,
            "Arguments not as expected",
        )
        self.assertEqual(
            result["entityTypes/brand/entities/test.BRAND_X"].status,
            ResourceCreationStatus.CREATED,
            "CREATED status expected",
        )
        self.assertEqual(
            result["entityTypes/brand/entities/test.BRAND_X"].resource, ENTITY_WITH_DESCRIPTION
        )

    def test_create_entities_with_existing_entity(self):

        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        client.entity_api.get_entity.return_value = ENTITY_WITH_DESCRIPTION
        service = CsvImportService(client)
        result = service.create_entities_from_csv(
            filename_input="./exabel_data_sdk/tests/resources/data/entities_with_description.csv",
            separator=";",
        )

        # first row
        # entityTypes/brand/test.brand_y;brand_y;brand_y description
        # fails with ValueError
        self.assertEqual(
            result["entityTypes/brand/test.brand_y"].status,
            ResourceCreationStatus.FAILED,
            "FAIL status expected",
        )
        self.assertEqual(
            result["entityTypes/brand/test.brand_y"].resource, None, "No entity expected"
        )

        # second row
        # entityTypes/brand/entities/test.BRAND_X;BRAND_X;BRAND_X description
        self.assertEqual(client.entity_api.create_entity.call_args_list, [], "Unexpected call")
        self.assertEqual(
            result["entityTypes/brand/entities/test.BRAND_X"].status,
            ResourceCreationStatus.EXISTS,
            "EXISTS status expected",
        )
        self.assertEqual(
            result["entityTypes/brand/entities/test.BRAND_X"].resource, ENTITY_WITH_DESCRIPTION
        )

    def test_create_entities_without_description(self):

        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        client.entity_api.get_entity.return_value = None
        client.entity_api.create_entity.return_value = ENTITY_WITHOUT_DESCRIPTION
        service = CsvImportService(client)
        result = service.create_entities_from_csv(
            filename_input="./exabel_data_sdk/tests/resources/data/"
            "entities_without_description.csv",
            separator=";",
        )

        # first row
        # entityTypes/brand/entities/test.BRAND_X;BRAND_X
        call_args = client.entity_api.create_entity.call_args_list[0]
        _, kwargs = call_args
        self.assertEqual(
            {
                "entity": ENTITY_WITHOUT_DESCRIPTION,
                "entity_type": "entityTypes/brand",
            },
            kwargs,
            "Arguments not as expected",
        )
        self.assertEqual(
            result["entityTypes/brand/entities/test.BRAND_X"].status,
            ResourceCreationStatus.CREATED,
            "CREATED expected",
        )
        self.assertEqual(
            result["entityTypes/brand/entities/test.BRAND_X"].resource, ENTITY_WITHOUT_DESCRIPTION
        )

    def test_create_relationship(self):

        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        client.entity_api.entity_exists.return_value = True
        client.relationship_api.get_relationship.return_value = None
        client.relationship_api.create_relationship.return_value = RELATIONSHIP
        service = CsvImportService(client)
        result = service.create_relationships_from_csv(
            filename_input="./exabel_data_sdk/tests/resources/data/relationships.csv", separator=";"
        )

        # entityTypes/company/company_x;
        # entityTypes/brand/test.brand_x;
        # relationshipTypes/test.HAS_BRAND
        call_args = client.relationship_api.create_relationship.call_args_list[0]
        _, kwargs = call_args
        self.assertEqual(
            {"relationship": RELATIONSHIP},
            kwargs,
            "Arguments not as expected",
        )
        self.assertEqual(
            result[
                "entityTypes/company/company_x;"
                "entityTypes/brand/test.brand_x;"
                "relationshipTypes/test.HAS_BRAND"
            ].status,
            ResourceCreationStatus.CREATED,
            "CREATED status expected",
        )
        self.assertEqual(
            result[
                "entityTypes/company/company_x;"
                "entityTypes/brand/test.brand_x;"
                "relationshipTypes/test.HAS_BRAND"
            ].resource,
            RELATIONSHIP,
        )

    def test_create_relationship_and_relationship_exists(self):

        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        client.entity_api.entity_exists.return_value = True
        client.relationship_api.get_relationship.return_value = RELATIONSHIP
        service = CsvImportService(client)
        result = service.create_relationships_from_csv(
            filename_input="./exabel_data_sdk/tests/resources/data/relationships.csv", separator=";"
        )

        # entityTypes/company/company_x;
        # entityTypes/brand/test.brand_x;
        # relationshipTypes/test.HAS_BRAND
        self.assertEqual(
            result[
                "entityTypes/company/company_x;"
                "entityTypes/brand/test.brand_x;"
                "relationshipTypes/test.HAS_BRAND"
            ].status,
            ResourceCreationStatus.EXISTS,
            "EXISTS status expected",
        )
        self.assertEqual(
            result[
                "entityTypes/company/company_x;"
                "entityTypes/brand/test.brand_x;"
                "relationshipTypes/test.HAS_BRAND"
            ].resource,
            RELATIONSHIP,
        )

    def test_create_relationship_and_entity_does_not_exist(self):

        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        client.entity_api.entity_exists.return_value = False
        service = CsvImportService(client)
        result = service.create_relationships_from_csv(
            filename_input="./exabel_data_sdk/tests/resources/data/relationships.csv", separator=";"
        )

        # entityTypes/company/company_x;
        # entityTypes/brand/test.brand_x;
        # relationshipTypes/test.HAS_BRAND
        self.assertEqual(
            result[
                "entityTypes/company/company_x;"
                "entityTypes/brand/test.brand_x;"
                "relationshipTypes/test.HAS_BRAND"
            ].status,
            ResourceCreationStatus.FAILED,
            "FAILED status expected",
        )
        self.assertEqual(
            result[
                "entityTypes/company/company_x;"
                "entityTypes/brand/test.brand_x;"
                "relationshipTypes/test.HAS_BRAND"
            ].resource,
            None,
            "Ne entity expected",
        )

    def test_create_relationship_and_relationship_type_does_not_exist(self):

        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        client.relationship_api.get_relationship_type.return_value = None
        service = CsvImportService(client)
        result = service.create_relationships_from_csv(
            filename_input="./exabel_data_sdk/tests/resources/data/relationships.csv", separator=";"
        )

        # entityTypes/company/company_x;
        # entityTypes/brand/test.brand_x;
        # relationshipTypes/test.HAS_BRAND
        self.assertEqual(
            result[
                "entityTypes/company/company_x;"
                "entityTypes/brand/test.brand_x;"
                "relationshipTypes/test.HAS_BRAND"
            ].status,
            ResourceCreationStatus.FAILED,
            "FAILED status expected",
        )
        self.assertEqual(
            result[
                "entityTypes/company/company_x;"
                "entityTypes/brand/test.brand_x;"
                "relationshipTypes/test.HAS_BRAND"
            ].resource,
            None,
            "Ne entity expected",
        )

    def test_create_relationship_and_create_throws_exception(self):

        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        client.entity_api.entity_exists.return_value = True
        client.relationship_api.get_relationship.return_value = None
        client.relationship_api.create_relationship.side_effect = ValueError("Create failed")
        service = CsvImportService(client)
        result = service.create_relationships_from_csv(
            filename_input="./exabel_data_sdk/tests/resources/data/relationships.csv", separator=";"
        )

        # entityTypes/company/company_x;
        # entityTypes/brand/test.brand_x;
        # relationshipTypes/test.HAS_BRAND
        self.assertEqual(
            result[
                "entityTypes/company/company_x;"
                "entityTypes/brand/test.brand_x;"
                "relationshipTypes/test.HAS_BRAND"
            ].status,
            ResourceCreationStatus.FAILED,
            "FAILED status expected",
        )
        self.assertEqual(
            result[
                "entityTypes/company/company_x;"
                "entityTypes/brand/test.brand_x;"
                "relationshipTypes/test.HAS_BRAND"
            ].resource,
            None,
            "Ne entity expected",
        )


if __name__ == "__main__":
    unittest.main()
