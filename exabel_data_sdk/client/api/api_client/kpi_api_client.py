from abc import ABC, abstractmethod

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


class KpiApiClient(ABC):
    """
    Superclass for clients that sends KPI requests to the Exabel Analytics API.
    """

    @abstractmethod
    def list_kpi_mapping_results(
        self, request: ListKpiMappingResultsRequest
    ) -> ListKpiMappingResultsResponse:
        """List KPI mapping results for a single KPI mapping collection."""

    @abstractmethod
    def list_company_base_model_results(
        self, request: ListCompanyBaseModelResultsRequest
    ) -> ListCompanyBaseModelResultsResponse:
        """List base model results for a company."""

    @abstractmethod
    def list_company_hierarchical_model_results(
        self, request: ListCompanyHierarchicalModelResultsRequest
    ) -> ListCompanyHierarchicalModelResultsResponse:
        """List hierarchical model results for a company."""

    @abstractmethod
    def list_company_kpi_mapping_results(
        self, request: ListCompanyKpiMappingResultsRequest
    ) -> ListCompanyKpiMappingResultsResponse:
        """List KPI mapping results for a single company KPI."""

    @abstractmethod
    def list_company_kpi_model_results(
        self, request: ListCompanyKpiModelResultsRequest
    ) -> ListCompanyKpiModelResultsResponse:
        """List model results for a single company KPI."""
