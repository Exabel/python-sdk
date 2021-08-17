from typing import Optional

from exabel_data_sdk.client.api.api_client.grpc.relationship_grpc_client import (
    RelationshipGrpcClient,
)
from exabel_data_sdk.client.api.api_client.http.relationship_http_client import (
    RelationshipHttpClient,
)
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.data_classes.relationship_type import RelationshipType
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    CreateRelationshipRequest,
    CreateRelationshipTypeRequest,
    DeleteRelationshipRequest,
    DeleteRelationshipTypeRequest,
    GetRelationshipRequest,
    GetRelationshipTypeRequest,
    ListRelationshipsRequest,
    ListRelationshipTypesRequest,
)


class RelationshipApi:
    """
    API class for entity relationship CRUD operations.
    """

    def __init__(self, config: ClientConfig, use_json: bool = False):
        self.client = (RelationshipHttpClient if use_json else RelationshipGrpcClient)(config)

    def list_relationship_types(
        self, page_size: int = 1000, page_token: str = None
    ) -> PagingResult[RelationshipType]:
        """
        List all relationship types.

        Args:
            page_size:  The maximum number of results to return. Defaults to 1000, which is
                        also the maximum size of this field.
            page_token: The page token to resume the results from.
        """
        response = self.client.list_relationship_types(
            ListRelationshipTypesRequest(page_size=page_size, page_token=page_token)
        )
        return PagingResult(
            results=[RelationshipType.from_proto(t) for t in response.relationship_types],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    def get_relationship_type(self, name: str) -> Optional[RelationshipType]:
        """
        Get one relationship type.

        Return None if the relationship type does not exist.

        Args:
            name:   The resource name of the requested relationship type, for example
                    "relationshipTypes/ns.type1"
        """
        try:
            response = self.client.get_relationship_type(GetRelationshipTypeRequest(name=name))
        except RequestError as error:
            if error.error_type == ErrorType.NOT_FOUND:
                return None
            raise
        return RelationshipType.from_proto(response)

    def create_relationship_type(self, relationship_type: RelationshipType) -> RelationshipType:
        """
        Create a relationship type.

        Args:
            relationship_type: The relationship type to create.
        """
        response = self.client.create_relationship_type(
            CreateRelationshipTypeRequest(relationship_type=relationship_type.to_proto())
        )
        return RelationshipType.from_proto(response)

    def delete_relationship_type(self, relationship_type: str) -> None:
        """
        Delete a relationship type.

        A relationship type cannot be deleted if there exist relationships with the type.

        Args:
            relationship_type: The relationship type to delete.
        """
        self.client.delete_relationship_type(DeleteRelationshipTypeRequest(name=relationship_type))

    def get_relationships_from_entity(
        self,
        relationship_type: str,
        from_entity: str,
        page_size: int = 1000,
        page_token: str = None,
    ) -> PagingResult[Relationship]:
        """
        Get relationships from the given entity.

        Args:
            relationship_type:  The resource name of the relationship type, for example
                                "relationshipTypes/namespace.relationshipTypeIdentifier"
            from_entity:        The resource name of the start point of the relationship,
                                for example "entityTypes/ns.type1/entities/ns.entity1".
            page_size:          The maximum number of results to return. Defaults to 1000, which is
                                also the maximum size of this field.
            page_token:         The page token to resume the results from, as returned from a
                                previous invocation of the method.
        """
        response = self.client.list_relationships(
            ListRelationshipsRequest(
                parent=relationship_type,
                from_entity=from_entity,
                page_size=page_size,
                page_token=page_token,
            )
        )
        return PagingResult(
            results=[Relationship.from_proto(r) for r in response.relationships],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    def get_relationships_to_entity(
        self,
        relationship_type: str,
        to_entity: str,
        page_size: int = 1000,
        page_token: str = None,
    ) -> PagingResult[Relationship]:
        """
        Get relationships to the given entity.

        Args:
            relationship_type:  The resource name of the relationship type, for example
                                "relationshipTypes/namespace.relationshipTypeIdentifier".
            to_entity:          The resource name of the end point of the relationship,
                                for example "entityTypes/ns.type1/entities/ns.entity1".
            page_size:          The maximum number of results to return. Defaults to 1000, which is
                                also the maximum size of this field.
            page_token:         The page token to resume the results from, as returned from a
                                previous invocation of the method.
        """
        response = self.client.list_relationships(
            ListRelationshipsRequest(
                parent=relationship_type,
                to_entity=to_entity,
                page_size=page_size,
                page_token=page_token,
            )
        )
        return PagingResult(
            results=[Relationship.from_proto(r) for r in response.relationships],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    def get_relationship(
        self, relationship_type: str, from_entity: str, to_entity: str
    ) -> Optional[Relationship]:
        """
        Get one relationship.

        Return None if the relationship does not exist.

        Args:
            relationship_type:  The type of the relationship, for example
                                "relationshipTypes/ns.type1".
            from_entity:        The resource name of the start point of the relationship,
                                for example "entityTypes/ns.type1/entities/ns.entity1".
            to_entity:          The resource name of the end point of the relationship, for example
                                "entityTypes/ns.type2/entities/ns.entity2".
        """
        try:
            response = self.client.get_relationship(
                GetRelationshipRequest(
                    parent=relationship_type, from_entity=from_entity, to_entity=to_entity
                )
            )
        except RequestError as error:
            if error.error_type == ErrorType.NOT_FOUND:
                return None
            raise
        return Relationship.from_proto(response)

    def create_relationship(self, relationship: Relationship) -> Relationship:
        """
        Create a relationship between two entities.

        Args:
            relationship:  The relationship to create.
        """
        response = self.client.create_relationship(
            CreateRelationshipRequest(relationship=relationship.to_proto())
        )
        return Relationship.from_proto(response)

    def delete_relationship(self, relationship_type: str, from_entity: str, to_entity: str) -> None:
        """
        Delete a relationship.

        Args:
            relationship_type:  The relationship type, for example "relationshipTypes/ns.type1".
            from_entity:        The resource name of the start point of the relationship,
                                for example "entityTypes/ns.type1/entities/ns.entity1".
            to_entity:          The resource name of the end point of the relationship,
                                for example "entityTypes/ns.type2/entities/ns.entity2".
        """
        self.client.delete_relationship(
            DeleteRelationshipRequest(
                parent=relationship_type, from_entity=from_entity, to_entity=to_entity
            )
        )

    def relationship_exists(self, relationship_type: str, from_entity: str, to_entity: str) -> bool:
        """
        Determine whether a relationship already exists.

        Args:
            relationship_type:  The relationship type, for example "relationshipTypes/ns.type1".
            from_entity:        The resource name of the start point of the relationship,
                                for example "entityTypes/ns.type1/entities/ns.entity1".
            to_entity:          The resource name of the end point of the relationship,
                                for example "entityTypes/ns.type2/entities/ns.entity2".
        """
        return self.get_relationship(relationship_type, from_entity, to_entity) is not None
