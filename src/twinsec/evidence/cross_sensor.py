from __future__ import annotations

from twinsec.core.models import DomainProfile, Evidence, TelemetryRecord


def cross_sensor_evidence(profile: DomainProfile, record: TelemetryRecord) -> Evidence:
    vals = [float(record.values[s]) for s in profile.signals]
    spans = [max(hi - lo, 1e-9) for lo, hi in zip(profile.plausible_min, profile.plausible_max)]
    centered = [abs(v - b) / span for v, b, span in zip(vals, profile.base, spans)]
    spread = max(centered) - min(centered)
    score = min(1.0, spread * 8.0)
    return Evidence("cross_sensor", score, f"normalized deviation spread={spread:.3f}")
