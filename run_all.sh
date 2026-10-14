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
