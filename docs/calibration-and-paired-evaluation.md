# Calibration and paired evaluation

The benchmark originally reported event detection, cyber attribution, diagnosis accuracy and reconstruction error. Those metrics are necessary but do not answer two important questions:

1. **Does diagnosis confidence mean what it claims?** A classifier that is wrong at confidence 0.95 is more problematic than one that is wrong at confidence 0.55, even when their hard-label accuracy is identical.
2. **Is a candidate method consistently better on matched cases?** Aggregate means can hide that gains come from only one domain or scenario.

## Confidence calibration

`twinsec.benchmark.calibration.confidence_calibration` treats diagnosis confidence as confidence in the predicted top label and reports:

- Brier score;
- binary top-label log loss;
- expected calibration error (ECE);
- maximum calibration error (MCE);
- mean overconfidence gap;
- populated reliability bins.

The benchmark metric path evaluates the declared scenario label inside the event window and `NORMAL` outside it. This deliberately exposes confident post-event false alarms rather than hiding them behind event-window diagnosis accuracy.

These are **top-label calibration diagnostics**. The current `Diagnosis` interface exposes one confidence value rather than a full probability distribution, so these metrics must not be described as full multiclass calibration.

## Paired comparison

`twinsec.benchmark.paired.compare_paired_metric` compares aligned baseline and candidate runs. Experiment drivers must match runs by:

- domain;
- scenario;
- random seed;
- event window;
- benchmark configuration and protocol version.

The summary reports baseline and candidate means, the mean paired delta, standard error, an approximate 95% interval, and counts of improved/worsened/tied pairs. The interval uses a normal approximation over paired deltas; it is descriptive rather than a strong inferential claim for small sample counts.

For metrics such as F1, use `higher_is_better=True`. For error metrics such as reconstruction RMSE, use `higher_is_better=False`. The stored `mean_delta` always remains `candidate - baseline` so result files have stable semantics.

## Research interpretation

A candidate should not be called more trustworthy merely because its mean F1 is higher. Stronger evidence combines discrimination, calibration, reconstruction quality, false-alarm behavior, and consistency across matched domains/scenarios/seeds.

Recommended release tables therefore include both hard-label performance and confidence calibration, followed by paired deltas against the frozen baseline.
