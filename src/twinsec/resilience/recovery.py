def recovered(source_trust: float, anomaly_score: float) -> bool:
    return source_trust > 0.70 and anomaly_score < 0.25
