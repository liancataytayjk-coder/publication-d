"""Clean the raw PSA downloads into long tables (geography x item x month).

Writes to data/processed/:
  cpi_long.parquet     geo, coding (old/new geographic code), group (all/b30), item, month, value
  cpi_weights.parquet  geo, coding, group, item, weight (2018 basket, percent of all items)
  prices_long.parquet  level (retail/wholesale/farmgate), source (raw file), commodity, geo, month, value (PHP/kg)
Geography labels are mapped to canonical names with rtl.regions.canon; nothing else
is changed. Missing cells ('..', '', '-') become NaN.
"""

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rtl.regions import canon  # noqa: E402

RAW = ROOT / "data/raw/psa"
OUT = ROOT / "data/processed"
MON = {m[:3].lower(): i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
     "November", "December"])}
ITEMS = [(r"^0 - ALL ITEMS", "all"), (r"^01 - FOOD AND", "food_bev"), (r"^01\.1 - FOOD", "food"),
         (r"^01\.1\.1\.12 - Rice", "rice"), (r"^04\.5 - ", "fuel_hh"), (r"^07\.2\.2 - ", "fuel_tr")]
CPI_FILES = {  # file: (coding, group)
    "cpi_all_2018old_backcast_1994_2017": ("old", "all"),
    "cpi_all_2018old_2018_2025": ("old", "all"),
    "cpi_all_2018new_2018_2026": ("new", "all"),
    "cpi_b30_2018old_backcast_allitems_2000_2011": ("old", "b30"),
    "cpi_b30_2018old_backcast_2012_2017": ("old", "b30"),
    "cpi_b30_2018old_2018_2025": ("old", "b30"),
    "cpi_b30_2018new_2018_2026": ("new", "b30"),
}
WEIGHT_FILES = {"cpi_all_2018old_weights": ("old", "all"), "cpi_all_2018new_weights": ("new", "all"),
                "cpi_b30_2018old_weights": ("old", "b30")}
PRICE_FILES = {
    "retail_cereals_oldseries_1990_2021": "retail", "retail_cereals_2012based_2012_2021": "retail",
    "retail_cereals_2018based_oldgeo_2018_2025": "retail", "retail_cereals_2018based_newgeo_2018_2026": "retail",
    "wholesale_cereals_oldgeo_2010_2025": "wholesale", "wholesale_cereals_newgeo_2010_2026": "wholesale",
    "farmgate_cereals_oldseries_1990_2020": "farmgate", "farmgate_cereals_newseries_2010_2026": "farmgate",
}


def item_of(label):
    for pat, name in ITEMS:
        if re.search(pat, label):
            return name
    return None


def to_num(s):
    return pd.to_numeric(s.astype(str).str.strip().replace({"..": np.nan, "": np.nan, "-": np.nan, "...": np.nan}),
                         errors="coerce")


def melt_wide(df, id_cols):
    """PxWeb CSV with time in columns like '1994 Jan' or '2012 January' -> long with a month column."""
    long = df.melt(id_vars=id_cols, var_name="time", value_name="value")
    m = long["time"].str.extract(r"^(\d{4})\s+([A-Za-z]+)")
    long["year"] = pd.to_numeric(m[0], errors="coerce")
    long["mon"] = m[1].str[:3].str.lower().map(MON)
    long = long.dropna(subset=["year", "mon"])
    long["month"] = pd.PeriodIndex.from_fields(year=long["year"].astype(int), month=long["mon"].astype(int), freq="M")
    long["value"] = to_num(long["value"])
    return long.drop(columns=["time", "year", "mon"])


def long_format(df):
    """Some tables come with year/period as columns rather than in the header; normalise."""
    cols = list(df.columns)
    if any(re.match(r"^\d{4}\s+[A-Za-z]+", c) for c in cols):
        id_cols = [c for c in cols if not re.match(r"^\d{4}\s+", c)]
        return melt_wide(df, id_cols)
    raise ValueError(f"unrecognised layout: {cols[:6]}")


def clean_cpi():
    frames = []
    for f, (coding, group) in CPI_FILES.items():
        d = pd.read_csv(RAW / f"{f}.csv.gz", dtype=str, keep_default_na=False)
        geo_col, item_col = d.columns[0], d.columns[1]
        d = long_format(d)
        d["geo"] = d[geo_col].map(canon)
        d["item"] = d[item_col].map(item_of)
        d["coding"], d["group"], d["file"] = coding, group, f
        frames.append(d[["geo", "coding", "group", "item", "month", "value", "file"]])
    cpi = pd.concat(frames, ignore_index=True).dropna(subset=["geo", "item", "value"])
    # overlapping files of the same coding/group (backcast vs current) do not overlap in months;
    # check, then keep one row per key
    dup = cpi.duplicated(["geo", "coding", "group", "item", "month"], keep=False)
    if dup.any():
        raise SystemExit(f"duplicate CPI keys: {cpi[dup].head()}")
    return cpi.drop(columns="file")


def clean_weights():
    frames = []
    for f, (coding, group) in WEIGHT_FILES.items():
        p = RAW / f"{f}.csv.gz"
        if not p.exists():
            continue
        d = pd.read_csv(p, dtype=str, keep_default_na=False)
        d.columns = ["geo_label", "item_label", "weight"]
        d["geo"] = d["geo_label"].map(canon)
        d["item"] = d["item_label"].map(item_of)
        d["weight"] = to_num(d["weight"])
        d["coding"], d["group"] = coding, group
        frames.append(d.dropna(subset=["geo", "item"])[["geo", "coding", "group", "item", "item_label", "weight"]])
    return pd.concat(frames, ignore_index=True)


def clean_prices():
    frames = []
    for f, level in PRICE_FILES.items():
        p = RAW / f"{f}.csv.gz"
        if not p.exists():
            print("missing", p)
            continue
        d = pd.read_csv(p, dtype=str, keep_default_na=False)
        geo_col, com_col = d.columns[0], d.columns[1]
        if "year" in [c.lower() for c in d.columns]:  # long layout: geo, commodity, year, period, value
            yc = [c for c in d.columns if c.lower() == "year"][0]
            pc = [c for c in d.columns if c.lower() == "period"][0]
            vc = [c for c in d.columns if c not in (geo_col, com_col, yc, pc)][0]
            d = d.rename(columns={vc: "value"})
            d["mon"] = d[pc].str[:3].str.lower().map(MON)
            d = d.dropna(subset=["mon"])
            d["month"] = pd.PeriodIndex.from_fields(year=d[yc].astype(int), month=d["mon"].astype(int), freq="M")
            d["value"] = to_num(d["value"])
        else:
            d = long_format(d)
        d["geo"] = d[geo_col].map(canon)
        d["commodity"] = d[com_col].str.strip()
        d["level"], d["source"] = level, f
        frames.append(d.dropna(subset=["geo", "value"])[["level", "source", "commodity", "geo", "month", "value"]])
    return pd.concat(frames, ignore_index=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cpi = clean_cpi()
    cpi.to_parquet(OUT / "cpi_long.parquet", index=False)
    w = clean_weights()
    w.to_parquet(OUT / "cpi_weights.parquet", index=False)
    pr = clean_prices()
    pr.to_parquet(OUT / "prices_long.parquet", index=False)
    print("CPI rows", len(cpi), cpi.groupby(["coding", "group", "item"]).month.agg(["min", "max", "count"]).to_string())
    print("weights", w.groupby(["coding", "group"]).size().to_dict())
    print(pr.groupby(["level", "source", "commodity"]).month.agg(["min", "max", "count"]).to_string())


if __name__ == "__main__":
    main()
