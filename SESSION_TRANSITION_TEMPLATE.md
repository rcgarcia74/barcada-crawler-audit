# Session Transition Template — Handoff from Session 40 → Session 41

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-40 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**PRIMARY LIVE CANDIDATE for Session 41: A-classify PART 1 (the `--classify`
producer) — DEFERRED at S40, BLOCKED, precisely gated.** S40 shipped A-classify
PART 2 (the classify-drift COMPARATOR, `3266bc4`); PART 1 (the cascade producer
that FEEDS it real prediction snapshots) is the carry-forward. **UNBLOCK CHECK
(run this FIRST at S41 open):** the producer needs a real parser_parquet
partition the scraper stage writes at **`worker_loop.py:193`**
(`.../parser/crawl_date=X/shard=NNNNN/has_website=*/bot_blocked=*/data-*.parquet`)
— it did NOT exist at S40 close (the parser has not produced one). If that path
still has no partition, PART 1 STAYS DEFERRED; do not commission it. Full PART 1
gates (a)-(d) live in `A_CLASSIFY_PROMPT.md` Open/carry-forward: (a) the
partition unblock check; (b) the Phase-0.COST gate APPLIES TO PART 1 (PART 2 was
$0; spend starts when the producer runs the cascade); (c) PREDICTION_COLUMNS
real-artifact re-verification is a PART 1 acceptance gate; (d) the re-scope flag
(consume-existing-partition vs inline-scraper). Other carry-forwards: D
(operator-led labeling), E (EXHAUSTED at 30).

**Session 41 invocation prompt:** `~/crawler-audit/A_CLASSIFY_PROMPT.md` is the
PART 1 spec (its PART 2 is now shipped — read it for the producer scope + the
(a)-(d) gates). Any S41 prompt should pin: repo HEAD anchor `3266bc4`, workspace
HEAD anchor (the S40 close-out commit + its anchor-pin follow-up), tag count
`15`, canonical baseline `970` (16-path) / **`1026`** combined (970 + the 13-test
S38 hermetic guard + the **43-test** S39+S40 drift sub-suite), Step 0.4
`cassette_count == 30` / `exclusions_count == 30`, and a Step 0.9 presence check
for the S33-S38 ADLS deliverables + the drift deliverables (drift.py +
drift_classify.py + tests/drift/).

**S40 shipped the drift workstream's DETECTION half; the workstream is
HALF-SHIPPED.** S39 shipped A-fetch (fetch-reachability comparator). S40 shipped
A-classify PART 2 (classifier-prediction comparator) extending the same `drift`
subcommand. Detection now exists for BOTH fetch and classify drift — but the
classify producer (the feed) is deferred (above). The part-scoped tag
`barcada-drift-classify-part2-v0` marks this; the workstream-closing tag waits
for PART 1.

Anchors for Session 41 cold start:
- Repo HEAD: `3266bc4` (S40: WA0.W7.classify-drift-comparator — drift_classify.py
  + classify metrics on the `drift` subcommand + tests/drift/test_drift_classify.py).
  Parent `7bbdc74` (S39 A-fetch). Tolerated delta: operator-side eval_data
  labeling commits between S40 close and S41 open — verify each is strictly
  `eval_data/*` via `git show --stat`.
- Workspace HEAD: the S40 primary close-out commit (SESSION_LOG.md +
  SESSION_TRANSITION_TEMPLATE.md + LESSONS.md + A_CLASSIFY_PROMPT.md PART 1
  carry-forward) + the anchor-pin follow-up succeeding it. S41 Phase 0 Step 0.1
  anchors workspace expectation there. NOTE: the operator-side uncommitted edit
  to `SESSION_36_PROMPT.md` is still unstaged since S36 — tolerate it.
- Canonical baseline: **970 tests** (16-path; UNCHANGED from S27-S40 close — the
  classify tests live in `tests/drift/`, outside the sweep; cli.py changed at
  S40 but the 16-path stayed 970, regression-checked).
- Combined baseline: **1026 tests** (the 16-path 970 + the S38 hermetic guard
  13 + the S39+S40 drift sub-suite `tests/drift/` **43** [22 fetch + 21
  classify]). This is the NEW cumulative-gate floor (was 1005 at S39); S41
  Phase 0.5 must assert against **1026, NOT 1005**, and never let it decrease.
- Narrower baseline: **944 tests** (14-path; 970 minus 19 cost_journal_adls
  minus 7 robots_gate_integration). Unchanged.
- Fixture counts (S40 Phase 0 Step 0.4): html=222 / expected=202 /
  meta=222 / baseline=1213 / **`cassette_count == 30`** /
  **`exclusions_count == 30`** — UNCHANGED (S39 deliverable is code + tests,
  no fixture change).
- Primary recommended scope: **A-classify** (prompt drafted + reviewed) — the
  one half-built workstream with a ready, source-verified prompt. First non-$0
  candidate; Phase-0.COST gated.
- Carry-forward candidates: A-classify (prediction-drift; cost-gated), D
  (Phase 4 PR-D tooling; operator-led labeling not yet begun), E (EXHAUSTED
  at 30).

**S39 Candidate SHIPPED (A-fetch — fetch-reachability drift comparator)** —
ONE commit, four files:
- **`7bbdc74`** (WA0.W7.drift-fetch-comparator):
  - `tools/baseline_v0/drift.py` (277 LOC) — the comparator. New `drift`
    subcommand: reads two canary parquet snapshots (`--baseline` run-N-1 /
    `--current` run-N), validates schema by importing
    `canary.PARQUET_COLUMNS` + `_make_dtypes` (require all 14, reject
    missing/dtype-mismatch, **TOLERATE EXTRAS**), inner-joins on `domain`
    (appeared/disappeared reported separately, never as drift), computes 4
    alerting metrics (reachability drop / robots flips / 5 exclusion-flag
    rises / per-domain 2xx→non-2xx regressions) + 2 informational deltas
    (body_bytes / elapsed_ms median, never gate), exit 0/1/2. stdout table +
    optional `--report` JSON (17 keys).
  - `tools/baseline_v0/cli.py` (+84) — `drift` subparser + dispatch; lazy
    default-constant import keeps `--help` dependency-light.
  - `tests/drift/__init__.py` (13) + `tests/drift/test_drift.py` (269; 22
    hermetic tests on synthetic parquets; bidirectional teeth + reverse teeth
    + schema/empty-intersection exit-2 + JSON-report + threshold-config).
  - **Production `canary.py` UNMODIFIED.** Provisional default thresholds
    (`--max-reachability-drop 0.05`, `--max-robots-flips 3`,
    `--max-exclusion-rate-rise 0.05`, `--max-regressions 1`) — flagged
    provisional until real snapshots calibrate.

---

## Handoff metadata

- Outgoing session number: 39
- Closing date: 2026-06-03
- Outgoing session scope: A-fetch — the fetch-reachability drift comparator
  (NEW operator-commissioned candidate that sidesteps A's blockers: no AI/ML
  decisions, no real parquets [synthetic test data], no launchd, ZERO LLM).
  Decided-before-invocation shape; Phase 1/2 design gates confirmed via
  AskUserQuestion. A Phase-3 baseline-bookkeeping HALT (tests first placed in
  the canonical-sweep `tests/baseline_v0/` → headline rose 970→992) was caught
  before commit and resolved by relocating to `tests/drift/`. 1 repo commit
  (`7bbdc74`). 1.TAG deferred (1-of-2 fork). LLM spend: $0. Infrastructure: $0.
- Also produced: `A_CLASSIFY_PROMPT.md` (the classify fork; reviewed twice
  against the live tree).
- Reason for transition: S39 scope completed cleanly Phase 0 → Phase 5; the
  baseline-bookkeeping HALT was resolved in-phase, not deferred; no in-flight
  sub-surface. Phase 6 close-out is this commit.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `3266bc4` (S40 WA0.W7.classify-drift-comparator). Parent
  `7bbdc74` (S39 WA0.W7.drift-fetch-comparator).
- Branch sync with `origin/main`: pushed at S40 close (`7bbdc74..3266bc4`;
  0 ahead / 0 behind verified).
- Tags (15 total; +1 from S39's 14 — S40 placed the part-scoped classify tag):
  - `pre-remediation-2026-05-19` / `baseline-v0` (`9e9a1fb`)
  - `workstream-0-week1-end` … `week7-end`
  - `workstream-0-end` at `a1c5636` (annotated; placed S27)
  - `workstream-a-week1-end` at `fdc8a7a` (placed S22)
  - `workstream-stage1-prestaged-flags-end` (`af6f1d4`),
    `workstream-stage1-step3-end` (`d4f06b8`) — operator eval_data tags
  - `adls-live-coverage-v0` at `d610f0b` (annotated; cross-cutting; names the
    SIX ADLS live commits S33-S38). Do NOT delete/move.
  - `barcada-drift-classify-part2-v0` at `3266bc4` (annotated; S40) —
    DELIVERABLE-SCOPED, NOT workstream-closing. The drift workstream is
    HALF-SHIPPED (detection without producer); the workstream-closing tag
    (`barcada-drift-classify-v0` or a workstream-end tag) waits for PART 1.
- Pre-push gate at HEAD `3266bc4`: VERIFIED GREEN at S40 close (ruff check
  "All checks passed!" + ruff format clean [365 files] + vermin 3.10 +
  validate_consistency 0 errors / 0 warnings).
- Unstaged operator territory (Sessions 8-39 precedent):
  `eval_data/stage1_labels.jsonl` (modified) + `eval_data/audits/`
  (untracked) + `.claude/scheduled_tasks.lock` (untracked) — present at S39
  open/close and left unstaged. Verify via `git status` at S40 open.
- Corpus: 222 .html / 202 expected.json / 222 meta.json (unchanged).
- 30 synthetic_crawl cassettes (20 S20 + 5 S31 + 5 S32) + 30 sidecars
  (UNCHANGED).
- ADDED Session 39 (1 commit, 4 files): `tools/baseline_v0/drift.py` (NEW;
  277 LOC) + `tools/baseline_v0/cli.py` (+84) + `tests/drift/__init__.py`
  (NEW; 13) + `tests/drift/test_drift.py` (NEW; 269; 22 tests). No `src/`
  changes. No cassette/driver changes. The S33-S38 live test files + the CI
  workflow + the S38 hermetic guard are UNTOUCHED.
- Combined test suite at HEAD `3266bc4`:
    - **970 passed** — canonical 16-path (UNCHANGED; the drift tests live in
      `tests/drift/`, OUTSIDE the sweep, by deliberate disposition).
    - **1026 passed** — the 16-path + the S38 hermetic guard
      (`tests/classifier/llm/test_prompt_logger.py`, 13) + the S39+S40 drift
      sub-suite (`tests/drift/`, **43** = 22 fetch + 21 classify). The S41
      cumulative gate must not let this decrease (was 1005 at S39).
    - **944** — narrower 14-path (unchanged).
    - OUT-OF-BAND live tests: `pytest -m live tests/classifier/pipeline/`
      → **6 passed, 209 deselected** (needs Docker + the Azurite image, else
      SKIPS). Ports: S33=10000 … S38=10005.
    - Stage 1 test counts: 32 (16 + 16) — unchanged; outside the canonical
      16-path.

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 39 start: `685ed13` (S38 baseline-clarity
  follow-up).
- Session 39 close-out workspace commits: 1 primary close-out `32273f4`
  (SESSION_LOG.md + SESSION_TRANSITION_TEMPLATE.md + LESSONS.md +
  A_CLASSIFY_PROMPT.md + SESSION_39_PROMPT.md) + this anchor-pin follow-up
  succeeding it (pinning `32273f4` into this template's Anchors section for
  S40).
- Branch sync with `origin/main`: 0 ahead / 0 behind expected after the
  Session 39 close push.

---

## Session 40 execution order (enforce strict sequence)

Same 7-phase shape regardless of scope choice (Phase 0 cold-start verify →
Phase 1 scope → Phase 2 design-gate → Phase 3 impl → Phase 4 pre-push →
Phase 5 push+tag → Phase 6 close-out). For A-classify, ADD the Phase-0.COST
spend gate (BLOCKING, before any live cascade run) per A_CLASSIFY_PROMPT.md.
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 40 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 39 entry (the A-fetch design gates; the
   baseline-bookkeeping HALT + tests/drift/ resolution; the A-classify audit
   findings).
3. Reading LESSONS.md additions Session 39 landed (the "S39 folding": "outside
   the 16-path" is a DIRECTORY fact, not a filename fact).
4. Reading the relevant section of BARCADA_CRAWLER_REMEDIATION_PLAN.md +
   CLASSIFICATION_ADJACENT_PLAN.md §Item 8 for the chosen S40 scope.
5. Reading A_CLASSIFY_PROMPT.md if A-classify is commissioned, OR
   commissioning a fresh draft at S40 open.
6. Running Phase 0 cold-start verification (mirror the prompt's 9-step
   shape, updating workspace HEAD anchor, repo HEAD anchor `3266bc4`, tag
   count `15`, canonical baseline `970` / combined `1026`, cassette
   fixture-count `30` / exclusions `30`, AND a Step 0.9 presence check for
   the S33-S38 ADLS deliverables AND the drift deliverables (drift.py +
   drift_classify.py + tests/drift/)).

---

## Outstanding operator-input requests entering Session 40

1. **Session 40 scope choice** — primary recommended: A-classify (prompt
   ready). Alternatives: D (operator-led labeling), E (plan-amendment to
   reopen). Surface at Phase 1.
2. **A-classify Phase-0.COST authorization** — A-classify routes 50 domains
   through the cascade (recurring LLM spend). The full-depth ceiling must be
   estimated + approved before ANY live run; default dev path is client-MOCK
   ($0). First non-$0 candidate — spend tracking vs the $100 ceiling is
   load-bearing.
3. **Eval_data labeling continuity** — operator-WIP edits to `eval_data/*`
   continue across sessions (Sessions 8-39 precedent).
4. **launchd kit installation** — `scripts/launchd/install_canary_schedule.sh`
   produces the real `canary_runs/*.parquet` the drift comparators consume in
   PRODUCTION (dev/test uses synthetic). NOT yet installed; A-fetch + A-classify
   ship dormant until it runs.
5. **Session 40 prompt** — A_CLASSIFY_PROMPT.md is ready; operator decides
   whether to commission it or a different scope.

---

## Notes for Session 40

Suggested S40 scope candidates (operator picks at S40 open):

### Candidate A-classify (PRIMARY; prompt drafted at A_CLASSIFY_PROMPT.md)

Extends the A-fetch comparator with classifier-prediction drift (Item-8
metric #1 — prediction agreement + KS on `signals_business_score`,
LABEL-FREE; calibration/Brier label-gated + OUT). TWO sub-surfaces: (PART 1) an
OPT-IN `--classify` producer leg that runs fetch → parser → cascade
components → async cascade → reads back `predictions.parquet` → appends
`PREDICTION_COLUMNS`; (PART 2) the classify metrics on the existing `drift`
subcommand. First non-$0 candidate (recurring LLM spend) → Phase-0.COST gate +
client-mock $0-dev. canary.py is TOOLING (editable); the src/ cascade is
INVOKED not modified. See A_CLASSIFY_PROMPT.md for the full source-verified
plan (the producer is bigger than a flag; the $0-dev path is client-mock NOT
vcrpy; the field is `signals_business_score`; `model_version` is the drift-
attribution signal).

### Candidate D (carry-forward): Phase 4 PR-D operator-led labeling

Unchanged. Tooling support only; labeling is operator territory. W0 closed
(`workstream-0-end` at `a1c5636`). Still gated on operator-led Stage 2/3
labeling start.

### Candidate E (EXHAUSTED at S32)

The cassette corpus reached the plan's **30 upper bound** at S32. **No further
+N without an explicit plan-bound revision** (raise the §4 W7 "~20-30" ceiling
first, as a plan-amendment session). Do NOT add cassettes under the current
plan.

### Live ADLS coverage (CLUSTER CLOSED + TAGGED at S38)

Every adlfs write surface has live coverage (cost-journal S33/S34, parquet
ShardWriter S35 + PartitionedShardWriter S37, page_storage S36, prompt_logger
S38). `adls-live-coverage-v0` at `d610f0b` closes the cluster. lease/SAS is an
anti-trap (production constructs none). NOT a carry-forward.

---

## Outstanding items carried forward to Session 40+

1. **Per-tier cost-accounting wiring** — CLOSED end-to-end S28.
2. **`barcada-drift` workstream** — A-fetch (fetch-reachability) SHIPPED S39
   (`7bbdc74`). A-classify (prediction-drift) is the next fork — prompt drafted
   at `A_CLASSIFY_PROMPT.md`; first non-$0 candidate, cost-gated.
3. **Cassette corpus expansion** — EXHAUSTED at 30. No further +N without a
   plan revision.
4. **Cassette-FP investigation** — archive.org + hashicorp.com + stripe.com
   (S20-locked; flags are correct behavior). DEFERRED.
5. **launchd kit smoke-then-install** — produces the real `canary_runs/*.parquet`
   the drift comparators consume in production. NOT yet installed.
6. **Phase 4 PR-D/E/F/G** — W0-side unblocked since S27; operator-led Stage 2/3
   labeling still needs to begin.
7-13. Prior CLOSED items (per-tier wiring S28; CRAWLING_POLICY S26; abfss
    CostJournal S25; live smoke script S29 + execution S30; ShardResult split
    S28; the full Azurite ADLS cluster CLUSTER CLOSED + TAGGED S38). Recorder
    reject-before-write / min-content-bytes + is_waf_challenge "Client
    Challenge" parser hygiene remain DEFERRED unless a session scopes
    `tools/synthetic_crawl/` or `scraper/parser.py`.

---

## Locked artifact reminders for Session 40

Carry-forward from Sessions 8-39. **NEW S39 LOCK**:
- `tools/baseline_v0/drift.py` at `7bbdc74` (277 LOC; the `drift` comparator;
  imports `canary.PARQUET_COLUMNS` + `_make_dtypes`; require-14 / tolerate-
  extras; inner-join + appeared/disappeared; exit 0/1/2; stdout + `--report`).
  A-classify EXTENDS this (auto-detect prediction columns) — do NOT fork it.
- `tools/baseline_v0/cli.py` `drift` subparser + dispatch at `7bbdc74`.
- `tests/drift/test_drift.py` at `7bbdc74` (269 LOC; 22 hermetic tests; NO
  live marker; OUTSIDE the canonical 16-path). A-classify ADDS to this dir;
  the existing 22 must stay green (fetch-only behavior unchanged).

S38 LOCKS (unchanged):
- `tests/classifier/llm/test_prompt_logger.py` at `094a12f` (282 LOC; 13
  hermetic file:// tests; NO live marker; the prompt_logger default-run guard).
- `tests/classifier/pipeline/test_prompt_logger_adls_azurite.py` at `d610f0b`
  (358 LOC; 1 `@pytest.mark.live` test; port 10005 / `barcada-azurite-prompts`;
  ENV-resolved auth). Keep its live marker + AzureBlobFileSystem teeth +
  file://→LocalFileSystem negative control + container pre-mkdir.
- `adls-live-coverage-v0` tag at `d610f0b`. Do NOT delete/move; do NOT place
  `workstream-a-week2-end` (superseded).

Prior live-ADLS locks (unchanged):
- **S37**: `test_partitioned_shard_writer_adls_azurite.py` at `f4e0a4a`
  (389 LOC; port 10004 / `barcada-azurite-partitioned`).
- **S36**: `test_page_storage_adls_azurite.py` at `25c3696` (343 LOC; port
  10003 / `barcada-azurite-pages`; env-var auth).
- **S35**: `test_parquet_writer_adls_azurite.py` at `f80ccdc` (309 LOC; port
  10002 / `barcada-azurite-parquet`).
- **S34**: `test_cost_journal_adls_azurite_concurrency.py` at `eba6585`
  (337 LOC; port 10001) + `.github/workflows/live-integration.yml` at
  `eba6585` (`workflow_dispatch` + nightly; NOT push/PR; the `-m live` over
  `tests/classifier/pipeline/` + skip-fail guard are load-bearing).
- **S33**: `test_cost_journal_adls_azurite.py` at `f1cdce8` (292 LOC; port
  10000) + the `live` marker in `pyproject.toml`.

Other locked artifacts (unchanged):
- `eval_data/` — labeling-workstream territory; operator-WIP expected.
- `stage1.schema.json` v1.0; `expected.schema.json` v1.1; `META_SCHEMA.md`
  v1.1; `meta.schema.json` v1.0.
- `pre-remediation-2026-05-19` / `baseline-v0` (`9e9a1fb`) tags; all
  `workstream-0-*-end`; `workstream-0-end` (`a1c5636`); `workstream-a-week1-end`
  (`fdc8a7a`); the 2 operator eval_data tags.
- `tests/runners/fixture_cascade/` — W4.1.5 driver; locked at `dd64963`
  except via W5.X commits (S27 `a1c5636`, S28 `9afde57` + `ae9e627`).
  S29-S39 did NOT touch this surface.
- `tests/fixtures/baseline-v0/` snapshot — locked at `9e9a1fb` (1213 files).
- `tools/baseline_v0/` (canary.py + cli.py generate/check/canary-run +
  generate.py/check.py/canary.py) + `tools/synthetic_crawl/` — locked except
  the S39 `drift` additions above. **canary.py is UNMODIFIED through S39 and
  is the producer A-classify will EXTEND (it is TOOLING, editable under a
  Phase-2 gate; the 14-col PARQUET_COLUMNS contract is FROZEN — append only).**
- `tests/fixtures/synthetic_crawls/` — 20 S20 (`7f11879`) + 5 S31 (`06d67c4`)
  + 5 S32 (`cfa0ec1`); never re-record/delete.
- `scripts/launchd/` — S20; locked. `scripts/smoke_test_adls_cost_journal.py`
  (`75a3937`; S29; 220 LOC).
- `src/barcada_scraper/scraper/robots.py` (`34a59b6`), `robots_gate.py`
  (`ba87e7e`), `robots_bypass_config.py` (`381ee89`) + tests — S21/S22.
- `cost_journal.py` (`1d9404e`); `cost_journal_local.py`; `cost_journal_adls.py`
  (`835a531`; constructs NO lease/SAS — anti-trap). UNMODIFIED.
- `output/parquet_writer.py`; `classifier/page_acquisition/page_storage.py`;
  `classifier/llm/prompt_logger.py` — all EMPIRICALLY VALIDATED against Azurite;
  modules UNMODIFIED.
- **A-classify reads but does NOT modify**: the Stage 1->2->3 cascade entry
  (`cascade.py:314` async `_run_stage1` / `stage1/run.py:150` `run_shard`;
  consumes `parser_parquet` + components, WRITES `predictions.parquet` per
  `output_schema.SCHEMA`); the prediction field is `signals_business_score`;
  rows carry `model_version`. The LLM client is `AsyncAzureOpenAI`
  (`azure_openai_adjudicator.py:55`, `embedder.py:42`) — openai/httpx, NOT
  requests (vcrpy does NOT replay it; mock the client for $0 dev).
- `tests/classifier/page_acquisition/test_page_storage.py` (hermetic guard);
  `tests/test_parquet_writer.py` (33 hermetic tests);
  `tests/classifier/pipeline/test_cost_journal_adls.py` (19 in-memory).
- `docs/CRAWLING_POLICY.md` (S26 `2314f5e`; 77 lines / 2.52 KB);
  `docs/phase4_implementation_plan.md`.
- `orchestrator/robots_integration.py` (`279bb77`) + 35 tests;
  `test_robots_gate_integration.py` (7 tests; `aed7873`);
  `orchestrator/vmss_worker.py` (`5eeaac7`), `job_runner.py` (`872527e`);
  the 3 worker_loop helpers; `test_worker_loop_persistence.py` (12 tests).
- S28 LOCKS: `classifier/stage1/run.py` (`776d203`), `test_run_cascade.py`.
- Production code under `src/barcada_scraper/` — locked unless a Phase 2 gate
  authorizes a specific module. S26+S27+S29-S39 added NO new src/
  authorizations.
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences; honored
  every commit.

---

## Combined-suite-at-Session-40-open baseline

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

Sub-totals identical to S27-S39 close: 210 conformance + 52 driver + 99
baseline_v0 + 33 synthetic_crawl + 32 robots + 30 robots_gate + 30
robots_bypass_config + 43 cost_journal + 13 cost_journal_local + 19
cost_journal_adls + 35 robots_integration + 74 vmss_worker + 129 job_runner +
152 worker_loop + 7 robots_gate_integration + 12 worker_loop_persistence =
970. (ALL SIX Azurite tests are live-marked + skip-by-default; the drift tests
live in tests/drift/, outside this sweep.)

Step 0.8 sub-suites (default-run; NOT in the canonical 16-path):

```
.venv/bin/python -m pytest tests/classifier/llm/test_prompt_logger.py -q   # expect 13 (S38 guard)
.venv/bin/python -m pytest tests/drift/ -q                                 # expect 43 (S39 fetch 22 + S40 classify 21)
```

Combined (16-path + both Step 0.8 sub-suites):

```
# Append to the 16-path above:
    tests/classifier/llm/test_prompt_logger.py
    tests/drift/
# Expected: 1026 passed (970 + 13 + 43). VERIFIED at 3266bc4. This is the
# count the S41 cumulative gate must not let decrease (was 1005 at S39).
```

OUT-OF-BAND live tests (NOT in the canonical count; need Docker + the Azurite
image, else SKIP):

```
.venv/bin/python -m pytest -m live tests/classifier/pipeline/
# Expected: 6 passed, 209 deselected. Ports: S33=10000 … S38=10005.
```

Cumulative-test-count gate: the count NEVER decreases between commit
boundaries. Narrower baselines (still valid): 480 / 538 / 944.

**Fixture-count assertions for S40 Phase 0 Step 0.4**: html_count=222,
expected_count=202, meta_count=222, baseline_count=1213,
**`cassette_count == 30`, `exclusions_count == 30`** (UNCHANGED).

---

## Pre-push gate at Session 40 open

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # all files OK (do not pin a fixed N)
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

Note on gate 4: validate_consistency runs against working-tree state; if
operator-WIP in eval_data introduces a schema violation between S39 close and
S40 open, the gate blocks even though no S40 commit touches eval_data. Per
LESSONS: surface to operator with the row+detail, propose operator-fix or
stash-and-restore; do NOT auto-fix. S39 ran the gate clean at Phase 4
(0 errors / 0 warnings).

---

## Context-window awareness

Session 39 ran Phase 0 → Phase 5 + a deferred Phase 6 across one context
window (Phase 0 verify + a pre-session source-verify + the A-fetch design +
impl with a baseline-bookkeeping HALT/resolution + 2 A-classify prompt
reviews + this close-out), comfortably within budget. Session 40 budget per
chosen candidate:

- A-classify: MEDIUM-LARGE (two sub-surfaces; the producer is fetch → parser →
  components → async cascade → output read-back, NOT a flag). Phase-0.COST
  gated; client-mock $0 dev. Watch context — the producer + its hermetic
  mock harness is substantial.
- Candidate D: operator-led; tooling only.
- Candidate E: EXHAUSTED; not available without a plan-bound revision.

Strategies (unchanged from S20-S39 prompts):
- Use Edit over Write for small additions; delegate multi-file design-of-record
  analysis to Explore.
- For A-classify's hermetic tests, MOCK the cascade entry / `AsyncAzureOpenAI`
  client (the `test_canary.py`-mocks-`requests.get` pattern) — vcrpy covers the
  FETCH leg only.
- **"Outside the 16-path" is a DIRECTORY fact, not a filename fact** — place a
  keep-the-headline-stable sub-suite in a dir the canonical 16-path does NOT
  sweep (e.g. `tests/drift/`), and re-run the canonical 16-path ALONE
  post-placement to confirm 970 (S39 LESSONS).
- For any live-service-backed test, default to the S33-S38 fixture shape
  (try/finally teardown + self-healing pre-clean + skip-if-unavailable;
  DISTINCT port + container; live marker off the headline).
- Survey ADLS coverage by CLIENT STACK + read the AUTH seam from the call-site
  signature (S35/S36/S38). Build `key=value` URLs by string-concat not
  `Path.as_uri()` (S38). Pre-create the container via `fs.mkdir` for
  write_to_dataset (S37). Verify a carve-out against the TEST BODY (S34).
  Grep production FIRST to confirm a lease/SAS-style candidate is real (S38).
- Source-verify facts behind option-set design BEFORE AskUserQuestion (S25).
- Phase 0 fixture-count commands use Python `rglob()`, NOT bare `find` (S28).
- Markdown-rendered shell commands may carry NBSP; secrets-referencing /
  ast.parse inline `python -c` trips the env hook — file-stage scripts via the
  Write tool and run `.venv/bin/python <path>`.
- The `rm -f` / `rm -rf` / `find -delete` / `os.remove` forms are
  env-hook-blocked — move throwaway helpers OUT of the repo tree via `mv` to
  `/tmp/` (or write helpers directly to `/tmp/`); operator runs `! rm ...`;
  in-fixture `docker rm -f` runs fine.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before the chosen S40 scope closes, finish the
  in-flight sub-surface, then transition (no mid-commit-batch transitions).

---

## Reporting in chat at session close

Same pattern as Sessions 13-39:

1. Commit SHA(s) of each Session 40 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 970 / 1026 baseline → S41 close.
4. Driver suite count (52/52 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (W0 closed S27; W A.1 closed S22; the S33-S38 ADLS
   cluster closed + tagged `adls-live-coverage-v0` at S38; S39 drift tag
   deferred — decide at S40 1.TAG if A-classify closes the workstream).
7. Carry-forward dispositions.
8. **Any spend (LLM, infrastructure)** — A-classify is the first non-$0
   candidate; record dev $0 vs any authorized live figure + running total
   vs the $100 ceiling.
9. Any new LESSONS patterns to fold in.

---
