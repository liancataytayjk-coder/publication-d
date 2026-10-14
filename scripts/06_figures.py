"""All figures, black and white, no titles inside the images (captions live in the documents).

Reads only saved outputs (output/tables/*.csv) and the processed panels; writes
output/figures/<name>.{png,tiff,pdf} via rtl.fig_style.save (byte-stable PDFs).
"""

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rtl.fig_style import A, B, C, LIGHT, MID, irf, save, setup, zero  # noqa: E402

T, F, P = ROOT / "output/tables", ROOT / "output/figures", ROOT / "data/processed"
EST = pd.read_csv(T / "estimates.csv")
M = lambda s: pd.Period(s, "M")  # noqa: E731


def q(spec, term="shock", outcome=None, rq=None):
    d = EST[(EST.spec == spec) & (EST.term == term)]
    if outcome:
        d = d[d.outcome == outcome]
    if rq:
        d = d[d.rq == rq]
    return d.sort_values("h")


def policy_lines(ax, labels=True):
    tr = ax.get_xaxis_transform()  # x in data, y in axes fraction
    for (m, lab), yy, ha in zip([("2019-03", "RTL (Mar 2019)"), ("2024-07", "15% tariff"),
                                 ("2025-09", "Import suspension")], (0.99, 0.99, 0.88), ("right", "right", "left")):
        x = M(m).to_timestamp()
        ax.axvline(x, color="0.0", linestyle=":", linewidth=0.8)
        if labels:
            ax.text(x, yy, (lab + " ") if ha == "right" else (" " + lab), transform=tr, fontsize=7, va="top", ha=ha)


def fig_framework():
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    ax.set_xlim(0, 10.4), ax.set_ylim(0, 6.6), ax.axis("off")

    def box(x, y, w, h, text, dashed=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06", fill=False,
                                    linestyle="--" if dashed else "-", linewidth=0.9))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=7.3)

    def arrow(x0, y0, x1, y1, dashed=False):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", linewidth=0.9, linestyle="--" if dashed else "-",
                                    shrinkA=2, shrinkB=2))

    box(0.1, 3.3, 1.9, 0.9, "World rice price\n(Thai 5%, USD)")
    box(0.1, 1.7, 1.9, 0.9, "Peso–dollar\nrate $E$")
    box(2.7, 2.5, 2.1, 0.9, "Import parity price\n$(1+\\tau)\\,E\\,P^W$")
    box(5.5, 3.7, 2.1, 0.9, "Wholesale and\nretail rice prices")
    box(5.5, 1.3, 2.1, 0.9, "Farmgate palay\nprice")
    box(8.2, 3.7, 2.1, 0.9, "Rice CPI and CPI\n(all; bottom 30%)")
    box(8.2, 1.3, 2.1, 0.9, "Farm income")
    box(2.7, 4.6, 2.1, 1.0, "Border regime:\nquota (to Feb 2019)\nor tariff $\\tau$", dashed=True)
    box(2.7, 0.3, 2.1, 1.0, "Import suspension,\nprice cap,\nNFA stocks", dashed=True)
    arrow(2.0, 3.75, 2.7, 3.15), arrow(2.0, 2.15, 2.7, 2.75)
    arrow(4.8, 3.15, 5.5, 4.0), arrow(4.8, 2.75, 5.5, 1.9)
    arrow(7.6, 4.15, 8.2, 4.15), arrow(7.6, 1.75, 8.2, 1.75)
    arrow(6.55, 2.2, 6.55, 3.7)
    arrow(3.75, 4.6, 3.75, 3.4, dashed=True), arrow(3.75, 1.3, 3.75, 2.5, dashed=True)
    ax.text(5.2, 6.4, "Pass-through $B_h$: the share of a 1% change in $E\\,P^W$ that reaches each price "
            "within $h$ months", ha="center", fontsize=7.3, style="italic")
    save(fig, "fig01_framework", F)


def fig_long_run():
    nat = pd.read_parquet(P / "panel_national.parquet")
    nat = nat[(nat.month >= M("1995-01")) & (nat.month <= M("2026-09"))].copy()
    base = nat[nat.month.dt.year == 2018]
    x = nat.month.dt.to_timestamp()
    fig, ax = plt.subplots(figsize=(6.3, 3.0))
    ax.plot(x, 100 * nat.cpi_rice / base.cpi_rice.mean(), color="0.0", linewidth=1.3, label="Rice CPI (PSA)")
    ax.plot(x, 100 * nat.thai5_php / base.thai5_php.mean(), color="0.0", linestyle="--", linewidth=0.9,
            label="World rice price in pesos (Thai 5%)")
    ax.set_yscale("log")
    ax.set_yticks([25, 50, 100, 200]), ax.set_yticklabels(["25", "50", "100", "200"])
    ax.yaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_ylabel("Index, 2018 average = 100 (log scale)")
    policy_lines(ax)
    ax.legend(loc="lower right")
    save(fig, "fig02_long_run", F)


def fig_gap():
    g = pd.read_csv(T / "rq3_gap_series.csv")
    x = pd.PeriodIndex(g.month, freq="M").to_timestamp()
    fig, ax = plt.subplots(figsize=(6.3, 2.8))
    ax.plot(x, g.gap_wholesale, color="0.0", linewidth=1.1, label="Wholesale RMR")
    ax.plot(x, g.gap_retail, color="0.0", linestyle="--", linewidth=0.9, label="Retail RMR")
    r = pd.read_csv(T / "rq3_gap.csv")
    ax.set_ylabel("100 × ln(domestic / world price)")
    policy_lines(ax)
    ax.legend(loc="upper left")
    save(fig, "fig03_border_gap", F)


def fig_rq1():
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    irf(ax, q("main"), A, "Before the law (1995–Feb 2019)")
    irf(ax, q("main_postparam"), B, "After the law (Mar 2019–2026)", band="lines")
    ax.set_ylabel("Percentage points per 1% world price rise")
    ax.legend(loc="upper left")
    save(fig, "fig04_rq1_passthrough", F)


def fig_rq2():
    fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.6), sharey=True)
    for ax, (y, lab) in zip(axes, [("dl_farmgate_palay", "Farmgate palay"), ("dl_wholesale_rmr", "Wholesale RMR"),
                                   ("dl_retail_rmr", "Retail RMR")]):
        irf(ax, q("chain_national", outcome=y), A, "Before the law (2011–Feb 2019)")
        irf(ax, q("chain_national_postparam", outcome=y), B, "After the law", band="lines")
        ax.text(0.03, 0.97, lab, transform=ax.transAxes, va="top", fontsize=8)
    axes[0].set_ylabel("Percentage points per 1%")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=2, fontsize=7.5, bbox_to_anchor=(0.5, -0.02))
    save(fig, "fig05_rq2_chain", F)


def fig_rq5():
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.8))
    irf(axes[0], q("all_items"), A, "All income households")
    irf(axes[0], q("all_items_b30"), B, "Bottom 30%", band="lines")
    axes[0].set_ylabel("Percentage points per 1%")
    axes[0].legend(loc="upper left", fontsize=7)
    irf(axes[1], q("gap_full"), A, "Gap, all income minus bottom 30%")
    axes[1].legend(loc="lower left", fontsize=7)
    save(fig, "fig06_rq5_poor", F)


def fig_rq4():
    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    irf(ax, q("het_insuff", term="shock_x_post_insuff"), A, "Rice-deficit regions")
    irf(ax, q("het_highpov", term="shock_x_post_highpov"), B, "High-poverty regions", band="lines")
    ax.set_ylabel("Extra change after the law (pp per 1%)")
    ax.legend(loc="upper left")
    save(fig, "fig07_rq4_regions", F)


ROB_LABELS = [("main", "Baseline"), ("a_real_shock", "(a) Real shock"), ("b_viet5", "(b) Viet 5%"),
              ("c_usd_fx_control", "(c) USD price + FX control"), ("d_macro_controls", "(d) Macro controls"),
              ("e_p6", "(e) 6 lags"), ("e_p18", "(e) 18 lags"), ("f_no_2008crisis", "(f) Without 2007–08 crisis"),
              ("g_no_2020", "(g) Without 2020"), ("h_end_2024m6", "(h) Ending June 2024"),
              ("i_symmetric_2012", "(i) 2012–2026 window"), ("j_asymmetry", "(j) Asymmetry"),
              ("k_drop_newgeo", "(k) Drop chained 2026"), ("o_cluster_region", "(o) Clustered SE")]


def robustness_table():
    rows = []
    for spec, lab in ROB_LABELS:
        for h in (6, 12):
            d = EST[(EST.spec == spec) & (EST.h == h) & (EST.term == "shock_x_post")]
            rows.append(dict(spec=spec, label=lab, h=h, beta=d.beta.iloc[0], se=d.se.iloc[0], lo=d.lo.iloc[0],
                             hi=d.hi.iloc[0]))
    loo = EST[EST.spec.str.startswith("l_loo") & (EST.term == "shock_x_post")]
    for h in (6, 12):
        d = loo[loo.h == h]
        rows.append(dict(spec="l_loo", label="(l) Leave one region out (range)", h=h, beta=d.beta.median(),
                         se=np.nan, lo=d.beta.min(), hi=d.beta.max()))
    sep = {h: (q("m_separate_post").set_index("h").loc[h], q("m_separate_pre").set_index("h").loc[h]) for h in (6, 12)}
    for h, (po, pr) in sep.items():
        b, s = po.beta - pr.beta, np.sqrt(po.se ** 2 + pr.se ** 2)
        rows.append(dict(spec="m_separate", label="(m) Separate pre/post models", h=h, beta=b, se=s,
                         lo=b - 1.645 * s, hi=b + 1.645 * s))
    out = pd.DataFrame(rows)
    out.to_csv(T / "robustness_theta.csv", index=False, float_format="%.4f")
    return out


def fig_robust():
    rb = robustness_table()
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 4.2), sharey=True)
    labels = rb[rb.h == 6].label.tolist()
    y = np.arange(len(labels))[::-1]
    for ax, h in zip(axes, (6, 12)):
        d = rb[rb.h == h]
        ax.hlines(y, d.lo, d.hi, color="0.0", linewidth=0.9)
        ax.plot(d.beta, y, "o", color="0.0", markersize=4, markerfacecolor="0.0")
        ax.axvline(0, color="0.0", linewidth=0.6)
        ax.axvline(d.beta.iloc[0], color=MID, linewidth=0.6, linestyle="--")
        ax.text(0.98, 0.99, f"h = {h} months", transform=ax.transAxes, ha="right", va="top", fontsize=8)
    fig.supxlabel("Change in cumulative pass-through after the law (pp per 1% world price rise)", fontsize=8.5)
    axes[0].set_yticks(y), axes[0].set_yticklabels(labels, fontsize=7.5)
    save(fig, "fig08_robustness", F)


def fig_episode_tariff():
    e = pd.read_csv(T / "episode_e1_national.csv")
    x = np.arange(1, len(e) + 1)
    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    ax.plot(x, e.actual, **A, label="Actual rice CPI")
    ax.plot(x, e.pred_world_only, **B, label="Predicted: world prices only")
    ax.plot(x, e.pred_total, **C, label="Predicted: world prices + tariff cut")
    zero(ax)
    ax.set_xticks(x), ax.set_xticklabels([m[2:4] + "/" + m[5:] for m in e.month], fontsize=7, rotation=45)
    ax.set_xlabel("Month (yy/mm)")
    ax.set_ylabel("Change since June 2024 (log points)")
    ax.legend(loc="lower left", fontsize=7.5)
    save(fig, "fig09_episode_tariff_cut", F)


def fig_episode_suspension():
    e = pd.read_csv(T / "episode_e4_suspension.csv")
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.9), sharey=True)
    for ax, s, lab in [(axes[0], "farmgate_palay", "Farmgate palay"), (axes[1], "retail_rmr", "Retail RMR")]:
        d = e[e.series == s]
        x = np.arange(1, len(d) + 1)
        ax.plot(x, d.actual, **A, label="Actual")
        ax.plot(x, d.pred_world_only, **B, label="Predicted from world prices")
        ax.axvspan(0.5, 4.5, color=LIGHT, linewidth=0)
        zero(ax)
        ax.set_xticks(x[::2]), ax.set_xticklabels([m[2:4] + "/" + m[5:] for m in d.month.iloc[::2]], fontsize=7)
        ax.text(0.03, 0.97, lab, transform=ax.transAxes, va="top", fontsize=8)
        ax.set_xlabel("Month (yy/mm)")
    axes[0].set_ylabel("Change since August 2025 (log points)")
    axes[1].legend(loc="lower right", fontsize=7)
    save(fig, "fig10_episode_suspension", F)


def fig_regions_episode():
    e = pd.read_csv(T / "episode_e2_regions.csv").sort_values("actual_m12", ascending=False)
    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    y = np.arange(len(e))
    ax.barh(y, e.actual_m12, color=LIGHT, edgecolor="0.0", linewidth=0.6, height=0.7)
    ax.axvline(e.pred_total_m12.iloc[0], color="0.0", linestyle="--", linewidth=0.9)
    ax.text(e.pred_total_m12.iloc[0], -1.0, "Predicted (world + tariff) ", fontsize=7, va="center", ha="right")
    ax.set_ylim(-1.6, len(e) - 0.4)
    ax.set_yticks(y), ax.set_yticklabels(e.region, fontsize=7.5)
    zero(ax, horizontal=False)
    ax.set_xlabel("Change in rice CPI, June 2024 to June 2025 (log points)")
    save(fig, "fig11_regions_episode", F)


def fig_validation():
    t1 = pd.read_csv(T / "replication_table1.csv")
    pv = pd.read_csv(T / "replication_pvar_irf.csv")
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.9))
    r = t1[t1.variable == "cpi_rice"]
    axes[0].plot(r.target_mean, r.est_mean, "o", color="0.0", markersize=4, label="Rice CPI, mean")
    axes[0].plot(r.target_sd, r.est_sd, "s", color="0.0", markerfacecolor="white", markersize=4, label="Rice CPI, SD")
    lim = [15, 80]
    axes[0].plot(lim, lim, color=MID, linewidth=0.6)
    axes[0].set_xlabel("Antonio et al. (2024), Table 1"), axes[0].set_ylabel("This study")
    axes[0].legend(loc="upper left", fontsize=7)
    d = pv[(pv["sample"] == "all") & (pv.response == "RPI") & (pv.shock == "THAI")]
    axes[1].fill_between(d.h, d.lo, d.hi, color=LIGHT, linewidth=0)
    axes[1].plot(d.h, d.irf, **A)
    zero(axes[1])
    axes[1].set_xlabel("Months after the shock"), axes[1].set_ylabel("Rice inflation, pp")
    save(fig, "fig12_validation", F)


def fig_descriptive():
    cc = pd.read_csv(T / "desc_crosscorr.csv")
    fig, ax = plt.subplots(figsize=(5.5, 2.8))
    for reg, st, lab in [("pre", A, "Before the law"), ("post", B, "After the law")]:
        d = cc[cc.regime == reg]
        ax.plot(d.k, d["corr"], label=lab, **st)
    zero(ax)
    ax.set_xticks(range(-6, 13, 2))
    ax.set_xlabel("k: months by which rice inflation follows the world shock")
    ax.set_ylabel("Correlation")
    ax.legend(loc="upper right")
    save(fig, "fig13_crosscorr", F)

    disp = pd.read_csv(T / "desc_dispersion.csv").dropna()
    fig, ax = plt.subplots(figsize=(5.5, 2.8))
    ax.plot(disp.year, disp.cv_retail_rmr_level_across_regions, **A)
    ax.axvline(2019, color="0.0", linestyle=":", linewidth=0.8)
    ax.text(2019.1, ax.get_ylim()[1], " RTL", fontsize=7, va="top")
    ax.set_xlabel("Year"), ax.set_ylabel("Coefficient of variation (%)")
    save(fig, "fig14_regional_dispersion", F)


def main():
    setup()
    fig_framework()
    fig_long_run()
    fig_gap()
    fig_rq1()
    fig_rq2()
    fig_rq5()
    fig_rq4()
    fig_robust()
    fig_episode_tariff()
    fig_episode_suspension()
    fig_regions_episode()
    fig_validation()
    fig_descriptive()
    print("figures:", sorted(p.name for p in F.glob("*.png")))


if __name__ == "__main__":
    main()
