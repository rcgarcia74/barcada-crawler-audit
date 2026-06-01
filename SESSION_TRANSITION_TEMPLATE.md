# Session Transition Template — Handoff from Session 32 → Session 33

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-32 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 33 invocation prompt:** NOT yet drafted at S32 close.
Per S20→S32 precedent, prompt-drafting is operator-commissioned
between sessions; operator decides whether to commission an S33
prompt or scope one at S33 open. A drafted prompt should mirror the
S20-S32 7-phase structure and pin: repo HEAD anchor `cfa0ec1`, tag
count `13`, canonical baseline `970`, Phase 0 Step 0.4
`cassette_count == 30` / `exclusions_count == 30`, and a Step 0.9
check that the 5 S31 + 5 S32 cassette dirs exist. Candidate set:
A (blocked), D (gated on labeling), **E (EXHAUSTED at the plan's
30 upper bound)**, K-a (OPTIONAL).

Anchors for Session 33 cold start:
- Workspace HEAD: the S32 close-out commit (SESSION_LOG.md +
  SESSION_TRANSITION_TEMPLATE.md + LESSONS.md) + 1-2 anchor-pin
  follow-ups pinning the actual close-out SHA into this section.
  S33 Phase 0 Step 0.1 MUST anchor workspace expectation to that
  SHA OR a later prompt-revision follow-up. Per S21-S32 LESSONS
  pattern "Workspace HEAD delta tolerance": tolerate N additional
  prompt-drafting / audit-correction commits between sessions;
  verify each is consistent with that pattern before continuing.
- Repo HEAD: `cfa0ec1` (S32 Candidate E continuation:
  WA0.W7.cassettes-corpus-expansion; +5 nonprofit/media/education
  cassettes; 25 → 30). Tolerated delta: operator-side eval_data
  labeling commits between S32 close and S33 open (Sessions 8-32
  precedent) — verify each is strictly `eval_data/*` via
  `git show --stat`.
- Canonical baseline: **970 tests** (16-path invocation;
  UNCHANGED from S27-S32 close — cassette additions are
  fixture-only and not exercised by any test in the invocation).
- Narrower baseline (for candidates that don't exercise ADLS
  test paths): **944 tests** (14-path; 970 minus 19
  cost_journal_adls minus 7 robots_gate_integration). Unchanged.
- **Fixture-count change at S32 (FLAGGED — S33 Phase 0 Step 0.4
  assertion target)**: `tests/fixtures/synthetic_crawls/` grew
  25 → 30 cassettes (+5 sidecars). The S33 Phase 0 Step 0.4 Python
  rglob() check MUST assert **`cassette_count == 30`** and
  **`exclusions_count == 30`** (NOT 25) — these are the exact
  variable names in the Step 0.4 block; leaving them at `== 25`
  HALTs S33 Phase 0 falsely. html=222 / expected=202 / meta=222 /
  baseline=1213 unchanged.
- Primary recommended scope: none — no carry-forward is on a
  critical path. Candidate E is now EXHAUSTED (plan upper bound 30
  reached). K-a (Azurite-backed CI test) remains OPTIONAL
  (defense-in-depth only per the S30 posture-validation LESSONS
  fold).
- Carry-forward candidates: A (barcada-drift; blocked on
  parquets + AI/ML), D (Phase 4 PR-D tooling; operator-led
  labeling not yet begun), **E (EXHAUSTED at 30 — no further +N
  without a plan-bound revision)**, K-a (Azurite-backed permanent
  CI test; OPTIONAL).

**S32 Candidate E continuation SHIPPED** — cassette corpus expanded
25 → 30 with 5 nonprofit/media/education domains (propublica.org,
apnews.com, c-span.org [media], eff.org [nonprofit], harvard.edu
[education]), each 200-OK real content, robots-gated,
byte-identical-replay verified, sidecar-shape-valid, zero exclusion
flags. Single bundled artifact commit `cfa0ec1`. No src/ / tooling /
.py changes. **Candidate E is now exhausted at the plan's 30 upper
bound.**

---

## Handoff metadata

- Outgoing session number: 32
- Closing date: 2026-06-01
- Outgoing session scope: Cassette corpus expansion continuation
  (S32 Candidate E; 25 → 30). 1 artifact-only code commit
  (`cfa0ec1`); 10 new fixture files (5 cassette.yaml + 5
  extract_hard_exclusions.json sidecars), 2,739,094 bytes. LLM
  spend: $0. Infrastructure: $0 (live HTTP GETs to public homepages
  + robots.txt; no paid service).
- Reason for transition: S32 single-candidate scope completed
  cleanly; Candidate E shipped end-to-end Phase 0 → Phase 6 in a
  single context window with no HALTs. No in-flight sub-surface.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `cfa0ec1` (WA0.W7.cassettes-corpus-expansion:
  +5 nonprofit/media/education cassettes (S32 Candidate E; 25 → 30)).
- Branch sync with `origin/main`: 0 ahead / 0 behind (pushed at
  S32 close).
- Tags (13 total; UNCHANGED from S30/S31 close):
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
- Pre-push gate state at HEAD `cfa0ec1`: VERIFIED GREEN at S32
  close (ruff check "All checks passed!" + ruff format 353 files
  + vermin 3.10 + validate_consistency 0 errors / 0 warnings).
  The pre-push hook also re-ran all gates green on push.
- Pre-S32 unstaged operator territory (Sessions 8-32 precedent):
  `eval_data/*` operator-WIP (`eval_data/stage1_labels.jsonl`
  modified at S32 open/close) + `eval_data/audits/` (untracked)
  + `.claude/scheduled_tasks.lock` (untracked) — all present at
  S32 open and left unstaged; verify via `git status` at S33 open.
  Repo HEAD was exactly `06d67c4` at S32 open (no tolerated
  operator-side eval_data COMMIT in `06d67c4..HEAD`).
- Corpus: 222 .html fixtures (unchanged from S17 close).
- 202 expected.json files (unchanged).
- 222 meta.json files (unchanged).
- **30 synthetic_crawl cassettes** (20 S20 + 5 S31 + 5 S32) + 30
  extract_hard_exclusions sidecars. WAS 25/25 at S31 close.
- MODIFIED Session 32 (1 artifact-only commit `cfa0ec1`):
    - `tests/fixtures/synthetic_crawls/propublica.org/` (NEW)
    - `tests/fixtures/synthetic_crawls/apnews.com/` (NEW)
    - `tests/fixtures/synthetic_crawls/c-span.org/` (NEW)
    - `tests/fixtures/synthetic_crawls/eff.org/` (NEW)
    - `tests/fixtures/synthetic_crawls/harvard.edu/` (NEW)
    - No `src/` changes. No test-suite changes. No tooling
      changes. No `.py` changes.
- (Unchanged from S31 close, all locked):
    - All S21-S29 deliverables.
    - The original 20 S20 cassettes at `7f11879` (UNTOUCHED;
      Q-E.3 = keep-as-is at S31 + S32).
    - The 5 S31 cassettes at `06d67c4` (UNTOUCHED).
    - `cost_journal_adls.py` (S25 full backend at `835a531`).
    - `docs/CRAWLING_POLICY.md` (S26 doc at `2314f5e`; 77 lines /
      2519 bytes).
    - S27+S28 deliverables; S29 K-b script at `75a3937`.
- Combined test suite at HEAD `cfa0ec1`:
    - **970 passed / 0 failed / 0 skipped** with the canonical
      16-path invocation (UNCHANGED — cassettes are fixture-only).
    - **944 passed / 0 failed / 0 skipped** with the narrower
      14-path invocation (unchanged).
    - **Stage 1 test counts**: 32 (16 test_run_cascade + 16
      test_cost_tracker) — unchanged. Outside the canonical
      16-path invocation.

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 32 start: `db79fe5` ("S32 prompt v2:
  reviewer-findings application"; succeeds `2b7f2e4` anchor-pin,
  which succeeds `b5f6bc5` S32 prompt draft). At S32 Phase 0 Step
  0.1 the 2 commits ahead of `b5f6bc5` were tolerated under the
  "Workspace HEAD delta tolerance" pattern (prompt-only edits).
- Session 32 close-out workspace commits: 1 primary close-out
  (SESSION_LOG.md + SESSION_TRANSITION_TEMPLATE.md + LESSONS.md)
  + 1-2 anchor-pin follow-ups (pinning the actual close-out SHA
  into this template's Anchors section for S33).
- **Last commit SHA at Session 32 CLOSE: the anchor-pin follow-up
  succeeding the primary close-out**. S33 Phase 0 Step 0.1 MUST
  anchor workspace expectation to that SHA OR the primary
  close-out. Per S21-S32 LESSONS pattern: tolerate N additional
  prompt-drafting / audit-correction commits between sessions.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected
  after Session 32 close push.

---

## Session 33 execution order (enforce strict sequence)

Same N-phase shape applies regardless of scope choice (Phase 0
cold-start verify → Phase 1 scope → Phase 2 design-gate → Phase 3
impl → Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 33 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 32 entry (cassette-expansion
   continuation narrative; per-cassette verification; the
   high-yield curation-DOWN-to-cap result; the khanacademy WAF
   reject).
3. Reading LESSONS.md additions Session 32 landed (2 new sections,
   "S32 folding" suffix: category-driven recording yield;
   is_waf_challenge "Client Challenge" signature gap).
4. Reading the relevant section of BARCADA_CRAWLER_
   REMEDIATION_PLAN.md for the chosen Session 33 scope.
5. Reading the Session 33 prompt if one has been drafted, OR
   commissioning a fresh draft at S33 open.
6. Running Phase 0 cold-start verification (mirror the S32 prompt's
   9-step shape, updating workspace HEAD anchor, repo HEAD anchor
   `cfa0ec1`, tag count `13`, canonical baseline `970`, and the
   **cassette fixture-count `30` / exclusions `30`**).

---

## Outstanding operator-input requests entering Session 33

1. **Session 33 scope choice** — pick from the carry-forwards in
   "Notes for Session 33" below. **Candidate E is now EXHAUSTED**
   (the plan's 30 upper bound is reached); no further cassette
   expansion without an explicit plan-bound revision. None of
   A/D/K-a is on a critical path.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*` continue across sessions (Sessions 8-32
   precedent). At S32 open the repo HEAD was exactly `06d67c4`
   (no new operator-side eval_data COMMIT since S31 close),
   with `eval_data/stage1_labels.jsonl` WIP + `eval_data/audits/`
   untracked.

3. **barcada-drift AI/ML alignment** — unchanged from S21-S32
   handoffs. 4 AI/ML team decisions need pre-resolution OR
   placeholders, plus 2+ canary_runs parquet files.

4. **launchd kit installation** — unchanged. Operator should run
   `scripts/launchd/install_canary_schedule.sh` when ready to
   enable the weekly Saturday canary job. Required prerequisite
   for Candidate A. **As of S32 close, NOT yet installed**
   (verified via `~/Library/LaunchAgents/` check during S32
   Phase 1 prerequisite audit: 0 barcada/canary plists; 0
   canary_runs parquets on disk).

5. **Session 33 prompt draft commissioning** — operator decides
   whether to commission an S33 prompt between sessions or scope
   one at S33 open.

6. **Live Azure smoke for ADLSCostJournal** — CLOSED at S30
   end-to-end. K-a Azurite-backed permanent CI test remains
   OPTIONAL defense-in-depth.

---

## Notes for Session 33

Suggested S33 scope candidates (operator picks at S33 open):

### Candidate A (carry-forward): `barcada-drift` skeleton

Unchanged. Per CLASSIFICATION_ADJACENT_PLAN.md §Item 8. Consumes
`canary_runs/<date>.parquet` artifacts. **Blocked**: 2+ parquet
files needed AND 4 AI/ML decisions (or placeholders). As of S32
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
plan-bound revision.** If the operator wants more cassettes in a
future session, that requires a Phase 2 (or plan) decision to
raise the bound first. Recording mechanics remain proven (S31+S32);
the S32 LESSONS refine pool-sizing to be category-driven.

### Candidate K-a (carry-forward; OPTIONAL since S30)

Per the S30-folded posture-validation LESSONS note: the K-b
operator-smoke (executed S30, trace clean) empirically closed the
mock-vs-prod divergence risk that K-a would have permanently
protected against. K-a is defense-in-depth only. Cost: ~50-100
LOC logic + ~70-100 LOC overhead floor ≈ ~120-200 LOC delivered
+ Docker setup + a 17th canonical path. No critical-path
justification at S33 open.

---

## Required reading (Session 33 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 32 entry — cassette-expansion
   continuation narrative; per-cassette determinism + sidecar
   verification; high-yield curation-DOWN-to-cap; the khanacademy
   WAF reject + reuters robots-exclusion.
3. **`LESSONS.md`** — the 2 new "S32 folding" sections
   (category-driven recording yield; is_waf_challenge "Client
   Challenge" signature gap) PLUS the 3 "S31 folding" sections.
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope
   section per Session 33 candidate choice. Plan is READ-ONLY.
5. **`tools/synthetic_crawl/recorder.py` + `cli.py`** — only if a
   future session raises the cassette bound (E is otherwise
   exhausted); record/replay mechanics; single `--domain` per
   invocation; robots gate; sidecar writer.
6. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A is chosen.
7. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   + **`scripts/smoke_test_adls_cost_journal.py`** — only if
   Candidate K-a is chosen.

---

## Outstanding items carried forward to Session 33+

1. **Per-tier cost-accounting wiring** — CLOSED end-to-end S28.
   All 8 `_TOTALS_FIELDS` slots wired. Unchanged.

2. **`barcada-drift` CLI** — §Item 8; 4 AI/ML decisions + 2+
   parquets outstanding. Re-verified empirically at S32 Phase 1:
   0 canary_runs parquets, 0 plist, no AI/ML responses.

3. **Cassette corpus expansion** — **EXHAUSTED at 30** (S32 hit
   the plan upper bound). No further +N without a plan revision.

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
    K-a) — carry-forward; OPTIONAL (defense-in-depth only).

13. **Recorder reject-before-write / min-content-bytes floor +
    is_waf_challenge "Client Challenge" signature** — parser/
    recorder-hygiene observations (S31 + S32 folds). NOT a fix
    unless a future session scopes `tools/synthetic_crawl/` or
    `scraper/parser.py` tooling.

---

## Locked artifact reminders for Session 33

Carry-forward from Sessions 8-32. **NEW S32 lock**: the 5 new
cassette dirs under `tests/fixtures/synthetic_crawls/`
(propublica.org / apnews.com / c-span.org / eff.org / harvard.edu)
at `cfa0ec1` (artifact-only fixtures; do NOT re-record or delete
without Phase 2 authorization).

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
  S28 at `9afde57` + `ae9e627` — all LOCKED). S29-S32 did NOT
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
  S22-extended at `1d9404e`. S27-S32 consumed the public API
  without modification.
- `src/barcada_scraper/classifier/pipeline/cost_journal_local.py`
  — production local-FS backend; locked.
- `src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
  — full backend at S25 SHA `835a531`. Public API:
  `ADLSCostJournal(journal_dir, run_id, credential=None,
  blob_backend=None)` with read / write_initial / try_update /
  exists / path. Locked. EMPIRICALLY VALIDATED at S30 against
  real Azure via the K-b script.
- `tests/classifier/pipeline/test_cost_journal_adls.py` — 19
  tests locked at `835a531`. Includes `DummyBlobBackend`.
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
- Production code under `src/barcada_scraper/` — locked unless
  Phase 2 design-gate explicitly authorizes a specific module.
  S21+S22+S23+S24+S25+S28 authorized the modules listed in prior
  handoffs. S26 + S27 + S29 + S30 + S31 + **S32** added NO new
  src/ authorizations (S31 + S32 were fixture-only).
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-33-open baseline

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

Sub-totals identical to S27-S32 close: 210 conformance + 52 driver
+ 99 baseline_v0 + 33 synthetic_crawl + 32 robots + 30 robots_gate
+ 30 robots_bypass_config + 43 cost_journal + 13 cost_journal_local
+ 19 cost_journal_adls + 35 robots_integration + 74 vmss_worker +
129 job_runner + 152 worker_loop + 7 robots_gate_integration + 12
worker_loop_persistence = 970. (S31's + S32's cassette additions
are fixture-only; the 33 synthetic_crawl tests are hermetic and do
not exercise committed cassettes — the canonical count is
unchanged.)

Cumulative-test-count gate: the count NEVER decreases between
commit boundaries.

Narrower baselines (still valid for S33 candidates that don't
exercise the ADLS test paths):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 944 (S27-S32-equivalent narrower; canonical 16-path minus 19
  cost_journal_adls minus 7 robots_gate_integration)

**Fixture-count assertions for S33 Phase 0 Step 0.4**: html_count=222,
expected_count=202, meta_count=222, baseline_count=1213,
**`cassette_count == 30`, `exclusions_count == 30`** (WAS 25/25
at S31 close; S32 added 5).

Choose at Phase 0 Step 0.5 per Candidate selection.

---

## Pre-push gate at Session 33 open

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 353+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

Note on gate 4: validate_consistency runs against working-tree
state; if operator-WIP in eval_data introduces a schema violation
between S32 close and S33 open, the gate will block even though
no S33 commit touches eval_data. Per LESSONS: surface to operator
with the row+detail, propose operator-fix or stash-and-restore;
do NOT auto-fix.

S32 ran the gate clean at Phase 4 (0 errors / 0 warnings / PASS;
532 stage1 rows OK), including the pre-push hook re-run on push.
The S28 transient "1 error" curiosity did NOT reproduce in
S29/S30/S31/S32. LESSONS-worthy if it reproduces in S33+.

---

## Context-window awareness

Session 32 ran Phase 0 → Phase 6 in a single context window with
1 artifact-only commit (15 live-HTTP recordings + curation-down-to-5
+ 1 commit + Phase 6 close-out), within budget. Session 33 budget
per chosen candidate:

- Candidate A (barcada-drift): only if launchd job has run ≥2
  times AND AI/ML decisions ready. ~370-400 LOC delivered (per
  the S29-folded additive-overhead LESSONS pattern).
- Candidate D (Phase 4 PR-D tooling): operator-led; tooling only.
- Candidate E: EXHAUSTED at 30; not available without a plan-bound
  revision.
- Candidate K-a (Azurite-backed integration test): ~120-200 LOC
  delivered + Docker setup. OPTIONAL; no critical-path
  justification.

Strategies (unchanged from S20-S32 prompts):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-HTTP corpus work, RECORD BROAD then CURATE BY
  CONTENT (S31/S32 pattern): expect 403/WAF + ReadTimeout rejects;
  keep only 200-OK real-content cassettes; verify byte-identical
  replay + sidecar shape + empty exclusion reasons before commit.
  Per the S32 fold: size the pool to the category mix (~1.1×N for
  low-WAF .edu/foundation/public-affairs-media; ~2.5×N for
  commerce/consumer); inspect title+visible-text, not just sidecar
  flags (is_waf_challenge missed khanacademy's "Client Challenge").
- Source-verify line numbers per Phase 3 commit (S23 LESSONS).
- Test against public API surface only (S24 LESSONS; S29/S30
  extensions).
- Source-verify facts behind option-set design BEFORE
  AskUserQuestion drafts (S25 LESSONS; S28/S29/S31/S32 demonstrated).
- Grep for same-shape tests outside the allowlist at Phase 0
  (S25 LESSONS).
- At Phase 2, count Q-* option sets; tier or split if >4 options
  (S26 LESSONS).
- Phase 0 fixture-count commands use the Python `rglob()` pattern,
  NOT bare `find` (S28 post-close LESSONS).
- For new wrapper-class + external-service surfaces, default to
  operator-smoke (K-b) posture, not permanent CI (K-a) — S30
  LESSONS.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S33 scope closes,
  transition per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-32:

1. Commit SHA(s) of each Session 33 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 970 baseline → S33 close.
4. Driver suite count (52/52 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (Workstream 0 closed at S27; W A.1 closed at
   S22's workstream-a-week1-end; W A.2 milestones depend on
   completion).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 32 handoff template. Refill at Session 33 close.
