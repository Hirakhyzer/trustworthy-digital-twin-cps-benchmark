# Baseline Findings

Validated locally for v0.1 with deterministic seed `7`, 180 simulation steps, seven reduced-order CPS adapters and 16 common scenario families. The full suite contains **112 domain-scenario runs**.

These numbers are **synthetic baseline outputs**, not real-world measurements and not statistical confidence estimates.

## Event detection vs cyber attribution

The benchmark deliberately separates:

1. **event/anomaly detection** — did the monitor recognize that behavior departed from the normal baseline?
2. **cyber attribution** — did the diagnosis correctly label the event as `CYBER_ATTACK` rather than fault, model mismatch or unknown?

Mean results across the seven adapters:

| Scenario | Event recall | Cyber-attribution recall |
|---|---:|---:|
| Bias attack | 1.000 | 0.266 |
| Drift attack | 0.974 | 0.291 |
| Freeze attack | 0.989 | 0.000 |
| Replay attack | 1.000 | 1.000 |
| Rewritten replay | 1.000 | 0.071 |
| Coordinated attack | 1.000 | 0.483 |
| Command manipulation | 0.960 | 0.614 |
| Attack + physical fault | 1.000 | 0.386 |
| Attack + model mismatch | 1.000 | 0.260 |

The central result is not that the framework is already a high-quality cyberattack classifier. It is that **deviation detection and root-cause attribution are different research problems**.

## Non-malicious confounders

- Normal operation produced an average event false-positive rate of approximately **0.2%**.
- Network degradation was always recognized as non-normal, but only about **40%** of event-window diagnoses were correctly labeled as `NETWORK_FAULT`.
- Model mismatch had only about **26.9%** correct attribution and created substantial post-window false alarms.
- Legitimate operational change was detected as non-normal but was not correctly attributed by the baseline classifier.
- Physical faults were detected as non-normal but were not reliably distinguished from cyber/model explanations.

## Cross-domain threshold transfer

Native normal-operation residual thresholds differ across adapters. With leave-one-domain-out mean-threshold transfer, relative threshold gaps were approximately:

- battery: **29.8%**
- water: **12.9%**
- robot: **6.4%**
- microgrid: **24.2%**
- factory: **8.1%**
- EV charging: **7.2%**
- railway: **2.5%**

This demonstrates that a single raw threshold is not automatically domain invariant. Future work should evaluate normalized representations and domain adaptation.

## Main v0.2 research targets

1. Attack-vs-fault-vs-model-mismatch discrimination.
2. Rewritten-replay attribution despite fresh metadata.
3. Freeze attribution without depending only on stale timestamps.
4. Operational-mode awareness to avoid false alarms during legitimate changes.
5. Twin-trust calibration under sustained model mismatch.
6. Multi-seed confidence intervals and statistical significance.
7. Confusion matrices and calibrated probabilistic diagnosis.
8. Cross-domain feature normalization and leave-one-domain-out generalization.

The baseline is intentionally transparent so future methods can be compared against it without hiding failure cases.
