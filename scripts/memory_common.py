"""Shared helpers for project-memory scripts."""

from __future__ import annotations

import re
from pathlib import Path, PureWindowsPath

SECRET_RE = re.compile(
    r'''(?ix)(
        (api[_-]?key|secret|token|password|passwd|credential)\s*[:=]\s*['"]?[A-Za-z0-9_./+=:@-]{8,}
        | AKIA[0-9A-Z]{16}
        | github_pat_[A-Za-z0-9_]{20,}
        | gh[pousr]_[A-Za-z0-9_]{20,}
        | -----BEGIN\s+(?P<key_type>(?:RSA\s+|DSA\s+|EC\s+|OPENSSH\s+|ENCRYPTED\s+)?PRIVATE\s+KEY)-----
          [\s\S]*?(?:-----END\s+(?P=key_type)-----|\Z)
    )''',
    re.VERBOSE,
)


def redact_secrets(text: str) -> str:
    return SECRET_RE.sub(lambda match: "[REDACTED_SECRET]" + "\n" * match.group().count("\n"), text)


def secret_hits(text: str, max_hits: int = 5) -> list[str]:
    hits: list[str] = []
    for match in SECRET_RE.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        hits.append(f"line {line}: [REDACTED_SECRET]")
        if len(hits) >= max_hits:
            break
    return hits


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def workspace_path(target: Path, value: str) -> Path:
    value = value.strip().replace("\\", "/")
    path = Path(value)
    if not value or path.is_absolute() or PureWindowsPath(value).drive or ":" in value or ".." in path.parts:
        raise ValueError("Paths must be relative and stay inside the target workspace.")
    resolved = (target / path).resolve()
    if not resolved.is_relative_to(target.resolve()):
        raise ValueError("Paths must stay inside the target workspace, including symlink targets.")
    return target / path


def normalize_memory_dir(value: str | None) -> str:
    value = (value or ".").strip().replace("\\", "/") or "."
    if Path(value).is_absolute() or PureWindowsPath(value).drive or ".." in Path(value).parts:
        raise ValueError("--memory-dir must be a relative directory inside the target workspace.")
    return "" if value in {".", "./"} else Path(value).as_posix().rstrip("/")


def detect_memory_dir(target: Path, memory_dir: str | None = None) -> str:
    if memory_dir is not None:
        return normalize_memory_dir(memory_dir)
    found = [name for name in ("", "memory", "project-memory")
             if (target / name / "CONTEXT_MANIFEST.md").is_file()]
    if len(found) > 1:
        raise ValueError("Multiple memory workspaces found; select one with --memory-dir.")
    return found[0] if found else ""


def markdown_headings(text: str) -> list[tuple[int, int, str]]:
    """Find ATX headings outside fenced blocks without altering section bodies."""
    headings: list[tuple[int, int, str]] = []
    fence = ""
    offset = 0
    for line in text.splitlines(keepends=True):
        if fence:
            closing = re.fullmatch(r" {0,3}(`{3,}|~{3,})[ \t]*", line.rstrip("\r\n"))
            if closing and closing[1][0] == fence[0] and len(closing[1]) >= len(fence):
                fence = ""
        else:
            opening = re.match(r" {0,3}(`{3,}|~{3,})(.*)", line)
            if opening and not (opening[1][0] == "`" and "`" in opening[2]):
                fence = opening[1]
            else:
                heading = re.match(r" {0,3}(#{1,6})\s+(.+?)\s*$", line)
                if heading:
                    headings.append((offset, len(heading[1]), heading[1] + " " + heading[2]))
        offset += len(line)
    return headings


class MemoryWorkspace:
    """Resolve logical docs using the manifest's project-root-relative locations."""

    def __init__(self, target: Path, memory_dir: str | None = None) -> None:
        self.target = target.resolve()
        self.memory_dir = detect_memory_dir(self.target, memory_dir)
        workspace_path(self.target, self.memory_dir or ".")
        self.manifest_path = workspace_path(self.target, self.default_location("CONTEXT_MANIFEST.md"))
        self.manifest = read_text(self.manifest_path)
        self.locations: dict[str, str] = {}
        headings = markdown_headings(self.manifest)
        for i, (start, level, heading) in enumerate(headings):
            if heading != "## Canonical locations":
                continue
            end = next((pos for pos, depth, _ in headings[i + 1:] if depth <= level), len(self.manifest))
            for line in self.manifest[start:end].splitlines():
                if not line.strip().startswith("|"):
                    continue
                cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
                if cells[0] == "Logical file" or all(re.fullmatch(r":?-+:?", cell) for cell in cells):
                    continue
                if len(cells) != 2 or not all(cells):
                    raise ValueError("Invalid Canonical locations row; expected logical file and relative path.")
                logical, location = cells
                if logical in self.locations:
                    raise ValueError(f"Duplicate canonical location for {logical}.")
                workspace_path(self.target, location)
                self.locations[logical] = location.replace("\\", "/")
        if self.path("CONTEXT_MANIFEST.md").resolve() != self.manifest_path.resolve():
            raise ValueError("The manifest cannot redirect its own canonical location.")

    def default_location(self, logical: str) -> str:
        return f"{self.memory_dir}/{logical}" if self.memory_dir else logical

    def location(self, logical: str) -> str:
        return self.locations.get(logical, self.default_location(logical))

    def path(self, logical: str) -> Path:
        return workspace_path(self.target, self.location(logical))

    def profile(self) -> str:
        match = re.search(r"(?im)^Profile:\s*(light|standard|research|academic)\s*$", self.manifest)
        return match[1] if match else "standard"
