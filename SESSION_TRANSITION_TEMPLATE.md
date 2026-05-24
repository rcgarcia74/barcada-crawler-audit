# Session Transition Template — Handoff from Session 23 → Session 24

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-23 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 24 invocation prompt:** not drafted at S23 close. Per the
S20→S21, S21→S22, S22→S23 precedent, prompt-drafting is operator-
commissioned between sessions, not always-on close-out work. If
operator wants a fresh prompt for S24, commission it as a separate
follow-up; otherwise scope S24 cold at session open using this
template + SESSION_LOG.md + LESSONS.md.

---

## Handoff metadata

- Outgoing session number: 23
- Closing date: 2026-05-23
- Outgoing session scope: W A.2 worker_loop / fetcher_core
  integration (Candidate G per S23 Phase 1). 5 per-module commits
  per Q-SHARED.1:
  `279bb77 WA2.W8.robots-integration-helpers`,
  `5eeaac7 WA2.W8.vmss-worker-bypass-env`,
  `872527e WA2.W8.job-runner-bypass-cli`,
  `4ec7b0a WA2.W8.worker-loop-gate-wiring`,
  `6e6e4ca WA2.W8.robots-gate-integration-test`.
  Ships end-to-end W A.2 (orchestrator wiring of RobotsGate at
  3 pre-fetch sites + CLI/env config plumbing + integration test).
  No tag placed (1.TAG = defer; W A.2 alone is not a workstream-end
  milestone). LLM spend: $0.
- Reason for transition: S23 5-commit scope completed cleanly;
  W A.2 shipped end-to-end with integration test pinning the
  Q-G.4 journal-write contract. No in-flight sub-surface. One
  explicit deferral: production-durable bypass-audit persistence
  in worker_loop (see "Outstanding items" below).

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `6e6e4ca` (WA2.W8.robots-gate-integration-test).
- Last commit subject: "WA2.W8.robots-gate-integration-test:
  tests/orchestrator/test_robots_gate_integration.py (in-process
  tmp_path end-to-end ALLOW / SKIP / BYPASS_ALLOW + ETag-advance
  per S23 Q-G.4 / Q-G.8; 4 new tests; 928 -> 932 combined)"
- Branch sync with `origin/main`: 0 ahead / 0 behind (verified at
  Session 23 close after push).
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
- Pre-push gate state at HEAD `6e6e4ca`: ALL CHECKS PASS (ruff +
  ruff format + vermin 3.10 + validate_consistency 0/0).
- Pre-S23 unstaged operator territory (Sessions 8-22 precedent —
  expected to stay unstaged across sessions): `eval_data/README.md`,
  `eval_data/TAXONOMY_GAP_LOG.md`, `eval_data/stage1_labels.jsonl`.
  S23 deviation: operator committed `eval_data/{stage1_labels,
  README, TAXONOMY_GAP_LOG}` modifications at `2fc4d8e` between S22
  close and S23 open. Out-of-scope territory either way.
- Corpus: 222 .html fixtures (unchanged from S17 close).
- 202 expected.json files (unchanged).
- 222 meta.json files (unchanged).
- 1213 baseline-v0 files (unchanged from S18 close at `9e9a1fb`).
- NEW Session 23:
    - `src/barcada_scraper/orchestrator/robots_integration.py`
      (244 LOC; W A.2 helpers: build_robots_gate,
      prewarm_robots_for_url, make_robots_disallow_row_fields,
      record_bypass_audit, load_bypass_config_or_empty).
    - `tests/orchestrator/test_robots_integration.py` (512 LOC;
      35 tests).
    - `tests/orchestrator/test_robots_gate_integration.py`
      (331 LOC; 4 in-process tmp_path integration tests
      pinning end-to-end ALLOW / SKIP / BYPASS_ALLOW + ETag
      advance via update_with_retry).
- MODIFIED Session 23:
    - `src/barcada_scraper/orchestrator/vmss_worker.py` (+17 lines;
      new optional `WorkerConfig.robots_bypass_config_path` field
      + reader for `BARCADA_ROBOTS_BYPASS_CONFIG` env var).
    - `src/barcada_scraper/orchestrator/job_runner.py` (+29 lines;
      new `JobRunArgs.robots_bypass_config_path` field +
      `--robots-bypass-config` CLI flag + new kwarg + substitution
      entry in `render_cloud_init` + both call sites updated).
    - `src/barcada_scraper/orchestrator/worker_loop.py`
      (+109 / -2 lines; new `bypass_config` + `bypass_audit_writer`
      kwargs on `_acquire_one_domain_t1` + per-domain gate
      construction + prewarm + 3-site wiring + scrape_stage2_pages_
      invoker plumbing with log-only writer).
    - `scripts/vmss/cloud_init.template.yaml` (+10 lines; new
      `${BARCADA_ROBOTS_BYPASS_CONFIG}` placeholder + `-e` line).
    - `tests/orchestrator/test_vmss_worker.py` (+65 lines; 7 new tests).
    - `tests/orchestrator/test_job_runner.py` (+131 lines; 8 new tests).
    - `tests/orchestrator/test_worker_loop.py` (+348 lines; 6 new tests).
- (Unchanged from S22 close, all locked):
    - `src/barcada_scraper/scraper/robots.py` (S21 parser at `34a59b6`)
    - `tests/scraper/test_robots.py` (32 tests)
    - `src/barcada_scraper/scraper/robots_gate.py` (S22 shim at
      `ba87e7e`)
    - `src/barcada_scraper/scraper/robots_bypass_config.py` (S22
      loader at `381ee89`)
    - `tests/scraper/test_robots_gate.py` (30 tests)
    - `tests/scraper/test_robots_bypass_config.py` (30 tests)
    - `src/barcada_scraper/classifier/pipeline/cost_journal.py`
      (S22 surface at `1d9404e`; S23 CONSUMES via
      `with_robots_bypass_appended` + `update_with_retry` but DOES
      NOT modify)
    - `docs/CRAWLING_POLICY.md` (S22 doc at `fdc8a7a`)
    - `tools/synthetic_crawl/`, `tools/baseline_v0/canary.py`,
      `tests/synthetic_crawl/`, `tests/baseline_v0/test_canary.py`,
      `tests/fixtures/synthetic_crawls/`, `scripts/launchd/` (S20
      deliverables)
- Combined test suite at HEAD `6e6e4ca`:
    - **932 passed / 0 failed / 0 skipped** with the 15-path
      invocation (S23 canonical S24-baseline below).
    - 593 passed when restricted to `tests/orchestrator/` only.
    - 480 passed when restricted to the S22 headline-suite paths
      (no orchestrator/, no journal-suite ride-along).
    - 538 passed for the broader S22 headline + journal-suite.

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 23 start: `577a70b` (utility scripts
  for labeling audit; 3 commits ahead of the S23 prompt's expected
  `8e6a7de` due to S22 close-out follow-up + S23 prompt drafting +
  prompt v2 audit + labeling utilities — matched the S20/S21/S22
  precedent for prompt-drafting between sessions).
- Session 23 close-out workspace commits will be 1 (primary close-
  out) + 1 follow-up pinning the S24 anchor SHA.
- **Last commit SHA at Session 23 CLOSE: <pinned by follow-up
  commit>**. S24 prompt's Phase 0 Step 0.1 MUST anchor workspace
  expectation to that SHA (NOT to the primary close-out commit's
  SHA, which the follow-up succeeds). Per S21+S22 LESSONS pattern
  "Workspace HEAD delta tolerance": tolerate N additional prompt-
  drafting / audit-correction commits between sessions; verify
  each is consistent with that pattern before continuing.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected
  after Session 23 close push.

---

## Session 24 execution order (enforce strict sequence)

Same N-phase shape applies regardless of scope choice (Phase 0
cold-start verify → Phase 1 scope → Phase 2 design-gate → Phase 3
impl → Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 24 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 23 entry.
3. Reading the LESSONS.md additions Session 23 landed (5 new
   sections at end of file, "S23 folding" suffix).
4. Reading the relevant section of BARCADA_CRAWLER_
   REMEDIATION_PLAN.md for the chosen Session 24 scope (see
   "Notes for Session 24" below).
5. Reading the Session 24 prompt if one has been drafted, OR
   commissioning a fresh draft at S24 open.
6. Running Phase 0 cold-start verification per the prompt's
   protocol (or per the S23 prompt template if S24 prompt is
   not yet drafted).

---

## Outstanding operator-input requests entering Session 24

1. **Session 24 scope choice** — pick from the candidates in
   "Notes for Session 24" below. W A.2 closed at S23 with one
   explicit production-persistence deferral; the natural follow-on
   is to close that deferral (Candidate I below). Carry-forward
   candidates A/B/D/E/H also remain available.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*.jsonl` continue across sessions (Sessions 8-23
   precedent). S23 saw operator-side eval_data commits +
   active labeling work mid-session (multiple WIP file
   creations/deletions). validate_consistency stayed green
   throughout.

3. **barcada-drift AI/ML alignment** — unchanged from S21/S22/S23
   handoff. If operator wants to ship `barcada-drift` in S24, the
   4 AI/ML team decisions need to be pre-resolved OR scoped
   narrowly with placeholders. Plus the prereq of 2+ parquet
   files (earliest natural date 2026-06-06).

4. **launchd kit installation** — S20 shipped
   `scripts/launchd/install_canary_schedule.sh` as files-only;
   operator should run the installer when ready to enable the
   weekly Saturday-9am canary job. Required prerequisite for
   Candidate A (barcada-drift needs 2+ canary_runs/*.parquet
   artifacts to exist).

5. **Session 24 prompt draft commissioning** — operator decides
   whether to commission a S24 prompt between sessions or scope
   one at S24 open.

---

## Notes for Session 24

Suggested S24 scope candidates (operator picks at S24 open):

### Candidate I (NEW): durable bypass-audit persistence in worker_loop

The lone explicit deferral from S23. worker_loop's
`scrape_stage2_pages_invoker` currently wires a log-only
`bypass_audit_writer` (LOG.warning per BYPASS_ALLOW). Closing
the gap requires:
- Opening a `CostJournal` handle at worker boot from
  `config.cost_journal_url` (parsing `abfss://acct/path/run_XXX.json`
  or `file://path/run_XXX.json` into journal_dir + run_id).
- Replacing the log-only writer with `record_bypass_audit(journal=
  journal, decision=decision)` so BYPASS_ALLOW decisions persist
  durably to `JournalState.robots_bypass_log` via
  `update_with_retry` (Q-G.4 protocol; commit 5's integration test
  already pins this end-to-end with LocalFSCostJournal in tmp_path).
- Handling the "journal not yet initialized" case at worker boot —
  call `j.write_initial(JournalState.fresh(...))` first or detect
  via `j.exists()`. Coordination needed with the existing
  orchestrator-side journal initialization (classifier/cli.py
  reads/writes the same journal).
- Tests: extend the S23 integration test or add a parallel one
  driving `scrape_stage2_pages_invoker` end-to-end with a real
  LocalFSCostJournal-backed worker.

Estimated 50-100 LOC. Touches:
- `src/barcada_scraper/orchestrator/worker_loop.py` (replace the
  log-only writer in scrape_stage2_pages_invoker)
- Possibly new helper in `orchestrator/robots_integration.py` or
  `classifier/pipeline/cost_journal.py` for the URL→handle parse
- Tests in `tests/orchestrator/test_worker_loop.py` +/- a new
  integration-style test

Prereqs: S23 deliverables stay locked at their landed SHAs (all
4 S22 surfaces + the 5 S23 surfaces). Decision on how to handle
the abfss:// case at worker boot (S23 integration test only
exercises LocalFSCostJournal in tmp_path).

### Candidate A (carry-forward): `barcada-drift` skeleton

Unchanged from S23 handoff. Per CLASSIFICATION_ADJACENT_PLAN.md
§Item 8. Consumes `canary_runs/<date>.parquet` artifacts.
**Blocked**: 2+ parquet files needed (launchd installer not yet
run as of S23 close; earliest natural date 2026-06-06).
Estimated ~300 LOC.

### Candidate B (carry-forward): Per-tier cost-accounting retrofit

Unchanged from S21/S22/S23 handoff. Closes Workstream 0;
warrants `workstream-0-end` tag. Touches W4.1.5 driver area
(locked except via W5.X-prefix commits). Estimated 100-200 LOC.

### Candidate D (carry-forward): Phase 4 PR-D operator-led labeling

Unchanged. Tooling support only; labeling itself is operator
territory.

### Candidate E (carry-forward): Cassette corpus expansion

Unchanged from S22/S23 handoff. S20 shipped 20 cassettes; plan's
upper bound is 30. Could expand or curate.

### Candidate H (carry-forward small): CRAWLING_POLICY.md tightening

Unchanged from S22/S23 handoff. Q-F.6's "minimal-first" estimate
cited ~1-2 KB; S22 shipped 8.1 KB. If operator prefers a tighter
doc, a small follow-up session could trim to ~2-3 KB while
preserving the essential robots-compliance contract. Estimated
<50 LOC of doc changes; no code.

---

## Required reading (Session 24 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 23 entry — 5-commit narrative;
   the Phase 2 design-gate decisions; the commit-2-bisectability
   adjustment; the production-vs-test journal asymmetry; the
   integration-test contract.
3. **`LESSONS.md`** — 5 new sections appended at S23 close
   (Bisectability vs Phase-1-named commit shape / Production-vs-
   test journal asymmetry / Source-verify line numbers per Phase 3
   commit / Cumulative test-count gate with new-file invocation
   expansion / False-premise verification questions).
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope
   section per Session 24 candidate choice. Plan is READ-ONLY.
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A (barcada-drift) is chosen.
6. **`src/barcada_scraper/orchestrator/robots_integration.py`** —
   only if Candidate I (durable persistence) is chosen.
   Especially `record_bypass_audit` (line ~165) which is what
   the Candidate-I writer would call.
7. **`src/barcada_scraper/orchestrator/worker_loop.py`** — only
   if Candidate I is chosen. The integration site for the new
   writer is in `scrape_stage2_pages_invoker` at the
   `_bypass_audit_writer` closure (~line 2117 post-S23).
8. **`src/barcada_scraper/classifier/pipeline/cost_journal.py`** —
   only if Candidate I is chosen. `open_journal` (factory) and
   `LocalFSCostJournal` / `ADLSCostJournal` (Phase 5 skeleton).
9. **`tests/orchestrator/test_robots_gate_integration.py`** —
   only if Candidate I is chosen. The S23 commit-5 integration
   test pins the contract Candidate I extends to production.
10. **`docs/CRAWLING_POLICY.md`** — only if Candidate H is chosen.

---

## Outstanding items carried forward to Session 24+

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

8. **Durable bypass-audit persistence in worker_loop** — NEW
   from S23. Production `scrape_stage2_pages_invoker` currently
   has a log-only `bypass_audit_writer`; durable persistence to
   `JournalState.robots_bypass_log` requires opening a
   `CostJournal` at worker boot. See Candidate I above.
   The S23 integration test
   (`tests/orchestrator/test_robots_gate_integration.py`) pins
   the contract end-to-end via `LocalFSCostJournal` in tmp_path.

---

## Locked artifact reminders for Session 24

Carry-forward from Sessions 8-23:

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
  locked at `34a59b6`. Candidate I (if chosen) CONSUMES the
  public API via the gate but does NOT modify the parser.
- `tests/scraper/test_robots.py` — S21 deliverable; locked at
  `34a59b6`.
- `src/barcada_scraper/scraper/robots_gate.py` — S22 deliverable;
  locked at `ba87e7e`. Candidate I CONSUMES the public API
  (RobotsGate.evaluate, GateDecision, BypassEntry, GATE_ACTION_*)
  but does NOT modify the shim.
- `src/barcada_scraper/scraper/robots_bypass_config.py` — S22
  deliverable; locked at `381ee89`.
- `tests/scraper/test_robots_gate.py` — S22 deliverable; locked
  at `ba87e7e`.
- `tests/scraper/test_robots_bypass_config.py` — S22 deliverable;
  locked at `381ee89`.
- `src/barcada_scraper/classifier/pipeline/cost_journal.py` —
  S22-extended at `1d9404e`. Candidate I CONSUMES the S22
  additions (`with_robots_bypass_appended`, `update_with_retry`,
  `BypassAuditEntry`, `LocalFSCostJournal`, `open_journal`) but
  does NOT modify them. The pre-S22 surfaces (CostTotals,
  ShardRecord, CeilingHistoryEntry, etc.) remain locked as before.
- `docs/CRAWLING_POLICY.md` — S22 deliverable; locked at
  `fdc8a7a`.
- **NEW S23**: `src/barcada_scraper/orchestrator/robots_integration.py`
  — locked at `279bb77`. Candidate I CONSUMES the public API
  (`build_robots_gate`, `prewarm_robots_for_url`,
  `make_robots_disallow_row_fields`, `record_bypass_audit`,
  `load_bypass_config_or_empty`, `ROBOTS_DISALLOW_ERROR_KIND`) and
  may add new helpers (e.g., a URL→CostJournal-handle parser) but
  MUST NOT modify the landed surface.
- **NEW S23**: `tests/orchestrator/test_robots_integration.py` —
  locked at `279bb77`. 35 tests.
- **NEW S23**: `tests/orchestrator/test_robots_gate_integration.py`
  — locked at `6e6e4ca`. 4 end-to-end integration tests. Adding
  new tests is allowed; modifying the S23 tests requires explicit
  authorization.
- **PARTIAL NEW S23**: `src/barcada_scraper/orchestrator/vmss_worker.py`
  — S23 added `WorkerConfig.robots_bypass_config_path` field +
  env reader at `5eeaac7`. The new public surface is locked. Pre-
  S23 surfaces remain locked as before.
- **PARTIAL NEW S23**: `src/barcada_scraper/orchestrator/job_runner.py`
  — S23 added `JobRunArgs.robots_bypass_config_path` field +
  `--robots-bypass-config` CLI flag + `render_cloud_init` kwarg +
  substitution entry at `872527e`. Locked.
- **PARTIAL NEW S23**: `scripts/vmss/cloud_init.template.yaml` —
  S23 added `${BARCADA_ROBOTS_BYPASS_CONFIG}` placeholder + `-e`
  line at `872527e`. Locked.
- **PARTIAL NEW S23**: `src/barcada_scraper/orchestrator/worker_loop.py`
  — S23 added gate construction + prewarm + 3-site wiring +
  `bypass_config` / `bypass_audit_writer` kwargs at `4ec7b0a`.
  The new optional kwargs on `_acquire_one_domain_t1` and the
  log-only writer in `scrape_stage2_pages_invoker` are locked
  (Candidate I REPLACES the log-only writer with a durable one
  but MUST preserve the kwargs' public shape on
  `_acquire_one_domain_t1`).
- `docs/phase4_implementation_plan.md` — Phase 4 governance
  reference; do NOT modify until Phase 4 work is operator-
  authorized.
- Production code under `src/barcada_scraper/` — locked unless
  Phase 2 design-gate explicitly authorizes a specific module.
  S21+S22+S23 authorized: `scraper/robots.py`, `scraper/
  robots_gate.py`, `scraper/robots_bypass_config.py`,
  `classifier/pipeline/cost_journal.py` (additive only),
  `orchestrator/robots_integration.py` (new),
  `orchestrator/vmss_worker.py` (additive),
  `orchestrator/job_runner.py` (additive),
  `orchestrator/worker_loop.py` (additive). No other src/ module
  is authorized.
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-24-open baseline

Canonical (15 paths; mirrors S23-close invocation):

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
    tests/orchestrator/test_robots_gate_integration.py -q
# Expected: 932 passed / 0 failed / 0 skipped
```

Sub-totals: 210 conformance + 46 driver + 99 baseline_v0 + 33
synthetic_crawl + 32 robots + 30 robots_gate + 30 robots_bypass_config
+ 43 cost_journal + 13 cost_journal_local + 2 cost_journal_adls +
35 robots_integration + 74 vmss_worker + 129 job_runner + 152
worker_loop + 4 robots_gate_integration = 932.

Cumulative-test-count gate: the count NEVER decreases between
commit boundaries.

Narrower baselines (still valid for S24 candidates that don't
exercise the orchestrator sub-surface):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 593 (`tests/orchestrator/` alone at HEAD `6e6e4ca`)

Choose at Phase 0 Step 0.5 per Candidate selection.

---

## Pre-push gate at Session 24 open

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 350+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

Note on gate 4: validate_consistency runs against working-tree
state; if operator-WIP in eval_data introduces a schema violation
between S23 close and S24 open, the gate will block even though
no S24 commit touches eval_data. Per LESSONS: surface to operator
with the row+detail, propose operator-fix or stash-and-restore;
do NOT auto-fix.

---

## Context-window awareness

Session 23 ran across 5 commits + Phase 2 source-verification +
2 Explore-subagent surveys + 1 mid-Phase-3 commit-shape
adjustment, well within context. Session 24 budget per chosen
candidate:

- Candidate I (durable persistence): 50-100 LOC + tests +
  CostJournal handle plumbing. Small-medium scope.
- Candidate B (per-tier cost-accounting): touches W4.1.5 area;
  more careful Phase 0 verification needed.
- Candidate A (barcada-drift): only if launchd job has run ≥2
  times AND AI/ML decisions ready.
- Candidate H (doc tightening): very small; <30 minutes.
- Candidate E (cassette corpus expansion): depends on operator
  curation choices.

Strategies (unchanged from S20-S23 prompts):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-HTTP corpus work, pilot 1-3 before full N-domain.
- Source-verify line numbers per Phase 3 commit, not just at
  Phase 2 (NEW S23 LESSONS pattern).

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S24 scope closes,
  transition per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-23:

1. Commit SHA(s) of each Session 24 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 932 baseline → S24 close.
4. Driver suite count (46/46 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (e.g., does S24 warrant a new tag?
   Unlikely for Candidate I alone — that's a follow-up
   persistence wire, not yet a workstream-end milestone).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 23 handoff template. Refill at Session 24 close
for Session 25.
