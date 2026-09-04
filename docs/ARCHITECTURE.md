# Architecture

The framework separates **domain semantics** from **security reasoning**.

Each domain adapter exposes a common reduced-order plant plus named telemetry signals. The twin produces a prediction and uncertainty for those same signals. Evidence modules evaluate physics residuals, temporal freshness, cross-sensor consistency, invariants and network quality. Trust and diagnosis are domain-independent; recovery uses a generic reconstruction interface before a domain adapter would map the result to its own safe action.

This separation is the principal software-architecture hypothesis of the project: security reasoning should be reusable across heterogeneous CPS while domain adapters retain physical meaning.
