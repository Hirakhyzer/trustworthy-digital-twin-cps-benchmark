from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from statistics import mean
from typing import Iterable, Mapping


@dataclass(frozen=True)
class PairedMetricSummary:
    metric: str
    pairs: int
    baseline_mean: float
    candidate_mean: float
    mean_delta: float
    standard_error: float
    ci95_lower: float
    ci95_upper: float
    improved: int
    worsened: int
    tied: int


def _pair_key(row: Mapping[str, object], fields: tuple[str, ...]) -> tuple[object, ...]:
    missing = [field for field in fields if field not in row]
    if missing:
        raise ValueError(f"paired benchmark row is missing key fields: {missing}")
    return tuple(row[field] for field in fields)


def compare_paired_metric(
    baseline: Iterable[Mapping[str, object]],
    candidate: Iterable[Mapping[str, object]],
    metric: str,
    *,
    higher_is_better: bool = True,
    pair_fields: tuple[str, ...] = ("domain", "scenario", "seed"),
) -> PairedMetricSummary:
    """Compare truly matched benchmark runs using paired deltas.

    By default, rows must align on ``domain``, ``scenario`` and ``seed``.
    Explicit alignment checks prevent silently comparing unrelated runs that
    happen to occupy the same list position.
    """
    left = list(baseline)
    right = list(candidate)
    if len(left) != len(right):
        raise ValueError("baseline and candidate must contain the same number of matched runs")
    if not left:
        raise ValueError("at least one matched run is required")
    if not pair_fields:
        raise ValueError("pair_fields must contain at least one alignment field")

    left_keys = [_pair_key(row, pair_fields) for row in left]
    right_keys = [_pair_key(row, pair_fields) for row in right]
    if len(set(left_keys)) != len(left_keys):
        raise ValueError("baseline contains duplicate pairing keys")
    if len(set(right_keys)) != len(right_keys):
        raise ValueError("candidate contains duplicate pairing keys")
    if left_keys != right_keys:
        mismatch = next(
            (index for index, (left_key, right_key) in enumerate(zip(left_keys, right_keys)) if left_key != right_key),
            0,
        )
        raise ValueError(
            "paired benchmark rows are misaligned at index "
            f"{mismatch}: baseline={left_keys[mismatch]!r}, candidate={right_keys[mismatch]!r}"
        )

    try:
        baseline_values = [float(row[metric]) for row in left]
        candidate_values = [float(row[metric]) for row in right]
    except KeyError as exc:
        raise ValueError(f"metric {metric!r} is missing from a benchmark row") from exc

    if not all(isfinite(value) for value in [*baseline_values, *candidate_values]):
        raise ValueError("paired metric values must be finite")

    raw_deltas = [c - b for b, c in zip(baseline_values, candidate_values)]
    utility_deltas = raw_deltas if higher_is_better else [-d for d in raw_deltas]

    delta_mean = mean(raw_deltas)
    if len(raw_deltas) > 1:
        centered = sum((d - delta_mean) ** 2 for d in raw_deltas)
        sample_sd = sqrt(centered / (len(raw_deltas) - 1))
        se = sample_sd / sqrt(len(raw_deltas))
    else:
        se = 0.0
    half_width = 1.96 * se

    tolerance = 1e-12
    improved = sum(d > tolerance for d in utility_deltas)
    worsened = sum(d < -tolerance for d in utility_deltas)
    tied = len(utility_deltas) - improved - worsened

    return PairedMetricSummary(
        metric=metric,
        pairs=len(raw_deltas),
        baseline_mean=mean(baseline_values),
        candidate_mean=mean(candidate_values),
        mean_delta=delta_mean,
        standard_error=se,
        ci95_lower=delta_mean - half_width,
        ci95_upper=delta_mean + half_width,
        improved=improved,
        worsened=worsened,
        tied=tied,
    )
