from dataclasses import dataclass

import pandas as pd

from exabel.client.api.data_classes.model_quality import ModelQuality
from exabel.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiModelData as ProtoKpiModelData,
)
from exabel.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    ModelQuality as ProtoModelQuality,
)


@dataclass
class KpiModelData:
    """
    Data for a KPI model.

    Attributes:
        prediction:         The prediction.
        prediction_yoy_rel: The relative YoY prediction.
        prediction_yoy_abs: The absolute YoY prediction.
        consensus:          The consensus.
        consensus_yoy_rel:  The relative YoY consensus.
        consensus_yoy_abs:  The absolute YoY consensus.
        delta_abs:          The absolute delta.
        delta_rel:          The relative delta.
        delta_by_error:     The delta by error.
        model_quality:      The model quality.
        mape:               The MAPE (mean absolute percentage error).
        mape_pit:           The point-in-time MAPE (mean absolute percentage error).
        mae:                The MAE (mean absolute error).
        mae_pit:            The point-in-time MAE (mean absolute error).
        error_count:        Number of data points used to calculate the MAE and MAPE.
        hit_rate:           The hit rate.
        hit_rate_count:     Number of data points used to calculate the hit rate.
        revision_1_week:    The 1 week revision.
        revision_1_month:   The 1 month revision.
        error:              Optional error, if the model estimation failed.
    """

    prediction: float | None
    prediction_yoy_rel: float | None
    prediction_yoy_abs: float | None
    consensus: float | None
    consensus_yoy_rel: float | None
    consensus_yoy_abs: float | None
    delta_abs: float | None
    delta_rel: float | None
    delta_by_error: float | None
    model_quality: ModelQuality | None
    mape: float | None
    mape_pit: float | None
    mae: float | None
    mae_pit: float | None
    error_count: int | None
    hit_rate: float | None
    hit_rate_count: int | None
    revision_1_week: float | None
    revision_1_month: float | None
    date: pd.Timestamp | None
    error: str

    @staticmethod
    def from_proto(proto: ProtoKpiModelData) -> "KpiModelData":
        """Create a KpiModelData from the given protobuf KpiModelData."""
        return KpiModelData(
            prediction=proto.prediction if proto.HasField("prediction") else None,
            prediction_yoy_rel=(
                proto.prediction_yoy_rel if proto.HasField("prediction_yoy_rel") else None
            ),
            prediction_yoy_abs=(
                proto.prediction_yoy_abs if proto.HasField("prediction_yoy_abs") else None
            ),
            consensus=proto.consensus if proto.HasField("consensus") else None,
            consensus_yoy_rel=(
                proto.consensus_yoy_rel if proto.HasField("consensus_yoy_rel") else None
            ),
            consensus_yoy_abs=(
                proto.consensus_yoy_abs if proto.HasField("consensus_yoy_abs") else None
            ),
            delta_abs=proto.delta_abs if proto.HasField("delta_abs") else None,
            delta_rel=proto.delta_rel if proto.HasField("delta_rel") else None,
            delta_by_error=proto.delta_by_error if proto.HasField("delta_by_error") else None,
            model_quality=(
                ModelQuality.from_proto(proto.model_quality)
                if proto.model_quality != ProtoModelQuality.MODEL_QUALITY_UNSPECIFIED
                else None
            ),
            mape=proto.mape if proto.HasField("mape") else None,
            mape_pit=proto.mape_pit if proto.HasField("mape_pit") else None,
            mae=proto.mae if proto.HasField("mae") else None,
            mae_pit=proto.mae_pit if proto.HasField("mae_pit") else None,
            error_count=proto.error_count if proto.HasField("error_count") else None,
            hit_rate=proto.hit_rate if proto.HasField("hit_rate") else None,
            hit_rate_count=proto.hit_rate_count if proto.HasField("hit_rate_count") else None,
            revision_1_week=proto.revision_1_week if proto.HasField("revision_1_week") else None,
            revision_1_month=proto.revision_1_month if proto.HasField("revision_1_month") else None,
            date=(
                pd.Timestamp(year=proto.date.year, month=proto.date.month, day=proto.date.day)
                if proto.HasField("date")
                else None
            ),
            error=proto.error,
        )
