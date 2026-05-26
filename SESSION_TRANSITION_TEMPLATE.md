# Session Transition Template — Handoff from Session 29 → Session 30

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-29 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 30 invocation prompt:** not yet drafted. Per S20→S21..
S28→S29 precedent, prompt-drafting is operator-commissioned
between sessions — not always-on close-out work. Either commission
an S30 prompt between sessions or scope one at S30 open. The
S29 prompt's Phase 6 note explicitly authorizes either option.

Anchors for Session 30 cold start:
- Workspace HEAD: THIS commit (the anchor-pinning follow-up,
  succeeding S29 primary close-out `0708a53`). S30 Phase 0
  Step 0.1 MUST anchor workspace expectation to THIS follow-up's
  SHA. Per S21-S28 LESSONS pattern "Workspace HEAD delta
  tolerance": tolerate N additional prompt-drafting / audit-
  correction commits between sessions; verify each is consistent
  with that pattern before continuing.
- Repo HEAD: `75a3937` (S29 K-b commit;
  WA2.W8.adls-live-smoke). Tolerated delta: operator-side
  eval_data labeling commits between S29 close and S30 open
  (Sessions 8-29 precedent).
- Canonical baseline: **970 tests** (16-path invocation;
  unchanged from S27/S28 close — S29's K-b ship is a new script
  under `scripts/`, NOT a test).
- Narrower baseline (for candidates that don't exercise ADLS test
  paths): **944 tests** (14-path; 970 minus 19 cost_journal_adls
  minus 7 robots_gate_integration). Unchanged from S27/S28 close.
- Primary recommended scope: none — no single carry-forward is
  blocking. S30 picks from carry-forwards A/D/E/K-a/K-b-exec
  (B closed S27, H closed S26, J closed S25, StgSplit closed S28,
  K-b-ship closed S29; K-b-EXECUTION against real Azure is the
  new operator-runnable carry-forward).
- Carry-forward candidates: A (barcada-drift; blocked on
  parquets + AI/ML), D (Phase 4 PR-D tooling), E (cassette corpus
  expansion), K-b-exec (script shipped S29 — operator runs it
  ad-hoc when Azure sandbox is available), K-a (Azurite-backed
  permanent CI test; still not shipped).

---

## Handoff metadata

- Outgoing session number: 29
- Closing date: 2026-05-26
- Outgoing session scope: ADLSCostJournal live Azure smoke
  (S29 Candidate K-b). 1 commit per Q-SHARED.1 = trivially
  per-module: `75a3937 WA2.W8.adls-live-smoke`. New file
  `scripts/smoke_test_adls_cost_journal.py` (220 LOC including
  Copyright header + docstring). NO src/ changes. NO test-suite
  changes. LLM spend: $0 (script not executed against real Azure
  during the session).
- Reason for transition: S29 single-commit scope completed
  cleanly; Candidate K-b shipped end-to-end. Phase 1 → Phase 6
  in a single context window with no HALTs. No in-flight
  sub-surface.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `75a3937` (WA2.W8.adls-live-smoke).
- Last commit subject: "WA2.W8.adls-live-smoke:
  scripts/smoke_test_adls_cost_journal.py (S29 Candidate K-b
  per Q-K.b.1 Option 1 + Q-K.b.2 Option 1 + Q-K.b.3 Option 1 +
  Q-K.b.4 Option 1; new operator-driven manual smoke script
  exercising the full 5-step ETag-conflict matrix against a live
  Azure container; ...)".
- Branch sync with `origin/main`: 0 ahead / 0 behind (verified
  at S29 close after push of `d4f06b8..75a3937`).
- Tags (11 total; unchanged from S27/S28 close):
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
- Pre-push gate state at HEAD `75a3937`: ALL CHECKS PASS (ruff +
  ruff format on 353 files + vermin 3.10 + validate_consistency
  0/0).
- Pre-S29 unstaged operator territory (Sessions 8-29 precedent —
  expected to stay unstaged across sessions):
  `eval_data/*.jsonl` operator-WIP edits (no specific files
  pinned here; verify via `git status` at S30 open).
  S29 saw 2 tolerated operator-side eval_data commits between
  S28 close (`ae9e627`) and S29 open (`d4f06b8`): `f1802ab`
  (Step 3 audit of professional_credentials) and `d4f06b8`
  (Step 3 audit + service_area patches). Both strictly
  `eval_data/*` per `git show --stat`.
- Corpus: 222 .html fixtures (unchanged from S17 close).
- 202 expected.json files (unchanged).
- 222 meta.json files (unchanged).
- 1213 baseline-v0 files (unchanged from S18 close at `9e9a1fb`).
- MODIFIED Session 29 (1 commit):
    - **`75a3937`**:
        - `scripts/smoke_test_adls_cost_journal.py` (NEW +220/0):
          operator-driven 5-step ETag-conflict-matrix smoke
          script. NEW under `scripts/` (NOT in the locked
          `scripts/launchd/` subdir). Mirrors
          `scripts/smoke_test_adls_gen2.py` conventions.
- (Unchanged from S28 close, all locked):
    - All S21-S26+S28 deliverables (32 robots tests + 30
      robots_gate + 30 robots_bypass_config + 43 cost_journal +
      13 cost_journal_local + 19 cost_journal_adls + 35
      robots_integration + 74 vmss_worker + 129 job_runner + 152
      worker_loop + 7 robots_gate_integration + 12
      worker_loop_persistence + 16 stage1 run_cascade + 16
      stage1 cost_tracker).
    - `cost_journal_adls.py` (S25 full backend at `835a531`).
    - `_open_cost_journal_for_worker` body (S25 abfss:// dispatch
      at `aed7873`).
    - `docs/CRAWLING_POLICY.md` (S26 tightened doc at `2314f5e`;
      77 lines / 2519 bytes).
    - S27+S28 deliverables (cascade.py per-tier wiring at
      `a1c5636` + Stage 1 invoker switch at `9afde57`;
      test_cost_journal_wiring.py at `a1c5636` + 1↔1
      replacement at `ae9e627`; ShardResult split at `776d203`).
    - All scraper/orchestrator surfaces locked per Out-of-scope
      list in SESSION_29_PROMPT.md.
- Combined test suite at HEAD `75a3937`:
    - **970 passed / 0 failed / 0 skipped** with the canonical
      16-path invocation (unchanged from S27/S28 close; S29's
      K-b ship is a new script, not a test).
    - **944 passed / 0 failed / 0 skipped** with the narrower
      14-path invocation (unchanged from S27/S28 close).
    - **Stage 1 test counts**: 32 (16 test_run_cascade + 16
      test_cost_tracker) — unchanged from S28 close. Outside
      the canonical 16-path invocation.

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 29 start: `586df7c` (2 prompt-
  finalization commits ahead of the S28 close anchor `3089faa`:
  `ff779aa` S29 prompt drafted + `586df7c` S29 prompt revision
  per reviewer feedback). At S29 Phase 0 Step 0.1 both were
  tolerated under the "Workspace HEAD delta tolerance" pattern
  (both were prompt-only edits).
- Session 29 close-out workspace commits: 2 (primary close-out
  `0708a53`: SESSION_LOG.md + SESSION_TRANSITION_TEMPLATE.md +
  LESSONS.md; THIS follow-up pinning the anchor SHA for S30
  Phase 0 Step 0.1).
- **Last commit SHA at Session 29 CLOSE: this commit (the
  follow-up pinning the anchor; succeeds `0708a53`)**. S30
  prompt's Phase 0 Step 0.1 MUST anchor workspace expectation
  to THIS follow-up's SHA. Per S21-S28 LESSONS pattern
  "Workspace HEAD delta tolerance": tolerate N additional
  prompt-drafting / audit-correction commits between sessions;
  verify each is consistent with that pattern before continuing.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected
  after Session 29 close push.

---

## Session 30 execution order (enforce strict sequence)

Same N-phase shape applies regardless of scope choice (Phase 0
cold-start verify → Phase 1 scope → Phase 2 design-gate → Phase 3
impl → Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 30 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 29 entry.
3. Reading the LESSONS.md additions Session 29 landed (2 new
   sections at end of file, "S29 folding" suffix).
4. Reading the relevant section of BARCADA_CRAWLER_
   REMEDIATION_PLAN.md for the chosen Session 30 scope (see
   "Notes for Session 30" below).
5. Reading the Session 30 prompt if one has been drafted, OR
   commissioning a fresh draft at S30 open.
6. Running Phase 0 cold-start verification per the prompt's
   protocol (or per the S29 prompt template if S30 prompt is
   not yet drafted; mirror the S29 Phase 0 9-step verification
   shape, updating workspace HEAD anchor, repo HEAD anchor
   (`75a3937`), and canonical baseline (970)).

---

## Outstanding operator-input requests entering Session 30

1. **Session 30 scope choice** — pick from the candidates in
   "Notes for Session 30" below. Candidate K-b (script ship)
   closed at S29; the carry-forwards (A/D/E/K-a/K-b-exec)
   remain. No new carry-forward introduced by S29.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*.jsonl` continue across sessions (Sessions 8-29
   precedent). S29 saw 2 operator-side eval_data commits between
   S28 close (`ae9e627`) and S29 open (`d4f06b8`):
   `f1802ab` + `d4f06b8`. validate_consistency stayed green
   throughout S29 (no transient first-run errors this session;
   the S28 curiosity did not reproduce).

3. **barcada-drift AI/ML alignment** — unchanged from S21-S29
   handoffs. If operator wants to ship `barcada-drift` in S30,
   the 4 AI/ML team decisions need to be pre-resolved OR scoped
   narrowly with placeholders. Plus the prereq of 2+ parquet
   files (earliest natural date 2026-06-06 if the launchd
   installer fires immediately after S29 close).

4. **launchd kit installation** — unchanged. Operator should
   run `scripts/launchd/install_canary_schedule.sh` when ready
   to enable the weekly Saturday-9am canary job. Required
   prerequisite for Candidate A. **As of S29 close, NOT yet
   installed** (verified via `~/Library/LaunchAgents/` check
   during Phase 1 prerequisite audit).

5. **Session 30 prompt draft commissioning** — operator decides
   whether to commission an S30 prompt between sessions or scope
   one at S30 open.

6. **Live Azure smoke for ADLSCostJournal EXECUTION** (S29's
   K-b carry-forward) — script shipped at S29
   (`scripts/smoke_test_adls_cost_journal.py`); not yet
   executed against real Azure. Operator runs it ad-hoc when
   an Azure sandbox container is available; trace + any
   divergence from DummyBlobBackend behavior should be captured
   in SESSION_LOG.md / LESSONS.md.

---

## Notes for Session 30

Suggested S30 scope candidates (operator picks at S30 open):

### Candidate A (carry-forward): `barcada-drift` skeleton

Unchanged from S21-S29 handoffs. Per
CLASSIFICATION_ADJACENT_PLAN.md §Item 8. Consumes
`canary_runs/<date>.parquet` artifacts. **Blocked**: 2+ parquet
files needed AND 4 AI/ML decisions (or placeholders). As of S29
close: launchd installer not yet run; 0 parquets on disk; no
AI/ML responses in workspace. Earliest natural date 2026-06-06.
Estimated ~300 LOC (apply the S29-folded LESSONS "Operator-
driven script LOC estimates run ~3× higher than logic-only
estimates" pattern if a fresh estimate is needed at S30 open).

### Candidate D (carry-forward): Phase 4 PR-D operator-led labeling

Unchanged. Tooling support only; labeling itself is operator
territory. W0 is closed (workstream-0-end at `a1c5636` placed
S27); Phase 4 PR-D/E/F/G work is W0-side unblocked. Still gated
on operator-led Stage 2/3 labeling start.

### Candidate E (carry-forward): Cassette corpus expansion

Unchanged from S22-S29 handoffs. S20 shipped 20 cassettes; plan's
upper bound is 30. Could expand or curate. Optional FP
re-investigation of archive.org / hashicorp.com / stripe.com.

### Candidate K-a (carry-forward): Azurite-backed integration test

Optional permanent CI safety net for ADLSCostJournal. Not chosen
at S29 (K-b was chosen instead). Still available: Docker-backed
integration test (~50-100 LOC + Docker setup); would add a 17th
path to the canonical invocation per Q-K.5 = Option 2.

### Candidate K-b-exec (NEW S29 carry-forward): Live smoke EXECUTION

**Carry-forward bound to operator availability of an Azure
sandbox, NOT to a session.** The S29 K-b script ships at
`scripts/smoke_test_adls_cost_journal.py` and is operator-
runnable when:

```bash
export AZURE_STORAGE_ACCOUNT="<your-account>"
export AZURE_STORAGE_CONTAINER="<your-container>"
az login   # or set AZURE_STORAGE_KEY
python scripts/smoke_test_adls_cost_journal.py
```

Expected output: 5-step `[N/5]` trace, then `"All 5 steps OK.
ADLSCostJournal behavior matches DummyBlobBackend."`, then
`"Deleted abfss://..."`. If any step diverges (e.g., a 412
mapping fires differently from `DummyBlobBackend`), paste the
trace into SESSION_LOG.md + LESSONS.md and consider an S30
follow-up to either fix the divergence in
`cost_journal_adls.py` or update the script.

---

## Required reading (Session 30 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 29 entry — single-commit
   narrative; Q-K.b.1 through Q-K.b.4 + Sub-question 1.TAG
   decisions; the empirical Phase 1 prerequisite check for
   Candidate A (0 parquets / no plist / no AI/ML responses);
   the public-API-only cleanup pattern surfaced.
3. **`LESSONS.md`** — 2 new sections appended at S29 close:
   - "Operator-driven script LOC estimates run ~3× higher than
     logic-only estimates" (S29 folding; LOC-budgeting accuracy
     for future operator-script estimates).
   - "Public-API-only cleanup pattern extends from tests to
     operator scripts" (S29 folding; extends S24 pattern).
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope
   section per Session 30 candidate choice. Plan is READ-ONLY.
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A (barcada-drift) is chosen.
6. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   — only if Candidate K-a is chosen (Azurite-backed test).
7. **`scripts/smoke_test_adls_cost_journal.py`** at S29 SHA
   `75a3937` — for reference if Candidate K-a is chosen (the
   K-b script's structure informs the K-a test layout) OR if
   Candidate K-b-exec surfaces a divergence requiring follow-up.
8. **`docs/CRAWLING_POLICY.md`** at S26 SHA `2314f5e` — only if
   operator wants to review the S26-tightened version (77 lines
   / 2.52 KB). Locked.

---

## Outstanding items carried forward to Session 30+

1. **Per-tier cost-accounting wiring** — CLOSED end-to-end S28.
   All 8 `_TOTALS_FIELDS` slots wired. Unchanged at S29 (no
   driver-area or cascade changes).

2. **`barcada-drift` CLI** — CLASSIFICATION_ADJACENT_PLAN.md
   §Item 8; 4 AI/ML team decisions outstanding. Blocked also
   on 2+ canary_runs parquet files. Unchanged. **S29 confirmed
   empirically** that launchd installer has NOT been run as of
   S29 close (no plist in `~/Library/LaunchAgents/`).

3. **Cassette corpus expansion** — current 20 domains is lower
   bound of plan's "~20-30". Unchanged.

4. **Cassette-FP investigation** — archive.org + hashicorp.com
   flagged as SaaS-shell FPs in S20's FP-curation log. Unchanged.

5. **launchd kit smoke-then-install** — Unchanged. Operator
   should run `scripts/launchd/install_canary_schedule.sh` to
   enable the weekly job. Required for Candidate A.

6. **Phase 4 PR-D/E/F/G** (forward look) — W0-side unblocked
   since S27 (workstream-0-end at `a1c5636`). Operator-led
   Stage 2 + Stage 3 labeling work still needs to begin before
   PR-D/E/F/G work can land.

7. **CRAWLING_POLICY.md size** — CLOSED at S26 (2.52 KB).

8. **abfss:// CostJournal Phase 5 promotion** — CLOSED at S25.

9. **Live Azure smoke for ADLSCostJournal SCRIPT** — CLOSED at
   S29 (Candidate K-b script ship). Script at
   `scripts/smoke_test_adls_cost_journal.py`.

10. **Stage 1 ShardResult LLM-vs-embedding split** — CLOSED S28
    (Candidate StgSplit).

11. **Live Azure smoke for ADLSCostJournal EXECUTION** (NEW S29
    carry-forward) — bound to operator availability of Azure
    sandbox, NOT to a session. Run ad-hoc via the K-b script.

12. **Azurite-backed CI test for ADLSCostJournal** (Candidate
    K-a) — still carry-forward; not shipped at S29 (K-b was
    chosen instead).

---

## Locked artifact reminders for Session 30

Carry-forward from Sessions 8-29 (additions for S29 marked NEW):

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
- `tests/runners/fixture_cascade/` — W4.1.5 driver area; locked
  at `dd64963` except via W5.X-prefix commits. S27 modifications
  at `a1c5636` and S28 modifications at `9afde57` + `ae9e627`
  are LOCKED. S29 did NOT touch this surface.
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
  S22-extended at `1d9404e`. S27 + S28 + S29 consumed the
  existing public API without modification.
- `src/barcada_scraper/classifier/pipeline/cost_journal_local.py`
  — production local-FS backend; locked.
- `src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
  — full backend shipped at S25 SHA `835a531`. Public API:
  `ADLSCostJournal(journal_dir, run_id, credential=None,
  blob_backend=None)` with read / write_initial / try_update /
  exists / path. Locked. **S29 CONSUMED this API in the K-b
  script without modification.**
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
  `aed7873` per Q-J.4 abfss:// dispatch; signature locked),
  `_ensure_journal_initialized` (locked at S24 SHA `48c324a`),
  `_build_durable_bypass_writer` (locked at S24 SHA `48c324a`).
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
- S28 LOCKS (unchanged at S29 close):
  - `src/barcada_scraper/classifier/stage1/run.py` —
    `ShardResult` adds `llm_cost_usd` + `embedding_cost_usd`
    (S28 SHA `776d203`).
  - `tests/classifier/stage1/test_run_cascade.py` — +1 net-new
    test at S28 SHA `776d203`.
- **NEW S29 LOCK**:
  - `scripts/smoke_test_adls_cost_journal.py` at S29 SHA
    `75a3937` (220 LOC). Operator-driven 5-step ETag-conflict-
    matrix smoke. Mirrors `scripts/smoke_test_adls_gen2.py`
    conventions. LOCKED — further modifications to the script
    require Phase 2 design-gate authorization at the session
    that proposes them. Adjacent files (other `scripts/smoke_*`
    siblings) are NOT locked.
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
  `classifier/stage1/run.py` (S28 additive: ShardResult +2 fields
  + _build_shard_result populate). S26 + S27 + **S29** added no
  new src/ authorizations.
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-30-open baseline

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

Sub-totals identical to S27/S28 close: 210 conformance + 52
driver + 99 baseline_v0 + 33 synthetic_crawl + 32 robots + 30
robots_gate + 30 robots_bypass_config + 43 cost_journal + 13
cost_journal_local + 19 cost_journal_adls + 35 robots_integration
+ 74 vmss_worker + 129 job_runner + 152 worker_loop + 7
robots_gate_integration + 12 worker_loop_persistence = 970.
(S29's K-b ship is a new script under `scripts/`, NOT a test —
the canonical 16-path count is unchanged.)

Cumulative-test-count gate: the count NEVER decreases between
commit boundaries.

Narrower baselines (still valid for S30 candidates that don't
exercise the new ADLS test paths):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 944 (S27/S28/S29-equivalent narrower; canonical 16-path minus
  19 cost_journal_adls minus 7 robots_gate_integration;
  verified post-S29-push)

Choose at Phase 0 Step 0.5 per Candidate selection.

---

## Pre-push gate at Session 30 open

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
between S29 close and S30 open, the gate will block even though
no S30 commit touches eval_data. Per LESSONS: surface to operator
with the row+detail, propose operator-fix or stash-and-restore;
do NOT auto-fix.

S29 did NOT reproduce the S28 transient "1 error" curiosity —
the gate ran clean on first invocation at both the per-commit
checkpoint and the Phase 4 whole-tree check. LESSONS-worthy if
the transient reproduces in S30+.

---

## Context-window awareness

Session 29 ran across 1 commit + Phase 2 source-verification +
Phase 6 close-out, comfortably within context. No HALTs, no
mid-Phase-3 extensions. Session 30 budget per chosen candidate:

- Candidate A (barcada-drift): only if launchd job has run ≥2
  times AND AI/ML decisions ready. Estimated ~300 LOC logic =
  ~900 LOC delivered per the S29 LESSONS overhead factor.
- Candidate D (Phase 4 PR-D tooling): operator-led; tooling only.
- Candidate E (cassette corpus expansion): depends on operator
  curation choices.
- Candidate K-a (Azurite-backed integration test): ~50-100 LOC
  logic = ~150-300 LOC delivered + Docker setup.
- Candidate K-b-exec (run the S29 script): no new code; carry-
  forward bound to operator running the script ad-hoc.

Strategies (unchanged from S20-S29 prompts):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-HTTP corpus work, pilot 1-3 before full N-domain.
- Source-verify line numbers per Phase 3 commit, not just at
  Phase 2 (S23 LESSONS pattern).
- Test against public API surface only — probe `.path` /
  behavior, not private attrs (S24 LESSONS pattern; S29 extended
  the same pattern to operator scripts via the
  parallel-SDK-client cleanup approach).
- Source-verify facts behind option-set design BEFORE
  AskUserQuestion drafts (S25 LESSONS pattern; S28 + S29
  demonstrated this directly).
- Grep for same-shape tests outside the prompt's explicit
  allowlist at Phase 0 (S25 LESSONS Q-J.8 extension lesson).
- At Phase 2, count the prompt's Q-* option set; if any single
  Q-* enumerates >4 options, tier the question or split the
  AskUserQuestion call rather than silently narrowing (S26
  LESSONS pattern).
- When deferring a low-severity wiring gap, document the specific
  parallel-API seam that will close it later (S27 LESSONS
  pattern).
- At retrofit time, audit existing test pins for "by design" vs
  "empirically true" distinction (S28 LESSONS pattern).
- Phase 0 fixture-count commands need `2>/dev/null` + a bounded
  timeout — use the Python `rglob()` pattern (S28 post-close
  LESSONS pattern).
- **NEW S29 LESSONS**:
  - When sizing operator-driven Python script deliverables in
    this codebase, multiply the "core logic" LOC estimate by
    ~3× for honest total-LOC sizing. Copyright + docstring +
    argparse alone are ~50 LOC of overhead before any logic.
  - When an operator-driven script needs an operation a wrapper
    class doesn't expose, construct a parallel SDK client
    rather than reach into private attrs. Same auth, same URL,
    no private-attr coupling.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S30 scope closes,
  transition per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-29:

1. Commit SHA(s) of each Session 30 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 970 baseline → S30 close.
4. Driver suite count (52/52 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (Workstream 0 closed at S27; no further
   workstream-0-* tags. workstream-A milestones depend on W A.2
   completion; W A.1 closed at S22's workstream-a-week1-end).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 29 handoff template. Refill at Session 30 close
per Phase 6 close-out protocol.
