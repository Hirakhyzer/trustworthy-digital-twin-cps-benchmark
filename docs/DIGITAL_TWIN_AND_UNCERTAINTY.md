# Digital Twin and Uncertainty

The baseline twin is deliberately transparent and reduced-order.

For telemetry \(y_k\), prediction \(\hat y_k\), measurement uncertainty \(\sigma_y\) and twin uncertainty \(\sigma_{DT}\), a future full implementation should evaluate:

\[
z_k = \frac{y_k-\hat y_k}{\sqrt{\sigma_y^2+\sigma_{DT}^2}}
\]

The current baseline represents uncertainty per signal and uses it to normalize residuals. Future work should add online uncertainty calibration, estimator covariance, parameter uncertainty and empirical coverage tests.

The twin is **not ground truth**. Its trust is tracked separately from telemetry trust.
