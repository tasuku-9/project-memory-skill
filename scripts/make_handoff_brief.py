#!/usr/bin/env python3
"""Create a rough handoff brief from continuity memory docs.

This script is intentionally simple. It extracts the most relevant sections and
prints a draft that a human or model should refine.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

FILES = [
    "CONTEXT_MANIFEST.md",
    "RECOVERY_NOTES.md",
    "HUMAN_BRIEF.md",
    "CURRENT_STATE.md",
    "ROADMAP.md",
    "DECISION_LOG.md",
    "RESEARCH_LOG.md",
    "HYPOTHESIS_LAB.md",
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def latest_markdown_section(text: str, heading_pattern: str | None = None) -> str:
    """Return the first matching level-2 markdown section.

    Newest-first files should put the latest real entry near the top, but many
    templates contain instructional sections first. `heading_pattern` lets us
    skip those and find actual dated or ID-based entries.
    """
    if not text.strip():
        return ""

    heading_re = re.compile(r"^##\s+.+$", flags=re.MULTILINE)
    headings = list(heading_re.finditer(text))
    if not headings:
        return text.strip()

    chosen = headings[0]
    if heading_pattern:
        wanted = re.compile(heading_pattern)
        for heading in headings:
            if wanted.search(heading.group(0)):
                chosen = heading
                break

    start = chosen.start()
    following = [h for h in headings if h.start() > chosen.start()]
    end = following[0].start() if following else len(text)
    return text[start:end].strip()


def excerpt(text: str, max_chars: int) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "\n\n...[excerpt truncated]"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a rough handoff brief from memory docs.")
    parser.add_argument("target", help="Target project/workspace directory")
    parser.add_argument("--max-section-chars", type=int, default=2500)
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    project = target.name
    today = dt.date.today().isoformat()

    print(f"# Handoff Brief - {project} - {today}")
    print("")
    print("This is a generated draft. Review before sending to another human or model.")
    print("")

    recovery = read_text(target / "RECOVERY_NOTES.md")
    print("## Latest recovery checkpoint")
    print("")
    print(excerpt(latest_markdown_section(recovery, r"^##\s+\d{4}-\d{2}-\d{2}"), args.max_section_chars) if recovery else "Missing `RECOVERY_NOTES.md`.")
    print("")

    for rel in ["HUMAN_BRIEF.md", "CURRENT_STATE.md", "ROADMAP.md"]:
        text = read_text(target / rel)
        print(f"## Excerpt: {rel}")
        print("")
        print(excerpt(text, args.max_section_chars) if text else f"Missing `{rel}`.")
        print("")

    for rel in ["DECISION_LOG.md", "RESEARCH_LOG.md", "HYPOTHESIS_LAB.md"]:
        text = read_text(target / rel)
        print(f"## Latest relevant section: {rel}")
        print("")
        pattern = {"DECISION_LOG.md": r"^##\s+DEC-", "RESEARCH_LOG.md": r"^##\s+RES-", "HYPOTHESIS_LAB.md": r"^##\s+HYP-"}.get(rel)
        print(excerpt(latest_markdown_section(text, pattern), args.max_section_chars) if text else f"Missing `{rel}`.")
        print("")

    manifest = read_text(target / "CONTEXT_MANIFEST.md")
    print("## Context manifest excerpt")
    print("")
    print(excerpt(manifest, args.max_section_chars) if manifest else "Missing `CONTEXT_MANIFEST.md`.")
    print("")
    print("## Next recommended action")
    print("")
    print("Review this generated brief, remove sensitive material, then give it to the next human or model.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
