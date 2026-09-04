from __future__ import annotations

from twinsec.core.models import Diagnosis, DiagnosisLabel, Evidence


def diagnose(evidence: list[Evidence], source: str = "telemetry") -> Diagnosis:
    by = {e.channel: e.score for e in evidence}
    physics = by.get("physics", 0.0)
    temporal = by.get("temporal", 0.0)
    invariant = by.get("invariant", 0.0)
    network = by.get("network", 0.0)
    cross = by.get("cross_sensor", 0.0)

    if network >= 0.80 and physics < 0.45:
        return Diagnosis(DiagnosisLabel.NETWORK_FAULT, network, source, tuple(evidence))
    if temporal >= 0.70:
        return Diagnosis(DiagnosisLabel.CYBER_ATTACK, max(temporal, physics), source, tuple(evidence))
    if physics >= 0.65 and cross >= 0.55:
        return Diagnosis(DiagnosisLabel.CYBER_ATTACK, max(physics, cross), source, tuple(evidence))
    if physics >= 0.65 and invariant < 0.25:
        return Diagnosis(DiagnosisLabel.MODEL_MISMATCH, physics * 0.85, None, tuple(evidence))
    if invariant >= 0.60 and physics >= 0.45:
        return Diagnosis(DiagnosisLabel.SENSOR_FAULT, max(invariant, physics), source, tuple(evidence))
    if physics >= 0.45:
        return Diagnosis(DiagnosisLabel.UNKNOWN, physics, source, tuple(evidence))
    return Diagnosis(DiagnosisLabel.NORMAL, 1.0 - max(physics, temporal, invariant, network, cross), None, tuple(evidence))
