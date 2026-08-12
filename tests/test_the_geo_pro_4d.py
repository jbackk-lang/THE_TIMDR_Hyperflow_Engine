"""
test_the_geo_pro_4d.py
-----------------------
Testy dla the_geo_pro_4d.py:
  - zbieznosc kappa/tau do wartosci analitycznych na helisie,
  - brak dzielenia przez zero na linii prostej,
  - bramkowanie min_speed,
  - niezmienniczosc na obrot 3D (dowolna os, wzor Rodriguesa).
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from the_geo_pro_4d import THE_GEO_PRO_4D


def helix_point(t, r=5.0, c=1.0):
    return (r * math.cos(t), r * math.sin(t), c * t)


def analytical_kappa_tau(r=5.0, c=1.0):
    denom = r * r + c * c
    return r / denom, c / denom


class TestHelixConvergence(unittest.TestCase):
    def _run(self, dt, r=5.0, c=1.0, t0=2.0):
        pts = [helix_point(t0 + k * dt, r, c) for k in range(4)]
        p_t3, p_t2, p_t1, p_t = pts
        return THE_GEO_PRO_4D(p_t, p_t1, p_t2, p_t3, min_speed=0.0)

    def test_converges_as_dt_shrinks(self):
        r, c = 5.0, 1.0
        kappa_true, tau_true = analytical_kappa_tau(r, c)
        errors = []
        for dt in (0.5, 0.1, 0.02, 0.01):
            res = self._run(dt, r, c)
            err_k = abs(res["curvature"] - kappa_true) / kappa_true
            err_t = abs(res["torsion"] - tau_true) / tau_true
            errors.append((err_k, err_t))
        for i in range(1, len(errors)):
            self.assertLess(errors[i][0], errors[i - 1][0])
            self.assertLess(errors[i][1], errors[i - 1][1])
        self.assertLess(errors[-1][0], 0.01)
        self.assertLess(errors[-1][1], 0.01)

    def test_helical_matches_sqrt_kappa2_tau2(self):
        res = self._run(0.05)
        expected_H = math.sqrt(res["curvature"] ** 2 + res["torsion"] ** 2)
        self.assertAlmostEqual(res["helical"], expected_H, places=9)


class TestStraightLineNoDivByZero(unittest.TestCase):
    def test_straight_line_zero_curvature_zero_torsion(self):
        p_t3 = (0.0, 0.0, 0.0)
        p_t2 = (1.0, 1.0, 1.0)
        p_t1 = (2.0, 2.0, 2.0)
        p_t = (3.0, 3.0, 3.0)
        res = THE_GEO_PRO_4D(p_t, p_t1, p_t2, p_t3, min_speed=0.0)
        self.assertFalse(res["gated"])
        self.assertEqual(res["curvature"], 0.0)
        self.assertEqual(res["torsion"], 0.0)
        self.assertEqual(res["helical"], 0.0)


class TestMinSpeedGating(unittest.TestCase):
    def test_gated_when_below_min_speed(self):
        pts = [(0.0, 0.0, 0.0)] * 4
        p_t3, p_t2, p_t1, p_t = pts
        res = THE_GEO_PRO_4D(p_t, p_t1, p_t2, p_t3, min_speed=1.0)
        self.assertTrue(res["gated"])
        self.assertEqual(res["curvature"], 0.0)
        self.assertEqual(res["torsion"], 0.0)
        self.assertEqual(res["helical"], 0.0)

    def test_not_gated_when_above_min_speed(self):
        r, c = 5.0, 1.0
        pts = [helix_point(2.0 + k * 0.05, r, c) for k in range(4)]
        p_t3, p_t2, p_t1, p_t = pts
        res = THE_GEO_PRO_4D(p_t, p_t1, p_t2, p_t3, min_speed=0.1)
        self.assertFalse(res["gated"])


class TestRotationInvariance(unittest.TestCase):
    @staticmethod
    def _rotation_matrix(axis, angle):
        n = math.sqrt(sum(x * x for x in axis))
        x, y, z = (a / n for a in axis)
        c, s = math.cos(angle), math.sin(angle)
        C = 1 - c
        return (
            (x * x * C + c, x * y * C - z * s, x * z * C + y * s),
            (y * x * C + z * s, y * y * C + c, y * z * C - x * s),
            (z * x * C - y * s, z * y * C + x * s, z * z * C + c),
        )

    @staticmethod
    def _apply(mat, p):
        return (
            mat[0][0] * p[0] + mat[0][1] * p[1] + mat[0][2] * p[2],
            mat[1][0] * p[0] + mat[1][1] * p[1] + mat[1][2] * p[2],
            mat[2][0] * p[0] + mat[2][1] * p[1] + mat[2][2] * p[2],
        )

    def test_curvature_torsion_invariant_under_rotation(self):
        r, c = 4.0, 0.7
        pts = [helix_point(1.0 + k * 0.05, r, c) for k in range(4)]
        p_t3, p_t2, p_t1, p_t = pts
        res_before = THE_GEO_PRO_4D(p_t, p_t1, p_t2, p_t3, min_speed=0.0)

        mat = self._rotation_matrix((1, 1, 1), 0.9)
        rp_t3, rp_t2, rp_t1, rp_t = (self._apply(mat, p) for p in pts)
        res_after = THE_GEO_PRO_4D(rp_t, rp_t1, rp_t2, rp_t3, min_speed=0.0)

        self.assertAlmostEqual(res_before["curvature"], res_after["curvature"], places=9)
        self.assertAlmostEqual(res_before["torsion"], res_after["torsion"], places=9)


if __name__ == "__main__":
    unittest.main()
