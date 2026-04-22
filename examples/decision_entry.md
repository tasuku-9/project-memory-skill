## DEC-2026-04-22-001 - Keep README as the entry point

- date: 2026-04-22
- decision: Keep `README.md` limited to entry-point orientation and move current truth into `CURRENT_STATE.md`.
- status: active
- context: The workspace was using README as both overview and current-state dump.
- alternatives considered:
  - keep current truth in README
  - split current truth into `CURRENT_STATE.md`
- rationale: A separate current-state file makes model migration and recovery safer.
- evidence: The workspace is meant to survive chat loss and agent handoffs.
- risks / tradeoffs: Another file must stay updated.
- expected impact: Less README overload and clearer routing.
- human_brief_update: yes
- human_brief_reason: Human orientation changed because the canonical source of current truth moved.
- revisit when: The split no longer reduces confusion.
- related files:
  - `README.md`
  - `CURRENT_STATE.md`
  - `DOCS_GUIDE.md`
