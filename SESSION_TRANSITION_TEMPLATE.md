# Session Transition Template — Handoff from Session 34 → Session 35

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-34 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 35 invocation prompt:** DRAFTED at S34 close
(operator-commissioned) at `~/crawler-audit/SESSION_35_PROMPT.md`.
Mirrors the S20-S34 7-phase structure and pins: repo HEAD anchor
`eba6585`, workspace HEAD anchor (the S34 close-out `a6eef0f` +
`27bd60b` anchor-pin + the prompt-drafting follow-up), tag count `13`,
canonical baseline `970`, Phase 0 Step 0.4
`cassette_count == 30` / `exclusions_count == 30`, and a Step 0.9
presence + POSTURE check (`check_s35_deliverables.py`) for the S31/S32
cassettes, the S33 Azurite primitive test, AND the NEW S34
deliverables (`live-integration.yml` — asserting it stays OFF push/PR —
+ the concurrency race test on port 10001). Both new Phase 0 checks
were validated green at S34 close against `eba6585`. Re-read the prompt
on S35 open; walk any reviewer flags per its "Reviewer-feedback
hygiene" section before mutating it.

**IMPORTANT — S35 again opens with a near-empty warm-candidate
queue.** S34 shipped the K-a CI wiring + the multi-writer concurrency
race test the carve-out actually called for. The remaining
carry-forwards are A (blocked), D (operator-led labeling), and E
(EXHAUSTED — needs a plan-bound revision to reopen). NONE is on a
critical path and NONE is self-contained. S35 may have no actionable
engineering scope unless the operator unblocks A, begins D labeling,
authorizes a plan amendment to reopen E, or commissions a fresh
candidate (e.g., extending the live ADLS coverage to lease/SAS paths).
Surface this at S35 Phase 1 exactly as S33/S34 did (the empty-queue
condition + the budget trade-off of a no-ship resolution).

Anchors for Session 35 cold start:
- Repo HEAD: `eba6585` (S34: WA2.W8.adls-live-concurrency+ci —
  +1 concurrency race test + 1 live-integration CI workflow).
  Tolerated delta: operator-side eval_data labeling commits between
  S34 close and S35 open (Sessions 8-34 precedent) — verify each is
  strictly `eval_data/*` via `git show --stat`.
- Workspace HEAD: the S34 primary close-out commit `a6eef0f`
  (SESSION_LOG.md + SESSION_TRANSITION_TEMPLATE.md + LESSONS.md) +
  THIS anchor-pin follow-up succeeding it (+ any later
  prompt-revision commits). S35 Phase 0 Step 0.1 MUST anchor
  workspace expectation to `a6eef0f` OR this anchor-pin follow-up OR
  a later follow-up. Per the S21-S34 LESSONS pattern "Workspace HEAD
  delta tolerance": tolerate N additional prompt-drafting /
  audit-correction commits between sessions.
- Canonical baseline: **970 tests** (16-path invocation; UNCHANGED
  from S27-S34 close). BOTH Azurite tests are `@pytest.mark.live` +
  skip-by-default and are NOT in the canonical invocation.
- Narrower baseline: **944 tests** (14-path; 970 minus 19
  cost_journal_adls minus 7 robots_gate_integration). Unchanged.
- Fixture counts (S35 Phase 0 Step 0.4): html=222 / expected=202 /
  meta=222 / baseline=1213 / **`cassette_count == 30`** /
  **`exclusions_count == 30`** — UNCHANGED from S33/S34 (the S34
  deliverable is test code + a CI workflow; no fixture change).
- Primary recommended scope: none — no carry-forward is on a
  critical path; none is self-contained.
- Carry-forward candidates: A (barcada-drift; blocked on parquets +
  AI/ML), D (Phase 4 PR-D tooling; operator-led labeling not yet
  begun), E (EXHAUSTED at 30 — no further +N without a plan-bound
  revision). **K-a is CLOSED; its CI wiring CLOSED at S34.**

**S34 Candidate SHIPPED (NEW candidate: K-a CI wiring + concurrency
race test)** — `eba6585`, single commit, 2 files, 425 insertions:
- `tests/classifier/pipeline/test_cost_journal_adls_azurite_concurrency.py`
  (337 LOC; 1 `@pytest.mark.live` test). 12 concurrent threads append
  distinct shards to one shared `run_<id>.json` blob via
  `update_with_retry`, asserting NO lost updates. This is the
  multi-writer concurrency the S33 "concurrency coverage" carve-out
  named but the S33 sequential test never exercised (see the S34
  LESSONS fold). Teeth proven via a negative control
  (`retry_delays_ms=()` → 1 shard persisted, 11
  `JournalConcurrencyError`).
- `.github/workflows/live-integration.yml` (88 LOC). Wires BOTH live
  tests into CI: `workflow_dispatch` + nightly `schedule`
  (cron `0 6 * * *`); NOT push/PR (live-on-demand, NOT default-CI).
  Job pre-pulls the Azurite image and runs `pytest -m live` over
  `tests/classifier/pipeline/` with a skip-robust count-agnostic
  guard (fails the job if any live test skipped or none passed).

---

## Handoff metadata

- Outgoing session number: 34
- Closing date: 2026-06-02
- Outgoing session scope: NEW candidate — wire the S33 K-a Azurite
  live test into CI. Phase 3 HALT on the carve-out (S33 named
  "concurrency coverage" against a sequential test; production is
  multiple-writer) → operator chose Path B → built the multi-writer
  race test, then CI-wired both. 1 repo commit (`eba6585`). LLM
  spend: $0. Infrastructure: $0 (local Docker + the already-pulled
  Azurite image; no paid Azure service touched).
- Reason for transition: S34 scope completed cleanly through
  Phase 0 → Phase 6; one HALT, resolved by operator to Path B; no
  in-flight sub-surface.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `eba6585` (WA2.W8.adls-live-concurrency+ci: race
  test + live-integration CI workflow).
- Branch sync with `origin/main`: pushed at S34 close (confirm
  0 ahead / 0 behind after the push).
- Tags (13 total; UNCHANGED; 1.TAG = defer):
  - `pre-remediation-2026-05-19` / `baseline-v0` (`9e9a1fb`)
  - `workstream-0-week1-end` … `week7-end`
  - `workstream-0-end` at `a1c5636` (annotated; placed S27)
  - `workstream-a-week1-end` at `fdc8a7a` (placed S22)
  - `workstream-stage1-prestaged-flags-end` (`af6f1d4`),
    `workstream-stage1-step3-end` (`d4f06b8`) — operator eval_data tags
  - NOTE: `workstream-a-week2-end` was OFFERED at S33 AND remained
    DEFERRED at S34 despite the CI wiring landing. If a future session
    declares W A.2 closed, that annotated tag remains appropriate.
- Pre-push gate at HEAD `eba6585`: VERIFIED GREEN at S34 close
  (ruff check "All checks passed!" + ruff format clean [count not
  pinned] + vermin 3.10 + validate_consistency 0 errors / 0 warnings).
- Unstaged operator territory (Sessions 8-34 precedent):
  `eval_data/stage1_labels.jsonl` (modified) + `eval_data/audits/`
  (untracked) + `.claude/scheduled_tasks.lock` (untracked) — present
  at S34 open/close and left unstaged. Verify via `git status` at
  S35 open.
- Corpus: 222 .html / 202 expected.json / 222 meta.json (unchanged).
- 30 synthetic_crawl cassettes (20 S20 + 5 S31 + 5 S32) + 30
  sidecars (UNCHANGED).
- ADDED Session 34 (1 commit `eba6585`):
    - `tests/classifier/pipeline/test_cost_journal_adls_azurite_concurrency.py`
      (NEW; 337 LOC; 1 `@pytest.mark.live` multi-writer race test +
      module-scoped Azurite fixture on port 10001 / container
      `barcada-azurite-racetest`).
    - `.github/workflows/live-integration.yml` (NEW; 88 LOC; CI
      workflow). No `src/` changes. No cassette/driver changes. The
      S33 test file + its `live` marker are UNTOUCHED.
- Combined test suite at HEAD `eba6585`:
    - **970 passed / 0 failed / 0 skipped** — canonical 16-path
      (UNCHANGED; both Azurite tests are live-marked + absent).
    - **944** — narrower 14-path (unchanged).
    - OUT-OF-BAND live tests: `pytest -m live tests/classifier/pipeline/`
      → **2 passed, 209 deselected** (needs Docker + the Azurite
      image, else SKIPS). CI runs exactly this + a skip-fail guard.
    - Stage 1 test counts: 32 (16 + 16) — unchanged; outside the
      canonical 16-path.

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 34 start: `3f27b70` ("S34 prompt:
  restore Step 0.9 S33-parity invariants + de-pin Phase 4 file
  count"; succeeds `8f37886` S34 prompt draft, atop `dc21714`). At
  S34 Phase 0 Step 0.1 the 2 commits ahead of `dc21714` were
  tolerated under "Workspace HEAD delta tolerance" (prompt-only edits).
- Session 34 close-out workspace commits: 1 primary close-out
  (SESSION_LOG.md + SESSION_TRANSITION_TEMPLATE.md + LESSONS.md)
  + 1-2 anchor-pin follow-ups (pinning the actual close-out SHA into
  this template's Anchors section for S35).
- **Last commit SHA at Session 34 CLOSE: this anchor-pin follow-up
  succeeding the primary close-out `a6eef0f`.** S35 Phase 0 Step 0.1
  MUST anchor workspace expectation to `a6eef0f` OR this anchor-pin
  follow-up OR a later follow-up.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected after
  the Session 34 close push.

---

## Session 35 execution order (enforce strict sequence)

Same N-phase shape regardless of scope choice (Phase 0 cold-start
verify → Phase 1 scope → Phase 2 design-gate → Phase 3 impl →
Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 35 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 34 entry (the carve-out HALT →
   Path B narrative; the multi-writer finding; the negative-control
   teeth check; the CI workflow shape).
3. Reading LESSONS.md additions Session 34 landed (1 new section,
   "S34 folding" suffix: a carve-out claim must be verified against
   the test BODY, not its name/marker).
4. Reading the relevant section of BARCADA_CRAWLER_REMEDIATION_PLAN.md
   for the chosen Session 35 scope.
5. Reading the Session 35 prompt if one has been drafted, OR
   commissioning a fresh draft at S35 open.
6. Running Phase 0 cold-start verification (mirror the S34 prompt's
   9-step shape, updating workspace HEAD anchor, repo HEAD anchor
   `eba6585`, tag count `13`, canonical baseline `970`, cassette
   fixture-count `30` / exclusions `30`, AND a Step 0.9 presence
   check for BOTH the S33 Azurite test AND the S34 deliverables).

---

## Outstanding operator-input requests entering Session 35

1. **Session 35 scope choice** — pick from the carry-forwards below.
   K-a + its CI wiring are CLOSED. Candidate E is EXHAUSTED (30
   upper bound). None of A/D is on a critical path. S35 may be a
   no-ship scope-resolution session — surface that at Phase 1.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*` continue across sessions (Sessions 8-34 precedent).

3. **barcada-drift AI/ML alignment** — 4 AI/ML team decisions need
   pre-resolution OR placeholders, plus 2+ canary_runs parquet files.
   Re-verified empirically at S34 Phase 1: 0 canary_runs parquets,
   0 plist, no AI/ML responses.

4. **launchd kit installation** — Operator should run
   `scripts/launchd/install_canary_schedule.sh` when ready. Required
   prerequisite for Candidate A. As of S34 close, NOT yet installed.

5. **Session 35 prompt draft commissioning** — operator decides
   whether to commission an S35 prompt between sessions.

6. **Live ADLS coverage extension (potential NEW candidate)** — the
   K-a primitive test (S33) + the multi-writer race test (S34) cover
   the ETag mapping + concurrent contention. Lease / SAS-token /
   container-level paths are NOT yet live-tested. If future churn in
   `cost_journal_adls.py` warrants it, that is a fresh candidate
   scoped from first principles (default to operator-smoke posture
   unless a named carve-out justifies permanent/CI coverage).

---

## Notes for Session 35

Suggested S35 scope candidates (operator picks at S35 open):

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

### K-a + CI wiring (CLOSED at S33/S34)

SHIPPED. The Azurite live primitive test (S33) + the multi-writer
concurrency race test + on-demand/nightly CI (S34) all exist. Not a
carry-forward. New live ADLS coverage (lease/SAS) would be a fresh
candidate.

---

## Required reading (Session 35 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 34 entry — carve-out HALT → Path B;
   multi-writer finding; negative-control teeth; CI workflow shape.
3. **`LESSONS.md`** — the new "S34 folding" section (carve-out ↔
   test-body verification) PLUS the "S33 folding" (live-emulator
   teardown + version skew) if a live-service scope is chosen.
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope section.
   READ-ONLY (exception: a plan-amendment session to reopen E).
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A is chosen.
6. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   + the two live test files + `.github/workflows/live-integration.yml`
   + `scripts/smoke_test_adls_cost_journal.py` — only if a new
   ADLS-surface / CI scope is chosen.

---

## Outstanding items carried forward to Session 35+

1. **Per-tier cost-accounting wiring** — CLOSED end-to-end S28.
2. **`barcada-drift` CLI** — §Item 8; 4 AI/ML decisions + 2+
   parquets outstanding. Re-verified empirically at S34 Phase 1.
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
12. **Azurite-backed CI test (K-a)** — CLOSED S33; **CI wiring +
    multi-writer concurrency coverage CLOSED S34** (`eba6585`). The
    live tests now run on-demand + nightly via `live-integration.yml`
    with a guard that fails on a silent skip. Default push/PR CI
    still does NOT run them (by design — live-on-demand). Potential
    future extension: lease/SAS live paths (fresh candidate).
13. **Recorder reject-before-write / min-content-bytes floor +
    is_waf_challenge "Client Challenge" signature** — parser/recorder
    hygiene (S31+S32 folds). NOT a fix unless a future session scopes
    `tools/synthetic_crawl/` or `scraper/parser.py`.

---

## Locked artifact reminders for Session 35

Carry-forward from Sessions 8-34. **NEW S34 LOCKS**:
- `tests/classifier/pipeline/test_cost_journal_adls_azurite_concurrency.py`
  at `eba6585` (337 LOC; 1 `@pytest.mark.live` multi-writer race
  test + its own module-scoped Azurite fixture). Do NOT modify
  without Phase 2 authorization.
- `.github/workflows/live-integration.yml` at `eba6585` (CI workflow;
  `workflow_dispatch` + nightly schedule; NOT push/PR). Its
  `-m live` selection over `tests/classifier/pipeline/` + the
  skip-fail guard are load-bearing; do NOT weaken to a default-CI
  trigger without a deliberate posture decision (S33 framing).

Prior locks (unchanged):
- **S33 LOCK**: `tests/classifier/pipeline/test_cost_journal_adls_azurite.py`
  at `f1cdce8` (292 LOC) + the `live` marker in `pyproject.toml`
  `[tool.pytest.ini_options]`.
- `eval_data/` — labeling-workstream territory; operator-WIP expected.
- `stage1.schema.json` v1.0 (49 keywords).
- `pre-remediation-2026-05-19` / `baseline-v0` (`9e9a1fb`) tags.
- All `workstream-0-*-end` tags; `workstream-0-end` (`a1c5636`);
  `workstream-a-week1-end` (`fdc8a7a`); the 2 operator eval_data tags.
- `tests/runners/fixture_cascade/` — W4.1.5 driver; locked at
  `dd64963` except via W5.X commits (S27 `a1c5636`, S28 `9afde57` +
  `ae9e627`). S29-S34 did NOT touch this surface.
- `tests/fixtures/baseline-v0/` snapshot — locked at `9e9a1fb`.
- `tools/baseline_v0/` + `tools/synthetic_crawl/` — S18-S20; locked.
- `tests/fixtures/synthetic_crawls/` — 20 S20 (`7f11879`) + 5 S31
  (`06d67c4`) + 5 S32 (`cfa0ec1`); never re-record/delete.
- `scripts/launchd/` — S20; locked.
- `src/barcada_scraper/scraper/robots.py` (`34a59b6`),
  `robots_gate.py` (`ba87e7e`), `robots_bypass_config.py`
  (`381ee89`) + their test files — S21/S22; locked.
- `cost_journal.py` (S22-extended `1d9404e`; public API consumed by
  S27-S34 without modification — incl. `update_with_retry`,
  `with_shard_appended`, `ShardRecord` used by the S34 race test via
  the public surface only).
- `cost_journal_local.py` — locked.
- `cost_journal_adls.py` — full backend at S25 `835a531`. Public API
  `ADLSCostJournal(journal_dir, run_id, credential=None,
  blob_backend=None)`. EMPIRICALLY VALIDATED at S30 (K-b smoke), S33
  (Azurite primitive), S34 (Azurite concurrency). The S34 race test
  injects the production `_AzureBlobBackend` via the public
  `blob_backend=` seam; it did NOT modify the module.
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
  Phase 2 gate authorizes a specific module. S26+S27+S29-**S34**
  added NO new src/ authorizations (S34 was test + CI only).
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-35-open baseline

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

Sub-totals identical to S27-S34 close: 210 conformance + 52 driver
+ 99 baseline_v0 + 33 synthetic_crawl + 32 robots + 30 robots_gate
+ 30 robots_bypass_config + 43 cost_journal + 13 cost_journal_local
+ 19 cost_journal_adls + 35 robots_integration + 74 vmss_worker +
129 job_runner + 152 worker_loop + 7 robots_gate_integration + 12
worker_loop_persistence = 970. (BOTH Azurite tests are live-marked +
skip-by-default and are NOT in this invocation.)

OUT-OF-BAND live tests (NOT in the canonical count; need Docker +
the Azurite image, else SKIP):

```
.venv/bin/python -m pytest -m live tests/classifier/pipeline/
# Expected: 2 passed, 209 deselected
# (CI live-integration.yml runs exactly this + a skip-fail guard.)
```

Cumulative-test-count gate: the count NEVER decreases between commit
boundaries.

Narrower baselines (still valid for S35 candidates that don't
exercise the ADLS test paths): 480 / 538 / 944.

**Fixture-count assertions for S35 Phase 0 Step 0.4**: html_count=222,
expected_count=202, meta_count=222, baseline_count=1213,
**`cassette_count == 30`, `exclusions_count == 30`** (UNCHANGED).

---

## Pre-push gate at Session 35 open

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
S34 close and S35 open, the gate blocks even though no S35 commit
touches eval_data. Per LESSONS: surface to operator with the
row+detail, propose operator-fix or stash-and-restore; do NOT
auto-fix. S34 ran the gate clean at Phase 4 (0 errors / 0 warnings).

---

## Context-window awareness

Session 34 ran Phase 0 → Phase 6 in a single context window with 1
repo commit (Phase 0 verify + Phase 1 scope + Phase 2 gates + a
Phase 3 HALT resolved to Path B [race test + negative control + CI
workflow] + Phase 6 close-out), within budget. Session 35 budget per
chosen candidate:

- Candidate A (barcada-drift): only if launchd job has run ≥2 times
  AND AI/ML decisions ready. ~370-400 LOC delivered.
- Candidate D: operator-led; tooling only.
- Candidate E: EXHAUSTED; not available without a plan-bound revision.
- A NEW live-ADLS candidate (lease/SAS): size at Phase 2; default to
  operator-smoke posture unless a named carve-out justifies CI.

Strategies (unchanged from S20-S34 prompts):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-service-backed test, default to the S33/S34 fixture
  shape: unconditional try/finally teardown + idempotent
  self-healing pre-clean + skip-if-unavailable; expect an
  SDK-vs-emulator version-skew flag may be needed; use a DISTINCT
  port + container name if it must coexist with the existing live
  fixtures; keep the test off the canonical headline (live marker,
  skip-by-default) unless a deliberate decision adds it.
- **Verify a carve-out against the TEST BODY, not its name/marker
  (S34 LESSONS) — and re-verify when CI-wiring an existing test.**
- Source-verify facts behind option-set design BEFORE AskUserQuestion
  drafts (S25 LESSONS).
- Phase 0 fixture-count commands use the Python `rglob()` pattern,
  NOT bare `find` (S28 post-close LESSONS).
- Markdown-rendered shell commands may carry NBSP in whitespace-
  sensitive args; stage scripts to a file via the Write tool when
  exactness matters (re-confirmed at S34 — inline grep with quoted
  spaces silently failed; the byte-scan + file-staged guard worked).

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S35 scope closes, transition
  per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-34:

1. Commit SHA(s) of each Session 35 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 970 baseline → S35 close.
4. Driver suite count (52/52 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (W0 closed S27; W A.1 closed S22; W A.2
   final-milestone tag `workstream-a-week2-end` OFFERED+DEFERRED at
   S33 AND S34).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 34 handoff template. Refill at Session 35 close.
