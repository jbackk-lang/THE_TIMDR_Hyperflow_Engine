"""
test_the_geo_pro_4d_radar.py
-----------------------------
THE_GEO_PRO_4D_Radar.py bylo kiedys niezalezna kopia tej samej logiki co
the_geo_pro_4d.py - i raz juz sie rozjechalo (patrz README, "Druga
poprawka": THE_GEO_PRO_4D_Radar dostalo poprawke bramkowania torsji
niezaleznie od the_geo_pro_4d.py). Teraz to cienki re-eksport - ten test
gwarantuje, ze to NADAL re-eksport (ten sam obiekt funkcji), nie nowa,
cicho zduplikowana implementacja, ktora moglaby znow sie rozjechac.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from the_geo_pro_4d import THE_GEO_PRO_4D
from THE_GEO_PRO_4D_Radar import THE_GEO_PRO_4D_Radar


class TestRadarIsThinReexport(unittest.TestCase):
    def test_radar_is_same_function_object(self):
        """Rdzen tego testu: identyczny OBIEKT funkcji, nie tylko 'daje
        ten sam wynik teraz' - wyklucza cicha duplikacje w przyszlosci."""
        self.assertIs(THE_GEO_PRO_4D_Radar, THE_GEO_PRO_4D)

    def test_radar_still_callable_with_required_min_speed(self):
        """Smoke test zachowania wywolania - upewnia sie, ze re-eksport
        faktycznie dziala (nie tylko istnieje jako alias)."""
        p_t3 = (0.0, 0.0, 0.0)
        p_t2 = (1.0, 0.0, 0.0)
        p_t1 = (2.0, 0.0, 0.0)
        p_t = (3.0, 0.0, 0.0)
        res = THE_GEO_PRO_4D_Radar(p_t, p_t1, p_t2, p_t3, min_speed=0.0)
        self.assertFalse(res["gated"])
        self.assertEqual(res["curvature"], 0.0)
        self.assertEqual(res["torsion"], 0.0)


if __name__ == "__main__":
    unittest.main()
