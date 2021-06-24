from exabel_data_sdk.client.api.api_client.entity_api_client import EntityApiClient
from exabel_data_sdk.client.api.api_client.http.base_http_client import BaseHttpClient
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


class EntityHttpClient(EntityApiClient, BaseHttpClient):
    """
    Client which sends entity requests to the Exabel Data API with JSON over gRPC.
    """

    def list_entity_types(self, request: ListEntityTypesRequest) -> ListEntityTypesResponse:
        return self._request("GET", "entityTypes", ListEntityTypesResponse(), body=request)

    def get_entity_type(self, request: GetEntityTypeRequest) -> EntityType:
        return self._request("GET", request.name, EntityType())

    def list_entities(self, request: ListEntitiesRequest) -> ListEntitiesResponse:
        return self._request(
            "GET", f"{request.parent}/entities", ListEntitiesResponse(), body=request
        )

    def get_entity(self, request: GetEntityRequest) -> Entity:
        return self._request("GET", request.name, Entity())

    def create_entity(self, request: CreateEntityRequest) -> Entity:
        return self._request("POST", f"{request.parent}/entities", Entity(), body=request.entity)

    def delete_entity(self, request: DeleteEntityRequest) -> None:
        return self._request("DELETE", f"{request.name}", None)

    def search_entities(self, request: SearchEntitiesRequest) -> SearchEntitiesResponse:
        return self._request(
            "POST", f"{request.parent}/entities:search", SearchEntitiesResponse(), body=request
        )
