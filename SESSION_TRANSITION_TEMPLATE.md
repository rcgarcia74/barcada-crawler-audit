# Session Transition Template — Handoff from Session 6 → Session 7

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-5
are summarized in SESSION_LOG.md.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

---

## Handoff metadata

- Outgoing session number: 6
- Closing date: 2026-05-19
- Outgoing session scope: Workstream 0 Week 1 Days 3-5 (audit §6
  fixture relocations C0.7a-d, sorted(glob)[0] refactor C0.8,
  C0.8 ruff format follow-up, fixture conformance test C0.9).
  Closes Workstream 0 Week 1.
- Reason for transition: workstream boundary (Week 1 → Week 2);
  Week 2's character is substantively different (live captures
  of SPA-framework sites vs static fixture cleanup).

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `4f9d23f`
- Last commit subject: `C0.8-format-fix: ruff format
  test_hard_exclusions.py (collapse multi-line calls)`
- Branch sync with `origin/main`: 0 commits ahead, 0 commits behind
- `pre-remediation-2026-05-19` tag at `3cbb9b3` (unchanged across
  all sessions; do not retag)
- Workstream tag created this session: `workstream-0-week1-end` at
  `4f9d23f` (pushed to origin; do not move)
- Pre-push gate state at HEAD: ALL CHECKS PASS (ruff check, ruff
  format --check, vermin --target=3.10-, validate_consistency for
  eval_data)
- Unstaged changes intentionally ignored across sessions
  (operator-side work in the locked tree):
    .claude/rules/code-correctness.md
    eval_data/README.md
    eval_data/TAXONOMY_GAP_LOG.md
    eval_data/stage1_labels.jsonl

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA: TBD (filled in after this session's transition
  commit pushes)
- Last commit subject: Workstream 0 Week 1 close (SESSION_LOG.md
  Session 6 + SESSION_TRANSITION_TEMPLATE.md fill for Week 2 +
  LESSONS.md create)
- Branch sync with `origin/main`: 0 commits ahead

---

## Active task list

The Session 6 task list (#6-#11) is fully complete. Task state is
session-local in Claude Code; it does NOT carry across sessions.

Session 7 should TaskCreate fresh tasks on open:
- C1.1: Source + capture 3 Next.js fixtures with populated
  `__NEXT_DATA__` (CSR-only, ISR, full-SSR variants); target
  `tests/fixtures/html/spa_hydration_next/`
- C1.2: Source + capture 2 Nuxt fixtures (`window.__NUXT__` or
  `<script id="__NUXT_DATA__">`); target
  `tests/fixtures/html/spa_hydration_nuxt/`
- C1.3: Source + capture 2 Apollo fixtures (`__APOLLO_STATE__`);
  target `tests/fixtures/html/spa_hydration_apollo/`
- C1.4: Source + capture 2 Redux fixtures (`__PRELOADED_STATE__`);
  target `tests/fixtures/html/spa_hydration_redux/`
- C1.5: Update `tests/scraper/test_fixture_conformance.py` COVERED
  set to include the 4 new directories + (optionally) add
  hydration-payload-specific conformance assertions

(Each capture should be its own commit per the per-fixture
discipline established in C0.5 and Days 3-5 work.)

---

## Operator decisions made during Session 6 that are reflected in plan + LESSONS.md

- Audit §6 relocations: 4 deletions (C0.7a/b/d) + 1 batch move
  (C0.7c) per audit's hedged recommendations.
- "Delete > Move when destination doesn't cleanly fit" — operator
  pattern, codified in LESSONS.md.
- C0.8 parametrize policy: only 100%-conforming directories.
- C0.9 lands with red builds (17 failures); each is a Week 5
  cleanup action item; xfail markers NOT to be added.
- `workstream-0-week1-end` tag at `4f9d23f` (HEAD with clean
  pre-push gate; not at C0.9 commit 6dace7d which would have ruff
  format failing).

## Outstanding operator-input requests blocking Session 7

None. Session 7 can begin work immediately on C1.1.

---

## Locked artifacts reminder (CRITICAL — do not modify)

- All of `eval_data/` — locked. Read-only context only. This
  includes `eval_data/canary_50_domains.txt` (consumable read-only
  for Workstream A.0 canary wiring later).
- `stage1.schema.json` v1.0 / 49 keywords — locked.
- `pre-remediation-2026-05-19` tag at `3cbb9b3` — do not retag or
  move.
- `workstream-0-week1-end` tag at `4f9d23f` — do not move.
- The 17 fixtures on the Week 5 cleanup punch list (see
  SESSION_LOG.md Session 6 entry) — DO NOT touch in Week 2; those
  are tracked intentional reds, scheduled for Week 5.

---

## Next concrete work unit

- **Action ID:** C1.1 (Next.js hydration captures; first of Week 2's
  9-fixture plan)
- **Scope:** Source 3 production Next.js marketing sites that ship
  with a populated `__NEXT_DATA__` `<script>` block. Variants needed:
    1. CSR-only — `__NEXT_DATA__` has `runtimeConfig` but minimal
       `props`
    2. ISR — `__NEXT_DATA__` with `props.pageProps` AND revalidation
       markers
    3. Full-SSR — `__NEXT_DATA__` with complete `props.pageProps`
       data
  Verify each by parsing the `__NEXT_DATA__` payload as JSON before
  saving the fixture.
- **Acceptance criteria:**
  - 3 fixtures saved at
    `tests/fixtures/html/spa_hydration_next/<domain>.html`
  - Each contains a parseable `__NEXT_DATA__` JSON block
  - Each captured with retry-on-TLS-error policy (≥3 attempts) per
    LESSONS.md / plan §11 Risk Register
  - UA: `Mozilla/5.0 (compatible; Barcada/1.0)` (current
    production UA; do NOT switch to BarcadaCrawler/1.0 yet — that
    is Workstream A.12 work)
  - pytest passes (no regressions in existing 64 + 145 tests)
  - 3 new commits, one per fixture, action-numbered C1.1.a/b/c
- **Files expected to be touched:**
  - NEW: `tests/fixtures/html/spa_hydration_next/<domain>.html` (×3)
  - Possibly: `tests/scraper/test_fixture_conformance.py` (extend
    COVERED set + add `test_spa_hydration_next_conformance`)
- **Files NOT to be touched:** everything under `eval_data/`,
  `stage1.schema.json`, and the `pre-remediation-*` /
  `workstream-0-*` tags. The 17 Week 5 punch-list fixtures.

---

## Required reading (Session 7 first 10 minutes)

In this order:
1. **This file** (you're reading it).
2. **`LESSONS.md`** (workspace) — operator patterns and observed
   conventions, including the retry-on-TLS-error policy and
   commit-message-via-tempfile pattern.
3. **`SESSION_LOG.md` Session 6 entry** — what just shipped, the
   17-fixture Week 5 punch list (DO NOT touch in Week 2; those
   land in Week 5).
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §3 Week 2** — the
   canonical plan for the 9 hydration captures (C1-C4).
5. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §11 Risk Register** —
   specifically "Recapture tooling needs retry policy" (lesson from
   C0.5d → C0.5d-followup). MUST apply to every Week 2 capture.
6. **`FIXTURE_AUDIT_REPORT.md` §12 Candidate Fixtures Reference** —
   detailed C1-C4 specifications.
7. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §14 Session Continuity
   Discipline** — read once if unfamiliar; sets the rules for how
   Session 7 closes out (when context grows, push to workstream
   tags, update SESSION_LOG.md, refill this template for Session 8).

After reading, verify repo state:

```
git -C /Users/administrator/projects/barcada-scraper status
git -C /Users/administrator/projects/barcada-scraper log --oneline -3
```

Last commit SHA must be `4f9d23f` (C0.8-format-fix). If anything
differs, surface to operator before doing work.

Then TaskCreate for C1.1.a/b/c, begin C1.1.a.

---

## Risk register state (plan §11)

Recent additions (set during Session 4, applied during Session 5):
- "Recapture tooling needs retry policy" — MUST apply to all
  Week 2 captures.

No risks escalated and unresolved by Session 6.

---

## Cost & schedule tracking

- Cost ceiling: $100 (operator-set 2026-05-19, alert at $50)
- Cost incurred Sessions 1-6: $0 (no LLM API calls for fixture
  work; curl + pytest only)
- Cost budget remaining: $100
- Schedule: 1.5 weeks elapsed of Workstream 0's 5-week budget.
  Week 2 (SPA hydration captures) and Weeks 3-5 still on schedule.
  Workstream 0 + A.0 completion target before reassessment (option
  (c) of the launch scenarios; no firm launch date).

---

## Notes for Session 7

- The C0.9 conformance test currently has 17 RED builds. These
  are acceptable per Risk #3. DO NOT add xfail markers. They are
  the Week 5 cleanup punch list. They are NOT a regression Session 7
  caused or needs to fix.
- 2 conformance tests SKIP (empty parametrize for `soft_404/` and
  `empty_google_sites/`) — both await Week 5 C0.3-followup /
  C0.4-followup repopulation.
- When Session 7 creates the first `spa_hydration_*/` directory,
  the catch-all `test_every_fixture_directory_has_a_test` will fail
  because COVERED doesn't include the new dir. Update COVERED in
  the same commit (C1.5) or earlier.
- File-based commit messages: heredocs break on apostrophes. Use
  `Write` tool to `/tmp/<action-id>-msg.txt`, then
  `git commit -F /tmp/...`. Pattern documented in LESSONS.md.
- "Confirm to commit?" gating before every commit — established
  pattern, see LESSONS.md.
- This template's structured fields will need refilling at Session 7
  close. Read plan §14 again if uncertain.
- If pre-push gate fails on the eval_data validate_consistency
  check, the failure is operator-side (in-progress labeling work);
  STOP and ask the operator. Do not use `--no-verify`.
