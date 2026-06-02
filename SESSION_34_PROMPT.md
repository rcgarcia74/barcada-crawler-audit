# Session 34 prompt — scope picked at Phase 1
# (S33 closed Candidate K-a at repo f1cdce8 — the Azurite-backed
#  live-on-demand ADLS integration test. K-a is now CLOSED. S34
#  enters with the SAME near-empty warm-candidate queue as S33:
#  A blocked / D operator-led / E exhausted. No new carry-forward
#  was introduced by S33.)

**Drafted at Session 33 close (2026-06-01), operator-commissioned.**
Mirrors the S20/.../S32/S33 prompt structure. Scope-agnostic at
Phases 0/1; scope-specific design gates at Phase 2 per chosen
candidate. Strict 7-phase ordering with halt-on-mismatch preserved.

This prompt should be invoked from `~/crawler-audit/SESSION_34_PROMPT.md`
or operator-mirrored to `~/Downloads/session-34-prompt.md`. Re-read
it on session open.

---

## Scope

Engineering session. Repo HEAD at `f1cdce8`
(WA2.W8.adls-azurite-ci-test; S33 Candidate K-a). Workspace HEAD at
the S33 close-out chain `dc21714` (primary `83e188a` + anchor-pin
`a9692af` + framing/self-reproduction correction `dc21714`) + this
prompt-drafting commit (see Step 0.1). **Workstream 0 fully closed
at S27 via the `workstream-0-end` tag at `a1c5636`**.

Carry-forward candidates entering S34:

- **barcada-drift (Candidate A)** — deferred since S20; still needs
  4 AI/ML decisions per CLASSIFICATION_ADJACENT_PLAN.md §Item 8 AND
  2+ `canary_runs/*.parquet` files. **S33 re-confirmed empirically**
  that the launchd installer has NOT been run (no plist in
  `~/Library/LaunchAgents/`; 0 `canary_runs` parquets on disk; the
  one parquet on disk is an unrelated stage2-pages canary in
  `~/Downloads`). Same state as S29/S30/S31/S32 close. **Remains
  BLOCKED.**

- **Phase 4 PR-D tooling (Candidate D)** — operator-led labeling
  territory. W0-side unblocked since S27; still gated on
  operator-led Stage 2/3 labeling.

- **Cassette corpus expansion (Candidate E) — EXHAUSTED.** S32 grew
  the corpus to 30, the plan's stated upper bound (§4 W7
  "~20-30 representative domains"). **No further +N is available
  without first amending the plan ceiling** (a Phase 1/2 or
  plan-revision decision). If the operator wants more cassettes,
  raise the bound first; do NOT add cassettes under the current
  plan.

- **ADLSCostJournal Azurite-backed CI test (Candidate K-a) —
  CLOSED at S33** (`f1cdce8`). The Azurite-backed live integration
  test now exists. **IMPORTANT framing for S34**: it is a
  **live-on-demand** net, NOT default-CI. The test is
  `@pytest.mark.live` + skip-by-default and is NOT in the canonical
  16-path — it guards `cost_journal_adls.py` only when run under
  `-m live` in a Docker-capable environment. What protects that
  module on the DEFAULT test run is still the **19 in-memory
  `DummyBlobBackend` tests** in `test_cost_journal_adls.py`. Wiring
  K-a into an actual CI pipeline (`-m live` + Docker in the runner)
  is a **separate, un-done step**. The `--skipApiVersionCheck` flag
  that absorbs the SDK-vs-Azurite x-ms-version skew is BAKED INTO
  the fixture's `docker run` (self-reproducing; confirmed at S33
  close). K-a is NOT a carry-forward; any new ADLS live-test work
  (e.g., CI wiring, lease/SAS coverage) is a FRESH candidate.

**No new carry-forward introduced by S33.** The S33 deliverable is
a single test file + a 3-line marker registration; the canonical
970 test count is unchanged.

**Scope-availability note (IMPORTANT):** with A blocked, D
operator-led, E exhausted, and K-a now closed, S34 may have **no
clearly-actionable engineering scope** unless the operator (a)
unblocks A (run the launchd installer + resolve the 4 AI/ML
decisions or authorize placeholders + accumulate ≥2 parquets), (b)
begins D labeling, (c) authorizes a plan-ceiling revision to reopen
E, or (d) commissions a NEW candidate (e.g., wiring K-a into CI).
Unlike S33, there is now NO self-contained optional candidate
remaining (K-a was that candidate and it shipped). Surface this at
Phase 1 before the candidate-choice AskUserQuestion.

Operator chooses at Phase 1 which candidate Session 34 ships.
Each candidate has its own Phase 2 design-gate template.

**Sessions 13-33 precedent:** this session does NOT modify the
W4.1.5 driver orchestration at `tests/runners/fixture_cascade/`
(locked at `dd64963` for original files; `cascade.py` extended at
`a1c5636` under S27 W5.X-prefix authorization, and at `9afde57`
under S28 W5.X-prefix authorization; `test_cost_journal_wiring.py`
added at `a1c5636` under S27 authorization and modified at
`ae9e627` under S28 Q-StgSplit.4 1↔1-replacement authorization).
Does NOT modify `expected.schema.json` v1.1 / `META_SCHEMA.md`
v1.1. Does NOT modify the committed `tests/fixtures/baseline-v0/`
snapshot at `9e9a1fb`. Does NOT modify the Session 19-33
deliverables. Does NOT modify the **S31 cassette deliverables** at
`06d67c4` (5 dirs) or the **S32 cassette deliverables** at
`cfa0ec1` (5 dirs) — never re-records or deletes any of the 30.
Does NOT modify the **S33 deliverable** at `f1cdce8`
(`tests/classifier/pipeline/test_cost_journal_adls_azurite.py` +
the `live` marker in `pyproject.toml`).

Does NOT modify production code under `src/barcada_scraper/`
UNLESS Phase 2 design-gate explicitly authorizes a specific module.
Of the S34 candidates: Candidate A would add a NEW `barcada-drift`
module (new file, not a modification of locked code); Candidate D
is tooling-only.

Full regression-protection checklist in **Out-of-scope** at the
end of this prompt. Re-read it before any code lands.

---

## Reviewer-feedback hygiene (if this prompt is reviewed)

If an external reviewer (operator-invoked) flags items in this
prompt before Session 34 starts, walk each flagged item against
on-disk reality at the workspace HEAD and repo HEAD `f1cdce8` (or
whatever HEAD the operator's machine carries), BEFORE applying any
change. Per S19-S33 pattern (LESSONS "Reviewer-feedback hygiene"):

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
halts catch hidden scope expansion (per S22-S33 "Implicit-
authorization HALT for src/-locks"). Phase 3 halts catch
regressions (including same-shape test failures outside the
prompt's explicit allowlist). Phase 4 halts catch pre-push gate
failures (incl. operator-WIP-in-locked-tree).

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

Run in order. Halt and surface to operator on any mismatch.

### Step 0.1 — Workspace + repo HEAD

```
# Workspace at Session 34 start. S33 close-out landed across:
# 83e188a (primary close-out: SESSION_LOG.md +
# SESSION_TRANSITION_TEMPLATE.md + LESSONS.md) + a9692af (anchor-pin
# pinning 83e188a) + dc21714 (operator-feedback framing correction:
# K-a live-on-demand + self-reproduction confirmation) + this
# prompt-drafting commit.
git -C ~/crawler-audit rev-parse HEAD
# Expect: dc21714 (S33 framing correction) OR this S34
# prompt-drafting commit succeeding it OR a later commit if
# additional workspace doc edits / further prompt revisions landed
# post-fixes. If N commits ahead of dc21714, verify each via
# `git log --oneline dc21714..HEAD` against expected
# prompt-finalization / doc-edit patterns; surface the SHA delta
# and request authorization if anything is unexpected. (S20-S33
# precedent: operator authorized continuation when 1-4 extra
# workspace commits were the strengthened prompts themselves.)

# Repo at Session 33 final state:
git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: f1cdce8 (WA2.W8.adls-azurite-ci-test: S33 Candidate K-a).
#
# Tolerated delta: operator-side eval_data labeling commits between
# S33 close and S34 open are expected (Sessions 8-33 precedent).
# Per the S22-folded "Workspace HEAD delta tolerance" LESSONS
# pattern: tolerate N additional commits as long as EACH commit's
# stat is strictly within eval_data/* (no src/barcada_scraper/*,
# no tests/* [INCLUDING no tests/fixtures/synthetic_crawls/* and no
# tests/classifier/pipeline/test_cost_journal_adls_azurite.py], no
# scripts/*, no docs/* touches). Verify via `git show --stat <sha>`
# for every commit in f1cdce8..HEAD; surface any non-eval_data
# delta for operator authorization before continuing.
```

### Step 0.2 — Tags (13 expected; unchanged from S30/S31/S32/S33 close)

```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort
# Expect 13 tags as of S33 close (UNCHANGED from S32 close; S33
# placed no tag per its 1.TAG = defer):
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

# NOTE: workstream-a-week2-end was OFFERED at S33 (K-a as the final
# W A.2 code milestone) but the operator DEFERRED it. If S34 declares
# W A.2 closed, that annotated tag remains appropriate (1.TAG).

# Tolerated delta: additional operator-side stage1-* / eval_data-*
# tags may land between S33 close and S34 open. For each new tag
# beyond the 13 expected, verify the tagged commit is eval_data-only
# via `git show --stat <tag>`; if so, treat as operator-domain
# marker. If a new tag points at any src/barcada_scraper/* / tests/*
# / scripts/* / docs/* commit, HALT for operator authorization.
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
# S29-S33 did NOT touch this surface.
```

### Step 0.4 — Fixture counts (use Python pattern per S28 LESSONS hygiene fold)

**IMPORTANT**: per S28-folded LESSONS "Phase 0 fixture-count
commands need `2>/dev/null` + a bounded timeout", do NOT use bare
`find` invocations here. Use the Python pattern below.

**UNCHANGED FROM S33**: all six counts are identical to S32/S33
close — S33 shipped a test file, NOT a cassette. `cassette_count`
and `exclusions_count` stay at **30**.

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
assert cassette_count == 30, cassette_count
assert exclusions_count == 30, exclusions_count
print(f'OK fixture counts: html={html_count} expected={expected_count} meta={meta_count} baseline={baseline_count} cassette={cassette_count} exclusions={exclusions_count}')
"
```

If the assertions fire, HALT and surface to operator.

### Step 0.5 — Test-suite baseline (S34 canonical)

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
# Sub-totals (16 paths; ALL identical to S27-S33 close — the S33
# Azurite test is @pytest.mark.live + skip-by-default and is NOT in
# this invocation; the 33 synthetic_crawl tests are hermetic):
#   210 conformance + 52 driver + 99 baseline_v0 +
#    33 synthetic_crawl + 32 robots + 30 robots_gate +
#    30 robots_bypass_config + 43 cost_journal +
#    13 cost_journal_local + 19 cost_journal_adls +
#    35 robots_integration + 74 vmss_worker +
#   129 job_runner + 152 worker_loop +
#     7 robots_gate_integration + 12 worker_loop_persistence = 970
#
# Pinned in SESSION_LOG.md "Canonical S33-close baseline" block.
```

The sub-paths add up to 970. Any drift = halt. If the headline
mismatches, re-run each sub-path independently to localize.

**Narrower baselines**:
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 944 (S27-S33-equivalent narrower; canonical 16-path minus 19
  cost_journal_adls minus 7 robots_gate_integration).

Whichever baseline is bound at Phase 1, hold it consistent across
ALL Phase 3 commits in S34. (If a candidate adds new test paths,
the count GROWS — the cumulative-test-count gate never lets it
decrease except for a Q-*-authorized same-shape 1↔1 replacement.)

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

# S20 canary + cassettes sub-surface (verify as separate runs; the
# combined -k 'canary' shows "23 passed, 48 deselected" because the
# -k filter applies to the WHOLE collection):
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

### Step 0.9 — S25-S33 invariants + cassette-dir + S33 Azurite-test presence

**Coverage note**: this Step 0.9 equals S33's Step 0.9 VERBATIM —
the public-API invariants (incl. the `_abfss_to_https` round-trip
assert + the `_FakeBackend` / `ADLSCostJournal` instantiation
asserting `j.path` / `j.exists() is False` / `j.read() is None`),
the S26 doc-stability check, the S27+S28 per-tier wiring smoke
(asserting all 8 `_TOTALS_FIELDS` slots populate via
`stage1_llm_usd == 0.04` / `stage1_embedding_usd == 0.01` / the
`math.isclose(totals.cost_usd, per_tier_sum + shard_sum)` invariant),
the S28 ShardResult check, the S28 cascade AST check, and the S29
K-b smoke-import check — PLUS the S33-Azurite/live-marker presence
check appended into the third helper script
(`check_s33_deliverables.py`, which supersets S33's cassette-only
`check_cassette_dirs.py`).

**First-run note**: the `/tmp/check_*.py` helper scripts in this
step use the file-tool staging pattern per the S32 asymmetric-hook
fold — the env hook blocks the inline `python -c` form when the
source string contains `ast.parse` (S28) or references the smoke
script's / Azure-credential secrets surface (S32/S33). Stage each
to a file — via the `cat >…<<'PYEOF'` heredocs shown below OR the
Write tool — and run via `.venv/bin/python <path>`. Run the S29
import check as its OWN Bash call (combining it with other
secrets-referencing `python -c` blocks trips the safety hook). If
any script fails to stage or execute, HALT before proceeding.

```
# Verify the S25-S30 public APIs unchanged, the 10 S31+S32 cassette
# dirs exist, AND the S33 Azurite-test deliverable is present.
# Re-run unconditionally at every S34 cold start.

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
    _journal_record_with_breakdown(journal=journal, shard_id='s1', stage=1, started_at='2026-06-01T00:00:00+00:00', domains_processed=10, components={'llm': 0.04, 'embedding': 0.01}, unattributed_cost_usd=0.0)
    _journal_record_with_breakdown(journal=journal, shard_id='s2', stage=2, started_at='2026-06-01T00:01:00+00:00', domains_processed=10, components={'fetch': 0.10, 'summarization': 0.20, 'classification': 0.30}, unattributed_cost_usd=0.0)
    _journal_record_with_breakdown(journal=journal, shard_id='s3', stage=3, started_at='2026-06-01T00:02:00+00:00', domains_processed=10, components={'evidence': 0.05, 'primary': 0.07, 'secondary': 0.0}, unattributed_cost_usd=0.03)
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
keys = [k.value for k in components_kw.value.keys if isinstance(k, ast.Constant)]
assert 'llm' in keys, f'Stage 1 components missing llm: {keys}'
assert 'embedding' in keys, f'Stage 1 components missing embedding: {keys}'
print('OK S28 cascade.py Stage 1 invoker AST structure intact (3 calls; stage=1 has llm + embedding)')
PYEOF
.venv/bin/python /tmp/check_s28_ast_phase0.py

# S29: K-b smoke script existence + import-loads cleanly.
# NOTE (S32 LESSONS): combining this import check with other
# secrets-referencing python -c blocks in ONE Bash call trips the
# safety hook ("interpreter accessing secrets file"). Run it as its
# own standalone script file / Bash call.
cat > /tmp/check_s29_smoke.py <<'PYEOF'
import importlib.util
from pathlib import Path
path = Path('scripts/smoke_test_adls_cost_journal.py')
assert path.exists(), f'S29 K-b script missing: {path}'
spec = importlib.util.spec_from_file_location('s29_smoke', str(path))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
assert hasattr(m, 'main') and hasattr(m, '_build_credential') and hasattr(m, '_delete_blob')
print('OK S29 K-b script intact (import OK; public surface intact)')
PYEOF
.venv/bin/python /tmp/check_s29_smoke.py

# S31 + S32 cassette dirs (10) + S33 Azurite-test deliverable + live
# marker. Supersets S33's cassette-only check_cassette_dirs.py by
# ALSO asserting the S33 deliverable presence + the live-marker
# registration (the appended-coverage delta over S33's Step 0.9).
cat > /tmp/check_s33_deliverables.py <<'PYEOF'
from pathlib import Path
root = Path('tests/fixtures/synthetic_crawls')
s31 = ('patagonia.com', 'deere.com', 'ford.com', 'pfizer.com', 'wholefoodsmarket.com')
s32 = ('propublica.org', 'apnews.com', 'c-span.org', 'eff.org', 'harvard.edu')
for d in s31 + s32:
    assert (root / d / 'cassette.yaml').exists(), f'missing cassette: {d}'
    assert (root / d / 'extract_hard_exclusions.json').exists(), f'missing sidecar: {d}'
azurite = Path('tests/classifier/pipeline/test_cost_journal_adls_azurite.py')
assert azurite.exists(), 'missing S33 Azurite test file'
text = azurite.read_text()
assert '@pytest.mark.live' in text, 'S33 Azurite test lost its live marker'
assert '--skipApiVersionCheck' in text, 'S33 fixture lost the baked version-skew flag'
pyproject = Path('pyproject.toml').read_text()
assert 'live:' in pyproject, 'live marker not registered in pyproject.toml'
print('OK S31+S32 cassettes (10) + S33 Azurite deliverable + live marker present')
PYEOF
.venv/bin/python /tmp/check_s33_deliverables.py
```

If any of 0.1-0.9 fail, HALT before doing any work.

**Optional Docker-gated check (NOT a halt condition)**: if Docker
is available locally, the operator MAY confirm the S33 live test
still self-reproduces:
```
.venv/bin/python -m pytest \
    tests/classifier/pipeline/test_cost_journal_adls_azurite.py -m live -q
# Expect: 1 passed (needs Docker + the Azurite image; SKIPS if absent).
# This is informational; Docker is NOT required for S34 unless the
# chosen scope is new ADLS live-test work. A skip here is fine and
# does NOT block S34.
```

---

## Required workspace reading (Session 34 first 10 minutes)

In this order:

1. **`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`** — full
   handoff state at S33 close. Lists scope candidates (A/D/E) with
   prerequisites. **Candidate K-a is CLOSED; Candidate E is
   EXHAUSTED at 30.** Note the explicit "S34 also opens with a
   near-empty warm-candidate queue" flag.

2. **`~/crawler-audit/SESSION_LOG.md`** Session 33 entry — what
   landed during Candidate K-a (1 commit `f1cdce8`). Documents the
   empty-warm-candidate-queue Phase 1, the concurrency carve-out,
   the baseline re-pin to 970 (Option 1), the version-skew finding
   + `--skipApiVersionCheck` fix, the unconditional-teardown
   validation, and the live-on-demand (not default-CI) framing.

3. **`~/crawler-audit/LESSONS.md`** — re-read LESSONS sections
   relevant to the chosen candidate:
   - **If Candidate A**: S29 prereq-audit fold + S22-S33
     "Plan-vs-reality at Phase 2" + S29 LOC additive-overhead-floor
     + AI/ML decision gating patterns.
   - **If Candidate D**: minimal LESSONS dependency; rely on
     operator labeling design.
   - **If a NEW live-service candidate** (e.g., K-a CI wiring):
     the S33 fold "A live-emulator fixture must tear down on
     setup-phase failure, and SDK-vs-emulator version skew is real"
     + S30 posture-validation fold + S24/S29/S30 public-API-only
     testing pattern.
   - **Only if the operator elects plan-amendment to reopen E**:
     the 3 S32 cassette folds AND the 3 S31 cassette folds
     (locate via `grep -n '^## .*(S3[12] folding)' LESSONS.md`).
   **Mandatory regardless of candidate**: the asymmetric reject-
   cleanup pattern (S32 folding) — informs the env-hook constraint
   on `rm -rf`/`find -delete` for any session.

4. **`~/crawler-audit/BARCADA_CRAWLER_REMEDIATION_PLAN.md`** —
   chosen-scope section per candidate:
   - **If Candidate D**: §11 Risk Register (Stage 2/3 labeling
     gates PR-D/E/F/G).
   - **If plan-amendment to reopen E**: §4 W7 (the "~20-30"
     ceiling is the line that must be raised before any cassette
     work).
   Plan is READ-ONLY by default; the only exception is the
   plan-amendment session shape, which has explicit operator
   authorization to edit.
   (Candidate A's plan anchor is `CLASSIFICATION_ADJACENT_PLAN.md`
   §Item 8 — listed at item 5.)

5. **`~/crawler-audit/CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8
   — only if Candidate A (barcada-drift) is chosen.

6. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   + **`tests/classifier/pipeline/test_cost_journal_adls_azurite.py`**
   + **`scripts/smoke_test_adls_cost_journal.py`** — only if a NEW
   ADLS live-test/CI-wiring candidate is chosen. READ-ONLY unless a
   Phase 2 gate authorizes a specific file.

---

## Phase 1 — Scope resolution (no code; pre-design-gate)

**FIRST**: surface the scope-availability note from the Scope
section above (A blocked / D operator-led / E exhausted / K-a
closed; NO self-contained optional candidate remains). S34 may have
no clearly-actionable engineering scope without operator action.
Then operator picks one candidate.

### Three invocation shapes (S34 continues the empty-warm-queue condition)

S33 was the first session to enter with an empty warm-candidate
queue and closed it by shipping K-a. S34 enters the SAME way but
without K-a as a fallback. The operator's scope decision can arrive
in one of three shapes; this prompt supports ALL THREE:

- **Decided before invocation (cleaner).** The operator names the
  candidate when commissioning S34. Phase 1 then CONFIRMS rather
  than elicits: skip the candidate-choice AskUserQuestion; still
  re-run the empirical prereq audit (for A: parquets + plist +
  AI/ML); proceed to that candidate's Phase 2 gate. If the named
  choice is "reopen E", see the plan-amendment shape below.

- **Decided at Phase 1 (more flexible).** S34 opens, Phase 0
  verifies state, Phase 1 surfaces the empty-queue condition
  explicitly and elicits the decision in-session via
  AskUserQuestion. **Context-budget caveat**: a Phase 1 that
  resolves to "plan amendment needed" or "no actionable scope" is
  a session that does NOT ship engineering — it spends budget on
  scope-resolution only. Surface that trade-off in the same
  AskUserQuestion so the operator chooses with eyes open; if the
  resolution is "nothing actionable", close at Phase 6 with the
  decision recorded (a legitimate no-ship outcome, not a failure).

- **Plan-amendment session shape (if the operator wants to reopen
  E).** Reopening Candidate E requires first raising the §4 W7
  "~20-30" ceiling in `BARCADA_CRAWLER_REMEDIATION_PLAN.md`, which
  is READ-ONLY by default. That plan edit is itself the Phase 2/3
  deliverable for such a session (explicit operator authorization
  to edit the plan; document in SESSION_LOG.md per the remediation-
  plan-read-only LESSONS). Only AFTER the ceiling is amended +
  committed may a subsequent recording sub-surface proceed under
  the proven S31/S32 mechanics. Do NOT record any cassette under
  the current 30 ceiling.

### Candidate A — `barcada-drift` (depends on AI/ML alignment + ≥2 parquets)

Per `CLASSIFICATION_ADJACENT_PLAN.md` §Item 8. Estimated ~300 LOC
logic + ~70-100 LOC overhead floor ≈ **~370-400 LOC delivered**.

**Prerequisites:**
- 2+ `canary_runs/*.parquet` files on operator's machine.
- AI/ML team responses on 4 §Item 8 decisions OR explicit
  operator-side placeholder choices with "AI/ML-to-tune" notes.

**HALT IF** the 4 AI/ML decisions are not pre-resolved AND
operator has not authorized explicit placeholder choices.

**Empirical prereq audit at S33 close** (carry-forward to S34
open): 0 `canary_runs` parquets on disk; no `barcada`/`canary`
plist in `~/Library/LaunchAgents/`; no AI/ML responses in
workspace.

Re-run these empirical checks at S34 Phase 1 BEFORE issuing the
candidate-choice AskUserQuestion (per S29 LESSONS pattern). If the
empirical state is unchanged, Candidate A remains blocked.

### Candidate D — Phase 4 PR-D operator-led labeling (operator territory)

Per plan §11 Risk Register. Stage 2 + Stage 3 labeling gates
PR-D/E/F/G. Operator-led; Claude Code's role limited to tooling.
W0-side unblocked at S27; still gated on operator-led labeling.

**Prerequisites:** Operator-scheduled labeling effort; Claude
Code's role limited to tooling around the labeling workflow.

### Candidate E — Cassette corpus expansion (EXHAUSTED)

The corpus reached the plan's **30 upper bound** at S32. **Not
available** without first amending the plan ceiling (raise §4 W7's
"~20-30" bound), made BEFORE any recording. Do NOT add cassettes
under the current plan. Recording mechanics remain proven
(S31+S32); the S32 LESSONS refine pool-sizing to be category-driven
(~1.1×N for low-WAF .edu/foundation/public-affairs media; ~2.5×N
for commerce/consumer).

### NEW candidate space (no warm carry-forward)

With K-a closed, any net-new scope the operator wants (e.g., wiring
K-a into a CI pipeline via `-m live` + Docker; extending the ADLS
live test to lease/SAS paths; a fresh tooling task) is a FRESH
candidate scoped at Phase 1/2 from first principles. Apply the same
hygiene: source-verify before option-set design; default new
external-service-backed tests to operator-smoke posture unless a
named carve-out justifies permanent/CI coverage (S30 LESSONS);
size new scripts with the ~70-100 LOC additive overhead floor.

### Sub-question 1.TAG — Tag at session close (pinned at Phase 1)

Independent of scope choice; resolved fully here at Phase 1.

- **Candidate A**: defer OR `barcada-drift-v0`.
- **Candidate D**: defer.
- **New W A.2 milestone work**: defer OR `workstream-a-week2-end`
  if the operator now considers W A.2 closed (it was OFFERED and
  DEFERRED at S33).

Phase 5 reads this resolution directly — no Phase 2 re-decision.

---

## Phase 2 — Design-gate elicitation (no code; AskUserQuestion)

Per chosen Phase 1 candidate. Source-verify at session-current HEAD
per the `[[verify-before-asking-discipline]]` AND the S22-S33
"Plan-vs-reality at Phase 2 source-verify" + S25 "source-verify
drives option-set design" LESSONS patterns BEFORE each
AskUserQuestion batch.

**HALT IF** any Phase 2 decision would require modifications to
`src/barcada_scraper/` beyond what was Phase-2-authorized OR to the
W4.1.5 driver beyond the S16/S27/S28 exceptions OR to any S19-S33
deliverable (including the S33 Azurite test / its fixture, or
re-recording/deleting any of the 30 existing cassettes) — surface
as a design-gate sub-question before patching.

### CRITICAL Phase 2 hygiene (4-option limit; empirical-vs-by-design; LOC additive floor; posture-validation)

Carry forward the S26/S28/S29/S30 hygiene notes verbatim: count
each Q-* option set (≤4 or tier/split); audit existing test pins
for by-design vs empirical; size new scripts with the ~70-100 LOC
additive overhead floor; default new external-service-backed tests
to operator-smoke (K-b) posture, not permanent CI, unless a named
carve-out justifies it (the S33 K-a carve-out was "concurrency
coverage").

### If Candidate A (barcada-drift)

Carry-forward from S22-S33 prompts (unchanged):
- Q-A.1 CLI namespace; Q-A.2 drift metric; Q-A.3 alert threshold;
  Q-A.4 input contract; Q-A.5 output shape; Q-A.6 test corpus.
(6 Q-* gates → split into 2-3 sequential AskUserQuestion calls;
both the 4-options-per-question and 4-questions-per-call caps
apply.)

### If Candidate D (Phase 4 PR-D tooling)

- **Q-D.1 Tooling shape**: batch validators / import scripts /
  hygiene tools. Operator-led design.

### If a NEW candidate (e.g., K-a CI wiring or ADLS extension)

Design the gates from first principles at session time; there is no
pre-baked template. Anchor on the S33 deliverable's shape (live
marker, skip-by-default, Docker-gated, self-reproducing fixture)
and the S30 posture note (carve-out required to escalate beyond
operator-smoke).

### Shared sub-questions (all candidates)

- **Q-SHARED.1 Commit shape**: per-module / per-sub-surface
  (S18-S33 default; Recommended) vs single bundled commit.

(Tag-at-close resolved at Phase 1 Sub-question 1.TAG.)

---

## Phase 3 — Implementation (per chosen commit shape, strict order)

### Non-interleaving rule (CRITICAL for bisectability)

If the chosen candidate has multiple sub-surfaces, complete each
fully before starting the next. Per S22-S33 precedent. If a
mid-sub-surface dependency emerges, HALT and surface as a
design-gate sub-question.

### Per-commit checkpoint protocol (single source of truth)

At EVERY Phase 3 commit boundary, run these 6 steps IN ORDER:

**1. Combined suite**

```
.venv/bin/python -m pytest \
    <the canonical 16-path invocation from Step 0.5> \
    <new S34 test paths if any> -q
# Candidate A: new barcada-drift test paths add to the headline.
# Candidate D: tooling tests add to the headline. A new live-marked
# test (e.g., K-a CI extension) stays OUT of the canonical headline
# unless a deliberate decision adds it (per the S33 Option-1 posture).
```

Expected: previous_baseline + N new tests, all passing. If
failing tests are NOT a deliberate consequence of the surface-
under-test → HALT.

**Phase 0 grep-for-same-shape-tests sanity** (S25 LESSONS): before
Phase 3, grep the test tree for same-shape tests that pin contracts
the chosen scope will modify. If found and not in the prompt's
explicit replacement allowlist, surface at Phase 0/2.

**2. Ruff sanity (touched files only) + mid-implementation format check**

```
.venv/bin/ruff check <touched paths>
.venv/bin/ruff format --check <touched paths>
```

**3. Verification table (build in chat per `[[double-check-before-commit]]`)**

Build a claim → reality → status table for every concrete claim in
the draft commit message. Any ✗ → fix the claim BEFORE staging.
Distinguish net-new tests from newly-in-invocation pre-existing
tests (S23 LESSONS). For exit-code claims use
`cmd > /tmp/out 2> /tmp/err; echo "Exit: $?"`. For new-file LOC
claims use `wc -l` (S29 LESSONS).

**4. `git status` check**

Only intended files staged; no surprise `eval_data/` or
unauthorized `src/` changes. Operator-side `eval_data/`
modifications stay unstaged.

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
Baseline bound at Phase 1: **970** (canonical 16-path). Hold it
consistent across all Phase 3 commits. A new live-marked test does
NOT raise the canonical headline (it is skip-by-default + absent
from the invocation) — verify it out-of-band per the S33 pattern.

---

## Phase 4 — Pre-push gate (whole-tree)

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # all files OK (count is whatever the tree currently holds; do not assert a fixed N)
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

HALT IF any gate red. Never use `--no-verify`.

### eval_data WIP halt protocol (per LESSONS)

validate_consistency runs against working-tree state. Operator-WIP
edits to `eval_data/*` can fail the gate even though no S34 commit
touches eval_data. When this fires:
1. Confirm the failing row is operator-WIP (`git diff eval_data/`),
   not committed HEAD (`git show HEAD:eval_data/...`).
2. Confirm the S34 commits do not touch eval_data
   (`git diff origin/main..HEAD -- eval_data/`).
3. Surface to operator with the exact row + reason + diff.
4. Two paths: (a) operator-fix in WT, re-run gate; (b) stash
   eval_data WIP, push, restore.
5. Do NOT auto-fix locked-artifact content.

S20+S22 precedent: operator chose (a). S21/S23-S33 did not need
this protocol at push (S28 saw a transient "1 error" that cleared
on identical re-run; S29-S33 did NOT reproduce it).

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
K-b execution at S30 plus the K-a Azurite test at S33. The
`workstream-a-week2-end` annotated tag was OFFERED at S33 and
DEFERRED; if S34 declares W A.2 closed it remains appropriate.

---

## Phase 6 — Workspace close-out

- Append Session 34 entry to `~/crawler-audit/SESSION_LOG.md`
  including a **Canonical S34-close baseline** block with the exact
  pytest invocation + verified count (per S22-S33 LESSONS).
  **If the fixture count changes (only possible via a plan-ceiling
  revision reopening E), record the new count with the exact
  variable names `cassette_count == N` / `exclusions_count == N`
  as the S35 Phase 0 Step 0.4 forward note.** Otherwise pin
  `cassette_count == 30` / `exclusions_count == 30` forward.
- Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md` for
  Session 35 — explicitly pin the S35 Phase 0 workspace anchor SHA
  per the S21-S33 post-audit pattern. After the close-out commit
  lands, expect **1-2 follow-up commits** pinning the actual SHA.
- Update `~/crawler-audit/LESSONS.md` with any new forward-
  applicable patterns.
- Workspace close-out: 1 primary commit + 1-2 follow-up commits.
  Push workspace after operator confirms.

Note: drafting the next-session prompt (`SESSION_35_PROMPT.md`) is
NOT a built-in Phase 6 step. Per S20→S33 precedent, prompt-drafting
is operator-commissioned between sessions. If the operator asks for
it explicitly at S34 close, draft it as a separate follow-up.

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

### A NEW candidate
0. Phase 1 carve-out / justification recorded in chat (if it ships
   a permanent or external-service-backed test).
1. Acceptance defined at the Phase 2 gate when the candidate is
   scoped.

### Shared (all candidates additionally satisfy)
- **S1.** Combined suite at session close: 970 baseline + N new
  tests, all passing. A new live-marked test stays out of the
  canonical headline (verified out-of-band).
- **S2.** Pre-push gate green (incl. eval_data WIP halt protocol).
- **S3.** Tag placed per 1.TAG OR explicit defer.
- **S4.** Regression-protection checklist held (see Out-of-scope).
  In particular: ALL S21-S33 deliverables stay at their SHAs;
  their public APIs unchanged; the 5 S31 + 5 S32 cassettes stay at
  `06d67c4` / `cfa0ec1`; the S33 Azurite test + live marker stay at
  `f1cdce8`; per-sub-suite counts stay green; CRAWLING_POLICY.md
  77 lines / 2519 bytes; the combined total stays at 970 (or grows)
  unless a Q-* authorizes a same-shape 1↔1 replacement.

---

## Out-of-scope (no exceptions without operator authorization)

Per the regression-protection checklist. **S33 added one new lock**
(the Azurite test file + the `live` marker at `f1cdce8`); otherwise
unchanged from S33 prompt.

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
all other S23 additions per S31/S32/S33 prompt.

**S24 deliverables:** the 3 worker_loop private helpers at
`48c324a`; the 5 retargeted test_stage2_pages_invoker_* fixtures;
`tests/orchestrator/test_worker_loop_persistence.py` at `aed7873`
(12); the 3 S24-added tests in test_robots_gate_integration.py.

**S25 deliverables:** `classifier/pipeline/cost_journal_adls.py`
at `835a531` (295 LOC; EMPIRICALLY validated at S30 via the K-b
smoke AND at S33 via the Azurite live test — but UNMODIFIED by
either; the S33 test injects the production `_AzureBlobBackend` via
the public `blob_backend=` seam);
`tests/classifier/pipeline/test_cost_journal_adls.py` at `835a531`
(19 tests + DummyBlobBackend; these 19 are the DEFAULT-run guard
for the module).

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

**S31 deliverables:**
`tests/fixtures/synthetic_crawls/{patagonia,deere,ford,pfizer,wholefoodsmarket}.com/`
at `06d67c4` — 10 fixture files across 5 domain dirs. Do NOT
re-record or delete without Phase 2 authorization.

**S32 deliverables:**
`tests/fixtures/synthetic_crawls/{propublica.org,apnews.com,c-span.org,eff.org,harvard.edu}/`
at `cfa0ec1` — 10 fixture files across 5 domain dirs (5 cassette.yaml
+ 5 extract_hard_exclusions.json; 2,739,094 bytes). Do NOT re-record
or delete without Phase 2 authorization. **Candidate E is EXHAUSTED
at 30; any new cassette requires a plan-ceiling revision first.**

**S33 deliverables (NEW LOCK):**
- `tests/classifier/pipeline/test_cost_journal_adls_azurite.py` at
  `f1cdce8` — 292 LOC; 1 `@pytest.mark.live` test + module-scoped
  Azurite fixture (unconditional try/finally teardown + idempotent
  self-healing pre-clean + skip-if-unavailable + the baked-in
  `--skipApiVersionCheck` flag). Do NOT modify without Phase 2
  authorization. **Live-on-demand, NOT default-CI.**
- The `live` marker registration in `pyproject.toml`
  `[tool.pytest.ini_options]` — load-bearing for `-m live`
  selection; do NOT remove.

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
edits across sessions expected and unstaged (Sessions 8-33
precedent); inter-session operator-side eval_data COMMITS tolerated
per "Workspace HEAD delta tolerance" (verify eval_data-only via
`git show --stat`). 2 operator-side stage1 TAGS
(`workstream-stage1-prestaged-flags-end`,
`workstream-stage1-step3-end`) point at eval_data-only commits.

**Production code:** `src/barcada_scraper/` — locked unless Phase 2
authorizes a specific module. S21-S25+S28 authorized (full list in
S31/S32/S33 prompt). S26+S27+S29+S30+S31+S32+S33 added no new src/
authorizations (S33 was test-only).

**Pipeline configs:** `configs/`.

**Phase 4 work:** PR-D/E/F/G W0-side unblocked since S27; still
gated on operator-led Stage 2/3 labeling.

---

## Verify-before-asking discipline (strict rule from S19-S33)

Per `[[double-check-before-commit]]`: **ALWAYS verify every
concrete claim in the commit message against actual source/output
BEFORE staging.** Fixture names, file counts, exit codes, line
counts, test counts, helper names, smoke outcomes, SHA prefixes,
regex matches, API signatures. No claims by pattern-completion.
Build a verification table (claim → reality → status) and reconcile
before "Confirm to commit?".

Specific to S34:
- Before claiming combined suite count, re-run pytest.
- Before claiming ruff/format clean, re-run ruff against touched
  files.
- Before claiming a SHA prefix, verify via
  `git show --no-patch --format=%h <ref>`.
- Before claiming a new-file LOC count, run `wc -l`.

Avoid bash pipe artifacts that mask Python exit codes:
`python_cmd 2>&1 | grep ... | tail` makes `$?` reflect tail's exit.
Use `> stdout.out 2> stderr.err; echo $?` or `${PIPESTATUS[0]}`.

LESSONS-folded discoveries from S22-S33 worth re-applying:
- Plan-vs-reality at Phase 2 (S22).
- Phase 2 source-verify drives option-set design (S25; S28/S29/S31/S33).
- Implicit-authorization HALT (S22-S33).
- Q-J.8 explicit allowlist may be incomplete; HALT-and-extend (S25).
- Local imports defeat module-attribute monkeypatch (S25).
- Test against public API surface only (S24; S29/S30/S33 extensions
  — S33 used the public `blob_backend=` seam to inject the
  production backend against Azurite).
- Source-verify line numbers per Phase 3 commit (S23).
- AskUserQuestion 4-option limit can silently truncate (S26).
- Empirical-vs-by-design distinction in test pins (S28).
- Phase 0 fixture-count commands need the Python rglob() pattern,
  NOT bare `find` (S28 post-close).
- Operator-driven script LOC: ~70-100 LOC additive overhead floor
  (S29).
- Empirical Phase 1 prerequisite check before scope-narrow (S29;
  S30/S31/S32/S33 re-validated — Candidate A unchanged).
- Operator-smoke posture (K-b) closes mock-vs-prod divergence in
  one execution; permanent CI (K-a) is optional and needs a named
  carve-out (S30); a permanent test shipped under Option 1 is
  live-on-demand, NOT default-CI (S33).
- A live-emulator fixture must tear down on setup-phase failure
  (try/finally wrapping the WHOLE setup, not post-yield); SDK-vs-
  emulator version skew is real — use the emulator-side
  compatibility flag when the SDK api_version is in locked code
  (S33).
- Reject-cassette cleanup is a two-step asymmetric pattern; `rm`/
  `find -delete` are env-hook-blocked — operator runs `! rm -rf`
  at close (S31; S32 confirmed; applies to any session).

---

## Commit hygiene (per LESSONS + S19-S33 additions)

- File-based commit messages at `/tmp/<id>-msg.txt`.
- Commit shape per Q-SHARED.1 (per-module default; single bundled
  commit only when the deliverable is genuinely one self-contained
  sub-surface, as K-a was at S33).
- "Confirm to commit?" before EVERY commit. Pair with verification
  table (always) and `git diff --staged` (per triggers).
- Commit body includes: action ref, scope summary, file touches,
  test count delta (with net-new vs newly-in-invocation distinction
  per S23 LESSONS), plan reference. NO `Co-Authored-By`.
- Pre-push gate must run green. Never use `--no-verify`.
- Pre-push vermin: `git ls-files '*.py' | xargs vermin
  --target=3.10` to filter venv-internal pytest 3.14 false-
  positives.
- Mid-implementation ruff format-check, not only pre-push.
- For S19-S33-test/fixture modifications: explicit Phase 2
  authorization required; document the modification scope in the
  commit body (Implicit-authorization HALT pattern).
- Workspace close-out (Phase 6) lands as its own commit, followed
  by 1-2 follow-up commits pinning the anchor SHA for S35.

---

## Context-window awareness

S33 ran Phase 0 → Phase 6 in a single context window with 1 commit
(Phase 0 verify + Docker/Azurite setup + 1 test file + 1 mid-impl
version-skew fix + close-out + 2 operator-feedback corrections),
comfortably within budget. S34 budget per scope:

- Candidate A: medium (~370-400 LOC delivered); only if unblocked.
- Candidate D: small; operator-led.
- A NEW candidate (e.g., K-a CI wiring): size at Phase 2.

Strategies:
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-service-backed test, default to the S33 fixture
  shape: unconditional try/finally teardown + idempotent
  self-healing pre-clean + skip-if-unavailable; expect an
  SDK-vs-emulator version-skew flag may be needed; keep the test
  off the canonical headline (live marker, skip-by-default) unless
  a deliberate decision adds it.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before the chosen S34 scope closes, finish
  the in-flight sub-surface, then close session and refill the
  transition template for Session 35.

---

## Reporting in chat at session close

After all Session 34 commits land + push + close-out per the
S13-33 pattern:

1. Commit SHA(s) of each S34 sub-surface.
2. Sub-surface(s) landed (per candidate).
3. Test count delta: 970 baseline → S34 close.
4. Driver suite count at S34 close (52/52 expected).
5. Files touched per sub-surface.
6. Tag dispositions (incl. any new tag per 1.TAG).
7. Per-tier cost-accounting wiring: CLOSED end-to-end since S28.
8. ADLSCostJournal status: K-b SHIP closed S29; K-b EXEC closed
   S30; K-a Azurite live-on-demand test closed S33 (NOT default-CI;
   CI wiring still un-done). Report S34's disposition if touched.
9. Any spend (LLM, infrastructure).
10. Verify-before-asking summary: source-verification findings.
11. Outstanding items for Session 35.
12. Tags state at S34 close.

Do not propose Phase 4 PR-D/E/F/G work unless Candidate D was
chosen and operator-led labeling is in flight.

---

## Carry-forward bakes (no amendment file needed)

All S33 close-out commits (`83e188a` primary + `a9692af` anchor-pin
+ `dc21714` framing correction) plus the S33 disposition have been
folded directly into this prompt — S34 does not need a separate
amendment file:

- **S33 close-out anchors** folded into Step 0.1 (workspace anchor
  = `dc21714` + this prompt-drafting commit; repo anchor `f1cdce8`
  with operator-eval_data-commit tolerance), Step 0.2 (13 tags,
  unchanged), Step 0.4 (cassettes/exclusions stay 30), Step 0.5
  (canonical 970), Step 0.9 (added the S33 Azurite-test +
  live-marker presence check + the baked-flag presence check).
- **1 NEW LESSONS section from S33** ("A live-emulator fixture must
  tear down on setup-phase failure, and SDK-vs-emulator version
  skew is real") referenced in the Verify-before-asking LESSONS
  list.
- **Candidate K-a CLOSED** (live-on-demand, not default-CI) folded
  into the carry-forward list + Scope section + Out-of-scope's S33
  deliverables (NEW LOCK).
- **Candidate E still EXHAUSTED** (30 reached) — requires a
  plan-ceiling revision first.

If new amendments arise pre-S34 open, walk them per the reviewer-
feedback hygiene pattern in this prompt's "Reviewer-feedback
hygiene" section.
