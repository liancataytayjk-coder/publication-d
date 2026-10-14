"""Check that the panel VAR recovers known coefficients and impulse responses."""

import numpy as np
import pandas as pd

from rtl.pvar import fit_pvar, irf, _fod

A_TRUE = np.array([[0.5, 0.2], [0.0, 0.3]])


def simulate(n_units=17, T=300, seed=1):
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n_units):
        fe = rng.normal(0, 1, 2)
        y = np.zeros(2)
        for t in range(T + 50):
            y = fe + A_TRUE @ y + rng.normal(0, 1, 2)
            if t >= 50:
                rows.append(dict(unit=i, t=t, x1=y[0], x2=y[1]))
    return pd.DataFrame(rows)


def test_fod_removes_constant():
    a = np.full((10, 1), 3.0)
    assert np.allclose(_fod(a)[:-1], 0)


def test_pvar_recovers_coefficients():
    # average over five simulated panels: the estimator is unbiased, single draws have SE ~0.02
    A = np.mean([fit_pvar(simulate(seed=s), ["x1", "x2"], "unit", "t", p=1)["A"][0] for s in range(5)], axis=0)
    assert np.allclose(A, A_TRUE, atol=0.03)


def test_irf_impact_is_cholesky_factor():
    res = fit_pvar(simulate(), ["x1", "x2"], "unit", "t", p=1)
    q = irf(res, H=5, draws=50)
    imp = q[(q.h == 0)].set_index(["response", "shock"]).irf
    P = np.linalg.cholesky(res["Sigma"])
    assert np.isclose(imp[("x1", "x1")], P[0, 0]) and np.isclose(imp[("x1", "x2")], 0)
    # h = 1 response of x1 to its own shock equals A[0,0] * P[0,0] + A[0,1] * P[1,0]
    h1 = q[(q.h == 1) & (q.response == "x1") & (q.shock == "x1")].irf.iloc[0]
    A = res["A"][0]
    assert np.isclose(h1, A[0, 0] * P[0, 0] + A[0, 1] * P[1, 0])
    assert (q.lo <= q.hi).all()
