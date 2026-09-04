# Trustworthy Digital-Twin CPS Benchmark

[![CI](https://github.com/Hirakhyzer/trustworthy-digital-twin-cps-benchmark/actions/workflows/ci.yml/badge.svg)](https://github.com/Hirakhyzer/trustworthy-digital-twin-cps-benchmark/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-PhD%20research%20prototype-orange)

A cross-domain research framework for **trustworthy digital-twin cybersecurity in cyber-physical systems (CPS)**. The repository standardizes telemetry, attack/fault scenarios, digital-twin uncertainty, evidence fusion, trust assessment, diagnosis, state reconstruction, recovery, and benchmark metrics across heterogeneous CPS domains.

> **Research boundary:** this repository is simulation-only and defensive. It contains no operational attack payloads, credentials, vendor-specific exploitation, or instructions for targeting real infrastructure. Domain models are reduced-order research abstractions and must not be described as validated operational twins.

## PhD-level research question

**Can a domain-independent trustworthy digital-twin framework distinguish cyberattacks from physical/sensor/network faults and model mismatch across heterogeneous CPS, while maintaining calibrated uncertainty and enabling resilient state reconstruction and recovery?**

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
- normalized physics residuals;
- temporal freshness and sequence evidence;
- domain invariants and cross-sensor consistency;
- network-quality evidence;
- weighted multi-source evidence fusion;
- dynamic **source trust** and **digital-twin trust**;
- explainable diagnosis labels;
- trust-aware state reconstruction;
- recovery supervision;
- native-domain and leave-one-domain-out calibration;
- cross-domain benchmark metrics and report generation;
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

## Dissertation-oriented experiments

1. **Cross-domain baseline:** compare identical detector architecture across all seven adapters.
2. **Attack vs fault discrimination:** evaluate cyber, sensor, physical, network, operational-change and model-mismatch classes.
3. **Leave-one-domain-out transfer:** calibrate on six domains and evaluate the held-out seventh.
4. **Unknown attack:** calibrate using bias/freeze/replay and test on rewritten replay, drift and coordinated manipulation.
5. **Trust ablation:** source trust only vs twin trust only vs joint trust.
6. **Uncertainty ablation:** fixed thresholds vs uncertainty-normalized residuals.
7. **Recovery evaluation:** compare raw telemetry, twin-only reconstruction and trust-weighted reconstruction.
8. **Model mismatch stress test:** vary mismatch without changing attack logic.

## Scientific integrity

All baseline outputs are synthetic and configuration dependent. Do not report them as measurements from real batteries, water plants, robots, grids, factories, EV infrastructure or railway systems. Every publication should record the commit SHA, configuration, seed, scenario window, thresholds, uncertainty assumptions, adapter version, and parameter provenance.

See `docs/` for the benchmark specification, thesis alignment, threat model, trust model, uncertainty model, evaluation protocol, reproducibility checklist, baseline findings, limitations, ethics/safety boundaries, and research roadmap.
