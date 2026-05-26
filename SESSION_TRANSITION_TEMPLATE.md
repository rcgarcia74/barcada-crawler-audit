# Session Transition Template — Handoff from Session 30 → Session 31

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-30 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 31 invocation prompt:** NOT YET DRAFTED at S30 close.
S30 was Candidate K-b-exec (operator-driven execution of the
S29 K-b smoke script against live Azure); zero code commits and
no in-flight scope. Per S20-S29 precedent, the next-session
prompt is operator-commissioned between sessions — not always-on
close-out work. If the operator wants to commission an S31
prompt, draft it post-close referencing this template + the
S30 SESSION_LOG.md entry + the new S30-folded LESSONS section
(posture-validation note for operator-smoke vs CI test
tradeoffs).

Anchors for Session 31 cold start:
- Workspace HEAD: the S30 close-out commit (succeeds the S30
  anchor-pin follow-up `5421cb2`, which itself succeeds the
  S30 prompt review-fixes commit `09f9dd8` and the S30 prompt
  draft `589c6af`). S31 Phase 0 Step 0.1 MUST anchor workspace
  expectation to the close-out commit's SHA (pinned by the
  follow-up commit that lands AFTER the primary close-out per
  S21-S29 LESSONS pattern "Workspace HEAD delta tolerance").
- Repo HEAD: `af6f1d4` (operator-side eval_data audit:
  A3 pre-staged flags + appointment_booking refinement;
  1 commit ahead of S29 close at `75a3937`; eval_data-only
  per `git show --stat`). Tolerated delta: operator-side
  eval_data labeling commits between S30 close and S31 open
  (Sessions 8-30 precedent).
- Canonical baseline: **970 tests** (16-path invocation;
  unchanged from S27/S28/S29 close — S30 shipped zero code
  commits).
- Narrower baseline (for candidates that don't exercise ADLS
  test paths): **944 tests** (14-path; 970 minus 19
  cost_journal_adls minus 7 robots_gate_integration). Unchanged
  from S27/S28/S29 close.
- Primary recommended scope: none — no carry-forward is on a
  critical path. K-a (Azurite-backed CI test) was **downgraded
  to OPTIONAL** at S30 per the new posture-validation LESSONS
  fold; it's defense-in-depth only.
- Carry-forward candidates: A (barcada-drift; blocked on
  parquets + AI/ML), D (Phase 4 PR-D tooling; operator-led
  labeling not yet begun), E (cassette corpus expansion 20 →
  25/30), K-a (Azurite-backed permanent CI test; NOW OPTIONAL
  rather than required per S30 LESSONS fold).

**S29 K-b-exec carry-forward CLOSED at S30** — the K-b script
ran clean end-to-end against a live Azure sandbox container on
its first execution; trace matched `DummyBlobBackend` behavior
in all 5 steps. No follow-up needed.

---

## Handoff metadata

- Outgoing session number: 30
- Closing date: 2026-05-26
- Outgoing session scope: ADLSCostJournal live Azure smoke
  EXECUTION (S30 Candidate K-b-exec). **Zero code commits.**
  Operator ran `scripts/smoke_test_adls_cost_journal.py`
  against a live Azure sandbox; Claude interpreted the 5-step
  trace. All 5 steps OK; ADLSCostJournal behavior matches
  `DummyBlobBackend`. LLM spend: $0. Infrastructure: ~$0
  (sub-cent Azure Blob operations on operator's sandbox).
- Reason for transition: S30 single-purpose scope completed
  cleanly; Candidate K-b-exec closed end-to-end. Phase 1 →
  Phase 6 in a single context window with no HALTs. No
  in-flight sub-surface.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `af6f1d4` (stage1 audit: A3 pre-staged flags
  + appointment_booking refinement; operator-side eval_data
  commit between S29 close and S30 open).
- Last commit subject: "stage1 audit: A3 pre-staged flags +
  appointment_booking refinement".
- Branch sync with `origin/main`: 0 ahead / 0 behind (no S30
  code commits).
- Tags (13 total; **2 NEW operator-side eval_data tags
  observed between S29 close and S30 open**):
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
  - **`workstream-stage1-prestaged-flags-end`** at `af6f1d4`
    (NEW; operator-side eval_data tag; observed at S30 open)
  - **`workstream-stage1-step3-end`** at `d4f06b8` (NEW;
    operator-side eval_data tag; observed at S30 open)
- Pre-push gate state at HEAD `af6f1d4`: not re-verified at S30
  close (no S30 code commits triggered Phase 4); state from
  S29 close preserved (ruff + ruff format on 353 files + vermin
  3.10 + validate_consistency 0/0).
- Pre-S30 unstaged operator territory (Sessions 8-30 precedent):
  `eval_data/*.jsonl` operator-WIP edits (no specific files
  pinned here; verify via `git status` at S31 open).
  S30 saw 1 tolerated operator-side eval_data commit between
  S29 close (`75a3937`) and S30 open (`af6f1d4`): the stage1
  audit commit. Strictly `eval_data/*` per `git show --stat`.
- Corpus: 222 .html fixtures (unchanged from S17 close).
- 202 expected.json files (unchanged).
- 222 meta.json files (unchanged).
- 1213 baseline-v0 files (unchanged from S18 close at `9e9a1fb`).
- MODIFIED Session 30 (0 code commits; trace-only):
    - No `src/` changes.
    - No test-suite changes.
    - No `scripts/` changes (the S29 K-b script was EXECUTED
      against live Azure; its content is unchanged at SHA
      `75a3937`).
- (Unchanged from S29 close, all locked):
    - All S21-S26+S28+S29 deliverables.
    - `cost_journal_adls.py` (S25 full backend at `835a531`).
    - `_open_cost_journal_for_worker` body (S25 abfss://
      dispatch at `aed7873`).
    - `docs/CRAWLING_POLICY.md` (S26 tightened doc at `2314f5e`;
      77 lines / 2519 bytes).
    - S27+S28 deliverables (cascade.py per-tier wiring at
      `a1c5636` + Stage 1 invoker switch at `9afde57`;
      test_cost_journal_wiring.py at `a1c5636` + 1↔1
      replacement at `ae9e627`; ShardResult split at `776d203`).
    - S29 deliverable: `scripts/smoke_test_adls_cost_journal.py`
      at `75a3937` (220 LOC; verified import-loads + public
      surface intact at S30 Phase 0 Step 0.9).
- Combined test suite at HEAD `af6f1d4`:
    - **970 passed / 0 failed / 0 skipped** with the canonical
      16-path invocation (unchanged from S27/S28/S29 close).
    - **944 passed / 0 failed / 0 skipped** with the narrower
      14-path invocation (unchanged from S27/S28/S29 close).
    - **Stage 1 test counts**: 32 (16 test_run_cascade + 16
      test_cost_tracker) — unchanged. Outside the canonical
      16-path invocation.

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 30 start: `5421cb2` (S30 Step 0.1
  anchor-pin update; succeeds `09f9dd8` S30 prompt review fixes,
  which succeeds `589c6af` S30 prompt drafted, which succeeds
  the S29 anchor-pin follow-up `e736eee`). At S30 Phase 0 Step
  0.1 all three workspace commits were tolerated under the
  "Workspace HEAD delta tolerance" pattern (all prompt-only
  edits).
- Session 30 close-out workspace commits: TBD (this template
  is part of the primary close-out commit; expected 1-2
  follow-up commits pinning the anchor SHA for S31 Phase 0
  Step 0.1, per S21-S29 LESSONS pattern).
- **Last commit SHA at Session 30 CLOSE: TBD (the anchor-pin
  follow-up commit that succeeds the primary close-out)**. S31
  prompt's Phase 0 Step 0.1 MUST anchor workspace expectation
  to THAT follow-up's SHA. Per S21-S30 LESSONS pattern: tolerate
  N additional prompt-drafting / audit-correction commits
  between sessions; verify each is consistent with that pattern
  before continuing.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected
  after Session 30 close push.

---

## Session 31 execution order (enforce strict sequence)

Same N-phase shape applies regardless of scope choice (Phase 0
cold-start verify → Phase 1 scope → Phase 2 design-gate → Phase 3
impl → Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 31 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 30 entry.
3. Reading the LESSONS.md additions Session 30 landed (1 new
   section at end of file, "S30 folding" suffix:
   posture-validation note for operator-smoke vs CI test
   tradeoffs).
4. Reading the relevant section of BARCADA_CRAWLER_
   REMEDIATION_PLAN.md for the chosen Session 31 scope (see
   "Notes for Session 31" below).
5. Reading the Session 31 prompt if one has been drafted, OR
   commissioning a fresh draft at S31 open.
6. Running Phase 0 cold-start verification per the prompt's
   protocol (or per the S30 prompt template if S31 prompt is
   not yet drafted; mirror the 9-step verification shape,
   updating workspace HEAD anchor, repo HEAD anchor
   (`af6f1d4`), tag count (`13`), and canonical baseline
   (`970`)).

---

## Outstanding operator-input requests entering Session 31

1. **Session 31 scope choice** — pick from the carry-forwards
   in "Notes for Session 31" below. Candidate K-b-exec (script
   execution) closed at S30; the remaining carry-forwards
   (A/D/E/K-a) are all available but none is on a critical
   path. **No new carry-forward introduced by S30.**

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*.jsonl` continue across sessions (Sessions 8-30
   precedent). S30 saw 1 operator-side eval_data commit
   between S29 close (`75a3937`) and S30 open (`af6f1d4`):
   the stage1 audit + 2 NEW operator-side eval_data tags
   (`workstream-stage1-prestaged-flags-end`,
   `workstream-stage1-step3-end`). validate_consistency state
   from S29 close preserved (not re-verified at S30 close —
   no S30 code commits triggered Phase 4).

3. **barcada-drift AI/ML alignment** — unchanged from S21-S30
   handoffs. If operator wants to ship `barcada-drift` in S31,
   the 4 AI/ML team decisions need to be pre-resolved OR scoped
   narrowly with placeholders. Plus the prereq of 2+ parquet
   files (earliest natural date 2026-06-06 if the launchd
   installer fires immediately after S30 close).

4. **launchd kit installation** — unchanged. Operator should
   run `scripts/launchd/install_canary_schedule.sh` when ready
   to enable the weekly Saturday-9am canary job. Required
   prerequisite for Candidate A. **As of S30 close, NOT yet
   installed** (verified via `~/Library/LaunchAgents/` check
   during S30 Phase 1 prerequisite audit; unchanged from S29
   close).

5. **Session 31 prompt draft commissioning** — operator decides
   whether to commission an S31 prompt between sessions or
   scope one at S31 open.

6. **Live Azure smoke for ADLSCostJournal** — **CLOSED at S30**
   end-to-end. Script shipped S29 + executed S30 + trace clean
   + behavior matches `DummyBlobBackend`. No further action
   required unless a future divergence surfaces (in which case
   the K-a Azurite-backed test becomes warranted; until then
   it stays optional defense-in-depth).

---

## Notes for Session 31

Suggested S31 scope candidates (operator picks at S31 open):

### Candidate A (carry-forward): `barcada-drift` skeleton

Unchanged from S21-S30 handoffs. Per
CLASSIFICATION_ADJACENT_PLAN.md §Item 8. Consumes
`canary_runs/<date>.parquet` artifacts. **Blocked**: 2+ parquet
files needed AND 4 AI/ML decisions (or placeholders). As of S30
close: launchd installer not yet run; 0 parquets on disk; no
AI/ML responses in workspace. Earliest natural date 2026-06-06.
Estimated ~300 LOC logic + ~70-100 LOC overhead floor ≈
~370-400 LOC delivered per the S29-folded LESSONS additive-
overhead pattern.

### Candidate D (carry-forward): Phase 4 PR-D operator-led labeling

Unchanged. Tooling support only; labeling itself is operator
territory. W0 is closed (workstream-0-end at `a1c5636` placed
S27); Phase 4 PR-D/E/F/G work is W0-side unblocked. Still gated
on operator-led Stage 2/3 labeling start.

### Candidate E (carry-forward): Cassette corpus expansion

Unchanged from S22-S30 handoffs. S20 shipped 20 cassettes;
plan's upper bound is 30. Could expand or curate. Optional FP
re-investigation of archive.org / hashicorp.com / stripe.com.

### Candidate K-a (carry-forward; DOWNGRADED to OPTIONAL at S30)

Per the new S30-folded LESSONS posture-validation note: the
K-b operator-smoke (executed S30, trace clean) empirically
closed the mock-vs-prod divergence risk that K-a would have
permanently protected against. K-a now serves only as
defense-in-depth, NOT as a prerequisite for confidence in the
ADLSCostJournal surface.

Operator may still choose K-a if a permanent CI safety net is
desired (e.g., if `cost_journal_adls.py` will see frequent
churn). Cost: ~50-100 LOC logic + ~70-100 LOC overhead floor
≈ ~120-200 LOC delivered + Docker setup + a 17th canonical
path. No critical-path justification at S31 open.

---

## Required reading (Session 31 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 30 entry — zero-commit narrative;
   the K-b-exec trace + interpretation; tag-variance disposition
   (2 new operator-side eval_data tags accepted); empirical
   Phase 1 prereq audit for Candidate A (unchanged from S29).
3. **`LESSONS.md`** — 1 new section appended at S30 close:
   - "Operator-smoke posture (K-b) can close mock-vs-prod
     divergence risk in one execution; permanent CI test (K-a)
     is then optional rather than required" (S30 folding;
     forward-applicable to similar wrapper-class + external-
     service surfaces).
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope
   section per Session 31 candidate choice. Plan is READ-ONLY.
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A (barcada-drift) is chosen.
6. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   — only if Candidate K-a is chosen (Azurite-backed test).
7. **`scripts/smoke_test_adls_cost_journal.py`** at S29 SHA
   `75a3937` — for reference if Candidate K-a is chosen (the
   K-b script's structure informs the K-a test layout).
8. **`docs/CRAWLING_POLICY.md`** at S26 SHA `2314f5e` — only if
   operator wants to review the S26-tightened version (77 lines
   / 2.52 KB). Locked.

---

## Outstanding items carried forward to Session 31+

1. **Per-tier cost-accounting wiring** — CLOSED end-to-end S28.
   All 8 `_TOTALS_FIELDS` slots wired. Unchanged at S30.

2. **`barcada-drift` CLI** — CLASSIFICATION_ADJACENT_PLAN.md
   §Item 8; 4 AI/ML team decisions outstanding. Blocked also
   on 2+ canary_runs parquet files. Unchanged from S29 close
   (re-verified empirically at S30 Phase 1: 0 parquets, 0
   plist, no AI/ML responses).

3. **Cassette corpus expansion** — current 20 domains is lower
   bound of plan's "~20-30". Unchanged.

4. **Cassette-FP investigation** — archive.org + hashicorp.com
   flagged as SaaS-shell FPs in S20's FP-curation log.
   Unchanged.

5. **launchd kit smoke-then-install** — Unchanged. Operator
   should run `scripts/launchd/install_canary_schedule.sh` to
   enable the weekly job. Required for Candidate A.

6. **Phase 4 PR-D/E/F/G** (forward look) — W0-side unblocked
   since S27. Operator-led Stage 2 + Stage 3 labeling work
   still needs to begin before PR-D/E/F/G work can land.

7. **CRAWLING_POLICY.md size** — CLOSED at S26 (2.52 KB).

8. **abfss:// CostJournal Phase 5 promotion** — CLOSED at S25.

9. **Live Azure smoke for ADLSCostJournal SCRIPT** — CLOSED at
   S29 (Candidate K-b script ship).

10. **Stage 1 ShardResult LLM-vs-embedding split** — CLOSED S28
    (Candidate StgSplit).

11. **Live Azure smoke for ADLSCostJournal EXECUTION** —
    **CLOSED at S30** (Candidate K-b-exec). Trace clean
    end-to-end; behavior matches `DummyBlobBackend`.

12. **Azurite-backed CI test for ADLSCostJournal** (Candidate
    K-a) — still carry-forward; **DOWNGRADED to OPTIONAL** at
    S30 per the new posture-validation LESSONS fold. Defense-
    in-depth only; not on any critical path.

---

## Locked artifact reminders for Session 31

Carry-forward from Sessions 8-30 (no NEW locks added at S30 —
zero code commits):

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
- **NEW S30-observed (operator-side, NOT placed by Claude)**:
  `workstream-stage1-prestaged-flags-end` at `af6f1d4` and
  `workstream-stage1-step3-end` at `d4f06b8`. Both eval_data-
  only commits. Treat as operator-domain markers.
- `tests/runners/fixture_cascade/` — W4.1.5 driver area; locked
  at `dd64963` except via W5.X-prefix commits. S27 modifications
  at `a1c5636` and S28 modifications at `9afde57` + `ae9e627`
  are LOCKED. S29 + S30 did NOT touch this surface.
- `tests/fixtures/baseline-v0/` snapshot — locked at `9e9a1fb`.
- `tools/baseline_v0/check.py`, `generate.py`, `determinism.py`,
  `canary.py` — S18-20 deliverables; locked.
- `tools/synthetic_crawl/` package — S20 deliverable; locked.
- `tests/fixtures/synthetic_crawls/` — S20 corpus; locked.
- `scripts/launchd/` — S20 deliverable; locked. (Other
  `scripts/` files are NOT locked; new operator-driven scripts
  may land per S29 K-b precedent.)
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
  S22-extended at `1d9404e`. S27-S30 consumed the existing
  public API without modification.
- `src/barcada_scraper/classifier/pipeline/cost_journal_local.py`
  — production local-FS backend; locked.
- `src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
  — full backend shipped at S25 SHA `835a531`. Public API:
  `ADLSCostJournal(journal_dir, run_id, credential=None,
  blob_backend=None)` with read / write_initial / try_update /
  exists / path. Locked. **EMPIRICALLY VALIDATED at S30
  against real Azure Blob storage via the K-b script.**
- `tests/classifier/pipeline/test_cost_journal_adls.py` — 19
  tests locked at `835a531`. Includes `DummyBlobBackend`.
- `docs/CRAWLING_POLICY.md` — tightened W A.1 doc at S26 SHA
  `2314f5e` (77 lines / 2.52 KB). Further trimming OR additions
  require Phase 2 design-gate authorization.
- `src/barcada_scraper/orchestrator/robots_integration.py` —
  S23 deliverable; locked at `279bb77`.
- `tests/orchestrator/test_robots_integration.py` — S23
  deliverable; locked at `279bb77`. 35 tests.
- The 4 S23 tests + 2 unchanged S24 tests + 1 S25-replaced test
  in `tests/orchestrator/test_robots_gate_integration.py` —
  locked at `aed7873`. 7 tests total.
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
- The S24 3-line wiring block in `scrape_stage2_pages_invoker`
  at `48c324a` (with adjacent comment updated at S25 SHA
  `aed7873`).
- `tests/orchestrator/test_worker_loop_persistence.py` — S24
  deliverable + 1 S25-replaced test; locked at `aed7873`. 12
  tests.
- The 5 S24-retargeted test_stage2_pages_invoker_* fixtures in
  `tests/orchestrator/test_worker_loop.py` — landed at `48c324a`.
  Do NOT revert to abfss://.
- `docs/phase4_implementation_plan.md` — Phase 4 governance
  reference; do NOT modify until Phase 4 work is operator-
  authorized.
- S28 LOCKS (unchanged at S30 close):
  - `src/barcada_scraper/classifier/stage1/run.py` —
    `ShardResult` adds `llm_cost_usd` + `embedding_cost_usd`
    (S28 SHA `776d203`).
  - `tests/classifier/stage1/test_run_cascade.py` — +1 net-new
    test at S28 SHA `776d203`.
- S29 LOCK (unchanged at S30 close):
  - `scripts/smoke_test_adls_cost_journal.py` at S29 SHA
    `75a3937` (220 LOC). Operator-driven 5-step ETag-conflict-
    matrix smoke. Mirrors `scripts/smoke_test_adls_gen2.py`
    conventions. LOCKED — further modifications to the script
    require Phase 2 design-gate authorization at the session
    that proposes them.
- Production code under `src/barcada_scraper/` — locked unless
  Phase 2 design-gate explicitly authorizes a specific module.
  S21+S22+S23+S24+S25+S28 authorized: `scraper/robots.py`,
  `scraper/robots_gate.py`, `scraper/robots_bypass_config.py`,
  `classifier/pipeline/cost_journal.py` (additive only),
  `classifier/pipeline/cost_journal_adls.py` (S25 skeleton →
  full backend),
  `orchestrator/robots_integration.py` (new),
  `orchestrator/vmss_worker.py` (additive),
  `orchestrator/job_runner.py` (additive),
  `orchestrator/worker_loop.py` (additive: S23 gate wiring +
  S24 durable persistence helpers + S25 abfss:// guard removal
  in 1 helper body),
  `classifier/stage1/run.py` (S28 additive: ShardResult +2
  fields + _build_shard_result populate). S26 + S27 + **S29 +
  S30** added no new src/ authorizations.
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-31-open baseline

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

Sub-totals identical to S27/S28/S29/S30 close: 210 conformance +
52 driver + 99 baseline_v0 + 33 synthetic_crawl + 32 robots + 30
robots_gate + 30 robots_bypass_config + 43 cost_journal + 13
cost_journal_local + 19 cost_journal_adls + 35 robots_integration
+ 74 vmss_worker + 129 job_runner + 152 worker_loop + 7
robots_gate_integration + 12 worker_loop_persistence = 970.
(S30's K-b-exec is operator-driven execution; no new tests, no
new scripts, no new code commits — the canonical count is
unchanged.)

Cumulative-test-count gate: the count NEVER decreases between
commit boundaries.

Narrower baselines (still valid for S31 candidates that don't
exercise the new ADLS test paths):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 944 (S27/S28/S29/S30-equivalent narrower; canonical 16-path
  minus 19 cost_journal_adls minus 7 robots_gate_integration)

Choose at Phase 0 Step 0.5 per Candidate selection.

---

## Pre-push gate at Session 31 open

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
between S30 close and S31 open, the gate will block even though
no S31 commit touches eval_data. Per LESSONS: surface to operator
with the row+detail, propose operator-fix or stash-and-restore;
do NOT auto-fix.

S29 did NOT reproduce the S28 transient "1 error" curiosity.
S30 did NOT re-run the gate (zero code commits). LESSONS-worthy
if the transient reproduces in S31+.

---

## Context-window awareness

Session 30 ran Phase 1 → Phase 6 in a single context window with
zero code commits + 1 trace interpretation, well within budget.
Session 31 budget per chosen candidate:

- Candidate A (barcada-drift): only if launchd job has run ≥2
  times AND AI/ML decisions ready. Estimated ~300 LOC logic +
  ~70-100 LOC overhead floor ≈ ~370-400 LOC delivered (per the
  S29-folded additive-overhead LESSONS pattern; NOT a linear
  ~3× multiplier).
- Candidate D (Phase 4 PR-D tooling): operator-led; tooling
  only.
- Candidate E (cassette corpus expansion): depends on operator
  curation choices.
- Candidate K-a (Azurite-backed integration test): ~50-100 LOC
  logic + ~70-100 LOC overhead floor ≈ ~120-200 LOC delivered
  + Docker setup. **NOW OPTIONAL** per the S30 LESSONS fold —
  no critical-path justification.

Strategies (unchanged from S20-S30 prompts):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-HTTP corpus work, pilot 1-3 before full N-domain.
- Source-verify line numbers per Phase 3 commit, not just at
  Phase 2 (S23 LESSONS pattern).
- Test against public API surface only — probe `.path` /
  behavior, not private attrs (S24 LESSONS pattern; S29
  extended to operator scripts via parallel-SDK-client cleanup;
  S30 empirically validated against real Azure).
- Source-verify facts behind option-set design BEFORE
  AskUserQuestion drafts (S25 LESSONS pattern; S28 + S29
  demonstrated this directly).
- Grep for same-shape tests outside the prompt's explicit
  allowlist at Phase 0 (S25 LESSONS Q-J.8 extension lesson).
- At Phase 2, count the prompt's Q-* option set; if any single
  Q-* enumerates >4 options, tier the question or split the
  AskUserQuestion call rather than silently narrowing (S26
  LESSONS pattern).
- When deferring a low-severity wiring gap, document the
  specific parallel-API seam that will close it later (S27
  LESSONS pattern).
- At retrofit time, audit existing test pins for "by design"
  vs "empirically true" distinction (S28 LESSONS pattern).
- Phase 0 fixture-count commands need `2>/dev/null` + a bounded
  timeout — use the Python `rglob()` pattern (S28 post-close
  LESSONS pattern).
- When sizing operator-driven Python script deliverables, use
  the additive overhead-floor framing (~70-100 LOC for
  Copyright + docstring + imports + argparse), NOT a linear
  ~3× multiplier (S29 LESSONS pattern; the K-b ~3× ratio was a
  small-logic special case).
- When an operator-driven script needs an operation a wrapper
  class doesn't expose, construct a parallel SDK client rather
  than reach into private attrs (S29 LESSONS pattern; S30
  validated empirically).
- **NEW S30 LESSONS pattern**: for new wrapper-class + external-
  service surfaces, default to operator-smoke (K-b-style)
  posture rather than permanent CI test (K-a-style). The
  one-off live-SDK trace closes mock-vs-prod divergence risk
  empirically; permanent CI is defense-in-depth only.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S31 scope closes,
  transition per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-30:

1. Commit SHA(s) of each Session 31 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 970 baseline → S31 close.
4. Driver suite count (52/52 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (Workstream 0 closed at S27; no further
   workstream-0-* tags. workstream-A milestones depend on W A.2
   completion; W A.1 closed at S22's workstream-a-week1-end).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 30 handoff template. Refill at Session 31 close.
