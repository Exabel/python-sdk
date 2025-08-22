from dataclasses import dataclass
from typing import Optional, Sequence

from exabel_data_sdk.client.api.data_classes.kpi_mapping_model import KpiMappingModel
from exabel_data_sdk.client.api.data_classes.kpi_model import KpiModel
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_service_pb2 import (
    ListCompanyKpiModelResultsResponse,
)


@dataclass
class CompanyKpiModels:
    """
    Models for a company KPI.

    Attributes:
        exabel_model:       The Exabel model.
        hierarchical_model: The hierarchical model.
        custom_models:      The custom models.
        kpi_mapping_models: The KPI mapping models.
    """

    exabel_model: Optional[KpiModel]
    hierarchical_model: Optional[KpiModel]
    custom_models: Sequence[KpiModel]
    kpi_mapping_models: Sequence[KpiMappingModel]

    @staticmethod
    def from_proto(proto: ListCompanyKpiModelResultsResponse) -> "CompanyKpiModels":
        """Create a CompanyKpiModelResult from the given ListCompanyKpiModelResultsResponse."""
        return CompanyKpiModels(
            exabel_model=(
                KpiModel.from_proto(proto.exabel_model) if proto.HasField("exabel_model") else None
            ),
            hierarchical_model=(
                KpiModel.from_proto(proto.hierarchical_model)
                if proto.HasField("hierarchical_model")
                else None
            ),
            custom_models=[KpiModel.from_proto(model) for model in proto.custom_models],
            kpi_mapping_models=[
                KpiMappingModel.from_proto(model) for model in proto.kpi_mapping_models
            ],
        )
