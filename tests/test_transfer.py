import unittest
from twinsec.benchmark.runner import BenchmarkRunner
from twinsec.benchmark.transfer import leave_one_domain_out_thresholds

class TransferTests(unittest.TestCase):
    def test_all_domains_have_transfer_threshold(self):
        out = leave_one_domain_out_thresholds(BenchmarkRunner(seed=7, steps=90))
        self.assertEqual(len(out), 7)
        self.assertTrue(all(v > 0 for v in out.values()))
