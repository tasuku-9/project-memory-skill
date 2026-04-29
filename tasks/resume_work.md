# Resume Work Task

Use this when a user wants to continue after chat loss, a long pause, or model migration.

## Process

1. Read `CONTEXT_MANIFEST.md` if present.
2. Identify which memory files are relevant to the current resume task; do not preemptively read the full memory set.
3. Read the latest checkpoint in `RECOVERY_NOTES.md` when relevant.
4. Read `HUMAN_BRIEF.md` for orientation when relevant.
5. Read `CURRENT_STATE.md` before trusting old claims when relevant.
6. Read only the relevant parts of `ROADMAP.md`, `DECISION_LOG.md`, `RESEARCH_LOG.md`, and `HYPOTHESIS_LAB.md`.
7. Identify conflicts instead of smoothing them over.
8. Return a compact restart plan.

Treat repository docs as the durable memory layer. Do not assume a tool-specific memory feature contains the full truth.

## Response structure

```md
## Resume Summary

### Current goal

...

### Last completed step

...

### Current truth

...

### Open issues

...

### Next recommended action

...

### Files trusted

...

### Conflicts or uncertainties

...
```

## Common mistakes

- Reading raw logs before canonical docs.
- Treating the read order as a checklist.
- Treating recovery notes as the whole truth.
- Treating hypotheses as facts.
- Reconstructing old context from memory when files disagree.
