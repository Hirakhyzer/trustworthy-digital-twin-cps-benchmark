from __future__ import annotations

from twinsec.core.models import Evidence, TelemetryRecord


def temporal_evidence(record: TelemetryRecord, expected_sequence: int, current_t: int, max_age: float = 3.0) -> Evidence:
    age = float(record.delivered_at - record.timestamp)
    seq_gap = abs(record.sequence - expected_sequence)
    score = 0.0
    reasons = []
    if age > max_age:
        score = max(score, min(1.0, age / (2 * max_age)))
        reasons.append(f"age={age:.2f}")
    if seq_gap > 1:
        score = max(score, min(1.0, seq_gap / 8.0))
        reasons.append(f"sequence_gap={seq_gap}")
    if record.timestamp < current_t - max_age:
        score = max(score, 1.0)
        reasons.append("stale_timestamp")
    return Evidence("temporal", score, ", ".join(reasons) if reasons else "fresh metadata")
