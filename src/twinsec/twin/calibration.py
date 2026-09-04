from __future__ import annotations

from twinsec.core.utils import quantile


def calibrate_residual_threshold(normal_scores, quantile_level: float = 0.995, floor: float = 0.45) -> float:
    """Calibrate a transparent residual threshold from normal-operation scores.

    The small floor prevents unrealistically tiny thresholds while still allowing
    domain-to-domain calibration differences to remain visible.
    """
    return max(floor, quantile(normal_scores, quantile_level))
