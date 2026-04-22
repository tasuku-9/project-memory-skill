# Example Handoff Brief - Project Name - 2026-04-21

## Purpose

This project needs continuity across chat loss and model migration. The memory docs separate current truth, plans, decisions, research, hypotheses, human summaries, and recovery checkpoints.

## Current confirmed state

- `README.md` is only the entry point.
- `CURRENT_STATE.md` is the canonical current-truth file.
- `HYPOTHESIS_LAB.md` is not treated as truth.

## Current goal

Initialize or clean up the continuity docs and use them after each meaningful work session.

## Last completed work

Created the canonical file set and the routing guide.

## Key decisions and rationale

- Decision: split current truth out of README.
- Rationale: avoids README overload and improves model handoff accuracy.

## Recent research evidence

- Initial evidence is process-level only. A real multi-session test is still needed.

## Active hypotheses

- A separated memory workspace reduces context drift.

## Roadmap / next work

- Fill in project-specific current state.
- Add the first real recovery checkpoint.
- Use the docs in one actual interrupted session and audit afterward.

## Risks and unresolved questions

- The structure may be too heavy for very small projects.
- Users may stop updating it unless the workflow stays lightweight.

## Privacy / omitted material

- Private files and raw logs are omitted.

## Files to read first

1. `CONTEXT_MANIFEST.md`
2. `RECOVERY_NOTES.md`
3. `HUMAN_BRIEF.md`
4. `CURRENT_STATE.md`

## Files or folders to ignore

- `.cache/`
- `logs/`
- `private/`
- generated outputs

## Next recommended action

Fill in `CURRENT_STATE.md` and add a real project-specific checkpoint to `RECOVERY_NOTES.md`.
