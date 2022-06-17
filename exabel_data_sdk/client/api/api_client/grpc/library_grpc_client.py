from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel_data_sdk.client.api.api_client.library_api_client import LibraryApiClient
from exabel_data_sdk.client.api.error_handler import handle_grpc_error
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.management.v1.all_pb2_grpc import LibraryServiceStub
from exabel_data_sdk.stubs.exabel.api.management.v1.folder_messages_pb2 import Folder
from exabel_data_sdk.stubs.exabel.api.management.v1.library_service_pb2 import (
    CreateFolderRequest,
    DeleteFolderRequest,
    GetFolderRequest,
    ListFolderAccessorsRequest,
    ListFolderAccessorsResponse,
    ListFoldersRequest,
    ListFoldersResponse,
    ListItemsRequest,
    ListItemsResponse,
    MoveItemsRequest,
    ShareFolderRequest,
    UnshareFolderRequest,
    UpdateFolderRequest,
)


class LibraryGrpcClient(LibraryApiClient, BaseGrpcClient):
    """
    Client which sends library requests to the Exabel Management API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.MANAGEMENT_API)
        self.stub = LibraryServiceStub(self.channel)

    @handle_grpc_error
    def list_folders(self, request: ListFoldersRequest) -> ListFoldersResponse:
        return self.stub.ListFolders(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def get_folder(self, request: GetFolderRequest) -> Folder:
        return self.stub.GetFolder(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def create_folder(self, request: CreateFolderRequest) -> Folder:
        return self.stub.CreateFolder(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def update_folder(self, request: UpdateFolderRequest) -> Folder:
        return self.stub.UpdateFolder(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def delete_folder(self, request: DeleteFolderRequest) -> None:
        return self.stub.DeleteFolder(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def list_items(self, request: ListItemsRequest) -> ListItemsResponse:
        return self.stub.ListItems(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def list_folder_accessors(
        self, request: ListFolderAccessorsRequest
    ) -> ListFolderAccessorsResponse:
        return self.stub.ListFolderAccessors(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def move_items(self, request: MoveItemsRequest) -> None:
        return self.stub.MoveItems(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def share_folder(self, request: ShareFolderRequest) -> None:
        return self.stub.ShareFolder(request, metadata=self.metadata, timeout=self.config.timeout)

    @handle_grpc_error
    def unshare_folder(self, request: UnshareFolderRequest) -> None:
        return self.stub.UnshareFolder(request, metadata=self.metadata, timeout=self.config.timeout)
