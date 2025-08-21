from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel_data_sdk.client.api.api_client.kpi_api_client import KpiApiClient
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_service_pb2 import (
    ListCompanyBaseModelResultsRequest,
    ListCompanyBaseModelResultsResponse,
    ListCompanyHierarchicalModelResultsRequest,
    ListCompanyHierarchicalModelResultsResponse,
    ListCompanyKpiMappingResultsRequest,
    ListCompanyKpiMappingResultsResponse,
    ListCompanyKpiModelResultsRequest,
    ListCompanyKpiModelResultsResponse,
    ListKpiMappingResultsRequest,
    ListKpiMappingResultsResponse,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_service_pb2_grpc import KpiServiceStub


class KpiGrpcClient(KpiApiClient, BaseGrpcClient):
    """
    Client which sends KPI requests to the Exabel Data API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.ANALYTICS_API)
        self.stub = KpiServiceStub(self.channel)

    def list_kpi_mapping_results(
        self, request: ListKpiMappingResultsRequest
    ) -> ListKpiMappingResultsResponse:
        return self.stub.ListKpiMappingResults(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    def list_company_base_model_results(
        self, request: ListCompanyBaseModelResultsRequest
    ) -> ListCompanyBaseModelResultsResponse:
        return self.stub.ListCompanyBaseModelResults(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    def list_company_hierarchical_model_results(
        self, request: ListCompanyHierarchicalModelResultsRequest
    ) -> ListCompanyHierarchicalModelResultsResponse:
        return self.stub.ListCompanyHierarchicalModelResults(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    def list_company_kpi_mapping_results(
        self, request: ListCompanyKpiMappingResultsRequest
    ) -> ListCompanyKpiMappingResultsResponse:
        return self.stub.ListCompanyKpiMappingResults(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    def list_company_kpi_model_results(
        self, request: ListCompanyKpiModelResultsRequest
    ) -> ListCompanyKpiModelResultsResponse:
        return self.stub.ListCompanyKpiModelResults(
            request, metadata=self.metadata, timeout=self.config.timeout
        )
