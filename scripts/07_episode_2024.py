"""Objective 3: the 2024 tariff cut (E1-E3) and the 2025 import suspension (E4).

E1  National rice CPI: predicted change from June 2024 to month m = sum_t B^post_{m-t} (f_t + tau_t),
    with B^post the cumulative post-law pass-through estimated on data ending 2024M6 (out of
    sample) and tau = 100 ln(1.15/1.35) in 2024M7 (EO 62). Compared with the actual change.
E2  The same by region, with the panel model estimated on data ending 2024M6.
E3  Pesos per month for a poverty-line family of five: PSA 2023 threshold (PHP 13,873) x the
    bottom-30% rice weight (2018) x the predicted change attributable to the tariff cut.
E4  (exploratory) Import suspension Sep-Dec 2025 and after: actual paths of farmgate, wholesale
    and retail prices against the paths predicted from world prices alone (full-sample
    post-law national models).
Writes output/tables/episode_*.csv and episode_numbers.json.
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rtl.lp import local_projection  # noqa: E402

P, T = ROOT / "data/processed", ROOT / "output/tables"
M = lambda s: pd.Period(s, "M")  # noqa: E731
TAU = 100 * np.log(1.15 / 1.35)
THRESHOLD = 13873.0  # PSA 2023, family of five, PHP per month (policy_context P13)


def post_B(df, y, unit, end, start="1995-01"):
    """Cumulative post-law B_h (h=0..12) from the re-parametrised regime model."""
    d = df.copy()
    d["pre"] = 1 - d.post
    mask = (d.month >= M(start)) & (d.month <= M(end))
    r = local_projection(d, y=y, x="f", time="t", unit=unit, horizons=12, p=12, interact=("pre",),
                         exog=("post",), sample=mask, cumulative=True,
                         se="driscoll_kraay" if unit else "newey_west")
    return r[r.term == "shock"].set_index("h").beta


def predict(B, shocks, months):
    """Predicted cumulative change from the month before months[0] to each month in months."""
    out = []
    for m in months:
        tot = 0.0
        for t in months:
            k = (m - t).n
            if 0 <= k <= 12:
                tot += B[k] * shocks.get(t, 0.0)
        out.append(tot)
    return np.array(out)


def main():
    nat = pd.read_parquet(P / "panel_national.parquet").sort_values("month").reset_index(drop=True)
    reg = pd.read_parquet(P / "panel_region.parquet").sort_values(["region", "month"]).reset_index(drop=True)
    w = pd.read_parquet(P / "cpi_weights.parquet")
    w_b30 = float(w[(w.geo == "Philippines") & (w.group == "b30") & (w["item"] == "rice")].weight.iloc[0])
    w_all = float(w[(w.geo == "Philippines") & (w.group == "all") & (w["item"] == "rice") & (w.coding == "old")]
                  .weight.iloc[0])
    nums = {"tau": TAU, "w_rice_b30": w_b30, "w_rice_all": w_all, "threshold": THRESHOLD}

    # ---------- E1: national ----------
    B = post_B(nat, "dl_rice", None, "2024-06")
    base = M("2024-06")
    months = pd.period_range("2024-07", "2025-06", freq="M")
    f = nat.set_index("month").f
    world = {m: f[m] for m in months}
    tariff = {M("2024-07"): TAU}
    both = {m: world[m] + tariff.get(m, 0.0) for m in months}
    lvl = nat.set_index("month").cpi_rice
    lvl_b30 = nat.set_index("month").cpi_rice_b30
    e1 = pd.DataFrame({"month": months.astype(str),
                       "actual": 100 * np.log(lvl[months].values / lvl[base]),
                       "actual_b30": 100 * np.log(lvl_b30[months].values / lvl_b30[base]),
                       "pred_world_only": predict(B, world, months),
                       "pred_tariff_only": predict(B, tariff, months),
                       "pred_total": predict(B, both, months)})
    e1.to_csv(T / "episode_e1_national.csv", index=False, float_format="%.4f")
    pd.DataFrame({"h": B.index, "B_post_to_2024m6": B.values}).to_csv(T / "episode_B_post.csv", index=False,
                                                                      float_format="%.5f")
    for k, mm in [("m6", "2024-12"), ("m12", "2025-06")]:
        r = e1[e1.month == mm].iloc[0]
        nums.update({f"e1_actual_{k}": r.actual, f"e1_actual_b30_{k}": r.actual_b30,
                     f"e1_pred_total_{k}": r.pred_total, f"e1_pred_tariff_{k}": r.pred_tariff_only,
                     f"e1_pred_world_{k}": r.pred_world_only,
                     f"e1_share_explained_{k}": r.pred_total / r.actual})
    nums["e1_B6"], nums["e1_B12"] = float(B[6]), float(B[12])

    # ---------- E2: regions ----------
    Bp = post_B(reg, "dl_rice", "region", "2024-06")
    rows = []
    for rname, g in reg.groupby("region"):
        s = g.set_index("month").cpi_rice
        rows.append(dict(region=rname, actual_m12=100 * np.log(s[M("2025-06")] / s[base]),
                         actual_m6=100 * np.log(s[M("2024-12")] / s[base])))
    e2 = pd.DataFrame(rows)
    e2["pred_total_m12"] = predict(Bp, both, months)[-1]
    e2["pred_tariff_m12"] = predict(Bp, tariff, months)[-1]
    e2["unexplained_m12"] = e2.actual_m12 - e2.pred_total_m12
    e2 = e2.sort_values("actual_m12").reset_index(drop=True)
    e2.to_csv(T / "episode_e2_regions.csv", index=False, float_format="%.4f")
    nums.update({"e2_pred_total_m12": float(e2.pred_total_m12.iloc[0]),
                 "e2_pred_tariff_m12": float(e2.pred_tariff_m12.iloc[0]),
                 "e2_largest_fall_region": e2.region.iloc[0], "e2_largest_fall": float(e2.actual_m12.iloc[0]),
                 "e2_smallest_fall_region": e2.region.iloc[-1], "e2_smallest_fall": float(e2.actual_m12.iloc[-1])})

    # ---------- E3: pesos ----------
    rice_spend = THRESHOLD * w_b30 / 100
    nums["e3_rice_spend"] = rice_spend
    nums["e3_saving_tariff_m12"] = -rice_spend * (np.exp(nums["e1_pred_tariff_m12"] / 100) - 1)
    nums["e3_saving_actual_m12"] = -rice_spend * (np.exp(nums["e1_actual_b30_m12"] / 100) - 1)
    nums["e3_full_tariff_wedge"] = -rice_spend * (np.exp(TAU / 100) - 1)

    # ---------- E4: suspension (exploratory) ----------
    start = M("2025-08")
    months4 = pd.period_range("2025-09", "2026-09", freq="M")
    world4 = {m: f[m] for m in months4}
    rows = []
    for y, lvlcol in [("dl_rice", "cpi_rice"), ("dl_farmgate_palay", "farmgate_palay"),
                      ("dl_wholesale_rmr", "wholesale_rmr"), ("dl_retail_rmr", "retail_rmr")]:
        Bf = post_B(nat, y, None, "2026-09", start="1995-01" if y == "dl_rice" else "2011-01")
        lv = nat.set_index("month")[lvlcol]
        pred = predict(Bf, world4, months4)
        for m, pv in zip(months4, pred):
            rows.append(dict(series=lvlcol, month=str(m), actual=100 * np.log(lv[m] / lv[start]),
                             pred_world_only=pv, level=lv[m]))
    e4 = pd.DataFrame(rows)
    e4.to_csv(T / "episode_e4_suspension.csv", index=False, float_format="%.4f")
    for s_ in ["cpi_rice", "farmgate_palay", "retail_rmr", "wholesale_rmr"]:
        q = e4[e4.series == s_].set_index("month")
        nums[f"e4_{s_}_dec25"] = float(q.loc["2025-12", "actual"])
        nums[f"e4_{s_}_apr26"] = float(q.loc["2026-04", "actual"])
        nums[f"e4_{s_}_sep26"] = float(q.loc["2026-09", "actual"])
        nums[f"e4_{s_}_pred_apr26"] = float(q.loc["2026-04", "pred_world_only"])
        nums[f"e4_{s_}_min"] = float(q.actual.min())
    lv = nat.set_index("month")
    nums["e4_rice_nov25_apr26"] = float(100 * np.log(lv.cpi_rice[M("2026-04")] / lv.cpi_rice[M("2025-11")]))
    nums["e4_world_nov25_apr26"] = float(100 * np.log(lv.thai5_php[M("2026-04")] / lv.thai5_php[M("2025-11")]))
    nums["e4_farm_aug25_sep25"] = float(100 * np.log(lv.farmgate_palay[M("2025-09")] / lv.farmgate_palay[M("2025-08")]))
    (T / "episode_numbers.json").write_text(json.dumps(nums, indent=2, default=float))
    print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in nums.items()}, indent=1))


if __name__ == "__main__":
    main()
