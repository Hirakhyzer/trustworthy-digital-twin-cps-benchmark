from __future__ import annotations


def brier_score(probabilities, labels):
    pairs = list(zip(probabilities, labels))
    if not pairs:
        return 0.0
    return sum((float(p) - float(y)) ** 2 for p, y in pairs) / len(pairs)


def expected_calibration_error(probabilities, labels, bins: int = 10):
    probabilities = list(probabilities)
    labels = list(labels)
    if not probabilities:
        return 0.0
    total = len(probabilities)
    ece = 0.0
    for i in range(bins):
        lo, hi = i / bins, (i + 1) / bins
        idx = [j for j, p in enumerate(probabilities) if lo <= p < hi or (i == bins - 1 and p == 1.0)]
        if not idx:
            continue
        conf = sum(probabilities[j] for j in idx) / len(idx)
        acc = sum(labels[j] for j in idx) / len(idx)
        ece += len(idx) / total * abs(conf - acc)
    return ece
