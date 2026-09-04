from __future__ import annotations

from twinsec.core.models import Evidence, TelemetryRecord


def network_evidence(record: TelemetryRecord | None, current_t: int) -> Evidence:
    if record is None:
        return Evidence("network", 1.0, "packet missing")
    delay = max(0.0, record.delivered_at - record.timestamp)
    score = min(1.0, max(0.0, (delay - 2.0) / 6.0))
    return Evidence("network", score, f"delay={delay:.2f}")
