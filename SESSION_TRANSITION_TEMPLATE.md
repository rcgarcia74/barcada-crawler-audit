# Session Transition Template — Handoff from Session 9 → Session 10

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-8
are summarized in SESSION_LOG.md; Session 9 close is in the most
recent SESSION_LOG.md entry.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

---

## Handoff metadata

- Outgoing session number: 9
- Closing date: 2026-05-20
- Outgoing session scope: Workstream 0 Week 3 second half — closes
  the C18 modern-SaaS candidate (5 fixtures, hybrid 3+2 spec per Path
  A operator decision) and the C7 mega-menu candidate (3 fixtures,
  Path C marker spec). Adds the Week-3-close conformance test
  extension for mega_menu. Tags `workstream-0-week3-end` at the final
  green-gate SHA (`cf0c14c`).
- Reason for transition: planned scope split (Week 3 complete; Week 4
  is a substantially different work unit — meta.json + expected-
  outputs generation, requiring the first ~$50-200 LLM cost
  expenditure of the remediation per plan §3 Week 4). Context at
  Session 9 close ~85% used — at/past the §14 transition threshold.
  Natural seam at Week 3 close + transition.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `cf0c14c`
- Last commit subject: `C7.d: extend test_fixture_conformance.py with
  test_mega_menu_conformance (Week 3 close)`
- Branch sync with `origin/main`: 0 commits ahead, 0 commits behind
- Tags (do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3` (nuclear-revert anchor)
  - `workstream-0-week1-end` at `4f9d23f` (Week 1 close)
  - `workstream-0-week2-end` at `e5d2f91` (Week 2 close)
  - `workstream-0-week3-end` at `cf0c14c` (Week 3 close — NEW this session)
- Pre-push gate state at HEAD: ALL CHECKS PASS (ruff check, ruff
  format --check, vermin --target=3.10-, validate_consistency for
  eval_data)
- Unstaged changes intentionally ignored across sessions (operator-
  side work in the locked tree, unchanged since Session 8 close):
    .claude/rules/code-correctness.md
    eval_data/README.md
    eval_data/TAXONOMY_GAP_LOG.md
    eval_data/stage1_labels.jsonl

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA: TBD (filled in after Session 9 close commit
  pushes; will be one commit ahead of `081b54e` which was the most
  recent Session 9 mid-session workspace commit)
- Last commit subject: Session 9 close: LESSONS.md amendments (3
  staged findings) + SESSION_LOG.md + SESSION_TRANSITION_TEMPLATE.md
  refill for Session 10
- Branch sync with `origin/main`: 0 commits ahead (after push)

---

## Active task list

The Session 9 task list (#1-#5) is fully complete:
- #1 C18.0 prevalence probe — closed (Path A 3+2 hybrid decision)
- #2 C18.a-e — 5 fixtures landed (twilio, hubspot, webflow, notion,
  snowflake)
- #3 C7.a-c — 3 fixtures landed (shopify, salesforce, synthetic
  microsoft-style)
- #4 Conformance extension (C7.d) — landed at cf0c14c
- #5 Session 9 close + workstream-0-week3-end tag — landed (this
  commit)

Task state is session-local in Claude Code; it does NOT carry across
sessions.

Session 10 should TaskCreate fresh tasks on open for Workstream 0
Week 4. Suggested tasks:

- **W4.0 meta.json schema lock**: Review plan §3 Week 4 meta.json
  schema (`source_url`, `captured_at`, `capture_method`,
  `content_type`, `content_length`, `encoding`, `response_status`,
  `expected_outcome`, `test_purpose`). Decide schema-version field
  shape, decide handling for synthetic fixtures
  (`capture_method: "synthetic_with_real_markers"`),
  decide handling for the empty-directory fixtures
  (soft_404/, empty_google_sites/). **Operator decision before any
  fixture generation.**

- **W4.1 meta.json generation across the corpus**: Per-fixture
  meta.json file generation. Current corpus is ~197 fixtures (+ the
  Week 3 additions). Estimate ~210-215 total meta.json files needed.
  Scripted generation likely cheapest — read each fixture, extract
  what can be extracted (content_length is easy, captured_at can be
  approximated from git log, source_url from fixture name +
  convention or from any existing capture script logs). Operator
  review of the script output before bulk commit.

- **W4.2 expected/<domain>.json generation**: Per-fixture expected-
  output generation. This requires running each fixture through the
  full pipeline (parser_output, barriers_verdict, stage1/2/3
  decisions). Stage 3 includes LLM calls — this is where the
  $50-200 plan-budgeted cost lands.

- **W4.3 Test infrastructure**: Update conformance tests to compare
  against expected/<domain>.json (replacing the current
  "exclusion_reason must be empty" style assertions with full
  comparison). May or may not be Week 4 vs Week 5 work depending on
  operator preference.

- **W3 retrospective question (operator-deferred from Session 9)**:
  Should verify-before-asking be promoted from ad-hoc discipline to
  a named Workstream 0 acceptance criterion? See "Open meta-question"
  section below.

- **Session 10 close + tag**: At end of Session 10, evaluate whether
  Week 4 is fully complete and tag `workstream-0-week4-end`. Note
  Week 4 may span multiple sessions given the meta.json + expected-
  output generation scope.

---

## Outstanding operator-input requests blocking Session 10

**W4.0 meta.json schema lock** — Plan §3 Week 4 specifies a schema
draft, but field-by-field details (e.g., timezone handling for
captured_at; whether expected_outcome is structured-JSON or free-text;
whether to add a schema_version field) need operator review before
bulk fixture generation. Session 10 should present the locked schema
to the operator first thing.

**W3 retrospective: verify-before-asking promotion** — see below.

---

## Operator decisions made during Session 9 (cross-ref to SESSION_LOG.md)

- **C18 hybrid spec (Path A)**: 3 structured-data-rich + 2 modern-
  minimal. JSON-LD Organization prevalence at 67% in the C18.0
  probe — above the 50% extinction threshold so the audit's marker
  doesn't need a Session-7-style spec revision. Original picks were
  Stripe + HubSpot + Webflow + Notion + Linear; Stripe and Linear
  were substituted (with Twilio and Snowflake) after verify-before-
  asking caught FPs (logged in LESSONS.md).

- **C7 Path C (marker relaxation)**: Conformance test accepts either
  aria-haspopup non-false OR aria-expanded+aria-controls combo. No
  density thresholds at this stage. Audit's literal
  aria-haspopup="menu" wording was illustrative-of-archetype, not
  binding (LESSONS.md "Audit-spec vs. production-reality drift").

- **C7.c Path B (synthetic-with-real-markers)**: Synthetic
  authored after 5 enterprise real-domain candidates failed in 5
  distinct ways. Filename `synthetic_microsoft_style_aria_controls.html`
  per operator spec; enterprise-realistic marker density (10×
  aria-expanded + 10× aria-controls).

- **LESSONS.md amendment timing for Session 9 close**: bundle the
  three findings (GitHub joins dd.js FP list; new FN-coverage-gap
  sub-section; enterprise-archetype-defended-sites append) into
  one workspace commit alongside SESSION_LOG.md and this template
  refill. Documented in commit messages, not edited mid-fixture-
  cycle.

- **Plan is read-only**: unchanged from prior sessions (memory:
  `feedback_remediation_plan_readonly.md`).

---

## Open meta-question for Session 10 retrospective

**Should verify-before-asking be promoted from ad-hoc discipline to
a named Workstream 0 acceptance criterion alongside 1:1:1?**

Three consecutive weeks of evidence that verify-before-asking
surfaces real spec/reality mismatches:
- Week 2 (Session 7 C1.1): Next.js App Router migration — audit
  marker `__NEXT_DATA__` superseded by `self.__next_f.push(...)` in
  Next.js 13+ (Oct 2022). Hybrid C1 spec adopted (1 Pages + 2 App
  Router).
- Week 3 (Session 9 C18.0): three detector FPs surfaced (dd.js,
  just-a-moment, _RE_SOFT_404 greedy-span) at a 36% rate across
  modern SaaS marketing sites; the dd.js FP rate climbed to 33% as
  the probe extended into enterprise sites during C7.c.
- Week 3 (Session 9 C7): aria-haspopup="menu" literal absent in
  0/3 audit-named candidates; relaxed to either-marker (Path C).
- Week 3 (Session 9 C7.c): three anti-bot FN patterns surfaced
  (Microsoft "blocked", Adobe HTTP/2 INTERNAL_ERROR, Oracle
  fw_error_www). None caught by existing detectors.

This is a rate, not a fluke. The discipline is anchored in three
LESSONS.md sub-sections at Session 9 close:
- "Probe framework generation before locking a fixture spec" (S7)
- "Synthetic-fixture HTML comments are regex-visible" (S8)
- "Detector precision findings" with FPs 1/2/3 and FNs 1/2/3 (S9)

Promotion shape options for the operator to choose at Week 3 retro:
- **(a) Plan amendment**: add verify-before-asking to plan §3
  acceptance criteria. Plan is read-only-archival, so this would
  land as a new document (e.g., `WORKSTREAM_0_ACCEPTANCE_CRITERIA.md`).
- **(b) CLAUDE.md / `.claude/rules/` codification**: add to the
  repo-side instructions so every future session reads the rule.
- **(c) Status quo**: keep as durable lesson in LESSONS.md only;
  rely on the §14 required-reading discipline to propagate it.

Operator decision deferred to Session 10 retrospective.

---

## Locked artifacts reminder (CRITICAL — do not modify)

- All of `eval_data/` — locked. Read-only context only. Includes
  `eval_data/canary_50_domains.txt`.
- `stage1.schema.json` v1.0 / 49 keywords — locked.
- `pre-remediation-2026-05-19` tag at `3cbb9b3` — do not retag or
  move.
- `workstream-0-week1-end` tag at `4f9d23f` — do not move.
- `workstream-0-week2-end` tag at `e5d2f91` — do not move.
- `workstream-0-week3-end` tag at `cf0c14c` — do not move.
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` — read-only, period. All
  deviations from the plan land in SESSION_LOG.md and LESSONS.md.
- The 17 fixtures on the Week 5 cleanup punch list (see
  SESSION_LOG.md Session 6 entry) — DO NOT touch in Session 10.

---

## Next concrete work unit

- **Action ID:** **W4.0** (meta.json schema lock — prerequisite
  before any bulk meta.json generation).
- **Scope:** Review plan §3 Week 4 meta.json schema with operator.
  Field-by-field decisions on:
    - timezone handling for `captured_at` (UTC ISO 8601 default?)
    - `expected_outcome` shape (structured JSON vs. free-text per
      plan example)
    - schema_version field (Y/N; if Y, semantic version vs. integer)
    - capture_method enumeration (live curl with retries / synthetic
      with real markers / synthetic / replaced-in-place / etc.)
    - empty-directory handling (do soft_404/ and empty_google_sites/
      need stub meta.json entries documenting the deletion?)
- **Acceptance criteria:**
  - Schema locked in a separate file (e.g.,
    `tests/fixtures/META_SCHEMA.md` or as a JSON Schema document)
  - Operator-approved before any bulk generation
  - One worked example meta.json file committed alongside the
    schema for reference (probably from one of the C5 or C18
    fixtures landed in Sessions 8-9)
- **Files expected to be touched:** new file in
  `tests/fixtures/META_SCHEMA.md` (or similar), new file as worked
  example, possibly an update to CLAUDE.md if meta.json conventions
  are project-wide. NOT bulk meta.json generation in W4.0 —
  that's W4.1.
- **Files NOT to be touched:** everything under `eval_data/`,
  `stage1.schema.json`, the tags, `BARCADA_CRAWLER_REMEDIATION_PLAN.md`,
  and the 17 Week-5 punch-list fixtures.

---

## Required reading (Session 10 first 10 minutes)

In this order:
1. **This file** (you're reading it).
2. **`LESSONS.md`** — operator patterns and observed conventions.
   Pay particular attention to:
   - "Detector precision findings" (FPs 1/2/3 + FNs 1/2/3 +
     deeper-circularity meta-observation) — the eventual W4
     expected-output generation could hit these same detectors.
   - "Audit-spec vs. production-reality drift" — applies forward to
     every framework-marker fixture (C1.2 Nuxt 2-vs-3, etc.) AND to
     audit examples in any other section the W4 work touches.
   - "Synthetic-fixture HTML comments are regex-visible" — applies
     to any synthetic fixture's meta.json `expected_outcome`
     free-text field if that field passes through any regex check.
3. **`SESSION_LOG.md` Session 9 entry** — what just shipped, the
   four production-precision findings, the C7.c synthetic
   resolution, the 9 repo commits, the Week 3 close.
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §3 Week 4** — meta.json
   and expected-outputs spec. **READ-ONLY.**
5. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §11 Risk Register** —
   especially "LLM cost drift during baseline regeneration" ($50-
   200 budget for W4.2 expected-output generation).
6. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §14 Session Continuity
   Discipline** — referenced for Session 10 close-out cadence.

After reading, verify repo state:

```
git -C /Users/administrator/projects/barcada-scraper status
git -C /Users/administrator/projects/barcada-scraper log --oneline -3
git -C /Users/administrator/projects/barcada-scraper tag -l 'workstream-*'
```

Expected:
- Last commit SHA: `cf0c14c` (C7.d).
- Tags: workstream-0-week1-end / week2-end / week3-end all present.
If anything differs, surface to operator before doing work.

Then begin W4.0 (meta.json schema lock). DO NOT skip — the schema
must be operator-approved before any bulk generation work begins.

---

## Risk register state (plan §11)

Recent additions (Sessions 4-9):
- "Recapture tooling needs retry policy" — STILL applies to every
  Session 10 capture (likely none in W4, but applies if any
  recapture is triggered during meta.json sourcing).
- Forward-applicable lessons in LESSONS.md (plan is read-only, so
  they cannot land in §11 itself):
  - "Probe framework generation before locking a fixture spec"
    (Session 7)
  - "Synthetic-fixture HTML comments are regex-visible" (Session 8)
  - **"Detector precision findings" with FPs and FNs** (Session 9 —
    NEW). Applies forward: W4.2 expected-output generation may run
    fixtures through the parser pipeline; pre-existing detector
    FPs/FNs could produce mis-classified expected outputs if not
    carefully reviewed. **Manual review of any expected outputs
    where `exclusion_reason != ''` is recommended before commit.**
  - **"Audit-spec vs. production-reality drift"** (Session 9 — NEW).
    Applies forward to any audit literal example referenced in W4
    fixture work; treat as illustrative, not binding.

Open latent gap (Issue 3 from Week 2 audit erratum, unchanged):
- Project's ruff `select` does not include "C" (mccabe), so
  cyclomatic-complexity violations escape pre-push. Manual
  `ruff check --select C901 <file>` in any code-modifying commit
  is the workaround until a project-config commit closes the gap.

LLM cost drift risk (plan §11, scheduled for W4.2 activation):
- Plan budgets $50-200 of LLM cost during Week 4 expected-output
  generation. Cost ceiling for the full remediation is $100
  (operator-set 2026-05-19, alert at $50). **The $100 ceiling vs.
  the $50-200 plan budget is inconsistent.** Either:
    - (a) Operator raises the ceiling before W4.2.
    - (b) Plan's $50-200 estimate is reduced through batch
      optimization, caching, model selection (claude-haiku-4-5
      for the early-stage Stage 1/2 classifications).
    - (c) Expected-output generation defers Stage 3 LLM calls and
      generates only Stage 1/2 expected outputs (Stage 3 LLM
      coverage lands later).
  **Operator decision needed at W4.0 or W4.2 latest.**

No new risks escalated and unresolved by Session 9.

---

## Cost & schedule tracking

- Cost ceiling: $100 (operator-set 2026-05-19, alert at $50)
- Cost incurred Sessions 1-9: $0 (no LLM API calls; curl + pytest
  + handwritten synthetic only)
- Cost budget remaining: $100
- Cost-vs-plan inconsistency flagged for W4.0 (above; $100 ceiling
  vs. $50-200 W4.2 budget)
- Schedule: 3 weeks elapsed of Workstream 0's 5-week budget.
  - Weeks 1-3 COMPLETE.
  - Weeks 4-5 still ahead.
  - Week 4 likely spans 2-3 sessions given meta.json + expected-
    output scope.

---

## Notes for Session 10

- **Conformance test red count at handoff is 17** (Week 5 punch
  list, unchanged from Week 1 close). Every Session 10 commit
  should verify the count stays at 17 unless the commit itself
  adds a known-failing fixture (which W4 work should not — W4 is
  per-fixture meta.json + expected outputs, not new fixtures).
- **2 conformance tests SKIP** (empty parametrize for `soft_404/`
  and `empty_google_sites/`) — both await Week 5 C0.3-followup /
  C0.4-followup repopulation.
- **The Week-3-end test surface is 17 fail / 169 pass / 2 skip**
  (was 17/161/2 at Week-2-end). W4 work should not change this
  count unless test infrastructure changes deliberately replace
  some assertions with expected-output-based ones.
- **File-based commit messages** still mandatory: heredocs break
  on apostrophes. Use `Write` to `/tmp/<action-id>-msg.txt`, then
  `git commit -F /tmp/...`. Pattern in LESSONS.md.
- **"Confirm to commit?" gating** before every commit — established
  pattern.
- **Verify-before-asking discipline** — hardened through Session 9
  (4-5 instances of "did you double check your work?" surfacing
  real gaps). Every "Confirm to commit?" must be preceded by a
  full verification table generated by re-parsing the on-disk
  file. Title-sanity and body-size-sanity checks added to the
  standard verify set after C7.c (the Microsoft block-page FN
  catch).
- **Three LESSONS.md sub-sections to apply forward** in W4:
  detector precision findings (don't trust raw extract_hard_exclusions
  output for expected_outcome generation without manual review);
  audit-spec drift (don't trust plan literal examples for meta.json
  schema fields without verification); synthetic comments are
  regex-visible (any free-text field in meta.json that gets parsed
  must be authored with anti-trip discipline).
- **Pre-push gate** may include validate_consistency failure from
  operator-side eval_data work. The 4 unstaged operator-side files
  in the locked tree are documented and routinely pass the gate;
  if the gate fails, STOP and ask the operator. Never use
  `--no-verify`.
- **Plan is read-only** — never edit
  `BARCADA_CRAWLER_REMEDIATION_PLAN.md`. Memory saved as
  `feedback_remediation_plan_readonly.md`.
- **Shell cwd drift**: use absolute paths or `cd /Users/administrator/
  projects/barcada-scraper` at the start of each Bash chain.
- **Workspace cwd**: when editing LESSONS.md / SESSION_LOG.md /
  this template, work in `/Users/administrator/crawler-audit/`.
- **W3 retrospective question** flagged above — promote verify-
  before-asking? Decision shape options listed; operator picks.
- This template's structured fields will need refilling at
  Session 10 close.
