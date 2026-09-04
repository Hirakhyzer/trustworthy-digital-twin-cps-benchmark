def should_isolate(source_trust: float, anomaly_score: float) -> bool:
    return source_trust < 0.35 and anomaly_score >= 0.45
