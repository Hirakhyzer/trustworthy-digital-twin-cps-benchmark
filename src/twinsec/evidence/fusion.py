from __future__ import annotations

from twinsec.core.models import Evidence


DEFAULT_WEIGHTS = {
    "physics": 0.30,
    "temporal": 0.27,
    "invariant": 0.18,
    "cross_sensor": 0.15,
    "network": 0.10,
}


def fuse(evidence: list[Evidence], weights=None) -> float:
    weights = weights or DEFAULT_WEIGHTS
    num = 0.0
    den = 0.0
    for item in evidence:
        w = float(weights.get(item.channel, 0.0))
        num += w * item.score
        den += w
    return num / den if den else 0.0
