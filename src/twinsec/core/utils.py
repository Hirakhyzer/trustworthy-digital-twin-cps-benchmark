from __future__ import annotations

import math


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def mean(values):
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def rmse(errors):
    errors = list(errors)
    return math.sqrt(sum(e * e for e in errors) / len(errors)) if errors else 0.0


def quantile(values, q: float):
    data = sorted(values)
    if not data:
        return 0.0
    q = clamp(q, 0.0, 1.0)
    pos = q * (len(data) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(data) - 1)
    frac = pos - lo
    return data[lo] * (1 - frac) + data[hi] * frac
