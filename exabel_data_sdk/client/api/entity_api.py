from typing import Optional, Sequence

from exabel_data_sdk.client.api.api_client.grpc.entity_grpc_client import EntityGrpcClient
from exabel_data_sdk.client.api.api_client.http.entity_http_client import EntityHttpClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.api.search_service import SearchService
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    CreateEntityRequest,
    DeleteEntityRequest,
    GetEntityRequest,
    GetEntityTypeRequest,
    ListEntitiesRequest,
    ListEntityTypesRequest,
    SearchEntitiesRequest,
    SearchTerm,
)


class EntityApi:
    """
    API class for CRUD operations on entities and entity types.

    Attributes:
        search: a SearchService which contains a number of utility methods for searching
    """

    def __init__(self, config: ClientConfig, use_json: bool):
        self.client = (EntityHttpClient if use_json else EntityGrpcClient)(config)
        self.search = SearchService(self.client)

    def list_entity_types(
        self, page_size: int = 1000, page_token: str = None
    ) -> PagingResult[EntityType]:
        """
        List all known entity types.

        Args:
            page_size:  The maximum number of results to return. Defaults to 1000, which is also
                        the maximum size of this field.
            page_token: The page token to resume the results from, as returned from a previous
                        request to this method with the same query parameters.
        """
        response = self.client.list_entity_types(
            ListEntityTypesRequest(page_size=page_size, page_token=page_token)
        )
        return PagingResult(
            results=[EntityType.from_proto(t) for t in response.entity_types],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    def get_entity_type(self, name: str) -> Optional[EntityType]:
        """
        Get one entity type.

        Return None if the entity type does not exist.

        Args:
            name:   The resource name of the requested entity type, for example
                    "entityTypes/ns.type1".
        """
        try:
            response = self.client.get_entity_type(GetEntityTypeRequest(name=name))
        except RequestError as error:
            if error.error_type == ErrorType.NOT_FOUND:
                return None
            raise
        return EntityType.from_proto(response)

    def list_entities(
        self, entity_type: str, page_size: int = 1000, page_token: str = None
    ) -> PagingResult[Entity]:
        """
        List all entities of a given entity type.

        Args:
            entity_type:    The entity type of the entities to list, for example
                            "entityTypes/ns.type1".
            page_size:      The maximum number of results to return.
                            Defaults to 1000, which is also the maximum size of this field.
            page_token:     The page token to resume the results from.
        """
        response = self.client.list_entities(
            ListEntitiesRequest(parent=entity_type, page_size=page_size, page_token=page_token)
        )
        return PagingResult(
            results=[Entity.from_proto(t) for t in response.entities],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    def get_entity(self, name: str) -> Optional[Entity]:
        """
        Get one entity.

        Return None if the entity does not exist.

        Args:
            name:   The resource name of the requested entity, for example
                    "entityTypes/ns.type1/entities/ns.entity1".
        """
        try:
            response = self.client.get_entity(GetEntityRequest(name=name))
        except RequestError as error:
            if error.error_type == ErrorType.NOT_FOUND:
                return None
            raise
        return Entity.from_proto(response)

    def create_entity(self, entity: Entity, entity_type: str) -> Entity:
        """
        Create an entity.

        Args:
            entity:         The entity to create.
            entity_type:    The entity type of the entity, for example "entityTypes/ns.type1".
        """
        response = self.client.create_entity(
            CreateEntityRequest(parent=entity_type, entity=entity.to_proto())
        )
        return Entity.from_proto(response)

    def delete_entity(self, name: str) -> None:
        """
        Delete one entity.

        All relationships and time series for this entity will also be deleted.

        Args:
            name:   The resource name of the entity to delete,
                    for example "entityTypes/ns.type1/entities/ns.entity1".
        """
        self.client.delete_entity(DeleteEntityRequest(name=name))

    def search_for_entities(self, entity_type: str, **search_terms: str) -> Sequence[Entity]:
        """
        Search for entities.

        Args:
            entity_type: The resource name of the entity type which is search for, for example
                    "entityTypes/ns.type1"
        """
        terms = []
        for field, query in search_terms.items():
            terms.append(SearchTerm(field=field, query=query))
        response = self.client.search_entities(
            SearchEntitiesRequest(parent=entity_type, terms=terms)
        )
        return [Entity.from_proto(t) for t in response.entities]

    def entity_exists(self, name: str) -> bool:
        """
        Determine whether an entity with the given name already exists.

        Args:
            name:   The resource name of the entity,
                    for example "entityTypes/ns.type1/entities/ns.entity1".
        """
        return self.get_entity(name) is not None
