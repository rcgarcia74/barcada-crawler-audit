# Session 25 prompt — scope picked at Phase 1
# (S24 closed Candidate I; S25 chooses from Candidate J new
#  + carry-forwards A/B/D/E/H from S22/S23/S24)

**Drafted at Session 24 close (2026-05-24).** Mirrors the
S20/S21/S22/S23/S24 prompt structure. Scope-agnostic at
Phases 0/1; scope-specific design gates at Phase 2 per chosen
candidate. Strict 7-phase ordering with halt-on-mismatch
preserved.

This prompt should be invoked from `~/Downloads/session-25-prompt.md`
(operator-mirrored) or directly from
`~/crawler-audit/SESSION_25_PROMPT.md`. Re-read it on session open.

---

## Scope

Engineering session. Workstream sub-surfaces available after
Session 24 closed Candidate I (3 commits) and left repo HEAD at
`aa23712` without a new tag (1.TAG=defer):

- **Candidate I shipped fully (S24)** — durable bypass-audit
  persistence in worker_loop. The production
  `scrape_stage2_pages_invoker` now opens a `CostJournal` per
  invoker invocation (Q-I.5), self-bootstraps if needed (Q-I.2),
  and persists every BYPASS_ALLOW decision to
  `JournalState.robots_bypass_log` via `record_bypass_audit`
  (Q-G.4 protocol). Log + continue on persistence failure (Q-I.6).
  File:// only; abfss:// raises `NotImplementedError` at journal
  construction (Q-I.1) — closing this gap is the natural S25
  follow-on named here as Candidate J.

- **Candidate J (NEW; Recommended)** — abfss:// CostJournal
  Phase 5 promotion. Completes the ADLSCostJournal skeleton in
  `src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
  to match the LocalFSCostJournal public API (`read`,
  `write_initial`, `try_update`, `exists`), then removes the
  abfss:// guard in worker_loop's `_open_cost_journal_for_worker`
  helper so abfss:// URLs flow through `open_journal` to the
  new ADLS backend. Closes the Q-I.1 explicit deferral.

- **barcada-drift (Candidate A)** — deferred per Q1.1=(A) at S20;
  still needs 4 AI/ML decisions per CLASSIFICATION_ADJACENT_PLAN.md
  §Item 8 AND 2+ `canary_runs/*.parquet` files (earliest natural
  date 2026-06-06 if the launchd installer has fired ≥2 Saturdays
  since S20 close).

- **Per-tier cost-accounting wiring gap (Candidate B)** — carry-
  forward from S14; severity LOW; closing it would justify
  `workstream-0-end` tag.

- **Phase 4 PR-D tooling (Candidate D)** — operator-led labeling
  territory.

- **Cassette corpus expansion (Candidate E)** — current 20 is lower
  bound of plan's "~20-30".

- **CRAWLING_POLICY.md tightening (Candidate H)** — S22 doc shipped
  at 8.1 KB vs the Q-F.6 ~1-2 KB estimate; trim to ~2-3 KB while
  preserving essential robots contract. <50 LOC.

Operator chooses at Phase 1 which candidate Session 25 ships. Each
candidate has its own Phase 2 design-gate template.

**Sessions 13-24 precedent:** this session does NOT modify the
W4.1.5 driver orchestration at `tests/runners/fixture_cascade/`
(locked at `dd64963`). Does NOT modify `expected.schema.json` v1.1
/ `META_SCHEMA.md` v1.1. Does NOT modify the committed
`tests/fixtures/baseline-v0/` snapshot at `9e9a1fb`. Does NOT
modify the Session 19 `check` sub-surface code or the Session 20
cassettes/canary sub-surface code or the Session 21 `robots.py`
parser at `34a59b6` or its tests, OR the Session 22 deliverables
(`scraper/robots_gate.py` @ `ba87e7e`,
`scraper/robots_bypass_config.py` @ `381ee89`, the `cost_journal.py`
S22 additions at `1d9404e`, `docs/CRAWLING_POLICY.md` at `fdc8a7a`),
OR the Session 23 deliverables (`orchestrator/robots_integration.py`
@ `279bb77`, `orchestrator/vmss_worker.py` additions at `5eeaac7`,
`orchestrator/job_runner.py` additions at `872527e`,
`scripts/vmss/cloud_init.template.yaml` additions at `872527e`,
`orchestrator/worker_loop.py` S23 additions at `4ec7b0a`, the
integration test file's 4 S23 tests at `6e6e4ca`), OR the Session 24
deliverables (the 3 new module-level helpers in `worker_loop.py`
at `48c324a`, the 12 unit tests in `test_worker_loop_persistence.py`
at `00d5b38`, the 3 new tests appended to
`test_robots_gate_integration.py` at `aa23712`, the 5 retargeted
test_stage2_pages_invoker_* fixtures in `test_worker_loop.py` at
`48c324a`). Does NOT modify production code under
`src/barcada_scraper/` UNLESS Phase 2 design-gate explicitly
authorizes a specific module.

Full regression-protection checklist in **Out-of-scope** at the
end of this prompt. Re-read it before any code lands.

---

## Reviewer-feedback hygiene (if this prompt is reviewed)

If an external reviewer (operator-invoked) flags items in this
prompt before Session 25 starts, walk each flagged item against
on-disk reality at workspace HEAD `763fd1a` and repo HEAD
`aa23712` (or whatever HEAD the operator's machine carries),
BEFORE applying any change. Per S19-S24 pattern (LESSONS
"Reviewer-feedback hygiene"):

- **OBSOLETE** items: SHAs already verified, claims already true.
  Skip with documented reasoning.
- **VALID-applies-now** items: bear on this session's scope. Apply.
- **VALID-applies-later** items: bear on deferred scope. Carry
  forward to the next prompt revision.
- **WRONG-PREMISE** items: assumes something not true. Skip with
  documented reasoning.

Empirical baseline: at S19 review 3 of 5 "must-fix" items
collapsed under cold-start verification; at S20 review 1 of 12
amendments was skipped because it would HALT spuriously (SR-4);
at S21+S22 post-close audit 2 of 3 operator-feedback items required
workspace-doc corrections; at S23 v1→v2 prompt-review cycle
resolved 6 findings before invocation; at S24 v1→v2 cycle resolved
8 findings (B-1, M-1, M-2, S-1, S-2, N-1, N-2, N-3). Review remains
the convergence mechanism; verify each.

---

## Halt protocol (when any phase's halt-condition fires)

Halt-condition format in chat (any phase's halt-on-mismatch):

```
HALT @ Phase N step S.s
Expected:    <claim from prompt>
Observed:    <actual reality from source>
Discrepancy: <one-line summary>
Surfacing to operator. Awaiting guidance.
```

After a halt:
- DO NOT take any action that mutates the repo or workspace.
- DO NOT proceed to Phase N+1.
- Wait for operator response.
- On operator guidance:
  (a) Resume the phase at the step that failed, with the
      discrepancy resolved.
  (b) Skip the phase per operator authorization (rare; document
      the skip in SESSION_LOG.md).
  (c) End the session early at Phase 6 close-out with the halt
      recorded in SESSION_LOG.md.

Halt is not failure — it's the contract. Phase 0 halts catch stale
state. Phase 1 halts catch unresolved scope-blockers. Phase 2
halts catch hidden scope expansion (per S22-S24 "Implicit-
authorization HALT for src/-locks" — any src/ touch not enumerated
in Out-of-scope's allow-list surfaces here). Phase 3 halts catch
regressions. Phase 4 halts catch pre-push gate failures (incl.
operator-WIP-in-locked-tree).

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

Run in order. Halt and surface to operator on any mismatch.

### Step 0.1 — Workspace + repo HEAD

```
# Workspace at Session 25 start (Session 24 close-out: primary +
# 1 follow-up pinning the S25 anchor SHA, all pushed):
git -C ~/crawler-audit rev-parse HEAD
# Expect: 763fd1a (S24 close-out follow-up: pin S25 Phase 0
# workspace anchor SHA) OR a later commit if additional workspace
# doc edits landed post-S24-close. If N commits ahead, verify each
# prior commit's subject via `git log --oneline 763fd1a..HEAD`
# against expected prompt-finalization / doc-edit patterns;
# surface the SHA delta and request authorization to proceed if
# anything is unexpected. (S20-S24 precedent: operator authorized
# continuation when 2-3 extra workspace commits were the
# strengthened prompts themselves.)

# Repo at Session 24 final commit:
git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: aa23712 (WA2.W8.bypass-persistence-integration-extension)
# — the canonical end-of-S24 ship SHA.
#
# Tolerated delta: operator-side eval_data labeling commits between
# S24 close and S25 open are expected (Sessions 8-24 precedent;
# at S24 open the repo had 4bed9b9 on top of 6e6e4ca, a single
# eval_data-only commit). Per the S22-folded "Workspace HEAD delta
# tolerance" LESSONS pattern: tolerate N additional commits as
# long as EACH commit's stat is strictly within eval_data/* (no
# src/barcada_scraper/* touches, no tests/* touches, no scripts/*
# touches, no docs/* touches). Verify via `git show --stat <sha>`
# for every commit in aa23712..HEAD; surface any non-eval_data
# delta for operator authorization before continuing.
```

### Step 0.2 — Tags (no change from S24 close)

```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort
# Expect 10 tags (unchanged from S22/S23/S24 close; S24 did not
# place a tag):
#   baseline-v0
#   pre-remediation-2026-05-19
#   workstream-0-week1-end
#   workstream-0-week2-end
#   workstream-0-week3-end
#   workstream-0-week4-1-5-end
#   workstream-0-week4-end
#   workstream-0-week5-end
#   workstream-0-week7-end
#   workstream-a-week1-end
```

### Step 0.3 — Driver locked

```
cd /Users/administrator/projects/barcada-scraper
git diff dd64963..HEAD -- tests/runners/fixture_cascade/ \
    ':(exclude)tests/runners/fixture_cascade/test_fixture_fetcher.py'
# Expect: empty (only test_fixture_fetcher.py changed via W5.X
# realign at 8d0fc0e in Session 16).
```

### Step 0.4 — Fixture counts (no change from S24 close)

```
find tests/fixtures/html -name '*.html' -type f | wc -l
# Expect: 222

find tests/fixtures/html -path '*/expected/*.json' -type f | wc -l
# Expect: 202

find tests/fixtures/html -name '*.meta.json' -type f | wc -l
# Expect: 222

find tests/fixtures/baseline-v0 -type f | wc -l
# Expect: 1213

find tests/fixtures/synthetic_crawls -name 'cassette.yaml' | wc -l
# Expect: 20

find tests/fixtures/synthetic_crawls -name 'extract_hard_exclusions.json' | wc -l
# Expect: 20
```

### Step 0.5 — Test-suite baseline (S25 canonical)

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
# Expect: 947 passed / 0 failed / 0 skipped
#
# Sub-totals (16 paths):
#   210 conformance + 46 driver + 99 baseline_v0 +
#    33 synthetic_crawl + 32 robots + 30 robots_gate +
#    30 robots_bypass_config + 43 cost_journal +
#    13 cost_journal_local + 2 cost_journal_adls +
#    35 robots_integration + 74 vmss_worker +
#   129 job_runner + 152 worker_loop +
#     7 robots_gate_integration (4 pre-S24 + 3 S24-new) +
#    12 worker_loop_persistence (all S24-new) = 947
#
# Pinned in SESSION_LOG.md "Canonical S24-close baseline" block.
# Re-verified post-S24-close-out at HEAD aa23712: 947 passed in
# ~48s. The 947 count is invariant under operator-side eval_data
# commits between S24 and S25 (eval_data is not in the invocation).
```

The sub-paths add up to the headline: 210 + 46 + 99 + 33 + 32 + 30
+ 30 + 43 + 13 + 2 + 35 + 74 + 129 + 152 + 7 + 12 = 947. Any drift
= halt.

If the headline mismatches, re-run each sub-path independently to
localize which sub-suite drifted:

```
.venv/bin/python -m pytest tests/scraper/test_fixture_conformance.py -q              # expect 210
.venv/bin/python -m pytest tests/runners/fixture_cascade/ -q                          # expect  46
.venv/bin/python -m pytest tests/baseline_v0/ -q                                       # expect  99
.venv/bin/python -m pytest tests/synthetic_crawl/ -q                                   # expect  33
.venv/bin/python -m pytest tests/scraper/test_robots.py -q                             # expect  32
.venv/bin/python -m pytest tests/scraper/test_robots_gate.py -q                        # expect  30
.venv/bin/python -m pytest tests/scraper/test_robots_bypass_config.py -q               # expect  30
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal.py -q           # expect  43
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal_local.py -q     # expect  13
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal_adls.py -q      # expect   2
.venv/bin/python -m pytest tests/orchestrator/test_robots_integration.py -q            # expect  35
.venv/bin/python -m pytest tests/orchestrator/test_vmss_worker.py -q                   # expect  74
.venv/bin/python -m pytest tests/orchestrator/test_job_runner.py -q                    # expect 129
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop.py -q                   # expect 152
.venv/bin/python -m pytest tests/orchestrator/test_robots_gate_integration.py -q       # expect   7
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop_persistence.py -q       # expect  12
```

**Narrower baselines** (valid for S25 candidates that don't
exercise the new test paths — H is the clearest example):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 932 (S23-baseline 15-path; no test_worker_loop_persistence)

Whichever baseline is bound at Phase 1, hold it consistent across
ALL Phase 3 commits in S25 — do not switch mid-session.

### Step 0.6 — Manifest + schema invariants (unchanged)

```
.venv/bin/python -c "
import json
m = json.load(open('tests/fixtures/baseline-v0/manifest.json'))
assert m['schema_version'] == 'baseline-v0/0.1.0', m['schema_version']
assert m['fixture_count'] == 202, m['fixture_count']
assert m['llm_mode'] == 'real', m['llm_mode']
assert m['driver_sha'].startswith('521e363'), m['driver_sha']
print(f'OK manifest baseline-v0/0.1.0; driver_sha prefix {m[\"driver_sha\"][:7]}')

s = json.load(open('tests/fixtures/expected.schema.json'))
assert len(s['properties']['stage3_decision']['required']) == 18
print('OK expected.schema.json v1.1 (18-col stage3 shape)')
"
```

### Step 0.7 — Existing sub-surface CLIs all work

```
.venv/bin/python -m tools.baseline_v0 --help 2>&1 \
    | grep -oE '\b(generate|check|canary-run)\b' | sort -u | wc -l
# Expect: 3 (distinct subcommands: generate, check, canary-run)

.venv/bin/python -m tools.synthetic_crawl --help 2>&1 \
    | grep -oE '\b(record|replay)\b' | sort -u | wc -l
# Expect: 2 (distinct subcommands: record, replay)
```

### Step 0.8 — Regression-protection sanity (any-candidate prereq)

```
# S19 check sub-surface tests (30 total)
.venv/bin/python -m pytest tests/baseline_v0/test_check.py \
    tests/baseline_v0/test_cli.py -k 'check' -q
# Expect: 30 passed

# S20 canary sub-surface tests (23 total)
.venv/bin/python -m pytest tests/baseline_v0/test_canary.py \
    tests/baseline_v0/test_cli.py -k 'canary' -q
# Expect: 23 passed

# S20 cassettes sub-surface tests (33 total)
.venv/bin/python -m pytest tests/synthetic_crawl/ -q
# Expect: 33 passed

# S21 robots-parser sub-surface tests (32 total)
.venv/bin/python -m pytest tests/scraper/test_robots.py -q
# Expect: 32 passed

# S22 robots-gate-shim sub-surface tests (30 total)
.venv/bin/python -m pytest tests/scraper/test_robots_gate.py -q
# Expect: 30 passed

# S22 robots-bypass-config-loader sub-surface tests (30 total)
.venv/bin/python -m pytest tests/scraper/test_robots_bypass_config.py -q
# Expect: 30 passed

# S22 cost-journal additions tests
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal.py -q
# Expect: 43 passed
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal_local.py -q
# Expect: 13 passed
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal_adls.py -q
# Expect: 2 passed

# S23 W A.2 sub-surface tests
.venv/bin/python -m pytest tests/orchestrator/test_robots_integration.py -q
# Expect: 35 passed
.venv/bin/python -m pytest tests/orchestrator/test_vmss_worker.py -q
# Expect: 74 passed
.venv/bin/python -m pytest tests/orchestrator/test_job_runner.py -q
# Expect: 129 passed
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop.py -q
# Expect: 152 passed

# S24 W A.2 sub-surface tests (NEW for S25):
.venv/bin/python -m pytest tests/orchestrator/test_robots_gate_integration.py -q
# Expect: 7 passed (4 S23 + 3 S24-new)
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop_persistence.py -q
# Expect: 12 passed
```

### Step 0.9 — S24-shipped public API stability (Candidate J prereq)

```
# If Candidate J (abfss:// Phase 5 promotion) is even possibly in
# scope, verify the PUBLIC integration contracts of all S24
# deliverables match what landed at S24 close. A change to any of
# these between S24 close and S25 open would invalidate the
# Candidate-J design.
#
# Scope: what Candidate J callers / mutators depend on:
#   _open_cost_journal_for_worker(config) -> CostJournal
#   _ensure_journal_initialized(journal, *, run_id) -> None
#   _build_durable_bypass_writer(journal) -> Callable
#   open_journal(*, journal_dir, run_id) -> CostJournal  (the dispatcher)
#   ADLSCostJournal.__init__(*, journal_dir, run_id) raises NotImplementedError
#     with "Phase 5 deliverable" marker (this is what Candidate J REMOVES)
#   (re-anchored Candidate J prerequisites: all S23 surfaces from S24 prompt's Step 0.9)

.venv/bin/python -c "
import inspect
from barcada_scraper.classifier.pipeline.cost_journal import (
    open_journal,
    JournalState,
    JournalAlreadyExistsError,
    CostJournal,
)
from barcada_scraper.classifier.pipeline.cost_journal_local import LocalFSCostJournal
from barcada_scraper.classifier.pipeline.cost_journal_adls import ADLSCostJournal
from barcada_scraper.orchestrator.worker_loop import (
    _open_cost_journal_for_worker,
    _ensure_journal_initialized,
    _build_durable_bypass_writer,
)
from barcada_scraper.orchestrator.vmss_worker import WorkerConfig

# S24 helper signatures.
def _params(fn): return set(inspect.signature(fn).parameters)
assert 'config' in _params(_open_cost_journal_for_worker)
assert {'journal', 'run_id'} <= _params(_ensure_journal_initialized)
assert 'journal' in _params(_build_durable_bypass_writer)

# open_journal dispatcher contract.
assert {'journal_dir', 'run_id'} <= _params(open_journal)

# LocalFSCostJournal public surface (Candidate J mirrors this).
for m in ('read', 'write_initial', 'try_update', 'exists'):
    assert hasattr(LocalFSCostJournal, m), m

# ADLSCostJournal still raises at __init__ (the seam Candidate J fills).
try:
    ADLSCostJournal(journal_dir='/tmp/_s25_phase0_check', run_id='x')
    raise AssertionError('ADLSCostJournal no longer raises — skeleton was completed; verify operator agency')
except NotImplementedError as exc:
    assert 'Phase 5 deliverable' in str(exc), str(exc)

print('OK all S24-shipped public APIs unchanged from S24 close')
"

# Verify the abfss:// guard in worker_loop's helper still fires.
# This is the seam Candidate J REMOVES; if it's already gone,
# someone has done the work and Phase 1 needs to be re-scoped.
.venv/bin/python -c "
from barcada_scraper.orchestrator.worker_loop import _open_cost_journal_for_worker
from barcada_scraper.orchestrator.vmss_worker import WorkerConfig
config = WorkerConfig(
    phase='scrape-stage2-pages',
    shard_queue_url='https://x.queue.core.windows.net/q',
    blob_output_url='file:///tmp/out',
    cost_journal_url='abfss://j@x.dfs.core.windows.net/c.jsonl',
    stop_flag_url='file:///tmp/stop.json',
    worker_id='test',
    # Sentinel GUID; no Azure call is made because the abfss:// guard
    # fires before credential resolution. Phase 0 Step 0.9 is a pure
    # in-process guard-presence check, not a live Azure smoke test.
    azure_client_id='00000000-0000-0000-0000-000000000000',
    crawl_date='2026-05-23',
    worker_concurrency=1,
)
try:
    _open_cost_journal_for_worker(config)
    raise AssertionError('abfss:// guard no longer fires — Candidate J already shipped?')
except NotImplementedError as exc:
    assert 'Phase 5 deliverable' in str(exc), str(exc)
    print('OK abfss:// guard intact (Candidate J seam present)')
"
```

If any of 0.1-0.9 fail, HALT before doing any work.

---

## Required workspace reading (Session 25 first 10 minutes)

In this order:

1. **`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`** — full
   handoff state at S24 close. Lists scope candidates (J new +
   A/B/D/E/H carry-forward) with prerequisites + estimated scope.
   The S25 scope choice at Phase 1 picks from these.

2. **`~/crawler-audit/SESSION_LOG.md`** Session 24 entry — what
   landed during Candidate I (3 commits). The 5 forward-applicable
   patterns folded into LESSONS at S24 close.

3. **`~/crawler-audit/LESSONS.md`** — 5 new sections folded at S24
   close, at end of file. Locate via
   `grep -n '^## .*(S24 folding)' LESSONS.md`. Especially:
   - "Tightened-precondition test-fixture retargeting" —
     applicable if Candidate J's ADLS completion tightens any
     preconditions on existing tests.
   - "Test against public API surface only" — DIRECTLY APPLICABLE.
     Candidate J's ADLSCostJournal mirrors LocalFSCostJournal's
     surface; tests should probe `.path` / behavior, not private
     `_journal_dir` / `_run_id` attrs.
   - "Q-I.7 'Both' test corpus shape works for small candidates"
     — applicable if Candidate J is small-medium scope.
   - "Q-I.6 'log + continue' closure-failure pattern" — not
     directly applicable to Candidate J (the ADLS backend is
     load-bearing for downstream correctness; persistence
     failures there should propagate, not log-and-continue).
   - "Workspace HEAD delta tolerance — eval_data-only path" —
     applicable at Phase 0 Step 0.1 for tolerating operator
     eval_data commits.

4. **`~/crawler-audit/BARCADA_CRAWLER_REMEDIATION_PLAN.md`** —
   chosen-scope section per Phase 1 candidate choice. Plan is
   READ-ONLY.

5. **`~/crawler-audit/CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8
   — only if Candidate A (barcada-drift) is chosen.

6. **`~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md`** —
   only if Candidate B (per-tier cost-accounting retrofit) is
   chosen. READ-ONLY.

7. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   — only if Candidate J is chosen. Read top-to-bottom; the
   Phase 5 skeleton is the work surface.

8. **`src/barcada_scraper/classifier/pipeline/cost_journal_local.py`**
   — only if Candidate J is chosen. ~176 LOC. The reference
   implementation Candidate J mirrors against ADLS (API contract
   + ETag semantics + lock semantics).

9. **`src/barcada_scraper/orchestrator/worker_loop.py`** lines
   2008-2113 — only if Candidate J is chosen. The 3-helper block
   (section header comment at 2008;
   `_open_cost_journal_for_worker` at lines 2014-2055;
   `_ensure_journal_initialized` at lines 2056-2081;
   `_build_durable_bypass_writer` at lines 2082-2113).
   `scrape_stage2_pages_invoker` starts immediately after at
   line 2114. Candidate J modifies the abfss:// guard inside
   `_open_cost_journal_for_worker` but preserves its signature.

10. **`tests/orchestrator/test_worker_loop_persistence.py`** at
    `00d5b38` — only if Candidate J is chosen. The 12 unit tests
    pin the S24 helpers' contracts. Candidate J may need to
    UPDATE the abfss:// rejection test
    (`test_open_cost_journal_abfss_raises_not_implemented_with_phase5_marker`)
    to a passing-through behavior, OR introduce a new helper
    that wraps the abfss:// dispatch separately. Phase 2 decides.

11. **`tests/classifier/pipeline/test_cost_journal_adls.py`** —
    only if Candidate J is chosen. The 2 existing tests pin the
    skeleton contract. Candidate J expands this file with full
    coverage of the new backend (`read` / `write_initial` /
    `try_update` / `exists` against an Azurite container or
    fsspec-adls mock or DummyADLS in-memory).

12. **`docs/CRAWLING_POLICY.md`** at `fdc8a7a` — only if
    Candidate H (doc tightening) is chosen.

---

## Phase 1 — Scope resolution (no code; pre-design-gate)

Operator picks one candidate. Candidates ordered by prerequisite-
readiness; each is independent.

### Candidate J — abfss:// CostJournal Phase 5 promotion (NEW; Recommended)

The natural follow-on to S24's Candidate I. Completes the
ADLSCostJournal skeleton + removes the abfss:// guard in
worker_loop's helper.

Scope:
- Complete `src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
  to implement the full `CostJournal` interface against ADLS Gen2
  (Azure Data Lake Storage). The skeleton already declares the
  class shape; implementation needs:
  - `read()` — read the state-file blob; compute ETag (likely the
    blob's native ETag or a SHA-256 over the body). Return
    `_ReadResult(state, etag)` or `None` if absent.
  - `write_initial(state)` — `PutBlob` with `If-None-Match: "*"`
    semantics (Azure blob "if not exists" precondition) to make
    initial writes race-safe. Raise `JournalAlreadyExistsError`
    on 412 Precondition Failed.
  - `try_update(*, expected_etag, new_state)` — `PutBlob` with
    `If-Match: <expected_etag>`. Returns True on 2xx, False on 412.
  - `exists()` — `HEAD` on the blob; True on 2xx, False on 404.
- Remove the abfss:// guard in
  `src/barcada_scraper/orchestrator/worker_loop.py`'s
  `_open_cost_journal_for_worker` (the `if url.startswith("abfss://"):
  raise NotImplementedError(...)` block). After removal, abfss://
  URLs flow through `open_journal(journal_dir=Path(url).parent, ...)`
  to construct an ADLSCostJournal.

  **NB**: `Path(url)` on a `abfss://acct/container/path/file.jsonl`
  URL won't parse cleanly under `pathlib.Path` (it treats `:` as
  a literal). Phase 2 Q-J.4 decides whether to use `fsspec.url_to_fs`
  to parse the URL, OR to keep the abfss:// → ADLSCostJournal
  routing inside `open_journal` (extending the factory's URL-
  scheme detection there instead of in the worker helper).

- Update
  `tests/classifier/pipeline/test_cost_journal_adls.py` from
  2 skeleton-marker tests to ~15-30 tests covering the new
  backend's full surface. Decision on test posture (Q-J.3) drives
  the test-corpus shape.
- Update
  `tests/orchestrator/test_worker_loop_persistence.py`'s
  `test_open_cost_journal_abfss_raises_not_implemented_with_phase5_marker`
  to instead verify that abfss:// URLs construct an
  ADLSCostJournal (NOT a LocalFSCostJournal). Q-I.7-style
  isolation preserved.
- Update
  `tests/orchestrator/test_robots_gate_integration.py`'s
  `test_invoker_abfss_cost_journal_url_raises_not_implemented`
  similarly OR delete it (the abfss:// rejection is no longer the
  contract; replaced by abfss:// dispatching to ADLS).

Estimated ~150-250 LOC of src/ changes (cost_journal_adls.py
completion) + ~200-400 LOC of test code (full ADLSCostJournal
coverage matching LocalFSCostJournal's 13 tests, scaled for
remote-storage edge cases) + ~5 LOC removal of the abfss:// guard
+ ~30 LOC of test updates to reverse the S24 rejection tests.
Total ~400-650 LOC. Likely the largest S25 scope; multi-commit
per-module.

**Prerequisites:**
- **All S24 public APIs stable** (Phase 0 Step 0.9 verifies).
  HALT if any drifted.
- **Test-posture decision** (Q-J.3) — must be pre-resolved at
  Phase 2 before Phase 3 begins. Three paths with very different
  blast radius:
  (a) Azurite container (real Azure-compatible storage in Docker;
      most realistic; requires Azurite available locally; tests
      are slower but verify against actual blob-storage semantics);
  (b) fsspec-adls mock (medium realism; doesn't exercise real
      ETag concurrency under load);
  (c) DummyADLS in-memory (no remote deps; fastest; lowest
      realism — risk of mocked-vs-prod divergence per the
      "integration tests must hit real boundaries" pattern).
- **URL parsing strategy** (Q-J.4) — how does the worker get from
  an `abfss://acct/container/path/file.jsonl` URL to a
  `journal_dir` + `run_id` pair for `open_journal`? Two paths:
  (a) Use `fsspec.url_to_fs` in the worker helper;
  (b) Move URL-parsing INTO `open_journal` (so worker just passes
      the URL string and `open_journal` decides scheme + dispatches).
- **Authentication strategy** (Q-J.5) — how does ADLSCostJournal
  acquire credentials? In production, vmss_worker.run() uses
  `DefaultAzureCredential` (managed identity). For ADLSCostJournal,
  the simplest is to use the same credential — but the credential
  itself may need to be threaded through `open_journal` (currently
  the factory accepts no credential argument).
- **Explicit Phase 2 authorization for src/ touches not in Out-of-
  scope's allow-list**: any cost_journal_adls.py / cost_journal.py
  touch beyond what Phase 2 authorizes HALTs per the S22-S24
  "Implicit-authorization HALT for src/-locks" LESSONS pattern.
  Candidate J specifically authorizes:
    - cost_journal_adls.py (NEW completion, was skeleton)
    - worker_loop.py (abfss:// guard removal in 1 helper)
    - test_cost_journal_adls.py (test expansion)
    - test_worker_loop_persistence.py (update 1 test)
    - test_robots_gate_integration.py (update or delete 1 test)
  No OTHER src/ files are authorized.

### Candidate A — `barcada-drift` (depends on AI/ML team alignment + ≥2 parquets)

Per `CLASSIFICATION_ADJACENT_PLAN.md` §Item 8. Consumes the
`canary_runs/<date>.parquet` artifacts the S20 launchd job
produces. Estimated ~300 LOC.

**Prerequisites:**
- 2+ `canary_runs/*.parquet` files exist on operator's machine.
  Earliest natural date: 2026-06-06 (two Saturdays from S20 close
  at 2026-05-23) assuming operator ran the launchd installer
  immediately after S20.
- AI/ML team responses on 4 §Item 8 decisions OR explicit
  operator-side placeholder choices with "AI/ML-to-tune" notes.

**HALT IF** the 4 AI/ML decisions are not pre-resolved going into
Session 25 AND operator has not authorized explicit placeholder
choices.

### Candidate B — Per-tier cost-accounting retrofit (closes Workstream 0)

The deferred-from-S14 per-tier cost-accounting wiring gap.
Currently severity LOW, carry-forward. Closing it would let
`workstream-0-end` tag be placed at the closing commit. Touches
the W4.1.5 driver area (`tests/runners/fixture_cascade/`) which
is locked except via W5.X-prefix commits per S16 precedent.
Estimated 100-200 LOC.

**Prerequisites:**
- Operator authorization at S25 Phase 1 for a W5.X-prefix commit
  touching the W4.1.5 driver. Without this auth, the candidate
  HALTs at Phase 1.
- Decision on whether the retrofit touches stage{1,2,3}_*_usd
  driver cost fields, per-row stage3_decision.evidence_cost_usd,
  or both.

### Candidate D — Phase 4 PR-D operator-led labeling (operator territory)

Per plan §11 Risk Register entry. Stage 2 + Stage 3 labeling
gates PR-D/E/F/G. Operator-led; Claude Code's role limited to
tooling.

**Prerequisites:**
- Operator-scheduled labeling effort.
- Claude Code's role limited to tooling around the labeling
  workflow.

### Candidate E — Cassette corpus expansion / additional fixtures

S20 shipped 20 cassettes; plan §4 W7 line 314 cites "~20-30
representative domains" — current 20 is the lower bound.

**Prerequisites:**
- Decision on which subset(s) to expand into.
- Operator review of S20's FP-curation log (archive.org +
  hashicorp.com flagged as SaaS-shell FPs; stripe.com WAF).

### Candidate H — CRAWLING_POLICY.md tightening pass

S22 shipped `docs/CRAWLING_POLICY.md` at 202 lines / 8.1 KB while
Q-F.6's "minimal-first" estimate cited ~1-2 KB. If operator
prefers a tighter doc, this candidate trims to ~2-3 KB while
preserving the essential robots-compliance contract.

**Prerequisites:**
- Operator decision on which sections to trim and which to
  preserve.

Estimated <50 LOC of doc changes; no code; <30 minutes.

### Sub-question 1.TAG — Tag at session close (pinned at Phase 1)

Independent of scope choice; resolved fully here at Phase 1 so
Phase 5 has an unambiguous tag decision. Options per scope:

- **Candidate J** (abfss:// promotion): defer OR place a
  candidate-specific tag (e.g., `cost-journal-phase-5-end`) —
  Phase 1 resolves.
- **Candidate A** (barcada-drift): defer OR place candidate-
  specific (e.g., `barcada-drift-v0`).
- **Candidate B** (per-tier cost-accounting): if it fully closes
  Workstream 0, place `workstream-0-end`. Otherwise defer.
- **Candidate D** (Phase 4 PR-D tooling): defer.
- **Candidate E** (cassette corpus expansion): defer.
- **Candidate H** (doc tightening): defer.

Phase 5 reads this resolution directly — no Phase 2 re-decision.

---

## Phase 2 — Design-gate elicitation (no code; AskUserQuestion)

Per chosen Phase 1 candidate. Each candidate has its own sub-
block. Source-verify at session-current HEAD per `[[verify-
before-asking-discipline]]` AND per S22-S24 "Plan-vs-reality at
Phase 2 source-verify" LESSONS pattern BEFORE each
AskUserQuestion batch.

**HALT IF** any Phase 2 decision would require modifications to
`src/barcada_scraper/` production code beyond what was Phase-2-
authorized (per S22-S24 "Implicit-authorization HALT for src/-
locks" LESSONS pattern; surface as an explicit AskUserQuestion
before patching) OR to the W4.1.5 driver (except via W5.X-prefix
per Candidate B's auth) OR to any S19-S24 deliverable — surface
as a design-gate sub-question before patching.

### If Candidate J (abfss:// CostJournal Phase 5 promotion)

- **Q-J.1 Backend implementation strategy**: (a) Direct
  `azure-storage-blob` SDK calls (most performant; matches
  vmss_worker's existing Azure deps; needs credential
  threading); (b) `fsspec.adlfs` filesystem wrapper (consistent
  with worker_loop's existing `fsspec.url_to_fs` pattern but
  adds ETag-precondition complexity since fsspec doesn't expose
  conditional-write primitives directly); (c) `azure-storage-
  file-datalake` (Gen2-specific SDK; cleanest API for ADLS
  semantics but new dependency).
- **Q-J.2 ETag source**: (a) Use Azure blob's native ETag header
  (string-quoted in headers; needs strip on read); (b) Hash the
  body with SHA-256 (matches LocalFSCostJournal's strategy;
  uniform across backends; ignores Azure's race-window).
- **Q-J.3 Test posture**: (a) Azurite container (real Azure-
  compatible storage in Docker; most realistic; CI-friendly with
  testcontainers); (b) fsspec-adls mock (no Docker; partial
  realism); (c) DummyADLS in-memory class implementing the same
  abstract methods (no remote deps; fastest; risk of mock-vs-
  prod divergence). Recommended (a) if Azurite is operator-
  available; else (c) with explicit follow-up TODO for real-
  storage integration in CI.
- **Q-J.4 URL parsing site**: (a) Inside `open_journal` —
  factory recognizes `abfss://` and parses to construct
  ADLSCostJournal (worker passes URL string raw); (b) Inside
  `_open_cost_journal_for_worker` — worker parses URL via fsspec
  before calling `open_journal`. Recommended (a) — centralizes
  URL-shape knowledge in the factory; worker stays scheme-
  agnostic.
- **Q-J.5 Authentication threading**: (a) ADLSCostJournal takes
  an optional `credential` kwarg defaulting to
  `DefaultAzureCredential()`; (b) ADLSCostJournal reads
  credentials from environment variables at construction
  time; (c) ADLSCostJournal is constructed with the credential
  injected by the worker's run() function (requires plumbing
  through `open_journal`). Recommended (a) — keeps the API
  ergonomic for tests + production.
- **Q-J.6 Concurrent-write semantics (Phase 2 source-verify, NOT
  an operator design gate)**: BEFORE the Q-J.* AskUserQuestion
  batch, Claude Code MUST source-verify that Azure's
  `If-None-Match: "*"` precondition on `PutBlob` returns 412
  Precondition Failed when the blob already exists — and that
  this maps cleanly to LocalFSCostJournal's race-loser
  `JournalAlreadyExistsError` semantics. The expected mapping:
    - Azure 412 Precondition Failed → catch in ADLSCostJournal →
      raise `JournalAlreadyExistsError` with the blob path.
    - Race winner: 2xx response; first `write_initial` succeeds.
    - Race loser: 412; `JournalAlreadyExistsError` propagates.
  Mirrors S24 Q-I.3's source-verify pattern (not an
  AskUserQuestion option pick; a fact-vs-design boundary item).
  If source-verification confirms the mapping holds, design
  proceeds. If Azure has eventual-consistency or different status
  semantics that break the precondition (unlikely for ADLS Gen2
  which is strongly consistent on blob writes per Azure docs),
  HALT and surface for a re-shaped Phase 2 elicitation that
  preserves the race-loser-raises-JournalAlreadyExistsError
  contract via a different mechanism.

  Verify via the azure-storage-blob SDK docs or a small Azurite
  smoke (if Q-J.3 elects Azurite posture). Cite the exact API
  call signature in Phase 2 documentation before proceeding to
  the AskUserQuestion batch.
- **Q-J.7 Test corpus shape**: (a) Extend
  `test_cost_journal_adls.py` from 2 skeleton tests to a full
  suite (~15-30 tests) covering each method's happy path +
  failure path + concurrency cases. Mirror LocalFSCostJournal's
  13 tests structure but add ADLS-specific cases (auth failure,
  blob-not-found, transient 5xx); (b) Add a new top-level
  integration test file driving worker_loop with abfss://
  cost_journal_url AND verifying the journal lands in Azurite.
  Recommended (a) + (b) "Both" style per Q-I.7 precedent —
  unit tests + integration tests together.
- **Q-J.8 Existing-test updates**: confirm that the 2 S24-landed
  abfss:// rejection tests
  (`test_open_cost_journal_abfss_raises_not_implemented_with_phase5_marker`
  in test_worker_loop_persistence.py;
  `test_invoker_abfss_cost_journal_url_raises_not_implemented`
  in test_robots_gate_integration.py) are REPLACED in place with
  passing-through tests that construct an ADLSCostJournal (and
  assert the type / dispatch path). The S24 LOCK on those 2
  tests is RELAXED here by explicit Phase 2 authorization, but
  ONLY for replacement — deletion and skipif-markers are NOT
  authorized:
    - Deletion would lose abfss:// dispatch coverage entirely
      from the regression suite.
    - skipif-markers risk silent test-skips in CI when Azurite
      isn't configured (failure mode: regression slips through
      because the only coverage test was conditionally skipped).
  Replacement is a net-zero test-count operation (1↔1 per file).
  Yes/no confirmation that the operator authorizes the
  replacement; no option-pick.

### If Candidate A (barcada-drift)

Carry-forward from S22-S24 prompts (unchanged).
- Q-A.1 CLI namespace; Q-A.2 drift metric; Q-A.3 alert threshold;
  Q-A.4 input contract; Q-A.5 output shape; Q-A.6 test corpus.

### If Candidate B (per-tier cost-accounting retrofit)

Carry-forward from S22-S24 prompts (unchanged).
- Q-B.1 scope of fields; Q-B.2 backfill behavior; Q-B.3 test
  approach; Q-B.4 W5.X-prefix commit shape; Q-B.5
  workstream-0-end tag.

### If Candidate D (Phase 4 PR-D tooling)

- **Q-D.1 Tooling shape**: batch validators / import scripts /
  hygiene tools. Operator-led design.

### If Candidate E (cassette corpus expansion)

- **Q-E.1 Target count**: 30 (plan's upper bound) vs 25 vs stay
  at 20.
- **Q-E.2 Subset focus**: bot-blocked vs non-English vs more
  business-classification-interesting domains.
- **Q-E.3 FP re-investigation**: re-record archive.org +
  hashicorp.com under different UA OR drop them OR keep as-is.

### If Candidate H (CRAWLING_POLICY.md tightening)

- **Q-H.1 Target size**: ~2 KB tight (operational reference) vs
  ~3 KB mid (operational + bypass policy detail).
- **Q-H.2 Section removals**: which of (Crawler identity / robots
  compliance / Bypass-config policy / Operational defaults table /
  Out-of-scope deferrals / References) to trim or remove.
- **Q-H.3 Reviewer audience**: assume the doc is read by ops
  (favor operational defaults) vs by compliance (favor bypass
  policy) vs both.

### Shared sub-questions (all candidates)

- **Q-SHARED.1 Commit shape**: per-module (S18-S24 default;
  Recommended) vs per-sub-surface bundled.

(Tag-at-close is resolved at Phase 1 Sub-question 1.TAG; Phase 5
reads that resolution directly without re-decision.)

---

## Phase 3 — Implementation (per-module commits, strict order)

Per Phase 2 commit-shape decision. Default = per-module. Each
commit must satisfy the 6-step per-commit checkpoint protocol
below.

### Non-interleaving rule (CRITICAL for bisectability)

If the chosen candidate has multiple sub-surfaces (Candidate J
clearly does: ADLSCostJournal impl + worker_loop guard removal +
new ADLS tests + updates to S24 tests), do NOT interleave.
Complete each sub-surface fully before starting the next. Per
S22-S24 precedent.

If a mid-sub-surface dependency on the other sub-surface emerges,
HALT and surface as a design-gate sub-question before continuing
— the dependency may indicate a Phase 2 question was missed. See
S23-folded LESSONS "Bisectability vs Phase-1-named commit shape"
and S24-folded "Tightened-precondition test-fixture retargeting"
for patterns.

### Recommended Candidate J commit order

1. **cost_journal_adls.py** — implement the ADLSCostJournal
   backend. Standalone change; no other consumers depend on the
   completion. Tests in `test_cost_journal_adls.py` updated in
   THIS commit (bundle src + tests like S24 Commit 1 to preserve
   bisectability) — the 2 existing skeleton-marker tests will
   regress at the new behavior; replace them with full coverage
   in the same commit.
2. **worker_loop.py abfss:// guard removal** — small src change
   (~5 LOC) PLUS update the 2 S24 tests
   (`test_open_cost_journal_abfss_raises_not_implemented_with_phase5_marker`
   in `test_worker_loop_persistence.py` AND
   `test_invoker_abfss_cost_journal_url_raises_not_implemented`
   in `test_robots_gate_integration.py`) in the same commit
   (same bundle-coupled rationale as S24 Commit 1).
3. **End-to-end Azurite test** (only if Q-J.7 = "Both") — new
   file or new tests appended to an existing integration file
   driving worker_loop with abfss:// against Azurite.

### Per-commit checkpoint protocol (single source of truth)

At EVERY Phase 3 commit boundary, run these 6 steps IN ORDER:

**1. Combined suite**

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
    tests/orchestrator/test_worker_loop_persistence.py \
    <new S25 test paths if any> -q
```

Expected: previous_baseline + N new tests, all passing. If
failing tests are NOT a deliberate consequence of the surface-
under-test → HALT.

**2. Ruff sanity (touched files only) + mid-implementation format
check per LESSONS**

```
.venv/bin/ruff check <touched paths>
.venv/bin/ruff format --check <touched paths>
```

If unclean → run `ruff format <touched paths>` and re-test; fold
the format-fix into the commit (per S19-S24 pattern).

**3. Verification table (build in chat per `[[double-check-before-
commit]]` strict rule)**

```
| Claim                          | Reality      | Status |
| ------------------------------ | ------------ | ------ |
| <every concrete claim in       | <verified    | ✓ / ✗  |
|  the draft commit message>     |  via source> |        |
```

Any ✗ → fix the claim in the commit message BEFORE staging.

Per S23 LESSONS "Cumulative test-count gate with new-file
invocation expansion": distinguish in the commit body between
net-new tests (added this commit) and newly-in-invocation pre-
existing tests (file joined the gate this commit).

For exit-code claims: use
`cmd > /tmp/out 2> /tmp/err; echo "Exit: $?"` to avoid the
bash-pipe-exit-code-masking pattern (LESSONS).

**4. `git status` check**

Only intended files staged; no surprise `eval_data/` or
unauthorized `src/barcada_scraper/` changes. Operator-side
`eval_data/` modifications are expected to stay unstaged across
sessions (Sessions 8-24 precedent).

**5. "Confirm to commit?" presented to operator**

Include in chat:
- Verification table from step 3
- Commit message file location (`/tmp/<id>-msg.txt`)
- File list to stage (M / A / D)

**6. After operator confirms**

Stage + commit + verify the new SHA landed
(`git log --oneline -1`) + verify combined suite still passes on
the new HEAD.

This 6-step protocol applies UNIFORMLY to every commit in Phase 3
(and Phase 6's workspace close-out commit). Mechanical; do not
skip steps.

### Cumulative test-count gate

Track combined-suite passing count at each commit boundary:

```
Phase 3 start                  : 947  (Session 24 close baseline)
After commit 1                 : >= 947 + N_commit_1_tests
After commit 2                 : >= 947 + N_commit_1_tests + N_commit_2_tests
...
```

**Rule**: the count NEVER decreases between checkpoints. A
decrease means a previously-passing test went red — regression.
HALT.

**The Q-J.7 commit-1 test-count exception is the ONLY decrease
authorized in S25. Any other count decrease HALTs.** Candidate J's
commit 1 replaces the 2 existing `test_cost_journal_adls.py`
skeleton-marker tests with N net-new ADLS-coverage tests; the
gate goes 947 → 947 − 2 + N. To distinguish this *one
intentional replacement* from a regression, commit 1's body MUST
include:
  (a) the 2 named replaced tests (the existing skeleton markers);
  (b) the value of N and the names of the N new tests;
  (c) explicit citation of the S24-folded LESSONS
      "Tightened-precondition test-fixture retargeting" pattern —
      same shape (precondition tightening from skeleton-rejection
      to real-backend-passes-through), different precondition than
      S24's abfss://-rejection-to-file://-only.

Do not generalize this carve-out. Future readers MUST NOT
interpret "intentional replacement" as a blanket exception; the
only path-set whose tests may shrink in S25 is
`tests/classifier/pipeline/test_cost_journal_adls.py` in commit 1,
and only by the exact 2-test delta named above. Q-J.8's
replacement of 2 abfss://-rejection tests in
test_worker_loop_persistence.py + test_robots_gate_integration.py
is a NET-ZERO operation (1 replaced ↔ 1 replaced per file; count
unchanged) — not an exception to this rule.

Baseline pre-resolved at Phase 1 per Phase 0 Step 0.5: 947 is the
canonical S25 baseline for any candidate that touches the
orchestrator sub-surface (Candidate J definitely; Candidates B/E
likely; Candidate H not). Whichever baseline is bound at Phase 1,
hold it consistent across ALL Phase 3 commits in S25 — do not
switch mid-session.

---

## Phase 4 — Pre-push gate (whole-tree)

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 351+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

HALT IF any gate red. Never use `--no-verify`.

### eval_data WIP halt protocol (per LESSONS)

validate_consistency runs against working-tree state. Operator-WIP
edits to `eval_data/*.jsonl` can introduce schema violations that
fail the gate even though no S25 commit touches eval_data.

When this fires:
1. Confirm the failing row's content is in operator-WIP
   (`git diff eval_data/...`), not in committed HEAD
   (`git show HEAD:eval_data/...`).
2. Confirm the S25 commits do not touch eval_data
   (`git diff origin/main..HEAD -- eval_data/`).
3. Surface to operator with the exact row + reason + diff vs
   committed state.
4. Two paths: (a) operator-fix in WT, then re-run gate;
   (b) stash eval_data WIP, push, restore.
5. Do NOT auto-fix locked-artifact content.

S20+S22 precedent: operator chose (a). S21/S23/S24 did not need
this protocol at Phase 4 push.

---

## Phase 5 — Push + tag

- Push to `origin/main` after operator confirms.
- Tag per Phase 1 Sub-question 1.TAG decision (or defer).

If a workstream-end tag is placed: include annotated message
summarizing all the workstream's work (mirror the
`workstream-a-week1-end` annotation pattern from S22 — name
every sub-surface commit + map to plan bullets + list any
deferrals).

---

## Phase 6 — Workspace close-out

- Append Session 25 entry to `~/crawler-audit/SESSION_LOG.md`
  including a **Canonical S25-close baseline** block with the
  exact pytest invocation + verified test count (per S22-S24
  LESSONS "Pin the S25 baseline for Phase 0 Step 0.5"; without
  this, S26 Phase 0 will infer from the "Combined headline"
  bullet and potentially HALT on accounting-mismatch).
- Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md` for
  Session 26 — explicitly pin the S26 Phase 0 workspace anchor
  SHA per S21-S24 post-audit pattern (LESSONS "Workspace HEAD
  delta tolerance"); do not omit. After the close-out commit
  lands, expect **1-2 follow-up commits** pinning the actual
  SHA (S21 needed 1; S22 needed 2 — the second pinned the
  canonical baseline test count discovered during audit; S23/S24
  needed 1).
- Update `~/crawler-audit/LESSONS.md` with any new forward-
  applicable patterns surfaced this session.
- Workspace close-out: 1 primary commit + 1-2 follow-up commits
  pinning the anchor SHA and any audit-surfaced corrections.
  Push workspace after operator confirms.

Note: drafting the next-session prompt (`SESSION_26_PROMPT.md`)
is NOT a built-in Phase 6 step. Per S20→S21, S21→S22, S22→S23,
S23→S24, S24→S25 precedent, prompt-drafting is an operator-
commissioned activity between sessions — not always-on close-out
work. If the operator asks for it explicitly at S25 close, draft
it as a separate follow-up; otherwise leave for the next session
to either operator-commission or scope out at S26 open.

---

## Acceptance criteria

**Per candidate (reduces if Phase 1 narrows scope):**

### Candidate J (abfss:// CostJournal Phase 5 promotion)

1. ADLSCostJournal in `cost_journal_adls.py` implements all four
   abstract methods (`read`, `write_initial`, `try_update`,
   `exists`) per the CostJournal contract.
2. `JournalAlreadyExistsError` raised on race-loser of
   `write_initial` per Q-J.6.
3. ETag protocol per Q-J.2 implemented + tested.
4. URL-parsing strategy per Q-J.4 implemented; the abfss:// guard
   in `_open_cost_journal_for_worker` removed and abfss:// URLs
   flow through `open_journal` to ADLSCostJournal.
5. Authentication strategy per Q-J.5 implemented.
6. Test corpus per Q-J.7 in place — at minimum a unit-test file
   replacing the 2 skeleton-marker tests with full-method
   coverage; Q-J.7 (b) "Both" adds end-to-end Azurite/mock
   integration tests.
7. The 2 S24 tests that pinned the abfss:// rejection contract
   are REPLACED in place per Q-J.8 with passing-through tests
   that construct an ADLSCostJournal (1↔1 per file; net-zero
   test-count change). Deletion and skipif-markers are NOT
   authorized (would lose abfss:// dispatch coverage). Explicit
   Phase 2 authorization for the replacement is documented in
   the commit body citing Q-J.8.
8. All S23 + S24 deliverables stay at their landed SHAs (their
   public APIs unchanged; the 3 S24 helpers'  signatures
   preserved; only the abfss:// guard body changes).
9. Tag per 1.TAG (defer OR candidate-specific).

### Candidate A (barcada-drift)

Carry-forward from S22-S24 prompts (unchanged):
1. `barcada-drift` (or `barcada-baseline drift`) CLI works
   against ≥2 canary_runs parquets.
2. Drift metric per Q-A.2 implemented + tested.
3. Alert threshold per Q-A.3 implemented + tested.
4. Output shape per Q-A.5 documented + tested.

### Candidate B (per-tier cost-accounting retrofit)

Carry-forward from S22-S24 prompts (unchanged):
1. Per-tier cost fields populated per Q-B.1 scope.
2. Backfill behavior per Q-B.2 executed.
3. Test coverage per Q-B.3 in place.
4. `workstream-0-end` tag placed if per-tier accounting fully
   closes the gap (Q-B.5).

### Candidate D (Phase 4 PR-D tooling)

1. Tooling shape per Q-D.1.

### Candidate E (cassette corpus expansion)

1. Cassette count grows to Q-E.1 target.
2. FP re-investigation per Q-E.3 if applicable.

### Candidate H (CRAWLING_POLICY.md tightening)

1. Doc size meets Q-H.1 target (±10%).
2. Removed sections per Q-H.2; preserved sections still
   self-contained.
3. Reviewer audience tone per Q-H.3.

### Shared (all candidates additionally satisfy)

Items numbered S1-S4 to avoid collision with candidate-specific
numbering.

- **S1.** Combined suite at session close: existing 947 baseline
  + N new tests, all passing (Candidate J expectation). For
  narrower-baseline candidates (H), the baseline is the chosen
  narrower count + N new.
- **S2.** Pre-push gate runs green (incl. eval_data WIP halt
  protocol applied if needed).
- **S3.** Tag placed per Phase 1 Sub-question 1.TAG OR explicit
  defer.
- **S4.** Regression-protection checklist held (see "Out-of-scope"
  below). In particular: ALL S21-S24 deliverables stay at the
  SHAs they landed at; their public APIs are unchanged. The 32
  robots-parser tests stay 32/32 green; the 30 robots_gate tests
  stay 30/30 green; the 30 robots_bypass_config tests stay 30/30
  green; the 43 cost_journal tests stay 43/43 green; the 13
  cost_journal_local tests stay 13/13 green; the 35
  robots_integration tests stay 35/35 green; the 74 vmss_worker
  + 129 job_runner + 152 worker_loop tests stay green (or grow);
  the 7 integration tests stay 7/7 green (modulo Q-J.8 updates
  to 1 test); the 12 worker_loop_persistence tests stay 12/12
  green (modulo Q-J.8 updates to 1 test). The 2 cost_journal_adls
  tests get REPLACED with a fuller suite per Q-J.7; this is the
  ONLY intentional test-count change in Candidate J.

---

## Out-of-scope (no exceptions without operator authorization)

Per the regression-protection checklist:

**S19 deliverables (Sessions 19 check sub-surface):**
- `tools/baseline_v0/check.py`
- `tests/baseline_v0/test_check.py` (24 tests)
- 6 check-dispatch tests in `tests/baseline_v0/test_cli.py`

**S20 deliverables (Sessions 20 cassettes + canary sub-surfaces):**
- `tools/synthetic_crawl/` package (4 files)
- `tools/baseline_v0/canary.py`
- `canary-run` subparser additions in `tools/baseline_v0/cli.py`
- `tests/synthetic_crawl/` package (3 files; 33 tests)
- `tests/baseline_v0/test_canary.py` (17 tests)
- 6 canary-dispatch tests in `tests/baseline_v0/test_cli.py`
- `tests/fixtures/synthetic_crawls/` (40 files: 20 cassettes + 20
  sidecars)
- `scripts/launchd/` (5 files)
- `pyproject.toml` vcrpy>=8.1 entry in dev extras
- `.gitignore` canary_runs/ entry

**S21 deliverables (Session 21 W A.1 robots-parser sub-surface):**
- `src/barcada_scraper/scraper/robots.py` (parser module; 282 LOC;
  public API at `34a59b6`).
- `tests/scraper/test_robots.py` (32 tests; pins stdlib quirks).

**S22 deliverables (Session 22 W A.1 W8 integration sub-surfaces):**
- `src/barcada_scraper/scraper/robots_gate.py` (shim; 339 LOC;
  public API at `ba87e7e`).
- `tests/scraper/test_robots_gate.py` (30 tests).
- `src/barcada_scraper/scraper/robots_bypass_config.py` (loader;
  178 LOC; public API at `381ee89`).
- `tests/scraper/test_robots_bypass_config.py` (30 tests).
- The S22 additions to `src/barcada_scraper/classifier/pipeline/
  cost_journal.py` are LOCKED at `1d9404e`. Candidate J consumes
  `CostJournal`, `JournalState`, `JournalAlreadyExistsError`,
  `update_with_retry`, `open_journal` but MUST NOT modify their
  landed S22 shapes. **HOWEVER**, Q-J.4 may authorize MOVING the
  abfss:// scheme detection into `open_journal` (the factory) —
  this is an ADDITIVE modification to the dispatcher's body, NOT
  a public-API break. Document in commit body if Q-J.4 routes
  through option (a).
- The S22 additions to `tests/classifier/pipeline/test_cost_journal.py`
  (14 new tests + 1 updated test) are locked.
- `docs/CRAWLING_POLICY.md` (202 lines; at `fdc8a7a`). Candidate H
  is the ONLY candidate that may modify this file.

**S23 deliverables (Session 23 W A.2 sub-surfaces):**
- `src/barcada_scraper/orchestrator/robots_integration.py`
  (244 LOC; public API at `279bb77`). Candidate J CONSUMES
  `record_bypass_audit` (transitively via the durable writer)
  but MUST NOT modify.
- `tests/orchestrator/test_robots_integration.py` (35 tests at
  `279bb77`). Locked.
- The S23 additions to `src/barcada_scraper/orchestrator/
  vmss_worker.py` at `5eeaac7`. Locked.
- The S23 additions to `tests/orchestrator/test_vmss_worker.py`
  (7 new tests). Locked.
- The S23 additions to `src/barcada_scraper/orchestrator/
  job_runner.py` at `872527e`. Locked.
- The S23 additions to `tests/orchestrator/test_job_runner.py`
  (8 new tests). Locked.
- The S23 additions to `scripts/vmss/cloud_init.template.yaml`.
  Locked.
- The S23 additions to `src/barcada_scraper/orchestrator/
  worker_loop.py` at `4ec7b0a` (gate construction + prewarm +
  3-site gate wiring). Locked.
- The S23 additions to `tests/orchestrator/test_worker_loop.py`
  (6 new tests at `4ec7b0a`). Locked.
- The 4 S23 tests in `tests/orchestrator/test_robots_gate_
  integration.py` (lines 144-332 of the file at the S23-landed
  shape). Locked.

**S24 deliverables (Session 24 W A.2 sub-surfaces — NEW for S25
lock-list):**
- The 3 module-level private helpers in
  `src/barcada_scraper/orchestrator/worker_loop.py` at `48c324a`:
  `_open_cost_journal_for_worker`, `_ensure_journal_initialized`,
  `_build_durable_bypass_writer`. Candidate J MODIFIES the body
  of `_open_cost_journal_for_worker` (removes the abfss:// guard;
  ~5 LOC delta) but MUST preserve the signature and the other
  two helpers entirely. Modifying signatures requires explicit
  Phase 2 authorization.
- The 3-line wiring block in `scrape_stage2_pages_invoker` at
  `48c324a`. Locked.
- The 5 retargeted test_stage2_pages_invoker_* fixtures in
  `tests/orchestrator/test_worker_loop.py` at `48c324a`. Locked
  — do NOT revert to abfss://.
- `tests/orchestrator/test_worker_loop_persistence.py` at
  `00d5b38` (12 tests). Candidate J REPLACES exactly 1 test per
  Q-J.8:
  `test_open_cost_journal_abfss_raises_not_implemented_with_phase5_marker`
  → replace with `test_open_cost_journal_abfss_constructs_adls_journal`
  (or similar) — 1↔1; net-zero test-count change for this file.
  Deletion is NOT authorized. All 11 other tests MUST stay
  unchanged. The Phase 2 authorization required to modify this
  S24-landed test is explicit in Q-J.8.
- The 3 S24-added tests in
  `tests/orchestrator/test_robots_gate_integration.py` at
  `aa23712`. Candidate J REPLACES exactly 1 test per Q-J.8:
  `test_invoker_abfss_cost_journal_url_raises_not_implemented`
  → replace with a passing-through test asserting an
  ADLSCostJournal is constructed (1↔1; net-zero test-count
  change for this file). Deletion is NOT authorized. The 2
  other S24 tests in this file
  (`test_invoker_persists_bypass_audit_through_production_wiring`,
  `test_invoker_helpers_export_intact`) MUST stay unchanged.

**W4.1.5 driver orchestration (locked since W4.1.5 close):**
- `tests/runners/fixture_cascade/` (except via W5.X-prefix commit
  with explicit operator auth — only Candidate B opens this with
  Q-B.4 W5.X-prefix decision)

**Baseline-v0 ground truth:**
- The committed `tests/fixtures/baseline-v0/` snapshot at `9e9a1fb`
  (1213 files)

**Existing W6 sub-surface (Session 18):**
- `tools/baseline_v0/generate.py`
- `tools/baseline_v0/determinism.py`
- Existing `generate` subparser in `tools/baseline_v0/cli.py`

**Schemas + plans (locked):**
- `expected.schema.json` v1.1
- `META_SCHEMA.md` v1.1
- `meta.schema.json` v1.0
- `stage1.schema.json` v1.0
- All workstream tags at their placed SHAs (10 tags as of S24
  close; new tags only via Phase 5 explicit placement)
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` (READ-ONLY)
- `CLASSIFICATION_ADJACENT_PLAN.md` (UPDATED only when AI/ML
  decisions land)
- `RECONCILIATION_2026-05-21.md`
- `docs/phase4_implementation_plan.md` (Phase 4 governance
  reference)

**Operator-owned territory:**
- All of `eval_data/` — labeling-workstream territory; per-row WIP
  edits across sessions are expected and unstaged (Sessions 8-24
  precedent). S22→S23+ inter-session operator-side eval_data
  COMMITS are tolerated per the "Workspace HEAD delta tolerance"
  LESSONS pattern — verify they're eval_data-only via
  `git show --stat <sha>` for each commit in the delta.

**Production code:**
- `src/barcada_scraper/` — locked unless Phase 2 design-gate
  explicitly authorizes a specific module. S21-S24 authorized:
  `scraper/robots.py`, `scraper/robots_gate.py`,
  `scraper/robots_bypass_config.py`,
  `classifier/pipeline/cost_journal.py` (additive only),
  `orchestrator/robots_integration.py` (new),
  `orchestrator/vmss_worker.py` (additive),
  `orchestrator/job_runner.py` (additive),
  `orchestrator/worker_loop.py` (additive: S23 gate wiring +
  S24 persistence helpers). Those authorizations do NOT extend
  to other src/ modules or to further modifications of the
  authorized files beyond their landed S21-S24 shapes.
  Candidate J authorizes: `classifier/pipeline/cost_journal_adls.py`
  (skeleton → full backend) AND a 5-LOC delta in
  `orchestrator/worker_loop.py`'s `_open_cost_journal_for_worker`
  body (abfss:// guard removal). NO other src/ touches without
  Phase 2 sub-question authorization.

**Pipeline configs:**
- `configs/`

**Phase 4 work:**
- Phase 4 PR-D/E/F/G work opens only when Workstream 0 fully
  closes AND operator-led Stage 2/3 labeling work begins.

---

## Verify-before-asking discipline (strict rule from S19-S24)

Per `[[double-check-before-commit]]` memory: **ALWAYS verify
every concrete claim in the commit message against actual source/
output BEFORE staging.** Fixture names, file counts, exit codes,
line counts, test counts, helper names, smoke outcomes, SHA
prefixes, regex matches, API signatures. No claims by pattern-
completion. Build a verification table in chat (claim → reality →
status) and reconcile before "Confirm to commit?".

Specific to S25:

- Before each chosen-candidate-specific claim in a commit message,
  verify against the actual source / runtime output:
  - Candidate J: `ADLSCostJournal` instantiation actually works
    against the chosen test posture (Azurite / fsspec mock /
    DummyADLS); `_open_cost_journal_for_worker(config)` with
    abfss:// URL constructs an ADLSCostJournal (NOT a
    LocalFSCostJournal, NOT a NotImplementedError); the 12
    other tests in `test_worker_loop_persistence.py` still pass
    unchanged; the 4 S23 tests + 2 unchanged S24 tests in
    `test_robots_gate_integration.py` still pass.
  - Candidate B: per-tier cost-journal field presence.
  - Candidate E: cassette counts post-record.
  - Candidate H: doc byte count post-trim matches Q-H.1 target.
- Before claiming combined suite count, re-run pytest.
- Before claiming ruff/format clean, re-run ruff against the
  touched files.
- Before claiming a SHA prefix in a commit message body, verify
  the prefix is correct via `git show --no-patch --format=%h <ref>`.

Avoid bash pipe artifacts that mask Python exit codes (LESSONS):
`python_cmd 2>&1 | grep ... | tail` makes `$?` reflect tail's
exit. Use `> stdout.out 2> stderr.err; echo $?` or
`${PIPESTATUS[0]}` when exit-code matters.

LESSONS-folded discoveries from S22-S24 worth re-applying if S25
takes Candidate J:

- **Plan-vs-reality at Phase 2** (S22 LESSONS): plan §5 wording
  may name a module/site that doesn't match the actual code
  shape. Verify the actual integration site via Explore BEFORE
  drafting Q-J.* options. For Candidate J specifically,
  source-verify `cost_journal_adls.py` at S25 Phase 0 to confirm
  the skeleton is still NotImplementedError-only and hasn't been
  partially completed between S24 close and S25 open.

- **Implicit-authorization HALT** (S22-S24 LESSONS): Q-J.*
  answers may require touching files NOT in S25 Out-of-scope's
  authorized-touch list (e.g., introducing a new helper module
  for ADLS-specific URL parsing). Surface explicit authorization
  in Phase 2 BEFORE the commit, not as a HALT mid-Phase-3.

- **Tightened-precondition test-fixture retargeting** (S24
  LESSONS): if Candidate J introduces stricter preconditions on
  any tests beyond the 2 explicitly named in Q-J.8, retarget
  those fixtures in the same commit as the src change. Bundle
  for bisectability.

- **Test against public API surface only** (S24 LESSONS):
  ADLSCostJournal tests should probe behavior via the public
  CostJournal abstract methods (`read`, `write_initial`,
  `try_update`, `exists`) + the `.path` property. Avoid
  asserting on private attrs or internal state.

- **Source-verify line numbers per Phase 3 commit** (S23
  LESSONS): worker_loop.py is now ~2989 LOC post-S24 (~2884
  pre-S23 + ~109 S23 additions + ~115 S24 additions); the
  `_open_cost_journal_for_worker` helper alone occupies
  lines 2014-2055 (its `if url.startswith("abfss://"):` guard
  block is at ~2033-2038 — the seam Candidate J removes).
  Re-Explore at session-current HEAD before drafting commit
  edits; line numbers shift as commits land.

- **Q-I.6 "log + continue" closure-failure pattern** (S24
  LESSONS): applies at the CLOSURE layer unchanged — the durable
  writer closure built by `_build_durable_bypass_writer` still
  swallows + LOG.exception's on persistence failure. What's new
  at Candidate J's ADLS-backend layer is the INVERSE rule:
  ADLSCostJournal MUST RE-RAISE on persistence failure
  (transient 5xx, auth failure, ETag exhaustion) so
  `update_with_retry`'s budget can do its job. The closure
  consumes whatever escapes that retry budget and applies Q-I.6
  there. Two layers, two opposite policies — both correct:
    - Backend (ADLSCostJournal): re-raise → enables retry +
      load-bearing failure surfacing.
    - Retry helper (update_with_retry): re-raise after budget
      exhaustion → enables closure to decide policy.
    - Closure (_build_durable_bypass_writer's _writer): swallow
      + LOG.exception → Q-I.6 unchanged, scrape availability
      preserved.

---

## Commit hygiene (per LESSONS + S19/S20/S21/S22/S23/S24 additions)

- File-based commit messages at `/tmp/<id>-msg.txt`.
- Per-module commits (Phase 3 commit shape unless Q-SHARED.1
  overrides).
- "Confirm to commit?" before EVERY commit. Pair with verification
  table (always) and `git diff --staged` (when appropriate per
  `[[double-check-before-commit]]` triggers).
- Commit body includes: action ref (e.g., `WA2.W8.adls-promotion`
  or `WJ.adls-promotion` — operator picks the prefix at Phase 1),
  scope summary, file touches, test count delta (with net-new vs
  newly-in-invocation pre-existing distinction per S23 LESSONS),
  plan reference. NO `Co-Authored-By`.
- Pre-push gate must run green. Never use `--no-verify`.
- Pre-push vermin: `git ls-files '*.py' | xargs vermin
  --target=3.10` to filter venv-internal pytest 3.14 false-
  positives.
- Mid-implementation ruff format-check, not only pre-push.
- For S24-test modifications: Q-J.8 explicit authorization
  required; document the modification scope (1 test in
  test_worker_loop_persistence.py + 1 test in
  test_robots_gate_integration.py) explicitly in the commit
  body (per S22-S24 LESSONS "Implicit-authorization HALT" pattern).
- Workspace close-out (Phase 6) lands as its own commit at session
  close, followed by 1 follow-up commit pinning the anchor SHA
  for the next session (S21-S24 pattern).

---

## Context-window awareness

S24 ran across 3 commits + Phase 2 source-verification +
1 mid-Phase-3 fixture-retargeting adjustment, well within
context. S25 budget per scope:

- Candidate J: medium-large (~400-650 LOC; ADLS backend
  completion + worker_loop guard removal + test corpus
  expansion). Likely needs 2-4 per-module commits.
- Candidate A: medium-large (~300 LOC).
- Candidate B: small-medium (100-200 LOC; sensitive driver-area
  touch).
- Candidate D/E: small.
- Candidate H: very small (<50 LOC of doc edits; <30 minutes).

Strategies:
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore
  subagent per S22-S24 "Explore-subagent + spot-check" LESSONS
  pattern.
- For Candidate J specifically, the ADLS backend implementation
  likely needs prototype-then-test cadence: implement one method
  + its tests, verify it works against the chosen posture, then
  the next method.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before the chosen S25 scope closes,
  transition per "no mid-commit-batch transitions" — finish
  in-flight sub-surface, then close session and refill the
  transition template for Session 26.

---

## Reporting in chat at session close

After all Session 25 commits land + push + close-out per the
S13-24 pattern:

1. Commit SHA(s) of each S25 sub-surface.
2. Sub-surface(s) landed (per candidate).
3. Test count delta: 947 (or 480/538/932) baseline → S25 close.
4. Driver suite count at S25 close (46/46 expected unless
   Candidate B W5.X-prefix realigned).
5. Files touched per sub-surface.
6. Tag dispositions (incl. any new tag per 1.TAG).
7. Per-tier cost-accounting wiring gap disposition: patched
   (Candidate B) or carry-forward.
8. abfss:// CostJournal promotion disposition: shipped
   (Candidate J) or carry-forward.
9. Any spend (LLM, infrastructure, cassette-capture).
10. Robots.txt compliance log (if Candidate J did live work
    against Azurite or Candidate E expanded the cassette corpus).
11. FP-curation log update (if Candidate E expanded the cassette
    corpus).
12. Verify-before-asking summary: any source-verification
    findings surfaced.
13. Outstanding items for Session 26.
14. Tags state at S25 close.

Do not propose Phase 4 PR-D/E/F/G work this session unless
Candidate D was chosen and operator-led labeling is in flight.

---

## Carry-forward bakes (no amendment file needed)

All S24 amendments (close-out commit `229b6f7` + follow-up
`763fd1a`) plus the S24 post-close verification have been folded
directly into this prompt — S25 does not need a separate
amendment file:

- **S24 close-out corrections** folded into Step 0.1 (workspace
  anchor `763fd1a`; repo anchor `aa23712` with operator-eval_data-
  commit tolerance), Step 0.5 (Canonical S24-close baseline 947
  pinned with 16-path invocation + sub-totals), Step 0.9 (S24-
  shipped public API stability check covers the 3 new helpers +
  the abfss:// guard's continued presence).
- **5 LESSONS sections from S24 close** referenced where they
  apply: Tightened-precondition test-fixture retargeting (Phase 3
  non-interleaving + Q-J.8 authorization); Test against public
  API surface only (Phase 2 + Phase 3 test design); Q-I.7 "Both"
  test corpus shape works for small candidates (Q-J.7 — same
  shape applicable to Candidate J's larger ~400-650 LOC scope);
  Q-I.6 "log + continue" pattern explicitly NOT applicable to
  ADLSCostJournal layer (Phase 2 design); Workspace HEAD delta
  tolerance — eval_data-only path (Phase 0 Step 0.1).

If new amendments arise pre-S25 open, walk them per the reviewer-
feedback hygiene pattern in this prompt's "Reviewer-feedback
hygiene" section.
