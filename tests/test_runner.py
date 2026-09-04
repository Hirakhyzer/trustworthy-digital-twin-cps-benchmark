import unittest
from twinsec.benchmark.runner import BenchmarkRunner
from twinsec.benchmark.scenarios import DEFAULT_SCENARIOS

class RunnerTests(unittest.TestCase):
    def test_normal_scenario_runs(self):
        runner = BenchmarkRunner(seed=7, steps=80)
        scenario = next(s for s in DEFAULT_SCENARIOS if s.name == "normal")
        results, metrics = runner.run("water", scenario)
        self.assertEqual(len(results), 80)
        self.assertEqual(metrics["domain"], "water")

    def test_bias_attack_has_nonzero_recall(self):
        runner = BenchmarkRunner(seed=7, steps=150)
        scenario = next(s for s in DEFAULT_SCENARIOS if s.name == "bias_attack")
        _, metrics = runner.run("factory", scenario)
        self.assertGreater(metrics["recall"], 0.0)
