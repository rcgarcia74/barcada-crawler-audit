# Session Transition Template — Handoff from Session 24 → Session 25

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-24 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 25 invocation prompt:** not drafted at S24 close. Per the
S20→S21, S21→S22, S22→S23, S23→S24 precedent, prompt-drafting is
operator-commissioned between sessions, not always-on close-out
work. If operator wants a fresh prompt for S25, commission it as a
separate follow-up; otherwise scope S25 cold at session open using
this template + SESSION_LOG.md + LESSONS.md.

---

## Handoff metadata

- Outgoing session number: 24
- Closing date: 2026-05-24
- Outgoing session scope: durable bypass-audit persistence in
  worker_loop (Candidate I per S24 Phase 1). 3 per-module commits
  per Q-SHARED.1 (commit 1 bundles src + coupled test-fixture
  retargeting):
  `48c324a WA2.W8.bypass-persistence-worker-loop`,
  `00d5b38 WA2.W8.bypass-persistence-unit-tests`,
  `aa23712 WA2.W8.bypass-persistence-integration-extension`.
  Closes the S23 explicit deferral (production scrape_stage2_pages_
  invoker now persists BYPASS_ALLOW decisions to
  JournalState.robots_bypass_log via record_bypass_audit, with
  Q-I.1 file://-only scope + Q-I.6 log-and-continue failure
  semantics). No tag placed (1.TAG = defer; Candidate I is not a
  workstream-end milestone). LLM spend: $0.
- Reason for transition: S24 3-commit scope completed cleanly;
  durable persistence shipped end-to-end with 15 net-new tests
  (12 unit + 3 integration-extension). No in-flight sub-surface.
  One natural follow-on: abfss:// CostJournal Phase 5 promotion
  (S24 helper raises NotImplementedError on abfss://; ADLS
  skeleton in cost_journal_adls.py is the work).

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `aa23712` (WA2.W8.bypass-persistence-integration-extension).
- Last commit subject: "WA2.W8.bypass-persistence-integration-extension:
  tests/orchestrator/test_robots_gate_integration.py (extend S23
  integration test with 3 end-to-end tests through
  scrape_stage2_pages_invoker per S24 Q-I.7 leg 2; 947 combined;
  pins durable production-path persistence + Q-I.1 fail-loud-at-
  startup)"
- Branch sync with `origin/main`: 0 ahead / 0 behind (verified at
  Session 24 close after push at HEAD `aa23712`).
- Tags (10 total; unchanged from S22 close; do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3`
  - `workstream-0-week1-end` at `4f9d23f`
  - `workstream-0-week2-end` at `e5d2f91`
  - `workstream-0-week3-end` at `cf0c14c`
  - `workstream-0-week4-1-5-end` at `dd64963` (annotated)
  - `workstream-0-week4-end` at `b2e2671` (annotated)
  - `workstream-0-week5-end` at `ddd3cb0` (annotated)
  - `baseline-v0` at `9e9a1fb` (annotated)
  - `workstream-0-week7-end` at `ea37102` (annotated)
  - `workstream-a-week1-end` at `fdc8a7a` (annotated; placed S22)
- Pre-push gate state at HEAD `aa23712`: ALL CHECKS PASS (ruff +
  ruff format + vermin 3.10 + validate_consistency 0/0).
- Pre-S24 unstaged operator territory (Sessions 8-24 precedent —
  expected to stay unstaged across sessions): `eval_data/README.md`,
  `eval_data/TAXONOMY_GAP_LOG.md`, `eval_data/stage1_labels.jsonl`.
  S24 delta tolerated: operator committed `4bed9b9 step 3 labeling
  audit, cleanup` between S23 close and S24 open (strictly
  eval_data-only path stat; tolerated per "Workspace HEAD delta
  tolerance" LESSONS).
- Corpus: 222 .html fixtures (unchanged from S17 close).
- 202 expected.json files (unchanged).
- 222 meta.json files (unchanged).
- 1213 baseline-v0 files (unchanged from S18 close at `9e9a1fb`).
- NEW Session 24:
    - `tests/orchestrator/test_worker_loop_persistence.py`
      (325 LOC; 12 focused unit tests for the 3 new worker_loop
      helpers: 5 for `_open_cost_journal_for_worker` + 3 for
      `_ensure_journal_initialized` + 4 for
      `_build_durable_bypass_writer`).
- MODIFIED Session 24:
    - `src/barcada_scraper/orchestrator/worker_loop.py` (+115 /
      -21 lines; 3 new module-level helpers near
      `scrape_stage2_pages_invoker` + closure replacement).
        - `_open_cost_journal_for_worker(config: WorkerConfig) ->
          CostJournal`
        - `_ensure_journal_initialized(journal: CostJournal, *,
          run_id: str) -> None`
        - `_build_durable_bypass_writer(journal: CostJournal) ->
          Callable[[GateDecision], None]`
        - The S23 log-only `_bypass_audit_writer` closure body is
          replaced by a 3-line wiring block that opens the journal,
          self-bootstraps if needed, and builds the durable writer.
    - `tests/orchestrator/test_worker_loop.py` (+21 / -5 lines;
      5 PRE-EXISTING test_stage2_pages_invoker_* fixtures retargeted
      from `abfss://` to `file://{tmp_path}/cost.jsonl` to satisfy
      the new Q-I.1 precondition. No new tests in this file; no
      assertion changes.).
    - `tests/orchestrator/test_robots_gate_integration.py` (+170 /
      -1 lines; 3 new end-to-end tests appended after the 4 S23
      tests, plus import block additions at the top: json,
      WorkerConfig, ShardMessage, scrape_stage2_pages_invoker.
      The 4 S23 tests stay UNMODIFIED at their landed shape.).
- (Unchanged from S23 close, all locked):
    - `src/barcada_scraper/scraper/robots.py` (S21 parser at `34a59b6`)
    - `tests/scraper/test_robots.py` (32 tests)
    - `src/barcada_scraper/scraper/robots_gate.py` (S22 shim at
      `ba87e7e`)
    - `src/barcada_scraper/scraper/robots_bypass_config.py` (S22
      loader at `381ee89`)
    - `tests/scraper/test_robots_gate.py` (30 tests)
    - `tests/scraper/test_robots_bypass_config.py` (30 tests)
    - `src/barcada_scraper/classifier/pipeline/cost_journal.py`
      (S22 surface at `1d9404e`; S24 CONSUMES
      `JournalAlreadyExistsError`, `JournalState`, `open_journal`,
      `record_bypass_audit` via robots_integration but DOES NOT
      modify cost_journal.py)
    - `src/barcada_scraper/classifier/pipeline/cost_journal_local.py`
      (LocalFSCostJournal; S24 CONSUMES the public API via
      `open_journal` factory but does NOT modify)
    - `src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
      (Phase 5 SKELETON; raises NotImplementedError with "Phase 5
      deliverable" marker. S24 verified at Phase 0 that the
      skeleton marker is intact. Promoting this skeleton is the
      natural S25 follow-on for abfss:// support.)
    - `docs/CRAWLING_POLICY.md` (S22 doc at `fdc8a7a`)
    - `tools/synthetic_crawl/`, `tools/baseline_v0/canary.py`,
      `tests/synthetic_crawl/`, `tests/baseline_v0/test_canary.py`,
      `tests/fixtures/synthetic_crawls/`, `scripts/launchd/` (S20
      deliverables)
    - All S23 deliverables (orchestrator/robots_integration.py
      @ `279bb77`; tests/orchestrator/test_robots_integration.py;
      vmss_worker.py + job_runner.py + cloud_init.template.yaml
      additions; the 4 S23 tests in test_robots_gate_integration.py).
- Combined test suite at HEAD `aa23712`:
    - **947 passed / 0 failed / 0 skipped** with the 16-path
      invocation (S24 canonical S25-baseline below).
    - 605 passed when restricted to `tests/orchestrator/` only
      (152 + 74 + 129 + 35 + 7 + 12 + plus shared baselines).
    - 480 passed when restricted to the S22 headline-suite paths
      (no orchestrator/, no journal-suite ride-along).
    - 538 passed for the broader S22 headline + journal-suite.
    - 932 passed for the S23-baseline 15-path invocation
      (without the new test_worker_loop_persistence.py file).

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 24 start: `b80e31e` (S24 prompt v2
  with 8 reviewer findings folded; 2 commits ahead of S23 close-out
  primary `8d99c98` due to prompt-drafting + reviewer-findings
  audit — matched the S20-S23 precedent for prompt-drafting between
  sessions).
- Session 24 close-out workspace commits: 1 primary + 1 follow-up
  (expected). After this primary commit lands, a follow-up commit
  pins the S25 Phase 0 workspace anchor SHA + any audit-surfaced
  corrections.
- **Last commit SHA at Session 24 CLOSE: the follow-up commit
  pinning the anchor** (the SHA below comes from the follow-up,
  not from the primary close-out). S25 prompt's Phase 0 Step 0.1
  MUST anchor workspace expectation to THIS follow-up's SHA.
  Per S21-S23 LESSONS pattern "Workspace HEAD delta tolerance":
  tolerate N additional prompt-drafting / audit-correction commits
  between sessions; verify each is consistent with that pattern
  before continuing.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected
  after Session 24 close push.

---

## Session 25 execution order (enforce strict sequence)

Same N-phase shape applies regardless of scope choice (Phase 0
cold-start verify → Phase 1 scope → Phase 2 design-gate → Phase 3
impl → Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 25 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 24 entry.
3. Reading the LESSONS.md additions Session 24 landed (5 new
   sections at end of file, "S24 folding" suffix).
4. Reading the relevant section of BARCADA_CRAWLER_
   REMEDIATION_PLAN.md for the chosen Session 25 scope (see
   "Notes for Session 25" below).
5. Reading the Session 25 prompt if one has been drafted, OR
   commissioning a fresh draft at S25 open.
6. Running Phase 0 cold-start verification per the prompt's
   protocol (or per the S24 prompt template if S25 prompt is
   not yet drafted).

---

## Outstanding operator-input requests entering Session 25

1. **Session 25 scope choice** — pick from the candidates in
   "Notes for Session 25" below. Candidate I closed at S24; the
   natural follow-on is the abfss:// promotion (Candidate J
   below) but A/B/D/E/H carry-forward candidates also remain
   available.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*.jsonl` continue across sessions (Sessions 8-24
   precedent). S24 saw `4bed9b9` (operator-side step-3 labeling
   audit + cleanup) commit pre-session and was tolerated under
   the eval_data-only path stat check. validate_consistency
   stayed green throughout S24.

3. **barcada-drift AI/ML alignment** — unchanged from S21-S24
   handoffs. If operator wants to ship `barcada-drift` in S25,
   the 4 AI/ML team decisions need to be pre-resolved OR scoped
   narrowly with placeholders. Plus the prereq of 2+ parquet
   files (earliest natural date 2026-06-06).

4. **launchd kit installation** — S20 shipped
   `scripts/launchd/install_canary_schedule.sh` as files-only;
   operator should run the installer when ready to enable the
   weekly Saturday-9am canary job. Required prerequisite for
   Candidate A (barcada-drift needs 2+ canary_runs/*.parquet
   artifacts to exist).

5. **Session 25 prompt draft commissioning** — operator decides
   whether to commission an S25 prompt between sessions or scope
   one at S25 open.

---

## Notes for Session 25

Suggested S25 scope candidates (operator picks at S25 open):

### Candidate J (NEW): abfss:// CostJournal Phase 5 promotion

The natural follow-on to S24 Candidate I. S24's
`_open_cost_journal_for_worker` currently raises NotImplementedError
on abfss:// URLs with a "Phase 5 deliverable" marker. The
`ADLSCostJournal` skeleton in
`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
needs to be promoted to a real backend matching the LocalFSCostJournal
public API (`read`, `write_initial`, `try_update`, `exists`).
Then the abfss:// guard in `_open_cost_journal_for_worker` is
removed so abfss:// URLs flow through `open_journal` to the new
ADLS backend.

Estimated 150-250 LOC of src/ changes (ADLSCostJournal completion)
+ 100-200 LOC of test code (azure-storage-blob mock against an
Azurite container or fsspec-adls stub) + ~5 LOC removal of the
abfss:// guard in worker_loop.py.

Prereqs:
- Azure storage SDK / fsspec-adls dependency availability (already
  pulled in elsewhere; verify imports).
- Decision on test posture: real Azurite container vs fsspec mock
  vs DummyADLS in-memory. The S23 LESSONS "Production-vs-test
  journal asymmetry" pattern applies here too — keep test posture
  deterministic.
- Source-verify the skeleton's existing methods + the ETag protocol
  it sketches before drafting Phase 2 design gates.

### Candidate A (carry-forward): `barcada-drift` skeleton

Unchanged from S21-S24 handoffs. Per CLASSIFICATION_ADJACENT_PLAN.md
§Item 8. Consumes `canary_runs/<date>.parquet` artifacts.
**Blocked**: 2+ parquet files needed (launchd installer not yet
run as of S24 close; earliest natural date 2026-06-06).
Estimated ~300 LOC.

### Candidate B (carry-forward): Per-tier cost-accounting retrofit

Unchanged from S21-S24 handoffs. Closes Workstream 0; warrants
`workstream-0-end` tag. Touches W4.1.5 driver area (locked except
via W5.X-prefix commits). Estimated 100-200 LOC.

### Candidate D (carry-forward): Phase 4 PR-D operator-led labeling

Unchanged. Tooling support only; labeling itself is operator
territory.

### Candidate E (carry-forward): Cassette corpus expansion

Unchanged from S22-S24 handoffs. S20 shipped 20 cassettes; plan's
upper bound is 30. Could expand or curate.

### Candidate H (carry-forward small): CRAWLING_POLICY.md tightening

Unchanged from S22-S24 handoffs. Q-F.6's "minimal-first" estimate
cited ~1-2 KB; S22 shipped 8.1 KB. If operator prefers a tighter
doc, a small follow-up session could trim to ~2-3 KB while
preserving the essential robots-compliance contract. Estimated
<50 LOC of doc changes; no code.

---

## Required reading (Session 25 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 24 entry — 3-commit narrative;
   the Phase 2 Q-I.1 through Q-I.7 design-gate decisions; the
   commit-1 bisectability bundling; the test fixture retargeting
   pattern.
3. **`LESSONS.md`** — 5 new sections appended at S24 close
   (Tightened-precondition test-fixture retargeting / Test
   against public API surface only / Q-I.7 "Both" test corpus
   shape works for small candidates / Q-I.6 "log + continue"
   closure-failure pattern / Workspace HEAD delta tolerance —
   eval_data-only path).
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope
   section per Session 25 candidate choice. Plan is READ-ONLY.
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A (barcada-drift) is chosen.
6. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   — only if Candidate J (abfss:// promotion) is chosen. The
   Phase 5 skeleton with NotImplementedError + "Phase 5
   deliverable" marker is what Candidate J completes.
7. **`src/barcada_scraper/classifier/pipeline/cost_journal_local.py`**
   — only if Candidate J is chosen. The LocalFSCostJournal is
   the reference implementation Candidate J mirrors against
   ADLS (`exists` / `read` / `write_initial` / `try_update` API
   contract; ETag semantics via SHA-256 hash; lock semantics
   via fcntl).
8. **`src/barcada_scraper/orchestrator/worker_loop.py`** — only
   if Candidate J is chosen. The abfss:// guard at
   `_open_cost_journal_for_worker` is the seam Candidate J
   removes once ADLSCostJournal is real.
9. **`tests/classifier/pipeline/test_cost_journal_adls.py`** —
   only if Candidate J is chosen. The 2 existing tests pin the
   skeleton contract; Candidate J expands the file with full
   coverage of the new backend.
10. **`docs/CRAWLING_POLICY.md`** — only if Candidate H is chosen.

---

## Outstanding items carried forward to Session 25+

1. **Per-tier cost-accounting wiring gap** — carry-forward from
   S14; severity LOW. Unchanged disposition.

2. **`barcada-drift` CLI** — CLASSIFICATION_ADJACENT_PLAN.md
   §Item 8; 4 AI/ML team decisions outstanding. Blocked also
   on 2+ canary_runs parquet files. Unchanged.

3. **Cassette corpus expansion** — current 20 domains is lower
   bound of plan's "~20-30". Unchanged.

4. **Cassette-FP investigation** — archive.org + hashicorp.com
   flagged as SaaS-shell FPs in S20's FP-curation log. Unchanged.

5. **launchd kit smoke-then-install** — Unchanged. Operator
   should run `scripts/launchd/install_canary_schedule.sh` to
   enable the weekly job. Required for Candidate A.

6. **Phase 4 PR-D/E/F/G** (forward look) — Unchanged. Opens
   after Workstream 0 fully closes AND operator-led Stage 2 +
   Stage 3 labeling work begins.

7. **CRAWLING_POLICY.md size** — Unchanged. Doc shipped at
   8.1 KB vs Q-F.6's ~1-2 KB estimate. See Candidate H above.

8. **abfss:// CostJournal Phase 5 promotion** — NEW from S24.
   S24's `_open_cost_journal_for_worker` raises NotImplementedError
   with the "Phase 5 deliverable" marker on any abfss:// URL.
   The ADLSCostJournal skeleton in
   `src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
   needs to be completed. See Candidate J above.

---

## Locked artifact reminders for Session 25

Carry-forward from Sessions 8-24:

- `eval_data/` — labeling-workstream territory. Operator-WIP
  edits across sessions are expected. Pre-push validate_
  consistency runs against WT state; surface per LESSONS pattern
  if blocked.
- `stage1.schema.json` v1.0 with 49 keywords.
- `pre-remediation-2026-05-19` tag.
- `baseline-v0` tag at `9e9a1fb`.
- All `workstream-0-*` tags at their placed SHAs (9 tags from
  S20 close; unchanged).
- `workstream-a-week1-end` tag at `fdc8a7a` (placed S22).
- `tests/runners/fixture_cascade/` — W4.1.5 driver locked at
  `dd64963` except via W5.X-prefix commits.
- `tests/fixtures/baseline-v0/` snapshot — locked at `9e9a1fb`.
- `tools/baseline_v0/check.py`, `generate.py`, `determinism.py`,
  `canary.py` — S18-20 deliverables; locked.
- `tools/synthetic_crawl/` package — S20 deliverable; locked.
- `tests/fixtures/synthetic_crawls/` — S20 corpus; locked.
- `scripts/launchd/` — S20 deliverable; locked.
- `src/barcada_scraper/scraper/robots.py` — S21 deliverable;
  locked at `34a59b6`.
- `tests/scraper/test_robots.py` — S21 deliverable; locked at
  `34a59b6`.
- `src/barcada_scraper/scraper/robots_gate.py` — S22 deliverable;
  locked at `ba87e7e`.
- `src/barcada_scraper/scraper/robots_bypass_config.py` — S22
  deliverable; locked at `381ee89`.
- `tests/scraper/test_robots_gate.py` — S22 deliverable.
- `tests/scraper/test_robots_bypass_config.py` — S22 deliverable.
- `src/barcada_scraper/classifier/pipeline/cost_journal.py` —
  S22-extended at `1d9404e`. Candidate J (if chosen) does NOT
  modify this file directly; cost_journal_adls.py is the work
  surface.
- `src/barcada_scraper/classifier/pipeline/cost_journal_local.py`
  — production local-FS backend; locked. Candidate J mirrors its
  API contract against ADLS but does NOT modify it.
- `docs/CRAWLING_POLICY.md` — S22 deliverable; locked at
  `fdc8a7a`.
- `src/barcada_scraper/orchestrator/robots_integration.py` —
  S23 deliverable; locked at `279bb77`. Candidate J CONSUMES
  `record_bypass_audit` but does NOT modify.
- `tests/orchestrator/test_robots_integration.py` — S23
  deliverable; locked at `279bb77`. 35 tests.
- The 4 S23 tests in
  `tests/orchestrator/test_robots_gate_integration.py` — locked
  at `6e6e4ca`. S24 appended 3 new tests after these 4; the 3
  S24-added tests are locked at `aa23712`. Adding new tests is
  allowed; modifying landed tests requires explicit authorization.
- `src/barcada_scraper/orchestrator/vmss_worker.py` (full surface)
  — S23 additions locked at `5eeaac7`; pre-S23 surfaces locked
  as before. Candidate J does NOT modify.
- `src/barcada_scraper/orchestrator/job_runner.py` — S23
  additions locked at `872527e`. Candidate J does NOT modify.
- `scripts/vmss/cloud_init.template.yaml` — S23 additions locked.
- **NEW S24 LOCKS**: the 3 module-level helpers in
  `src/barcada_scraper/orchestrator/worker_loop.py`
  (`_open_cost_journal_for_worker`, `_ensure_journal_initialized`,
  `_build_durable_bypass_writer`) are locked at `48c324a`.
  Candidate J REMOVES the abfss:// guard in
  `_open_cost_journal_for_worker` but preserves the surrounding
  helper structure + public signatures.
- **NEW S24 LOCKS**: `tests/orchestrator/test_worker_loop_persistence.py`
  — S24 deliverable; locked at `00d5b38`. 12 tests. Adding new
  tests is allowed; modifying landed tests requires explicit
  authorization. Candidate J updates
  `test_open_cost_journal_abfss_raises_not_implemented_with_phase5_marker`
  (if the abfss:// guard is removed). That update is allowed only
  under explicit Phase 2 authorization.
- **NEW S24 LOCKS**: the 5 retargeted test_stage2_pages_invoker_*
  fixtures in `tests/orchestrator/test_worker_loop.py` — landed
  at `48c324a`. Do NOT revert to abfss://.
- `docs/phase4_implementation_plan.md` — Phase 4 governance
  reference; do NOT modify until Phase 4 work is operator-
  authorized.
- Production code under `src/barcada_scraper/` — locked unless
  Phase 2 design-gate explicitly authorizes a specific module.
  S21+S22+S23+S24 authorized: `scraper/robots.py`,
  `scraper/robots_gate.py`, `scraper/robots_bypass_config.py`,
  `classifier/pipeline/cost_journal.py` (additive only),
  `orchestrator/robots_integration.py` (new),
  `orchestrator/vmss_worker.py` (additive),
  `orchestrator/job_runner.py` (additive),
  `orchestrator/worker_loop.py` (additive: S23 gate wiring +
  S24 durable persistence helpers). No other src/ module is
  authorized.
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-25-open baseline

Canonical (16 paths; mirrors S24-close invocation):

```
.venv/bin/python -m pytest \
    tests/scraper/test_fixture_conformance.py \
    tests/runners/fixture_cascade/ \
    tests/baseline_v0/ \
    tests/synthetic_crawl/ \
    tests/scraper/test_robots.py \
    tests/scraper/test_robots_gate.py \
    tests/scraper/test_robots_bypass_config.py \
    tests/classifier/pipeline/test_cost_journal.py \
    tests/classifier/pipeline/test_cost_journal_local.py \
    tests/classifier/pipeline/test_cost_journal_adls.py \
    tests/orchestrator/test_robots_integration.py \
    tests/orchestrator/test_vmss_worker.py \
    tests/orchestrator/test_job_runner.py \
    tests/orchestrator/test_worker_loop.py \
    tests/orchestrator/test_robots_gate_integration.py \
    tests/orchestrator/test_worker_loop_persistence.py -q
# Expected: 947 passed / 0 failed / 0 skipped
```

Sub-totals: 210 conformance + 46 driver + 99 baseline_v0 + 33
synthetic_crawl + 32 robots + 30 robots_gate + 30 robots_bypass_config
+ 43 cost_journal + 13 cost_journal_local + 2 cost_journal_adls +
35 robots_integration + 74 vmss_worker + 129 job_runner + 152
worker_loop + 7 robots_gate_integration (4 pre-S24 + 3 new) +
12 worker_loop_persistence = 947.

Cumulative-test-count gate: the count NEVER decreases between
commit boundaries.

Narrower baselines (still valid for S25 candidates that don't
exercise the new test paths):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 932 (S23-baseline 15-path; no test_worker_loop_persistence)

Choose at Phase 0 Step 0.5 per Candidate selection.

---

## Pre-push gate at Session 25 open

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 351+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

Note on gate 4: validate_consistency runs against working-tree
state; if operator-WIP in eval_data introduces a schema violation
between S24 close and S25 open, the gate will block even though
no S25 commit touches eval_data. Per LESSONS: surface to operator
with the row+detail, propose operator-fix or stash-and-restore;
do NOT auto-fix.

---

## Context-window awareness

Session 24 ran across 3 commits + Phase 2 source-verification +
1 mid-Phase-3 fixture-retargeting adjustment, well within context.
Session 25 budget per chosen candidate:

- Candidate J (abfss:// promotion): 150-250 LOC src/ + 100-200
  LOC tests. Medium scope; multi-commit per-module.
- Candidate B (per-tier cost-accounting): touches W4.1.5 area;
  more careful Phase 0 verification needed.
- Candidate A (barcada-drift): only if launchd job has run ≥2
  times AND AI/ML decisions ready.
- Candidate H (doc tightening): very small; <30 minutes.
- Candidate E (cassette corpus expansion): depends on operator
  curation choices.

Strategies (unchanged from S20-S24 prompts):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-HTTP corpus work, pilot 1-3 before full N-domain.
- Source-verify line numbers per Phase 3 commit, not just at
  Phase 2 (S23 LESSONS pattern).
- Test against public API surface only — probe `.path.parent` /
  `.path.name` not private `_journal_dir` / `_run_id` attrs
  (S24 LESSONS pattern).

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S25 scope closes,
  transition per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-24:

1. Commit SHA(s) of each Session 25 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 947 baseline → S25 close.
4. Driver suite count (46/46 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (e.g., does S25 warrant a new tag?
   Candidate J alone — completing the ADLS skeleton — is not
   a workstream-end milestone; defer is the safe default).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 24 handoff template. Refill at Session 25 close
for Session 26.
