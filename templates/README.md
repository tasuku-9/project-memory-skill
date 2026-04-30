# {{PROJECT_NAME}}

This file is the entry point for the project memory workspace.

It should answer:

- what this project is
- who or what it is for
- how to use this workspace
- which files to read first

It should not carry the full current truth, full decision history, raw research log, or recovery checkpoints.

project-memory is not a checklist of files to update every time.
It is a routed memory system: update only the canonical files whose responsibility changed.
Most sessions update 1-3 files, not the whole memory set.

## Purpose

<!-- Write a concise description of the project, research area, product, writing task, or long-running work. -->

## Current orientation

For the current source of truth, read:

1. `CONTEXT_MANIFEST.md`
2. latest entry in `RECOVERY_NOTES.md`
3. `HUMAN_BRIEF.md`
4. `CURRENT_STATE.md`

## Document map

| File | Role |
| --- | --- |
| `CURRENT_STATE.md` | Current confirmed truth |
| `ROADMAP.md` | Planned future work |
| `DECISION_LOG.md` | Decisions and why they were made |
| `RESEARCH_LOG.md` | Experiments, investigations, evidence, observations |
| `HYPOTHESIS_LAB.md` | Unverified hypotheses and raw sparks |
| `HUMAN_BRIEF.md` | Summary for human decisions |
| `RECOVERY_NOTES.md` | Fast resume notes after interruption |
| `DOCS_GUIDE.md` | Rules for where to write information |
| `CONTEXT_MANIFEST.md` | Read order, canonical sources, ignore rules |
| `GLOSSARY.md` | Project-specific terms |

## How to resume work

1. Read the latest entry in `RECOVERY_NOTES.md`.
2. Read `HUMAN_BRIEF.md` for orientation.
3. Check `CURRENT_STATE.md` before trusting old claims.
4. Use `ROADMAP.md` for next planned work.
5. Use `DECISION_LOG.md` and `RESEARCH_LOG.md` when you need rationale or evidence.

## Agent note

If this repository also uses `AGENTS.md`, `CLAUDE.md`, or similar tool-facing files, keep those files short and point them here.
The durable project memory belongs in the canonical docs, not in tool-specific notes.

## Privacy note

Do not store secrets, credentials, private source text, or sensitive personal data in canonical docs. Use `private/` for sensitive material and make sure it is ignored.
