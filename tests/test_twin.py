import unittest
from twinsec.domains.registry import make_domain
from twinsec.twin.base import DigitalTwin

class TwinTests(unittest.TestCase):
    def test_prediction_schema(self):
        d = make_domain("battery")
        twin = DigitalTwin(d.profile)
        p = twin.predict(0, d.control(0))
        self.assertEqual(set(p.values), set(d.profile.signals))
        self.assertTrue(all(v > 0 for v in p.uncertainty.values()))
