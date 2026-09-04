# Diagnosis and Explainability

Baseline labels:

`NORMAL`, `CYBER_ATTACK`, `SENSOR_FAULT`, `PHYSICAL_FAULT`, `NETWORK_FAULT`, `MODEL_MISMATCH`, `OPERATIONAL_CHANGE`, and `UNKNOWN`.

Every diagnosis retains its evidence channels, scores and human-readable reasons. This supports explanations such as:

- temporal metadata strongly inconsistent;
- physics residual exceeds calibrated threshold;
- invariant violation localized to one source;
- network delivery degraded while physics remains plausible.

The baseline classifier is heuristic by design. It is an interpretable reference method, not a claim of optimal classification.
