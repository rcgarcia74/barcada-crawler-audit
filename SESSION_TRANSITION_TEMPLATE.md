# Session Transition Template — Handoff from Session 37 → Session 38

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-37 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 38 invocation prompt:** NOT yet drafted. Per the S20→S37
precedent, drafting the next-session prompt is operator-commissioned
between sessions (NOT a built-in Phase 6 step). If the operator wants
one, it should mirror the S20-S37 7-phase structure and pin: repo HEAD
anchor `f4e0a4a`, workspace HEAD anchor (the S37 close-out commit + its
anchor-pin follow-up), tag count `13`, canonical baseline `970`, Phase 0
Step 0.4 `cassette_count == 30` / `exclusions_count == 30`, and a Step
0.9 presence + POSTURE check for the S31/S32 cassettes, the S33 Azurite
primitive, the S34 deliverables (`live-integration.yml` OFF push/PR + the
concurrency race test on port 10001), the S35 deliverable (the parquet
ShardWriter adlfs test on port 10002), the S36 deliverable (the
page_storage adlfs test on port 10003 with env-var auth), AND the NEW
S37 deliverable (the PartitionedShardWriter adlfs test on port 10004
driving the Hive `write_to_dataset` path with the explicit
`storage_options=` seam).

**IMPORTANT — S38 again opens with a near-empty warm-candidate
queue.** S37 shipped fresh live ADLS coverage for `PartitionedShardWriter`
(the Hive `write_to_dataset` path — the second half of
`output/parquet_writer.py`). The remaining carry-forwards are A (blocked),
D (operator-led labeling), and E (EXHAUSTED — needs a plan-bound revision
to reopen). NONE is on a critical path and NONE is self-contained. S38
may have no actionable engineering scope unless the operator unblocks A,
begins D labeling, authorizes a plan amendment to reopen E, or
commissions a fresh candidate. Fresh-candidate space now narrows to the
STILL-uncovered adlfs write surface `prompt_logger` (fsspec `wb` single
JSONL object) and the still-untested lease/SAS/container-level
cost-journal paths (azure-storage-blob stack). Surface the empty-queue
condition at S38 Phase 1 exactly as S33/S34/S35/S36/S37 did (the
condition + the budget trade-off of a no-ship resolution).

Anchors for Session 38 cold start:
- Repo HEAD: `f4e0a4a` (S37: WA2.W8.adls-live-partitioned-writer — +1
  `@pytest.mark.live` PartitionedShardWriter adlfs test). Tolerated delta:
  operator-side eval_data labeling commits between S37 close and S38
  open (Sessions 8-37 precedent) — verify each is strictly `eval_data/*`
  via `git show --stat`.
- Workspace HEAD: the S37 primary close-out commit (SESSION_LOG.md +
  SESSION_TRANSITION_TEMPLATE.md + LESSONS.md) + THIS anchor-pin
  follow-up succeeding it (+ any later prompt-revision commits). S38
  Phase 0 Step 0.1 MUST anchor workspace expectation to the S37
  close-out OR this anchor-pin follow-up OR a later follow-up. Per the
  S21-S37 LESSONS pattern "Workspace HEAD delta tolerance": tolerate N
  additional prompt-drafting / audit-correction commits between sessions.
- Canonical baseline: **970 tests** (16-path invocation; UNCHANGED from
  S27-S37 close). ALL FIVE Azurite tests are `@pytest.mark.live` +
  skip-by-default and are NOT in the canonical invocation.
- Narrower baseline: **944 tests** (14-path; 970 minus 19
  cost_journal_adls minus 7 robots_gate_integration). Unchanged.
- Fixture counts (S38 Phase 0 Step 0.4): html=222 / expected=202 /
  meta=222 / baseline=1213 / **`cassette_count == 30`** /
  **`exclusions_count == 30`** — UNCHANGED from S33/S34/S35/S36/S37 (the
  S37 deliverable is one live test file; no fixture change).
- Primary recommended scope: none — no carry-forward is on a
  critical path; none is self-contained.
- Carry-forward candidates: A (barcada-drift; blocked on parquets +
  AI/ML), D (Phase 4 PR-D tooling; operator-led labeling not yet
  begun), E (EXHAUSTED at 30 — no further +N without a plan-bound
  revision). **K-a + its CI wiring CLOSED at S33/S34; the parquet
  ShardWriter adlfs leg CLOSED at S35; the page_storage adlfs leg CLOSED
  at S36; the PartitionedShardWriter Hive adlfs leg CLOSED at S37.**

**S37 Candidate SHIPPED (NEW candidate: fresh live ADLS coverage for
PartitionedShardWriter)** — `f4e0a4a`, single commit, 1 file, 389 LOC:
- `tests/classifier/pipeline/test_partitioned_shard_writer_adls_azurite.py`
  (389 LOC; 1 `@pytest.mark.live` test). Drives the production
  `output/parquet_writer.py::PartitionedShardWriter` over an `abfss://` URL
  against Azurite via `adlfs.AzureBlobFileSystem`, writing three records
  that derive THREE distinct Hive partitions, then reading the dataset
  back through a FRESH adlfs handle with `pyarrow.dataset.HivePartitioning`.
  This closes the SECOND half of `parquet_writer.py`'s live coverage — the
  Hive `pq.write_to_dataset(filesystem=fs, partition_cols=...)` path, a
  DIFFERENT pyarrow code path than the S35-covered single-file `ShardWriter`.
  **Auth seam (S36 discipline): explicit `storage_options=` kwarg
  (`parquet_writer.py:361`), SAME shared-key seam as S35, NOT env-resolved.**
  **The key finding (S37 LESSONS fold): the makedirs-no-op gotcha is SHARPER
  here** — a multi-partition `write_to_dataset` against a FRESH container
  hits adlfs's non-idempotent `create_container` on the 2nd partition
  (`ContainerAlreadyExists` → `ValueError`), because the production
  `makedirs(partition_root, exist_ok=True)` no-ops on adlfs. Fix (proven in
  a build-time spike): the fixture pre-creates the container via `fs.mkdir`
  (catch `FileExistsError`), matching the production assumption that the
  output container exists before sharded writes. Teeth proven via a
  negative control (a `file://` writer resolves to `LocalFileSystem` with an
  absolute `partition_root` → both blob assertions fire). Own module-scoped
  Azurite fixture on a DISTINCT port (10004) + name
  (`barcada-azurite-partitioned`) so all FIVE live fixtures coexist under
  one `-m live` run (verified: 5 passed, 209 deselected). Auto-joins
  `live-integration.yml`'s `-m live tests/classifier/pipeline/`
  selection — no workflow edit.

---

## S38 forward notes (operator, recorded at S37 close — NOT actions now)

Two notes the operator raised at S37 close for the S38 handoff. Neither is
an action for S37; both are decisions to settle off-session and capture in
the S38 bundle.

1. **`parquet_writer.py` is now FULLY live-covered — completeness boundary.**
   Both halves are closed: the single-file `ShardWriter` path (S35, port
   10002) AND the Hive-partitioned `PartitionedShardWriter`
   `write_to_dataset` path (S37, port 10004). There is no remaining
   uncovered adlfs write path in `output/parquet_writer.py`. This is the
   clean completeness marker for the **parquet cluster** — worth recording
   explicitly because it is the natural closure point to cite whenever the
   tag taxonomy (note 2) is settled.

2. **Tag-taxonomy drift — settle it off-session before S38, don't defer a
   7th time.** `workstream-a-week2-end` has been OFFERED-but-DEFERRED six
   times (S33→S37). The operator's correction: the S33–S37 ADLS live-test
   cluster is **plan-Workstream-B-adjacent, NOT Workstream-A** — so the
   `workstream-a-*` name is likely wrong for it. The off-session decision to
   capture in the S38 bundle, so S38 has a real choice instead of a
   default-defer:
   - **Correct tag identity** for the S33–S37 ADLS live-test cluster (a
     `workstream-b-*`-family name, or whatever the plan's Workstream-B
     taxonomy dictates) — reconcile against
     `BARCADA_CRAWLER_REMEDIATION_PLAN.md`'s Workstream-B definition.
     (Separate concern: the COMMIT subjects use the `WA2.W8.*` prefix,
     established + operator-flagged at S35/S36; that is the commit-label
     convention, not the tag name. The tag taxonomy decision is about what
     ANNOTATED TAG, if any, marks the cluster — not about rewriting pushed
     commit subjects.)
   - **The bar that CLOSES the cluster** — e.g. is the cluster "done" at the
     parquet completeness boundary (note 1) plus cost-journal + page_storage,
     or does it stay open until `prompt_logger` + lease/SAS are also covered?
     Define the closing bar so a future session can place the tag with a
     clear rationale rather than defer again.

---

## Handoff metadata

- Outgoing session number: 37
- Closing date: 2026-06-03
- Outgoing session scope: NEW candidate — fresh live ADLS coverage for
  the PartitionedShardWriter Hive `write_to_dataset` path (decided at
  Phase 1 via AskUserQuestion). Phase 2 source-verify confirmed the auth
  seam matches S35 (explicit `storage_options=` kwarg, not env-resolved).
  A build-time spike caught the partitioned-path container-creation race
  (non-idempotent `create_container` across partitions) BEFORE the test
  body landed; the fix is a fixture pre-`mkdir`. Built one
  `@pytest.mark.live` test driving the production `PartitionedShardWriter`
  against Azurite via adlfs, with a demonstrated negative-control teeth
  check. 1 repo commit (`f4e0a4a`). LLM spend: $0. Infrastructure: $0
  (local Docker + the already-pulled Azurite image; no paid Azure service
  touched).
- Reason for transition: S37 scope completed cleanly through
  Phase 0 → Phase 6; no HALT (the spike's container-creation finding was
  resolved in-Phase-3, not surfaced as a post-commit HALT); no in-flight
  sub-surface.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `f4e0a4a` (WA2.W8.adls-live-partitioned-writer:
  PartitionedShardWriter Hive adlfs Azurite live test).
- Branch sync with `origin/main`: pushed at S37 close (confirm
  0 ahead / 0 behind after the push).
- Tags (13 total; UNCHANGED; 1.TAG = defer):
  - `pre-remediation-2026-05-19` / `baseline-v0` (`9e9a1fb`)
  - `workstream-0-week1-end` … `week7-end`
  - `workstream-0-end` at `a1c5636` (annotated; placed S27)
  - `workstream-a-week1-end` at `fdc8a7a` (placed S22)
  - `workstream-stage1-prestaged-flags-end` (`af6f1d4`),
    `workstream-stage1-step3-end` (`d4f06b8`) — operator eval_data tags
  - NOTE: `workstream-a-week2-end` was OFFERED at S33 AND remained
    DEFERRED at S34, S35, S36 AND S37 (six defers) despite five live-ADLS
    surfaces landing. **TAG-TAXONOMY DRIFT (operator, S37 close): the
    S33–S37 ADLS live-test cluster is plan-Workstream-B-adjacent, NOT A —
    so `workstream-a-week2-end` is likely the WRONG tag name for it.** Do
    NOT settle this by another defer-by-default at S38. See the "S38 forward
    notes" section below: the off-session decision (correct tag identity +
    the bar that closes the cluster) should be captured in the S38 bundle so
    S38 does not make the same defer call a seventh time.
- Pre-push gate at HEAD `f4e0a4a`: VERIFIED GREEN at S37 close
  (ruff check "All checks passed!" + ruff format clean [358 files;
  count not pinned] + vermin 3.10 + validate_consistency 0 errors /
  0 warnings).
- Unstaged operator territory (Sessions 8-37 precedent):
  `eval_data/stage1_labels.jsonl` (modified) + `eval_data/audits/`
  (untracked) + `.claude/scheduled_tasks.lock` (untracked) — present
  at S37 open/close and left unstaged. Verify via `git status` at
  S38 open.
- Corpus: 222 .html / 202 expected.json / 222 meta.json (unchanged).
- 30 synthetic_crawl cassettes (20 S20 + 5 S31 + 5 S32) + 30
  sidecars (UNCHANGED).
- ADDED Session 37 (1 commit `f4e0a4a`):
    - `tests/classifier/pipeline/test_partitioned_shard_writer_adls_azurite.py`
      (NEW; 389 LOC; 1 `@pytest.mark.live` PartitionedShardWriter adlfs
      test + module-scoped Azurite fixture on port 10004 / container
      `barcada-azurite-partitioned`). No `src/` changes. No cassette/driver
      changes. The S33 + S34 + S35 + S36 live test files + the CI workflow
      are UNTOUCHED.
- Combined test suite at HEAD `f4e0a4a`:
    - **970 passed / 0 failed / 0 skipped** — canonical 16-path
      (UNCHANGED; all five Azurite tests are live-marked + absent).
    - **944** — narrower 14-path (unchanged).
    - OUT-OF-BAND live tests: `pytest -m live tests/classifier/pipeline/`
      → **5 passed, 209 deselected** (needs Docker + the Azurite
      image, else SKIPS). CI runs exactly this + a skip-fail guard.
      Ports: S33=10000, S34=10001, S35=10002, S36=10003, S37=10004.
    - Stage 1 test counts: 32 (16 + 16) — unchanged; outside the
      canonical 16-path.

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 37 start: `fbbed97` ("S37 prompt fix:
  reconcile page_storage hermetic count 16->13"; succeeds `f8bd862` S37
  prompt draft, which succeeds `fedb096` S36 anchor-pin). At S37 Phase 0
  Step 0.1 the 2 commits ahead of `fedb096` were tolerated under
  "Workspace HEAD delta tolerance" (prompt-only edits).
- Session 37 close-out workspace commits: 1 primary close-out `bf52f8d`
  (SESSION_LOG.md + SESSION_TRANSITION_TEMPLATE.md + LESSONS.md) + this
  anchor-pin follow-up (pinning `bf52f8d` into this template's Anchors
  section for S38).
- **Last commit SHA at Session 37 CLOSE: this anchor-pin follow-up
  succeeding the primary close-out `bf52f8d`.** S38 Phase 0 Step 0.1 MUST
  anchor workspace expectation to `bf52f8d` OR this anchor-pin follow-up
  OR a later follow-up.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected after
  the Session 37 close push.

---

## Session 38 execution order (enforce strict sequence)

Same N-phase shape regardless of scope choice (Phase 0 cold-start
verify → Phase 1 scope → Phase 2 design-gate → Phase 3 impl →
Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 38 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 37 entry (the partitioned-path
   container-creation finding; the explicit-`storage_options=` auth seam;
   the negative-control teeth check; the build-time spike note).
3. Reading LESSONS.md additions Session 37 landed (1 new section,
   "S37 folding" suffix: the makedirs-no-op gotcha is sharper on the
   partitioned write_to_dataset path — pyarrow's per-partition create_dir
   hits adlfs's non-idempotent create_container).
4. Reading the relevant section of BARCADA_CRAWLER_REMEDIATION_PLAN.md
   for the chosen Session 38 scope.
5. Reading the Session 38 prompt if one has been drafted, OR
   commissioning a fresh draft at S38 open.
6. Running Phase 0 cold-start verification (mirror the S37 prompt's
   9-step shape, updating workspace HEAD anchor, repo HEAD anchor
   `f4e0a4a`, tag count `13`, canonical baseline `970`, cassette
   fixture-count `30` / exclusions `30`, AND a Step 0.9 presence
   check for the S33 + S34 + S35 + S36 + S37 live deliverables).

---

## Outstanding operator-input requests entering Session 38

1. **Session 38 scope choice** — pick from the carry-forwards below.
   K-a + its CI wiring + the parquet ShardWriter adlfs leg + the
   page_storage adlfs leg + the PartitionedShardWriter Hive adlfs leg are
   CLOSED. Candidate E is EXHAUSTED (30 upper bound). None of A/D is on a
   critical path. S38 may be a no-ship scope-resolution session — surface
   that at Phase 1.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*` continue across sessions (Sessions 8-37 precedent).

3. **barcada-drift AI/ML alignment** — 4 AI/ML team decisions need
   pre-resolution OR placeholders, plus 2+ canary_runs parquet files.
   Re-verified empirically at S37 Phase 1: 0 canary_runs parquets,
   0 plist, no AI/ML responses.

4. **launchd kit installation** — Operator should run
   `scripts/launchd/install_canary_schedule.sh` when ready. Required
   prerequisite for Candidate A. As of S37 close, NOT yet installed.

5. **Session 38 prompt draft commissioning** — operator decides
   whether to commission an S38 prompt between sessions.

6. **Remaining uncovered adlfs write surfaces (potential NEW
   candidate)** — the parquet `ShardWriter` (S35), `page_storage` (S36),
   and the `PartitionedShardWriter` Hive `write_to_dataset` path (S37) are
   now covered. The only STILL-uncovered adlfs write surface is
   `prompt_logger` (fsspec `wb` single JSONL object). Plus lease/SAS/
   container-level cost-journal live paths (azure-storage-blob stack).
   Each is a fresh candidate scoped from first principles (default to the
   S33/S34/S35/S36/S37 live-fixture shape; distinct port 10005+ if
   coexisting). NOTE the S36 auth-seam lesson: read the production call
   site's SIGNATURE first to determine whether auth is an injected
   kwarg or env-resolved; AND the S37 lesson for any `write_to_dataset`
   path: pre-create the container via `fs.mkdir`.

---

## Notes for Session 38

Suggested S38 scope candidates (operator picks at S38 open):

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

### Live ADLS coverage (PartitionedShardWriter adlfs leg CLOSED at S37)

The `PartitionedShardWriter` Hive `write_to_dataset` adlfs path is now
live-tested (S37, port 10004), alongside the parquet `ShardWriter` (S35,
port 10002), the page_storage write path (S36, port 10003), the
cost-journal ETag primitive (S33) + multi-writer race (S34). NOT a
carry-forward. The ONE remaining adlfs write surface (`prompt_logger`)
and the lease/SAS cost-journal paths remain fresh-candidate space.

---

## Required reading (Session 38 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 37 entry — the partitioned-path
   container-creation finding; explicit-`storage_options=` auth seam;
   negative-control teeth; build-time spike note.
3. **`LESSONS.md`** — the new "S37 folding" section (makedirs-no-op
   sharper on write_to_dataset) PLUS the "S36 folding" (survey the AUTH
   seam), "S35 folding" (adlfs is a separate ADLS write stack), "S33
   folding" (live-emulator teardown + version skew) and "S34 folding"
   (carve-out ↔ test-body verification) if a live-service scope is chosen.
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope section.
   READ-ONLY (exception: a plan-amendment session to reopen E).
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A is chosen.
6. **`src/barcada_scraper/classifier/llm/prompt_logger.py`** +
   `src/barcada_scraper/output/parquet_writer.py` +
   `src/barcada_scraper/classifier/page_acquisition/page_storage.py`
   + the five live test files + `.github/workflows/live-integration.yml`
   — only if a new ADLS-surface / CI scope is chosen.

---

## Outstanding items carried forward to Session 38+

1. **Per-tier cost-accounting wiring** — CLOSED end-to-end S28.
2. **`barcada-drift` CLI** — §Item 8; 4 AI/ML decisions + 2+
   parquets outstanding. Re-verified empirically at S37 Phase 1.
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
    (`eba6585`); parquet ShardWriter adlfs write path CLOSED S35
    (`f80ccdc`, port 10002); page_storage adlfs write path CLOSED S36
    (`25c3696`, port 10003); **PartitionedShardWriter Hive
    `write_to_dataset` adlfs path CLOSED S37** (`f4e0a4a`, port 10004).
    The five live tests run on-demand + nightly via `live-integration.yml`
    with a guard that fails on a silent skip. Default push/PR CI still
    does NOT run them (by design). The ONE remaining uncovered adlfs write
    surface (fresh candidate): `prompt_logger`; plus lease/SAS cost-journal
    paths.
13. **Recorder reject-before-write / min-content-bytes floor +
    is_waf_challenge "Client Challenge" signature** — parser/recorder
    hygiene (S31+S32 folds). NOT a fix unless a future session scopes
    `tools/synthetic_crawl/` or `scraper/parser.py`.

---

## Locked artifact reminders for Session 38

Carry-forward from Sessions 8-37. **NEW S37 LOCK**:
- `tests/classifier/pipeline/test_partitioned_shard_writer_adls_azurite.py`
  at `f4e0a4a` (389 LOC; 1 `@pytest.mark.live` PartitionedShardWriter adlfs
  test + its own module-scoped Azurite fixture on port 10004 / container
  `barcada-azurite-partitioned`). Do NOT modify without Phase 2
  authorization. It auto-joins `live-integration.yml`'s `-m live` dir
  selection; keep its live marker + the `AzureBlobFileSystem` teeth
  assertion + the `write_to_dataset`/`HivePartitioning` drive + the
  container pre-`mkdir` intact.

Prior live-ADLS locks (unchanged):
- **S36 LOCK**: `test_page_storage_adls_azurite.py` at `25c3696`
  (343 LOC; port 10003 / `barcada-azurite-pages`; 1 `@pytest.mark.live`
  page_storage adlfs test with `AZURE_STORAGE_CONNECTION_STRING` env-var
  auth). Keep its live marker + the `AzureBlobFileSystem` teeth + the
  env-var seam intact.
- **S35 LOCK**: `test_parquet_writer_adls_azurite.py` at `f80ccdc`
  (309 LOC; port 10002 / `barcada-azurite-parquet`; 1 `@pytest.mark.live`
  parquet ShardWriter adlfs test). Keep its live marker + the
  `AzureBlobFileSystem` teeth assertion intact.
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
  `ae9e627`). S29-S37 did NOT touch this surface.
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
  EMPIRICALLY VALIDATED against Azurite via adlfs at S35 (`ShardWriter`
  single-file path) AND S37 (`PartitionedShardWriter` Hive
  `write_to_dataset` path). Both live tests inject only the public
  `storage_options=` seam + `abfss://` URL; the module is UNMODIFIED.
  BOTH halves of the module's live ADLS coverage are now closed.
- `classifier/page_acquisition/page_storage.py` — `write_pages` /
  `_write_pages_via_fsspec` / `_write_pages_local`. EMPIRICALLY VALIDATED
  against Azurite via adlfs at S36 (the S36 test injects only the public
  `write_pages` seam + `abfss://` URL + the `AZURE_STORAGE_CONNECTION_STRING`
  env var; it did NOT modify the module).
- `tests/classifier/page_acquisition/test_page_storage.py` — the
  hermetic `file://` guard for `write_pages`; locked.
- `tests/test_parquet_writer.py` — 33 hermetic `file://` tests (incl. 14
  PartitionedShardWriter tests); the default-run guard; locked.
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
  Phase 2 gate authorizes a specific module. S26+S27+S29-**S37**
  added NO new src/ authorizations (S35 + S36 + S37 were test-only
  additions).
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-38-open baseline

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

Sub-totals identical to S27-S37 close: 210 conformance + 52 driver
+ 99 baseline_v0 + 33 synthetic_crawl + 32 robots + 30 robots_gate
+ 30 robots_bypass_config + 43 cost_journal + 13 cost_journal_local
+ 19 cost_journal_adls + 35 robots_integration + 74 vmss_worker +
129 job_runner + 152 worker_loop + 7 robots_gate_integration + 12
worker_loop_persistence = 970. (ALL FIVE Azurite tests are
live-marked + skip-by-default and are NOT in this invocation.)

OUT-OF-BAND live tests (NOT in the canonical count; need Docker +
the Azurite image, else SKIP):

```
.venv/bin/python -m pytest -m live tests/classifier/pipeline/
# Expected: 5 passed, 209 deselected
# (CI live-integration.yml runs exactly this + a skip-fail guard.)
# Ports: S33=10000, S34=10001, S35=10002, S36=10003, S37=10004.
```

Cumulative-test-count gate: the count NEVER decreases between commit
boundaries.

Narrower baselines (still valid for S38 candidates that don't
exercise the ADLS test paths): 480 / 538 / 944.

**Fixture-count assertions for S38 Phase 0 Step 0.4**: html_count=222,
expected_count=202, meta_count=222, baseline_count=1213,
**`cassette_count == 30`, `exclusions_count == 30`** (UNCHANGED).

---

## Pre-push gate at Session 38 open

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
S37 close and S38 open, the gate blocks even though no S38 commit
touches eval_data. Per LESSONS: surface to operator with the
row+detail, propose operator-fix or stash-and-restore; do NOT
auto-fix. S37 ran the gate clean at Phase 4 (0 errors / 0 warnings).

---

## Context-window awareness

Session 37 ran Phase 0 → Phase 6 in a single context window with 1
repo commit (Phase 0 verify + Phase 1 scope + Phase 2 source-verify +
operator-confirmed design + Phase 3 impl with a build-time spike that
caught the container-creation race + Phase 6 close-out), within budget.
Session 38 budget per chosen candidate:

- Candidate A (barcada-drift): only if launchd job has run ≥2 times
  AND AI/ML decisions ready. ~370-400 LOC delivered.
- Candidate D: operator-led; tooling only.
- Candidate E: EXHAUSTED; not available without a plan-bound revision.
- A NEW live-ADLS candidate (`prompt_logger` adlfs path, or lease/SAS):
  size at Phase 2; default to operator-smoke posture unless a named
  carve-out justifies CI.

Strategies (unchanged from S20-S37 prompts):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-service-backed test, default to the S33/S34/S35/S36/S37
  fixture shape: unconditional try/finally teardown + idempotent
  self-healing pre-clean + skip-if-unavailable; expect an
  SDK-vs-emulator version-skew flag may be needed; use a DISTINCT
  port + container name if it must coexist with the existing live
  fixtures (S33=10000, S34=10001, S35=10002, S36=10003, S37=10004 →
  use 10005+); keep the test off the canonical headline (live marker,
  skip-by-default) unless a deliberate decision adds it.
- **Survey ADLS coverage by CLIENT STACK (azure-storage-blob SDK vs
  fsspec/adlfs), not by "is there an Azurite test" (S35 LESSONS); AND
  survey the AUTH seam — read the production call site's signature to see
  whether auth is an injected kwarg or env-resolved (S36 LESSONS).**
- **For any `pq.write_to_dataset`/`ds.write_dataset` path over adlfs,
  pre-create the container via `fs.mkdir` (catch `FileExistsError`); a
  multi-partition write against a FRESH container hits adlfs's
  non-idempotent `create_container`. Make the spike write MULTIPLE
  partitions to expose it (S37 LESSONS).**
- **Verify a carve-out against the TEST BODY, not its name/marker
  (S34 LESSONS) — and re-verify when CI-wiring an existing test.**
- Source-verify facts behind option-set design BEFORE AskUserQuestion
  drafts (S25 LESSONS).
- For a URL-only `fsspec.url_to_fs` resolution, clear the adlfs instance
  cache (`AzureBlobFileSystem.clear_instance_cache()`) so a stale anon
  instance is not reused (S36 LESSONS).
- Phase 0 fixture-count commands use the Python `rglob()` pattern,
  NOT bare `find` (S28 post-close LESSONS).
- Markdown-rendered shell commands may carry NBSP in whitespace-
  sensitive args; stage scripts to a file via the Write tool when
  exactness matters (re-confirmed S34/S35/S36/S37 — secrets-referencing
  inline `python -c` also trips the env hook; file-staged scripts work).
- The `rm -f` / `rm -rf` / `find -delete` forms are env-hook-blocked
  (re-confirmed S35: a `docker rm -f` pre-clean in an inline Bash call
  tripped the destructive-op hook). Operator runs destructive cleanup
  via `! rm ...`; inside test fixtures the `docker rm -f` runs fine
  (the hook gates the agent's Bash calls, not subprocess in pytest).

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S38 scope closes, transition
  per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-37:

1. Commit SHA(s) of each Session 38 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 970 baseline → S38 close.
4. Driver suite count (52/52 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (W0 closed S27; W A.1 closed S22; W A.2
   final-milestone tag `workstream-a-week2-end` OFFERED+DEFERRED at
   S33 AND S34 AND S35 AND S36 AND S37).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 37 handoff template. Refill at Session 38 close.
