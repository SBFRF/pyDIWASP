import unittest
import numpy as np
from infospec import compangle
from private.hsig import hsig
from private.check_data import check_data


class TestCoreFunctions(unittest.TestCase):
    def test_hsig_calculates_significant_wave_height(self):
        freqs = np.array([1.0, 2.0])
        dirs = np.array([0.0, np.pi / 2])
        S = np.ones((2, 2))
        SM = {"freqs": freqs, "dirs": dirs, "S": S}

        result = hsig(SM)

        expected = 4 * np.sqrt(
            np.sum(S) * (freqs[1] - freqs[0]) * (dirs[1] - dirs[0])
        )
        self.assertAlmostEqual(result, expected)

    def test_compangle_converts_to_compass_bearing(self):
        angle = 90
        xaxisdir = 90

        result = compangle(angle, xaxisdir)

        self.assertEqual(result, 180)

    def test_check_data_enforces_minimum_resolution(self):
        ep = {"dres": 5, "nfft": 32, "iter": 10, "smooth": "off", "method": "IMLM"}

        validated = check_data(ep, 3)

        self.assertEqual(validated["dres"], 10)
        self.assertEqual(validated["nfft"], 64)
        self.assertEqual(validated["iter"], 10)
        self.assertEqual(validated["smooth"], "off")
        self.assertEqual(validated["method"], "IMLM")


if __name__ == "__main__":
    unittest.main()
