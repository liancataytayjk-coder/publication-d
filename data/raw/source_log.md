# Raw data source log

All files were downloaded on 14 October 2026 by `scripts/01_download_psa.py` and
`scripts/01_download_world.py`. They are never edited. PSA files come from the PxWeb
API at `https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/` + the table id below.
To stay under the API cell limit, the PSA files keep only the national and regional
rows (no provinces) and only the items named in the Notes column. The values are as
served.

| File | Source / table id | Base, units | Coverage | Notes |
|---|---|---|---|---|
| psa/cpi_all_2018old_backcast_1994_2017.csv.gz | PSA OpenSTAT `PI/CPI/2018/0012M4ACP15.px` | CPI 2018 = 100, PSA backcast | 1994M1–2017M12; PH + 18 areas (17 regions + AONCR), old geographic code | Items: all items, 01 food & non-alcoholic beverages, 01.1 food, 01.1.1.12 rice, 04.5 electricity, gas & other fuels, 07.2.2 fuels & lubricants for transport |
| psa/cpi_all_2018old_2018_2025.csv.gz | `PI/CPI/2018/0012M4ACP09.px` | CPI 2018 = 100 | 2018M1–2025M12; old code | Same items |
| psa/cpi_all_2018old_weights.csv.gz | `PI/CPI/2018/0012M4ACP12.px` | % of all items, 2018 basket | old code | All 354 items |
| psa/cpi_all_2018new_2018_2026.csv.gz | `PI/CPI/2018NEW/0012M4ACP22.px` | CPI 2018 = 100 | 2018M1–2026M9; new geographic code (adds NIR; VI and VII lose Negros) | Same items as old-code files |
| psa/cpi_all_2018new_weights.csv.gz | `PI/CPI/2018NEW/0012M4ACP25.px` | % of all items | new code | All items |
| psa/cpi_b30_2018old_backcast_allitems_2000_2011.csv.gz | `PI/BIH/2018/0022M4ABOT5.px` | Bottom-30% CPI 2018 = 100, backcast | 2000M1–2011M12; old code | All items only |
| psa/cpi_b30_2018old_backcast_2012_2017.csv.gz | `PI/BIH/2018/0022M4ABOT4.px` | Bottom-30% CPI 2018 = 100, backcast | 2012M1–2017M12 | Same six items |
| psa/cpi_b30_2018old_2018_2025.csv.gz | `PI/BIH/2018/0022M4ABOT1.px` | Bottom-30% CPI 2018 = 100 | 2018M1–2025M12 | Region XII labelled "Reg12" in this table (first pull missed it; re-pulled with a wider label pattern) |
| psa/cpi_b30_2018old_weights.csv.gz | `PI/BIH/2018/0022M4ABOT3.px` | % of all items, bottom-30% basket | old code | "Reg12" as above |
| psa/cpi_b30_2018new_2018_2026.csv.gz | `PI/BIH/2018NEW/0022M4ABIR1.px` | Bottom-30% CPI 2018 = 100 | 2018M1–2026M9; new code | Region labels "Region 1" … "Region 12" |
| psa/retail_cereals_oldseries_1990_2021.csv.gz | `RP/0042M4ARP01.px` | PHP per kg | 1990–2021, monthly | Rice: special, premium, well-milled (WMR), regular-milled (RMR) |
| psa/retail_cereals_2012based_2012_2021.csv.gz | `NRP/0042M4ARN01.px` | PHP per kg | 2012–2021 | Rice items of the 2012-based retail price survey |
| psa/retail_cereals_2018based_oldgeo_2018_2025.csv.gz | `2018/0042M4ARA01.px` | PHP per kg | 2018–2025, old code | Rice: well-milled, regular-milled, special |
| psa/retail_cereals_2018based_newgeo_2018_2026.csv.gz | `2018NEW/0042M4ARN01.px` | PHP per kg | 2018–2026, new code | Same |
| psa/wholesale_cereals_oldgeo_2010_2025.csv.gz | `NWS/0052M4AWA01.px` | PHP per kg | 2010–2025, old code | Rice: special, premium, WMR, RMR |
| psa/wholesale_cereals_newgeo_2010_2026.csv.gz | `NWSNEW/0052M4AWB01.px` | PHP per kg | 2010–2026, new code | Same |
| psa/farmgate_cereals_oldseries_1990_2020.csv.gz | `FG/0032M4AFP01.px` | PHP per kg | 1990–2020 | Palay (paddy) fancy and other variety, dry, converted to 14% moisture |
| psa/farmgate_cereals_newseries_2010_2026.csv.gz | `NFG/0032M4AFN01.px` | PHP per kg | 2010–2026 | Same |
| worldbank/CMO-Historical-Data-Monthly_2026-10.xlsx | World Bank Pink Sheet, https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx | Nominal USD per tonne (rice, urea) or per barrel (crude) | 1960M1–2026M9 ("Updated on October 02, 2026") | Used: Rice Thai 5%, Thai 25%, Viet Namese 5% (from about 2011), Urea, Crude oil Dubai |
| bsp/pesodollar_2026-10.xlsx | BSP, https://www.bsp.gov.ph/Statistics/External/pesodollar.xlsx | PHP per USD | 1945–2026, sheet "monthly" (average) | Server refuses some browser user-agents; the script uses a plain client string |
| noaa/oni_ascii_2026-10.txt.gz | NOAA Climate Prediction Center, https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt | °C anomaly (Oceanic Niño Index), 3-month running season | 1950 DJF–2026 JAS | Gzipped copy of the text file; each season is assigned to its centre month |
