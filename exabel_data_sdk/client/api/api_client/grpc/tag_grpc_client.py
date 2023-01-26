from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel_data_sdk.client.api.api_client.tag_api_client import TagApiClient
from exabel_data_sdk.client.api.error_handler import handle_grpc_error
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    AddEntitiesRequest,
    AddEntitiesResponse,
    CreateTagRequest,
    DeleteTagRequest,
    GetTagRequest,
    ListTagEntitiesRequest,
    ListTagEntitiesResponse,
    ListTagsRequest,
    ListTagsResponse,
    RemoveEntitiesRequest,
    RemoveEntitiesResponse,
    Tag,
    UpdateTagRequest,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2_grpc import TagServiceStub


class TagGrpcClient(TagApiClient, BaseGrpcClient):
    """
    Client which sends tag requests to the Exabel Analytics API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.ANALYTICS_API)
        self.stub = TagServiceStub(self.channel)

    @handle_grpc_error
    def create_tag(self, request: CreateTagRequest) -> Tag:
        return self.stub.CreateTag(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def get_tag(self, request: GetTagRequest) -> Tag:
        return self.stub.GetTag(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def update_tag(self, request: UpdateTagRequest) -> Tag:
        return self.stub.UpdateTag(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def delete_tag(self, request: DeleteTagRequest) -> None:
        return self.stub.DeleteTag(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def list_tags(self, request: ListTagsRequest) -> ListTagsResponse:
        return self.stub.ListTags(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def add_entities(self, request: AddEntitiesRequest) -> AddEntitiesResponse:
        return self.stub.AddEntities(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def remove_entities(self, request: RemoveEntitiesRequest) -> RemoveEntitiesResponse:
        return self.stub.RemoveEntities(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def list_entities(self, request: ListTagEntitiesRequest) -> ListTagEntitiesResponse:
        return self.stub.ListTagEntities(
            request, metadata=self.metadata, timeout=self.config.timeout
        )
