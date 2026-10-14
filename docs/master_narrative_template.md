---
title: "Master Document: How the Rice Tariffication Study Was Built"
subtitle: "Narrative of the process, every decision and every document, with all code"
date: "October 2026"
---

<#-- Rendered by scripts/11_master_document.py. --#>

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
({{ n.val_cpi_retail }}), and the Thai and Vietnamese world prices were compared
({{ n.val_thai_viet }}, low, which is why the Vietnamese price is a robustness check).

## 4. Phase 3: validation

Two independent checks came before any new estimate. Simulation tests confirm that the
local projection and the panel VAR recover known responses; one panel VAR test first
failed because a single simulated sample was two standard errors off, and was rewritten
to average five samples, after checking that the estimator is unbiased.

The replication gate gave a split verdict. The data replication was exact: our regional
means and standard deviations equal Antonio et al.'s in all 17 regions, and the fuel item
turned out to be transport fuels. The main impulse response was reproduced. But the third
criterion failed: the peak response in rice-deficit regions was {{ n.g3_peak_ratio }} times
that in surplus regions, just below the required 1.3, and the poverty ordering did not
hold. The skill's rule is not to loosen a criterion after seeing the result. A search for
a coding error found none, and two lags gave the same answer. An exploratory diagnostic
showed that the paper's own words ("immediate impact and peak almost twice") fit the
impact response ({{ n.g3_impact_ratio }}) better than the peak. The decision (D11) was to
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
