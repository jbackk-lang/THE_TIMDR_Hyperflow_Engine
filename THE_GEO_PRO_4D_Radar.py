"""
THE_GEO_PRO_4D_Radar.py
-----------------------
Cienki re-eksport `the_geo_pro_4d.THE_GEO_PRO_4D` pod nazwą użytą w
pierwotnym pseudokodzie ("...Radar"), żeby NIE było drugiej, niezależnej
kopii tej samej logiki geometrycznej.

Dlaczego to ma znaczenie: wcześniej ten plik miał WŁASNĄ, zduplikowaną
implementację — treściowo identyczną z `the_geo_pro_4d.py` (dwa niezależne
kopiuj-wklej tego samego wzoru), ale bez wspólnego źródła prawdy. Historia
tego repo (README.md, sekcja "Druga poprawka") już opisuje, że ten
konkretny plik raz dostał poprawkę bramkowania torsji (na `kappa` zamiast
`cross_norm == 0`) niezależnie od `the_geo_pro_4d.py` — czyli dokładnie ten
mechanizm rozjazdu (dwie kopie, jedna naprawiona, druga nie) już się tu
raz zdarzył. Re-eksport eliminuje możliwość, żeby zdarzył się ponownie:
jest teraz JEDNO miejsce z implementacją (`the_geo_pro_4d.py`), a ten plik
tylko je re-eksportuje pod historyczną nazwą.

Test regresyjny na tożsamość funkcji:
`tests/test_the_geo_pro_4d_radar.py::test_radar_is_same_function_object`.

Drobna, jawna zmiana zachowania: poprzednio `min_speed` było tu
wymagane (brak wartości domyślnej), teraz — jako że to ten sam obiekt
funkcji co `THE_GEO_PRO_4D` — ma domyślną wartość 1.0
(`the_geo_pro_4d.DEFAULT_MIN_SPEED`). Wywołania z jawnym `min_speed=...`
działają bez zmian.
"""

from the_geo_pro_4d import THE_GEO_PRO_4D as THE_GEO_PRO_4D_Radar
from the_geo_pro_4d import DEFAULT_MIN_CURVATURE

__all__ = ["THE_GEO_PRO_4D_Radar", "DEFAULT_MIN_CURVATURE"]
