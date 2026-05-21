# Session Transition Template — Handoff from Session 13 → Session 14

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-13 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

---

## Handoff metadata

- Outgoing session number: 13
- Closing date: 2026-05-21
- Outgoing session scope: W4.1.5 (fixture-cascade driver). Built
  three engineering surfaces (parser-output adapter, FetcherSet
  bypass at `fetcher_core` seam, end-to-end cascade orchestrator +
  CLI) at `tests/runners/fixture_cascade/`. Small-subset validation
  against 10 fixtures in fake mode confirmed acceptance criteria
  1-4 + 6 (criterion 5 met under fake mode; real-mode validation
  deferred to W4.2 operator-driven step). Tag `workstream-0-week4-1-5-end`
  placed at repo HEAD `dd64963`.
- Reason for transition: natural seam at W4.1.5 close per plan §3
  Week 4 boundary. W4.2 is the operator-driven generation step
  against the full 198-fixture corpus, distinct from the W4.1.5
  engineering work just completed.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `5449ba6` (README — Fixture-cascade driver
  section; post-W4.1.5-tag doc hygiene per CLAUDE.md).
- Last commit subject: "docs: README — Fixture-cascade driver
  section (post-W4.1.5)"
- W4.1.5-tag commit: `dd64963` (W4.1.5.S3, the clean checkout
  target for the `workstream-0-week4-1-5-end` annotated tag per
  LESSONS Session 6 "tag at clean SHA not milestone SHA"; the
  README commit lands AFTER the tag as expected doc hygiene, not
  as part of the tagged work unit).
- Branch sync with `origin/main`: 0 commits ahead, 0 commits behind
  (verified at Session 13 close).
- Tags (do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3` (nuclear-revert anchor)
  - `workstream-0-week1-end` at `4f9d23f`
  - `workstream-0-week2-end` at `e5d2f91`
  - `workstream-0-week3-end` at `cf0c14c`
  - **NEW Session 13**: `workstream-0-week4-1-5-end` at `dd64963`
    (annotated tag SHA `f9be833a`). Annotation: "Fixture-cascade
    driver landed. Reusable at W A.0 W6 as `barcada-baseline generate`
    foundation. W4.2 expected-outputs generation begins on the next
    commit. Output lifetime: until W A.0 W6 OR until Phase 4 PR-E
    lands, whichever comes first."
  - NO `workstream-0-week4-end` tag yet — Week 4 sub-tag pattern
    per Session 12 sequencing decision. Operator may add a capstone
    tag at W4.3 close if desired.
- Pre-push gate state at HEAD `dd64963`: ALL CHECKS PASS (ruff +
  vermin + validate_consistency).
- Unstaged changes intentionally ignored across sessions
  (operator-side work in the locked tree, unchanged since Session 8
  close PLUS one item touched during this session's pre-push gate
  run):
    .claude/rules/code-correctness.md
    eval_data/README.md
    eval_data/TAXONOMY_GAP_LOG.md
    eval_data/stage1_labels.jsonl

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA: `c528a47` (W4.1.5.V, pushed 2026-05-21)
- Last commit subject: "W4.1.5.V: small-subset validation report
  (10 fixtures, fake mode)"
- Branch sync with `origin/main`: 0 commits ahead.

---

## Active task list

The Session 13 task list (cold-start verification → W4.1.5.T →
Surfaces S1/S2/S3 → V + tag → close-out) is fully complete:

- TODO resolution (`W4.1.5.T`, workspace `a34f7a2`): COMPLETE.
- Surface 1 parser adapter + 18 tests (repo `d337fb5`): COMPLETE.
- Surface 2 FetcherSet substitute + 19 tests (repo `02ac0e8`):
  COMPLETE.
- Surface 3 cascade orchestrator + CLI + 9 integration tests
  (repo `dd64963`): COMPLETE. Total 46/46 tests pass at HEAD.
- Small-subset validation (10 fixtures, fake mode) +
  workspace report `working/w4_1_5_small_subset_validation_2026-05-21.md`
  (workspace `c528a47`): COMPLETE.
- Annotated tag `workstream-0-week4-1-5-end` placed at repo `dd64963`:
  COMPLETE.
- Push (repo main + tag; workspace main): COMPLETE.

Task state is session-local in Claude Code; it does NOT carry across
sessions. Session 14 should TaskCreate fresh tasks on open.

Suggested Session 14 tasks:

- **W4.2 expected outputs across the 198-fixture corpus** (NEXT
  CONCRETE WORK UNIT, per plan §3 Week 4 (W4.2)). Steps:

  1. **Real-mode small-subset validation (gating check)**.
     Operator runs (with Azure credentials in env):
     ```
     AZURE_OPENAI_ENDPOINT=... AZURE_OPENAI_KEY=... \
     python -m tests.runners.fixture_cascade.cli \
         --output-dir <tmp-real-validation> \
         --run-id w4-2-real-validation \
         --llm-mode real --max-fixtures 10
     ```
     Expected cost ~$0.015-$0.06 (extrapolated from the $0.30 /
     198-fixture audit ballpark per
     `working/phase4_current_state_2026-05-21.md` Q3). If actual
     observed cost differs >3× from the per-call ballpark, halt
     and escalate before the full-corpus run.

  2. **Full-corpus run**:
     ```
     AZURE_OPENAI_ENDPOINT=... AZURE_OPENAI_KEY=... \
     python -m tests.runners.fixture_cascade.cli \
         --output-dir <w4-2-output-dir> \
         --run-id w4-2-full-corpus \
         --llm-mode real
     ```
     No `--max-fixtures` cap. Expected cost ~$0.30; expected
     wallclock ~5-15 minutes depending on Azure quota.

  3. **Human review** of each emitted `expected/<domain>.json` in
     `<output-dir>/expected/`. Spot-check at least one fixture per
     directory (~30 categories). The 198 outputs are the durable
     ground truth W4.3 will compare against, so the review is
     non-trivial — flag domains whose Stage 1/2/3 verdicts seem
     wrong against the fixture HTML, decide per-domain whether to
     keep the cascade output verbatim or annotate.

  4. **Copy into fixture tree**. For each reviewed-OK domain, copy
     `<output-dir>/expected/<domain>.json` into the matching
     `tests/fixtures/html/<category>/expected/<domain>.json`. Two
     considerations:
     - The W4.0 worked example
       `tests/fixtures/html/legitimate_business/expected/twilio.com.json`
       carries a `_placeholder` marker. Operator decides whether
       W4.2 overwrites it with real driver output OR protects it
       (analogous to the `PROTECTED_PRE_EXISTING_META` pattern in
       `generate_meta_json.py`).
     - 3 international_business fixtures are nested
       (`international_business/<locale>/<domain>.html`). The
       `expected/` directory layout should mirror that nesting if
       conformance tests are nesting-aware; verify against
       `tests/scraper/test_fixture_conformance.py` before copy.

  5. **One coordinated commit** containing the per-fixture JSON
     adds + (optionally) the worked-example resolution. Action
     reference `W4.2`. Per LESSONS.md "Confirm to commit?" gating.

  Acceptance criteria (W4.2):
  - Full 198 expected.json files produced.
  - Total LLM cost lands within 3× of $0.30 estimate (~$0.10-$0.90
    range).
  - Each fixture's expected.json human-reviewed (or
    deliberately-skipped-with-rationale) before commit.
  - Workspace + repo pre-push gates green at the W4.2 commit SHA.

- **W4.3 test infrastructure update** (FOLLOWS W4.2 close). Replace
  `exclusion_reason` assertions with `expected/<domain>.json`
  comparison logic in `tests/scraper/test_fixture_conformance.py`.
  At W4.3 time, decide whether the schema-shape divergence (18-col
  `stage3_decision` vs. v1.0 `expected.schema.json` legacy triple)
  bumps the schema to v1.1 OR maps via the consolidator.

- **W5 multipage + edge cases + repopulation** (FOLLOWS W4.3
  close). 20 multipage_boilerplate fixtures, 3 multilingual
  parking, soft_404 repopulation (6), empty_google_sites
  repopulation (3), edge-case robustness fixtures.

---

## Outstanding operator-input requests entering Session 14

**One material item**: real-mode small-subset validation result
(Step 1 above). The Session 13 fake-mode validation met acceptance
criterion 5 trivially ($0.00) but did NOT validate the cost shape
against the $0.30 audit ballpark. Before the full-corpus run, the
real-mode subset must surface actual per-call cost so the operator
can decide whether the cost envelope holds.

If real-mode subset cost is materially off (>3× per-call ballpark),
halt and escalate before the full-corpus run rather than running
through.

**No other gates** between Session 14 open and W4.2 generation work.

---

## Operator decisions made during Session 13 (cross-ref to SESSION_LOG.md)

- **Plan example shape** (TODO resolution): full 18-column rendition
  matching `stage3_predictions` parquet schema at
  `stage3/output_schema.py:112-140`. META_SCHEMA v1.0 prose
  divergence remains deferred prose-only register entry (e).
- **Driver location**: `tests/runners/fixture_cascade/` (test-runner
  side; sibling to `tests/fixtures/` rather than under it or under
  `tools/`).
- **LLM-mode wiring**: both fake + real modes via `--llm-mode` CLI
  flag. Fake default for plumbing tests + CI; real for W4.2
  generation. Real-mode wiring reads `AZURE_OPENAI_ENDPOINT` +
  `AZURE_OPENAI_KEY` from env (matches production cli.py pattern).
- **Synthetic LR bundle**: `predict_proba` returns 0.50 for every
  row, routing Stage 1 LR-tier rows to LLM escalation. Operator
  refinement: annotate LR/LLM-tier rows in expected.json as
  `synthetic_lr_used: true`. META_SCHEMA v1.0 allows this via
  JSON Schema Draft 7 default `additionalProperties: true`; no
  register bump needed.
- **expected.json shape**: emit actual 18-col `stage3_decision`
  per plan §3 W4.2 updated example. v1.0 `expected.schema.json`
  conformance validation skipped at W4.1.5; W4.3 will either bump
  the schema to v1.1 or map via the consolidator. Both options
  documented in the validation report's "Open items" section.
- **Worked-example handling deferred**: the
  `legitimate_business/expected/twilio.com.json` `_placeholder`
  resolution is W4.2 decision time (overwrite vs. protect).
- **Push hold-then-confirm**: operator initially chose "Hold" on
  the push gate, then explicitly authorized push in a follow-up
  message. Pre-push gate ran clean (ruff + vermin +
  validate_consistency).

---

## Pattern note for Session 14 (W4.2 review + copy cadence)

W4.2 is operator-driven generation + review work, not engineering.
The relevant patterns from Sessions 6 + 11:

- **Sample review before bulk** (Session 11 W4.1 pattern). Operator
  reviewed sample meta.json output across categories before the
  full 197-fixture bulk landed. W4.2 should follow the same shape:
  10-fixture real-mode review → operator approval → full-corpus
  run → per-directory spot-check → commit.

- **One coordinated commit for bulk** (Session 11 W4.1). The W4.1
  `generate_meta_json.py --bulk` landed 197 meta.json files in one
  commit (`9e1bda9`). W4.2 should follow the same shape: one
  commit for the 198 expected.json adds.

- **Confirm-to-commit gating** before every commit
  (LESSONS.md anchor pattern).

- **Verify-before-asking discipline**. Before committing each
  fixture's expected.json, double-check:
  - File matches the consolidator's output (no manual editing
    that would diverge from driver-reproducible state).
  - Domain stem in the JSON's parser_output matches the filename.
  - `synthetic_lr_used` annotation absent (real mode shouldn't
    produce it — synthetic_lr_used is fake-mode-only because in
    real mode the LR is real).
  - Any "missing fixture" or "ERROR_OTHER" patterns that should
    have surfaced did NOT silently slip through.

- **Driver-level input contracts** (LESSONS.md Session 12). If the
  driver behaves unexpectedly during W4.2, the source of truth is
  the runtime code, not the validation report or the plan
  documentation. Re-verify at session-current HEAD before
  diagnosing.

---

## Locked artifacts reminder (CRITICAL — do not modify)

- All of `eval_data/` — locked. Read-only context only.
- `stage1.schema.json` v1.0 / 49 keywords — locked.
- All Workstream 0 tags — locked (pre-remediation-2026-05-19 +
  workstream-0-week1/2/3-end + the new **workstream-0-week4-1-5-end**).
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` — read-only as of Session 12
  absorption close. Session 13's W4.1.5.T plan-update was a
  continuation-of-absorption authorized inline (the TODO comment
  itself acknowledged the deferred repo-read step). The file is
  CLOSED to further amendments going forward unless operator
  re-authorizes another halt-and-reconcile.
- The 17 fixtures on the Week 5 cleanup punch list — DO NOT touch
  in Session 14.
- `tests/fixtures/META_SCHEMA.md` + `tests/fixtures/meta.schema.json`
  + `tests/fixtures/expected.schema.json` — locked W4.0 schema
  artifacts. Six deferred prose-only register entries documented
  below; they fold into the next real machine-schema bump.
- 197 `<domain>.meta.json` files (commit `9e1bda9`) +
  `tests/fixtures/generate_meta_json.py`. The W4.0 worked example
  `legitimate_business/twilio.com.meta.json` IS locked via
  `PROTECTED_PRE_EXISTING_META`; operator-protected.
- `docs/phase4_implementation_plan.md` — governance reference; do
  NOT modify until Phase 4 PR-D/E/F/G sequencing is
  operator-authorized.
- `~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md` — workspace
  design-of-record; read-only.
- `~/crawler-audit/RECONCILIATION_2026-05-21.md` — archival
  historical record; do not edit.
- **NEW Session 13**: `tests/runners/fixture_cascade/` — the W4.1.5
  driver. Per W4.2 boundary, modifications to the driver itself are
  out-of-scope for W4.2 (which only consumes the driver's outputs).
  Discovery-driven bug fixes during real-mode validation may need
  operator authorization to land alongside W4.2 generation; surface
  before patching.
- **NEW Session 13**: `~/crawler-audit/working/w4_1_5_small_subset_validation_2026-05-21.md`
  — durable validation artifact; whitelisted in workspace
  `.gitignore`. Read-only.

---

## Next concrete work unit

- **Action ID:** **W4.2** (expected outputs across the 198-fixture
  corpus, per plan §3 Week 4 (W4.2)).
- **Scope:** Run the W4.1.5 fixture-cascade driver against the
  198-fixture corpus in `--llm-mode real`, human-review the
  resulting per-fixture `expected/<domain>.json`, and copy them
  into `tests/fixtures/html/<category>/expected/`.
- **Acceptance criteria:** see "Active task list" above.
- **Files expected to be touched:**
  - 198 new `tests/fixtures/html/<category>/expected/<domain>.json`
    files (one per fixture).
  - Possibly `tests/fixtures/html/legitimate_business/expected/twilio.com.json`
    (overwrite-or-protect operator decision at W4.2 time).
- **Files NOT to be touched:**
  - Anything under `tests/runners/fixture_cascade/` (driver
    treated as locked at W4.2; bug-fix discovery requires explicit
    operator authorization).
  - `eval_data/`, `stage1.schema.json`, the META_SCHEMA artifacts,
    the tags, the 17 W5-punch-list fixtures, the 197 W4.1 meta.json
    files.
  - `BARCADA_CRAWLER_REMEDIATION_PLAN.md` (read-only).
  - `docs/phase4_implementation_plan.md` (governance reference).
  - Production code under `src/barcada_scraper/`.

---

## Required reading (Session 14 first 10 minutes)

In this order:

1. **This file** (you're reading it).
2. **`LESSONS.md`** — operator patterns and observed conventions.
   The Session 13-relevant entries are unchanged from Session 12;
   "Verify-before-asking discipline (extension)" and "Driver-level
   input contracts" both apply forward.
3. **`SESSION_LOG.md` Session 13 entry** — what landed during the
   engineering session (commits, tag, validation result, operator
   decisions).
4. **`working/w4_1_5_small_subset_validation_2026-05-21.md`** — the
   validation report. "Open items for W4.2" section is the punch
   list Session 14 picks up.
5. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §3 Week 4 (W4.2)** — the
   inserted sub-section with the updated 18-column `stage3_decision`
   example (workspace SHA `a34f7a2`). **READ-ONLY.**
6. **`~/crawler-audit/working/phase4_current_state_2026-05-21.md`**
   — the cost envelope and material caveats. Q3 caveat #1
   ("Stage 2 page-acquisition short-circuit doesn't exist") has now
   been RESOLVED by the W4.1.5 driver; the rest still apply.
7. **`tests/runners/fixture_cascade/cli.py`** — the CLI surface.
   Real-mode env vars + flags.

After reading, verify repo state:

```
git -C /Users/administrator/projects/barcada-scraper status
git -C /Users/administrator/projects/barcada-scraper log --oneline -5
git -C /Users/administrator/projects/barcada-scraper tag -l 'workstream-*'
```

Expected:
- Last commit SHA: `5449ba6` (the post-tag README hygiene
  commit; W4.2 lands new commits but doesn't modify existing
  ones).
- Tags include `workstream-0-week4-1-5-end` pointing at `dd64963`
  (the Surface 3 commit; tag is intentionally NOT at the README
  commit since that's doc hygiene, not part of the tagged work
  unit).
If anything differs, surface to operator before doing work.

Then run the real-mode small-subset validation (Step 1 of W4.2),
present cost result to operator, await approval before the
full-corpus run.

---

## Risk register state (plan §11)

No new risks escalated and unresolved by Session 13.

Forward-applicable entries (unchanged from Session 12 close):

- "Recapture tooling needs retry policy" — STILL applies. W4.2 is
  generation work, not capture work — applies if any recapture
  is triggered.
- "Phase 4 infrastructure half landed concurrently with Workstream 0
  without plan absorption" — RESOLVED by Session 12 absorption.
  Future Phase 4 landings during a Workstream 0-E read-only period
  should escalate before compounding.
- "W4.2 expected-output lifetime constrained" — STILL applies.
  W4.2 outputs valid until W A.0 W6 OR Phase 4 PR-E lands,
  whichever comes first. The tag annotation on
  `workstream-0-week4-1-5-end` documents this constraint.
- "Phase 4 measurement half blocked on operator-led labeling"
  — STILL applies. PR-D requires Stage 2 + Stage 3 labeling;
  not currently scheduled.
- Forward-applicable lessons in LESSONS.md (unchanged at Session
  13 close — no new entries added this session because all surfaces
  used previously-established patterns).

Open latent gap (Issue 3 from Week 2 audit erratum, unchanged):
- Project's ruff `select` does not include "C" (mccabe), so
  cyclomatic-complexity violations escape pre-push. Manual
  `ruff check --select C901 <file>` in any code-modifying commit
  is the workaround. W4.2 has minimal code-modifying surface (most
  work is JSON-file authoring via the driver), so the gap is
  less acute this round.

LLM cost drift risk (plan §11) — Session 13 update:
- W4.1.5 close: $0 incurred (fake mode only).
- W4.2 expected combined LLM cost: ~$0.30 ballpark per Claude Code
  Q3 verification 2026-05-21. Material caveats unchanged:
  ±25% on per-call cost; ±50% on total feasible if cache hit rate
  is materially below 80%. Stop and escalate if actual spend
  trends >3× the $0.30 estimate before $50 alert threshold. Cost
  ceiling $100 untouched through Session 13 close. Budget
  remaining: $100.

---

## Deferred prose-only fixes (fold into next real schema bump)

Unchanged from Session 12 close. Six entries:

**Pre-existing (Session 11):**
- (a) META_SCHEMA.md §2.4 line 95 + §5 line 149: C0.7c nginx-401
  partition mismatch.
- (b) META_SCHEMA.md §2.4 line 93 + §5 line 150: replaced_in_place
  `captured_at` semantics.
- (c) META_SCHEMA.md §2.4 vocabulary extension:
  `approximated_from_synthetic_invalid_fallback` source-string.

**Session 12 additions:**
- (d) `tier_decided="parser_rule"` vocabulary entry (PR-F partial).
- (e) `expected/<domain>.json` shape reconciliation against
  `stage3/output_schema.py:112-140` — the 18-column shape.
  **Session 13 W4.1.5.T addressed the plan-side example update**
  (workspace SHA `a34f7a2`); META_SCHEMA / expected.schema.json
  alignment still deferred to the next bump.
- (f) Output durability annotation — until W A.0 W6 OR Phase 4 PR-E.

All six fold into the eventual v1.1 machine-schema bump's diff.
NO new prose-only entries added by Session 13 (the synthetic-LR
annotation question landed in v1.0's existing tolerance for
additional `stage1_decision` properties — no schema action needed).

---

## Cost & schedule tracking

- Cost ceiling: $100 (operator-set 2026-05-19, alert at $50).
- Cost incurred Sessions 1-13: $0. Session 13 was fake-mode-only
  on the driver path; no Azure calls.
- Cost budget remaining: $100.
- W4.2 expected spend: ~$0.30 LLM ballpark. Real-mode subset
  validation in Session 14 should refine the estimate before
  the full-corpus run.
- Schedule: ~3-4 weeks elapsed of Workstream 0's 5-week budget.
  - Weeks 1-3 COMPLETE.
  - Week 4 IN PROGRESS: W4.0 done, W4.1 done, W4.1.5 DONE
    (this session); W4.2 PROPOSED for Session 14; W4.3 follows.
  - Week 5 ahead.
  - Per Session 12 framing, W4.1.5 pulled cascade-driver engineering
    forward from W A.0 W6 by ~2 weeks. Weeks 4-5 may run ~1 week
    beyond the original budget; W A.0 W6 recovers the time.

---

## Notes for Session 14

- **Conformance test red count entering Session 14: 17** (Week 5
  punch list, byte-stable through W4.1.5 close). W4.2 generation
  itself does NOT change the test count; W4.3 (which adopts the
  new `expected/<domain>.json` comparison) is where conformance
  reds shift. Every Session 14 commit should verify count stays at
  17.
- **2 conformance tests still SKIP** (empty parametrize for
  `soft_404/` and `empty_google_sites/`) — both await Week 5
  C0.3-followup / C0.4-followup repopulation.
- **File-based commit messages** still mandatory. Pattern:
  Write to `/tmp/<id>-msg.txt`, then `git commit -F /tmp/...`.
- **"Confirm to commit?" gating** before every commit.
- **Verify-before-asking discipline** — bidirectional. Source of
  truth is the artifact, not the recall. Applies forward to the
  human-review step of W4.2 (each per-fixture verdict needs
  source-checking against the fixture HTML, not against the
  cascade's verdict alone).
- **Pre-push gate** may include validate_consistency failure from
  operator-side eval_data work. Documented + routinely passes.
  Never use `--no-verify`.
- **Plan is read-only** — never edit
  `BARCADA_CRAWLER_REMEDIATION_PLAN.md`. The Session 13 W4.1.5.T
  update was a continuation-of-absorption per the inline TODO; no
  further edits absent operator re-authorization.
- **Shell cwd drift**: use absolute paths or `cd /Users/administrator/
  projects/barcada-scraper` at the start of each Bash chain.
- **Workspace cwd**: when editing LESSONS.md / SESSION_LOG.md /
  this template, work in `/Users/administrator/crawler-audit/`.
- **W4 tag pattern**: per Session 12 sequencing decision, Week 4
  does NOT close with a single tag. `workstream-0-week4-1-5-end`
  placed this session; W4.2 + W4.3 land WITHOUT their own
  tags (the bookkeeping markers are the SESSION_LOG.md entries).
  Operator may revisit at W4.3 close.
- **W4.2 driver-locked policy**: the W4.1.5 driver at
  `tests/runners/fixture_cascade/` is treated as locked at W4.2.
  Discovery-driven bug fixes during real-mode validation require
  operator authorization. Surface before patching.
- **W4.2 worked-example handling**: operator decides at W4.2
  sample-review time whether the W4.0 placeholder
  (`legitimate_business/expected/twilio.com.json`) gets overwritten
  by driver output or protected via a `PROTECTED_PRE_EXISTING_*`
  analog.
- **This template's structured fields will need refilling at
  Session 14 close.**
