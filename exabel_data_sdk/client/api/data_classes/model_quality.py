from enum import Enum

from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    ModelQuality as ProtoModelQuality,
)


class ModelQuality(Enum):
    """Enum representing the model quality."""

    # Low model quality.
    LOW = 1
    # Medium model quality.
    MEDIUM = 2
    # High model quality.
    HIGH = 3
    # Very high model quality.
    VERY_HIGH = 4

    @staticmethod
    def from_proto(proto: ProtoModelQuality.ValueType) -> "ModelQuality":
        """Create a ModelQuality from the given protobuf ModelQuality."""
        if proto == ProtoModelQuality.MODEL_QUALITY_LOW:
            return ModelQuality.LOW
        if proto == ProtoModelQuality.MODEL_QUALITY_MEDIUM:
            return ModelQuality.MEDIUM
        if proto == ProtoModelQuality.MODEL_QUALITY_HIGH:
            return ModelQuality.HIGH
        if proto == ProtoModelQuality.MODEL_QUALITY_VERY_HIGH:
            return ModelQuality.VERY_HIGH
        raise AssertionError("Unknown model quality")
