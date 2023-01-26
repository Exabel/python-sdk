"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....exabel.api.analytics.v1 import tag_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_tag__messages__pb2
from .....exabel.api.analytics.v1 import tag_service_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

class TagServiceStub(object):
    """Service for managing tags. See the User Guide for more information about tags.

    Requests to the TagService are executed in the context of the customer's service account (SA).
    The SA is a special user that is a member of the customer user group, giving it access to all
    folders that are shared with this user group, but not to private folders.
    Hence, only tags that are in folders shared to the SA, via the customer user group,
    will be accessible via the TagService.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateTag = channel.unary_unary('/exabel.api.analytics.v1.TagService/CreateTag', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.CreateTagRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__messages__pb2.Tag.FromString)
        self.GetTag = channel.unary_unary('/exabel.api.analytics.v1.TagService/GetTag', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.GetTagRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__messages__pb2.Tag.FromString)
        self.UpdateTag = channel.unary_unary('/exabel.api.analytics.v1.TagService/UpdateTag', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.UpdateTagRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__messages__pb2.Tag.FromString)
        self.DeleteTag = channel.unary_unary('/exabel.api.analytics.v1.TagService/DeleteTag', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.DeleteTagRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.ListTags = channel.unary_unary('/exabel.api.analytics.v1.TagService/ListTags', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.ListTagsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.ListTagsResponse.FromString)
        self.AddEntities = channel.unary_unary('/exabel.api.analytics.v1.TagService/AddEntities', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.AddEntitiesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.AddEntitiesResponse.FromString)
        self.RemoveEntities = channel.unary_unary('/exabel.api.analytics.v1.TagService/RemoveEntities', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.RemoveEntitiesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.RemoveEntitiesResponse.FromString)
        self.ListTagEntities = channel.unary_unary('/exabel.api.analytics.v1.TagService/ListTagEntities', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.ListTagEntitiesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.ListTagEntitiesResponse.FromString)

class TagServiceServicer(object):
    """Service for managing tags. See the User Guide for more information about tags.

    Requests to the TagService are executed in the context of the customer's service account (SA).
    The SA is a special user that is a member of the customer user group, giving it access to all
    folders that are shared with this user group, but not to private folders.
    Hence, only tags that are in folders shared to the SA, via the customer user group,
    will be accessible via the TagService.
    """

    def CreateTag(self, request, context):
        """Create a tag.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTag(self, request, context):
        """Get a tag.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateTag(self, request, context):
        """Update a tag.

        Note that that this method will update all fields unless `update_mask` is set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteTag(self, request, context):
        """Delete a tag.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListTags(self, request, context):
        """List all tags accessible by the user.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddEntities(self, request, context):
        """Add entities to a tag. Entities that exist in the tag already will be ignored

        Entities that exist in the tag already will be ignored.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveEntities(self, request, context):
        """Remove a set of entities from tag.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListTagEntities(self, request, context):
        """List all entities in a tag.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_TagServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'CreateTag': grpc.unary_unary_rpc_method_handler(servicer.CreateTag, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.CreateTagRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__messages__pb2.Tag.SerializeToString), 'GetTag': grpc.unary_unary_rpc_method_handler(servicer.GetTag, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.GetTagRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__messages__pb2.Tag.SerializeToString), 'UpdateTag': grpc.unary_unary_rpc_method_handler(servicer.UpdateTag, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.UpdateTagRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__messages__pb2.Tag.SerializeToString), 'DeleteTag': grpc.unary_unary_rpc_method_handler(servicer.DeleteTag, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.DeleteTagRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'ListTags': grpc.unary_unary_rpc_method_handler(servicer.ListTags, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.ListTagsRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.ListTagsResponse.SerializeToString), 'AddEntities': grpc.unary_unary_rpc_method_handler(servicer.AddEntities, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.AddEntitiesRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.AddEntitiesResponse.SerializeToString), 'RemoveEntities': grpc.unary_unary_rpc_method_handler(servicer.RemoveEntities, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.RemoveEntitiesRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.RemoveEntitiesResponse.SerializeToString), 'ListTagEntities': grpc.unary_unary_rpc_method_handler(servicer.ListTagEntities, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.ListTagEntitiesRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.ListTagEntitiesResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.analytics.v1.TagService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class TagService(object):
    """Service for managing tags. See the User Guide for more information about tags.

    Requests to the TagService are executed in the context of the customer's service account (SA).
    The SA is a special user that is a member of the customer user group, giving it access to all
    folders that are shared with this user group, but not to private folders.
    Hence, only tags that are in folders shared to the SA, via the customer user group,
    will be accessible via the TagService.
    """

    @staticmethod
    def CreateTag(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.TagService/CreateTag', exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.CreateTagRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_tag__messages__pb2.Tag.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTag(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.TagService/GetTag', exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.GetTagRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_tag__messages__pb2.Tag.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateTag(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.TagService/UpdateTag', exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.UpdateTagRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_tag__messages__pb2.Tag.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteTag(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.TagService/DeleteTag', exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.DeleteTagRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListTags(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.TagService/ListTags', exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.ListTagsRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.ListTagsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddEntities(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.TagService/AddEntities', exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.AddEntitiesRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.AddEntitiesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RemoveEntities(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.TagService/RemoveEntities', exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.RemoveEntitiesRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.RemoveEntitiesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListTagEntities(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.TagService/ListTagEntities', exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.ListTagEntitiesRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_tag__service__pb2.ListTagEntitiesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)