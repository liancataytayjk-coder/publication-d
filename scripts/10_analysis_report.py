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
