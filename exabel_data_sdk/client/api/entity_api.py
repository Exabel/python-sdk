from typing import Sequence

from exabel_data_sdk.client.api.base_api import BaseApi
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.api.error_handler import handle_grpc_error
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
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2_grpc import EntityServiceStub


class EntityApi(BaseApi):
    """
    API class for CRUD operations on entities and entity types.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config)
        self.stub = EntityServiceStub(self.channel)

    @handle_grpc_error
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
        response = self.stub.ListEntityTypes(
            ListEntityTypesRequest(page_size=page_size, page_token=page_token),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return PagingResult(
            results=[EntityType.from_proto(t) for t in response.entity_types],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    @handle_grpc_error
    def get_entity_type(self, name: str) -> EntityType:
        """
        Get one entity type.

        Args:
            name:   The resource name of the requested entity type, for example
                    "entityTypes/ns.type1".
        """
        response = self.stub.GetEntityType(
            GetEntityTypeRequest(name=name),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return EntityType.from_proto(response)

    @handle_grpc_error
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
        response = self.stub.ListEntities(
            ListEntitiesRequest(parent=entity_type, page_size=page_size, page_token=page_token),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return PagingResult(
            results=[Entity.from_proto(t) for t in response.entities],
            next_page_token=response.next_page_token,
            total_size=response.total_size,
        )

    @handle_grpc_error
    def get_entity(self, name: str) -> Entity:
        """
        Get one entity.

        Args:
            name:   The resource name of the requested entity, for example
                    "entityTypes/ns.type1/entities/ns.entity1".
        """
        response = self.stub.GetEntity(
            GetEntityRequest(name=name),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return Entity.from_proto(response)

    @handle_grpc_error
    def create_entity(self, entity: Entity, entity_type: str) -> Entity:
        """
        Create an entity.

        Args:
            entity:         The entity to create.
            entity_type:    The entity type of the entity, for example "entityTypes/ns.type1".
        """
        response = self.stub.CreateEntity(
            CreateEntityRequest(parent=entity_type, entity=entity.to_proto()),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return Entity.from_proto(response)

    @handle_grpc_error
    def delete_entity(self, name: str) -> None:
        """
        Delete one entity.

        All relationships and time series for this entity will also be deleted.

        Args:
            name:   The resource name of the entity to delete,
                    for example "entityTypes/ns.type1/entities/ns.entity1".
        """
        self.stub.DeleteEntity(
            DeleteEntityRequest(name=name),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )

    @handle_grpc_error
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
        response = self.stub.SearchEntities(
            SearchEntitiesRequest(parent=entity_type, terms=terms),
            metadata=self.metadata,
            timeout=self.config.timeout,
        )
        return [Entity.from_proto(t) for t in response.entities]

    def entity_exists(self, name: str) -> bool:
        """
        Determine whether an entity with the given name already exists.

        Args:
            name:   The resource name of the entity,
                    for example "entityTypes/ns.type1/entities/ns.entity1".
        """
        try:
            self.get_entity(name)
            return True
        except RequestError as error:
            if error.error_type is ErrorType.NOT_FOUND:
                return False
            raise
