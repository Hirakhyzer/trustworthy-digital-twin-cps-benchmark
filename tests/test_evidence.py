import unittest
from twinsec.core.models import Evidence
from twinsec.evidence.fusion import fuse

class EvidenceTests(unittest.TestCase):
    def test_fusion_bounds(self):
        score = fuse([Evidence("physics", 1.0, "x"), Evidence("temporal", 0.0, "y")])
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
