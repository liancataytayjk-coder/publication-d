"""Objective 1: descriptive statistics (pre-specified in CLAUDE.md, section 4.6 of the skill).

Writes to output/tables/:
  desc_subperiods.csv     mean and SD of monthly inflation (rice CPI, world shock, chain prices) by sub-period
  desc_annual.csv         annual (Dec/Dec) inflation: rice all income, rice bottom 30%, headline,
                          headline bottom 30%, world rice in PHP; rice contribution to headline (E5)
  desc_episodes.csv       world price episodes: runs of >= 3 months with 12-month change >= +15%
  desc_crosscorr.csv      correlation of world shock f_t with national rice inflation at t+k, pre/post law
  desc_dispersion.csv     cross-region SD of monthly rice inflation and CV of retail RMR price levels, by year
  desc_adf.csv            ADF unit-root tests (levels in logs and monthly changes)
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
P, T = ROOT / "data/processed", ROOT / "output/tables"
M = lambda s: pd.Period(s, "M")  # noqa: E731
PERIODS = [("1995M1-2007M9", "1995-01", "2007-09"), ("2007M10-2008M12 (world crisis)", "2007-10", "2008-12"),
           ("2009M1-2019M2 (quotas)", "2009-01", "2019-02"), ("2019M3-2024M6 (35% tariff)", "2019-03", "2024-06"),
           ("2024M7-2026M9 (15% tariff, suspension, indexed tariff)", "2024-07", "2026-09")]


def main():
    nat = pd.read_parquet(P / "panel_national.parquet").sort_values("month")
    nat = nat[nat.month <= M("2026-09")].set_index("month")
    reg = pd.read_parquet(P / "panel_region.parquet")
    w = pd.read_parquet(P / "cpi_weights.parquet")

    rows = []
    for name, a, b in PERIODS:
        s = nat.loc[M(a):M(b)]
        for v in ["dl_rice", "dl_rice_b30", "f", "dl_all", "dl_farmgate_palay", "dl_wholesale_rmr", "dl_retail_rmr"]:
            x = s[v].dropna()
            if len(x) > 2:
                rows.append(dict(period=name, variable=v, months=len(x), mean=x.mean(), sd=x.std(),
                                 annualised_mean=12 * x.mean()))
    pd.DataFrame(rows).to_csv(T / "desc_subperiods.csv", index=False, float_format="%.3f")

    dec = nat[nat.index.month == 12]
    ann = pd.DataFrame({
        "rice_all": 100 * np.log(dec.cpi_rice).diff(), "rice_b30": 100 * np.log(dec.cpi_rice_b30).diff(),
        "headline_all": 100 * np.log(dec.cpi_all).diff(), "headline_b30": 100 * np.log(dec.cpi_all_b30).diff(),
        "world_rice_php": 100 * np.log(dec.thai5_php).diff()})
    ann.index = ann.index.year
    wa = float(w[(w.geo == "Philippines") & (w.group == "all") & (w["item"] == "rice") & (w.coding == "old")].weight.iloc[0])
    wb = float(w[(w.geo == "Philippines") & (w.group == "b30") & (w["item"] == "rice")].weight.iloc[0])
    ann["rice_contrib_all"] = wa / 100 * ann.rice_all       # E5, approximate (2018 weights)
    ann["rice_contrib_b30"] = wb / 100 * ann.rice_b30
    sep = nat.loc[M("2026-09")]
    sep25 = nat.loc[M("2025-09")]
    ann.loc[2026] = [100 * np.log(sep.cpi_rice / sep25.cpi_rice), 100 * np.log(sep.cpi_rice_b30 / sep25.cpi_rice_b30),
                     100 * np.log(sep.cpi_all / sep25.cpi_all), 100 * np.log(sep.cpi_all_b30 / sep25.cpi_all_b30),
                     100 * np.log(sep.thai5_php / sep25.thai5_php), np.nan, np.nan]
    ann.loc[2026, "rice_contrib_all"] = wa / 100 * ann.loc[2026, "rice_all"]
    ann.loc[2026, "rice_contrib_b30"] = wb / 100 * ann.loc[2026, "rice_b30"]
    ann.index.name = "year"  # 2026 = September 2025 to September 2026
    ann.dropna(how="all").to_csv(T / "desc_annual.csv", float_format="%.3f")

    yoy = 100 * np.log(nat.thai5_php / nat.thai5_php.shift(12))
    hot = (yoy >= 15).astype(int)
    eps, start = [], None
    for m, v in hot.items():
        if v and start is None:
            start = m
        if (not v or m == hot.index[-1]) and start is not None:
            end = m - 1 if not v else m
            if (end - start).n + 1 >= 3:
                s = nat.loc[start:end]
                eps.append(dict(start=str(start), end=str(end), months=(end - start).n + 1,
                                peak_world_yoy=yoy.loc[start:end].max(),
                                world_change=100 * np.log(s.thai5_php.iloc[-1] / nat.thai5_php.loc[start - 1]),
                                rice_cpi_change=100 * np.log(s.cpi_rice.iloc[-1] / nat.cpi_rice.loc[start - 1])))
            start = None
    pd.DataFrame(eps).to_csv(T / "desc_episodes.csv", index=False, float_format="%.2f")

    cc = []
    for name, a, b in [("pre", "1995-01", "2019-02"), ("post", "2019-03", "2026-09")]:
        s = nat.loc[M(a):M(b)]
        for k in range(-6, 13):
            cc.append(dict(regime=name, k=k, corr=s.f.corr(s.dl_rice.shift(-k))))
    pd.DataFrame(cc).to_csv(T / "desc_crosscorr.csv", index=False, float_format="%.4f")

    reg["year"] = reg.month.dt.year
    disp = reg.groupby("month").agg(sd_rice_infl=("dl_rice", "std")).reset_index()
    disp["year"] = disp.month.dt.year
    d1 = disp.groupby("year").sd_rice_infl.mean()
    lv = reg.dropna(subset=["retail_rmr"]).groupby(["year", "region"]).retail_rmr.mean().reset_index()
    d2 = lv.groupby("year").retail_rmr.agg(lambda x: 100 * x.std() / x.mean())
    pd.DataFrame({"sd_monthly_rice_inflation_across_regions": d1, "cv_retail_rmr_level_across_regions": d2}) \
        .loc[1995:2026].to_csv(T / "desc_dispersion.csv", float_format="%.3f")

    adf = []
    for v, lab in [("cpi_rice", "ln rice CPI"), ("thai5_php", "ln world rice (PHP)"), ("retail_rmr", "ln retail RMR"),
                   ("farmgate_palay", "ln farmgate palay")]:
        x = np.log(nat[v].dropna())
        for form, s in [("level", x), ("monthly change", 100 * x.diff().dropna())]:
            stat, p, *_ = adfuller(s, regression="ct" if form == "level" else "c", autolag="AIC", result_object=False)
            adf.append(dict(series=lab, form=form, start=str(s.index.min()), adf_stat=stat, p_value=p))
    pd.DataFrame(adf).to_csv(T / "desc_adf.csv", index=False, float_format="%.3f")
    print(pd.read_csv(T / "desc_subperiods.csv").query("variable in ['dl_rice','f']").round(2).to_string(index=False))
    print(pd.read_csv(T / "desc_episodes.csv").to_string(index=False))
    print(pd.read_csv(T / "desc_annual.csv").tail(9).round(2).to_string(index=False))


if __name__ == "__main__":
    main()
