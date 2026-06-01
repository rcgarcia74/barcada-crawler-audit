# Session Transition Template — Handoff from Session 33 → Session 34

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-33 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 34 invocation prompt:** NOT yet drafted at S33 close.
Per S20→S33 precedent, prompt-drafting is operator-commissioned
between sessions; operator decides whether to commission an S34
prompt or scope one at S34 open. A drafted prompt should mirror the
S20-S33 7-phase structure and pin: repo HEAD anchor `f1cdce8`, tag
count `13`, canonical baseline `970`, Phase 0 Step 0.4
`cassette_count == 30` / `exclusions_count == 30`, and a Step 0.9
check that the 5 S31 + 5 S32 cassette dirs exist AND the S33 Azurite
test file is present.

**IMPORTANT — S34 also opens with a near-empty warm-candidate
queue.** With K-a now CLOSED (S33), the remaining carry-forwards are
A (blocked), D (operator-led labeling), and E (EXHAUSTED — needs a
plan-bound revision to reopen). NONE is on a critical path and NONE
is self-contained the way K-a was. S34 may have no actionable
engineering scope unless the operator unblocks A, begins D labeling,
or authorizes a plan amendment to reopen E. Surface this at S34
Phase 1 exactly as S33 did (the "empty warm-candidate queue"
condition + the budget trade-off of a no-ship resolution).

Anchors for Session 34 cold start:
- Workspace HEAD: `83e188a` (S33 primary close-out: SESSION_LOG.md
  + SESSION_TRANSITION_TEMPLATE.md + LESSONS.md) + THIS anchor-pin
  follow-up succeeding it (+ any later prompt-revision commits). S34
  Phase 0 Step 0.1 MUST anchor workspace expectation to `83e188a`
  OR this anchor-pin follow-up OR a later prompt-revision follow-up.
  Per the S21-S33 LESSONS pattern "Workspace HEAD delta tolerance":
  tolerate N additional prompt-drafting / audit-correction commits
  between sessions; verify each is consistent with that pattern
  before continuing.
- Repo HEAD: `f1cdce8` (S33 Candidate K-a:
  WA2.W8.adls-azurite-ci-test; +1 Azurite-backed live test + a
  3-line `live`-marker registration in pyproject.toml). Tolerated
  delta: operator-side eval_data labeling commits between S33 close
  and S34 open (Sessions 8-33 precedent) — verify each is strictly
  `eval_data/*` via `git show --stat`.
- Canonical baseline: **970 tests** (16-path invocation; UNCHANGED
  from S27-S33 close). The S33 Azurite test is `@pytest.mark.live`
  + skip-by-default and is NOT in the canonical invocation — it does
  not affect the 970 headline.
- Narrower baseline (for candidates that don't exercise ADLS test
  paths): **944 tests** (14-path; 970 minus 19 cost_journal_adls
  minus 7 robots_gate_integration). Unchanged.
- Fixture counts (S34 Phase 0 Step 0.4): html=222 / expected=202 /
  meta=222 / baseline=1213 / **`cassette_count == 30`** /
  **`exclusions_count == 30`** — UNCHANGED from S33 (K-a was
  test-code, not a cassette; no fixture change at S33).
- Primary recommended scope: none — no carry-forward is on a
  critical path; none is self-contained now that K-a is closed.
- Carry-forward candidates: A (barcada-drift; blocked on parquets +
  AI/ML), D (Phase 4 PR-D tooling; operator-led labeling not yet
  begun), E (EXHAUSTED at 30 — no further +N without a plan-bound
  revision). **K-a is CLOSED (S33).**

**S33 Candidate K-a SHIPPED** — added
`tests/classifier/pipeline/test_cost_journal_adls_azurite.py`
(292 LOC; 1 `@pytest.mark.live` test) exercising ADLSCostJournal's
full 5-step ETag-conflict matrix against the REAL `_AzureBlobBackend`
(real azure-storage-blob 12.28.0 SDK) over a live Azurite blob
emulator in Docker. Closes the carry-forward K-a as **live-on-demand**
(`-m live`, Docker-gated) defense-in-depth coverage for the
concurrency carve-out — NOT default-CI coverage (the test is
skip-by-default and absent from the canonical 16-path). Single
commit `f1cdce8` (test file + a 3-line `live`-marker registration in
pyproject.toml). No `src/` changes.

---

## Handoff metadata

- Outgoing session number: 33
- Closing date: 2026-06-01
- Outgoing session scope: ADLSCostJournal Azurite-backed CI test
  (S33 Candidate K-a). 1 code commit (`f1cdce8`); 1 new test file +
  a 3-line pyproject marker registration. LLM spend: $0.
  Infrastructure: $0 (local Docker + local Azurite emulator; no paid
  Azure service touched). Docker Desktop was started locally
  (`open -a Docker`) and the Azurite image (267 MB) pulled — both
  remain on the operator's machine for re-runs.
- Reason for transition: S33 single-candidate scope completed
  cleanly; Candidate K-a shipped end-to-end Phase 0 → Phase 6 in a
  single context window with no HALTs (one mid-implementation
  test-failure on an Azure/Azurite version skew, fixed via
  `--skipApiVersionCheck`; the failure validated the fixture's
  unconditional teardown — no orphaned container). No in-flight
  sub-surface.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `f1cdce8` (WA2.W8.adls-azurite-ci-test:
  tests/classifier/pipeline/test_cost_journal_adls_azurite.py
  (S33 Candidate K-a)).
- Branch sync with `origin/main`: 0 ahead / 0 behind (pushed at
  S33 close).
- Tags (13 total; UNCHANGED from S30/S31/S32 close):
  - `pre-remediation-2026-05-19` at `3cbb9b3`
  - `workstream-0-week1-end` at `4f9d23f`
  - `workstream-0-week2-end` at `e5d2f91`
  - `workstream-0-week3-end` at `cf0c14c`
  - `workstream-0-week4-1-5-end` at `dd64963` (annotated)
  - `workstream-0-week4-end` at `b2e2671` (annotated)
  - `workstream-0-week5-end` at `ddd3cb0` (annotated)
  - `baseline-v0` at `9e9a1fb` (annotated)
  - `workstream-0-week7-end` at `ea37102` (annotated)
  - `workstream-0-end` at `a1c5636` (annotated; placed S27)
  - `workstream-a-week1-end` at `fdc8a7a` (annotated; placed S22)
  - `workstream-stage1-prestaged-flags-end` at `af6f1d4`
    (operator-side eval_data tag)
  - `workstream-stage1-step3-end` at `d4f06b8` (operator-side
    eval_data tag)
  - NOTE: `workstream-a-week2-end` was OFFERED at S33 (K-a as the
    final W A.2 code milestone) but the operator DEFERRED it. If a
    future session declares W A.2 closed, that annotated tag remains
    appropriate.
- Pre-push gate state at HEAD `f1cdce8`: VERIFIED GREEN at S33
  close (ruff check "All checks passed!" + ruff format 354 files +
  vermin 3.10 + validate_consistency 0 errors / 0 warnings; 532
  stage1 rows OK). The pre-push hook also re-ran all gates green on
  push.
- Pre-S33 unstaged operator territory (Sessions 8-33 precedent):
  `eval_data/*` operator-WIP (`eval_data/stage1_labels.jsonl`
  modified at S33 open/close) + `eval_data/audits/` (untracked)
  + `.claude/scheduled_tasks.lock` (untracked) — all present at
  S33 open and left unstaged; verify via `git status` at S34 open.
  Repo HEAD was exactly `cfa0ec1` at S33 open (no tolerated
  operator-side eval_data COMMIT in `cfa0ec1..HEAD`).
- Corpus: 222 .html fixtures (unchanged from S17 close).
- 202 expected.json files (unchanged).
- 222 meta.json files (unchanged).
- 30 synthetic_crawl cassettes (20 S20 + 5 S31 + 5 S32) + 30
  extract_hard_exclusions sidecars (UNCHANGED — K-a added no
  cassettes).
- MODIFIED Session 33 (1 commit `f1cdce8`):
    - `tests/classifier/pipeline/test_cost_journal_adls_azurite.py`
      (NEW; 292 LOC; 1 `@pytest.mark.live` test + module-scoped
      Azurite fixture + docker/readiness helpers).
    - `pyproject.toml` (M; registered the `live` marker under
      `[tool.pytest.ini_options]`, 3 lines).
    - No `src/` changes. No cassette changes. No driver changes.
- (Unchanged from S32 close, all locked):
    - All S21-S29 deliverables.
    - The original 20 S20 cassettes at `7f11879` (UNTOUCHED).
    - The 5 S31 cassettes at `06d67c4` + 5 S32 cassettes at
      `cfa0ec1` (UNTOUCHED).
    - `cost_journal_adls.py` (S25 full backend at `835a531`;
      EMPIRICALLY validated at S30 via the K-b smoke AND at S33 via
      the Azurite live test).
    - `docs/CRAWLING_POLICY.md` (S26 doc at `2314f5e`; 77 lines /
      2519 bytes).
    - S27+S28 deliverables; S29 K-b script at `75a3937`.
- Combined test suite at HEAD `f1cdce8`:
    - **970 passed / 0 failed / 0 skipped** with the canonical
      16-path invocation (UNCHANGED — the Azurite test is
      live-marked + absent from the invocation).
    - **944 passed / 0 failed / 0 skipped** with the narrower
      14-path invocation (unchanged).
    - **1 passed** for the OUT-OF-BAND live test
      (`-m live tests/classifier/pipeline/test_cost_journal_adls_azurite.py`;
      needs Docker + the Azurite image, else SKIPS).
    - **Stage 1 test counts**: 32 (16 test_run_cascade + 16
      test_cost_tracker) — unchanged. Outside the canonical 16-path.

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 33 start: `67431db` ("S33 prompt v2.1:
  M-3 Scope-section K-a framing softened"; succeeds 1881e70 /
  b713503 / ca17535 — all S33 prompt drafting + reviewer-findings +
  S32 post-close feedback, atop `8f13c03`). At S33 Phase 0 Step 0.1
  the 4 commits ahead of `8f13c03` were tolerated under the
  "Workspace HEAD delta tolerance" pattern (prompt-only edits).
- Session 33 close-out workspace commits: 1 primary close-out
  (SESSION_LOG.md + SESSION_TRANSITION_TEMPLATE.md + LESSONS.md)
  + 1-2 anchor-pin follow-ups (pinning the actual close-out SHA
  into this template's Anchors section for S34).
- **Last commit SHA at Session 33 CLOSE: this anchor-pin follow-up
  succeeding the primary close-out `83e188a`.** S34 Phase 0 Step
  0.1 MUST anchor workspace expectation to `83e188a` OR this
  anchor-pin follow-up OR a later follow-up. Per S21-S33 LESSONS
  pattern: tolerate N additional prompt-drafting / audit-correction
  commits between sessions.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected
  after Session 33 close push.

---

## Session 34 execution order (enforce strict sequence)

Same N-phase shape applies regardless of scope choice (Phase 0
cold-start verify → Phase 1 scope → Phase 2 design-gate → Phase 3
impl → Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 34 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 33 entry (K-a Azurite-test
   narrative; the empty-warm-candidate-queue Phase 1; the version-
   skew finding + `--skipApiVersionCheck` fix; the unconditional-
   teardown validation).
3. Reading LESSONS.md additions Session 33 landed (1 new section,
   "S33 folding" suffix: live-emulator fixture teardown + SDK-vs-
   emulator version skew + the carve-out/baseline-re-pin meta-pattern).
4. Reading the relevant section of BARCADA_CRAWLER_
   REMEDIATION_PLAN.md for the chosen Session 34 scope.
5. Reading the Session 34 prompt if one has been drafted, OR
   commissioning a fresh draft at S34 open.
6. Running Phase 0 cold-start verification (mirror the S33 prompt's
   9-step shape, updating workspace HEAD anchor, repo HEAD anchor
   `f1cdce8`, tag count `13`, canonical baseline `970`, cassette
   fixture-count `30` / exclusions `30`, AND a Step 0.9 presence
   check for the S33 Azurite test file).

---

## Outstanding operator-input requests entering Session 34

1. **Session 34 scope choice** — pick from the carry-forwards in
   "Notes for Session 34" below. **K-a is CLOSED (S33).** Candidate
   E is EXHAUSTED (30 upper bound). None of A/D is on a critical
   path; both need operator action to become actionable. S34 may be
   a no-ship scope-resolution session — surface that at Phase 1.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*` continue across sessions (Sessions 8-33
   precedent). At S33 open the repo HEAD was exactly `cfa0ec1`
   (no new operator-side eval_data COMMIT since S32 close),
   with `eval_data/stage1_labels.jsonl` WIP + `eval_data/audits/`
   untracked.

3. **barcada-drift AI/ML alignment** — unchanged from S21-S33
   handoffs. 4 AI/ML team decisions need pre-resolution OR
   placeholders, plus 2+ canary_runs parquet files.

4. **launchd kit installation** — unchanged. Operator should run
   `scripts/launchd/install_canary_schedule.sh` when ready to
   enable the weekly Saturday canary job. Required prerequisite
   for Candidate A. **As of S33 close, NOT yet installed**
   (verified via `~/Library/LaunchAgents/` check during S33
   Phase 1 prerequisite audit: 0 barcada/canary plists; 0
   canary_runs parquets on disk).

5. **Session 34 prompt draft commissioning** — operator decides
   whether to commission an S34 prompt between sessions or scope
   one at S34 open.

6. **Azurite-backed CI test (K-a)** — CLOSED at S33, but as a
   **live-on-demand** net, NOT default-CI. The test is
   `@pytest.mark.live` + skip-by-default and is NOT in the canonical
   16-path, so it guards `cost_journal_adls.py` only when explicitly
   run under `-m live` in a Docker-capable environment. Wiring it
   into an actual CI pipeline is a separate, **un-done** step: the
   test needs Docker + the Azurite image in the runner, and it skips
   (does not fail) when they are absent; the pipeline must invoke
   `-m live` for it to fire. Do not over-trust it as automatic
   churn protection until that wiring exists.

---

## Notes for Session 34

Suggested S34 scope candidates (operator picks at S34 open):

### Candidate A (carry-forward): `barcada-drift` skeleton

Unchanged. Per CLASSIFICATION_ADJACENT_PLAN.md §Item 8. Consumes
`canary_runs/<date>.parquet` artifacts. **Blocked**: 2+ parquet
files needed AND 4 AI/ML decisions (or placeholders). As of S33
close: launchd installer not yet run; 0 canary_runs parquets on
disk; no AI/ML responses in workspace. Estimated ~300 LOC logic +
~70-100 LOC overhead floor ≈ ~370-400 LOC delivered.

### Candidate D (carry-forward): Phase 4 PR-D operator-led labeling

Unchanged. Tooling support only; labeling itself is operator
territory. W0 closed (workstream-0-end at `a1c5636` placed S27);
Phase 4 PR-D/E/F/G work is W0-side unblocked. Still gated on
operator-led Stage 2/3 labeling start.

### Candidate E (EXHAUSTED at S32)

The cassette corpus reached the plan's **30 upper bound** at S32
(`tests/fixtures/synthetic_crawls/` = 20 S20 + 5 S31 + 5 S32). The
plan §4 W7 cites "~20-30 representative domains"; 30 is the stated
ceiling. **No further +N is available without an explicit
plan-bound revision.** If the operator wants more cassettes, that
requires a Phase 2 (or plan) decision to raise the bound first.
Recording mechanics remain proven (S31+S32); the S32 LESSONS refine
pool-sizing to be category-driven.

### Candidate K-a (CLOSED at S33)

SHIPPED at `f1cdce8` — the Azurite-backed live integration test now
exists. Not a carry-forward. If future churn in `cost_journal_adls.py`
warrants broader live coverage (e.g., lease/SAS paths beyond the
5-step ETag matrix), that would be a NEW candidate, scoped fresh.

---

## Required reading (Session 34 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 33 entry — K-a Azurite-test
   narrative; the empty-warm-candidate-queue Phase 1; the
   version-skew finding + `--skipApiVersionCheck` fix; the
   unconditional-teardown validation; the carve-out + baseline re-pin.
3. **`LESSONS.md`** — the new "S33 folding" section (live-emulator
   fixture teardown + SDK-vs-emulator version skew + the
   carve-out/baseline-re-pin meta-pattern) PLUS the 3 "S32 folding"
   and 3 "S31 folding" sections if a live-HTTP or live-service scope
   is chosen.
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope
   section per Session 34 candidate choice. Plan is READ-ONLY
   (exception: a plan-amendment session to reopen E, with explicit
   operator authorization).
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A is chosen.
6. **`tools/synthetic_crawl/recorder.py` + `cli.py`** — only if a
   future session raises the cassette bound (E is otherwise
   exhausted).
7. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   + **`tests/classifier/pipeline/test_cost_journal_adls_azurite.py`**
   + **`scripts/smoke_test_adls_cost_journal.py`** — only if a new
   ADLS-surface scope is chosen.

---

## Outstanding items carried forward to Session 34+

1. **Per-tier cost-accounting wiring** — CLOSED end-to-end S28.
   All 8 `_TOTALS_FIELDS` slots wired. Unchanged.

2. **`barcada-drift` CLI** — §Item 8; 4 AI/ML decisions + 2+
   parquets outstanding. Re-verified empirically at S33 Phase 1:
   0 canary_runs parquets, 0 plist, no AI/ML responses.

3. **Cassette corpus expansion** — EXHAUSTED at 30 (S32 hit the
   plan upper bound). No further +N without a plan revision.

4. **Cassette-FP investigation** — archive.org + hashicorp.com
   (SaaS/SPA-shell `empty_page`) + stripe.com (WAF) flagged in
   S20's FP-curation log. DEFERRED at S31 + S32 (Q-E.3 =
   keep-as-is; touching them needs explicit authorization as they
   are S20-locked; the flags are correct behavior).

5. **launchd kit smoke-then-install** — Unchanged. Required for
   Candidate A.

6. **Phase 4 PR-D/E/F/G** (forward look) — W0-side unblocked
   since S27. Operator-led Stage 2 + Stage 3 labeling still
   needs to begin.

7. **CRAWLING_POLICY.md size** — CLOSED at S26 (2.52 KB).

8. **abfss:// CostJournal Phase 5 promotion** — CLOSED at S25.

9. **Live Azure smoke for ADLSCostJournal SCRIPT** — CLOSED S29.

10. **Stage 1 ShardResult LLM-vs-embedding split** — CLOSED S28.

11. **Live Azure smoke for ADLSCostJournal EXECUTION** — CLOSED
    S30. Trace clean; behavior matches `DummyBlobBackend`.

12. **Azurite-backed CI test for ADLSCostJournal** (Candidate
    K-a) — **CLOSED S33** (`f1cdce8`). An automated 5-step-ETag-matrix
    test against real Azurite now exists and verifies the real
    `_AzureBlobBackend` matches the in-memory `DummyBlobBackend` —
    but it is **live-on-demand** (`@pytest.mark.live`, skip-by-default,
    absent from the canonical 16-path), so it only fires under
    `-m live` in a Docker-capable environment. Default CI/test runs
    do NOT exercise it; pipeline wiring (`-m live` + Docker) is a
    separate un-done step. **Self-reproducing**: the
    `--skipApiVersionCheck` flag (which absorbs the SDK-vs-Azurite
    x-ms-version skew) is baked into the fixture's `docker run` args,
    NOT a manual flag — confirmed at S33 close by a clean
    from-no-container `-m live` run (`1 passed`). Disabling version
    validation entirely (vs pinning) means future azure-storage-blob
    upgrades cannot reintroduce the skew, and a failed container
    start SKIPS rather than silently passing — so there is NO latent
    version-skew gap for S34.

13. **Recorder reject-before-write / min-content-bytes floor +
    is_waf_challenge "Client Challenge" signature** — parser/
    recorder-hygiene observations (S31 + S32 folds). NOT a fix
    unless a future session scopes `tools/synthetic_crawl/` or
    `scraper/parser.py` tooling.

---

## Locked artifact reminders for Session 34

Carry-forward from Sessions 8-33. **NEW S33 lock**:
`tests/classifier/pipeline/test_cost_journal_adls_azurite.py` at
`f1cdce8` (292 LOC; 1 `@pytest.mark.live` test + module-scoped
Azurite fixture) AND the `live` marker registration in
`pyproject.toml` `[tool.pytest.ini_options]`. Do NOT modify without
Phase 2 authorization.

- `eval_data/` — labeling-workstream territory. Operator-WIP
  edits across sessions are expected. Pre-push validate_
  consistency runs against WT state; surface per LESSONS pattern
  if blocked.
- `stage1.schema.json` v1.0 with 49 keywords.
- `pre-remediation-2026-05-19` tag.
- `baseline-v0` tag at `9e9a1fb`.
- All `workstream-0-*-end` tags at their placed SHAs.
- `workstream-0-end` tag at `a1c5636` (annotated; placed S27).
  Do NOT move.
- `workstream-a-week1-end` tag at `fdc8a7a` (placed S22).
- Operator-side: `workstream-stage1-prestaged-flags-end` at
  `af6f1d4` and `workstream-stage1-step3-end` at `d4f06b8`. Both
  eval_data-only commits. Treat as operator-domain markers.
- `tests/runners/fixture_cascade/` — W4.1.5 driver area; locked
  at `dd64963` except via W5.X-prefix commits (S27 at `a1c5636`,
  S28 at `9afde57` + `ae9e627` — all LOCKED). S29-S33 did NOT
  touch this surface.
- `tests/fixtures/baseline-v0/` snapshot — locked at `9e9a1fb`.
- `tools/baseline_v0/` (check.py, generate.py, determinism.py,
  canary.py) — S18-20 deliverables; locked.
- `tools/synthetic_crawl/` package — S20 deliverable; locked.
  (The S31 + S32 cassette additions did NOT modify the tooling.)
- `tests/fixtures/synthetic_crawls/` — original 20 S20 cassettes
  locked at `7f11879`; 5 S31 cassettes locked at `06d67c4`; 5
  S32 cassettes locked at `cfa0ec1`.
- `scripts/launchd/` — S20 deliverable; locked. (Other `scripts/`
  files are NOT locked; new operator-driven scripts may land.)
- `src/barcada_scraper/scraper/robots.py` — S21; locked at
  `34a59b6`. `tests/scraper/test_robots.py` — S21; locked.
- `src/barcada_scraper/scraper/robots_gate.py` — S22; locked at
  `ba87e7e`. `src/barcada_scraper/scraper/robots_bypass_config.py`
  — S22; locked at `381ee89`. Plus their test files.
- `src/barcada_scraper/classifier/pipeline/cost_journal.py` —
  S22-extended at `1d9404e`. S27-S33 consumed the public API
  without modification.
- `src/barcada_scraper/classifier/pipeline/cost_journal_local.py`
  — production local-FS backend; locked.
- `src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
  — full backend at S25 SHA `835a531`. Public API:
  `ADLSCostJournal(journal_dir, run_id, credential=None,
  blob_backend=None)` with read / write_initial / try_update /
  exists / path. Locked. EMPIRICALLY VALIDATED at S30 (K-b live
  smoke) AND at S33 (Azurite live integration test). The S33 test
  injects the production `_AzureBlobBackend` via the public
  `blob_backend=` seam; it did NOT modify the module.
- `tests/classifier/pipeline/test_cost_journal_adls.py` — 19
  in-memory tests locked at `835a531`. Includes `DummyBlobBackend`.
- `tests/classifier/pipeline/test_cost_journal_adls_azurite.py` —
  S33 live test locked at `f1cdce8` (see NEW S33 lock above).
- `docs/CRAWLING_POLICY.md` — S26 SHA `2314f5e` (77 lines /
  2.52 KB). Changes require Phase 2 design-gate authorization.
- `src/barcada_scraper/orchestrator/robots_integration.py` — S23;
  locked at `279bb77`. Plus its 35-test file.
- The 4 S23 + 2 S24 + 1 S25-replaced tests in
  `tests/orchestrator/test_robots_gate_integration.py` — locked
  at `aed7873`. 7 tests total.
- `src/barcada_scraper/orchestrator/vmss_worker.py` — S23
  additions locked at `5eeaac7`.
- `src/barcada_scraper/orchestrator/job_runner.py` — S23
  additions locked at `872527e`.
- `scripts/vmss/cloud_init.template.yaml` — S23 additions locked.
- The 3 module-level helpers in
  `src/barcada_scraper/orchestrator/worker_loop.py`:
  `_open_cost_journal_for_worker` (body modified at S25 SHA
  `aed7873`; signature locked), `_ensure_journal_initialized`
  (locked at S24 SHA `48c324a`), `_build_durable_bypass_writer`
  (locked at S24 SHA `48c324a`).
- `tests/orchestrator/test_worker_loop_persistence.py` — S24 + 1
  S25-replaced test; locked at `aed7873`. 12 tests.
- The 5 S24-retargeted test_stage2_pages_invoker_* fixtures in
  `tests/orchestrator/test_worker_loop.py` — landed at `48c324a`.
- `docs/phase4_implementation_plan.md` — Phase 4 governance
  reference; do NOT modify until Phase 4 work is authorized.
- S28 LOCKS: `src/barcada_scraper/classifier/stage1/run.py`
  (ShardResult +2 fields at `776d203`);
  `tests/classifier/stage1/test_run_cascade.py` (+1 test at
  `776d203`).
- S29 LOCK: `scripts/smoke_test_adls_cost_journal.py` at
  `75a3937` (220 LOC). LOCKED — modifications require Phase 2
  authorization.
- `pyproject.toml` — NOT a locked artifact, but the S33 `live`
  marker registration under `[tool.pytest.ini_options]` is
  load-bearing for the Azurite test's `-m live` selection; do not
  remove it.
- Production code under `src/barcada_scraper/` — locked unless
  Phase 2 design-gate explicitly authorizes a specific module.
  S21+S22+S23+S24+S25+S28 authorized the modules listed in prior
  handoffs. S26 + S27 + S29 + S30 + S31 + S32 + **S33** added NO
  new src/ authorizations (S33 was a test-only ship).
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-34-open baseline

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

Sub-totals identical to S27-S33 close: 210 conformance + 52 driver
+ 99 baseline_v0 + 33 synthetic_crawl + 32 robots + 30 robots_gate
+ 30 robots_bypass_config + 43 cost_journal + 13 cost_journal_local
+ 19 cost_journal_adls + 35 robots_integration + 74 vmss_worker +
129 job_runner + 152 worker_loop + 7 robots_gate_integration + 12
worker_loop_persistence = 970. (The S33 Azurite test is live-marked
+ skip-by-default and is NOT in this invocation; the canonical count
is unchanged.)

OUT-OF-BAND live test (NOT in the canonical count; needs Docker +
the Azurite image, else SKIPS):

```
.venv/bin/python -m pytest \
    tests/classifier/pipeline/test_cost_journal_adls_azurite.py -m live
# Expected: 1 passed
```

Cumulative-test-count gate: the count NEVER decreases between
commit boundaries.

Narrower baselines (still valid for S34 candidates that don't
exercise the ADLS test paths):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 944 (S27-S33-equivalent narrower; canonical 16-path minus 19
  cost_journal_adls minus 7 robots_gate_integration)

**Fixture-count assertions for S34 Phase 0 Step 0.4**: html_count=222,
expected_count=202, meta_count=222, baseline_count=1213,
**`cassette_count == 30`, `exclusions_count == 30`** (UNCHANGED from
S33 — K-a added no cassettes).

Choose at Phase 0 Step 0.5 per Candidate selection.

---

## Pre-push gate at Session 34 open

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 354+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

Note on gate 4: validate_consistency runs against working-tree
state; if operator-WIP in eval_data introduces a schema violation
between S33 close and S34 open, the gate will block even though
no S34 commit touches eval_data. Per LESSONS: surface to operator
with the row+detail, propose operator-fix or stash-and-restore;
do NOT auto-fix.

S33 ran the gate clean at Phase 4 (0 errors / 0 warnings / PASS;
532 stage1 rows OK), including the pre-push hook re-run on push.
The S28 transient "1 error" curiosity did NOT reproduce in
S29/S30/S31/S32/S33. LESSONS-worthy if it reproduces in S34+.

---

## Context-window awareness

Session 33 ran Phase 0 → Phase 6 in a single context window with
1 test-only commit (Phase 0 verify + Docker/Azurite setup + 1 test
file + 1 mid-impl version-skew fix + Phase 6 close-out), within
budget. Session 34 budget per chosen candidate:

- Candidate A (barcada-drift): only if launchd job has run ≥2
  times AND AI/ML decisions ready. ~370-400 LOC delivered (per
  the S29-folded additive-overhead LESSONS pattern).
- Candidate D (Phase 4 PR-D tooling): operator-led; tooling only.
- Candidate E: EXHAUSTED at 30; not available without a plan-bound
  revision.
- (K-a is CLOSED — not a candidate.)

Strategies (unchanged from S20-S33 prompts):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-service-backed test (Azurite/LocalStack/DB
  container), default to the S33 fixture shape: unconditional
  try/finally teardown + idempotent self-healing pre-clean +
  skip-if-unavailable; expect an SDK-vs-emulator version-skew flag
  may be needed; keep the test off the canonical headline (live
  marker, skip-by-default) unless a deliberate decision adds it.
- For any live-HTTP corpus work, RECORD BROAD then CURATE BY
  CONTENT (S31/S32 pattern); size the pool to the category mix.
- Source-verify line numbers per Phase 3 commit (S23 LESSONS).
- Test against public API surface only (S24 LESSONS; S29/S30/S33
  extensions — the S33 live test used the public `blob_backend=`
  seam to inject the production backend).
- Source-verify facts behind option-set design BEFORE
  AskUserQuestion drafts (S25 LESSONS; S28-S33 demonstrated).
- Grep for same-shape tests outside the allowlist at Phase 0
  (S25 LESSONS).
- At Phase 2, count Q-* option sets; tier or split if >4 options
  (S26 LESSONS).
- Phase 0 fixture-count commands use the Python `rglob()` pattern,
  NOT bare `find` (S28 post-close LESSONS).

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S34 scope closes,
  transition per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-33:

1. Commit SHA(s) of each Session 34 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 970 baseline → S34 close.
4. Driver suite count (52/52 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (Workstream 0 closed at S27; W A.1 closed at
   S22's workstream-a-week1-end; W A.2 final-milestone tag
   `workstream-a-week2-end` OFFERED+DEFERRED at S33).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 33 handoff template. Refill at Session 34 close.
