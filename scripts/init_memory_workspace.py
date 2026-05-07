#!/usr/bin/env python3
"""Initialize a continuity/research memory workspace.

Usage:
    python scripts/init_memory_workspace.py /path/to/project --profile standard
"""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = PACKAGE_ROOT / "templates"
PROFILES_DIR = PACKAGE_ROOT / "profiles"

PROFILE_DEFAULTS = {
    "light": {"capture_trigger": "light"},
    "standard": {"capture_trigger": "standard"},
    "research": {"capture_trigger": "research"},
    "academic": {"capture_trigger": "academic"},
}

DOC_ROLES = {
    "README.md": "Entry point and workspace orientation",
    "CURRENT_STATE.md": "Current confirmed truth",
    "ROADMAP.md": "Planned future work",
    "DECISION_LOG.md": "Decisions and why they were made",
    "RESEARCH_LOG.md": "Experiments, investigations, evidence, observations",
    "HYPOTHESIS_LAB.md": "Unverified hypotheses and raw sparks",
    "HUMAN_BRIEF.md": "Summary for human decisions",
    "RECOVERY_NOTES.md": "Fast resume notes after interruption",
    "LOGBOOK.md": "Compact combined log for light profile history",
    "DOCS_GUIDE.md": "Rules for where to write information",
    "CONTEXT_MANIFEST.md": "Read order, canonical sources, ignore rules",
    "LITERATURE_NOTES.md": "Prior work and its relevance",
    "FIGURES_LOG.md": "Figures and tables linked to data and methods",
    "GLOSSARY.md": "Project-specific terms",
}

READ_ORDER = [
    "RECOVERY_NOTES.md",
    "HUMAN_BRIEF.md",
    "CURRENT_STATE.md",
    "ROADMAP.md",
    "DECISION_LOG.md",
    "RESEARCH_LOG.md",
    "HYPOTHESIS_LAB.md",
    "LOGBOOK.md",
    "LITERATURE_NOTES.md",
    "FIGURES_LOG.md",
    "DOCS_GUIDE.md",
    "GLOSSARY.md",
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


def has_doc(files: list[str], rel_path: str) -> bool:
    return rel_path in files


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


def display_path(rel_path: str, memory_dir: str = "") -> str:
    return f"{memory_dir}/{rel_path}" if memory_dir else rel_path


def doc_ref(rel_path: str, memory_dir: str = "") -> str:
    return f"`{display_path(rel_path, memory_dir)}`"


def numbered(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, 1))


def bullet_docs(items: list[str], memory_dir: str = "") -> str:
    return "\n".join(f"- {doc_ref(item, memory_dir)}" for item in items)


def document_map(files: list[str], memory_dir: str = "") -> str:
    rows = ["| File | Role |", "| --- | --- |"]
    for rel_path in files:
        if rel_path.startswith("."):
            continue
        role = DOC_ROLES.get(rel_path)
        if role:
            rows.append(f"| {doc_ref(rel_path, memory_dir)} | {role} |")
    return "\n".join(rows)


def current_orientation(files: list[str], memory_dir: str = "") -> str:
    ordered = ["CONTEXT_MANIFEST.md", "RECOVERY_NOTES.md", "HUMAN_BRIEF.md", "CURRENT_STATE.md", "LOGBOOK.md"]
    return numbered([doc_ref(item, memory_dir) for item in ordered if has_doc(files, item)])


def resume_steps(files: list[str], memory_dir: str = "") -> str:
    steps = [f"Read the latest entry in {doc_ref('RECOVERY_NOTES.md', memory_dir)}."]
    if has_doc(files, "HUMAN_BRIEF.md"):
        steps.append(f"Read {doc_ref('HUMAN_BRIEF.md', memory_dir)} for orientation.")
    steps.append(f"Check {doc_ref('CURRENT_STATE.md', memory_dir)} before trusting old claims.")
    if has_doc(files, "ROADMAP.md"):
        steps.append(f"Use {doc_ref('ROADMAP.md', memory_dir)} for next planned work.")
    if has_doc(files, "LOGBOOK.md"):
        steps.append(f"Use {doc_ref('LOGBOOK.md', memory_dir)} for decisions, notes, hypotheses, and lightweight history.")
    supporting = [
        item
        for item in ["DECISION_LOG.md", "RESEARCH_LOG.md", "HYPOTHESIS_LAB.md", "LITERATURE_NOTES.md", "FIGURES_LOG.md"]
        if has_doc(files, item)
    ]
    if supporting:
        steps.append(f"Use {format_doc_list([doc_ref(item, memory_dir) for item in supporting])} when you need detail.")
    return numbered(steps)


def read_first(files: list[str], memory_dir: str = "") -> str:
    items = []
    for rel_path in READ_ORDER:
        if has_doc(files, rel_path):
            role = DOC_ROLES.get(rel_path, "memory doc")
            items.append(f"{doc_ref(rel_path, memory_dir)} - {role}")
    return numbered(items)


def canonical_sources(files: list[str], memory_dir: str = "") -> str:
    rows = ["| Question | Trust this first |", "| --- | --- |"]
    rows.append(f"| What is true now? | {doc_ref('CURRENT_STATE.md', memory_dir)} |")
    if has_doc(files, "ROADMAP.md"):
        rows.append(f"| What should happen next? | {doc_ref('ROADMAP.md', memory_dir)} and latest {doc_ref('RECOVERY_NOTES.md', memory_dir)} |")
    else:
        rows.append(f"| What should happen next? | latest {doc_ref('RECOVERY_NOTES.md', memory_dir)} |")
    if has_doc(files, "DECISION_LOG.md"):
        rows.append(f"| Why was this choice made? | {doc_ref('DECISION_LOG.md', memory_dir)} |")
    elif has_doc(files, "LOGBOOK.md"):
        rows.append(f"| Why was this choice made? | {doc_ref('LOGBOOK.md', memory_dir)} |")
    if has_doc(files, "RESEARCH_LOG.md"):
        rows.append(f"| What evidence or experiment supports this? | {doc_ref('RESEARCH_LOG.md', memory_dir)} |")
    elif has_doc(files, "LOGBOOK.md"):
        rows.append(f"| What evidence or observation supports this? | {doc_ref('LOGBOOK.md', memory_dir)} |")
    if has_doc(files, "HYPOTHESIS_LAB.md"):
        rows.append(f"| What is speculative? | {doc_ref('HYPOTHESIS_LAB.md', memory_dir)} |")
    elif has_doc(files, "LOGBOOK.md"):
        rows.append(f"| What is speculative? | {doc_ref('LOGBOOK.md', memory_dir)} |")
    if has_doc(files, "HUMAN_BRIEF.md"):
        rows.append(f"| What should a human read quickly? | {doc_ref('HUMAN_BRIEF.md', memory_dir)} |")
    rows.append(f"| Where should new information be written? | {doc_ref('DOCS_GUIDE.md', memory_dir)} |")
    return "\n".join(rows)


def canonical_locations(files: list[str], memory_dir: str = "") -> str:
    rows = ["| Logical file | Canonical location |", "| --- | --- |"]
    for rel_path in files:
        if rel_path.startswith("."):
            continue
        rows.append(f"| `{rel_path}` | {doc_ref(rel_path, memory_dir)} |")
    return "\n".join(rows)


def conflict_handling(files: list[str], memory_dir: str = "") -> str:
    items = [f"Prefer {doc_ref('CURRENT_STATE.md', memory_dir)} for current truth."]
    if has_doc(files, "DECISION_LOG.md"):
        items.append(f"Prefer the latest relevant dated {doc_ref('DECISION_LOG.md', memory_dir)} entry for rationale.")
    if has_doc(files, "RESEARCH_LOG.md"):
        items.append(f"Prefer the latest relevant dated {doc_ref('RESEARCH_LOG.md', memory_dir)} entry for evidence.")
    if has_doc(files, "LOGBOOK.md"):
        items.append(f"Use the latest relevant {doc_ref('LOGBOOK.md', memory_dir)} entry for lightweight history, decisions, observations, and hypotheses.")
    if has_doc(files, "ROADMAP.md"):
        items.append(f"Treat {doc_ref('ROADMAP.md', memory_dir)} as intent, not proof.")
    if has_doc(files, "HYPOTHESIS_LAB.md"):
        items.append(f"Treat {doc_ref('HYPOTHESIS_LAB.md', memory_dir)} as unverified by default.")
    items.append(f"Treat {doc_ref('RECOVERY_NOTES.md', memory_dir)} as the resume pointer, not the full source of truth.")
    items.append("Report the conflict before merging claims.")
    return numbered(items)


def initial_docs_summary(files: list[str]) -> str:
    docs = [DOC_ROLES[item].lower() for item in files if item in DOC_ROLES and not item.startswith(".")]
    return f"Added canonical docs for {format_doc_list(docs)}."


def initial_next_step(files: list[str], memory_dir: str = "") -> str:
    targets = [doc_ref("README.md", memory_dir), doc_ref("CURRENT_STATE.md", memory_dir)]
    if has_doc(files, "HUMAN_BRIEF.md"):
        targets.append(doc_ref("HUMAN_BRIEF.md", memory_dir))
    elif has_doc(files, "LOGBOOK.md"):
        targets.append(doc_ref("LOGBOOK.md", memory_dir))
    return f"Fill in {format_doc_list(targets)} with project-specific context."


def canonical_docs_to_trust(files: list[str], memory_dir: str = "") -> str:
    preferred = ["CONTEXT_MANIFEST.md", "DOCS_GUIDE.md", "CURRENT_STATE.md", "HUMAN_BRIEF.md", "LOGBOOK.md", "RECOVERY_NOTES.md"]
    docs = [item for item in preferred if has_doc(files, item)]
    return bullet_docs(docs, memory_dir)


def render_template(text: str, project_name: str, today: str, profile: str, files: list[str], memory_dir: str = "") -> str:
    capture_trigger = PROFILE_DEFAULTS[profile]["capture_trigger"]
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{DATE}}": today,
        "{{PROFILE}}": profile,
        "{{CAPTURE_TRIGGER}}": capture_trigger,
        "{{MEMORY_ROOT}}": memory_dir or ".",
        "{{DOCUMENT_MAP}}": document_map(files, memory_dir),
        "{{CURRENT_ORIENTATION}}": current_orientation(files, memory_dir),
        "{{RESUME_STEPS}}": resume_steps(files, memory_dir),
        "{{READ_FIRST}}": read_first(files, memory_dir),
        "{{CANONICAL_SOURCES}}": canonical_sources(files, memory_dir),
        "{{CANONICAL_LOCATIONS}}": canonical_locations(files, memory_dir),
        "{{CONFLICT_HANDLING}}": conflict_handling(files, memory_dir),
        "{{ENTRY_CANONICAL_DOCS}}": canonical_docs_to_trust(files, memory_dir),
        "{{INITIAL_DOCS_SUMMARY}}": initial_docs_summary(files),
        "{{INITIAL_NEXT_STEP}}": initial_next_step(files, memory_dir),
        "{{INITIAL_CANONICAL_DOCS}}": canonical_docs_to_trust(files, memory_dir),
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def format_doc_list(items: list[str]) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"


def recommended_next_targets(files: list[str], memory_dir: str = "") -> str:
    preferred = [display_path("README.md", memory_dir), display_path("CURRENT_STATE.md", memory_dir)]
    if "HUMAN_BRIEF.md" in files:
        preferred.append(display_path("HUMAN_BRIEF.md", memory_dir))
    preferred.append(f"the latest {display_path('RECOVERY_NOTES.md', memory_dir)} checkpoint")
    return format_doc_list(preferred)


def validate_iso_date(value: str) -> str:
    try:
        dt.date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"Invalid --date value: {value!r}. Use YYYY-MM-DD.") from exc
    return value


def template_source(rel_path: str, profile: str) -> Path:
    profile_src = TEMPLATES_DIR / profile / rel_path
    if profile_src.exists():
        return profile_src
    return TEMPLATES_DIR / rel_path


def find_collisions(target_dir: Path, files: list[str]) -> list[str]:
    return [rel_path for rel_path in files if (target_dir / rel_path).exists()]


def copy_file(rel_path: str, target_dir: Path, project_name: str, today: str, profile: str, files: list[str], memory_dir: str, overwrite: bool, dry_run: bool) -> tuple[str, str]:
    src = template_source(rel_path, profile)
    dst = (target_dir / memory_dir / rel_path) if memory_dir else (target_dir / rel_path)
    out_path = display_path(rel_path, memory_dir)
    if not src.exists():
        return out_path, "missing-template"
    existed_before = dst.exists()
    if existed_before and not overwrite:
        return out_path, "skipped-existing"
    if dry_run:
        return out_path, "would-overwrite" if existed_before else "would-write"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() in {".md", ".txt", ""} or src.name.startswith("."):
        text = src.read_text(encoding="utf-8")
        dst.write_text(render_template(text, project_name, today, profile, files, memory_dir), encoding="utf-8")
    else:
        shutil.copy2(src, dst)
    return out_path, "overwritten" if existed_before else "written"


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize continuity memory docs in a project directory.")
    parser.add_argument("target", help="Target project/workspace directory")
    parser.add_argument("--profile", choices=["light", "standard", "research", "academic"], default="standard")
    parser.add_argument("--project-name", help="Project name for template placeholders")
    parser.add_argument("--date", help="Date to use for template placeholders, default: today")
    parser.add_argument("--memory-dir", help="Place memory files in a relative subdirectory, for example: memory")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    target_dir = Path(args.target).expanduser().resolve()
    project_name = args.project_name or target_dir.name
    today = validate_iso_date(args.date) if args.date else dt.date.today().isoformat()
    files = load_profile(args.profile)
    explicit_memory_dir = args.memory_dir is not None
    memory_dir = normalize_memory_dir(args.memory_dir)
    collisions = [] if explicit_memory_dir or args.overwrite else find_collisions(target_dir, files)
    auto_memory_dir = False
    if collisions:
        memory_dir = "memory"
        auto_memory_dir = True

    if not args.dry_run:
        (target_dir / memory_dir).mkdir(parents=True, exist_ok=True) if memory_dir else target_dir.mkdir(parents=True, exist_ok=True)

    print(f"Target: {target_dir}")
    print(f"Profile: {args.profile}")
    print(f"Project name: {project_name}")
    print(f"Date: {today}")
    print(f"Memory directory: {memory_dir or '.'}")
    if auto_memory_dir:
        print(f"Detected existing same-name files; writing memory workspace under `{memory_dir}/`.")
        print("Collisions: " + ", ".join(collisions))
    print("")

    counts: dict[str, int] = {}
    for rel_path in files:
        out_path, status = copy_file(rel_path, target_dir, project_name, today, args.profile, files, memory_dir, args.overwrite, args.dry_run)
        counts[status] = counts.get(status, 0) + 1
        print(f"{status:16} {out_path}")

    print("")
    print("Summary:")
    for status, count in sorted(counts.items()):
        print(f"- {status}: {count}")

    if not args.dry_run:
        print(f"\nNext: fill in {recommended_next_targets(files, memory_dir)}.")
        print(f"If the repo also uses AGENTS.md or CLAUDE.md, point them to {display_path('CONTEXT_MANIFEST.md', memory_dir)} and the canonical docs instead of duplicating memory there.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
