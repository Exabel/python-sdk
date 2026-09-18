"""Model resources with typed configuration shared by every API client."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from google.protobuf.json_format import MessageToDict, ParseDict

from exabel.stubs.exabel.api.analytics.v1 import prediction_model_messages_pb2 as proto


@dataclass
class PredictionModel:
    """Get returns configuration even when it cannot be submitted as a write."""

    display_name: str
    configuration: dict[str, Any] | None = None
    name: str | None = None
    description: str = ""
    folder: str = ""
    configuration_error: str = ""
    configuration_writable: bool | None = None
    model_type: str = ""
    schedule: dict[str, Any] | None = None
    create_time: datetime | None = None
    update_time: datetime | None = None

    def to_proto(self) -> proto.PredictionModel:
        """Exclude output-only fields; configuration uses the API's JSON names and values."""
        result = proto.PredictionModel(
            name=self.name, display_name=self.display_name, description=self.description
        )
        if self.configuration is not None:
            ParseDict(self.configuration, result.configuration)
            result.configuration.SetInParent()
        return result

    @staticmethod
    def from_proto(value: proto.PredictionModel) -> "PredictionModel":
        """Preserve the distinction between list metadata and inspected configuration."""
        return PredictionModel(
            name=value.name,
            display_name=value.display_name,
            description=value.description,
            folder=value.folder,
            configuration_error=value.configuration_error,
            configuration_writable=value.configuration_writable
            if value.HasField("configuration_writable")
            else None,
            model_type=value.model_type,
            create_time=value.create_time.ToDatetime(tzinfo=timezone.utc)
            if value.HasField("create_time")
            else None,
            update_time=value.update_time.ToDatetime(tzinfo=timezone.utc)
            if value.HasField("update_time")
            else None,
            schedule=MessageToDict(value.schedule) if value.HasField("schedule") else None,
            configuration=MessageToDict(value.configuration)
            if value.HasField("configuration")
            else None,
        )
