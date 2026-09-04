import unittest
from twinsec.trust.source import SourceTrust

class TrustTests(unittest.TestCase):
    def test_trust_falls_under_anomaly(self):
        t = SourceTrust()
        before = t.value
        t.update(0.9)
        self.assertLess(t.value, before)
