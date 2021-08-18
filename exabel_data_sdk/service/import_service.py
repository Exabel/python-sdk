from typing import Mapping

import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.relationship import Relationship


class CsvImportService:
    def __init__(self, client: ExabelClient):
        self._client = client

    def _check_entity_format(self, entity_name: str) -> None:
        name_parts = entity_name.split("/")
        if len(name_parts) != 4:
            raise ValueError(f"Invalid resource name: {entity_name}")

    def _load_entities(self, entities_input: pd.DataFrame) -> Mapping[str, Entity]:

        for c in ["entity_resource_name", "display_name"]:
            if c not in entities_input.columns:
                raise ValueError(f"Missing required column in input: {c}")

        result = {}
        for i, entity in entities_input.iterrows():
            entity_name = entity["entity_resource_name"]
            try:
                self._check_entity_format(entity_name)
                name_parts = entity_name.split("/")
                entity_type = f"{name_parts[0]}/{name_parts[1]}"
                if not self._client.entity_api.entity_exists(entity_name):
                    entity = self._client.entity_api.create_entity(
                        entity=Entity(
                            name=entity_name,
                            display_name=entity["display_name"],
                            description=entity["description"]
                            if "description" in entities_input.columns
                            else "",
                            properties={},
                        ),
                        entity_type=entity_type,
                    )
                    result[entity_name] = entity
            except Exception as e:
                result[entity_name] = None
        return dict(result)

    def _load_relationships(
        self, relationships_input: pd.DataFrame, separator: str
    ) -> Mapping[str, Relationship]:

        for c in ["entity_from", "entity_to", "relationship_type"]:
            if c not in relationships_input.columns:
                raise ValueError(f"Missing required column in input: {c}")

        result = {}
        for i, relationship_input in relationships_input.iterrows():
            relationship_type_name = relationship_input["relationship_type"]
            entity_from_name = relationship_input["entity_from"]
            entity_to_name = relationship_input["entity_to"]
            relationship_key = (
                f"{entity_from_name}{separator}"
                f"{entity_to_name}{separator}"
                f"{relationship_type_name}"
            )

            relationship_type = self._client.relationship_api.get_relationship_type(
                name=relationship_type_name
            )
            if relationship_type is None:
                result[relationship_key] = None
            elif not self._client.entity_api.entity_exists(entity_from_name):
                result[relationship_key] = None
            elif not self._client.entity_api.entity_exists(entity_to_name):
                result[relationship_key] = None
            else:
                try:
                    relationship = self._client.relationship_api.create_relationship(
                        relationship=Relationship(
                            relationship_type=relationship_type_name,
                            from_entity=entity_from_name,
                            to_entity=entity_to_name,
                            description="",
                            properties={},
                        )
                    )
                    result[relationship_key] = relationship
                except Exception as e:
                    result[relationship_key] = None

        return dict(result)

    def create_relationships_from_csv(
        self, filename_input: str, separator: str
    ) -> Mapping[str, Relationship]:
        """
        Processes an input CSV file containing entity names and relationship
        types to create relationships.

        Returns a Mapping between input values and the Relationship object that
        was created. If the Relationship exists nothing will be returned for
        this relationship. If the relationship does not exist but creation
        fails, None will be returned for this relationship configuration.

        The CSV file should have a header line with the following fields
            entity_from;entity_to;relationship_type
        subsequently followed by rows of values. The separator is configurable
        using the script argument '--sep' and defaults to ';'.

        entity_from and entity_to are entity resource names and must be
        previously created in the Exabel platform.

        The relationship_type must be previously created in the Exabel platform.

        Example:
            entity_from;entity_to;relationship_type
            entityTypes/company/company_x;entityTypes/brand/test.brand_x;relationshipTypes/test.HAS_BRAND

        """
        relationships_input = pd.read_csv(filename_input, header=0, sep=separator)
        res = self._load_relationships(relationships_input, separator)
        return res

    def create_entities_from_csv(self, filename_input: str, separator: str) -> Mapping[str, Entity]:
        """
        Processes an input CSV file containing entity resource names and types
        to create entities.

        Returns a mapping between entity resource name from input and created
        Entity object. If the entity exists nothing will be returned for this
        entity. If the entity does not exist but creation fails, None will be
        returned for this entity resource name.

        The CSV file should have a header line with the following fields
            entity_resource_name;display_name;description
        subsequently followed by rows of values. The separator is configurable
        using the script argument '--sep' and defaults to ';'. The description
        field is optional.

        The entity_resource_name is on the following format:
        entityTypes/<entity_type>/entities/<entity_id>

        <entity_type>: an entity type defined in the Exabel platform. May be
        prefixed with a namespace.
        <entity_id>: must match the regex \\w[\\w-]{0,63}. May be prefixed with
        a namespace

        The display_name field is an Entity display_name.

        The description field is one or more paragraphs of text description.

        Example:
            entity_resource_name;display_name;description
            entityTypes/brand/entities/shazam;Shazam;Shazam description
            entityTypes/test.company_and_brand/entities/test.Apple-Shazam;Apple - Shazam;Apple and Shazam description

        """
        entities_input = pd.read_csv(filename_input, header=0, sep=separator)
        res = self._load_entities(entities_input)
        return res
