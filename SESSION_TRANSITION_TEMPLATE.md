# Session Transition Template — Handoff from Session 25 → Session 26

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-25 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 26 invocation prompt:** not yet drafted at S25 close.
Per S20→S21, S21→S22, …, S24→S25 precedent, the next-session prompt
is operator-commissioned between sessions; if not commissioned in
advance, scope it at S26 open using this template + the S25
SESSION_LOG entry. Anchors that S26 Phase 0 must verify:
- Workspace HEAD: `<S25 close-out follow-up SHA>` (pinned by the
  follow-up commit on this template; see "Workspace state" below).
- Repo HEAD: `aed7873` (S25 Commit 2 final).
- Canonical baseline: 964 tests (16-path invocation).
- Carry-forward candidates: A, B, D, E, H (unchanged from S22-S24
  handoffs). Candidate J CLOSED at S25.

---

## Handoff metadata

- Outgoing session number: 25
- Closing date: 2026-05-24
- Outgoing session scope: abfss:// CostJournal Phase 5 promotion
  (Candidate J per S25 Phase 1). 2 per-module commits per Q-SHARED.1:
  `835a531 WA2.W8.adls-promotion-backend` (ADLSCostJournal full
  backend + DummyBlobBackend test posture; 947 → 964 combined),
  `aed7873 WA2.W8.adls-promotion-worker-loop` (abfss:// guard
  removed in _open_cost_journal_for_worker; 2 S24 fail-loud tests
  replaced 1↔1; 964 preserved).
  Closes S24's Q-I.1 file://-only deferral (abfss:// URLs now
  dispatch through open_journal → ADLSCostJournal). No tag placed
  (1.TAG = defer; Candidate J alone is not a workstream-end
  milestone — W A.2 sub-workstream continues across S23 + S24 + S25
  + future). LLM spend: $0.
- Reason for transition: S25 2-commit scope completed cleanly;
  abfss:// promotion shipped end-to-end with 17 net-new tests in
  test_cost_journal_adls.py (2 → 19) plus 3 1↔1 same-shape test
  replacements across 3 files (test_cost_journal.py +
  test_worker_loop_persistence.py + test_robots_gate_integration.py).
  No in-flight sub-surface. The W A.2 next natural follow-on is the
  per-tier cost-accounting retrofit (Candidate B) if operator wants
  to close Workstream 0 and place `workstream-0-end`.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `aed7873` (WA2.W8.adls-promotion-worker-loop).
- Last commit subject: "WA2.W8.adls-promotion-worker-loop:
  src/barcada_scraper/orchestrator/worker_loop.py +
  tests/orchestrator/test_worker_loop_persistence.py +
  tests/orchestrator/test_robots_gate_integration.py (S25
  Candidate J Commit 2; abfss:// guard removed in
  _open_cost_journal_for_worker; 2 S24 fail-loud tests replaced
  1<->1; 964 combined preserved)"
- Branch sync with `origin/main`: 0 ahead / 0 behind (verified
  at S25 close after push at HEAD `aed7873`).
- Tags (10 total; unchanged from S22 close; do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3`
  - `workstream-0-week1-end` at `4f9d23f`
  - `workstream-0-week2-end` at `e5d2f91`
  - `workstream-0-week3-end` at `cf0c14c`
  - `workstream-0-week4-1-5-end` at `dd64963` (annotated)
  - `workstream-0-week4-end` at `b2e2671` (annotated)
  - `workstream-0-week5-end` at `ddd3cb0` (annotated)
  - `baseline-v0` at `9e9a1fb` (annotated)
  - `workstream-0-week7-end` at `ea37102` (annotated)
  - `workstream-a-week1-end` at `fdc8a7a` (annotated; placed S22)
- Pre-push gate state at HEAD `aed7873`: ALL CHECKS PASS (ruff +
  ruff format + vermin 3.10 + validate_consistency 0/0).
- Pre-S25 unstaged operator territory (Sessions 8-25 precedent —
  expected to stay unstaged across sessions): `eval_data/README.md`,
  `eval_data/TAXONOMY_GAP_LOG.md`, `eval_data/stage1_labels.jsonl`.
  S25 saw no new operator-side eval_data commits between S24 close
  and S25 open (the only deltas at S25 Phase 0 were the workspace's
  own S25-prompt commits, which Phase 0 Step 0.1 tolerated).
- Corpus: 222 .html fixtures (unchanged from S17 close).
- 202 expected.json files (unchanged).
- 222 meta.json files (unchanged).
- 1213 baseline-v0 files (unchanged from S18 close at `9e9a1fb`).
- MODIFIED Session 25 (Commit 1 SHA `835a531`):
    - `src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
      (~50 LOC skeleton → 295 LOC full backend). Adds:
        - `BlobNotFoundError`, `ConditionNotMetError` (backend-layer
          exceptions).
        - `_BlobBackend` Protocol (minimal upload/download/exists
          surface).
        - `_abfss_to_https` URL helper (translates abfss://
          container@account.dfs… → https://account.blob…/container/path).
        - `_AzureBlobBackend` (production wrapper around
          azure-storage-blob's BlobClient with If-None-Match/If-Match
          → ResourceExistsError/ResourceModifiedError mapping).
        - Full `ADLSCostJournal` (read / write_initial / try_update /
          exists + path property as str URL).
    - `tests/classifier/pipeline/test_cost_journal_adls.py` (29 LOC
      → 339 LOC; 2 → 19 tests). Adds `DummyBlobBackend` in-memory
      simulator + full method coverage + update_with_retry chain
      tests + bypass-log round-trip + 4 _abfss_to_https tests.
    - `tests/classifier/pipeline/test_cost_journal.py` — Q-J.8
      EXTENSION authorized at Phase 3 HALT (1↔1 replacement;
      net-zero for that file). Same shape as the other 3 Q-J.8
      replacements.
- MODIFIED Session 25 (Commit 2 SHA `aed7873`):
    - `src/barcada_scraper/orchestrator/worker_loop.py`
      (`_open_cost_journal_for_worker` body only; +48 / -21 LOC):
      abfss:// guard removed; abfss:// dispatch uses
      string `rsplit('/', 1)` (NOT pathlib — collapse hazard
      source-verified at Phase 2). Helper signature preserved.
      Adjacent invoker-site comment updated to note Phase 5 shipped.
      Other 2 S24 helpers untouched.
    - `tests/orchestrator/test_worker_loop_persistence.py` (Q-J.8
      1↔1 replacement; 12 tests preserved). Adds ADLSCostJournal
      import. Replaces
      `test_open_cost_journal_abfss_raises_not_implemented_with_phase5_marker`
      with `test_open_cost_journal_abfss_constructs_adls_journal`.
    - `tests/orchestrator/test_robots_gate_integration.py` (Q-J.8
      1↔1 replacement; 7 tests preserved). Replaces
      `test_invoker_abfss_cost_journal_url_raises_not_implemented`
      with `test_invoker_abfss_cost_journal_url_constructs_adls_journal`
      (spies the helper + stubs init/build_writer/fetch_one/write_pages
      to reach dispatch without real Azure / network / fsspec). The
      4 S23 tests + 2 unchanged S24 tests in this file untouched.
- (Unchanged from S24 close, all locked except where Q-J.8 above
  explicitly authorizes):
    - `src/barcada_scraper/scraper/robots.py` (S21 parser at `34a59b6`)
    - `tests/scraper/test_robots.py` (32 tests)
    - `src/barcada_scraper/scraper/robots_gate.py` (S22 shim at
      `ba87e7e`)
    - `src/barcada_scraper/scraper/robots_bypass_config.py` (S22
      loader at `381ee89`)
    - `tests/scraper/test_robots_gate.py` (30 tests)
    - `tests/scraper/test_robots_bypass_config.py` (30 tests)
    - `src/barcada_scraper/classifier/pipeline/cost_journal.py`
      (S22 surface at `1d9404e`; S25 CONSUMES it via Commit 1 but
      does NOT modify — the abfss://-routing in open_journal already
      existed at S22 with the conditional import path)
    - `src/barcada_scraper/classifier/pipeline/cost_journal_local.py`
      (LocalFSCostJournal; S25 does NOT modify)
    - `docs/CRAWLING_POLICY.md` (S22 doc at `fdc8a7a`)
    - `tools/synthetic_crawl/`, `tools/baseline_v0/canary.py`,
      `tests/synthetic_crawl/`, `tests/baseline_v0/test_canary.py`,
      `tests/fixtures/synthetic_crawls/`, `scripts/launchd/` (S20
      deliverables)
    - All S23 deliverables (orchestrator/robots_integration.py
      @ `279bb77`; tests/orchestrator/test_robots_integration.py;
      vmss_worker.py + job_runner.py + cloud_init.template.yaml
      additions)
    - S24 worker_loop.py helpers (2 of 3 untouched at S25;
      `_open_cost_journal_for_worker` body modified only as
      authorized by Q-J.4 / Q-J.8)
    - The 5 S24 retargeted test_stage2_pages_invoker_* fixtures
      in test_worker_loop.py (still file://, NOT reverted to abfss://)
- Combined test suite at HEAD `aed7873`:
    - **964 passed / 0 failed / 0 skipped** with the 16-path
      invocation (S25 canonical S26-baseline below).
    - 605 + 17 = 622 passed when restricted to `tests/orchestrator/`
      + `tests/classifier/pipeline/test_cost_journal_adls.py`.
    - 480 passed when restricted to S22 headline-suite paths
      (no orchestrator/, no journal-suite ride-along).
    - 538 passed for the broader S22 headline + journal-suite.
    - The S23 932-baseline is no longer a useful narrower floor
      (test_cost_journal_adls.py grew from 2 → 19; the natural
      narrower S25-equivalent baseline would now be 949).

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 25 start: `0d24d2d` (S25 prompt v2
  with 6 reviewer findings applied; 2 commits ahead of S24
  close-out follow-up `763fd1a` due to prompt-drafting + v1→v2
  reviewer-findings audit — matched the S20-S24 precedent for
  prompt-drafting between sessions). At S25 Phase 0 Step 0.1 this
  was tolerated under the "Workspace HEAD delta tolerance"
  pattern (both extra commits were SESSION_25_PROMPT.md edits only).
- Session 25 close-out workspace commits: 1 (this file's primary
  edit) + 1 expected follow-up pinning the anchor SHA for S26
  Phase 0 Step 0.1.
- **Last commit SHA at Session 25 CLOSE: this commit (the follow-up
  pinning the anchor)**. S26 prompt's Phase 0 Step 0.1 MUST anchor
  workspace expectation to THIS follow-up's SHA, NOT to the primary
  close-out (which this follow-up succeeds). Per S21-S24 LESSONS
  pattern "Workspace HEAD delta tolerance": tolerate N additional
  prompt-drafting / audit-correction commits between sessions;
  verify each is consistent with that pattern before continuing.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected
  after Session 25 close push.

---

## Session 26 execution order (enforce strict sequence)

Same N-phase shape applies regardless of scope choice (Phase 0
cold-start verify → Phase 1 scope → Phase 2 design-gate → Phase 3
impl → Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 26 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 25 entry.
3. Reading the LESSONS.md additions Session 25 landed (3 new
   sections at end of file, "S25 folding" suffix).
4. Reading the relevant section of BARCADA_CRAWLER_
   REMEDIATION_PLAN.md for the chosen Session 26 scope (see
   "Notes for Session 26" below).
5. Reading the Session 26 prompt if one has been drafted, OR
   commissioning a fresh draft at S26 open.
6. Running Phase 0 cold-start verification per the prompt's
   protocol (or per the S25 prompt template if S26 prompt is
   not yet drafted).

---

## Outstanding operator-input requests entering Session 26

1. **Session 26 scope choice** — pick from the candidates in
   "Notes for Session 26" below. Candidate J closed at S25; the
   carry-forwards (A/B/D/E/H) remain. Candidate B specifically
   would close Workstream 0 and warrant `workstream-0-end` tag.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*.jsonl` continue across sessions (Sessions 8-25
   precedent). S25 saw NO operator-side eval_data commits between
   S24 close and S25 open. validate_consistency stayed green
   throughout S25.

3. **barcada-drift AI/ML alignment** — unchanged from S21-S25
   handoffs. If operator wants to ship `barcada-drift` in S26,
   the 4 AI/ML team decisions need to be pre-resolved OR scoped
   narrowly with placeholders. Plus the prereq of 2+ parquet
   files (earliest natural date 2026-06-06).

4. **launchd kit installation** — unchanged. Operator should
   run `scripts/launchd/install_canary_schedule.sh` when ready
   to enable the weekly Saturday-9am canary job. Required
   prerequisite for Candidate A.

5. **Session 26 prompt draft commissioning** — operator decides
   whether to commission an S26 prompt between sessions or scope
   one at S26 open.

6. **Live Azure smoke for ADLSCostJournal** (optional, NEW) —
   S25 shipped ADLSCostJournal tested against DummyBlobBackend
   in-memory (Q-J.3 (c)). The production code path against real
   Azure / Azurite has never been exercised. A small operator-
   driven smoke test (write_initial + try_update + read against a
   sandbox container) would close the mock-vs-prod divergence
   risk. Estimated 15-30 minutes of operator work; no S26 scope
   needed unless the smoke surfaces a bug.

---

## Notes for Session 26

Suggested S26 scope candidates (operator picks at S26 open):

### Candidate A (carry-forward): `barcada-drift` skeleton

Unchanged from S21-S25 handoffs. Per CLASSIFICATION_ADJACENT_PLAN.md
§Item 8. Consumes `canary_runs/<date>.parquet` artifacts.
**Blocked**: 2+ parquet files needed (launchd installer not yet
run as of S25 close; earliest natural date 2026-06-06).
Estimated ~300 LOC.

### Candidate B (carry-forward): Per-tier cost-accounting retrofit

Unchanged from S21-S25 handoffs. Closes Workstream 0; warrants
`workstream-0-end` tag. Touches W4.1.5 driver area (locked except
via W5.X-prefix commits). Estimated 100-200 LOC.

Now that Candidate J (abfss://) closed at S25, the cost-accounting
retrofit can plausibly use abfss:// CostJournal end-to-end in its
verification — though the per-tier wiring itself does not require
ADLS; LocalFSCostJournal still works.

### Candidate D (carry-forward): Phase 4 PR-D operator-led labeling

Unchanged. Tooling support only; labeling itself is operator
territory.

### Candidate E (carry-forward): Cassette corpus expansion

Unchanged from S22-S25 handoffs. S20 shipped 20 cassettes; plan's
upper bound is 30. Could expand or curate.

### Candidate H (carry-forward small): CRAWLING_POLICY.md tightening

Unchanged from S22-S25 handoffs. Q-F.6's "minimal-first" estimate
cited ~1-2 KB; S22 shipped 8.1 KB. Estimated <50 LOC of doc changes;
no code; <30 minutes.

---

## Required reading (Session 26 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 25 entry — 2-commit narrative;
   the Q-J.1 through Q-J.8 + 1.TAG decisions; the mid-Phase-3
   HALT-and-extend for Q-J.8; the abfss:// → ADLSCostJournal
   end-to-end wiring narrative.
3. **`LESSONS.md`** — 3 new sections appended at S25 close
   ("S25 folding" suffix): Phase 2 source-verify drives option-set
   design / Q-J.8 explicit allowlist may be incomplete /
   Local imports defeat module-attribute monkeypatch.
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope
   section per Session 26 candidate choice. Plan is READ-ONLY.
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A (barcada-drift) is chosen.
6. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   — only if Candidate B chooses to verify per-tier wiring
   against ADLS, OR if operator wants to review the S25 shipment.
7. **`docs/CRAWLING_POLICY.md`** — only if Candidate H is chosen.

---

## Outstanding items carried forward to Session 26+

1. **Per-tier cost-accounting wiring gap** — carry-forward from
   S14; severity LOW. Unchanged disposition.

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

6. **Phase 4 PR-D/E/F/G** (forward look) — Unchanged. Opens
   after Workstream 0 fully closes AND operator-led Stage 2 +
   Stage 3 labeling work begins.

7. **CRAWLING_POLICY.md size** — Unchanged. Doc shipped at
   8.1 KB vs Q-F.6's ~1-2 KB estimate. See Candidate H above.

8. **abfss:// CostJournal Phase 5 promotion** — CLOSED at S25
   (Commits `835a531` + `aed7873`). Removed from carry-forward.

9. **Live Azure smoke for ADLSCostJournal** (NEW S25→S26) —
   optional operator-driven smoke against real Azure / Azurite
   to close mock-vs-prod divergence risk. Not a session-scope
   blocker.

---

## Locked artifact reminders for Session 26

Carry-forward from Sessions 8-25:

- `eval_data/` — labeling-workstream territory. Operator-WIP
  edits across sessions are expected. Pre-push validate_
  consistency runs against WT state; surface per LESSONS pattern
  if blocked.
- `stage1.schema.json` v1.0 with 49 keywords.
- `pre-remediation-2026-05-19` tag.
- `baseline-v0` tag at `9e9a1fb`.
- All `workstream-0-*` tags at their placed SHAs (9 tags from
  S20 close; unchanged).
- `workstream-a-week1-end` tag at `fdc8a7a` (placed S22).
- `tests/runners/fixture_cascade/` — W4.1.5 driver locked at
  `dd64963` except via W5.X-prefix commits.
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
  S22-extended at `1d9404e`. S25's Q-J.8 extension touched ONLY
  the test file `tests/classifier/pipeline/test_cost_journal.py`
  (1↔1 replacement); the production file is unchanged.
- `src/barcada_scraper/classifier/pipeline/cost_journal_local.py`
  — production local-FS backend; locked.
- **NEW S25 LOCK**:
  `src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
  — full backend shipped at SHA `835a531`. Public API:
  `ADLSCostJournal(journal_dir, run_id, credential=None,
  blob_backend=None)` with read / write_initial / try_update /
  exists / path. Backend layer: `_BlobBackend` Protocol +
  `_AzureBlobBackend` production wrapper + `_abfss_to_https`
  URL helper + `BlobNotFoundError` + `ConditionNotMetError`.
  Locked at `835a531`.
- **NEW S25 LOCK**:
  `tests/classifier/pipeline/test_cost_journal_adls.py` — 19
  tests covering all 4 abstract methods + update_with_retry
  chain + bypass-log round-trip + 4 URL-conversion tests.
  Locked at `835a531`. Includes the `DummyBlobBackend`
  in-memory simulator class (used by Q-J.8-extension test in
  test_cost_journal.py at line 382-onward).
- `docs/CRAWLING_POLICY.md` — S22 deliverable; locked at
  `fdc8a7a`.
- `src/barcada_scraper/orchestrator/robots_integration.py` —
  S23 deliverable; locked at `279bb77`.
- `tests/orchestrator/test_robots_integration.py` — S23
  deliverable; locked at `279bb77`. 35 tests.
- The 4 S23 tests + 2 unchanged S24 tests + 1 S25-replaced test
  in `tests/orchestrator/test_robots_gate_integration.py` —
  locked at `aed7873`. 7 tests total. Adding new tests is
  allowed; modifying landed tests requires explicit authorization.
- `src/barcada_scraper/orchestrator/vmss_worker.py` (full surface)
  — S23 additions locked at `5eeaac7`; pre-S23 surfaces locked
  as before.
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
  `aed7873` to note Phase 5 shipped).
- `tests/orchestrator/test_worker_loop_persistence.py` — S24
  deliverable + 1 S25-replaced test; locked at `aed7873`. 12
  tests. Adding new tests is allowed; modifying landed tests
  requires explicit authorization.
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
  in 1 helper body). No other src/ module is authorized.
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-26-open baseline

Canonical (16 paths; mirrors S25-close invocation):

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
# Expected: 964 passed / 0 failed / 0 skipped
```

Sub-totals: 210 conformance + 46 driver + 99 baseline_v0 + 33
synthetic_crawl + 32 robots + 30 robots_gate + 30 robots_bypass_config
+ 43 cost_journal + 13 cost_journal_local + 19 cost_journal_adls +
35 robots_integration + 74 vmss_worker + 129 job_runner + 152
worker_loop + 7 robots_gate_integration (4 S23 + 2 S24-unchanged
+ 1 S25-replaced) + 12 worker_loop_persistence (11 S24-unchanged
+ 1 S25-replaced) = 964.

Cumulative-test-count gate: the count NEVER decreases between
commit boundaries.

Narrower baselines (still valid for S26 candidates that don't
exercise the new ADLS test paths):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 949 (S25-equivalent narrower; 16-path minus
  test_cost_journal_adls.py's 19 + test_robots_gate_integration.py's
  7 — for Candidate-H-style doc-only candidates)

Choose at Phase 0 Step 0.5 per Candidate selection.

---

## Pre-push gate at Session 26 open

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 351+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

Note on gate 4: validate_consistency runs against working-tree
state; if operator-WIP in eval_data introduces a schema violation
between S25 close and S26 open, the gate will block even though
no S26 commit touches eval_data. Per LESSONS: surface to operator
with the row+detail, propose operator-fix or stash-and-restore;
do NOT auto-fix.

---

## Context-window awareness

Session 25 ran across 2 commits + Phase 2 source-verification +
1 mid-Phase-3 HALT-and-extend + Phase 6 close-out, well within
context. Session 26 budget per chosen candidate:

- Candidate A (barcada-drift): only if launchd job has run ≥2
  times AND AI/ML decisions ready. Estimated ~300 LOC.
- Candidate B (per-tier cost-accounting): touches W4.1.5 area;
  more careful Phase 0 verification needed. Estimated 100-200 LOC.
- Candidate D (Phase 4 PR-D tooling): operator-led; tooling only.
- Candidate E (cassette corpus expansion): depends on operator
  curation choices.
- Candidate H (doc tightening): very small; <30 minutes.

Strategies (unchanged from S20-S25 prompts):
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

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S26 scope closes,
  transition per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-25:

1. Commit SHA(s) of each Session 26 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 964 baseline → S26 close.
4. Driver suite count (46/46 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (e.g., does S26 warrant a new tag?
   Candidate B alone — closing Workstream 0 — warrants
   `workstream-0-end`; A/D/E/H do not).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 25 handoff template. Refill at Session 26 close
per Phase 6 close-out protocol.
