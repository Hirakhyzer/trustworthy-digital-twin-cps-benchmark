from twinsec.benchmark.runner import BenchmarkRunner
from twinsec.benchmark.scenarios import DEFAULT_SCENARIOS
from twinsec.diagnosis.root_cause import explain

runner = BenchmarkRunner(seed=7, steps=150)
scenario = next(s for s in DEFAULT_SCENARIOS if s.name == "bias_attack")
results, metrics = runner.run("battery", scenario)
print("Metrics:", metrics)
alarm = next((r for r in results if r.diagnosis.label.value != "NORMAL"), None)
if alarm:
    print("First non-normal diagnosis:", explain(alarm.diagnosis))
