import math

from twinsec.benchmark.calibration import confidence_calibration
from twinsec.benchmark.paired import compare_paired_metric
from twinsec.core.models import DiagnosisLabel


def _row(metric, value, *, domain="water", scenario="bias", seed=1):
    return {"domain": domain, "scenario": scenario, "seed": seed, metric: value}


def test_perfect_confidence_predictions_are_well_calibrated():
    rows = [
        (DiagnosisLabel.NORMAL, 1.0, DiagnosisLabel.NORMAL),
        (DiagnosisLabel.CYBER_ATTACK, 1.0, DiagnosisLabel.CYBER_ATTACK),
    ]
    report = confidence_calibration(rows)
    assert report.brier_score == 0.0
    assert report.expected_calibration_error == 0.0
    assert report.overconfidence_gap == 0.0


def test_confident_wrong_predictions_are_penalized():
    rows = [
        (DiagnosisLabel.CYBER_ATTACK, 0.9, DiagnosisLabel.NORMAL),
        (DiagnosisLabel.NORMAL, 0.9, DiagnosisLabel.CYBER_ATTACK),
    ]
    report = confidence_calibration(rows)
    assert report.brier_score > 0.8
    assert report.expected_calibration_error > 0.8
    assert report.overconfidence_gap > 0.8


def test_calibration_rejects_invalid_confidence():
    try:
        confidence_calibration([(DiagnosisLabel.NORMAL, 1.2, DiagnosisLabel.NORMAL)])
    except ValueError as exc:
        assert "confidence" in str(exc)
    else:
        raise AssertionError("invalid confidence should fail")


def test_paired_summary_tracks_improvement_direction():
    baseline = [_row("f1", 0.4, seed=1), _row("f1", 0.6, seed=2), _row("f1", 0.5, seed=3)]
    candidate = [_row("f1", 0.5, seed=1), _row("f1", 0.7, seed=2), _row("f1", 0.5, seed=3)]
    summary = compare_paired_metric(baseline, candidate, "f1")
    assert summary.pairs == 3
    assert summary.improved == 2
    assert summary.worsened == 0
    assert summary.tied == 1
    assert summary.mean_delta > 0


def test_lower_is_better_reverses_utility_direction_not_raw_delta():
    baseline = [_row("rmse", 2.0, seed=1), _row("rmse", 3.0, seed=2)]
    candidate = [_row("rmse", 1.0, seed=1), _row("rmse", 2.5, seed=2)]
    summary = compare_paired_metric(baseline, candidate, "rmse", higher_is_better=False)
    assert summary.improved == 2
    assert summary.mean_delta < 0


def test_paired_summary_requires_matched_run_count():
    try:
        compare_paired_metric([_row("f1", 0.5)], [], "f1")
    except ValueError as exc:
        assert "same number" in str(exc)
    else:
        raise AssertionError("unmatched experiments should fail")


def test_paired_summary_rejects_same_length_but_misaligned_rows():
    baseline = [_row("f1", 0.5, seed=1), _row("f1", 0.6, seed=2)]
    candidate = [_row("f1", 0.7, seed=2), _row("f1", 0.8, seed=1)]
    try:
        compare_paired_metric(baseline, candidate, "f1")
    except ValueError as exc:
        assert "misaligned" in str(exc)
    else:
        raise AssertionError("permuted runs must not be treated as matched pairs")


def test_paired_summary_rejects_duplicate_pair_keys():
    baseline = [_row("f1", 0.5, seed=1), _row("f1", 0.6, seed=1)]
    candidate = [_row("f1", 0.7, seed=1), _row("f1", 0.8, seed=1)]
    try:
        compare_paired_metric(baseline, candidate, "f1")
    except ValueError as exc:
        assert "duplicate" in str(exc)
    else:
        raise AssertionError("duplicate matched-run identities should fail")


def test_paired_summary_rejects_nonfinite_metrics():
    baseline = [_row("f1", 0.5)]
    candidate = [_row("f1", math.nan)]
    try:
        compare_paired_metric(baseline, candidate, "f1")
    except ValueError as exc:
        assert "finite" in str(exc)
    else:
        raise AssertionError("NaN benchmark metrics should fail")
