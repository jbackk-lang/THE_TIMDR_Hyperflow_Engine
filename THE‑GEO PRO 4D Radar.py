def THE_GEO_PRO_4D_Radar(p_t, p_t1, p_t2, p_t3, min_speed):

    # prędkość
    v  = p_t  - p_t1
    v1 = p_t1 - p_t2

    # przyspieszenie
    a  = v  - v1
    a1 = v1 - (p_t2 - p_t3)

    # szarpnięcie
    j = a - a1

    speed = norm(v)

    # bramkowanie
    if speed < min_speed:
        return {
            "gated": True,
            "curvature": 0.0,
            "torsion": 0.0,
            "helical": 0.0
        }

    # krzywizna
    cross_va = cross(v, a)
    cross_norm = norm(cross_va)

    if cross_norm == 0:
        return {
            "gated": False,
            "curvature": 0.0,
            "torsion": 0.0,
            "helical": 0.0
        }

    kappa = cross_norm / (speed**3)

    # torsja
    tau = det(v, a, j) / (cross_norm**2)

    # helikalność
    H = sqrt(kappa*kappa + tau*tau)

    return {
        "gated": False,
        "curvature": kappa,
        "torsion": tau,
        "helical": H
    }
