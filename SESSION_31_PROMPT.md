# Session 31 prompt — scope picked at Phase 1
# (S30 closed Candidate K-b-exec; S31 chooses from carry-forwards
#  A/D/E/K-a — no new carry-forward introduced by S30)

**Drafted at Session 30 close (2026-05-26).** Mirrors the
S20/S21/.../S29/S30 prompt structure. Scope-agnostic at Phases
0/1; scope-specific design gates at Phase 2 per chosen candidate.
Strict 7-phase ordering with halt-on-mismatch preserved.

This prompt should be invoked from `~/crawler-audit/SESSION_31_PROMPT.md`
or operator-mirrored to `~/Downloads/session-31-prompt.md`. Re-read
it on session open.

---

## Scope

Engineering session. Workstream sub-surfaces available after
Session 30 closed Candidate K-b-exec (0 code commits + 2 workspace
close-out commits). Repo HEAD at `af6f1d4` (UNCHANGED from S30
open; S30 had zero code commits — the K-b-exec scope was
operator-driven script execution + trace interpretation only).
Workspace HEAD at `67a9c40`. **Workstream 0 fully closed at
S27 via the `workstream-0-end` tag at `a1c5636`**.

Carry-forward candidates entering S31 (K-b-exec fully closed S30):

- **barcada-drift (Candidate A)** — deferred per Q1.1=(A) at S20;
  still needs 4 AI/ML decisions per CLASSIFICATION_ADJACENT_PLAN.md
  §Item 8 AND 2+ `canary_runs/*.parquet` files. **S30 re-confirmed
  empirically** that the launchd installer has NOT been run as of
  S30 close (no plist in `~/Library/LaunchAgents/`; 0 parquets on
  disk). Same state as S29 close.

- **Phase 4 PR-D tooling (Candidate D)** — operator-led labeling
  territory. W0-side unblocked since S27 (`workstream-0-end`
  placed); still gated on operator-led Stage 2/3 labeling. **S30
  observation**: operator placed 2 new operator-side eval_data
  tags (`workstream-stage1-prestaged-flags-end` → `af6f1d4`;
  `workstream-stage1-step3-end` → `d4f06b8`) between S29 close
  and S30 open, suggesting labeling workflow activity. This does
  not unblock PR-D itself but signals movement.

- **Cassette corpus expansion (Candidate E)** — current 20 is
  lower bound of plan's "~20-30". Unchanged from S29/S30 handoffs.

- **ADLSCostJournal Azurite-backed CI test (Candidate K-a)** —
  **DOWNGRADED TO OPTIONAL at S30** per the new S30-folded LESSONS
  posture-validation note. The K-b operator-smoke (executed S30,
  trace clean) empirically closed the mock-vs-prod divergence
  risk that K-a would have permanently protected against. K-a now
  serves only as defense-in-depth; it is NOT on any critical
  path. Operator may still choose it if a permanent CI safety
  net is desired for `cost_journal_adls.py` churn, but the
  S30 LESSONS fold explicitly downgrades the urgency.

**No new carry-forward introduced by S30.** The K-b-exec script
ran clean end-to-end against a live Azure container on its first
execution; ADLSCostJournal behavior matches `DummyBlobBackend`
in all 5 ETag-conflict-matrix steps.

Operator chooses at Phase 1 which candidate Session 31 ships.
Each candidate has its own Phase 2 design-gate template.

**Sessions 13-30 precedent:** this session does NOT modify the
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
at `75a3937`). **S30 produced zero repo code changes** — there
is no S30 lock to add.

Does NOT modify production code under `src/barcada_scraper/`
UNLESS Phase 2 design-gate explicitly authorizes a specific
module. None of the S31 candidates (A/D/E/K-a) currently
anticipate new src/ authorizations beyond what's already
authorized for their respective surfaces. (Candidate K-a will
likely consume `ADLSCostJournal` without modifying it, mirroring
S29 K-b's posture.)

Full regression-protection checklist in **Out-of-scope** at the
end of this prompt. Re-read it before any code lands.

---

## Reviewer-feedback hygiene (if this prompt is reviewed)

If an external reviewer (operator-invoked) flags items in this
prompt before Session 31 starts, walk each flagged item against
on-disk reality at workspace HEAD `67a9c40` and repo HEAD
`af6f1d4` (or whatever HEAD the operator's machine carries),
BEFORE applying any change. Per S19-S30 pattern (LESSONS
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
halts catch hidden scope expansion (per S22-S30 "Implicit-
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
# Workspace at Session 31 start. S30 close-out landed across 2
# workspace commits: 9d4691e (primary close-out: SESSION_LOG.md +
# SESSION_TRANSITION_TEMPLATE.md + LESSONS.md) + 67a9c40
# (anchor-pinning follow-up). This prompt drafted as a follow-up
# commit succeeding 67a9c40.
git -C ~/crawler-audit rev-parse HEAD
# Expect: the S31 prompt-drafting commit (succeeds 67a9c40 S30
# anchor-pin follow-up, which itself succeeds 9d4691e S30 primary
# close-out). OR a later commit if additional workspace doc edits
# (incl. an anchor-pin follow-up of THIS commit, or further
# prompt revisions) landed post-draft. If N commits ahead, verify
# each prior commit's subject via `git log --oneline 67a9c40..HEAD`
# against expected prompt-finalization / doc-edit patterns;
# surface the SHA delta and request authorization to proceed if
# anything is unexpected.
# (S20-S30 precedent: operator authorized continuation when 1-3
# extra workspace commits were the strengthened prompts
# themselves.)

# Repo at Session 30 final state:
git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: af6f1d4 (stage1 audit: A3 pre-staged flags +
# appointment_booking refinement) — UNCHANGED from S30 close
# because S30 produced zero repo code commits.
#
# Tolerated delta: operator-side eval_data labeling commits between
# S30 close and S31 open are expected (Sessions 8-30 precedent).
# Per the S22-folded "Workspace HEAD delta tolerance" LESSONS
# pattern: tolerate N additional commits as long as EACH commit's
# stat is strictly within eval_data/* (no src/barcada_scraper/*
# touches, no tests/* touches, no scripts/* touches, no docs/*
# touches). Verify via `git show --stat <sha>` for every commit in
# af6f1d4..HEAD; surface any non-eval_data delta for operator
# authorization before continuing.
```

### Step 0.2 — Tags (S30 baseline includes 2 new operator-side stage1 tags)

```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort
# Expect 13 tags as of S30 close (was 11 at S29; the 2 new
# operator-side stage1 tags landed between S29 close and S30
# open; both eval_data-only):
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
#   workstream-stage1-prestaged-flags-end       (NEW S29→S30; -> af6f1d4)
#   workstream-stage1-step3-end                 (NEW S29→S30; -> d4f06b8)

git -C /Users/administrator/projects/barcada-scraper rev-list -n 1 workstream-0-end
# Expect: a1c5636… (matches the S27 placement; UNCHANGED).

# Tolerated delta: additional operator-side stage1-* / eval_data-*
# tags may land between S30 close and S31 open per the operator's
# labeling workflow cadence. For each new tag in `git tag -l`
# beyond the 13 expected, verify the tagged commit is eval_data-
# only via `git show --stat <tag>`; if so, treat as operator-
# domain marker (S30 precedent). If a new tag points at any
# src/barcada_scraper/* / tests/* / scripts/* / docs/* commit,
# HALT for operator authorization.
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
# S29 + S30 did NOT touch this surface.
```

### Step 0.4 — Fixture counts (use Python pattern per S28 LESSONS hygiene fold)

**IMPORTANT**: per S28-folded LESSONS "Phase 0 fixture-count
commands need `2>/dev/null` + a bounded timeout", do NOT use bare
`find` invocations here. They hung indefinitely in S28; S30 also
exercised this discipline at close-out (see SESSION_LOG.md S30
"Post-close-out workspace hygiene" subsection for the load-bearing
record of hung-process cleanup). Use the Python pattern below —
returned all 6 counts in <2s in prior sessions when the
equivalent `find` commands had been hung 15+ hours.

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

### Step 0.5 — Test-suite baseline (S31 canonical)

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
# Sub-totals (16 paths; ALL identical to S27/S28/S29/S30 close —
# S30 was K-b-exec EXECUTION only, no repo code changes):
#   210 conformance + 52 driver + 99 baseline_v0 +
#    33 synthetic_crawl + 32 robots + 30 robots_gate +
#    30 robots_bypass_config + 43 cost_journal +
#    13 cost_journal_local + 19 cost_journal_adls +
#    35 robots_integration + 74 vmss_worker +
#   129 job_runner + 152 worker_loop +
#     7 robots_gate_integration (4 S23 + 2 S24-unchanged + 1 S25-replaced) +
#    12 worker_loop_persistence (11 S24-unchanged + 1 S25-replaced) = 970
#
# Pinned in SESSION_LOG.md "Canonical S30-close baseline" block.
# The 970 count is invariant under operator-side eval_data
# commits between S30 and S31 (eval_data is not in the invocation).
```

The sub-paths add up to the headline: 210 + 52 + 99 + 33 + 32 + 30
+ 30 + 43 + 13 + 19 + 35 + 74 + 129 + 152 + 7 + 12 = 970. Any drift
= halt.

If the headline mismatches, re-run each sub-path independently to
localize which sub-suite drifted (see S30 prompt Step 0.5 for the
14-line per-path invocation block).

**Narrower baselines** (valid for S31 candidates that don't
exercise the ADLS or robots-gate-integration test paths):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 944 (S27/S28/S29/S30-equivalent narrower; canonical 16-path
  minus 19 cost_journal_adls minus 7 robots_gate_integration).

If Candidate K-a is chosen, the canonical 16-path invocation MAY
extend to a **17-path invocation** with the new Azurite-backed
test file (e.g., `tests/classifier/pipeline/test_cost_journal_adls_azurite.py`)
per Q-K-a.4 = Option 2. Whichever baseline is bound at Phase 1,
hold it consistent across ALL Phase 3 commits in S31 — do not
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

# S20 canary + cassettes sub-surface (23 + 33 = 56 total)
.venv/bin/python -m pytest tests/baseline_v0/test_canary.py \
    tests/baseline_v0/test_cli.py -k 'canary' tests/synthetic_crawl/ -q
# Expect: 56 passed

# S21-S26 sub-surfaces (per-suite expectations broken out for
# halt-localization clarity; collapsed sum = 576):
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
# Sum (also verifiable as a one-liner): 32+30+30+43+13+19+35+74+129+152+7+12 = 576

# S27 + S28 per-tier cost-accounting wiring tests
.venv/bin/python -m pytest tests/runners/fixture_cascade/test_cost_journal_wiring.py -q
# Expect: 6 passed

# S28 Stage 1 ShardResult split tests (outside canonical 16-path)
.venv/bin/python -m pytest tests/classifier/stage1/test_run_cascade.py tests/classifier/stage1/test_cost_tracker.py -q
# Expect: 32 passed (16 run_cascade + 16 cost_tracker)
```

### Step 0.9 — S25-shipped + S26-shipped + S27-shipped + S28-shipped + S29-shipped + S30-validated invariants

```
# Verify the S25-S29 deliverables match what landed at each
# session's close. **S30 validated the ADLSCostJournal public
# API empirically against real Azure Blob storage** — the K-b
# script trace at S30 close confirmed write_initial / read /
# try_update / 412-mapping behavior matches DummyBlobBackend.
# Re-run unconditionally at every S31 cold start.

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

# S27: per-tier wiring helper signature stability.
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

    _journal_record_with_breakdown(journal=journal, shard_id='s1', stage=1, started_at='2026-05-26T00:00:00+00:00', domains_processed=10, components={'llm': 0.04, 'embedding': 0.01}, unattributed_cost_usd=0.0)
    _journal_record_with_breakdown(journal=journal, shard_id='s2', stage=2, started_at='2026-05-26T00:01:00+00:00', domains_processed=10, components={'fetch': 0.10, 'summarization': 0.20, 'classification': 0.30}, unattributed_cost_usd=0.0)
    _journal_record_with_breakdown(journal=journal, shard_id='s3', stage=3, started_at='2026-05-26T00:02:00+00:00', domains_processed=10, components={'evidence': 0.05, 'primary': 0.07, 'secondary': 0.0}, unattributed_cost_usd=0.03)

    state = journal.read().state
    per_tier_sum = sum(getattr(state.totals, fname) for fname in cj._TOTALS_FIELDS.values())
    shard_sum = sum(s.cost_usd for s in state.shards)
    assert state.totals.stage1_llm_usd == 0.04
    assert state.totals.stage1_embedding_usd == 0.01
    assert math.isclose(state.totals.cost_usd, per_tier_sum + shard_sum, abs_tol=1e-9), (state.totals.cost_usd, per_tier_sum, shard_sum)
    for fname in cj._TOTALS_FIELDS.values():
        assert hasattr(state.totals, fname), fname

print('OK S27+S28 per-tier wiring invariant holds at S31 cold start (all 8 slots populate)')
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
# Save to a script file and run via .venv/bin/python (the safety
# hook blocks the inline `python -c` form when the source string
# contains 'ast.parse').
cat > /tmp/check_s28_ast_phase0.py <<'PYEOF'
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

assert len(all_calls) == 3, f'expected 3 calls; found {len(all_calls)}'
assert len(stage1_calls) == 1, f'expected 1 stage=1 call; found {len(stage1_calls)}'

call = stage1_calls[0]
components_kw = next((kw for kw in call.keywords if kw.arg == 'components'), None)
assert components_kw is not None, 'Stage 1 call missing components kwarg'
assert isinstance(components_kw.value, ast.Dict), 'components must be a dict literal'
keys = [k.value for k in components_kw.value.keys
        if isinstance(k, ast.Constant)]
assert 'llm' in keys, f'Stage 1 components missing llm: {keys}'
assert 'embedding' in keys, f'Stage 1 components missing embedding: {keys}'
print('OK S28 cascade.py Stage 1 invoker AST structure intact (3 calls; stage=1 has llm + embedding)')
PYEOF
.venv/bin/python /tmp/check_s28_ast_phase0.py

# S29 NEW: K-b smoke script existence + import-loads cleanly.
.venv/bin/python -c "
import importlib.util
from pathlib import Path

path = Path('scripts/smoke_test_adls_cost_journal.py')
assert path.exists(), f'S29 K-b script missing: {path}'

spec = importlib.util.spec_from_file_location('s29_smoke', str(path))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# Verify the load-bearing public surface used by the script.
assert hasattr(m, 'main'), 'main() missing from K-b smoke script'
assert hasattr(m, '_build_credential'), '_build_credential helper missing'
assert hasattr(m, '_delete_blob'), '_delete_blob helper missing'

print('OK S29 K-b script intact (import OK; public surface intact)')
"

# (S30 produced zero repo code commits — no new behavior to
# invariant-check at Step 0.9. The S30 disposition is captured
# in workspace docs SESSION_LOG.md + LESSONS.md as documentary
# record, NOT as a Phase 0 load-bearing dependency. If those
# docs are missing for any reason, S31 Phase 6 re-records them;
# this does not block Phase 0.)
```

If any of 0.1-0.9 fail, HALT before doing any work.

---

## Required workspace reading (Session 31 first 10 minutes)

In this order:

1. **`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`** — full
   handoff state at S30 close. Lists scope candidates
   (A/D/E/K-a) with prerequisites + estimated scope.
   The S31 scope choice at Phase 1 picks from these.
   **K-b-exec is NOT a candidate** — closed S30.

2. **`~/crawler-audit/SESSION_LOG.md`** Session 30 entry — what
   landed during Candidate K-b-exec close (0 code commits + 2
   close-out workspace commits). The S30 disposition documents
   the redacted live-Azure trace, the tag-variance acceptance
   (2 new operator-side eval_data tags), and the empirical
   Phase 1 prereq check for Candidate A (unchanged from S29).

3. **`~/crawler-audit/LESSONS.md`** — 1 new section folded at
   S30 close, at end of file ("S30 folding" suffix). Locate via
   `grep -n '^## .*(S30 folding)' LESSONS.md`. Read with care:
   - "Operator-smoke posture (K-b) can close mock-vs-prod
     divergence risk in one execution; permanent CI test (K-a)
     is then optional rather than required" (S30 folding) —
     **MANDATORY READ before Phase 1 if K-a is being considered**.
     Documents how the K-b operator-smoke at S30 empirically
     closed the mock-vs-prod divergence risk for ADLSCostJournal;
     K-a is now defense-in-depth ONLY, not on a critical path.
     Forward-applicable to similar wrapper-class + external-
     service surfaces.

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
   **Empirically validated at S30** against real Azure.

8. **`tests/classifier/pipeline/test_cost_journal_adls.py`** at
   `835a531` — only if Candidate K-a touches ADLS testing. 19
   tests against `DummyBlobBackend` in-memory.

9. **`scripts/smoke_test_adls_cost_journal.py`** at S29 SHA
   `75a3937` — for reference if Candidate K-a is chosen (the
   K-b script's structure informs the K-a test layout). The S30
   trace verified its behavior matches DummyBlobBackend
   end-to-end against real Azure.

10. **`docs/CRAWLING_POLICY.md`** at S26 SHA `2314f5e` — only if
    operator wants to review the S26-tightened version (77 lines /
    2.52 KB).

11. **`tests/runners/fixture_cascade/cascade.py`** at S28 SHA
    `9afde57` — for reference if any candidate touches the
    driver. Module docstring documents that all 8 `_TOTALS_FIELDS`
    slots are wired (Stage 1 closure shipped S28). S29 + S30 did
    NOT touch this surface.

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
LOC delivered**. Use the S29-folded LESSONS additive-overhead
framing, NOT a linear ~3× multiplier.

**Prerequisites:**
- 2+ `canary_runs/*.parquet` files exist on operator's machine.
  Earliest natural date: 2026-06-06 (two Saturdays from S20 close
  at 2026-05-23) assuming operator ran the launchd installer
  immediately after S20.
- AI/ML team responses on 4 §Item 8 decisions OR explicit
  operator-side placeholder choices with "AI/ML-to-tune" notes.

**HALT IF** the 4 AI/ML decisions are not pre-resolved going into
Session 31 AND operator has not authorized explicit placeholder
choices.

**Empirical prereq audit at S30 close** (carry-forward to S31
open):
- 0 parquets on disk under any `canary_runs/` path (verified via
  `Path.rglob('*.parquet')` across repo + workspace).
- No `barcada` / `canary` plist in `~/Library/LaunchAgents/`
  (verified via `Path.home() / 'Library' / 'LaunchAgents'`).
- No AI/ML team responses or operator-side placeholder
  authorizations found anywhere in workspace.

Re-run these empirical checks at S31 Phase 1 BEFORE issuing the
candidate-choice AskUserQuestion (per S29 LESSONS pattern
"Empirical Phase 1 prerequisite check before scope-narrow"). If
the empirical state is unchanged, Candidate A remains blocked.

### Candidate D — Phase 4 PR-D operator-led labeling (operator territory)

Per plan §11 Risk Register entry. Stage 2 + Stage 3 labeling
gates PR-D/E/F/G. Operator-led; Claude Code's role limited to
tooling. W0-side unblocked at S27 (`workstream-0-end` tag at
`a1c5636`); still gated on operator-led labeling.

**S30 observation**: operator placed 2 new operator-side stage1-
related tags between S29 close and S30 open
(`workstream-stage1-prestaged-flags-end`,
`workstream-stage1-step3-end`). **These tags do NOT unblock PR-D**
— D remains gated specifically on Stage 2/3 labeling, and Stage 1
audit activity does not bridge to Stage 2/3 in any way documented
here. Operator-discretion at Phase 1 whether the Stage 1 cadence
informs S31's candidate ordering (e.g., as a signal that broader
labeling momentum exists), but the prereq status itself is
unchanged from S29.

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

### Candidate K-a — Azurite-backed integration test (OPTIONAL per S30 LESSONS)

**DOWNGRADED to OPTIONAL at S30** per the new posture-validation
LESSONS fold. The K-b operator-smoke at S30 empirically closed
the mock-vs-prod divergence risk that K-a would have permanently
protected against. K-a now serves only as defense-in-depth, NOT
on any critical path.

S25 shipped ADLSCostJournal against `DummyBlobBackend` in-memory.
S29 shipped Candidate K-b (operator-driven script). S30 executed
the K-b script against real Azure; trace clean end-to-end. K-a
remains a Docker-backed integration test option that spins up an
Azurite container and exercises the same operations against a
real Azure-compatible blob service.

**Operator should pick K-a only if** there's a forward-looking
reason it provides ongoing value beyond what the S30 K-b execution
already provided:
- `cost_journal_adls.py` will see frequent churn in upcoming
  sessions (the K-b script's one-off validation goes stale).
- Production traffic patterns are anticipated to exercise
  concurrency or feature paths the K-b script's sequential
  5-step matrix did not cover.
- CI safety net is required by a downstream consumer (e.g., a
  team SLO that mandates regression protection for the ADLS
  backend).

If NONE of those forward-looking justifications apply, **K-a
should remain deferred** at S31 — the S30 LESSONS fold says
defense-in-depth is a choice, not a default.

**Phase 1 carve-out capture (if K-a is picked):** at the moment
of selecting K-a, name the carve-out reason from the list above
(concurrency / production-feature-coverage / customer-visible-
critical-path) OR record explicit operator-override
("defense-in-depth without specific carve-out"). Pin the choice
in chat at Phase 1 so Phase 2 can proceed to K-a design without
re-litigating the candidate choice itself. This replaces what
might otherwise be a redundant Phase 2 Q-K-a.0 gate — Phase 1
is the right place to capture justification because it's
inseparable from scope resolution.

**Prerequisites:**
- Docker available locally; Azurite image pullable.

**Scope estimate**: ~50-100 LOC logic = **~150-300 LOC delivered**
+ Docker setup per the S29-folded LESSONS additive-overhead
pattern.

**Recommended posture if K-a chosen**: pair with a Q-K-a.4 =
Option 2 decision (add a 17th path to the canonical invocation)
so the Azurite test stays part of the regression gate.

### (REMOVED at S31) Candidate K-b-exec — CLOSED at S30

K-b-exec carry-forward was closed end-to-end at S30: operator
ran `scripts/smoke_test_adls_cost_journal.py` against a live
Azure sandbox container; trace clean for all 5 ETag-conflict-
matrix steps; ADLSCostJournal behavior matches DummyBlobBackend.
Trace recorded (REDACTED account/container per operator
preference) in SESSION_LOG.md S30 entry. **Do NOT re-issue
K-b-exec as a candidate at S31 unless operator explicitly
requests a re-run** (e.g., to validate against a different
sandbox account or after upstream changes to Azure SDK).

### Sub-question 1.TAG — Tag at session close (pinned at Phase 1)

Independent of scope choice; resolved fully here at Phase 1 so
Phase 5 has an unambiguous tag decision. Options per scope:

- **Candidate A** (barcada-drift): defer OR place candidate-
  specific (e.g., `barcada-drift-v0`).
- **Candidate D** (Phase 4 PR-D tooling): defer.
- **Candidate E** (cassette corpus expansion): defer.
- **Candidate K-a** (Azurite-backed CI test): defer OR consider
  `workstream-a-week2-end` if K-a is the final W A.2 code
  milestone (operator decides; see Phase 5 note below).

Phase 5 reads this resolution directly — no Phase 2 re-decision.

**Note on workstream-A.2-end**: W A.1 closed at S22's
`workstream-a-week1-end`. W A.2 is the orchestrator-side robots
work that landed across S23+S24+S25, plus the ADLS Phase 5
promotion at S25, plus the K-b operator smoke at S29 (script
ship), plus the K-b execution at S30 (operator-driven validation
trace). If K-a (CI Azurite test) ships at S31, it would arguably
be the final code piece. Operator-discretion whether to tag at
S31 close if K-a ships.

---

## Phase 2 — Design-gate elicitation (no code; AskUserQuestion)

Per chosen Phase 1 candidate. Each candidate has its own sub-
block. Source-verify at session-current HEAD per `[[verify-
before-asking-discipline]]` AND per S22-S30 "Plan-vs-reality at
Phase 2 source-verify" + S25-folded "Phase 2 source-verify drives
option-set design, not just gates" + S27-folded "Re-source-verify
the seam at closure time" LESSONS patterns BEFORE each
AskUserQuestion batch.

**HALT IF** any Phase 2 decision would require modifications to
`src/barcada_scraper/` production code beyond what was Phase-2-
authorized (per S22-S30 "Implicit-authorization HALT for src/-
locks" LESSONS pattern; surface as an explicit AskUserQuestion
before patching) OR to the W4.1.5 driver beyond the S16/S27/S28
W5.X-prefix exceptions OR to any S19-S30 deliverable — surface as
a design-gate sub-question before patching.

### CRITICAL Phase 2 hygiene from S26 LESSONS (4-option limit)

Before drafting EACH AskUserQuestion batch, count the prompt's
option set per Q-*. If any single Q-* enumerates >4 mutually-
exclusive options, tier the question or split horizontally. Do
NOT silently narrow. (See S30 prompt Phase 2 for the full
explanation.)

### CRITICAL Phase 2 hygiene from S28 LESSONS (empirical-vs-by-design)

When closing a deferred gap or otherwise extending an existing
surface, audit EVERY existing test pin in the affected area for
the "by design" / "empirically true" distinction. (See S30
prompt Phase 2 for the full explanation.)

### CRITICAL Phase 2 hygiene from S29 LESSONS (LOC budgeting — additive overhead floor)

When a candidate proposes new operator-driven Python files,
audit the proposed LOC estimate by ADDING the overhead floor
(~70-100 LOC for Copyright header + module docstring + imports +
argparse), NOT multiplying by ~3×. (See S30 prompt Phase 2 for
the full table.)

### **CRITICAL Phase 2 hygiene from S30 LESSONS (posture-validation: operator-smoke vs CI test)**

Per the new S30-folded LESSONS section "Operator-smoke posture
(K-b) can close mock-vs-prod divergence risk in one execution;
permanent CI test (K-a) is then optional rather than required":

When a candidate proposes a NEW external-service-backed test or
smoke for a wrapper class (Azure SDK, AWS SDK, GCP SDK, network
service, etc.), explicitly default to **operator-smoke (K-b-
style) posture** at Phase 2, NOT permanent-CI-test (K-a-style)
posture. Reasoning:

1. Land the wrapper + unit tests against an in-memory double
   (already done for ADLSCostJournal at S25; analogous for any
   new surface).
2. Ship a one-off operator-driven smoke script next to it
   (mirror `scripts/smoke_test_adls_*.py` conventions:
   Copyright header, argparse, env-var-driven auth, public-API-
   only consumption, parallel-SDK-client cleanup).
3. Run the smoke once against a real sandbox; capture the
   trace.
4. **Only escalate to a K-a-style permanent CI test if the
   smoke surfaces a divergence** that the in-memory double
   didn't catch, OR if the surface gets heavy enough write/
   read traffic in production that ongoing regression
   protection is genuinely needed.

**Exception cases where K-a should be the Phase 2 default
instead** (carve-out at the design gate):

- Wrapper-class behavior depends on **concurrent** access
  patterns the in-memory double cannot model (e.g., real
  contention on the same blob from multiple workers).
- Production usage will hit a feature of the real service
  (server-side encryption, custom domain, network ACLs) that
  the smoke can't easily exercise in a single run.
- The wrapper class is on a critical path for a
  customer-visible feature where any regression must be caught
  *before* the smoke could be re-run.

In all three carve-out cases, document the carve-out at the
Phase 2 design gate so the K-b vs K-a tradeoff is explicit.

For **Candidate K-a specifically at S31**: the operator-discretion
threshold is whether the S30 K-b trace closed the divergence risk
sufficiently for the operator's current confidence needs. If yes,
defer K-a. If no, justify the carve-out at Phase 2 and proceed.

### If Candidate A (barcada-drift)

Carry-forward from S22-S30 prompts (unchanged).
- Q-A.1 CLI namespace; Q-A.2 drift metric; Q-A.3 alert threshold;
  Q-A.4 input contract; Q-A.5 output shape; Q-A.6 test corpus.

(NB: Candidate A has 6 Q-* gates. Two AskUserQuestion caps apply
independently and BOTH need to be checked: 4 OPTIONS per question
(S26 LESSONS) + 4 QUESTIONS per call (schema cap). Split into
2-3 sequential AskUserQuestion calls.)

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

(Carve-out justification was captured at Phase 1 candidate
selection per the K-a Phase 1 entry; Phase 2 does NOT re-litigate
that choice. Phase 2 designs the test once K-a is the chosen
scope.)

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

### Shared sub-questions (all candidates)

- **Q-SHARED.1 Commit shape**: per-module (S18-S30 default;
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
next. Per S22-S30 precedent.

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
    <new S31 test paths if any> -q
# If Candidate K-a is chosen with Q-K-a.4 = Option 2, the
# concrete addition is:
#     tests/classifier/pipeline/test_cost_journal_adls_azurite.py
# (17-path invocation; recompute headline as 970 + N new
# Azurite tests).
```

Expected: previous_baseline + N new tests, all passing. If
failing tests are NOT a deliberate consequence of the surface-
under-test → HALT.

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
the format-fix into the commit (per S19-S30 pattern).

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
~70-100 LOC additive overhead floor": if the commit ships a new
script/file, claim total LOC (via `wc -l`) NOT logic-only LOC.

**4. `git status` check**

Only intended files staged; no surprise `eval_data/` or
unauthorized `src/barcada_scraper/` changes. Operator-side
`eval_data/` modifications are expected to stay unstaged across
sessions (Sessions 8-30 precedent).

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
Phase 3 start                  : 970  (Session 30 close baseline)
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
canonical S31 baseline for any candidate that touches the
orchestrator sub-surface OR the driver sub-surface OR the journal
sub-surface (Candidate K-a definitely; A/D/E less so).
Whichever baseline is bound at Phase 1, hold it consistent across
ALL Phase 3 commits in S31 — do not switch mid-session.

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
fail the gate even though no S31 commit touches eval_data.

When this fires:
1. Confirm the failing row's content is in operator-WIP
   (`git diff eval_data/...`), not in committed HEAD
   (`git show HEAD:eval_data/...`).
2. Confirm the S31 commits do not touch eval_data
   (`git diff origin/main..HEAD -- eval_data/`).
3. Surface to operator with the exact row + reason + diff vs
   committed state.
4. Two paths: (a) operator-fix in WT, then re-run gate;
   (b) stash eval_data WIP, push, restore.
5. Do NOT auto-fix locked-artifact content.

S20+S22 precedent: operator chose (a). S21/S23/S24/S25/S26/S27/S28/S29/S30
did not need this protocol at Phase 4 push (S28 saw a transient
"1 error" first-run that cleared on identical re-run; S29-S30 did
NOT reproduce the transient). LESSONS-worthy if the transient
reproduces in S31+.

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
plus the K-b script at S29 plus the K-b execution at S30). If
Candidate K-a is chosen at S31 AND operator considers it the
final W A.2 code milestone, a `workstream-a-week2-end` annotated
tag would be appropriate at S31 Phase 5.

---

## Phase 6 — Workspace close-out

- Append Session 31 entry to `~/crawler-audit/SESSION_LOG.md`
  including a **Canonical S31-close baseline** block with the
  exact pytest invocation + verified test count (per S22-S30
  LESSONS "Pin the baseline for the next session's Phase 0
  Step 0.5"; without this, S32 Phase 0 will infer from the
  "Combined headline" bullet and potentially HALT on
  accounting-mismatch).
- Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md` for
  Session 32 — explicitly pin the S32 Phase 0 workspace anchor
  SHA per S21-S30 post-audit pattern (LESSONS "Workspace HEAD
  delta tolerance"); do not omit. After the close-out commit
  lands, expect **1-2 follow-up commits** pinning the actual
  SHA (S21 needed 1; S22 needed 2; S27 needed 1; S28 needed 2
  including a post-close hygiene fold; S29 needed 1; S30 needed
  1).
- Update `~/crawler-audit/LESSONS.md` with any new forward-
  applicable patterns surfaced this session.
- Workspace close-out: 1 primary commit + 1-2 follow-up commits
  pinning the anchor SHA and any audit-surfaced corrections.
  Push workspace after operator confirms.

Note: drafting the next-session prompt (`SESSION_32_PROMPT.md`)
is NOT a built-in Phase 6 step. Per S20→S21..S26→S27→S28→S29→S30
precedent, prompt-drafting is operator-commissioned between
sessions — not always-on close-out work. If the operator asks for
it explicitly at S31 close, draft it as a separate follow-up;
otherwise leave for the next session to either operator-commission
or scope out at S32 open.

---

## Acceptance criteria

**Per candidate (reduces if Phase 1 narrows scope):**

### Candidate A (barcada-drift)

Carry-forward from S22-S30 prompts (unchanged):
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

0. Phase 1 carve-out justification recorded in chat at scope
   selection (which carve-out applies, OR explicit operator-
   override for defense-in-depth). See Phase 1 Candidate K-a
   entry for the capture protocol.
1. Azurite-backed integration test passes locally + (if Q-K-a.4
   includes CI) in CI; mock-vs-prod divergence empirically
   closed for the operations covered (already empirically
   closed at S30 for the operations in the K-b script).
2. If Q-K-a.4 = Option 2 (17-path), the new test path is added
   to the canonical invocation and the Canonical S31-close
   baseline reflects the new headline count.

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
  - **S30 produced zero repo locks** (the K-b-exec disposition
    is documented in SESSION_LOG.md, not in repo code).
  - Per-sub-suite test counts stay green (or grow): same as
    S30 prompt acceptance criteria (32 robots-parser / 30
    robots_gate / 30 robots_bypass_config / 43 cost_journal /
    13 cost_journal_local / 19 cost_journal_adls / 35
    robots_integration / 74 vmss_worker / 129 job_runner /
    152 worker_loop / 7 robots_gate_integration / 12
    worker_loop_persistence / 52 driver / 16 stage1
    run_cascade / 16 stage1 cost_tracker).
  - `docs/CRAWLING_POLICY.md` stays at 77 lines / 2519 bytes
    unchanged from S26 SHA `2314f5e` (verified at Phase 0
    Step 0.9).
  - All other S25-S29 invariants from Phase 0 Step 0.9 hold.
  - The combined total stays at 970 (or grows) unless a Q-*
    AskUserQuestion explicitly authorizes a same-shape 1↔1
    replacement.

---

## Out-of-scope (no exceptions without operator authorization)

Per the regression-protection checklist. Unchanged from S30
prompt — **S30 produced zero repo code commits**, so no new
locks are added at S31 open.

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
  cost_journal.py` are LOCKED at `1d9404e`.
- The S22 additions to `tests/classifier/pipeline/test_cost_journal.py`
  (14 new tests + 1 updated test) are locked, EXCEPT for the
  S25 Q-J.8-extension replacement at SHA `835a531`.

**S23 deliverables (Session 23 W A.2 sub-surfaces):**
- `src/barcada_scraper/orchestrator/robots_integration.py`
  (244 LOC; public API at `279bb77`).
- `tests/orchestrator/test_robots_integration.py` (35 tests at
  `279bb77`).
- All other S23 additions per S30 prompt Out-of-scope list.

**S24 deliverables (Session 24 W A.2 sub-surfaces):**
- The 3 module-level private helpers in
  `src/barcada_scraper/orchestrator/worker_loop.py` at `48c324a`.
- The 5 retargeted test_stage2_pages_invoker_* fixtures.
- `tests/orchestrator/test_worker_loop_persistence.py` at S25
  `aed7873` (12 tests; 11 S24-unchanged + 1 S25-replaced).
- The 3 S24-added tests in
  `tests/orchestrator/test_robots_gate_integration.py`.

**S25 deliverables (Session 25 W A.2 sub-surfaces):**
- `src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
  at S25 SHA `835a531` (295 LOC; full backend). **Empirically
  validated at S30** against real Azure Blob storage via the
  K-b script. Candidate K-a (if chosen at S31) may CONSUME
  `ADLSCostJournal` but MUST NOT modify the public API
  signatures without explicit Phase 2 authorization.
- `tests/classifier/pipeline/test_cost_journal_adls.py` at S25
  SHA `835a531` (19 tests + `DummyBlobBackend`).
- All other S25 deliverables per S30 prompt Out-of-scope list.

**S26 deliverables (Session 26 W A.1 W8 sub-surface):**
- `docs/CRAWLING_POLICY.md` at S26 SHA `2314f5e` (77 lines /
  2519 bytes).

**S27 deliverables (Session 27 W A.0 W5.X sub-surface):**
- `tests/runners/fixture_cascade/cascade.py` per-tier wiring
  changes at S27 SHA `a1c5636` (extended at S28).
- `tests/runners/fixture_cascade/test_cost_journal_wiring.py` at
  S27 SHA `a1c5636` (modified at S28).

**S28 deliverables (Session 28 carry-forward closure):**
- `src/barcada_scraper/classifier/stage1/run.py` at S28 SHA
  `776d203` (ShardResult +2 fields).
- `tests/classifier/stage1/test_run_cascade.py` at S28 SHA
  `776d203` (+1 net-new test).
- `tests/runners/fixture_cascade/cascade.py` Stage 1 invoker
  switch at S28 SHA `9afde57`.
- `tests/runners/fixture_cascade/test_cost_journal_wiring.py`
  1↔1 same-shape replacement at S28 SHA `ae9e627`.

**S29 deliverables (Session 29 carry-forward closure):**
- `scripts/smoke_test_adls_cost_journal.py` at S29 SHA `75a3937`
  (220 LOC; operator-driven 5-step ETag-conflict-matrix smoke).
  **Empirically validated at S30** end-to-end against real Azure;
  trace matches DummyBlobBackend.

**S30 deliverables (Session 30 carry-forward closure):**
- **No repo code changes.** S30 was K-b-exec execution only.
- Workspace docs (SESSION_LOG.md, LESSONS.md,
  SESSION_TRANSITION_TEMPLATE.md) updated at S30 close commits
  `9d4691e` (primary) + `67a9c40` (anchor-pin).

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
- All workstream tags at their placed SHAs (13 tags as of S30
  close — includes 2 new operator-side stage1 tags)
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` (READ-ONLY)
- `CLASSIFICATION_ADJACENT_PLAN.md` (UPDATED only when AI/ML
  decisions land)
- `RECONCILIATION_2026-05-21.md`
- `docs/phase4_implementation_plan.md` (Phase 4 governance
  reference)

**Operator-owned territory:**
- All of `eval_data/` — labeling-workstream territory; per-row WIP
  edits across sessions are expected and unstaged (Sessions 8-30
  precedent). S22→S30 inter-session operator-side eval_data
  COMMITS are tolerated per the "Workspace HEAD delta tolerance"
  LESSONS pattern — verify they're eval_data-only via
  `git show --stat <sha>` for each commit in the delta.
  S30 saw 2 new operator-side **TAGS** at S30 open
  (`workstream-stage1-prestaged-flags-end`,
  `workstream-stage1-step3-end`) both pointing at eval_data-only
  commits; treat as in-class with the eval_data commit tolerance.

**Production code:**
- `src/barcada_scraper/` — locked unless Phase 2 design-gate
  explicitly authorizes a specific module. S21-S25+S28
  authorized (full list in S30 prompt; unchanged).
  S26 + S27 + S29 + **S30** added no new src/ authorizations.
  None of the S31 candidates currently anticipate new src/
  authorizations.

**Pipeline configs:**
- `configs/`

**Phase 4 work:**
- Phase 4 PR-D/E/F/G work UNBLOCKED on the W0 side since S27
  (workstream-0-end placed); still gated on operator-led Stage 2/3
  labeling. Candidate D opens when labeling begins.

---

## Verify-before-asking discipline (strict rule from S19-S30)

Per `[[double-check-before-commit]]` memory: **ALWAYS verify
every concrete claim in the commit message against actual source/
output BEFORE staging.** Fixture names, file counts, exit codes,
line counts, test counts, helper names, smoke outcomes, SHA
prefixes, regex matches, API signatures. No claims by pattern-
completion. Build a verification table in chat (claim → reality →
status) and reconcile before "Confirm to commit?".

Specific to S31:

- Before each chosen-candidate-specific claim in a commit message,
  verify against the actual source / runtime output:
  - Candidate A: barcada-drift CLI invocation produces the
    expected output shape against ≥2 parquets.
  - Candidate D: tooling smoke produces expected output.
  - Candidate E: cassette count post-record; FP-curation log
    updated.
  - Candidate K-a: Azurite container produces the expected 412
    on race-loser write_initial; full ETag-conflict matrix
    passes locally + (if CI integration chosen) in CI.
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

LESSONS-folded discoveries from S22-S30 worth re-applying:

- **Plan-vs-reality at Phase 2** (S22 LESSONS).
- **Phase 2 source-verify drives option-set design** (S25 LESSONS;
  S28 + S29 demonstrated this directly).
- **Implicit-authorization HALT** (S22-S30 LESSONS): Q-*
  answers may require touching files NOT in S31 Out-of-scope's
  authorized-touch list. Surface explicit authorization in
  Phase 2 BEFORE the commit, not as a HALT mid-Phase-3.
- **Q-J.8 explicit allowlist may be incomplete; HALT-and-extend
  pattern** (S25 LESSONS).
- **Local imports defeat module-attribute monkeypatch** (S25
  LESSONS).
- **Tightened-precondition test-fixture retargeting** (S24
  LESSONS).
- **Test against public API surface only** (S24 LESSONS, S29
  extension): tests should probe behavior via the public surface.
  S29 extended the same pattern to operator-driven scripts.
  **S30 empirically validated this** end-to-end against real
  Azure — the parallel `BlobClient` in `_delete_blob` works
  without touching `ADLSCostJournal._backend._client`.
- **Source-verify line numbers per Phase 3 commit** (S23
  LESSONS).
- **AskUserQuestion 4-option limit can silently truncate a Q-*
  option set** (S26 LESSONS).
- **Deferred wiring gaps fold cleanly into workstream-end if the
  original implementation left a parallel-API seam** (S27
  LESSONS).
- **Empirical-vs-by-design distinction in test pins** (S28
  LESSONS).
- **Phase 0 fixture-count commands need `2>/dev/null` + a
  bounded timeout** (S28 post-close LESSONS; S30 surfaced 5
  hung `bfs`/find processes from prior sessions during close —
  killed at operator authorization).
- **Operator-driven script LOC estimates need a ~70-100 LOC
  additive overhead floor, not a linear multiplier** (S29
  LESSONS).
- **Public-API-only cleanup pattern extends from tests to
  operator scripts** (S29 LESSONS).
- **Empirical Phase 1 prerequisite check before scope-narrow**
  (S29 LESSONS; S30 re-validated empirically — Candidate A
  prereqs unchanged from S29 close).
- **Operator-smoke posture (K-b) can close mock-vs-prod
  divergence risk in one execution; permanent CI test (K-a)
  is then optional rather than required** (NEW S30 LESSONS):
  when a wrapper class is verified against in-memory doubles in
  unit tests, a single first-run live-SDK smoke can close the
  mock-vs-prod divergence risk empirically. Permanent CI
  infrastructure (Docker/Azurite/simulator) becomes a
  defense-in-depth choice, not a prerequisite. Forward-applicable
  rule: for new wrapper-class + external-service surfaces,
  default to K-b posture; escalate to K-a only when a defined
  carve-out applies (concurrency / production-feature-coverage /
  customer-visible-critical-path). For Candidate K-a at S31
  specifically, this means the operator must justify the
  carve-out at Q-K-a.0 before committing to ship K-a.

---

## Commit hygiene (per LESSONS + S19-S30 additions)

- File-based commit messages at `/tmp/<id>-msg.txt`.
- Per-module commits (Phase 3 commit shape unless Q-SHARED.1
  overrides).
- "Confirm to commit?" before EVERY commit. Pair with verification
  table (always) and `git diff --staged` (when appropriate per
  `[[double-check-before-commit]]` triggers).
- Commit body includes: action ref (S30 used
  `S30 close-out` for the workspace commit; S31 chooses its own
  per candidate), scope summary, file touches, test count delta
  (with net-new vs newly-in-invocation pre-existing distinction
  per S23 LESSONS), plan reference. NO `Co-Authored-By`.
- Pre-push gate must run green. Never use `--no-verify`.
- Pre-push vermin: `git ls-files '*.py' | xargs vermin
  --target=3.10` to filter venv-internal pytest 3.14 false-
  positives.
- Mid-implementation ruff format-check, not only pre-push.
- For S19-S30-test modifications: explicit Phase 2 authorization
  required; document the modification scope explicitly in the
  commit body (per S22-S30 LESSONS "Implicit-authorization HALT"
  pattern).
- Workspace close-out (Phase 6) lands as its own commit at session
  close, followed by 1-2 follow-up commits pinning the anchor SHA
  for the next session (S21-S30 pattern).

---

## Context-window awareness

S30 ran across 0 code commits + Phase 6 close-out (2 close-out
commits), comfortably within context. S31 budget per scope:

- Candidate A: medium (~300 LOC logic + ~70-100 LOC overhead
  floor ≈ ~370-400 LOC delivered).
- Candidate D: small.
- Candidate E: small.
- Candidate K-a: medium (~50-100 LOC logic + ~70-100 LOC
  overhead floor ≈ ~120-200 LOC delivered + Docker setup;
  **OPTIONAL at S31** per the S30 LESSONS fold).

Strategies:
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore
  subagent per S22-S30 "Explore-subagent + spot-check" LESSONS
  pattern.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before the chosen S31 scope closes,
  transition per "no mid-commit-batch transitions" — finish
  in-flight sub-surface, then close session and refill the
  transition template for Session 32.

---

## Reporting in chat at session close

After all Session 31 commits land + push + close-out per the
S13-30 pattern:

1. Commit SHA(s) of each S31 sub-surface.
2. Sub-surface(s) landed (per candidate).
3. Test count delta: 970 (or 480/538/944/17-path) baseline → S31 close.
4. Driver suite count at S31 close (52/52 expected unless
   candidate added new driver-area tests).
5. Files touched per sub-surface.
6. Tag dispositions (incl. any new tag per 1.TAG).
7. Per-tier cost-accounting wiring: CLOSED end-to-end since S28
   (regression-protection enforced via Phase 0 Step 0.9 invariant
   smokes + Phase 3 per-commit checkpoint).
8. ADLSCostJournal status: K-b SHIP closed S29; K-b EXEC closed
   S30 (trace matches DummyBlobBackend); K-a status per S31
   scope choice (deferred OR shipped with Q-K-a.0 justification).
9. Any spend (LLM, infrastructure, cassette-capture).
10. Robots.txt compliance log (if Candidate E expanded the
    cassette corpus).
11. FP-curation log update (if Candidate E expanded the cassette
    corpus).
12. Verify-before-asking summary: any source-verification
    findings surfaced.
13. Outstanding items for Session 32.
14. Tags state at S31 close.

Do not propose Phase 4 PR-D/E/F/G work this session unless
Candidate D was chosen and operator-led labeling is in flight.

---

## Carry-forward bakes (no amendment file needed)

All S30 close-out commits (`9d4691e` primary + `67a9c40` anchor
follow-up) plus the S30 disposition have been folded directly
into this prompt — S31 does not need a separate amendment file:

- **S30 close-out anchors** folded into Step 0.1 (workspace
  anchor `67a9c40` with operator-eval_data-commit + prompt-
  drafting-commit tolerance; repo anchor `af6f1d4` with
  operator-eval_data-commit tolerance; reflects S30's zero-code-
  commit posture), Step 0.2 (13 tags expected; includes the 2
  new operator-side stage1 tags), Step 0.5 (Canonical S30-close
  baseline 970 pinned with 16-path invocation; 944 narrower for
  candidates that don't touch ADLS or robots_gate_integration),
  Step 0.9 (S24+S25+S26+S27+S28+S29 stability PLUS new S30
  workspace-doc invariants: SESSION_LOG.md S30 entry present;
  LESSONS.md S30 folding section present).
- **1 NEW LESSONS section from S30 close**:
  - "Operator-smoke posture (K-b) can close mock-vs-prod
    divergence risk in one execution; permanent CI test (K-a)
    is then optional rather than required" referenced at
    Phase 2 "CRITICAL Phase 2 hygiene from S30 LESSONS
    (posture-validation: K-b vs K-a)" (apply when sizing any
    new wrapper-class + external-service candidate) AND at
    Phase 1 Candidate K-a's OPTIONAL designation AND at Phase 2
    Q-K-a.0 (carve-out justification required before K-a ships)
    AND at the Verify-before-asking section's LESSONS-folded-
    discoveries list.
- **K-b-exec closure** folded into the carry-forward list at
  the top (Candidate K-b-exec REMOVED from S31 candidates;
  documented as closed at S30 in SESSION_LOG.md) AND Out-of-
  scope's S30 deliverables note (no repo code changes;
  workspace docs only).
- **Tag-variance disposition** folded into Step 0.2 (13 tags
  expected; 2 new operator-side stage1 tags accepted in-class
  with eval_data commit tolerance per S30 operator
  authorization).

If new amendments arise pre-S31 open, walk them per the reviewer-
feedback hygiene pattern in this prompt's "Reviewer-feedback
hygiene" section.
