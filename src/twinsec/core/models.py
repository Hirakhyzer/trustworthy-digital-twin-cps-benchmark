from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Sequence


class DiagnosisLabel(str, Enum):
    NORMAL = "NORMAL"
    CYBER_ATTACK = "CYBER_ATTACK"
    SENSOR_FAULT = "SENSOR_FAULT"
    PHYSICAL_FAULT = "PHYSICAL_FAULT"
    NETWORK_FAULT = "NETWORK_FAULT"
    MODEL_MISMATCH = "MODEL_MISMATCH"
    OPERATIONAL_CHANGE = "OPERATIONAL_CHANGE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class TelemetryRecord:
    source: str
    timestamp: float
    sequence: int
    values: Mapping[str, float]
    delivered_at: float


@dataclass(frozen=True)
class TwinPrediction:
    timestamp: float
    values: Mapping[str, float]
    uncertainty: Mapping[str, float]


@dataclass(frozen=True)
class Evidence:
    channel: str
    score: float
    reason: str


@dataclass(frozen=True)
class Diagnosis:
    label: DiagnosisLabel
    confidence: float
    suspected_source: str | None
    evidence: Sequence[Evidence] = field(default_factory=tuple)


@dataclass(frozen=True)
class StepResult:
    t: int
    truth: Mapping[str, float]
    telemetry: TelemetryRecord | None
    prediction: TwinPrediction
    diagnosis: Diagnosis
    source_trust: float
    twin_trust: float
    reconstructed: Mapping[str, float] | None
    in_event_window: bool


@dataclass(frozen=True)
class Scenario:
    name: str
    family: str
    start: int = 80
    end: int = 130
    magnitude: float = 1.0
    target_index: int = 0


@dataclass(frozen=True)
class DomainProfile:
    name: str
    signals: tuple[str, str, str]
    base: tuple[float, float, float]
    decay: tuple[float, float, float]
    control_gain: tuple[float, float, float]
    coupling: tuple[float, float, float]
    noise: tuple[float, float, float]
    uncertainty: tuple[float, float, float]
    plausible_min: tuple[float, float, float]
    plausible_max: tuple[float, float, float]
    invariant_weights: tuple[float, float, float]
    invariant_tolerance: float
    description: str
