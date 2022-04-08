from exabel_data_sdk.client.api.api_client.entity_api_client import EntityApiClient
from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.http.base_http_client import BaseHttpClient
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    CreateEntityRequest,
    CreateEntityTypeRequest,
    DeleteEntitiesRequest,
    DeleteEntityRequest,
    DeleteEntityTypeRequest,
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
    UpdateEntityRequest,
    UpdateEntityTypeRequest,
)


class EntityHttpClient(EntityApiClient, BaseHttpClient):
    """
    Client which sends entity requests to the Exabel Data API with JSON over HTTP.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.DATA_API)

    def list_entity_types(self, request: ListEntityTypesRequest) -> ListEntityTypesResponse:
        return self._request("GET", "entityTypes", ListEntityTypesResponse(), body=request)

    def get_entity_type(self, request: GetEntityTypeRequest) -> EntityType:
        return self._request("GET", request.name, EntityType())

    def create_entity_type(self, request: CreateEntityTypeRequest) -> EntityType:
        return self._request("POST", "entityTypes", EntityType(), body=request.entity_type)

    def update_entity_type(self, request: UpdateEntityTypeRequest) -> EntityType:
        return self._request(
            "PATCH", request.entity_type.name, EntityType(), body=request.entity_type
        )

    def delete_entity_type(self, request: DeleteEntityTypeRequest) -> None:
        return self._request("DELETE", request.name, None)

    def list_entities(self, request: ListEntitiesRequest) -> ListEntitiesResponse:
        return self._request(
            "GET", f"{request.parent}/entities", ListEntitiesResponse(), body=request
        )

    def get_entity(self, request: GetEntityRequest) -> Entity:
        return self._request("GET", request.name, Entity())

    def create_entity(self, request: CreateEntityRequest) -> Entity:
        return self._request("POST", f"{request.parent}/entities", Entity(), body=request.entity)

    def update_entity(self, request: UpdateEntityRequest) -> Entity:
        return self._request("PATCH", request.entity.name, Entity(), body=request.entity)

    def delete_entity(self, request: DeleteEntityRequest) -> None:
        return self._request("DELETE", request.name, None)

    def delete_entities(self, request: DeleteEntitiesRequest) -> None:
        return self._request("DELETE", f"{request.parent}/entities", None, body=request)

    def search_entities(self, request: SearchEntitiesRequest) -> SearchEntitiesResponse:
        return self._request(
            "POST", f"{request.parent}/entities:search", SearchEntitiesResponse(), body=request
        )
