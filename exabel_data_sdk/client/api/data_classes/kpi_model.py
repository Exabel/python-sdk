from dataclasses import dataclass

from exabel_data_sdk.client.api.data_classes.kpi_model_data import KpiModelData
from exabel_data_sdk.client.api.data_classes.kpi_model_weight_groups import KpiModelWeightGroups
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import KpiModel as ProtoKpiModel


@dataclass
class KpiModel:
    """
    Represents a KPI model.

    Attributes:
        name:           The resource name of the model.
        id:             The numeric id of the model.
        display_name:   The display name of the model.
        data:           The data of the model.
        weights:        The weight groups of the model.
    """

    name: str
    id: int
    display_name: str
    data: KpiModelData
    weights: KpiModelWeightGroups

    @staticmethod
    def from_proto(proto: ProtoKpiModel) -> "KpiModel":
        """Create a KpiModel from the given protobuf KpiModel."""
        return KpiModel(
            name=proto.name,
            id=proto.id,
            display_name=proto.display_name,
            data=KpiModelData.from_proto(proto.data),
            weights=KpiModelWeightGroups.from_proto(proto.weights),
        )
