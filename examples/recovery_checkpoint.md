# Example Recovery Checkpoint

```md
## 2026-04-21 - Field mapping review paused

### Done

- Compared the old category mapping with the new field-split mapping.
- Confirmed that the runtime app still uses the coarse profile by default.
- Identified one candidate category that needs more calibration before promotion.

### Current state

- Coarse runtime mapping remains the safe default.
- Field-split mapping is experimental.
- The candidate category is not yet current truth.

### Open issues

- Need five more representative examples before changing runtime behavior.
- Need a human decision on whether to prioritize category expansion or UI wording.

### Next recommended step

- Add a `RESEARCH_LOG.md` entry for the latest calibration run, then update `ROADMAP.md` with the next data-collection task.

### Canonical docs to trust

- `CURRENT_STATE.md`
- `ROADMAP.md`
- `RESEARCH_LOG.md`
- `DECISION_LOG.md`
```
