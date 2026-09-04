from __future__ import annotations

from dataclasses import replace
from twinsec.core.models import TelemetryRecord


def replace_values(record: TelemetryRecord, values):
    return replace(record, values=dict(values))
