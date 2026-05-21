# Session Transition Template — Handoff from Session 14 → Session 15

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-14 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

---

## Handoff metadata

- Outgoing session number: 14
- Closing date: 2026-05-21
- Outgoing session scope: W4.2 expected-outputs generation against the
  full 198-fixture corpus. Ran the W4.1.5 fixture-cascade driver in
  `--llm-mode real` against all 198 fixtures, human-reviewed the
  resulting per-fixture `expected/<domain>.json`, and committed them
  under `tests/fixtures/html/<category>/expected/`. One coordinated
  commit at `cc2ba2c`; pushed to `origin/main`. No tag at W4.2 close
  per Session 12 sequencing decision.
- Reason for transition: natural seam at W4.2 close per plan §3 Week 4
  boundary. W4.3 (test infrastructure update) is a distinct work unit
  with its own design questions (schema bump v1.0 → v1.1 vs.
  consolidator mapping; conformance enumerator rglob change).

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `cc2ba2c` (W4.2 coordinated commit — 198
  expected.json files).
- Last commit subject: "W4.2: 198 expected.json files generated via
  fixture-cascade driver (real-mode)"
- Branch sync with `origin/main`: 0 commits ahead, 0 commits behind
  (verified at Session 14 close).
- Tags (do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3` (nuclear-revert anchor)
  - `workstream-0-week1-end` at `4f9d23f`
  - `workstream-0-week2-end` at `e5d2f91`
  - `workstream-0-week3-end` at `cf0c14c`
  - `workstream-0-week4-1-5-end` at `dd64963` (annotated tag SHA
    `f9be833a`). Annotation unchanged from Session 13 close: covers
    W A.0 W6 reusability + W4.2 output lifetime constraints.
  - NO `workstream-0-week4-end` tag — Week 4 sub-tag pattern per
    Session 12 sequencing decision. Operator may add a capstone tag
    at W4.3 close if desired.
- Pre-push gate state at HEAD `cc2ba2c`: ALL CHECKS PASS (ruff +
  ruff format + vermin 3.10 target + validate_consistency).
- Unstaged changes intentionally ignored across sessions
  (operator-side work in the locked tree, unchanged since Session 8
  close):
    eval_data/README.md
    eval_data/stage1_labels.jsonl
  These two files have been routinely unstaged through Sessions 8-14.
  Session 14 did NOT touch them; the validate_consistency pre-push
  gate confirms eval_data integrity (532 stage1_labels rows OK, 460
  partner_type_anchors rows OK).

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 14 start: `e60bee7` (Session 13 touch-up).
- Session 14 in `/Users/administrator/crawler-audit/`: NO commits
  landed this session. W4.2 is repo-side generation work; the
  workspace was read-only context for the operator-driven review.
  Session 14 close-out (this template refill + SESSION_LOG.md entry)
  is the only workspace write of the session.
- Branch sync with `origin/main`: depends on whether this close-out
  is committed and pushed.

---

## Active task list

The Session 14 task list (cold-start verification → Step A → B → C →
D → E) is fully complete:

- **Step 1 cold-start verification**: COMPLETE.
- **Step A real-mode small-subset validation**: COMPLETE. Two runs:
  - v1 (sorted-by-domain first 10): $0.00226, under-exercised cascade
    (0 Stage 3 calls). Operator chose re-run with diverse subset.
  - v2 (curated 10 fixtures including twilio/hubspot/snowflake/notion/
    salesforce/shopify/webflow/mozilla/wikimedia/siemens): $0.1066,
    6 Stage 3 LLM verdicts, validated cost-shape against Q3 envelope.
- **Step B full-corpus 198-fixture run**: COMPLETE. Total $0.26345
  in 117s wallclock. No mid-run halt. All five intermediate parquets
  produced. 198/198 expected.json emitted.
- **Step C per-fixture human review**: COMPLETE. Per-category sampling
  across 29 categories. All 12 Stage 3 LLM verdicts source-verified
  defensible. Stage 1 FN cluster (17 of 27 "legitimate*" fixtures →
  is_business=False) documented as current cascade behavior.
- **Step D copy into fixture tree**: COMPLETE. 198 files copied; 28
  new `expected/` directories created (one per category, plus the 3
  nested international_business locale dirs); twilio.com.json
  overwritten per operator decision.
- **Step E commit + push**: COMPLETE. Commit `cc2ba2c` with full
  file-based message at `/tmp/W4.2-msg.txt`. Pre-push gate clean.
  Pushed to origin/main.

Task state is session-local in Claude Code; it does NOT carry across
sessions. Session 15 should TaskCreate fresh tasks on open.

Suggested Session 15 tasks:

- **W4.3 test infrastructure update** (NEXT CONCRETE WORK UNIT, per
  plan §3 Week 4 (W4.3) — implicit; W4.3 was the test-side counterpart
  to W4.2's generation work).

  **The W4.3 gating design question**: the W4.2 commit `cc2ba2c`
  contains 198 expected.json files with the **18-column**
  `stage3_decision` shape (mirroring `stage3/output_schema.py:112-140`).
  The locked `tests/fixtures/expected.schema.json` v1.0 still
  requires the **legacy 3-field** `{partner_type, confidence, tier}`
  triple. The Session 13 W4.1.5.T plan-update fixed the plan §3 W4.2
  example to the 18-col shape; the locked machine schema is the
  remaining divergence. Two paths (operator decides at W4.3 design
  time):
    - **(a) Schema bump v1.0 → v1.1**: update
      `tests/fixtures/expected.schema.json` to match the 18-col shape.
      Cleanest semantic alignment but is a machine-schema bump that
      lands the six deferred prose-only fixes (a)-(f) per LESSONS.md
      "Defer prose-only schema fixes; bump only when machine schema
      changes" alongside it.
    - **(b) Consolidator mapping**: build a layer in
      `tests/runners/fixture_cascade/consolidate.py` (or a new
      adapter) that emits both the 18-col record AND a legacy
      `{partner_type, confidence, tier}` triple synthesized from it,
      keeping v1.0 alive. Avoids a schema bump but adds adapter code.

  **W4.3 scope** (per plan §3 W4.2 + LESSONS Session 14):

  1. **Resolve the schema-shape question** (operator-decision-gate
     before any test code lands). Path (a) requires the schema bump
     to land first; path (b) requires the adapter to land first.

  2. **Replace `exclusion_reason` assertions with `expected/<domain>.json`
     comparison logic** in `tests/scraper/test_fixture_conformance.py`
     so the 169 currently-passing conformance tests compare against
     the committed expected.json rather than against
     `exclusion_reason` strings. Today's 17 reds (Week 5 punch list)
     should remain red; this is a behavior-preserving refactor at the
     test-infrastructure layer, NOT a fixture-content change.

  3. **Conformance enumerator rglob change**:
     `tests/scraper/test_fixture_conformance.py:38` currently uses
     `sorted((FIXTURES / category).glob("*.html"))`. The 3 nested
     `international_business/<locale>/<domain>.html` fixtures are
     NOT discovered by this enumeration. W4.3 must change the
     enumeration to `rglob("*.html")` (or restructure the parametrize
     to traverse locales explicitly) so the 3 nested expected.json
     files become part of conformance coverage. Conformance count
     should shift from 17 reds / 169 pass / 2 skip to (likely)
     17 reds / 172 pass / 2 skip after this change.

  4. **Validation**: after W4.3 lands, the conformance test count
     should be **17 reds (Week 5 punch list unchanged) + 172 passed
     + 2 skipped**. If counts drift in unexpected ways (e.g.
     previously-passing tests start failing because the new
     comparison logic surfaces real Stage 1/2/3 verdict mismatches
     against the W4.2 snapshot), surface for diagnosis rather than
     silently accepting.

  5. **Coordinated commit** for W4.3 (action ref `W4.3`).

  **W4.3 acceptance criteria** (proposed; operator may revise at
  design time):
  - The 198 W4.2-committed expected.json files become the conformance
    test ground truth.
  - `exclusion_reason` assertions removed from
    `tests/scraper/test_fixture_conformance.py`.
  - Nested fixtures discoverable by the conformance enumerator.
  - 17 conformance reds remain (Week 5 punch list, not the test-
    infrastructure refactor's job to fix).
  - Pre-push gates green.
  - No driver changes at `tests/runners/fixture_cascade/`.

- **W5 multipage + edge cases + repopulation** (FOLLOWS W4.3 close).
  20 multipage_boilerplate fixtures, 3 multilingual parking, soft_404
  repopulation (6), empty_google_sites repopulation (3), edge-case
  robustness fixtures. The Week 5 punch list (17 conformance reds)
  also closes here.

---

## Outstanding operator-input requests entering Session 15

**Material item — W4.3 design decision**: schema-shape reconciliation
path (a) vs (b) above. The recommended sequencing is to present this
via AskUserQuestion as the first design-gate question after Session
15 cold-start verification, BEFORE any test code or schema lands.

**Material item — per-tier cost-accounting wiring gap**: surfaced
during W4.2 generation. The cost journal's
`totals.stage{1_llm,1_embedding,2_summarization,2_classification,
3_evidence,3_primary}_usd` fields are NOT incremented (all $0.0 in
the W4.2 run journal). `totals.cost_usd` and per-shard `cost_usd`
reconcile correctly, so total spend is captured accurately, but the
per-tier breakdown for telemetry/extrapolation is unavailable. Per-row
`stage3_decision.evidence_cost_usd` is also $0 for all rows ($0.0237
gap between sum-of-per-row primary+evidence cost and the Stage 3
shard total). This is a wiring gap in `tests/runners/fixture_cascade/`
(driver-locked policy applies). Operator decides whether to:
- Authorize a W4.3.X-prefixed patch to fix the cost-journal
  per-tier aggregation + Stage 3 evidence_cost_usd per-row recording.
- Defer to a future cleanup pass (low priority since total cost IS
  captured correctly).

**No other gates** between Session 15 open and W4.3 work.

---

## Operator decisions made during Session 14 (cross-ref to SESSION_LOG.md)

- **Step A re-run with diverse subset**: the sorted-by-domain first-10
  was unrepresentative (1 Stage 2 call, 0 Stage 3 calls). Operator
  chose to re-run Step A with 10 curated fixtures across legitimate
  business / mega_menu / nonprofit / international categories to
  validate cost-shape before the full corpus run.
- **Step B authorization**: operator approved proceeding to the full
  198-fixture run after Step A v2 demonstrated semantically real
  verdicts and a defensible per-call cost shape ($0.0156 avg Stage 3
  primary, 3× Q3 ballpark but within material caveats; full-corpus
  extrapolation $0.65, below $0.90 halt).
- **Step C → D authorization (land all 198 verbatim)**: operator
  reviewed the Stage 1 FN cluster + fixture-taxonomy/content
  mismatches and chose to land all 198 expected.json files as-is
  (documenting current cascade behavior). No driver-bug-suspected
  cases. Fixture-recategorization deferred to W5.
- **Twilio.com.json overwrite**: operator chose overwrite (not
  protect) for the W4.0 schema-lock placeholder. The W4.0 `_w4_note`
  anticipated this supersession ("Real parser_output generated in
  W4.2"). Overwritten with the W4.2 cascade verdict (Stage 3 ISV
  @ 0.92, 18-col stage3 shape, 168-key parser_output).
- **Push authorization**: operator authorized push directly after
  confirm-to-commit (no Hold/re-authorize round-trip as Session 13
  had).

---

## Pattern note for Session 15 (W4.3 test infrastructure)

W4.3 is engineering work touching `tests/scraper/test_fixture_
conformance.py`. The patterns from Sessions 11 + 13:

- **Surface-by-surface decomposition with operator approval gates**
  (Session 13 W4.1.5 pattern). W4.3 has at least three surfaces:
  schema-or-adapter resolution, enumerator rglob change, and the
  exclusion_reason → expected.json comparison refactor. Each could
  land as its own commit (with the schema/adapter possibly going
  first as a structural prerequisite).

- **Verify-before-asking on schemas**: before changing the
  conformance test, source-verify the W4.2 expected.json shape
  (cc2ba2c) actually present in the committed files. The 18-col
  stage3 shape is real; the v1.0 expected.schema.json legacy triple
  is real; the divergence is documented in deferred prose-only fix
  register entry (e).

- **Driver-level input contracts** (LESSONS Session 12): if the
  conformance test consumes consolidator output, source-verify
  `tests/runners/fixture_cascade/consolidate.py` shape at session-
  current HEAD before designing the comparison logic.

- **Confirm-to-commit gating** before every commit (LESSONS.md
  anchor pattern).

- **Driver-locked policy continues**: the W4.1.5 driver remains
  locked at `dd64963`. W4.3 should not modify
  `tests/runners/fixture_cascade/` UNLESS the schema path (b)
  consolidator-mapping decision lands first and explicitly requires
  the adapter to live there. If the adapter lives in
  `tests/scraper/` or elsewhere, the driver stays locked.

- **Conformance count discipline**: the 17 reds at W4.2 close are
  the Week 5 punch list. W4.3 is behavior-preserving for those reds
  — they should remain red after the refactor. New reds surfaced
  by the refactor are a design-question signal, not a routine
  outcome to accept.

---

## Locked artifacts reminder (CRITICAL — do not modify)

- All of `eval_data/` — locked. Read-only context only.
- `stage1.schema.json` v1.0 / 49 keywords — locked.
- All Workstream 0 tags — locked (pre-remediation-2026-05-19 +
  workstream-0-week1/2/3-end + workstream-0-week4-1-5-end).
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` — read-only as of Session 12
  absorption close. Session 13's W4.1.5.T plan-update was a
  continuation-of-absorption authorized inline. The file is CLOSED
  to further amendments going forward unless operator re-authorizes
  another halt-and-reconcile.
- The 17 fixtures on the Week 5 cleanup punch list — DO NOT touch
  in Session 15.
- `tests/fixtures/META_SCHEMA.md` + `tests/fixtures/meta.schema.json`
  + `tests/fixtures/expected.schema.json` — locked W4.0 schema
  artifacts UNLESS operator authorizes the W4.3 schema bump path (a),
  in which case `expected.schema.json` becomes the W4.3 surface to
  modify and the six deferred prose-only register entries fold in.
- 197 `<domain>.meta.json` files (commit `9e1bda9`) +
  `tests/fixtures/generate_meta_json.py`. W4.0 worked-example META
  protection unchanged.
- **NEW Session 14**: 198 `<domain>.expected.json` files (commit
  `cc2ba2c`). The W4.2 ground truth. W4.3 conformance tests
  COMPARE AGAINST these files; W4.3 should NOT modify them.
  Regeneration only via the W4.1.5 driver + W4.2 operator-driven
  generation + review cycle.
- `tests/runners/fixture_cascade/` — the W4.1.5 driver, locked at
  `dd64963`. Driver-bug-suspected discovery during W4.3 requires
  operator authorization to patch.
- `docs/phase4_implementation_plan.md` — governance reference; do
  NOT modify until Phase 4 PR-D/E/F/G sequencing is
  operator-authorized.
- `~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md` — workspace
  design-of-record; read-only.
- `~/crawler-audit/RECONCILIATION_2026-05-21.md` — archival
  historical record; do not edit.
- `~/crawler-audit/working/w4_1_5_small_subset_validation_2026-05-21.md`
  — durable validation artifact; whitelisted in workspace
  `.gitignore`. Read-only.

---

## Next concrete work unit

- **Action ID:** **W4.3** (test infrastructure update — replace
  `exclusion_reason` assertions with `expected/<domain>.json`
  comparison logic in `tests/scraper/test_fixture_conformance.py`).
- **Scope:** see "Active task list" above. The gating design
  question (schema bump v1.1 vs. consolidator mapping) opens the
  session.
- **Acceptance criteria:** see "Active task list" above.
- **Files expected to be touched:**
  - `tests/scraper/test_fixture_conformance.py` (primary surface).
  - Possibly `tests/fixtures/expected.schema.json` (if path (a)
    schema bump chosen).
  - Possibly a new `tests/scraper/` adapter or
    `tests/runners/fixture_cascade/consolidate.py` extension (if
    path (b) adapter chosen — and only with operator authorization
    for the driver-located variant).
- **Files NOT to be touched:**
  - The 198 expected.json files under `tests/fixtures/html/*/expected/`
    (W4.2 ground truth; regenerated only via the driver).
  - The W4.1.5 driver at `tests/runners/fixture_cascade/` (unless
    path (b) requires it AND operator authorizes).
  - `eval_data/`, `stage1.schema.json`, the META_SCHEMA artifacts
    (unless path (a) chosen, in which case `expected.schema.json`
    becomes the surface).
  - The 17 W5-punch-list fixtures, the 197 W4.1 meta.json files.
  - `BARCADA_CRAWLER_REMEDIATION_PLAN.md` (read-only).
  - `docs/phase4_implementation_plan.md` (governance reference).
  - Production code under `src/barcada_scraper/`.

---

## Required reading (Session 15 first 10 minutes)

In this order:

1. **This file** (you're reading it).
2. **`LESSONS.md`** — operator patterns and observed conventions.
   The Session 13-relevant entries are unchanged from Session 12;
   any new Session 14 entries (likely none — Session 14 was
   generation work using established patterns) will be at the
   bottom. "Verify-before-asking discipline (extension)" and
   "Driver-level input contracts" both apply forward.
3. **`SESSION_LOG.md` Session 14 entry** — what landed during the
   W4.2 generation session (Step A v1/v2 + Step B + Step C
   findings + Step D copy mechanics + the commit `cc2ba2c`).
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §3 Week 4 (W4.2)** sub-
   section — the 18-col `stage3_decision` example reconciled at
   Session 13 W4.1.5.T (workspace SHA `a34f7a2`). **READ-ONLY.**
5. **`tests/fixtures/expected.schema.json` v1.0** — the locked
   legacy 3-field schema. Surface for path (a) decision.
6. **`tests/scraper/test_fixture_conformance.py`** — the
   conformance test source-of-truth. Read the
   `_iter_fixtures()` / `glob` / `parametrize` shape at session-
   current HEAD before designing the comparison refactor.
7. **`tests/runners/fixture_cascade/consolidate.py`** — the
   consolidator surface. Surface for path (b) decision.
8. **One sample committed `expected/<domain>.json`** (recommended:
   `tests/fixtures/html/legitimate_business/expected/twilio.com.json`)
   — to source-verify the 18-col stage3 shape that W4.3 will
   compare against.

After reading, verify repo state:

```
git -C /Users/administrator/projects/barcada-scraper status
git -C /Users/administrator/projects/barcada-scraper log --oneline -5
git -C /Users/administrator/projects/barcada-scraper tag -l 'workstream-*'
find /Users/administrator/projects/barcada-scraper/tests/fixtures/html -path '*/expected/*.json' -type f | wc -l
```

Expected:
- Last commit SHA: `cc2ba2c` (the W4.2 coordinated commit).
- Tags include `workstream-0-week4-1-5-end` pointing at `dd64963`.
- 198 expected.json files on disk.
- 0 ahead / 0 behind origin/main.
- Only `eval_data/README.md` + `eval_data/stage1_labels.jsonl` showing
  as unstaged changes (locked, operator-side work).

If anything differs, surface to operator before doing work.

Then open the W4.3 design discussion: schema bump vs. consolidator
mapping via AskUserQuestion before any code lands.

---

## Risk register state (plan §11)

No new risks escalated and unresolved by Session 14.

Forward-applicable entries (unchanged from Session 13 close):

- "Recapture tooling needs retry policy" — STILL applies.
- "Phase 4 infrastructure half landed concurrently with Workstream 0
  without plan absorption" — RESOLVED by Session 12 absorption.
- "W4.2 expected-output lifetime constrained" — STILL applies.
  W4.2 outputs (commit `cc2ba2c`) valid until W A.0 W6 OR Phase 4
  PR-E lands, whichever comes first. The tag annotation on
  `workstream-0-week4-1-5-end` documents this constraint.
- "Phase 4 measurement half blocked on operator-led labeling" —
  STILL applies. PR-D requires Stage 2 + Stage 3 labeling.
- Forward-applicable lessons in LESSONS.md.

**NEW Session 14 — surface to risk register if not already**:
- **Cost-journal per-tier accounting gap**. The W4.1.5 driver's
  cost-journal totals.stage{N}_*_usd fields are not incremented; per-
  row stage3_decision.evidence_cost_usd is $0 for all rows. Captures
  total spend correctly (totals.cost_usd is accurate, per-shard
  cost_usd is accurate) but breaks downstream cost-shape extrapolation
  by tier. Fix requires operator authorization to touch the
  driver-locked surface. Severity: LOW (total cost telemetry intact;
  per-tier is "nice-to-have" for future cost-envelope work).

LLM cost drift risk (plan §11) — Session 14 update:
- W4.2 close: $0.26345 incurred (full-corpus real-mode generation).
- Cost incurred Sessions 1-14: $0.26345 total.
- Cost budget remaining: $99.74.
- Material caveats from Q3 (phase4_current_state_2026-05-21.md):
  ±25% on per-call cost; ±50% on total feasible if cache hit rate
  is materially below 80%. Session 14 observed `cached_input_tokens=0`
  (the cold-cache state — too few calls in the W4.2 run to warm
  the cache).
- Stop and escalate if actual spend trends >3× original $0.30
  estimate (>$0.90); not triggered at W4.2 close.

---

## Deferred prose-only fixes (fold into next real schema bump)

Unchanged from Session 13 close. Six entries:

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
  (workspace SHA `a34f7a2`); **Session 14 landed the actual
  18-col shape across 198 committed expected.json files** (commit
  `cc2ba2c`). META_SCHEMA / expected.schema.json alignment **still
  deferred** to the next bump. **W4.3 may bump the schema** (path
  (a) above), which would fold this entry in.
- (f) Output durability annotation — until W A.0 W6 OR Phase 4 PR-E.

NO new prose-only entries added by Session 14. The Stage 1 FN
cluster + the 4 fixture-taxonomy/content mismatches are documented
in the W4.2 commit message body, not in the schema-fix register
(they're classifier-quality / fixture-curation concerns, not schema
concerns).

All six fold into the eventual v1.1 machine-schema bump's diff.

---

## Cost & schedule tracking

- Cost ceiling: $100 (operator-set 2026-05-19, alert at $50).
- Cost incurred Sessions 1-14: $0.26345 (Session 14 was the first
  session with real Azure spend).
- Cost budget remaining: $99.73655 (round: $99.74).
- W4.3 expected spend: ~$0 (no LLM calls — test-infrastructure
  refactor only).
- Schedule: ~4.5 weeks elapsed of Workstream 0's 5-week budget.
  - Weeks 1-3 COMPLETE.
  - Week 4 IN PROGRESS: W4.0 done, W4.1 done, W4.1.5 DONE, **W4.2
    DONE this session**; W4.3 PROPOSED for Session 15.
  - Week 5 ahead.
  - Per Session 12 framing, W4.1.5 pulled cascade-driver engineering
    forward from W A.0 W6 by ~2 weeks. Weeks 4-5 may run ~1 week
    beyond the original budget; W A.0 W6 recovers the time.

---

## Notes for Session 15

- **Conformance test red count entering Session 15: 17** (Week 5
  punch list, byte-stable through W4.2 close). W4.3 must be
  behavior-preserving for those reds — they should remain red after
  the conformance test refactor. Verify count is still 17 at
  W4.3 commit. Note: after the rglob change, conformance count may
  shift from 17/169/2 to 17/172/2 (the 3 nested
  international_business fixtures become discoverable as passing
  tests).
- **2 conformance tests still SKIP** (empty parametrize for
  `soft_404/` and `empty_google_sites/`) — both await Week 5
  C0.3-followup / C0.4-followup repopulation.
- **File-based commit messages** still mandatory. Pattern: Write to
  `/tmp/<id>-msg.txt`, then `git commit -F /tmp/...`.
- **"Confirm to commit?" gating** before every commit.
- **Verify-before-asking discipline** — bidirectional. Source of
  truth is the artifact, not the recall. For W4.3, the W4.2-
  committed expected.json files at `cc2ba2c` ARE the comparison
  ground truth — verify their shape directly from the files, not
  from recall of this template.
- **Pre-push gate** at Session 14 close included a new "validate_
  consistency" step on the eval_data/ tree (532 stage1 rows + 460
  partner anchor rows OK). Routinely passes. Never use `--no-verify`.
- **Plan is read-only** — never edit
  `BARCADA_CRAWLER_REMEDIATION_PLAN.md`. The Session 13 W4.1.5.T
  update was a continuation-of-absorption per the inline TODO; no
  further edits absent operator re-authorization.
- **Shell cwd drift**: use absolute paths or `cd /Users/administrator/
  projects/barcada-scraper` at the start of each Bash chain.
- **Workspace cwd**: when editing LESSONS.md / SESSION_LOG.md / this
  template, work in `/Users/administrator/crawler-audit/`.
- **W4 tag pattern**: per Session 12 sequencing decision, Week 4
  does NOT close with a single tag. `workstream-0-week4-1-5-end`
  placed at W4.1.5; W4.2 + W4.3 land WITHOUT their own tags. The
  bookkeeping markers are the SESSION_LOG.md entries. Operator may
  revisit at W4.3 close.
- **W4.3 driver-locked policy**: the W4.1.5 driver at
  `tests/runners/fixture_cascade/` remains locked. Only the
  consolidator-mapping path (b) would require touching it, and only
  with explicit operator authorization. If the per-tier
  cost-accounting wiring gap is taken up alongside W4.3, the patch
  is a separate W4.3.X-prefixed commit with its own confirm-to-commit
  gate.
- **W4.2 ground truth durability**: the 198 expected.json files at
  `cc2ba2c` ARE the ground truth W4.3 compares against. Do NOT
  modify them as a shortcut to making conformance tests pass.
  If a comparison fails, the failure is either:
    (i) a W4.3 refactor bug (fix the test),
    (ii) a real cascade drift since W4.2 (root-cause in production
         code, not in the W4.2 snapshot), OR
    (iii) operator-directed regeneration via the driver + a new W4.x
          commit (not the conformance refactor's scope).
- **Cost telemetry**: the per-tier accounting gap means
  `totals.stage*_*_usd` fields are unreliable. Use shard-level
  `cost_usd` and `totals.cost_usd` for any cost extrapolation work.
  Per-row primary_classification_cost_usd is reliable; per-row
  evidence_cost_usd is NOT (shows $0 for all rows; ~$0.0237 of
  Stage 3 evidence cost lives only at the shard level).
- **This template's structured fields will need refilling at
  Session 15 close.**
