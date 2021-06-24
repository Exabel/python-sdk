from exabel_data_sdk.client.api.api_client.http.base_http_client import BaseHttpClient
from exabel_data_sdk.client.api.api_client.relationship_api_client import RelationshipApiClient
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
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
)


class RelationshipHttpClient(RelationshipApiClient, BaseHttpClient):
    """
    Client which sends relationship requests to the Exabel Data API with JSON over gRPC.
    """

    def list_relationship_types(
        self, request: ListRelationshipTypesRequest
    ) -> ListRelationshipTypesResponse:
        return self._request("GET", "relationshipTypes", ListRelationshipTypesResponse())

    def get_relationship_type(self, request: GetRelationshipTypeRequest) -> RelationshipType:
        return self._request("GET", request.name, RelationshipType())

    def create_relationship_type(self, request: CreateRelationshipTypeRequest) -> RelationshipType:
        return self._request(
            "POST", "relationshipTypes", RelationshipType(), body=request.relationship_type
        )

    def delete_relationship_type(self, request: DeleteRelationshipTypeRequest) -> None:
        return self._request("DELETE", request.name, None)

    def list_relationships(self, request: ListRelationshipsRequest) -> ListRelationshipsResponse:
        return self._request(
            "GET", f"{request.parent}/relationships", ListRelationshipsResponse(), body=request
        )

    def get_relationship(self, request: GetRelationshipRequest) -> Relationship:
        # Since GetRelationship has the same url as ListRelationships, these requests cannot be
        # distinguished by the server, and we get a ListRelationshipsResponse.
        response = self._request(
            "GET", f"{request.parent}/relationships", ListRelationshipsResponse(), body=request
        )
        assert response.total_size <= 1
        if not response.total_size:
            raise RequestError(ErrorType.NOT_FOUND, "The relationship does not exist.")
        return response.relationships[0]

    def create_relationship(self, request: CreateRelationshipRequest) -> Relationship:
        return self._request(
            "POST",
            f"{request.relationship.parent}/relationships",
            Relationship(),
            body=request.relationship,
        )

    def delete_relationship(self, request: DeleteRelationshipRequest) -> None:
        return self._request("DELETE", f"{request.parent}/relationships", None, body=request)
