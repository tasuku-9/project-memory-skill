from __future__ import annotations

import base64
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from make_handoff_brief import latest_markdown_section
from memory_common import MemoryWorkspace, redact_secrets


class RegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="project-memory-regression-")
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name)

    def run_cli(self, script: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script), str(self.target), *args],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        )

    def init(self, profile: str = "standard", *args: str) -> None:
        result = self.run_cli("init_memory_workspace.py", "--profile", profile, *args)
        self.assertEqual(0, result.returncode, result.stderr)

    def snapshot(self) -> dict[str, bytes]:
        return {path.relative_to(self.target).as_posix(): path.read_bytes()
                for path in self.target.rglob("*") if path.is_file()}

    def test_repeated_init_preserves_files_and_profile(self) -> None:
        for profile in ("light", "standard", "research", "academic"):
            with self.subTest(profile=profile):
                # Explicit custom roots exercise repeat initialization outside auto-detection.
                self.init(profile, "--memory-dir", profile)
                current = self.target / profile / "CURRENT_STATE.md"
                current.write_text(current.read_text(encoding="utf-8") + "\nUSER_STATE\n", encoding="utf-8")
                before = self.snapshot()
                result = self.run_cli("init_memory_workspace.py", "--memory-dir", profile)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(before, self.snapshot())

    def test_repeated_root_init_does_not_create_second_workspace(self) -> None:
        self.init("research")
        before = self.snapshot()
        result = self.run_cli("init_memory_workspace.py")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.target / "memory").exists())

    def test_repeated_init_detects_existing_subdirectory(self) -> None:
        (self.target / "README.md").write_text("# User README\n", encoding="utf-8")
        self.init()
        before = self.snapshot()
        result = self.run_cli("init_memory_workspace.py")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_second_destination_collision_stops_before_writes(self) -> None:
        (self.target / "README.md").write_text("# User README\n", encoding="utf-8")
        (self.target / "memory").mkdir()
        (self.target / "memory" / "ROADMAP.md").write_text("# User roadmap\n", encoding="utf-8")
        before = self.snapshot()
        result = self.run_cli("init_memory_workspace.py")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("refusing a partial workspace", result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_profile_change_is_not_a_partial_migration(self) -> None:
        self.init("light")
        before = self.snapshot()
        for flags in ((), ("--overwrite",)):
            result = self.run_cli("init_memory_workspace.py", "--profile", "academic", *flags)
            self.assertNotEqual(0, result.returncode)
            self.assertEqual(before, self.snapshot())

    def test_memory_destination_file_is_rejected_without_partial_writes(self) -> None:
        (self.target / "README.md").write_text("# User README\n", encoding="utf-8")
        (self.target / "memory").write_text("USER_FILE\n", encoding="utf-8")
        before = self.snapshot()
        result = self.run_cli("init_memory_workspace.py")
        self.assertNotEqual(0, result.returncode)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_explicit_overwrite_and_dry_run(self) -> None:
        self.init("light")
        current = self.target / "CURRENT_STATE.md"
        current.write_text("RESET_ME\n", encoding="utf-8")
        before = self.snapshot()
        preview = self.run_cli("init_memory_workspace.py", "--overwrite", "--dry-run")
        self.assertEqual(0, preview.returncode, preview.stderr)
        self.assertEqual(before, self.snapshot())
        reset = self.run_cli("init_memory_workspace.py", "--overwrite")
        self.assertEqual(0, reset.returncode, reset.stderr)
        self.assertNotIn("RESET_ME", current.read_text(encoding="utf-8"))
        self.assertEqual("light", MemoryWorkspace(self.target).profile())

    def test_multiple_manifests_require_explicit_selection(self) -> None:
        self.init()
        self.init("research", "--memory-dir", "memory")
        before = self.snapshot()
        for script in ("init_memory_workspace.py", "audit_memory_workspace.py", "make_handoff_brief.py"):
            with self.subTest(script=script):
                result = self.run_cli(script)
                self.assertNotEqual(0, result.returncode)
                self.assertIn("Multiple memory workspaces", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                explicit = self.run_cli(script, "--memory-dir", ".")
                self.assertEqual(0, explicit.returncode, explicit.stderr)
        self.assertEqual(before, self.snapshot())

    def map_current_state(self, memory_dir: str = "") -> Path:
        self.init("light", "--memory-dir", memory_dir or ".")
        workspace = MemoryWorkspace(self.target, memory_dir)
        old = workspace.path("CURRENT_STATE.md")
        text = old.read_text(encoding="utf-8")
        old.write_text(text + "\nSTALE_SENTINEL\n", encoding="utf-8")
        mapped = self.target / "docs" / "current state.md"
        mapped.parent.mkdir(exist_ok=True)
        mapped.write_text(text + "\nCANONICAL_SENTINEL\n", encoding="utf-8")
        manifest = workspace.manifest.replace(
            f"| `CURRENT_STATE.md` | `{workspace.location('CURRENT_STATE.md')}` |",
            "| `CURRENT_STATE.md` | `docs/current state.md` |",
        )
        workspace.manifest_path.write_text(manifest, encoding="utf-8")
        return mapped

    def test_audit_and_handoff_follow_root_relative_canonical_mapping(self) -> None:
        self.map_current_state("memory")
        audit = self.run_cli("audit_memory_workspace.py", "--strict", "--json")
        self.assertEqual(0, audit.returncode, audit.stderr + audit.stdout)
        self.assertIn("docs/current state.md", json.loads(audit.stdout)["ok"])
        handoff = self.run_cli("make_handoff_brief.py", "--max-section-chars", "20000")
        self.assertEqual(0, handoff.returncode, handoff.stderr)
        self.assertIn("CANONICAL_SENTINEL", handoff.stdout)
        self.assertNotIn("STALE_SENTINEL", handoff.stdout)

    def test_missing_mapped_doc_does_not_fall_back_to_stale_copy(self) -> None:
        mapped = self.map_current_state()
        mapped.unlink()
        audit = self.run_cli("audit_memory_workspace.py", "--strict", "--json")
        self.assertNotEqual(0, audit.returncode)
        self.assertIn("docs/current state.md", json.loads(audit.stdout)["missing"])
        handoff = self.run_cli("make_handoff_brief.py", "--max-section-chars", "20000")
        self.assertIn("Missing `CURRENT_STATE.md`", handoff.stdout)
        self.assertNotIn("STALE_SENTINEL", handoff.stdout)

    def test_overwrite_does_not_reset_custom_mappings(self) -> None:
        self.map_current_state()
        before = self.snapshot()
        result = self.run_cli("init_memory_workspace.py", "--overwrite")
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(before, self.snapshot())

    def test_invalid_canonical_paths_fail_before_export(self) -> None:
        self.init("light")
        path = self.target / "CONTEXT_MANIFEST.md"
        original = path.read_text(encoding="utf-8")
        for location in ("../outside.md", "/outside.md", "C:\\outside.md", "C:outside.md", "CURRENT_STATE.md:stream"):
            with self.subTest(location=location):
                path.write_text(original.replace("| `CURRENT_STATE.md` | `CURRENT_STATE.md` |", f"| `CURRENT_STATE.md` | `{location}` |"), encoding="utf-8")
                for script in ("audit_memory_workspace.py", "make_handoff_brief.py"):
                    result = self.run_cli(script)
                    self.assertNotEqual(0, result.returncode)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual("", result.stdout)

    def test_duplicate_canonical_rows_are_rejected(self) -> None:
        self.init("light")
        path = self.target / "CONTEXT_MANIFEST.md"
        row = "| `CURRENT_STATE.md` | `CURRENT_STATE.md` |"
        path.write_text(path.read_text(encoding="utf-8").replace(row, row + "\n" + row), encoding="utf-8")
        result = self.run_cli("audit_memory_workspace.py")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Duplicate canonical location", result.stderr)

    def test_unsafe_memory_directories_are_rejected_by_all_clis(self) -> None:
        for location in ("../outside", "/outside", "C:\\outside", "C:outside"):
            for script in ("init_memory_workspace.py", "audit_memory_workspace.py", "make_handoff_brief.py"):
                with self.subTest(location=location, script=script):
                    result = self.run_cli(script, "--memory-dir", location)
                    self.assertNotEqual(0, result.returncode)
                    self.assertNotIn("Traceback", result.stderr)
        self.assertEqual({}, self.snapshot())

    def test_handoff_retains_code_and_ignores_fenced_example_headings(self) -> None:
        for fence in ("```", "~~~~", "````"):
            with self.subTest(fence=fence):
                text = (f"# Log\n\n## Entry template\n{fence}md\n## RES-TEMPLATE\n{fence}\n"
                        f"\n## RES-2026-09-07-001 - Real entry\nCommand:\n{fence}sh\n"
                        f"python validate.py --seed 42\n## RES-NOT-A-HEADING\n{fence}\nResult: passed\n"
                        "\n## RES-2026-09-06-001 - Older entry\nOLD_SENTINEL\n")
                selected = latest_markdown_section(text, r"^##\s+RES-")
                self.assertIn("Real entry", selected)
                self.assertIn("python validate.py --seed 42", selected)
                self.assertIn("Result: passed", selected)
                self.assertIn(fence + "sh", selected)
                self.assertNotIn("RES-TEMPLATE", selected)
                self.assertNotIn("OLD_SENTINEL", selected)

    def test_handoff_retains_actual_recovery_command(self) -> None:
        self.init("light")
        (self.target / "RECOVERY_NOTES.md").write_text(
            "# Recovery\n\n## 2026-09-07 - Resume\n```sh\npython resume.py --seed 42\n```\n",
            encoding="utf-8",
        )
        handoff = self.run_cli("make_handoff_brief.py")
        self.assertEqual(0, handoff.returncode, handoff.stderr)
        self.assertIn("python resume.py --seed 42", handoff.stdout)

    def test_private_key_redaction_removes_bodies_and_unclosed_blocks(self) -> None:
        for kind in ("", "RSA ", "OPENSSH ", "ENCRYPTED "):
            for closed in (False, True):
                with self.subTest(kind=kind, closed=closed):
                    key = f"-----BEGIN {kind}PRIVATE KEY-----\nPRIVATE_BODY_SENTINEL\n"
                    if closed:
                        key += f"-----END {kind}PRIVATE KEY-----\n"
                    result = redact_secrets("Before\n" + key + ("After\n" if closed else ""))
                    self.assertIn("[REDACTED_SECRET]", result)
                    self.assertNotIn("PRIVATE_BODY_SENTINEL", result)
                    self.assertNotIn("PRIVATE KEY-----", result)
                    if closed:
                        self.assertIn("After", result)

    def test_handoff_redacts_before_truncation_and_scans_unexcerpted_text(self) -> None:
        self.init("light")
        token = "ghp_" + "X" * 36
        log = self.target / "LOGBOOK.md"
        for text in (token, "A" * 200 + "\n" + token):
            log.write_text(text, encoding="utf-8")
            result = self.run_cli("make_handoff_brief.py", "--max-section-chars", "14", "--fail-on-secret")
            self.assertEqual(2, result.returncode, result.stderr)
            self.assertNotIn("ghp_", result.stdout)

    def test_handoff_private_key_body_never_reaches_default_output(self) -> None:
        self.init("light")
        (self.target / "LOGBOOK.md").write_text(
            "-----BEGIN PRIVATE KEY-----\nPRIVATE_BODY_SENTINEL\n-----END PRIVATE KEY-----\n",
            encoding="utf-8",
        )
        result = self.run_cli("make_handoff_brief.py")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertNotIn("PRIVATE_BODY_SENTINEL", result.stdout)

    def test_audit_never_echoes_tokens_in_secret_or_other_warnings(self) -> None:
        self.init("light")
        token = "ghp_" + "X" * 36
        (self.target / "CURRENT_STATE.md").write_text("Maybe " + token + "\n", encoding="utf-8")
        for flags in ((), ("--json",)):
            result = self.run_cli("audit_memory_workspace.py", *flags)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("Possible secret/credential", result.stdout)
            self.assertIn("[REDACTED_SECRET]", result.stdout)
            self.assertNotIn("ghp_", result.stdout)

    def test_asset_warnings_do_not_echo_private_key_bodies(self) -> None:
        self.init("academic")
        (self.target / "FIGURES_LOG.md").write_text(
            "# Figures\n\n### FIG-007\n**Title**: Image\n**Storage**: saved\n"
            "**Asset path(s)**:\n-----BEGIN PRIVATE KEY-----\nPRIVATE_BODY_SENTINEL\n-----END PRIVATE KEY-----\n",
            encoding="utf-8",
        )
        result = self.run_cli("audit_memory_workspace.py", "--json")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Possible secret/credential", result.stdout)
        self.assertNotIn("PRIVATE_BODY_SENTINEL", result.stdout)

    def test_asset_audit_checks_real_files_and_storage_status(self) -> None:
        self.init("academic", "--memory-dir", "memory")
        figures = self.target / "memory" / "FIGURES_LOG.md"
        figures.write_text(
            "# Figures\n\n### FIG-007\n**Title**: Supplied image\n**Storage**: saved\n"
            "**Asset path(s)**:\n- `figures/source image.png`\n**Original source**: user\n",
            encoding="utf-8",
        )
        missing = self.run_cli("audit_memory_workspace.py", "--strict")
        self.assertNotEqual(0, missing.returncode)
        self.assertIn("Visual asset is missing or empty", missing.stdout)
        asset = self.target / "figures" / "source image.png"
        asset.parent.mkdir()
        asset.touch()
        empty = self.run_cli("audit_memory_workspace.py", "--strict")
        self.assertNotEqual(0, empty.returncode)
        asset.write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="))
        saved = self.run_cli("audit_memory_workspace.py", "--strict")
        self.assertEqual(0, saved.returncode, saved.stdout + saved.stderr)
        for status in ("pending", "unavailable"):
            figures.write_text(f"# Figures\n\n### FIG-007\n**Title**: Supplied image\n**Storage**: {status}\n**Asset path(s)**:\n", encoding="utf-8")
            unavailable = self.run_cli("audit_memory_workspace.py", "--strict")
            self.assertNotEqual(0, unavailable.returncode)
            self.assertIn(f"Visual asset not saved ({status})", unavailable.stdout)


if __name__ == "__main__":
    unittest.main()
