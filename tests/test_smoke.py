from __future__ import annotations

import shutil
import subprocess
import sys
import unittest
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
PROFILES_DIR = ROOT / "profiles"
TEMP_ROOT = ROOT / ".tmp_test_runs"


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def load_profile(profile: str) -> list[str]:
    profile_path = PROFILES_DIR / f"{profile}.txt"
    return [
        line.strip()
        for line in profile_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def repo_files() -> list[str]:
    ignored_parts = {".git", "__pycache__", ".pytest_cache", ".tmp_test_runs"}
    files: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in ignored_parts for part in rel.parts):
            continue
        files.append(rel.as_posix())
    return sorted(files)


class SmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        TEMP_ROOT.mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls) -> None:
        if TEMP_ROOT.exists():
            shutil.rmtree(TEMP_ROOT, ignore_errors=True)

    def make_workspace(self, name: str) -> Path:
        workspace = TEMP_ROOT / name
        if workspace.exists():
            shutil.rmtree(workspace, ignore_errors=True)
        workspace.mkdir(parents=True, exist_ok=True)
        return workspace

    def test_manifest_matches_repository_files(self) -> None:
        expected = [
            line.strip()
            for line in (ROOT / "manifest.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(expected, repo_files())

    def test_profiles_only_reference_existing_templates(self) -> None:
        for profile_path in sorted(PROFILES_DIR.glob("*.txt")):
            with self.subTest(profile=profile_path.stem):
                for rel_path in load_profile(profile_path.stem):
                    self.assertTrue((ROOT / "templates" / rel_path).exists(), rel_path)

    def test_init_and_audit_succeed_for_every_profile(self) -> None:
        for profile_path in sorted(PROFILES_DIR.glob("*.txt")):
            profile = profile_path.stem
            with self.subTest(profile=profile):
                workspace = self.make_workspace(f"{profile}-workspace")
                init_result = run_script(
                    str(SCRIPTS_DIR / "init_memory_workspace.py"),
                    str(workspace),
                    "--profile",
                    profile,
                )
                expected_files = sorted(load_profile(profile))
                actual_files = sorted(
                    path.relative_to(workspace).as_posix()
                    for path in workspace.rglob("*")
                    if path.is_file()
                )
                self.assertEqual(expected_files, actual_files)
                self.assertIn(f"Profile: {profile}", init_result.stdout)
                if profile == "light":
                    self.assertNotIn("HUMAN_BRIEF.md", init_result.stdout)
                else:
                    self.assertIn("HUMAN_BRIEF.md", init_result.stdout)

                audit_result = run_script(
                    str(SCRIPTS_DIR / "audit_memory_workspace.py"),
                    str(workspace),
                    "--profile",
                    profile,
                )
                self.assertIn("Missing files: none", audit_result.stdout)
                self.assertIn("Warnings: none", audit_result.stdout)

    def test_manifest_profile_matches_selected_profile(self) -> None:
        for profile_path in sorted(PROFILES_DIR.glob("*.txt")):
            profile = profile_path.stem
            with self.subTest(profile=profile):
                workspace = self.make_workspace(f"{profile}-manifest-workspace")
                run_script(
                    str(SCRIPTS_DIR / "init_memory_workspace.py"),
                    str(workspace),
                    "--profile",
                    profile,
                )
                manifest = (workspace / "CONTEXT_MANIFEST.md").read_text(encoding="utf-8")
                self.assertIn(f"Profile: {profile}", manifest)
                self.assertIn(f"Capture trigger strength: {profile}", manifest)

    def test_audit_defaults_to_manifest_profile(self) -> None:
        workspace = self.make_workspace("audit-manifest-profile-workspace")
        run_script(
            str(SCRIPTS_DIR / "init_memory_workspace.py"),
            str(workspace),
            "--profile",
            "academic",
        )
        result = run_script(str(SCRIPTS_DIR / "audit_memory_workspace.py"), str(workspace))
        self.assertIn("Profile: academic", result.stdout)
        self.assertIn("Missing files: none", result.stdout)

    def test_default_profile_is_standard(self) -> None:
        workspace = self.make_workspace("default-profile-workspace")
        result = run_script(str(SCRIPTS_DIR / "init_memory_workspace.py"), str(workspace))
        self.assertIn("Profile: standard", result.stdout)
        manifest = (workspace / "CONTEXT_MANIFEST.md").read_text(encoding="utf-8")
        self.assertIn("Profile: standard", manifest)

    def test_init_rejects_invalid_date(self) -> None:
        workspace = self.make_workspace("invalid-date-workspace")
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "init_memory_workspace.py"),
                str(workspace),
                "--date",
                "not-a-date",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Invalid --date value", result.stderr + result.stdout)

    def test_light_profile_docs_do_not_reference_missing_memory_files(self) -> None:
        workspace = self.make_workspace("light-reference-workspace")
        run_script(
            str(SCRIPTS_DIR / "init_memory_workspace.py"),
            str(workspace),
            "--profile",
            "light",
        )
        existing = {path.name for path in workspace.iterdir() if path.is_file()}
        optional_tool_files = {"AGENTS.md", "CLAUDE.md"}
        for path in sorted(workspace.glob("*.md")):
            refs = set(re.findall(r"`([^`]+\.md)`", path.read_text(encoding="utf-8")))
            missing = sorted(ref for ref in refs if ref not in existing and ref not in optional_tool_files)
            self.assertEqual([], missing, f"{path.name} references missing memory files")

    def test_init_auto_routes_to_memory_dir_on_collision(self) -> None:
        workspace = self.make_workspace("collision-auto-memory-workspace")
        (workspace / "README.md").write_text("# Existing README\n", encoding="utf-8")
        (workspace / "ROADMAP.md").write_text("# Existing Roadmap\n", encoding="utf-8")
        init_result = run_script(
            str(SCRIPTS_DIR / "init_memory_workspace.py"),
            str(workspace),
            "--profile",
            "standard",
        )
        self.assertIn("Memory directory: memory", init_result.stdout)
        self.assertTrue((workspace / "memory" / "CONTEXT_MANIFEST.md").exists())
        manifest = (workspace / "memory" / "CONTEXT_MANIFEST.md").read_text(encoding="utf-8")
        self.assertIn("Memory root: `memory`", manifest)
        self.assertIn("`memory/CURRENT_STATE.md`", manifest)
        audit_result = run_script(
            str(SCRIPTS_DIR / "audit_memory_workspace.py"),
            str(workspace),
            "--profile",
            "standard",
        )
        self.assertIn("Memory directory: memory", audit_result.stdout)
        self.assertIn("Missing files: none", audit_result.stdout)
        self.assertIn("Warnings: none", audit_result.stdout)

    def test_audit_warns_on_explicit_root_collision(self) -> None:
        workspace = self.make_workspace("collision-explicit-root-workspace")
        (workspace / "README.md").write_text("# Existing README\n", encoding="utf-8")
        (workspace / "ROADMAP.md").write_text("# Existing Roadmap\n", encoding="utf-8")
        run_script(
            str(SCRIPTS_DIR / "init_memory_workspace.py"),
            str(workspace),
            "--profile",
            "standard",
            "--memory-dir",
            ".",
        )
        audit_result = run_script(
            str(SCRIPTS_DIR / "audit_memory_workspace.py"),
            str(workspace),
            "--profile",
            "standard",
            "--memory-dir",
            ".",
        )
        self.assertIn("ROADMAP.md: Missing expected section", audit_result.stdout)

    def test_strict_audit_returns_nonzero_on_missing(self) -> None:
        workspace = self.make_workspace("strict-missing-workspace")
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "audit_memory_workspace.py"),
                str(workspace),
                "--profile",
                "research",
                "--strict",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Missing files:", result.stdout)

    def test_handoff_generation_runs_on_research_workspace(self) -> None:
        workspace = self.make_workspace("handoff-workspace")
        run_script(
            str(SCRIPTS_DIR / "init_memory_workspace.py"),
            str(workspace),
            "--profile",
            "research",
        )
        result = run_script(
            str(SCRIPTS_DIR / "make_handoff_brief.py"),
            str(workspace),
            "--max-section-chars",
            "400",
        )
        self.assertIn("# Handoff Brief", result.stdout)
        self.assertIn("## Latest recovery checkpoint", result.stdout)
        self.assertIn("## Excerpt: HUMAN_BRIEF.md", result.stdout)
        self.assertNotIn("DEC-YYYY-MM-DD", result.stdout)
        self.assertNotIn("RES-YYYY-MM-DD", result.stdout)
        self.assertNotIn("HYP-YYYY-MM-DD", result.stdout)

    def test_academic_handoff_includes_literature_and_figures(self) -> None:
        workspace = self.make_workspace("academic-handoff-workspace")
        run_script(
            str(SCRIPTS_DIR / "init_memory_workspace.py"),
            str(workspace),
            "--profile",
            "academic",
        )
        result = run_script(
            str(SCRIPTS_DIR / "make_handoff_brief.py"),
            str(workspace),
            "--max-section-chars",
            "400",
        )
        self.assertIn("## Excerpt: LITERATURE_NOTES.md", result.stdout)
        self.assertIn("## Excerpt: FIGURES_LOG.md", result.stdout)

    def test_light_handoff_uses_logbook_without_missing_heavy_docs(self) -> None:
        workspace = self.make_workspace("light-handoff-workspace")
        run_script(
            str(SCRIPTS_DIR / "init_memory_workspace.py"),
            str(workspace),
            "--profile",
            "light",
        )
        result = run_script(
            str(SCRIPTS_DIR / "make_handoff_brief.py"),
            str(workspace),
            "--max-section-chars",
            "400",
        )
        self.assertIn("## Excerpt: LOGBOOK.md", result.stdout)
        self.assertNotIn("Missing `HUMAN_BRIEF.md`", result.stdout)
        self.assertNotIn("Missing `ROADMAP.md`", result.stdout)

    def test_handoff_detects_memory_dir(self) -> None:
        workspace = self.make_workspace("memory-dir-handoff-workspace")
        (workspace / "README.md").write_text("# Existing README\n", encoding="utf-8")
        run_script(
            str(SCRIPTS_DIR / "init_memory_workspace.py"),
            str(workspace),
            "--profile",
            "standard",
        )
        result = run_script(
            str(SCRIPTS_DIR / "make_handoff_brief.py"),
            str(workspace),
            "--max-section-chars",
            "400",
        )
        self.assertIn("# Handoff Brief", result.stdout)
        self.assertIn("## Excerpt: HUMAN_BRIEF.md", result.stdout)
        self.assertNotIn("Missing `RECOVERY_NOTES.md`", result.stdout)


if __name__ == "__main__":
    unittest.main()
