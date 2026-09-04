import unittest

from twinsec.benchmark.runner import BenchmarkRunner
from twinsec.benchmark.scenarios import DEFAULT_SCENARIOS
from twinsec.benchmark.transfer import leave_one_domain_out_thresholds


class ResearchBaselineTests(unittest.TestCase):
    def setUp(self):
        self.runner = BenchmarkRunner(seed=7, steps=180)

    def scenario(self, name):
        return next(s for s in DEFAULT_SCENARIOS if s.name == name)

    def test_normal_false_positive_rate_is_low(self):
        _, metrics = self.runner.run("railway", self.scenario("normal"))
        self.assertLess(metrics["false_positive_rate"], 0.05)

    def test_plain_replay_is_attributed(self):
        _, metrics = self.runner.run("railway", self.scenario("replay_attack"))
        self.assertGreater(metrics["cyber_recall"], 0.80)

    def test_rewritten_replay_exposes_attribution_gap(self):
        _, metrics = self.runner.run("railway", self.scenario("rewritten_replay"))
        self.assertGreater(metrics["recall"], 0.80)
        self.assertLess(metrics["cyber_recall"], 0.40)

    def test_native_thresholds_are_not_identical(self):
        values = [self.runner.calibrate_domain(d) for d in (
            "battery","water","robot","microgrid","factory","ev_charging","railway"
        )]
        self.assertGreater(max(values) - min(values), 0.10)


if __name__ == "__main__":
    unittest.main()
