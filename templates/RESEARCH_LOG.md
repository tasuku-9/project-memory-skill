# Research Log

This file records experiments, observations, investigations, literature checks, evidence, failures, and interpretation.

Do not use this file for untested brainstorming. Put untested ideas in `HYPOTHESIS_LAB.md`.

Do not use this file for final current truth. Promote supported conclusions into `CURRENT_STATE.md` only when warranted.

## Entry template

```md
## RES-YYYY-MM-DD-001 - Short title

- date:
- question:
- hypothesis / expectation:
- method:
- inputs / sources:
- result:
- interpretation:
- confidence: high | medium | low
- limitations:
- changed my mind about:
- next test:
- related hypotheses:
- related decisions:
- should update current state?: yes | no | unsure
- human_brief_update: yes | no
- human_brief_reason:
```

## RES-{{DATE}}-001 - Initial research log

- date: {{DATE}}
- question: What needs to be preserved so research continuity survives chat loss or model migration?
- hypothesis / expectation: Separating hypotheses, evidence, decisions, and current truth will reduce accidental overclaiming.
- method: Initialize a structured research memory workspace.
- inputs / sources: Continuity memory template.
- result: Research logging is available as a canonical evidence layer.
- interpretation: Future research entries should capture method, result, interpretation, confidence, and limitations.
- confidence: medium
- limitations: This is a process setup entry, not a domain research result.
- changed my mind about: None yet.
- next test: Use the log during a real research session and check whether it prevents context drift.
- related hypotheses:
  - `HYPOTHESIS_LAB.md`
- related decisions:
  - `DECISION_LOG.md`
- should update current state?: no
- human_brief_update: no
- human_brief_reason: No immediate human-facing change beyond workspace setup.
