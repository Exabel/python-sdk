from dataclasses import dataclass

from exabel_data_sdk.client.api.data_classes.kpi_mapping_group_reference import (
    KpiMappingGroupReference,
)
from exabel_data_sdk.client.api.data_classes.kpi_model_data import KpiModelData
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiMappingModel as ProtoKpiMappingModel,
)


@dataclass
class KpiMappingModel:
    """
    Represents a model built on a single KPI mapping.

    Attributes:
        group:  The KPI mapping group of the model.
        data:   The data for the model.
    """

    group: KpiMappingGroupReference
    data: KpiModelData

    @staticmethod
    def from_proto(proto: ProtoKpiMappingModel) -> "KpiMappingModel":
        """Create a KpiMappingModel from the given protobuf KpiMappingModel."""
        return KpiMappingModel(
            group=KpiMappingGroupReference.from_proto(proto.source),
            data=KpiModelData.from_proto(proto.kpi_model_data),
        )
