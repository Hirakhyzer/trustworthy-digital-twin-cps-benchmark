from __future__ import annotations

from twinsec.core.models import DomainProfile, Evidence, TelemetryRecord


def invariant_value(profile: DomainProfile, values) -> float:
    centered = [float(values[s]) - b for s, b in zip(profile.signals, profile.base)]
    return sum(w * x for w, x in zip(profile.invariant_weights, centered))


def invariant_evidence(profile: DomainProfile, record: TelemetryRecord) -> Evidence:
    value = abs(invariant_value(profile, record.values))
    score = min(1.0, max(0.0, (value - profile.invariant_tolerance) / max(profile.invariant_tolerance, 1e-9)))
    return Evidence("invariant", score, f"|invariant|={value:.3f}")
