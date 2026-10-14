"""Download PSA OpenSTAT tables (CPI, rice retail/wholesale/farmgate prices) unchanged.

Each table is saved as a gzipped CSV under data/raw/psa/, national and regional rows
only, with only the commodities this study uses (the values are never altered).
Every file is listed in data/raw/source_log.md. Existing files are skipped unless
--force is given.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rtl.pxweb_download import main as pxweb  # noqa: E402

API = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/"
REGIONS = r"^(PHILIPPINES|\.\.[^.].*|NCR|AONCR|CAR|Region \w+|Reg\d+\w*|MIMAROPA REGION|BARMM|CARAGA|NIR)$"
CPI_ITEMS = r"^(0 - ALL ITEMS|01 - FOOD AND|01\.1 - FOOD|01\.1\.1\.12 - Rice|04\.5 - |07\.2\.2 - )"
RICE_RETAIL = r"(?i)^rice|milled rice"
PALAY = r"(?i)^palay"
COMMODITY = "Commodity Description"

TABLES = [
    # (table path, output name, extra args)
    ("PI/CPI/2018/0012M4ACP15.px", "cpi_all_2018old_backcast_1994_2017", ["--select", f"{COMMODITY}={CPI_ITEMS}"]),
    ("PI/CPI/2018/0012M4ACP09.px", "cpi_all_2018old_2018_2025", ["--select", f"{COMMODITY}={CPI_ITEMS}"]),
    ("PI/CPI/2018/0012M4ACP12.px", "cpi_all_2018old_weights", []),
    ("PI/CPI/2018NEW/0012M4ACP22.px", "cpi_all_2018new_2018_2026", ["--select", f"{COMMODITY}={CPI_ITEMS}"]),
    ("PI/CPI/2018NEW/0012M4ACP25.px", "cpi_all_2018new_weights", []),
    ("PI/BIH/2018/0022M4ABOT5.px", "cpi_b30_2018old_backcast_allitems_2000_2011", []),
    ("PI/BIH/2018/0022M4ABOT4.px", "cpi_b30_2018old_backcast_2012_2017", ["--select", f"{COMMODITY}={CPI_ITEMS}"]),
    ("PI/BIH/2018/0022M4ABOT1.px", "cpi_b30_2018old_2018_2025", ["--select", f"{COMMODITY}={CPI_ITEMS}"]),
    ("PI/BIH/2018/0022M4ABOT3.px", "cpi_b30_2018old_weights", []),
    ("PI/BIH/2018NEW/0022M4ABIR1.px", "cpi_b30_2018new_2018_2026", ["--select", f"{COMMODITY}={CPI_ITEMS}"]),
    ("RP/0042M4ARP01.px", "retail_cereals_oldseries_1990_2021", ["--select", f"Commodity={RICE_RETAIL}"]),
    ("NRP/0042M4ARN01.px", "retail_cereals_2012based_2012_2021", ["--select", f"Commodity={RICE_RETAIL}"]),
    ("2018/0042M4ARA01.px", "retail_cereals_2018based_oldgeo_2018_2025", ["--select", f"Commodity={RICE_RETAIL}"]),
    ("2018NEW/0042M4ARN01.px", "retail_cereals_2018based_newgeo_2018_2026", ["--select", f"Commodity={RICE_RETAIL}"]),
    ("NWS/0052M4AWA01.px", "wholesale_cereals_oldgeo_2010_2025", ["--select", f"Commodity={RICE_RETAIL}"]),
    ("NWSNEW/0052M4AWB01.px", "wholesale_cereals_newgeo_2010_2026", ["--select", f"Commodity={RICE_RETAIL}"]),
    ("FG/0032M4AFP01.px", "farmgate_cereals_oldseries_1990_2020", ["--select", f"Commodity={PALAY}"]),
    ("NFG/0032M4AFN01.px", "farmgate_cereals_newseries_2010_2026", ["--select", f"Commodity={PALAY}"]),
]


def run(force=False, only=None):
    for table, name, extra in TABLES:
        if only and only not in table + name:
            continue
        out = ROOT / "data/raw/psa" / f"{name}.csv.gz"
        args = [API, table, str(out), "--geo-regex", REGIONS] + extra + (["--force"] if force else [])
        print(">>", table)
        pxweb(args)


if __name__ == "__main__":
    only = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")), None)
    run(force="--force" in sys.argv, only=only)
