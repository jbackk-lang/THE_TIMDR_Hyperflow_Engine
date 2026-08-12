"""
the_geo_pro_4d.py
------------------
Prawdziwa (nie pseudokodowa) implementacja THE-GEO PRO 4D.

Kontekst / historia poprawek — patrz README.md, sekcja
"THE-GEO PRO -> THE-GEO PRO 4D: historia walidacji":

  1. Oryginalny wzor na skret w tym repo (Torsion.compute w sekcji
     "THE-GEO PRO" nizej w README), oparty na roznicach KIERUNKOW
     jednostkowych (D_t2, D_t1, D_t), zostal sprawdzony na czystej,
     bezszumowej helisie analitycznej i NIE zbiega do prawdziwej
     torsji -- blad zostaje na poziomie 90-99% nawet przy zageszczaniu
     probkowania (dt = 0.5 .. 0.005).

  2. Ten plik implementuje poprawiona wersje ("4D" = pozycje
     parametryzowane czasem t jako 4. wspolrzedna krzywej). Krzywizna
     i skret sa liczone z pochodnych predkosci / przyspieszenia /
     szarpniecia (v, a, j) wyliczonych roznicami skonczonymi z 4
     kolejnych punktow:

         kappa = |v x a| / |v|^3
         tau   = det(v, a, j) / |v x a|^2
         H     = sqrt(kappa^2 + tau^2)      (helikalnosc)

     Zbiega poprawnie do wartosci analitycznych (patrz testy i README).

  3. Implementacja jest matematycznie identyczna z
     FLIGHT-TRACKING-TIMDR/core/curvature_detector_3d.py (sprawdzone
     numerycznie -- wyniki v/a/j bit-identyczne dla tych samych
     wejsc). Rozni sie tylko interfejsem: zwraca dict zgodny z
     oryginalnym pseudokodem THE-GEO PRO 4D i dodatkowo liczy
     "helical".

  4. Poprawka wzgledem pseudokodu uzytkownika: dodano zabezpieczenie
     przed dzieleniem przez zero, gdy v i a sa rownolegle (linia
     prosta) -- wtedy cross_norm ~ 0, wiec kappa = tau = 0 zamiast
     ZeroDivisionError / NaN.

Wejscie: p_t, p_t1, p_t2, p_t3 -- krotki (x, y, z). p_t = pozycja
najnowsza, p_t3 = pozycja sprzed 3 krokow (najstarsza).
"""

import math
from typing import Dict, Tuple

Point3 = Tuple[float, float, float]

DEFAULT_MIN_SPEED = 1.0


def _sub(a: Point3, b: Point3) -> Point3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _norm(v: Point3) -> float:
    return math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)


def _cross(a: Point3, b: Point3) -> Point3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _dot(a: Point3, b: Point3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def THE_GEO_PRO_4D(
    p_t: Point3,
    p_t1: Point3,
    p_t2: Point3,
    p_t3: Point3,
    min_speed: float = DEFAULT_MIN_SPEED,
) -> Dict[str, float]:
    """Krzywizna, skret i helikalnosc trajektorii 3D sparametryzowanej czasem.

    Zwraca dict: {"gated", "curvature", "torsion", "helical"}.
    gated=True gdy predkosc ponizej min_speed (szum GPS/sensora przy
    postoju) -- wtedy pozostale pola sa wyzerowane, zeby nie wzmacniac
    szumu przy dzieleniu przez mala predkosc.
    """
    v = _sub(p_t, p_t1)
    v1 = _sub(p_t1, p_t2)
    a = _sub(v, v1)
    a1 = _sub(v1, _sub(p_t2, p_t3))
    j = _sub(a, a1)

    speed = _norm(v)
    if speed < min_speed:
        return {"gated": True, "curvature": 0.0, "torsion": 0.0, "helical": 0.0}

    cross_va = _cross(v, a)
    cross_norm = _norm(cross_va)

    if cross_norm < 1e-12:
        # v i a rownolegle (linia prosta) -- krzywizna 0, skret nieokreslony -> 0
        kappa = 0.0
        tau = 0.0
    else:
        kappa = cross_norm / speed ** 3
        tau = _dot(cross_va, j) / cross_norm ** 2

    H = math.sqrt(kappa * kappa + tau * tau)

    return {"gated": False, "curvature": kappa, "torsion": tau, "helical": H}
