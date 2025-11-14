from dataclasses import dataclass
from typing import Optional

from exabel_data_sdk.client.api.data_classes.kpi_model_run import KpiModelRun
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiModelRuns as ProtoKpiModelRuns,
)


@dataclass
class KpiModelRuns:
    """
    Information about the runs for a KPI model.

    Attributes:
        initial_run:        Initial run.
        daily_run:          Latest daily run.
        pit_backtest_run:   PiT backtest run.
    """

    initial_run: Optional[KpiModelRun]
    daily_run: Optional[KpiModelRun]
    pit_backtest_run: Optional[KpiModelRun]

    @staticmethod
    def from_proto(proto: ProtoKpiModelRuns) -> "KpiModelRuns":
        """Create a KpiModelRuns from the given protobuf KpiModelRuns."""
        return KpiModelRuns(
            initial_run=(
                KpiModelRun.from_proto(proto.initial_run) if proto.HasField("initial_run") else None
            ),
            daily_run=(
                KpiModelRun.from_proto(proto.daily_run) if proto.HasField("daily_run") else None
            ),
            pit_backtest_run=(
                KpiModelRun.from_proto(proto.pit_backtest_run)
                if proto.HasField("pit_backtest_run")
                else None
            ),
        )
