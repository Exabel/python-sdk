from abc import ABC, abstractmethod

from exabel_data_sdk.stubs.exabel.api.management.v1.all_pb2 import (
    CreateFolderRequest,
    DeleteFolderRequest,
    Folder,
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


class LibraryApiClient(ABC):
    """
    Superclass for clients that send library requests to the Exabel Management API.
    """

    @abstractmethod
    def list_folders(self, request: ListFoldersRequest) -> ListFoldersResponse:
        """List all folders. Folders are returned without items."""

    @abstractmethod
    def get_folder(self, request: GetFolderRequest) -> Folder:
        """Get a folder including its items."""

    @abstractmethod
    def create_folder(self, request: CreateFolderRequest) -> Folder:
        """Create a new folder."""

    @abstractmethod
    def update_folder(self, request: UpdateFolderRequest) -> Folder:
        """Update a folder."""

    @abstractmethod
    def delete_folder(self, request: DeleteFolderRequest) -> None:
        """Delete a folder."""

    @abstractmethod
    def list_items(self, request: ListItemsRequest) -> ListItemsResponse:
        """List all items of a specific type."""

    @abstractmethod
    def list_folder_accessors(
        self, request: ListFolderAccessorsRequest
    ) -> ListFolderAccessorsResponse:
        """List the accessors of a specific folder."""

    @abstractmethod
    def move_items(self, request: MoveItemsRequest) -> None:
        """Move multiple items into a folder."""

    @abstractmethod
    def share_folder(self, request: ShareFolderRequest) -> None:
        """Share a folder with a group."""

    @abstractmethod
    def unshare_folder(self, request: UnshareFolderRequest) -> None:
        """Remove sharing of a folder with a group."""
