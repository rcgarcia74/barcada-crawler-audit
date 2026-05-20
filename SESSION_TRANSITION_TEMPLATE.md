# Session Transition Template — Handoff from Session 7 → Session 8

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-6
are summarized in SESSION_LOG.md; Session 7 close is in the most
recent SESSION_LOG.md entry.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

---

## Handoff metadata

- Outgoing session number: 7
- Closing date: 2026-05-20
- Outgoing session scope: Workstream 0 Week 2 (C1.1-C1.5, 10 SPA
  hydration fixtures + conformance test extension). Closes Workstream
  0 Week 2. (Session 7 also produced a post-close C1.5-followup commit
  b56df6e refactoring _balanced_brace_json — see Week 2 audit erratum
  in SESSION_LOG.md.)
- Reason for transition: workstream-day boundary (end of Week 2)
  AND substantive character change (live-capture SPA fixtures →
  international + SaaS + nonprofit + mega-menu gap fixtures with
  potentially different probe-before-lock concerns per framework
  area).

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `e5d2f91`
- Last commit subject: `C1.5: extend test_fixture_conformance.py
  with hydration-payload tests`
- Branch sync with `origin/main`: 0 commits ahead, 0 commits behind
- Tags (do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3` (nuclear-revert anchor)
  - `workstream-0-week1-end` at `4f9d23f` (Week 1 close)
  - `workstream-0-week2-end` at `e5d2f91` (Week 2 close, NEW this
    session)
- Pre-push gate state at HEAD: ALL CHECKS PASS (ruff check, ruff
  format --check, vermin --target=3.10-, validate_consistency for
  eval_data)
- Unstaged changes intentionally ignored across sessions (operator-
  side work in the locked tree):
    .claude/rules/code-correctness.md
    eval_data/README.md
    eval_data/TAXONOMY_GAP_LOG.md
    eval_data/stage1_labels.jsonl

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA: TBD (filled in after this session's transition
  commit pushes; will be one commit ahead of `29d1bed` which was
  the Session 7 opener)
- Last commit subject: Session 7 close: workstream-0-week2-end
  narrative + SESSION_TRANSITION_TEMPLATE.md refill for Session 8
- Branch sync with `origin/main`: 0 commits ahead (after push)

---

## Active task list

The Session 7 task list (#1-#5) is fully complete:
- #1 C1.1 (Next.js): 3 fixtures landed
- #2 C1.2 (Nuxt, expanded from 2): 3 fixtures landed
- #3 C1.3 (Apollo): 2 fixtures landed (1 real + 1 synthetic)
- #4 C1.4 (Redux): 2 fixtures landed (2 synthetic)
- #5 C1.5 (conformance test extension): landed

Task state is session-local in Claude Code; it does NOT carry across
sessions.

Session 8 should TaskCreate fresh tasks on open for Week 3:
- C5.a-c: 3 international-TLD captures (.de, .jp, .com.br) into new
  `tests/fixtures/html/international_business/{de,jp,br}/` (1 each)
- C22.a-c: 2-3 archetypal nonprofit fixtures extending
  `tests/fixtures/html/legitimate_nonprofit/` (Wikimedia
  Foundation, an `@type=EducationalOrganization`, an archetypal
  philanthropy)
- C18.a-e: 5 modern SaaS fixtures extending
  `tests/fixtures/html/legitimate_business/` with hreflang +
  canonical + JSON-LD Organization schema + mega-menu + blog link
- C7.a-c: 3 mega-menu fixtures into new
  `tests/fixtures/html/mega_menu/` with `aria-haspopup` + multi-
  column nested `<ul>` panels
- Total: 13-14 fixtures. Consider splitting Session 8 (C5 + C22)
  and Session 9 (C18 + C7) at a natural breakpoint to keep each
  session under the §14 context-window threshold.

(Each capture per-commit as established in Sessions 5-7.)

---

## Operator decisions made during Session 7 that are recorded
in SESSION_LOG.md + LESSONS.md

- C1.1 hybrid scope: 1 Pages-Router (`__NEXT_DATA__`) + 2 App-Router
  (`self.__next_f.push`). Audit/plan spec was written for the
  pre-Next.js-13 (Oct 2022) Pages-Router-only world.
- C1.2 scope expansion 2 → 3 fixtures (3 Nuxt 3, no Nuxt 2 found
  in 6-site probe).
- C1.3 hybrid: 1 real (coursera.org) + 1 synthetic — Apollo SSR
  cache extraction is a 7.7%-prevalence legacy pattern.
- C1.4 both synthetic — Redux SSR (`__PRELOADED_STATE__`) is 0/12
  extinct in 2026 production marketing/consumer surfaces.
- Plan is read-only: `BARCADA_CRAWLER_REMEDIATION_PLAN.md` must
  NOT be edited despite §14 wording. All deviations land in
  SESSION_LOG.md and LESSONS.md only. (Memory:
  `feedback_remediation_plan_readonly.md`.)
- "Probe framework generation before locking a fixture spec" added
  to LESSONS.md Diagnostic patterns. Applies to C5+, C18+, C22+, C7,
  and all future framework-marker fixture work.

---

## Outstanding operator-input requests blocking Session 8

None. Session 8 can begin Week 3 work immediately. The probe-before-
lock discipline (LESSONS.md) is the standing decision — apply per
framework area without re-asking.

A judgment call worth surfacing at Session 8 open: **C18 modern SaaS
JSON-LD assumption**. The audit assumed modern SaaS marketing
typically ships JSON-LD `@type=Organization`. The Session 7 probe
results suggest the audit's framework assumptions may have drifted
across multiple areas, so verifying the JSON-LD prevalence in
modern SaaS marketing before sourcing C18 candidates is prudent
(treat it as the probe-before-lock step for C18).

---

## Locked artifacts reminder (CRITICAL — do not modify)

- All of `eval_data/` — locked. Read-only context only. This
  includes `eval_data/canary_50_domains.txt` (consumable read-only
  for Workstream A.0 canary wiring later).
- `stage1.schema.json` v1.0 / 49 keywords — locked.
- `pre-remediation-2026-05-19` tag at `3cbb9b3` — do not retag or
  move.
- `workstream-0-week1-end` tag at `4f9d23f` — do not move.
- `workstream-0-week2-end` tag at `e5d2f91` — do not move.
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` — read-only, period. All
  deviations from the plan land in SESSION_LOG.md and LESSONS.md.
- The 17 fixtures on the Week 5 cleanup punch list (see SESSION_LOG.md
  Session 6 entry) — DO NOT touch in Week 3; those are tracked
  intentional reds, scheduled for Week 5.

---

## Next concrete work unit

- **Action ID:** C5.a (first .de international B2B capture; first of
  Week 3's 3-fixture international set, before C18, C22, C7)
- **Scope:** Source 1 production German B2B site with `.de` TLD and
  `<html lang="de">`. Include `<link rel="alternate" hreflang="en"
  href="..."/>` if available so the English-alternative path is
  exercised (audit Candidate #5 requirement). Apply LESSONS.md
  probe-before-lock discipline — verify the chosen site still
  produces useful structured HTML before locking.
- **Acceptance criteria:**
  - 1 fixture saved at
    `tests/fixtures/html/international_business/de/<domain>.html`
  - Captured with retry-on-TLS-error policy (≥3 attempts) per
    LESSONS.md
  - UA: `Mozilla/5.0 (compatible; Barcada/1.0)`
  - HTML has `<html lang="de">` and visible German body text
  - Pre-push gates green
  - 1 commit, action-numbered C5.a (or C5.de.a if the operator
    prefers per-locale sub-numbering)
- **Files expected to be touched:**
  - NEW: `tests/fixtures/html/international_business/de/<domain>.html`
  - C5.c will require a COVERED-set bump in
    test_fixture_conformance.py (similar to the C1.5 pattern; can be
    rolled into a Week-3-close conformance commit, OR added at C5.a
    if a `test_international_business_de_conformance` is wanted from
    the start)
- **Files NOT to be touched:** everything under `eval_data/`,
  `stage1.schema.json`, the `pre-remediation-*` and `workstream-0-*`
  tags, `BARCADA_CRAWLER_REMEDIATION_PLAN.md`, and the 17 Week-5
  punch-list fixtures.

---

## Required reading (Session 8 first 10 minutes)

In this order:
1. **This file** (you're reading it).
2. **`LESSONS.md`** (workspace) — operator patterns and observed
   conventions, INCLUDING the new "Probe framework generation
   before locking a fixture spec" entry under Diagnostic patterns.
3. **`SESSION_LOG.md` Session 7 entry** — what just shipped, the
   4 production-extinction findings (Next.js Pages Router, Nuxt 2,
   Apollo SSR, Redux SSR), the per-action operator decisions, the
   17-fixture Week 5 punch list (DO NOT touch).
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §3 Week 3** — the
   canonical plan for the 13-14 high-priority gap fixtures (C5,
   C18, C22, C7). NOTE: read-only.
5. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §11 Risk Register** —
   "Recapture tooling needs retry policy" still applies to every
   Week 3 capture.
6. **`FIXTURE_AUDIT_REPORT.md` §12** — detailed C5/C7/C18/C22
   specifications.
7. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §14 Session Continuity
   Discipline** — referenced for Session 8 close-out cadence.

After reading, verify repo state:

```
git -C /Users/administrator/projects/barcada-scraper status
git -C /Users/administrator/projects/barcada-scraper log --oneline -3
```

Last commit SHA must be `e5d2f91` (C1.5). If anything differs,
surface to operator before doing work.

Then probe before sourcing C5.a candidates (≥4 .de B2B sites),
choose a representative, present picks to operator, capture, commit.

---

## Risk register state (plan §11)

Recent additions (set during Session 4, applied through Session 7):
- "Recapture tooling needs retry policy" — STILL applies to every
  Week 3 capture.
- (Session 7 narrative): the "Framework hydration patterns drift
  across major versions" lesson is captured in LESSONS.md (plan
  is read-only, so it cannot land in §11 itself, but the
  forward-applicable forward-pattern discipline is durable in
  LESSONS.md and forms the standing approach for C5+, C18+, C22+,
  C7, and beyond).

No new risks escalated and unresolved by Session 7.

---

## Cost & schedule tracking

- Cost ceiling: $100 (operator-set 2026-05-19, alert at $50)
- Cost incurred Sessions 1-7: $0 (no LLM API calls for fixture
  work; curl + pytest + handwritten synthetic fixtures only)
- Cost budget remaining: $100
- Schedule: 2.5 weeks elapsed of Workstream 0's 5-week budget.
  Weeks 1-2 complete. Weeks 3-5 still ahead. Workstream 0 + A.0
  completion target before reassessment (option (c) of the launch
  scenarios; no firm launch date).

---

## Notes for Session 8

- **The C0.9 conformance test now has 17 RED builds** (down from 18
  at C1.1.a-to-C1.4.b interim state where the catch-all was failing
  uncovered-directory). The 17 are the Week 5 punch list — tracked,
  intentional, no xfail markers per §11.
- **2 conformance tests SKIP** (empty parametrize for `soft_404/`
  and `empty_google_sites/`) — both await Week 5 C0.3-followup /
  C0.4-followup repopulation.
- **When Session 8 creates the first `international_business/`
  directory**, the catch-all `test_every_fixture_directory_has_a_test`
  WILL fail because COVERED doesn't include the new dir. Same dynamic
  as Session 7 C1.1.a's first commit. Update COVERED in the same
  commit OR roll into a Week-3-close conformance commit (mirror of
  C1.5). Operator preference at end of Week 2 was the latter (roll
  conformance work into a closing commit), but Session 8 can choose
  either.
- **File-based commit messages** still mandatory: heredocs break on
  apostrophes. Use `Write` to `/tmp/<action-id>-msg.txt`, then
  `git commit -F /tmp/...`. Pattern documented in LESSONS.md.
- **"Confirm to commit?" gating** before every commit — established
  pattern, see LESSONS.md.
- **Shell cwd drift**: a `cd /tmp/...` in one Bash invocation
  persists into the next. Always use absolute paths for git ops
  (`mkdir -p /Users/administrator/projects/barcada-scraper/tests/...`)
  or start each Bash chain with `cd /Users/administrator/projects/
  barcada-scraper`. Session 7 hit this bug once during C1.2.a setup;
  fixture went to `/tmp/c2_captures/tests/...` instead of the
  project tree. Easily caught (git status surfaced the missing path)
  but worth avoiding.
- This template's structured fields will need refilling at Session 8
  close. Read plan §14 again if uncertain.
- **If pre-push gate fails on the eval_data validate_consistency
  check**, the failure is operator-side (in-progress labeling work);
  STOP and ask the operator. Do not use `--no-verify`.
- **Plan is read-only** — never attempt to edit
  `BARCADA_CRAWLER_REMEDIATION_PLAN.md`. Memory saved as
  `feedback_remediation_plan_readonly.md`.
