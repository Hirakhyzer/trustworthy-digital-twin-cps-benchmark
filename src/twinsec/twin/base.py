from __future__ import annotations

from dataclasses import dataclass

from twinsec.core.models import DomainProfile, TwinPrediction
from twinsec.core.utils import clamp


@dataclass
class DigitalTwin:
    profile: DomainProfile
    mismatch: float = 0.0

    def __post_init__(self):
        self.state = list(self.profile.base)

    def reset(self):
        self.state = list(self.profile.base)

    def predict(self, t: int, control: float) -> TwinPrediction:
        p = self.profile
        nxt = []
        for i in range(3):
            deviation = self.state[i] - p.base[i]
            coupled = p.coupling[i] * (self.state[0] - p.base[0])
            gain = p.control_gain[i] * (1.0 + self.mismatch)
            decay = p.decay[i] * (1.0 - 0.4 * self.mismatch)
            dx = -decay * deviation + gain * (control - 0.65) + coupled
            value = clamp(
                self.state[i] + dx,
                p.plausible_min[i],
                p.plausible_max[i],
            )
            nxt.append(value)
        self.state = nxt
        return TwinPrediction(
            timestamp=float(t),
            values={k: v for k, v in zip(p.signals, nxt)},
            uncertainty={k: u * (1.0 + abs(self.mismatch) * 2.0) for k, u in zip(p.signals, p.uncertainty)},
        )
