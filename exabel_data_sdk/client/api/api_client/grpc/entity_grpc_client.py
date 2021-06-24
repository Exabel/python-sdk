from exabel_data_sdk.client.api.api_client.entity_api_client import EntityApiClient
from exabel_data_sdk.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel_data_sdk.client.api.error_handler import handle_grpc_error
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    CreateEntityRequest,
    DeleteEntityRequest,
    Entity,
    EntityType,
    GetEntityRequest,
    GetEntityTypeRequest,
    ListEntitiesRequest,
    ListEntitiesResponse,
    ListEntityTypesRequest,
    ListEntityTypesResponse,
    SearchEntitiesRequest,
    SearchEntitiesResponse,
)
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2_grpc import EntityServiceStub


class EntityGrpcClient(EntityApiClient, BaseGrpcClient):
    """
    Client which sends entity requests to the Exabel Data API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config)
        self.stub = EntityServiceStub(self.channel)

    @handle_grpc_error
    def list_entity_types(self, request: ListEntityTypesRequest) -> ListEntityTypesResponse:
        return self.stub.ListEntityTypes(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def get_entity_type(self, request: GetEntityTypeRequest) -> EntityType:
        return self.stub.GetEntityType(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def list_entities(self, request: ListEntitiesRequest) -> ListEntitiesResponse:
        return self.stub.ListEntities(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def get_entity(self, request: GetEntityRequest) -> Entity:
        return self.stub.GetEntity(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def create_entity(self, request: CreateEntityRequest) -> Entity:
        return self.stub.CreateEntity(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def delete_entity(self, request: DeleteEntityRequest) -> None:
        self.stub.DeleteEntity(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def search_entities(self, request: SearchEntitiesRequest) -> SearchEntitiesResponse:
        return self.stub.SearchEntities(
            request, metadata=self.metadata, timeout=self.config.timeout
        )
