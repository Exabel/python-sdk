from dataclasses import dataclass
from typing import Optional, Sequence

from exabel_data_sdk.client.api.data_classes.kpi import Kpi
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiBreakdown as ProtoKpiBreakdown,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiBreakdownNode as ProtoKpiBreakdownNode,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiHierarchy as ProtoKpiHierarchy,
)


@dataclass
class KpiBreakdownNode:
    """
    A single node in a KpiBreakdown.

    Attributes:
        kpi:        The KPI represented by this node.
        header:     The string representing this node, when the node represents a grouping of KPIs
                    and not a single one.
        children:   The children of this node.
    """

    kpi: Optional[Kpi]
    header: Optional[str]
    children: Sequence["KpiBreakdownNode"]

    @staticmethod
    def from_proto(proto: ProtoKpiBreakdownNode) -> "KpiBreakdownNode":
        """Create a KpiBreakdownNode from the given protobuf KpiBreakdownNode."""
        return KpiBreakdownNode(
            kpi=Kpi.from_proto(proto.kpi) if proto.HasField("kpi") else None,
            header=proto.header if proto.HasField("header") else None,
            children=[KpiBreakdownNode.from_proto(n) for n in proto.children],
        )


@dataclass
class KpiBreakdown:
    """
    A KpiBreakdown.

    Attributes:
        nodes: The nodes of the KpiBreakdown.
    """

    kpis: Sequence[KpiBreakdownNode]

    @staticmethod
    def from_proto(proto: ProtoKpiBreakdown) -> "KpiBreakdown":
        """Create a KpiBreakdown from the given protobuf KpiBreakdown."""
        return KpiBreakdown(kpis=[KpiBreakdownNode.from_proto(kpi) for kpi in proto.kpis])


@dataclass
class KpiHierarchy:
    """
    A KpiHierarchy.

    Attributes:
        name:       The resource name of the KpiHierarchy.
        freq:       The frequency of the KpiHierarchy.
        breakdown:  The breakdown of the KpiHierarchy.
    """

    name: str
    freq: str
    breakdown: KpiBreakdown

    @staticmethod
    def from_proto(proto: ProtoKpiHierarchy) -> "KpiHierarchy":
        """Create a KpiHierarchy from the given protobuf KpiHierarchy."""
        return KpiHierarchy(
            name=proto.name,
            freq=proto.freq,
            breakdown=KpiBreakdown.from_proto(proto.breakdown),
        )
