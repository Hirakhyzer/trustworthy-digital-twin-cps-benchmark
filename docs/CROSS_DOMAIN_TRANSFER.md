# Cross-Domain Transfer

The benchmark includes leave-one-domain-out threshold transfer.

For each held-out domain:
1. calibrate on the other six domains;
2. aggregate the training-domain thresholds;
3. apply the transferred threshold to the unseen domain;
4. compare with that domain's native calibration.

This v0.1 experiment is intentionally simple. Future work should compare feature normalization, representation learning, domain adaptation and invariant-based transfer while preventing target-domain leakage.
