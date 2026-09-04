from __future__ import annotations

from enum import Enum


class RecoveryState(str, Enum):
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    DIAGNOSE = "DIAGNOSE"
    ISOLATE = "ISOLATE"
    RECONSTRUCT = "RECONSTRUCT"
    DEGRADED = "DEGRADED"
    VERIFY = "VERIFY"
    RECOVERY = "RECOVERY"


def choose_state(anomaly_score: float, source_trust: float):
    if anomaly_score < 0.25:
        return RecoveryState.NORMAL
    if anomaly_score < 0.45:
        return RecoveryState.WATCH
    if source_trust < 0.35:
        return RecoveryState.RECONSTRUCT
    return RecoveryState.DIAGNOSE
