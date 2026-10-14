"""Panel vector autoregression as in Love and Zicchino (2006) and Abrigo and Love (2016).

Fixed effects are removed with forward orthogonal deviations (the Helmert
transformation): each observation is replaced by its scaled deviation from the mean of
all *future* observations of the same unit, so the transformed error stays
uncorrelated with past values. The transformed lags are then instrumented with the
untransformed lags (just-identified GMM, which equals two-stage least squares).
Orthogonalized impulse responses use the Cholesky factor of the residual covariance,
in the order the variables are given; confidence bands come from Monte Carlo draws
of the coefficients from their estimated normal distribution.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _fod(a: np.ndarray) -> np.ndarray:
    """Forward orthogonal deviations of a (T, k) array; the last row is lost (NaN)."""
    T = a.shape[0]
    out = np.full_like(a, np.nan, dtype=float)
    csum = np.cumsum(a[::-1], axis=0)[::-1]  # csum[t] = sum_{s>=t} a[s]
    for t in range(T - 1):
        n_fut = T - t - 1
        fut_mean = csum[t + 1] / n_fut
        out[t] = np.sqrt(n_fut / (n_fut + 1)) * (a[t] - fut_mean)
    return out


def fit_pvar(df: pd.DataFrame, variables: list[str], unit: str, time: str, p: int = 1):
    """Estimate a PVAR(p). df: one row per unit-time, sorted, no gaps within units.

    Returns dict with A (list of p (K,K) matrices, A[q][i, j] = effect of var j at lag q+1
    on var i), Sigma (residual covariance), V (covariance of vec of the stacked
    coefficient matrix, rows = equations), n (observations used).
    """
    K = len(variables)
    Ys, Xs, Zs = [], [], []
    for _, g in df.sort_values([unit, time]).groupby(unit, sort=False):
        y = g[variables].to_numpy(float)
        T = len(y)
        if T <= p + 2:
            continue
        lags = np.hstack([y[p - q - 1:T - q - 1] for q in range(p)])  # rows t = p..T-1
        cur = y[p:]
        ok = ~np.isnan(cur).any(1) & ~np.isnan(lags).any(1)
        cur, lags = cur[ok], lags[ok]
        Ys.append(_fod(cur)[:-1])
        Xs.append(_fod(lags)[:-1])
        Zs.append(lags[:-1])
    Y, X, Z = np.vstack(Ys), np.vstack(Xs), np.vstack(Zs)
    ZX_inv = np.linalg.inv(Z.T @ X)
    B = ZX_inv @ (Z.T @ Y)  # (K*p, K): column k = equation k
    U = Y - X @ B
    n = Y.shape[0]
    Sigma = U.T @ U / (n - K * p)
    Q = ZX_inv @ (Z.T @ Z) @ ZX_inv.T  # (Kp, Kp)
    V = np.kron(Sigma, Q)  # covariance of vec(B) stacked by equation
    A = [B[q * K:(q + 1) * K].T for q in range(p)]
    return dict(A=A, B=B, Sigma=Sigma, V=V, n=n, variables=list(variables), p=p)


def _oirf(A, Sigma, H):
    K = Sigma.shape[0]
    p = len(A)
    P = np.linalg.cholesky(Sigma)
    # MA coefficients
    Phi = [np.eye(K)]
    for h in range(1, H + 1):
        Phi.append(sum(A[q] @ Phi[h - q - 1] for q in range(min(p, h))))
    return np.array([ph @ P for ph in Phi])  # (H+1, K, K): [h, response, shock]


def irf(res, H: int = 10, draws: int = 200, level: float = 0.95, seed: int = 0):
    """Orthogonalized IRFs with Monte Carlo bands. Returns long DataFrame."""
    K, p = len(res["variables"]), res["p"]
    point = _oirf(res["A"], res["Sigma"], H)
    rng = np.random.default_rng(seed)
    vecB = res["B"].T.reshape(-1)  # equation-major, matches kron(Sigma, Q)
    sims = []
    Lv = np.linalg.cholesky(res["V"] + 1e-14 * np.eye(len(vecB)))
    for _ in range(draws):
        b = (vecB + Lv @ rng.standard_normal(len(vecB))).reshape(K, K * p).T
        A = [b[q * K:(q + 1) * K].T for q in range(p)]
        sims.append(_oirf(A, res["Sigma"], H))
    sims = np.array(sims)
    lo = np.percentile(sims, 100 * (1 - level) / 2, axis=0)
    hi = np.percentile(sims, 100 * (1 + level) / 2, axis=0)
    rows = []
    names = res["variables"]
    for h in range(H + 1):
        for i, r in enumerate(names):
            for j, s in enumerate(names):
                rows.append(dict(h=h, response=r, shock=s, irf=point[h, i, j], lo=lo[h, i, j], hi=hi[h, i, j]))
    return pd.DataFrame(rows)
