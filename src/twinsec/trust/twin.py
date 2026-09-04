from __future__ import annotations

from dataclasses import dataclass
from twinsec.core.utils import clamp


@dataclass
class TwinTrust:
    value: float = 0.90

    def update(self, residual_score: float, invariant_score: float, model_mismatch: float):
        penalty = 0.025 * max(0.0, residual_score - invariant_score) + 0.35 * abs(model_mismatch)
        recovery = 0.012 if residual_score < 0.30 else 0.0
        self.value = clamp(self.value - penalty + recovery, 0.05, 0.99)
        return self.value
