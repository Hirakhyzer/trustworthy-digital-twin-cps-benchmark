from twinsec.benchmark.calibration import confidence_calibration
from twinsec.benchmark.paired import compare_paired_metric
from twinsec.core.models import DiagnosisLabel


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
    baseline = [{"f1": 0.4}, {"f1": 0.6}, {"f1": 0.5}]
    candidate = [{"f1": 0.5}, {"f1": 0.7}, {"f1": 0.5}]
    summary = compare_paired_metric(baseline, candidate, "f1")
    assert summary.pairs == 3
    assert summary.improved == 2
    assert summary.worsened == 0
    assert summary.tied == 1
    assert summary.mean_delta > 0


def test_lower_is_better_reverses_utility_direction_not_raw_delta():
    baseline = [{"rmse": 2.0}, {"rmse": 3.0}]
    candidate = [{"rmse": 1.0}, {"rmse": 2.5}]
    summary = compare_paired_metric(
        baseline, candidate, "rmse", higher_is_better=False
    )
    assert summary.improved == 2
    assert summary.mean_delta < 0


def test_paired_summary_requires_matched_run_count():
    try:
        compare_paired_metric([{"f1": 0.5}], [], "f1")
    except ValueError as exc:
        assert "same number" in str(exc)
    else:
        raise AssertionError("unmatched experiments should fail")
