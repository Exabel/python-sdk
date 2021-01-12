from exabel_data_sdk.client.api.base_api import BaseApi
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.data_classes.relationship_type import RelationshipType
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.api.error_handler import handle_grpc_error
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
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2_grpc import RelationshipServiceStub


class RelationshipApi(BaseApi):
    """
    API class for entity relationship CRUD operations.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config)
        self.stub = RelationshipServiceStub(self.channel)

    @handle_grpc_error
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
        response = self.stub.ListRelationshipTypes(
            ListRelationshipTypesRequest(page_size=page_size, page_token=page_token),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return PagingResult(
            results=[RelationshipType.from_proto(t) for t in response.relationship_types],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    @handle_grpc_error
    def get_relationship_type(self, name: str) -> RelationshipType:
        """
        Get one relationship type.

        Args:
            name:   The resource name of the requested relationship type, for example
                    "relationshipTypes/ns.type1"
        """
        response = self.stub.GetRelationshipType(
            GetRelationshipTypeRequest(name=name),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return RelationshipType.from_proto(response)

    @handle_grpc_error
    def create_relationship_type(self, relationship_type: RelationshipType) -> RelationshipType:
        """
        Create a relationship type.

        Args:
            relationship_type: The relationship type to create.
        """
        response = self.stub.CreateRelationshipType(
            CreateRelationshipTypeRequest(relationship_type=relationship_type.to_proto()),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return RelationshipType.from_proto(response)

    @handle_grpc_error
    def delete_relationship_type(self, relationship_type: str) -> None:
        """
        Delete a relationship type.

        A relationship type cannot be deleted if there exist relationships with the type.

        Args:
            relationship_type: The relationship type to delete.
        """
        self.stub.DeleteRelationshipType(
            DeleteRelationshipTypeRequest(name=relationship_type),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )

    @handle_grpc_error
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
        response = self.stub.ListRelationships(
            ListRelationshipsRequest(
                parent=relationship_type,
                from_entity=from_entity,
                page_size=page_size,
                page_token=page_token,
            ),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return PagingResult(
            results=[Relationship.from_proto(r) for r in response.relationships],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    @handle_grpc_error
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
        response = self.stub.ListRelationships(
            ListRelationshipsRequest(
                parent=relationship_type,
                to_entity=to_entity,
                page_size=page_size,
                page_token=page_token,
            ),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return PagingResult(
            results=[Relationship.from_proto(r) for r in response.relationships],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    @handle_grpc_error
    def get_relationship(
        self, relationship_type: str, from_entity: str, to_entity: str
    ) -> Relationship:
        """
        Get one relationship.

        Args:
            relationship_type:  The type of the relationship, for example
                                "relationshipTypes/ns.type1".
            from_entity:        The resource name of the start point of the relationship,
                                for example "entityTypes/ns.type1/entities/ns.entity1".
            to_entity:          The resource name of the end point of the relationship, for example
                                "entityTypes/ns.type2/entities/ns.entity2".
        """
        response = self.stub.GetRelationship(
            GetRelationshipRequest(
                parent=relationship_type, from_entity=from_entity, to_entity=to_entity
            ),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return Relationship.from_proto(response)

    @handle_grpc_error
    def create_relationship(self, relationship: Relationship) -> Relationship:
        """
        Create a relationship between two entities.

        Args:
            relationship:  The relationship to create.
        """
        response = self.stub.CreateRelationship(
            CreateRelationshipRequest(relationship=relationship.to_proto()),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return Relationship.from_proto(response)

    @handle_grpc_error
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
        self.stub.DeleteRelationship(
            DeleteRelationshipRequest(
                parent=relationship_type, from_entity=from_entity, to_entity=to_entity
            ),
            metadata=self.metadata,
            timeout=self.config.timeout,
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
        try:
            self.get_relationship(relationship_type, from_entity, to_entity)
            return True
        except RequestError as error:
            if error.error_type is ErrorType.NOT_FOUND:
                return False
            raise
