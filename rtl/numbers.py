"""Build the numbers dictionary n and the markdown tables t used by every document.

Nothing in a document is typed by hand: each number comes from output/tables/*.csv or
*.json through this module and is saved to output/tables/paper_numbers.json.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "output/tables"


def f2(x, d=2):
    s = f"{x:.{d}f}"
    if float(s) == 0:
        s = s.lstrip("-")
    return s.replace("-", "−")


def stars(b, se):
    if se is None or np.isnan(se) or se == 0:
        return ""
    p = 2 * (1 - stats.norm.cdf(abs(b / se)))
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def pval(b, se):
    return 2 * (1 - stats.norm.cdf(abs(b / se)))


def md_table(header, rows, align=None):
    align = align or ["l"] + ["r"] * (len(header) - 1)
    sep = ["---:" if a == "r" else ":---" for a in align]
    lines = ["| " + " | ".join(header) + " |", "| " + " | ".join(sep) + " |"]
    lines += ["| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |" for r in rows]
    return "\n" + "\n".join(lines) + "\n"


def build():
    est = pd.read_csv(T / "estimates.csv")
    n, t = {}, {}

    def get(spec, h, term="shock", outcome=None):
        d = est[(est.spec == spec) & (est.h == h) & (est.term == term)]
        if outcome:
            d = d[d.outcome == outcome]
        r = d.iloc[0]
        return float(r.beta), float(r.se), int(r.nobs)

    def put(key, spec, h, term="shock", outcome=None, d=2):
        b, s, nobs = get(spec, h, term, outcome)
        n[key] = f2(b, d)
        n[key + "_se"] = f2(s, d)
        n[key + "_p"] = f2(pval(b, s), 2)
        n[key + "_st"] = stars(b, s)
        n[key + "_raw"] = b
        n[key + "_nobs"] = nobs
        return b, s

    # ---- RQ1
    for h in (0, 3, 6, 12):
        put(f"rq1_full_{h}", "full_sample", h)
        put(f"rq1_pre_{h}", "main", h)
        put(f"rq1_post_{h}", "main_postparam", h)
        put(f"rq1_th_{h}", "main", h, "shock_x_post")
        put(f"rq1_nat_pre_{h}", "national", h)
        put(f"rq1_nat_post_{h}", "national_postparam", h)
        put(f"rq1_nat_th_{h}", "national", h, "shock_x_post")
    n["rq1_ratio6"] = f2(n["rq1_post_6_raw"] / n["rq1_pre_6_raw"], 1)
    n["rq1_nobs"] = n["rq1_pre_6_nobs"]
    rows = []
    for h in (0, 3, 6, 9, 12):
        pre, post, th = get("main", h), get("main_postparam", h), get("main", h, "shock_x_post")
        rows.append([h, f"{f2(pre[0])}{stars(*pre[:2])} ({f2(pre[1])})", f"{f2(post[0])}{stars(*post[:2])} ({f2(post[1])})",
                     f"{f2(th[0])}{stars(*th[:2])} ({f2(th[1])})", pre[2]])
    t["rq1"] = md_table(["Months (h)", "Before the law", "After the law", "Change θ", "Observations"], rows)

    # ---- RQ2
    labels = {"dl_farmgate_palay": "Farmgate palay", "dl_wholesale_rmr": "Wholesale RMR",
              "dl_retail_rmr": "Retail RMR", "dl_rice": "Rice CPI"}
    rows = []
    for y, lab in labels.items():
        key = y.replace("dl_", "")
        for h in (6, 12):
            put(f"rq2_{key}_pre_{h}", "chain_national", h, outcome=y)
            put(f"rq2_{key}_post_{h}", "chain_national_postparam", h, outcome=y)
            put(f"rq2_{key}_th_{h}", "chain_national", h, "shock_x_post", outcome=y)
        r = [lab]
        for h in (6, 12):
            pre, post, th = (get("chain_national", h, outcome=y), get("chain_national_postparam", h, outcome=y),
                             get("chain_national", h, "shock_x_post", outcome=y))
            r += [f"{f2(pre[0])}{stars(*pre[:2])} ({f2(pre[1])})", f"{f2(post[0])}{stars(*post[:2])} ({f2(post[1])})",
                  f"{f2(th[0])}{stars(*th[:2])} ({f2(th[1])})"]
        rows.append(r)
    t["rq2"] = md_table(["Price", "Before, h=6", "After, h=6", "Change, h=6", "Before, h=12", "After, h=12",
                         "Change, h=12"], rows)
    for h in (6, 12):
        put(f"rq2_farmreg_post_{h}", "farmgate_regional_postparam", h)
        put(f"rq2_farmreg_th_{h}", "farmgate_regional", h, "shock_x_post")
        put(f"rq2_retreg_th_{h}", "retail_regional", h, "shock_x_post")

    # ---- RQ3
    g = pd.read_csv(T / "rq3_gap.csv")
    rows = []
    names = {"post": "Law in force (from Mar 2019)", "tariff15": "15% tariff (from Jul 2024)",
             "ban": "Import suspension (Sep–Dec 2025)", "ln_world": "World price (log × 100)"}
    for _, r in g.iterrows():
        k = f"rq3_{r.outcome.replace('gap_', '')}_{r.spec}_{r.term}"
        n[k], n[k + "_se"], n[k + "_p"], n[k + "_st"] = f2(r.beta, 1), f2(r.se, 1), f2(r.p, 3), stars(r.beta, r.se)
        n[k + "_raw"] = float(r.beta)
    for term in ["post", "tariff15", "ban", "ln_world"]:
        row = [names[term]]
        for yv in ["gap_wholesale", "gap_retail"]:
            for spec in ["its", "its_world"]:
                d = g[(g.outcome == yv) & (g.spec == spec) & (g.term == term)]
                row.append("" if d.empty else f"{f2(d.beta.iloc[0], 2 if term == 'ln_world' else 1)}"
                           f"{stars(d.beta.iloc[0], d.se.iloc[0])} ({f2(d.se.iloc[0], 2 if term == 'ln_world' else 1)})")
        rows.append(row)
    t["rq3"] = md_table(["", "Wholesale (1)", "Wholesale (2)", "Retail (1)", "Retail (2)"], rows)
    gs = pd.read_csv(T / "rq3_gap_series.csv")
    gs["period"] = pd.cut(pd.PeriodIndex(gs.month, freq="M").to_timestamp(),
                          [pd.Timestamp("2009-12-01"), pd.Timestamp("2019-02-28"), pd.Timestamp("2024-06-30"),
                           pd.Timestamp("2026-10-01")], labels=["pre", "tariff35", "after2024"])
    for per, v in gs.groupby("period", observed=True).gap_wholesale.mean().items():
        n[f"rq3_mean_gap_{per}"] = f2(v, 0)

    # ---- RQ4
    for g_ in ["insuff", "highpov"]:
        for h in (6, 12):
            put(f"rq4_{g_}_{h}", f"het_{g_}", h, f"shock_x_post_{g_}")
            put(f"rq4_{g_}_level_{h}", f"het_{g_}", h, f"shock_x_{g_}")
    rows = []
    for g_, lab in [("insuff", "Rice-deficit regions"), ("highpov", "High-poverty regions")]:
        r = [lab]
        for h in (6, 12):
            b, s, _ = get(f"het_{g_}", h, f"shock_x_post_{g_}")
            r.append(f"{f2(b)}{stars(b, s)} ({f2(s)})")
            r.append(f2(pval(b, s), 3))
        rows.append(r)
    t["rq4"] = md_table(["Group", "θ post×G, h=6", "p", "θ post×G, h=12", "p"], rows)

    # ---- RQ5
    for h in (0, 6, 12):
        put(f"rq5_gap_{h}", "gap_full", h, d=3)
        put(f"rq5_all_{h}", "all_items", h, d=3)
        put(f"rq5_b30_{h}", "all_items_b30", h, d=3)
        put(f"rq5_gapth_{h}", "gap", h, "shock_x_post", d=3)
        put(f"rq5_rice_{h}", "rice_national_2001", h, d=3)
    ep = json.loads((T / "episode_numbers.json").read_text())
    wa, wb = ep["w_rice_all"], ep["w_rice_b30"]
    n["w_rice_all"], n["w_rice_b30"] = f2(wa, 1), f2(wb, 1)
    mech = n["rq5_rice_6_raw"] * (wa - wb) / 100
    n["rq5_mech6"] = f2(mech, 3)
    n["rq5_mech_share"] = f"{100 * mech / n['rq5_gap_6_raw']:.0f}"
    n["rq5_ratio6"] = f2(n["rq5_b30_6_raw"] / n["rq5_all_6_raw"], 1)
    rows = []
    for spec, lab in [("all_items", "All-items CPI, all income"), ("all_items_b30", "All-items CPI, bottom 30%"),
                      ("gap_full", "Gap ΔD (all income − bottom 30%)"), ("rice_national_2001", "Rice CPI (national)")]:
        r = [lab]
        for h in (0, 6, 12):
            b, s, _ = get(spec, h)
            r.append(f"{f2(b, 3)}{stars(b, s)} ({f2(s, 3)})")
        rows.append(r)
    t["rq5"] = md_table(["Outcome", "h = 0", "h = 6", "h = 12"], rows)

    # ---- robustness
    rb = pd.read_csv(T / "robustness_theta.csv")
    rows = []
    for lab in rb.label.unique():
        r = [lab]
        for h in (6, 12):
            d = rb[(rb.label == lab) & (rb.h == h)].iloc[0]
            if np.isnan(d.se):
                r.append(f"{f2(d.lo)} to {f2(d.hi)}")
            else:
                r.append(f"{f2(d.beta)}{stars(d.beta, d.se)} ({f2(d.se)})")
        rows.append(r)
    t["robust"] = md_table(["Check", "Change θ, h = 6", "Change θ, h = 12"], rows)
    for _, d in rb.iterrows():
        n[f"rob_{d.spec}_{d.h}"] = f2(d.beta)
        if not np.isnan(d.se):
            n[f"rob_{d.spec}_{d.h}_se"] = f2(d.se)
    nl = rb[rb.se.notna()]
    for h in (6, 12):
        n[f"rob_min{h}"] = f2(nl[nl.h == h].beta.min())
        n[f"rob_max{h}"] = f2(nl[nl.h == h].beta.max())
    loo = rb[rb.spec == "l_loo"]
    for _, d in loo.iterrows():
        n[f"rob_loo_lo_{d.h}"], n[f"rob_loo_hi_{d.h}"] = f2(d.lo), f2(d.hi)
    for h in (6, 12):
        put(f"rob_placebo_{h}", "n_placebo_2016m3", h, "shock_x_placebo")
        put(f"rob_sep_pre_{h}", "m_separate_pre", h)
        put(f"rob_sep_post_{h}", "m_separate_post", h)
        put(f"rob_asym_{h}", "j_asymmetry", h, "shock_x_fpos")
        for spec in ["h_end_2024m6", "i_symmetric_2012", "b_viet5", "d_macro_controls"]:
            put(f"rob_post_{spec}_{h}", spec + "_postparam", h)
            put(f"rob_pre_{spec}_{h}", spec, h)
    n["rob_n_sig6"] = int(sum(1 for _, d in rb[(rb.h == 6) & rb.se.notna()].iterrows() if d.lo > 0))
    n["rob_n_checks6"] = int(rb[(rb.h == 6) & rb.se.notna()].shape[0])
    n["rob_n_sig12"] = int(sum(1 for _, d in rb[(rb.h == 12) & rb.se.notna()].iterrows() if d.lo > 0))

    # ---- replication gate
    gate = pd.read_csv(T / "replication_gate.csv")
    t["gate"] = md_table(["Criterion", "Target", "Result", "Pass"],
                         [[r.criterion, r.target, r.estimate, "yes" if r.passed else "**no**"] for r in gate.itertuples()],
                         ["l", "l", "l", "l"])
    n["gate_n_pass"], n["gate_n"] = int(gate.passed.sum()), len(gate)
    diag = pd.read_csv(T / "replication_g3_diagnostic.csv").query("p == 1").set_index("sample")
    n["g3_peak_ratio"] = f2(diag.loc["insufficient", "peak"] / diag.loc["sufficient", "peak"])
    n["g3_impact_ratio"] = f2(diag.loc["insufficient", "impact_h0"] / diag.loc["sufficient", "impact_h0"])
    for s_ in ["insufficient", "sufficient", "low_poverty", "high_poverty"]:
        n[f"g3_peak_{s_}"] = f2(diag.loc[s_, "peak"], 3)
        n[f"g3_impact_{s_}"] = f2(diag.loc[s_, "impact_h0"], 3)
        n[f"g3_cum_{s_}"] = f2(diag.loc[s_, "cum_h0_5"], 3)
    d2 = pd.read_csv(T / "replication_g3_diagnostic.csv").query("p == 2").set_index("sample")
    n["g3_peak_ratio_p2"] = f2(d2.loc["insufficient", "peak"] / d2.loc["sufficient", "peak"])
    pv = pd.read_csv(T / "replication_pvar_irf.csv").query("sample == 'all' and response == 'RPI'")
    th = pv[pv.shock == "THAI"].set_index("h")
    n["g2_h1"], n["g2_h1_lo"], n["g2_h1_hi"] = f2(th.irf[1], 3), f2(th.lo[1], 3), f2(th.hi[1], 3)
    n["g2_h0"], n["g2_h6"] = f2(th.irf[0], 3), f2(th.irf[6], 3)
    lp = pd.read_csv(T / "replication_lp_indicative.csv").set_index("h")
    for h in (1, 3, 6):
        n[f"ind_lp_{h}"] = f2(lp.beta[h])
    t1 = pd.read_csv(T / "replication_table1.csv")
    n["g1_max_dev"] = f2(t1[t1.variable == "cpi_rice"].dev_mean.abs().max(), 3)
    ch = json.loads((T / "replication_choice.json").read_text())
    n["g1b_other_dev"] = f2(ch["fuel_median_abs_dev"]["cpi_fuel_hh"], 1)

    # ---- episode
    for k, v in ep.items():
        n["ep_" + k] = v if isinstance(v, str) else (f2(v, 1) if abs(v) >= 1 else f2(v, 2))
    n["ep_e1_share_world_m12"] = f"{100 * ep['e1_actual_m12'] / ep['e1_pred_world_m12']:.0f}"
    n["ep_e1_share_total_m12"] = f"{100 * ep['e1_actual_m12'] / ep['e1_pred_total_m12']:.0f}"
    n["ep_e1_share_total_m6"] = f"{100 * ep['e1_actual_m6'] / ep['e1_pred_total_m6']:.0f}"
    n["ep_e1_missing_m12"] = f2(ep["e1_actual_m12"] - ep["e1_pred_total_m12"], 1)
    n["ep_e3_rice_spend"] = f"{ep['e3_rice_spend']:,.0f}"
    n["ep_e3_saving_tariff_m12"] = f"{ep['e3_saving_tariff_m12']:,.0f}"
    n["ep_e3_full_tariff_wedge"] = f"{ep['e3_full_tariff_wedge']:,.0f}"
    n["ep_e3_saving_actual_m12"] = f"{ep['e3_saving_actual_m12']:,.0f}"
    n["ep_threshold"] = f"{ep['threshold']:,.0f}"
    e2 = pd.read_csv(T / "episode_e2_regions.csv")
    t["ep_regions"] = md_table(["Region", "Actual change, 6 months", "Actual change, 12 months",
                                "Predicted, 12 months", "Actual − predicted"],
                               [[r.region, f2(r.actual_m6, 1), f2(r.actual_m12, 1), f2(r.pred_total_m12, 1),
                                 f2(r.unexplained_m12, 1)] for r in e2.itertuples()])
    n["ep_n_regions_below_pred"] = int((e2.actual_m12 < e2.pred_total_m12).sum())

    # ---- descriptive
    sp = pd.read_csv(T / "desc_subperiods.csv")
    rows = []
    for per in sp.period.unique():
        d = sp[sp.period == per].set_index("variable")
        rows.append([per, f2(d.loc["dl_rice", "annualised_mean"], 1), f2(d.loc["dl_rice", "sd"]),
                     f2(d.loc["f", "annualised_mean"], 1), f2(d.loc["f", "sd"]), int(d.loc["dl_rice", "months"])])
    t["desc_periods"] = md_table(["Period", "Rice CPI, % a year", "Rice CPI, SD monthly", "World rice (PHP), % a year",
                                  "World, SD monthly", "Months"], rows)
    for per, key in [("2009M1-2019M2 (quotas)", "quota"), ("2019M3-2024M6 (35% tariff)", "tariff35"),
                     ("2024M7-2026M9 (15% tariff, suspension, indexed tariff)", "late"), ("1995M1-2007M9", "early")]:
        d = sp[sp.period == per].set_index("variable")
        n[f"desc_sd_rice_{key}"] = f2(d.loc["dl_rice", "sd"])
        n[f"desc_mean_rice_{key}"] = f2(d.loc["dl_rice", "annualised_mean"], 1)
    an = pd.read_csv(T / "desc_annual.csv").set_index("year")
    for y in [2008, 2018, 2019, 2023, 2024, 2025, 2026]:
        for c in ["rice_all", "rice_b30", "headline_all", "headline_b30", "rice_contrib_all", "rice_contrib_b30"]:
            n[f"ann_{c}_{y}"] = f2(an.loc[y, c], 1) if y in an.index and not np.isnan(an.loc[y, c]) else "n.a."
    rows = [[y, f2(r.rice_all, 1), f2(r.rice_b30, 1), f2(r.headline_all, 1), f2(r.headline_b30, 1),
             f2(r.world_rice_php, 1), f2(r.rice_contrib_all, 2), f2(r.rice_contrib_b30, 2)]
            for y, r in an.loc[2012:].iterrows()]
    t["desc_annual"] = md_table(["Year", "Rice, all", "Rice, bottom 30%", "Headline, all", "Headline, bottom 30%",
                                 "World rice (PHP)", "Rice contribution, all", "Rice contribution, bottom 30%"], rows)
    epi = pd.read_csv(T / "desc_episodes.csv")
    epi = epi[epi.start >= "1995-01"]
    t["desc_episodes"] = md_table(["Start", "End", "Months", "Peak 12-month rise, world (%)", "World change (log pts)",
                                   "Rice CPI change (log pts)"],
                                  [[r.start, r.end, r.months, f2(r.peak_world_yoy, 0), f2(r.world_change, 1),
                                    f2(r.rice_cpi_change, 1)] for r in epi.itertuples()])
    n["desc_n_episodes"] = len(epi)
    disp = pd.read_csv(T / "desc_dispersion.csv").set_index("year")
    n["cv_2015_17"] = f2(disp.loc[2015:2017, "cv_retail_rmr_level_across_regions"].mean(), 1)
    n["cv_2021_24"] = f2(disp.loc[2021:2024, "cv_retail_rmr_level_across_regions"].mean(), 1)
    n["cv_2026"] = f2(disp.loc[2026, "cv_retail_rmr_level_across_regions"], 1)
    cc = pd.read_csv(T / "desc_crosscorr.csv")
    for reg in ["pre", "post"]:
        d = cc[(cc.regime == reg) & (cc.k >= 0)]
        n[f"cc_{reg}_max"] = f2(d["corr"].max())
        n[f"cc_{reg}_kmax"] = int(d.loc[d["corr"].idxmax(), "k"])
    pv_ = pd.read_csv(T / "proxy_validation.csv")
    n["val_thai_viet"] = f2(pv_.corr_monthly_change.iloc[0])
    n["val_cpi_retail"] = f2(pv_.corr_monthly_change.iloc[1])
    n["val_all_b30"] = f2(pv_.corr_monthly_change.iloc[3], 3)
    adf = pd.read_csv(T / "desc_adf.csv")
    n["adf_rice_level_p"] = f2(adf.p_value.iloc[0])
    groups = pd.read_csv(T / "region_groups.csv")
    t["groups"] = md_table(["Region", "Poverty 2015 (%)", "Poverty class", "Self-sufficiency index", "Rice supply",
                            "Rice weight, all (%)", "Rice weight, bottom 30% (%)"],
                           [[r.region, f2(r.poverty_2015, 1), r.poverty_class, f2(r.self_sufficiency_index),
                             "deficit" if r.insuff else "surplus", f2(r.w_rice_all, 1), f2(r.w_rice_b30, 1)]
                            for r in groups.itertuples()])
    n["n_insuff"], n["n_highpov"] = int(groups.insuff.sum()), int(groups.highpov.sum())

    # strip raw helper floats before saving
    clean = {k: v for k, v in n.items() if not k.endswith("_raw")}
    (T / "paper_numbers.json").write_text(json.dumps(clean, indent=1, default=str, ensure_ascii=False))
    (T / "paper_tables.json").write_text(json.dumps(t, indent=1, ensure_ascii=False))
    return clean, t
