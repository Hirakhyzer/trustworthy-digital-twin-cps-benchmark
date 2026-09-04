from __future__ import annotations

from twinsec.core.models import Diagnosis


def explain(diagnosis: Diagnosis) -> dict:
    ranked = sorted(diagnosis.evidence, key=lambda x: x.score, reverse=True)
    return {
        "label": diagnosis.label.value,
        "confidence": diagnosis.confidence,
        "suspected_source": diagnosis.suspected_source,
        "evidence": [
            {"channel": e.channel, "score": e.score, "reason": e.reason}
            for e in ranked
        ],
    }
