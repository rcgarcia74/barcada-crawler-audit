# Session Transition Template — Handoff from Session 12 → Session 13

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Session 12 close is in the most
recent SESSION_LOG.md entry.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

---

## Handoff metadata

- Outgoing session number: 12
- Closing date: 2026-05-21
- Outgoing session scope: Governance-only halt-and-reconcile.
  Session 12 opened against W4.2 (expected/<domain>.json
  generation across 198-fixture corpus). Pre-script verification
  surfaced a cascade-model drift between the plan's W4.2 framing
  (Stage 1 RULES + Stage 2 LR + Stage 3 sentinel) and current
  code's actual cascade composition (Stage 1 three-tier with LLM
  tail; Stage 2 two-pass LLM with outbound HTTP via `FetcherSet`;
  Stage 3 three upstream parquets + four T3 path fetches per
  domain). Operator paused W4.2 and authorized a reconciliation
  pass. Two Claude Code source-verification reports landed
  (Phase 4 PR status + Levers 2/3/7 + W4.2 cost envelope; Stage 3
  input shape). Reconciliation document
  `~/crawler-audit/RECONCILIATION_2026-05-21.md` produced and
  absorbed into BARCADA_CRAWLER_REMEDIATION_PLAN.md per §6.1
  eleven-amendment coordinated edit set. Read-only-period
  discipline broken with explicit one-time operator authorization.
- Reason for transition: natural seam at reconciliation close.
  W4.1.5 (fixture-cascade driver) is a substantively different
  work unit — engineering work building parser-output adapter,
  FetcherSet bypass, end-to-end cascade orchestrator. Phase-4-
  aligned. Session 12 closed governance-only; Session 13 opens
  engineering.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `5513b4c6` (verified Session 12 at 2026-05-21)
- Last commit subject: post-PR-COST/A/B/C state (four Phase 4
  infrastructure PRs landed during Workstream 0 read-only period;
  pre-Session-12 sequence)
- Branch sync with `origin/main`: 0 commits ahead, 0 commits
  behind (verified at session open; Session 12 made no repo
  changes)
- Tags (do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3` (nuclear-revert anchor)
  - `workstream-0-week1-end` at `4f9d23f` (Week 1 close)
  - `workstream-0-week2-end` at `e5d2f91` (Week 2 close)
  - `workstream-0-week3-end` at `cf0c14c` (Week 3 close)
  - NO `workstream-0-week4-end` tag yet — Week 4 spans multiple
    sessions and sub-units (W4.0/W4.1 complete; W4.1.5/W4.2/W4.3
    pending)
  - Tag-naming pattern at Session 13 W4.1.5 close:
    `workstream-0-week4-1-5-end` per plan §3 Week 4 (W4.1.5)
    tagging spec + LESSONS.md "Workstream tag at clean
    completion" + "tag at clean SHA not milestone SHA"
- Pre-push gate state at HEAD: expected ALL CHECKS PASS at
  `5513b4c6` (Session 11 pre-push gate state, unchanged through
  Session 12). Verify via pre-push checks at Session 13 first
  code-modifying commit.
- Unstaged changes intentionally ignored across sessions
  (operator-side work in the locked tree, unchanged since
  Session 8 close):
    .claude/rules/code-correctness.md
    eval_data/README.md
    eval_data/TAXONOMY_GAP_LOG.md
    eval_data/stage1_labels.jsonl

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA: TBD (filled in after Session 12 close commits
  push)
- Last commit subject: Session 12 close — absorption tag
  `reconciliation-2026-05-21-absorbed` placed at absorption
  commit SHA
- Branch sync with `origin/main`: 0 commits ahead (after push)

---

## Active task list

The Session 12 task list (W4.2 discovery → halt-and-reconcile →
plan absorption) is fully complete:

- W4.2 discovery sequence + Path-A/B/C/D elicitation + operator
  pause: complete (documented in SESSION_LOG.md Session 12 entry).
- Reconciliation pass + two Claude Code source-verification
  reports + reconciliation document at
  `~/crawler-audit/RECONCILIATION_2026-05-21.md`: complete.
- Plan absorption (eleven §6.1 amendments) into
  BARCADA_CRAWLER_REMEDIATION_PLAN.md: complete (one coordinated
  commit).
- SESSION_LOG.md Session 12 entry append: complete.
- LESSONS.md two new entries (verify-before-asking extension;
  driver-level input contracts) append: complete.
- This template refill for Session 13: complete (you're reading
  it).
- Three workspace artifacts placed
  (PIPELINE_ARCHITECTURE_TARGET_STATE.md +
  RECONCILIATION_2026-05-21.md + three working/ reports):
  complete.
- Workspace tag `reconciliation-2026-05-21-absorbed` placed at
  absorption commit SHA: complete.
- Workspace push: complete.

Task state is session-local in Claude Code; it does NOT carry
across sessions.

Session 13 should TaskCreate fresh tasks on open. Suggested tasks:

- **W4.1.5 fixture-cascade driver** (NEXT CONCRETE WORK UNIT, per
  plan §3 Week 4 (W4.1.5) + `RECONCILIATION_2026-05-21.md` §5.1).
  Three engineering surfaces (out-of-scope items listed
  separately):

  1. **Parser-output parquet construction from fixture HTML.**
     Adapter that takes fixture HTML files, synthesizes a
     fetched-page envelope (URL from fixture filename, status=200,
     content=HTML, etc.), runs the parser
     (`src/barcada_scraper/scraper/parser.py`) against the
     envelope, and writes a parser-output parquet row in the
     schema Stage 1 expects. Specifics:
     - URL derivation: bare-domain form from filename stem for
       real-domain captures; `https://<stem>.invalid/` per RFC
       2606 for synthetic-variant fixtures (matches W4.1 meta.json
       `source_url` derivation pattern).
     - Status default: 200 (fixture runs return 200 unconditionally;
       tier-promotion logic via `PROTECTION_ERROR_KINDS` is not
       exercised in fixture mode — that's W A.0 W7 synthetic-
       crawl-tape territory).
     - Encoding: utf-8 default; fixture meta.json carries explicit
       encoding for non-utf-8 captures (Big5, Shift-JIS, etc.).
     - Output parquet schema: matches Stage 1's expected
       `parser_output` columns (verify against current parser
       output schema at Session 13 open via repo read — out of
       scope for this template's authoring).

  2. **FetcherSet bypass at the `fetcher_core` seam** (verified
     seam per Stage 3 input shape verification 2026-05-21 Q3). A
     fixture-backed `FetcherSet` substitute that, when Stage 2 or
     Stage 3 requests any URL, returns the fixture HTML for that
     domain. Same adapter shape works for both stages because
     Stage 3 reuses Stage 2's `FetcherSet` type at
     `stage3/run.py:111-113`. Specifics:
     - Substitute returns the fixture HTML for ANY URL requested
       against the domain (every `/products`, `/solutions`,
       `/customers`, `/industries` request returns the same
       fixture HTML for Stage 3's T3 path acquisition).
     - Cost tracking: substitute does not increment bandwidth
       tracker (no real network use); does not affect the LLM
       cost tracker (which fires on Stage 2/3 LLM calls
       independently).
     - Lives at adapter/seam level; production cascade code stays
       untouched.

  3. **End-to-end cascade driver script.** Orchestrates parser →
     Stage 1 → Stage 2 → Stage 3 against the fixture corpus.
     Specifics:
     - Writes all intermediate parquets (parser output, Stage 1
       predictions, Stage 2 predictions, Stage 2 summaries,
       Stage 3 predictions, `pages.parquet` outputs).
     - Writes consolidated `expected/<domain>.json` per fixture
       matching META_SCHEMA v1.0 (six deferred prose-only fixes
       per "Deferred prose-only fixes" section below).
     - Writes a `RUN_ID`-stamped cost journal entry per PR-COST
       extension; operator can inspect to confirm cost-envelope
       tracking.
     - Restricts writes to workspace + `tests/fixtures/html/*/
       expected/` directories.
     - Idempotent re-run (analogous to W4.1 `generate_meta_json.py`
       `--bulk` / `--force` pattern).

  Acceptance criteria (W4.1.5):
  - Driver runs against 198-fixture corpus end-to-end without
    manual intervention.
  - For each fixture, all five intermediate parquets exist and
    conform to current code's schemas.
  - Per-fixture `expected/<domain>.json` produced and conforms to
    META_SCHEMA v1.0 (with the six deferred prose-only fixes).
  - Driver writes a `RUN_ID`-stamped cost journal entry.
  - Total LLM cost across the corpus run lands within 3× of the
    $0.30 Claude Code estimate (orders-of-magnitude floor and
    ceiling; tighter validation deferred to actual run).
  - Driver does not write outside the workspace +
    `tests/fixtures/html/*/expected/` directories.
  - Pre-push gate green at the W4.1.5 commit SHA.
  - Tag `workstream-0-week4-1-5-end` placed at clean checkout
    target with the annotation specified at plan §3 Week 4
    (W4.1.5) "Tagging" sub-section.

  Out-of-scope for W4.1.5:
  - Modifying pipeline code (production cascade stays untouched).
  - Eval-data labeling (Phase 4 PR-D territory; not currently
    scheduled).
  - Mocking LLM calls (LLM fires for real against fixture-derived
    inputs).
  - Coverage of tier-escalation paths (T1→T2→T3 promotion on
    `PROTECTION_ERROR_KINDS`) — fixture runs return 200
    unconditionally.

- **W4.2 expected outputs across the 198-fixture corpus** (FOLLOWS
  W4.1.5 close). Runs the W4.1.5 driver across the corpus and
  produces `expected/<domain>.json` per fixture. Cost envelope
  ~$0.30 LLM per Claude Code Q3 verification 2026-05-21; well
  within $100 ceiling. Output durability: until W A.0 W6 OR
  Phase 4 PR-E lands, whichever comes first (per plan §11
  Risk Register new entry).

- **W4.3 test infrastructure update** (FOLLOWS W4.2 close).
  Replace `exclusion_reason` assertions with full
  `expected/<domain>.json` comparison logic in
  `tests/scraper/test_fixture_conformance.py`. Self-contained
  after W4.2 produces expected outputs.

- **W5 multipage + edge case fixtures + repopulation** (FOLLOWS
  W4.3 close). 20 multipage_boilerplate fixtures, 3 multilingual
  parking fixtures, soft_404 repopulation (6 fixtures),
  empty_google_sites repopulation (3 fixtures), edge-case
  robustness fixtures.

---

## Outstanding operator-input requests entering Session 13

**None.** All Session 12 decisions resolved:

- Read-only-period discipline broken with explicit one-time
  authorization for the reconciliation absorption: resolved
  (one-shot; future amendments resume the read-only convention
  unless re-authorized).
- Reconciliation document location: resolved
  (`~/crawler-audit/RECONCILIATION_2026-05-21.md`).
- W4.1.5 sequencing: resolved (between W4.1 close and W4.2 open;
  Path-D sub-path (i) — real end-to-end driver, not mock-LLM or
  sentinel-extension).
- Tagging at W4.1.5 close: resolved
  (`workstream-0-week4-1-5-end` annotation per plan §3 Week 4
  (W4.1.5) "Tagging" sub-section).
- Architecture rationale document placement: resolved
  (`~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md`).
- Verification report preservation: resolved (three reports at
  `~/crawler-audit/working/`).
- Drift correction on Edits 4/5 sub-naming: resolved (Option 2 +
  refinement; new headings only at touch points; broader Week 4
  harmonization deferred).

Session 13 opens with full authorization to begin W4.1.5
engineering. No operator-input gates between session open and
W4.1.5 sample-review.

**Suggested operator-interaction cadence for Session 13:**
- Present three-surface design sketch (parser-output adapter,
  FetcherSet bypass, orchestrator) before code-modifying commits.
- Run on 5-10 representative fixtures first (across RULES /
  LR / LLM / exclusion paths); sample-review before bulk run.
- "Confirm to commit?" gating before each commit (LESSONS.md
  established pattern).

---

## Operator decisions made during Session 12 (cross-ref to SESSION_LOG.md)

- **Read-only-period discipline broken with explicit operator
  authorization** for the Session 12 reconciliation absorption.
  One-shot exception; future plan amendments resume the read-only
  convention unless re-authorized.
- **Reconciliation document at `~/crawler-audit/RECONCILIATION_2026-05-21.md`**;
  treated as one-shot historical record (per AUDIT_REPORT.md
  preservation convention), not a living document.
- **Sequencing: W4.1.5 (fixture-cascade driver) inserted between
  W4.1 and W4.2.** Path-D sub-path (i): real end-to-end driver,
  not mock-LLM or sentinel-extension. W4.2 follows W4.1.5 close.
- **Tag at W4.1.5 close per existing tagging discipline**
  (LESSONS.md "Workstream tag at clean completion" +
  "tag at clean SHA not milestone SHA"). Tag name:
  `workstream-0-week4-1-5-end`.
- **Architecture rationale document placement** at
  `~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md`. Marked
  as design-of-record for unimplemented work; do NOT use as
  source-of-truth for current code claims.
- **Three Claude Code source-verification reports preserved** as
  durable workspace artifacts at
  `~/crawler-audit/working/phase4_status_2026-05-21.md`,
  `phase4_current_state_2026-05-21.md`, and
  `stage3_input_shape_2026-05-21.md`.
- **Plan-amendments commit shape:** one coordinated commit
  applying all eleven §6.1 edits to
  BARCADA_CRAWLER_REMEDIATION_PLAN.md. SESSION_LOG.md,
  LESSONS.md, SESSION_TRANSITION_TEMPLATE.md, and artifact
  placement land in separate commits at session close.
- **Drift correction during absorption (Edits 4/5 sub-naming):**
  Option 2 + refinement. New `### Week 4 (W4.1.5):` and
  `### Week 4 (W4.2):` headings inserted only at touch points;
  no retroactive W4.0/W4.1/W4.3 headings; broader Week 4
  harmonization deferred to separate operator-authorized edit
  if desired.

---

## Pattern note for Session 13 (engineering-design + verify-before-asking)

Session 12 reinforced two patterns and surfaced two new ones:

- **Halt-and-reconcile cadence** (reinforced this session). When
  pre-script verification surfaces drift between plan-assumed
  state and current code state, halt → enumerate paths →
  reconcile pass with source verification → operator-authorized
  absorption. The cadence preserves read-only-period discipline
  by making any break explicit, one-shot, and documented.

- **Engineering-design cadence with mid-stream operator
  decisions** (reinforced from Session 11). When single-unit
  drafting (e.g., W4.1.5 cascade driver) surfaces multiple
  independent design questions during sample review, present
  each as a flagged decision rather than bundling. Session 13
  W4.1.5 likely surfaces flags around parser-output schema
  reconciliation, FetcherSet bypass mechanism, expected.json
  schema reconciliation with `stage3/output_schema.py:112-140`.

- **NEW Session 12: bidirectional verify-before-asking** (LESSONS.md
  §"Verify-before-asking discipline (extension)" this session).
  Operator-issued state claims about multi-PR multi-week work
  history also require source verification, not acceptance from
  operator recall alone. Operator claim "Phase 4 has not been
  implemented" was contradicted by Claude Code source
  verification (four PRs landed). Applies forward whenever next
  decision depends on a multi-artifact state claim.

- **NEW Session 12: driver-level input contracts** (LESSONS.md
  §"Driver-level input contracts" this session). Before scoping
  any work unit that runs pipeline against synthetic inputs,
  verify the driver-level input contract at runtime-code source.
  Applies forward to W4.1.5 driver design (parser-output schema,
  Stage 1/2/3 input parquets), W A.0 W7 synthetic-crawl-tapes,
  and any future synthetic-input work.

W4.1.5 falls under engineering-design (single-unit script drafting
across three surfaces). Session 13 should draft the design sketch
across all three surfaces, run sample on 5-10 representative
fixtures, present sample output for operator review, then run the
full bulk after sample approval.

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
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` — read-only as of Session
  12 close (the read-only-period break was one-shot for the
  reconciliation absorption; the file is closed to further
  amendments per operator convention). All deviations from the
  plan land in SESSION_LOG.md and LESSONS.md as before.
- The 17 fixtures on the Week 5 cleanup punch list (see
  SESSION_LOG.md Session 6 entry) — DO NOT touch in Session 13.
- `tests/fixtures/META_SCHEMA.md` + `tests/fixtures/meta.schema.json`
  + `tests/fixtures/expected.schema.json` — locked W4.0 schema
  artifacts. Schema bumps land via documented semver progression
  per META_SCHEMA §4, NOT via inline edits to v1.0. Six prose-only
  discrepancies tracked in the Deferred prose-only fixes section
  below — those fold into the next real schema bump, NOT into a
  prose-only bump.
- 197 `<domain>.meta.json` files (commit `9e1bda9`) +
  `tests/fixtures/generate_meta_json.py` (the W4.1 bulk-generation
  script). The meta.json files are not "locked" per se — they can
  be regenerated via `python tests/fixtures/generate_meta_json.py
  --bulk --force` if META_SCHEMA bumps and existing files go
  stale. But the W4.0 worked example
  (`legitimate_business/twilio.com.meta.json`) IS locked via the
  `PROTECTED_PRE_EXISTING_META` frozenset in the generator script;
  operator-protected.
- **NEW Session 12** (per plan §14 amendment): `docs/phase4_implementation_plan.md`
  (in-repo) is a governance reference; do NOT modify under any
  circumstance until Phase 4 PR-D/E/F/G sequencing is
  operator-authorized.
- **NEW Session 12** (per plan §14 amendment):
  `~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md` is a
  workspace design-of-record for unimplemented work; read-only.
  Do NOT use as source-of-truth for current code claims.
- **NEW Session 12** (per plan §14 amendment):
  `~/crawler-audit/RECONCILIATION_2026-05-21.md` is an archival
  historical record; not a governing document. Do not edit or
  amend.

---

## Next concrete work unit

- **Action ID:** **W4.1.5** (fixture-cascade driver per plan §3
  Week 4 (W4.1.5) + `RECONCILIATION_2026-05-21.md` §5.1).
- **Scope:** Build the engineering infrastructure that lets the
  full Stage 1 + Stage 2 + Stage 3 cascade run end-to-end against
  fixture HTML inputs. Three engineering surfaces: parser-output
  parquet construction adapter, FetcherSet bypass at
  `fetcher_core` seam, end-to-end cascade driver script. LLM
  calls fire for real against fixture-derived inputs; cost
  envelope ~$0.30 per Claude Code Q3 verification 2026-05-21.
- **Acceptance criteria:** as listed under "Active task list"
  above + plan §3 Week 4 (W4.1.5).
- **Files expected to be touched:**
  - One or more new Python modules under `tests/fixtures/` or
    `tools/` (location TBD: Session 13 design-time decision).
    Possible scaffolding: `tests/fixtures/fixture_cascade_driver.py`
    or `tools/fixture_cascade_driver.py`.
  - Possibly extends `tests/fixtures/generate_meta_json.py` if
    shared helpers (URL derivation, fixture iteration) are
    extracted.
  - 198 new `<domain>.json` files under
    `tests/fixtures/html/<category>/expected/` (if W4.1.5 close
    folds into W4.2 — operator decision at Session 13 design
    time; alternatively, W4.1.5 closes with driver-only, W4.2
    is a separate landing).
  - Five intermediate parquet artifact directories per fixture
    (parser output, Stage 1 predictions, Stage 2 predictions,
    Stage 2 summaries, Stage 3 predictions). Location TBD at
    Session 13 design time (likely under a `tests/fixtures/
    cascade_artifacts/` or similar — but could also live in a
    workspace `~/crawler-audit/working/` tree, depending on
    long-term vs. ephemeral framing).
- **Files NOT to be touched:**
  - Everything under `eval_data/`.
  - `stage1.schema.json` + the locked W4.0 schema artifacts
    (META_SCHEMA.md, meta.schema.json, expected.schema.json).
  - The tags.
  - `BARCADA_CRAWLER_REMEDIATION_PLAN.md` (read-only after
    Session 12 absorption close).
  - The 17 Week-5 punch-list fixtures.
  - The 197 W4.1 meta.json files (those represent provenance,
    not driver outputs; no need to touch in W4.1.5).
  - The W4.0 worked example
    `legitimate_business/expected/twilio.com.json` (carries a
    `_placeholder` parser_output marker; operator decides at
    Session 13 W4.1.5 close whether driver overwrites it with
    real output OR protects it like the meta.json was protected).
  - Production cascade code (`src/barcada_scraper/scraper/parser.py`,
    `src/barcada_scraper/classifier/stage{1,2,3}/`, etc.). The
    bypass is at adapter/seam level; production code stays
    untouched.

---

## Required reading (Session 13 first 10 minutes)

In this order:

1. **This file** (you're reading it).
2. **`LESSONS.md`** — operator patterns and observed conventions.
   Pay particular attention to:
   - **NEW Session 12**: "Verify-before-asking discipline
     (extension)" — bidirectional pattern; applies to W4.1.5
     design-decision sample-review.
   - **NEW Session 12**: "Driver-level input contracts" — direct
     forward-applicable pattern for W4.1.5 (parser-output schema
     reconciliation, FetcherSet bypass design).
   - "Defer prose-only schema fixes" (Session 11) — applies if
     W4.1.5 driver design surfaces new META_SCHEMA prose-only
     discrepancies.
   - "Verify-before-asking discipline" + "Close-out claims-by-
     analogy" (Session 10/11) — sample-review verification
     discipline.
3. **`SESSION_LOG.md` Session 12 entry** — W4.2 discovery, halt-
   and-reconcile, reconciliation pass, eleven §6.1 amendments
   absorbed, drift correction on Edits 4/5 sub-naming.
4. **`~/crawler-audit/RECONCILIATION_2026-05-21.md` §4 + §5.1**
   — dependency map between remediation-plan work units and
   Phase 4 PRs (§4), W4.1.5 scope per Path-D sub-path (i) (§5.1).
   Skim other sections.
5. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §3 Week 4 (W4.1.5)** —
   the inserted sub-section with scope, three engineering
   surfaces, acceptance criteria, tagging discipline. **READ-ONLY.**
6. **`~/crawler-audit/working/stage3_input_shape_2026-05-21.md`**
   — Stage 3 input contract verification. Q4 Sub-option (i) is
   the chosen W4.1.5 path; Q5 confirms no existing bypass
   mechanism.
7. **`~/crawler-audit/working/phase4_current_state_2026-05-21.md`**
   — Levers 2/3/7 current state (NOT applied) + W4.2 cost
   envelope ~$0.30. Material caveat #1 (Stage 2 page-acquisition
   short-circuit doesn't exist) is the engineering work W4.1.5
   builds.
8. **`tests/fixtures/META_SCHEMA.md`** — schema spec for both
   meta.json and expected/<domain>.json. Re-read §3 (expected.json)
   and §3.1 (sentinel values). Note that the W4.1.5 driver
   produces real expected outputs, not sentinel triples (the
   sentinel pattern was Flag 1's Session 10 resolution; W4.1.5
   supersedes it by producing real Stage 3 outputs).
9. **`tests/fixtures/generate_meta_json.py`** — the W4.1 bulk-
   generation script. W4.1.5 may borrow its shape (CLI flags,
   idempotency via `PROTECTED_PRE_EXISTING_*`, in-script +
   jsonschema validation) or extend it as a sibling.

After reading, verify repo state:

```
git -C /Users/administrator/projects/barcada-scraper status
git -C /Users/administrator/projects/barcada-scraper log --oneline -5
git -C /Users/administrator/projects/barcada-scraper tag -l 'workstream-*'
```

Expected:
- Last commit SHA: `5513b4c6` (unchanged across Session 12).
- Recent commits include Phase 4 PR-COST/A/B/C landings.
- Tags: `pre-remediation-2026-05-19` +
  `workstream-0-week1-end` / `week2-end` / `week3-end`. NO
  `week4-end` or `week4-1-5-end` tag yet.
If anything differs, surface to operator before doing work.

Then begin W4.1.5 design sketch across the three engineering
surfaces. Run sample on 5-10 representative fixtures spanning
RULES / LR / LLM / exclusion-path routing; present to operator;
await sample approval before bulk run.

---

## Risk register state (plan §11)

Recent additions (Sessions 4-12):

- "Recapture tooling needs retry policy" — STILL applies. W4.1.5
  driver builds adapter machinery, not capture work — applies if
  any recapture is triggered.
- **NEW Session 12** (in plan §11 directly per §6.1 Edit 9; not
  LESSONS.md-only):
  - "Phase 4 infrastructure half landed concurrently with
    Workstream 0 without plan absorption" — describes the gap;
    resolved by RECONCILIATION_2026-05-21.md absorption this
    session. Future Phase 4 PR-D/E/F/G landings during a
    Workstream 0-E read-only period should escalate before
    compounding.
  - "W4.2 expected-output lifetime constrained" — outputs at
    W4.2 close are valid until W A.0 W6 OR Phase 4 PR-E lands,
    whichever comes first. Lifetime annotation tracked in
    Deferred prose-only fixes register item (f) below.
  - "Phase 4 measurement half blocked on operator-led labeling"
    — PR-D requires Stage 2 + Stage 3 labeling; not currently
    scheduled. Plan does not commit to a Phase 4 ship date.
- Forward-applicable lessons in LESSONS.md (plan is read-only
  again post-Session-12-absorption-close):
  - "Probe framework generation before locking a fixture spec"
    (Session 7)
  - "Synthetic-fixture HTML comments are regex-visible"
    (Session 8)
  - "Detector precision findings" with FPs and FNs (Session 9)
  - "Audit-spec vs. production-reality drift" (Session 9)
  - "Verify-before-asking discipline" (Session 10; header naming
    + operator-ratchet + A/B/C trigger condition)
  - "Defer prose-only schema fixes; bump only when machine
    schema changes" (Session 11)
  - "Close-out claims-by-analogy in handoff documents"
    (Session 11 → Session 12-prep)
  - **NEW Session 12**: "Verify-before-asking discipline
    (extension)" — bidirectional pattern.
  - **NEW Session 12**: "Driver-level input contracts" —
    verify cascade input shape before scoping generation work.

Open latent gap (Issue 3 from Week 2 audit erratum, unchanged):
- Project's ruff `select` does not include "C" (mccabe), so
  cyclomatic-complexity violations escape pre-push. Manual
  `ruff check --select C901 <file>` in any code-modifying commit
  is the workaround until a project-config commit closes the
  gap. W4.1.5 driver will be the third code-modifying commit
  series; apply manual McCabe to each new module.

LLM cost drift risk (plan §11) — Session 12 update:
- W4.1.5 + W4.2 expected combined LLM cost: ~$0.30 ballpark per
  Claude Code Q3 verification 2026-05-21. Material caveats
  documented in `~/crawler-audit/working/phase4_current_state_2026-05-21.md`
  (token estimates ±25%; cache-hit assumption ≥80%; Stage 2
  page-acquisition short-circuit is engineering work W4.1.5
  builds). Stop and escalate if actual spend trends >3× the
  $0.30 estimate before $50 alert threshold. Cost ceiling $100
  untouched through Session 12 close ($0 incurred); budget
  remaining $100.

No new risks escalated and unresolved by Session 12.

---

## Deferred prose-only fixes (fold into next real schema bump)

These are text-only inconsistencies in locked schema artifacts
whose machine-readable schemas are unaffected. Per operator
Session 11 path-A resolution + LESSONS.md "Defer prose-only
schema fixes; bump only when machine schema changes", prose
corrections are NOT semver-bumped on their own; they ride the
next real schema bump's diff so the locked-artifact churn stays
minimal.

The register grew to six entries in Session 12 (three pre-existing
+ three new per RECONCILIATION_2026-05-21.md §6.2):

**Pre-existing (Session 11):**

- **(a) META_SCHEMA.md §2.4 line 95 + §5 line 149** (Session 11
  path-A finding): both say the C0.7c nginx-401 split lives in
  `parking_default_pages/`. Reality: C0.7c moved those 4 files
  OUT of `parking_default_pages/` INTO `auth_403/`. Machine
  schemas are silent on directory→response mapping; prose-only.

- **(b) META_SCHEMA.md §2.4 line 93 + §5 line 150** (Session 11
  Flag B resolution): strict reading says `captured_at` derives
  from the file's first-add commit via `--diff-filter=A --follow`.
  For `replaced_in_place` files the W4.1 generator extends the
  recipe to use the replacement commit author date as
  captured_at. Machine schema only says `format: date-time`;
  prose-only.

- **(c) META_SCHEMA.md §2.4 vocabulary extension** (Session 11
  Flag A option b): the `provenance_note` Recommended
  source-string vocabulary needs the new canonical value
  `approximated_from_synthetic_invalid_fallback`. Machine schema
  is `additionalProperties: {type: string}`; prose-only.

**New (Session 12 per RECONCILIATION_2026-05-21.md §6.2):**

- **(d) META_SCHEMA.md `tier_decided="parser_rule"` valid
  vocabulary entry** (Session 12 / Phase 4 PR-F partial
  implementation). PR-F partially landed adds the constant
  `TIER_PARSER_RULE = "parser_rule"` at
  `stage3/output_schema.py:53` and is recognized in
  result-counting at `stage3/run.py:791`, but no code path
  currently emits it (PR-F's parser pre-classifier is unstarted,
  blocked on PR-D). META_SCHEMA prose should list `parser_rule`
  as a valid `tier_decided` value for forward compatibility.

- **(e) `expected/<domain>.json` schema reconciliation against
  `stage3/output_schema.py:112-140` actual columns** (Session 12
  / RECONCILIATION_2026-05-21.md §6.1 Edit 5). META_SCHEMA prose
  currently references a `stage3_decision: {partner_type,
  confidence, tier}` shape. Actual columns differ; reconcile
  against PR-A's schema. The plan §3 Week 4 (W4.2) entry carries
  a TODO comment placeholder for this reconciliation, to be
  resolved at Session 13 open via repo read of `stage3/output_schema.py`.

- **(f) Output durability annotation** (Session 12 /
  RECONCILIATION_2026-05-21.md §6.1 Edit 5). META_SCHEMA prose
  should explicitly state that `expected/<domain>.json` outputs
  at W4.2 close have a known shorter-than-final lifetime: "until
  W A.0 W6 supersedes via baseline-v0 generation, OR until
  Phase 4 PR-E lands and Levers 2/3/7 change cascade behavior,
  whichever comes first." The plan §11 Risk Register entry
  "W4.2 expected-output lifetime constrained" carries the
  authoritative narrative; META_SCHEMA prose folds it in at the
  next semver bump.

All six fold into the eventual v1.1 machine-schema bump's diff.

---

## Cost & schedule tracking

- Cost ceiling: $100 (operator-set 2026-05-19, alert at $50)
- Cost incurred Sessions 1-12: $0 (Session 12 was governance-only;
  no LLM API calls; no repo modifications)
- Cost budget remaining: $100
- W4.1.5 + W4.2 combined expected spend: ~$0.30 LLM ballpark per
  Claude Code Q3 verification 2026-05-21. Material caveats:
  ±25% on per-call cost; ±50% on total feasible if cache hit
  rate is materially below 80%. Stop and escalate if actual
  W4.1.5/W4.2 spend trends >3× the $0.30 estimate before $50
  alert threshold.
- Schedule: ~3-4 weeks elapsed of Workstream 0's 5-week budget.
  - Weeks 1-3 COMPLETE.
  - Week 4 OPEN: W4.0 schema lock + W4.0 worked example + W4.1
    bulk meta.json all DONE; W4.1.5 fixture-cascade driver
    PROPOSED for Session 13; W4.2 expected outputs + W4.3 test
    infrastructure pending after W4.1.5 close. Likely spans
    Sessions 13-14, possibly 15.
  - Week 5 still ahead.
  - The W4.1.5 work unit pulls cascade-driver engineering ~2
    weeks forward from W A.0 W6 (per plan §4 W6 amendment per
    §6.1 Edit 6); Weeks 4-5 may extend ~1 week beyond the
    original 5-week plan, but W A.0 W6 budget gets the time
    back. Net schedule impact ~zero; surface shape changes.

---

## Notes for Session 13

- **Conformance test red count at handoff is 17** (Week 5 punch
  list, byte-stable through W4.1 landing and Session 12 governance-
  only close). Every Session 13 commit should verify the count
  stays at 17 unless the commit itself deliberately changes test
  infrastructure (W4.3 may legitimately shift counts when
  expected.json comparison replaces "exclusion_reason must be
  empty" assertions — document any deliberate shift in commit
  message).
- **2 conformance tests SKIP** (empty parametrize for `soft_404/`
  and `empty_google_sites/`) — both await Week 5 C0.3-followup /
  C0.4-followup repopulation.
- **The Session-12-close test surface is 17 fail / 169 pass / 2
  skip / 64 hard_exclusions pass.** Same as Session 11 close
  (Session 12 made no repo changes).
- **File-based commit messages** still mandatory: heredocs break
  on apostrophes. Use `Write` to `/tmp/<action-id>-msg.txt`,
  then `git commit -F /tmp/...`. Pattern in LESSONS.md.
- **"Confirm to commit?" gating** before every commit —
  established pattern.
- **Verify-before-asking discipline** — NAMED (LESSONS.md
  Session 10) + REINFORCED Session 11 + EXTENDED Session 12
  (bidirectional). Standard pre-commit verification set: file
  content re-read, schema conformance check (jsonschema strict),
  test surface invariant check, anti-trip scan on any synthetic
  test_purpose, byte-exact match for derived numeric fields,
  idempotency re-run, debug-artifact scan, scope-creep scan via
  `git status` outside bulk scope. Bidirectional check on any
  operator-issued multi-artifact state claim (Session 12
  pattern).
- **NEW Session 12 LESSONS.md additions**: "Verify-before-asking
  discipline (extension)" + "Driver-level input contracts" —
  applies forward to all W4.1.5 driver work + future synthetic-
  input work.
- **Pre-push gate** may include validate_consistency failure from
  operator-side eval_data work. The 4 unstaged operator-side
  files in the locked tree are documented and routinely pass the
  gate; if the gate fails, STOP and ask the operator. Never use
  `--no-verify`.
- **Plan is read-only again** — never edit
  `BARCADA_CRAWLER_REMEDIATION_PLAN.md`. The Session 12
  absorption was a one-shot break with explicit operator
  authorization; the file is closed to further amendments per
  operator convention. Any new amendment proposal must trigger
  another halt-and-reconcile-style operator authorization.
- **Shell cwd drift**: use absolute paths or `cd /Users/administrator/
  projects/barcada-scraper` at the start of each Bash chain.
- **Workspace cwd**: when editing LESSONS.md / SESSION_LOG.md /
  this template, work in `/Users/administrator/crawler-audit/`.
- **W4 tag pattern shifted**: per Session 12 sequencing decision,
  Week 4 no longer closes with a single `workstream-0-week4-end`
  tag. Instead: `workstream-0-week4-1-5-end` at W4.1.5 close;
  W4.2 / W4.3 follow without their own tags (Week 4 is closed
  conceptually at W4.3 complete; the bookkeeping marker is the
  W4.1.5 tag + SESSION_LOG.md entries marking W4.2 / W4.3
  completion). Operator may revisit at W4.3 close if a Week 4
  capstone tag is desired.
- **W4.1.5 driver location decision pending**: at Session 13
  design time, decide whether the driver lives at
  `tests/fixtures/fixture_cascade_driver.py` (sibling to
  `generate_meta_json.py`), `tools/fixture_cascade_driver.py`
  (clearly tooling, not tests), or under a workspace path like
  `~/crawler-audit/working/`. Surface the tradeoff to operator
  before code lands.
- **W4.1.5 worked-example handling**: the existing
  `tests/fixtures/html/legitimate_business/expected/twilio.com.json`
  carries a `_placeholder` parser_output marker (W4.0 schema-lock
  shape demo). W4.1.5 driver either replaces it with real
  cascade output OR protects it via `PROTECTED_PRE_EXISTING_*`
  analogous to the meta.json protection. Operator decides at
  Session 13 sample-review time.
- **This template's structured fields will need refilling at
  Session 13 close.**
