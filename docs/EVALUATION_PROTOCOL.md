# Evaluation Protocol

Report at minimum:

## Detection
precision, recall, F1, false-positive rate, detection delay.

## Diagnosis
confusion matrix and per-class precision/recall for cyber, sensor fault, physical fault, network fault, model mismatch, operational change and unknown.

## Twin / reconstruction
prediction RMSE, reconstruction RMSE and uncertainty coverage.

## Trust
Brier score, expected calibration error and trust trajectories.

## Generalization
leave-one-domain-out degradation relative to native-domain calibration.

Use multiple random seeds and confidence intervals before making scientific claims. The deterministic seed in v0.1 is for software regression and reproducibility, not statistical significance.
