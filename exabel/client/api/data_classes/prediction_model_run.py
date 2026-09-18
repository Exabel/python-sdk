from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum, IntEnum
from typing import Any

from google.protobuf.json_format import MessageToDict

from exabel.stubs.exabel.api.analytics.v1.all_pb2 import (
    PredictionModelRun as ProtoPredictionModelRun,
)
from exabel.stubs.exabel.api.analytics.v1.prediction_model_messages_pb2 import (
    ModelConfiguration as ProtoModelConfiguration,
)


class ModelConfiguration(Enum):
    """Specifies a model configuration."""

    UNSPECIFIED = ProtoModelConfiguration.MODEL_CONFIGURATION_NOT_SPECIFIED

    # Latest configuration.
    LATEST = ProtoModelConfiguration.LATEST
    # Configuration of the active run.
    ACTIVE = ProtoModelConfiguration.ACTIVE
    # Configuration of a specific run.
    SPECIFIC_RUN = ProtoModelConfiguration.SPECIFIC_RUN


class PredictionModelRunState(IntEnum):
    """State of the exact requested run, including partial and infrastructure failures."""

    @classmethod
    def parse(cls, value: int) -> "PredictionModelRunState | int":
        """Keep states this SDK version does not know as their raw integer."""
        try:
            return cls(value)
        except ValueError:
            return value

    UNSPECIFIED = 0
    WAITING = 1
    SCHEDULED = 2
    RUNNING = 3
    SUCCEEDED = 4
    FAILED = 5
    CANCELLED = 6
    MIXED = 7
    TIMED_OUT = 8
    OUT_OF_MEMORY = 9


@dataclass(frozen=True)
class PredictionModelEntityOutcome:
    """Recorded evaluation outcome for an entity within a run."""

    entity: str
    state: PredictionModelRunState | int
    error: str = ""


class PredictionModelRun:
    """
    A prediction model run in the Analytics API.

    Attributes:
        name (str):                         The resource name of the model run, for example
                                            "predictionModels/123/runs/4".
        description (str):                  A description of the run.
        configuration (ModelConfiguration): Which model configuration to use.
        configuration_source (int):         When using ModelConfiguration.SPECIFIC_RUN,
                                            this specifies the run from which to retrieve the
                                            configuration. It is not used for other configurations.
        auto_activate (bool):               Whether to automatically activate the run if it
                                            completes successfully. The run will not be activated
                                            if it fails for any of the entities in the model.
    """

    def __init__(
        self,
        name: str | None = None,
        description: str = "",
        configuration: ModelConfiguration = ModelConfiguration.LATEST,
        configuration_source: int | None = None,
        auto_activate: bool = False,
        *,
        state: PredictionModelRunState | int = PredictionModelRunState.UNSPECIFIED,
        create_time: datetime | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        active: bool = False,
        error: str = "",
        model_configuration: dict[str, Any] | None = None,
        configuration_error: str = "",
        model_configuration_writable: bool | None = None,
        entity_outcomes: tuple[PredictionModelEntityOutcome, ...] = (),
    ):
        """
        Create a prediction model run in the Analytics API.

        When creating a new prediction model run in the API, the name should be set to None.

        Args:
            name (str):                         The resource name of the model run, for example
                                                "predictionModels/123/runs/4".
            description (str):                  A description of the run.
            configuration (ModelConfiguration): Which model configuration to use.
            configuration_source (int):         When using ModelConfiguration.SPECIFIC_RUN,
                                                this specifies the run from which to retrieve the
                                                configuration. It is not used for other
                                                configurations.
            auto_activate (bool):               Whether to automatically activate the run if it
                                                completes successfully. The run will not be
                                                activated if it fails for any of the entities in
                                                the model.
        """
        self.name = name
        self.description = description
        self.configuration = configuration
        self.configuration_source = configuration_source
        self.auto_activate = auto_activate
        self.state = state
        self.create_time = create_time
        self.start_time = start_time
        self.end_time = end_time
        self.active = active
        self.error = error
        self.model_configuration = model_configuration
        self.configuration_error = configuration_error
        self.model_configuration_writable = model_configuration_writable
        self.entity_outcomes = entity_outcomes

    @staticmethod
    def from_proto(model_run: ProtoPredictionModelRun) -> "PredictionModelRun":
        """Create a PredictionModelRun from the given protobuf PredictionModelRun."""
        return PredictionModelRun(
            name=model_run.name,
            description=model_run.description,
            configuration=ModelConfiguration(model_run.configuration)
            if model_run.configuration in {v.value for v in ModelConfiguration}
            else ModelConfiguration.UNSPECIFIED,
            configuration_source=(
                model_run.configuration_source
                if model_run.HasField("configuration_source")
                else None
            ),
            auto_activate=model_run.auto_activate,
            state=PredictionModelRunState.parse(model_run.state),
            create_time=model_run.create_time.ToDatetime(tzinfo=timezone.utc)
            if model_run.HasField("create_time")
            else None,
            start_time=model_run.start_time.ToDatetime(tzinfo=timezone.utc)
            if model_run.HasField("start_time")
            else None,
            end_time=model_run.end_time.ToDatetime(tzinfo=timezone.utc)
            if model_run.HasField("end_time")
            else None,
            active=model_run.active,
            error=model_run.error,
            model_configuration=MessageToDict(model_run.model_configuration)
            if model_run.HasField("model_configuration")
            else None,
            configuration_error=model_run.configuration_error,
            model_configuration_writable=model_run.model_configuration_writable
            if model_run.HasField("model_configuration_writable")
            else None,
            entity_outcomes=tuple(
                PredictionModelEntityOutcome(
                    o.entity, PredictionModelRunState.parse(o.state), o.error
                )
                for o in model_run.entity_outcomes
            ),
        )

    def to_proto(self) -> ProtoPredictionModelRun:
        """Create a protobuf PredictionModelRun from this PredictionModelRun."""
        if (
            self.configuration == ModelConfiguration.SPECIFIC_RUN
            and self.configuration_source is None
        ):
            raise ValueError(
                "The argument 'configuration_source' must be specified when using "
                "ModelConfiguration.SPECIFIC_RUN."
            )
        return ProtoPredictionModelRun(
            name=self.name,
            description=self.description,
            configuration=self.configuration.value,
            configuration_source=self.configuration_source,
            auto_activate=self.auto_activate,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PredictionModelRun):
            return False
        return (
            self.name == other.name
            and self.description == other.description
            and self.configuration == other.configuration
            and self.configuration_source == other.configuration_source
            and self.auto_activate == other.auto_activate
            and self.state == other.state
            and self.create_time == other.create_time
            and self.start_time == other.start_time
            and self.end_time == other.end_time
            and self.active == other.active
            and self.error == other.error
            and self.model_configuration == other.model_configuration
            and self.model_configuration_writable == other.model_configuration_writable
            and self.configuration_error == other.configuration_error
            and self.entity_outcomes == other.entity_outcomes
        )

    def __repr__(self) -> str:
        return (
            f"PredictionModelRun(name='{self.name}', description='{self.description}', "
            f"configuration={self.configuration}, "
            f"configuration_source='{self.configuration_source}', "
            f"auto_activate={self.auto_activate})"
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, PredictionModelRun):
            raise ValueError(
                f"Cannot compare PredictionModelRun to non-PredictionModelRun: {other}"
            )
        return (self.name or "") < (other.name or "")
