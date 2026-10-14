# Opening the Rice Border — project brief

**Question.** Did the Philippine Rice Tariffication Law (RTL, Republic Act 11203,
in force from March 2019), which replaced quantitative restrictions (QR) on rice
imports with a 35% tariff, change how much and how fast world rice prices pass
through to Philippine consumer, retail, wholesale and farmgate rice prices, and who
gained and lost (consumers vs farmers, rice-deficit vs rice-surplus regions, the
bottom 30% of households)? Units: 17 regions (old PSA geographic code), monthly,
1994–September 2026. Outputs: working paper (three objectives), journal manuscript
(IMRAD), analysis report with statistical annex, master document. Reference paper:
Antonio, Valera, Mishra, Pede, Yamano and Vieira (2024), *Rice price inflation
dynamics in the Philippines*, MPRA Paper 123641 (panel VAR, 17 regions, 1994M1–2023M3).
Started 14 October 2026 from a one-line request; the concept note
(`docs/concept_note.md`) was drafted by Claude and awaits the user's revision.

## Conventions

- `data/raw/` holds untouched downloads only; every file gets an entry in
  `data/raw/source_log.md` (URL, date pulled, base year, coverage).
- `data/processed/` and `output/` are written by scripts, never by hand.
- `replication/antonio2024_targets.csv` holds the reference paper's numbers.
- No new-data estimate is reported until the replication gate passes.
- Every specification choice goes in the decisions log below, with the evidence,
  labelled pre-registered / supplementary / exploratory.
- Documents are rendered from templates; never edit rendered .md/.docx by hand.
- Policy facts only from `paper/policy_context.md` (each has a URL).
- Style: as simple as possible, define every term on first use (words → formula →
  example), paragraphs over bullets/tables, label fragile results as fragile.
- Package `rtl/` (estimators, helpers); scripts numbered `scripts/01_…` to `11_…`;
  `./run_all.sh` rebuilds everything.

## Research questions and hypotheses (draft, 14 Oct 2026)

Objective 1 (descriptive): how rice prices, their volatility, their gap to world
prices and their regional dispersion behaved before and after the RTL.

Objective 2 (estimation):

- **RQ1. Pass-through.** How much of a 1% change in the world rice price, in pesos,
  reaches regional consumer rice prices within 6 and 12 months, and did this change
  after March 2019? H1a (integration): pass-through rose, as the trade-reform
  literature predicts when quotas become an ad valorem tariff (Baffes and Gardner
  2003). H1b (rigidity): it did not rise, because of domestic market power and
  downward price rigidity (Trinidad, Ravago and Balisacan 2026; Bathan et al. 2025).
- **RQ2. Along the chain.** Did the law change pass-through to farmgate palay,
  wholesale and retail prices differently? H2: farmgate pass-through rose more than
  retail pass-through (farmers newly exposed to world prices).
- **RQ3. The border gap.** Did the gap between domestic and world rice prices fall
  after the law, and again after the 2024 tariff cut? H3: yes, but by less than the
  tariff change implies.
- **RQ4. Regions.** Did the change in pass-through differ between rice-deficit and
  rice-surplus regions, and between high- and low-poverty regions? H4a: larger
  increase in rice-deficit (import-dependent) regions; H4b: no difference.
- **RQ5. The poor.** Do world rice shocks raise the bottom-30% consumer price index
  (CPI) more than the all-income CPI (a regressive effect), and did the law change
  this? H5: regressive, because rice weighs about twice as much in the poor's basket.

Objective 3 (policy): what the estimates imply for the 2024 tariff cut (35% → 15%),
the 2025 import suspension and the 2026 price-indexed tariff, in pesos for a
poverty-line family.

## Reference specification (read from Antonio et al. 2024)

- Model: panel VAR, equation (1) X_it = A(L) X_it−1 + f_i + ε_it, five endogenous
  variables in Cholesky order ENSO → FPI (fuel price inflation) → UREA → THAI (Thai 5%
  broken rice) → RPI (rice price inflation). Fixed effects removed by forward
  orthogonal deviations (Helmert), estimated by GMM with lagged regressors as
  instruments (Love and Zicchino 2006). Lag length not reported.
- Variables: "first-differenced natural logarithm form" (p. 13); THAI and UREA in
  real pesos (USD price × monthly average PHP/USD ÷ national CPI). ENSO is a sea
  surface temperature anomaly index (can be negative, so it cannot be logged).
- Sample: balanced, 17 regions, 1994M1–2023M3 (IRFs labelled 1994M11–2023M3).
- Output: orthogonalized impulse responses over 10 months, 95% intervals from 200
  Monte Carlo draws. Results are shown only in figures (Figs. 3–5); no IRF numbers in
  tables.
- Tables usable as targets: Table 1 (regional mean and standard deviation of RPI
  and FPI); Table 3 (poverty incidence 2015 and Low/Medium/High class); Table 4
  (rice self-sufficiency index and class).

## Decisions log

| # | Date | Decision | Evidence / reason | Status |
| --- | --- | --- | --- | --- |
| D1 | 14 Oct 2026 | Read Table 1 "rice/fuel price inflation" as the **level** of the regional CPI index (2018 = 100), 1994M1–2023M3. | Means of 63–77 with standard deviations of 18–38 cannot be monthly inflation rates; they match an index with base 2018 = 100 that rose from about 35 to 120. | pre-registered |
| D2 | 14 Oct 2026 | Rice price = PSA CPI item "01.1.1.12 – Rice". Fuel price = whichever of 04.5 "Electricity, gas and other fuels" or 07.2.2 "Fuels and lubricants for personal transport equipment" is closer to Table 1 FPI (median absolute deviation of regional means); the other is a robustness alternative. | The paper does not name the fuel item; the table settles it (skill rule 1.2). | pre-registered |
| D3 | 14 Oct 2026 | Replicate the PVAR with one lag. | Stata `pvar` (Abrigo and Love 2016) default `lags(1)`; the paper reports none. Two lags as a check. | pre-registered |
| D4 | 14 Oct 2026 | ENSO = NOAA Oceanic Niño Index (ONI), entered in levels (not logged). | The paper describes an SST anomaly over centred 30-year base periods, which is the ONI definition; an anomaly can be negative. | pre-registered |
| D5 | 14 Oct 2026 | Geography: 17 regions in PSA's *old* geographic code (long history 1994–Dec 2025). Extend to Jan–Sep 2026 by chaining new-code monthly growth onto old-code levels; regions whose boundaries differ between the codes have their 2026 months flagged `new_geo_ext` and dropped in robustness check (k). NIR is not a unit. *Amended 14 Oct 2026 (before any estimate):* the overlap check (`output/tables/geo_overlap_check.csv`) shows identical 2018–2025 series for 13 regions and differences for VI and VII (Negros moved to NIR) and also XII and BARMM (Cotabato City), so all four are flagged. | Old-code tables end Dec 2025; new-code tables run to Sep 2026; the reference uses 17 regions. | pre-registered |
| D6 | 14 Oct 2026 | Law date: first post-RTL month = March 2019 (`post` = 1 from 2019M3). | RA 11203 approved 14 Feb 2019; in force 15 days after publication, commonly dated 5 March 2019 (`paper/policy_context.md` P1–P2). | pre-registered |
| D7 | 14 Oct 2026 | World rice shock f_t = 100·Δln(Thai 5% USD/t × PHP/USD), nominal pesos; the reference's real-peso version is robustness (a). | Outcomes are nominal CPI changes; a nominal shock keeps both sides in the same units. The Thai 5% is the reference's world price and the longest Pink Sheet rice series. | pre-registered |
| D8 | 14 Oct 2026 | Local projection lead set: Teulings–Zubanov leads 1..h−1 (as in Kpodar and Liu 2022 and the bundled `lp.py`). | The reference paper uses a VAR, so it does not fix the lead set; we keep the skill's tested default. | pre-registered |
| D10 | 14 Oct 2026 | Fuel price inflation (FPI) in the replica = CPI item 07.2.2 (transport fuels). | G1b: exact match to Table 1. | pre-registered rule, applied |
| D11 | 14 Oct 2026 | Proceed to estimation although G3 failed, **conditionally**: G1 and G2 validate the data and the core estimator (the national/pooled response); G3 concerns the reference's group ordering, read by eye from figures. Every document reports the G3 failure; the regional heterogeneity results (RQ4) are labelled "not validated against the reference". The user may overrule and ask for estimation to stop. | Skill rule: if a gate fails, say so and label later results as conditional on the choice to continue. | decision after the gate result |
| D9 | 14 Oct 2026 | Region groups for heterogeneity are taken unchanged from Antonio et al. (2024): rice-insufficient = Table 4 "Insufficient" (NCR, CALABARZON, Central Visayas, Zamboanga Peninsula, Northern Mindanao, Davao); high poverty = Table 3 "High". | Groups fixed by a published source before any estimate, built from pre-period data (2015 FIES; production), so they cannot be chosen after the results. | pre-registered |

## Replication gate (pre-registered 14 Oct 2026, before any data were downloaded)

All on the reference sample (17 regions, old geographic code).

- **G1 (data):** regional mean of the rice CPI level (01.1.1.12, 2018 = 100) over
  1994M1–2023M3 within ±0.5 index points of Table 1 for at least 15 of 17 regions,
  and the regional standard deviation within ±0.5 for at least 15 of 17.
- **G1b (fuel item, decides D2):** the better-matching fuel candidate meets the same
  ±0.5 rule for its means in at least 15 of 17 regions. If neither does, D2 stays
  open and the fuel variable is labelled "not replicated".
- **G2 (shape, PVAR replica):** PVAR(1) with fixed effects removed by forward
  orthogonal deviations, GMM with lagged levels as instruments, Cholesky order
  ENSO → FPI → UREA → THAI → RPI, sample 1994M1–2023M3, 200 Monte Carlo draws.
  The response of RPI to a one-standard-deviation THAI shock must (i) be positive
  with the 95% band above zero at h = 1, (ii) peak at h = 1 or h = 2, and (iii) fall
  below 25% of its peak by h = 6. The response to the FPI shock must (iv) be positive
  at h = 0 and (v) fall below 25% of its h = 0 value by h = 3.
- **G3 (ordering):** with the same model estimated on the Table 4 groups, the peak
  RPI response to THAI in rice-insufficient regions divided by that in sufficient
  regions lies in [1.3, 3.0] (paper: "almost twice"); and the peak in high-poverty
  regions is below the peak in low-poverty regions (paper: Fig. 4).

Indicative only (not part of the gate): the local projection on the reference
sample gives a positive cumulative pass-through of THAI to RPI at h = 1–3.

**Result (run 14 Oct 2026): FAIL on G3; G1, G1b and G2 PASS** (`output/tables/replication_gate.csv`).

- G1: rice CPI means and SDs match Table 1 in 17 of 17 regions (median deviation 0.000).
- G1b: the fuel item is 07.2.2 "Fuels and lubricants for personal transport equipment"
  (17 of 17, median deviation 0.000; 04.5 deviates by 6.3 points). This settles D2.
- G2: THAI → RPI response 0.256 at h = 1 (95% band 0.215 to 0.303), peak at h = 1,
  0.01 of the peak by h = 6; FPI → RPI 0.143 at impact, −0.04 of impact by h = 3. All pass.
- G3: peak ratio insufficient/sufficient = 1.26 (range [1.3, 3.0]): **fail**; peak
  high-poverty 0.260 vs low-poverty 0.255: **fail** (should be lower).
- What was checked after the failure (no code error found): the two-lag model gives a
  ratio of 1.27 (`replication_g3_diagnostic.csv`). *Exploratory:* the paper's wording
  is about the immediate impact and persistence, not the peak; on those measures the
  pattern holds (impact ratio 1.69; low-poverty impact 0.236 vs high 0.102; six-month
  cumulative 0.676 vs 0.572). The pre-registered criterion is not changed.
- Indicative LP on the reference sample: cumulative pass-through of the real THAI
  shock 0.08 at h = 1, 0.15 at h = 3, 0.17 at h = 6 (all with 90% bands above zero).

## Estimation plan (pre-specified 14 Oct 2026, before any estimate on the new data)

**Common settings.** Local projections (Jordà 2005) estimated by OLS for each
horizon h = 0..12 with p = 12 lags of the outcome and the shock, Teulings–Zubanov
leads 1..h−1, a linear trend, region fixed effects in panels; cumulative responses
B_h (running-sum outcome); Driscoll–Kraay standard errors (bandwidth h + 1) for
panels and Newey–West (h + 1 lags) for national series; 90% bands. Units 100·Δln
throughout, so coefficients read as "percentage points per 1% world price change".
Main panel sample 1995M1–2026M9 (1994 supplies lags). `post` = 1 from 2019M3.
Regime-specific pass-through: the shock is interacted with `post` (θ_h = change),
`post` enters as a level dummy; the post-regime B_h is read from the same model
re-parametrised with a `pre` interaction.

- **RQ1:** outcome regional rice CPI inflation π^R_rt; decided on the cumulative
  change θ at h = 6 and h = 12 (H1a: θ > 0; H1b: θ ≤ 0), and on B_h pre and post.
- **RQ2:** national monthly farmgate palay (other variety, dry), wholesale and retail
  regular-milled rice (RMR) prices, 2010M1–2026M9, single-series LPs with the `post`
  interaction, Newey–West; decided on cumulative B_12 pre and post for farmgate vs
  retail. Check: regional farmgate panel (Driscoll–Kraay).
- **RQ3:** border gap G_t = 100·ln(P^wholesale_RMR,t / P^world_t), P^world = Thai 5%
  in pesos per kg. Segmented (interrupted time-series) regression
  G_t = a + b·post_t + c·tariff15_t + d·ban_t + month dummies + ε_t, with tariff15 = 1
  from 2024M7 and ban = 1 in 2025M9–2025M12, Newey–West (12 lags), 2010M1–2026M9.
  H3: b < 0, c < 0, with |c| below the 16.0 log-point tariff wedge. Check: add ln
  world price as a regressor.
- **RQ4:** RQ1 model with interactions shock×G, shock×post, shock×post×G (and
  post×G as a level dummy) for G = rice-insufficient and G = high poverty (D9), one
  group at a time. Decided on the cumulative θ_{post×G} at h = 12, Bonferroni across
  the two group tests (each judged at 10%/2 = 5%).
- **RQ5:** national all-items inflation gap ΔD_t = π^A_t − π^B30_t (all income minus
  bottom 30%), 2001M1–2026M9, Newey–West, with and without the `post` interaction;
  negative = regressive. Mechanism: B^rice_h × (w^A_rice − w^B30_rice) using PSA's
  official 2018 weights.

**Robustness menu** (applied to RQ1, decisive horizons h = 6 and 12):
(a) real shock (deflated by national CPI, as in the reference); (b) Viet 5% instead of
Thai 5%; (c) world price in US dollars with the exchange-rate change as a control;
(d) controls: exchange rate, crude oil (Dubai) in pesos, urea in pesos, ONI;
(e) p = 6 and p = 18; (f) excluding the 2007M10–2008M12 world rice crisis;
(g) excluding 2020; (h) sample ending 2024M6 (before the 2024 tariff cut);
(i) symmetric window 2012M3–2026M9; (j) asymmetry, shock × 1[shock > 0];
(k) dropping `new_geo_ext` observations; (l) leaving one region out (range);
(m) fully separate pre and post estimation; (n) placebo law date 2016M3 within
1995M1–2019M2; (o) standard errors clustered by region.

**Objective 3 (pre-registered here, before the main results).** E1: the 2024 tariff
cut is a shock τ = 100·ln(1.15/1.35) = −16.0 to the peso cost of imports in 2024M7;
predicted national rice inflation from 2024M7 to month m = Σ_t B^post_{m−t}(f_t + τ_t)
from the national post-regime model estimated on data ending 2024M6 (out of sample);
compare with actual and report the share explained at 6 and 12 months. E2: the same
by region with the panel model. E3: pesos per month for a poverty-line family of
five (PSA poverty threshold × bottom-30% rice weight × predicted change).
E4: descriptive farmgate and retail paths during the 2025 import suspension.
E5 (Objective 1): yearly contribution of rice to headline inflation (weight × rice
inflation) for all income and the bottom 30%.

## Results

Pending.

## Documents

Pending (see `paper/` and `docs/` once rendered).

## Pipeline

`./run_all.sh` rebuilds everything from `data/raw/` (`--download` to refresh).

## Open questions

- [ ] Exact Official Gazette publication date of RA 11203 (D6 uses March 2019).
- [ ] Antonio et al. lag length and ENSO transformation (D3, D4 are our readings).
- [ ] Applied rice tariff for April–September 2026 under EO 105.
- [ ] User to revise the concept note and confirm the target journal or course
      format; no formatting template has been provided yet.
