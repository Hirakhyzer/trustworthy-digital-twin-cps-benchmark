from __future__ import annotations

from dataclasses import dataclass
from math import log
from typing import Iterable

from twinsec.core.models import DiagnosisLabel


@dataclass(frozen=True)
class CalibrationBin:
    lower: float
    upper: float
    count: int
    mean_confidence: float
    accuracy: float


@dataclass(frozen=True)
class CalibrationReport:
    count: int
    brier_score: float
    log_loss: float
    expected_calibration_error: float
    maximum_calibration_error: float
    overconfidence_gap: float
    bins: tuple[CalibrationBin, ...]


def confidence_calibration(
    predictions: Iterable[tuple[DiagnosisLabel, float, DiagnosisLabel]],
    *,
    bins: int = 10,
    epsilon: float = 1e-12,
) -> CalibrationReport:
    """Evaluate whether diagnosis confidence matches empirical correctness.

    Each input is ``(predicted_label, confidence, expected_label)``. Confidence
    is interpreted as probability assigned to the predicted class. This is a
    top-label calibration diagnostic, not a replacement for full multiclass
    probabilistic evaluation.
    """
    if bins < 1:
        raise ValueError("bins must be positive")

    rows = []
    for predicted, confidence, expected in predictions:
        p = float(confidence)
        if not 0.0 <= p <= 1.0:
            raise ValueError("confidence must be within [0, 1]")
        rows.append((p, 1.0 if predicted == expected else 0.0))

    if not rows:
        return CalibrationReport(0, 0.0, 0.0, 0.0, 0.0, 0.0, ())

    n = len(rows)
    brier = sum((p - correct) ** 2 for p, correct in rows) / n
    loss = 0.0
    for p, correct in rows:
        q = min(max(p, epsilon), 1.0 - epsilon)
        loss -= correct * log(q) + (1.0 - correct) * log(1.0 - q)
    loss /= n

    output_bins = []
    weighted_gap = 0.0
    maximum_gap = 0.0
    for index in range(bins):
        lower = index / bins
        upper = (index + 1) / bins
        members = [
            row for row in rows
            if lower <= row[0] <= upper and (index == bins - 1 or row[0] < upper)
        ]
        if not members:
            continue
        mean_confidence = sum(p for p, _ in members) / len(members)
        accuracy = sum(correct for _, correct in members) / len(members)
        gap = abs(mean_confidence - accuracy)
        weighted_gap += len(members) / n * gap
        maximum_gap = max(maximum_gap, gap)
        output_bins.append(
            CalibrationBin(lower, upper, len(members), mean_confidence, accuracy)
        )

    mean_confidence = sum(p for p, _ in rows) / n
    accuracy = sum(correct for _, correct in rows) / n
    return CalibrationReport(
        count=n,
        brier_score=brier,
        log_loss=loss,
        expected_calibration_error=weighted_gap,
        maximum_calibration_error=maximum_gap,
        overconfidence_gap=mean_confidence - accuracy,
        bins=tuple(output_bins),
    )
