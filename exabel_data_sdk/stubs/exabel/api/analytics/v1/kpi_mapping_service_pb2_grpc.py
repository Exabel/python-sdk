"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from .....exabel.api.analytics.v1 import kpi_mapping_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__messages__pb2
from .....exabel.api.analytics.v1 import kpi_mapping_service_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2
GRPC_GENERATED_VERSION = '1.71.2'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in exabel/api/analytics/v1/kpi_mapping_service_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class KpiMappingServiceStub(object):
    """Service for managing KPI mapping groups.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateKpiMappingGroup = channel.unary_unary('/exabel.api.analytics.v1.KpiMappingService/CreateKpiMappingGroup', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.CreateKpiMappingGroupRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__messages__pb2.KpiMappingGroup.FromString, _registered_method=True)
        self.GetKpiMappingGroup = channel.unary_unary('/exabel.api.analytics.v1.KpiMappingService/GetKpiMappingGroup', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.GetKpiMappingGroupRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__messages__pb2.KpiMappingGroup.FromString, _registered_method=True)
        self.ListKpiMappingGroups = channel.unary_unary('/exabel.api.analytics.v1.KpiMappingService/ListKpiMappingGroups', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.ListKpiMappingGroupsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.ListKpiMappingGroupsResponse.FromString, _registered_method=True)
        self.UpdateKpiMappingGroup = channel.unary_unary('/exabel.api.analytics.v1.KpiMappingService/UpdateKpiMappingGroup', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.UpdateKpiMappingGroupRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__messages__pb2.KpiMappingGroup.FromString, _registered_method=True)

class KpiMappingServiceServicer(object):
    """Service for managing KPI mapping groups.
    """

    def CreateKpiMappingGroup(self, request, context):
        """Create a KPI mapping group.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetKpiMappingGroup(self, request, context):
        """Retrieve a KPI mapping group.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListKpiMappingGroups(self, request, context):
        """List KPI mapping groups for a KPI mapping.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateKpiMappingGroup(self, request, context):
        """Update a KPI mapping group.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_KpiMappingServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'CreateKpiMappingGroup': grpc.unary_unary_rpc_method_handler(servicer.CreateKpiMappingGroup, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.CreateKpiMappingGroupRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__messages__pb2.KpiMappingGroup.SerializeToString), 'GetKpiMappingGroup': grpc.unary_unary_rpc_method_handler(servicer.GetKpiMappingGroup, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.GetKpiMappingGroupRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__messages__pb2.KpiMappingGroup.SerializeToString), 'ListKpiMappingGroups': grpc.unary_unary_rpc_method_handler(servicer.ListKpiMappingGroups, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.ListKpiMappingGroupsRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.ListKpiMappingGroupsResponse.SerializeToString), 'UpdateKpiMappingGroup': grpc.unary_unary_rpc_method_handler(servicer.UpdateKpiMappingGroup, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.UpdateKpiMappingGroupRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__messages__pb2.KpiMappingGroup.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.analytics.v1.KpiMappingService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('exabel.api.analytics.v1.KpiMappingService', rpc_method_handlers)

class KpiMappingService(object):
    """Service for managing KPI mapping groups.
    """

    @staticmethod
    def CreateKpiMappingGroup(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.KpiMappingService/CreateKpiMappingGroup', exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.CreateKpiMappingGroupRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__messages__pb2.KpiMappingGroup.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GetKpiMappingGroup(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.KpiMappingService/GetKpiMappingGroup', exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.GetKpiMappingGroupRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__messages__pb2.KpiMappingGroup.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def ListKpiMappingGroups(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.KpiMappingService/ListKpiMappingGroups', exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.ListKpiMappingGroupsRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.ListKpiMappingGroupsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def UpdateKpiMappingGroup(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.KpiMappingService/UpdateKpiMappingGroup', exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__service__pb2.UpdateKpiMappingGroupRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__messages__pb2.KpiMappingGroup.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)