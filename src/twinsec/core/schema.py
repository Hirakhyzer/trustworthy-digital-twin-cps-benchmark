from __future__ import annotations

SCHEMA_VERSION = "0.1"

REQUIRED_TELEMETRY_FIELDS = (
    "source",
    "timestamp",
    "sequence",
    "values",
    "delivered_at",
)

COMMON_EVENT_FAMILIES = (
    "NORMAL",
    "OPERATIONAL_CHANGE",
    "SENSOR_FAULT",
    "PHYSICAL_FAULT",
    "NETWORK_DEGRADATION",
    "BIAS_ATTACK",
    "DRIFT_ATTACK",
    "FREEZE_ATTACK",
    "REPLAY_ATTACK",
    "REWRITTEN_REPLAY",
    "COMMAND_MANIPULATION",
    "COORDINATED_ATTACK",
    "ATTACK_PLUS_FAULT",
    "MODEL_MISMATCH",
    "ATTACK_PLUS_MODEL_MISMATCH",
    "RECOVERY",
)
