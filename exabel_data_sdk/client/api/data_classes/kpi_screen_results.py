from dataclasses import dataclass
from typing import Sequence

from exabel_data_sdk.client.api.data_classes.company import Company
from exabel_data_sdk.client.api.data_classes.company_kpi_model_result import CompanyKpiModelResult
from exabel_data_sdk.client.api.data_classes.fiscal_period import FiscalPeriod
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiScreenCompanyResult as ProtoKpiScreenCompanyResult,
)


@dataclass
class KpiScreenCompanyResult:
    """
    KPI screen results for a single company.

    Attributes:
        company:        The company.
        fiscal_period:  The fiscal period for this result.
        results:        KPI model results for this company.
    """

    company: Company
    fiscal_period: FiscalPeriod | None
    results: Sequence[CompanyKpiModelResult]

    @staticmethod
    def from_proto(proto: ProtoKpiScreenCompanyResult) -> "KpiScreenCompanyResult":
        """Create a KpiScreenCompanyResult from the given protobuf message."""
        return KpiScreenCompanyResult(
            company=Company.from_proto(proto.company),
            fiscal_period=(
                FiscalPeriod.from_proto(proto.fiscal_period)
                if proto.HasField("fiscal_period")
                else None
            ),
            results=[CompanyKpiModelResult.from_proto(r) for r in proto.results],
        )
