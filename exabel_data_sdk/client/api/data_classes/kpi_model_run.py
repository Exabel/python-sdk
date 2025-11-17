from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from dateutil import tz
from google.protobuf.timestamp_pb2 import Timestamp as ProtoTimestamp

from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiModelRun as ProtoKpiModelRun,
)


@dataclass
class KpiModelRun:
    """
    Information about a single KPI model run.

    Attributes:
        created_at:  The time the run was created.
        started_at:  The time the run was started.
        finished_at: The time the run finished.
        error:       An optional error message if the run failed.
    """

    created_at: Optional[datetime]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    error: Optional[str]

    @staticmethod
    def from_proto(proto: ProtoKpiModelRun) -> "KpiModelRun":
        """Create a KpiModelRun from the given protobuf KpiModelRun."""
        return KpiModelRun(
            created_at=(
                KpiModelRun._proto_timestamp_to_datetime(proto.created_at)
                if proto.HasField("created_at")
                else None
            ),
            started_at=(
                KpiModelRun._proto_timestamp_to_datetime(proto.started_at)
                if proto.HasField("started_at")
                else None
            ),
            finished_at=(
                KpiModelRun._proto_timestamp_to_datetime(proto.finished_at)
                if proto.HasField("finished_at")
                else None
            ),
            error=proto.error if proto.HasField("error") else None,
        )

    @staticmethod
    def _proto_timestamp_to_datetime(timestamp: ProtoTimestamp) -> Optional[datetime]:
        """Convert a protobuf Timestamp to a datetime object."""
        return datetime.fromtimestamp(timestamp.seconds, tz=tz.tzutc())
