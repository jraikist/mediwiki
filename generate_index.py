#!/usr/bin/env python3
"""
generate_index.py
Scans the docs/ folder and writes a wiki index with links to all .md files
(excluding index.md) into docs/index.md.
"""

import os
import re
from pathlib import Path

DOCS_DIR = Path("docs")
INDEX_FILE = DOCS_DIR / "index.md"

# --- Config ---
WIKI_TITLE = "Muistiinpanot"
WIKI_DESCRIPTION = "Tervetuloa! Lista Jaakon muistiinpanoista."


def slugify_to_title(filename: str) -> str:
    """Convert a filename like 'my-page-title.md' → 'My Page Title'."""
    name = Path(filename).stem          # strip .md
    name = re.sub(r"[-_]+", " ", name)  # hyphens/underscores → spaces
    return name.title()


def build_index():
    md_files = sorted(
        f for f in DOCS_DIR.iterdir()
        if f.is_file() and f.suffix == ".md" and f.name != "index.md"
    )

    if not md_files:
        print("No .md files found in docs/ (excluding index.md).")
        return

    lines = [
        f"# {WIKI_TITLE}",
        "",
        WIKI_DESCRIPTION,
        "",
        "## Sivut",
        "",
    ]

    for md_file in md_files:
        title = slugify_to_title(md_file.name)
        # MkDocs expects links relative to the docs/ root, without the leading docs/
        link = md_file.name
        lines.append(f"- [{title}]({link})")

    lines.append("")  # trailing newline
    lines.append("Jaakko Raikisto") # Add signature
    lines.append("jaakko@raikisto.fi")

    INDEX_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅  Written {len(md_files)} link(s) to {INDEX_FILE}")
    for f in md_files:
        print(f"   • {slugify_to_title(f.name)} → {f.name}")


if __name__ == "__main__":
    build_index()
