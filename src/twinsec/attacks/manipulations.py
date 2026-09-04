from __future__ import annotations

from dataclasses import replace
from twinsec.core.models import TelemetryRecord
from .base import replace_values


def bias(record: TelemetryRecord, key: str, amount: float) -> TelemetryRecord:
    values = dict(record.values)
    values[key] = float(values[key]) + amount
    return replace_values(record, values)


def drift(record: TelemetryRecord, key: str, amount: float, progress: float) -> TelemetryRecord:
    return bias(record, key, amount * progress)


def freeze(record: TelemetryRecord, frozen: TelemetryRecord) -> TelemetryRecord:
    return replace_values(record, frozen.values)


def replay(record: TelemetryRecord, old: TelemetryRecord, rewrite_metadata: bool = False) -> TelemetryRecord:
    if rewrite_metadata:
        return replace_values(record, old.values)
    return replace(old, delivered_at=record.delivered_at)


def coordinated(record: TelemetryRecord, amount: float) -> TelemetryRecord:
    values = {k: float(v) + amount * (i + 1) for i, (k, v) in enumerate(record.values.items())}
    return replace_values(record, values)
