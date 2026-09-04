from __future__ import annotations

from twinsec.core.models import Evidence, TelemetryRecord, TwinPrediction
from twinsec.twin.residuals import residual_score


def physics_evidence(record: TelemetryRecord, prediction: TwinPrediction, threshold: float) -> Evidence:
    score = residual_score(record, prediction)
    normalized = min(1.0, max(0.0, (score - threshold) / max(threshold, 1e-9)))
    return Evidence("physics", normalized, f"max normalized residual={score:.3f}, threshold={threshold:.3f}")
