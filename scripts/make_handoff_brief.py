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

from memory_common import SECRET_RE, redact_secrets

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
PROFILES_DIR = PACKAGE_ROOT / "profiles"
MEMORY_DIR_CANDIDATES = ["memory", "project-memory"]

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


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def normalize_memory_dir(value: str | None) -> str:
    if value is None:
        return ""
    value = value.strip().replace("\\", "/")
    if value in {"", ".", "./"}:
        return ""
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise SystemExit("--memory-dir must be a relative directory inside the target workspace.")
    return path.as_posix().strip("/")


def detect_memory_dir(target: Path, memory_dir: str | None = None) -> str:
    if memory_dir is not None:
        return normalize_memory_dir(memory_dir)
    if (target / "CONTEXT_MANIFEST.md").exists():
        return ""
    for candidate in MEMORY_DIR_CANDIDATES:
        if (target / candidate / "CONTEXT_MANIFEST.md").exists():
            return candidate
    return ""


def doc_path(target: Path, rel_path: str, memory_dir: str = "") -> Path:
    return (target / memory_dir / rel_path) if memory_dir else (target / rel_path)


def strip_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def detect_profile(target: Path, memory_dir: str = "") -> str:
    manifest = read_text(doc_path(target, "CONTEXT_MANIFEST.md", memory_dir))
    match = re.search(r"(?im)^Profile:\s*(light|standard|research|academic)\s*$", manifest)
    return match.group(1) if match else "standard"


def latest_markdown_section(text: str, heading_pattern: str | None = None) -> str:
    """Return the first matching level-2 markdown section.

    Newest-first files should put the latest real entry near the top, but many
    templates contain instructional sections first. `heading_pattern` lets us
    skip those and find actual dated or ID-based entries.
    """
    text = strip_fenced_code(text)
    if not text.strip():
        return ""

    heading_re = re.compile(r"^##\s+.+$", flags=re.MULTILINE)
    headings = list(heading_re.finditer(text))
    if not headings:
        return text.strip()

    chosen = headings[0]
    if heading_pattern:
        wanted = re.compile(heading_pattern)
        chosen = None
        for heading in headings:
            if wanted.search(heading.group(0)):
                chosen = heading
                break
        if chosen is None:
            return ""

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
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")

    parser = argparse.ArgumentParser(description="Generate a rough handoff brief from memory docs.")
    parser.add_argument("target", help="Target project/workspace directory")
    parser.add_argument("--profile", choices=PROFILE_CHOICES, help="Profile to use; defaults to CONTEXT_MANIFEST.md when available")
    parser.add_argument("--memory-dir", help="Memory subdirectory to read; auto-detects memory/ or project-memory/ when omitted")
    parser.add_argument("--max-section-chars", type=int, default=2500)
    parser.add_argument("--no-redact-secrets", action="store_true", help="Do not redact likely secrets from the generated brief")
    parser.add_argument("--fail-on-secret", action="store_true", help="Exit non-zero if likely secrets were found in the generated brief")
    args = parser.parse_args()

    if args.fail_on_secret and args.no_redact_secrets:
        raise SystemExit("--fail-on-secret cannot be combined with --no-redact-secrets.")

    target = Path(args.target).expanduser().resolve()
    memory_dir = detect_memory_dir(target, args.memory_dir)
    profile = args.profile or detect_profile(target, memory_dir)
    profile_files = set(load_profile(profile))
    project = target.name
    today = dt.date.today().isoformat()
    secret_found = False

    def safe_print(text: str = "") -> None:
        nonlocal secret_found
        if SECRET_RE.search(text):
            secret_found = True
            if not args.no_redact_secrets:
                text = redact_secrets(text)
        print(text)

    safe_print(f"# Handoff Brief - {project} - {today}")
    safe_print("")
    safe_print("This is a generated draft. Review before sending to another human or model.")
    safe_print("")

    recovery = read_text(doc_path(target, "RECOVERY_NOTES.md", memory_dir))
    safe_print("## Latest recovery checkpoint")
    safe_print("")
    safe_print(excerpt(latest_markdown_section(recovery, r"^##\s+\d{4}-\d{2}-\d{2}"), args.max_section_chars) if recovery else "Missing `RECOVERY_NOTES.md`.")
    safe_print("")

    for rel in [item for item in EXCERPT_ORDER if item in profile_files]:
        text = read_text(doc_path(target, rel, memory_dir))
        safe_print(f"## Excerpt: {rel}")
        safe_print("")
        safe_print(excerpt(text, args.max_section_chars) if text else f"Missing `{rel}`.")
        safe_print("")

    for rel in [item for item in LATEST_SECTION_PATTERNS if item in profile_files]:
        text = read_text(doc_path(target, rel, memory_dir))
        safe_print(f"## Latest relevant section: {rel}")
        safe_print("")
        pattern = LATEST_SECTION_PATTERNS.get(rel)
        section = latest_markdown_section(text, pattern)
        safe_print(excerpt(section, args.max_section_chars) if section else ("No matching entries found." if text else f"Missing `{rel}`."))
        safe_print("")

    manifest = read_text(doc_path(target, "CONTEXT_MANIFEST.md", memory_dir))
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
