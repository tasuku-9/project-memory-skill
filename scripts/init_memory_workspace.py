#!/usr/bin/env python3
"""Initialize a continuity/research memory workspace.

Usage:
    python scripts/init_memory_workspace.py /path/to/project --profile research
"""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = PACKAGE_ROOT / "templates"
PROFILES_DIR = PACKAGE_ROOT / "profiles"


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


def render_template(text: str, project_name: str, today: str) -> str:
    return text.replace("{{PROJECT_NAME}}", project_name).replace("{{DATE}}", today)


def copy_file(rel_path: str, target_dir: Path, project_name: str, today: str, overwrite: bool, dry_run: bool) -> tuple[str, str]:
    src = TEMPLATES_DIR / rel_path
    dst = target_dir / rel_path
    if not src.exists():
        return rel_path, "missing-template"
    existed_before = dst.exists()
    if existed_before and not overwrite:
        return rel_path, "skipped-existing"
    if dry_run:
        return rel_path, "would-overwrite" if existed_before else "would-write"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() in {".md", ".txt", ""} or src.name.startswith("."):
        text = src.read_text(encoding="utf-8")
        dst.write_text(render_template(text, project_name, today), encoding="utf-8")
    else:
        shutil.copy2(src, dst)
    return rel_path, "overwritten" if existed_before else "written"


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize continuity memory docs in a project directory.")
    parser.add_argument("target", help="Target project/workspace directory")
    parser.add_argument("--profile", choices=["light", "standard", "research"], default="research")
    parser.add_argument("--project-name", help="Project name for template placeholders")
    parser.add_argument("--date", help="Date to use for template placeholders, default: today")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    target_dir = Path(args.target).expanduser().resolve()
    project_name = args.project_name or target_dir.name
    today = args.date or dt.date.today().isoformat()
    files = load_profile(args.profile)

    if not args.dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    print(f"Target: {target_dir}")
    print(f"Profile: {args.profile}")
    print(f"Project name: {project_name}")
    print(f"Date: {today}")
    print("")

    counts: dict[str, int] = {}
    for rel_path in files:
        _, status = copy_file(rel_path, target_dir, project_name, today, args.overwrite, args.dry_run)
        counts[status] = counts.get(status, 0) + 1
        print(f"{status:16} {rel_path}")

    print("")
    print("Summary:")
    for status, count in sorted(counts.items()):
        print(f"- {status}: {count}")

    if not args.dry_run:
        print("\nNext: fill in README.md, CURRENT_STATE.md, HUMAN_BRIEF.md, and the latest RECOVERY_NOTES.md checkpoint.")
        print("If the repo also uses AGENTS.md or CLAUDE.md, point them to CONTEXT_MANIFEST.md and the canonical docs instead of duplicating memory there.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
