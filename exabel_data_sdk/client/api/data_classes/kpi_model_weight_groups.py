from dataclasses import dataclass
from typing import Optional, Sequence

from exabel_data_sdk.client.api.data_classes.kpi_mapping_group import KpiMappingGroup
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiModelFeatureWeight as ProtoKpiModelFeatureWeight,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiModelWeightGroup as ProtoKpiModelWeightGroup,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiModelWeightGroups as ProtoKpiModelWeightGroups,
)


@dataclass
class KpiModelFeatureWeight:
    """ "
    The weight for a single feature.

    Attributes:
        display_name:   The display name of the feature.
        weight:         The weight of the feature.
    """

    display_name: str
    weight: Optional[float]

    @staticmethod
    def from_proto(
        proto: ProtoKpiModelFeatureWeight,
    ) -> "KpiModelFeatureWeight":
        """Create a KpiModelFeatureWeight from the given protobuf KpiModelFeatureWeight."""
        return KpiModelFeatureWeight(
            display_name=proto.display_name,
            weight=proto.weight if proto.HasField("weight") else None,
        )


@dataclass
class KpiModelWeightGroup:
    """ "
    Represents a weight group.

    Attributes:
        display_name:   The display name of the weight group.
        group:          The KPI mapping group the group originates from, if any.
        weights:        The weights of the weight group.
    """

    display_name: str
    group: Optional[KpiMappingGroup]
    weights: Sequence[KpiModelFeatureWeight]

    @staticmethod
    def from_proto(proto: ProtoKpiModelWeightGroup) -> "KpiModelWeightGroup":
        """Create a KpiModelWeightGroup from the given protobuf KpiModelWeightGroup."""
        return KpiModelWeightGroup(
            display_name=proto.display_name,
            group=KpiMappingGroup.from_proto(proto.group) if proto.HasField("group") else None,
            weights=[KpiModelFeatureWeight.from_proto(w) for w in proto.feature_weights],
        )


@dataclass
class KpiModelWeightGroups:
    """
    Represents the weight groups of a KPI model.

    Attributes:
        is_coefficients:    Whether the weight groups are coefficients.
        weight_groups:      The weight groups.
    """

    is_coefficients: bool
    weight_groups: Sequence[KpiModelWeightGroup]

    @staticmethod
    def from_proto(proto: ProtoKpiModelWeightGroups) -> "KpiModelWeightGroups":
        """Create a KpiModelWeightGroups from the given protobuf KpiModelWeightGroups."""
        return KpiModelWeightGroups(
            is_coefficients=proto.is_coefficients,
            weight_groups=[KpiModelWeightGroup.from_proto(wg) for wg in proto.weight_groups],
        )
