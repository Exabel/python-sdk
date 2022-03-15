"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....exabel.api.data.v1 import entity_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2
from .....exabel.api.data.v1 import entity_service_pb2 as exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

class EntityServiceStub(object):
    """Manages entity types and entities in the Data API.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListEntityTypes = channel.unary_unary('/exabel.api.data.v1.EntityService/ListEntityTypes', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntityTypesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntityTypesResponse.FromString)
        self.GetEntityType = channel.unary_unary('/exabel.api.data.v1.EntityService/GetEntityType', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.GetEntityTypeRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.EntityType.FromString)
        self.ListEntities = channel.unary_unary('/exabel.api.data.v1.EntityService/ListEntities', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntitiesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntitiesResponse.FromString)
        self.GetEntity = channel.unary_unary('/exabel.api.data.v1.EntityService/GetEntity', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.GetEntityRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.FromString)
        self.CreateEntity = channel.unary_unary('/exabel.api.data.v1.EntityService/CreateEntity', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.CreateEntityRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.FromString)
        self.UpdateEntity = channel.unary_unary('/exabel.api.data.v1.EntityService/UpdateEntity', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.UpdateEntityRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.FromString)
        self.DeleteEntity = channel.unary_unary('/exabel.api.data.v1.EntityService/DeleteEntity', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.DeleteEntityRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.SearchEntities = channel.unary_unary('/exabel.api.data.v1.EntityService/SearchEntities', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.SearchEntitiesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.SearchEntitiesResponse.FromString)

class EntityServiceServicer(object):
    """Manages entity types and entities in the Data API.
    """

    def ListEntityTypes(self, request, context):
        """Lists all known entity types.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEntityType(self, request, context):
        """Gets one entity type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListEntities(self, request, context):
        """Lists all entities of a given entity type. Some entity types are too large
        and cannot be listed. SearchEntities can be used for those instead.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEntity(self, request, context):
        """Gets one entity.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateEntity(self, request, context):
        """Creates one entity and returns it.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateEntity(self, request, context):
        """Updates one entity and returns it.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteEntity(self, request, context):
        """Deletes one entity. ALL relationships and time series for this entity will
        also be deleted.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchEntities(self, request, context):
        """Search for entities.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_EntityServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListEntityTypes': grpc.unary_unary_rpc_method_handler(servicer.ListEntityTypes, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntityTypesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntityTypesResponse.SerializeToString), 'GetEntityType': grpc.unary_unary_rpc_method_handler(servicer.GetEntityType, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.GetEntityTypeRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.EntityType.SerializeToString), 'ListEntities': grpc.unary_unary_rpc_method_handler(servicer.ListEntities, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntitiesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntitiesResponse.SerializeToString), 'GetEntity': grpc.unary_unary_rpc_method_handler(servicer.GetEntity, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.GetEntityRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.SerializeToString), 'CreateEntity': grpc.unary_unary_rpc_method_handler(servicer.CreateEntity, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.CreateEntityRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.SerializeToString), 'UpdateEntity': grpc.unary_unary_rpc_method_handler(servicer.UpdateEntity, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.UpdateEntityRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.SerializeToString), 'DeleteEntity': grpc.unary_unary_rpc_method_handler(servicer.DeleteEntity, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.DeleteEntityRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'SearchEntities': grpc.unary_unary_rpc_method_handler(servicer.SearchEntities, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.SearchEntitiesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.SearchEntitiesResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.data.v1.EntityService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class EntityService(object):
    """Manages entity types and entities in the Data API.
    """

    @staticmethod
    def ListEntityTypes(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.EntityService/ListEntityTypes', exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntityTypesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntityTypesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetEntityType(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.EntityService/GetEntityType', exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.GetEntityTypeRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.EntityType.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListEntities(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.EntityService/ListEntities', exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntitiesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntitiesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetEntity(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.EntityService/GetEntity', exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.GetEntityRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateEntity(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.EntityService/CreateEntity', exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.CreateEntityRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateEntity(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.EntityService/UpdateEntity', exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.UpdateEntityRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteEntity(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.EntityService/DeleteEntity', exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.DeleteEntityRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SearchEntities(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.EntityService/SearchEntities', exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.SearchEntitiesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.SearchEntitiesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)