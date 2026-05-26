# Session 30 prompt — scope picked at Phase 1
# (S29 closed Candidate K-b SHIP; S30 chooses from carry-forwards
#  A/D/E/K-a/K-b-exec)

**Drafted at Session 29 close (2026-05-26).** Mirrors the
S20/S21/S22/S23/S24/S25/S26/S27/S28/S29 prompt structure.
Scope-agnostic at Phases 0/1; scope-specific design gates at
Phase 2 per chosen candidate. Strict 7-phase ordering with
halt-on-mismatch preserved.

This prompt should be invoked from `~/Downloads/session-30-prompt.md`
(operator-mirrored) or directly from
`~/crawler-audit/SESSION_30_PROMPT.md`. Re-read it on session open.

---

## Scope

Engineering session. Workstream sub-surfaces available after
Session 29 closed Candidate K-b SHIP (1 commit + 2 workspace
close-out commits). Repo HEAD at `75a3937`; workspace HEAD at
`e736eee`. **Workstream 0 fully closed at S27 via the
`workstream-0-end` tag at `a1c5636`**; S28 shipped Stage 1
ShardResult split; S29 shipped the K-b operator-driven smoke
script. No new W0-tag implicated for S30.

Carry-forward candidates entering S30 (K-b SHIP fully closed S29):

- **barcada-drift (Candidate A)** — deferred per Q1.1=(A) at S20;
  still needs 4 AI/ML decisions per CLASSIFICATION_ADJACENT_PLAN.md
  §Item 8 AND 2+ `canary_runs/*.parquet` files (earliest natural
  date 2026-06-06 if the launchd installer fires ≥2 Saturdays
  since S20 close). **S29 confirmed empirically** that the
  launchd installer has NOT been run as of S29 close (no plist
  in `~/Library/LaunchAgents/`; 0 parquets on disk).

- **Phase 4 PR-D tooling (Candidate D)** — operator-led labeling
  territory. W0-side unblocked since S27 (`workstream-0-end`
  placed); still gated on operator-led Stage 2/3 labeling.

- **Cassette corpus expansion (Candidate E)** — current 20 is
  lower bound of plan's "~20-30".

- **ADLSCostJournal Azurite-backed CI test (Candidate K-a)** —
  alternative flavor of K not chosen at S29. Permanent CI safety
  net (vs K-b's one-off operator smoke). ~50-100 LOC + Docker
  setup. Would add a 17th path to the canonical invocation per
  Q-K.5 = Option 2.

- **K-b live-Azure smoke EXECUTION (Candidate K-b-exec; NEW
  S29 carry-forward)** — script shipped at S29
  (`scripts/smoke_test_adls_cost_journal.py`); not yet executed
  against real Azure. Carry-forward is bound to operator
  availability of an Azure sandbox container, NOT to a session.
  Operator runs:
  ```bash
  export AZURE_STORAGE_ACCOUNT="<account>"
  export AZURE_STORAGE_CONTAINER="<container>"
  az login   # or set AZURE_STORAGE_KEY
  python scripts/smoke_test_adls_cost_journal.py
  ```
  Expected output: 5-step `[N/5]` trace, then `"All 5 steps OK.
  ADLSCostJournal behavior matches DummyBlobBackend."`, then
  `"Deleted abfss://..."`. If any step diverges, paste the trace
  into SESSION_LOG.md + LESSONS.md and consider an S30 follow-up
  to either fix the divergence in `cost_journal_adls.py` or
  update the script.

**No new carry-forward introduced by S29.** The K-b script
shipped cleanly; the only remaining K-side work is execution +
optional K-a CI safety net.

Operator chooses at Phase 1 which candidate Session 30 ships.
Each candidate has its own Phase 2 design-gate template.

**Sessions 13-29 precedent:** this session does NOT modify the
W4.1.5 driver orchestration at `tests/runners/fixture_cascade/`
(locked at `dd64963` for original files; `cascade.py` extended at
`a1c5636` under S27 W5.X-prefix authorization, and at `9afde57`
under S28 W5.X-prefix authorization; `test_cost_journal_wiring.py`
added at `a1c5636` under S27 authorization and modified at
`ae9e627` under S28 Q-StgSplit.4 1↔1-replacement authorization).
Does NOT modify `expected.schema.json` v1.1 / `META_SCHEMA.md`
v1.1. Does NOT modify the committed `tests/fixtures/baseline-v0/`
snapshot at `9e9a1fb`. Does NOT modify the Session 19 `check`
sub-surface code or the Session 20 cassettes/canary sub-surface
code or the Session 21 `robots.py` parser at `34a59b6` or its
tests, OR the Session 22 deliverables, OR the Session 23
deliverables, OR the Session 24 deliverables, OR the Session 25
deliverables, OR the Session 26 `docs/CRAWLING_POLICY.md` at
`2314f5e`, OR the Session 27 `cascade.py` per-tier wiring at
`a1c5636`, OR the Session 28 deliverables (`stage1/run.py`
ShardResult split at `776d203`; `test_run_cascade.py` +1 net-new
test at `776d203`; `cascade.py` Stage 1 invoker switch at
`9afde57` including the dead-code removal of `_journal_record`;
`test_cost_journal_wiring.py` 1↔1 replacement at `ae9e627`), OR
the Session 29 deliverable (`scripts/smoke_test_adls_cost_journal.py`
at `75a3937`).

Does NOT modify production code under `src/barcada_scraper/`
UNLESS Phase 2 design-gate explicitly authorizes a specific
module. None of the S30 candidates (A/D/E/K-a/K-b-exec)
currently anticipate new src/ authorizations beyond what's
already authorized for their respective surfaces. (Candidate K-a
will likely consume `ADLSCostJournal` without modifying it,
mirroring S29 K-b's posture.)

Full regression-protection checklist in **Out-of-scope** at the
end of this prompt. Re-read it before any code lands.

---

## Reviewer-feedback hygiene (if this prompt is reviewed)

If an external reviewer (operator-invoked) flags items in this
prompt before Session 30 starts, walk each flagged item against
on-disk reality at workspace HEAD `e736eee` and repo HEAD
`75a3937` (or whatever HEAD the operator's machine carries),
BEFORE applying any change. Per S19-S29 pattern (LESSONS
"Reviewer-feedback hygiene"):

- **OBSOLETE** items: SHAs already verified, claims already true.
  Skip with documented reasoning.
- **VALID-applies-now** items: bear on this session's scope. Apply.
- **VALID-applies-later** items: bear on deferred scope. Carry
  forward to the next prompt revision.
- **WRONG-PREMISE** items: assumes something not true. Skip with
  documented reasoning.

Empirical baseline: review remains the convergence mechanism;
verify each item against source before mutating the prompt.

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
halts catch hidden scope expansion (per S22-S29 "Implicit-
authorization HALT for src/-locks" — any src/ touch not enumerated
in Out-of-scope's allow-list surfaces here). Phase 3 halts catch
regressions (including same-shape test failures outside the
prompt's explicit allowlist — see S25-folded LESSONS "Q-J.8
explicit allowlist may be incomplete; HALT-and-extend pattern").
Phase 4 halts catch pre-push gate failures (incl. operator-WIP-
in-locked-tree).

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

Run in order. Halt and surface to operator on any mismatch.

### Step 0.1 — Workspace + repo HEAD

```
# Workspace at Session 30 start. S29 close-out landed across 2
# workspace commits: 0708a53 (primary close-out: SESSION_LOG.md
# + SESSION_TRANSITION_TEMPLATE.md + LESSONS.md) + e736eee
# (anchor-pinning follow-up). This prompt drafted as a follow-up
# commit succeeding e736eee.
git -C ~/crawler-audit rev-parse HEAD
# Expect: 589c6af (S30 prompt-drafted post-S29-close, succeeding
# e736eee) OR a later commit if additional workspace doc edits or
# an S30 prompt-revision landed post-draft. If N commits ahead, verify
# each prior commit's subject via `git log --oneline e736eee..HEAD`
# against expected prompt-finalization / doc-edit patterns;
# surface the SHA delta and request authorization to proceed if
# anything is unexpected.
# (S20-S29 precedent: operator authorized continuation when 1-2
# extra workspace commits were the strengthened prompts
# themselves.)

# Repo at Session 29 final commit:
git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: 75a3937 (WA2.W8.adls-live-smoke) — the canonical
# end-of-S29 ship SHA.
#
# Tolerated delta: operator-side eval_data labeling commits between
# S29 close and S30 open are expected (Sessions 8-29 precedent).
# Per the S22-folded "Workspace HEAD delta tolerance" LESSONS
# pattern: tolerate N additional commits as long as EACH commit's
# stat is strictly within eval_data/* (no src/barcada_scraper/*
# touches, no tests/* touches, no scripts/* touches, no docs/*
# touches). Verify via `git show --stat <sha>` for every commit in
# 75a3937..HEAD; surface any non-eval_data delta for operator
# authorization before continuing.
#
# Known post-S29 eval_data commit at prompt-drafting time:
#   - af6f1d4 (2026-05-26 16:00 "stage1 audit: A3 pre-staged
#     flags + appointment_booking refinement"; 3 files all
#     under eval_data/). Tolerated.
# Additional eval_data commits may land between prompt-draft
# and S30 open.
```

### Step 0.2 — Tags (unchanged since S27 close; S28 and S29 each placed no tag)

```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort
# Expect 11 tags (UNCHANGED since S27 close; S28 and S29 placed
# no tag):
#   baseline-v0
#   pre-remediation-2026-05-19
#   workstream-0-end                   (placed S27 at a1c5636)
#   workstream-0-week1-end
#   workstream-0-week2-end
#   workstream-0-week3-end
#   workstream-0-week4-1-5-end
#   workstream-0-week4-end
#   workstream-0-week5-end
#   workstream-0-week7-end
#   workstream-a-week1-end

git -C /Users/administrator/projects/barcada-scraper rev-list -n 1 workstream-0-end
# Expect: a1c5636… (matches the S27 placement; UNCHANGED).
```

### Step 0.3 — Driver locked (with S16 + S27 + S28 exceptions)

```
cd /Users/administrator/projects/barcada-scraper
git diff dd64963..HEAD -- tests/runners/fixture_cascade/ \
    ':(exclude)tests/runners/fixture_cascade/test_fixture_fetcher.py' \
    ':(exclude)tests/runners/fixture_cascade/cascade.py' \
    ':(exclude)tests/runners/fixture_cascade/test_cost_journal_wiring.py'
# Expect: empty.
# The 3 excluded files have legitimate W5.X-prefix modifications:
#   - test_fixture_fetcher.py changed at 8d0fc0e (S16 W5.X realign).
#   - cascade.py extended at a1c5636 (S27 Candidate B per-tier wiring)
#     and again at 9afde57 (S28 Candidate StgSplit Stage 1 invoker
#     switch + dead-code removal of _journal_record).
#   - test_cost_journal_wiring.py added at a1c5636 (S27 deliverable)
#     and modified at ae9e627 (S28 Q-StgSplit.4 1↔1 replacement).
# Any non-empty diff outside these 3 files = HALT.
# S29 did NOT touch this surface.
```

### Step 0.4 — Fixture counts (use Python pattern per S28 LESSONS hygiene fold)

**IMPORTANT**: per S28-folded LESSONS "Phase 0 fixture-count
commands need `2>/dev/null` + a bounded timeout", do NOT use bare
`find` invocations here. They hung indefinitely in S28 and
accumulated ~24 stuck shells in the background-task registry.
Use the Python pattern below — returned all 6 counts in <2s when
the equivalent `find` commands had been hung 15+ hours.

```
.venv/bin/python -c "
from pathlib import Path
root = Path('tests/fixtures')
html_count = sum(1 for _ in (root / 'html').rglob('*.html'))
expected_count = sum(1 for p in (root / 'html').rglob('*.json') if '/expected/' in str(p))
meta_count = sum(1 for _ in (root / 'html').rglob('*.meta.json'))
baseline_count = sum(1 for p in (root / 'baseline-v0').rglob('*') if p.is_file())
cassette_count = sum(1 for _ in (root / 'synthetic_crawls').rglob('cassette.yaml'))
exclusions_count = sum(1 for _ in (root / 'synthetic_crawls').rglob('extract_hard_exclusions.json'))
assert html_count == 222, html_count
assert expected_count == 202, expected_count
assert meta_count == 222, meta_count
assert baseline_count == 1213, baseline_count
assert cassette_count == 20, cassette_count
assert exclusions_count == 20, exclusions_count
print(f'OK fixture counts: html={html_count} expected={expected_count} meta={meta_count} baseline={baseline_count} cassette={cassette_count} exclusions={exclusions_count} (unchanged from the locked snapshot)')
"
```

If the assertions fire, HALT and surface to operator.

**Fallback `find` pattern** (if Python is unavailable for any
reason; NOT recommended): always include `2>/dev/null` AND wrap
the Bash tool call with `timeout=60000` AND prepend the command
with `timeout 60s` for double-bounded wallclock. Kill before
retry if any command hangs >30 seconds.

### Step 0.5 — Test-suite baseline (S30 canonical)

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
# Expect: 970 passed / 0 failed / 0 skipped
#
# Sub-totals (16 paths; ALL identical to S27/S28/S29 close — S29's
# K-b ship is a new SCRIPT under scripts/, NOT a test):
#   210 conformance + 52 driver + 99 baseline_v0 +
#    33 synthetic_crawl + 32 robots + 30 robots_gate +
#    30 robots_bypass_config + 43 cost_journal +
#    13 cost_journal_local + 19 cost_journal_adls +
#    35 robots_integration + 74 vmss_worker +
#   129 job_runner + 152 worker_loop +
#     7 robots_gate_integration (4 S23 + 2 S24-unchanged + 1 S25-replaced) +
#    12 worker_loop_persistence (11 S24-unchanged + 1 S25-replaced) = 970
#
# Note: the S28 +1 net-new test
# (`test_shard_result_carries_llm_and_embedding_cost_split`) lives
# in tests/classifier/stage1/test_run_cascade.py — OUTSIDE the
# canonical 16-path invocation, so the headline count holds at 970.
# If a future session adds a stage1-touching candidate, expand the
# invocation to include tests/classifier/stage1/ and recompute the
# headline at that prompt's Phase 0 Step 0.5.
#
# Pinned in SESSION_LOG.md "Canonical S29-close baseline" block.
# The 970 count is invariant under operator-side eval_data
# commits between S29 and S30 (eval_data is not in the invocation).
```

The sub-paths add up to the headline: 210 + 52 + 99 + 33 + 32 + 30
+ 30 + 43 + 13 + 19 + 35 + 74 + 129 + 152 + 7 + 12 = 970. Any drift
= halt.

If the headline mismatches, re-run each sub-path independently to
localize which sub-suite drifted:

```
.venv/bin/python -m pytest tests/scraper/test_fixture_conformance.py -q              # expect 210
.venv/bin/python -m pytest tests/runners/fixture_cascade/ -q                          # expect  52
.venv/bin/python -m pytest tests/baseline_v0/ -q                                       # expect  99
.venv/bin/python -m pytest tests/synthetic_crawl/ -q                                   # expect  33
.venv/bin/python -m pytest tests/scraper/test_robots.py -q                             # expect  32
.venv/bin/python -m pytest tests/scraper/test_robots_gate.py -q                        # expect  30
.venv/bin/python -m pytest tests/scraper/test_robots_bypass_config.py -q               # expect  30
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal.py -q           # expect  43
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal_local.py -q     # expect  13
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal_adls.py -q      # expect  19
.venv/bin/python -m pytest tests/orchestrator/test_robots_integration.py -q            # expect  35
.venv/bin/python -m pytest tests/orchestrator/test_vmss_worker.py -q                   # expect  74
.venv/bin/python -m pytest tests/orchestrator/test_job_runner.py -q                    # expect 129
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop.py -q                   # expect 152
.venv/bin/python -m pytest tests/orchestrator/test_robots_gate_integration.py -q       # expect   7
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop_persistence.py -q       # expect  12
```

**Narrower baselines** (valid for S30 candidates that don't
exercise the new ADLS or robots-gate-integration test paths):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 944 (S27/S28/S29-equivalent narrower for candidates that don't
  touch ADLS or robots_gate_integration; canonical 16-path minus
  19 cost_journal_adls minus 7 robots_gate_integration; verified
  post-S29-close at `75a3937`). Canonical 14-path invocation:

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
      tests/orchestrator/test_robots_integration.py \
      tests/orchestrator/test_vmss_worker.py \
      tests/orchestrator/test_job_runner.py \
      tests/orchestrator/test_worker_loop.py \
      tests/orchestrator/test_worker_loop_persistence.py -q
  # Expect: 944 passed / 0 failed / 0 skipped
  # Sub-totals (14 paths; 210 + 52 + 99 + 33 + 32 + 30 + 30 + 43 +
  #   13 + 35 + 74 + 129 + 152 + 12 = 944).
  ```

If Candidate K-a is chosen, the canonical 16-path invocation MAY
extend to a **17-path invocation** with the new Azurite-backed
test file (e.g., `tests/classifier/pipeline/test_cost_journal_adls_azurite.py`)
per Q-K.5 = Option 2. Whichever baseline is bound at Phase 1,
hold it consistent across ALL Phase 3 commits in S30 — do not
switch mid-session.

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

# S25 ADLS backend tests
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal_adls.py -q
# Expect: 19 passed

# S23 W A.2 sub-surface tests
.venv/bin/python -m pytest tests/orchestrator/test_robots_integration.py -q
# Expect: 35 passed
.venv/bin/python -m pytest tests/orchestrator/test_vmss_worker.py -q
# Expect: 74 passed
.venv/bin/python -m pytest tests/orchestrator/test_job_runner.py -q
# Expect: 129 passed
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop.py -q
# Expect: 152 passed

# S24 + S25 W A.2 integration tests
.venv/bin/python -m pytest tests/orchestrator/test_robots_gate_integration.py -q
# Expect: 7 passed (4 S23 + 2 S24-unchanged + 1 S25-replaced)
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop_persistence.py -q
# Expect: 12 passed (11 S24-unchanged + 1 S25-replaced)

# S27 + S28 per-tier cost-accounting wiring tests
.venv/bin/python -m pytest tests/runners/fixture_cascade/test_cost_journal_wiring.py -q
# Expect: 6 passed (5 cascade-driven + 1 helper-direct unit test;
# S28 1↔1 same-shape replaced test_stage1_per_tier_slots_remain_zero_by_design
# with test_stage1_per_tier_slots_populate_from_split)

# S28 Stage 1 ShardResult split tests (outside canonical 16-path)
.venv/bin/python -m pytest tests/classifier/stage1/test_run_cascade.py -q
# Expect: 16 passed (15 historical pre-existing + 1 S28-added
# `test_shard_result_carries_llm_and_embedding_cost_split`; all 16
# pre-existing at S30-open).
.venv/bin/python -m pytest tests/classifier/stage1/test_cost_tracker.py -q
# Expect: 16 passed (all pre-existing — unchanged since before S28).
```

### Step 0.9 — S25-shipped + S26-shipped + S27-shipped + S28-shipped + S29-shipped public API + doc stability (any-candidate prereq)

```
# Verify the S25 deliverables match what landed at S25 close, the
# S26 CRAWLING_POLICY.md tightening matches its landed shape, the
# S27 cascade.py per-tier wiring helper matches its landed
# signature, the S28 Stage 1 ShardResult split + cascade.py Stage 1
# invoker shape match their landed structure, AND the S29 K-b
# smoke script exists at its landed path + remains import-loadable.
# A change to any of these between S29 close and S30 open would
# invalidate carry-forward candidate assumptions. Run
# unconditionally at every S30 cold start.

.venv/bin/python -c "
import inspect
from barcada_scraper.classifier.pipeline.cost_journal import (
    open_journal,
    JournalState,
    JournalAlreadyExistsError,
    CostJournal,
)
from barcada_scraper.classifier.pipeline.cost_journal_local import LocalFSCostJournal
from barcada_scraper.classifier.pipeline.cost_journal_adls import (
    ADLSCostJournal,
    BlobNotFoundError,
    ConditionNotMetError,
    _abfss_to_https,
)
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

# LocalFSCostJournal public surface.
for m in ('read', 'write_initial', 'try_update', 'exists'):
    assert hasattr(LocalFSCostJournal, m), m

# S25: ADLSCostJournal full surface (4 abstract methods + path).
for m in ('read', 'write_initial', 'try_update', 'exists', 'path'):
    assert hasattr(ADLSCostJournal, m), m
sig = inspect.signature(ADLSCostJournal.__init__)
required_kwargs = {'journal_dir', 'run_id'}
optional_kwargs = {'credential', 'blob_backend'}
all_kwargs = set(sig.parameters) - {'self'}
assert required_kwargs <= all_kwargs, all_kwargs
assert optional_kwargs <= all_kwargs, all_kwargs

# S25: _abfss_to_https translates correctly.
assert _abfss_to_https('abfss://c@acct.dfs.core.windows.net/p/file.json') == \\
    'https://acct.blob.core.windows.net/c/p/file.json'

# S25: ADLSCostJournal constructs via injected backend without
# touching Azure SDK / credentials.
class _FakeBackend:
    def upload(self, *, data, if_none_match=None, if_match=None):
        return '\"etag-fake\"'
    def download(self):
        raise BlobNotFoundError('not yet written')
    def exists(self): return False

j = ADLSCostJournal(
    journal_dir='abfss://c@acct.dfs.core.windows.net/p',
    run_id='x',
    blob_backend=_FakeBackend(),
)
assert j.path == 'abfss://c@acct.dfs.core.windows.net/p/run_x.json'
assert j.exists() is False
assert j.read() is None

print('OK all S24-shipped + S25-shipped public APIs unchanged')
"

# Verify the S25 abfss:// dispatch in worker_loop's helper still
# routes abfss:// URLs to ADLSCostJournal.
.venv/bin/python -c "
from unittest.mock import patch
from barcada_scraper.orchestrator.worker_loop import _open_cost_journal_for_worker
from barcada_scraper.orchestrator.vmss_worker import WorkerConfig
from barcada_scraper.classifier.pipeline.cost_journal_adls import ADLSCostJournal

config = WorkerConfig(
    phase='scrape-stage2-pages',
    shard_queue_url='https://x.queue.core.windows.net/q',
    blob_output_url='file:///tmp/out',
    cost_journal_url='abfss://j@x.dfs.core.windows.net/c.jsonl',
    stop_flag_url='file:///tmp/stop.json',
    worker_id='test',
    azure_client_id='00000000-0000-0000-0000-000000000000',
    crawl_date='2026-05-23',
    worker_concurrency=1,
)
with patch(
    'barcada_scraper.classifier.pipeline.cost_journal_adls._AzureBlobBackend.__init__',
    lambda self, **_kw: None,
):
    journal = _open_cost_journal_for_worker(config)
assert isinstance(journal, ADLSCostJournal), type(journal).__name__
assert journal.path == 'abfss://j@x.dfs.core.windows.net/run_2026-05-23.json'
print('OK abfss:// dispatch routes to ADLSCostJournal (S25 Candidate J seam intact)')
"

# S26: CRAWLING_POLICY.md doc stability — landed at S26 SHA
# 2314f5e at 77 lines / 2519 bytes; verify it hasn't drifted.
test "$(wc -l < docs/CRAWLING_POLICY.md)" = "77" && \
    test "$(wc -c < docs/CRAWLING_POLICY.md)" = "2519" || \
    { echo "HALT: CRAWLING_POLICY.md drifted from S26-landed shape (expected 77 lines / 2519 bytes)"; exit 1; }
echo "OK docs/CRAWLING_POLICY.md unchanged from S26 close (77 lines / 2519 bytes)"

# Verify the load-bearing content still present:
.venv/bin/python -c "
content = open('docs/CRAWLING_POLICY.md').read()
markers = ['BypassAuthorization', 'first-match-wins', 'ETag-', 'authorized_by']
missing = [m for m in markers if m not in content]
assert not missing, f'missing markers: {missing}'
print('OK CRAWLING_POLICY.md load-bearing content (audit record / first-match / ETag / sidecar schema) all present')
"

# S27: cascade.py per-tier wiring helper signature stability.
.venv/bin/python -c "
import inspect
from tests.runners.fixture_cascade import cascade as cm
assert hasattr(cm, '_journal_record_with_breakdown'), '_journal_record_with_breakdown helper missing'
sig = inspect.signature(cm._journal_record_with_breakdown)
expected_params = {'journal', 'shard_id', 'stage', 'started_at', 'domains_processed', 'components', 'unattributed_cost_usd'}
assert expected_params <= set(sig.parameters), set(sig.parameters)
print('OK S27 _journal_record_with_breakdown helper signature unchanged from a1c5636')
"

# S27 + S28: per-tier wiring invariant smoke (all 8 slots populate).
.venv/bin/python -c "
import math, tempfile
from pathlib import Path
from tests.runners.fixture_cascade.cascade import _journal_record_with_breakdown
from barcada_scraper.classifier.pipeline import cost_journal as cj

with tempfile.TemporaryDirectory() as td:
    journal_dir = Path(td)
    journal = cj.open_journal(journal_dir=journal_dir, run_id='phase0-smoke')
    journal.write_initial(cj.JournalState.fresh(run_id='phase0-smoke', ceiling_usd=10.0))

    _journal_record_with_breakdown(
        journal=journal, shard_id='s1', stage=1,
        started_at='2026-05-26T00:00:00+00:00', domains_processed=10,
        components={'llm': 0.04, 'embedding': 0.01}, unattributed_cost_usd=0.0,
    )
    _journal_record_with_breakdown(
        journal=journal, shard_id='s2', stage=2,
        started_at='2026-05-26T00:01:00+00:00', domains_processed=10,
        components={'fetch': 0.10, 'summarization': 0.20, 'classification': 0.30},
        unattributed_cost_usd=0.0,
    )
    _journal_record_with_breakdown(
        journal=journal, shard_id='s3', stage=3,
        started_at='2026-05-26T00:02:00+00:00', domains_processed=10,
        components={'evidence': 0.05, 'primary': 0.07, 'secondary': 0.0},
        unattributed_cost_usd=0.03,
    )

    state = journal.read().state
    per_tier_sum = sum(getattr(state.totals, fname) for fname in cj._TOTALS_FIELDS.values())
    shard_sum = sum(s.cost_usd for s in state.shards)
    assert state.totals.stage1_llm_usd == 0.04
    assert state.totals.stage1_embedding_usd == 0.01
    assert math.isclose(state.totals.cost_usd, per_tier_sum + shard_sum, abs_tol=1e-9), (state.totals.cost_usd, per_tier_sum, shard_sum)
    for fname in cj._TOTALS_FIELDS.values():
        assert hasattr(state.totals, fname), fname

print('OK S27+S28 per-tier wiring invariant holds at S30 cold start (all 8 slots populate)')
"

# S28: ShardResult split field presence (compile-time guarantee).
.venv/bin/python -c "
from barcada_scraper.classifier.stage1.run import ShardResult
fields = set(ShardResult.__dataclass_fields__.keys())
assert 'llm_cost_usd' in fields, fields
assert 'embedding_cost_usd' in fields, fields
assert 'cost_usd' in fields, fields  # aggregate retained
assert len(fields) == 14, f'expected 14 fields; got {len(fields)}: {fields}'
print('OK S28 ShardResult llm_cost_usd + embedding_cost_usd fields present; total 14 fields')
"

# S28: cascade.py Stage 1 invoker call-site structure (AST-based).
.venv/bin/python -c "
import ast
with open('tests/runners/fixture_cascade/cascade.py') as f:
    tree = ast.parse(f.read())

all_calls = []
stage1_calls = []
for node in ast.walk(tree):
    if isinstance(node, ast.Call):
        func = node.func
        name = (func.attr if isinstance(func, ast.Attribute)
                else (func.id if isinstance(func, ast.Name) else None))
        if name == '_journal_record_with_breakdown':
            all_calls.append(node)
            stage_kw = next((kw for kw in node.keywords if kw.arg == 'stage'), None)
            if (stage_kw and isinstance(stage_kw.value, ast.Constant)
                    and stage_kw.value.value == 1):
                stage1_calls.append(node)

assert len(all_calls) == 3, f'expected 3 calls (one per stage); found {len(all_calls)}'
assert len(stage1_calls) == 1, f'expected 1 stage=1 call; found {len(stage1_calls)}'

call = stage1_calls[0]
components_kw = next((kw for kw in call.keywords if kw.arg == 'components'), None)
assert components_kw is not None, 'Stage 1 call missing components kwarg'
assert isinstance(components_kw.value, ast.Dict), 'components must be a dict literal'
keys = [k.value for k in components_kw.value.keys
        if isinstance(k, ast.Constant)]
assert 'llm' in keys, f'Stage 1 components missing llm: {keys}'
assert 'embedding' in keys, f'Stage 1 components missing embedding: {keys}'
print('OK S28 cascade.py Stage 1 invoker structure intact (3 _journal_record_with_breakdown calls; stage=1 has llm + embedding components)')
"

# S29 NEW: K-b smoke script existence + import-loads cleanly.
.venv/bin/python -c "
import importlib.util
from pathlib import Path

path = Path('scripts/smoke_test_adls_cost_journal.py')
assert path.exists(), f'S29 K-b script missing: {path}'

# Verify import-loads cleanly (no syntax errors; all imports resolve).
# Matches S25/S26/S27/S28 Step 0.9 precedent — pin behavior, not size.
# A bug fix to the script between S29 and S30 (anticipated by Phase 1
# Candidate K-b-exec at the 'follow-up to fix the divergence' clause)
# would alter LOC without altering correctness; the import-load +
# public-surface check below is the load-bearing signal.
spec = importlib.util.spec_from_file_location('s29_smoke', str(path))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# Verify the load-bearing public surface used by the script.
assert hasattr(m, 'main'), 'main() missing from K-b smoke script'
assert hasattr(m, '_build_credential'), '_build_credential helper missing'
assert hasattr(m, '_delete_blob'), '_delete_blob helper missing'

print('OK S29 K-b script intact (import OK; public surface intact)')
"
```

If any of 0.1-0.9 fail, HALT before doing any work.

---

## Required workspace reading (Session 30 first 10 minutes)

In this order:

1. **`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`** — full
   handoff state at S29 close. Lists scope candidates
   (A/D/E/K-a/K-b-exec) with prerequisites + estimated scope.
   The S30 scope choice at Phase 1 picks from these.

2. **`~/crawler-audit/SESSION_LOG.md`** Session 29 entry — what
   landed during Candidate K-b ship (1 commit + 2 close-out
   workspace commits). The S29 disposition documents the
   empirical Phase 1 prereq check for Candidate A and the
   parallel-SDK-client cleanup pattern that surfaced.

3. **`~/crawler-audit/LESSONS.md`** — 2 new sections folded at
   S29 close, at end of file ("S29 folding" suffix). Locate via
   `grep -n '^## .*(S29 folding)' LESSONS.md`. Read with care:
   - "Operator-driven script LOC estimates need a ~70-100 LOC
     additive overhead floor, not a linear multiplier" (S29
     folding) — **MANDATORY READ for any Phase 1 candidate that
     proposes an operator-driven script or CLI tool**. Documents
     how Copyright + docstring + argparse overhead drove S29's
     K-b script from "~30 LOC" prompt-estimate to 220 LOC
     delivered, and why the right framing is ADDITIVE
     (logic + ~70-100 LOC floor), not multiplicative
     (logic × 3×). The ~3× ratio observed for K-b is a special
     case where logic is small enough that overhead dominates.
   - "Public-API-only cleanup pattern extends from tests to
     operator scripts" (S29 folding) — extends S24 pattern.
     Forward-applicable: any new script/test that consumes a
     wrapper class needing an operation NOT in the public
     surface should construct a parallel SDK client rather than
     reach into private attrs.

4. **`~/crawler-audit/BARCADA_CRAWLER_REMEDIATION_PLAN.md`** —
   chosen-scope section per Phase 1 candidate choice. Plan is
   READ-ONLY.

5. **`~/crawler-audit/CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8
   — only if Candidate A (barcada-drift) is chosen.

6. **`~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md`** —
   only if Candidate K-a touches ADLS Phase 5 promotion
   invariants. READ-ONLY.

7. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   — only if Candidate K-a touches the ADLS backend. 295 LOC.
   The full Phase 5 backend shipped at S25 SHA `835a531`.

8. **`tests/classifier/pipeline/test_cost_journal_adls.py`** at
   `835a531` — only if Candidate K-a touches ADLS testing. 19
   tests against `DummyBlobBackend` in-memory.

9. **`scripts/smoke_test_adls_cost_journal.py`** at S29 SHA
   `75a3937` — for reference if Candidate K-a is chosen (the
   K-b script's structure informs the K-a test layout) OR if
   Candidate K-b-exec surfaces a divergence requiring follow-up.
   220 LOC.

10. **`docs/CRAWLING_POLICY.md`** at S26 SHA `2314f5e` — only if
    operator wants to review the S26-tightened version (77 lines /
    2.52 KB).

11. **`tests/runners/fixture_cascade/cascade.py`** at S28 SHA
    `9afde57` — for reference if any candidate touches the
    driver. Module docstring documents that all 8 `_TOTALS_FIELDS`
    slots are wired (Stage 1 closure shipped S28). S29 did NOT
    touch this surface.

12. **`src/barcada_scraper/classifier/stage1/run.py`** at S28 SHA
    `776d203` — for reference if Candidate A or any future stage1-
    touching candidate is chosen. ShardResult has 14 fields
    (LLM/embedding split added S28).

---

## Phase 1 — Scope resolution (no code; pre-design-gate)

Operator picks one candidate. Candidates ordered by prerequisite-
readiness; each is independent.

### Candidate A — `barcada-drift` (depends on AI/ML team alignment + ≥2 parquets)

Per `CLASSIFICATION_ADJACENT_PLAN.md` §Item 8. Consumes the
`canary_runs/<date>.parquet` artifacts the S20 launchd job
produces. Estimated ~300 LOC logic + ~70-100 LOC overhead floor
(Copyright header + module docstring + argparse) ≈ **~370-400
LOC delivered**. The S29-folded LESSONS "~3×" ratio reflects
the overhead-floor:logic-LOC relationship at very small logic
budgets (K-b: 70 LOC logic + 150 LOC overhead = 220 LOC total
≈ 3× total/logic); it is NOT a linear multiplier. For larger
logic budgets the overhead floor stays roughly constant, so
total/logic ratio compresses toward 1×.

**Prerequisites:**
- 2+ `canary_runs/*.parquet` files exist on operator's machine.
  Earliest natural date: 2026-06-06 (two Saturdays from S20 close
  at 2026-05-23) assuming operator ran the launchd installer
  immediately after S20.
- AI/ML team responses on 4 §Item 8 decisions OR explicit
  operator-side placeholder choices with "AI/ML-to-tune" notes.

**HALT IF** the 4 AI/ML decisions are not pre-resolved going into
Session 30 AND operator has not authorized explicit placeholder
choices.

**Empirical prereq audit at S29 close** (carry-forward to S30
open):
- 0 parquets on disk under any `canary_runs/` path (verified via
  `Path.rglob('*.parquet')` across repo + workspace).
- No `barcada` / `canary` plist in `~/Library/LaunchAgents/`
  (verified via `Path.home() / 'Library' / 'LaunchAgents'`).
- No AI/ML team responses or operator-side placeholder
  authorizations found anywhere in workspace.

Re-run these empirical checks at S30 Phase 1 BEFORE issuing the
candidate-choice AskUserQuestion (per S29 LESSONS pattern
"Empirical Phase 1 prerequisite check before scope-narrow"). If
the empirical state is unchanged, Candidate A remains blocked.

### Candidate D — Phase 4 PR-D operator-led labeling (operator territory)

Per plan §11 Risk Register entry. Stage 2 + Stage 3 labeling
gates PR-D/E/F/G. Operator-led; Claude Code's role limited to
tooling. W0-side unblocked at S27 (`workstream-0-end` tag at
`a1c5636`); still gated on operator-led labeling.

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

### Candidate K-a — Azurite-backed integration test (alternative to K-b-exec)

S25 shipped ADLSCostJournal against `DummyBlobBackend` in-memory.
S29 shipped Candidate K-b (operator-driven script). K-a is the
remaining alternative: a Docker-backed integration test that
spins up an Azurite container and exercises
`write_initial` → `try_update` → `read` → ETag conflict path
against a real Azure-compatible blob service. Permanent CI
safety net (vs K-b's one-off operator smoke).

**Prerequisites:**
- Docker available locally; Azurite image pullable.

**Scope estimate**: ~50-100 LOC logic = **~150-300 LOC delivered**
+ Docker setup per the S29-folded LESSONS pattern.

**Recommended posture if K-a chosen**: pair with a Q-K.5 = Option
2 decision (add a 17th path to the canonical invocation) so the
Azurite test stays part of the regression gate.

### Candidate K-b-exec — Execute the S29 K-b script (NEW S29 carry-forward)

Bound to operator availability of an Azure sandbox container,
NOT to a session. Script ships at
`scripts/smoke_test_adls_cost_journal.py` (220 LOC; 5-step
ETag-conflict matrix). Operator runs:

```bash
export AZURE_STORAGE_ACCOUNT="<account>"
export AZURE_STORAGE_CONTAINER="<container>"
az login   # or set AZURE_STORAGE_KEY
python scripts/smoke_test_adls_cost_journal.py
```

Expected output: 5-step `[N/5]` trace, then
`"All 5 steps OK. ADLSCostJournal behavior matches DummyBlobBackend."`,
then `"Deleted abfss://..."`.

**Prerequisites:**
- Operator has an Azure sandbox container.
- `az login` is current OR `AZURE_STORAGE_KEY` is set.

**Acceptance:**
- Script exits 0 with the expected trace → carry-forward closed;
  paste the trace into SESSION_LOG.md as a passing smoke.
- Any step diverges from `DummyBlobBackend` behavior → paste
  the trace into LESSONS.md + open S31 follow-up to either fix
  the divergence in `cost_journal_adls.py` or update the script.

**This candidate has ~0 LOC of new code.** Claude Code's role is
to interpret the operator's trace and propose follow-up only if
divergence is observed.

### Sub-question 1.TAG — Tag at session close (pinned at Phase 1)

Independent of scope choice; resolved fully here at Phase 1 so
Phase 5 has an unambiguous tag decision. Options per scope:

- **Candidate A** (barcada-drift): defer OR place candidate-
  specific (e.g., `barcada-drift-v0`).
- **Candidate D** (Phase 4 PR-D tooling): defer.
- **Candidate E** (cassette corpus expansion): defer.
- **Candidate K-a** (Azurite-backed CI test): defer OR consider
  `workstream-a-week2-end` if K-a is the final W A.2 milestone
  (operator decides; see Phase 5 note below).
- **Candidate K-b-exec** (run the K-b script): defer (no code
  ships; no milestone implicated).

Phase 5 reads this resolution directly — no Phase 2 re-decision.

**Note on workstream-A.2-end**: W A.1 closed at S22's
`workstream-a-week1-end`. W A.2 is the orchestrator-side robots
work that landed across S23+S24+S25, plus the ADLS Phase 5
promotion at S25, plus the K-b operator smoke at S29. K-a (if
chosen) would arguably be the final piece. Operator-discretion
whether to tag at S30 close if K-a ships.

---

## Phase 2 — Design-gate elicitation (no code; AskUserQuestion)

Per chosen Phase 1 candidate. Each candidate has its own sub-
block. Source-verify at session-current HEAD per `[[verify-
before-asking-discipline]]` AND per S22-S29 "Plan-vs-reality at
Phase 2 source-verify" + S25-folded "Phase 2 source-verify drives
option-set design, not just gates" + S27-folded "Re-source-verify
the seam at closure time" LESSONS patterns BEFORE each
AskUserQuestion batch.

**HALT IF** any Phase 2 decision would require modifications to
`src/barcada_scraper/` production code beyond what was Phase-2-
authorized (per S22-S29 "Implicit-authorization HALT for src/-
locks" LESSONS pattern; surface as an explicit AskUserQuestion
before patching) OR to the W4.1.5 driver beyond the S16/S27/S28
W5.X-prefix exceptions OR to any S19-S29 deliverable — surface as
a design-gate sub-question before patching.

### **CRITICAL Phase 2 hygiene from S26 LESSONS** (apply BEFORE every AskUserQuestion call)

Per S26-folded LESSONS "AskUserQuestion 4-option limit can
silently truncate a Q-* option set":

**Before drafting EACH AskUserQuestion batch**, count the prompt's
option set per Q-*. If any single Q-* enumerates >4 mutually-
exclusive options:

1. **Tier the question** — split into a single-select "broad
   category" Q-X.A (≤4 options) followed by a multi-select
   "details" Q-X.B (≤4 options) once the category narrows.
2. **OR split horizontally** — issue two separate
   AskUserQuestion calls for the >4-option Q-*. Each is a
   discrete operator decision point.
3. **OR enumerate explicitly in chat first** — list the full N
   options as text, ask the operator to pre-narrow to ≤4 before
   the AskUserQuestion call.

Do NOT silently narrow.

### **CRITICAL Phase 2 hygiene from S28 LESSONS (empirical-vs-by-design)** (apply during retrofit-style closures)

Per S28-folded LESSONS "Empirical-vs-by-design distinction in
test pins": when closing a deferred gap or otherwise extending an
existing surface, audit EVERY existing test pin in the affected
area for the "by design" / "empirically true" distinction. Grep
the affected test files for phrases like "by design",
"intentionally $0", "deferred", "out of scope". Each match is a
candidate for either 1↔1 replacement (Q-StgSplit.4-style) or
re-framing in place (comment/docstring/name update).

This is not a candidate-specific concern; it applies whenever
S30's scope extends a surface that has existing test assertions
encoding the OLD design.

### **CRITICAL Phase 2 hygiene from S29 LESSONS (LOC budgeting)** (apply when sizing any candidate with new files)

Per S29-folded LESSONS "Operator-driven script LOC estimates
need a ~70-100 LOC additive overhead floor, not a linear
multiplier": when a candidate proposes new operator-driven
Python files (scripts, tests, CLIs), audit the proposed LOC
estimate by ADDING the overhead floor, not multiplying:

- Mandatory Copyright header: ~13 LOC
- Module docstring (usage + auth + safety): ~20-30 LOC
- Imports + format-standard spacing: ~10-15 LOC
- Argparse (if applicable): ~30-50 LOC

That's **~70-100 LOC of additive overhead** before any logic.

- "~30 LOC logic" → ~100-130 LOC delivered (overhead dominates;
  total/logic ≈ 3-4×; S29 K-b matched this band).
- "~50 LOC logic" → ~120-150 LOC delivered (total/logic ≈ 2.5×).
- "~100 LOC logic" → ~170-200 LOC delivered (total/logic ≈ 1.7-2×).
- "~300 LOC logic" → ~370-400 LOC delivered (total/logic ≈ 1.3×).

**Do NOT apply a linear ~3× multiplier.** The K-b case happened
to land at ~3× because its logic was small enough that overhead
dominated. For larger logic budgets the overhead floor stays
roughly constant, so the total/logic ratio compresses toward 1×.
Applying ~3× linearly to a ~300 LOC logic candidate would
overstate scope by ~500 LOC and could nudge the operator to
decline a perfectly-sized candidate on false budget grounds.

Surface this budgeting note in any Phase 2 Q-* that asks the
operator to choose between scope variants — let them see the
real LOC implications.

### If Candidate A (barcada-drift)

Carry-forward from S22-S29 prompts (unchanged).
- Q-A.1 CLI namespace; Q-A.2 drift metric; Q-A.3 alert threshold;
  Q-A.4 input contract; Q-A.5 output shape; Q-A.6 test corpus.

(NB: Candidate A has 6 Q-* gates. Two AskUserQuestion caps apply
independently and BOTH need to be checked:
- 4 OPTIONS per question (the S26 LESSONS topic): check each Q-*
  individually; if any single Q-* exceeds 4 options, apply the
  tier/split protocol from "CRITICAL Phase 2 hygiene" above.
- 4 QUESTIONS per call (a separate tool-schema cap; not the
  S26 LESSONS cap): batching all 6 Q-* into one AskUserQuestion
  would violate this; split into 2-3 sequential calls (e.g.,
  3 + 3, or 2 + 2 + 2).)

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

### If Candidate K-a (Azurite-backed integration test)

- **Q-K-a.1 Auth posture**: connection-string auth vs shared-key
  auth vs DefaultAzureCredential (Azurite supports all three;
  connection-string is the simplest for CI).
- **Q-K-a.2 Test scope**: full ETag-conflict matrix (mirroring
  the K-b script's 5-step trace) vs single happy-path
  round-trip.
- **Q-K-a.3 New file vs append**: new file
  `tests/classifier/pipeline/test_cost_journal_adls_azurite.py`
  vs append to `test_cost_journal_adls.py` with a `pytest.mark.live`
  marker.
- **Q-K-a.4 CI integration**: mark as `live` and skip-by-default
  in the canonical 16-path invocation, OR add a 17th path to
  the invocation that runs only when Docker/Azurite is
  available.
- **Q-K-a.5 Azurite lifecycle**: spin up Azurite via fixture
  (auto-start container) vs require operator-started Azurite
  on a fixed port vs CI-environment-only.

### If Candidate K-b-exec (run the S29 K-b script)

No Phase 2 design gates apply — the script is already shipped.
Operator's role at S30 is to execute the script and report the
trace. Claude Code's role is to interpret the trace + propose
follow-up only if divergence from `DummyBlobBackend` is
observed.

If divergence IS observed, the follow-up scope opens new design
gates at the S30+1 session (or as an in-session pivot at S30
Phase 3, if operator authorizes scope expansion mid-session).
Anticipated divergence shapes:

- **Step 2 (re-write_initial)** returns a different exception
  type than `JournalAlreadyExistsError` → cost_journal_adls.py
  exception mapping needs update OR script's `except` clause
  needs widening.
- **Step 4 (try_update fresh etag)** returns False on Azure →
  `_AzureBlobBackend.upload` ETag handling needs investigation.
- **Step 5 (try_update stale etag)** returns True on Azure →
  CRITICAL bug in ETag preconditioning; would need immediate
  follow-up.
- **Cleanup `_delete_blob`** errors → operator's container needs
  cleanup; not a code bug.

### Shared sub-questions (all candidates)

- **Q-SHARED.1 Commit shape**: per-module (S18-S29 default;
  Recommended) vs per-sub-surface bundled.

(Tag-at-close is resolved at Phase 1 Sub-question 1.TAG; Phase 5
reads that resolution directly without re-decision.)

---

## Phase 3 — Implementation (per-module commits, strict order)

Per Phase 2 commit-shape decision. Default = per-module. Each
commit must satisfy the 6-step per-commit checkpoint protocol
below.

### Non-interleaving rule (CRITICAL for bisectability)

If the chosen candidate has multiple sub-surfaces, do NOT
interleave. Complete each sub-surface fully before starting the
next. Per S22-S29 precedent.

If a mid-sub-surface dependency on the other sub-surface emerges,
HALT and surface as a design-gate sub-question before continuing.

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
    <new S30 test paths if any> -q
# If Candidate K-a is chosen with Q-K-a.4 = Option 2, the
# concrete addition is:
#     tests/classifier/pipeline/test_cost_journal_adls_azurite.py
# (17-path invocation; recompute headline as 970 + N new
# Azurite tests).
```

Expected: previous_baseline + N new tests, all passing. If
failing tests are NOT a deliberate consequence of the surface-
under-test → HALT (and apply the S25-folded "Q-J.8 allowlist may
be incomplete; HALT-and-extend" pattern if the failure is a
same-shape regression outside the prompt's explicit allowlist).

**Phase 0 grep-for-same-shape-tests sanity** (S25 LESSONS
forward-applicable): before starting Phase 3, run a grep against
the test tree for any same-shape tests that pin contracts the
chosen scope will modify. If found and not in the prompt's
explicit replacement allowlist, surface at Phase 0 / Phase 2,
not at Phase 3 mid-commit.

**2. Ruff sanity (touched files only) + mid-implementation format
check per LESSONS**

```
.venv/bin/ruff check <touched paths>
.venv/bin/ruff format --check <touched paths>
```

If unclean → run `ruff format <touched paths>` and re-test; fold
the format-fix into the commit (per S19-S29 pattern).

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

Per S29 LESSONS "Operator-driven script LOC estimates need a
~70-100 LOC additive overhead floor, not a linear multiplier":
if the commit ships a new script/file, claim total LOC (via
`wc -l`) NOT logic-only LOC. Verification-table mismatch on LOC
is a common ✗ source.

**4. `git status` check**

Only intended files staged; no surprise `eval_data/` or
unauthorized `src/barcada_scraper/` changes. Operator-side
`eval_data/` modifications are expected to stay unstaged across
sessions (Sessions 8-29 precedent).

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
Phase 3 start                  : 970  (Session 29 close baseline)
After commit 1                 : >= 970 + N_commit_1_tests
After commit 2                 : >= 970 + N_commit_1_tests + N_commit_2_tests
...
```

**Rule**: the count NEVER decreases between checkpoints. A
decrease means a previously-passing test went red — regression.
HALT.

**Authorized decreases**: only if a Q-* AskUserQuestion at Phase 2
explicitly authorized a same-shape test replacement (e.g.,
Q-J.8-style or Q-StgSplit.4-style 1↔1 replacement preserving
net-zero count). The commit body MUST cite the authorization +
name the replaced test + name the replacement.

Baseline pre-resolved at Phase 1 per Phase 0 Step 0.5: 970 is the
canonical S30 baseline for any candidate that touches the
orchestrator sub-surface OR the driver sub-surface OR the journal
sub-surface (Candidate K-a definitely; A/D/E less so).
Whichever baseline is bound at Phase 1, hold it consistent across
ALL Phase 3 commits in S30 — do not switch mid-session.

If Candidate K-a is chosen with Q-K-a.4 = Option 2 (17-path
invocation), expand the invocation in step 1 of the checkpoint
to include the new test path; recompute the headline as 970 + N
new Azurite tests.

---

## Phase 4 — Pre-push gate (whole-tree)

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 353+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

HALT IF any gate red. Never use `--no-verify`.

### eval_data WIP halt protocol (per LESSONS)

validate_consistency runs against working-tree state. Operator-WIP
edits to `eval_data/*.jsonl` can introduce schema violations that
fail the gate even though no S30 commit touches eval_data.

When this fires:
1. Confirm the failing row's content is in operator-WIP
   (`git diff eval_data/...`), not in committed HEAD
   (`git show HEAD:eval_data/...`).
2. Confirm the S30 commits do not touch eval_data
   (`git diff origin/main..HEAD -- eval_data/`).
3. Surface to operator with the exact row + reason + diff vs
   committed state.
4. Two paths: (a) operator-fix in WT, then re-run gate;
   (b) stash eval_data WIP, push, restore.
5. Do NOT auto-fix locked-artifact content.

S20+S22 precedent: operator chose (a). S21/S23/S24/S25/S26/S27/S28/S29
did not need this protocol at Phase 4 push (S28 saw a transient
"1 error" first-run that cleared on identical re-run with no
intervening edits; S29 did NOT reproduce the transient).
LESSONS-worthy if the transient reproduces in S30+.

---

## Phase 5 — Push + tag

- Push to `origin/main` after operator confirms.
- Tag per Phase 1 Sub-question 1.TAG decision (or defer).

If a workstream-end tag is placed: include annotated message
summarizing all the workstream's work (mirror the
`workstream-a-week1-end` annotation pattern from S22 and the
`workstream-0-end` annotation pattern from S27 — name every
sub-surface commit + map to plan bullets + list any deferrals).

Note: workstream-0-end already placed at S27. workstream-A is
mid-flight (W A.1 closed at S22's `workstream-a-week1-end`; W A.2
is the orchestrator-side robots work landed across S23+S24+S25
plus the K-b script at S29). If Candidate K-a is chosen at S30
AND operator considers it the final W A.2 code milestone
(K-b-exec is execution, not code, so it does not gate the tag), a
`workstream-a-week2-end` annotated tag would be appropriate at
S30 Phase 5.

---

## Phase 6 — Workspace close-out

- Append Session 30 entry to `~/crawler-audit/SESSION_LOG.md`
  including a **Canonical S30-close baseline** block with the
  exact pytest invocation + verified test count (per S22-S29
  LESSONS "Pin the baseline for the next session's Phase 0
  Step 0.5"; without this, S31 Phase 0 will infer from the
  "Combined headline" bullet and potentially HALT on
  accounting-mismatch).
- Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md` for
  Session 31 — explicitly pin the S31 Phase 0 workspace anchor
  SHA per S21-S29 post-audit pattern (LESSONS "Workspace HEAD
  delta tolerance"); do not omit. After the close-out commit
  lands, expect **1-2 follow-up commits** pinning the actual
  SHA (S21 needed 1; S22 needed 2; S27 needed 1; S28 needed 2
  including a post-close hygiene fold; S29 needed 1).
- Update `~/crawler-audit/LESSONS.md` with any new forward-
  applicable patterns surfaced this session.
- Workspace close-out: 1 primary commit + 1-2 follow-up commits
  pinning the anchor SHA and any audit-surfaced corrections.
  Push workspace after operator confirms.

Note: drafting the next-session prompt (`SESSION_31_PROMPT.md`)
is NOT a built-in Phase 6 step. Per S20→S21..S26→S27→S28→S29
precedent, prompt-drafting is operator-commissioned between
sessions — not always-on close-out work. If the operator asks for
it explicitly at S30 close, draft it as a separate follow-up;
otherwise leave for the next session to either operator-commission
or scope out at S31 open.

---

## Acceptance criteria

**Per candidate (reduces if Phase 1 narrows scope):**

### Candidate A (barcada-drift)

Carry-forward from S22-S29 prompts (unchanged):
1. `barcada-drift` (or `barcada-baseline drift`) CLI works
   against ≥2 canary_runs parquets.
2. Drift metric per Q-A.2 implemented + tested.
3. Alert threshold per Q-A.3 implemented + tested.
4. Output shape per Q-A.5 documented + tested.

### Candidate D (Phase 4 PR-D tooling)

1. Tooling shape per Q-D.1.

### Candidate E (cassette corpus expansion)

1. Cassette count grows to Q-E.1 target.
2. FP re-investigation per Q-E.3 if applicable.

### Candidate K-a (Azurite-backed integration test)

1. Azurite-backed integration test passes locally + (if Q-K-a.4
   includes CI) in CI; mock-vs-prod divergence empirically
   closed for the operations covered.
2. If Q-K-a.4 = Option 2 (17-path), the new test path is added
   to the canonical invocation and the Canonical S30-close
   baseline reflects the new headline count.

### Candidate K-b-exec (run the S29 K-b script)

1. Operator-driven script produces the expected 5-step trace
   against a live Azure container.
2. Trace is captured in SESSION_LOG.md / LESSONS.md.
3. Any divergence from DummyBlobBackend behavior is documented
   in a new LESSONS section for S31 to fold.

### Shared (all candidates additionally satisfy)

Items numbered S1-S4 to avoid collision with candidate-specific
numbering.

- **S1.** Combined suite at session close: existing 970 baseline
  + N new tests, all passing. For narrower-baseline candidates,
  the baseline is the chosen narrower count + N new. For K-a
  with Q-K-a.4 = Option 2, the new 17-path baseline.
- **S2.** Pre-push gate runs green (incl. eval_data WIP halt
  protocol applied if needed).
- **S3.** Tag placed per Phase 1 Sub-question 1.TAG OR explicit
  defer.
- **S4.** Regression-protection checklist held (see "Out-of-scope"
  below). In particular:
  - ALL S21-S29 deliverables stay at the SHAs they landed at;
    their public APIs are unchanged.
  - Per-sub-suite test counts stay green (or grow): 32 robots-
    parser / 30 robots_gate / 30 robots_bypass_config / 43
    cost_journal / 13 cost_journal_local / 19 cost_journal_adls
    / 35 robots_integration / 74 vmss_worker / 129 job_runner /
    152 worker_loop / 7 robots_gate_integration (4 S23 +
    2 S24-unchanged + 1 S25-replaced) / 12
    worker_loop_persistence (11 S24-unchanged + 1 S25-replaced)
    / 52 driver (46 S15-anchor + 6 S27-added cost_journal_wiring
    of which one was S28 1↔1 replaced).
  - `docs/CRAWLING_POLICY.md` stays at 77 lines / 2519 bytes
    unchanged from S26 SHA `2314f5e` (verified at Phase 0
    Step 0.9).
  - `tests/runners/fixture_cascade/cascade.py`'s
    `_journal_record_with_breakdown` helper signature unchanged
    from S27 `a1c5636` (verified at Phase 0 Step 0.9).
  - `tests/runners/fixture_cascade/cascade.py` Stage 1 invoker
    uses `_journal_record_with_breakdown(stage=1,
    components={'llm', 'embedding'})` shape (verified at
    Phase 0 Step 0.9 via AST inspection).
  - `src/barcada_scraper/classifier/stage1/run.py` ShardResult
    has `llm_cost_usd` + `embedding_cost_usd` fields (verified
    at Phase 0 Step 0.9 via dataclass introspection).
  - `scripts/smoke_test_adls_cost_journal.py` exists at S29 SHA
    `75a3937` and import-loads cleanly (verified at Phase 0
    Step 0.9).
  - The combined total stays at 970 (or grows) unless a Q-*
    AskUserQuestion explicitly authorizes a same-shape 1↔1
    replacement.

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
  cost_journal.py` are LOCKED at `1d9404e`. The S22 abfss://
  scheme detection in `open_journal` is intact and supplied by
  S25's ADLSCostJournal at the dispatch target.
- The S22 additions to `tests/classifier/pipeline/test_cost_journal.py`
  (14 new tests + 1 updated test) are locked, EXCEPT for the
  S25 Q-J.8-extension replacement at SHA `835a531`.

**S23 deliverables (Session 23 W A.2 sub-surfaces):**
- `src/barcada_scraper/orchestrator/robots_integration.py`
  (244 LOC; public API at `279bb77`).
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

**S24 deliverables (Session 24 W A.2 sub-surfaces):**
- The 3 module-level private helpers in
  `src/barcada_scraper/orchestrator/worker_loop.py` at `48c324a`:
  `_open_cost_journal_for_worker` (BODY modified at S25
  `aed7873`; SIGNATURE locked at S24), `_ensure_journal_initialized`
  (LOCKED at S24), `_build_durable_bypass_writer` (LOCKED at S24).
- The 3-line wiring block in `scrape_stage2_pages_invoker` at
  `48c324a`. Adjacent comment updated at S25 `aed7873`.
- The 5 retargeted test_stage2_pages_invoker_* fixtures in
  `tests/orchestrator/test_worker_loop.py` at `48c324a`. Locked
  — do NOT revert to abfss://.
- `tests/orchestrator/test_worker_loop_persistence.py` at S25
  `aed7873` (12 tests; 11 S24-unchanged + 1 S25-replaced).
- The 3 S24-added tests in
  `tests/orchestrator/test_robots_gate_integration.py` —
  2 S24-unchanged + 1 S25-replaced at SHA `aed7873`.

**S25 deliverables (Session 25 W A.2 sub-surfaces):**
- `src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
  at S25 SHA `835a531` (295 LOC; full backend; public API:
  `ADLSCostJournal`, `BlobNotFoundError`, `ConditionNotMetError`,
  `_BlobBackend` Protocol, `_AzureBlobBackend`, `_abfss_to_https`).
  Candidate K-a may CONSUME `ADLSCostJournal` but MUST NOT
  modify the public API signatures without explicit Phase 2
  authorization. Candidate K-a (Azurite-backed test) may ADD a
  separate test file under `tests/classifier/pipeline/` but MUST
  NOT modify `cost_journal_adls.py` itself.
- `tests/classifier/pipeline/test_cost_journal_adls.py` at S25
  SHA `835a531` (19 tests + the `DummyBlobBackend` helper class).
  Locked.
- The S25 Q-J.8-extension replacement in
  `tests/classifier/pipeline/test_cost_journal.py` at SHA
  `835a531` (`test_open_journal_abfss_routes_to_adls_journal`).
  Locked.
- The body-only modification to
  `src/barcada_scraper/orchestrator/worker_loop.py`'s
  `_open_cost_journal_for_worker` at S25 SHA `aed7873`.
- The S25 invoker-site comment update at SHA `aed7873`.

**S26 deliverables (Session 26 W A.1 W8 sub-surface):**
- `docs/CRAWLING_POLICY.md` at S26 SHA `2314f5e` (77 lines /
  2519 bytes; the W A.1 robots-compliance doc tightened from
  8.1 KB to 2.52 KB). No candidate at S30 should modify this doc
  unless Phase 2 design-gate explicitly authorizes further
  tightening, extension, or rewrite.

**S27 deliverables (Session 27 W A.0 W5.X sub-surface):**
- `tests/runners/fixture_cascade/cascade.py` per-tier wiring
  changes at S27 SHA `a1c5636`:
    - Module docstring "Per-tier cost-accounting wiring
      (WA0.W5.X, S27 Candidate B + S28 Candidate StgSplit)"
      paragraph (extended at S28 to reflect Stage 1 closure).
    - Module-level helper `_journal_record_with_breakdown` with
      the signature
      `(*, journal, shard_id, stage, started_at,
        domains_processed, components, unattributed_cost_usd=0.0)
        -> None`.
      Signature locked at S27; further modifications require
      Phase 2 design-gate authorization.
    - Stage 2 invoker (`components={fetch, summarization,
      classification}, unattributed_cost_usd=0.0`). Locked.
    - Stage 3 invoker (`components={evidence, primary, secondary},
      unattributed_cost_usd=s3_result.fetch_cost_usd`). Locked.
    - Stage 1 invoker SWITCHED at S28 SHA `9afde57` to use
      `_journal_record_with_breakdown` with
      `components={'llm': s1_result.llm_cost_usd, 'embedding':
      s1_result.embedding_cost_usd}, unattributed_cost_usd=0.0`.
      Locked at S28; further modifications require Phase 2
      design-gate authorization.
- `tests/runners/fixture_cascade/test_cost_journal_wiring.py` at
  S27 SHA `a1c5636` (338 LOC; 6 tests). S28 1↔1 same-shape
  replaced `test_stage1_per_tier_slots_remain_zero_by_design`
  with `test_stage1_per_tier_slots_populate_from_split` at SHA
  `ae9e627` (net-zero count). Module docstring updated at S28
  to reflect Stage 1 closure. No candidate at S30 should
  modify this file unless Phase 2 design-gate explicitly
  authorizes.

**S28 deliverables (Session 28 carry-forward closure):**
- `src/barcada_scraper/classifier/stage1/run.py` at S28 SHA
  `776d203`:
    - `ShardResult` adds 2 fields `llm_cost_usd: float` and
      `embedding_cost_usd: float` between `cost_usd` and
      `cached_input_tokens`. Field count 12 → 14. Locked at
      S28; further field additions require Phase 2 design-gate
      authorization.
    - `_build_shard_result` body updated to populate the 2 new
      fields from `cost_tracker.llm_cost_usd` /
      `cost_tracker.embedding_cost_usd`. Locked.
    - Docstring documents cardinal invariant
      `cost_usd == llm_cost_usd + embedding_cost_usd`.
- `tests/classifier/stage1/test_run_cascade.py` at S28 SHA
  `776d203`:
    - +1 net-new test
      `test_shard_result_carries_llm_and_embedding_cost_split`
      asserts both new fields present + non-negative + invariant
      holds + values agree with the source CostTracker
      properties. Locked.
- `tests/runners/fixture_cascade/cascade.py` Stage 1 invoker
  switch at S28 SHA `9afde57`:
    - Stage 1 invoker block replaced (formerly used
      `_journal_record`; now uses `_journal_record_with_breakdown`
      with `components={'llm', 'embedding'}`). Locked.
    - Removed now-orphaned `_journal_record` helper (24 LOC). Do
      NOT re-introduce this helper without Phase 2 design-gate
      authorization.
    - Module docstring updated to reflect all 8 `_TOTALS_FIELDS`
      slots wired. Locked.
- `tests/runners/fixture_cascade/test_cost_journal_wiring.py`
  1↔1 same-shape replacement at S28 SHA `ae9e627`:
    - `test_stage1_per_tier_slots_remain_zero_by_design` REMOVED.
    - `test_stage1_per_tier_slots_populate_from_split` ADDED at
      same shape. Locked.
    - `test_injected_adjudicator_costs_route_to_correct_slots`
      comment updated from "$0 by design" to "$0 empirically
      because the 3 sample fixtures rules-classify". Locked.
    - Module docstring updated to "S27 Candidate B + S28
      Candidate StgSplit — all 8 `_TOTALS_FIELDS` slots are
      wired". Locked.

**S29 deliverables (Session 29 carry-forward closure — NEW for S30 lock-list):**
- `scripts/smoke_test_adls_cost_journal.py` at S29 SHA
  `75a3937` (220 LOC including 13-line Copyright header +
  ~28-line module docstring):
    - Operator-driven 5-step ETag-conflict-matrix smoke against
      a live Azure container. Public-API-only consumption of
      `ADLSCostJournal`. Mirrors `scripts/smoke_test_adls_gen2.py`
      conventions (Copyright header, argparse, env-var-driven
      auth, auto-delete cleanup via parallel `BlobClient`).
    - Argparse: `--account`, `--container`, `--prefix`,
      `--run-id`, `--ceiling-usd`; env-var defaults from
      `AZURE_STORAGE_ACCOUNT` / `AZURE_STORAGE_CONTAINER`.
    - Auth precedence: `AZURE_STORAGE_KEY → AzureNamedKeyCredential`
      else `DefaultAzureCredential`.
    - 5-step trace: write_initial → re-write_initial (412) →
      read → try_update happy → try_update stale (412); auto-
      delete in finally via parallel `BlobClient`.
    - Exit codes: 0 success / 2 missing account / 3-6 per-step
      failure. stderr for FAIL lines; stdout for OK lines.
    - LOCKED — further modifications to the script require
      Phase 2 design-gate authorization at the session that
      proposes them. Adjacent files (other `scripts/smoke_*`
      siblings) are NOT locked.

**W4.1.5 driver orchestration (locked since W4.1.5 close):**
- `tests/runners/fixture_cascade/` (except via W5.X-prefix commit
  with explicit operator auth — only S16/S27/S28 W5.X commits
  have opened this surface; all are closed).

**Baseline-v0 ground truth:**
- The committed `tests/fixtures/baseline-v0/` snapshot at `9e9a1fb`
  (1213 files).

**Existing W6 sub-surface (Session 18):**
- `tools/baseline_v0/generate.py`
- `tools/baseline_v0/determinism.py`
- Existing `generate` subparser in `tools/baseline_v0/cli.py`

**Schemas + plans (locked):**
- `expected.schema.json` v1.1
- `META_SCHEMA.md` v1.1
- `meta.schema.json` v1.0
- `stage1.schema.json` v1.0
- All workstream tags at their placed SHAs (11 tags as of S27/S28/S29
  close)
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` (READ-ONLY)
- `CLASSIFICATION_ADJACENT_PLAN.md` (UPDATED only when AI/ML
  decisions land)
- `RECONCILIATION_2026-05-21.md`
- `docs/phase4_implementation_plan.md` (Phase 4 governance
  reference)

**Operator-owned territory:**
- All of `eval_data/` — labeling-workstream territory; per-row WIP
  edits across sessions are expected and unstaged (Sessions 8-29
  precedent). S22→S29 inter-session operator-side eval_data
  COMMITS are tolerated per the "Workspace HEAD delta tolerance"
  LESSONS pattern — verify they're eval_data-only via
  `git show --stat <sha>` for each commit in the delta.

**Production code:**
- `src/barcada_scraper/` — locked unless Phase 2 design-gate
  explicitly authorizes a specific module. S21-S25+S28 authorized:
  `scraper/robots.py`, `scraper/robots_gate.py`,
  `scraper/robots_bypass_config.py`,
  `classifier/pipeline/cost_journal.py` (additive only),
  `classifier/pipeline/cost_journal_adls.py` (S25 skeleton →
  full backend),
  `orchestrator/robots_integration.py` (new),
  `orchestrator/vmss_worker.py` (additive),
  `orchestrator/job_runner.py` (additive),
  `orchestrator/worker_loop.py` (additive: S23 gate wiring +
  S24 persistence helpers + S25 abfss:// guard removal in 1
  helper body),
  `classifier/stage1/run.py` (S28 additive: ShardResult +2 fields
  + _build_shard_result populate).
  S26 + S27 + S29 added no new src/ authorizations (doc-only,
  driver-only, or scripts-only respectively).
  None of the S30 candidates currently anticipate new src/
  authorizations.

**Pipeline configs:**
- `configs/`

**Phase 4 work:**
- Phase 4 PR-D/E/F/G work UNBLOCKED on the W0 side since S27
  (workstream-0-end placed); still gated on operator-led Stage 2/3
  labeling. Candidate D opens when labeling begins.

---

## Verify-before-asking discipline (strict rule from S19-S29)

Per `[[double-check-before-commit]]` memory: **ALWAYS verify
every concrete claim in the commit message against actual source/
output BEFORE staging.** Fixture names, file counts, exit codes,
line counts, test counts, helper names, smoke outcomes, SHA
prefixes, regex matches, API signatures. No claims by pattern-
completion. Build a verification table in chat (claim → reality →
status) and reconcile before "Confirm to commit?".

Specific to S30:

- Before each chosen-candidate-specific claim in a commit message,
  verify against the actual source / runtime output:
  - Candidate A: barcada-drift CLI invocation produces the
    expected output shape against ≥2 parquets.
  - Candidate D: tooling smoke produces expected output.
  - Candidate E: cassette count post-record; FP-curation log
    updated.
  - Candidate K-a: Azurite container produces the expected 412
    on race-loser write_initial; full ETag-conflict matrix
    passes.
  - Candidate K-b-exec: operator-captured trace verbatim.
- Before claiming combined suite count, re-run pytest.
- Before claiming ruff/format clean, re-run ruff against the
  touched files.
- Before claiming a SHA prefix in a commit message body, verify
  the prefix is correct via `git show --no-patch --format=%h <ref>`.
- Before claiming a new-file LOC count, run `wc -l` on the
  delivered file (NOT the logic-only estimate) per S29 LESSONS.

Avoid bash pipe artifacts that mask Python exit codes (LESSONS):
`python_cmd 2>&1 | grep ... | tail` makes `$?` reflect tail's
exit. Use `> stdout.out 2> stderr.err; echo $?` or
`${PIPESTATUS[0]}` when exit-code matters.

LESSONS-folded discoveries from S22-S29 worth re-applying:

- **Plan-vs-reality at Phase 2** (S22 LESSONS): plan §5 wording
  may name a module/site that doesn't match the actual code
  shape. Verify the actual integration site via Explore BEFORE
  drafting Q-* options.

- **Phase 2 source-verify drives option-set design** (S25 LESSONS):
  for any candidate touching a new SDK / external system / language
  feature, verify the underlying facts BEFORE drafting AskUserQuestion
  options. If a fact-check would invalidate one or more options,
  the question structure is misleading the operator. Re-shape the
  option set first, then ask. S28 demonstrated this directly:
  pre-Q-StgSplit grep showed CostTracker already had
  llm_cost_usd / embedding_cost_usd properties, collapsing
  Q-StgSplit.1 from 3 options to 2 and narrowing Q-StgSplit.7's
  src/ scope estimate from ~80-100 LOC to ~10-15 LOC. S29 also
  demonstrated this: reading cost_journal_adls.py at Phase 2
  confirmed `_AzureBlobBackend` takes a credential OBJECT (not
  shared-key kwargs); this shaped Q-K.b.3 to be precise about
  adapter-construction wording.

- **Implicit-authorization HALT** (S22-S29 LESSONS): Q-*
  answers may require touching files NOT in S30 Out-of-scope's
  authorized-touch list (e.g., introducing a new helper module
  for Azurite-specific test setup). Surface explicit authorization
  in Phase 2 BEFORE the commit, not as a HALT mid-Phase-3.

- **Q-J.8 explicit allowlist may be incomplete; HALT-and-extend
  pattern** (S25 LESSONS): Out-of-scope + Q-*-style explicit
  allowlists are defenses against silent scope expansion, not
  exhaustive inventories. Grep for same-shape items at Phase 0;
  HALT-and-extend if surfaced mid-Phase-3; land regression + fix
  atomically.

- **Local imports defeat module-attribute monkeypatch** (S25
  LESSONS): when writing tests that mock a name a target function
  calls, identify the import site (top-of-module vs deferred-
  inside-function) BEFORE assuming the textbook monkeypatch
  pattern. Deferred imports require patching at the SOURCE module.

- **Tightened-precondition test-fixture retargeting** (S24
  LESSONS): if the chosen candidate introduces stricter
  preconditions on any tests, retarget those fixtures in the same
  commit as the src change. Bundle for bisectability.

- **Test against public API surface only** (S24 LESSONS, S29
  extension): tests should probe behavior via the public surface.
  Avoid asserting on private attrs. S29 extended the same pattern
  to operator-driven scripts: when a script needs an operation a
  wrapper class doesn't expose (e.g., `delete_blob` on
  `ADLSCostJournal`), construct a parallel SDK client with the
  same auth + URL rather than reach into private attrs.

- **Source-verify line numbers per Phase 3 commit** (S23
  LESSONS): worker_loop.py is ~3000+ LOC post-S25; stage1/
  files may also have drifted. Re-Explore at session-current HEAD
  before drafting commit edits.

- **AskUserQuestion 4-option limit can silently truncate a Q-*
  option set** (S26 LESSONS): count the Q-* option set BEFORE
  drafting AskUserQuestion calls. If >4 mutually-exclusive
  options, tier the question or split horizontally.

- **Deferred wiring gaps fold cleanly into workstream-end if the
  original implementation left a parallel-API seam** (S27
  LESSONS): when scoping a candidate that closes a deferred gap,
  re-source-verify at Phase 2 that the seam still exists. APIs
  drift between sessions; treating a years-old disposition as
  gospel without re-verifying is the path to wrong Q-* options.

- **Empirical-vs-by-design distinction in test pins** (S28
  LESSONS): when closing a deferred gap or extending an existing
  surface, audit existing test pins for "$X == 0.0 by design"
  assertions. Either 1↔1 replace them with the new design pin OR
  re-frame their comments to clarify the assertion is now
  empirical rather than design-load-bearing.

- **Phase 0 fixture-count commands need `2>/dev/null` + a
  bounded timeout** (S28 post-close LESSONS): bare `find`
  invocations can hang indefinitely in shell-wrapped contexts.
  Use the Python `rglob()` pattern in Step 0.4; if shell `find`
  is unavoidable, always filter stderr and bound wallclock both
  via the Bash tool's `timeout` arg AND via `timeout 60s`
  prefixed on the inner command.

- **Operator-driven script LOC estimates need a ~70-100 LOC
  additive overhead floor, not a linear multiplier** (S29
  LESSONS): Copyright + docstring + imports + argparse total
  ~70-100 LOC of overhead in this codebase, ADDITIVE to whatever
  logic the script needs. So "~30 LOC logic" → ~100-130 LOC
  delivered (overhead dominates; total/logic ≈ 3-4×), but
  "~300 LOC logic" → ~370-400 LOC delivered (overhead is a
  smaller fraction; total/logic ≈ 1.3×). Do NOT multiply linearly
  by ~3×; the K-b ~3× ratio was a small-logic special case.
  Verification-table LOC claims should use `wc -l` on the
  delivered file (not the estimate), or expect ✗ rows.

- **Public-API-only cleanup pattern extends from tests to
  operator scripts** (S29 LESSONS): when an operator-driven
  script needs an operation a wrapper class doesn't expose
  (e.g., `delete_blob` on `ADLSCostJournal`), construct a
  parallel SDK client with the same auth + URL rather than
  reach into private attrs. Same auth, same URL, no
  private-attr coupling. Same principle as S24's test pattern,
  broader scope.

- **Empirical Phase 1 prerequisite check before scope-narrow**
  (S29 LESSONS): when a candidate's prereqs are external-state-
  dependent (e.g., "≥2 parquets on disk", "launchd installed",
  "AI/ML decisions resolved"), run the empirical check at
  Phase 1 BEFORE re-issuing the scope question. Gives the
  operator a concrete go/no-go rather than a "depends on what's
  on disk" qualifier. S29 confirmed Candidate A's prereqs
  empirically unmet (0 parquets, no plist, no AI/ML responses)
  before the operator picked K-b.

---

## Commit hygiene (per LESSONS + S19-S29 additions)

- File-based commit messages at `/tmp/<id>-msg.txt`.
- Per-module commits (Phase 3 commit shape unless Q-SHARED.1
  overrides).
- "Confirm to commit?" before EVERY commit. Pair with verification
  table (always) and `git diff --staged` (when appropriate per
  `[[double-check-before-commit]]` triggers).
- Commit body includes: action ref (e.g., S29 used
  `WA2.W8.adls-live-smoke`; S30 chooses its own per candidate),
  scope summary, file touches, test count delta (with net-new vs
  newly-in-invocation pre-existing distinction per S23 LESSONS),
  plan reference. NO `Co-Authored-By`.
- Pre-push gate must run green. Never use `--no-verify`.
- Pre-push vermin: `git ls-files '*.py' | xargs vermin
  --target=3.10` to filter venv-internal pytest 3.14 false-
  positives.
- Mid-implementation ruff format-check, not only pre-push.
- For S19-S29-test modifications: explicit Phase 2 authorization
  required; document the modification scope explicitly in the
  commit body (per S22-S29 LESSONS "Implicit-authorization HALT"
  pattern).
- Workspace close-out (Phase 6) lands as its own commit at session
  close, followed by 1-2 follow-up commits pinning the anchor SHA
  for the next session (S21-S29 pattern). S26 demonstrated that a
  POST-close-out correction commit is sometimes necessary; S28
  demonstrated that a POST-close-out hygiene fold can also land
  after the anchor-pinning follow-up. When this happens, the new
  HEAD supersedes the prior pin, and the next session's Phase 0
  will need to tolerate the additional commit per the Workspace
  HEAD delta tolerance pattern.

---

## Context-window awareness

S29 ran across 1 commit + Phase 2 source-verification + Phase 6
close-out (2 close-out commits), comfortably within context. S30
budget per scope:

- Candidate A: medium (~300 LOC logic + ~70-100 LOC overhead
  floor ≈ ~370-400 LOC delivered; see Phase 1 Candidate A for
  the additive-overhead framing that supersedes a linear ~3×
  multiplier).
- Candidate D: small.
- Candidate E: small.
- Candidate K-a: medium (~50-100 LOC logic + ~70-100 LOC
  overhead floor ≈ ~120-200 LOC delivered + Docker setup).
- Candidate K-b-exec: ~0 LOC (operator-driven; Claude Code only
  interprets trace).

Strategies:
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore
  subagent per S22-S29 "Explore-subagent + spot-check" LESSONS
  pattern.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before the chosen S30 scope closes,
  transition per "no mid-commit-batch transitions" — finish
  in-flight sub-surface, then close session and refill the
  transition template for Session 31.

---

## Reporting in chat at session close

After all Session 30 commits land + push + close-out per the
S13-29 pattern:

1. Commit SHA(s) of each S30 sub-surface.
2. Sub-surface(s) landed (per candidate).
3. Test count delta: 970 (or 480/538/944/17-path) baseline → S30 close.
4. Driver suite count at S30 close (52/52 expected unless
   candidate added new driver-area tests).
5. Files touched per sub-surface.
6. Tag dispositions (incl. any new tag per 1.TAG).
7. Per-tier cost-accounting wiring: CLOSED end-to-end since S28
   (regression-protection enforced via Phase 0 Step 0.9 invariant
   smokes + Phase 3 per-commit checkpoint).
8. ADLSCostJournal live-smoke disposition: K-b SHIP closed S29;
   K-a CI test status + K-b-EXEC trace status per S30 scope.
9. Any spend (LLM, infrastructure, cassette-capture).
10. Robots.txt compliance log (if Candidate E expanded the
    cassette corpus).
11. FP-curation log update (if Candidate E expanded the cassette
    corpus).
12. Verify-before-asking summary: any source-verification
    findings surfaced.
13. Outstanding items for Session 31.
14. Tags state at S30 close.

Do not propose Phase 4 PR-D/E/F/G work this session unless
Candidate D was chosen and operator-led labeling is in flight.

---

## Carry-forward bakes (no amendment file needed)

All S29 close-out commits (`0708a53` primary + `e736eee` anchor
follow-up) plus the S29 deliverable have been folded directly
into this prompt — S30 does not need a separate amendment file:

- **S29 close-out anchors** folded into Step 0.1 (workspace
  anchor `e736eee` with operator-eval_data-commit + prompt-
  drafting-commit tolerance; repo anchor `75a3937` with
  operator-eval_data-commit tolerance), Step 0.5 (Canonical
  S29-close baseline 970 pinned with 16-path invocation +
  sub-totals + breadcrumb note for the S28 +1 net-new test
  location; 944 narrower for candidates that don't touch ADLS
  or robots_gate_integration), Step 0.9 (S24+S25+S26+S27+S28
  stability PLUS new S29 K-b script existence + import-load
  check + public-surface verification).
- **2 LESSONS sections from S29 close**:
  - "Operator-driven script LOC estimates need a ~70-100 LOC
    additive overhead floor, not a linear multiplier"
    referenced at Phase 2 "CRITICAL Phase 2 hygiene from S29
    LESSONS (LOC budgeting)" (apply when sizing any candidate
    with new files) AND at the Verify-before-asking section's
    LESSONS-folded-discoveries list.
  - "Public-API-only cleanup pattern extends from tests to
    operator scripts" referenced at Phase 2 (in Candidate K-a's
    sub-question about Azurite-specific test setup) AND at the
    Verify-before-asking section's LESSONS-folded-discoveries
    list (as an extension of S24's test pattern).
- **Empirical Phase 1 prerequisite check** (S29 LESSONS-worthy
  pattern; folded but not yet a stand-alone LESSONS section)
  referenced at Phase 1 "Empirical prereq audit at S29 close"
  (for Candidate A) AND at the Verify-before-asking section's
  LESSONS-folded-discoveries list.

If new amendments arise pre-S30 open, walk them per the reviewer-
feedback hygiene pattern in this prompt's "Reviewer-feedback
hygiene" section.
