---
title: "Did Rice Tariffication Open the Border? World Price Pass-Through to Philippine Consumers, Farmers and the Poor"
author: "[Name 1], [Name 2], [Name 3]"
date: "October 2026"
---



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

# 1. Introduction

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

# 2. Methods

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

# 3. Results

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

# 4. Discussion

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

# Declarations

**Funding:** [to be completed]. **Competing interests:** none declared. **Data and code
availability:** all data are public (PSA OpenSTAT, World Bank, BSP, NOAA); raw files,
code and a one-command rebuild are in the replication package. **Author contributions:**
[to be completed].

# References

::: {#refs}
:::

# Figures

![Figure 1. Cumulative response of regional rice CPIs to a 1% world rice price rise (pesos), before the law (solid, grey 90% band) and after it (dashed, dotted 90% band), percentage points.](../output/figures/fig04_rq1_passthrough.png){width=80%}

![Figure 2. Cumulative response of national farmgate palay, wholesale and retail regular-milled rice prices to a 1% world rice price rise, before (solid) and after (dashed) the law, 90% bands.](../output/figures/fig05_rq2_chain.png){width=100%}

![Figure 3. Left: response of the all-items CPI for all income households (solid) and the bottom 30% (dashed). Right: response of the inflation gap, all income minus bottom 30%. Percentage points per 1%, 90% bands.](../output/figures/fig06_rq5_poor.png){width=95%}

![Figure 4. Change in the national rice CPI since June 2024 (log points): actual, predicted from world prices only, and predicted from world prices plus the July 2024 tariff cut, using post-law pass-through estimated on data ending June 2024.](../output/figures/fig09_episode_tariff_cut.png){width=80%}

![Figure 5. Change in cumulative pass-through after the law across robustness checks, at 6 and 12 months, with 90% intervals.](../output/figures/fig08_robustness.png){width=95%}
