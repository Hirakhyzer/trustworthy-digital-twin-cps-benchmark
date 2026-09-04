from twinsec.benchmark.runner import BenchmarkRunner
from twinsec.benchmark.scenarios import DEFAULT_SCENARIOS

runner = BenchmarkRunner(seed=7, steps=180)
for name in ("bias_attack", "freeze_attack", "rewritten_replay", "coordinated_attack"):
    scenario = next(s for s in DEFAULT_SCENARIOS if s.name == name)
    _, m = runner.run("railway", scenario)
    print(
        name,
        "event_recall=", round(m["recall"], 3),
        "cyber_attribution_recall=", round(m["cyber_recall"], 3),
        "f1=", round(m["f1"], 3),
    )
