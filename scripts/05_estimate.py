"""Estimate RQ1-RQ5 and the robustness menu exactly as pre-specified in CLAUDE.md.

All local projections: h = 0..12, p = 12, Teulings-Zubanov leads, trend, cumulative
responses, 90% bands; Driscoll-Kraay (panel) or Newey-West (national).
Writes output/tables/estimates.csv (one long table: rq, spec, outcome, cumulative, h,
term, beta, se, lo, hi, nobs, n_units, r2) and output/tables/rq3_gap.csv.

Term names: 'shock' is the pre-law pass-through when the model interacts the shock
with `post`, and the post-law pass-through when it interacts with `pre`;
'shock_x_post' is the change (theta). Specs whose name ends in '_postparam' are the
re-parametrised models that give the post-law B_h directly.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rtl.lp import local_projection  # noqa: E402

P = ROOT / "data/processed"
T = ROOT / "output/tables"
H, LAGS = 12, 12
M = lambda s: pd.Period(s, "M")  # noqa: E731
ROWS = []


def run(rq, spec, df, y, x="f", unit="region", se=None, interact=(), exog=(), controls=(), start="1995-01",
        end="2026-09", p=LAGS, extra_mask=None, cumulative=True):
    se = se or ("driscoll_kraay" if unit else "newey_west")
    mask = (df.month >= M(start)) & (df.month <= M(end))
    if extra_mask is not None:
        mask &= extra_mask
    res = local_projection(df, y=y, x=x, time="t", unit=unit, horizons=H, p=p, interact=tuple(interact),
                           exog=tuple(exog), controls=tuple(controls), sample=mask, cumulative=cumulative, se=se)
    res.insert(0, "cumulative", cumulative)
    res.insert(0, "outcome", y)
    res.insert(0, "spec", spec)
    res.insert(0, "rq", rq)
    ROWS.append(res)
    return res


def regime(rq, spec, df, y, unit="region", **kw):
    """Pre-law B (shock), change theta (shock_x_post), and post-law B (spec + '_postparam')."""
    ex = tuple(kw.pop("exog", ()))
    run(rq, spec, df, y, unit=unit, interact=("post",) + tuple(kw.pop("interact_more", ())), exog=("post",) + ex,
        **kw)
    run(rq, spec + "_postparam", df, y, unit=unit, interact=("pre",), exog=("post",) + ex, **kw)


def main():
    reg = pd.read_parquet(P / "panel_region.parquet").sort_values(["region", "month"]).reset_index(drop=True)
    nat = pd.read_parquet(P / "panel_national.parquet").sort_values("month").reset_index(drop=True)
    nat = nat[nat.month <= M("2026-09")].reset_index(drop=True)
    for d in (reg, nat):
        d["fpos"] = (d.f > 0).astype(float)
        d["placebo"] = (d.month >= M("2016-03")).astype(int)
        d["pre"] = 1 - d.post

    # ---------------- RQ1: regional rice CPI ----------------
    run("RQ1", "full_sample", reg, "dl_rice")
    regime("RQ1", "main", reg, "dl_rice")
    regime("RQ1", "national", nat, "dl_rice", unit=None)

    # ---------------- RQ2: along the chain (national, 2010-) ----------------
    for y in ["dl_farmgate_palay", "dl_wholesale_rmr", "dl_retail_rmr", "dl_rice"]:
        regime("RQ2", "chain_national", nat, y, unit=None, start="2011-01")
    farm = reg[reg.region != "NCR"].reset_index(drop=True)
    regime("RQ2", "farmgate_regional", farm, "dl_farmgate_palay", start="2011-01")
    regime("RQ2", "retail_regional", reg, "dl_retail_rmr", start="2011-01")

    # ---------------- RQ4: heterogeneity (D9, D11: not validated) ----------------
    for g in ["insuff", "highpov"]:
        run("RQ4", f"het_{g}", reg, "dl_rice", interact=(g, "post", f"post_{g}"), exog=("post", f"post_{g}"))

    # ---------------- RQ5: distribution (national) ----------------
    run("RQ5", "gap_full", nat, "dD", unit=None, start="2001-01")
    regime("RQ5", "gap", nat, "dD", unit=None, start="2001-01")
    run("RQ5", "rice_national_2001", nat, "dl_rice", unit=None, start="2001-01")
    run("RQ5", "all_items", nat, "dl_all", unit=None, start="2001-01")
    run("RQ5", "all_items_b30", nat, "dl_all_b30", unit=None, start="2001-01")

    # ---------------- Robustness (RQ1 main) ----------------
    R = "ROB"
    regime(R, "a_real_shock", reg, "dl_rice", x="f_real")
    regime(R, "b_viet5", reg, "dl_rice", x="f_viet", start="2005-02")
    regime(R, "c_usd_fx_control", reg, "dl_rice", x="f_usd", controls=("dl_fx",))
    regime(R, "d_macro_controls", reg, "dl_rice", controls=("dl_fx", "dl_dubai_php", "dl_urea_php", "oni"))
    regime(R, "e_p6", reg, "dl_rice", p=6)
    regime(R, "e_p18", reg, "dl_rice", p=18, start="1995-07")
    regime(R, "f_no_2008crisis", reg, "dl_rice", extra_mask=~reg.month.between(M("2007-10"), M("2008-12")))
    regime(R, "g_no_2020", reg, "dl_rice", extra_mask=~reg.month.between(M("2020-01"), M("2020-12")))
    regime(R, "h_end_2024m6", reg, "dl_rice", end="2024-06")
    regime(R, "i_symmetric_2012", reg, "dl_rice", start="2012-03")
    run(R, "j_asymmetry", reg, "dl_rice", interact=("post", "fpos"), exog=("post", "fpos"))
    regime(R, "k_drop_newgeo", reg, "dl_rice", extra_mask=reg.new_geo_ext == 0)
    for r in sorted(reg.region.unique()):
        d = reg[reg.region != r].reset_index(drop=True)
        run(R, f"l_loo_{r}", d, "dl_rice", interact=("post",), exog=("post",))
    run(R, "m_separate_pre", reg, "dl_rice", end="2019-02")
    run(R, "m_separate_post", reg, "dl_rice", start="2019-03")
    run(R, "n_placebo_2016m3", reg, "dl_rice", interact=("placebo",), exog=("placebo",), end="2019-02")
    regime(R, "o_cluster_region", reg, "dl_rice", se="cluster")

    est = pd.concat(ROWS, ignore_index=True)
    est.to_csv(T / "estimates.csv", index=False, float_format="%.6f")

    # ---------------- RQ3: border gap, interrupted time series ----------------
    g = nat[(nat.month >= M("2010-01")) & (nat.month <= M("2026-09"))].copy()
    g["gap_wholesale"] = 100 * np.log(g.wholesale_rmr / (g.thai5_php / 1000))
    g["gap_retail"] = 100 * np.log(g.retail_rmr / (g.thai5_php / 1000))
    g["ln_world"] = 100 * np.log(g.thai5_php / 1000)
    months = pd.get_dummies(g.month.dt.month, prefix="m", drop_first=True).astype(float)
    rows = []
    for yv in ["gap_wholesale", "gap_retail"]:
        for spec, cols in [("its", ["post", "tariff15", "ban"]), ("its_world", ["post", "tariff15", "ban", "ln_world"])]:
            X = sm.add_constant(pd.concat([g[cols].astype(float), months], axis=1))
            fit = sm.OLS(g[yv], X).fit(cov_type="HAC", cov_kwds={"maxlags": 12})
            for c in cols:
                rows.append(dict(outcome=yv, spec=spec, term=c, beta=fit.params[c], se=fit.bse[c],
                                 p=fit.pvalues[c], nobs=int(fit.nobs), r2=fit.rsquared))
    pd.DataFrame(rows).to_csv(T / "rq3_gap.csv", index=False, float_format="%.5f")
    g[["month", "gap_wholesale", "gap_retail", "ln_world", "post", "tariff15", "ban"]].assign(
        month=lambda d: d.month.astype(str)).to_csv(T / "rq3_gap_series.csv", index=False, float_format="%.4f")

    key = est[(est.h.isin([6, 12]))]
    show = key[key.spec.isin(["full_sample", "main", "main_postparam", "national", "national_postparam"])]
    print(show[["rq", "spec", "h", "term", "beta", "se"]].round(3).to_string(index=False))
    print(pd.DataFrame(rows).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
