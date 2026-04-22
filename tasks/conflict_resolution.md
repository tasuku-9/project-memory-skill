# Conflict Resolution Task

Use this when continuity files disagree.

## Conflict types

- current state disagrees with old decisions
- roadmap assumes a hypothesis is true
- human brief is stale relative to newer logs
- recovery notes mention a next step that is no longer valid
- README says something current-state-specific that moved elsewhere
- research evidence weakens an active assumption

## Resolution process

1. Quote or summarize the conflicting claims.
2. Identify file, section, and date for each claim when possible.
3. Apply the priority order from `SKILL.md`.
4. Decide whether the conflict is:
   - stale doc
   - unresolved uncertainty
   - genuine contradiction
   - different scopes
5. Propose patches.
6. Do not overwrite uncertainty with false certainty.

## Priority order for current truth

1. `CURRENT_STATE.md`
2. latest relevant `DECISION_LOG.md`
3. latest relevant `RESEARCH_LOG.md`
4. latest `RECOVERY_NOTES.md`
5. `HUMAN_BRIEF.md`
6. `ROADMAP.md`
7. `HYPOTHESIS_LAB.md`

## Patch pattern

- Update `CURRENT_STATE.md` with the resolved truth.
- Add or update `Retired or no-longer-true claims` when useful.
- Add a `DECISION_LOG.md` entry if resolution requires a meaningful choice.
- Update `HUMAN_BRIEF.md` if the human-level picture changed.
- Add a fresh `RECOVERY_NOTES.md` checkpoint.
