from __future__ import annotations

from statistics import mean
from twinsec.domains.registry import DOMAIN_PROFILES
from twinsec.twin.calibration import calibrate_residual_threshold


def leave_one_domain_out_thresholds(runner):
    out = {}
    domains = list(DOMAIN_PROFILES)
    calibrated = {d: runner.calibrate_domain(d) for d in domains}
    for held_out in domains:
        train = [v for d, v in calibrated.items() if d != held_out]
        out[held_out] = mean(train)
    return out


def threshold_transfer_gap(native_threshold: float, transferred_threshold: float) -> float:
    return abs(transferred_threshold - native_threshold) / max(native_threshold, 1e-9)
