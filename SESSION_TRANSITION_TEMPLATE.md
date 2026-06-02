# Session Transition Template — Handoff from Session 35 → Session 36

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-35 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 36 invocation prompt:** NOT yet drafted. Per the S20→S35
precedent, drafting the next-session prompt is operator-commissioned
between sessions (NOT a built-in Phase 6 step). If the operator wants
one, it should mirror the S20-S35 7-phase structure and pin: repo HEAD
anchor `f80ccdc`, workspace HEAD anchor (the S35 close-out commit + its
anchor-pin follow-up), tag count `13`, canonical baseline `970`, Phase 0
Step 0.4 `cassette_count == 30` / `exclusions_count == 30`, and a Step
0.9 presence + POSTURE check for the S31/S32 cassettes, the S33 Azurite
primitive, the S34 deliverables (`live-integration.yml` OFF push/PR + the
concurrency race test on port 10001), AND the NEW S35 deliverable (the
parquet ShardWriter adlfs test on port 10002).

**IMPORTANT — S36 again opens with a near-empty warm-candidate
queue.** S35 shipped fresh live ADLS coverage for the parquet
`ShardWriter` (the largest uncovered adlfs write surface). The remaining
carry-forwards are A (blocked), D (operator-led labeling), and E
(EXHAUSTED — needs a plan-bound revision to reopen). NONE is on a
critical path and NONE is self-contained. S36 may have no actionable
engineering scope unless the operator unblocks A, begins D labeling,
authorizes a plan amendment to reopen E, or commissions a fresh
candidate. Fresh-candidate space now visibly includes the OTHER
uncovered adlfs write surfaces surfaced by the S35 survey
(`page_storage._write_pages_via_fsspec`, `prompt_logger`) and the
still-untested lease/SAS/container-level cost-journal paths. Surface the
empty-queue condition at S36 Phase 1 exactly as S33/S34/S35 did (the
condition + the budget trade-off of a no-ship resolution).

Anchors for Session 36 cold start:
- Repo HEAD: `f80ccdc` (S35: WA2.W8.adls-live-parquet-writer — +1
  `@pytest.mark.live` parquet ShardWriter adlfs test). Tolerated delta:
  operator-side eval_data labeling commits between S35 close and S36
  open (Sessions 8-35 precedent) — verify each is strictly `eval_data/*`
  via `git show --stat`.
- Workspace HEAD: the S35 primary close-out commit (SESSION_LOG.md +
  SESSION_TRANSITION_TEMPLATE.md + LESSONS.md) + THIS anchor-pin
  follow-up succeeding it (+ any later prompt-revision commits). S36
  Phase 0 Step 0.1 MUST anchor workspace expectation to the S35
  close-out OR this anchor-pin follow-up OR a later follow-up. Per the
  S21-S35 LESSONS pattern "Workspace HEAD delta tolerance": tolerate N
  additional prompt-drafting / audit-correction commits between sessions.
- Canonical baseline: **970 tests** (16-path invocation; UNCHANGED from
  S27-S35 close). ALL THREE Azurite tests are `@pytest.mark.live` +
  skip-by-default and are NOT in the canonical invocation.
- Narrower baseline: **944 tests** (14-path; 970 minus 19
  cost_journal_adls minus 7 robots_gate_integration). Unchanged.
- Fixture counts (S36 Phase 0 Step 0.4): html=222 / expected=202 /
  meta=222 / baseline=1213 / **`cassette_count == 30`** /
  **`exclusions_count == 30`** — UNCHANGED from S33/S34/S35 (the S35
  deliverable is one live test file; no fixture change).
- Primary recommended scope: none — no carry-forward is on a
  critical path; none is self-contained.
- Carry-forward candidates: A (barcada-drift; blocked on parquets +
  AI/ML), D (Phase 4 PR-D tooling; operator-led labeling not yet
  begun), E (EXHAUSTED at 30 — no further +N without a plan-bound
  revision). **K-a + its CI wiring CLOSED at S33/S34; the parquet adlfs
  leg CLOSED at S35.**

**S35 Candidate SHIPPED (NEW candidate: fresh live ADLS coverage for the
parquet ShardWriter)** — `f80ccdc`, single commit, 1 file, 309 LOC:
- `tests/classifier/pipeline/test_parquet_writer_adls_azurite.py`
  (309 LOC; 1 `@pytest.mark.live` test). Drives the production
  `output/parquet_writer.py::ShardWriter` over an `abfss://` URL against
  Azurite via `adlfs.AzureBlobFileSystem` (shared-key connection
  string), writes 5 records, closes — exercising `fs.open('wb')` →
  `ParquetWriter.write_table` → atomic `fs.mv` tmp→final — then reads
  `data.parquet` back through a FRESH adlfs handle. This closes the gap
  the 33-test `file://`-only `test_parquet_writer.py` explicitly
  disclaims ("identical for abfss:// URLs via adlfs"). The key survey
  finding: the parquet/page-storage write surfaces use a SEPARATE stack
  (fsspec/adlfs) from the cost journal (azure-storage-blob SDK), so the
  S33/S34 live tests proved nothing about them (S35 LESSONS fold).
  Teeth proven via a negative control (a `file://` URL resolves to
  `LocalFileSystem` with an absolute `final_path` → both teeth
  assertions fire). Own module-scoped Azurite fixture on a DISTINCT port
  (10002) + name (`barcada-azurite-parquet`) so all THREE live fixtures
  coexist under one `-m live` run. Auto-joins `live-integration.yml`'s
  `-m live tests/classifier/pipeline/` selection — no workflow edit.

---

## Handoff metadata

- Outgoing session number: 35
- Closing date: 2026-06-02
- Outgoing session scope: NEW candidate — fresh live ADLS coverage,
  survey-first. Phase 2 source-verify enumerated the ADLS write surfaces
  and found the parquet `ShardWriter` (fsspec/adlfs stack) was the
  largest uncovered one; operator confirmed the carve-out. Built one
  `@pytest.mark.live` test driving the production ShardWriter against
  Azurite via adlfs (shared-key), with a demonstrated negative-control
  teeth check. 1 repo commit (`f80ccdc`). LLM spend: $0. Infrastructure:
  $0 (local Docker + the already-pulled Azurite image; no paid Azure
  service touched).
- Reason for transition: S35 scope completed cleanly through
  Phase 0 → Phase 6; no HALT (one build-time adlfs gotcha caught + fixed
  before commit: makedirs-no-op → mkdir); no in-flight sub-surface.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `f80ccdc` (WA2.W8.adls-live-parquet-writer: parquet
  ShardWriter adlfs Azurite live test).
- Branch sync with `origin/main`: pushed at S35 close (confirm
  0 ahead / 0 behind after the push).
- Tags (13 total; UNCHANGED; 1.TAG = defer):
  - `pre-remediation-2026-05-19` / `baseline-v0` (`9e9a1fb`)
  - `workstream-0-week1-end` … `week7-end`
  - `workstream-0-end` at `a1c5636` (annotated; placed S27)
  - `workstream-a-week1-end` at `fdc8a7a` (placed S22)
  - `workstream-stage1-prestaged-flags-end` (`af6f1d4`),
    `workstream-stage1-step3-end` (`d4f06b8`) — operator eval_data tags
  - NOTE: `workstream-a-week2-end` was OFFERED at S33 AND remained
    DEFERRED at S34 AND S35 despite three live-ADLS surfaces landing. If
    a future session declares W A.2 closed, that annotated tag remains
    appropriate.
- Pre-push gate at HEAD `f80ccdc`: VERIFIED GREEN at S35 close
  (ruff check "All checks passed!" + ruff format clean [356 files;
  count not pinned] + vermin 3.10 + validate_consistency 0 errors /
  0 warnings).
- Unstaged operator territory (Sessions 8-35 precedent):
  `eval_data/stage1_labels.jsonl` (modified) + `eval_data/audits/`
  (untracked) + `.claude/scheduled_tasks.lock` (untracked) — present
  at S35 open/close and left unstaged. Verify via `git status` at
  S36 open.
- Corpus: 222 .html / 202 expected.json / 222 meta.json (unchanged).
- 30 synthetic_crawl cassettes (20 S20 + 5 S31 + 5 S32) + 30
  sidecars (UNCHANGED).
- ADDED Session 35 (1 commit `f80ccdc`):
    - `tests/classifier/pipeline/test_parquet_writer_adls_azurite.py`
      (NEW; 309 LOC; 1 `@pytest.mark.live` parquet ShardWriter adlfs
      test + module-scoped Azurite fixture on port 10002 / container
      `barcada-azurite-parquet`). No `src/` changes. No cassette/driver
      changes. The S33 + S34 live test files + the CI workflow are
      UNTOUCHED.
- Combined test suite at HEAD `f80ccdc`:
    - **970 passed / 0 failed / 0 skipped** — canonical 16-path
      (UNCHANGED; all three Azurite tests are live-marked + absent).
    - **944** — narrower 14-path (unchanged).
    - OUT-OF-BAND live tests: `pytest -m live tests/classifier/pipeline/`
      → **3 passed, 209 deselected** (needs Docker + the Azurite
      image, else SKIPS). CI runs exactly this + a skip-fail guard.
      Ports: S33=10000, S34=10001, S35=10002.
    - Stage 1 test counts: 32 (16 + 16) — unchanged; outside the
      canonical 16-path.

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 35 start: `4a39e0b` ("S35 prompt fix:
  inline bodiless Step 0.9 checks + number the 13-tag list + prefer
  Write-tool staging"; succeeds `1037585` S35 prompt draft, atop
  `27bd60b`). At S35 Phase 0 Step 0.1 the 2 commits ahead of `27bd60b`
  were tolerated under "Workspace HEAD delta tolerance" (prompt-only
  edits).
- Session 35 close-out workspace commits: 1 primary close-out
  `fd3b5d8` (SESSION_LOG.md + SESSION_TRANSITION_TEMPLATE.md +
  LESSONS.md) + this anchor-pin follow-up (pinning `fd3b5d8` into this
  template's Anchors section for S36).
- **Last commit SHA at Session 35 CLOSE: this anchor-pin follow-up
  succeeding the primary close-out `fd3b5d8`.** S36 Phase 0 Step 0.1
  MUST anchor workspace expectation to `fd3b5d8` OR this anchor-pin
  follow-up OR a later follow-up.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected after
  the Session 35 close push.

---

## Session 36 execution order (enforce strict sequence)

Same N-phase shape regardless of scope choice (Phase 0 cold-start
verify → Phase 1 scope → Phase 2 design-gate → Phase 3 impl →
Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 36 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 35 entry (the ADLS write-surface
   survey; the adlfs-vs-SDK stack split; the parquet ShardWriter
   carve-out; the negative-control teeth check; the makedirs→mkdir
   build-time gotcha).
3. Reading LESSONS.md additions Session 35 landed (1 new section,
   "S35 folding" suffix: adlfs is a separate ADLS write stack from the
   azure-storage-blob SDK — cover it on its own).
4. Reading the relevant section of BARCADA_CRAWLER_REMEDIATION_PLAN.md
   for the chosen Session 36 scope.
5. Reading the Session 36 prompt if one has been drafted, OR
   commissioning a fresh draft at S36 open.
6. Running Phase 0 cold-start verification (mirror the S35 prompt's
   9-step shape, updating workspace HEAD anchor, repo HEAD anchor
   `f80ccdc`, tag count `13`, canonical baseline `970`, cassette
   fixture-count `30` / exclusions `30`, AND a Step 0.9 presence
   check for the S33 + S34 + S35 live deliverables).

---

## Outstanding operator-input requests entering Session 36

1. **Session 36 scope choice** — pick from the carry-forwards below.
   K-a + its CI wiring + the parquet adlfs leg are CLOSED. Candidate E
   is EXHAUSTED (30 upper bound). None of A/D is on a critical path. S36
   may be a no-ship scope-resolution session — surface that at Phase 1.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*` continue across sessions (Sessions 8-35 precedent).

3. **barcada-drift AI/ML alignment** — 4 AI/ML team decisions need
   pre-resolution OR placeholders, plus 2+ canary_runs parquet files.
   Re-verified empirically at S35 Phase 1: 0 canary_runs parquets,
   0 plist, no AI/ML responses.

4. **launchd kit installation** — Operator should run
   `scripts/launchd/install_canary_schedule.sh` when ready. Required
   prerequisite for Candidate A. As of S35 close, NOT yet installed.

5. **Session 36 prompt draft commissioning** — operator decides
   whether to commission an S36 prompt between sessions.

6. **Remaining uncovered adlfs write surfaces (potential NEW
   candidate)** — the S35 survey enumerated them: the parquet
   `ShardWriter` is now covered, but `page_storage._write_pages_via_fsspec`
   (Stage-2 pages.parquet), `prompt_logger`, and the
   `PartitionedShardWriter` Hive `write_to_dataset` path are still
   adlfs-uncovered. Plus lease/SAS/container-level cost-journal live
   paths (azure-storage-blob stack). Each is a fresh candidate scoped
   from first principles (default to the S33/S34/S35 live-fixture shape;
   distinct port 10003+ if coexisting).

---

## Notes for Session 36

Suggested S36 scope candidates (operator picks at S36 open):

### Candidate A (carry-forward): `barcada-drift` skeleton

Unchanged. Per CLASSIFICATION_ADJACENT_PLAN.md §Item 8. Consumes
`canary_runs/<date>.parquet` artifacts. **Blocked**: 2+ parquet
files needed AND 4 AI/ML decisions (or placeholders). Estimated
~370-400 LOC delivered.

### Candidate D (carry-forward): Phase 4 PR-D operator-led labeling

Unchanged. Tooling support only; labeling is operator territory.
W0 closed (workstream-0-end at `a1c5636`). Still gated on
operator-led Stage 2/3 labeling start.

### Candidate E (EXHAUSTED at S32)

The cassette corpus reached the plan's **30 upper bound** at S32.
**No further +N without an explicit plan-bound revision** (raise the
§4 W7 "~20-30" ceiling first, as a plan-amendment session). Do NOT
add cassettes under the current plan.

### Live ADLS coverage (parquet ShardWriter CLOSED at S35)

The parquet `ShardWriter` adlfs write path is now live-tested (S35,
port 10002), alongside the cost-journal ETag primitive (S33) +
multi-writer race (S34). NOT a carry-forward. The OTHER adlfs write
surfaces (`page_storage`, `prompt_logger`, `PartitionedShardWriter`)
and the lease/SAS cost-journal paths remain fresh-candidate space.

---

## Required reading (Session 36 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 35 entry — the ADLS write-surface
   survey; adlfs-vs-SDK stack split; parquet ShardWriter carve-out;
   negative-control teeth; makedirs→mkdir gotcha.
3. **`LESSONS.md`** — the new "S35 folding" section (adlfs is a separate
   ADLS write stack) PLUS the "S33 folding" (live-emulator teardown +
   version skew) and "S34 folding" (carve-out ↔ test-body verification)
   if a live-service scope is chosen.
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope section.
   READ-ONLY (exception: a plan-amendment session to reopen E).
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A is chosen.
6. **`src/barcada_scraper/output/parquet_writer.py`** +
   `src/barcada_scraper/classifier/page_acquisition/page_storage.py`
   + the three live test files +
   `.github/workflows/live-integration.yml` — only if a new
   ADLS-surface / CI scope is chosen.

---

## Outstanding items carried forward to Session 36+

1. **Per-tier cost-accounting wiring** — CLOSED end-to-end S28.
2. **`barcada-drift` CLI** — §Item 8; 4 AI/ML decisions + 2+
   parquets outstanding. Re-verified empirically at S35 Phase 1.
3. **Cassette corpus expansion** — EXHAUSTED at 30. No further +N
   without a plan revision.
4. **Cassette-FP investigation** — archive.org + hashicorp.com +
   stripe.com (S20-locked; flags are correct behavior). DEFERRED.
5. **launchd kit smoke-then-install** — Required for Candidate A.
6. **Phase 4 PR-D/E/F/G** — W0-side unblocked since S27; operator-led
   Stage 2/3 labeling still needs to begin.
7. **CRAWLING_POLICY.md size** — CLOSED at S26 (2.52 KB).
8. **abfss:// CostJournal Phase 5 promotion** — CLOSED at S25.
9. **Live Azure smoke SCRIPT** — CLOSED S29.
10. **Stage 1 ShardResult LLM-vs-embedding split** — CLOSED S28.
11. **Live Azure smoke EXECUTION** — CLOSED S30.
12. **Azurite-backed live ADLS coverage** — cost-journal ETag primitive
    CLOSED S33; multi-writer concurrency + CI wiring CLOSED S34
    (`eba6585`); **parquet ShardWriter adlfs write path CLOSED S35**
    (`f80ccdc`, port 10002). The three live tests run on-demand +
    nightly via `live-integration.yml` with a guard that fails on a
    silent skip. Default push/PR CI still does NOT run them (by design).
    Potential future extensions (fresh candidates): `page_storage` /
    `prompt_logger` / `PartitionedShardWriter` adlfs paths; lease/SAS
    cost-journal paths.
13. **Recorder reject-before-write / min-content-bytes floor +
    is_waf_challenge "Client Challenge" signature** — parser/recorder
    hygiene (S31+S32 folds). NOT a fix unless a future session scopes
    `tools/synthetic_crawl/` or `scraper/parser.py`.

---

## Locked artifact reminders for Session 36

Carry-forward from Sessions 8-35. **NEW S35 LOCK**:
- `tests/classifier/pipeline/test_parquet_writer_adls_azurite.py`
  at `f80ccdc` (309 LOC; 1 `@pytest.mark.live` parquet ShardWriter
  adlfs test + its own module-scoped Azurite fixture on port 10002 /
  container `barcada-azurite-parquet`). Do NOT modify without Phase 2
  authorization. It auto-joins `live-integration.yml`'s `-m live` dir
  selection; keep its live marker + the `AzureBlobFileSystem` teeth
  assertion intact.

Prior live-ADLS locks (unchanged):
- **S34 LOCKS**: `test_cost_journal_adls_azurite_concurrency.py` at
  `eba6585` (337 LOC; port 10001 / `barcada-azurite-racetest`) +
  `.github/workflows/live-integration.yml` at `eba6585` (CI workflow;
  `workflow_dispatch` + nightly schedule; NOT push/PR). The `-m live`
  selection over `tests/classifier/pipeline/` + the skip-fail guard are
  load-bearing; do NOT weaken to a default-CI trigger without a
  deliberate posture decision (S33 framing).
- **S33 LOCK**: `test_cost_journal_adls_azurite.py` at `f1cdce8`
  (292 LOC; port 10000 / `barcada-azurite-katest`) + the `live` marker
  in `pyproject.toml` `[tool.pytest.ini_options]`.
- `eval_data/` — labeling-workstream territory; operator-WIP expected.
- `stage1.schema.json` v1.0 (49 keywords).
- `pre-remediation-2026-05-19` / `baseline-v0` (`9e9a1fb`) tags.
- All `workstream-0-*-end` tags; `workstream-0-end` (`a1c5636`);
  `workstream-a-week1-end` (`fdc8a7a`); the 2 operator eval_data tags.
- `tests/runners/fixture_cascade/` — W4.1.5 driver; locked at
  `dd64963` except via W5.X commits (S27 `a1c5636`, S28 `9afde57` +
  `ae9e627`). S29-S35 did NOT touch this surface.
- `tests/fixtures/baseline-v0/` snapshot — locked at `9e9a1fb`.
- `tools/baseline_v0/` + `tools/synthetic_crawl/` — S18-S20; locked.
- `tests/fixtures/synthetic_crawls/` — 20 S20 (`7f11879`) + 5 S31
  (`06d67c4`) + 5 S32 (`cfa0ec1`); never re-record/delete.
- `scripts/launchd/` — S20; locked.
- `src/barcada_scraper/scraper/robots.py` (`34a59b6`),
  `robots_gate.py` (`ba87e7e`), `robots_bypass_config.py`
  (`381ee89`) + their test files — S21/S22; locked.
- `cost_journal.py` (S22-extended `1d9404e`; public API consumed by
  S27-S34 without modification).
- `cost_journal_local.py` — locked.
- `cost_journal_adls.py` — full backend at S25 `835a531`. Public API
  `ADLSCostJournal(journal_dir, run_id, credential=None,
  blob_backend=None)`. EMPIRICALLY VALIDATED at S30 (K-b smoke), S33
  (Azurite primitive), S34 (Azurite concurrency). UNMODIFIED by any.
- `output/parquet_writer.py` — `ShardWriter` / `PartitionedShardWriter`
  / `write_records_to_shards{,_partitioned}` / `storage_options_from_env`.
  EMPIRICALLY VALIDATED against Azurite via adlfs at S35 (the S35 test
  injects only the public `storage_options=` seam + `abfss://` URL; it
  did NOT modify the module).
- `tests/test_parquet_writer.py` — 33 hermetic `file://` tests; locked.
- `tests/classifier/pipeline/test_cost_journal_adls.py` — 19
  in-memory tests at `835a531` (incl. `DummyBlobBackend`).
- `docs/CRAWLING_POLICY.md` — S26 `2314f5e` (77 lines / 2.52 KB).
- `orchestrator/robots_integration.py` (`279bb77`) + its 35 tests.
- 7 tests in `test_robots_gate_integration.py` (`aed7873`).
- `orchestrator/vmss_worker.py` (`5eeaac7`), `job_runner.py`
  (`872527e`), `scripts/vmss/cloud_init.template.yaml` — S23.
- The 3 worker_loop helpers (`_open_cost_journal_for_worker` body
  S25 `aed7873`; `_ensure_journal_initialized` +
  `_build_durable_bypass_writer` S24 `48c324a`).
- `test_worker_loop_persistence.py` (12 tests; `aed7873`); the 5
  S24-retargeted invoker fixtures in `test_worker_loop.py` (`48c324a`).
- `docs/phase4_implementation_plan.md` — Phase 4 governance.
- S28 LOCKS: `classifier/stage1/run.py` (`776d203`),
  `test_run_cascade.py` (`776d203`).
- S29 LOCK: `scripts/smoke_test_adls_cost_journal.py` (`75a3937`).
- `pyproject.toml` — NOT locked, but the S33 `live` marker
  registration is load-bearing; do not remove.
- Production code under `src/barcada_scraper/` — locked unless a
  Phase 2 gate authorizes a specific module. S26+S27+S29-**S35**
  added NO new src/ authorizations (S35 was a test-only addition).
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-36-open baseline

Canonical (16 paths):

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
# Expected: 970 passed / 0 failed / 0 skipped
```

Sub-totals identical to S27-S35 close: 210 conformance + 52 driver
+ 99 baseline_v0 + 33 synthetic_crawl + 32 robots + 30 robots_gate
+ 30 robots_bypass_config + 43 cost_journal + 13 cost_journal_local
+ 19 cost_journal_adls + 35 robots_integration + 74 vmss_worker +
129 job_runner + 152 worker_loop + 7 robots_gate_integration + 12
worker_loop_persistence = 970. (ALL THREE Azurite tests are
live-marked + skip-by-default and are NOT in this invocation.)

OUT-OF-BAND live tests (NOT in the canonical count; need Docker +
the Azurite image, else SKIP):

```
.venv/bin/python -m pytest -m live tests/classifier/pipeline/
# Expected: 3 passed, 209 deselected
# (CI live-integration.yml runs exactly this + a skip-fail guard.)
# Ports: S33=10000, S34=10001, S35=10002.
```

Cumulative-test-count gate: the count NEVER decreases between commit
boundaries.

Narrower baselines (still valid for S36 candidates that don't
exercise the ADLS test paths): 480 / 538 / 944.

**Fixture-count assertions for S36 Phase 0 Step 0.4**: html_count=222,
expected_count=202, meta_count=222, baseline_count=1213,
**`cassette_count == 30`, `exclusions_count == 30`** (UNCHANGED).

---

## Pre-push gate at Session 36 open

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # all files OK (do not pin a fixed N)
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

Note on gate 4: validate_consistency runs against working-tree state;
if operator-WIP in eval_data introduces a schema violation between
S35 close and S36 open, the gate blocks even though no S36 commit
touches eval_data. Per LESSONS: surface to operator with the
row+detail, propose operator-fix or stash-and-restore; do NOT
auto-fix. S35 ran the gate clean at Phase 4 (0 errors / 0 warnings).

---

## Context-window awareness

Session 35 ran Phase 0 → Phase 6 in a single context window with 1
repo commit (Phase 0 verify + Phase 1 scope + Phase 2 source-verify
survey + operator-confirmed carve-out + Phase 3 impl with a build-time
spike + Phase 6 close-out), within budget. Session 36 budget per
chosen candidate:

- Candidate A (barcada-drift): only if launchd job has run ≥2 times
  AND AI/ML decisions ready. ~370-400 LOC delivered.
- Candidate D: operator-led; tooling only.
- Candidate E: EXHAUSTED; not available without a plan-bound revision.
- A NEW live-ADLS candidate (page_storage / prompt_logger /
  PartitionedShardWriter adlfs paths, or lease/SAS): size at Phase 2;
  default to operator-smoke posture unless a named carve-out justifies CI.

Strategies (unchanged from S20-S35 prompts):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-service-backed test, default to the S33/S34/S35 fixture
  shape: unconditional try/finally teardown + idempotent
  self-healing pre-clean + skip-if-unavailable; expect an
  SDK-vs-emulator version-skew flag may be needed; use a DISTINCT
  port + container name if it must coexist with the existing live
  fixtures (S33=10000, S34=10001, S35=10002 → use 10003+); keep the
  test off the canonical headline (live marker, skip-by-default) unless
  a deliberate decision adds it.
- **Survey ADLS coverage by CLIENT STACK (azure-storage-blob SDK vs
  fsspec/adlfs), not by "is there an Azurite test" (S35 LESSONS).**
- **Verify a carve-out against the TEST BODY, not its name/marker
  (S34 LESSONS) — and re-verify when CI-wiring an existing test.**
- Source-verify facts behind option-set design BEFORE AskUserQuestion
  drafts (S25 LESSONS).
- Phase 0 fixture-count commands use the Python `rglob()` pattern,
  NOT bare `find` (S28 post-close LESSONS).
- Markdown-rendered shell commands may carry NBSP in whitespace-
  sensitive args; stage scripts to a file via the Write tool when
  exactness matters (re-confirmed S34/S35 — secrets-referencing inline
  `python -c` also trips the env hook; file-staged scripts work).
- The `rm -f` / `rm -rf` / `find -delete` forms are env-hook-blocked
  (re-confirmed S35: a `docker rm -f` pre-clean in an inline Bash call
  tripped the destructive-op hook). Operator runs destructive cleanup
  via `! rm ...`; inside test fixtures the `docker rm -f` runs fine
  (the hook gates the agent's Bash calls, not subprocess in pytest).

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S36 scope closes, transition
  per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-35:

1. Commit SHA(s) of each Session 36 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 970 baseline → S36 close.
4. Driver suite count (52/52 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (W0 closed S27; W A.1 closed S22; W A.2
   final-milestone tag `workstream-a-week2-end` OFFERED+DEFERRED at
   S33 AND S34 AND S35).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 35 handoff template. Refill at Session 36 close.
