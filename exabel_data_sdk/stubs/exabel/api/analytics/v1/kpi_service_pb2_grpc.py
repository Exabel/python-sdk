"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from .....exabel.api.analytics.v1 import kpi_service_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2
GRPC_GENERATED_VERSION = '1.71.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in exabel/api/analytics/v1/kpi_service_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class KpiServiceStub(object):
    """Service to retrieve KPI results.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListKpiMappingResults = channel.unary_unary('/exabel.api.analytics.v1.KpiService/ListKpiMappingResults', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListKpiMappingResultsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListKpiMappingResultsResponse.FromString, _registered_method=True)
        self.ListCompanyBaseModelResults = channel.unary_unary('/exabel.api.analytics.v1.KpiService/ListCompanyBaseModelResults', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyBaseModelResultsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyBaseModelResultsResponse.FromString, _registered_method=True)
        self.ListCompanyHierarchicalModelResults = channel.unary_unary('/exabel.api.analytics.v1.KpiService/ListCompanyHierarchicalModelResults', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyHierarchicalModelResultsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyHierarchicalModelResultsResponse.FromString, _registered_method=True)
        self.ListCompanyKpiMappingResults = channel.unary_unary('/exabel.api.analytics.v1.KpiService/ListCompanyKpiMappingResults', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyKpiMappingResultsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyKpiMappingResultsResponse.FromString, _registered_method=True)
        self.ListCompanyKpiModelResults = channel.unary_unary('/exabel.api.analytics.v1.KpiService/ListCompanyKpiModelResults', request_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyKpiModelResultsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyKpiModelResultsResponse.FromString, _registered_method=True)

class KpiServiceServicer(object):
    """Service to retrieve KPI results.
    """

    def ListKpiMappingResults(self, request, context):
        """List KPI mapping results for a single KPI mapping collection.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListCompanyBaseModelResults(self, request, context):
        """List base model results for a company.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListCompanyHierarchicalModelResults(self, request, context):
        """List hierarchical model results for a company.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListCompanyKpiMappingResults(self, request, context):
        """List KPI mapping results for a single company KPI.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListCompanyKpiModelResults(self, request, context):
        """List model results for a single company KPI.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_KpiServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListKpiMappingResults': grpc.unary_unary_rpc_method_handler(servicer.ListKpiMappingResults, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListKpiMappingResultsRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListKpiMappingResultsResponse.SerializeToString), 'ListCompanyBaseModelResults': grpc.unary_unary_rpc_method_handler(servicer.ListCompanyBaseModelResults, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyBaseModelResultsRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyBaseModelResultsResponse.SerializeToString), 'ListCompanyHierarchicalModelResults': grpc.unary_unary_rpc_method_handler(servicer.ListCompanyHierarchicalModelResults, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyHierarchicalModelResultsRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyHierarchicalModelResultsResponse.SerializeToString), 'ListCompanyKpiMappingResults': grpc.unary_unary_rpc_method_handler(servicer.ListCompanyKpiMappingResults, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyKpiMappingResultsRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyKpiMappingResultsResponse.SerializeToString), 'ListCompanyKpiModelResults': grpc.unary_unary_rpc_method_handler(servicer.ListCompanyKpiModelResults, request_deserializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyKpiModelResultsRequest.FromString, response_serializer=exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyKpiModelResultsResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.analytics.v1.KpiService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('exabel.api.analytics.v1.KpiService', rpc_method_handlers)

class KpiService(object):
    """Service to retrieve KPI results.
    """

    @staticmethod
    def ListKpiMappingResults(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.KpiService/ListKpiMappingResults', exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListKpiMappingResultsRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListKpiMappingResultsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def ListCompanyBaseModelResults(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.KpiService/ListCompanyBaseModelResults', exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyBaseModelResultsRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyBaseModelResultsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def ListCompanyHierarchicalModelResults(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.KpiService/ListCompanyHierarchicalModelResults', exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyHierarchicalModelResultsRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyHierarchicalModelResultsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def ListCompanyKpiMappingResults(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.KpiService/ListCompanyKpiMappingResults', exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyKpiMappingResultsRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyKpiMappingResultsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def ListCompanyKpiModelResults(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.analytics.v1.KpiService/ListCompanyKpiModelResults', exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyKpiModelResultsRequest.SerializeToString, exabel_dot_api_dot_analytics_dot_v1_dot_kpi__service__pb2.ListCompanyKpiModelResultsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)