#!/usr/bin/env python3
"""Audit a continuity/research memory workspace for missing files and common drift."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
PROFILES_DIR = PACKAGE_ROOT / "profiles"

SECRET_RE = re.compile(
    r'''(?i)(api[_-]?key|secret|token|password|passwd|credential)
    \s*[:=]\s*['"]?[A-Za-z0-9_./+=:@-]{8,}''',
    re.VERBOSE,
)
SPECULATION_RE = re.compile(r"(?i)\b(might|maybe|could be|possibly|hypothesis|untested|speculative)\b|かもしれ|仮説|未検証")
YES_RE = re.compile(r"(?im)^-\s*human_brief_update\s*:\s*yes\s*$")
DATE_FIELD_RE = re.compile(r"(?im)^-\s*date\s*:\s*(\d{4}-\d{2}-\d{2})\s*$")
LAST_UPDATED_RE = re.compile(r"(?im)^Last updated:\s*(\d{4}-\d{2}-\d{2})\s*$")
LAST_SYNCED_FIELDS = [
    "`CURRENT_STATE.md`:",
    "`ROADMAP.md`:",
    "latest `DECISION_LOG.md`:",
    "latest `RESEARCH_LOG.md`:",
    "latest `RECOVERY_NOTES.md`:",
]
EXPECTED_CURRENT_SECTIONS = [
    "## Stable facts",
    "## Active operating decisions",
    "## Current context",
]
EXPECTED_HYP_SECTIONS = [
    "## Raw sparks",
    "## Working hypotheses",
]


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
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def line_hits(text: str, pattern: re.Pattern[str], max_hits: int = 5) -> list[str]:
    hits: list[str] = []
    for i, line in enumerate(text.splitlines(), 1):
        if pattern.search(line):
            hits.append(f"line {i}: {line[:160]}")
            if len(hits) >= max_hits:
                break
    return hits


def parse_iso_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def extract_last_updated(text: str) -> date | None:
    match = LAST_UPDATED_RE.search(text)
    return parse_iso_date(match.group(1)) if match else None


def extract_trigger_dates(text: str) -> list[date]:
    dates: list[date] = []
    current_date: date | None = None
    for line in text.splitlines():
        date_match = DATE_FIELD_RE.match(line)
        if date_match:
            current_date = parse_iso_date(date_match.group(1))
            continue
        if YES_RE.match(line) and current_date is not None:
            dates.append(current_date)
    return dates


def audit(target: Path, profile: str) -> dict[str, object]:
    required = load_profile(profile)
    result: dict[str, object] = {
        "target": str(target),
        "profile": profile,
        "missing": [],
        "warnings": [],
        "ok": [],
    }
    warnings: list[dict[str, object]] = result["warnings"]  # type: ignore[assignment]
    ok: list[str] = result["ok"]  # type: ignore[assignment]

    for rel in required:
        path = target / rel
        if not path.exists():
            result["missing"].append(rel)  # type: ignore[index]
        else:
            ok.append(rel)

    readme = target / "README.md"
    if readme.exists():
        text = read_text(readme)
        if len(text) > 20000:
            warnings.append({"file": "README.md", "issue": "README is large; consider moving current truth/history/plans into canonical docs."})
        overloaded_terms = ["Decision Log", "Research Log", "Hypothesis", "Roadmap", "Current State"]
        if sum(term.lower() in text.lower() for term in overloaded_terms) >= 4 and len(text) > 8000:
            warnings.append({"file": "README.md", "issue": "README may be carrying multiple canonical roles."})

    current_state = target / "CURRENT_STATE.md"
    if current_state.exists():
        text = read_text(current_state)
        hits = line_hits(text, SPECULATION_RE)
        if hits:
            warnings.append({
                "file": "CURRENT_STATE.md",
                "issue": "Possible speculative language in current truth file. Verify these are confirmed.",
                "examples": hits,
            })
        for section in EXPECTED_CURRENT_SECTIONS:
            if section not in text:
                warnings.append({"file": "CURRENT_STATE.md", "issue": f"Missing expected section: {section}"})
        for field in ["Source", "Revisit when"]:
            if field not in text:
                warnings.append({"file": "CURRENT_STATE.md", "issue": f"Current state may be missing `{field}` fields."})

    hypothesis = target / "HYPOTHESIS_LAB.md"
    if hypothesis.exists():
        text = read_text(hypothesis)
        for section in EXPECTED_HYP_SECTIONS:
            if section not in text:
                warnings.append({"file": "HYPOTHESIS_LAB.md", "issue": f"Missing expected section: {section}"})
        hyp_count = len(re.findall(r"^##\s+HYP-", text, flags=re.MULTILINE))
        status_count = len(re.findall(r"status\s*:", text, flags=re.IGNORECASE))
        if hyp_count and hyp_count > status_count:
            warnings.append({"file": "HYPOTHESIS_LAB.md", "issue": "Some working hypotheses may be missing status fields."})

    research = target / "RESEARCH_LOG.md"
    if research.exists():
        text = read_text(research)
        for field in ["method", "result", "interpretation", "confidence", "limitations"]:
            if field not in text.lower():
                warnings.append({"file": "RESEARCH_LOG.md", "issue": f"Research log may be missing `{field}` fields."})

    recovery = target / "RECOVERY_NOTES.md"
    if recovery.exists():
        text = read_text(recovery)
        if len(text) > 25000:
            warnings.append({"file": "RECOVERY_NOTES.md", "issue": "Recovery notes are large; keep only compact checkpoints and move detail to canonical docs."})
        if "Next recommended step" not in text and "Next Recommended Step" not in text:
            warnings.append({"file": "RECOVERY_NOTES.md", "issue": "No obvious next recommended step found."})

    human_brief = target / "HUMAN_BRIEF.md"
    if human_brief.exists():
        hb_text = read_text(human_brief)
        hb_updated = extract_last_updated(hb_text)
        if hb_updated is None:
            warnings.append({"file": "HUMAN_BRIEF.md", "issue": "Missing or invalid `Last updated:` field."})
        for marker in LAST_SYNCED_FIELDS:
            if marker not in hb_text:
                warnings.append({"file": "HUMAN_BRIEF.md", "issue": f"Missing sync marker: {marker}"})
        if "## Tracked threads" not in hb_text and "## Active threads" not in hb_text:
            warnings.append({"file": "HUMAN_BRIEF.md", "issue": "Missing `Tracked threads` or `Active threads` section."})
        trigger_dates: list[date] = []
        for rel in ["DECISION_LOG.md", "RESEARCH_LOG.md"]:
            path = target / rel
            if path.exists():
                trigger_dates.extend(extract_trigger_dates(read_text(path)))
        if trigger_dates and hb_updated is not None:
            latest_trigger = max(trigger_dates)
            if latest_trigger > hb_updated:
                warnings.append({
                    "file": "HUMAN_BRIEF.md",
                    "issue": "HUMAN_BRIEF.md may be stale relative to entries marked `human_brief_update: yes`.",
                    "latest_trigger": latest_trigger.isoformat(),
                    "last_updated": hb_updated.isoformat(),
                })

    contextignore = target / ".contextignore"
    if not contextignore.exists():
        warnings.append({"file": ".contextignore", "issue": "Missing context ignore file; generated logs/caches/private files may be read accidentally."})
    else:
        text = read_text(contextignore)
        for pattern in ["private/", ".cache/", "logs/", "*.log"]:
            if pattern not in text:
                warnings.append({"file": ".contextignore", "issue": f"Missing recommended ignore pattern: {pattern}"})

    for rel in ["README.md", "CURRENT_STATE.md", "ROADMAP.md", "DECISION_LOG.md", "RESEARCH_LOG.md", "HYPOTHESIS_LAB.md", "HUMAN_BRIEF.md", "RECOVERY_NOTES.md"]:
        path = target / rel
        if path.exists():
            hits = line_hits(read_text(path), SECRET_RE)
            if hits:
                warnings.append({"file": rel, "issue": "Possible secret/credential in canonical docs.", "examples": hits})

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit continuity memory workspace docs.")
    parser.add_argument("target", help="Target project/workspace directory")
    parser.add_argument("--profile", choices=["light", "standard", "research"], default="research")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    result = audit(target, args.profile)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    print(f"Audit target: {result['target']}")
    print(f"Profile: {result['profile']}")
    print("")
    missing = result["missing"]
    if missing:
        print("Missing files:")
        for item in missing:  # type: ignore[union-attr]
            print(f"- {item}")
    else:
        print("Missing files: none")

    warnings = result["warnings"]
    print("")
    if warnings:
        print("Warnings:")
        for warning in warnings:  # type: ignore[union-attr]
            print(f"- {warning['file']}: {warning['issue']}")
            if "latest_trigger" in warning:
                print(f"  - latest trigger: {warning['latest_trigger']}")
                print(f"  - last updated: {warning['last_updated']}")
            for ex in warning.get("examples", []):
                print(f"  - {ex}")
    else:
        print("Warnings: none")

    print("")
    print(f"Existing expected files: {len(result['ok'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
