#!/usr/bin/env python3
"""Create a rough handoff brief from continuity memory docs.

This script is intentionally simple. It extracts the most relevant sections and
prints a draft that a human or model should refine.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

from memory_common import MemoryWorkspace, SECRET_RE, markdown_headings, read_text, redact_secrets

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
PROFILES_DIR = PACKAGE_ROOT / "profiles"

PROFILE_CHOICES = ["light", "standard", "research", "academic"]

EXCERPT_ORDER = [
    "HUMAN_BRIEF.md",
    "CURRENT_STATE.md",
    "ROADMAP.md",
    "LOGBOOK.md",
    "LITERATURE_NOTES.md",
    "FIGURES_LOG.md",
]

LATEST_SECTION_PATTERNS = {
    "DECISION_LOG.md": r"^##\s+DEC-",
    "RESEARCH_LOG.md": r"^##\s+RES-",
    "HYPOTHESIS_LAB.md": r"^##\s+HYP-",
}


def load_profile(profile: str) -> list[str]:
    profile_path = PROFILES_DIR / f"{profile}.txt"
    if not profile_path.exists():
        available = ", ".join(sorted(p.stem for p in PROFILES_DIR.glob("*.txt")))
        raise SystemExit(f"Unknown profile: {profile!r}. Available: {available}")
    return [
        line.strip()
        for line in profile_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def latest_markdown_section(text: str, heading_pattern: str | None = None) -> str:
    """Return the first matching level-2 markdown section.

    Newest-first files should put the latest real entry near the top, but many
    templates contain instructional sections first. `heading_pattern` lets us
    skip those and find actual dated or ID-based entries.
    """
    headings = markdown_headings(text)
    candidates = [(start, level, heading) for start, level, heading in headings
                  if level == 2 and (heading_pattern is None or re.search(heading_pattern, heading))]
    if not candidates:
        return text.strip() if not headings and heading_pattern is None else ""
    start, level, _ = candidates[0]
    end = next((pos for pos, depth, _ in headings if pos > start and depth <= level), len(text))
    return text[start:end].strip()


def excerpt(text: str, max_chars: int) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "\n\n...[excerpt truncated]"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")

    parser = argparse.ArgumentParser(description="Generate a rough handoff brief from memory docs.")
    parser.add_argument("target", help="Target project/workspace directory")
    parser.add_argument("--profile", choices=PROFILE_CHOICES, help="Profile to use; defaults to CONTEXT_MANIFEST.md when available")
    parser.add_argument("--memory-dir", help="Memory subdirectory to read; auto-detects memory/ or project-memory/ when omitted")
    parser.add_argument("--max-section-chars", type=int, default=2500)
    parser.add_argument("--no-redact-secrets", action="store_true", help="Do not redact likely secrets from the generated brief")
    parser.add_argument("--fail-on-secret", action="store_true", help="Exit non-zero if likely secrets were found in source docs read for the brief, before excerpting")
    args = parser.parse_args()

    if args.fail_on_secret and args.no_redact_secrets:
        raise SystemExit("--fail-on-secret cannot be combined with --no-redact-secrets.")

    target = Path(args.target).expanduser().resolve()
    if args.max_section_chars <= 0:
        parser.error("--max-section-chars must be positive.")
    try:
        workspace = MemoryWorkspace(target, args.memory_dir)
    except ValueError as exc:
        parser.error(str(exc))
    profile = args.profile or workspace.profile()
    profile_files = set(load_profile(profile))
    project = target.name
    today = dt.date.today().isoformat()
    secret_found = False

    def protect(text: str) -> str:
        nonlocal secret_found
        if SECRET_RE.search(text):
            secret_found = True
        return text if args.no_redact_secrets else redact_secrets(text)

    def read_doc(logical: str) -> str:
        return protect(read_text(workspace.path(logical)))

    def safe_print(text: str = "") -> None:
        print(protect(text))

    safe_print(f"# Handoff Brief - {project} - {today}")
    safe_print("")
    safe_print("This is a generated draft. Review before sending to another human or model.")
    safe_print("")

    recovery = read_doc("RECOVERY_NOTES.md")
    safe_print("## Latest recovery checkpoint")
    safe_print("")
    safe_print(excerpt(latest_markdown_section(recovery, r"^##\s+\d{4}-\d{2}-\d{2}"), args.max_section_chars) if recovery else "Missing `RECOVERY_NOTES.md`.")
    safe_print("")

    for rel in [item for item in EXCERPT_ORDER if item in profile_files]:
        text = read_doc(rel)
        safe_print(f"## Excerpt: {rel}")
        safe_print("")
        safe_print(excerpt(text, args.max_section_chars) if text else f"Missing `{rel}`.")
        safe_print("")

    for rel in [item for item in LATEST_SECTION_PATTERNS if item in profile_files]:
        text = read_doc(rel)
        safe_print(f"## Latest relevant section: {rel}")
        safe_print("")
        pattern = LATEST_SECTION_PATTERNS.get(rel)
        section = latest_markdown_section(text, pattern)
        safe_print(excerpt(section, args.max_section_chars) if section else ("No matching entries found." if text else f"Missing `{rel}`."))
        safe_print("")

    manifest = read_doc("CONTEXT_MANIFEST.md")
    safe_print("## Context manifest excerpt")
    safe_print("")
    safe_print(excerpt(manifest, args.max_section_chars) if manifest else "Missing `CONTEXT_MANIFEST.md`.")
    safe_print("")
    safe_print("## Next recommended action")
    safe_print("")
    safe_print("Review this generated brief, remove sensitive material, then give it to the next human or model.")

    if args.fail_on_secret and secret_found:
        print("Likely secret detected in handoff brief.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
