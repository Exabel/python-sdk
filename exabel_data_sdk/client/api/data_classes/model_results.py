from dataclasses import dataclass
from typing import Sequence

from exabel_data_sdk.client.api.data_classes.company_kpi_model_result import CompanyKpiModelResult
from exabel_data_sdk.client.api.data_classes.fiscal_period import FiscalPeriod
from exabel_data_sdk.client.api.data_classes.kpi_hierarchy import KpiHierarchy
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_service_pb2 import (
    ListCompanyBaseModelResultsResponse,
    ListCompanyHierarchicalModelResultsResponse,
)


@dataclass
class BaseModelResults:
    """
    Base model results for a company.

    Attributes:
        results: List of results.
        fiscal_period: Fiscal period the results are for.
    """

    results: Sequence[CompanyKpiModelResult]
    fiscal_period: FiscalPeriod

    @staticmethod
    def from_proto(proto: ListCompanyBaseModelResultsResponse) -> "BaseModelResults":
        """Create a BaseModelResults from the given protobuf message."""
        return BaseModelResults(
            results=[CompanyKpiModelResult.from_proto(r) for r in proto.results],
            fiscal_period=FiscalPeriod.from_proto(proto.period),
        )


@dataclass
class HierarchicalModelResults:
    """
    Hierarchical model results for a company.

    Attributes:
        results: List of results.
        hierarchy: Hierarchy the results are for.
        fiscal_period: Fiscal period the results are for.
    """

    results: Sequence[CompanyKpiModelResult]
    hierarchy: KpiHierarchy
    fiscal_period: FiscalPeriod

    @staticmethod
    def from_proto(
        proto: ListCompanyHierarchicalModelResultsResponse,
    ) -> "HierarchicalModelResults":
        """Create a HierarchicalModelResults from the given protobuf message."""
        return HierarchicalModelResults(
            results=[CompanyKpiModelResult.from_proto(r) for r in proto.results],
            hierarchy=KpiHierarchy.from_proto(proto.kpi_hierarchy),
            fiscal_period=FiscalPeriod.from_proto(proto.period),
        )
