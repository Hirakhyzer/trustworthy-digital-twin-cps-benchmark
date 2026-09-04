# Trust Model

The benchmark maintains two distinct quantities:

- **source trust:** confidence in a telemetry source;
- **twin trust:** confidence in the digital-twin prediction.

Source trust decreases when fused evidence is persistently anomalous and recovers slowly during consistent operation. Twin trust can decrease when residual behavior is more consistent with model mismatch than with source inconsistency.

Future experiments should evaluate calibration using Brier score and expected calibration error rather than treating raw trust values as probabilities without validation.
