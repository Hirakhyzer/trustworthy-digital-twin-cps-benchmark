from __future__ import annotations

from twinsec.core.models import TelemetryRecord, TwinPrediction


def normalized_residuals(record: TelemetryRecord, prediction: TwinPrediction) -> dict[str, float]:
    out = {}
    for key, predicted in prediction.values.items():
        measured = float(record.values[key])
        sigma = max(float(prediction.uncertainty.get(key, 1.0)), 1e-9)
        out[key] = abs(measured - predicted) / sigma
    return out


def residual_score(record: TelemetryRecord, prediction: TwinPrediction) -> float:
    values = normalized_residuals(record, prediction).values()
    values = list(values)
    return max(values) if values else 0.0
