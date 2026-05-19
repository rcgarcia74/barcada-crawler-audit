# Session Transition Template

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Lives at the root of
the workspace; overwritten at each transition (use git history to
recover prior handoffs).

Pair this with the latest entry in `SESSION_LOG.md` and the relevant
section of `BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session
cold and be productive within ~10 minutes.

---

## Handoff metadata

- Outgoing session number: ____
- Closing date: ____
- Outgoing session scope (one line): ____
- Reason for transition (workstream boundary, context-window, operator request, etc.): ____

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main` (Workstream 0+ discipline; no feature branches)
- Last commit SHA: ____
- Last commit subject: ____
- Branch sync with `origin/main`: ____ commits ahead, ____ commits behind
- `pre-remediation-2026-05-19` tag at `3cbb9b3` (unchanged across all sessions; do not retag)
- Most recent workstream tag (if any): ____
- Unstaged changes the outgoing session is intentionally ignoring (e.g., operator-side `eval_data/` work): ____

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA: ____
- Last commit subject: ____
- Branch sync with `origin/main`: ____ commits ahead, ____ commits behind

---

## Active task list

- Total tasks open at session close: ____
- Last in-progress task at close (if any): ____
- Pending tasks queued for the incoming session: ____

(If the outgoing session left tasks in `in_progress` state, the
incoming session should treat them as the resume point.)

---

## Operator decisions made during the outgoing session that are not yet reflected in the plan body

(Each decision should also be in `SESSION_LOG.md`'s outgoing-session
entry. List here for the incoming session's quick read.)

- ____
- ____
- ____

---

## Outstanding operator-input requests blocking the incoming session

If any, the incoming session should re-surface these before doing work.

- ____
- ____

---

## Locked artifacts reminder

- All of `eval_data/` — locked. Read-only context only.
- `stage1.schema.json` v1.0 / 49 keywords — locked.
- `pre-remediation-2026-05-19` tag — do not retag.

---

## Next concrete work unit

- Action ID (from remediation plan, e.g., `C0.7a`, `C0.9`, `A0.4`): ____
- Scope (one paragraph): ____
- Acceptance criteria (what makes the action complete): ____
- Files expected to be touched: ____
- Files NOT to be touched (beyond the locked artifacts): ____

---

## Risk register state

- Recent additions/changes to plan §11 (last session or two): ____
- Risks the outgoing session escalated but did not resolve: ____

---

## Cost & schedule tracking

- Cost budget remaining (against $100 ceiling, $50 alert): ____
- Workstream progress vs plan timeline: ____
- Notable schedule slips or accelerations: ____

---

## Notes for the incoming session

Free-form. Anything that doesn't fit a structured field but the next
session would benefit from knowing within the first 10 minutes:

- ____
- ____
- ____
