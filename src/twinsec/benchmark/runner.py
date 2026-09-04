from __future__ import annotations

import random
from dataclasses import replace

from twinsec.attacks.manipulations import bias, coordinated, drift, freeze, replay
from twinsec.benchmark.metrics import classification_metrics
from twinsec.benchmark.scenarios import CYBER_FAMILIES, DEFAULT_SCENARIOS
from twinsec.core.models import StepResult, TelemetryRecord
from twinsec.domains.registry import DOMAIN_PROFILES, make_domain
from twinsec.evidence.cross_sensor import cross_sensor_evidence
from twinsec.evidence.fusion import fuse
from twinsec.evidence.invariant import invariant_evidence
from twinsec.evidence.network import network_evidence
from twinsec.evidence.physics import physics_evidence
from twinsec.evidence.temporal import temporal_evidence
from twinsec.diagnosis.classifier import diagnose
from twinsec.resilience.reconstruction import reconstruct
from twinsec.trust.source import SourceTrust
from twinsec.trust.twin import TwinTrust
from twinsec.twin.base import DigitalTwin
from twinsec.twin.calibration import calibrate_residual_threshold
from twinsec.twin.residuals import residual_score


class BenchmarkRunner:
    def __init__(self, seed: int = 7, steps: int = 180):
        self.seed = seed
        self.steps = steps

    def _record(self, domain, truth, t, delay=0.0):
        noise_rng = random.Random(self.seed * 10000 + t * 97 + sum(map(ord, domain.profile.name)))
        values = {}
        for key, value, sigma in zip(domain.profile.signals, truth.values(), domain.profile.noise):
            values[key] = float(value) + noise_rng.gauss(0.0, sigma)
        return TelemetryRecord(
            source=f"{domain.profile.name}.telemetry",
            timestamp=float(t),
            sequence=t,
            values=values,
            delivered_at=float(t) + delay,
        )

    def calibrate_domain(self, domain_name: str, steps: int = 70):
        domain = make_domain(domain_name, self.seed)
        twin = DigitalTwin(domain.profile)
        scores = []
        for t in range(steps):
            control = domain.control(t)
            truth = domain.step(t)
            record = self._record(domain, truth, t)
            pred = twin.predict(t, control)
            scores.append(residual_score(record, pred))
        return calibrate_residual_threshold(scores)

    def run(self, domain_name: str, scenario, threshold: float | None = None):
        domain = make_domain(domain_name, self.seed)
        mismatch = scenario.magnitude if scenario.family == "MODEL_MISMATCH" else (
            0.15 if scenario.family == "ATTACK_PLUS_MODEL_MISMATCH" else 0.0
        )
        twin = DigitalTwin(domain.profile, mismatch=mismatch)
        source_trust = SourceTrust()
        twin_trust = TwinTrust()
        threshold = threshold if threshold is not None else self.calibrate_domain(domain_name)
        history = []
        results = []
        last_good = None

        for t in range(self.steps):
            in_window = scenario.start <= t < scenario.end
            family = scenario.family
            physical_fault = in_window and family in {"PHYSICAL_FAULT", "ATTACK_PLUS_FAULT"}
            command_scale = scenario.magnitude if in_window and family == "COMMAND_MANIPULATION" else 1.0
            if in_window and family == "OPERATIONAL_CHANGE":
                command_scale = 1.0 + scenario.magnitude

            control = domain.control(t)
            truth = domain.step(t, physical_fault=physical_fault, command_scale=command_scale)
            delay = 0.0
            packet_loss = False
            if in_window and family == "NETWORK_DEGRADATION":
                delay = 5.0 if t % 4 else 8.0
                packet_loss = (t % 5 == 0)

            record = None if packet_loss else self._record(domain, truth, t, delay=delay)
            prediction = twin.predict(t, control)

            if record is not None and in_window:
                key = domain.profile.signals[scenario.target_index]
                span = max(domain.profile.plausible_max[scenario.target_index] - domain.profile.plausible_min[scenario.target_index], 1.0)
                amount = scenario.magnitude * max(domain.profile.uncertainty[scenario.target_index] * 4.5, span * 0.015)
                if family in {"BIAS_ATTACK", "ATTACK_PLUS_MODEL_MISMATCH", "RECOVERY"}:
                    record = bias(record, key, amount)
                elif family == "SENSOR_FAULT":
                    record = bias(record, key, amount * 0.65)
                elif family == "DRIFT_ATTACK":
                    progress = (t - scenario.start + 1) / max(1, scenario.end - scenario.start)
                    record = drift(record, key, amount, progress)
                elif family == "FREEZE_ATTACK" and last_good is not None:
                    record = freeze(record, last_good)
                elif family in {"REPLAY_ATTACK", "REWRITTEN_REPLAY"} and history:
                    old = history[max(0, len(history) - 12)]
                    record = replay(record, old, rewrite_metadata=(family == "REWRITTEN_REPLAY"))
                elif family == "COORDINATED_ATTACK":
                    record = coordinated(record, amount * 0.35)
                elif family == "ATTACK_PLUS_FAULT":
                    record = bias(record, key, amount)

            evidence = []
            if record is None:
                evidence.append(network_evidence(None, t))
            else:
                evidence.extend([
                    physics_evidence(record, prediction, threshold),
                    temporal_evidence(record, t, t),
                    invariant_evidence(domain.profile, record),
                    cross_sensor_evidence(domain.profile, record),
                    network_evidence(record, t),
                ])
            anomaly = fuse(evidence)
            s_trust = source_trust.update(anomaly)
            p_score = next((e.score for e in evidence if e.channel == "physics"), 0.0)
            i_score = next((e.score for e in evidence if e.channel == "invariant"), 0.0)
            t_trust = twin_trust.update(p_score, i_score, mismatch)
            diag = diagnose(evidence, source=f"{domain_name}.telemetry")
            reconstructed = reconstruct(record, prediction, s_trust, t_trust)

            results.append(StepResult(
                t=t,
                truth=dict(truth),
                telemetry=record,
                prediction=prediction,
                diagnosis=diag,
                source_trust=s_trust,
                twin_trust=t_trust,
                reconstructed=reconstructed,
                in_event_window=in_window,
            ))
            if record is not None:
                history.append(record)
                if family != "FREEZE_ATTACK" or not in_window:
                    last_good = record

        metrics = classification_metrics(results, scenario.family, CYBER_FAMILIES)
        metrics.update({
            "domain": domain_name,
            "scenario": scenario.name,
            "family": scenario.family,
            "threshold": threshold,
            "final_source_trust": results[-1].source_trust,
            "final_twin_trust": results[-1].twin_trust,
        })
        return results, metrics

    def run_suite(self, domains=None, scenarios=None):
        domains = domains or list(DOMAIN_PROFILES)
        scenarios = scenarios or DEFAULT_SCENARIOS
        rows = []
        for domain_name in domains:
            threshold = self.calibrate_domain(domain_name)
            for scenario in scenarios:
                _, metrics = self.run(domain_name, scenario, threshold=threshold)
                rows.append(metrics)
        return rows
