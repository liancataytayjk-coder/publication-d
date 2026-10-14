"""Build the analysis panels from the cleaned long tables.

Outputs (data/processed/):
  panel_region.parquet    17 regions x months, 1994M1-2026M9 (old geographic code, D5)
  panel_national.parquet  national monthly series (CPIs, chain prices, world prices, shocks)
  output/tables/geo_overlap_check.csv  agreement of old- and new-code regional series, 2018-2025
  output/tables/region_groups.csv      heterogeneity groups (D9) and 2018 rice weights

Rates are 100 x change in natural log (D7); the shock f is the world rice price in pesos.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rtl.regions import REGIONS  # noqa: E402

P = ROOT / "data/processed"
T = ROOT / "output/tables"
LAW = pd.Period("2019-03", "M")       # D6
TARIFF15 = pd.Period("2024-07", "M")  # EO 62 (policy_context P7)
BAN = (pd.Period("2025-09", "M"), pd.Period("2025-12", "M"))  # EO 93 / EO 102 (P9-P10)
CAP = (pd.Period("2023-09", "M"), pd.Period("2023-10", "M"))  # EO 39 / EO 42 (P5-P6)
END = pd.Period("2026-09", "M")


def dlog(s):
    return 100 * np.log(s).diff()


def chain_old_with_new(cpi, group, item):
    """Old-code levels to Dec 2025, extended with new-code monthly growth to END (D5)."""
    old = cpi[(cpi.coding == "old") & (cpi.group == group) & (cpi["item"] == item)]
    new = cpi[(cpi.coding == "new") & (cpi.group == group) & (cpi["item"] == item)]
    o = old.pivot_table(index="month", columns="geo", values="value")
    n = new.pivot_table(index="month", columns="geo", values="value")
    last = o.index.max()
    ext = n.loc[n.index > last]
    if len(ext):
        growth = n.loc[n.index >= last].pct_change().loc[ext.index] + 1
        lvl = o.loc[[last]].to_numpy()
        rows = []
        for m in ext.index:
            lvl = lvl * growth.loc[[m]].reindex(columns=o.columns).to_numpy()
            rows.append(pd.DataFrame(lvl, index=[m], columns=o.columns))
        o = pd.concat([o] + rows)
    return o.sort_index()


def overlap_check(cpi, group, item):
    old = cpi[(cpi.coding == "old") & (cpi.group == group) & (cpi["item"] == item)].pivot_table(
        index="month", columns="geo", values="value")
    new = cpi[(cpi.coding == "new") & (cpi.group == group) & (cpi["item"] == item)].pivot_table(
        index="month", columns="geo", values="value")
    rows = []
    for g in sorted(set(old.columns) & set(new.columns)):
        a, b = old[g], new[g]
        idx = a.dropna().index.intersection(b.dropna().index)
        da, db = dlog(a.loc[idx]), dlog(b.loc[idx])
        rows.append(dict(group=group, item=item, geo=g, months=len(idx),
                         max_abs_level_diff=float((a.loc[idx] - b.loc[idx]).abs().max()),
                         corr_monthly_change=float(da.corr(db))))
    return pd.DataFrame(rows)


def back_chain(newer, older):
    """Extend `newer` backwards with the monthly growth of `older` (join on growth rates)."""
    first = newer.dropna().index.min()
    g = older.sort_index()
    out = newer.dropna().copy()
    prev = out.loc[first]
    for m in sorted(g.index[g.index < first], reverse=True):
        nxt = m + 1
        if nxt in g.index and not np.isnan(g.loc[nxt]) and not np.isnan(g.loc[m]):
            prev = prev * g.loc[m] / g.loc[nxt]
            out.loc[m] = prev
    return out.sort_index()


def chain_prices():
    """National and regional rice chain prices, PHP/kg, 2010M1-2026M9 (D12)."""
    pr = pd.read_parquet(P / "prices_long.parquet")

    def s(src, com, geo):
        x = pr[(pr.source == src) & (pr.commodity == com) & (pr.geo == geo)]
        return x.set_index("month").value.sort_index()

    out = {}
    geos = ["Philippines"] + REGIONS
    for geo in geos:
        for tag, c18, c12, cold in [("rmr", "RICE, REGULAR-MILLED, 1 KG", "RICE, REGULAR MILLED, LOOSE, 1 KG",
                                     "Regular Milled Rice (RMR)"),
                                    ("wmr", "RICE, WELL-MILLED, 1 KG", "RICE, WELL MILLED, LOOSE, 1 KG",
                                     "Well Milled Rice (WMR)")]:
            r18 = s("retail_cereals_2018based_oldgeo_2018_2025", c18, geo)
            r18n = s("retail_cereals_2018based_newgeo_2018_2026", c18, geo)
            if len(r18) and len(r18n):  # extend old-code 2018 series to 2026 with new-code growth (D5)
                last = r18.index.max()
                g = r18n[r18n.index >= last]
                r18 = pd.concat([r18, r18.loc[last] * (g / g.loc[last]).iloc[1:]])
            r = back_chain(r18, s("retail_cereals_2012based_2012_2021", c12, geo))
            r = back_chain(r, s("retail_cereals_oldseries_1990_2021", cold, geo))
            out[(geo, "retail_" + tag)] = r
            ws_old = s("wholesale_cereals_oldgeo_2010_2025", cold, geo)
            ws_new = s("wholesale_cereals_newgeo_2010_2026", cold, geo)
            if len(ws_old) and len(ws_new):
                last = ws_old.index.max()
                g = ws_new[ws_new.index >= last]
                ws_old = pd.concat([ws_old, ws_old.loc[last] * (g / g.loc[last]).iloc[1:]])
            out[(geo, "wholesale_" + tag)] = ws_old
        fg = s("farmgate_cereals_newseries_2010_2026", "Palay [Paddy] Other Variety, dry (conv. to 14% mc)", geo)
        out[(geo, "farmgate_palay")] = fg
    df = pd.DataFrame(out)
    df = df[(df.index >= pd.Period("2010-01", "M")) & (df.index <= END)]
    df.columns = pd.MultiIndex.from_tuples(df.columns, names=["geo", "series"])
    long = df.stack("geo", future_stack=True).reset_index().rename(columns={"level_0": "month"})
    long["splice_join"] = long.month.isin([pd.Period("2012-01", "M"), pd.Period("2018-01", "M")]).astype(int)
    return long


def main():
    cpi = pd.read_parquet(P / "cpi_long.parquet")
    w = pd.read_parquet(P / "world_monthly.parquet")
    weights = pd.read_parquet(P / "cpi_weights.parquet")
    T.mkdir(parents=True, exist_ok=True)

    checks = pd.concat([overlap_check(cpi, g, i) for g, i in
                        [("all", "rice"), ("all", "all"), ("all", "fuel_hh"), ("all", "fuel_tr"), ("b30", "rice")]])
    checks.to_csv(T / "geo_overlap_check.csv", index=False, float_format="%.4f")

    # ---------------- regional panel ----------------
    series = {}
    for group, item, name in [("all", "rice", "cpi_rice"), ("all", "all", "cpi_all"), ("all", "food", "cpi_food"),
                              ("all", "fuel_hh", "cpi_fuel_hh"), ("all", "fuel_tr", "cpi_fuel_tr"),
                              ("b30", "rice", "cpi_rice_b30"), ("b30", "all", "cpi_all_b30")]:
        wide = chain_old_with_new(cpi, group, item)
        series[name] = wide.stack().rename(name)
    reg = pd.concat(series.values(), axis=1).reset_index()
    reg.columns = ["month", "geo"] + list(series)
    nat = reg[reg.geo == "Philippines"].drop(columns="geo").set_index("month")
    reg = reg[reg.geo.isin(REGIONS)].copy()
    reg = reg[(reg.month >= pd.Period("1994-01", "M")) & (reg.month <= END)]
    reg["region"] = reg["geo"]
    reg["new_geo_ext"] = ((reg.month > pd.Period("2025-12", "M"))
                          & reg.region.isin(["Western Visayas", "Central Visayas", "SOCCSKSARGEN", "BARMM"])).astype(int)

    # world block and shocks
    w = w.set_index("month")
    nat = nat.join(w, how="outer")
    nat = nat[(nat.index >= pd.Period("1990-01", "M")) & (nat.index <= END)]
    nat["thai5_php"] = nat.thai5 * nat.fx
    nat["viet5_php"] = nat.viet5 * nat.fx
    nat["f"] = dlog(nat.thai5_php)                       # D7
    nat["f_real"] = dlog(nat.thai5_php / nat.cpi_all)    # robustness (a), reference version
    nat["f_viet"] = dlog(nat.viet5_php)                  # robustness (b)
    nat["f_usd"] = dlog(nat.thai5)                       # robustness (c)
    nat["dl_fx"] = dlog(nat.fx)
    nat["dl_dubai_php"] = dlog(nat.dubai * nat.fx)
    nat["dl_urea_php"] = dlog(nat.urea * nat.fx)
    nat["dl_urea_real"] = dlog(nat.urea * nat.fx / nat.cpi_all)
    for c in ["cpi_rice", "cpi_all", "cpi_food", "cpi_fuel_hh", "cpi_fuel_tr", "cpi_rice_b30", "cpi_all_b30"]:
        nat["dl_" + c.replace("cpi_", "")] = dlog(nat[c])
    nat["dD"] = nat.dl_all - nat.dl_all_b30  # RQ5 gap: negative = poor face more inflation
    nat["post"] = (nat.index >= LAW).astype(int)
    nat["tariff15"] = (nat.index >= TARIFF15).astype(int)
    nat["ban"] = ((nat.index >= BAN[0]) & (nat.index <= BAN[1])).astype(int)
    nat["cap"] = ((nat.index >= CAP[0]) & (nat.index <= CAP[1])).astype(int)
    nat.index.name = "month"
    nat = nat.reset_index()
    nat["t"] = (nat.month - pd.Period("1990-01", "M")).apply(lambda x: x.n)

    keep = ["month", "t", "f", "f_real", "f_viet", "f_usd", "dl_fx", "dl_dubai_php", "dl_urea_php", "dl_urea_real",
            "oni", "post", "tariff15", "ban", "cap", "thai5", "thai5_php", "fx", "cpi_all"]
    reg = reg.merge(nat[keep].rename(columns={"cpi_all": "cpi_all_nat"}), on="month", how="left")
    reg = reg.sort_values(["region", "month"]).reset_index(drop=True)
    for c in ["cpi_rice", "cpi_all", "cpi_food", "cpi_fuel_hh", "cpi_fuel_tr", "cpi_rice_b30", "cpi_all_b30"]:
        reg["dl_" + c.replace("cpi_", "")] = reg.groupby("region")[c].transform(dlog)

    groups = pd.read_csv(ROOT / "replication/antonio2024_region_groups.csv")
    groups["insuff"] = (groups.self_sufficiency_class == "Insufficient").astype(int)
    groups["highpov"] = (groups.poverty_class == "High").astype(int)
    wr = weights[(weights["item"] == "rice") & (weights.coding == "old")].pivot_table(
        index="geo", columns="group", values="weight").rename(columns={"all": "w_rice_all", "b30": "w_rice_b30"})
    groups = groups.merge(wr, left_on="region", right_index=True, how="left")
    groups.to_csv(T / "region_groups.csv", index=False, float_format="%.3f")
    reg = reg.merge(groups[["region", "insuff", "highpov"]], on="region", how="left")
    for g in ["insuff", "highpov"]:
        reg[f"post_{g}"] = reg.post * reg[g]
    reg["pre"] = 1 - reg.post
    nat["pre"] = 1 - nat.post

    chain = chain_prices()
    for c in ["retail_rmr", "retail_wmr", "wholesale_rmr", "wholesale_wmr", "farmgate_palay"]:
        chain["dl_" + c] = chain.groupby("geo")[c].transform(dlog)
    nat_chain = chain[chain.geo == "Philippines"].drop(columns="geo")
    nat = nat.merge(nat_chain, on="month", how="left")
    reg_chain = chain[chain.geo.isin(REGIONS)].rename(columns={"geo": "region"}).drop(columns="splice_join")
    reg = reg.merge(reg_chain, on=["region", "month"], how="left")

    # proxy validation: correlations of monthly changes over the common sample
    pv = []
    for a, b, label in [("f", "f_viet", "World price: Thai 5% vs Viet 5% (PHP)"),
                        ("dl_rice", "dl_retail_rmr", "Rice CPI vs retail price survey, RMR"),
                        ("dl_rice", "dl_retail_wmr", "Rice CPI vs retail price survey, WMR"),
                        ("dl_rice", "dl_rice_b30", "Rice CPI: all income vs bottom 30%"),
                        ("dl_retail_rmr", "dl_wholesale_rmr", "Retail vs wholesale RMR"),
                        ("dl_wholesale_rmr", "dl_farmgate_palay", "Wholesale RMR vs farmgate palay")]:
        x = nat[[a, b, "month"]].dropna()
        pv.append(dict(pair=label, start=str(x.month.min()), end=str(x.month.max()), months=len(x),
                       corr_monthly_change=x[a].corr(x[b])))
    pd.DataFrame(pv).to_csv(T / "proxy_validation.csv", index=False, float_format="%.3f")

    reg.to_parquet(P / "panel_region.parquet", index=False)
    nat.to_parquet(P / "panel_national.parquet", index=False)
    print("regional panel:", reg.region.nunique(), "regions", reg.month.min(), "-", reg.month.max(),
          "rows", len(reg), "missing dl_rice", int(reg.dl_rice.isna().sum()))
    print("overlap check (rice, all):\n", checks[(checks["item"] == "rice") & (checks.group == "all")]
          [["geo", "months", "max_abs_level_diff", "corr_monthly_change"]].to_string(index=False))


if __name__ == "__main__":
    main()
