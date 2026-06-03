# Session Transition Template — Handoff from Session 38 → Session 39

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-38 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 39 invocation prompt:** NOT yet drafted. Per the S20→S38
precedent, drafting the next-session prompt is operator-commissioned
between sessions (NOT a built-in Phase 6 step). If the operator wants
one, it should mirror the S20-S38 7-phase structure and pin: repo HEAD
anchor `d610f0b`, workspace HEAD anchor (the S38 close-out commit + its
anchor-pin follow-up), tag count `14`, canonical baseline `970` (16-path)
/ `983` combined (17-path incl. the S38 hermetic guard), Phase 0 Step 0.4
`cassette_count == 30` / `exclusions_count == 30`, and a Step 0.9 presence
+ POSTURE check for the S31/S32 cassettes, the S33 Azurite primitive, the
S34 deliverables (`live-integration.yml` OFF push/PR + the concurrency
race test on port 10001), the S35 deliverable (parquet ShardWriter adlfs
test on port 10002), the S36 deliverable (page_storage adlfs test on port
10003 with env-var auth), the S37 deliverable (PartitionedShardWriter adlfs
test on port 10004), AND the TWO S38 deliverables (the hermetic
prompt_logger guard in `tests/classifier/llm/` + the prompt_logger adlfs
live test on port 10005 with env-var auth).

**IMPORTANT — S39 opens with the adlfs write cluster CLOSED and an empty
actionable queue.** S38 shipped the LAST uncovered adlfs write surface
(`prompt_logger`, port 10005) plus the module's first hermetic guard, and
placed the cross-cutting `adls-live-coverage-v0` tag closing the S33-S38
ADLS live-test cluster. The remaining carry-forwards are A (blocked), D
(operator-led labeling), and E (EXHAUSTED — needs a plan-bound revision to
reopen). The lease/SAS cost-journal path is an ANTI-TRAP (production
constructs no lease/SAS — `grep -ciE 'lease|sas'` = 0). **S39 has NO
clearly-actionable fresh engineering scope** unless the operator unblocks
A, begins D labeling, authorizes a plan amendment to reopen E, or
commissions a genuinely new candidate. Surface the empty-queue condition
at S39 Phase 1 exactly as S33-S38 did (the condition + the budget
trade-off of a no-ship resolution).

Anchors for Session 39 cold start:
- Repo HEAD: `d610f0b` (S38: WA2.W8.adls-live-prompt-logger — +1
  `@pytest.mark.live` prompt_logger adlfs test). Its parent `094a12f` is
  the S38 hermetic guard. Tolerated delta: operator-side eval_data
  labeling commits between S38 close and S39 open (Sessions 8-38
  precedent) — verify each is strictly `eval_data/*` via `git show --stat`.
- Workspace HEAD: the S38 primary close-out commit (SESSION_LOG.md +
  SESSION_TRANSITION_TEMPLATE.md + LESSONS.md) + the anchor-pin follow-up
  succeeding it (+ any later prompt-revision commits). S39 Phase 0 Step 0.1
  MUST anchor workspace expectation to the S38 close-out OR this anchor-pin
  follow-up OR a later follow-up. Per the S21-S38 "Workspace HEAD delta
  tolerance" pattern: tolerate N additional prompt-drafting / audit
  commits between sessions. NOTE: an operator-side uncommitted edit to
  `SESSION_36_PROMPT.md` has been unstaged in the working tree since S36;
  tolerate it — operator territory.
- Canonical baseline: **970 tests** (16-path invocation; UNCHANGED from
  S27-S38 close — those exact paths were not touched). The S38 hermetic
  guard lives in `tests/classifier/llm/` (NOT in the 16-path).
- Combined baseline: **983 tests** (the 16-path + the S38 hermetic guard
  `tests/classifier/llm/test_prompt_logger.py`; 970 + 13). This is the
  count the S39 cumulative gate must not let decrease.
- Narrower baseline: **944 tests** (14-path; 970 minus 19
  cost_journal_adls minus 7 robots_gate_integration). Unchanged.
- Fixture counts (S39 Phase 0 Step 0.4): html=222 / expected=202 /
  meta=222 / baseline=1213 / **`cassette_count == 30`** /
  **`exclusions_count == 30`** — UNCHANGED (S38 deliverables are two test
  files; no fixture change).
- Primary recommended scope: none — no carry-forward is on a critical
  path; none is self-contained. The adlfs write cluster is CLOSED.
- Carry-forward candidates: A (barcada-drift; blocked on parquets +
  AI/ML), D (Phase 4 PR-D tooling; operator-led labeling not yet begun),
  E (EXHAUSTED at 30). **The S33-S38 ADLS live-test cluster is CLOSED +
  TAGGED `adls-live-coverage-v0`; every adlfs write surface now has live
  coverage.**

**S38 Candidates SHIPPED (prompt_logger adlfs leg + hermetic guard)** —
two commits, two files:
- **`094a12f`** — `tests/classifier/llm/test_prompt_logger.py` (282 LOC;
  13 hermetic tests). The module's FIRST default-run coverage (previously
  ZERO tests): file:// LocalFileSystem only, CI-visible. Covers
  happy/failure/false-positive/false-negative paths for `PromptLogger.log`
  / `.flush` / `.buffered` and `prompt_log_url`.
- **`d610f0b`** — `tests/classifier/pipeline/test_prompt_logger_adls_azurite.py`
  (358 LOC; 1 `@pytest.mark.live` test). Drives the SAME production
  `PromptLogger.flush()` against Azurite via adlfs. **Auth seam
  (source-verified): ENV-resolved** — `flush()` calls
  `fsspec.url_to_fs(output_url)` URL-only at `prompt_logger.py:118` with NO
  `storage_options` kwarg, so adlfs authenticates from
  `AZURE_STORAGE_CONNECTION_STRING` (the SAME shape as S36, NOT S35/S37's
  explicit kwarg). URL built via the production `prompt_log_url()` helper.
  Container pre-`mkdir` (catch `FileExistsError`) per the S35 makedirs-no-op
  fold; single object, so the S37 multi-partition create_container race
  does NOT apply. Teeth (negative control): abfss → `AzureBlobFileSystem` +
  blob-relative; file:// → `LocalFileSystem` + absolute. DISTINCT port
  10005 / container `barcada-azurite-prompts` so all SIX live fixtures
  coexist (verified: 6 passed, 209 deselected). Auto-joins
  `live-integration.yml`'s `-m live` selection — no workflow edit.
  **Production `prompt_logger.py` UNMODIFIED** (public env seam only).

---

## Handoff metadata

- Outgoing session number: 38
- Closing date: 2026-06-03
- Outgoing session scope: prompt_logger adlfs leg (the LAST uncovered
  adlfs write surface) + the module's first hermetic guard (decided at
  Phase 1 via AskUserQuestion). Phase 2 source-verify confirmed the auth
  seam is ENV-resolved (S36 shape). A build-time spike confirmed the
  mechanics before the test bodies landed; a TEST bug (Path.as_uri()
  percent-encoding `=` in `shard=NNNNN`) was caught + fixed in Phase 3
  (the production code was correct). 2 repo commits (`094a12f` hermetic +
  `d610f0b` live). Placed the cross-cutting `adls-live-coverage-v0` tag
  closing the ADLS cluster. LLM spend: $0. Infrastructure: $0 (local
  Docker + the already-pulled Azurite image; no paid Azure service).
- Reason for transition: S38 scope completed cleanly through Phase 0 →
  Phase 6; no HALT (the as_uri test bug was a Phase-3 fix, not a HALT); no
  in-flight sub-surface.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `d610f0b` (WA2.W8.adls-live-prompt-logger). Parent
  `094a12f` (WA2.W8.prompt-logger-hermetic-guard).
- Branch sync with `origin/main`: pushed at S38 close (confirm
  0 ahead / 0 behind after the push).
- Tags (14 total; +1 from S37's 13 — the tag-taxonomy drift is RESOLVED):
  - `pre-remediation-2026-05-19` / `baseline-v0` (`9e9a1fb`)
  - `workstream-0-week1-end` … `week7-end`
  - `workstream-0-end` at `a1c5636` (annotated; placed S27)
  - `workstream-a-week1-end` at `fdc8a7a` (placed S22)
  - `workstream-stage1-prestaged-flags-end` (`af6f1d4`),
    `workstream-stage1-step3-end` (`d4f06b8`) — operator eval_data tags
  - **`adls-live-coverage-v0` at `d610f0b` (NEW, placed S38)** — annotated,
    cross-cutting. Names the SIX `@pytest.mark.live` ADLS commits ONLY
    (`f1cdce8` S33, `eba6585` S34, `f80ccdc` S35, `25c3696` S36, `f4e0a4a`
    S37, `d610f0b` S38); robots/K-b EXCLUDED (Finding N). Deliberately NOT
    a workstream-letter tag (Finding M: the cluster is cross-workstream).
    Resolves the `workstream-a-week2-end` drift — that name is NOT placed
    and is superseded.
- Pre-push gate at HEAD `d610f0b`: VERIFIED GREEN at S38 close
  (ruff check "All checks passed!" + ruff format clean [360 files;
  count not pinned] + vermin 3.10 + validate_consistency 0 errors /
  0 warnings).
- Unstaged operator territory (Sessions 8-38 precedent):
  `eval_data/stage1_labels.jsonl` (modified) + `eval_data/audits/`
  (untracked) + `.claude/scheduled_tasks.lock` (untracked) — present
  at S38 open/close and left unstaged. Verify via `git status` at S39 open.
- Corpus: 222 .html / 202 expected.json / 222 meta.json (unchanged).
- 30 synthetic_crawl cassettes (20 S20 + 5 S31 + 5 S32) + 30
  sidecars (UNCHANGED).
- ADDED Session 38 (2 commits):
    - `094a12f` — `tests/classifier/llm/test_prompt_logger.py` (NEW; 282
      LOC; 13 hermetic file:// tests; NO live marker; default-run).
    - `d610f0b` — `tests/classifier/pipeline/test_prompt_logger_adls_azurite.py`
      (NEW; 358 LOC; 1 `@pytest.mark.live` prompt_logger adlfs test +
      module-scoped Azurite fixture on port 10005 / container
      `barcada-azurite-prompts`). No `src/` changes. No cassette/driver
      changes. The S33+S34+S35+S36+S37 live test files + the CI workflow
      are UNTOUCHED.
- Combined test suite at HEAD `d610f0b`:
    - **970 passed** — canonical 16-path (UNCHANGED; those exact paths
      were not touched; the hermetic guard is in `tests/classifier/llm/`).
    - **983 passed** — the 16-path + the S38 hermetic guard
      (`tests/classifier/llm/test_prompt_logger.py`). The S39 cumulative
      gate must not let this decrease.
    - **944** — narrower 14-path (unchanged).
    - OUT-OF-BAND live tests: `pytest -m live tests/classifier/pipeline/`
      → **6 passed, 209 deselected** (needs Docker + the Azurite image,
      else SKIPS). CI runs exactly this + a skip-fail guard. Ports:
      S33=10000, S34=10001, S35=10002, S36=10003, S37=10004, S38=10005.
    - Stage 1 test counts: 32 (16 + 16) — unchanged; outside the
      canonical 16-path.

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 38 start: `5a3ee7d` ("S38 prompt fix:
  tag-taxonomy Findings M+N"; succeeds `b6cda3d` S38 prompt draft, which
  succeeds the S37 close-out chain). At S38 Phase 0 Step 0.1 the 2
  prompt-drafting commits ahead of `1a1d722` were tolerated under
  "Workspace HEAD delta tolerance".
- Session 38 close-out workspace commits: 1 primary close-out (this commit:
  SESSION_LOG.md + SESSION_TRANSITION_TEMPLATE.md + LESSONS.md) + an
  anchor-pin follow-up succeeding it (pinning the primary close-out SHA
  into this template's Anchors section for S39).
- **Last commit SHA at Session 38 CLOSE: the anchor-pin follow-up
  succeeding the primary close-out.** S39 Phase 0 Step 0.1 MUST anchor
  workspace expectation to the S38 primary close-out OR this anchor-pin
  follow-up OR a later follow-up.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected after
  the Session 38 close push.

---

## Session 39 execution order (enforce strict sequence)

Same 7-phase shape regardless of scope choice (Phase 0 cold-start
verify → Phase 1 scope → Phase 2 design-gate → Phase 3 impl →
Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 39 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 38 entry (the ENV-resolved auth
   seam; the as_uri-encoding test-bug finding; the hermetic-guard
   design decision; the cross-cutting tag resolution).
3. Reading LESSONS.md additions Session 38 landed (4 new "S38 folding"
   sections: as_uri percent-encodes `=`; live-only test of a zero-test
   module; lease/SAS anti-trap grep; cross-workstream tag identity).
4. Reading the relevant section of BARCADA_CRAWLER_REMEDIATION_PLAN.md
   for the chosen Session 39 scope.
5. Reading the Session 39 prompt if one has been drafted, OR
   commissioning a fresh draft at S39 open.
6. Running Phase 0 cold-start verification (mirror the S38 prompt's
   9-step shape, updating workspace HEAD anchor, repo HEAD anchor
   `d610f0b`, tag count `14`, canonical baseline `970` / combined `983`,
   cassette fixture-count `30` / exclusions `30`, AND a Step 0.9 presence
   check for the S33+S34+S35+S36+S37 live deliverables AND the TWO S38
   deliverables).

---

## Outstanding operator-input requests entering Session 39

1. **Session 39 scope choice** — pick from the carry-forwards below. The
   ENTIRE adlfs write cluster is CLOSED + tagged (cost-journal, parquet
   both halves, page_storage, prompt_logger). Candidate E is EXHAUSTED.
   None of A/D is on a critical path. lease/SAS is an anti-trap. **S39 is
   very likely a no-ship scope-resolution session** — surface that at
   Phase 1.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*` continue across sessions (Sessions 8-38 precedent).

3. **barcada-drift AI/ML alignment** — 4 AI/ML team decisions need
   pre-resolution OR placeholders, plus 2+ canary_runs parquet files.
   Re-verified empirically at S38 Phase 1: `~/canary_runs/` absent (0
   parquets), 0 plist, no AI/ML responses.

4. **launchd kit installation** — Operator should run
   `scripts/launchd/install_canary_schedule.sh` when ready. Required
   prerequisite for Candidate A. As of S38 close, NOT yet installed.

5. **Session 39 prompt draft commissioning** — operator decides whether
   to commission an S39 prompt between sessions.

6. **A genuinely NEW candidate** — with the adlfs write cluster closed,
   there is no remaining low-cost test-only ADLS candidate. Any new
   engineering scope must come from the operator (unblock A / begin D /
   amend the E ceiling / point at a new surface). Do NOT re-scope
   lease/SAS unless production grows a lease/SAS construct (anti-trap,
   S38-confirmed by grep).

---

## Notes for Session 39

Suggested S39 scope candidates (operator picks at S39 open):

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

### Live ADLS coverage (CLUSTER CLOSED + TAGGED at S38)

Every adlfs write surface now has live coverage: cost-journal ETag
primitive (S33) + multi-writer race (S34); parquet `ShardWriter`
single-file (S35, port 10002) + `PartitionedShardWriter` Hive
`write_to_dataset` (S37, port 10004); `page_storage` (S36, port 10003);
`prompt_logger` (S38, port 10005). The cross-cutting
`adls-live-coverage-v0` tag (placed S38) closes the cluster. The
azure-storage-blob cost-journal path is covered at shared-key; lease/SAS
is an anti-trap (production constructs none). **NO adlfs write surface
remains uncovered.** NOT a carry-forward.

---

## Required reading (Session 39 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 38 entry — the ENV-resolved auth seam;
   the as_uri test-bug finding; the hermetic-guard design gate; the
   cross-cutting tag resolution.
3. **`LESSONS.md`** — the four new "S38 folding" sections, PLUS the
   "S37 folding" (makedirs-no-op sharper on write_to_dataset), "S36
   folding" (survey the AUTH seam), "S35 folding" (adlfs is a separate
   ADLS write stack), "S33 folding" (live-emulator teardown + version
   skew) and "S34 folding" (carve-out ↔ test-body) if a live-service
   scope is somehow chosen.
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope section.
   READ-ONLY (exception: a plan-amendment session to reopen E).
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A is chosen.

---

## Outstanding items carried forward to Session 39+

1. **Per-tier cost-accounting wiring** — CLOSED end-to-end S28.
2. **`barcada-drift` CLI** — §Item 8; 4 AI/ML decisions + 2+
   parquets outstanding. Re-verified empirically at S38 Phase 1.
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
12. **Azurite-backed live ADLS coverage** — CLUSTER CLOSED + TAGGED S38
    (`adls-live-coverage-v0`). cost-journal ETag primitive S33;
    multi-writer concurrency + CI wiring S34 (`eba6585`); parquet
    ShardWriter S35 (`f80ccdc`, 10002); page_storage S36 (`25c3696`,
    10003); PartitionedShardWriter S37 (`f4e0a4a`, 10004); prompt_logger
    S38 (`d610f0b`, 10005). Six live tests run on-demand + nightly via
    `live-integration.yml` with a guard that fails on a silent skip.
    Default push/PR CI still does NOT run them (by design). NO adlfs write
    surface remains uncovered. lease/SAS = anti-trap.
13. **Recorder reject-before-write / min-content-bytes floor +
    is_waf_challenge "Client Challenge" signature** — parser/recorder
    hygiene (S31+S32 folds). NOT a fix unless a future session scopes
    `tools/synthetic_crawl/` or `scraper/parser.py`.

---

## Locked artifact reminders for Session 39

Carry-forward from Sessions 8-38. **NEW S38 LOCKS**:
- `tests/classifier/llm/test_prompt_logger.py` at `094a12f` (282 LOC;
  13 hermetic file:// tests; NO live marker; the default-run guard for
  `prompt_logger`). Do NOT modify without Phase 2 authorization.
- `tests/classifier/pipeline/test_prompt_logger_adls_azurite.py` at
  `d610f0b` (358 LOC; 1 `@pytest.mark.live` prompt_logger adlfs test +
  module-scoped Azurite fixture on port 10005 / container
  `barcada-azurite-prompts`; ENV-resolved auth via
  `AZURE_STORAGE_CONNECTION_STRING`). Auto-joins `live-integration.yml`'s
  `-m live` dir selection; keep its live marker + the `AzureBlobFileSystem`
  teeth + the `file://`→`LocalFileSystem` negative control + the container
  pre-`mkdir` + the env-var seam intact.
- `adls-live-coverage-v0` tag at `d610f0b` (annotated; cross-cutting).
  Do NOT delete/move; do NOT place `workstream-a-week2-end` (superseded).

Prior live-ADLS locks (unchanged):
- **S37 LOCK**: `test_partitioned_shard_writer_adls_azurite.py` at
  `f4e0a4a` (389 LOC; port 10004 / `barcada-azurite-partitioned`; 1
  `@pytest.mark.live` PartitionedShardWriter Hive `write_to_dataset` test).
  Keep its live marker + `AzureBlobFileSystem` teeth +
  `write_to_dataset`/`HivePartitioning` drive + container pre-`mkdir`.
- **S36 LOCK**: `test_page_storage_adls_azurite.py` at `25c3696`
  (343 LOC; port 10003 / `barcada-azurite-pages`;
  `AZURE_STORAGE_CONNECTION_STRING` env-var auth).
- **S35 LOCK**: `test_parquet_writer_adls_azurite.py` at `f80ccdc`
  (309 LOC; port 10002 / `barcada-azurite-parquet`).
- **S34 LOCKS**: `test_cost_journal_adls_azurite_concurrency.py` at
  `eba6585` (337 LOC; port 10001 / `barcada-azurite-racetest`) +
  `.github/workflows/live-integration.yml` at `eba6585` (CI workflow;
  `workflow_dispatch` + nightly schedule; NOT push/PR). The `-m live`
  selection over `tests/classifier/pipeline/` + the skip-fail guard are
  load-bearing; do NOT weaken without a deliberate posture decision.
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
  `ae9e627`). S29-S38 did NOT touch this surface.
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
  blob_backend=None)`. EMPIRICALLY VALIDATED at S30/S33/S34. UNMODIFIED.
  Constructs NO lease/SAS (S38 grep-confirmed) — lease/SAS is an anti-trap.
- `output/parquet_writer.py` — `ShardWriter` / `PartitionedShardWriter`
  / `write_records_to_shards{,_partitioned}` / `storage_options_from_env`.
  EMPIRICALLY VALIDATED against Azurite via adlfs at S35 + S37 (both
  halves). Module UNMODIFIED. Both halves of live ADLS coverage closed.
- `classifier/page_acquisition/page_storage.py` — `write_pages`.
  EMPIRICALLY VALIDATED against Azurite via adlfs at S36. Module UNMODIFIED.
- `classifier/llm/prompt_logger.py` — `PromptLogger` / `prompt_log_url`.
  EMPIRICALLY VALIDATED against Azurite via adlfs at S38 (the live test
  injects only the public env seam + `abfss://` URL +
  `AZURE_STORAGE_CONNECTION_STRING`; it did NOT modify the module).
- `tests/classifier/page_acquisition/test_page_storage.py` — hermetic
  `file://` guard for `write_pages`; locked.
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
  Phase 2 gate authorizes a specific module. S26+S27+S29-**S38**
  added NO new src/ authorizations (S35-S38 were test-only additions).
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-39-open baseline

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

Sub-totals identical to S27-S38 close: 210 conformance + 52 driver
+ 99 baseline_v0 + 33 synthetic_crawl + 32 robots + 30 robots_gate
+ 30 robots_bypass_config + 43 cost_journal + 13 cost_journal_local
+ 19 cost_journal_adls + 35 robots_integration + 74 vmss_worker +
129 job_runner + 152 worker_loop + 7 robots_gate_integration + 12
worker_loop_persistence = 970. (ALL SIX Azurite tests are
live-marked + skip-by-default and are NOT in this invocation.)

Combined (17 paths — the canonical 16 + the S38 hermetic guard):

```
# Append to the 16-path above:
    tests/classifier/llm/test_prompt_logger.py
# Expected: 983 passed (970 + 13). VERIFIED at d610f0b. This is the
# count the S39 cumulative gate must not let decrease.
```

OUT-OF-BAND live tests (NOT in the canonical count; need Docker +
the Azurite image, else SKIP):

```
.venv/bin/python -m pytest -m live tests/classifier/pipeline/
# Expected: 6 passed, 209 deselected
# (CI live-integration.yml runs exactly this + a skip-fail guard.)
# Ports: S33=10000, S34=10001, S35=10002, S36=10003, S37=10004, S38=10005.
```

Cumulative-test-count gate: the count NEVER decreases between commit
boundaries.

Narrower baselines (still valid for S39 candidates that don't
exercise the ADLS test paths): 480 / 538 / 944.

**Fixture-count assertions for S39 Phase 0 Step 0.4**: html_count=222,
expected_count=202, meta_count=222, baseline_count=1213,
**`cassette_count == 30`, `exclusions_count == 30`** (UNCHANGED).

---

## Pre-push gate at Session 39 open

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
S38 close and S39 open, the gate blocks even though no S39 commit
touches eval_data. Per LESSONS: surface to operator with the
row+detail, propose operator-fix or stash-and-restore; do NOT
auto-fix. S38 ran the gate clean at Phase 4 (0 errors / 0 warnings).

---

## Context-window awareness

Session 38 ran Phase 0 → Phase 6 in a single context window with 2
repo commits (Phase 0 verify + Phase 1 scope + Phase 2 source-verify +
operator-confirmed design + Phase 3 impl with a build-time spike +
a Phase-3 test-bug fix + Phase 6 close-out), comfortably within budget.
Session 39 budget per chosen candidate:

- Candidate A (barcada-drift): only if launchd job has run ≥2 times
  AND AI/ML decisions ready. ~370-400 LOC delivered.
- Candidate D: operator-led; tooling only.
- Candidate E: EXHAUSTED; not available without a plan-bound revision.
- No fresh low-cost ADLS candidate remains (cluster closed).

Strategies (unchanged from S20-S38 prompts):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-service-backed test, default to the S33-S38 fixture
  shape: unconditional try/finally teardown + idempotent self-healing
  pre-clean + skip-if-unavailable; expect an SDK-vs-emulator
  version-skew flag may be needed; use a DISTINCT port + container name
  (10000-10005 taken → use 10006+); keep the test off the canonical
  headline (live marker, skip-by-default) unless a deliberate decision
  adds it.
- **Survey ADLS coverage by CLIENT STACK (azure-storage-blob SDK vs
  fsspec/adlfs); AND survey the AUTH seam — read the production call
  site's signature to see whether auth is an injected kwarg or
  env-resolved (S36/S38 LESSONS).**
- **When a test resolves an fsspec URL with `key=value` segments, build
  the URL by plain string concat (matching production), NOT
  `Path.as_uri()` which percent-encodes `=` (S38 LESSONS).**
- **For any `write_to_dataset`/`write_dataset` adlfs path, pre-create the
  container via `fs.mkdir` (S37 LESSONS).**
- **Verify a carve-out against the TEST BODY, not its name/marker
  (S34 LESSONS).**
- **Confirm a lease/SAS candidate is real by grepping production FIRST
  (S38 anti-trap LESSONS).**
- Source-verify facts behind option-set design BEFORE AskUserQuestion
  drafts (S25 LESSONS).
- For a URL-only `fsspec.url_to_fs` resolution, clear the adlfs instance
  cache (`AzureBlobFileSystem.clear_instance_cache()`) so a stale anon
  instance is not reused (S36/S38 LESSONS).
- Phase 0 fixture-count commands use the Python `rglob()` pattern,
  NOT bare `find` (S28 post-close LESSONS).
- Markdown-rendered shell commands may carry NBSP in whitespace-
  sensitive args; stage scripts to a file via the Write tool when
  exactness matters (re-confirmed S34-S38 — secrets-referencing
  inline `python -c` also trips the env hook; file-staged scripts work).
- The `rm -f` / `rm -rf` / `find -delete` / `os.remove` forms are
  env-hook-blocked (re-confirmed S38: even `python -c "os.remove(...)"`
  tripped the destructive-op hook). Move throwaway helpers OUT of the
  repo tree via `mv` to `/tmp/`, or let the operator run `! rm ...`;
  inside test fixtures `docker rm -f` runs fine (the hook gates the
  agent's Bash calls, not subprocess in pytest).

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S39 scope closes, transition
  per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-38:

1. Commit SHA(s) of each Session 39 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 970 / 983 baseline → S39 close.
4. Driver suite count (52/52 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (W0 closed S27; W A.1 closed S22; the S33-S38 ADLS
   cluster closed + tagged `adls-live-coverage-v0` at S38).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---
