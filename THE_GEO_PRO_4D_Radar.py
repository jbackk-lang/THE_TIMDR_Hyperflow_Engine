"""
THE_GEO_PRO_4D_Radar.py
------------------------
Poprawiona wersja pliku "THE-GEO PRO 4D Radar" -- oryginalnie wklejony
tu jako pseudokod (uzywal niezdefiniowanych norm/cross/det, wiec nie
dalby sie uruchomic) i zawieral ten sam blad co druga poprawka opisana
w README.md ("Druga poprawka: bramkowanie oparte na cross_norm==0 nie
wystarcza"): `if cross_norm == 0` chroni tylko przed dzieleniem przez
doslowne zero, nie przed wzmocnieniem szumu, gdy trajektoria jest
niemal (ale nie dokladnie) prosta -- np. cross_norm=1e-6 przechodzi
przez ten warunek i daje torsje rzedu 1e6 zamiast ~0.

Ta wersja jest funkcjonalnie identyczna z the_geo_pro_4d.py w tym repo
(patrz tam pelna historia walidacji i testy) -- prawdziwy, uruchamialny
kod Python z poprawionym bramkowaniem torsji na podstawie krzywizny
kappa zamiast samego cross_norm.
"""

import math
from typing import Dict, Tuple

Point3 = Tuple[float, float, float]

DEFAULT_MIN_CURVATURE = 1e-4


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


def THE_GEO_PRO_4D_Radar(
    p_t: Point3,
    p_t1: Point3,
    p_t2: Point3,
    p_t3: Point3,
    min_speed: float,
    min_curvature: float = DEFAULT_MIN_CURVATURE,
) -> Dict[str, float]:
    # predkosc
    v = _sub(p_t, p_t1)
    v1 = _sub(p_t1, p_t2)

    # przyspieszenie
    a = _sub(v, v1)
    a1 = _sub(v1, _sub(p_t2, p_t3))

    # szarpniecie
    j = _sub(a, a1)

    speed = _norm(v)

    # bramkowanie predkosci -- przy postoju/wolnym ruchu szum czujnika
    # jest wzmacniany przez dzielenie przez |v|^3
    if speed < min_speed:
        return {"gated": True, "curvature": 0.0, "torsion": 0.0, "helical": 0.0}

    # krzywizna
    cross_va = _cross(v, a)
    cross_norm = _norm(cross_va)
    kappa = cross_norm / speed ** 3

    # bramkowanie torsji -- POPRAWKA: na podstawie kappa, nie
    # "if cross_norm == 0" (ktore lapie tylko doslowne zero, nie male
    # nie-zerowe wartosci wynikajace z szumu na niemal prostym torze)
    if kappa < min_curvature:
        tau = 0.0
    else:
        tau = _dot(cross_va, j) / cross_norm ** 2

    # helikalnosc
    H = math.sqrt(kappa * kappa + tau * tau)

    return {"gated": False, "curvature": kappa, "torsion": tau, "helical": H}
