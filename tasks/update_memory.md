# Update Memory Task

Use this when a user wants to preserve, classify, or sync new work into the continuity docs.

## Operating assumption

The human usually does not write the memory docs directly.
The AI agent should route and write updates during the chat or coding session.

Treat repository markdown files as the durable shared memory layer.
Do not treat tool-specific hidden memory as the canonical source of truth.

## Update scope protocol

Project memory is a routed memory system, not a checklist of files to update every time.

Before reading beyond `CONTEXT_MANIFEST.md`, identify which memory files are relevant to the current update.
For non-trivial work, briefly state which files will be read and which relevant files will not be read.
Do not preemptively read the full memory set.

Before editing memory files, produce a short update plan that says:

- which files will be updated
- why each file needs an update
- which relevant files will not be touched

Then apply only the necessary changes.
Most sessions should update 1-3 files.
Larger updates are appropriate only for major transitions such as phase changes, major hypothesis confirmation or rejection, architecture or approach changes, release checkpoints, or large migrations.

If you are about to edit memory files without an update plan, stop and produce the plan first.

## Process

1. Read `CONTEXT_MANIFEST.md` if present.
2. Read the latest `RECOVERY_NOTES.md` checkpoint if needed to establish the resume context.
3. Read `CURRENT_STATE.md` and `HUMAN_BRIEF.md` only when present and relevant to the update.
4. Read only the relevant parts of `ROADMAP.md`, `DECISION_LOG.md`, `RESEARCH_LOG.md`, `HYPOTHESIS_LAB.md`, or `LOGBOOK.md` when those files exist and are relevant; do not treat the file list as a checklist.
5. Classify each new piece of information by status.
6. Write patch-ready updates only to the files that should change.
7. After routing updates, check whether the human-facing picture changed.
8. If yes, update `HUMAN_BRIEF.md` when present; if no, leave it unchanged and avoid summary churn.
9. Update `RECOVERY_NOTES.md` only when the resume pointer changed at a meaningful stopping point.

## Routing rules

| New material | Default destination |
| --- | --- |
| Eligible raw idea, discomfort, half-formed thought | `HYPOTHESIS_LAB.md` under `Raw sparks`, or `LOGBOOK.md` in light |
| Eligible recurring or structured hypothesis | `HYPOTHESIS_LAB.md` under `Working hypotheses`, or `LOGBOOK.md` in light |
| New experiment, source check, observation, comparison | `RESEARCH_LOG.md` when present; otherwise `DECISION_LOG.md` for direction-changing findings or `LOGBOOK.md` in the light profile |
| Choice, adoption, rejection, deferral | `DECISION_LOG.md`, or `LOGBOOK.md` in light |
| Current trusted assumption | `CURRENT_STATE.md` |
| Human-facing orientation change | `HUMAN_BRIEF.md` |
| Fast restart checkpoint | `RECOVERY_NOTES.md` |

Apply Conversation capture in the project's `DOCS_GUIDE.md` and the selected capture strength in `CONTEXT_MANIFEST.md` before using these routes. If the guide is absent, use the conversation capture rule in `SKILL.md`.

These destinations do not create independent write triggers. Use only files belonging to the chosen workspace; a boundary with no qualifying change requires no edits.
Use `RECOVERY_NOTES.md` only as a short resume pointer, not as the source of truth.

## Promotion rule

Do not promote anything directly from `HYPOTHESIS_LAB.md` to `CURRENT_STATE.md`.

Promotion to `CURRENT_STATE.md` requires at least one of:

- evidence or results in `RESEARCH_LOG.md` when present
- an explicit operating decision in `DECISION_LOG.md`
- a direction-changing finding in `DECISION_LOG.md` when the selected profile does not include `RESEARCH_LOG.md`
- a clearly stated user decision
- a cited external source when the claim depends on external facts

Only promote an item when the source is traceable and the item is worth using as a future working assumption.

## Output shape

```md
## Proposed updates

### <Changed canonical file>
<Only the necessary update>
```

For an explicit update request, say clearly if nothing should change. During ordinary conversation, do not add unsolicited no-write or holding-status reports.
