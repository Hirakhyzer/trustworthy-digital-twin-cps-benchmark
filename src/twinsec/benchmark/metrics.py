from __future__ import annotations

from twinsec.core.models import DiagnosisLabel
from twinsec.core.utils import rmse


FAMILY_TO_LABEL = {
    "NORMAL": DiagnosisLabel.NORMAL,
    "OPERATIONAL_CHANGE": DiagnosisLabel.OPERATIONAL_CHANGE,
    "SENSOR_FAULT": DiagnosisLabel.SENSOR_FAULT,
    "PHYSICAL_FAULT": DiagnosisLabel.PHYSICAL_FAULT,
    "NETWORK_DEGRADATION": DiagnosisLabel.NETWORK_FAULT,
    "BIAS_ATTACK": DiagnosisLabel.CYBER_ATTACK,
    "DRIFT_ATTACK": DiagnosisLabel.CYBER_ATTACK,
    "FREEZE_ATTACK": DiagnosisLabel.CYBER_ATTACK,
    "REPLAY_ATTACK": DiagnosisLabel.CYBER_ATTACK,
    "REWRITTEN_REPLAY": DiagnosisLabel.CYBER_ATTACK,
    "COMMAND_MANIPULATION": DiagnosisLabel.CYBER_ATTACK,
    "COORDINATED_ATTACK": DiagnosisLabel.CYBER_ATTACK,
    "ATTACK_PLUS_FAULT": DiagnosisLabel.CYBER_ATTACK,
    "MODEL_MISMATCH": DiagnosisLabel.MODEL_MISMATCH,
    "ATTACK_PLUS_MODEL_MISMATCH": DiagnosisLabel.CYBER_ATTACK,
    "RECOVERY": DiagnosisLabel.CYBER_ATTACK,
}


def _binary_metrics(tp, fp, tn, fn):
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    fpr = fp / (fp + tn) if fp + tn else 0.0
    return precision, recall, f1, fpr


def classification_metrics(step_results, event_family: str, cyber_families: set[str]):
    expected_cyber = event_family in cyber_families
    expected_event = event_family != "NORMAL"

    ctp = cfp = ctn = cfn = 0
    atp = afp = atn = afn = 0
    recon_errors = []
    first_anomaly = None
    diagnosis_correct = 0
    diagnosis_total = 0
    expected_label = FAMILY_TO_LABEL.get(event_family, DiagnosisLabel.UNKNOWN)

    for result in step_results:
        predicted_cyber = result.diagnosis.label == DiagnosisLabel.CYBER_ATTACK
        predicted_anomaly = result.diagnosis.label != DiagnosisLabel.NORMAL
        truth_cyber = expected_cyber and result.in_event_window
        truth_event = expected_event and result.in_event_window

        if truth_cyber and predicted_cyber: ctp += 1
        elif truth_cyber and not predicted_cyber: cfn += 1
        elif not truth_cyber and predicted_cyber: cfp += 1
        else: ctn += 1

        if truth_event and predicted_anomaly:
            atp += 1
            if first_anomaly is None:
                first_anomaly = result.t
        elif truth_event and not predicted_anomaly: afn += 1
        elif not truth_event and predicted_anomaly: afp += 1
        else: atn += 1

        if result.in_event_window:
            diagnosis_total += 1
            if result.diagnosis.label == expected_label:
                diagnosis_correct += 1

        if result.reconstructed:
            for key in result.truth:
                recon_errors.append(float(result.reconstructed[key]) - float(result.truth[key]))

    precision, recall, f1, fpr = _binary_metrics(atp, afp, atn, afn)
    cprecision, crecall, cf1, cfpr = _binary_metrics(ctp, cfp, ctn, cfn)

    delay = None
    if expected_event and first_anomaly is not None:
        start = next((r.t for r in step_results if r.in_event_window), None)
        delay = first_anomaly - start if start is not None else None

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "false_positive_rate": fpr,
        "detection_delay": delay,
        "cyber_precision": cprecision,
        "cyber_recall": crecall,
        "cyber_f1": cf1,
        "cyber_false_positive_rate": cfpr,
        "diagnosis_accuracy": diagnosis_correct / diagnosis_total if diagnosis_total else 1.0,
        "reconstruction_rmse": rmse(recon_errors),
    }
