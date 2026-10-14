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
