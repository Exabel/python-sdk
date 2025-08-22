from dataclasses import dataclass

from exabel_data_sdk.client.api.data_classes.kpi import Kpi
from exabel_data_sdk.client.api.data_classes.kpi_model import KpiModel
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    CompanyKpiModelResult as ProtoCompanyKpiModelResult,
)


@dataclass
class CompanyKpiModelResult:
    """
    A company KPI model result.

    Attributes:
        kpi:                        The KPI.
        model:                      The KPI model.
        accessible_mappings_count:  The number of accessible KPI mappings for the current user.
        total_mappings_count:       The total number of KPI mappings.
        models_count:               The number of KPI models.
    """

    kpi: Kpi
    model: KpiModel
    accessible_mappings_count: int
    total_mappings_count: int
    models_count: int

    @staticmethod
    def from_proto(proto: ProtoCompanyKpiModelResult) -> "CompanyKpiModelResult":
        """Create a CompanyKpiModelResult from the given protobuf CompanyKpiModelResult."""
        return CompanyKpiModelResult(
            kpi=Kpi.from_proto(proto.kpi),
            model=KpiModel.from_proto(proto.model),
            accessible_mappings_count=proto.accessible_mappings_count,
            total_mappings_count=proto.total_mappings_count,
            models_count=proto.models_count,
        )
