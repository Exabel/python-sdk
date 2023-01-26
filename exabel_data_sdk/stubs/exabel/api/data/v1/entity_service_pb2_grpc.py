"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....exabel.api.data.v1 import entity_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2
from .....exabel.api.data.v1 import entity_service_pb2 as exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

class EntityServiceStub(object):
    """Service for managing entity types and entities. See the User Guide for more information about
    entity types and entities.
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
    """Service for managing entity types and entities. See the User Guide for more information about
    entity types and entities.
    """

    def ListEntityTypes(self, request, context):
        """Lists all known entity types.

        Lists all entity types available to your customer, including those created by you, in the
        global catalog, and from data sets you are subscribed to.
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
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateEntityType(self, request, context):
        """Updates one entity type and returns it.

        This can also be used to create an entity type by setting `allow_missing` to `true`.

        Note that that this method will update all fields unless `update_mask` is set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteEntityType(self, request, context):
        """Deletes one entity type.

        This can only be performed on entity types with no entities. You should delete entities before
        deleting their entity type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListEntities(self, request, context):
        """Lists all entities of a given entity type.

        List all entities of a given entity type.
        Some entity types are too large to be listed (company, regional, security, listing) - use the
        Search method instead.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteEntities(self, request, context):
        """Deletes entities.

        Deletes ***all*** entities of a given entity type, and their relationships and time series.
        This is useful for cleaning up erroneous data imports and data that is no longer needed.
        Note that the `confirm` field must be set to `true`. Only entities in your namespace(s) are
        deleted, and the entity type itself is *not* deleted.
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

        This can also be used to create an entity by setting `allow_missing` to `true`.

        Note that that this method will update all fields unless `update_mask` is set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteEntity(self, request, context):
        """Deletes one entity.

        This will delete ***all*** relationships and time series for the entity.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchEntities(self, request, context):
        """Search for entities.

        Currently, only companies, securities and listings can be searched.

        If multiple search terms are present, each search is performed individually, with results
        returned in separate `SearchResult` objects.

        Companies may be searched by any of the following fields:
        * `isin` (International Securities Identification Number)
        * `mic` (Market Identifier Code) and `ticker`
        * `bloomberg_ticker` (eg `AAPL US`)
        * `bloomberg_symbol` (eg `AAPL US Equity`)
        * `figi` (Financial Instruments Global Identifier)
        * `factset_identifier`: either FactSet entity identifier or FactSet permanent identifier ("FSYM_ID")
        * `text`

        `mic` and `ticker` must come in pairs, with `mic` immediately before `ticker`. Each pair is
        treated as one search query.

        The `text` field supports free text search for ISINs, tickers and/or company names. If a
        search term is sufficiently long, a prefix search will be performed. Up to five companies are
        returned for each search.

        Securities may be searched by `isin` or `mic`/`ticker`. Listings may be searched by
        `mic`/`ticker`.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_EntityServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListEntityTypes': grpc.unary_unary_rpc_method_handler(servicer.ListEntityTypes, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntityTypesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntityTypesResponse.SerializeToString), 'GetEntityType': grpc.unary_unary_rpc_method_handler(servicer.GetEntityType, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.GetEntityTypeRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.EntityType.SerializeToString), 'CreateEntityType': grpc.unary_unary_rpc_method_handler(servicer.CreateEntityType, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.CreateEntityTypeRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.EntityType.SerializeToString), 'UpdateEntityType': grpc.unary_unary_rpc_method_handler(servicer.UpdateEntityType, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.UpdateEntityTypeRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.EntityType.SerializeToString), 'DeleteEntityType': grpc.unary_unary_rpc_method_handler(servicer.DeleteEntityType, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.DeleteEntityTypeRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'ListEntities': grpc.unary_unary_rpc_method_handler(servicer.ListEntities, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntitiesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.ListEntitiesResponse.SerializeToString), 'DeleteEntities': grpc.unary_unary_rpc_method_handler(servicer.DeleteEntities, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.DeleteEntitiesRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'GetEntity': grpc.unary_unary_rpc_method_handler(servicer.GetEntity, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.GetEntityRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.SerializeToString), 'CreateEntity': grpc.unary_unary_rpc_method_handler(servicer.CreateEntity, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.CreateEntityRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.SerializeToString), 'UpdateEntity': grpc.unary_unary_rpc_method_handler(servicer.UpdateEntity, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.UpdateEntityRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__messages__pb2.Entity.SerializeToString), 'DeleteEntity': grpc.unary_unary_rpc_method_handler(servicer.DeleteEntity, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.DeleteEntityRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'SearchEntities': grpc.unary_unary_rpc_method_handler(servicer.SearchEntities, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.SearchEntitiesRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_entity__service__pb2.SearchEntitiesResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.data.v1.EntityService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class EntityService(object):
    """Service for managing entity types and entities. See the User Guide for more information about
    entity types and entities.
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