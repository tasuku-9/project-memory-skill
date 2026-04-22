# Update Memory Task

Use this when a user wants to preserve, classify, or sync new work into the continuity docs.

## Operating assumption

The human usually does not write the memory docs directly.
The AI agent should route and write updates during the chat or coding session.

Treat repository markdown files as the durable shared memory layer.
Do not treat tool-specific hidden memory as the canonical source of truth.

## Process

1. Read `CONTEXT_MANIFEST.md` if present.
2. Read the latest `RECOVERY_NOTES.md` checkpoint.
3. Read `HUMAN_BRIEF.md` and `CURRENT_STATE.md`.
4. Read only the relevant parts of `ROADMAP.md`, `DECISION_LOG.md`, `RESEARCH_LOG.md`, and `HYPOTHESIS_LAB.md`.
5. Classify each new piece of information by status.
6. Write patch-ready updates only to the files that should change.
7. After routing updates, check whether the human-facing picture changed.
8. If yes, update `HUMAN_BRIEF.md`; if no, leave it unchanged and avoid summary churn.
9. End with an updated `RECOVERY_NOTES.md` checkpoint when the session reached a meaningful stopping point.

## Routing rules

| New material | Default destination |
| --- | --- |
| New raw idea, discomfort, half-formed thought | `HYPOTHESIS_LAB.md` under `Raw sparks` |
| Recurring or structured hypothesis | `HYPOTHESIS_LAB.md` under `Working hypotheses` |
| New experiment, source check, observation, comparison | `RESEARCH_LOG.md` |
| Choice, adoption, rejection, deferral | `DECISION_LOG.md` |
| Current trusted assumption | `CURRENT_STATE.md` |
| Human-facing orientation change | `HUMAN_BRIEF.md` |
| Fast restart checkpoint | `RECOVERY_NOTES.md` |

Do not require the human to explicitly ask for logging.
Prefer over-capturing in `HYPOTHESIS_LAB.md` over losing potentially useful ideas.

## Promotion rule

Do not promote anything directly from `HYPOTHESIS_LAB.md` to `CURRENT_STATE.md`.

Promotion to `CURRENT_STATE.md` requires at least one of:

- evidence or results in `RESEARCH_LOG.md`
- an explicit operating decision in `DECISION_LOG.md`
- a clearly stated user decision
- a cited external source when the claim depends on external facts

Only promote an item when the source is traceable and the item is worth using as a future working assumption.

## Output shape

```md
## Proposed updates

### CURRENT_STATE.md
...

### DECISION_LOG.md
...

### RESEARCH_LOG.md
...

### HYPOTHESIS_LAB.md
...

### HUMAN_BRIEF.md
...

### RECOVERY_NOTES.md
...
```

If nothing should change, say so clearly.
