import unittest
from twinsec.core.models import TelemetryRecord
from twinsec.attacks.manipulations import bias, replay

class AttackTests(unittest.TestCase):
    def test_bias_is_in_memory_only(self):
        r = TelemetryRecord("x", 1.0, 1, {"a": 2.0}, 1.0)
        m = bias(r, "a", 3.0)
        self.assertEqual(r.values["a"], 2.0)
        self.assertEqual(m.values["a"], 5.0)

    def test_rewritten_replay_preserves_current_metadata(self):
        current = TelemetryRecord("x", 10.0, 10, {"a": 10.0}, 10.0)
        old = TelemetryRecord("x", 3.0, 3, {"a": 3.0}, 3.0)
        m = replay(current, old, rewrite_metadata=True)
        self.assertEqual(m.timestamp, 10.0)
        self.assertEqual(m.sequence, 10)
        self.assertEqual(m.values["a"], 3.0)
