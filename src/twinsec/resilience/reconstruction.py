from __future__ import annotations

from twinsec.core.models import TelemetryRecord, TwinPrediction


def reconstruct(record: TelemetryRecord | None, prediction: TwinPrediction, source_trust: float, twin_trust: float):
    if record is None:
        return dict(prediction.values)
    if source_trust >= 0.55:
        return dict(record.values)
    alpha = twin_trust / max(twin_trust + source_trust, 1e-9)
    return {
        key: alpha * float(prediction.values[key]) + (1.0 - alpha) * float(record.values[key])
        for key in prediction.values
    }
