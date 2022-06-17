"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....exabel.api.management.v1 import folder_messages_pb2 as exabel_dot_api_dot_management_dot_v1_dot_folder__messages__pb2
from .....exabel.api.management.v1 import library_service_pb2 as exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

class LibraryServiceStub(object):
    """Service to manage library items.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListFolders = channel.unary_unary('/exabel.api.management.v1.LibraryService/ListFolders', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListFoldersRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListFoldersResponse.FromString)
        self.GetFolder = channel.unary_unary('/exabel.api.management.v1.LibraryService/GetFolder', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.GetFolderRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_management_dot_v1_dot_folder__messages__pb2.Folder.FromString)
        self.CreateFolder = channel.unary_unary('/exabel.api.management.v1.LibraryService/CreateFolder', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.CreateFolderRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_management_dot_v1_dot_folder__messages__pb2.Folder.FromString)
        self.UpdateFolder = channel.unary_unary('/exabel.api.management.v1.LibraryService/UpdateFolder', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.UpdateFolderRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_management_dot_v1_dot_folder__messages__pb2.Folder.FromString)
        self.DeleteFolder = channel.unary_unary('/exabel.api.management.v1.LibraryService/DeleteFolder', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.DeleteFolderRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.ListItems = channel.unary_unary('/exabel.api.management.v1.LibraryService/ListItems', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListItemsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListItemsResponse.FromString)
        self.MoveItems = channel.unary_unary('/exabel.api.management.v1.LibraryService/MoveItems', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.MoveItemsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.MoveItemsResponse.FromString)
        self.ListFolderAccessors = channel.unary_unary('/exabel.api.management.v1.LibraryService/ListFolderAccessors', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListFolderAccessorsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListFolderAccessorsResponse.FromString)
        self.ShareFolder = channel.unary_unary('/exabel.api.management.v1.LibraryService/ShareFolder', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ShareFolderRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.UnshareFolder = channel.unary_unary('/exabel.api.management.v1.LibraryService/UnshareFolder', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.UnshareFolderRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)

class LibraryServiceServicer(object):
    """Service to manage library items.
    """

    def ListFolders(self, request, context):
        """List all folders. Folders are returned without folder items.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFolder(self, request, context):
        """Get a folder including its items.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateFolder(self, request, context):
        """Create a folder.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateFolder(self, request, context):
        """Update a folder.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteFolder(self, request, context):
        """Delete a folder.

        The folder must be empty.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListItems(self, request, context):
        """List all items of a specific type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MoveItems(self, request, context):
        """Move items to a folder.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListFolderAccessors(self, request, context):
        """List the accessors of a specific folder.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ShareFolder(self, request, context):
        """Share a folder with a group.

        - To grant write access to a group with only read access, call this method with the write flag set to true.
        - To revoke only write access from a group, call this method with the write flag set to false.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnshareFolder(self, request, context):
        """Remove sharing of a folder with a group.

        This revokes both read and write access. To revoke only write access, use ShareFolder
        with the write flag set to false.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_LibraryServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListFolders': grpc.unary_unary_rpc_method_handler(servicer.ListFolders, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListFoldersRequest.FromString, response_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListFoldersResponse.SerializeToString), 'GetFolder': grpc.unary_unary_rpc_method_handler(servicer.GetFolder, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.GetFolderRequest.FromString, response_serializer=exabel_dot_api_dot_management_dot_v1_dot_folder__messages__pb2.Folder.SerializeToString), 'CreateFolder': grpc.unary_unary_rpc_method_handler(servicer.CreateFolder, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.CreateFolderRequest.FromString, response_serializer=exabel_dot_api_dot_management_dot_v1_dot_folder__messages__pb2.Folder.SerializeToString), 'UpdateFolder': grpc.unary_unary_rpc_method_handler(servicer.UpdateFolder, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.UpdateFolderRequest.FromString, response_serializer=exabel_dot_api_dot_management_dot_v1_dot_folder__messages__pb2.Folder.SerializeToString), 'DeleteFolder': grpc.unary_unary_rpc_method_handler(servicer.DeleteFolder, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.DeleteFolderRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'ListItems': grpc.unary_unary_rpc_method_handler(servicer.ListItems, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListItemsRequest.FromString, response_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListItemsResponse.SerializeToString), 'MoveItems': grpc.unary_unary_rpc_method_handler(servicer.MoveItems, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.MoveItemsRequest.FromString, response_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.MoveItemsResponse.SerializeToString), 'ListFolderAccessors': grpc.unary_unary_rpc_method_handler(servicer.ListFolderAccessors, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListFolderAccessorsRequest.FromString, response_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListFolderAccessorsResponse.SerializeToString), 'ShareFolder': grpc.unary_unary_rpc_method_handler(servicer.ShareFolder, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ShareFolderRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'UnshareFolder': grpc.unary_unary_rpc_method_handler(servicer.UnshareFolder, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.UnshareFolderRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.management.v1.LibraryService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class LibraryService(object):
    """Service to manage library items.
    """

    @staticmethod
    def ListFolders(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/ListFolders', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListFoldersRequest.SerializeToString, exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListFoldersResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFolder(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/GetFolder', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.GetFolderRequest.SerializeToString, exabel_dot_api_dot_management_dot_v1_dot_folder__messages__pb2.Folder.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateFolder(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/CreateFolder', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.CreateFolderRequest.SerializeToString, exabel_dot_api_dot_management_dot_v1_dot_folder__messages__pb2.Folder.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateFolder(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/UpdateFolder', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.UpdateFolderRequest.SerializeToString, exabel_dot_api_dot_management_dot_v1_dot_folder__messages__pb2.Folder.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteFolder(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/DeleteFolder', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.DeleteFolderRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListItems(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/ListItems', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListItemsRequest.SerializeToString, exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListItemsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MoveItems(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/MoveItems', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.MoveItemsRequest.SerializeToString, exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.MoveItemsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListFolderAccessors(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/ListFolderAccessors', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListFolderAccessorsRequest.SerializeToString, exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListFolderAccessorsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ShareFolder(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/ShareFolder', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ShareFolderRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UnshareFolder(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/UnshareFolder', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.UnshareFolderRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)