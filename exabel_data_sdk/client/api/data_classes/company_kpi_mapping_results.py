from dataclasses import dataclass
from typing import List, Sequence

from exabel_data_sdk.client.api.data_classes.company import Company
from exabel_data_sdk.client.api.data_classes.kpi import Kpi
from exabel_data_sdk.client.api.data_classes.kpi_mapping_result_data import KpiMappingResultData
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    CompanyKpiMappingResults as ProtoCompanyKpiMappingResults,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    SingleCompanyKpiMappingResults as ProtoSingleCompanyKpiMappingResults,
)


@dataclass
class SingleCompanyKpiMappingResults:
    """
    KPI mapping results for a single company KPI.

    Attributes:
        kpi:    The KPI.
        data:   The results.
    """

    kpi: Kpi
    data: List[KpiMappingResultData]

    @staticmethod
    def from_proto(proto: ProtoSingleCompanyKpiMappingResults) -> "SingleCompanyKpiMappingResults":
        """
        Create a SingleCompanyKpiMappingResults from the given protobuf
        SingleCompanyKpiMappingResults.
        """
        return SingleCompanyKpiMappingResults(
            kpi=Kpi.from_proto(proto.kpi),
            data=[KpiMappingResultData.from_proto(d) for d in proto.data],
        )


@dataclass
class CompanyKpiMappingResults:
    """
    KPI mapping results for a company.

    Attributes:
        company: The company.
        results: The results.
    """

    company: Company
    results: Sequence[SingleCompanyKpiMappingResults]

    @staticmethod
    def from_proto(proto: ProtoCompanyKpiMappingResults) -> "CompanyKpiMappingResults":
        """Create a CompanyKpiMappingResults from the given protobuf CompanyKpiMappingResults."""
        return CompanyKpiMappingResults(
            company=Company.from_proto(proto.entity),
            results=[SingleCompanyKpiMappingResults.from_proto(r) for r in proto.kpi_results],
        )
