"""Clean the non-PSA sources into one monthly table: data/processed/world_monthly.parquet.

Columns: month (Period[M]), thai5, viet5, urea, dubai (US dollars per tonne or
barrel, Pink Sheet), fx (PHP per USD, BSP monthly average), oni (NOAA Oceanic Nino
Index, the anomaly of the 3-month season centred on that month).
"""

import gzip
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
          "October", "November", "December"]
ONI_CENTRE = {"DJF": 1, "JFM": 2, "FMA": 3, "MAM": 4, "AMJ": 5, "MJJ": 6, "JJA": 7, "JAS": 8,
              "ASO": 9, "SON": 10, "OND": 11, "NDJ": 12}
PINK = {"Rice, Thai 5%": "thai5", "Rice, Viet Namese 5%": "viet5", "Urea": "urea", "Crude oil, Dubai": "dubai",
        "Rice, Thai 25%": "thai25"}


def pink_sheet():
    x = pd.read_excel(RAW / "worldbank/CMO-Historical-Data-Monthly_2026-10.xlsx", "Monthly Prices", header=None)
    names = [str(v).strip() for v in x.iloc[4]]
    body = x.iloc[6:].copy()
    body.columns = names
    body = body[body.iloc[:, 0].astype(str).str.match(r"^\d{4}M\d{2}$")]
    out = pd.DataFrame({"month": pd.PeriodIndex(body.iloc[:, 0].str.replace("M", "-"), freq="M")})
    for name, col in PINK.items():
        out[col] = pd.to_numeric(body[name].replace("…", np.nan), errors="coerce").to_numpy()
    return out


def bsp_fx():
    x = pd.read_excel(RAW / "bsp/pesodollar_2026-10.xlsx", "monthly", header=None)
    x = x.iloc[7:, 1:4]
    x.columns = ["year", "mname", "fx"]
    x = x[x["mname"].isin(MONTHS)].copy()
    x["year"] = pd.to_numeric(x["year"], errors="coerce").ffill().astype(int)
    x["fx"] = pd.to_numeric(x["fx"], errors="coerce")
    x["month"] = pd.PeriodIndex.from_fields(year=x["year"], month=x["mname"].map(MONTHS.index) + 1, freq="M")
    return x[["month", "fx"]].dropna()


def oni():
    rows = gzip.open(RAW / "noaa/oni_ascii_2026-10.txt.gz").read().decode().split("\n")[1:]
    recs = []
    for r in rows:
        f = r.split()
        if len(f) == 4:
            recs.append((pd.Period(year=int(f[1]), month=ONI_CENTRE[f[0]], freq="M"), float(f[3])))
    return pd.DataFrame(recs, columns=["month", "oni"])


def main():
    w = pink_sheet().merge(bsp_fx(), on="month", how="left").merge(oni(), on="month", how="left")
    w = w[w["month"] >= pd.Period("1990-01", "M")].reset_index(drop=True)
    out = ROOT / "data/processed/world_monthly.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    w.to_parquet(out, index=False)
    print(w.tail(3).to_string())
    print("missing:", w.isna().sum().to_dict())


if __name__ == "__main__":
    main()
