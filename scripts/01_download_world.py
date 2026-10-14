"""Download non-PSA sources unchanged: World Bank Pink Sheet, BSP peso-dollar rate, NOAA ONI.

Files go to data/raw/<source>/ exactly as served (the xlsx files are binary copies,
the ONI text file is gzipped). Every file is listed in data/raw/source_log.md.
"""

import gzip
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    ("https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx",
     "worldbank/CMO-Historical-Data-Monthly_2026-10.xlsx", False),
    ("https://www.bsp.gov.ph/Statistics/External/pesodollar.xlsx", "bsp/pesodollar_2026-10.xlsx", False),
    ("https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt", "noaa/oni_ascii_2026-10.txt.gz", True),
]


def get(url):
    for attempt in range(5):
        try:
            r = requests.get(url, timeout=120, headers={"User-Agent": "curl/8.5.0"})
            r.raise_for_status()
            return r.content
        except requests.RequestException:
            if attempt == 4:
                raise
            time.sleep(2 ** (attempt + 1))


def run(force=False):
    for url, rel, gz in FILES:
        out = ROOT / "data/raw" / rel
        if out.exists() and not force:
            print("exists:", out)
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        body = get(url)
        out.write_bytes(gzip.compress(body, mtime=0) if gz else body)
        print(f"wrote {out} ({len(body):,} bytes)")


if __name__ == "__main__":
    run(force="--force" in sys.argv)
