import unittest
from twinsec.trust.calibration import brier_score, expected_calibration_error

class CalibrationTests(unittest.TestCase):
    def test_perfect_calibration_scores(self):
        self.assertAlmostEqual(brier_score([0.0, 1.0], [0, 1]), 0.0)
        self.assertAlmostEqual(expected_calibration_error([0.0, 1.0], [0, 1]), 0.0)
