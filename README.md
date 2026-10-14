# Opening the Rice Border

Did the Philippine Rice Tariffication Law (RA 11203, March 2019) change how world rice
prices pass through to Philippine consumers, farmers and the poor? A fully reproducible
study on public data (PSA, World Bank, BSP, NOAA), 17 regions, 1994–September 2026,
replicating Antonio et al. (2024/2025) first.

## Documents

| Document | File | What it is |
|---|---|---|
| Working paper | `paper/working_paper.docx` | Six chapters, three objectives; Chapter 3 is a tutorial on the method |
| Journal manuscript | `paper/manuscript.docx` | Short IMRAD version |
| Analysis report | `docs/analysis_report.docx` | One analysis per page, with figures, in plain words |
| Statistical annex | `docs/statistical_annex.docx` | Every estimate, all horizons |
| Master document | `docs/master_document.docx` | Narrative of the process + every document + all code |
| Project brief | `CLAUDE.md` | Questions, decisions log, replication gate, plan, results, open questions |
| Session handoff | `docs/session_handoff.Rmd` | How to continue in a new session |

Every rendered document comes from a template (`*_template.md`) and the numbers in
`output/tables/paper_numbers.json`. Edit the templates, never the outputs.

## Rebuild

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
./run_all.sh              # from data/raw/ (about 5 minutes)
./run_all.sh --download   # refresh the raw data first
```

## Layout

`data/raw/` untouched downloads and `source_log.md`; `data/processed/` built by
scripts (not committed); `rtl/` estimators and helpers (local projections, panel VAR,
region names, numbers for documents); `scripts/01_…11_` the pipeline; `tests/`
simulation tests; `replication/` the reference paper's targets and groups;
`output/tables`, `output/figures` results; `paper/`, `docs/` templates and documents.
