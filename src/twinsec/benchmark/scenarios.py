from __future__ import annotations

from twinsec.core.models import Scenario


DEFAULT_SCENARIOS = (
    Scenario("normal", "NORMAL"),
    Scenario("operational_change", "OPERATIONAL_CHANGE", magnitude=0.55),
    Scenario("sensor_fault", "SENSOR_FAULT", magnitude=1.6),
    Scenario("physical_fault", "PHYSICAL_FAULT", magnitude=1.0),
    Scenario("network_degradation", "NETWORK_DEGRADATION", magnitude=1.0),
    Scenario("bias_attack", "BIAS_ATTACK", magnitude=2.2),
    Scenario("drift_attack", "DRIFT_ATTACK", magnitude=2.4),
    Scenario("freeze_attack", "FREEZE_ATTACK", magnitude=1.0),
    Scenario("replay_attack", "REPLAY_ATTACK", magnitude=1.0),
    Scenario("rewritten_replay", "REWRITTEN_REPLAY", magnitude=1.0),
    Scenario("command_manipulation", "COMMAND_MANIPULATION", magnitude=0.55),
    Scenario("coordinated_attack", "COORDINATED_ATTACK", magnitude=1.3),
    Scenario("attack_plus_fault", "ATTACK_PLUS_FAULT", magnitude=1.8),
    Scenario("model_mismatch", "MODEL_MISMATCH", magnitude=0.18),
    Scenario("attack_plus_model_mismatch", "ATTACK_PLUS_MODEL_MISMATCH", magnitude=2.0),
    Scenario("recovery", "RECOVERY", start=65, end=105, magnitude=2.2),
)

CYBER_FAMILIES = {
    "BIAS_ATTACK", "DRIFT_ATTACK", "FREEZE_ATTACK", "REPLAY_ATTACK",
    "REWRITTEN_REPLAY", "COMMAND_MANIPULATION", "COORDINATED_ATTACK",
    "ATTACK_PLUS_FAULT", "ATTACK_PLUS_MODEL_MISMATCH", "RECOVERY",
}
