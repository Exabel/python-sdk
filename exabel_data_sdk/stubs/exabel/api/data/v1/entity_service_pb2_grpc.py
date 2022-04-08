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
        self.CreateEntityType = channel.unary_unary('/exabel.api.data.v1.EntityService/CreateEntityType', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.CreateEntityTypeRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.EntityType.FromString)
        self.UpdateEntityType = channel.unary_unary('/exabel.api.data.v1.EntityService/UpdateEntityType', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.UpdateEntityTypeRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.EntityType.FromString)
        self.DeleteEntityType = channel.unary_unary('/exabel.api.data.v1.EntityService/DeleteEntityType', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.DeleteEntityTypeRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
        self.ListEntities = channel.unary_unary('/exabel.api.data.v1.EntityService/ListEntities', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntitiesRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntitiesResponse.FromString)
        self.DeleteEntities = channel.unary_unary('/exabel.api.data.v1.EntityService/DeleteEntities', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.DeleteEntitiesRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)
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

        Retrieves the entity type catalogue.
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

    def CreateEntityType(self, request, context):
        """Creates one entity type and returns it.

        An entity can explicitly be created using this method, or it can implicitly be created by the
        update method if its `allow_missing` parameter is set to true.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateEntityType(self, request, context):
        """Updates one entity type and returns it.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteEntityType(self, request, context):
        """Deletes one entity type.

        This can only be performed on types without any entities.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListEntities(self, request, context):
        """Lists all entities of a given entity type.

        Some entity types are too large and cannot be listed. SearchEntities can be used for those instead.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteEntities(self, request, context):
        """Deletes entities.

        Deletes all entities of a given entity type (and their relationships). Note
        that the 'confirm' field must be set for the operation to succeed. Only
        entities in the current writable namespace(s) are deleted, and the entity
        type itself is not deleted.
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

        This method can also be used to create an entity, provided `allow_missing` is set to `true`.
        When this method is used to create an entity, the `update_mask` parameter is ignored.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteEntity(self, request, context):
        """Deletes one entity.

        **All** relationships and time series for this entity will also be deleted.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchEntities(self, request, context):
        """Search for entities.

        Currently only companies, securities and listings can be searched.

        When multiple terms are present, each search is performed individually, with the results of each
        query put into one `SearchResult`.

        An exception to the above are the `MIC` and `ticker` fields, which must come in pairs, with
        `MIC` immediately before `ticker`. One such pair is treated as one search query.

        A search for companies should contain either
        * an `ISIN` (International Securities Identification Number) field, or
        * a `MIC` (Market Identifier Code) **and** a `ticker` field, or
        * a `bloomberg_ticker` or a `bloomberg_symbol` field, or
        * a `FIGI` (Financial Instruments Global Identifier), or
        * a `factset_identifier`, either a FactSet entity identifier or a FactSet permanent identifier (also known as "FSYM_ID"), or
        * a `text` field.

        A `text` field is a free text search field, which searches for ISINs, tickers and/or company
        names. If a search term is sufficiently long, it will also perform a prefix search. A maximum
        of five companies are returned for each search.

        A search for securities should contain either
        * an `ISIN` (International Securities Identification Number) field, or
        * a `MIC` (Market Identifier Code) and a `ticker` field.

        A search for listings should contain
        * a `MIC` (Market Identifier Code) and a `ticker` field.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_EntityServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListEntityTypes': grpc.unary_unary_rpc_method_handler(servicer.ListEntityTypes, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntityTypesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntityTypesResponse.SerializeToString), 'GetEntityType': grpc.unary_unary_rpc_method_handler(servicer.GetEntityType, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.GetEntityTypeRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.EntityType.SerializeToString), 'CreateEntityType': grpc.unary_unary_rpc_method_handler(servicer.CreateEntityType, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.CreateEntityTypeRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.EntityType.SerializeToString), 'UpdateEntityType': grpc.unary_unary_rpc_method_handler(servicer.UpdateEntityType, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.UpdateEntityTypeRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.EntityType.SerializeToString), 'DeleteEntityType': grpc.unary_unary_rpc_method_handler(servicer.DeleteEntityType, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.DeleteEntityTypeRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'ListEntities': grpc.unary_unary_rpc_method_handler(servicer.ListEntities, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntitiesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntitiesResponse.SerializeToString), 'DeleteEntities': grpc.unary_unary_rpc_method_handler(servicer.DeleteEntities, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.DeleteEntitiesRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'GetEntity': grpc.unary_unary_rpc_method_handler(servicer.GetEntity, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.GetEntityRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.SerializeToString), 'CreateEntity': grpc.unary_unary_rpc_method_handler(servicer.CreateEntity, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.CreateEntityRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.SerializeToString), 'UpdateEntity': grpc.unary_unary_rpc_method_handler(servicer.UpdateEntity, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.UpdateEntityRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.SerializeToString), 'DeleteEntity': grpc.unary_unary_rpc_method_handler(servicer.DeleteEntity, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.DeleteEntityRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'SearchEntities': grpc.unary_unary_rpc_method_handler(servicer.SearchEntities, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.SearchEntitiesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.SearchEntitiesResponse.SerializeToString)}
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
    def CreateEntityType(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.EntityService/CreateEntityType', exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.CreateEntityTypeRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.EntityType.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateEntityType(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.EntityService/UpdateEntityType', exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.UpdateEntityTypeRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.EntityType.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteEntityType(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.EntityService/DeleteEntityType', exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.DeleteEntityTypeRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListEntities(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.EntityService/ListEntities', exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntitiesRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntitiesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteEntities(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.EntityService/DeleteEntities', exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.DeleteEntitiesRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

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