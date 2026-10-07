from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
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


def compare_paired_metric(
    baseline: Iterable[Mapping[str, float]],
    candidate: Iterable[Mapping[str, float]],
    metric: str,
    *,
    higher_is_better: bool = True,
) -> PairedMetricSummary:
    """Compare matched benchmark runs without pretending pairs are independent.

    Inputs must already be aligned by the experiment driver (same domain,
    scenario, seed and protocol). The reported 95% interval is a normal
    approximation over paired deltas and should be treated as descriptive for
    small samples.
    """
    left = list(baseline)
    right = list(candidate)
    if len(left) != len(right):
        raise ValueError("baseline and candidate must contain the same number of matched runs")
    if not left:
        raise ValueError("at least one matched run is required")

    baseline_values = [float(row[metric]) for row in left]
    candidate_values = [float(row[metric]) for row in right]
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
