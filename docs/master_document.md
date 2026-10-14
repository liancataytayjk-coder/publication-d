---
title: "Master Document: How the Rice Tariffication Study Was Built"
subtitle: "Narrative of the process, every decision and every document, with all code"
date: "October 2026"
---



# Part I. The narrative

This document is for learning. It tells how the study *Opening the Rice Border* was
built, step by step: what was done, why each decision was made, and what went wrong and
how it was fixed. The appendices reproduce every other document of the study and all of
its code, so this single file is the complete record.

## 1. Starting point

The request was one line: study the Rice Tariffication Law (RTL) "from back to back".
There was no concept note, no reference paper and an empty repository. The first step
was therefore to write a concept note (`docs/concept_note.md`) and to find a reference
paper whose published results could be reproduced with public data. Several candidates
were read: a Department of Finance note with annual regressions (too few observations),
Bathan et al. (2025) with autoregressive distributed lag models (many software-specific
choices, hard to reproduce exactly), Trinidad, Ravago and Balisacan (2026) with vector
error correction models, and Antonio et al. (2024), a panel vector autoregression (VAR)
on PSA regional rice inflation, 1994–2023. Antonio et al. was chosen because its Table 1
reports exact regional statistics that can be checked, its data are entirely public,
and its question, how world prices drive regional rice inflation, is the natural base
for asking whether the law changed that link.

## 2. Phase 1: pinning down the question and the specification

The brief in `CLAUDE.md` sets five research questions under three objectives and pairs
each with hypotheses, including the competing pair H1a (integration: pass-through rises)
and H1b (rigidity: it does not). Reading the reference paper as a replicator settled
several ambiguities. Its Table 1 calls the variables "rice price inflation", but means
around 70 with standard deviations around 20 can only be index *levels* with base 2018
(decision D1). The paper does not name its fuel price, so the rule was fixed in advance
that whichever PSA fuel index matches Table 1 would be used (D2). The lag length is not
reported; the Stata default of one lag was chosen (D3). The El Niño variable can be
negative and cannot be logged, so it enters in levels (D4).

Before any data were downloaded, the replication gate (G1–G3) and the full estimation
plan, including fifteen robustness checks and the policy episode analysis, were written
into `CLAUDE.md` and committed to git. The commit time stamps are the proof that the
choices were made before the results were seen.

## 3. Phase 2: data

Every series came from an official source through a script: PSA OpenSTAT for the
consumer price indices (all income and bottom 30%), their weights and the rice price
surveys; the World Bank Pink Sheet for world rice prices; the BSP for exchange rates;
NOAA for the El Niño index. Each raw file is stored unchanged and logged in
`data/raw/source_log.md`.

Three things went wrong and were fixed. First, the PSA bottom-30% tables label Region XII
as "Reg12", so the first download silently missed one region; a count check (18 instead
of 19 geographies) caught it, and the label pattern was widened. Second, the API
occasionally stalled; the downloader was given shorter time-outs, visible retries and a
progress dot per region. Third, the PSA introduced a new geographic code with a Negros
Island Region. A check of the overlap months showed that the old and new codes agree
exactly for 13 regions but differ for Western and Central Visayas (Negros) and also for
SOCCSKSARGEN and BARMM (Cotabato City), so all four are flagged in the 2026 months that
had to be chained from the new code (D5, amended before any estimate).

National retail prices had to be joined from three PSA surveys. The 2012-based and
2018-based series agree closely (correlation of monthly changes 0.99), the older series
less so (0.79); the join is on growth rates and the join months are flagged (D12). The
rice CPI and the retail price survey were checked against each other
(0.98), and the Thai and Vietnamese world prices were compared
(0.43, low, which is why the Vietnamese price is a robustness check).

## 4. Phase 3: validation

Two independent checks came before any new estimate. Simulation tests confirm that the
local projection and the panel VAR recover known responses; one panel VAR test first
failed because a single simulated sample was two standard errors off, and was rewritten
to average five samples, after checking that the estimator is unbiased.

The replication gate gave a split verdict. The data replication was exact: our regional
means and standard deviations equal Antonio et al.'s in all 17 regions, and the fuel item
turned out to be transport fuels. The main impulse response was reproduced. But the third
criterion failed: the peak response in rice-deficit regions was 1.26 times
that in surplus regions, just below the required 1.3, and the poverty ordering did not
hold. The skill's rule is not to loosen a criterion after seeing the result. A search for
a coding error found none, and two lags gave the same answer. An exploratory diagnostic
showed that the paper's own words ("immediate impact and peak almost twice") fit the
impact response (1.69) better than the peak. The decision (D11) was to
proceed, because the data and the core estimator were validated, but to report the
failure in every document and to label region-group results as not validated. The user
may overrule this.

## 5. Phase 4: estimation

All models follow the pre-registered plan. The headline numbers are in `CLAUDE.md` and
in the documents. The most robust finding is along the chain: from 2011 to 2019
pass-through to farmgate, wholesale and retail prices was zero, and since the law it is
about one half, largest at the farmgate. The consumer-price result (RQ1) is suggestive
but fragile, and the documents say exactly where it weakens: with data ending June 2024,
with the Vietnamese price, and at twelve months with macroeconomic controls. World rice
shocks are regressive. The out-of-sample test of the 2024 tariff cut shows that consumers
received the fall in world prices but not the tariff cut. The 2025–26 import suspension
appears in the data as a sharp domestic price surge with flat world prices; because the
model was not built for a closed border, it is reported as exploratory.

## 6. Phases 5 and 6: figures and writing

All figures are black and white, without titles inside the image, and were rendered and
inspected; several were redrawn to remove overlapping labels and legends. Every document
is rendered from a template; every number comes from the saved tables through
`output/tables/paper_numbers.json`. Two kinds of error were caught by re-reading the
rendered documents: inline equations containing generated numbers did not survive the
conversion to Word, and were rewritten as text; and a few sentences claimed more than the
estimates show (for example, a policy recommendation not tied to an estimate, and a
miscalculated offset of the 2026 indexed tariff), and were corrected.

## 7. Phase 7: delivery

`./run_all.sh` rebuilds everything from the raw files; `./run_all.sh --download`
refreshes the data first. `docs/session_handoff.Rmd` tells a new session how to continue.

# Part II. Appendices

The appendices reproduce every other document of the study. Their headings are demoted
by one level.

# Appendix A. Concept note

*Source file: `docs/concept_note.md`*

## Concept note: the Rice Tariffication Law and rice prices in the Philippines

*Drafted by Claude on 14 October 2026 from the user's request ("the research question we
would like to explore next is Rice Tariffication Law in the Philippines, complete from
back-to-back"). The user should revise this note; every later document follows it.*

### The problem in everyday terms

Rice is the Philippine staple. The poorest 30% of households spend about a sixth of
their budget on it, and about two million farm households sell palay (unmilled rice)
for a living. For decades the government kept imported rice out with quantitative
restrictions (QR): only the National Food Authority (NFA), or traders holding NFA
permits, could import, and only in the volumes the government allowed. Domestic rice
was therefore much dearer than rice in Bangkok or Ho Chi Minh City.

Republic Act (RA) 11203, the Rice Tariffication Law (RTL), signed on 14 February 2019,
replaced the quotas with a tariff (35% on rice from ASEAN countries). Anyone with a
sanitary import clearance could now import any amount, so long as the duty was paid.
The tariff revenue funds the Rice Competitiveness Enhancement Fund (RCEF) for
farmers. Later policy kept changing the border: a cut of the tariff to 15% in July
2024 (Executive Order 62), a suspension of imports from September to December 2025
(EO 93 and EO 102), and a price-indexed tariff of 15–35% from January 2026 (EO 105).

### Main question

Did replacing quotas with tariffs change how strongly and how fast world rice prices
reach Filipino consumers and farmers, and who gained and who lost?

### Why it matters now

Rice inflation drove headline inflation in 2018, before the law, and again in
2023–2024. The government cut the tariff in 2024 on the expectation that lower duties
would lower retail prices. Critics argue that retail prices did not fall as much as
the tariff cut implied, and farmers' groups argue that open imports depress palay
prices. Both claims are about *pass-through*, which this study measures.

### Reference paper

Antonio, Valera, Mishra, Pede, Yamano and Vieira (2024), *Rice price inflation
dynamics in the Philippines* (MPRA Paper 123641). They estimate a panel vector
autoregression for 17 regions, 1994–2023, and find that world rice price shocks have
the largest and most persistent effect on regional rice inflation, with larger
effects in rice-deficit regions. We replicate their data and their main impulse
response first, then extend the design to ask whether the law changed pass-through.

### Proposed data

All official and public: Philippine Statistics Authority (PSA) consumer price index
(CPI) for rice by region (all income households and the bottom 30%), PSA retail,
wholesale and farmgate rice prices, World Bank Pink Sheet world rice prices, Bangko
Sentral ng Pilipinas (BSP) peso–dollar rates, and the National Oceanic and
Atmospheric Administration (NOAA) El Niño index.

### Expected outputs

A working paper with three objectives (descriptive, estimation, policy), a journal
manuscript, a visual analysis report with a statistical annex, a master document for
learning, and fully reproducible code.



# Appendix B. Project brief and decisions log (CLAUDE.md)

*Source file: `CLAUDE.md`*

## Opening the Rice Border — project brief

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

### Conventions

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

### Research questions and hypotheses (draft, 14 Oct 2026)

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

### Reference specification (read from Antonio et al. 2024)

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

### Decisions log

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

### Replication gate (pre-registered 14 Oct 2026, before any data were downloaded)

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

### Estimation plan (pre-specified 14 Oct 2026, before any estimate on the new data)

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

### Results (14 Oct 2026; `output/tables/estimates.csv`, `rq3_gap.csv`, `episode_*.csv`)

All conditional on D11 (replication gate G3 failed narrowly). Cumulative pass-through
in percentage points per 1% world price change; standard errors in parentheses.

- **RQ1 (pre-registered).** Regional rice CPI, 1995–2026: pre-law B6 = 0.157 (0.050),
  B12 = 0.201 (0.072); post-law B6 = 0.460 (0.141), B12 = 0.400 (0.178); change θ6 = 0.303
  (0.162, significant at 10% only), θ12 = 0.199 (0.210, not significant). H1a weakly
  supported at 6 months, not at 12. Fragile: θ6 = 0.13 (0.18) with data ending 2024M6
  (h); θ12 = 0.06 (0.16) with macro controls (d). Stronger in the symmetric 2012–2026
  window (i): θ6 = 0.44 (0.20). Stable leaving any region out (θ6 0.29–0.32). Placebo
  law date 2016M3: θ6 = 0.07 (0.10).
- **RQ2 (pre-registered).** National, 2011–2026: pre-law pass-through ≈ 0 at every
  stage; post-law B6 farmgate 0.74 (0.25), wholesale 0.61 (0.16), retail 0.53 (0.13),
  rice CPI 0.45 (0.12); changes significant at h = 6 for all; at h = 12 only the
  wholesale/retail/CPI changes are near 10%. H2 (farmgate rises most) supported in
  point estimates.
- **RQ3 (pre-registered).** Wholesale–world gap fell 11.2 log points after the law
  (6.6, p = 0.09) and *rose* 10.6 (4.5, p = 0.02) after the 2024 tariff cut. With the
  world price as a control, the law effect vanishes (+5.5, ns) and the tariff-cut
  rise is 15.2 (4.5). H3 rejected for the 2024 cut.
- **RQ4 (pre-registered; not validated, D11).** No significant difference at the
  decisive h = 12 (rice-insufficient −0.05 (0.07); high poverty +0.06 (0.05)). At h = 6
  the high-poverty term is +0.09 (0.04), below the Bonferroni 5% threshold only at h = 6.
- **RQ5 (pre-registered).** World rice shocks are regressive: gap ΔD B6 = −0.060
  (0.010); bottom-30% CPI B6 = 0.110 vs all-income 0.045. No change after the law
  (θ6 = +0.018 (0.021)). Rice weights 8.87% (all) vs 17.87% (bottom 30%) explain about
  a third of the gap.
- **Objective 3 (pre-registered E1–E3; E4 exploratory).** Out-of-sample: predicted fall
  in the rice CPI June 2024 → June 2025 = 21.3% (15.0 world + 6.3 tariff); actual 15.4%,
  i.e. the world-price part only. Poverty-line family rice spending PHP 2,479/month;
  predicted tariff saving PHP 151/month (full wedge PHP 367). Suspension episode: rice
  CPI +21.1% Nov 2025 → Apr 2026 while world peso price +11.4%; world prices alone
  predict +4.3% by Apr 2026 (from Aug 2025).
- **Objective 1.** Rice inflation volatility (SD of monthly change) 0.82 (2009–2019M2),
  1.52 (2019M3–2024M6), 2.33 (2024M7–2026M9). Cross-region CV of retail RMR price
  6.7% (2015–2017) → about 4% (2021–2024).

### Documents

Pending (see `paper/` and `docs/` once rendered).

### Pipeline

`./run_all.sh` rebuilds everything from `data/raw/` (`--download` to refresh).

### Open questions

- [ ] Exact Official Gazette publication date of RA 11203 (D6 uses March 2019).
- [ ] Antonio et al. lag length and ENSO transformation (D3, D4 are our readings).
- [ ] Applied rice tariff for April–September 2026 under EO 105.
- [ ] User to revise the concept note and confirm the target journal or course
      format; no formatting template has been provided yet.



# Appendix C. Raw data source log

*Source file: `data/raw/source_log.md`*

## Raw data source log

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



# Appendix D. Sourced policy facts

*Source file: `paper/policy_context.md`*

## Sourced policy facts

Every policy fact used in a document must appear here with its source. Primary texts
are from the Lawphil Project (Arellano Law Foundation), which reproduces the official
texts. Pulled 14 October 2026.

| # | Fact | Source |
|---|---|---|
| P1 | RA 11203 ("Rice Tariffication Law") amends RA 8178 (Agricultural Tariffication Act of 1996) and replaces quantitative restrictions on rice imports with tariffs. Approved 14 February 2019 by President Duterte. | https://lawphil.net/statutes/repacts/ra2019/ra_11203_2019.html |
| P2 | RA 11203 Sec. 20: the Act takes effect fifteen days after publication. The law and the end of the National Food Authority's import-licensing role are commonly dated 5 March 2019 (secondary sources; the publication date is not in the Lawphil text). | Lawphil (above); USDA FAS GAIN report "Philippines: Rice Tariffication Law Enacted" (2019), https://www.fas.usda.gov/data/philippines-rice-tariffication-law-enacted |
| P3 | Tariffs under RA 11203: 35% on rice imported from ASEAN countries; 40% within the minimum access volume (MAV) of 350,000 t from non-ASEAN sources; MAV reverted to 350,000 t from 805,200 t. | PhilRice, *RCEF FAQ 02: Rice Tariffication* (2019), https://www.philrice.gov.ph/wp-content/uploads/2019/09/RCEF_FAQ02-RiceTariff.pdf |
| P4 | RA 11203 creates the Rice Competitiveness Enhancement Fund (RCEF), PHP 10 billion a year for six years, for mechanization, seeds, credit and extension. | RA 11203 Sec. 13 (Lawphil, above); PhilRice FAQ (above) |
| P5 | Executive Order (EO) 39, 31 August 2023: mandated price ceilings of PHP 41/kg for regular milled rice and PHP 45/kg for well-milled rice nationwide. | https://lawphil.net/executive/execord/eo2023/eo_39_2023.html |
| P6 | EO 42, 4 October 2023: lifts the EO 39 price ceilings. | https://lawphil.net/executive/execord/eo2023/eo_42_2023.html ; PCO release, https://pco.gov.ph/news_releases/executive-order-no-42-lifting-the-mandated-price-ceilings-on-rice-under-executive-order-no-39-s-2023/ |
| P7 | EO 62, 20 June 2024: sets the most-favoured-nation (MFN) tariff on rice at 15% (from 35%) until 2028, reviewed every four months; the rice rates take effect fifteen days after publication. First imports at 15% were reported in the first week of July 2024. | https://lawphil.net/executive/execord/eo2024/eo_62_2024.html ; Daily Tribune, 19 July 2024, https://tribune.net.ph/2024/07/19/35000-mt-rice-imports-arrived-under-lower-tariff-order |
| P8 | RA 12078, approved 6 December 2024: amends RA 8178/RA 11203; extends RCEF to 2031 at PHP 30 billion a year; lets the Department of Agriculture (DA) declare a food security emergency on rice and release NFA buffer stocks; lets the President suspend imports when local prices collapse. | https://lawphil.net/statutes/repacts/ra2024/ra_12078_2024.html |
| P9 | EO 93, 29 August 2025: suspends imports of regular milled and well-milled rice from 1 September 2025 for 60 days (to 30 October 2025), citing a sharp fall in palay prices after heavy imports at the reduced tariff. | https://lawphil.net/executive/execord/eo2025/eo_93_2025.html |
| P10 | EO 102, 30 October 2025: extends the suspension to 31 December 2025. | https://lawphil.net/executive/execord/eo2025/eo_102_2025.html |
| P11 | EO 105, 7 November 2025: keeps the MFN rice tariff at 15% to 31 December 2025; from 1 January 2026 the tariff rises 5 percentage points per 5% fall in international rice prices and falls 5 points per 5% rise, never below 15% or above 35%. | https://lawphil.net/executive/execord/eo2025/eo_105_2025.html |
| P12 | Imports resumed on 1 January 2026; reports differ on whether the tariff was 15% or 20% in early 2026; a USDA FAS report (February 2026) states 15% through March 2026. | Philstar, 9 January 2026, https://www.philstar.com/headlines/2026/01/09/2499697/philippines-resumes-importing-rice-tariff-still-15 ; USDA FAS GAIN RP2026-0004, https://www.fas.usda.gov/data/gain/2026/02/philippines-philippines-implements-quarterly-rice-import-tariff-adjustment-based-international |
| P13 | PSA official poverty threshold, full year 2023: PHP 13,873 per month for a family of five (food threshold PHP 9,581). | PSA, *2023 Full Year Official Poverty Statistics* (15 August 2024), https://psa.gov.ph/sites/default/files/phdsd/2023%20FY%20Official%20Poverty%20Statistics%20Publication_15August2024.pdf |

### Facts still to confirm (open)

- The exact Official Gazette publication date of RA 11203 (P2), which fixes the first
  month of the tariff regime. The study uses March 2019 as the first post-law month.
- The applied rice tariff for April–September 2026 under EO 105 (P11–P12).



# Appendix E. Analysis report

*Source file: `docs/analysis_report.md`*




> **How to read this report.** *Log points:* we measure changes as 100 × the change in
> the natural log of a price, which is close to a percentage change. *Shock:* a 1% rise
> in the world rice price (Thai 5% broken rice, in pesos). *Response or pass-through:*
> how many percentage points a domestic price has risen, in total, a given number of
> months after that 1% shock; 0.5 means half of the world price change has reached the
> domestic price. *Before/after the law:* before or from March 2019, when the Rice
> Tariffication Law (RTL) replaced import quotas with a tariff. *Gap:* all-income
> inflation minus bottom-30% inflation; negative means the poor face more inflation.
> *Bands:* grey areas and dotted lines are 90% intervals; if a band excludes zero, the
> estimate is significant at 10%. Full tables of every estimate are in the Statistical
> Annex.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Part A. Checking the tools

### A1. Can we reproduce the reference study?

**Context and process.** Before trusting any new number, we checked that our data and
code reproduce Antonio et al. (2024), who studied regional rice inflation from 1994 to
2023. We wrote down pass criteria before downloading any data, rebuilt their data from
PSA's website and re-estimated their panel vector autoregression.

![Left: regional rice CPI means and standard deviations, theirs vs ours. Right: response of rice inflation to a world rice price shock in our replica.](../output/figures/fig12_validation.png){width=90%}

**What the figure shows.** All 34 points on the left lie on the line of equality: our
regional means and standard deviations equal theirs (largest difference
0.000). On the right, rice inflation jumps after a world price shock, peaks
after one month at 0.256 points and is gone by month six, as in their paper.

**What it means.** The data and the core method are right. One pre-registered check
failed: rice-deficit regions respond 1.26 times as strongly as surplus
regions at the peak, short of the 1.3 we required. Results by region group are therefore
labelled "not validated" throughout.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Part B. The data at a glance (Objective 1)

### B1. Domestic and world rice prices since 1995

**Context and process.** We put the PSA rice consumer price index (CPI) and the world
rice price in pesos on the same scale (2018 = 100) to see whether they move together,
and how that changed with the law.

![Rice CPI and world rice price in pesos, index 2018 = 100, log scale.](../output/figures/fig02_long_run.png){width=95%}

**What the figure shows.** Under quotas (to 2019) the domestic price was smooth and
often far from the world price, for example in 2014–2016. After 2019 the two lines
move together much more, through the 2023 spike and the 2025 fall, until early 2026,
when domestic prices jumped while world prices were flat.

**What it means.** The law tied domestic prices to world prices. Monthly rice inflation
became more volatile: its standard deviation rose from 0.82 under
quotas to 1.52 under the 35% tariff and 2.33
after July 2024.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

### B2. The gap between domestic and world prices

**Context and process.** We compute how far the domestic price per kilogram is above
the world price per kilogram, in log points, every month since 2010.

![Border gap for wholesale (solid) and retail (dashed) regular-milled rice.](../output/figures/fig03_border_gap.png){width=95%}

**What the figure shows.** The gap averaged 46 log points under
quotas, 35 under the 35% tariff and 46
after the 2024 tariff cut.

**What it means.** The law narrowed the gap, but cutting the tariff in 2024 did not
narrow it further; it widened. A lower duty that does not show up in the gap was kept
somewhere along the chain.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

### B3. Are regional rice markets more integrated?

**Context and process.** We measure how different retail rice prices are across the 17
regions each year (coefficient of variation: standard deviation divided by the mean).

![Coefficient of variation of retail regular-milled rice prices across regions.](../output/figures/fig14_regional_dispersion.png){width=80%}

**What the figure shows.** Dispersion fell from 6.7% in 2015–2017 to
4.1% in 2021–2024, then rose to 5.6% in 2026.

**What it means.** With imports open to any trader, rice moves more freely across
regions and prices converge. The 2026 rise coincides with the price surge after the
import suspension.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

### B4. When do world shocks show up in domestic inflation?

**Context and process.** We correlate this month's world price change with rice
inflation k months later, separately before and after the law.

![Correlation between the world shock and rice inflation k months later.](../output/figures/fig13_crosscorr.png){width=80%}

**What the figure shows.** Before the law the correlation peaks at 0.28
after 2 months; after the law at 0.35 after
4 months. Both lines are noisy.

**What it means.** In both regimes world price changes reach domestic inflation within
about half a year. Simple correlations cannot say more; the estimates in Part C control
for other influences.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Part C. The estimates (Objective 2)

### C1. Did pass-through to consumer rice prices rise? (RQ1)

**Context and process.** For each horizon from 0 to 12 months we regress the total rice
inflation in each region on the world price shock, allowing the response to differ
before and after March 2019, with twelve lags, corrections for later shocks, a trend and
region effects (local projections).

![Cumulative response of regional rice CPIs to a 1% world price rise, before (solid) and after (dashed) the law.](../output/figures/fig04_rq1_passthrough.png){width=80%}

**What the figure shows.** Six months after a 1% world price rise, regional rice prices
are 0.16 points higher before the law and 0.46 after it. The bands
overlap at twelve months.

**What it means.** Pass-through to consumers rose after the law, but the evidence is
suggestive: the change (0.30) is significant only at 10% at six months and not
at twelve.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

### C2. How robust is that change?

**Context and process.** We re-estimated the change in pass-through under fifteen
alternative choices fixed in advance: other world prices, controls, lag lengths,
excluded years, sample windows and error types.

![Change in pass-through after the law across checks, at 6 (left) and 12 (right) months.](../output/figures/fig08_robustness.png){width=95%}

**What the figure shows.** At six months the change ranges from 0.13 to
0.44 and stays significant in 12 of 15 checks.
It is smallest with data ending June 2024 (0.13). At twelve months it
is significant in 2 checks.

**What it means.** The direction is stable; the size and significance are not. At six
months, much of the measured rise depends on the months after mid-2024.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

### C3. Who along the chain feels world prices? (RQ2)

**Context and process.** The same method on national farmgate palay, wholesale and
retail rice prices, 2011 to 2026.

![Response of farmgate, wholesale and retail prices before (solid) and after (dashed) the law.](../output/figures/fig05_rq2_chain.png){width=100%}

**What the figure shows.** Before the law the responses are flat at zero at every stage.
After it, six-month pass-through is 0.74 at the farmgate,
0.61 at wholesale and 0.53 at retail.

**What it means.** This is the clearest result of the study. Under quotas, farmers and
consumers were insulated from world prices; under tariffs they are not, and farmers most
of all. Low world prices now mean low palay prices.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

### C4. Do world rice shocks hurt the poor more? (RQ5)

**Context and process.** National all-items CPIs for all households and for the bottom
30%, and their gap, 2001–2026.

![Response of all-items CPIs (left) and of the gap between them (right).](../output/figures/fig06_rq5_poor.png){width=95%}

**What the figure shows.** Six months after a 1% world rice price rise the bottom-30%
CPI is 0.110 points higher, against 0.045 for all households; the gap
falls by −0.060.

**What it means.** World rice shocks are regressive: they raise the cost of living of
the poor 2.4 times as much. Rice's larger weight in the poor's basket
(17.9% against 8.9%) explains about 36% of
this.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

### C5. Do regions differ? (RQ4, not validated)

**Context and process.** We allowed the post-law change to differ in rice-deficit and
high-poverty regions (groups from Antonio et al.).

![Extra post-law change in rice-deficit (solid) and high-poverty (dashed) regions.](../output/figures/fig07_rq4_regions.png){width=80%}

**What the figure shows.** At twelve months the extra change is −0.05
(deficit) and 0.06 (high poverty); neither is significant.

**What it means.** We find no robust regional difference in how the law changed
pass-through. Because the reference paper's group pattern did not replicate, this part
carries little weight.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## Part D. The current episode and policy (Objective 3)

### D1. Did the 2024 tariff cut reach consumers?

**Context and process.** Using only data up to June 2024, we predicted how much the rice
CPI should fall after July 2024 from world prices and from the cut of the tariff from 35%
to 15% (−16.0 log points in the import cost), and compared with what happened.

![Rice CPI since June 2024: actual, predicted from world prices, and predicted from world prices plus the tariff cut.](../output/figures/fig09_episode_tariff_cut.png){width=80%}

**What the figure shows.** By June 2025 the rice CPI fell −15.4 log
points. World prices alone predicted −15.0; world prices and the
tariff cut, −21.3.

**What it means.** Consumers got the fall in world prices but not the tariff cut. For a
poverty-line family of five, which spends about PHP 2,479 a month on
rice, the predicted tariff saving of about PHP 151 a month did
not materialise.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

### D2. The tariff cut by region

**Context and process.** The same comparison for each region's rice CPI.

![Change in regional rice CPIs, June 2024 to June 2025, and the predicted change.](../output/figures/fig11_regions_episode.png){width=80%}

**What the figure shows.** Falls range from −7.7 in
CAR to −23.6 in
Cagayan Valley; only 2 regions fell by more
than predicted.

**What it means.** The shortfall was general, not confined to a few regions.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

### D3. The 2025 import suspension (exploratory)

**Context and process.** We compared farmgate and retail prices after August 2025 with
the path predicted from world prices alone.

![Farmgate (left) and retail (right) prices since August 2025, actual and predicted from world prices; grey = suspension.](../output/figures/fig10_episode_suspension.png){width=95%}

**What the figure shows.** Farmgate prices first fell (−8.9% in
September 2025), then rose 31.1% by April 2026; retail prices
rose 24.2%. World prices predicted 7.6%
and 4.7%.

**What it means.** Closing the border was followed by a price surge far beyond what world
prices explain, felt by consumers months after the suspension ended. The model was not
built for a closed border, so we treat this as descriptive.



# Appendix F. Statistical annex

*Source file: `docs/statistical_annex.md`*


Every estimate of the study, generated from `output/tables/estimates.csv`. Coefficients are cumulative responses in percentage points per 1% world rice price rise (pesos); standard errors in parentheses (Driscoll–Kraay for regional panels, Newey–West for national series); \* p<0.10, \*\* p<0.05, \*\*\* p<0.01. Robustness specs are lettered as in the pre-registered plan (`CLAUDE.md`).

## A. Descriptive and policy tables

### Table A1. World rice price episodes since 1995

| Start | End | Months | Peak 12-month rise, world (%) | World change (log pts) | Rice CPI change (log pts) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1995-05 | 1996-04 | 12 | 40 | 15.7 | 25.9 |
| 1997-12 | 1998-11 | 12 | 50 | 21.3 | 4.7 |
| 2002-04 | 2002-06 | 3 | 17 | 5.7 | 0.3 |
| 2004-03 | 2005-09 | 19 | 35 | 29.2 | 12.2 |
| 2008-02 | 2009-03 | 14 | 96 | 61.7 | 23.4 |
| 2011-08 | 2011-11 | 4 | 21 | 14.4 | −0.9 |
| 2016-05 | 2016-07 | 3 | 19 | 12.9 | 0.7 |
| 2018-01 | 2018-04 | 4 | 22 | 13.8 | 2.2 |
| 2020-03 | 2020-06 | 4 | 28 | 13.2 | 3.4 |
| 2022-08 | 2024-06 | 23 | 39 | 46.2 | 23.4 |
| 2026-06 | 2026-09 | 4 | 34 | 11.0 | −1.7 |


### Table A2. The 2024 tariff cut by region (log points)

| Region | Actual change, 6 months | Actual change, 12 months | Predicted, 12 months | Actual − predicted |
| :--- | ---: | ---: | ---: | ---: |
| Cagayan Valley | −4.6 | −23.6 | −21.0 | −2.6 |
| SOCCSKSARGEN | −5.8 | −23.0 | −21.0 | −2.0 |
| Zamboanga Peninsula | −4.5 | −20.6 | −21.0 | 0.4 |
| Central Luzon | −6.2 | −20.3 | −21.0 | 0.7 |
| Caraga Region | −4.2 | −20.1 | −21.0 | 0.9 |
| Bicol Region | −4.5 | −19.6 | −21.0 | 1.4 |
| Northern Mindanao | −1.9 | −18.0 | −21.0 | 3.0 |
| Davao Region | −5.0 | −17.3 | −21.0 | 3.7 |
| MIMAROPA | −10.5 | −15.7 | −21.0 | 5.3 |
| Eastern Visayas | −1.9 | −15.5 | −21.0 | 5.5 |
| BARMM | −2.4 | −14.9 | −21.0 | 6.2 |
| Ilocos Region | −3.1 | −13.1 | −21.0 | 8.0 |
| Central Visayas | −3.1 | −13.0 | −21.0 | 8.0 |
| CALABARZON | −2.5 | −11.9 | −21.0 | 9.1 |
| Western Visayas | −3.3 | −11.5 | −21.0 | 9.5 |
| NCR | −1.9 | −10.0 | −21.0 | 11.0 |
| CAR | 0.3 | −7.7 | −21.0 | 13.3 |


### Table A3. Region groups (Antonio et al. 2024) and 2018 rice weights

| Region | Poverty 2015 (%) | Poverty class | Self-sufficiency index | Rice supply | Rice weight, all (%) | Rice weight, bottom 30% (%) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| NCR | 4.9 | Low | 0.00 | deficit | 1.0 | 0.4 |
| CAR | 26.5 | Medium | 1.30 | surplus | 0.2 | 0.3 |
| Ilocos Region | 22.6 | Low | 2.70 | surplus | 0.4 | 0.7 |
| Cagayan Valley | 30.5 | Medium | 6.01 | surplus | 0.3 | 0.6 |
| Central Luzon | 13.4 | Low | 2.11 | surplus | 1.0 | 1.1 |
| CALABARZON | 10.6 | Low | 0.16 | deficit | 1.2 | 1.3 |
| MIMAROPA | 35.1 | High | 2.62 | surplus | 0.3 | 0.8 |
| Bicol Region | 40.6 | High | 1.30 | surplus | 0.5 | 1.7 |
| Western Visayas | 27.5 | Medium | 2.25 | surplus | 0.8 | 2.0 |
| Central Visayas | 34.2 | High | 0.19 | deficit | 0.6 | 1.0 |
| Eastern Visayas | 48.8 | High | 1.30 | surplus | 0.5 | 1.6 |
| Zamboanga Peninsula | 48.9 | High | 1.18 | deficit | 0.3 | 0.9 |
| Northern Mindanao | 50.8 | High | 1.09 | deficit | 0.4 | 1.0 |
| Davao Region | 30.8 | Medium | 0.61 | deficit | 0.5 | 1.0 |
| SOCCSKSARGEN | 37.5 | High | 1.54 | surplus | 0.5 | 1.4 |
| Caraga Region | 47.0 | High | 1.37 | surplus | 0.3 | 0.9 |
| BARMM | 76.2 | High | 1.45 | surplus | 0.2 | 1.2 |


### Table A4. Rice inflation by period

| Period | Rice CPI, % a year | Rice CPI, SD monthly | World rice (PHP), % a year | World, SD monthly | Months |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1995M1-2007M9 | 4.6 | 1.36 | 6.8 | 4.76 | 153 |
| 2007M10-2008M12 (world crisis) | 16.1 | 3.31 | 42.7 | 15.24 | 15 |
| 2009M1-2019M2 (quotas) | 3.2 | 0.82 | −1.8 | 4.37 | 122 |
| 2019M3-2024M6 (35% tariff) | 3.3 | 1.52 | 10.4 | 5.09 | 64 |
| 2024M7-2026M9 (15% tariff, suspension, indexed tariff) | −0.4 | 2.33 | −9.2 | 6.29 | 27 |


### Table A5. Annual inflation and rice contributions

| Year | Rice, all | Rice, bottom 30% | Headline, all | Headline, bottom 30% | World rice (PHP) | Rice contribution, all | Rice contribution, bottom 30% |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2012 | 2.1 | nan | 2.8 | 2.8 | −11.1 | 0.18 | nan |
| 2013 | 8.1 | 6.8 | 3.7 | 4.5 | −14.0 | 0.71 | 1.22 |
| 2014 | 7.6 | 7.0 | 1.9 | 3.0 | −6.3 | 0.67 | 1.25 |
| 2015 | −2.6 | −2.4 | 0.7 | 0.8 | −8.6 | −0.23 | −0.42 |
| 2016 | 0.5 | 0.5 | 2.2 | 1.8 | 8.0 | 0.05 | 0.09 |
| 2017 | 1.1 | 0.6 | 2.9 | 2.6 | 9.6 | 0.10 | 0.11 |
| 2018 | 6.2 | 7.0 | 5.0 | 6.0 | 4.1 | 0.55 | 1.24 |
| 2019 | −10.1 | −11.8 | 2.3 | 1.3 | 2.8 | −0.90 | −2.10 |
| 2020 | 0.1 | −0.2 | 3.2 | 3.6 | 13.1 | 0.01 | −0.03 |
| 2021 | −0.1 | −0.2 | 3.0 | 3.3 | −21.8 | −0.01 | −0.04 |
| 2022 | 3.4 | 3.8 | 7.7 | 9.0 | 25.8 | 0.30 | 0.68 |
| 2023 | 17.9 | 19.4 | 3.9 | 4.8 | 32.0 | 1.59 | 3.46 |
| 2024 | 0.8 | 0.7 | 2.9 | 2.5 | −15.0 | 0.07 | 0.12 |
| 2025 | −13.1 | −15.1 | 1.8 | 1.1 | −21.1 | −1.17 | −2.69 |
| 2026 | 18.5 | 21.2 | 6.9 | 8.6 | 34.3 | 1.64 | 3.78 |


### Table A6. Replication gate

| Criterion | Target | Result | Pass |
| :--- | :--- | :--- | :--- |
| G1 rice CPI means within 0.5 of Table 1 | >= 15 of 17 | 17 of 17 (median \|dev\| 0.000) | yes |
| G1 rice CPI SDs within 0.5 of Table 1 | >= 15 of 17 | 17 of 17 (median \|dev\| 0.000) | yes |
| G1b fuel CPI means within 0.5 (better candidate) | >= 15 of 17 | cpi_fuel_tr: 17 of 17 (median \|dev\| 0.000; other cpi_fuel_hh: 6.338) | yes |
| G2(i) THAI->RPI 95% band above zero at h=1 | lo > 0 | irf 0.256 [0.215, 0.303] | yes |
| G2(ii) THAI->RPI peaks at h=1 or 2 | h in {1,2} | peak at h=1 (0.256) | yes |
| G2(iii) THAI->RPI below 25% of peak by h=6 | < 0.25 x peak | h=6: 0.002 (0.01 of peak) | yes |
| G2(iv) FPI->RPI positive at h=0 | > 0 | 0.143 [0.143, 0.143] | yes |
| G2(v) FPI->RPI below 25% of impact by h=3 | < 0.25 x h0 | h=3: -0.006 (-0.04 of impact) | yes |
| G3 peak ratio insufficient/sufficient | in [1.3, 3.0] | 1.26 (0.296 / 0.235) | **no** |
| G3 peak high poverty < low poverty | high < low | high 0.260 vs low 0.255 | **no** |


### Table A7. Border gap regressions

|  | Wholesale (1) | Wholesale (2) | Retail (1) | Retail (2) |
| :--- | ---: | ---: | ---: | ---: |
| Law in force (from Mar 2019) | −11.2* (6.6) | 5.5 (5.4) | −11.4 (7.2) | 7.4 (5.1) |
| 15% tariff (from Jul 2024) | 10.6** (4.5) | 15.2*** (4.5) | 9.4** (4.8) | 14.6*** (3.6) |
| Import suspension (Sep–Dec 2025) | 2.0 (4.3) | −13.8*** (4.2) | 2.3 (4.0) | −15.4*** (3.5) |
| World price (log × 100) |  | −0.83*** (0.18) |  | −0.93*** (0.17) |


## B. All local projection estimates

### Table B1. full_sample — dl_rice

RQ1, regional rice CPI, one regime, 1995M1–2026M9

| h | shock | N | Units |
| :--- | ---: | ---: | ---: |
| 0 | 0.043** (0.018) | 6460 | 17 |
| 1 | 0.118*** (0.029) | 6443 | 17 |
| 2 | 0.127*** (0.037) | 6426 | 17 |
| 3 | 0.189*** (0.045) | 6409 | 17 |
| 4 | 0.231*** (0.052) | 6392 | 17 |
| 5 | 0.241*** (0.048) | 6375 | 17 |
| 6 | 0.228*** (0.042) | 6358 | 17 |
| 7 | 0.232*** (0.046) | 6341 | 17 |
| 8 | 0.250*** (0.046) | 6324 | 17 |
| 9 | 0.239*** (0.045) | 6307 | 17 |
| 10 | 0.232*** (0.052) | 6290 | 17 |
| 11 | 0.240*** (0.055) | 6273 | 17 |
| 12 | 0.243*** (0.058) | 6256 | 17 |


### Table B2. main — dl_rice

RQ1 main: shock = before the law, shock_x_post = change

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.036 (0.023) | 0.030 (0.037) | 6460 | 17 |
| 1 | 0.099*** (0.033) | 0.083 (0.090) | 6443 | 17 |
| 2 | 0.103** (0.050) | 0.096 (0.104) | 6426 | 17 |
| 3 | 0.154** (0.062) | 0.143 (0.127) | 6409 | 17 |
| 4 | 0.171** (0.070) | 0.253* (0.153) | 6392 | 17 |
| 5 | 0.164** (0.064) | 0.323** (0.160) | 6375 | 17 |
| 6 | 0.157*** (0.050) | 0.303* (0.162) | 6358 | 17 |
| 7 | 0.161*** (0.050) | 0.310* (0.164) | 6341 | 17 |
| 8 | 0.173*** (0.045) | 0.331** (0.168) | 6324 | 17 |
| 9 | 0.168*** (0.049) | 0.310* (0.173) | 6307 | 17 |
| 10 | 0.178*** (0.059) | 0.250 (0.198) | 6290 | 17 |
| 11 | 0.196*** (0.066) | 0.206 (0.207) | 6273 | 17 |
| 12 | 0.201*** (0.072) | 0.199 (0.210) | 6256 | 17 |


### Table B3. main_postparam — dl_rice

RQ1 main re-parametrised: shock = after the law

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.066** (0.027) | −0.030 (0.037) | 6460 | 17 |
| 1 | 0.181** (0.082) | −0.083 (0.090) | 6443 | 17 |
| 2 | 0.199** (0.082) | −0.096 (0.104) | 6426 | 17 |
| 3 | 0.298*** (0.101) | −0.143 (0.127) | 6409 | 17 |
| 4 | 0.424*** (0.125) | −0.253* (0.153) | 6392 | 17 |
| 5 | 0.487*** (0.134) | −0.323** (0.160) | 6375 | 17 |
| 6 | 0.460*** (0.141) | −0.303* (0.162) | 6358 | 17 |
| 7 | 0.471*** (0.143) | −0.310* (0.164) | 6341 | 17 |
| 8 | 0.504*** (0.149) | −0.331** (0.168) | 6324 | 17 |
| 9 | 0.478*** (0.151) | −0.310* (0.173) | 6307 | 17 |
| 10 | 0.428** (0.174) | −0.250 (0.198) | 6290 | 17 |
| 11 | 0.402** (0.179) | −0.206 (0.207) | 6273 | 17 |
| 12 | 0.400** (0.178) | −0.199 (0.210) | 6256 | 17 |


### Table B4. national — dl_rice

RQ1, national rice CPI (Newey–West)

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.045 (0.028) | 0.019 (0.040) | 380 | 1 |
| 1 | 0.107*** (0.039) | 0.048 (0.093) | 379 | 1 |
| 2 | 0.112** (0.055) | 0.042 (0.108) | 378 | 1 |
| 3 | 0.163** (0.067) | 0.087 (0.131) | 377 | 1 |
| 4 | 0.180** (0.073) | 0.192 (0.151) | 376 | 1 |
| 5 | 0.172** (0.071) | 0.281* (0.152) | 375 | 1 |
| 6 | 0.165*** (0.057) | 0.275* (0.150) | 374 | 1 |
| 7 | 0.170*** (0.056) | 0.276* (0.149) | 373 | 1 |
| 8 | 0.184*** (0.050) | 0.293* (0.157) | 372 | 1 |
| 9 | 0.182*** (0.055) | 0.269* (0.163) | 371 | 1 |
| 10 | 0.188*** (0.066) | 0.225 (0.188) | 370 | 1 |
| 11 | 0.201*** (0.072) | 0.193 (0.196) | 369 | 1 |
| 12 | 0.206*** (0.077) | 0.184 (0.200) | 368 | 1 |


### Table B5. national_postparam — dl_rice

RQ1, national, after the law

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.064** (0.028) | −0.019 (0.040) | 380 | 1 |
| 1 | 0.155* (0.082) | −0.048 (0.093) | 379 | 1 |
| 2 | 0.154* (0.084) | −0.042 (0.108) | 378 | 1 |
| 3 | 0.250** (0.102) | −0.087 (0.131) | 377 | 1 |
| 4 | 0.372*** (0.122) | −0.192 (0.151) | 376 | 1 |
| 5 | 0.454*** (0.124) | −0.281* (0.152) | 375 | 1 |
| 6 | 0.439*** (0.129) | −0.275* (0.150) | 374 | 1 |
| 7 | 0.446*** (0.129) | −0.276* (0.149) | 373 | 1 |
| 8 | 0.478*** (0.138) | −0.293* (0.157) | 372 | 1 |
| 9 | 0.451*** (0.141) | −0.269* (0.163) | 371 | 1 |
| 10 | 0.412** (0.162) | −0.225 (0.188) | 370 | 1 |
| 11 | 0.394** (0.167) | −0.193 (0.196) | 369 | 1 |
| 12 | 0.390** (0.167) | −0.184 (0.200) | 368 | 1 |


### Table B6. chain_national — dl_farmgate_palay

RQ2, national chain prices 2011M1–2026M9

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.035 (0.063) | 0.218** (0.106) | 188 | 1 |
| 1 | 0.028 (0.120) | 0.422*** (0.160) | 187 | 1 |
| 2 | −0.026 (0.167) | 0.586*** (0.217) | 186 | 1 |
| 3 | −0.039 (0.179) | 0.687*** (0.255) | 185 | 1 |
| 4 | −0.024 (0.174) | 0.754*** (0.272) | 184 | 1 |
| 5 | −0.040 (0.192) | 0.782*** (0.284) | 183 | 1 |
| 6 | −0.002 (0.222) | 0.742** (0.355) | 182 | 1 |
| 7 | 0.007 (0.275) | 0.726* (0.403) | 181 | 1 |
| 8 | −0.044 (0.312) | 0.743* (0.421) | 180 | 1 |
| 9 | −0.076 (0.315) | 0.727* (0.430) | 179 | 1 |
| 10 | −0.018 (0.329) | 0.565 (0.435) | 178 | 1 |
| 11 | 0.040 (0.319) | 0.570 (0.411) | 177 | 1 |
| 12 | 0.029 (0.292) | 0.560 (0.390) | 176 | 1 |


### Table B6. chain_national — dl_wholesale_rmr

RQ2, national chain prices 2011M1–2026M9

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.055 (0.066) | 0.082 (0.090) | 188 | 1 |
| 1 | 0.067 (0.085) | 0.159 (0.143) | 187 | 1 |
| 2 | −0.023 (0.110) | 0.283 (0.175) | 186 | 1 |
| 3 | −0.135 (0.137) | 0.511** (0.207) | 185 | 1 |
| 4 | −0.161 (0.156) | 0.693*** (0.226) | 184 | 1 |
| 5 | −0.063 (0.174) | 0.658*** (0.227) | 183 | 1 |
| 6 | −0.165 (0.190) | 0.772*** (0.257) | 182 | 1 |
| 7 | 0.051 (0.256) | 0.595* (0.310) | 181 | 1 |
| 8 | −0.060 (0.233) | 0.679** (0.309) | 180 | 1 |
| 9 | −0.123 (0.269) | 0.702** (0.348) | 179 | 1 |
| 10 | −0.052 (0.296) | 0.607 (0.375) | 178 | 1 |
| 11 | −0.070 (0.307) | 0.596 (0.399) | 177 | 1 |
| 12 | −0.112 (0.290) | 0.613 (0.392) | 176 | 1 |


### Table B6. chain_national — dl_retail_rmr

RQ2, national chain prices 2011M1–2026M9

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.002 (0.031) | 0.051 (0.044) | 188 | 1 |
| 1 | 0.005 (0.056) | 0.138 (0.118) | 187 | 1 |
| 2 | −0.032 (0.074) | 0.186 (0.138) | 186 | 1 |
| 3 | −0.045 (0.087) | 0.303** (0.152) | 185 | 1 |
| 4 | −0.062 (0.100) | 0.465*** (0.171) | 184 | 1 |
| 5 | −0.077 (0.114) | 0.580*** (0.178) | 183 | 1 |
| 6 | −0.030 (0.131) | 0.556*** (0.194) | 182 | 1 |
| 7 | −0.012 (0.147) | 0.519** (0.204) | 181 | 1 |
| 8 | 0.018 (0.159) | 0.534** (0.222) | 180 | 1 |
| 9 | −0.007 (0.177) | 0.491** (0.244) | 179 | 1 |
| 10 | −0.021 (0.193) | 0.516* (0.269) | 178 | 1 |
| 11 | −0.045 (0.203) | 0.531* (0.289) | 177 | 1 |
| 12 | −0.036 (0.205) | 0.487* (0.291) | 176 | 1 |


### Table B6. chain_national — dl_rice

RQ2, national chain prices 2011M1–2026M9

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | −0.002 (0.028) | 0.050 (0.041) | 189 | 1 |
| 1 | 0.003 (0.047) | 0.126 (0.105) | 188 | 1 |
| 2 | −0.042 (0.063) | 0.178 (0.119) | 187 | 1 |
| 3 | −0.058 (0.074) | 0.286** (0.133) | 186 | 1 |
| 4 | −0.070 (0.083) | 0.417*** (0.150) | 185 | 1 |
| 5 | −0.079 (0.095) | 0.505*** (0.158) | 184 | 1 |
| 6 | −0.033 (0.110) | 0.479*** (0.172) | 183 | 1 |
| 7 | −0.031 (0.121) | 0.463*** (0.178) | 182 | 1 |
| 8 | −0.009 (0.131) | 0.469** (0.191) | 181 | 1 |
| 9 | −0.022 (0.142) | 0.434** (0.203) | 180 | 1 |
| 10 | −0.041 (0.154) | 0.468** (0.223) | 179 | 1 |
| 11 | −0.055 (0.162) | 0.476** (0.239) | 178 | 1 |
| 12 | −0.046 (0.164) | 0.444* (0.239) | 177 | 1 |


### Table B7. chain_national_postparam — dl_farmgate_palay

RQ2, after the law

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.252*** (0.097) | −0.218** (0.106) | 188 | 1 |
| 1 | 0.450*** (0.115) | −0.422*** (0.160) | 187 | 1 |
| 2 | 0.560*** (0.127) | −0.586*** (0.217) | 186 | 1 |
| 3 | 0.648*** (0.164) | −0.687*** (0.255) | 185 | 1 |
| 4 | 0.730*** (0.183) | −0.754*** (0.272) | 184 | 1 |
| 5 | 0.742*** (0.204) | −0.782*** (0.284) | 183 | 1 |
| 6 | 0.740*** (0.251) | −0.742** (0.355) | 182 | 1 |
| 7 | 0.733*** (0.245) | −0.726* (0.403) | 181 | 1 |
| 8 | 0.699*** (0.206) | −0.743* (0.421) | 180 | 1 |
| 9 | 0.651*** (0.214) | −0.727* (0.430) | 179 | 1 |
| 10 | 0.547*** (0.211) | −0.565 (0.435) | 178 | 1 |
| 11 | 0.610*** (0.188) | −0.570 (0.411) | 177 | 1 |
| 12 | 0.589*** (0.201) | −0.560 (0.390) | 176 | 1 |


### Table B7. chain_national_postparam — dl_wholesale_rmr

RQ2, after the law

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.137** (0.058) | −0.082 (0.090) | 188 | 1 |
| 1 | 0.226** (0.104) | −0.159 (0.143) | 187 | 1 |
| 2 | 0.260** (0.109) | −0.283 (0.175) | 186 | 1 |
| 3 | 0.377*** (0.134) | −0.511** (0.207) | 185 | 1 |
| 4 | 0.531*** (0.138) | −0.693*** (0.226) | 184 | 1 |
| 5 | 0.596*** (0.132) | −0.658*** (0.227) | 183 | 1 |
| 6 | 0.607*** (0.159) | −0.772*** (0.257) | 182 | 1 |
| 7 | 0.646*** (0.155) | −0.595* (0.310) | 181 | 1 |
| 8 | 0.620*** (0.155) | −0.679** (0.309) | 180 | 1 |
| 9 | 0.579*** (0.164) | −0.702** (0.348) | 179 | 1 |
| 10 | 0.555*** (0.158) | −0.607 (0.375) | 178 | 1 |
| 11 | 0.526*** (0.165) | −0.596 (0.399) | 177 | 1 |
| 12 | 0.501*** (0.170) | −0.613 (0.392) | 176 | 1 |


### Table B7. chain_national_postparam — dl_retail_rmr

RQ2, after the law

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.053* (0.029) | −0.051 (0.044) | 188 | 1 |
| 1 | 0.144 (0.094) | −0.138 (0.118) | 187 | 1 |
| 2 | 0.155 (0.096) | −0.186 (0.138) | 186 | 1 |
| 3 | 0.258** (0.110) | −0.303** (0.152) | 185 | 1 |
| 4 | 0.403*** (0.123) | −0.465*** (0.171) | 184 | 1 |
| 5 | 0.503*** (0.123) | −0.580*** (0.178) | 183 | 1 |
| 6 | 0.526*** (0.132) | −0.556*** (0.194) | 182 | 1 |
| 7 | 0.507*** (0.137) | −0.519** (0.204) | 181 | 1 |
| 8 | 0.552*** (0.146) | −0.534** (0.222) | 180 | 1 |
| 9 | 0.484*** (0.143) | −0.491** (0.244) | 179 | 1 |
| 10 | 0.495*** (0.156) | −0.516* (0.269) | 178 | 1 |
| 11 | 0.485*** (0.164) | −0.531* (0.289) | 177 | 1 |
| 12 | 0.451*** (0.169) | −0.487* (0.291) | 176 | 1 |


### Table B7. chain_national_postparam — dl_rice

RQ2, after the law

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.048* (0.027) | −0.050 (0.041) | 189 | 1 |
| 1 | 0.129 (0.084) | −0.126 (0.105) | 188 | 1 |
| 2 | 0.137* (0.081) | −0.178 (0.119) | 187 | 1 |
| 3 | 0.228** (0.094) | −0.286** (0.133) | 186 | 1 |
| 4 | 0.347*** (0.109) | −0.417*** (0.150) | 185 | 1 |
| 5 | 0.425*** (0.111) | −0.505*** (0.158) | 184 | 1 |
| 6 | 0.445*** (0.119) | −0.479*** (0.172) | 183 | 1 |
| 7 | 0.432*** (0.122) | −0.463*** (0.178) | 182 | 1 |
| 8 | 0.460*** (0.129) | −0.469** (0.191) | 181 | 1 |
| 9 | 0.412*** (0.124) | −0.434** (0.203) | 180 | 1 |
| 10 | 0.427*** (0.137) | −0.468** (0.223) | 179 | 1 |
| 11 | 0.421*** (0.143) | −0.476** (0.239) | 178 | 1 |
| 12 | 0.398*** (0.142) | −0.444* (0.239) | 177 | 1 |


### Table B8. farmgate_regional — dl_farmgate_palay

RQ2 check, regional farmgate panel (16 regions; no farmgate data for NCR)

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.058 (0.074) | 0.222* (0.115) | 2959 | 16 |
| 1 | 0.062 (0.131) | 0.420** (0.177) | 2942 | 16 |
| 2 | 0.018 (0.178) | 0.596** (0.238) | 2925 | 16 |
| 3 | 0.010 (0.194) | 0.706** (0.279) | 2908 | 16 |
| 4 | 0.040 (0.191) | 0.764*** (0.289) | 2891 | 16 |
| 5 | 0.022 (0.206) | 0.781*** (0.287) | 2874 | 16 |
| 6 | 0.082 (0.229) | 0.691** (0.335) | 2857 | 16 |
| 7 | 0.100 (0.278) | 0.662* (0.389) | 2840 | 16 |
| 8 | 0.047 (0.325) | 0.685 (0.419) | 2823 | 16 |
| 9 | 0.011 (0.340) | 0.691 (0.435) | 2806 | 16 |
| 10 | 0.053 (0.350) | 0.506 (0.441) | 2789 | 16 |
| 11 | 0.103 (0.343) | 0.522 (0.424) | 2772 | 16 |
| 12 | 0.071 (0.307) | 0.540 (0.392) | 2755 | 16 |


### Table B9. farmgate_regional_postparam — dl_farmgate_palay

RQ2 check, after the law

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.280*** (0.090) | −0.222* (0.115) | 2959 | 16 |
| 1 | 0.482*** (0.110) | −0.420** (0.177) | 2942 | 16 |
| 2 | 0.614*** (0.135) | −0.596** (0.238) | 2925 | 16 |
| 3 | 0.715*** (0.178) | −0.706** (0.279) | 2908 | 16 |
| 4 | 0.803*** (0.187) | −0.764*** (0.289) | 2891 | 16 |
| 5 | 0.803*** (0.195) | −0.781*** (0.287) | 2874 | 16 |
| 6 | 0.773*** (0.232) | −0.691** (0.335) | 2857 | 16 |
| 7 | 0.762*** (0.226) | −0.662* (0.389) | 2840 | 16 |
| 8 | 0.731*** (0.203) | −0.685 (0.419) | 2823 | 16 |
| 9 | 0.703*** (0.204) | −0.691 (0.435) | 2806 | 16 |
| 10 | 0.559*** (0.188) | −0.506 (0.441) | 2789 | 16 |
| 11 | 0.625*** (0.174) | −0.522 (0.424) | 2772 | 16 |
| 12 | 0.611*** (0.188) | −0.540 (0.392) | 2755 | 16 |


### Table B10. retail_regional — dl_retail_rmr

RQ2 check, regional retail RMR panel

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.002 (0.034) | 0.056 (0.046) | 3196 | 17 |
| 1 | 0.012 (0.061) | 0.147 (0.117) | 3179 | 17 |
| 2 | −0.025 (0.078) | 0.202 (0.135) | 3162 | 17 |
| 3 | −0.042 (0.092) | 0.313** (0.152) | 3145 | 17 |
| 4 | −0.056 (0.104) | 0.477*** (0.171) | 3128 | 17 |
| 5 | −0.057 (0.123) | 0.567*** (0.187) | 3111 | 17 |
| 6 | −0.012 (0.143) | 0.528** (0.206) | 3094 | 17 |
| 7 | 0.001 (0.158) | 0.508** (0.215) | 3077 | 17 |
| 8 | 0.021 (0.173) | 0.524** (0.232) | 3060 | 17 |
| 9 | −0.001 (0.194) | 0.495* (0.255) | 3043 | 17 |
| 10 | −0.017 (0.210) | 0.505* (0.281) | 3026 | 17 |
| 11 | −0.041 (0.217) | 0.503* (0.295) | 3009 | 17 |
| 12 | −0.029 (0.220) | 0.458 (0.294) | 2992 | 17 |


### Table B11. retail_regional_postparam — dl_retail_rmr

RQ2 check, after the law

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.058** (0.029) | −0.056 (0.046) | 3196 | 17 |
| 1 | 0.159* (0.089) | −0.147 (0.117) | 3179 | 17 |
| 2 | 0.177** (0.089) | −0.202 (0.135) | 3162 | 17 |
| 3 | 0.271** (0.106) | −0.313** (0.152) | 3145 | 17 |
| 4 | 0.421*** (0.121) | −0.477*** (0.171) | 3128 | 17 |
| 5 | 0.510*** (0.125) | −0.567*** (0.187) | 3111 | 17 |
| 6 | 0.516*** (0.137) | −0.528** (0.206) | 3094 | 17 |
| 7 | 0.509*** (0.139) | −0.508** (0.215) | 3077 | 17 |
| 8 | 0.545*** (0.145) | −0.524** (0.232) | 3060 | 17 |
| 9 | 0.494*** (0.142) | −0.495* (0.255) | 3043 | 17 |
| 10 | 0.488*** (0.156) | −0.505* (0.281) | 3026 | 17 |
| 11 | 0.462*** (0.157) | −0.503* (0.295) | 3009 | 17 |
| 12 | 0.428*** (0.155) | −0.458 (0.294) | 2992 | 17 |


### Table B12. het_insuff — dl_rice

RQ4, rice-deficit regions (not validated)

| h | shock | shock_x_insuff | shock_x_post | shock_x_post_insuff | N | Units |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.031 (0.023) | 0.015 (0.009) | 0.031 (0.036) | −0.003 (0.016) | 6460 | 17 |
| 1 | 0.088*** (0.031) | 0.030*** (0.011) | 0.082 (0.084) | 0.003 (0.031) | 6443 | 17 |
| 2 | 0.086** (0.043) | 0.049* (0.027) | 0.111 (0.098) | −0.044 (0.038) | 6426 | 17 |
| 3 | 0.130** (0.051) | 0.068* (0.040) | 0.174 (0.119) | −0.088* (0.050) | 6409 | 17 |
| 4 | 0.148** (0.060) | 0.067* (0.035) | 0.284* (0.149) | −0.090* (0.050) | 6392 | 17 |
| 5 | 0.149** (0.060) | 0.044** (0.022) | 0.346** (0.163) | −0.067 (0.046) | 6375 | 17 |
| 6 | 0.148*** (0.049) | 0.027* (0.015) | 0.325* (0.169) | −0.063 (0.045) | 6358 | 17 |
| 7 | 0.160*** (0.051) | 0.003 (0.015) | 0.336* (0.173) | −0.072 (0.048) | 6341 | 17 |
| 8 | 0.174*** (0.046) | −0.003 (0.016) | 0.352** (0.174) | −0.058 (0.055) | 6324 | 17 |
| 9 | 0.168*** (0.051) | 0.001 (0.017) | 0.336* (0.180) | −0.072 (0.059) | 6307 | 17 |
| 10 | 0.178*** (0.060) | −0.001 (0.015) | 0.273 (0.206) | −0.065 (0.066) | 6290 | 17 |
| 11 | 0.195*** (0.066) | 0.004 (0.017) | 0.231 (0.211) | −0.069 (0.071) | 6273 | 17 |
| 12 | 0.199*** (0.073) | 0.004 (0.014) | 0.216 (0.209) | −0.047 (0.066) | 6256 | 17 |


### Table B13. het_highpov — dl_rice

RQ4, high-poverty regions (not validated)

| h | shock | shock_x_highpov | shock_x_post | shock_x_post_highpov | N | Units |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.043 (0.029) | −0.013 (0.014) | 0.023 (0.041) | 0.012 (0.017) | 6460 | 17 |
| 1 | 0.105*** (0.039) | −0.012 (0.015) | 0.051 (0.086) | 0.060** (0.026) | 6443 | 17 |
| 2 | 0.106* (0.054) | −0.006 (0.015) | 0.057 (0.097) | 0.074** (0.034) | 6426 | 17 |
| 3 | 0.153** (0.063) | 0.003 (0.013) | 0.107 (0.118) | 0.070* (0.037) | 6409 | 17 |
| 4 | 0.172** (0.071) | −0.002 (0.012) | 0.207 (0.146) | 0.086*** (0.032) | 6392 | 17 |
| 5 | 0.170** (0.071) | −0.011 (0.017) | 0.273* (0.158) | 0.093*** (0.033) | 6375 | 17 |
| 6 | 0.164*** (0.060) | −0.012 (0.024) | 0.257 (0.159) | 0.088** (0.040) | 6358 | 17 |
| 7 | 0.167*** (0.060) | −0.012 (0.027) | 0.269* (0.156) | 0.078 (0.048) | 6341 | 17 |
| 8 | 0.184*** (0.054) | −0.022 (0.027) | 0.290* (0.159) | 0.078 (0.049) | 6324 | 17 |
| 9 | 0.186*** (0.057) | −0.035 (0.027) | 0.272 (0.167) | 0.072 (0.046) | 6307 | 17 |
| 10 | 0.197*** (0.068) | −0.036 (0.026) | 0.215 (0.191) | 0.065 (0.045) | 6290 | 17 |
| 11 | 0.211*** (0.075) | −0.027 (0.023) | 0.176 (0.200) | 0.057 (0.051) | 6273 | 17 |
| 12 | 0.217*** (0.081) | −0.031 (0.022) | 0.170 (0.202) | 0.056 (0.053) | 6256 | 17 |


### Table B14. gap_full — dD

RQ5, gap all income − bottom 30%, 2001M1–2026M9

| h | shock | N | Units |
| :--- | ---: | ---: | ---: |
| 0 | −0.014*** (0.004) | 308 | 1 |
| 1 | −0.031*** (0.006) | 307 | 1 |
| 2 | −0.042*** (0.012) | 306 | 1 |
| 3 | −0.053*** (0.015) | 305 | 1 |
| 4 | −0.059*** (0.015) | 304 | 1 |
| 5 | −0.063*** (0.014) | 303 | 1 |
| 6 | −0.060*** (0.010) | 302 | 1 |
| 7 | −0.056*** (0.010) | 301 | 1 |
| 8 | −0.062*** (0.010) | 300 | 1 |
| 9 | −0.050*** (0.010) | 299 | 1 |
| 10 | −0.054*** (0.014) | 298 | 1 |
| 11 | −0.053*** (0.017) | 297 | 1 |
| 12 | −0.052*** (0.016) | 296 | 1 |


### Table B15. gap — dD

RQ5 gap with regime interaction

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | −0.013** (0.005) | −0.004 (0.008) | 308 | 1 |
| 1 | −0.031*** (0.009) | −0.001 (0.012) | 307 | 1 |
| 2 | −0.050*** (0.015) | 0.021 (0.019) | 306 | 1 |
| 3 | −0.063*** (0.020) | 0.032 (0.025) | 305 | 1 |
| 4 | −0.067*** (0.020) | 0.025 (0.025) | 304 | 1 |
| 5 | −0.069*** (0.019) | 0.017 (0.024) | 303 | 1 |
| 6 | −0.065*** (0.014) | 0.018 (0.021) | 302 | 1 |
| 7 | −0.065*** (0.014) | 0.028 (0.020) | 301 | 1 |
| 8 | −0.071*** (0.013) | 0.028 (0.020) | 300 | 1 |
| 9 | −0.059*** (0.014) | 0.029 (0.023) | 299 | 1 |
| 10 | −0.064*** (0.018) | 0.033 (0.027) | 298 | 1 |
| 11 | −0.064*** (0.022) | 0.037 (0.030) | 297 | 1 |
| 12 | −0.061*** (0.022) | 0.031 (0.030) | 296 | 1 |


### Table B16. gap_postparam — dD

RQ5 gap after the law

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | −0.017*** (0.006) | 0.004 (0.008) | 308 | 1 |
| 1 | −0.032*** (0.007) | 0.001 (0.012) | 307 | 1 |
| 2 | −0.028*** (0.010) | −0.021 (0.019) | 306 | 1 |
| 3 | −0.031*** (0.012) | −0.032 (0.025) | 305 | 1 |
| 4 | −0.042*** (0.011) | −0.025 (0.025) | 304 | 1 |
| 5 | −0.052*** (0.013) | −0.017 (0.024) | 303 | 1 |
| 6 | −0.047*** (0.014) | −0.018 (0.021) | 302 | 1 |
| 7 | −0.037*** (0.011) | −0.028 (0.020) | 301 | 1 |
| 8 | −0.042*** (0.010) | −0.028 (0.020) | 300 | 1 |
| 9 | −0.029** (0.012) | −0.029 (0.023) | 299 | 1 |
| 10 | −0.030** (0.015) | −0.033 (0.027) | 298 | 1 |
| 11 | −0.027* (0.014) | −0.037 (0.030) | 297 | 1 |
| 12 | −0.030** (0.014) | −0.031 (0.030) | 296 | 1 |


### Table B17. rice_national_2001 — dl_rice

RQ5 mechanism, national rice CPI 2001M1–2026M9

| h | shock | N | Units |
| :--- | ---: | ---: | ---: |
| 0 | 0.056** (0.023) | 309 | 1 |
| 1 | 0.130*** (0.038) | 308 | 1 |
| 2 | 0.143*** (0.044) | 307 | 1 |
| 3 | 0.196*** (0.052) | 306 | 1 |
| 4 | 0.251*** (0.057) | 305 | 1 |
| 5 | 0.268*** (0.058) | 304 | 1 |
| 6 | 0.240*** (0.050) | 303 | 1 |
| 7 | 0.239*** (0.052) | 302 | 1 |
| 8 | 0.253*** (0.051) | 301 | 1 |
| 9 | 0.244*** (0.055) | 300 | 1 |
| 10 | 0.234*** (0.066) | 299 | 1 |
| 11 | 0.233*** (0.073) | 298 | 1 |
| 12 | 0.239*** (0.075) | 297 | 1 |


### Table B18. all_items — dl_all

RQ5, all-items CPI, all income

| h | shock | N | Units |
| :--- | ---: | ---: | ---: |
| 0 | 0.013*** (0.004) | 309 | 1 |
| 1 | 0.024*** (0.007) | 308 | 1 |
| 2 | 0.024*** (0.008) | 307 | 1 |
| 3 | 0.033*** (0.010) | 306 | 1 |
| 4 | 0.047*** (0.011) | 305 | 1 |
| 5 | 0.052*** (0.009) | 304 | 1 |
| 6 | 0.045*** (0.009) | 303 | 1 |
| 7 | 0.050*** (0.008) | 302 | 1 |
| 8 | 0.048*** (0.007) | 301 | 1 |
| 9 | 0.052*** (0.008) | 300 | 1 |
| 10 | 0.044*** (0.010) | 299 | 1 |
| 11 | 0.045*** (0.011) | 298 | 1 |
| 12 | 0.043*** (0.012) | 297 | 1 |


### Table B19. all_items_b30 — dl_all_b30

RQ5, all-items CPI, bottom 30%

| h | shock | N | Units |
| :--- | ---: | ---: | ---: |
| 0 | 0.028*** (0.007) | 308 | 1 |
| 1 | 0.056*** (0.011) | 307 | 1 |
| 2 | 0.068*** (0.018) | 306 | 1 |
| 3 | 0.089*** (0.023) | 305 | 1 |
| 4 | 0.108*** (0.024) | 304 | 1 |
| 5 | 0.120*** (0.022) | 303 | 1 |
| 6 | 0.110*** (0.018) | 302 | 1 |
| 7 | 0.111*** (0.017) | 301 | 1 |
| 8 | 0.113*** (0.014) | 300 | 1 |
| 9 | 0.104*** (0.016) | 299 | 1 |
| 10 | 0.101*** (0.020) | 298 | 1 |
| 11 | 0.100*** (0.025) | 297 | 1 |
| 12 | 0.100*** (0.026) | 296 | 1 |


### Table B20. a_real_shock — dl_rice

Robustness check, a real shock

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.029 (0.024) | 0.026 (0.038) | 6460 | 17 |
| 1 | 0.088** (0.035) | 0.080 (0.095) | 6443 | 17 |
| 2 | 0.099* (0.053) | 0.093 (0.110) | 6426 | 17 |
| 3 | 0.150** (0.066) | 0.140 (0.132) | 6409 | 17 |
| 4 | 0.168** (0.074) | 0.254 (0.158) | 6392 | 17 |
| 5 | 0.162** (0.070) | 0.336** (0.167) | 6375 | 17 |
| 6 | 0.157*** (0.055) | 0.315* (0.166) | 6358 | 17 |
| 7 | 0.160*** (0.054) | 0.326* (0.171) | 6341 | 17 |
| 8 | 0.169*** (0.048) | 0.346* (0.178) | 6324 | 17 |
| 9 | 0.167*** (0.051) | 0.330* (0.184) | 6307 | 17 |
| 10 | 0.176*** (0.062) | 0.265 (0.210) | 6290 | 17 |
| 11 | 0.194*** (0.069) | 0.218 (0.220) | 6273 | 17 |
| 12 | 0.199*** (0.076) | 0.213 (0.221) | 6256 | 17 |


### Table B21. a_real_shock_postparam — dl_rice

Robustness check, a real shock postparam

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.055* (0.028) | −0.026 (0.038) | 6460 | 17 |
| 1 | 0.168** (0.086) | −0.080 (0.095) | 6443 | 17 |
| 2 | 0.191** (0.088) | −0.093 (0.110) | 6426 | 17 |
| 3 | 0.290*** (0.105) | −0.140 (0.132) | 6409 | 17 |
| 4 | 0.422*** (0.129) | −0.254 (0.158) | 6392 | 17 |
| 5 | 0.499*** (0.140) | −0.336** (0.167) | 6375 | 17 |
| 6 | 0.472*** (0.145) | −0.315* (0.166) | 6358 | 17 |
| 7 | 0.486*** (0.151) | −0.326* (0.171) | 6341 | 17 |
| 8 | 0.515*** (0.160) | −0.346* (0.178) | 6324 | 17 |
| 9 | 0.496*** (0.163) | −0.330* (0.184) | 6307 | 17 |
| 10 | 0.441** (0.187) | −0.265 (0.210) | 6290 | 17 |
| 11 | 0.413** (0.192) | −0.218 (0.220) | 6273 | 17 |
| 12 | 0.412** (0.190) | −0.213 (0.221) | 6256 | 17 |


### Table B22. b_viet5 — dl_rice

Robustness check, b viet5

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.003 (0.023) | 0.082 (0.060) | 3519 | 17 |
| 1 | 0.022 (0.043) | 0.126 (0.098) | 3502 | 17 |
| 2 | −0.029 (0.047) | 0.103 (0.116) | 3468 | 17 |
| 3 | 0.071 (0.048) | 0.200 (0.157) | 3434 | 17 |
| 4 | 0.076 (0.060) | 0.210 (0.180) | 3400 | 17 |
| 5 | 0.066 (0.066) | 0.302 (0.192) | 3366 | 17 |
| 6 | 0.086 (0.086) | 0.330 (0.222) | 3332 | 17 |
| 7 | 0.104 (0.102) | 0.345 (0.264) | 3298 | 17 |
| 8 | 0.115 (0.109) | 0.393 (0.287) | 3264 | 17 |
| 9 | 0.111 (0.113) | 0.389 (0.300) | 3230 | 17 |
| 10 | 0.106 (0.110) | 0.407 (0.289) | 3196 | 17 |
| 11 | 0.116 (0.105) | 0.400 (0.261) | 3162 | 17 |
| 12 | 0.097 (0.106) | 0.290 (0.256) | 3145 | 17 |


### Table B23. b_viet5_postparam — dl_rice

Robustness check, b viet5 postparam

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.086 (0.057) | −0.082 (0.060) | 3519 | 17 |
| 1 | 0.147 (0.100) | −0.126 (0.098) | 3502 | 17 |
| 2 | 0.074 (0.098) | −0.103 (0.116) | 3468 | 17 |
| 3 | 0.271* (0.139) | −0.200 (0.157) | 3434 | 17 |
| 4 | 0.286* (0.149) | −0.210 (0.180) | 3400 | 17 |
| 5 | 0.367** (0.160) | −0.302 (0.192) | 3366 | 17 |
| 6 | 0.416** (0.180) | −0.330 (0.222) | 3332 | 17 |
| 7 | 0.450** (0.211) | −0.345 (0.264) | 3298 | 17 |
| 8 | 0.508** (0.227) | −0.393 (0.287) | 3264 | 17 |
| 9 | 0.500** (0.234) | −0.389 (0.300) | 3230 | 17 |
| 10 | 0.513** (0.227) | −0.407 (0.289) | 3196 | 17 |
| 11 | 0.516** (0.200) | −0.400 (0.261) | 3162 | 17 |
| 12 | 0.387* (0.204) | −0.290 (0.256) | 3145 | 17 |


### Table B24. c_usd_fx_control — dl_rice

Robustness check, c usd fx control

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.031 (0.024) | 0.022 (0.037) | 6460 | 17 |
| 1 | 0.092*** (0.032) | 0.072 (0.082) | 6443 | 17 |
| 2 | 0.110** (0.052) | 0.083 (0.103) | 6426 | 17 |
| 3 | 0.165*** (0.062) | 0.109 (0.123) | 6409 | 17 |
| 4 | 0.188*** (0.068) | 0.197 (0.151) | 6392 | 17 |
| 5 | 0.172*** (0.062) | 0.267 (0.165) | 6375 | 17 |
| 6 | 0.167*** (0.053) | 0.251 (0.176) | 6358 | 17 |
| 7 | 0.180*** (0.050) | 0.249 (0.187) | 6341 | 17 |
| 8 | 0.177*** (0.051) | 0.285 (0.199) | 6324 | 17 |
| 9 | 0.183*** (0.053) | 0.287 (0.205) | 6307 | 17 |
| 10 | 0.188*** (0.062) | 0.227 (0.239) | 6290 | 17 |
| 11 | 0.207*** (0.069) | 0.177 (0.253) | 6273 | 17 |
| 12 | 0.214*** (0.074) | 0.186 (0.257) | 6256 | 17 |


### Table B25. c_usd_fx_control_postparam — dl_rice

Robustness check, c usd fx control postparam

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.053** (0.026) | −0.022 (0.037) | 6460 | 17 |
| 1 | 0.164** (0.074) | −0.072 (0.082) | 6443 | 17 |
| 2 | 0.193** (0.079) | −0.083 (0.103) | 6426 | 17 |
| 3 | 0.274*** (0.094) | −0.109 (0.123) | 6409 | 17 |
| 4 | 0.386*** (0.122) | −0.197 (0.151) | 6392 | 17 |
| 5 | 0.439*** (0.137) | −0.267 (0.165) | 6375 | 17 |
| 6 | 0.418*** (0.149) | −0.251 (0.176) | 6358 | 17 |
| 7 | 0.429*** (0.160) | −0.249 (0.187) | 6341 | 17 |
| 8 | 0.462*** (0.171) | −0.285 (0.199) | 6324 | 17 |
| 9 | 0.470*** (0.175) | −0.287 (0.205) | 6307 | 17 |
| 10 | 0.415** (0.209) | −0.227 (0.239) | 6290 | 17 |
| 11 | 0.384* (0.216) | −0.177 (0.253) | 6273 | 17 |
| 12 | 0.400* (0.217) | −0.186 (0.257) | 6256 | 17 |


### Table B26. d_macro_controls — dl_rice

Robustness check, d macro controls

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.026 (0.023) | 0.067** (0.032) | 6443 | 17 |
| 1 | 0.087*** (0.027) | 0.137** (0.065) | 6443 | 17 |
| 2 | 0.099** (0.040) | 0.138* (0.078) | 6426 | 17 |
| 3 | 0.153*** (0.049) | 0.160 (0.102) | 6409 | 17 |
| 4 | 0.184*** (0.052) | 0.240* (0.127) | 6392 | 17 |
| 5 | 0.167*** (0.045) | 0.321** (0.138) | 6375 | 17 |
| 6 | 0.163*** (0.039) | 0.277** (0.137) | 6358 | 17 |
| 7 | 0.180*** (0.039) | 0.243* (0.136) | 6341 | 17 |
| 8 | 0.198*** (0.044) | 0.234* (0.137) | 6324 | 17 |
| 9 | 0.203*** (0.043) | 0.199 (0.139) | 6307 | 17 |
| 10 | 0.215*** (0.047) | 0.143 (0.145) | 6290 | 17 |
| 11 | 0.244*** (0.048) | 0.087 (0.151) | 6273 | 17 |
| 12 | 0.249*** (0.050) | 0.064 (0.155) | 6256 | 17 |


### Table B27. d_macro_controls_postparam — dl_rice

Robustness check, d macro controls postparam

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.092*** (0.022) | −0.067** (0.032) | 6443 | 17 |
| 1 | 0.224*** (0.056) | −0.137** (0.065) | 6443 | 17 |
| 2 | 0.237*** (0.062) | −0.138* (0.078) | 6426 | 17 |
| 3 | 0.313*** (0.079) | −0.160 (0.102) | 6409 | 17 |
| 4 | 0.423*** (0.106) | −0.240* (0.127) | 6392 | 17 |
| 5 | 0.488*** (0.118) | −0.321** (0.138) | 6375 | 17 |
| 6 | 0.440*** (0.119) | −0.277** (0.137) | 6358 | 17 |
| 7 | 0.423*** (0.121) | −0.243* (0.136) | 6341 | 17 |
| 8 | 0.432*** (0.121) | −0.234* (0.137) | 6324 | 17 |
| 9 | 0.401*** (0.124) | −0.199 (0.139) | 6307 | 17 |
| 10 | 0.358*** (0.133) | −0.143 (0.145) | 6290 | 17 |
| 11 | 0.330** (0.136) | −0.087 (0.151) | 6273 | 17 |
| 12 | 0.313** (0.137) | −0.064 (0.155) | 6256 | 17 |


### Table B28. e_p6 — dl_rice

Robustness check, e p6

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.039* (0.022) | 0.026 (0.037) | 6477 | 17 |
| 1 | 0.101*** (0.031) | 0.074 (0.093) | 6460 | 17 |
| 2 | 0.104** (0.049) | 0.085 (0.106) | 6443 | 17 |
| 3 | 0.151** (0.061) | 0.137 (0.131) | 6426 | 17 |
| 4 | 0.165** (0.069) | 0.259* (0.156) | 6409 | 17 |
| 5 | 0.160** (0.064) | 0.331** (0.161) | 6392 | 17 |
| 6 | 0.153*** (0.051) | 0.310* (0.162) | 6375 | 17 |
| 7 | 0.159*** (0.050) | 0.316* (0.167) | 6358 | 17 |
| 8 | 0.177*** (0.047) | 0.335* (0.174) | 6341 | 17 |
| 9 | 0.169*** (0.049) | 0.323* (0.180) | 6324 | 17 |
| 10 | 0.178*** (0.058) | 0.258 (0.207) | 6307 | 17 |
| 11 | 0.195*** (0.063) | 0.208 (0.215) | 6290 | 17 |
| 12 | 0.206*** (0.070) | 0.191 (0.218) | 6273 | 17 |


### Table B29. e_p6_postparam — dl_rice

Robustness check, e p6 postparam

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.065** (0.029) | −0.026 (0.037) | 6477 | 17 |
| 1 | 0.175** (0.085) | −0.074 (0.093) | 6460 | 17 |
| 2 | 0.189** (0.085) | −0.085 (0.106) | 6443 | 17 |
| 3 | 0.288*** (0.103) | −0.137 (0.131) | 6426 | 17 |
| 4 | 0.424*** (0.127) | −0.259* (0.156) | 6409 | 17 |
| 5 | 0.491*** (0.135) | −0.331** (0.161) | 6392 | 17 |
| 6 | 0.463*** (0.141) | −0.310* (0.162) | 6375 | 17 |
| 7 | 0.476*** (0.146) | −0.316* (0.167) | 6358 | 17 |
| 8 | 0.512*** (0.153) | −0.335* (0.174) | 6341 | 17 |
| 9 | 0.492*** (0.158) | −0.323* (0.180) | 6324 | 17 |
| 10 | 0.436** (0.182) | −0.258 (0.207) | 6307 | 17 |
| 11 | 0.403** (0.188) | −0.208 (0.215) | 6290 | 17 |
| 12 | 0.397** (0.188) | −0.191 (0.218) | 6273 | 17 |


### Table B30. e_p18 — dl_rice

Robustness check, e p18

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.036 (0.025) | 0.022 (0.039) | 6358 | 17 |
| 1 | 0.093** (0.037) | 0.070 (0.098) | 6341 | 17 |
| 2 | 0.090 (0.058) | 0.085 (0.111) | 6324 | 17 |
| 3 | 0.132* (0.071) | 0.123 (0.132) | 6307 | 17 |
| 4 | 0.148* (0.081) | 0.229 (0.156) | 6290 | 17 |
| 5 | 0.138* (0.078) | 0.301* (0.165) | 6273 | 17 |
| 6 | 0.121* (0.065) | 0.284* (0.168) | 6256 | 17 |
| 7 | 0.113* (0.060) | 0.298* (0.174) | 6239 | 17 |
| 8 | 0.121** (0.054) | 0.329* (0.180) | 6222 | 17 |
| 9 | 0.123** (0.059) | 0.310* (0.182) | 6205 | 17 |
| 10 | 0.131* (0.072) | 0.260 (0.207) | 6188 | 17 |
| 11 | 0.153* (0.080) | 0.223 (0.217) | 6171 | 17 |
| 12 | 0.160* (0.086) | 0.226 (0.219) | 6154 | 17 |


### Table B31. e_p18_postparam — dl_rice

Robustness check, e p18 postparam

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.058** (0.029) | −0.022 (0.039) | 6358 | 17 |
| 1 | 0.162* (0.089) | −0.070 (0.098) | 6341 | 17 |
| 2 | 0.175** (0.089) | −0.085 (0.111) | 6324 | 17 |
| 3 | 0.255** (0.103) | −0.123 (0.132) | 6307 | 17 |
| 4 | 0.377*** (0.124) | −0.229 (0.156) | 6290 | 17 |
| 5 | 0.440*** (0.135) | −0.301* (0.165) | 6273 | 17 |
| 6 | 0.406*** (0.143) | −0.284* (0.168) | 6256 | 17 |
| 7 | 0.411*** (0.151) | −0.298* (0.174) | 6239 | 17 |
| 8 | 0.450*** (0.161) | −0.329* (0.180) | 6222 | 17 |
| 9 | 0.434*** (0.160) | −0.310* (0.182) | 6205 | 17 |
| 10 | 0.391** (0.182) | −0.260 (0.207) | 6188 | 17 |
| 11 | 0.376** (0.188) | −0.223 (0.217) | 6171 | 17 |
| 12 | 0.386** (0.187) | −0.226 (0.219) | 6154 | 17 |


### Table B32. f_no_2008crisis — dl_rice

Robustness check, f no 2008crisis

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.007 (0.017) | 0.052 (0.034) | 6205 | 17 |
| 1 | 0.044* (0.025) | 0.127 (0.091) | 6188 | 17 |
| 2 | 0.024 (0.037) | 0.164 (0.101) | 6171 | 17 |
| 3 | 0.060 (0.045) | 0.227** (0.115) | 6154 | 17 |
| 4 | 0.063 (0.048) | 0.350*** (0.135) | 6137 | 17 |
| 5 | 0.072 (0.049) | 0.413*** (0.142) | 6120 | 17 |
| 6 | 0.105* (0.057) | 0.365** (0.152) | 6103 | 17 |
| 7 | 0.124* (0.070) | 0.359** (0.164) | 6086 | 17 |
| 8 | 0.155** (0.073) | 0.366** (0.176) | 6069 | 17 |
| 9 | 0.146* (0.076) | 0.349* (0.182) | 6052 | 17 |
| 10 | 0.137* (0.083) | 0.309 (0.203) | 6035 | 17 |
| 11 | 0.142* (0.083) | 0.280 (0.205) | 6018 | 17 |
| 12 | 0.129 (0.084) | 0.286 (0.203) | 6001 | 17 |


### Table B33. f_no_2008crisis_postparam — dl_rice

Robustness check, f no 2008crisis postparam

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.059** (0.027) | −0.052 (0.034) | 6205 | 17 |
| 1 | 0.172** (0.084) | −0.127 (0.091) | 6188 | 17 |
| 2 | 0.188** (0.084) | −0.164 (0.101) | 6171 | 17 |
| 3 | 0.287*** (0.099) | −0.227** (0.115) | 6154 | 17 |
| 4 | 0.413*** (0.121) | −0.350*** (0.135) | 6137 | 17 |
| 5 | 0.484*** (0.126) | −0.413*** (0.142) | 6120 | 17 |
| 6 | 0.471*** (0.136) | −0.365** (0.152) | 6103 | 17 |
| 7 | 0.483*** (0.142) | −0.359** (0.164) | 6086 | 17 |
| 8 | 0.521*** (0.151) | −0.366** (0.176) | 6069 | 17 |
| 9 | 0.495*** (0.153) | −0.349* (0.182) | 6052 | 17 |
| 10 | 0.446** (0.173) | −0.309 (0.203) | 6035 | 17 |
| 11 | 0.422** (0.173) | −0.280 (0.205) | 6018 | 17 |
| 12 | 0.415** (0.169) | −0.286 (0.203) | 6001 | 17 |


### Table B34. g_no_2020 — dl_rice

Robustness check, g no 2020

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.037 (0.023) | 0.038 (0.043) | 6256 | 17 |
| 1 | 0.100*** (0.033) | 0.105 (0.111) | 6239 | 17 |
| 2 | 0.102** (0.050) | 0.114 (0.124) | 6222 | 17 |
| 3 | 0.156** (0.061) | 0.174 (0.150) | 6205 | 17 |
| 4 | 0.174** (0.068) | 0.312* (0.176) | 6188 | 17 |
| 5 | 0.166*** (0.063) | 0.403** (0.181) | 6171 | 17 |
| 6 | 0.161*** (0.049) | 0.388** (0.184) | 6154 | 17 |
| 7 | 0.163*** (0.049) | 0.390** (0.189) | 6137 | 17 |
| 8 | 0.175*** (0.044) | 0.420** (0.191) | 6120 | 17 |
| 9 | 0.169*** (0.048) | 0.399** (0.195) | 6103 | 17 |
| 10 | 0.178*** (0.058) | 0.358 (0.228) | 6086 | 17 |
| 11 | 0.193*** (0.064) | 0.323 (0.232) | 6069 | 17 |
| 12 | 0.197*** (0.070) | 0.332 (0.222) | 6052 | 17 |


### Table B35. g_no_2020_postparam — dl_rice

Robustness check, g no 2020 postparam

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.075** (0.034) | −0.038 (0.043) | 6256 | 17 |
| 1 | 0.205** (0.104) | −0.105 (0.111) | 6239 | 17 |
| 2 | 0.215** (0.105) | −0.114 (0.124) | 6222 | 17 |
| 3 | 0.330*** (0.128) | −0.174 (0.150) | 6205 | 17 |
| 4 | 0.486*** (0.152) | −0.312* (0.176) | 6188 | 17 |
| 5 | 0.569*** (0.157) | −0.403** (0.181) | 6171 | 17 |
| 6 | 0.549*** (0.165) | −0.388** (0.184) | 6154 | 17 |
| 7 | 0.553*** (0.169) | −0.390** (0.189) | 6137 | 17 |
| 8 | 0.595*** (0.171) | −0.420** (0.191) | 6120 | 17 |
| 9 | 0.568*** (0.174) | −0.399** (0.195) | 6103 | 17 |
| 10 | 0.536*** (0.202) | −0.358 (0.228) | 6086 | 17 |
| 11 | 0.516** (0.202) | −0.323 (0.232) | 6069 | 17 |
| 12 | 0.530*** (0.188) | −0.332 (0.222) | 6052 | 17 |


### Table B36. h_end_2024m6 — dl_rice

Robustness check, h end 2024m6

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.034 (0.024) | 0.029 (0.040) | 6001 | 17 |
| 1 | 0.096*** (0.034) | 0.098 (0.111) | 6001 | 17 |
| 2 | 0.105** (0.051) | 0.073 (0.108) | 6001 | 17 |
| 3 | 0.161*** (0.062) | 0.070 (0.123) | 6001 | 17 |
| 4 | 0.178** (0.070) | 0.114 (0.154) | 6001 | 17 |
| 5 | 0.184*** (0.063) | 0.146 (0.174) | 6001 | 17 |
| 6 | 0.175*** (0.050) | 0.126 (0.177) | 6001 | 17 |
| 7 | 0.173*** (0.050) | 0.162 (0.190) | 6001 | 17 |
| 8 | 0.186*** (0.043) | 0.222 (0.197) | 6001 | 17 |
| 9 | 0.175*** (0.046) | 0.197 (0.193) | 6001 | 17 |
| 10 | 0.185*** (0.056) | 0.188 (0.194) | 6001 | 17 |
| 11 | 0.196*** (0.062) | 0.185 (0.191) | 6001 | 17 |
| 12 | 0.199*** (0.068) | 0.196 (0.189) | 6001 | 17 |


### Table B37. h_end_2024m6_postparam — dl_rice

Robustness check, h end 2024m6 postparam

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.063** (0.030) | −0.029 (0.040) | 6001 | 17 |
| 1 | 0.194* (0.104) | −0.098 (0.111) | 6001 | 17 |
| 2 | 0.178** (0.087) | −0.073 (0.108) | 6001 | 17 |
| 3 | 0.231** (0.099) | −0.070 (0.123) | 6001 | 17 |
| 4 | 0.292** (0.130) | −0.114 (0.154) | 6001 | 17 |
| 5 | 0.330** (0.154) | −0.146 (0.174) | 6001 | 17 |
| 6 | 0.301* (0.160) | −0.126 (0.177) | 6001 | 17 |
| 7 | 0.335* (0.174) | −0.162 (0.190) | 6001 | 17 |
| 8 | 0.408** (0.183) | −0.222 (0.197) | 6001 | 17 |
| 9 | 0.372** (0.177) | −0.197 (0.193) | 6001 | 17 |
| 10 | 0.372** (0.178) | −0.188 (0.194) | 6001 | 17 |
| 11 | 0.381** (0.174) | −0.185 (0.191) | 6001 | 17 |
| 12 | 0.395** (0.169) | −0.196 (0.189) | 6001 | 17 |


### Table B38. i_symmetric_2012 — dl_rice

Robustness check, i symmetric 2012

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | −0.003 (0.036) | 0.052 (0.046) | 2975 | 17 |
| 1 | 0.014 (0.060) | 0.141 (0.113) | 2958 | 17 |
| 2 | −0.023 (0.079) | 0.199 (0.132) | 2941 | 17 |
| 3 | −0.034 (0.095) | 0.300** (0.149) | 2924 | 17 |
| 4 | −0.045 (0.104) | 0.441*** (0.169) | 2907 | 17 |
| 5 | −0.033 (0.123) | 0.500*** (0.186) | 2890 | 17 |
| 6 | 0.027 (0.139) | 0.444** (0.200) | 2873 | 17 |
| 7 | 0.038 (0.148) | 0.424** (0.199) | 2856 | 17 |
| 8 | 0.044 (0.158) | 0.450** (0.207) | 2839 | 17 |
| 9 | 0.020 (0.172) | 0.429* (0.219) | 2822 | 17 |
| 10 | −0.002 (0.184) | 0.443* (0.240) | 2805 | 17 |
| 11 | −0.023 (0.191) | 0.438* (0.250) | 2788 | 17 |
| 12 | −0.011 (0.187) | 0.398* (0.240) | 2771 | 17 |


### Table B39. i_symmetric_2012_postparam — dl_rice

Robustness check, i symmetric 2012 postparam

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.049* (0.027) | −0.052 (0.046) | 2975 | 17 |
| 1 | 0.155* (0.085) | −0.141 (0.113) | 2958 | 17 |
| 2 | 0.176** (0.083) | −0.199 (0.132) | 2941 | 17 |
| 3 | 0.266*** (0.098) | −0.300** (0.149) | 2924 | 17 |
| 4 | 0.396*** (0.115) | −0.441*** (0.169) | 2907 | 17 |
| 5 | 0.467*** (0.120) | −0.500*** (0.186) | 2890 | 17 |
| 6 | 0.471*** (0.130) | −0.444** (0.200) | 2873 | 17 |
| 7 | 0.462*** (0.130) | −0.424** (0.199) | 2856 | 17 |
| 8 | 0.493*** (0.133) | −0.450** (0.207) | 2839 | 17 |
| 9 | 0.450*** (0.126) | −0.429* (0.219) | 2822 | 17 |
| 10 | 0.441*** (0.138) | −0.443* (0.240) | 2805 | 17 |
| 11 | 0.415*** (0.137) | −0.438* (0.250) | 2788 | 17 |
| 12 | 0.387*** (0.131) | −0.398* (0.240) | 2771 | 17 |


### Table B40. j_asymmetry — dl_rice

Robustness check, j asymmetry

| h | shock | shock_x_post | shock_x_fpos | N | Units |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.017 (0.032) | 0.036 (0.034) | 0.050 (0.041) | 6460 | 17 |
| 1 | 0.057 (0.055) | 0.095 (0.087) | 0.099 (0.068) | 6443 | 17 |
| 2 | −0.003 (0.073) | 0.115 (0.097) | 0.204** (0.090) | 6426 | 17 |
| 3 | −0.015 (0.090) | 0.172 (0.118) | 0.309*** (0.115) | 6409 | 17 |
| 4 | −0.036 (0.107) | 0.286** (0.141) | 0.357** (0.140) | 6392 | 17 |
| 5 | −0.077 (0.117) | 0.360** (0.148) | 0.390*** (0.151) | 6375 | 17 |
| 6 | −0.034 (0.129) | 0.333** (0.154) | 0.309* (0.160) | 6358 | 17 |
| 7 | −0.016 (0.140) | 0.337** (0.157) | 0.289* (0.173) | 6341 | 17 |
| 8 | −0.011 (0.148) | 0.357** (0.162) | 0.284 (0.182) | 6324 | 17 |
| 9 | 0.040 (0.160) | 0.332** (0.166) | 0.218 (0.199) | 6307 | 17 |
| 10 | 0.085 (0.172) | 0.280 (0.190) | 0.190 (0.213) | 6290 | 17 |
| 11 | 0.090 (0.177) | 0.242 (0.196) | 0.222 (0.223) | 6273 | 17 |
| 12 | 0.059 (0.183) | 0.239 (0.195) | 0.267 (0.237) | 6256 | 17 |


### Table B41. k_drop_newgeo — dl_rice

Robustness check, k drop newgeo

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.036 (0.023) | 0.033 (0.036) | 6424 | 17 |
| 1 | 0.098*** (0.033) | 0.096 (0.089) | 6411 | 17 |
| 2 | 0.102** (0.050) | 0.113 (0.101) | 6398 | 17 |
| 3 | 0.154** (0.062) | 0.162 (0.126) | 6385 | 17 |
| 4 | 0.170** (0.070) | 0.268* (0.154) | 6372 | 17 |
| 5 | 0.165** (0.064) | 0.332** (0.163) | 6359 | 17 |
| 6 | 0.158*** (0.050) | 0.310* (0.162) | 6346 | 17 |
| 7 | 0.161*** (0.050) | 0.315* (0.164) | 6333 | 17 |
| 8 | 0.174*** (0.045) | 0.335** (0.168) | 6320 | 17 |
| 9 | 0.168*** (0.049) | 0.310* (0.173) | 6307 | 17 |
| 10 | 0.178*** (0.059) | 0.250 (0.198) | 6290 | 17 |
| 11 | 0.196*** (0.066) | 0.206 (0.207) | 6273 | 17 |
| 12 | 0.201*** (0.072) | 0.199 (0.210) | 6256 | 17 |


### Table B42. k_drop_newgeo_postparam — dl_rice

Robustness check, k drop newgeo postparam

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.069*** (0.026) | −0.033 (0.036) | 6424 | 17 |
| 1 | 0.194** (0.080) | −0.096 (0.089) | 6411 | 17 |
| 2 | 0.215*** (0.080) | −0.113 (0.101) | 6398 | 17 |
| 3 | 0.316*** (0.099) | −0.162 (0.126) | 6385 | 17 |
| 4 | 0.439*** (0.127) | −0.268* (0.154) | 6372 | 17 |
| 5 | 0.496*** (0.137) | −0.332** (0.163) | 6359 | 17 |
| 6 | 0.468*** (0.141) | −0.310* (0.162) | 6346 | 17 |
| 7 | 0.476*** (0.143) | −0.315* (0.164) | 6333 | 17 |
| 8 | 0.508*** (0.149) | −0.335** (0.168) | 6320 | 17 |
| 9 | 0.478*** (0.151) | −0.310* (0.173) | 6307 | 17 |
| 10 | 0.428** (0.174) | −0.250 (0.198) | 6290 | 17 |
| 11 | 0.402** (0.179) | −0.206 (0.207) | 6273 | 17 |
| 12 | 0.400** (0.178) | −0.199 (0.210) | 6256 | 17 |


### Table B43. m_separate_pre — dl_rice

Robustness check, m separate pre

| h | shock | N | Units |
| :--- | ---: | ---: | ---: |
| 0 | 0.041* (0.023) | 4913 | 17 |
| 1 | 0.094*** (0.034) | 4913 | 17 |
| 2 | 0.106** (0.050) | 4913 | 17 |
| 3 | 0.162*** (0.061) | 4913 | 17 |
| 4 | 0.181*** (0.067) | 4913 | 17 |
| 5 | 0.187*** (0.059) | 4913 | 17 |
| 6 | 0.183*** (0.047) | 4913 | 17 |
| 7 | 0.182*** (0.047) | 4913 | 17 |
| 8 | 0.193*** (0.040) | 4913 | 17 |
| 9 | 0.187*** (0.042) | 4913 | 17 |
| 10 | 0.192*** (0.053) | 4913 | 17 |
| 11 | 0.200*** (0.059) | 4913 | 17 |
| 12 | 0.206*** (0.065) | 4913 | 17 |


### Table B44. m_separate_post — dl_rice

Robustness check, m separate post

| h | shock | N | Units |
| :--- | ---: | ---: | ---: |
| 0 | 0.040 (0.026) | 1547 | 17 |
| 1 | 0.155** (0.074) | 1530 | 17 |
| 2 | 0.177** (0.072) | 1513 | 17 |
| 3 | 0.255*** (0.091) | 1496 | 17 |
| 4 | 0.394*** (0.108) | 1479 | 17 |
| 5 | 0.440*** (0.110) | 1462 | 17 |
| 6 | 0.436*** (0.124) | 1445 | 17 |
| 7 | 0.395*** (0.127) | 1428 | 17 |
| 8 | 0.424*** (0.129) | 1411 | 17 |
| 9 | 0.340** (0.136) | 1394 | 17 |
| 10 | 0.372*** (0.109) | 1377 | 17 |
| 11 | 0.346*** (0.084) | 1360 | 17 |
| 12 | 0.288*** (0.081) | 1343 | 17 |


### Table B45. n_placebo_2016m3 — dl_rice

Robustness check, n placebo 2016m3

| h | shock | shock_x_placebo | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.043* (0.024) | −0.022 (0.042) | 4913 | 17 |
| 1 | 0.100*** (0.035) | −0.066 (0.063) | 4913 | 17 |
| 2 | 0.118** (0.050) | −0.123 (0.109) | 4913 | 17 |
| 3 | 0.178*** (0.061) | −0.174 (0.140) | 4913 | 17 |
| 4 | 0.193*** (0.068) | −0.125 (0.115) | 4913 | 17 |
| 5 | 0.190*** (0.061) | −0.007 (0.093) | 4913 | 17 |
| 6 | 0.179*** (0.047) | 0.071 (0.095) | 4913 | 17 |
| 7 | 0.178*** (0.047) | 0.073 (0.107) | 4913 | 17 |
| 8 | 0.189*** (0.038) | 0.098 (0.133) | 4913 | 17 |
| 9 | 0.178*** (0.039) | 0.150 (0.144) | 4913 | 17 |
| 10 | 0.184*** (0.051) | 0.161 (0.138) | 4913 | 17 |
| 11 | 0.194*** (0.057) | 0.152 (0.137) | 4913 | 17 |
| 12 | 0.201*** (0.062) | 0.126 (0.139) | 4913 | 17 |


### Table B46. o_cluster_region — dl_rice

Robustness check, o cluster region

| h | shock | shock_x_post | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.036*** (0.007) | 0.030** (0.014) | 6460 | 17 |
| 1 | 0.099*** (0.009) | 0.083*** (0.024) | 6443 | 17 |
| 2 | 0.103*** (0.012) | 0.096*** (0.024) | 6426 | 17 |
| 3 | 0.154*** (0.011) | 0.143*** (0.027) | 6409 | 17 |
| 4 | 0.171*** (0.010) | 0.253*** (0.034) | 6392 | 17 |
| 5 | 0.164*** (0.010) | 0.323*** (0.038) | 6375 | 17 |
| 6 | 0.157*** (0.009) | 0.303*** (0.032) | 6358 | 17 |
| 7 | 0.161*** (0.009) | 0.310*** (0.031) | 6341 | 17 |
| 8 | 0.173*** (0.010) | 0.331*** (0.031) | 6324 | 17 |
| 9 | 0.168*** (0.011) | 0.310*** (0.029) | 6307 | 17 |
| 10 | 0.178*** (0.010) | 0.250*** (0.026) | 6290 | 17 |
| 11 | 0.196*** (0.010) | 0.206*** (0.028) | 6273 | 17 |
| 12 | 0.201*** (0.012) | 0.199*** (0.030) | 6256 | 17 |


### Table B47. o_cluster_region_postparam — dl_rice

Robustness check, o cluster region postparam

| h | shock | shock_x_pre | N | Units |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.066*** (0.010) | −0.030** (0.014) | 6460 | 17 |
| 1 | 0.181*** (0.021) | −0.083*** (0.024) | 6443 | 17 |
| 2 | 0.199*** (0.024) | −0.096*** (0.024) | 6426 | 17 |
| 3 | 0.298*** (0.027) | −0.143*** (0.027) | 6409 | 17 |
| 4 | 0.424*** (0.032) | −0.253*** (0.034) | 6392 | 17 |
| 5 | 0.487*** (0.032) | −0.323*** (0.038) | 6375 | 17 |
| 6 | 0.460*** (0.026) | −0.303*** (0.032) | 6358 | 17 |
| 7 | 0.471*** (0.026) | −0.310*** (0.031) | 6341 | 17 |
| 8 | 0.504*** (0.026) | −0.331*** (0.031) | 6324 | 17 |
| 9 | 0.478*** (0.023) | −0.310*** (0.029) | 6307 | 17 |
| 10 | 0.428*** (0.022) | −0.250*** (0.026) | 6290 | 17 |
| 11 | 0.402*** (0.022) | −0.206*** (0.028) | 6273 | 17 |
| 12 | 0.400*** (0.023) | −0.199*** (0.030) | 6256 | 17 |


### Table B-LOO. Robustness (l): change θ leaving one region out


| Region left out | θ, h = 6 | θ, h = 12 |
| :--- | ---: | ---: |
| BARMM | 0.308 (0.160) | 0.210 (0.211) |
| Bicol Region | 0.292 (0.158) | 0.188 (0.208) |
| CALABARZON | 0.313 (0.164) | 0.206 (0.212) |
| CAR | 0.307 (0.163) | 0.199 (0.212) |
| Cagayan Valley | 0.299 (0.159) | 0.194 (0.209) |
| Caraga Region | 0.294 (0.161) | 0.193 (0.207) |
| Central Luzon | 0.301 (0.159) | 0.199 (0.208) |
| Central Visayas | 0.308 (0.164) | 0.196 (0.213) |
| Davao Region | 0.296 (0.161) | 0.201 (0.207) |
| Eastern Visayas | 0.309 (0.160) | 0.213 (0.209) |
| Ilocos Region | 0.309 (0.160) | 0.199 (0.209) |
| MIMAROPA | 0.305 (0.166) | 0.190 (0.214) |
| NCR | 0.320 (0.165) | 0.212 (0.214) |
| Northern Mindanao | 0.298 (0.160) | 0.195 (0.206) |
| SOCCSKSARGEN | 0.286 (0.162) | 0.190 (0.208) |
| Western Visayas | 0.309 (0.166) | 0.209 (0.211) |
| Zamboanga Peninsula | 0.298 (0.160) | 0.199 (0.206) |



# Appendix G. Working paper

*Source file: `paper/working_paper.md`*




**Abstract.** In March 2019 the Philippines replaced its quantitative restrictions on
rice imports with a 35% tariff (Republic Act 11203, the Rice Tariffication Law). We ask
whether the law changed how much of a world rice price movement reaches Filipino
consumers and farmers. We first reproduce the data and the main impulse response of
Antonio et al. [-@antonio2025] exactly, then estimate local projections on a panel of
17 regions from 1995 to September 2026. Before the law, a 1% rise in the world rice
price in pesos raised regional rice consumer prices by 0.16 percentage
points within six months; after the law, by 0.46. The increase is
significant only at the 10% level and is fragile: it is smaller with data ending in
June 2024 and with macroeconomic controls at twelve months. Along the supply chain,
pass-through to farmgate palay, wholesale and retail prices was close to zero from
2011 to 2019 and between 0.53 and 0.74
afterwards, so farmers are now more exposed to world prices than consumers. World rice
shocks are regressive: the consumer price index (CPI) of the poorest 30% of households
responds 2.4 times as strongly as the all-income CPI. The 2024 tariff cut
from 35% to 15% did not reach consumers: rice prices fell by about what world prices
alone predicted, and the gap between domestic and world prices widened. The
2025 import suspension was followed by a 21.1% rise in the rice
CPI between November 2025 and April 2026.

**Keywords:** rice; tariffication; price transmission; local projections; inflation
inequality; Philippines. **JEL:** F13, Q17, Q18, E31.

## Chapter 1. Introduction

### 1.1 Background

Rice is the Philippine staple. In the 2018 consumer basket rice takes
8.9% of spending for the average household and 17.9% for the
poorest 30% (the PSA's official CPI weights). About two million farm households sell
palay, the unmilled grain. A change in the price of rice therefore moves the cost of
living of the poor, the income of farmers and headline inflation at the same time.

For decades the government kept imported rice out with *quantitative restrictions*
(QR): only the National Food Authority (NFA), or traders holding its permits, could
import, and only in the volumes the government allowed. Republic Act (RA) 11203, the
*Rice Tariffication Law* (RTL), approved on 14 February 2019 and in force from March
2019, replaced the quotas with a tariff: 35% on rice from countries of the Association
of Southeast Asian Nations (ASEAN), with any private importer free to bring in any
amount once the duty is paid. The tariff revenue funds the Rice Competitiveness
Enhancement Fund (RCEF) for farmers. The border kept changing afterwards. Executive
Order (EO) 62 cut the tariff to 15% from July 2024; EO 93 and EO 102 suspended imports
of regular- and well-milled rice from September to December 2025; and from January
2026 EO 105 ties the tariff (15–35%) to world prices. All policy facts are listed with
their sources in `paper/policy_context.md`.

### 1.2 Rationale

Each of these measures rests on a claim about *pass-through*, that is, about how much
of a change in the cost of imported rice reaches domestic prices. The law's promise
was that open imports would tie domestic prices to cheaper world prices. The 2024 tariff
cut assumed that a lower duty would lower retail prices. The 2025 suspension assumed
that keeping imports out would raise palay prices. Yet the evidence on pass-through
since 2019 is thin and mixed. Simulation studies predicted large falls in retail prices
[@balie2020; @briones2019]; time-series studies find weak long-run links between world
and domestic prices and strong market power downstream [@bathan2025; @trinidad2026].
The closest study to ours, Antonio et al. [-@antonio2025], shows that world rice prices
are the largest driver of regional rice inflation from 1994 to 2023, but it does not
ask whether the law changed that link.

### 1.3 Objectives

The **general objective** is to measure whether, and for whom, the RTL changed the
transmission of world rice prices to Philippine rice prices.

*Objective 1 (descriptive)* is to document how rice prices, their volatility, their gap
to world prices and their dispersion across regions behaved before and after the law,
and how much rice contributed to inflation for all households and for the poorest 30%.

*Objective 2 (estimation)* is to estimate pass-through and its change with the law. It
answers five research questions (RQs). **RQ1:** how much of a 1% change in the world
rice price, in pesos, reaches regional consumer rice prices within 6 and 12 months, and
did this change after March 2019? **RQ2:** did the law change pass-through to farmgate,
wholesale and retail prices differently? **RQ3:** did the gap between domestic and
world prices fall after the law, and again after the 2024 tariff cut? **RQ4:** did the
change differ between rice-deficit and rice-surplus regions, and between high- and
low-poverty regions? **RQ5:** do world rice shocks raise the CPI of the poorest 30%
more than the all-income CPI?

We test competing hypotheses. **H1a (integration):** pass-through rose, as the
trade-reform literature predicts when quotas become an ad valorem tariff
[@baffes2003; @mundlak1992]. **H1b (rigidity):** it did not rise, because of market
power and downward price rigidity in the domestic chain [@trinidad2026; @bathan2025].
**H2:** farmgate pass-through rose more than retail pass-through. **H3:** the gap fell,
but by less than the tariff change implies. **H4a:** the increase was larger in
rice-deficit regions; **H4b:** no difference. **H5:** world rice shocks are regressive.

*Objective 3 (policy)* is to use the estimates to assess the 2024 tariff cut, the 2025
import suspension and the 2026 price-indexed tariff, in pesos for a poverty-line family.

### 1.4 Significance

For the Department of Agriculture (DA), the National Economic and Development
Authority's successor, the Department of Economy, Planning and Development (DEPDev),
and the Tariff Commission, the study says how much a tariff change is likely to move
retail and farmgate prices, and how quickly. For the Bangko Sentral ng Pilipinas (BSP),
it measures how strongly world rice shocks feed into the CPI. For social protection,
it shows how much more these shocks hurt the poorest households.

### 1.5 Scope and limitations

The study uses monthly official data for 17 regions from 1994 to September 2026. It
measures *price* responses; it does not measure quantities, profits or welfare
directly. The law is a single national event, so the comparison is between periods,
not between treated and untreated places, and other things changed after 2019
(the pandemic, the 2023 world price spike, the 2024 tariff cut). We address this with
robustness checks, a placebo law date and an out-of-sample test, but the "after the
law" period mixes the law with everything that followed. Finally, the replication of
the reference paper passed on data and on the main response but failed on one
pre-registered criterion about region groups (Section 4.4); results by region group
are therefore labelled as not validated.

### 1.6 Definition of terms

**Log change and inflation.** We measure every change as 100 times the change in the
natural logarithm, which is close to the percentage change for small changes:
$\pi_t = 100\,[\ln P_t - \ln P_{t-1}]$. If the rice CPI goes from 100 to 101, $\pi_t
\approx 1.0$.

**World rice price shock.** $f_t = 100\,\Delta \ln(P^W_t E_t)$, where $P^W_t$ is the
World Bank's Thai 5% broken rice price in US dollars per tonne and $E_t$ is pesos per
dollar. If the dollar price rises 3% and the peso is unchanged, $f_t \approx 3$.

**Pass-through.** How many percentage points domestic prices rise for each 1% rise in
the world price. The cumulative pass-through after $h$ months is
$B_h = \sum_{j=0}^{h}\beta_j$. A value of $B_6 = 0.4$ means that a 10% world price
rise raises the domestic price by about 4% within six months.

**Change in pass-through.** $\theta_h = B^{\text{after}}_h - B^{\text{before}}_h$.

**Inflation gap.** $D_t = 100\,\ln(P^{A}_t/P^{B30}_t)$, where $A$ is the all-income CPI
and $B30$ the bottom-30% CPI; its monthly change is $\Delta D_t = \pi^{A}_t -
\pi^{B30}_t$. If $\Delta D$ is negative, prices rose faster for the poor: the shock is
*regressive*.

**Border gap.** $G_t = 100\,\ln(P^{\text{dom}}_t / (P^W_t E_t/1000))$, the domestic
price per kilogram relative to the world price per kilogram, both in pesos.

**Official statistics and our constructions.** The CPIs (all income and bottom 30%),
their weights, and the retail, wholesale and farmgate prices are the Philippine
Statistics Authority's (PSA). The shock, the gaps, the spliced series, the region
groups (taken from Antonio et al.) and all estimates are ours.

## Chapter 2. Review of Related Literature

### 2.1 How world prices reach domestic markets

The law of one price says that, with free trade, the domestic price of an imported good
equals the world price times the exchange rate, plus the tariff and transport costs.
Mundlak and Larson [-@mundlak1992] estimate that domestic agricultural prices move
almost one-for-one with world prices on average, while Baffes and Gardner
[-@baffes2003] show that transmission depends on policy: it is weak under quotas and
state trading and rises after reforms. A quota cuts the link, because the domestic price
is set by domestic supply and the quota, while the quota rent absorbs world price
changes. A tariff restores the link, scaled by the share of imported cost in the final
price. Dawe [-@dawe2008] and Dawe and Timmer [-@dawe2012] explain why Asian governments,
including the Philippines, long chose stable domestic rice prices over integration with
a thin and volatile world market.

### 2.2 Empirical pass-through and its timing

Studies of food price transmission to developing countries find partial and slow
transmission [@ceballos2017; @dawe2015]. Furceri et al. [-@furceri2016] use local
projections to show that global food price shocks raise domestic headline inflation
for several months, more in poorer countries. Kpodar and Liu [-@kpodar2022] use the same
method, with a correction for later shocks, to show that fuel price increases raise the
inflation of poor households more. Price responses along a chain are often asymmetric:
increases pass through faster than decreases [@meyer2004].

### 2.3 Rice tariffication in the Philippines

Before the law was passed, simulations predicted that removing quotas would lower
retail rice prices by 10–17% and farm prices by more [@balie2020; @briones2019], with
net gains for poor consumers and losses for many farmers [@balie2021; @briones2021].
Clarete [-@clarete2022] stresses that market structure decides whether the gains
reach consumers. After the law, Bathan et al. [-@bathan2025] find, with autoregressive
distributed lag models on 2012–2024 data, that farmgate prices drive wholesale and
retail prices asymmetrically and that the law had only short-run effects. Bathan
[-@bathan2026] finds similar vertical responses after tariffication. Trinidad, Ravago and
Balisacan [-@trinidad2026] find limited transmission from international to domestic
prices and argue that competition policy must accompany tariff cuts.

### 2.4 Regional evidence and the reference study

Valera, Balié and Magrini [-@valera2022] show that rice prices are a major source of
regional inflation. Antonio et al. [-@antonio2025] estimate a panel vector
autoregression (VAR) for 17 regions from 1994 to 2023: a world rice shock raises
regional rice inflation, peaks after one month and fades within about five months;
the effect is larger in rice-deficit regions. Their data are public, so we use their
paper as the reference to replicate.

### 2.5 Synthesis and gap

The literature agrees that world prices matter and that the domestic chain is not
perfectly competitive. It does not tell us whether the switch from quotas to tariffs
*changed* pass-through to consumers, farmers and the poor, and how the later policy
reversals (tariff cut, suspension, indexed tariff) fit that picture. That is the gap
this study fills.

### 2.6 Conceptual framework

Figure 1 summarises the framework. The world price and the exchange rate set the
import parity price, $(1+\tau)E_tP^W_t$. The border regime decides how much of a change
in that price reaches the wholesale, retail and farmgate markets: under a quota very
little, under a tariff more. Retail rice prices feed the CPI, with a weight twice as
large for the poor. Dashed arrows show the policy levers studied in Objective 3.

![Conceptual framework. Solid arrows show how a world price change travels to domestic prices; dashed boxes and arrows show the policy levers (border regime, import suspension, price cap, NFA stocks).](../output/figures/fig01_framework.png){width=95%}

The general theory gives the estimating equation. If importers price at import parity
plus a marketing margin $m$, $P^{\text{dom}} = (1+\tau)EP^W + m$, then a 1% change in
$EP^W$ changes the domestic price by
$\partial\ln P^{\text{dom}}/\partial\ln(EP^W) = (1+\tau)EP^W/P^{\text{dom}}$, the share
of the import cost in the final price. Under a binding quota this elasticity is close
to zero. The farmgate price is the milled price minus milling and marketing costs, so
in percentage terms it moves *more* than the retail price [@gardner1975], which is H2.
Finally, by cost-of-living index theory, group $g$'s inflation is
$\pi^g = \sum_k w^g_k\pi_k$, so the effect of a rice shock on the gap is roughly
$B^{\text{rice}}_h(w^{A}_{\text{rice}} - w^{B30}_{\text{rice}})$, which is negative because
the poor's rice weight is larger (H5). Deaton [-@deaton1989] and Ivanic and Martin
[-@ivanic2008] show that the welfare effect then depends on whether a household is a
net buyer or a net seller of rice.

## Chapter 3. Digression: the model and how to implement it

This chapter is a tutorial. Someone new to the method should be able to reproduce the
study from it.

### 3.1 The question an impulse response answers

We want the path of domestic rice prices in the months after a world price change,
holding everything else as it would otherwise have been. That path is an *impulse
response*: the response of $y$ at $t+h$ to a one-unit shock at $t$, for $h = 0, 1, 2,\dots$

### 3.2 The local projection idea

A VAR estimates one model of how all variables evolve together and then iterates it
forward to get the responses. A *local projection* [@jorda2005] skips the iteration: for
each horizon $h$ it runs a separate regression of the outcome $h$ months ahead on
today's shock. If the VAR is right both give the same answer [@plagborg2021]; if it is
wrong, the local projection is more robust, and its standard errors are simple
[@montielolea2021].

### 3.3 The specification term by term

For each $h = 0, \dots, 12$ we estimate by ordinary least squares

$$\sum_{j=0}^{h}\pi_{r,t+j} = \alpha_{r} + B_h f_t + \theta_h (f_t\times \text{post}_t) + \sum_{q=1}^{12}\gamma_q \pi_{r,t-q} + \sum_{q=1}^{12}\lambda_q f_{t-q} + \sum_{l=1}^{h-1}\rho_l f_{t+l} + \delta\, \text{post}_t + \kappa t + \varepsilon_{r,t+h}. \quad (1)$$

The left side is the *cumulative* rice inflation from $t$ to $t+h$ in region $r$, so
$B_h$ is directly the cumulative pass-through. $\alpha_r$ are *region fixed effects*:
they let each region have its own average inflation. The twelve past values of rice
inflation and of the shock account for earlier movements and for seasonal patterns,
such as the lean months before the harvest. The *Teulings–Zubanov leads*
$f_{t+1},\dots,f_{t+h-1}$ make sure $B_h$ is not confused with the effect of later
shocks [@teulings2014]. $\text{post}_t$ equals 1 from March 2019; $\theta_h$ is the change
in pass-through after the law, and $B_h + \theta_h$ is the post-law pass-through. The
trend $\kappa t$ absorbs slow drifts.

### 3.4 From monthly effects to the level

Because the left side is a running sum, $B_6 = 0.4$ means that a 1% world price rise
raises the *level* of the rice CPI by 0.4% after six months. The monthly effect at
horizon $h$ is $B_h - B_{h-1}$.

### 3.5 Standard errors

Standard errors measure how uncertain an estimate is. Because all regions face the same
world price in the same month, their errors are correlated across regions and over time.
*Driscoll–Kraay* standard errors [@driscoll1998] allow for correlation over time and
across regions; for single national series we use *Newey–West* standard errors
[@newey1987], which allow for correlation over time. Bands in the figures are 90%
intervals.

### 3.6 The panel and group differences

To ask whether a group $G$ of regions (for example rice-deficit regions) changed
differently, we add $f_t\times G_r$, $f_t\times\text{post}_t\times G_r$ and the
corresponding dummies. The coefficient on the triple product is the extra change in
group $G$.

### 3.7 Checking the implementation

Before any real estimate we checked the code in two ways. First, simulation tests
(`tests/test_lp.py`, `tests/test_pvar.py`) generate data with a known response and
confirm that the estimators recover it. Second, the replication gate (Section 4.4)
reproduces a published result on the same public data.

### 3.8 Step-by-step implementation

The whole study runs from one command, `./run_all.sh`. The steps are: download the raw
files unchanged (`scripts/01_download_*.py`); clean them into long tables
(`02_clean_*.py`); build the regional and national panels (`03_build_panel.py`); run
the replication gate (`04_replicate.py`); estimate (`05_estimate.py`); run the episode
analysis (`07_episode_2024.py`) and the descriptive statistics (`09_descriptive.py`);
draw the figures (`06_figures.py`); and render the documents (`08_paper.py`,
`10_analysis_report.py`, `11_master_document.py`). The core call is:

```python
from rtl.lp import local_projection
res = local_projection(panel, y="dl_rice", x="f", time="t", unit="region",
                       horizons=12, p=12, interact=("post",), exog=("post",),
                       cumulative=True, se="driscoll_kraay")
```

### 3.9 Common pitfalls

Do not mix outcomes in levels and shocks in changes. Do not drop the leads: without them
$B_h$ partly measures later shocks. Do not use standard errors clustered only by region
when the shock is common to all regions: robustness check (o) shows they are several
times too small. Do not read a single significant horizon as a result; decide in
advance which horizons count (here $h = 6$ and $h = 12$).

## Chapter 4. Methodology

### 4.1 Design

The design compares pass-through before and after a national policy change, within a
panel of regions, with the reference study replicated first and every specification
fixed in advance. The pre-registered plan, the decisions log (D1–D12) and the
replication gate are in `CLAUDE.md` and were committed to the repository before the
corresponding estimates were run.

### 4.2 Data

Table 1 lists the variables. All are official and public; each raw file is logged in
`data/raw/source_log.md` with its URL, date pulled, base year and coverage.

| Variable | Symbol | Source | Coverage | Use |
| :--- | :--- | :--- | :--- | :--- |
| Rice CPI, all income, by region (item 01.1.1.12, 2018 = 100) | $P^{R}_{rt}$ | PSA OpenSTAT | 1994M1–2026M9 | RQ1, RQ4, Objective 3 |
| All-items CPI, all income and bottom 30% | $P^{A}_t, P^{B30}_t$ | PSA OpenSTAT | 2000M1–2026M9 | RQ5 |
| CPI weights 2018 (all income; bottom 30%) | $w^g_k$ | PSA OpenSTAT | 2018 | RQ5, Objective 3 |
| Retail, wholesale prices of regular-milled rice; farmgate palay | $P^{\text{ret}}, P^{\text{whs}}, P^{\text{farm}}$ | PSA price surveys | 2010M1–2026M9 | RQ2, RQ3 |
| Thai 5% and Viet 5% rice; urea; Dubai crude | $P^W_t$ | World Bank Pink Sheet | 1990M1–2026M9 | Shock, robustness |
| Peso–dollar rate, monthly average | $E_t$ | BSP | 1990M1–2026M9 | Shock |
| Oceanic Niño Index | ONI | NOAA | 1990M1–2026M8 | Replication, robustness |

: Table 1. Variables and sources.

Three construction choices matter. *Geography:* we use PSA's old 17-region code, which
has the long history, and extend it to 2026 with the growth of the new code; four regions
whose boundaries changed (Western and Central Visayas, SOCCSKSARGEN, BARMM) are flagged
for those months (D5). *Splicing:* national retail prices join three PSA survey series
on growth rates; the 2012-based and 2018-based series agree closely (correlation of
monthly changes 0.99), the 1990-based series less so (D12). *Validation:* the rice CPI
and the separate retail price survey move together (correlation of monthly changes
0.98); the bottom-30% and all-income rice CPIs correlate at
0.995; the Thai and Vietnamese world prices correlate at only
0.43, which is why the Vietnamese price is a robustness check.

### 4.3 Methods by objective

*Objective 1* uses summary statistics by sub-period, annual inflation by income group,
the contribution of rice to headline inflation (rice weight times rice inflation),
episodes of world price spikes (at least three months with a 12-month rise of 15% or
more), cross-correlations between the shock and rice inflation, the dispersion of rice
prices across regions, and unit-root tests.

*Objective 2* uses equation (1) for RQ1 (panel, 1995–2026), the same equation on national
farmgate, wholesale and retail prices for RQ2 (2011–2026, Newey–West), an interrupted
time-series regression of the border gap $G_t$ on dummies for the law, the 15% tariff and
the suspension with month dummies for RQ3, triple interactions for RQ4, and national
local projections of the all-items CPIs and of $\Delta D_t$ for RQ5 (2001–2026). The
decisive horizons are $h = 6$ and $h = 12$; for RQ4 we use a Bonferroni correction
across the two group tests, so each is judged at 5%. The robustness menu has fifteen
checks, lettered (a) to (o), listed in Table 6.

*Objective 3* applies the post-law pass-through, estimated only on data that end in
June 2024, to the July 2024 tariff cut, which lowers the peso cost of imports by
$100\ln(1.15/1.35)$ = −16.0 log points. The predicted change in the rice CPI from
June 2024 to month $m$ is $\sum_t B_{m-t}(f_t + \tau_t)$; we compare it with the actual
change, by region, and convert the tariff part into pesos for a poverty-line family of
five, using the PSA's 2023 poverty threshold (PHP 13,873 a month) and the
bottom-30% rice weight. The 2025 suspension is analysed descriptively (exploratory).

### 4.4 Validation: the replication gate

We fixed the pass criteria before downloading any data (Table 2). The data replication
is exact: our regional rice CPI means and standard deviations for 1994M1–2023M3 equal
those in Antonio et al.'s Table 1 in all 17 regions (largest deviation
0.000), and their "fuel price" turns out to be CPI item 07.2.2, transport
fuels (the other candidate deviates by 6.3 points). Our panel VAR
replica reproduces their main response: a one-standard-deviation world price shock
raises rice inflation by 0.256 points after one month (95% band 0.215 to
0.303), the peak, and the response is gone by month six
(0.002). The gate **failed** on the third criterion: the peak response in
rice-deficit regions is 1.26 times that in surplus regions, below the
pre-registered range of 1.3 to 3.0, and the peak in high-poverty regions is not below
that in low-poverty regions. No coding error was found, and two lags give the same
ratio (1.27). An exploratory look shows that the paper's wording fits
the *impact* response better than the peak (impact ratio 1.69; low-
versus high-poverty impact 0.236 versus 0.102),
but we did not change the criterion. We proceeded with estimation (decision D11) because
the data and the core estimator are validated; region-group results (RQ4) are labelled
as not validated.


| Criterion | Target | Result | Pass |
| :--- | :--- | :--- | :--- |
| G1 rice CPI means within 0.5 of Table 1 | >= 15 of 17 | 17 of 17 (median \|dev\| 0.000) | yes |
| G1 rice CPI SDs within 0.5 of Table 1 | >= 15 of 17 | 17 of 17 (median \|dev\| 0.000) | yes |
| G1b fuel CPI means within 0.5 (better candidate) | >= 15 of 17 | cpi_fuel_tr: 17 of 17 (median \|dev\| 0.000; other cpi_fuel_hh: 6.338) | yes |
| G2(i) THAI->RPI 95% band above zero at h=1 | lo > 0 | irf 0.256 [0.215, 0.303] | yes |
| G2(ii) THAI->RPI peaks at h=1 or 2 | h in {1,2} | peak at h=1 (0.256) | yes |
| G2(iii) THAI->RPI below 25% of peak by h=6 | < 0.25 x peak | h=6: 0.002 (0.01 of peak) | yes |
| G2(iv) FPI->RPI positive at h=0 | > 0 | 0.143 [0.143, 0.143] | yes |
| G2(v) FPI->RPI below 25% of impact by h=3 | < 0.25 x h0 | h=3: -0.006 (-0.04 of impact) | yes |
| G3 peak ratio insufficient/sufficient | in [1.3, 3.0] | 1.26 (0.296 / 0.235) | **no** |
| G3 peak high poverty < low poverty | high < low | high 0.260 vs low 0.255 | **no** |


: Table 2. Replication gate against Antonio et al. (2024), pre-registered 14 October 2026.

![Replication. Left: regional means (circles) and standard deviations (squares) of the rice CPI, 1994M1–2023M3, in Antonio et al. (2024, Table 1) and in this study; the line is equality. Right: response of regional rice inflation (percentage points) to a one-standard-deviation world rice price shock in the panel VAR replica, with the 95% Monte Carlo band (grey).](../output/figures/fig12_validation.png){width=90%}

### 4.5 Software and reproducibility

Python 3 with pandas, statsmodels and linearmodels; figures in matplotlib; documents
rendered from templates with Jinja2 and pandoc. Raw files are kept unchanged; every
output and every number in this paper is regenerated by `./run_all.sh`.

### 4.6 Ethics

The study uses only published aggregate statistics; no human subjects are involved.

## Chapter 5. Results and Discussion

### 5.1 Objective 1: rice prices before and after the law

Figure 2 shows the rice CPI and the world rice price in pesos since 1995. Until 2008 the
two move together loosely; the 2008 world price spike passes into domestic prices with
a lag and a smaller amplitude. Between 2012 and 2018, under quotas, the domestic price
stays well above the world price and barely reacts to it. After 2019 the two move
together much more closely, including the 2023 spike and the 2025 fall, until the
domestic surge of early 2026 at a time of stable world prices.

![Rice consumer price index (PSA) and the world rice price (Thai 5%) in pesos, monthly, index 2018 average = 100, log scale. Dotted lines mark the Rice Tariffication Law (March 2019), the 15% tariff (July 2024) and the import suspension (September 2025).](../output/figures/fig02_long_run.png){width=95%}

Table 3 summarises rice inflation by period. Under quotas (2009 to February 2019)
monthly rice inflation was calm, with a standard deviation of 0.82
points. It rose to 1.52 under the 35% tariff and to
2.33 after July 2024: an open border imports world volatility. In the
law's first year (2019) the rice CPI fell by −10.1% (December to
December), and by −11.8% for the bottom 30%. In 2023, when world
prices spiked, it rose by 17.9%, contributing about
1.6 percentage points to headline inflation for all
households and 3.5 for the bottom 30% (Table 4).


| Period | Rice CPI, % a year | Rice CPI, SD monthly | World rice (PHP), % a year | World, SD monthly | Months |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1995M1-2007M9 | 4.6 | 1.36 | 6.8 | 4.76 | 153 |
| 2007M10-2008M12 (world crisis) | 16.1 | 3.31 | 42.7 | 15.24 | 15 |
| 2009M1-2019M2 (quotas) | 3.2 | 0.82 | −1.8 | 4.37 | 122 |
| 2019M3-2024M6 (35% tariff) | 3.3 | 1.52 | 10.4 | 5.09 | 64 |
| 2024M7-2026M9 (15% tariff, suspension, indexed tariff) | −0.4 | 2.33 | −9.2 | 6.29 | 27 |


: Table 3. Rice CPI inflation and world rice price changes by period (national; annualised means of monthly log changes, and standard deviations of monthly changes).


| Year | Rice, all | Rice, bottom 30% | Headline, all | Headline, bottom 30% | World rice (PHP) | Rice contribution, all | Rice contribution, bottom 30% |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2012 | 2.1 | nan | 2.8 | 2.8 | −11.1 | 0.18 | nan |
| 2013 | 8.1 | 6.8 | 3.7 | 4.5 | −14.0 | 0.71 | 1.22 |
| 2014 | 7.6 | 7.0 | 1.9 | 3.0 | −6.3 | 0.67 | 1.25 |
| 2015 | −2.6 | −2.4 | 0.7 | 0.8 | −8.6 | −0.23 | −0.42 |
| 2016 | 0.5 | 0.5 | 2.2 | 1.8 | 8.0 | 0.05 | 0.09 |
| 2017 | 1.1 | 0.6 | 2.9 | 2.6 | 9.6 | 0.10 | 0.11 |
| 2018 | 6.2 | 7.0 | 5.0 | 6.0 | 4.1 | 0.55 | 1.24 |
| 2019 | −10.1 | −11.8 | 2.3 | 1.3 | 2.8 | −0.90 | −2.10 |
| 2020 | 0.1 | −0.2 | 3.2 | 3.6 | 13.1 | 0.01 | −0.03 |
| 2021 | −0.1 | −0.2 | 3.0 | 3.3 | −21.8 | −0.01 | −0.04 |
| 2022 | 3.4 | 3.8 | 7.7 | 9.0 | 25.8 | 0.30 | 0.68 |
| 2023 | 17.9 | 19.4 | 3.9 | 4.8 | 32.0 | 1.59 | 3.46 |
| 2024 | 0.8 | 0.7 | 2.9 | 2.5 | −15.0 | 0.07 | 0.12 |
| 2025 | −13.1 | −15.1 | 1.8 | 1.1 | −21.1 | −1.17 | −2.69 |
| 2026 | 18.5 | 21.2 | 6.9 | 8.6 | 34.3 | 1.64 | 3.78 |


: Table 4. Annual inflation (December to December, log points) and the approximate contribution of rice to headline inflation (2018 rice weight × rice inflation). 2026 is September 2025 to September 2026.

Regional rice prices also converged. The coefficient of variation of retail
regular-milled rice prices across regions fell from 6.7% in 2015–2017 to
4.1% in 2021–2024, a sign of better-integrated regional markets, before
rising to 5.6% in 2026 (Figure 3). The border gap (Figure 4) fell from an
average of 46 log points under quotas (2010 to February 2019) to
35 under the 35% tariff, and rose again to
46 after the tariff cut. We identify
11 world price episodes since 1995 (Annex Table A1). Before the
law, world price shocks were followed by rice inflation with a correlation of at most
0.28; after the law, by up to 0.35 at a lag of
4 months. Rice CPI levels are not stationary (augmented Dickey–Fuller
p = 0.26); monthly changes are, which is why we model changes.

![Coefficient of variation (%) of the annual average retail price of regular-milled rice across the 17 regions. The dotted line marks the Rice Tariffication Law.](../output/figures/fig14_regional_dispersion.png){width=80%}

![Border gap: 100 × ln of the domestic price of regular-milled rice (wholesale, solid; retail, dashed) over the world price (Thai 5%) in pesos per kilogram, monthly 2010–2026.](../output/figures/fig03_border_gap.png){width=95%}

### 5.2 Objective 2: pass-through and the law

**RQ1: consumer rice prices.** Over the whole period, a 1% rise in the world price
raises regional rice CPIs by 0.23 percentage points within six months and
0.24 within twelve. Table 5 and Figure 5 split this by regime. Before
the law, pass-through at six months was 0.16 (0.05); after
it, 0.46 (0.14), about 2.9 times larger.
The change θ~6~ = 0.30 (0.16) is significant at the 10%
level only (p = 0.06); at twelve months it is 0.20
(0.21, p = 0.34), not significant. The national rice CPI
gives the same picture (0.16 before, 0.44 after).
So the evidence supports H1a at six months, weakly, and cannot reject H1b at twelve.


| Months (h) | Before the law | After the law | Change θ | Observations |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.04 (0.02) | 0.07** (0.03) | 0.03 (0.04) | 6460 |
| 3 | 0.15** (0.06) | 0.30*** (0.10) | 0.14 (0.13) | 6409 |
| 6 | 0.16*** (0.05) | 0.46*** (0.14) | 0.30* (0.16) | 6358 |
| 9 | 0.17*** (0.05) | 0.48*** (0.15) | 0.31* (0.17) | 6307 |
| 12 | 0.20*** (0.07) | 0.40** (0.18) | 0.20 (0.21) | 6256 |


: Table 5. Cumulative pass-through of a 1% world rice price change (pesos) to regional rice CPIs, percentage points; Driscoll–Kraay standard errors in parentheses; \*, \*\*, \*\*\* significant at 10%, 5%, 1%. 17 regions, 1995M1–2026M9.

![Cumulative response of regional rice CPIs to a 1% rise in the world rice price in pesos, before the law (solid, grey 90% band) and after it (dashed, dotted 90% band), percentage points.](../output/figures/fig04_rq1_passthrough.png){width=80%}

The robustness checks (Table 6, Figure 6) show where the result is solid and where it
is fragile. The change at six months ranges from 0.13 to 0.44 across
the checks and keeps its 90% band above zero in 12 of 15
checks with standard errors; at twelve months it ranges from 0.06 to
0.40 and its band excludes zero in 2. It
is larger without the 2007–08 crisis (0.37), without 2020
(0.39), and in a window of seven years on each side of the law
(0.44, significant at 5%, and 0.40 at
twelve months). It weakens with the Vietnamese price (0.33, imprecise)
and, importantly, with data ending in June 2024: then the change at six months is only
0.13 (0.18). With macroeconomic controls
the change at twelve months falls to 0.06. Leaving out any one
region changes $\theta_6$ only within 0.29 to 0.32. A placebo
law date in March 2016, within the quota period, gives 0.07
(0.10), not significant. Standard errors clustered only by region are
several times smaller and overstate precision, as Section 3.9 warned.


| Check | Change θ, h = 6 | Change θ, h = 12 |
| :--- | ---: | ---: |
| Baseline | 0.30* (0.16) | 0.20 (0.21) |
| (a) Real shock | 0.31* (0.17) | 0.21 (0.22) |
| (b) Viet 5% | 0.33 (0.22) | 0.29 (0.26) |
| (c) USD price + FX control | 0.25 (0.18) | 0.19 (0.26) |
| (d) Macro controls | 0.28** (0.14) | 0.06 (0.16) |
| (e) 6 lags | 0.31* (0.16) | 0.19 (0.22) |
| (e) 18 lags | 0.28* (0.17) | 0.23 (0.22) |
| (f) Without 2007–08 crisis | 0.37** (0.15) | 0.29 (0.20) |
| (g) Without 2020 | 0.39** (0.18) | 0.33 (0.22) |
| (h) Ending June 2024 | 0.13 (0.18) | 0.20 (0.19) |
| (i) 2012–2026 window | 0.44** (0.20) | 0.40* (0.24) |
| (j) Asymmetry | 0.33** (0.15) | 0.24 (0.20) |
| (k) Drop chained 2026 | 0.31* (0.16) | 0.20 (0.21) |
| (o) Clustered SE | 0.30*** (0.03) | 0.20*** (0.03) |
| (l) Leave one region out (range) | 0.29 to 0.32 | 0.19 to 0.21 |
| (m) Separate pre/post models | 0.25* (0.13) | 0.08 (0.10) |


: Table 6. Robustness of the change in pass-through after the law, θ, at 6 and 12 months (percentage points per 1%); standard errors in parentheses; for (l) the range across the 17 leave-one-out estimates.

![Change in cumulative pass-through after the law at 6 months (left) and 12 months (right) across the robustness checks: point estimates with 90% intervals; for (l) the range across leave-one-region-out estimates. The dashed line is the baseline.](../output/figures/fig08_robustness.png){width=95%}

**RQ2: along the chain.** The clearest result of the study is in Table 7 and Figure 7.
From 2011 to February 2019, pass-through to farmgate, wholesale and retail prices was
statistically zero at every stage. After the law, six-month pass-through is
0.74 for farmgate palay, 0.61 for
wholesale rice and 0.53 for retail rice; all changes are
significant at six months. At twelve months the changes are smaller and less precise.
Farmgate pass-through is the largest, which supports H2: as the framework predicts,
the price farmers receive now moves more, in percent, than the price consumers pay. The
regional farmgate panel gives a similar post-law value (0.77).
In this window the pre-law consumer pass-through is near zero rather than the
0.16 of the long sample, because the 1995–2008 years, when world and
domestic prices moved together, are excluded.


| Price | Before, h=6 | After, h=6 | Change, h=6 | Before, h=12 | After, h=12 | Change, h=12 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Farmgate palay | 0.00 (0.22) | 0.74*** (0.25) | 0.74** (0.35) | 0.03 (0.29) | 0.59*** (0.20) | 0.56 (0.39) |
| Wholesale RMR | −0.16 (0.19) | 0.61*** (0.16) | 0.77*** (0.26) | −0.11 (0.29) | 0.50*** (0.17) | 0.61 (0.39) |
| Retail RMR | −0.03 (0.13) | 0.53*** (0.13) | 0.56*** (0.19) | −0.04 (0.20) | 0.45*** (0.17) | 0.49* (0.29) |
| Rice CPI | −0.03 (0.11) | 0.45*** (0.12) | 0.48*** (0.17) | −0.05 (0.16) | 0.40*** (0.14) | 0.44* (0.24) |


: Table 7. Cumulative pass-through to national farmgate, wholesale and retail rice prices and the rice CPI, before and after the law, 2011M1–2026M9; Newey–West standard errors in parentheses.

![Cumulative response of national farmgate palay, wholesale and retail regular-milled rice prices to a 1% world rice price rise, before (solid) and after (dashed) the law, with 90% bands.](../output/figures/fig05_rq2_chain.png){width=100%}

**RQ3: the border gap.** Table 8 shows that the wholesale–world gap fell by
−11.2 log points after the law (p =
0.089), and rose by 10.6 after the
2024 tariff cut (p = 0.020). Holding the world price
constant (columns 2 and 4), the gap moves −0.8 points
for each 1% rise in the world price, so domestic prices absorb only a small part of
world movements in *levels*; the law dummy is then no longer negative, and the tariff
cut is associated with a gap 15.2 points wider. H3 is
rejected for the 2024 cut: lowering the duty by 20 points did not narrow the gap.


|  | Wholesale (1) | Wholesale (2) | Retail (1) | Retail (2) |
| :--- | ---: | ---: | ---: | ---: |
| Law in force (from Mar 2019) | −11.2* (6.6) | 5.5 (5.4) | −11.4 (7.2) | 7.4 (5.1) |
| 15% tariff (from Jul 2024) | 10.6** (4.5) | 15.2*** (4.5) | 9.4** (4.8) | 14.6*** (3.6) |
| Import suspension (Sep–Dec 2025) | 2.0 (4.3) | −13.8*** (4.2) | 2.3 (4.0) | −15.4*** (3.5) |
| World price (log × 100) |  | −0.83*** (0.18) |  | −0.93*** (0.17) |


: Table 8. Interrupted time-series regressions of the border gap (100 × ln domestic/world price), 2010M1–2026M9, with month dummies; Newey–West (12 lags) standard errors in parentheses. Columns (2) and (4) add the log world price.

**RQ4: regions (not validated).** Table 9 and Figure 8 show no significant difference at
the decisive twelve-month horizon: the extra change in rice-deficit regions is
−0.05 (0.07) and in high-poverty regions
0.06 (0.05). At six months the high-poverty term is
0.09 (p = 0.03), below the Bonferroni threshold, but
this horizon was not the decisive one. We cannot reject H4b. Because the reference
paper's group ordering did not replicate (Section 4.4), we put little weight on these
group results.


| Group | θ post×G, h=6 | p | θ post×G, h=12 | p |
| :--- | ---: | ---: | ---: | ---: |
| Rice-deficit regions | −0.06 (0.05) | 0.163 | −0.05 (0.07) | 0.479 |
| High-poverty regions | 0.09** (0.04) | 0.027 | 0.06 (0.05) | 0.295 |


: Table 9. Extra change in pass-through after the law in rice-deficit and high-poverty regions (θ on shock × post × group), percentage points per 1%; Driscoll–Kraay standard errors; Bonferroni threshold 5% for each test.

![Extra change in cumulative pass-through after the law in rice-deficit regions (solid, grey band) and high-poverty regions (dashed, dotted band), percentage points per 1%, 90% bands.](../output/figures/fig07_rq4_regions.png){width=80%}

**RQ5: the poor.** A 1% world rice price rise raises the all-items CPI of all households
by 0.045 percentage points within six months and that of the bottom 30% by
0.110, 2.4 times as much (Table 10, Figure 9). The inflation
gap falls by −0.060 (0.010): world rice shocks are regressive,
supporting H5. The difference in rice weights alone (17.9% against
8.9%) predicts a gap of −0.022, about 36% of
the estimate; the rest presumably comes from other foods whose prices follow rice, which
also weigh more for the poor. The law did not change the regressive pattern
(θ~6~ = 0.018, standard error 0.021).


| Outcome | h = 0 | h = 6 | h = 12 |
| :--- | ---: | ---: | ---: |
| All-items CPI, all income | 0.013*** (0.004) | 0.045*** (0.009) | 0.043*** (0.012) |
| All-items CPI, bottom 30% | 0.028*** (0.007) | 0.110*** (0.018) | 0.100*** (0.026) |
| Gap ΔD (all income − bottom 30%) | −0.014*** (0.004) | −0.060*** (0.010) | −0.052*** (0.016) |
| Rice CPI (national) | 0.056** (0.023) | 0.240*** (0.050) | 0.239*** (0.075) |


: Table 10. Cumulative response of national all-items CPIs, their gap and the national rice CPI to a 1% world rice price rise, percentage points, 2001M1–2026M9; Newey–West standard errors.

![Left: cumulative response of the all-items CPI for all income households (solid) and for the bottom 30% (dashed). Right: response of the inflation gap, all income minus bottom 30% (negative = regressive). Percentage points per 1% world rice price rise, 90% bands.](../output/figures/fig06_rq5_poor.png){width=95%}

### 5.3 Objective 3: what the estimates imply for policy

**The 2024 tariff cut.** Using only data up to June 2024, the post-law model predicts
that the rice CPI should have fallen by −21.3 log points between
June 2024 and June 2025: −15.0 from falling world prices and
−6.3 from the tariff cut. The actual fall was
−15.4, 103% of the world-price part alone
and 73% of the total (Figure 10). After six months the actual
fall (−3.7) was only 36% of the predicted
(−10.3). In other words, consumers received the fall in world
prices but not the tariff cut, the pattern Trinidad, Ravago and Balisacan
[-@trinidad2026] describe. In 2 of 17 regions the fall
exceeded the prediction (Annex Table A2); the largest fall was in
Cagayan Valley (−23.6) and the smallest in
CAR (−7.7) (Figure 11).

![Change in the national rice CPI since June 2024 (log points): actual (solid), predicted from world prices only (dashed), and predicted from world prices plus the July 2024 tariff cut (dotted). Predictions use post-law pass-through estimated on data ending June 2024.](../output/figures/fig09_episode_tariff_cut.png){width=80%}

![Change in regional rice CPIs from June 2024 to June 2025 (log points). The dashed line is the predicted change from world prices and the tariff cut.](../output/figures/fig11_regions_episode.png){width=80%}

In pesos: a poverty-line family of five (PHP 13,873 a month in 2023) spends
about PHP 2,479 a month on rice if its budget shares are those of the
bottom-30% CPI. A full pass-through of the tariff wedge would save it about PHP
367 a month; the model predicts PHP
151 after a year; the actual fall in the bottom-30% rice CPI,
mostly due to world prices, was worth about PHP 398.

**The 2025 import suspension (exploratory).** Farmgate palay prices fell
−8.9% in September 2025, the first month of the suspension and
the start of the main harvest, then rose. Between November 2025 and April 2026 the rice
CPI rose 21.1% while the world price in pesos rose
11.4%. From August 2025 to April 2026, world prices alone predict
a rise of 4.7% in retail and 7.6%
in farmgate prices; the actual rises were 24.2% and
31.1% (Figure 12). The suspension appears to have raised
farm prices, as intended, but with a delay and at a large cost to consumers that
outlasted the suspension itself. This reading is descriptive: imports resumed in January
2026 at a tariff that may have been 15% or 20% (`policy_context.md`, P12), and the model
was not designed for a closed border.

![Farmgate palay (left) and retail regular-milled rice (right): change since August 2025 (log points), actual (solid) and predicted from world prices (dashed). Grey shading marks the import suspension, September–December 2025.](../output/figures/fig10_episode_suspension.png){width=95%}

**The 2026 price-indexed tariff.** EO 105 raises the tariff by 5 points for every 5%
fall in world prices and lowers it for every 5% rise, within bounds of 15% and 35%.
Near a 20% tariff, a 5% world price rise lowers the duty factor by
$\ln(1.15/1.20) \approx -4.3\%$, so the rule offsets about 85% of a world price move in
the peso cost of imports while the tariff stays within its bounds. Combined with a
post-law pass-through of about 0.40 at twelve months, the rule would leave
only a small part of world price moves in consumer prices, but only between the bounds,
and only if tariff changes pass through, which the 2024 episode questions. Our data
cover only nine months of the rule, so we do not estimate it.

## Chapter 6. Summary, Conclusions and Recommendations

### 6.1 Summary

*Objective 1.* Since the law, domestic rice prices track world prices more closely,
regional prices have converged, and monthly rice inflation has become more volatile.
The domestic–world gap narrowed under the 35% tariff and widened again after 2024.

*Objective 2.* Pass-through to consumer rice prices roughly doubled to tripled after the
law at six months (0.16 to 0.46), but the change is significant
only at 10% and is fragile. Along the chain, pass-through went from about zero to
about 0.53–0.74, largest for farmers.
World rice shocks raise the poor's CPI 2.4 times as much as the average.

*Objective 3.* The 2024 tariff cut did not reach consumers within a year; the 2025
suspension was followed by a sharp rise in both farmgate and retail prices.

### 6.2 Conclusions

The law did open the border to world price movements, most clearly for farmers, and it
coincided with a large one-off fall in rice prices in 2019. But openness works in both
directions: the poor now feel world price spikes more, and later cuts in the tariff were
absorbed in the chain rather than passed on.

### 6.3 Recommendations

To the **Tariff Commission and DEPDev**: judge tariff changes by their pass-through. Our
estimates suggest that at most part of a tariff cut reaches retail prices within a year;
the indexed tariff of EO 105 should be evaluated after a full year of data. To the
**Philippine Competition Commission and the DA**: the widening gap after the 2024 cut
points to margins in importing, milling and wholesaling; monitor them. To the **DA and
the Department of Social Welfare and Development**: because world rice shocks raise the
poor's CPI 2.4 times as much as the average (RQ5), support during world
price spikes is best targeted at poor households; border measures change prices for all
buyers. To the **DA**: in the 2025–26 episode farm prices rose mostly after the suspension
ended (5.4% above August 2025 by December, 31.1%
by April 2026), while retail prices rose by 24.2% (E4, exploratory);
suspensions should be weighed against that consumer cost, and alternatives such as the
RCEF productivity programmes, which this study does not evaluate, deserve evaluation.

### 6.4 Further research

Household-level data from the Family Income and Expenditure Survey would show net
buyers and net sellers directly; import volumes and margins by stage would show where
the tariff cut was absorbed; and a longer post-2026 sample will allow the indexed tariff
to be evaluated.

## References





# Appendix H. Journal manuscript

*Source file: `paper/manuscript.md`*




**Abstract.** The Philippines replaced quantitative restrictions on rice imports with a
35% tariff in March 2019. Using monthly official data for 17 regions from 1995 to
September 2026 and local projections, we estimate how much of a world rice price change
reaches domestic prices before and after the reform. We first reproduce the data and the
main impulse response of Antonio et al. (2025) exactly; one pre-registered criterion on
region groups fails. Six-month pass-through to regional rice consumer prices rises from
0.16 to 0.46 percentage points per 1%, a change significant
only at the 10% level and sensitive to the sample end and to macroeconomic controls.
Along the supply chain, pass-through rises from about zero to 0.74
(farmgate), 0.61 (wholesale) and 0.53
(retail). World rice shocks raise the bottom-30% consumer price index 2.4
times as much as the all-income index. An out-of-sample test shows that the 2024 tariff
cut from 35% to 15% did not reach consumers within a year, and the domestic–world price
gap widened.

**Keywords:** rice; tariffication; price transmission; local projections; Philippines.
**JEL:** F13, Q17, Q18, E31.

## 1. Introduction

Rice takes 8.9% of the average Filipino household's consumer basket and
17.9% of the poorest 30% households' basket. For decades, quantitative
restrictions (QR) and a state importer insulated domestic prices from the world market.
Republic Act 11203, the Rice Tariffication Law (RTL), replaced them with a 35% tariff
from March 2019. Later measures moved the border back and forth: a 15% tariff from July
2024, an import suspension from September to December 2025, and a price-indexed tariff
from January 2026.

Each measure assumes something about pass-through, the share of a change in the cost
of imported rice that reaches domestic prices. The trade-reform literature predicts
that replacing quotas with tariffs raises pass-through [@baffes2003; @mundlak1992].
Studies of the Philippine chain since 2019 find weak links to world prices and market
power downstream [@bathan2025; @trinidad2026]. Antonio et al. [-@antonio2025] show that
world rice prices are the main driver of regional rice inflation, but do not test for a
change with the law.

We make three contributions. First, we replicate Antonio et al. on the same public
data, with pass criteria fixed in advance, and report one failure. Second, we estimate
the change in pass-through with the law for consumer, retail, wholesale and farmgate
prices, and for the consumer price index (CPI) of the poorest 30%. Third, we test the
2024 tariff cut out of sample.

## 2. Methods

**Data.** Philippine Statistics Authority (PSA) regional rice CPI (2018 = 100, item
01.1.1.12), all-income and bottom-30% CPIs and weights, and national retail, wholesale
and farmgate rice prices; World Bank Pink Sheet rice prices (Thai 5%); Bangko Sentral ng
Pilipinas (BSP) exchange rates. The shock is $f_t = 100\,\Delta\ln(P^W_tE_t)$, the world
price in pesos. The 17-region panel uses the PSA's old geographic code, extended to 2026
with new-code growth; the rice CPI and the separate retail price survey correlate at
0.98 in monthly changes.

**Specification.** For $h = 0,\dots,12$ we regress cumulative rice inflation
$\sum_{j\le h}\pi_{r,t+j}$ on $f_t$, $f_t\times\text{post}_t$ (post = 1 from March 2019),
twelve lags of $\pi$ and $f$, Teulings–Zubanov leads $f_{t+1},\dots,f_{t+h-1}$
[@teulings2014], a trend and region fixed effects [@jorda2005]. $B_h$ is cumulative
pass-through and $\theta_h$ its change. Panel standard errors are Driscoll–Kraay
[@driscoll1998]; national ones Newey–West. Decisive horizons, $h = 6$ and $h = 12$, and
a fifteen-item robustness menu were fixed before estimation.

**Validation.** Before downloading data we registered a replication gate (Table 1). Our
rice CPI statistics match Antonio et al.'s Table 1 exactly in all 17 regions; a panel VAR
replica reproduces their response to a world price shock (0.256 at one month,
fading by month six). The ratio of peak responses in rice-deficit to surplus regions is
1.26, below the registered range [1.3, 3.0], and the poverty ordering is
not reproduced. We proceed, with region-group results labelled as not validated.


| Criterion | Target | Result | Pass |
| :--- | :--- | :--- | :--- |
| G1 rice CPI means within 0.5 of Table 1 | >= 15 of 17 | 17 of 17 (median \|dev\| 0.000) | yes |
| G1 rice CPI SDs within 0.5 of Table 1 | >= 15 of 17 | 17 of 17 (median \|dev\| 0.000) | yes |
| G1b fuel CPI means within 0.5 (better candidate) | >= 15 of 17 | cpi_fuel_tr: 17 of 17 (median \|dev\| 0.000; other cpi_fuel_hh: 6.338) | yes |
| G2(i) THAI->RPI 95% band above zero at h=1 | lo > 0 | irf 0.256 [0.215, 0.303] | yes |
| G2(ii) THAI->RPI peaks at h=1 or 2 | h in {1,2} | peak at h=1 (0.256) | yes |
| G2(iii) THAI->RPI below 25% of peak by h=6 | < 0.25 x peak | h=6: 0.002 (0.01 of peak) | yes |
| G2(iv) FPI->RPI positive at h=0 | > 0 | 0.143 [0.143, 0.143] | yes |
| G2(v) FPI->RPI below 25% of impact by h=3 | < 0.25 x h0 | h=3: -0.006 (-0.04 of impact) | yes |
| G3 peak ratio insufficient/sufficient | in [1.3, 3.0] | 1.26 (0.296 / 0.235) | **no** |
| G3 peak high poverty < low poverty | high < low | high 0.260 vs low 0.255 | **no** |


: Table 1. Pre-registered replication gate against Antonio et al. (2024 working paper version).

**Border gap and episode.** The gap $G_t = 100\ln(P^{\text{dom}}_t/(E_tP^W_t/1000))$ is
regressed on dummies for the law, the 15% tariff and the suspension, with month dummies.
For the 2024 cut we apply post-law pass-through estimated on data ending June 2024 to
world shocks and to the tariff shock $100\ln(1.15/1.35)$ = −16.0.

## 3. Results

**Pass-through to consumers.** Table 2 reports cumulative pass-through to regional rice
CPIs. The change at six months, 0.30 (0.16), is significant at
10% (p = 0.06); at twelve months, 0.20 (0.21), it
is not.


| Months (h) | Before the law | After the law | Change θ | Observations |
| :--- | ---: | ---: | ---: | ---: |
| 0 | 0.04 (0.02) | 0.07** (0.03) | 0.03 (0.04) | 6460 |
| 3 | 0.15** (0.06) | 0.30*** (0.10) | 0.14 (0.13) | 6409 |
| 6 | 0.16*** (0.05) | 0.46*** (0.14) | 0.30* (0.16) | 6358 |
| 9 | 0.17*** (0.05) | 0.48*** (0.15) | 0.31* (0.17) | 6307 |
| 12 | 0.20*** (0.07) | 0.40** (0.18) | 0.20 (0.21) | 6256 |


: Table 2. Cumulative pass-through to regional rice CPIs (pp per 1%), 1995M1–2026M9; Driscoll–Kraay standard errors; \* p<0.10, \*\* p<0.05, \*\*\* p<0.01.

**Robustness.** Across checks the six-month change ranges from 0.13 to
0.44. It is larger in a symmetric 2012–2026 window (0.44)
and without the 2007–08 crisis (0.37), but only
0.13 (0.18) with data ending June 2024, and the
twelve-month change is 0.06 with macroeconomic controls. A
placebo law date in 2016 gives 0.07 (0.10). Full results
are in Table 3.


| Check | Change θ, h = 6 | Change θ, h = 12 |
| :--- | ---: | ---: |
| Baseline | 0.30* (0.16) | 0.20 (0.21) |
| (a) Real shock | 0.31* (0.17) | 0.21 (0.22) |
| (b) Viet 5% | 0.33 (0.22) | 0.29 (0.26) |
| (c) USD price + FX control | 0.25 (0.18) | 0.19 (0.26) |
| (d) Macro controls | 0.28** (0.14) | 0.06 (0.16) |
| (e) 6 lags | 0.31* (0.16) | 0.19 (0.22) |
| (e) 18 lags | 0.28* (0.17) | 0.23 (0.22) |
| (f) Without 2007–08 crisis | 0.37** (0.15) | 0.29 (0.20) |
| (g) Without 2020 | 0.39** (0.18) | 0.33 (0.22) |
| (h) Ending June 2024 | 0.13 (0.18) | 0.20 (0.19) |
| (i) 2012–2026 window | 0.44** (0.20) | 0.40* (0.24) |
| (j) Asymmetry | 0.33** (0.15) | 0.24 (0.20) |
| (k) Drop chained 2026 | 0.31* (0.16) | 0.20 (0.21) |
| (o) Clustered SE | 0.30*** (0.03) | 0.20*** (0.03) |
| (l) Leave one region out (range) | 0.29 to 0.32 | 0.19 to 0.21 |
| (m) Separate pre/post models | 0.25* (0.13) | 0.08 (0.10) |


: Table 3. Change in pass-through after the law, θ, across robustness checks.

**Along the chain.** From 2011 to February 2019 pass-through was statistically zero at
the farmgate, wholesale and retail levels; after the law it is large and significant at
six months (Table 4), and largest at the farmgate.


| Price | Before, h=6 | After, h=6 | Change, h=6 | Before, h=12 | After, h=12 | Change, h=12 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Farmgate palay | 0.00 (0.22) | 0.74*** (0.25) | 0.74** (0.35) | 0.03 (0.29) | 0.59*** (0.20) | 0.56 (0.39) |
| Wholesale RMR | −0.16 (0.19) | 0.61*** (0.16) | 0.77*** (0.26) | −0.11 (0.29) | 0.50*** (0.17) | 0.61 (0.39) |
| Retail RMR | −0.03 (0.13) | 0.53*** (0.13) | 0.56*** (0.19) | −0.04 (0.20) | 0.45*** (0.17) | 0.49* (0.29) |
| Rice CPI | −0.03 (0.11) | 0.45*** (0.12) | 0.48*** (0.17) | −0.05 (0.16) | 0.40*** (0.14) | 0.44* (0.24) |


: Table 4. Pass-through to national farmgate, wholesale and retail rice prices, 2011M1–2026M9; Newey–West standard errors.

**Regions (not validated).** The extra post-law change is −0.05
(0.07) in rice-deficit and 0.06 (0.05)
in high-poverty regions at twelve months, neither significant.

**The poor.** A 1% world price rise raises the all-items CPI by 0.045 pp for all
households and 0.110 pp for the bottom 30% within six months; the gap falls by
−0.060 (0.010). Rice weights explain about 36%
of the gap. The pattern did not change with the law.

**Border gap.** The wholesale gap fell −11.2 log points after the
law (p = 0.089) and rose 10.6 after
the 2024 tariff cut (p = 0.020); controlling for the world
price, the rise is 15.2 (Table 5).


|  | Wholesale (1) | Wholesale (2) | Retail (1) | Retail (2) |
| :--- | ---: | ---: | ---: | ---: |
| Law in force (from Mar 2019) | −11.2* (6.6) | 5.5 (5.4) | −11.4 (7.2) | 7.4 (5.1) |
| 15% tariff (from Jul 2024) | 10.6** (4.5) | 15.2*** (4.5) | 9.4** (4.8) | 14.6*** (3.6) |
| Import suspension (Sep–Dec 2025) | 2.0 (4.3) | −13.8*** (4.2) | 2.3 (4.0) | −15.4*** (3.5) |
| World price (log × 100) |  | −0.83*** (0.18) |  | −0.93*** (0.17) |


: Table 5. Border gap regressions, 2010M1–2026M9; Newey–West standard errors.

**The 2024 tariff cut.** The model predicted a fall of −21.3 log points
in the rice CPI from June 2024 to June 2025 (−15.0 from world prices,
−6.3 from the tariff). The actual fall, −15.4,
matches the world-price part alone. For a poverty-line family of five the forgone saving
is about PHP 151 a month on predicted pass-through, out of a
full tariff wedge of PHP 367.

**The 2025 suspension (exploratory).** Between November 2025 and April 2026 the rice CPI
rose 21.1% while the world price in pesos rose
11.4%.

## 4. Discussion

The law opened the border most visibly for farmers: farmgate prices now follow world
prices closely, which is the intended transmission of a tariff regime and the source of
farmers' complaints about low palay prices. For consumers the evidence of higher
pass-through is suggestive rather than conclusive, and later tariff cuts appear to have
been absorbed along the chain, consistent with Trinidad, Ravago and Balisacan
[-@trinidad2026]. World rice shocks remain regressive.

**Policy.** Tariff changes should be judged by measured pass-through, not by the size of
the tariff change; the chain's margins after the 2024 cut deserve scrutiny by competition
authorities; and support during world price spikes is best targeted at poor households.

**Limitations.** The law is a single national event, so "after the law" mixes the law with
the pandemic, the 2023 world price spike and the 2024 tariff cut. The replication failed
on region groups. The 2025–26 episode is descriptive. The policy calculations use 2018
basket weights and the 2023 poverty threshold.

**Conclusion.** Tariffication tied Philippine rice prices more closely to the world
market, especially at the farmgate, but tariff cuts after 2019 did not lower consumer
prices as intended.

## Declarations

**Funding:** [to be completed]. **Competing interests:** none declared. **Data and code
availability:** all data are public (PSA OpenSTAT, World Bank, BSP, NOAA); raw files,
code and a one-command rebuild are in the replication package. **Author contributions:**
[to be completed].

## References



## Figures

![Figure 1. Cumulative response of regional rice CPIs to a 1% world rice price rise (pesos), before the law (solid, grey 90% band) and after it (dashed, dotted 90% band), percentage points.](../output/figures/fig04_rq1_passthrough.png){width=80%}

![Figure 2. Cumulative response of national farmgate palay, wholesale and retail regular-milled rice prices to a 1% world rice price rise, before (solid) and after (dashed) the law, 90% bands.](../output/figures/fig05_rq2_chain.png){width=100%}

![Figure 3. Left: response of the all-items CPI for all income households (solid) and the bottom 30% (dashed). Right: response of the inflation gap, all income minus bottom 30%. Percentage points per 1%, 90% bands.](../output/figures/fig06_rq5_poor.png){width=95%}

![Figure 4. Change in the national rice CPI since June 2024 (log points): actual, predicted from world prices only, and predicted from world prices plus the July 2024 tariff cut, using post-law pass-through estimated on data ending June 2024.](../output/figures/fig09_episode_tariff_cut.png){width=80%}

![Figure 5. Change in cumulative pass-through after the law across robustness checks, at 6 and 12 months, with 90% intervals.](../output/figures/fig08_robustness.png){width=95%}



# Appendix I. Submission checklist

*Source file: `paper/SUBMISSION_CHECKLIST.md`*

## Submission checklist (manuscript)

Items that remain before the manuscript can be submitted.

- [ ] **Target journal and format.** None chosen yet. Candidates that fit the topic: *Food
      Policy*, *Journal of Agricultural Economics*, *Australian Journal of Agricultural and
      Resource Economics*, *Philippine Review of Economics*. Then apply the journal's
      template (word limit, reference style, title page, figure format).
- [ ] **Authors and declarations.** Replace `[Name 1]`–`[Name 3]`; complete funding and
      author contributions.
- [ ] **Tables and figures at the end.** The draft keeps tables in the text; move them
      after the references if the journal requires it.
- [ ] **Replication gate.** Disclose the failed criterion G3 (done in the text) and keep
      the region-group results labelled as not validated, or drop them.
- [ ] **Reference version.** Targets come from the MPRA working-paper version of Antonio
      et al. (2024); the published version (AJARE 2025, 69(2): 440–452) was not read.
      Check that its Table 1 and figures are unchanged.
- [ ] **References not on Crossref.** Bathan, Daloonpate and Mahathanseth (2025, J. ISSAAS)
      and the MPRA paper were verified from their PDFs. Clarete (2022): add the book
      editors.
- [ ] **Policy facts.** Confirm the Official Gazette publication date of RA 11203 and the
      applied rice tariff in 2026 (`policy_context.md`, open items).
- [ ] **Cover letter and data statement.** Not written yet. The data statement can say
      that all data are public and that `./run_all.sh --download` rebuilds everything.
- [ ] **Language check** against the house style of the chosen journal.



# Appendix J. All code

## `run_all.sh`

```bash
#!/usr/bin/env bash
# Rebuild the whole study from data/raw/. Add --download to refresh the raw files first.
set -euo pipefail
cd "$(dirname "$0")"
PY=${PYTHON:-.venv/bin/python}
[ -x "$PY" ] || PY=python3

if [[ "${1:-}" == "--download" ]]; then
  $PY scripts/01_download_psa.py
  $PY scripts/01_download_world.py
fi

$PY scripts/02_clean_world.py
$PY scripts/02_clean_psa.py
$PY scripts/03_build_panel.py
$PY scripts/04_replicate.py
$PY scripts/05_estimate.py
$PY scripts/07_episode_2024.py
$PY scripts/09_descriptive.py
$PY scripts/06_figures.py
$PY scripts/08_paper.py
$PY scripts/10_analysis_report.py
$PY -m pytest -q tests
$PY scripts/11_master_document.py
echo "run_all: done"

```

## `rtl/__init__.py`

```python

```

## `rtl/crossref_check.py`

```python
"""Check references against Crossref before citing them.

Usage:
  python crossref_check.py "Rice prices and income distribution in Thailand" "The economic effects of energy price shocks"
  python crossref_check.py --bib paper/references.bib     # checks every title in a .bib file

Prints the top matches (title, authors, journal, volume(issue), pages, year, DOI)
so you can compare them with the citation. Flag any reference with no match in
the .bib `note` field and in the submission checklist; never invent details.
"""

import re
import sys
import time
import urllib.parse

import requests


def lookup(q, rows=2):
    url = "https://api.crossref.org/works?rows=%d&query.bibliographic=%s" % (rows, urllib.parse.quote(q))
    r = requests.get(url, timeout=30, headers={"User-Agent": "reference-check (mailto:none@example.org)"})
    r.raise_for_status()
    for it in r.json()["message"]["items"]:
        authors = ", ".join(a.get("family", "?") for a in it.get("author", [])[:5])
        year = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
        print(f"  - {(it.get('title') or ['?'])[0]} | {authors} | {(it.get('container-title') or [''])[0]} "
              f"{it.get('volume', '')}({it.get('issue', '')}) {it.get('page', '')} | {year} | doi:{it.get('DOI')}")


def main(argv):
    if argv[:1] == ["--bib"]:
        titles = re.findall(r"^\s*title\s*=\s*[{\"](.+?)[}\"],?\s*$", open(argv[1]).read(), flags=re.M)
    else:
        titles = argv
    for t in titles:
        t = re.sub(r"[{}\\]", "", t)
        print(t)
        try:
            lookup(t)
        except Exception as e:  # noqa: BLE001
            print("  ! lookup failed:", e)
        time.sleep(1)


if __name__ == "__main__":
    main(sys.argv[1:])

```

## `rtl/fig_style.py`

```python
"""Black-and-white journal figure style.

No colour: series differ by line style and marker; bands are light grey fill
(series 1) or dotted bounds (series 2); serif font; no title inside the image
(captions belong in the document). save() writes 300-dpi PNG and TIFF and a
vector PDF without CreationDate, so reruns are byte-identical.

    from fig_style import setup, save, irf, A, B
    setup()
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    irf(ax, df_all, A, "All income"); irf(ax, df_b30, B, "Bottom 30%", band="lines")
    ax.set_ylabel("Percentage points"); ax.legend(); save(fig, "fig1_rq1", outdir)
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

BLACK, DARK, MID, LIGHT = "0.0", "0.25", "0.55", "0.85"
A = dict(color=BLACK, linestyle="-", marker="o", markersize=3.5, markerfacecolor=BLACK)     # series 1
B = dict(color=BLACK, linestyle="--", marker="s", markersize=3.5, markerfacecolor="white")  # series 2
C = dict(color=DARK, linestyle=":", marker="^", markersize=3.5, markerfacecolor="white")    # series 3


def setup():
    plt.rcParams.update({
        "font.family": "DejaVu Serif", "font.size": 9, "axes.edgecolor": BLACK, "axes.labelcolor": BLACK,
        "xtick.color": BLACK, "ytick.color": BLACK, "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": False, "legend.frameon": False, "figure.dpi": 100, "hatch.linewidth": 0.6,
        "lines.linewidth": 1.4,
    })


def save(fig, name, outdir):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    fig.savefig(outdir / f"{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(outdir / f"{name}.tiff", dpi=300, bbox_inches="tight", pil_kwargs={"compression": "tiff_lzw"})
    fig.savefig(outdir / f"{name}.pdf", bbox_inches="tight", metadata={"CreationDate": None})
    plt.close(fig)


def zero(ax, horizontal=True):
    (ax.axhline if horizontal else ax.axvline)(0, color=BLACK, linewidth=0.6)


def irf(ax, q, style, label=None, band="fill", H=12):
    """Plot an impulse response from a frame with columns h, beta, lo, hi."""
    if band == "fill":
        ax.fill_between(q.h, q.lo, q.hi, color=LIGHT, linewidth=0)
    elif band == "lines":
        for col in ("lo", "hi"):
            ax.plot(q.h, q[col], color=BLACK, linestyle=":", linewidth=0.8)
    ax.plot(q.h, q.beta, label=label, **style)
    zero(ax)
    ax.set_xticks(range(0, H + 1, 2))
    ax.set_xlabel("Months after the shock")

```

## `rtl/lp.py`

```python
"""Local projections with the Teulings-Zubanov correction (as in Kpodar and Liu 2022, eq. 1).

For each horizon h the outcome y_{t+h} is regressed on p lags of y and of the
shock x, the shock x_t, the Teulings-Zubanov leads x_{t+1}, ..., x_{t+h-1},
optional controls (contemporaneous plus p lags), a linear time trend and,
for panels, unit fixed effects. beta_h is the coefficient on x_t.

The lead set follows Annex Tables 1-2 of the reference paper: no lead at h = 0
or h = 1, leads 1..h-1 thereafter. Change the lead range in _design() if your
reference paper differs, and log it in the decisions log.

Copy into the project package (e.g. <pkg>/lp.py). Requires pandas, numpy,
statsmodels, linearmodels, scipy.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
from scipy import stats


def _design(df, y, x, unit, time, h, p, controls, interact, cumulative, tz, exog=()):
    g = df.groupby(unit, sort=False) if unit else None

    def shift(col, k):
        return g[col].shift(k) if g is not None else df[col].shift(k)

    out = pd.DataFrame(index=df.index)
    if cumulative:
        out["dep"] = sum(shift(y, -j) for j in range(h + 1))
    else:
        out["dep"] = shift(y, -h)
    out["shock"] = df[x]
    for name in interact:
        out[f"shock_x_{name}"] = df[x] * df[name]
    for q in range(1, p + 1):
        out[f"{y}_l{q}"] = shift(y, q)
        out[f"{x}_l{q}"] = shift(x, q)
    if tz:
        for lead in range(1, h):
            out[f"{x}_f{lead}"] = shift(x, -lead)
    for c in controls:
        out[c] = df[c]
        for q in range(1, p + 1):
            out[f"{c}_l{q}"] = shift(c, q)
    for c in exog:
        out[c] = df[c]
    out["trend"] = df[time]
    return out


def local_projection(
    df: pd.DataFrame,
    y: str,
    x: str,
    time: str,
    unit: str | None = None,
    horizons: int = 12,
    p: int = 12,
    controls: tuple[str, ...] = (),
    interact: tuple[str, ...] = (),
    exog: tuple[str, ...] = (),
    sample: pd.Series | None = None,
    cumulative: bool = False,
    tz: bool = True,
    trend: bool = True,
    se: str = "cluster",
    level: float = 0.90,
) -> pd.DataFrame:
    """Estimate beta_h for h = 0..horizons.

    df must be sorted by unit then time with consecutive months (gaps as NaN).
    `time` is an integer month counter used for the trend and panel index.
    controls enter with p lags; exog (e.g. dummies) enter contemporaneously only.
    sample: boolean mask on df rows; observations outside it are dropped after
    lags and leads are built, so pre-sample data still supply the lags.
    se: 'cluster' (by unit), 'robust', 'driscoll_kraay' (panels) or
    'newey_west' (single series, h + 1 lags).
    Returns one row per horizon and coefficient of interest ('shock' and each
    'shock_x_<name>').
    """
    z = stats.norm.ppf(0.5 + level / 2)
    rows = []
    for h in range(horizons + 1):
        d = _design(df, y, x, unit, time, h, p, list(controls), list(interact), cumulative, tz, list(exog))
        if sample is not None:
            d = d[sample.reindex(d.index).fillna(False).astype(bool)]
        if not trend:
            d = d.drop(columns="trend")
        if unit:
            d[unit] = df[unit]
        d = d.dropna()
        regs = [c for c in d.columns if c not in ("dep", unit)]
        regs = [c for c in regs if d[c].nunique() > 1]  # drop dummies with no variation in sample
        if unit:
            idx = pd.MultiIndex.from_arrays([d[unit], df.loc[d.index, time]])
            mod = PanelOLS(d["dep"].set_axis(idx), d[regs].set_axis(idx).assign(const=1.0),
                           entity_effects=True, drop_absorbed=True)
            kw = {"cluster": dict(cov_type="clustered", cluster_entity=True),
                  "robust": dict(cov_type="robust"),
                  "driscoll_kraay": dict(cov_type="kernel", kernel="bartlett", bandwidth=h + 1)}[se]
            res = mod.fit(**kw)
            params, ses, nobs, r2 = res.params, res.std_errors, res.nobs, res.rsquared_within
            n_units = d[unit].nunique()
        else:
            X = sm.add_constant(d[regs])
            if se == "newey_west":
                res = sm.OLS(d["dep"], X).fit(cov_type="HAC", cov_kwds={"maxlags": h + 1})
            else:
                res = sm.OLS(d["dep"], X).fit(cov_type="HC1")
            params, ses, nobs, r2 = res.params, res.bse, int(res.nobs), res.rsquared_adj
            n_units = 1
        for term in ["shock"] + [f"shock_x_{n}" for n in interact]:
            b, s = params[term], ses[term]
            rows.append(dict(h=h, term=term, beta=b, se=s, lo=b - z * s, hi=b + z * s,
                             nobs=nobs, n_units=n_units, r2=r2))
    return pd.DataFrame(rows)

```

## `rtl/numbers.py`

```python
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

```

## `rtl/pvar.py`

```python
"""Panel vector autoregression as in Love and Zicchino (2006) and Abrigo and Love (2016).

Fixed effects are removed with forward orthogonal deviations (the Helmert
transformation): each observation is replaced by its scaled deviation from the mean of
all *future* observations of the same unit, so the transformed error stays
uncorrelated with past values. The transformed lags are then instrumented with the
untransformed lags (just-identified GMM, which equals two-stage least squares).
Orthogonalized impulse responses use the Cholesky factor of the residual covariance,
in the order the variables are given; confidence bands come from Monte Carlo draws
of the coefficients from their estimated normal distribution.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _fod(a: np.ndarray) -> np.ndarray:
    """Forward orthogonal deviations of a (T, k) array; the last row is lost (NaN)."""
    T = a.shape[0]
    out = np.full_like(a, np.nan, dtype=float)
    csum = np.cumsum(a[::-1], axis=0)[::-1]  # csum[t] = sum_{s>=t} a[s]
    for t in range(T - 1):
        n_fut = T - t - 1
        fut_mean = csum[t + 1] / n_fut
        out[t] = np.sqrt(n_fut / (n_fut + 1)) * (a[t] - fut_mean)
    return out


def fit_pvar(df: pd.DataFrame, variables: list[str], unit: str, time: str, p: int = 1):
    """Estimate a PVAR(p). df: one row per unit-time, sorted, no gaps within units.

    Returns dict with A (list of p (K,K) matrices, A[q][i, j] = effect of var j at lag q+1
    on var i), Sigma (residual covariance), V (covariance of vec of the stacked
    coefficient matrix, rows = equations), n (observations used).
    """
    K = len(variables)
    Ys, Xs, Zs = [], [], []
    for _, g in df.sort_values([unit, time]).groupby(unit, sort=False):
        y = g[variables].to_numpy(float)
        T = len(y)
        if T <= p + 2:
            continue
        lags = np.hstack([y[p - q - 1:T - q - 1] for q in range(p)])  # rows t = p..T-1
        cur = y[p:]
        ok = ~np.isnan(cur).any(1) & ~np.isnan(lags).any(1)
        cur, lags = cur[ok], lags[ok]
        Ys.append(_fod(cur)[:-1])
        Xs.append(_fod(lags)[:-1])
        Zs.append(lags[:-1])
    Y, X, Z = np.vstack(Ys), np.vstack(Xs), np.vstack(Zs)
    ZX_inv = np.linalg.inv(Z.T @ X)
    B = ZX_inv @ (Z.T @ Y)  # (K*p, K): column k = equation k
    U = Y - X @ B
    n = Y.shape[0]
    Sigma = U.T @ U / (n - K * p)
    Q = ZX_inv @ (Z.T @ Z) @ ZX_inv.T  # (Kp, Kp)
    V = np.kron(Sigma, Q)  # covariance of vec(B) stacked by equation
    A = [B[q * K:(q + 1) * K].T for q in range(p)]
    return dict(A=A, B=B, Sigma=Sigma, V=V, n=n, variables=list(variables), p=p)


def _oirf(A, Sigma, H):
    K = Sigma.shape[0]
    p = len(A)
    P = np.linalg.cholesky(Sigma)
    # MA coefficients
    Phi = [np.eye(K)]
    for h in range(1, H + 1):
        Phi.append(sum(A[q] @ Phi[h - q - 1] for q in range(min(p, h))))
    return np.array([ph @ P for ph in Phi])  # (H+1, K, K): [h, response, shock]


def irf(res, H: int = 10, draws: int = 200, level: float = 0.95, seed: int = 0):
    """Orthogonalized IRFs with Monte Carlo bands. Returns long DataFrame."""
    K, p = len(res["variables"]), res["p"]
    point = _oirf(res["A"], res["Sigma"], H)
    rng = np.random.default_rng(seed)
    vecB = res["B"].T.reshape(-1)  # equation-major, matches kron(Sigma, Q)
    sims = []
    Lv = np.linalg.cholesky(res["V"] + 1e-14 * np.eye(len(vecB)))
    for _ in range(draws):
        b = (vecB + Lv @ rng.standard_normal(len(vecB))).reshape(K, K * p).T
        A = [b[q * K:(q + 1) * K].T for q in range(p)]
        sims.append(_oirf(A, res["Sigma"], H))
    sims = np.array(sims)
    lo = np.percentile(sims, 100 * (1 - level) / 2, axis=0)
    hi = np.percentile(sims, 100 * (1 + level) / 2, axis=0)
    rows = []
    names = res["variables"]
    for h in range(H + 1):
        for i, r in enumerate(names):
            for j, s in enumerate(names):
                rows.append(dict(h=h, response=r, shock=s, irf=point[h, i, j], lo=lo[h, i, j], hi=hi[h, i, j]))
    return pd.DataFrame(rows)

```

## `rtl/pxweb_download.py`

```python
r"""Download a PxWeb table (PSA OpenSTAT and other statistics offices) unchanged to a gzipped CSV.

Pulls every value of every variable, one geography at a time to stay under the
PxWeb cell limit, retries with exponential backoff, and decodes Latin-1 when
UTF-8 fails. The API's CSV responses are stacked but otherwise unchanged, so the
file is a faithful raw download. Log it in data/raw/source_log.md afterwards.

Usage:
  python pxweb_download.py <api_base> <table_path> <out.csv.gz> [--geo-regex REGEX] [--force]

Example (PSA, bottom-30% CPI, 2018=100):
  python pxweb_download.py https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/2M/PI/ \
      BIH/2018NEW/0022M4ABIR1.px data/raw/psa/cpi_b30_2018new_2018_2026.csv.gz \
      --geo-regex '^(PHILIPPINES|\.\.[^.].*)$'

--geo-regex keeps only geography labels that match (e.g. country and regions,
not provinces). Check the number of geographies printed against what you expect.
--select CODE=REGEX (repeatable) keeps only the values of variable CODE whose label
matches REGEX (e.g. the rice item of a 354-item CPI table), to stay under the cell
limit. Values themselves are never altered; log the selection in source_log.md.
"""

import argparse
import io
import re
import time
from pathlib import Path

import pandas as pd
import requests

GEO_CODES = ("Geolocation", "Area", "Region", "Geography")


def post(url, query):
    for attempt in range(5):
        try:
            r = requests.post(url, json=query, timeout=(15, 90))
            r.raise_for_status()
            try:
                return r.content.decode("utf-8-sig")
            except UnicodeDecodeError:
                return r.content.decode("latin-1")
        except requests.RequestException as e:
            print(f"[retry {attempt + 1}: {type(e).__name__}]", end="", flush=True)
            if attempt == 4:
                raise
            time.sleep(2 ** (attempt + 1))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("api_base")
    ap.add_argument("table")
    ap.add_argument("out")
    ap.add_argument("--geo-regex", default=None)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--select", action="append", default=[], help="CODE=REGEX on value labels")
    a = ap.parse_args(argv)
    out = Path(a.out)
    if out.exists() and not a.force:
        print("exists:", out)
        return
    url = a.api_base.rstrip("/") + "/" + a.table
    meta = requests.get(url, timeout=60).json()
    geo = next((v for v in meta["variables"] if v["code"] in GEO_CODES), None)
    sel_rx = dict(x.split("=", 1) for x in a.select)
    rest = []
    for v in meta["variables"]:
        if v is geo:
            continue
        if v["code"] in sel_rx:
            rx_v = re.compile(sel_rx[v["code"]])
            vals = [c for c, t in zip(v["values"], v["valueTexts"]) if rx_v.search(t)]
            if not vals:
                raise SystemExit(f"--select {v['code']} matched nothing")
            rest.append({"code": v["code"], "selection": {"filter": "item", "values": vals}})
        else:
            rest.append({"code": v["code"], "selection": {"filter": "all", "values": ["*"]}})
    if geo is None:
        codes = [None]
    else:
        rx = re.compile(a.geo_regex, re.I) if a.geo_regex else None
        codes = [c for c, t in zip(geo["values"], geo["valueTexts"]) if rx is None or rx.match(t)]
    parts = []
    for code in codes:
        sel = list(rest)
        if code is not None:
            sel.insert(0, {"code": geo["code"], "selection": {"filter": "item", "values": [code]}})
        text = post(url, {"query": sel, "response": {"format": "csv"}})
        parts.append(pd.read_csv(io.StringIO(text), dtype=str, keep_default_na=False))
        print(".", end="", flush=True)
        time.sleep(0.5)
    df = pd.concat(parts, ignore_index=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"wrote {out}: {len(codes)} geographies, {df.shape[0]} rows x {df.shape[1]} cols")


if __name__ == "__main__":
    main()

```

## `rtl/regions.py`

```python
"""Map PSA geography labels (they differ across tables) to one canonical region name.

Canonical names follow Antonio et al. (2024), Table 1. 'Philippines' is the national
aggregate; 'NIR' (Negros Island Region, new geographic code only) and 'AONCR' (areas
outside NCR) are kept but are not units of the regional panel.
"""

import re

REGIONS = ["NCR", "CAR", "Ilocos Region", "Cagayan Valley", "Central Luzon", "CALABARZON", "MIMAROPA",
           "Bicol Region", "Western Visayas", "Central Visayas", "Eastern Visayas", "Zamboanga Peninsula",
           "Northern Mindanao", "Davao Region", "SOCCSKSARGEN", "Caraga Region", "BARMM"]

# Ordered patterns; the first that matches wins. Matching is case-insensitive on the
# label with leading dots and spaces removed.
_PATTERNS = [
    (r"^philippines$", "Philippines"),
    (r"^(areas outside|aoncr)", "AONCR"),
    (r"negros island|^nir$", "NIR"),
    (r"national capital|^ncr$|^ncr ", "NCR"),
    (r"cordillera|^car$|^car ", "CAR"),
    (r"bangsamoro|autonomous region|armm|^barmm$", "BARMM"),
    (r"mimaropa|region iv-?b", "MIMAROPA"),
    (r"calabarzon|region iv-?a\b|region 4a", "CALABARZON"),
    (r"caraga|region xiii|region 13", "Caraga Region"),
    (r"soccsksargen|region xii\b|region 12|^reg12", "SOCCSKSARGEN"),
    (r"davao region|region xi\b|region 11", "Davao Region"),
    (r"northern mindanao|region x\b|region 10", "Northern Mindanao"),
    (r"zamboanga peninsula|region ix\b|region 9", "Zamboanga Peninsula"),
    (r"eastern visayas|region viii\b|region 8", "Eastern Visayas"),
    (r"central visayas|region vii\b|region 7", "Central Visayas"),
    (r"western visayas|region vi\b|region 6", "Western Visayas"),
    (r"bicol|region v\b|region 5", "Bicol Region"),
    (r"central luzon|region iii\b|region 3", "Central Luzon"),
    (r"cagayan valley|region ii\b|region 2", "Cagayan Valley"),
    (r"ilocos region|region i\b|region 1", "Ilocos Region"),
]


def canon(label: str) -> str | None:
    if str(label).startswith("...."):  # provinces and cities are indented four dots in PxWeb
        return None
    s = re.sub(r"^[.\s]+", "", str(label)).strip().lower()
    for pat, name in _PATTERNS:
        if re.search(pat, s):
            return name
    return None

```

## `rtl/render_doc.py`

```python
r"""Render a Jinja2 markdown template with the numbers dictionary, then convert to .docx with pandoc.

Numbers come from output/tables/paper_numbers.json (written by the paper script),
so no estimate is ever typed by hand. Jinja comment delimiters are changed to
<#-- --#> because pandoc uses {#refs} for the reference list.

Usage:
  python render_doc.py <template.md> <out.md> [--numbers output/tables/paper_numbers.json]
                       [--bib paper/references.bib] [--toc] [--resource-path dir1:dir2]

In templates: {{ n.rq1_h12 }} for a number; put `::: {#refs}` / `:::` where the
reference list goes; escape a literal @ as \@; leave blank lines around tables.
"""

import argparse
import json
from pathlib import Path

import jinja2
import pypandoc


def render(template, out, numbers=None, bib=None, toc=False, resource_path=None, tables=None):
    template, out = Path(template), Path(out)
    n = json.loads(Path(numbers).read_text()) if numbers else {}
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template.parent), undefined=jinja2.StrictUndefined,
                             keep_trailing_newline=True, comment_start_string="<#--", comment_end_string="--#>")
    text = env.get_template(template.name).render(n=n, t=tables or {})
    out.write_text(text)
    args = []
    if bib:
        args += ["--citeproc", f"--bibliography={bib}", "--metadata=link-citations:true"]
    if toc:
        args += ["--toc", "--toc-depth=2"]
    args.append(f"--resource-path={resource_path or out.parent}")
    pypandoc.convert_file(str(out), "docx", outputfile=str(out.with_suffix(".docx")), extra_args=args)
    print("wrote", out, "and", out.with_suffix(".docx"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("template")
    ap.add_argument("out")
    ap.add_argument("--numbers")
    ap.add_argument("--bib")
    ap.add_argument("--toc", action="store_true")
    ap.add_argument("--resource-path")
    a = ap.parse_args()
    render(a.template, a.out, a.numbers, a.bib, a.toc, a.resource_path)

```

## `scripts/01_download_psa.py`

```python
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

```

## `scripts/01_download_world.py`

```python
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

```

## `scripts/02_clean_psa.py`

```python
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

```

## `scripts/02_clean_world.py`

```python
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

```

## `scripts/03_build_panel.py`

```python
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

```

## `scripts/04_replicate.py`

```python
"""Replication gate (pre-registered in CLAUDE.md, 14 Oct 2026) against Antonio et al. (2024).

G1  regional mean and SD of the rice CPI level, 1994M1-2023M3, vs Table 1 (+-0.5, >=15/17)
G1b the same for the two fuel candidates; the closer one becomes FPI (D2)
G2  PVAR(1) replica: shape of the RPI response to THAI and FPI shocks
G3  ordering: rice-insufficient vs sufficient regions; high vs low poverty
Indicative: panel local projection of rice inflation on the real THAI shock.

Writes output/tables/replication_gate.csv, replication_table1.csv, replication_pvar_irf.csv,
replication_lp_indicative.csv and output/tables/replication_choice.json (the fuel item).
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rtl.lp import local_projection  # noqa: E402
from rtl.pvar import fit_pvar, irf  # noqa: E402

T = ROOT / "output/tables"
START, END = pd.Period("1994-01", "M"), pd.Period("2023-03", "M")
TOL, NEED = 0.5, 15


def table1_check(reg, targets):
    s = reg[(reg.month >= START) & (reg.month <= END)]
    rows = []
    for var, prefix in [("cpi_rice", "rice_cpi_level"), ("cpi_fuel_hh", "fuel_cpi_level"),
                        ("cpi_fuel_tr", "fuel_cpi_level")]:
        stats = s.groupby("region")[var].agg(["mean", "std", "count"])
        for _, t in targets[targets.outcome.str.startswith(prefix)].iterrows():
            r = t.outcome.split("|")[1]
            rows.append(dict(variable=var, region=r, target_mean=t.beta, est_mean=stats.loc[r, "mean"],
                             target_sd=t.se, est_sd=stats.loc[r, "std"], n_months=int(stats.loc[r, "count"])))
    d = pd.DataFrame(rows)
    d["dev_mean"] = d.est_mean - d.target_mean
    d["dev_sd"] = d.est_sd - d.target_sd
    return d


def pvar_data(reg, fuel):
    d = reg[(reg.month >= START) & (reg.month <= END)].copy()
    d["RPI"] = d.dl_rice
    d["FPI"] = d["dl_" + fuel.replace("cpi_", "")]
    d["THAI"] = d.groupby("region").thai5_php.transform(lambda s: 100 * np.log(s).diff()) \
        - d.groupby("region").cpi_all_nat.transform(lambda s: 100 * np.log(s).diff())
    d["UREA"] = d.dl_urea_real
    d["ENSO"] = d.oni
    return d.dropna(subset=["RPI", "FPI", "THAI", "UREA", "ENSO"])


ORDER = ["ENSO", "FPI", "UREA", "THAI", "RPI"]


def shape(q, shock):
    r = q[(q.response == "RPI") & (q.shock == shock)].set_index("h")
    return r


def main():
    reg = pd.read_parquet(ROOT / "data/processed/panel_region.parquet")
    targets = pd.read_csv(ROOT / "replication/antonio2024_targets.csv")
    gate = []

    # ---- G1 / G1b
    t1 = table1_check(reg, targets)
    t1.to_csv(T / "replication_table1.csv", index=False, float_format="%.3f")
    rice = t1[t1.variable == "cpi_rice"]
    n_mean = int((rice.dev_mean.abs() <= TOL).sum())
    n_sd = int((rice.dev_sd.abs() <= TOL).sum())
    gate.append(dict(criterion="G1 rice CPI means within 0.5 of Table 1", target=f">= {NEED} of 17",
                     estimate=f"{n_mean} of 17 (median |dev| {rice.dev_mean.abs().median():.3f})",
                     passed=n_mean >= NEED))
    gate.append(dict(criterion="G1 rice CPI SDs within 0.5 of Table 1", target=f">= {NEED} of 17",
                     estimate=f"{n_sd} of 17 (median |dev| {rice.dev_sd.abs().median():.3f})", passed=n_sd >= NEED))
    fuel_mad = {v: t1[t1.variable == v].dev_mean.abs().median() for v in ["cpi_fuel_hh", "cpi_fuel_tr"]}
    fuel = min(fuel_mad, key=fuel_mad.get)
    fsub = t1[t1.variable == fuel]
    n_fuel = int((fsub.dev_mean.abs() <= TOL).sum())
    gate.append(dict(criterion="G1b fuel CPI means within 0.5 (better candidate)", target=f">= {NEED} of 17",
                     estimate=f"{fuel}: {n_fuel} of 17 (median |dev| {fuel_mad[fuel]:.3f}; other "
                              f"{[v for v in fuel_mad if v != fuel][0]}: {max(fuel_mad.values()):.3f})",
                     passed=n_fuel >= NEED))
    (T / "replication_choice.json").write_text(json.dumps(
        {"fuel": fuel, "fuel_median_abs_dev": fuel_mad, "fuel_replicated": bool(n_fuel >= NEED)}, indent=2))

    # ---- G2: PVAR replica on all 17 regions
    d = pvar_data(reg, fuel)
    res = fit_pvar(d, ORDER, "region", "t", p=1)
    q = irf(res, H=10, draws=200, level=0.95, seed=2024)
    q["sample"] = "all"
    r = shape(q, "THAI")
    peak_h = int(r.irf.idxmax())
    peak = r.irf.max()
    gate.append(dict(criterion="G2(i) THAI->RPI 95% band above zero at h=1", target="lo > 0",
                     estimate=f"irf {r.irf[1]:.3f} [{r.lo[1]:.3f}, {r.hi[1]:.3f}]", passed=bool(r.lo[1] > 0)))
    gate.append(dict(criterion="G2(ii) THAI->RPI peaks at h=1 or 2", target="h in {1,2}",
                     estimate=f"peak at h={peak_h} ({peak:.3f})", passed=peak_h in (1, 2)))
    gate.append(dict(criterion="G2(iii) THAI->RPI below 25% of peak by h=6", target="< 0.25 x peak",
                     estimate=f"h=6: {r.irf[6]:.3f} ({r.irf[6] / peak:.2f} of peak)",
                     passed=bool(r.irf[6] < 0.25 * peak)))
    rf = shape(q, "FPI")
    gate.append(dict(criterion="G2(iv) FPI->RPI positive at h=0", target="> 0",
                     estimate=f"{rf.irf[0]:.3f} [{rf.lo[0]:.3f}, {rf.hi[0]:.3f}]", passed=bool(rf.irf[0] > 0)))
    gate.append(dict(criterion="G2(v) FPI->RPI below 25% of impact by h=3", target="< 0.25 x h0",
                     estimate=f"h=3: {rf.irf[3]:.3f} ({rf.irf[3] / rf.irf[0]:.2f} of impact)",
                     passed=bool(rf.irf[3] < 0.25 * rf.irf[0])))

    # ---- G3: subsamples
    groups = pd.read_csv(ROOT / "replication/antonio2024_region_groups.csv").set_index("region")
    peaks, irfs = {}, [q]
    subs = {"insufficient": groups.index[groups.self_sufficiency_class == "Insufficient"],
            "sufficient": groups.index[groups.self_sufficiency_class == "Sufficient"],
            "low_poverty": groups.index[groups.poverty_class == "Low"],
            "high_poverty": groups.index[groups.poverty_class == "High"]}
    for name, regs in subs.items():
        rs = fit_pvar(d[d.region.isin(regs)], ORDER, "region", "t", p=1)
        qs = irf(rs, H=10, draws=200, level=0.95, seed=2024)
        qs["sample"] = name
        irfs.append(qs)
        peaks[name] = shape(qs, "THAI").irf.max()
    ratio = peaks["insufficient"] / peaks["sufficient"]
    gate.append(dict(criterion="G3 peak ratio insufficient/sufficient", target="in [1.3, 3.0]",
                     estimate=f"{ratio:.2f} ({peaks['insufficient']:.3f} / {peaks['sufficient']:.3f})",
                     passed=bool(1.3 <= ratio <= 3.0)))
    gate.append(dict(criterion="G3 peak high poverty < low poverty", target="high < low",
                     estimate=f"high {peaks['high_poverty']:.3f} vs low {peaks['low_poverty']:.3f}",
                     passed=bool(peaks["high_poverty"] < peaks["low_poverty"])))
    pd.concat(irfs).to_csv(T / "replication_pvar_irf.csv", index=False, float_format="%.5f")

    # ---- exploratory diagnostic after G3 failed (not part of the gate): impact (h=0) and
    # six-month cumulative responses by group, p = 1 and p = 2, matching the paper's wording
    from rtl.pvar import _oirf
    diag = []
    subs["medium_poverty"] = groups.index[groups.poverty_class == "Medium"]
    for p_ in (1, 2):
        for name, regs in subs.items():
            rs = fit_pvar(d[d.region.isin(regs)], ORDER, "region", "t", p=p_)
            o = _oirf(rs["A"], rs["Sigma"], 10)[:, ORDER.index("RPI"), ORDER.index("THAI")]
            diag.append(dict(p=p_, sample=name, impact_h0=o[0], peak=o.max(), peak_h=int(o.argmax()),
                             cum_h0_5=o[:6].sum()))
    pd.DataFrame(diag).to_csv(T / "replication_g3_diagnostic.csv", index=False, float_format="%.4f")

    # ---- indicative: LP on the reference sample
    s = reg.sort_values(["region", "month"]).reset_index(drop=True)
    s["f_real_shock"] = s.f_real
    mask = (s.month >= pd.Period("1995-01", "M")) & (s.month <= END)
    lp = local_projection(s, y="dl_rice", x="f_real_shock", time="t", unit="region", horizons=6, p=12,
                          cumulative=True, se="driscoll_kraay", sample=mask)
    lp.to_csv(T / "replication_lp_indicative.csv", index=False, float_format="%.5f")

    g = pd.DataFrame(gate)
    g.to_csv(T / "replication_gate.csv", index=False)
    print(g.to_string(index=False))
    print("\nOVERALL:", "PASS" if g.passed.all() else "FAIL")
    print("\nindicative LP (cumulative, real THAI):\n", lp[["h", "beta", "se", "lo", "hi"]].round(4).to_string())


if __name__ == "__main__":
    main()

```

## `scripts/05_estimate.py`

```python
"""Estimate RQ1-RQ5 and the robustness menu exactly as pre-specified in CLAUDE.md.

All local projections: h = 0..12, p = 12, Teulings-Zubanov leads, trend, cumulative
responses, 90% bands; Driscoll-Kraay (panel) or Newey-West (national).
Writes output/tables/estimates.csv (one long table: rq, spec, outcome, cumulative, h,
term, beta, se, lo, hi, nobs, n_units, r2) and output/tables/rq3_gap.csv.

Term names: 'shock' is the pre-law pass-through when the model interacts the shock
with `post`, and the post-law pass-through when it interacts with `pre`;
'shock_x_post' is the change (theta). Specs whose name ends in '_postparam' are the
re-parametrised models that give the post-law B_h directly.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rtl.lp import local_projection  # noqa: E402

P = ROOT / "data/processed"
T = ROOT / "output/tables"
H, LAGS = 12, 12
M = lambda s: pd.Period(s, "M")  # noqa: E731
ROWS = []


def run(rq, spec, df, y, x="f", unit="region", se=None, interact=(), exog=(), controls=(), start="1995-01",
        end="2026-09", p=LAGS, extra_mask=None, cumulative=True):
    se = se or ("driscoll_kraay" if unit else "newey_west")
    mask = (df.month >= M(start)) & (df.month <= M(end))
    if extra_mask is not None:
        mask &= extra_mask
    res = local_projection(df, y=y, x=x, time="t", unit=unit, horizons=H, p=p, interact=tuple(interact),
                           exog=tuple(exog), controls=tuple(controls), sample=mask, cumulative=cumulative, se=se)
    res.insert(0, "cumulative", cumulative)
    res.insert(0, "outcome", y)
    res.insert(0, "spec", spec)
    res.insert(0, "rq", rq)
    ROWS.append(res)
    return res


def regime(rq, spec, df, y, unit="region", **kw):
    """Pre-law B (shock), change theta (shock_x_post), and post-law B (spec + '_postparam')."""
    ex = tuple(kw.pop("exog", ()))
    run(rq, spec, df, y, unit=unit, interact=("post",) + tuple(kw.pop("interact_more", ())), exog=("post",) + ex,
        **kw)
    run(rq, spec + "_postparam", df, y, unit=unit, interact=("pre",), exog=("post",) + ex, **kw)


def main():
    reg = pd.read_parquet(P / "panel_region.parquet").sort_values(["region", "month"]).reset_index(drop=True)
    nat = pd.read_parquet(P / "panel_national.parquet").sort_values("month").reset_index(drop=True)
    nat = nat[nat.month <= M("2026-09")].reset_index(drop=True)
    for d in (reg, nat):
        d["fpos"] = (d.f > 0).astype(float)
        d["placebo"] = (d.month >= M("2016-03")).astype(int)
        d["pre"] = 1 - d.post

    # ---------------- RQ1: regional rice CPI ----------------
    run("RQ1", "full_sample", reg, "dl_rice")
    regime("RQ1", "main", reg, "dl_rice")
    regime("RQ1", "national", nat, "dl_rice", unit=None)

    # ---------------- RQ2: along the chain (national, 2010-) ----------------
    for y in ["dl_farmgate_palay", "dl_wholesale_rmr", "dl_retail_rmr", "dl_rice"]:
        regime("RQ2", "chain_national", nat, y, unit=None, start="2011-01")
    farm = reg[reg.region != "NCR"].reset_index(drop=True)
    regime("RQ2", "farmgate_regional", farm, "dl_farmgate_palay", start="2011-01")
    regime("RQ2", "retail_regional", reg, "dl_retail_rmr", start="2011-01")

    # ---------------- RQ4: heterogeneity (D9, D11: not validated) ----------------
    for g in ["insuff", "highpov"]:
        run("RQ4", f"het_{g}", reg, "dl_rice", interact=(g, "post", f"post_{g}"), exog=("post", f"post_{g}"))

    # ---------------- RQ5: distribution (national) ----------------
    run("RQ5", "gap_full", nat, "dD", unit=None, start="2001-01")
    regime("RQ5", "gap", nat, "dD", unit=None, start="2001-01")
    run("RQ5", "rice_national_2001", nat, "dl_rice", unit=None, start="2001-01")
    run("RQ5", "all_items", nat, "dl_all", unit=None, start="2001-01")
    run("RQ5", "all_items_b30", nat, "dl_all_b30", unit=None, start="2001-01")

    # ---------------- Robustness (RQ1 main) ----------------
    R = "ROB"
    regime(R, "a_real_shock", reg, "dl_rice", x="f_real")
    regime(R, "b_viet5", reg, "dl_rice", x="f_viet", start="2005-02")
    regime(R, "c_usd_fx_control", reg, "dl_rice", x="f_usd", controls=("dl_fx",))
    regime(R, "d_macro_controls", reg, "dl_rice", controls=("dl_fx", "dl_dubai_php", "dl_urea_php", "oni"))
    regime(R, "e_p6", reg, "dl_rice", p=6)
    regime(R, "e_p18", reg, "dl_rice", p=18, start="1995-07")
    regime(R, "f_no_2008crisis", reg, "dl_rice", extra_mask=~reg.month.between(M("2007-10"), M("2008-12")))
    regime(R, "g_no_2020", reg, "dl_rice", extra_mask=~reg.month.between(M("2020-01"), M("2020-12")))
    regime(R, "h_end_2024m6", reg, "dl_rice", end="2024-06")
    regime(R, "i_symmetric_2012", reg, "dl_rice", start="2012-03")
    run(R, "j_asymmetry", reg, "dl_rice", interact=("post", "fpos"), exog=("post", "fpos"))
    regime(R, "k_drop_newgeo", reg, "dl_rice", extra_mask=reg.new_geo_ext == 0)
    for r in sorted(reg.region.unique()):
        d = reg[reg.region != r].reset_index(drop=True)
        run(R, f"l_loo_{r}", d, "dl_rice", interact=("post",), exog=("post",))
    run(R, "m_separate_pre", reg, "dl_rice", end="2019-02")
    run(R, "m_separate_post", reg, "dl_rice", start="2019-03")
    run(R, "n_placebo_2016m3", reg, "dl_rice", interact=("placebo",), exog=("placebo",), end="2019-02")
    regime(R, "o_cluster_region", reg, "dl_rice", se="cluster")

    est = pd.concat(ROWS, ignore_index=True)
    est.to_csv(T / "estimates.csv", index=False, float_format="%.6f")

    # ---------------- RQ3: border gap, interrupted time series ----------------
    g = nat[(nat.month >= M("2010-01")) & (nat.month <= M("2026-09"))].copy()
    g["gap_wholesale"] = 100 * np.log(g.wholesale_rmr / (g.thai5_php / 1000))
    g["gap_retail"] = 100 * np.log(g.retail_rmr / (g.thai5_php / 1000))
    g["ln_world"] = 100 * np.log(g.thai5_php / 1000)
    months = pd.get_dummies(g.month.dt.month, prefix="m", drop_first=True).astype(float)
    rows = []
    for yv in ["gap_wholesale", "gap_retail"]:
        for spec, cols in [("its", ["post", "tariff15", "ban"]), ("its_world", ["post", "tariff15", "ban", "ln_world"])]:
            X = sm.add_constant(pd.concat([g[cols].astype(float), months], axis=1))
            fit = sm.OLS(g[yv], X).fit(cov_type="HAC", cov_kwds={"maxlags": 12})
            for c in cols:
                rows.append(dict(outcome=yv, spec=spec, term=c, beta=fit.params[c], se=fit.bse[c],
                                 p=fit.pvalues[c], nobs=int(fit.nobs), r2=fit.rsquared))
    pd.DataFrame(rows).to_csv(T / "rq3_gap.csv", index=False, float_format="%.5f")
    g[["month", "gap_wholesale", "gap_retail", "ln_world", "post", "tariff15", "ban"]].assign(
        month=lambda d: d.month.astype(str)).to_csv(T / "rq3_gap_series.csv", index=False, float_format="%.4f")

    key = est[(est.h.isin([6, 12]))]
    show = key[key.spec.isin(["full_sample", "main", "main_postparam", "national", "national_postparam"])]
    print(show[["rq", "spec", "h", "term", "beta", "se"]].round(3).to_string(index=False))
    print(pd.DataFrame(rows).round(3).to_string(index=False))


if __name__ == "__main__":
    main()

```

## `scripts/06_figures.py`

```python
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

```

## `scripts/07_episode_2024.py`

```python
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

```

## `scripts/08_paper.py`

```python
"""Build the numbers dictionary and tables, then render the working paper and the manuscript.

paper/<doc>_template.md -> Jinja2 (numbers n, tables t) -> paper/<doc>.md -> pandoc (citeproc) -> .docx
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rtl.numbers import build  # noqa: E402
from rtl.render_doc import render  # noqa: E402

DOCS = ["working_paper", "manuscript"]


def main():
    n, t = build()
    num = ROOT / "output/tables/paper_numbers.json"
    for d in DOCS:
        tpl = ROOT / f"paper/{d}_template.md"
        if tpl.exists():
            render(tpl, ROOT / f"paper/{d}.md", numbers=num, bib=ROOT / "paper/references.bib",
                   toc=(d == "working_paper"), resource_path=str(ROOT / "paper"), tables=t)


if __name__ == "__main__":
    main()

```

## `scripts/09_descriptive.py`

```python
"""Objective 1: descriptive statistics (pre-specified in CLAUDE.md, section 4.6 of the skill).

Writes to output/tables/:
  desc_subperiods.csv     mean and SD of monthly inflation (rice CPI, world shock, chain prices) by sub-period
  desc_annual.csv         annual (Dec/Dec) inflation: rice all income, rice bottom 30%, headline,
                          headline bottom 30%, world rice in PHP; rice contribution to headline (E5)
  desc_episodes.csv       world price episodes: runs of >= 3 months with 12-month change >= +15%
  desc_crosscorr.csv      correlation of world shock f_t with national rice inflation at t+k, pre/post law
  desc_dispersion.csv     cross-region SD of monthly rice inflation and CV of retail RMR price levels, by year
  desc_adf.csv            ADF unit-root tests (levels in logs and monthly changes)
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
P, T = ROOT / "data/processed", ROOT / "output/tables"
M = lambda s: pd.Period(s, "M")  # noqa: E731
PERIODS = [("1995M1-2007M9", "1995-01", "2007-09"), ("2007M10-2008M12 (world crisis)", "2007-10", "2008-12"),
           ("2009M1-2019M2 (quotas)", "2009-01", "2019-02"), ("2019M3-2024M6 (35% tariff)", "2019-03", "2024-06"),
           ("2024M7-2026M9 (15% tariff, suspension, indexed tariff)", "2024-07", "2026-09")]


def main():
    nat = pd.read_parquet(P / "panel_national.parquet").sort_values("month")
    nat = nat[nat.month <= M("2026-09")].set_index("month")
    reg = pd.read_parquet(P / "panel_region.parquet")
    w = pd.read_parquet(P / "cpi_weights.parquet")

    rows = []
    for name, a, b in PERIODS:
        s = nat.loc[M(a):M(b)]
        for v in ["dl_rice", "dl_rice_b30", "f", "dl_all", "dl_farmgate_palay", "dl_wholesale_rmr", "dl_retail_rmr"]:
            x = s[v].dropna()
            if len(x) > 2:
                rows.append(dict(period=name, variable=v, months=len(x), mean=x.mean(), sd=x.std(),
                                 annualised_mean=12 * x.mean()))
    pd.DataFrame(rows).to_csv(T / "desc_subperiods.csv", index=False, float_format="%.3f")

    dec = nat[nat.index.month == 12]
    ann = pd.DataFrame({
        "rice_all": 100 * np.log(dec.cpi_rice).diff(), "rice_b30": 100 * np.log(dec.cpi_rice_b30).diff(),
        "headline_all": 100 * np.log(dec.cpi_all).diff(), "headline_b30": 100 * np.log(dec.cpi_all_b30).diff(),
        "world_rice_php": 100 * np.log(dec.thai5_php).diff()})
    ann.index = ann.index.year
    wa = float(w[(w.geo == "Philippines") & (w.group == "all") & (w["item"] == "rice") & (w.coding == "old")].weight.iloc[0])
    wb = float(w[(w.geo == "Philippines") & (w.group == "b30") & (w["item"] == "rice")].weight.iloc[0])
    ann["rice_contrib_all"] = wa / 100 * ann.rice_all       # E5, approximate (2018 weights)
    ann["rice_contrib_b30"] = wb / 100 * ann.rice_b30
    sep = nat.loc[M("2026-09")]
    sep25 = nat.loc[M("2025-09")]
    ann.loc[2026] = [100 * np.log(sep.cpi_rice / sep25.cpi_rice), 100 * np.log(sep.cpi_rice_b30 / sep25.cpi_rice_b30),
                     100 * np.log(sep.cpi_all / sep25.cpi_all), 100 * np.log(sep.cpi_all_b30 / sep25.cpi_all_b30),
                     100 * np.log(sep.thai5_php / sep25.thai5_php), np.nan, np.nan]
    ann.loc[2026, "rice_contrib_all"] = wa / 100 * ann.loc[2026, "rice_all"]
    ann.loc[2026, "rice_contrib_b30"] = wb / 100 * ann.loc[2026, "rice_b30"]
    ann.index.name = "year"  # 2026 = September 2025 to September 2026
    ann.dropna(how="all").to_csv(T / "desc_annual.csv", float_format="%.3f")

    yoy = 100 * np.log(nat.thai5_php / nat.thai5_php.shift(12))
    hot = (yoy >= 15).astype(int)
    eps, start = [], None
    for m, v in hot.items():
        if v and start is None:
            start = m
        if (not v or m == hot.index[-1]) and start is not None:
            end = m - 1 if not v else m
            if (end - start).n + 1 >= 3:
                s = nat.loc[start:end]
                eps.append(dict(start=str(start), end=str(end), months=(end - start).n + 1,
                                peak_world_yoy=yoy.loc[start:end].max(),
                                world_change=100 * np.log(s.thai5_php.iloc[-1] / nat.thai5_php.loc[start - 1]),
                                rice_cpi_change=100 * np.log(s.cpi_rice.iloc[-1] / nat.cpi_rice.loc[start - 1])))
            start = None
    pd.DataFrame(eps).to_csv(T / "desc_episodes.csv", index=False, float_format="%.2f")

    cc = []
    for name, a, b in [("pre", "1995-01", "2019-02"), ("post", "2019-03", "2026-09")]:
        s = nat.loc[M(a):M(b)]
        for k in range(-6, 13):
            cc.append(dict(regime=name, k=k, corr=s.f.corr(s.dl_rice.shift(-k))))
    pd.DataFrame(cc).to_csv(T / "desc_crosscorr.csv", index=False, float_format="%.4f")

    reg["year"] = reg.month.dt.year
    disp = reg.groupby("month").agg(sd_rice_infl=("dl_rice", "std")).reset_index()
    disp["year"] = disp.month.dt.year
    d1 = disp.groupby("year").sd_rice_infl.mean()
    lv = reg.dropna(subset=["retail_rmr"]).groupby(["year", "region"]).retail_rmr.mean().reset_index()
    d2 = lv.groupby("year").retail_rmr.agg(lambda x: 100 * x.std() / x.mean())
    pd.DataFrame({"sd_monthly_rice_inflation_across_regions": d1, "cv_retail_rmr_level_across_regions": d2}) \
        .loc[1995:2026].to_csv(T / "desc_dispersion.csv", float_format="%.3f")

    adf = []
    for v, lab in [("cpi_rice", "ln rice CPI"), ("thai5_php", "ln world rice (PHP)"), ("retail_rmr", "ln retail RMR"),
                   ("farmgate_palay", "ln farmgate palay")]:
        x = np.log(nat[v].dropna())
        for form, s in [("level", x), ("monthly change", 100 * x.diff().dropna())]:
            stat, p, *_ = adfuller(s, regression="ct" if form == "level" else "c", autolag="AIC", result_object=False)
            adf.append(dict(series=lab, form=form, start=str(s.index.min()), adf_stat=stat, p_value=p))
    pd.DataFrame(adf).to_csv(T / "desc_adf.csv", index=False, float_format="%.3f")
    print(pd.read_csv(T / "desc_subperiods.csv").query("variable in ['dl_rice','f']").round(2).to_string(index=False))
    print(pd.read_csv(T / "desc_episodes.csv").to_string(index=False))
    print(pd.read_csv(T / "desc_annual.csv").tail(9).round(2).to_string(index=False))


if __name__ == "__main__":
    main()

```

## `scripts/10_analysis_report.py`

```python
"""Render the visual analysis report and generate the statistical annex (every estimate).

docs/analysis_report_template.md -> docs/analysis_report.{md,docx}
output/tables/*.csv              -> docs/statistical_annex.{md,docx}
"""

import json
import sys
from pathlib import Path

import pandas as pd
import pypandoc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rtl.numbers import f2, md_table, stars  # noqa: E402
from rtl.render_doc import render  # noqa: E402

T = ROOT / "output/tables"
SPEC_NOTES = {
    "full_sample": "RQ1, regional rice CPI, one regime, 1995M1–2026M9",
    "main": "RQ1 main: shock = before the law, shock_x_post = change",
    "main_postparam": "RQ1 main re-parametrised: shock = after the law",
    "national": "RQ1, national rice CPI (Newey–West)",
    "national_postparam": "RQ1, national, after the law",
    "chain_national": "RQ2, national chain prices 2011M1–2026M9",
    "chain_national_postparam": "RQ2, after the law",
    "farmgate_regional": "RQ2 check, regional farmgate panel (16 regions; no farmgate data for NCR)",
    "farmgate_regional_postparam": "RQ2 check, after the law",
    "retail_regional": "RQ2 check, regional retail RMR panel",
    "retail_regional_postparam": "RQ2 check, after the law",
    "het_insuff": "RQ4, rice-deficit regions (not validated)",
    "het_highpov": "RQ4, high-poverty regions (not validated)",
    "gap_full": "RQ5, gap all income − bottom 30%, 2001M1–2026M9",
    "gap": "RQ5 gap with regime interaction",
    "gap_postparam": "RQ5 gap after the law",
    "rice_national_2001": "RQ5 mechanism, national rice CPI 2001M1–2026M9",
    "all_items": "RQ5, all-items CPI, all income",
    "all_items_b30": "RQ5, all-items CPI, bottom 30%",
}


def annex():
    est = pd.read_csv(T / "estimates.csv")
    tabs = json.loads((T / "paper_tables.json").read_text())
    out = ["---", 'title: "Statistical Annex"', 'subtitle: "Rice Tariffication and Rice Prices"',
           'date: "October 2026"', "---", "",
           "Every estimate of the study, generated from `output/tables/estimates.csv`. Coefficients are "
           "cumulative responses in percentage points per 1% world rice price rise (pesos); standard "
           "errors in parentheses (Driscoll–Kraay for regional panels, Newey–West for national series); "
           "\\* p<0.10, \\*\\* p<0.05, \\*\\*\\* p<0.01. Robustness specs are lettered as in the "
           "pre-registered plan (`CLAUDE.md`).", "",
           "# A. Descriptive and policy tables", "",
           "## Table A1. World rice price episodes since 1995", tabs["desc_episodes"], "",
           "## Table A2. The 2024 tariff cut by region (log points)", tabs["ep_regions"], "",
           "## Table A3. Region groups (Antonio et al. 2024) and 2018 rice weights", tabs["groups"], "",
           "## Table A4. Rice inflation by period", tabs["desc_periods"], "",
           "## Table A5. Annual inflation and rice contributions", tabs["desc_annual"], "",
           "## Table A6. Replication gate", tabs["gate"], "",
           "## Table A7. Border gap regressions", tabs["rq3"], "",
           "# B. All local projection estimates", ""]
    specs = [s for s in est.spec.unique() if not s.startswith("l_loo")]
    for i, spec in enumerate(specs, 1):
        d = est[est.spec == spec]
        for outcome in d.outcome.unique():
            q = d[d.outcome == outcome]
            terms = list(q.term.unique())
            rows = []
            for h in sorted(q.h.unique()):
                r = [h]
                for term in terms:
                    x = q[(q.h == h) & (q.term == term)].iloc[0]
                    r.append(f"{f2(x.beta, 3)}{stars(x.beta, x.se)} ({f2(x.se, 3)})")
                x = q[q.h == h].iloc[0]
                r += [int(x.nobs), int(x.n_units)]
                rows.append(r)
            note = SPEC_NOTES.get(spec, "Robustness check, " + spec.replace("_", " "))
            out += [f"## Table B{i}. {spec} — {outcome}", "", note, md_table(["h"] + terms + ["N", "Units"], rows), ""]
    loo = est[est.spec.str.startswith("l_loo") & (est.term == "shock_x_post") & est.h.isin([6, 12])]
    rows = []
    for spec in sorted(loo.spec.unique()):
        q = loo[loo.spec == spec].set_index("h")
        rows.append([spec.replace("l_loo_", ""), f"{f2(q.beta[6], 3)} ({f2(q.se[6], 3)})",
                     f"{f2(q.beta[12], 3)} ({f2(q.se[12], 3)})"])
    out += ["## Table B-LOO. Robustness (l): change θ leaving one region out", "",
            md_table(["Region left out", "θ, h = 6", "θ, h = 12"], rows)]
    path = ROOT / "docs/statistical_annex.md"
    path.write_text("\n".join(out))
    pypandoc.convert_file(str(path), "docx", outputfile=str(path.with_suffix(".docx")), extra_args=["--toc"])
    print("wrote", path)


def main():
    render(ROOT / "docs/analysis_report_template.md", ROOT / "docs/analysis_report.md",
           numbers=T / "paper_numbers.json", resource_path=str(ROOT / "docs"))
    annex()


if __name__ == "__main__":
    main()

```

## `scripts/11_master_document.py`

```python
"""Assemble the master document: narrative + every document + all code + git log.

docs/master_narrative_template.md (rendered with the numbers) is followed by appendices,
each with its YAML front matter stripped and its headings demoted by one level.
Writes docs/master_document.md and .docx.
"""

import re
import subprocess
import sys
from pathlib import Path

import jinja2
import pypandoc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

APPENDICES = [
    ("Concept note", "docs/concept_note.md"),
    ("Project brief and decisions log (CLAUDE.md)", "CLAUDE.md"),
    ("Raw data source log", "data/raw/source_log.md"),
    ("Sourced policy facts", "paper/policy_context.md"),
    ("Analysis report", "docs/analysis_report.md"),
    ("Statistical annex", "docs/statistical_annex.md"),
    ("Working paper", "paper/working_paper.md"),
    ("Journal manuscript", "paper/manuscript.md"),
    ("Submission checklist", "paper/SUBMISSION_CHECKLIST.md"),
]
CODE_GLOBS = ["run_all.sh", "rtl/*.py", "scripts/*.py", "tests/*.py"]


def strip_yaml(text):
    return re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)


def demote(text):
    out, fence = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            fence = not fence
        out.append("#" + line if (not fence and re.match(r"^#{1,5} ", line)) else line)
    return "\n".join(out)


def main():
    import json
    n = json.loads((ROOT / "output/tables/paper_numbers.json").read_text())
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ROOT / "docs"), undefined=jinja2.StrictUndefined,
                             comment_start_string="<#--", comment_end_string="--#>")
    parts = [env.get_template("master_narrative_template.md").render(n=n)]
    letter = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for title, rel in APPENDICES:
        p = ROOT / rel
        if not p.exists():
            continue
        body = demote(strip_yaml(p.read_text()))
        body = body.replace("::: {#refs}\n:::", "")  # one reference list, at the end
        parts.append(f"\n# Appendix {next(letter)}. {title}\n\n*Source file: `{rel}`*\n\n{body}\n")
    code = [f"\n# Appendix {next(letter)}. All code\n"]
    for g in CODE_GLOBS:
        for f in sorted(ROOT.glob(g)):
            lang = "bash" if f.suffix == ".sh" else "python"
            code.append(f"\n## `{f.relative_to(ROOT)}`\n\n```{lang}\n{f.read_text()}\n```\n")
    parts.append("".join(code))
    log = subprocess.run(["git", "log", "--date=iso", "--pretty=format:%h %ad %s"], cwd=ROOT,
                         capture_output=True, text=True).stdout
    parts.append(f"\n# Appendix {next(letter)}. Git log\n\n```\n{log}\n```\n")
    parts.append("\n# References\n\n::: {#refs}\n:::\n")
    out = ROOT / "docs/master_document.md"
    out.write_text("\n".join(parts))
    pypandoc.convert_file(str(out), "docx", outputfile=str(out.with_suffix(".docx")),
                          extra_args=["--toc", "--toc-depth=2", "--citeproc",
                                      f"--bibliography={ROOT / 'paper/references.bib'}",
                                      f"--resource-path={ROOT / 'docs'}:{ROOT / 'paper'}"])
    print("wrote", out)


if __name__ == "__main__":
    main()

```

## `tests/test_lp.py`

```python
"""Check that the local projection recovers a known impulse response."""

import numpy as np
import pandas as pd
import pytest

from rtl.lp import local_projection

RHO = 0.4
B = [0.04, 0.02, 0.01]  # direct effect of x_t, x_{t-1}, x_{t-2} on y_t


def true_irf(H):
    """Response of y_{t+h} to a unit x_t when y_t = RHO*y_{t-1} + sum_j B_j x_{t-j} + e."""
    irf = []
    for h in range(H + 1):
        prev = irf[-1] if irf else 0.0
        irf.append(RHO * prev + (B[h] if h < len(B) else 0.0))
    return np.array(irf)


def simulate(n_units, T, seed=0):
    rng = np.random.default_rng(seed)
    frames = []
    for i in range(n_units):
        x = rng.normal(0, 3, T)
        y = np.zeros(T)
        for t in range(T):
            y[t] = 0.002 * (i % 5) + RHO * (y[t - 1] if t else 0) + rng.normal(0, 0.2)
            y[t] += sum(b * x[t - j] for j, b in enumerate(B) if t - j >= 0)
        frames.append(pd.DataFrame({"unit": i, "t": np.arange(T), "y": y, "x": x}))
    return pd.concat(frames, ignore_index=True)


@pytest.mark.parametrize("unit,se", [(None, "newey_west"), ("unit", "cluster"), ("unit", "driscoll_kraay")])
def test_recovers_irf(unit, se):
    df = simulate(1 if unit is None else 20, 3000 if unit is None else 400)
    res = local_projection(df, "y", "x", time="t", unit=unit, horizons=6, p=12, se=se)
    est = res.loc[res.term == "shock", "beta"].to_numpy()
    np.testing.assert_allclose(est, true_irf(6), atol=0.006)


def test_cumulative_is_running_sum():
    df = simulate(10, 400, seed=1)
    m = local_projection(df, "y", "x", time="t", unit="unit", horizons=4, p=6)
    c = local_projection(df, "y", "x", time="t", unit="unit", horizons=4, p=6, cumulative=True)
    np.testing.assert_allclose(c.beta, np.cumsum(true_irf(4)), atol=0.01)
    assert np.all(c.se.to_numpy()[1:] > 0) and len(m) == len(c)


def test_interaction_detects_group_difference():
    df = simulate(20, 400, seed=2)
    df["G"] = (df.unit % 2).astype(float)
    df["y"] += 0.03 * df.G * df.x  # extra impact effect in group G
    res = local_projection(df, "y", "x", time="t", unit="unit", horizons=0, p=6, interact=("G",))
    theta = res.loc[res.term == "shock_x_G", "beta"].iloc[0]
    assert abs(theta - 0.03) < 0.005

```

## `tests/test_pvar.py`

```python
"""Check that the panel VAR recovers known coefficients and impulse responses."""

import numpy as np
import pandas as pd

from rtl.pvar import fit_pvar, irf, _fod

A_TRUE = np.array([[0.5, 0.2], [0.0, 0.3]])


def simulate(n_units=17, T=300, seed=1):
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n_units):
        fe = rng.normal(0, 1, 2)
        y = np.zeros(2)
        for t in range(T + 50):
            y = fe + A_TRUE @ y + rng.normal(0, 1, 2)
            if t >= 50:
                rows.append(dict(unit=i, t=t, x1=y[0], x2=y[1]))
    return pd.DataFrame(rows)


def test_fod_removes_constant():
    a = np.full((10, 1), 3.0)
    assert np.allclose(_fod(a)[:-1], 0)


def test_pvar_recovers_coefficients():
    # average over five simulated panels: the estimator is unbiased, single draws have SE ~0.02
    A = np.mean([fit_pvar(simulate(seed=s), ["x1", "x2"], "unit", "t", p=1)["A"][0] for s in range(5)], axis=0)
    assert np.allclose(A, A_TRUE, atol=0.03)


def test_irf_impact_is_cholesky_factor():
    res = fit_pvar(simulate(), ["x1", "x2"], "unit", "t", p=1)
    q = irf(res, H=5, draws=50)
    imp = q[(q.h == 0)].set_index(["response", "shock"]).irf
    P = np.linalg.cholesky(res["Sigma"])
    assert np.isclose(imp[("x1", "x1")], P[0, 0]) and np.isclose(imp[("x1", "x2")], 0)
    # h = 1 response of x1 to its own shock equals A[0,0] * P[0,0] + A[0,1] * P[1,0]
    h1 = q[(q.h == 1) & (q.response == "x1") & (q.shock == "x1")].irf.iloc[0]
    A = res["A"][0]
    assert np.isclose(h1, A[0, 0] * P[0, 0] + A[0, 1] * P[1, 0])
    assert (q.lo <= q.hi).all()

```


# Appendix K. Git log

```
f4b9c79 2026-10-14 18:27:29 +0000 Phase 4: estimates for RQ1-RQ5, robustness menu, 2024 tariff-cut and 2025 suspension episodes, descriptives
9231ec8 2026-10-14 18:20:41 +0000 Phases 2-3: raw data, cleaning, panels, PVAR replica and replication gate
1b68579 2026-10-14 18:05:00 +0000 Phase 1: project brief, reference specification, pre-registered replication gate and estimation plan
```


# References

::: {#refs}
:::
