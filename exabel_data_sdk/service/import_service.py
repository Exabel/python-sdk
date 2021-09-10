import logging
from enum import Enum
from typing import Generic, Mapping, Optional, TypeVar

import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.relationship import Relationship

TResource = TypeVar("TResource")


class ResourceCreationStatus(Enum):
    """
    Status values for resource creation.
    """

    # Denotes that a resource was created.
    CREATED = 1

    # Denotes that a resource already existed.
    EXISTS = 2

    # Denotes that creation failed.
    FAILED = 3


class ResourceCreationResult(Generic[TResource]):
    """
    Class for returning resource creation results.
    """

    def __init__(self, status: ResourceCreationStatus, resource: Optional[TResource]):
        self.status = status
        self.resource = resource


class CsvImportService:
    """
    Services for importing objects using CSV files
    """

    def __init__(self, client: ExabelClient):
        self._client = client
        self._logger = logging.getLogger(__name__)

    def _check_entity_format(self, entity_name: str) -> None:
        name_parts = entity_name.split("/")
        if len(name_parts) != 4:
            raise ValueError(f"Invalid resource name: {entity_name}")

    def _load_entities(
        self, entities_input: pd.DataFrame
    ) -> Mapping[str, ResourceCreationResult[Entity]]:

        for c in ["entity_resource_name", "display_name"]:
            if c not in entities_input.columns:
                raise ValueError(f"Missing required column in input: {c}")

        result = {}
        for _, entity_input in entities_input.iterrows():
            entity_name = entity_input["entity_resource_name"]
            try:
                self._check_entity_format(entity_name)
                entity = self._client.entity_api.get_entity(entity_name)
                if entity is None:
                    name_parts = entity_name.split("/")
                    entity = self._client.entity_api.create_entity(
                        entity=Entity(
                            name=entity_name,
                            display_name=entity_input["display_name"],
                            description=entity_input["description"]
                            if "description" in entities_input.columns
                            else "",
                            properties={},
                        ),
                        entity_type=f"{name_parts[0]}/{name_parts[1]}",
                    )
                    result[entity_name] = ResourceCreationResult(
                        ResourceCreationStatus.CREATED, entity
                    )
                else:
                    result[entity_name] = ResourceCreationResult(
                        ResourceCreationStatus.EXISTS, entity
                    )
            # pylint: disable=broad-except
            except Exception as e:
                self._logger.warning("Failed to create entity '%s': %s", entity_name, e)
                result[entity_name] = ResourceCreationResult(ResourceCreationStatus.FAILED, None)
        return result

    def _load_relationships(
        self, relationships_input: pd.DataFrame, separator: str
    ) -> Mapping[str, ResourceCreationResult[Relationship]]:

        for c in ["entity_from", "entity_to", "relationship_type"]:
            if c not in relationships_input.columns:
                raise ValueError(f"Missing required column in input: {c}")

        results = {}
        for _, relationship_input in relationships_input.iterrows():
            relationship_type_name = relationship_input["relationship_type"]
            entity_from_name = relationship_input["entity_from"]
            entity_to_name = relationship_input["entity_to"]
            relationship_key = (
                f"{entity_from_name}{separator}"
                f"{entity_to_name}{separator}"
                f"{relationship_type_name}"
            )
            result: ResourceCreationResult[Relationship]

            relationship_type = self._client.relationship_api.get_relationship_type(
                name=relationship_type_name
            )
            if relationship_type is None:
                self._logger.warning("Relationship type %s does not exist", relationship_type_name)
                result = ResourceCreationResult(ResourceCreationStatus.FAILED, None)
            elif not self._client.entity_api.entity_exists(entity_from_name):
                self._logger.warning("From entity %s does not exist", entity_from_name)
                result = ResourceCreationResult(ResourceCreationStatus.FAILED, None)
            elif not self._client.entity_api.entity_exists(entity_to_name):
                self._logger.warning("To entity %s does not exist", entity_to_name)
                result = ResourceCreationResult(ResourceCreationStatus.FAILED, None)
            else:
                relationship = self._client.relationship_api.get_relationship(
                    relationship_type_name, entity_from_name, entity_to_name
                )
                if relationship is None:
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
                        result = ResourceCreationResult(
                            ResourceCreationStatus.CREATED, relationship
                        )
                    # pylint: disable=broad-except
                    except Exception as e:
                        self._logger.warning(
                            "Failed to create relationship '%s': %s", relationship_key, e
                        )
                        result = ResourceCreationResult(ResourceCreationStatus.FAILED, None)
                else:
                    result = ResourceCreationResult(ResourceCreationStatus.EXISTS, relationship)

            assert result is not None
            results[relationship_key] = result

        return results

    def create_entities_from_csv(
        self, filename_input: str, separator: str
    ) -> Mapping[str, ResourceCreationResult[Entity]]:
        """
        Creates entities as defined in a CSV input file and returns a mapping between the entity
        resource names and the created Entity objects.

        The result of the upload is returned in a ResourceCreationResult mapping. The
        ResourceCreationResult object has 2 fields, status for entity creation status and resource
        for the entity itself. Valid values for status are:
        CREATED - the entity was created and is returned in the resource field
        EXISTS - the entity already exists and is returned in the resource field
        FAILED - entity creation failed and None is returned in the resource field. The reason for
        failure is logged.

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

        The display_name field is an entity display_name.

        The description field is one or more paragraphs of text description.

        Example:
            entity_resource_name;display_name;description
            entityTypes/brand/entities/shazam;Shazam;Shazam description
            entityTypes/test.company_and_brand/entities/test.Apple-Shazam;Apple - Shazam;Apple and Shazam description#pylint: disable=line-too-long

        """  # noqa
        entities_input = pd.read_csv(filename_input, header=0, sep=separator)
        return self._load_entities(entities_input)

    def create_relationships_from_csv(
        self, filename_input: str, separator: str
    ) -> Mapping[str, ResourceCreationResult[Relationship]]:
        """
        Creates relationships as defined in a CSV input file and returns a mapping between
        the input values and the created Relationship objects.

        The result of the upload is returned in a ResourceCreationResult mapping. The
        ResourceCreationResult object has 2 fields, status for relationship creation status and
        resource for the relationship itself. Valid values for status are:
        CREATED - the relationship was created and is returned in the resource field
        EXISTS - the relationship already exists and is returned in the resource field
        FAILED - relationship creation failed and None is returned in the resource field. The
        reason for failure is logged.

        The CSV file should have a header line with the following fields
            entity_from;entity_to;relationship_type
        subsequently followed by rows of values. The separator is configurable
        using the script argument '--sep' and defaults to ';'.
        The key for the return mapping is a concatenation of the values in entity_from, entity_to
        and relationship_type using the same separator as the input.

        entity_from and entity_to are entity resource names and must be
        previously created in the Exabel platform.

        The relationship_type must be previously created in the Exabel platform.

        Example:
            entity_from;entity_to;relationship_type
            entityTypes/company/entities/company_x;entityTypes/brand/entities/test.brand_x;relationshipTypes/test.HAS_BRAND#pylint: disable=line-too-long

        """  # noqa
        relationships_input = pd.read_csv(filename_input, header=0, sep=separator)
        return self._load_relationships(relationships_input, separator)
