# Session Transition Template — Handoff from Session 28 → Session 29

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-28 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 29 invocation prompt:** not yet drafted at S28 close.
Per S20→S21..S26→S27→S28 precedent, prompt-drafting is operator-
commissioned between sessions. If operator commissions one, mirror
the S20-S28 7-phase structure (Phase 0 cold-start verify → Phase 1
scope → Phase 2 design-gate → Phase 3 impl → Phase 4 pre-push →
Phase 5 push+tag → Phase 6 close-out) with halt-on-mismatch at
every phase.

Anchors for Session 29 cold start:
- Workspace HEAD: THIS commit (the anchor-pinning follow-up,
  succeeding `2bb5879` S28 primary close-out). S29 Phase 0
  Step 0.1 MUST anchor workspace expectation to THIS follow-up's
  SHA. Per S21-S27 LESSONS pattern "Workspace HEAD delta
  tolerance": tolerate N additional prompt-drafting / audit-
  correction commits between sessions; verify each is consistent
  with that pattern before continuing.
- Repo HEAD: `ae9e627` (S28 Commit 3 final;
  WA0.W5.X.stage1-cost-split-wiring-test).
- Canonical baseline: **970 tests** (16-path invocation; unchanged
  from S27 close — S28's 1↔1 replacement was net-zero on the
  canonical count, and S28's +1 net-new test is in
  tests/classifier/stage1/ which is OUTSIDE the canonical 16-path
  invocation).
- Narrower baseline (for candidates that don't exercise ADLS test
  paths): **944 tests** (14-path; 970 minus 19 cost_journal_adls
  minus 7 robots_gate_integration). Unchanged from S27 close.
- Primary recommended scope: none — no single carry-forward is
  blocking. S29 picks from carry-forwards A/D/E/K (B closed S27,
  H closed S26, J closed S25, StgSplit closed S28).
- Carry-forward candidates: A (barcada-drift; blocked on
  parquets), D (Phase 4 PR-D tooling), E (cassette corpus
  expansion), K (ADLSCostJournal live Azure smoke).

---

## Handoff metadata

- Outgoing session number: 28
- Closing date: 2026-05-26
- Outgoing session scope: Stage 1 ShardResult LLM-vs-embedding
  split (S28 Candidate StgSplit). 3 commits per Q-StgSplit.6:
  `776d203 WA0.W5.X.stage1-cost-split-shardresult`,
  `9afde57 WA0.W5.X.stage1-cost-split-cascade-invoker`,
  `ae9e627 WA0.W5.X.stage1-cost-split-wiring-test`.
  All 8 `_TOTALS_FIELDS` slots now populate after a full cascade
  run (closes the S27 deferred 2-slot gap). LLM spend: $0.
- Reason for transition: S28 3-commit scope completed cleanly;
  Candidate StgSplit shipped end-to-end with the deferred S27
  cost-accounting gap closed. Phase 1 → Phase 6 in a single
  context window with no HALTs. No in-flight sub-surface.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `ae9e627`
  (WA0.W5.X.stage1-cost-split-wiring-test).
- Last commit subject: "WA0.W5.X.stage1-cost-split-wiring-test:
  tests/runners/fixture_cascade/test_cost_journal_wiring.py
  (S28 Candidate StgSplit Commit 3 of 3 per Q-StgSplit.4 Option 1
  1<->1 same-shape replacement; ...)".
- Branch sync with `origin/main`: 0 ahead / 0 behind (verified
  at S28 close after push of `a1c5636..ae9e627`).
- Tags (11 total; unchanged from S27 close):
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
- Pre-push gate state at HEAD `ae9e627`: ALL CHECKS PASS (ruff +
  ruff format on 352 files + vermin 3.10 + validate_consistency
  0/0).
- Pre-S28 unstaged operator territory (Sessions 8-28 precedent —
  expected to stay unstaged across sessions):
  `eval_data/TAXONOMY_GAP_LOG.md`,
  `eval_data/audits/step3_professional_credentials_queue.jsonl`,
  `eval_data/stage1_labels.jsonl`.
  S28 saw NO new operator-side eval_data commits between S27
  close and S28 open.
- Corpus: 222 .html fixtures (unchanged from S17 close).
- 202 expected.json files (unchanged).
- 222 meta.json files (unchanged).
- 1213 baseline-v0 files (unchanged from S18 close at `9e9a1fb`).
- MODIFIED Session 28 (3 commits):
    - **`776d203`**:
        - `src/barcada_scraper/classifier/stage1/run.py` (+19/-2):
          ShardResult adds `llm_cost_usd: float` +
          `embedding_cost_usd: float` after `cost_usd` (12 → 14
          fields). `_build_shard_result` populates both from
          `cost_tracker.llm_cost_usd` /
          `cost_tracker.embedding_cost_usd`. Docstring documents
          cardinal invariant.
        - `tests/classifier/stage1/test_run_cascade.py` (+35/0):
          +1 net-new test
          `test_shard_result_carries_llm_and_embedding_cost_split`.
    - **`9afde57`**:
        - `tests/runners/fixture_cascade/cascade.py` (+25/-38):
          Stage 1 invoker switched from `_journal_record` to
          `_journal_record_with_breakdown` with components
          `{'llm', 'embedding'}`. Module docstring updated to
          reflect S28 closure. Removed now-orphaned
          `_journal_record` helper (24 LOC).
    - **`ae9e627`**:
        - `tests/runners/fixture_cascade/test_cost_journal_wiring.py`
          (+53/-29): 1↔1 same-shape replacement of
          `test_stage1_per_tier_slots_remain_zero_by_design` with
          `test_stage1_per_tier_slots_populate_from_split` (net-
          zero count); module docstring + injected-costs comment
          updates.
- (Unchanged from S27 close, all locked):
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
    - S27 deliverables (cascade.py per-tier wiring helper at
      `a1c5636`; the helper signature is locked — S28 used it
      without modification).
    - All scraper/orchestrator surfaces locked per Out-of-scope
      list in SESSION_28_PROMPT.md.
- Combined test suite at HEAD `ae9e627`:
    - **970 passed / 0 failed / 0 skipped** with the canonical
      16-path invocation (unchanged from S27 close; S28's 1↔1
      replacement preserved the count).
    - **944 passed / 0 failed / 0 skipped** with the narrower
      14-path invocation (unchanged from S27 close).
    - **+1 net-new test** in
      `tests/classifier/stage1/test_run_cascade.py` is OUTSIDE
      the canonical 16-path invocation. Total stage1 tests
      passing: 32 (16 test_run_cascade + 16 test_cost_tracker).

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 28 start: `4ad1f33` (S28 prompt
  drafted post-S27-close; 1 commit ahead of `258cd86` S27-close
  anchor due to prompt-drafting — matched the S20-S27 precedent).
  At Session 28 Phase 0 Step 0.1 this was tolerated under the
  "Workspace HEAD delta tolerance" pattern (the extra commit was
  a SESSION_28_PROMPT.md + SESSION_TRANSITION_TEMPLATE.md edit
  only).
- Session 28 close-out workspace commits: 2 (primary
  `2bb5879` close-out: SESSION_LOG.md + SESSION_TRANSITION_TEMPLATE.md
  + LESSONS.md; THIS follow-up pinning the anchor SHA for S29
  Phase 0 Step 0.1).
- **Last commit SHA at Session 28 CLOSE: this commit (the
  follow-up pinning the anchor; succeeds `2bb5879`)**. S29
  prompt's Phase 0 Step 0.1 MUST anchor workspace expectation to
  THIS follow-up's SHA, NOT to `2bb5879` (which this follow-up
  succeeds). Per S21-S27 LESSONS pattern "Workspace HEAD delta
  tolerance": tolerate N additional prompt-drafting / audit-
  correction commits between sessions; verify each is consistent
  with that pattern before continuing.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected
  after Session 28 close push.

---

## Session 29 execution order (enforce strict sequence)

Same N-phase shape applies regardless of scope choice (Phase 0
cold-start verify → Phase 1 scope → Phase 2 design-gate → Phase 3
impl → Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 29 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 28 entry.
3. Reading the LESSONS.md addition Session 28 landed (1 new
   section at end of file, "S28 folding" suffix).
4. Reading the relevant section of BARCADA_CRAWLER_
   REMEDIATION_PLAN.md for the chosen Session 29 scope (see
   "Notes for Session 29" below).
5. Reading the Session 29 prompt if one has been drafted, OR
   commissioning a fresh draft at S29 open.
6. Running Phase 0 cold-start verification per the prompt's
   protocol (or per the S28 prompt template if S29 prompt is
   not yet drafted; mirror the S28 Phase 0 9-step verification
   shape, updating workspace HEAD anchor, repo HEAD anchor
   (`ae9e627`), and canonical baseline (970)).

---

## Outstanding operator-input requests entering Session 29

1. **Session 29 scope choice** — pick from the candidates in
   "Notes for Session 29" below. Candidate StgSplit closed at
   S28; the carry-forwards (A/D/E/K) remain. No new carry-
   forward introduced by S28.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*.jsonl` continue across sessions (Sessions 8-28
   precedent). S28 saw NO operator-side eval_data commits
   between S27 close and S28 open. validate_consistency stayed
   green throughout S28 (modulo one transient "1 error" first-
   run that cleared on re-run; noted in SESSION_LOG.md S28 entry
   as a curiosity, not a halt-blocker).

3. **barcada-drift AI/ML alignment** — unchanged from S21-S28
   handoffs. If operator wants to ship `barcada-drift` in S29,
   the 4 AI/ML team decisions need to be pre-resolved OR scoped
   narrowly with placeholders. Plus the prereq of 2+ parquet
   files (earliest natural date 2026-06-06 if the launchd
   installer fired immediately after S20 close).

4. **launchd kit installation** — unchanged. Operator should
   run `scripts/launchd/install_canary_schedule.sh` when ready
   to enable the weekly Saturday-9am canary job. Required
   prerequisite for Candidate A.

5. **Session 29 prompt draft commissioning** — operator decides
   whether to commission an S29 prompt between sessions or scope
   one at S29 open.

6. **Live Azure smoke for ADLSCostJournal** (Candidate K;
   carry-forward from S25→S26→S27→S28) — S25 shipped
   ADLSCostJournal tested against DummyBlobBackend in-memory.
   The production code path against real Azure / Azurite has
   never been exercised.

---

## Notes for Session 29

Suggested S29 scope candidates (operator picks at S29 open):

### Candidate A (carry-forward): `barcada-drift` skeleton

Unchanged from S21-S28 handoffs. Per CLASSIFICATION_ADJACENT_PLAN.md
§Item 8. Consumes `canary_runs/<date>.parquet` artifacts.
**Blocked**: 2+ parquet files needed (launchd installer not yet
run as of S28 close; earliest natural date 2026-06-06 if installed
post-S20-close). Estimated ~300 LOC.

### Candidate D (carry-forward): Phase 4 PR-D operator-led labeling

Unchanged. Tooling support only; labeling itself is operator
territory. W0 is closed (workstream-0-end at `a1c5636` placed
S27); Phase 4 PR-D/E/F/G work is W0-side unblocked. Still gated
on operator-led Stage 2/3 labeling start.

### Candidate E (carry-forward): Cassette corpus expansion

Unchanged from S22-S28 handoffs. S20 shipped 20 cassettes; plan's
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

---

## Required reading (Session 29 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 28 entry — 3-commit narrative;
   Q-StgSplit.1 through Q-StgSplit.7 + Sub-question 1.TAG
   decisions; the closed S27 carry-forward; the empirical-vs-by-
   design test-pin distinction that surfaced.
3. **`LESSONS.md`** — 1 new section appended at S28 close
   ("S28 folding" suffix): "Empirical-vs-by-design distinction
   in test pins".
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope
   section per Session 29 candidate choice. Plan is READ-ONLY.
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A (barcada-drift) is chosen.
6. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   — only if Candidate K touches the ADLS backend.
7. **`docs/CRAWLING_POLICY.md`** at S26 SHA `2314f5e` — only if
   operator wants to review the S26-tightened version (77 lines
   / 2.52 KB). Locked.

---

## Outstanding items carried forward to Session 29+

1. **Per-tier cost-accounting wiring** — CLOSED end-to-end S28.
   All 8 `_TOTALS_FIELDS` slots wired. Empirically $0 in default
   fake mode against the fixture corpus (rules-classified
   fixtures skip Tier 2/3); the wiring fires under non-zero
   adjudicator costs at Stage 1.

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

6. **Phase 4 PR-D/E/F/G** (forward look) — W0-side unblocked
   since S27 (workstream-0-end at `a1c5636`). Operator-led
   Stage 2 + Stage 3 labeling work still needs to begin before
   PR-D/E/F/G work can land.

7. **CRAWLING_POLICY.md size** — CLOSED at S26 (2.52 KB).

8. **abfss:// CostJournal Phase 5 promotion** — CLOSED at S25.

9. **Live Azure smoke for ADLSCostJournal** (Candidate K) —
   carry-forward from S25→S26→S27→S28. Optional; not a session-
   scope blocker.

10. **Stage 1 ShardResult LLM-vs-embedding split** — CLOSED S28
    (Candidate StgSplit). 3-commit ship across `776d203` /
    `9afde57` / `ae9e627`.

---

## Locked artifact reminders for Session 29

Carry-forward from Sessions 8-28 (additions for S28 marked NEW):

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
  at `dd64963` except via W5.X-prefix commits. **S27 ADDITION**:
  `cascade.py` modified at SHA `a1c5636` (per-tier cost-
  accounting retrofit). **NEW S28 ADDITIONS** (under W5.X-prefix
  authorization per Q-StgSplit.3):
  - `cascade.py` extended at SHA `9afde57` (Stage 1 invoker switch
    to `_journal_record_with_breakdown` + dead-code removal of
    orphaned `_journal_record`; module docstring updated). The
    `_journal_record_with_breakdown` helper signature is
    unchanged from S27; further modifications require Phase 2
    design-gate authorization.
  - `test_cost_journal_wiring.py` modified at SHA `ae9e627`
    (1↔1 replacement per Q-StgSplit.4; net-zero test count).
  Both S28 modifications are now LOCKED.
- **S27 LOCK**:
  `tests/runners/fixture_cascade/test_cost_journal_wiring.py`
  — locked at `a1c5636` for the original 6 tests; S28 1↔1
  replaced one of those 6 with a same-shape test
  (`test_stage1_per_tier_slots_populate_from_split` at SHA
  `ae9e627`). Test count unchanged at 6.
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
  S22-extended at `1d9404e`. S27 + S28 consumed the existing
  public API (`with_stage_cost_added`, `with_shard_appended`,
  `update_with_retry`) without modification.
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
- **NEW S28 LOCKS**:
  - `src/barcada_scraper/classifier/stage1/run.py` —
    `ShardResult` adds `llm_cost_usd` + `embedding_cost_usd`
    fields (S28 SHA `776d203`; field count 12 → 14). Both fields
    populated from CostTracker's pre-existing properties.
    `_build_shard_result` body updated. Cardinal invariant in
    docstring: `cost_usd == llm_cost_usd + embedding_cost_usd`.
    LOCKED — additional ShardResult fields require Phase 2
    design-gate authorization.
  - `tests/classifier/stage1/test_run_cascade.py` — +1 net-new
    test `test_shard_result_carries_llm_and_embedding_cost_split`
    at S28 SHA `776d203`. LOCKED.
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
  + _build_shard_result populate). S26 + S27 added no new src/
  authorizations. **S28 added 1 new src/ authorization** for
  `classifier/stage1/run.py` per Q-StgSplit.7 Option 1
  (cost_tracker.py did NOT need modification — properties
  already existed).
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-29-open baseline

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

Sub-totals identical to S27 close: 210 conformance + 52 driver +
99 baseline_v0 + 33 synthetic_crawl + 32 robots + 30 robots_gate
+ 30 robots_bypass_config + 43 cost_journal + 13
cost_journal_local + 19 cost_journal_adls + 35 robots_integration
+ 74 vmss_worker + 129 job_runner + 152 worker_loop + 7
robots_gate_integration + 12 worker_loop_persistence = 970.
(S28's 1↔1 replacement inside the 52 driver count preserved net
total; S28's +1 net-new test in stage1/ is OUTSIDE this
invocation.)

Cumulative-test-count gate: the count NEVER decreases between
commit boundaries.

Narrower baselines (still valid for S29 candidates that don't
exercise the new ADLS test paths):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 944 (S27/S28-equivalent narrower; canonical 16-path minus 19
  cost_journal_adls minus 7 robots_gate_integration; verified
  post-S28-push)

Choose at Phase 0 Step 0.5 per Candidate selection.

---

## Pre-push gate at Session 29 open

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
between S28 close and S29 open, the gate will block even though
no S29 commit touches eval_data. Per LESSONS: surface to operator
with the row+detail, propose operator-fix or stash-and-restore;
do NOT auto-fix.

S28 saw a transient "1 error" first-run that cleared on identical
re-run with no intervening edits. Documented in S28 SESSION_LOG
entry as a curiosity (possible race with operator-WIP saves).
LESSONS-worthy if it reproduces in S29.

---

## Context-window awareness

Session 28 ran across 3 commits + Phase 2 source-verification +
Phase 6 close-out, comfortably within context. No HALTs, no
mid-Phase-3 extensions. Session 29 budget per chosen candidate:

- Candidate A (barcada-drift): only if launchd job has run ≥2
  times AND AI/ML decisions ready. Estimated ~300 LOC.
- Candidate D (Phase 4 PR-D tooling): operator-led; tooling only.
- Candidate E (cassette corpus expansion): depends on operator
  curation choices.
- Candidate K (ADLSCostJournal live smoke): K-a ~50-100 LOC +
  Docker; K-b ~30 LOC operator-driven.

Strategies (unchanged from S20-S28 prompts):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-HTTP corpus work, pilot 1-3 before full N-domain.
- Source-verify line numbers per Phase 3 commit, not just at
  Phase 2 (S23 LESSONS pattern).
- Test against public API surface only — probe `.path` /
  behavior, not private attrs (S24 LESSONS pattern).
- Source-verify facts behind option-set design BEFORE
  AskUserQuestion drafts (S25 LESSONS pattern). S28 demonstrated
  this directly: pre-Q-StgSplit grep showed CostTracker already
  had llm_cost_usd / embedding_cost_usd properties, collapsing
  Q-StgSplit.1 from 3 options to 2 and narrowing Q-StgSplit.7's
  src/ touch from "stage1/run.py + cost_tracker.py" to
  "stage1/run.py only".
- Grep for same-shape tests outside the prompt's explicit
  allowlist at Phase 0 (S25 LESSONS Q-J.8 extension lesson).
- At Phase 2, count the prompt's Q-* option set; if any single
  Q-* enumerates >4 options, tier the question or split the
  AskUserQuestion call rather than silently narrowing (S26
  LESSONS pattern).
- When deferring a low-severity wiring gap, document the specific
  parallel-API seam that will close it later (S27 LESSONS
  pattern). S28's StgSplit closure demonstrated the seam
  documentation paid for itself directly.
- **NEW S28 LESSONS**: at retrofit time, audit existing test
  pins for "by design" vs "empirically true" distinction. Old
  pins that assert `X == 0.0` AS A DESIGN INVARIANT may stay
  literally true under the retrofit while their semantic intent
  changes; 1↔1 replace them or re-frame their comments
  explicitly so future readers can tell whether the assertion
  is still load-bearing.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S29 scope closes,
  transition per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-28:

1. Commit SHA(s) of each Session 29 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 970 baseline → S29 close.
4. Driver suite count (52/52 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (Workstream 0 closed at S27; no further
   workstream-0-* tags. workstream-A milestones depend on W A.2
   completion; W A.1 closed at S22's workstream-a-week1-end).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 28 handoff template. Refill at Session 29 close
per Phase 6 close-out protocol.
