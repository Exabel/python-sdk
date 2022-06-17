from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.http.base_http_client import BaseHttpClient
from exabel_data_sdk.client.api.api_client.library_api_client import LibraryApiClient
from exabel_data_sdk.client.client_config import ClientConfig
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


class LibraryHttpClient(LibraryApiClient, BaseHttpClient):
    """
    Client which sends library requests to the Exabel Management API with JSON over HTTP.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.MANAGEMENT_API)

    def list_folders(self, request: ListFoldersRequest) -> ListFoldersResponse:
        return self._request("GET", "folders", ListFoldersResponse())

    def get_folder(self, request: GetFolderRequest) -> Folder:
        return self._request("GET", request.name, Folder())

    def create_folder(self, request: CreateFolderRequest) -> Folder:
        return self._request("POST", "folders", Folder(), body=request.folder)

    def update_folder(self, request: UpdateFolderRequest) -> Folder:
        return self._request("PATCH", request.folder.name, Folder(), body=request.folder)

    def delete_folder(self, request: DeleteFolderRequest) -> None:
        return self._request("DELETE", request.name, None)

    def list_items(self, request: ListItemsRequest) -> ListItemsResponse:
        return self._request("GET", f"{request.parent}/items", ListItemsResponse())

    def list_folder_accessors(
        self, request: ListFolderAccessorsRequest
    ) -> ListFolderAccessorsResponse:
        return self._request("GET", f"{request.name}/accessors", ListFolderAccessorsResponse())

    def move_items(self, request: MoveItemsRequest) -> None:
        return self._request("POST", f"{request.target_folder}:moveItems", None)

    def share_folder(self, request: ShareFolderRequest) -> None:
        return self._request("POST", f"{request.folder}:share", None, body=request)

    def unshare_folder(self, request: UnshareFolderRequest) -> None:
        return self._request("POST", f"{request.folder}:unshare", None, body=request)
