"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from .....exabel.api.data.v1 import relationship_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2
from .....exabel.api.data.v1 import relationship_service_pb2 as exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in exabel/api/data/v1/relationship_service_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class RelationshipServiceStub(object):
    """Service for managing relationship types and relationships. See the User Guide for more
    information about relationship types and relationships:
    https://help.exabel.com/docs/relationships
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListRelationshipTypes = channel.unary_unary('/exabel.api.data.v1.RelationshipService/ListRelationshipTypes', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.ListRelationshipTypesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.ListRelationshipTypesResponse.FromString, _registered_method=True)
        self.GetRelationshipType = channel.unary_unary('/exabel.api.data.v1.RelationshipService/GetRelationshipType', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.GetRelationshipTypeRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.RelationshipType.FromString, _registered_method=True)
        self.CreateRelationshipType = channel.unary_unary('/exabel.api.data.v1.RelationshipService/CreateRelationshipType', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.CreateRelationshipTypeRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.RelationshipType.FromString, _registered_method=True)
        self.UpdateRelationshipType = channel.unary_unary('/exabel.api.data.v1.RelationshipService/UpdateRelationshipType', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.UpdateRelationshipTypeRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.RelationshipType.FromString, _registered_method=True)
        self.DeleteRelationshipType = channel.unary_unary('/exabel.api.data.v1.RelationshipService/DeleteRelationshipType', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.DeleteRelationshipTypeRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, _registered_method=True)
        self.ListRelationships = channel.unary_unary('/exabel.api.data.v1.RelationshipService/ListRelationships', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.ListRelationshipsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.ListRelationshipsResponse.FromString, _registered_method=True)
        self.GetRelationship = channel.unary_unary('/exabel.api.data.v1.RelationshipService/GetRelationship', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.GetRelationshipRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.Relationship.FromString, _registered_method=True)
        self.CreateRelationship = channel.unary_unary('/exabel.api.data.v1.RelationshipService/CreateRelationship', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.CreateRelationshipRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.Relationship.FromString, _registered_method=True)
        self.UpdateRelationship = channel.unary_unary('/exabel.api.data.v1.RelationshipService/UpdateRelationship', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.UpdateRelationshipRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.Relationship.FromString, _registered_method=True)
        self.DeleteRelationship = channel.unary_unary('/exabel.api.data.v1.RelationshipService/DeleteRelationship', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.DeleteRelationshipRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, _registered_method=True)

class RelationshipServiceServicer(object):
    """Service for managing relationship types and relationships. See the User Guide for more
    information about relationship types and relationships:
    https://help.exabel.com/docs/relationships
    """

    def ListRelationshipTypes(self, request, context):
        """List all relationship types from a common catalog.

        Lists all relationship types available to your customer, including those created by you, in
        the global catalog, and from data sets you are subscribed to.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRelationshipType(self, request, context):
        """Gets one relationship type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateRelationshipType(self, request, context):
        """Creates one relationship type and returns it.

        It is also possible to create a relationship type by calling `UpdateRelationshipType`
        with `allow_missing` set to `true`.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateRelationshipType(self, request, context):
        """Updates one relationship type and returns it.

        This can also be used to create a relationship type by setting `allow_missing` to `true`.

        Note that this method update all fields unless `update_mask` is set.

        Note that modifying the `is_ownership` property may be a slow operation, as all individual
        relationships of this type will have to be updated.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteRelationshipType(self, request, context):
        """Deletes one relationship type.

        This can only be performed on relationship types with no relationships. You should delete
        relationships before deleting their entity type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListRelationships(self, request, context):
        """Lists relationship of a specific type.

        If neither `from_entity` or `to_entity` is given, it is expected that this call will
        take some time to complete.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRelationship(self, request, context):
        """Gets one relationship.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateRelationship(self, request, context):
        """Creates one relationship and returns it.

        It is also possible to create a relationship by calling `UpdateRelationship`
        with `allow_missing` set to `true`.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateRelationship(self, request, context):
        """Updates one relationship and returns it.

        This can also be used to create a relationship by setting `allow_missing` to `true`.

        Note that this method will update all fields unless `update_mask` is set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteRelationship(self, request, context):
        """Deletes one relationship.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_RelationshipServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListRelationshipTypes': grpc.unary_unary_rpc_method_handler(servicer.ListRelationshipTypes, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.ListRelationshipTypesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.ListRelationshipTypesResponse.SerializeToString), 'GetRelationshipType': grpc.unary_unary_rpc_method_handler(servicer.GetRelationshipType, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.GetRelationshipTypeRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.RelationshipType.SerializeToString), 'CreateRelationshipType': grpc.unary_unary_rpc_method_handler(servicer.CreateRelationshipType, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.CreateRelationshipTypeRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.RelationshipType.SerializeToString), 'UpdateRelationshipType': grpc.unary_unary_rpc_method_handler(servicer.UpdateRelationshipType, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.UpdateRelationshipTypeRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.RelationshipType.SerializeToString), 'DeleteRelationshipType': grpc.unary_unary_rpc_method_handler(servicer.DeleteRelationshipType, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.DeleteRelationshipTypeRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'ListRelationships': grpc.unary_unary_rpc_method_handler(servicer.ListRelationships, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.ListRelationshipsRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.ListRelationshipsResponse.SerializeToString), 'GetRelationship': grpc.unary_unary_rpc_method_handler(servicer.GetRelationship, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.GetRelationshipRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.Relationship.SerializeToString), 'CreateRelationship': grpc.unary_unary_rpc_method_handler(servicer.CreateRelationship, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.CreateRelationshipRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.Relationship.SerializeToString), 'UpdateRelationship': grpc.unary_unary_rpc_method_handler(servicer.UpdateRelationship, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.UpdateRelationshipRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.Relationship.SerializeToString), 'DeleteRelationship': grpc.unary_unary_rpc_method_handler(servicer.DeleteRelationship, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.DeleteRelationshipRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.data.v1.RelationshipService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('exabel.api.data.v1.RelationshipService', rpc_method_handlers)

class RelationshipService(object):
    """Service for managing relationship types and relationships. See the User Guide for more
    information about relationship types and relationships:
    https://help.exabel.com/docs/relationships
    """

    @staticmethod
    def ListRelationshipTypes(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.RelationshipService/ListRelationshipTypes', exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.ListRelationshipTypesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.ListRelationshipTypesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GetRelationshipType(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.RelationshipService/GetRelationshipType', exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.GetRelationshipTypeRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.RelationshipType.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def CreateRelationshipType(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.RelationshipService/CreateRelationshipType', exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.CreateRelationshipTypeRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.RelationshipType.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def UpdateRelationshipType(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.RelationshipService/UpdateRelationshipType', exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.UpdateRelationshipTypeRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.RelationshipType.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def DeleteRelationshipType(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.RelationshipService/DeleteRelationshipType', exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.DeleteRelationshipTypeRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def ListRelationships(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.RelationshipService/ListRelationships', exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.ListRelationshipsRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.ListRelationshipsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GetRelationship(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.RelationshipService/GetRelationship', exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.GetRelationshipRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.Relationship.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def CreateRelationship(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.RelationshipService/CreateRelationship', exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.CreateRelationshipRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.Relationship.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def UpdateRelationship(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.RelationshipService/UpdateRelationship', exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.UpdateRelationshipRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_relationship__messages__pb2.Relationship.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def DeleteRelationship(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.RelationshipService/DeleteRelationship', exabel_dot_api_dot_data_dot_v1_dot_relationship__service__pb2.DeleteRelationshipRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)