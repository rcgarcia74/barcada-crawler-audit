# Session Transition Template — Handoff from Session 27 → Session 28

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-27 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 28 invocation prompt:** not yet drafted as of Session 27
close. Per the S20→S21..S26→S27 precedent, prompt-drafting is
operator-commissioned between sessions; the operator decides whether
to commission an S28 prompt or scope one at S28 open. Apply
reviewer-feedback hygiene per the eventual prompt's "Reviewer-
feedback hygiene" section if any pre-S28-open reviewer findings
surface.

Anchors for Session 28 cold start:
- Workspace HEAD: `5aab563` (S27 primary close-out commit:
  SESSION_LOG.md + SESSION_TRANSITION_TEMPLATE.md + LESSONS.md).
  THIS commit (the anchor-pinning follow-up) supersedes it as the
  actual S28 Phase 0 Step 0.1 target. Per S21-S26 LESSONS pattern
  "Workspace HEAD delta tolerance": tolerate N additional
  prompt-drafting / audit-correction commits between sessions;
  verify each is consistent with that pattern before continuing.
  (S26→S27 saw 2 prompt commits; S20→S21 saw 1; S22→S23 saw 2;
  S27→S28 will depend on whether operator commissions a prompt
  before S28 open.)
- Repo HEAD: `a1c5636` (S27 Commit 1 final;
  WA0.W5.X.per-tier-cost-wiring).
- Canonical baseline: **970 tests** (16-path invocation; driver
  sub-suite grew 46 → 52 with the 6 net-new per-tier-wiring tests).
- Narrower baseline (for candidates that don't exercise ADLS test
  paths): **944 tests** (14-path; 970 minus 19 cost_journal_adls
  minus 7 robots_gate_integration).
- Primary recommended scope: none — Workstream 0 fully closes at
  S27 with the workstream-0-end tag at `a1c5636`. S28 picks from
  carry-forwards A/D/E/K (B closed S27, H closed S26, J closed S25).
- Carry-forward candidates: A (barcada-drift; blocked on parquets),
  D (Phase 4 PR-D tooling), E (cassette corpus expansion), K
  (ADLSCostJournal live Azure smoke). PLUS new from S27: Stage 1
  ShardResult LLM-vs-embedding split (would unblock (1,llm) /
  (1,embedding) per-tier slots; deferred for a future src/ scope).

---

## Handoff metadata

- Outgoing session number: 27
- Closing date: 2026-05-26
- Outgoing session scope: per-tier cost-accounting retrofit
  (S27 Candidate B). 1 commit per Q-SHARED.1:
  `a1c5636 WA0.W5.X.per-tier-cost-wiring` (cascade.py +105 / -6;
  test_cost_journal_wiring.py NEW 338 LOC; 964 → 970 combined
  suite; 6 of 8 _TOTALS_FIELDS slots wired; Stage 1 + Stage 3
  fetch stay $0 by design).
  `workstream-0-end` tag PLACED at `a1c5636` with full W0-closure
  annotation (mirrors workstream-a-week1-end pattern). LLM spend:
  $0.
- Reason for transition: S27 1-commit scope completed cleanly;
  Candidate B shipped end-to-end with workstream-0-end milestone
  reached. Phase 1 → Phase 6 in a single context window with no
  HALTs. No in-flight sub-surface.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `a1c5636` (WA0.W5.X.per-tier-cost-wiring).
- Last commit subject: "WA0.W5.X.per-tier-cost-wiring:
  tests/runners/fixture_cascade/cascade.py +
  tests/runners/fixture_cascade/test_cost_journal_wiring.py
  (S27 Candidate B per Q-B.1 Option 1 driver-only scope; 6 of 8
  _TOTALS_FIELDS slots wired from Stage 2/3 ShardResult components;
  Stage 1 (1,llm)/(1,embedding) intentionally $0 pending Stage 1
  ShardResult split; Stage 3 fetch_cost_usd rolls through
  shard.cost_usd lacking (3,'fetch') slot; 964 -> 970 (6 net-new
  tests); single W5.X-prefix bundled commit per Q-B.4;
  LocalFSCostJournal verification per Q-B.6; closes S14
  carry-forward cost-accounting wiring gap)".
- Branch sync with `origin/main`: 0 ahead / 0 behind (verified
  at S27 close after push of `2314f5e..a1c5636`).
- Tags (11 total; NEW S27 = `workstream-0-end`):
  - `pre-remediation-2026-05-19` at `3cbb9b3`
  - `workstream-0-week1-end` at `4f9d23f`
  - `workstream-0-week2-end` at `e5d2f91`
  - `workstream-0-week3-end` at `cf0c14c`
  - `workstream-0-week4-1-5-end` at `dd64963` (annotated)
  - `workstream-0-week4-end` at `b2e2671` (annotated)
  - `workstream-0-week5-end` at `ddd3cb0` (annotated)
  - `baseline-v0` at `9e9a1fb` (annotated)
  - `workstream-0-week7-end` at `ea37102` (annotated)
  - **`workstream-0-end` at `a1c5636` (annotated; NEW S27)**
  - `workstream-a-week1-end` at `fdc8a7a` (annotated; placed S22)
- Pre-push gate state at HEAD `a1c5636`: ALL CHECKS PASS (ruff +
  ruff format on 352 files + vermin 3.10 + validate_consistency
  0/0).
- Pre-S27 unstaged operator territory (Sessions 8-27 precedent —
  expected to stay unstaged across sessions):
  `eval_data/TAXONOMY_GAP_LOG.md`,
  `eval_data/audits/step3_professional_credentials_queue.jsonl`,
  `eval_data/stage1_labels.jsonl`.
  S27 saw NO new operator-side eval_data commits between S26 close
  and S27 open.
- Corpus: 222 .html fixtures (unchanged from S17 close).
- 202 expected.json files (unchanged).
- 222 meta.json files (unchanged).
- 1213 baseline-v0 files (unchanged from S18 close at `9e9a1fb`).
- MODIFIED Session 27 (Commit 1 SHA `a1c5636`):
    - `tests/runners/fixture_cascade/cascade.py` (+105 / -6 LOC):
        - Module docstring extended with "Per-tier cost-accounting
          wiring (WA0.W5.X, S27 Candidate B)" paragraph.
        - New module-level helper `_journal_record_with_breakdown`
          (chained `with_stage_cost_added` + `with_shard_appended`
          in one `update_with_retry` round-trip).
        - Stage 2 invoker replaced (components dict; unattributed
          $0).
        - Stage 3 invoker replaced (components dict; fetch as
          unattributed).
        - Stage 1 invoker unchanged.
    - `tests/runners/fixture_cascade/test_cost_journal_wiring.py`
      NEW 338 LOC; 6 driver-level integration tests (5
      cascade-driven + 1 helper-direct unit test).
- (Unchanged from S26 close, all locked):
    - All S21-S26 deliverables (32 robots tests + 30 robots_gate +
      30 robots_bypass_config + 43 cost_journal + 13
      cost_journal_local + 19 cost_journal_adls + 35
      robots_integration + 74 vmss_worker + 129 job_runner + 152
      worker_loop + 7 robots_gate_integration + 12
      worker_loop_persistence).
    - `cost_journal_adls.py` (S25 full backend at `835a531`).
    - `_open_cost_journal_for_worker` body (S25 abfss:// dispatch
      at `aed7873`).
    - `docs/CRAWLING_POLICY.md` (S26 tightened doc at `2314f5e`;
      77 lines / 2519 bytes).
    - All scraper/orchestrator surfaces locked per Out-of-scope
      list in SESSION_27_PROMPT.md.
- Combined test suite at HEAD `a1c5636`:
    - **970 passed / 0 failed / 0 skipped** with the canonical
      16-path invocation (964 → 970; +6 net-new driver-level
      tests from `test_cost_journal_wiring.py`).
    - **944 passed / 0 failed / 0 skipped** with the narrower
      14-path invocation (canonical minus 19 cost_journal_adls
      minus 7 robots_gate_integration; verified post-push).
    - 480 / 538 / 938 narrower-baselines (S22 / S26 era) remain
      valid for future candidates that don't touch journal or
      orchestrator paths.

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 27 start: `9b6c2d8` (S27 prompt v2
  amendment; 2 commits ahead of `c0458dc` S26-close anchor due to
  prompt-drafting + v1→v2 reviewer-findings audit — matched the
  S20-S26 precedent for prompt-drafting between sessions). At
  Session 27 Phase 0 Step 0.1 this was tolerated under the
  "Workspace HEAD delta tolerance" pattern (both extra commits
  were SESSION_27_PROMPT.md / SESSION_TRANSITION_TEMPLATE.md edits
  only).
- Session 27 close-out workspace commits: 1 (this file's primary
  edit + SESSION_LOG entry + LESSONS S27 fold) + 1 expected
  follow-up pinning the anchor SHA for S28 Phase 0 Step 0.1.
- **Last commit SHA at Session 27 CLOSE: this commit (the
  follow-up pinning the anchor)**. S28 prompt's Phase 0 Step 0.1
  MUST anchor workspace expectation to THIS follow-up's SHA, NOT
  to the primary close-out (which this follow-up succeeds). Per
  S21-S26 LESSONS pattern "Workspace HEAD delta tolerance":
  tolerate N additional prompt-drafting / audit-correction
  commits between sessions; verify each is consistent with that
  pattern before continuing.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected
  after Session 27 close push.

---

## Session 28 execution order (enforce strict sequence)

Same N-phase shape applies regardless of scope choice (Phase 0
cold-start verify → Phase 1 scope → Phase 2 design-gate → Phase 3
impl → Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 28 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 27 entry.
3. Reading the LESSONS.md addition Session 27 landed (1 new
   section at end of file, "S27 folding" suffix).
4. Reading the relevant section of BARCADA_CRAWLER_
   REMEDIATION_PLAN.md for the chosen Session 28 scope (see
   "Notes for Session 28" below).
5. Reading the Session 28 prompt if one has been drafted, OR
   commissioning a fresh draft at S28 open.
6. Running Phase 0 cold-start verification per the prompt's
   protocol (or per the S27 prompt template if S28 prompt is
   not yet drafted; mirror the S27 Phase 0 9-step verification
   shape, updating workspace HEAD anchor, repo HEAD anchor
   (`a1c5636`), and canonical baseline (970)).

---

## Outstanding operator-input requests entering Session 28

1. **Session 28 scope choice** — pick from the candidates in
   "Notes for Session 28" below. Candidate B closed at S27; the
   carry-forwards (A/D/E/K) remain, plus the new S27-deferred
   Stage 1 ShardResult split.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*.jsonl` continue across sessions (Sessions 8-27
   precedent). S27 saw NO operator-side eval_data commits between
   S26 close and S27 open. validate_consistency stayed green
   throughout S27.

3. **barcada-drift AI/ML alignment** — unchanged from S21-S27
   handoffs. If operator wants to ship `barcada-drift` in S28,
   the 4 AI/ML team decisions need to be pre-resolved OR scoped
   narrowly with placeholders. Plus the prereq of 2+ parquet
   files (earliest natural date 2026-06-06 if the launchd
   installer fired immediately after S20 close).

4. **launchd kit installation** — unchanged. Operator should
   run `scripts/launchd/install_canary_schedule.sh` when ready
   to enable the weekly Saturday-9am canary job. Required
   prerequisite for Candidate A.

5. **Session 28 prompt draft commissioning** — operator decides
   whether to commission an S28 prompt between sessions or scope
   one at S28 open.

6. **Live Azure smoke for ADLSCostJournal** (Candidate K;
   carry-forward from S25→S26→S27) — S25 shipped ADLSCostJournal
   tested against DummyBlobBackend in-memory. The production
   code path against real Azure / Azurite has never been
   exercised.

---

## Notes for Session 28

Suggested S28 scope candidates (operator picks at S28 open):

### Candidate A (carry-forward): `barcada-drift` skeleton

Unchanged from S21-S27 handoffs. Per CLASSIFICATION_ADJACENT_PLAN.md
§Item 8. Consumes `canary_runs/<date>.parquet` artifacts.
**Blocked**: 2+ parquet files needed (launchd installer not yet
run as of S27 close; earliest natural date 2026-06-06 if installed
post-S20-close).  Estimated ~300 LOC.

### Candidate D (carry-forward): Phase 4 PR-D operator-led labeling

Unchanged. Tooling support only; labeling itself is operator
territory.

### Candidate E (carry-forward): Cassette corpus expansion

Unchanged from S22-S27 handoffs. S20 shipped 20 cassettes; plan's
upper bound is 30. Could expand or curate. Optional FP
re-investigation of archive.org / hashicorp.com / stripe.com.

### Candidate K (carry-forward from S25): ADLSCostJournal live smoke

Optional operator-driven smoke against real Azure / Azurite to
close the mock-vs-prod divergence risk for the S25-shipped
ADLSCostJournal backend. Two flavors:
- **K-a: Azurite container** — Docker-backed integration test
  (~50-100 LOC + Docker setup).
- **K-b: Operator-driven sandbox smoke** — ~30 LOC Python
  script; no CI integration.

### NEW S27-deferred: Stage 1 ShardResult LLM-vs-embedding split

Would let `(1, 'llm')` / `(1, 'embedding')` per-tier slots in
`cost_journal._TOTALS_FIELDS` populate from real Stage 1 costs.
Currently `stage1_run.ShardResult` exposes only an aggregate
`cost_usd` with no LLM-vs-embedding breakdown, so the S27
retrofit left those two slots at $0. Closing this would touch
`src/barcada_scraper/classifier/stage1/run.py` and
`stage1/cost_tracker.py` (src/ scope — requires Phase 2 design-
gate authorization for additive src/ touch).  Estimated ~80-100
LOC. Tag implication: NONE (no workstream milestone left after
workstream-0-end).

---

## Required reading (Session 28 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 27 entry — 1-commit narrative;
   Q-B.1 through Q-B.6 + Q-SHARED.1 decisions; the closed S14
   carry-forward; the new workstream-0-end tag annotation.
3. **`LESSONS.md`** — 1 new section appended at S27 close
   ("S27 folding" suffix): "Deferred wiring gaps fold cleanly
   into workstream-end if the original implementation left a
   parallel-API seam".
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope
   section per Session 28 candidate choice. Plan is READ-ONLY.
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A (barcada-drift) is chosen.
6. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   — only if Candidate K touches the ADLS backend.
7. **`tests/runners/fixture_cascade/cascade.py`** at S27 HEAD —
   only if Stage 1 ShardResult split candidate is chosen
   (cascade.py's docstring documents exactly which slots remain
   at $0 and why).
8. **`docs/CRAWLING_POLICY.md`** at S26 SHA `2314f5e` — only if
   operator wants to review the S26-tightened version (77 lines
   / 2.52 KB). Locked.

---

## Outstanding items carried forward to Session 28+

1. **Per-tier cost-accounting wiring gap** — CLOSED at S27 for
   6 of 8 _TOTALS_FIELDS slots. The remaining 2 slots
   (`stage1_llm_usd`, `stage1_embedding_usd`) stay $0 by design
   pending Stage 1 ShardResult split (see Candidate "Stage 1
   ShardResult split" above).

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

6. **Phase 4 PR-D/E/F/G** (forward look) — opens now that
   Workstream 0 fully closes (workstream-0-end tag at `a1c5636`).
   Operator-led Stage 2 + Stage 3 labeling work still needs to
   begin before PR-D/E/F/G work can land.

7. **CRAWLING_POLICY.md size** — CLOSED at S26 (2.52 KB).

8. **abfss:// CostJournal Phase 5 promotion** — CLOSED at S25.

9. **Live Azure smoke for ADLSCostJournal** (Candidate K) —
   carry-forward from S25→S26→S27. Optional; not a session-scope
   blocker.

10. **Stage 1 ShardResult LLM-vs-embedding split** (NEW S27
    deferral) — would close the remaining 2 of 8 _TOTALS_FIELDS
    slots. src/ scope; needs Phase 2 design-gate authorization.

---

## Locked artifact reminders for Session 28

Carry-forward from Sessions 8-27 (additions for S27 marked NEW):

- `eval_data/` — labeling-workstream territory. Operator-WIP
  edits across sessions are expected. Pre-push validate_
  consistency runs against WT state; surface per LESSONS pattern
  if blocked.
- `stage1.schema.json` v1.0 with 49 keywords.
- `pre-remediation-2026-05-19` tag.
- `baseline-v0` tag at `9e9a1fb`.
- All `workstream-0-*-end` tags at their placed SHAs.
- **NEW S27 LOCK**: `workstream-0-end` tag at `a1c5636`
  (annotated). Do NOT move.
- `workstream-a-week1-end` tag at `fdc8a7a` (placed S22).
- `tests/runners/fixture_cascade/` — W4.1.5 driver area; locked
  at `dd64963` except via W5.X-prefix commits. **NEW S27
  ADDITION**: `cascade.py` modified at SHA `a1c5636` under
  W5.X-prefix authorization for the per-tier cost-accounting
  retrofit (2nd W5.X commit in the driver area; 1st was Session
  16's `8d0fc0e`). The new
  `_journal_record_with_breakdown` helper and the Stage 2/3
  invoker pattern are locked at `a1c5636`; further modifications
  require Phase 2 design-gate authorization. Stage 1's invoker
  intentionally unchanged.
- **NEW S27 LOCK**:
  `tests/runners/fixture_cascade/test_cost_journal_wiring.py`
  — S27 deliverable; locked at `a1c5636`. 6 tests (5 cascade-
  driven + 1 helper-direct unit test).
- `tests/fixtures/baseline-v0/` snapshot — locked at `9e9a1fb`.
- `tools/baseline_v0/check.py`, `generate.py`, `determinism.py`,
  `canary.py` — S18-20 deliverables; locked.
- `tools/synthetic_crawl/` package — S20 deliverable; locked.
- `tests/fixtures/synthetic_crawls/` — S20 corpus; locked.
- `scripts/launchd/` — S20 deliverable; locked.
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
  S22-extended at `1d9404e`; S25 Q-J.8 extension touched ONLY
  the test file; production file unchanged. S27 consumed the
  existing public API (`with_stage_cost_added`,
  `with_shard_appended`, `update_with_retry`) without
  modification.
- `src/barcada_scraper/classifier/pipeline/cost_journal_local.py`
  — production local-FS backend; locked.
- `src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
  — full backend shipped at S25 SHA `835a531`. Public API:
  `ADLSCostJournal(journal_dir, run_id, credential=None,
  blob_backend=None)` with read / write_initial / try_update /
  exists / path. Locked.
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
- Production code under `src/barcada_scraper/` — locked unless
  Phase 2 design-gate explicitly authorizes a specific module.
  S21+S22+S23+S24+S25 authorized: `scraper/robots.py`,
  `scraper/robots_gate.py`, `scraper/robots_bypass_config.py`,
  `classifier/pipeline/cost_journal.py` (additive only),
  `classifier/pipeline/cost_journal_adls.py` (S25 skeleton →
  full backend),
  `orchestrator/robots_integration.py` (new),
  `orchestrator/vmss_worker.py` (additive),
  `orchestrator/job_runner.py` (additive),
  `orchestrator/worker_loop.py` (additive: S23 gate wiring +
  S24 durable persistence helpers + S25 abfss:// guard removal
  in 1 helper body). S26 added no new src/ authorizations
  (doc-only). S27 added no new src/ authorizations
  (driver-only, W5.X-prefix).
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-28-open baseline

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

Sub-totals: 210 conformance + 52 driver + 99 baseline_v0 + 33
synthetic_crawl + 32 robots + 30 robots_gate + 30 robots_bypass_config
+ 43 cost_journal + 13 cost_journal_local + 19 cost_journal_adls +
35 robots_integration + 74 vmss_worker + 129 job_runner + 152
worker_loop + 7 robots_gate_integration + 12 worker_loop_persistence
= 970. (Only the driver sub-suite changed S26 → S27: 46 → 52; all
15 other counts unchanged.)

Cumulative-test-count gate: the count NEVER decreases between
commit boundaries.

Narrower baselines (still valid for S28 candidates that don't
exercise the new ADLS test paths):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 938 (S26 narrower 14-path; no longer applicable after S27 since
  driver suite grew — replaced by 944)
- 944 (S27-equivalent narrower; canonical 16-path minus 19
  cost_journal_adls minus 7 robots_gate_integration; verified
  post-S27-push)

Choose at Phase 0 Step 0.5 per Candidate selection.

---

## Pre-push gate at Session 28 open

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 352+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

Note on gate 4: validate_consistency runs against working-tree
state; if operator-WIP in eval_data introduces a schema violation
between S27 close and S28 open, the gate will block even though
no S28 commit touches eval_data. Per LESSONS: surface to operator
with the row+detail, propose operator-fix or stash-and-restore;
do NOT auto-fix.

---

## Context-window awareness

Session 27 ran across 1 commit + Phase 2 source-verification +
Phase 6 close-out, comfortably within context. No HALTs, no
mid-Phase-3 extensions. Session 28 budget per chosen candidate:

- Candidate A (barcada-drift): only if launchd job has run ≥2
  times AND AI/ML decisions ready. Estimated ~300 LOC.
- Candidate D (Phase 4 PR-D tooling): operator-led; tooling only.
- Candidate E (cassette corpus expansion): depends on operator
  curation choices.
- Candidate K (ADLSCostJournal live smoke): K-a ~50-100 LOC +
  Docker; K-b ~30 LOC operator-driven.
- Stage 1 ShardResult split (NEW S27 deferral): ~80-100 LOC;
  touches src/stage1/. Needs Phase 2 src/ authorization.

Strategies (unchanged from S20-S27 prompts):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-HTTP corpus work, pilot 1-3 before full N-domain.
- Source-verify line numbers per Phase 3 commit, not just at
  Phase 2 (S23 LESSONS pattern).
- Test against public API surface only — probe `.path` /
  behavior, not private attrs (S24 LESSONS pattern).
- Source-verify facts behind option-set design BEFORE
  AskUserQuestion drafts (S25 LESSONS pattern).
- Grep for same-shape tests outside the prompt's explicit
  allowlist at Phase 0 (S25 LESSONS Q-J.8 extension lesson).
- At Phase 2, count the prompt's Q-* option set; if any single
  Q-* enumerates >4 options, tier the question or split the
  AskUserQuestion call rather than silently narrowing (S26
  LESSONS pattern).
- **NEW S27 LESSONS**: when deferring a low-severity wiring gap,
  document the specific parallel-API seam that will close it
  later. The S14 → S27 deferred-to-closed cycle worked because
  the original cost_journal API shipped both rollup and
  per-component modes as a deliberately two-mode design. Without
  the seam, "defer" silently becomes "src/-surgery later".

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S28 scope closes,
  transition per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-27:

1. Commit SHA(s) of each Session 28 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 970 baseline → S28 close.
4. Driver suite count (52/52 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (Workstream 0 closed at S27 — no further
   workstream-0-* tags. workstream-A milestones depend on W A.2
   completion; W A.1 closed at S22's workstream-a-week1-end).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 27 handoff template. Refill at Session 28 close
per Phase 6 close-out protocol.
