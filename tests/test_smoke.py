from __future__ import annotations

import shutil
import subprocess
import sys
import unittest
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
    ignored_parts = {".git", "__pycache__", ".tmp_test_runs"}
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


if __name__ == "__main__":
    unittest.main()
