# Migrate Context Task

Use this when context must be handed to another model, human, repository, or workspace.

## Goal

Produce a compact, accurate handoff that preserves enough information to continue safely without copying every file or chat transcript.

## Canonical rule

Treat repository markdown docs as the durable shared memory layer.
Do not rely on hidden tool-specific memory as the only source of truth.

## Read order

1. `CONTEXT_MANIFEST.md`
2. latest `RECOVERY_NOTES.md`
3. `HUMAN_BRIEF.md`
4. `CURRENT_STATE.md`
5. `ROADMAP.md`
6. selected `DECISION_LOG.md` entries
7. selected `RESEARCH_LOG.md` entries
8. selected `HYPOTHESIS_LAB.md` entries

## Handoff brief structure

```md
# Handoff Brief - PROJECT - YYYY-MM-DD

## Purpose

## Current confirmed state

## Current goal

## Last completed work

## Key decisions and rationale

## Recent research evidence

## Active hypotheses

## Roadmap / next work

## Risks and unresolved questions

## Privacy / omitted material

## Files to read first

## Files or folders to ignore

## Next recommended action
```

## Privacy handling

- Do not copy private source text or credentials.
- State when private material was omitted.
- Summarize sensitive findings without reproducing sensitive content.

## Quality checks

The brief should be short enough to paste into another model, but specific enough to prevent wrong assumptions.
