import unittest
from twinsec.core.models import TelemetryRecord, TwinPrediction
from twinsec.resilience.reconstruction import reconstruct

class ReconstructionTests(unittest.TestCase):
    def test_low_trust_moves_toward_twin(self):
        r = TelemetryRecord("x", 0, 0, {"a": 10.0}, 0)
        p = TwinPrediction(0, {"a": 2.0}, {"a": 1.0})
        out = reconstruct(r, p, source_trust=0.1, twin_trust=0.9)
        self.assertLess(out["a"], 5.0)
