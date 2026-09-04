from __future__ import annotations

from dataclasses import dataclass
import random

from twinsec.core.models import DomainProfile
from twinsec.core.utils import clamp


@dataclass
class GenericDomain:
    profile: DomainProfile
    seed: int = 7

    def __post_init__(self):
        self.rng = random.Random(self.seed)
        self.state = list(self.profile.base)
        self.energy_like = 0.0

    def reset(self):
        self.rng = random.Random(self.seed)
        self.state = list(self.profile.base)
        self.energy_like = 0.0

    def control(self, t: int) -> float:
        # Reproducible mixed operating profile with slow and step-like changes.
        periodic = 0.65 + 0.25 * __import__("math").sin(t / 17.0)
        pulse = 0.20 if 45 <= t < 65 else 0.0
        return periodic + pulse

    def step(self, t: int, physical_fault: bool = False, command_scale: float = 1.0):
        u = self.control(t) * command_scale
        p = self.profile
        nxt = []
        for i in range(3):
            deviation = self.state[i] - p.base[i]
            coupled = p.coupling[i] * (self.state[0] - p.base[0])
            dx = -p.decay[i] * deviation + p.control_gain[i] * (u - 0.65) + coupled
            if physical_fault:
                dx += (0.018 + 0.006 * i) * max(abs(p.base[i]), 1.0)
            noise = self.rng.gauss(0.0, p.noise[i] * 0.20)
            value = self.state[i] + dx + noise
            value = clamp(value, p.plausible_min[i], p.plausible_max[i])
            nxt.append(value)
        self.state = nxt
        self.energy_like += max(0.0, u)
        return {name: value for name, value in zip(p.signals, self.state)}
