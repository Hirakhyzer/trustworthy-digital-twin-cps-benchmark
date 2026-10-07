# Trustworthy Digital-Twin CPS Benchmark

[![CI](https://github.com/Hirakhyzer/trustworthy-digital-twin-cps-benchmark/actions/workflows/ci.yml/badge.svg)](https://github.com/Hirakhyzer/trustworthy-digital-twin-cps-benchmark/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-research%20prototype-orange)

A cross-domain research framework for **trustworthy digital-twin cybersecurity in cyber-physical systems (CPS)**. The repository standardizes telemetry, attack/fault scenarios, digital-twin uncertainty, evidence fusion, trust assessment, diagnosis, state reconstruction, recovery, and benchmark metrics across heterogeneous CPS domains.

> **Research boundary:** this repository is simulation-only and defensive. It contains no operational attack payloads, credentials, vendor-specific exploitation, or instructions for targeting real infrastructure. Domain models are reduced-order research abstractions and must not be described as validated operational twins.

## Research question

**Can a domain-independent trustworthy digital-twin framework distinguish cyberattacks from physical/sensor/network faults and model mismatch across heterogeneous CPS while maintaining calibrated uncertainty and enabling resilient state reconstruction and recovery?**

## Cross-domain architecture

```text
 Battery ─┐
 Water ───┤
 Robot ───┤
 Grid ────┤
 Factory ─┤──> Common CPS / Telemetry Interface
 EV ──────┤                 |
 Railway ─┘                 v
                    Digital Twin API
                         |
        +----------------+----------------+
        |                |                |
     Physics          Temporal         Invariants
     Evidence          Evidence        / Cross-sensor
        +----------------+----------------+
                         |
                    Trust Engine
                         |
                 Uncertainty Fusion
                         |
                      Diagnosis
                         |
              +----------+----------+
              |                     |
       Source Isolation        State Reconstruction
              +----------+----------+
                         |
                  Recovery Manager
                         |
                   Domain Adapter
```

## Included domain adapters

| Adapter | Representative signals |
|---|---|
| Battery | SOC, voltage, temperature |
| Water | level, flow, pressure |
| Robot | position, velocity, range |
| Microgrid | frequency, voltage, power balance |
| Smart factory | temperature, vibration, motor current |
| EV charging | SOC, charging power, meter energy |
| Railway | position, velocity, occupancy score |

These are **benchmark profiles**, not replacements for the larger domain repositories or real engineering simulators.

## Common scenario taxonomy

`NORMAL`, `OPERATIONAL_CHANGE`, `SENSOR_FAULT`, `PHYSICAL_FAULT`, `NETWORK_DEGRADATION`, `BIAS_ATTACK`, `DRIFT_ATTACK`, `FREEZE_ATTACK`, `REPLAY_ATTACK`, `REWRITTEN_REPLAY`, `COMMAND_MANIPULATION`, `COORDINATED_ATTACK`, `ATTACK_PLUS_FAULT`, `MODEL_MISMATCH`, `ATTACK_PLUS_MODEL_MISMATCH`, and `RECOVERY`.

## Core research capabilities

- common telemetry and event schema;
- reusable reduced-order domain adapters;
- digital-twin predictions with explicit uncertainty;
- normalized physics residuals and multi-source evidence fusion;
- dynamic source trust and digital-twin trust;
- explainable diagnosis and trust-aware state reconstruction;
- native-domain and leave-one-domain-out calibration;
- event detection, cyber attribution and reconstruction metrics;
- **diagnosis-confidence calibration** with Brier score, log loss, ECE, MCE and overconfidence gap;
- **paired baseline-vs-candidate evaluation** with matched deltas and approximate confidence intervals;
- deterministic seeds and reproducibility guidance.

## Quick start

```bash
git clone https://github.com/Hirakhyzer/trustworthy-digital-twin-cps-benchmark.git
cd trustworthy-digital-twin-cps-benchmark
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
python -m unittest discover -s tests -v
python scripts/run_demo.py
python scripts/run_benchmark.py
python scripts/run_leave_one_domain_out.py
```

## Evaluation direction

The benchmark is designed to test more than raw anomaly-detection accuracy. Current evaluation supports:

1. cross-domain event detection and cyber attribution;
2. attack-vs-fault-vs-model-mismatch discrimination;
3. leave-one-domain-out threshold transfer;
4. unknown-attack evaluation;
5. source/twin trust ablation;
6. uncertainty-normalized evidence ablation;
7. recovery and reconstruction error;
8. model-mismatch stress testing;
9. diagnosis-confidence calibration;
10. paired candidate-vs-baseline comparisons across matched experiments.

A higher F1 score alone is not treated as sufficient evidence of trustworthiness. Calibration, false alarms, reconstruction quality, and consistency across domains/scenarios/seeds should be reported together. See `docs/calibration-and-paired-evaluation.md` for the new evaluation semantics.

## Scientific integrity

All baseline outputs are synthetic and configuration dependent. Do not report them as measurements from real batteries, water plants, robots, grids, factories, EV infrastructure or railway systems. Every publication should record the commit SHA, configuration, seed, scenario window, thresholds, uncertainty assumptions, adapter version, and parameter provenance.

See `docs/` for the benchmark specification, threat model, trust model, uncertainty model, evaluation protocol, reproducibility checklist, baseline findings, limitations, ethics/safety boundaries, and research roadmap.
