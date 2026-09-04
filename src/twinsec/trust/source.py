from __future__ import annotations

from dataclasses import dataclass
from twinsec.core.utils import clamp


@dataclass
class SourceTrust:
    value: float = 0.95
    recovery_rate: float = 0.018
    penalty_rate: float = 0.20

    def update(self, anomaly_score: float):
        if anomaly_score > 0.45:
            self.value -= self.penalty_rate * anomaly_score
        else:
            self.value += self.recovery_rate * (1.0 - anomaly_score)
        self.value = clamp(self.value, 0.02, 0.99)
        return self.value
