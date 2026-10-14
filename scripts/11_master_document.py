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
