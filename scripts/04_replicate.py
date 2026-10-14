"""Replication gate (pre-registered in CLAUDE.md, 14 Oct 2026) against Antonio et al. (2024).

G1  regional mean and SD of the rice CPI level, 1994M1-2023M3, vs Table 1 (+-0.5, >=15/17)
G1b the same for the two fuel candidates; the closer one becomes FPI (D2)
G2  PVAR(1) replica: shape of the RPI response to THAI and FPI shocks
G3  ordering: rice-insufficient vs sufficient regions; high vs low poverty
Indicative: panel local projection of rice inflation on the real THAI shock.

Writes output/tables/replication_gate.csv, replication_table1.csv, replication_pvar_irf.csv,
replication_lp_indicative.csv and output/tables/replication_choice.json (the fuel item).
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rtl.lp import local_projection  # noqa: E402
from rtl.pvar import fit_pvar, irf  # noqa: E402

T = ROOT / "output/tables"
START, END = pd.Period("1994-01", "M"), pd.Period("2023-03", "M")
TOL, NEED = 0.5, 15


def table1_check(reg, targets):
    s = reg[(reg.month >= START) & (reg.month <= END)]
    rows = []
    for var, prefix in [("cpi_rice", "rice_cpi_level"), ("cpi_fuel_hh", "fuel_cpi_level"),
                        ("cpi_fuel_tr", "fuel_cpi_level")]:
        stats = s.groupby("region")[var].agg(["mean", "std", "count"])
        for _, t in targets[targets.outcome.str.startswith(prefix)].iterrows():
            r = t.outcome.split("|")[1]
            rows.append(dict(variable=var, region=r, target_mean=t.beta, est_mean=stats.loc[r, "mean"],
                             target_sd=t.se, est_sd=stats.loc[r, "std"], n_months=int(stats.loc[r, "count"])))
    d = pd.DataFrame(rows)
    d["dev_mean"] = d.est_mean - d.target_mean
    d["dev_sd"] = d.est_sd - d.target_sd
    return d


def pvar_data(reg, fuel):
    d = reg[(reg.month >= START) & (reg.month <= END)].copy()
    d["RPI"] = d.dl_rice
    d["FPI"] = d["dl_" + fuel.replace("cpi_", "")]
    d["THAI"] = d.groupby("region").thai5_php.transform(lambda s: 100 * np.log(s).diff()) \
        - d.groupby("region").cpi_all_nat.transform(lambda s: 100 * np.log(s).diff())
    d["UREA"] = d.dl_urea_real
    d["ENSO"] = d.oni
    return d.dropna(subset=["RPI", "FPI", "THAI", "UREA", "ENSO"])


ORDER = ["ENSO", "FPI", "UREA", "THAI", "RPI"]


def shape(q, shock):
    r = q[(q.response == "RPI") & (q.shock == shock)].set_index("h")
    return r


def main():
    reg = pd.read_parquet(ROOT / "data/processed/panel_region.parquet")
    targets = pd.read_csv(ROOT / "replication/antonio2024_targets.csv")
    gate = []

    # ---- G1 / G1b
    t1 = table1_check(reg, targets)
    t1.to_csv(T / "replication_table1.csv", index=False, float_format="%.3f")
    rice = t1[t1.variable == "cpi_rice"]
    n_mean = int((rice.dev_mean.abs() <= TOL).sum())
    n_sd = int((rice.dev_sd.abs() <= TOL).sum())
    gate.append(dict(criterion="G1 rice CPI means within 0.5 of Table 1", target=f">= {NEED} of 17",
                     estimate=f"{n_mean} of 17 (median |dev| {rice.dev_mean.abs().median():.3f})",
                     passed=n_mean >= NEED))
    gate.append(dict(criterion="G1 rice CPI SDs within 0.5 of Table 1", target=f">= {NEED} of 17",
                     estimate=f"{n_sd} of 17 (median |dev| {rice.dev_sd.abs().median():.3f})", passed=n_sd >= NEED))
    fuel_mad = {v: t1[t1.variable == v].dev_mean.abs().median() for v in ["cpi_fuel_hh", "cpi_fuel_tr"]}
    fuel = min(fuel_mad, key=fuel_mad.get)
    fsub = t1[t1.variable == fuel]
    n_fuel = int((fsub.dev_mean.abs() <= TOL).sum())
    gate.append(dict(criterion="G1b fuel CPI means within 0.5 (better candidate)", target=f">= {NEED} of 17",
                     estimate=f"{fuel}: {n_fuel} of 17 (median |dev| {fuel_mad[fuel]:.3f}; other "
                              f"{[v for v in fuel_mad if v != fuel][0]}: {max(fuel_mad.values()):.3f})",
                     passed=n_fuel >= NEED))
    (T / "replication_choice.json").write_text(json.dumps(
        {"fuel": fuel, "fuel_median_abs_dev": fuel_mad, "fuel_replicated": bool(n_fuel >= NEED)}, indent=2))

    # ---- G2: PVAR replica on all 17 regions
    d = pvar_data(reg, fuel)
    res = fit_pvar(d, ORDER, "region", "t", p=1)
    q = irf(res, H=10, draws=200, level=0.95, seed=2024)
    q["sample"] = "all"
    r = shape(q, "THAI")
    peak_h = int(r.irf.idxmax())
    peak = r.irf.max()
    gate.append(dict(criterion="G2(i) THAI->RPI 95% band above zero at h=1", target="lo > 0",
                     estimate=f"irf {r.irf[1]:.3f} [{r.lo[1]:.3f}, {r.hi[1]:.3f}]", passed=bool(r.lo[1] > 0)))
    gate.append(dict(criterion="G2(ii) THAI->RPI peaks at h=1 or 2", target="h in {1,2}",
                     estimate=f"peak at h={peak_h} ({peak:.3f})", passed=peak_h in (1, 2)))
    gate.append(dict(criterion="G2(iii) THAI->RPI below 25% of peak by h=6", target="< 0.25 x peak",
                     estimate=f"h=6: {r.irf[6]:.3f} ({r.irf[6] / peak:.2f} of peak)",
                     passed=bool(r.irf[6] < 0.25 * peak)))
    rf = shape(q, "FPI")
    gate.append(dict(criterion="G2(iv) FPI->RPI positive at h=0", target="> 0",
                     estimate=f"{rf.irf[0]:.3f} [{rf.lo[0]:.3f}, {rf.hi[0]:.3f}]", passed=bool(rf.irf[0] > 0)))
    gate.append(dict(criterion="G2(v) FPI->RPI below 25% of impact by h=3", target="< 0.25 x h0",
                     estimate=f"h=3: {rf.irf[3]:.3f} ({rf.irf[3] / rf.irf[0]:.2f} of impact)",
                     passed=bool(rf.irf[3] < 0.25 * rf.irf[0])))

    # ---- G3: subsamples
    groups = pd.read_csv(ROOT / "replication/antonio2024_region_groups.csv").set_index("region")
    peaks, irfs = {}, [q]
    subs = {"insufficient": groups.index[groups.self_sufficiency_class == "Insufficient"],
            "sufficient": groups.index[groups.self_sufficiency_class == "Sufficient"],
            "low_poverty": groups.index[groups.poverty_class == "Low"],
            "high_poverty": groups.index[groups.poverty_class == "High"]}
    for name, regs in subs.items():
        rs = fit_pvar(d[d.region.isin(regs)], ORDER, "region", "t", p=1)
        qs = irf(rs, H=10, draws=200, level=0.95, seed=2024)
        qs["sample"] = name
        irfs.append(qs)
        peaks[name] = shape(qs, "THAI").irf.max()
    ratio = peaks["insufficient"] / peaks["sufficient"]
    gate.append(dict(criterion="G3 peak ratio insufficient/sufficient", target="in [1.3, 3.0]",
                     estimate=f"{ratio:.2f} ({peaks['insufficient']:.3f} / {peaks['sufficient']:.3f})",
                     passed=bool(1.3 <= ratio <= 3.0)))
    gate.append(dict(criterion="G3 peak high poverty < low poverty", target="high < low",
                     estimate=f"high {peaks['high_poverty']:.3f} vs low {peaks['low_poverty']:.3f}",
                     passed=bool(peaks["high_poverty"] < peaks["low_poverty"])))
    pd.concat(irfs).to_csv(T / "replication_pvar_irf.csv", index=False, float_format="%.5f")

    # ---- exploratory diagnostic after G3 failed (not part of the gate): impact (h=0) and
    # six-month cumulative responses by group, p = 1 and p = 2, matching the paper's wording
    from rtl.pvar import _oirf
    diag = []
    subs["medium_poverty"] = groups.index[groups.poverty_class == "Medium"]
    for p_ in (1, 2):
        for name, regs in subs.items():
            rs = fit_pvar(d[d.region.isin(regs)], ORDER, "region", "t", p=p_)
            o = _oirf(rs["A"], rs["Sigma"], 10)[:, ORDER.index("RPI"), ORDER.index("THAI")]
            diag.append(dict(p=p_, sample=name, impact_h0=o[0], peak=o.max(), peak_h=int(o.argmax()),
                             cum_h0_5=o[:6].sum()))
    pd.DataFrame(diag).to_csv(T / "replication_g3_diagnostic.csv", index=False, float_format="%.4f")

    # ---- indicative: LP on the reference sample
    s = reg.sort_values(["region", "month"]).reset_index(drop=True)
    s["f_real_shock"] = s.f_real
    mask = (s.month >= pd.Period("1995-01", "M")) & (s.month <= END)
    lp = local_projection(s, y="dl_rice", x="f_real_shock", time="t", unit="region", horizons=6, p=12,
                          cumulative=True, se="driscoll_kraay", sample=mask)
    lp.to_csv(T / "replication_lp_indicative.csv", index=False, float_format="%.5f")

    g = pd.DataFrame(gate)
    g.to_csv(T / "replication_gate.csv", index=False)
    print(g.to_string(index=False))
    print("\nOVERALL:", "PASS" if g.passed.all() else "FAIL")
    print("\nindicative LP (cumulative, real THAI):\n", lp[["h", "beta", "se", "lo", "hi"]].round(4).to_string())


if __name__ == "__main__":
    main()
