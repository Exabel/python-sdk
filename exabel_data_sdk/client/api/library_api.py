from typing import Sequence

from exabel_data_sdk.client.api.api_client.grpc.library_grpc_client import LibraryGrpcClient
from exabel_data_sdk.client.api.api_client.http.library_http_client import LibraryHttpClient
from exabel_data_sdk.client.api.data_classes.folder import Folder
from exabel_data_sdk.client.api.data_classes.folder_accessor import FolderAccessor
from exabel_data_sdk.client.api.data_classes.folder_item import FolderItem, FolderItemType
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.management.v1.library_service_pb2 import (
    GetFolderRequest,
    ListFolderAccessorsRequest,
    ListFoldersRequest,
    ListItemsRequest,
    ShareFolderRequest,
    UnshareFolderRequest,
)


class LibraryApi:
    """
    API class for library operations.
    """

    def __init__(self, config: ClientConfig, use_json: bool = False):
        self.client = LibraryHttpClient(config) if use_json else LibraryGrpcClient(config)

    def list_folders(self) -> Sequence[Folder]:
        """
        List all folders. Folders are returned without items.
        """
        response = self.client.list_folders(ListFoldersRequest())
        return [Folder.from_proto(folder) for folder in response.folders]

    def get_folder(self, name: str) -> Folder:
        """
        Get a folder including its items.

        Args:
            name: Resource name of the folder, for example "folders/123".
        """
        proto_folder = self.client.get_folder(GetFolderRequest(name=name))
        return Folder.from_proto(proto_folder)

    def list_items(
        self,
        item_type: FolderItemType,
        folder_name: str = None,
    ) -> Sequence[FolderItem]:
        """
        List all items of a specific type.

        Args:
            item_type:   Item type.
            folder_name: Optional resource name of a folder to list items from,
                         for example "folders/123".
        """
        response = self.client.list_items(
            ListItemsRequest(item_type=item_type.value, parent=folder_name)
        )
        return [FolderItem.from_proto(item) for item in response.items]

    def list_folder_accessors(self, folder_name: str) -> Sequence[FolderAccessor]:
        """
        List groups with access to the given folder.

        Args:
            folder_name: Resource name of the folder, for example "folders/123".
        """
        response = self.client.list_folder_accessors(ListFolderAccessorsRequest(name=folder_name))
        return [FolderAccessor.from_proto(accessor) for accessor in response.folder_accessors]

    def share_folder(self, folder_name: str, group_name: str, write: bool = False) -> None:
        """
        Share a folder with a group.

        Sharing a folder implies giving read access, while write access can be controlled with the
        `write` flag. Use this method also to change whether an already shared folder should be
        shared with write access or not.

        Args:
            folder_name:    Resource name of the folder, for example "folders/123".
            group_name:     Resource name of the group, for example "groups/123".
            write:          Share with write access.
        """
        self.client.share_folder(
            ShareFolderRequest(folder=folder_name, group=group_name, write=write)
        )

    def unshare_folder(self, folder_name: str, group_name: str) -> None:
        """
        Remove sharing of a folder with a group.

        Args:
            folder_name:    Resource name of the folder, for example "folders/123".
            group_name:     Resource name of the group, for example "groups/123".
        """
        self.client.unshare_folder(UnshareFolderRequest(folder=folder_name, group=group_name))
