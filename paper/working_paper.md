---
title: "Opening the Rice Border: World Price Pass-Through, Domestic Rice Prices and the Poor after the Philippine Rice Tariffication Law"
subtitle: "Working paper"
author: "[Name 1], [Name 2], [Name 3]"
date: "October 2026"
---



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

# Chapter 1. Introduction

## 1.1 Background

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

## 1.2 Rationale

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

## 1.3 Objectives

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

## 1.4 Significance

For the Department of Agriculture (DA), the National Economic and Development
Authority's successor, the Department of Economy, Planning and Development (DEPDev),
and the Tariff Commission, the study says how much a tariff change is likely to move
retail and farmgate prices, and how quickly. For the Bangko Sentral ng Pilipinas (BSP),
it measures how strongly world rice shocks feed into the CPI. For social protection,
it shows how much more these shocks hurt the poorest households.

## 1.5 Scope and limitations

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

## 1.6 Definition of terms

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

# Chapter 2. Review of Related Literature

## 2.1 How world prices reach domestic markets

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

## 2.2 Empirical pass-through and its timing

Studies of food price transmission to developing countries find partial and slow
transmission [@ceballos2017; @dawe2015]. Furceri et al. [-@furceri2016] use local
projections to show that global food price shocks raise domestic headline inflation
for several months, more in poorer countries. Kpodar and Liu [-@kpodar2022] use the same
method, with a correction for later shocks, to show that fuel price increases raise the
inflation of poor households more. Price responses along a chain are often asymmetric:
increases pass through faster than decreases [@meyer2004].

## 2.3 Rice tariffication in the Philippines

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

## 2.4 Regional evidence and the reference study

Valera, Balié and Magrini [-@valera2022] show that rice prices are a major source of
regional inflation. Antonio et al. [-@antonio2025] estimate a panel vector
autoregression (VAR) for 17 regions from 1994 to 2023: a world rice shock raises
regional rice inflation, peaks after one month and fades within about five months;
the effect is larger in rice-deficit regions. Their data are public, so we use their
paper as the reference to replicate.

## 2.5 Synthesis and gap

The literature agrees that world prices matter and that the domestic chain is not
perfectly competitive. It does not tell us whether the switch from quotas to tariffs
*changed* pass-through to consumers, farmers and the poor, and how the later policy
reversals (tariff cut, suspension, indexed tariff) fit that picture. That is the gap
this study fills.

## 2.6 Conceptual framework

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

# Chapter 3. Digression: the model and how to implement it

This chapter is a tutorial. Someone new to the method should be able to reproduce the
study from it.

## 3.1 The question an impulse response answers

We want the path of domestic rice prices in the months after a world price change,
holding everything else as it would otherwise have been. That path is an *impulse
response*: the response of $y$ at $t+h$ to a one-unit shock at $t$, for $h = 0, 1, 2,\dots$

## 3.2 The local projection idea

A VAR estimates one model of how all variables evolve together and then iterates it
forward to get the responses. A *local projection* [@jorda2005] skips the iteration: for
each horizon $h$ it runs a separate regression of the outcome $h$ months ahead on
today's shock. If the VAR is right both give the same answer [@plagborg2021]; if it is
wrong, the local projection is more robust, and its standard errors are simple
[@montielolea2021].

## 3.3 The specification term by term

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

## 3.4 From monthly effects to the level

Because the left side is a running sum, $B_6 = 0.4$ means that a 1% world price rise
raises the *level* of the rice CPI by 0.4% after six months. The monthly effect at
horizon $h$ is $B_h - B_{h-1}$.

## 3.5 Standard errors

Standard errors measure how uncertain an estimate is. Because all regions face the same
world price in the same month, their errors are correlated across regions and over time.
*Driscoll–Kraay* standard errors [@driscoll1998] allow for correlation over time and
across regions; for single national series we use *Newey–West* standard errors
[@newey1987], which allow for correlation over time. Bands in the figures are 90%
intervals.

## 3.6 The panel and group differences

To ask whether a group $G$ of regions (for example rice-deficit regions) changed
differently, we add $f_t\times G_r$, $f_t\times\text{post}_t\times G_r$ and the
corresponding dummies. The coefficient on the triple product is the extra change in
group $G$.

## 3.7 Checking the implementation

Before any real estimate we checked the code in two ways. First, simulation tests
(`tests/test_lp.py`, `tests/test_pvar.py`) generate data with a known response and
confirm that the estimators recover it. Second, the replication gate (Section 4.4)
reproduces a published result on the same public data.

## 3.8 Step-by-step implementation

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

## 3.9 Common pitfalls

Do not mix outcomes in levels and shocks in changes. Do not drop the leads: without them
$B_h$ partly measures later shocks. Do not use standard errors clustered only by region
when the shock is common to all regions: robustness check (o) shows they are several
times too small. Do not read a single significant horizon as a result; decide in
advance which horizons count (here $h = 6$ and $h = 12$).

# Chapter 4. Methodology

## 4.1 Design

The design compares pass-through before and after a national policy change, within a
panel of regions, with the reference study replicated first and every specification
fixed in advance. The pre-registered plan, the decisions log (D1–D12) and the
replication gate are in `CLAUDE.md` and were committed to the repository before the
corresponding estimates were run.

## 4.2 Data

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

## 4.3 Methods by objective

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

## 4.4 Validation: the replication gate

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

## 4.5 Software and reproducibility

Python 3 with pandas, statsmodels and linearmodels; figures in matplotlib; documents
rendered from templates with Jinja2 and pandoc. Raw files are kept unchanged; every
output and every number in this paper is regenerated by `./run_all.sh`.

## 4.6 Ethics

The study uses only published aggregate statistics; no human subjects are involved.

# Chapter 5. Results and Discussion

## 5.1 Objective 1: rice prices before and after the law

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

## 5.2 Objective 2: pass-through and the law

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

## 5.3 Objective 3: what the estimates imply for policy

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

# Chapter 6. Summary, Conclusions and Recommendations

## 6.1 Summary

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

## 6.2 Conclusions

The law did open the border to world price movements, most clearly for farmers, and it
coincided with a large one-off fall in rice prices in 2019. But openness works in both
directions: the poor now feel world price spikes more, and later cuts in the tariff were
absorbed in the chain rather than passed on.

## 6.3 Recommendations

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

## 6.4 Further research

Household-level data from the Family Income and Expenditure Survey would show net
buyers and net sellers directly; import volumes and margins by stage would show where
the tariff cut was absorbed; and a longer post-2026 sample will allow the indexed tariff
to be evaluated.

# References

::: {#refs}
:::
