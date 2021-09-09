from exabel_data_sdk.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel_data_sdk.client.api.api_client.relationship_api_client import RelationshipApiClient
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
    ListRelationshipsResponse,
    ListRelationshipTypesRequest,
    ListRelationshipTypesResponse,
    Relationship,
    RelationshipType,
    UpdateRelationshipRequest,
    UpdateRelationshipTypeRequest,
)
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2_grpc import RelationshipServiceStub


class RelationshipGrpcClient(RelationshipApiClient, BaseGrpcClient):
    """
    Client which sends relationship requests to the Exabel Data API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config)
        self.stub = RelationshipServiceStub(self.channel)

    @handle_grpc_error
    def list_relationship_types(
        self, request: ListRelationshipTypesRequest
    ) -> ListRelationshipTypesResponse:
        return self.stub.ListRelationshipTypes(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def get_relationship_type(self, request: GetRelationshipTypeRequest) -> RelationshipType:
        return self.stub.GetRelationshipType(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def create_relationship_type(self, request: CreateRelationshipTypeRequest) -> RelationshipType:
        return self.stub.CreateRelationshipType(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def update_relationship_type(self, request: UpdateRelationshipTypeRequest) -> RelationshipType:
        return self.stub.UpdateRelationshipType(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def delete_relationship_type(self, request: DeleteRelationshipTypeRequest) -> None:
        return self.stub.DeleteRelationshipType(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def list_relationships(self, request: ListRelationshipsRequest) -> ListRelationshipsResponse:
        return self.stub.ListRelationships(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def get_relationship(self, request: GetRelationshipRequest) -> Relationship:
        return self.stub.GetRelationship(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def create_relationship(self, request: CreateRelationshipRequest) -> Relationship:
        return self.stub.CreateRelationship(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def update_relationship(self, request: UpdateRelationshipRequest) -> Relationship:
        return self.stub.UpdateRelationship(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def delete_relationship(self, request: DeleteRelationshipRequest) -> None:
        self.stub.DeleteRelationship(request, metadata=self.metadata, timeout=self.config.timeout)
