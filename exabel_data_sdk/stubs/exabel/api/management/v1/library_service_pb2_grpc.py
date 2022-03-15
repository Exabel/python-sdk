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
        self.ListItems = channel.unary_unary('/exabel.api.management.v1.LibraryService/ListItems', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListItemsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListItemsResponse.FromString)
        self.ListSharedGroups = channel.unary_unary('/exabel.api.management.v1.LibraryService/ListSharedGroups', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListSharedGroupsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListSharedGroupsResponse.FromString)
        self.ShareFolder = channel.unary_unary('/exabel.api.management.v1.LibraryService/ShareFolder', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ShareFolderRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.UnshareFolder = channel.unary_unary('/exabel.api.management.v1.LibraryService/UnshareFolder', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.UnshareFolderRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.TransferOwnership = channel.unary_unary('/exabel.api.management.v1.LibraryService/TransferOwnership', request_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.TransferOwnershipRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.TransferOwnershipResponse.FromString)

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

    def ListItems(self, request, context):
        """List all items of a specific type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListSharedGroups(self, request, context):
        """List the groups that a specific folder is shared with.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ShareFolder(self, request, context):
        """Share a folder with a group.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnshareFolder(self, request, context):
        """Remove sharing of a folder with a group.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TransferOwnership(self, request, context):
        """Transfer ownership of items from one user to another.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_LibraryServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListFolders': grpc.unary_unary_rpc_method_handler(servicer.ListFolders, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListFoldersRequest.FromString, response_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListFoldersResponse.SerializeToString), 'GetFolder': grpc.unary_unary_rpc_method_handler(servicer.GetFolder, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.GetFolderRequest.FromString, response_serializer=exabel_dot_api_dot_management_dot_v1_dot_folder__messages__pb2.Folder.SerializeToString), 'ListItems': grpc.unary_unary_rpc_method_handler(servicer.ListItems, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListItemsRequest.FromString, response_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListItemsResponse.SerializeToString), 'ListSharedGroups': grpc.unary_unary_rpc_method_handler(servicer.ListSharedGroups, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListSharedGroupsRequest.FromString, response_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListSharedGroupsResponse.SerializeToString), 'ShareFolder': grpc.unary_unary_rpc_method_handler(servicer.ShareFolder, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ShareFolderRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'UnshareFolder': grpc.unary_unary_rpc_method_handler(servicer.UnshareFolder, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.UnshareFolderRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'TransferOwnership': grpc.unary_unary_rpc_method_handler(servicer.TransferOwnership, request_deserializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.TransferOwnershipRequest.FromString, response_serializer=exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.TransferOwnershipResponse.SerializeToString)}
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
    def ListItems(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/ListItems', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListItemsRequest.SerializeToString, exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListItemsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListSharedGroups(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/ListSharedGroups', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListSharedGroupsRequest.SerializeToString, exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ListSharedGroupsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ShareFolder(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/ShareFolder', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.ShareFolderRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UnshareFolder(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/UnshareFolder', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.UnshareFolderRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TransferOwnership(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.management.v1.LibraryService/TransferOwnership', exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.TransferOwnershipRequest.SerializeToString, exabel_dot_api_dot_management_dot_v1_dot_library__service__pb2.TransferOwnershipResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)