"""Shared helpers for project-memory scripts."""

from __future__ import annotations

import re

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


def redact_secrets(text: str) -> str:
    return SECRET_RE.sub("[REDACTED_SECRET]", text)
