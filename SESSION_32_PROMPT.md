# Session 32 prompt — scope picked at Phase 1
# (S31 closed Candidate E to 25 cassettes; S32 chooses from carry-
#  forwards A/D/E-continuation/K-a — no new carry-forward introduced
#  by S31 beyond the E-to-30 continuation room)

**Drafted at Session 31 close (2026-05-31).** Mirrors the
S20/.../S30/S31 prompt structure. Scope-agnostic at Phases
0/1; scope-specific design gates at Phase 2 per chosen candidate.
Strict 7-phase ordering with halt-on-mismatch preserved.

This prompt should be invoked from `~/crawler-audit/SESSION_32_PROMPT.md`
or operator-mirrored to `~/Downloads/session-32-prompt.md`. Re-read
it on session open.

---

## Scope

Engineering session. Workstream sub-surfaces available after
Session 31 closed Candidate E (cassette corpus expansion, 20 → 25;
1 artifact-only repo commit). Repo HEAD at `06d67c4`
(WA0.W7.cassettes-corpus-expansion; ADVANCED from S31 open
`af6f1d4`). Workspace HEAD at the S31 post-close LESSONS-fold +
this prompt-drafting commit (see Step 0.1). **Workstream 0 fully
closed at S27 via the `workstream-0-end` tag at `a1c5636`**.

Carry-forward candidates entering S32:

- **barcada-drift (Candidate A)** — deferred per Q1.1=(A) at S20;
  still needs 4 AI/ML decisions per CLASSIFICATION_ADJACENT_PLAN.md
  §Item 8 AND 2+ `canary_runs/*.parquet` files. **S31 re-confirmed
  empirically** that the launchd installer has NOT been run as of
  S31 close (no plist in `~/Library/LaunchAgents/`; 0 parquets on
  disk). Same state as S29/S30 close.

- **Phase 4 PR-D tooling (Candidate D)** — operator-led labeling
  territory. W0-side unblocked since S27 (`workstream-0-end`
  placed); still gated on operator-led Stage 2/3 labeling.

- **Cassette corpus expansion — continuation (Candidate E)** —
  S31 grew the corpus 20 → 25 (patagonia.com / deere.com /
  ford.com / pfizer.com / wholefoodsmarket.com). The plan's upper
  bound is 30 (§4 W7 "~20-30 representative domains"), so another
  **+5** is available. Recording mechanics proven at S31. **If
  chosen, rebalance the candidate pool toward nonprofit / media /
  education domains** (lower WAF incidence) to offset S31's
  commerce-heavy skew, per the S31-folded LESSONS "~40% yield" +
  "writes-before-validates" notes.

- **ADLSCostJournal Azurite-backed CI test (Candidate K-a)** —
  **OPTIONAL** per the S30-folded LESSONS posture-validation note.
  The K-b operator-smoke (executed S30, trace clean) empirically
  closed the mock-vs-prod divergence risk that K-a would have
  permanently protected against. K-a is defense-in-depth ONLY;
  NOT on any critical path. Operator may still choose it if a
  permanent CI safety net is desired for `cost_journal_adls.py`
  churn.

**No new carry-forward introduced by S31** beyond the E-to-30
continuation room. The S31 cassette additions are fixture-only;
the canonical 970 test count is unchanged.

Operator chooses at Phase 1 which candidate Session 32 ships.
Each candidate has its own Phase 2 design-gate template.

**Sessions 13-31 precedent:** this session does NOT modify the
W4.1.5 driver orchestration at `tests/runners/fixture_cascade/`
(locked at `dd64963` for original files; `cascade.py` extended at
`a1c5636` under S27 W5.X-prefix authorization, and at `9afde57`
under S28 W5.X-prefix authorization; `test_cost_journal_wiring.py`
added at `a1c5636` under S27 authorization and modified at
`ae9e627` under S28 Q-StgSplit.4 1↔1-replacement authorization).
Does NOT modify `expected.schema.json` v1.1 / `META_SCHEMA.md`
v1.1. Does NOT modify the committed `tests/fixtures/baseline-v0/`
snapshot at `9e9a1fb`. Does NOT modify the Session 19-30
deliverables. Does NOT modify the **S31 cassette deliverables**
at `06d67c4` (the 5 new cassette dirs) UNLESS a Candidate E
continuation explicitly adds NEW dirs (never re-records or
deletes the existing 25).

Does NOT modify production code under `src/barcada_scraper/`
UNLESS Phase 2 design-gate explicitly authorizes a specific
module. None of the S32 candidates (A/D/E/K-a) currently
anticipate new src/ authorizations. (Candidate E is fixture-only;
Candidate K-a will likely consume `ADLSCostJournal` without
modifying it.)

Full regression-protection checklist in **Out-of-scope** at the
end of this prompt. Re-read it before any code lands.

---

## Reviewer-feedback hygiene (if this prompt is reviewed)

If an external reviewer (operator-invoked) flags items in this
prompt before Session 32 starts, walk each flagged item against
on-disk reality at the workspace HEAD and repo HEAD `06d67c4` (or
whatever HEAD the operator's machine carries), BEFORE applying any
change. Per S19-S31 pattern (LESSONS "Reviewer-feedback hygiene"):

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
halts catch hidden scope expansion (per S22-S31 "Implicit-
authorization HALT for src/-locks"). Phase 3 halts catch
regressions (including same-shape test failures outside the
prompt's explicit allowlist). Phase 4 halts catch pre-push gate
failures (incl. operator-WIP-in-locked-tree).

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

Run in order. Halt and surface to operator on any mismatch.

### Step 0.1 — Workspace + repo HEAD

```
# Workspace at Session 32 start. S31 close-out landed across:
# e1e7ade (primary close-out: SESSION_LOG.md +
# SESSION_TRANSITION_TEMPLATE.md + LESSONS.md) + 8c80c26 (anchor-
# pin follow-up) + a post-close LESSONS-fold commit (folds the 2
# S31-folding sections "Recorder writes-before-validates" +
# "Recording yield ~40%" + the SESSION_LOG cross-reference + the
# Step 0.4 variable-name pin) + this prompt-drafting commit.
git -C ~/crawler-audit rev-parse HEAD
# Expect: b5f6bc5 (S31 post-close: folds the 2 S31-folding LESSONS
# sections + the SESSION_LOG cross-reference + the Step 0.4
# variable-name pins + this S32 prompt draft; succeeds the
# anchor-pin 8c80c26, which succeeds the primary close-out
# e1e7ade) OR this anchor-pin follow-up of b5f6bc5 OR a later
# commit if additional workspace doc edits / further prompt
# revisions landed post-fixes. If N commits ahead, verify each
# prior commit's subject via `git log --oneline b5f6bc5..HEAD`
# against expected prompt-finalization / doc-edit patterns;
# surface the SHA delta and request authorization if anything is
# unexpected. (S20-S31 precedent: operator authorized continuation
# when 1-3 extra workspace commits were the strengthened prompts
# themselves.)

# Repo at Session 31 final state:
git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: 06d67c4 (WA0.W7.cassettes-corpus-expansion: +5
# business-classification cassettes (S31 Candidate E)).
#
# Tolerated delta: operator-side eval_data labeling commits between
# S31 close and S32 open are expected (Sessions 8-31 precedent).
# Per the S22-folded "Workspace HEAD delta tolerance" LESSONS
# pattern: tolerate N additional commits as long as EACH commit's
# stat is strictly within eval_data/* (no src/barcada_scraper/*,
# no tests/* [INCLUDING no tests/fixtures/synthetic_crawls/*], no
# scripts/*, no docs/* touches). Verify via `git show --stat <sha>`
# for every commit in 06d67c4..HEAD; surface any non-eval_data
# delta for operator authorization before continuing.
```

### Step 0.2 — Tags (13 expected; unchanged from S30/S31 close)

```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort
# Expect 13 tags as of S31 close (UNCHANGED from S30 close; S31
# placed no tag per its 1.TAG = defer for Candidate E):
#   baseline-v0
#   pre-remediation-2026-05-19
#   workstream-0-end                            (placed S27 at a1c5636)
#   workstream-0-week1-end
#   workstream-0-week2-end
#   workstream-0-week3-end
#   workstream-0-week4-1-5-end
#   workstream-0-week4-end
#   workstream-0-week5-end
#   workstream-0-week7-end
#   workstream-a-week1-end
#   workstream-stage1-prestaged-flags-end       (operator-side; -> af6f1d4)
#   workstream-stage1-step3-end                 (operator-side; -> d4f06b8)

git -C /Users/administrator/projects/barcada-scraper rev-list -n 1 workstream-0-end
# Expect: a1c5636… (matches the S27 placement; UNCHANGED).

# Tolerated delta: additional operator-side stage1-* / eval_data-*
# tags may land between S31 close and S32 open per the operator's
# labeling workflow cadence. For each new tag beyond the 13
# expected, verify the tagged commit is eval_data-only via
# `git show --stat <tag>`; if so, treat as operator-domain marker.
# If a new tag points at any src/barcada_scraper/* / tests/* /
# scripts/* / docs/* commit, HALT for operator authorization.
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
#   - cascade.py extended at a1c5636 (S27) and 9afde57 (S28).
#   - test_cost_journal_wiring.py added at a1c5636 (S27) + modified
#     at ae9e627 (S28).
# Any non-empty diff outside these 3 files = HALT.
# S29 + S30 + S31 did NOT touch this surface.
```

### Step 0.4 — Fixture counts (use Python pattern per S28 LESSONS hygiene fold)

**IMPORTANT**: per S28-folded LESSONS "Phase 0 fixture-count
commands need `2>/dev/null` + a bounded timeout", do NOT use bare
`find` invocations here. Use the Python pattern below.

**FLAGGED CHANGE FROM S31**: `cassette_count` and
`exclusions_count` BOTH advance 20 → **25** (S31 added 5 cassette
dirs at `06d67c4`). The other 4 counts are unchanged. Do NOT
leave these at `== 20` or this step HALTs falsely.

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
assert cassette_count == 25, cassette_count    # WAS 20 through S30; +5 at S31
assert exclusions_count == 25, exclusions_count  # WAS 20 through S30; +5 at S31
print(f'OK fixture counts: html={html_count} expected={expected_count} meta={meta_count} baseline={baseline_count} cassette={cassette_count} exclusions={exclusions_count}')
"
```

If the assertions fire, HALT and surface to operator.

**Fallback `find` pattern** (NOT recommended): always include
`2>/dev/null` AND wrap the Bash tool call with `timeout=60000` AND
prepend `timeout 60s`. Kill before retry if any command hangs
>30 seconds.

### Step 0.5 — Test-suite baseline (S32 canonical)

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
# Sub-totals (16 paths; ALL identical to S27/S28/S29/S30/S31 close
# — S31 added only fixture-only cassettes, NOT exercised by any
# test in the invocation; the 33 synthetic_crawl tests are
# hermetic):
#   210 conformance + 52 driver + 99 baseline_v0 +
#    33 synthetic_crawl + 32 robots + 30 robots_gate +
#    30 robots_bypass_config + 43 cost_journal +
#    13 cost_journal_local + 19 cost_journal_adls +
#    35 robots_integration + 74 vmss_worker +
#   129 job_runner + 152 worker_loop +
#     7 robots_gate_integration + 12 worker_loop_persistence = 970
#
# Pinned in SESSION_LOG.md "Canonical S31-close baseline" block.
```

The sub-paths add up to 970. Any drift = halt. If the headline
mismatches, re-run each sub-path independently to localize.

**Narrower baselines**:
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 944 (S27-S31-equivalent narrower; canonical 16-path minus 19
  cost_journal_adls minus 7 robots_gate_integration).

If Candidate K-a is chosen with Q-K-a.4 = Option 2, the canonical
16-path MAY extend to a **17-path invocation** with a new
Azurite-backed test file. Whichever baseline is bound at Phase 1,
hold it consistent across ALL Phase 3 commits in S32.

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

# S20 canary + cassettes sub-surface.
# NOTE (S31 LESSONS): the combined `-k 'canary'` command shows
# "23 passed, 48 deselected" because pytest's -k filter applies to
# the WHOLE collection and deselects the synthetic_crawl tests
# (no 'canary' in their names). This is NOT a regression. Verify
# the 56 as two separate runs instead:
.venv/bin/python -m pytest tests/baseline_v0/test_canary.py -q          # expect 17
.venv/bin/python -m pytest tests/baseline_v0/test_cli.py -k 'canary' -q # expect  6
.venv/bin/python -m pytest tests/synthetic_crawl/ -q                    # expect 33
# 17 + 6 + 33 = 56.

# S21-S26 sub-surfaces (collapsed sum = 576):
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
# Sum: 32+30+30+43+13+19+35+74+129+152+7+12 = 576

# S27 + S28 per-tier cost-accounting wiring tests
.venv/bin/python -m pytest tests/runners/fixture_cascade/test_cost_journal_wiring.py -q
# Expect: 6 passed

# S28 Stage 1 ShardResult split tests (outside canonical 16-path)
.venv/bin/python -m pytest tests/classifier/stage1/test_run_cascade.py tests/classifier/stage1/test_cost_tracker.py -q
# Expect: 32 passed (16 run_cascade + 16 cost_tracker)
```

### Step 0.9 — S25-S30 invariants + S31 cassette-dir presence

```
# Verify the S25-S30 deliverables match what landed at each
# session's close, AND that the 5 S31 cassette dirs exist.
# Re-run unconditionally at every S32 cold start.

.venv/bin/python -c "
import inspect
from barcada_scraper.classifier.pipeline.cost_journal import (
    open_journal, JournalState, JournalAlreadyExistsError, CostJournal,
)
from barcada_scraper.classifier.pipeline.cost_journal_local import LocalFSCostJournal
from barcada_scraper.classifier.pipeline.cost_journal_adls import (
    ADLSCostJournal, BlobNotFoundError, ConditionNotMetError, _abfss_to_https,
)
from barcada_scraper.orchestrator.worker_loop import (
    _open_cost_journal_for_worker, _ensure_journal_initialized, _build_durable_bypass_writer,
)
from barcada_scraper.orchestrator.vmss_worker import WorkerConfig

def _params(fn): return set(inspect.signature(fn).parameters)
assert 'config' in _params(_open_cost_journal_for_worker)
assert {'journal', 'run_id'} <= _params(_ensure_journal_initialized)
assert 'journal' in _params(_build_durable_bypass_writer)
assert {'journal_dir', 'run_id'} <= _params(open_journal)
for m in ('read', 'write_initial', 'try_update', 'exists'):
    assert hasattr(LocalFSCostJournal, m), m
for m in ('read', 'write_initial', 'try_update', 'exists', 'path'):
    assert hasattr(ADLSCostJournal, m), m
sig = inspect.signature(ADLSCostJournal.__init__)
all_kwargs = set(sig.parameters) - {'self'}
assert {'journal_dir', 'run_id'} <= all_kwargs, all_kwargs
assert {'credential', 'blob_backend'} <= all_kwargs, all_kwargs
assert _abfss_to_https('abfss://c@acct.dfs.core.windows.net/p/file.json') == \\
    'https://acct.blob.core.windows.net/c/p/file.json'
class _FakeBackend:
    def upload(self, *, data, if_none_match=None, if_match=None): return '\"etag-fake\"'
    def download(self): raise BlobNotFoundError('not yet written')
    def exists(self): return False
j = ADLSCostJournal(journal_dir='abfss://c@acct.dfs.core.windows.net/p', run_id='x', blob_backend=_FakeBackend())
assert j.path == 'abfss://c@acct.dfs.core.windows.net/p/run_x.json'
assert j.exists() is False
assert j.read() is None
print('OK all S24-shipped + S25-shipped public APIs unchanged')
"

# S26: CRAWLING_POLICY.md doc stability.
test "$(wc -l < docs/CRAWLING_POLICY.md)" = "77" && \
    test "$(wc -c < docs/CRAWLING_POLICY.md)" = "2519" || \
    { echo "HALT: CRAWLING_POLICY.md drifted from S26-landed shape"; exit 1; }
echo "OK docs/CRAWLING_POLICY.md unchanged from S26 close (77 lines / 2519 bytes)"

# S27 + S28: per-tier wiring invariant smoke (all 8 slots populate).
.venv/bin/python -c "
import math, tempfile
from pathlib import Path
from tests.runners.fixture_cascade.cascade import _journal_record_with_breakdown
from barcada_scraper.classifier.pipeline import cost_journal as cj
with tempfile.TemporaryDirectory() as td:
    journal = cj.open_journal(journal_dir=Path(td), run_id='phase0-smoke')
    journal.write_initial(cj.JournalState.fresh(run_id='phase0-smoke', ceiling_usd=10.0))
    _journal_record_with_breakdown(journal=journal, shard_id='s1', stage=1, started_at='2026-05-31T00:00:00+00:00', domains_processed=10, components={'llm': 0.04, 'embedding': 0.01}, unattributed_cost_usd=0.0)
    _journal_record_with_breakdown(journal=journal, shard_id='s2', stage=2, started_at='2026-05-31T00:01:00+00:00', domains_processed=10, components={'fetch': 0.10, 'summarization': 0.20, 'classification': 0.30}, unattributed_cost_usd=0.0)
    _journal_record_with_breakdown(journal=journal, shard_id='s3', stage=3, started_at='2026-05-31T00:02:00+00:00', domains_processed=10, components={'evidence': 0.05, 'primary': 0.07, 'secondary': 0.0}, unattributed_cost_usd=0.03)
    state = journal.read().state
    per_tier_sum = sum(getattr(state.totals, fname) for fname in cj._TOTALS_FIELDS.values())
    shard_sum = sum(s.cost_usd for s in state.shards)
    assert state.totals.stage1_llm_usd == 0.04
    assert state.totals.stage1_embedding_usd == 0.01
    assert math.isclose(state.totals.cost_usd, per_tier_sum + shard_sum, abs_tol=1e-9)
print('OK S27+S28 per-tier wiring invariant holds (all 8 slots populate)')
"

# S28: ShardResult split field presence.
.venv/bin/python -c "
from barcada_scraper.classifier.stage1.run import ShardResult
fields = set(ShardResult.__dataclass_fields__.keys())
assert 'llm_cost_usd' in fields and 'embedding_cost_usd' in fields and 'cost_usd' in fields
assert len(fields) == 14, f'{len(fields)}: {fields}'
print('OK S28 ShardResult 14 fields present')
"

# S28: cascade.py Stage 1 invoker AST structure. Save to a file
# and run via .venv/bin/python (the safety hook blocks the inline
# `python -c` form when the source string contains 'ast.parse').
# (See S31 prompt Step 0.9 for the /tmp/check_s28_ast_phase0.py
# script body — reuse it verbatim.)

# S29: K-b smoke script existence + import-loads cleanly.
.venv/bin/python -c "
import importlib.util
from pathlib import Path
path = Path('scripts/smoke_test_adls_cost_journal.py')
assert path.exists(), f'S29 K-b script missing: {path}'
spec = importlib.util.spec_from_file_location('s29_smoke', str(path))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
assert hasattr(m, 'main') and hasattr(m, '_build_credential') and hasattr(m, '_delete_blob')
print('OK S29 K-b script intact (import OK; public surface intact)')
"

# S31 NEW: the 5 cassette dirs exist with cassette.yaml + sidecar.
.venv/bin/python -c "
from pathlib import Path
root = Path('tests/fixtures/synthetic_crawls')
new = ('patagonia.com', 'deere.com', 'ford.com', 'pfizer.com', 'wholefoodsmarket.com')
for d in new:
    assert (root / d / 'cassette.yaml').exists(), f'missing cassette: {d}'
    assert (root / d / 'extract_hard_exclusions.json').exists(), f'missing sidecar: {d}'
print('OK S31 +5 cassette dirs present (patagonia/deere/ford/pfizer/wholefoodsmarket)')
"

# (S31 produced one fixture-only repo commit — no new src/ behavior
# to invariant-check beyond the cassette-dir presence above. The
# S31 disposition is captured in workspace docs as documentary
# record, NOT as a Phase 0 load-bearing dependency.)
```

If any of 0.1-0.9 fail, HALT before doing any work.

---

## Required workspace reading (Session 32 first 10 minutes)

In this order:

1. **`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`** — full
   handoff state at S31 close. Lists scope candidates
   (A/D/E-continuation/K-a) with prerequisites + estimated scope.
   **Candidate E is at 25; the +5-to-30 continuation is the
   freshest carry-forward.**

2. **`~/crawler-audit/SESSION_LOG.md`** Session 31 entry — what
   landed during Candidate E (1 artifact-only commit `06d67c4`).
   Documents the per-cassette verification, curation rejects, the
   FP-curation all-empty result, the `-k 'canary'` quirk, and the
   LESSONS-folded subsection.

3. **`~/crawler-audit/LESSONS.md`** — the 3 `(S31 folding)`
   sections (locate via `grep -n '^## .*(S31 folding)' LESSONS.md`):
   - "Live-HTTP corpus curation: record broad, curate by content"
   - "Recorder writes-before-validates produces a reject-cleanup tax"
   - "Recording yield on business-interesting public homepages is
     ~40%" — **MANDATORY READ before Phase 1 if Candidate E
     continuation is being considered** (drives candidate-pool
     sizing ~2.5×N + the nonprofit/media rebalance).

4. **`~/crawler-audit/BARCADA_CRAWLER_REMEDIATION_PLAN.md`** §4 W7
   — chosen-scope section. Plan is READ-ONLY.

5. **`tools/synthetic_crawl/recorder.py` + `cli.py`** — only if
   Candidate E continuation is chosen (record/replay mechanics;
   single `--domain` per invocation; robots gate; sidecar writer;
   note the writes-before-validates behavior per S31 LESSONS).

6. **`~/crawler-audit/CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8
   — only if Candidate A (barcada-drift) is chosen.

7. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   + **`scripts/smoke_test_adls_cost_journal.py`** — only if
   Candidate K-a touches the ADLS surface. READ-ONLY for K-a.

---

## Phase 1 — Scope resolution (no code; pre-design-gate)

Operator picks one candidate. Candidates ordered by prerequisite-
readiness; each is independent.

### Candidate A — `barcada-drift` (depends on AI/ML alignment + ≥2 parquets)

Per `CLASSIFICATION_ADJACENT_PLAN.md` §Item 8. Estimated ~300 LOC
logic + ~70-100 LOC overhead floor ≈ **~370-400 LOC delivered**.

**Prerequisites:**
- 2+ `canary_runs/*.parquet` files on operator's machine.
- AI/ML team responses on 4 §Item 8 decisions OR explicit
  operator-side placeholder choices with "AI/ML-to-tune" notes.

**HALT IF** the 4 AI/ML decisions are not pre-resolved AND
operator has not authorized explicit placeholder choices.

**Empirical prereq audit at S31 close** (carry-forward to S32
open): 0 parquets on disk; no `barcada`/`canary` plist in
`~/Library/LaunchAgents/`; no AI/ML responses in workspace.

Re-run these empirical checks at S32 Phase 1 BEFORE issuing the
candidate-choice AskUserQuestion (per S29 LESSONS pattern). If
the empirical state is unchanged, Candidate A remains blocked.

### Candidate D — Phase 4 PR-D operator-led labeling (operator territory)

Per plan §11 Risk Register. Stage 2 + Stage 3 labeling gates
PR-D/E/F/G. Operator-led; Claude Code's role limited to tooling.
W0-side unblocked at S27; still gated on operator-led labeling.

**Prerequisites:** Operator-scheduled labeling effort; Claude
Code's role limited to tooling around the labeling workflow.

### Candidate E — Cassette corpus expansion (CONTINUATION 25 → 30)

S31 grew the corpus 20 → 25; plan §4 W7 cites "~20-30
representative domains" — current 25 leaves room for **+5** to
hit the upper bound.

**Prerequisites:**
- Decision on the +5 target count (30) vs a smaller bump.
- Per S31-folded LESSONS, budget a candidate pool of **~2.5×N**
  domains (so ~12-13 candidates for +5) when WAF risk is not
  pre-filtered, and **rebalance toward nonprofit / media /
  education** to offset S31's commerce skew.
- Operator sign-off on the candidate domain list BEFORE recording
  (outward-facing live HTTP to named third parties).

**Recording mechanics (proven at S31):**
`python -m tools.synthetic_crawl record --domain <d>
--cassette-root tests/fixtures/synthetic_crawls --user-agent
"barcada-synthetic-crawl/0.1 (+https://barcada.io)"`. Record
broad; reject 403/WAF (writes a denial-page cassette dir →
`mv`-aside) + ReadTimeout (leaves an empty dir → `mv`-aside);
keep only 200-OK real-content cassettes of the intended category.
Verify each kept cassette: byte-identical replay (SHA stable ×2;
exits 0/0), sidecar shape == the 20-key reference, empty
exclusion reasons. Single bundled artifact commit (S20/S31
precedent). **Fixture-only → net-zero on the 970 test count**;
the count moves only the Phase 0 Step 0.4 fixture-count check
(25 → 30) — pin it for S33.

### Candidate K-a — Azurite-backed integration test (OPTIONAL per S30 LESSONS)

**OPTIONAL** — the S30 K-b operator-smoke empirically closed the
mock-vs-prod divergence risk K-a would have permanently protected
against. Defense-in-depth only; NOT on any critical path.

**Operator should pick K-a only if** a forward-looking reason
applies: `cost_journal_adls.py` will see frequent churn;
production traffic patterns will exercise concurrency/feature
paths the K-b 5-step matrix did not cover; a downstream consumer
mandates a CI safety net.

**Phase 1 carve-out capture (if K-a is picked):** name the
carve-out reason (concurrency / production-feature-coverage /
customer-visible-critical-path) OR record explicit operator-
override ("defense-in-depth without specific carve-out"). Pin the
choice in chat at Phase 1.

**Prerequisites:** Docker available locally; Azurite image
pullable.

**Scope estimate**: ~50-100 LOC logic = **~120-200 LOC delivered**
+ Docker setup.

**Recommended posture if K-a chosen**: pair with Q-K-a.4 =
Option 2 (add a 17th path to the canonical invocation).

### Sub-question 1.TAG — Tag at session close (pinned at Phase 1)

Independent of scope choice; resolved fully here at Phase 1.

- **Candidate A**: defer OR `barcada-drift-v0`.
- **Candidate D**: defer.
- **Candidate E continuation**: defer (S20/S31 cassette commits
  were untagged artifact commits).
- **Candidate K-a**: defer OR `workstream-a-week2-end` if K-a is
  the final W A.2 code milestone (operator decides).

Phase 5 reads this resolution directly — no Phase 2 re-decision.

---

## Phase 2 — Design-gate elicitation (no code; AskUserQuestion)

Per chosen Phase 1 candidate. Source-verify at session-current
HEAD per the `[[verify-before-asking-discipline]]` AND the S22-S31
"Plan-vs-reality at Phase 2 source-verify" + S25 "source-verify
drives option-set design" LESSONS patterns BEFORE each
AskUserQuestion batch.

**HALT IF** any Phase 2 decision would require modifications to
`src/barcada_scraper/` beyond what was Phase-2-authorized OR to
the W4.1.5 driver beyond the S16/S27/S28 exceptions OR to any
S19-S31 deliverable (including re-recording/deleting any of the
25 existing cassettes) — surface as a design-gate sub-question
before patching.

### CRITICAL Phase 2 hygiene (4-option limit; empirical-vs-by-design; LOC additive floor; posture-validation)

Carry forward the S26/S28/S29/S30 hygiene notes verbatim (see S31
prompt Phase 2): count each Q-* option set (≤4 or tier/split);
audit existing test pins for by-design vs empirical; size new
scripts with the ~70-100 LOC additive overhead floor; default new
external-service-backed tests to operator-smoke (K-b) posture, not
permanent CI (K-a).

### If Candidate A (barcada-drift)

Carry-forward from S22-S31 prompts (unchanged):
- Q-A.1 CLI namespace; Q-A.2 drift metric; Q-A.3 alert threshold;
  Q-A.4 input contract; Q-A.5 output shape; Q-A.6 test corpus.
(6 Q-* gates → split into 2-3 sequential AskUserQuestion calls;
both the 4-options-per-question and 4-questions-per-call caps
apply.)

### If Candidate D (Phase 4 PR-D tooling)

- **Q-D.1 Tooling shape**: batch validators / import scripts /
  hygiene tools. Operator-led design.

### If Candidate E (cassette corpus expansion continuation)

- **Q-E.1 Target count**: 30 (plan upper bound, +5) vs a smaller
  bump (e.g. +3 to 28) vs stay at 25.
- **Q-E.2 Subset focus**: nonprofit / media / education
  (Recommended — rebalances S31's commerce skew + lower WAF
  incidence) vs more business-classification-interesting vs
  bot-blocked/WAF vs non-English/international.
- **Q-E.3 FP re-investigation** (still carry-forward): re-record
  archive.org + hashicorp.com under a different UA OR drop them OR
  keep as-is (Recommended — touches NO S20-locked artifact). NB:
  re-record/drop would modify/delete S20-locked cassettes →
  requires explicit authorization (implicit-authorization HALT).
- **Q-E.4 Candidate-pool size**: confirm the ~2.5×N pool (≈12-13
  candidates for +5) per the S31 "~40% yield" LESSONS, OR
  pre-filter for WAF first (adds a `curl -I` HEAD pre-check step).

### If Candidate K-a (Azurite-backed integration test)

(Carve-out captured at Phase 1; Phase 2 designs the test.)
- **Q-K-a.1 Auth posture**: connection-string vs shared-key vs
  DefaultAzureCredential.
- **Q-K-a.2 Test scope**: full 5-step ETag-conflict matrix vs
  single happy-path round-trip.
- **Q-K-a.3 New file vs append**: new
  `tests/classifier/pipeline/test_cost_journal_adls_azurite.py`
  vs append with a `pytest.mark.live` marker.
- **Q-K-a.4 CI integration**: mark `live` + skip-by-default in the
  16-path, OR add a 17th path.
- **Q-K-a.5 Azurite lifecycle**: fixture auto-start vs operator-
  started on a fixed port vs CI-environment-only.

### Shared sub-questions (all candidates)

- **Q-SHARED.1 Commit shape**: per-module / per-sub-surface
  (S18-S31 default; Recommended) vs single bundled artifact commit
  (the S20/S31 default for fixture-only cassette corpus work).

(Tag-at-close resolved at Phase 1 Sub-question 1.TAG.)

---

## Phase 3 — Implementation (per chosen commit shape, strict order)

### Non-interleaving rule (CRITICAL for bisectability)

If the chosen candidate has multiple sub-surfaces, complete each
fully before starting the next. Per S22-S31 precedent. If a
mid-sub-surface dependency emerges, HALT and surface as a
design-gate sub-question.

### Per-commit checkpoint protocol (single source of truth)

At EVERY Phase 3 commit boundary, run these 6 steps IN ORDER:

**1. Combined suite**

```
.venv/bin/python -m pytest \
    <the canonical 16-path invocation from Step 0.5> \
    <new S32 test paths if any> -q
# Candidate E continuation: fixture-only → still 970 (no new test
# paths). Candidate K-a with Q-K-a.4 = Option 2: add
# tests/classifier/pipeline/test_cost_journal_adls_azurite.py and
# recompute headline as 970 + N new Azurite tests.
```

Expected: previous_baseline + N new tests, all passing. If
failing tests are NOT a deliberate consequence of the surface-
under-test → HALT.

**Phase 0 grep-for-same-shape-tests sanity** (S25 LESSONS): before
Phase 3, grep the test tree for same-shape tests that pin
contracts the chosen scope will modify. If found and not in the
prompt's explicit replacement allowlist, surface at Phase 0/2.

**2. Ruff sanity (touched files only) + mid-implementation format check**

```
.venv/bin/ruff check <touched paths>
.venv/bin/ruff format --check <touched paths>
```
(Candidate E continuation touches only fixtures → no `.py` → ruff
N/A; confirm `git status` shows no `.py` touched.)

**3. Verification table (build in chat per `[[double-check-before-commit]]`)**

Build a claim → reality → status table for every concrete claim in
the draft commit message. Any ✗ → fix the claim BEFORE staging.
Distinguish net-new tests from newly-in-invocation pre-existing
tests (S23 LESSONS). For exit-code claims use
`cmd > /tmp/out 2> /tmp/err; echo "Exit: $?"`. For new-file LOC
claims use `wc -l` (S29 LESSONS). For cassette work, verify the
per-cassette gate (replay SHA stable; sidecar shape; empty
exclusion reasons) and the new fixture counts.

**4. `git status` check**

Only intended files staged; no surprise `eval_data/` or
unauthorized `src/` changes. Operator-side `eval_data/`
modifications stay unstaged. **For Candidate E continuation:
verify any reject dirs were moved aside (not left untracked in
the tree) so the fixture-count is exactly the intended new total.**

**5. "Confirm to commit?" presented to operator**

Include: verification table; commit message file location
(`/tmp/<id>-msg.txt`); file list to stage (M / A / D).

**6. After operator confirms**

Stage + commit + verify the new SHA (`git log --oneline -1`) +
verify combined suite still passes on the new HEAD.

### Cumulative test-count gate

Track combined-suite passing count at each commit boundary. The
count NEVER decreases between checkpoints. Authorized decreases
ONLY for a Q-*-authorized same-shape 1↔1 replacement (cite the
authorization + name replaced + replacement in the commit body).
Baseline bound at Phase 1: **970** (or the chosen narrower / K-a
17-path). Hold it consistent across all Phase 3 commits.

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
edits to `eval_data/*` can fail the gate even though no S32 commit
touches eval_data. When this fires:
1. Confirm the failing row is operator-WIP (`git diff eval_data/`),
   not committed HEAD (`git show HEAD:eval_data/...`).
2. Confirm the S32 commits do not touch eval_data
   (`git diff origin/main..HEAD -- eval_data/`).
3. Surface to operator with the exact row + reason + diff.
4. Two paths: (a) operator-fix in WT, re-run gate; (b) stash
   eval_data WIP, push, restore.
5. Do NOT auto-fix locked-artifact content.

S20+S22 precedent: operator chose (a). S21/S23-S31 did not need
this protocol at push (S28 saw a transient "1 error" that cleared
on identical re-run; S29-S31 did NOT reproduce it).

---

## Phase 5 — Push + tag

- Push to `origin/main` after operator confirms.
- Tag per Phase 1 Sub-question 1.TAG decision (or defer).

If a workstream-end tag is placed: include an annotated message
naming every sub-surface commit + mapping to plan bullets + listing
deferrals (mirror `workstream-a-week1-end` / `workstream-0-end`).

Note: workstream-0-end placed at S27. W A.1 closed at S22's
`workstream-a-week1-end`; W A.2 is the orchestrator-side robots
work landed across S23+S24+S25 plus the K-b script at S29 plus the
K-b execution at S30. If Candidate K-a ships at S32 AND operator
considers it the final W A.2 code milestone, a
`workstream-a-week2-end` annotated tag would be appropriate.

---

## Phase 6 — Workspace close-out

- Append Session 32 entry to `~/crawler-audit/SESSION_LOG.md`
  including a **Canonical S32-close baseline** block with the
  exact pytest invocation + verified count (per S22-S31 LESSONS).
  **If Candidate E continued, record the new fixture-count
  (cassettes/exclusions 25 → 30) as the S33 Phase 0 Step 0.4
  forward note with the exact variable names
  `cassette_count == N` / `exclusions_count == N`.**
- Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md` for
  Session 33 — explicitly pin the S33 Phase 0 workspace anchor SHA
  per the S21-S31 post-audit pattern. After the close-out commit
  lands, expect **1-2 follow-up commits** pinning the actual SHA.
- Update `~/crawler-audit/LESSONS.md` with any new forward-
  applicable patterns.
- Workspace close-out: 1 primary commit + 1-2 follow-up commits.
  Push workspace after operator confirms.

Note: drafting the next-session prompt (`SESSION_33_PROMPT.md`) is
NOT a built-in Phase 6 step. Per S20→S31 precedent, prompt-drafting
is operator-commissioned between sessions. If the operator asks for
it explicitly at S32 close, draft it as a separate follow-up.

---

## Acceptance criteria

**Per candidate (reduces if Phase 1 narrows scope):**

### Candidate A (barcada-drift)
1. `barcada-drift` CLI works against ≥2 canary_runs parquets.
2. Drift metric per Q-A.2 implemented + tested.
3. Alert threshold per Q-A.3 implemented + tested.
4. Output shape per Q-A.5 documented + tested.

### Candidate D (Phase 4 PR-D tooling)
1. Tooling shape per Q-D.1.

### Candidate E (cassette corpus expansion continuation)
1. Cassette count grows to Q-E.1 target (≤30).
2. Each new cassette: robots-gate passed; 200-OK real content;
   byte-identical replay; sidecar shape valid; exclusion reasons
   inspected.
3. FP re-investigation per Q-E.3 if applicable (else keep-as-is).
4. S33 Phase 0 Step 0.4 fixture-count forward note pinned with
   exact variable names.

### Candidate K-a (Azurite-backed integration test)
0. Phase 1 carve-out justification recorded in chat.
1. Azurite-backed test passes locally + (if Q-K-a.4 includes CI)
   in CI.
2. If Q-K-a.4 = Option 2, the new path is added to the canonical
   invocation and the Canonical S32-close baseline reflects the
   new headline.

### Shared (all candidates additionally satisfy)
- **S1.** Combined suite at session close: 970 baseline + N new
  tests, all passing (or the chosen narrower / K-a 17-path).
- **S2.** Pre-push gate green (incl. eval_data WIP halt protocol).
- **S3.** Tag placed per 1.TAG OR explicit defer.
- **S4.** Regression-protection checklist held (see Out-of-scope).
  In particular: ALL S21-S31 deliverables stay at their SHAs;
  their public APIs unchanged; the 5 S31 cassettes stay at
  `06d67c4`; per-sub-suite counts stay green; CRAWLING_POLICY.md
  77 lines / 2519 bytes; the combined total stays at 970 (or
  grows) unless a Q-* authorizes a same-shape 1↔1 replacement.

---

## Out-of-scope (no exceptions without operator authorization)

Per the regression-protection checklist. **S31 added one new lock**
(the 5 cassette dirs at `06d67c4`); otherwise unchanged from S31
prompt.

**S19 deliverables:** `tools/baseline_v0/check.py`;
`tests/baseline_v0/test_check.py` (24 tests); 6 check-dispatch
tests in `tests/baseline_v0/test_cli.py`.

**S20 deliverables:** `tools/synthetic_crawl/` package (4 files);
`tools/baseline_v0/canary.py`; `canary-run` subparser;
`tests/synthetic_crawl/` (33 tests); `tests/baseline_v0/test_canary.py`
(17 tests); 6 canary-dispatch tests; the original 20 cassettes +
20 sidecars at `7f11879`; `scripts/launchd/` (5 files);
`pyproject.toml` vcrpy>=8.1 dev entry; `.gitignore` canary_runs/.

**S21 deliverables:** `src/barcada_scraper/scraper/robots.py`
(282 LOC; `34a59b6`); `tests/scraper/test_robots.py` (32 tests).

**S22 deliverables:** `scraper/robots_gate.py` (`ba87e7e`);
`tests/scraper/test_robots_gate.py` (30); `scraper/robots_bypass_config.py`
(`381ee89`); `tests/scraper/test_robots_bypass_config.py` (30);
the S22 `cost_journal.py` additions at `1d9404e`; the S22
`test_cost_journal.py` additions (14 new + 1 updated), EXCEPT the
S25 Q-J.8-extension replacement at `835a531`.

**S23 deliverables:** `orchestrator/robots_integration.py`
(`279bb77`); `tests/orchestrator/test_robots_integration.py` (35);
all other S23 additions per S31 prompt.

**S24 deliverables:** the 3 worker_loop private helpers at
`48c324a`; the 5 retargeted test_stage2_pages_invoker_* fixtures;
`tests/orchestrator/test_worker_loop_persistence.py` at `aed7873`
(12); the 3 S24-added tests in test_robots_gate_integration.py.

**S25 deliverables:** `classifier/pipeline/cost_journal_adls.py`
at `835a531` (295 LOC; EMPIRICALLY validated at S30);
`tests/classifier/pipeline/test_cost_journal_adls.py` at `835a531`
(19 tests + DummyBlobBackend); all other S25 deliverables.

**S26 deliverables:** `docs/CRAWLING_POLICY.md` at `2314f5e`
(77 lines / 2519 bytes).

**S27 deliverables:** `cascade.py` per-tier wiring at `a1c5636`
(extended S28); `test_cost_journal_wiring.py` at `a1c5636`
(modified S28).

**S28 deliverables:** `classifier/stage1/run.py` at `776d203`
(ShardResult +2 fields); `test_run_cascade.py` at `776d203`
(+1 test); `cascade.py` Stage 1 invoker switch at `9afde57`;
`test_cost_journal_wiring.py` 1↔1 replacement at `ae9e627`.

**S29 deliverables:** `scripts/smoke_test_adls_cost_journal.py` at
`75a3937` (220 LOC).

**S30 deliverables:** No repo code changes (K-b-exec execution
only); workspace docs at `9d4691e` + `67a9c40`.

**S31 deliverables (NEW LOCK):**
- `tests/fixtures/synthetic_crawls/{patagonia,deere,ford,pfizer,wholefoodsmarket}.com/`
  at `06d67c4` — WA0.W7.cassettes-corpus-expansion: 10 fixture
  files across 5 domain dirs (5 cassette.yaml + 5
  extract_hard_exclusions.json; 2.18 MB). Do NOT re-record or
  delete without Phase 2 authorization. A Candidate E continuation
  may ADD new dirs but MUST NOT touch these 5 (or the original 20).

**W4.1.5 driver orchestration:** `tests/runners/fixture_cascade/`
(except via W5.X-prefix commit — only S16/S27/S28 opened it; all
closed).

**Baseline-v0 ground truth:** the committed
`tests/fixtures/baseline-v0/` snapshot at `9e9a1fb` (1213 files).

**Existing W6 sub-surface (Session 18):**
`tools/baseline_v0/generate.py`, `determinism.py`, the existing
`generate` subparser.

**Schemas + plans (locked):** `expected.schema.json` v1.1;
`META_SCHEMA.md` v1.1; `meta.schema.json` v1.0; `stage1.schema.json`
v1.0; all 13 workstream tags at their placed SHAs;
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` (READ-ONLY);
`CLASSIFICATION_ADJACENT_PLAN.md` (UPDATED only when AI/ML
decisions land); `RECONCILIATION_2026-05-21.md`;
`docs/phase4_implementation_plan.md`.

**Operator-owned territory:** all of `eval_data/` — per-row WIP
edits across sessions expected and unstaged (Sessions 8-31
precedent); inter-session operator-side eval_data COMMITS tolerated
per "Workspace HEAD delta tolerance" (verify eval_data-only via
`git show --stat`). 2 operator-side stage1 TAGS
(`workstream-stage1-prestaged-flags-end`,
`workstream-stage1-step3-end`) point at eval_data-only commits.

**Production code:** `src/barcada_scraper/` — locked unless Phase 2
authorizes a specific module. S21-S25+S28 authorized (full list in
S31 prompt). S26+S27+S29+S30+**S31** added no new src/
authorizations.

**Pipeline configs:** `configs/`.

**Phase 4 work:** PR-D/E/F/G W0-side unblocked since S27; still
gated on operator-led Stage 2/3 labeling.

---

## Verify-before-asking discipline (strict rule from S19-S31)

Per `[[double-check-before-commit]]`: **ALWAYS verify every
concrete claim in the commit message against actual source/output
BEFORE staging.** Fixture names, file counts, exit codes, line
counts, test counts, helper names, smoke outcomes, SHA prefixes,
regex matches, API signatures, cassette replay SHAs, sidecar
shapes. No claims by pattern-completion. Build a verification
table (claim → reality → status) and reconcile before "Confirm to
commit?".

Specific to S32:
- Candidate E: each new cassette records 200-OK real content,
  robots-gate-passes, replays byte-identically, sidecar
  shape-valid, exclusion reasons inspected; the new fixture-count
  is exactly the intended total (no stray reject dirs left).
- Before claiming combined suite count, re-run pytest.
- Before claiming ruff/format clean, re-run ruff against touched
  files (N/A for fixture-only commits — confirm no `.py` touched).
- Before claiming a SHA prefix, verify via
  `git show --no-patch --format=%h <ref>`.
- Before claiming a new-file LOC count, run `wc -l`.

Avoid bash pipe artifacts that mask Python exit codes:
`python_cmd 2>&1 | grep ... | tail` makes `$?` reflect tail's
exit. Use `> stdout.out 2> stderr.err; echo $?` or
`${PIPESTATUS[0]}`.

LESSONS-folded discoveries from S22-S31 worth re-applying:
- Plan-vs-reality at Phase 2 (S22).
- Phase 2 source-verify drives option-set design (S25; S28/S29/S31).
- Implicit-authorization HALT (S22-S31).
- Q-J.8 explicit allowlist may be incomplete; HALT-and-extend (S25).
- Local imports defeat module-attribute monkeypatch (S25).
- Tightened-precondition test-fixture retargeting (S24).
- Test against public API surface only (S24; S29/S30 extensions).
- Source-verify line numbers per Phase 3 commit (S23).
- AskUserQuestion 4-option limit can silently truncate (S26).
- Deferred wiring gaps fold cleanly if a parallel-API seam exists (S27).
- Empirical-vs-by-design distinction in test pins (S28).
- Phase 0 fixture-count commands need `2>/dev/null` + bounded
  timeout — use the Python rglob() pattern (S28 post-close).
- Operator-driven script LOC: ~70-100 LOC additive overhead floor,
  not a linear multiplier (S29).
- Public-API-only cleanup pattern extends to operator scripts (S29).
- Empirical Phase 1 prerequisite check before scope-narrow (S29;
  S30/S31 re-validated — Candidate A unchanged).
- Operator-smoke posture (K-b) closes mock-vs-prod divergence in
  one execution; permanent CI (K-a) is then optional (S30).
- **Live-HTTP corpus curation: record broad, curate by content —
  never pre-trust a domain list (S31)**: WAF-403 + ReadTimeout +
  off-scope rejects only surface at record time; get operator
  sign-off on the candidate set, record broad, keep only 200-OK
  real-content cassettes, verify replay/sidecar/exclusions before
  commit; `mv`-aside rejects (`rm`/`rmtree` blocked by the env
  hook) so the next Phase 0 fixture-count is clean.
- **Recorder writes-before-validates produces a reject-cleanup tax
  (S31)**: `record()` writes the cassette dir BEFORE validating
  usefulness — WAF-403 writes a full denial-page dir; ReadTimeout
  leaves an empty dir. A reject-before-write design would close
  both (recorder-hygiene observation; no code fix unless a session
  scopes `tools/synthetic_crawl/` tooling).
- **Recording yield on business-interesting public homepages is
  ~40% (S31)**: budget a ~2.5×N candidate pool for +N cassettes
  when WAF risk is not pre-filtered; rebalance toward nonprofit /
  media / education to offset commerce skew.
- **Carry-forward non-reproduction (S31 observation)**: the 3
  S30-carry-forward observations (execution-only session shape;
  test-collection invariance under operator commits; in-class
  eval_data tag tolerance) did NOT reproduce at S31 and remain
  carry-forward unless S32 reproduces them.

---

## Commit hygiene (per LESSONS + S19-S31 additions)

- File-based commit messages at `/tmp/<id>-msg.txt`.
- Commit shape per Q-SHARED.1 (per-module default; single bundled
  artifact commit for fixture-only cassette corpus work, S20/S31
  precedent).
- "Confirm to commit?" before EVERY commit. Pair with verification
  table (always) and `git diff --staged` (per triggers).
- Commit body includes: action ref (S31 used
  `WA0.W7.cassettes-corpus-expansion`; S32 chooses its own per
  candidate), scope summary, file touches, test count delta (with
  net-new vs newly-in-invocation distinction per S23 LESSONS),
  plan reference. NO `Co-Authored-By`.
- Pre-push gate must run green. Never use `--no-verify`.
- Pre-push vermin: `git ls-files '*.py' | xargs vermin
  --target=3.10` to filter venv-internal pytest 3.14 false-
  positives.
- Mid-implementation ruff format-check, not only pre-push.
- For S19-S31-test/fixture modifications: explicit Phase 2
  authorization required; document the modification scope in the
  commit body (Implicit-authorization HALT pattern).
- Workspace close-out (Phase 6) lands as its own commit, followed
  by 1-2 follow-up commits pinning the anchor SHA for S33.

---

## Context-window awareness

S31 ran Phase 0 → Phase 6 in a single context window with 1
artifact-only commit (5 live-HTTP recordings + curation + close-
out), comfortably within budget. S32 budget per scope:

- Candidate A: medium (~370-400 LOC delivered).
- Candidate D: small.
- Candidate E continuation: small-to-medium (live-HTTP latency for
  a ~12-13 candidate pool to net +5; expect a reject rate per the
  ~40% yield LESSONS).
- Candidate K-a: medium (~120-200 LOC delivered + Docker setup;
  OPTIONAL).

Strategies:
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For live-HTTP corpus work, RECORD BROAD then CURATE BY CONTENT;
  `mv`-aside rejects; verify replay/sidecar/exclusions before
  commit.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before the chosen S32 scope closes, finish
  the in-flight sub-surface, then close session and refill the
  transition template for Session 33.

---

## Reporting in chat at session close

After all Session 32 commits land + push + close-out per the
S13-31 pattern:

1. Commit SHA(s) of each S32 sub-surface.
2. Sub-surface(s) landed (per candidate).
3. Test count delta: 970 (or narrower / 17-path) baseline → S32
   close.
4. Driver suite count at S32 close (52/52 expected).
5. Files touched per sub-surface.
6. Tag dispositions (incl. any new tag per 1.TAG).
7. Per-tier cost-accounting wiring: CLOSED end-to-end since S28.
8. ADLSCostJournal status: K-b SHIP closed S29; K-b EXEC closed
   S30; K-a status per S32 scope choice.
9. Any spend (LLM, infrastructure, cassette-capture).
10. Robots.txt compliance log (if Candidate E continued).
11. FP-curation log update (if Candidate E continued).
12. Verify-before-asking summary: source-verification findings.
13. Outstanding items for Session 33 (incl. the new cassette
    fixture-count if Candidate E continued; whether E is then
    exhausted at 30).
14. Tags state at S32 close.

Do not propose Phase 4 PR-D/E/F/G work unless Candidate D was
chosen and operator-led labeling is in flight.

---

## Carry-forward bakes (no amendment file needed)

All S31 close-out commits (`e1e7ade` primary + `8c80c26` anchor-pin
+ the post-close LESSONS-fold commit) plus the S31 disposition have
been folded directly into this prompt — S32 does not need a
separate amendment file:

- **S31 close-out anchors** folded into Step 0.1 (workspace anchor
  = the S32 prompt-drafting commit succeeding the post-close
  LESSONS-fold; repo anchor `06d67c4` with operator-eval_data-
  commit tolerance), Step 0.2 (13 tags, unchanged), Step 0.4
  (cassettes/exclusions 20 → **25**), Step 0.5 (canonical 970),
  Step 0.9 (added the S31 +5 cassette-dir presence check).
- **2 NEW LESSONS sections from S31 post-close** ("Recorder
  writes-before-validates"; "Recording yield ~40%") referenced at
  Phase 1 Candidate E + Phase 2 Q-E.2/Q-E.4 + the Verify-before-
  asking LESSONS list. (Plus the close-out "Live-HTTP corpus
  curation" section.)
- **Candidate E continuation** room (25 → 30) folded into the
  carry-forward list + Phase 1 + Phase 2 Q-E.* with the
  nonprofit/media rebalance guidance.
- **S31 cassette lock** folded into Out-of-scope's S31 deliverables.

If new amendments arise pre-S32 open, walk them per the reviewer-
feedback hygiene pattern in this prompt's "Reviewer-feedback
hygiene" section.
