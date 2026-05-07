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
MEMORY_DIR_CANDIDATES = ["memory", "project-memory"]

SECRET_RE = re.compile(
    r'''(?ix)(
        (api[_-]?key|secret|token|password|passwd|credential)\s*[:=]\s*['"]?[A-Za-z0-9_./+=:@-]{8,}
        | AKIA[0-9A-Z]{16}
        | github_pat_[A-Za-z0-9_]{20,}
        | gh[pousr]_[A-Za-z0-9_]{20,}
        | -----BEGIN\s+(RSA\s+|DSA\s+|EC\s+|OPENSSH\s+)?PRIVATE\s+KEY-----
    )''',
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
EXPECTED_ROADMAP_SECTIONS = [
    "## Current objective",
    "## Now",
    "## Blockers",
]
EXPECTED_DECISION_SECTIONS = [
    "## Entry template",
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


def display_path(rel_path: str, memory_dir: str = "") -> str:
    return f"{memory_dir}/{rel_path}" if memory_dir else rel_path


def detect_profile(target: Path, memory_dir: str = "") -> str:
    manifest = read_text(doc_path(target, "CONTEXT_MANIFEST.md", memory_dir))
    match = re.search(r"(?im)^Profile:\s*(light|standard|research|academic)\s*$", manifest)
    return match.group(1) if match else "standard"


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


def audit(target: Path, profile: str, memory_dir: str = "") -> dict[str, object]:
    required = load_profile(profile)
    result: dict[str, object] = {
        "target": str(target),
        "profile": profile,
        "memory_dir": memory_dir or ".",
        "missing": [],
        "warnings": [],
        "ok": [],
    }
    warnings: list[dict[str, object]] = result["warnings"]  # type: ignore[assignment]
    ok: list[str] = result["ok"]  # type: ignore[assignment]

    for rel in required:
        path = doc_path(target, rel, memory_dir)
        if not path.exists():
            result["missing"].append(display_path(rel, memory_dir))  # type: ignore[index]
        else:
            ok.append(display_path(rel, memory_dir))

    readme = doc_path(target, "README.md", memory_dir)
    if readme.exists():
        text = read_text(readme)
        if len(text) > 20000:
            warnings.append({"file": display_path("README.md", memory_dir), "issue": "README is large; consider moving current truth/history/plans into canonical docs."})
        overloaded_terms = ["Decision Log", "Research Log", "Hypothesis", "Roadmap", "Current State"]
        if sum(term.lower() in text.lower() for term in overloaded_terms) >= 4 and len(text) > 8000:
            warnings.append({"file": display_path("README.md", memory_dir), "issue": "README may be carrying multiple canonical roles."})

    roadmap = doc_path(target, "ROADMAP.md", memory_dir)
    if roadmap.exists():
        text = read_text(roadmap)
        for section in EXPECTED_ROADMAP_SECTIONS:
            if section not in text:
                warnings.append({"file": display_path("ROADMAP.md", memory_dir), "issue": f"Missing expected section: {section}"})

    decision_log = doc_path(target, "DECISION_LOG.md", memory_dir)
    if decision_log.exists():
        text = read_text(decision_log)
        for section in EXPECTED_DECISION_SECTIONS:
            if section not in text:
                warnings.append({"file": display_path("DECISION_LOG.md", memory_dir), "issue": f"Missing expected section: {section}"})

    current_state = doc_path(target, "CURRENT_STATE.md", memory_dir)
    if current_state.exists():
        text = read_text(current_state)
        hits = line_hits(text, SPECULATION_RE)
        if hits:
            warnings.append({
                "file": display_path("CURRENT_STATE.md", memory_dir),
                "issue": "Possible speculative language in current truth file. Verify these are confirmed.",
                "examples": hits,
            })
        for section in EXPECTED_CURRENT_SECTIONS:
            if section not in text:
                warnings.append({"file": display_path("CURRENT_STATE.md", memory_dir), "issue": f"Missing expected section: {section}"})
        for field in ["Source", "Revisit when"]:
            if field not in text:
                warnings.append({"file": display_path("CURRENT_STATE.md", memory_dir), "issue": f"Current state may be missing `{field}` fields."})

    hypothesis = doc_path(target, "HYPOTHESIS_LAB.md", memory_dir)
    if hypothesis.exists():
        text = read_text(hypothesis)
        for section in EXPECTED_HYP_SECTIONS:
            if section not in text:
                warnings.append({"file": display_path("HYPOTHESIS_LAB.md", memory_dir), "issue": f"Missing expected section: {section}"})
        hyp_count = len(re.findall(r"^##\s+HYP-", text, flags=re.MULTILINE))
        status_count = len(re.findall(r"status\s*:", text, flags=re.IGNORECASE))
        if hyp_count and hyp_count > status_count:
            warnings.append({"file": display_path("HYPOTHESIS_LAB.md", memory_dir), "issue": "Some working hypotheses may be missing status fields."})

    research = doc_path(target, "RESEARCH_LOG.md", memory_dir)
    if research.exists():
        text = read_text(research)
        for field in ["method", "result", "interpretation", "confidence", "limitations"]:
            if field not in text.lower():
                warnings.append({"file": display_path("RESEARCH_LOG.md", memory_dir), "issue": f"Research log may be missing `{field}` fields."})

    recovery = doc_path(target, "RECOVERY_NOTES.md", memory_dir)
    if recovery.exists():
        text = read_text(recovery)
        if len(text) > 25000:
            warnings.append({"file": display_path("RECOVERY_NOTES.md", memory_dir), "issue": "Recovery notes are large; keep only compact checkpoints and move detail to canonical docs."})
        if "Next recommended step" not in text and "Next Recommended Step" not in text:
            warnings.append({"file": display_path("RECOVERY_NOTES.md", memory_dir), "issue": "No obvious next recommended step found."})

    human_brief = doc_path(target, "HUMAN_BRIEF.md", memory_dir)
    if human_brief.exists():
        hb_text = read_text(human_brief)
        hb_updated = extract_last_updated(hb_text)
        if hb_updated is None:
            warnings.append({"file": display_path("HUMAN_BRIEF.md", memory_dir), "issue": "Missing or invalid `Last updated:` field."})
        for marker in LAST_SYNCED_FIELDS:
            if marker not in hb_text:
                warnings.append({"file": display_path("HUMAN_BRIEF.md", memory_dir), "issue": f"Missing sync marker: {marker}"})
        if "## Tracked threads" not in hb_text and "## Active threads" not in hb_text:
            warnings.append({"file": display_path("HUMAN_BRIEF.md", memory_dir), "issue": "Missing `Tracked threads` or `Active threads` section."})
        trigger_dates: list[date] = []
        for rel in ["DECISION_LOG.md", "RESEARCH_LOG.md"]:
            path = doc_path(target, rel, memory_dir)
            if path.exists():
                trigger_dates.extend(extract_trigger_dates(read_text(path)))
        if trigger_dates and hb_updated is not None:
            latest_trigger = max(trigger_dates)
            if latest_trigger > hb_updated:
                warnings.append({
                    "file": display_path("HUMAN_BRIEF.md", memory_dir),
                    "issue": "HUMAN_BRIEF.md may be stale relative to entries marked `human_brief_update: yes`.",
                    "latest_trigger": latest_trigger.isoformat(),
                    "last_updated": hb_updated.isoformat(),
                })

    contextignore = doc_path(target, ".contextignore", memory_dir)
    if not contextignore.exists():
        warnings.append({"file": display_path(".contextignore", memory_dir), "issue": "Missing context ignore file; generated logs/caches/private files may be read accidentally."})
    else:
        text = read_text(contextignore)
        for pattern in ["private/", ".cache/", "logs/", "*.log"]:
            if pattern not in text:
                warnings.append({"file": display_path(".contextignore", memory_dir), "issue": f"Missing recommended ignore pattern: {pattern}"})

    for rel in ["README.md", "CURRENT_STATE.md", "ROADMAP.md", "DECISION_LOG.md", "RESEARCH_LOG.md", "HYPOTHESIS_LAB.md", "HUMAN_BRIEF.md", "RECOVERY_NOTES.md"]:
        path = doc_path(target, rel, memory_dir)
        if path.exists():
            hits = line_hits(read_text(path), SECRET_RE)
            if hits:
                warnings.append({"file": display_path(rel, memory_dir), "issue": "Possible secret/credential in canonical docs.", "examples": hits})

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit continuity memory workspace docs.")
    parser.add_argument("target", help="Target project/workspace directory")
    parser.add_argument("--profile", choices=["light", "standard", "research", "academic"], help="Profile to audit; defaults to CONTEXT_MANIFEST.md when available")
    parser.add_argument("--memory-dir", help="Memory subdirectory to audit; auto-detects memory/ or project-memory/ when omitted")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when missing files or warnings are found")
    args = parser.parse_args()

    target = Path(args.target).expanduser().resolve()
    memory_dir = detect_memory_dir(target, args.memory_dir)
    profile = args.profile or detect_profile(target, memory_dir)
    result = audit(target, profile, memory_dir)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if args.strict and (result["missing"] or result["warnings"]) else 0

    print(f"Audit target: {result['target']}")
    print(f"Profile: {result['profile']}")
    print(f"Memory directory: {result['memory_dir']}")
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
    return 1 if args.strict and (missing or warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
