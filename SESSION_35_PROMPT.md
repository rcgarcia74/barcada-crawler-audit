# Session 35 prompt — scope picked at Phase 1
# (S34 closed a NEW candidate at repo eba6585 — the K-a CI wiring
#  PLUS the multi-writer concurrency race test the S33 carve-out
#  actually called for. That candidate is now CLOSED. S35 enters with
#  the SAME near-empty warm-candidate queue as S33/S34: A blocked /
#  D operator-led / E exhausted. No new carry-forward was introduced
#  by S34.)

**Drafted at Session 34 close (2026-06-02), operator-commissioned.**
Mirrors the S20/.../S33/S34 prompt structure. Scope-agnostic at
Phases 0/1; scope-specific design gates at Phase 2 per chosen
candidate. Strict 7-phase ordering with halt-on-mismatch preserved.

This prompt should be invoked from `~/crawler-audit/SESSION_35_PROMPT.md`.
Re-read it on session open.

---

## Scope

Engineering session. Repo HEAD at `eba6585`
(WA2.W8.adls-live-concurrency+ci; S34). Workspace HEAD at the S34
close-out chain `a6eef0f` (primary close-out) + `27bd60b` (anchor-pin)
+ this prompt-drafting commit (see Step 0.1). **Workstream 0 fully
closed at S27 via the `workstream-0-end` tag at `a1c5636`**.

Carry-forward candidates entering S35:

- **barcada-drift (Candidate A)** — deferred since S20; still needs
  4 AI/ML decisions per CLASSIFICATION_ADJACENT_PLAN.md §Item 8 AND
  2+ `canary_runs/*.parquet` files. **S34 re-confirmed empirically**
  that the launchd installer has NOT been run (no plist in
  `~/Library/LaunchAgents/`; 0 `canary_runs` parquets on disk; the
  parquets on disk are unrelated stage2/stage3 pipeline samples in
  `~/Downloads`). Same state as S29-S34 close. **Remains BLOCKED.**

- **Phase 4 PR-D tooling (Candidate D)** — operator-led labeling
  territory. W0-side unblocked since S27; still gated on
  operator-led Stage 2/3 labeling.

- **Cassette corpus expansion (Candidate E) — EXHAUSTED.** S32 grew
  the corpus to 30, the plan's stated upper bound (§4 W7
  "~20-30 representative domains"). **No further +N is available
  without first amending the plan ceiling** (a Phase 1/2 or
  plan-revision decision). Do NOT add cassettes under the current
  plan.

- **K-a CI wiring + concurrency coverage (S34 candidate) — CLOSED
  at S34** (`eba6585`). The live Azurite tests now run on-demand +
  nightly via `.github/workflows/live-integration.yml`, and the
  multi-writer concurrency race the S33 "concurrency coverage"
  carve-out named now exists
  (`test_cost_journal_adls_azurite_concurrency.py`). **NOT a
  carry-forward.** Any new ADLS live-test work (e.g., lease/SAS-token
  live paths, container-level ops) is a FRESH candidate.

**No new carry-forward introduced by S34.** The S34 deliverable was
a single commit (1 new test file + 1 new CI workflow); the canonical
970 test count is unchanged.

**Scope-availability note (IMPORTANT):** with A blocked, D
operator-led, E exhausted, and the S34 candidate now closed, S35 may
have **no clearly-actionable engineering scope** unless the operator
(a) unblocks A (run the launchd installer + resolve the 4 AI/ML
decisions or authorize placeholders + accumulate ≥2 parquets), (b)
begins D labeling, (c) authorizes a plan-ceiling revision to reopen
E, or (d) commissions a NEW candidate (e.g., live lease/SAS ADLS
coverage). There is NO self-contained optional candidate remaining.
Surface this at Phase 1 before the candidate-choice AskUserQuestion.

Operator chooses at Phase 1 which candidate Session 35 ships.
Each candidate has its own Phase 2 design-gate template.

**Sessions 13-34 precedent:** this session does NOT modify the
W4.1.5 driver orchestration at `tests/runners/fixture_cascade/`
(locked at `dd64963` for original files; `cascade.py` extended at
`a1c5636`/S27 + `9afde57`/S28; `test_cost_journal_wiring.py` added at
`a1c5636`/S27 + modified at `ae9e627`/S28). Does NOT modify
`expected.schema.json` v1.1 / `META_SCHEMA.md` v1.1. Does NOT modify
the committed `tests/fixtures/baseline-v0/` snapshot at `9e9a1fb`.
Does NOT modify the Session 19-34 deliverables. Does NOT modify the
S31 cassette deliverables at `06d67c4` or the S32 cassette
deliverables at `cfa0ec1` — never re-records or deletes any of the
30. Does NOT modify the **S33 deliverable** at `f1cdce8`
(`test_cost_journal_adls_azurite.py` + the `live` marker in
`pyproject.toml`). Does NOT modify the **S34 deliverables** at
`eba6585` (`test_cost_journal_adls_azurite_concurrency.py` +
`.github/workflows/live-integration.yml`).

Does NOT modify production code under `src/barcada_scraper/` UNLESS
Phase 2 design-gate explicitly authorizes a specific module. Of the
S35 candidates: Candidate A would add a NEW `barcada-drift` module
(new file, not a modification of locked code); Candidate D is
tooling-only.

Full regression-protection checklist in **Out-of-scope** at the end
of this prompt. Re-read it before any code lands.

---

## Reviewer-feedback hygiene (if this prompt is reviewed)

If an external reviewer (operator-invoked) flags items in this prompt
before Session 35 starts, walk each flagged item against on-disk
reality at the workspace HEAD and repo HEAD `eba6585`, BEFORE applying
any change. Per S19-S34 pattern:

- **OBSOLETE** items: SHAs already verified, claims already true.
  Skip with documented reasoning.
- **VALID-applies-now** items: bear on this session's scope. Apply.
- **VALID-applies-later** items: bear on deferred scope. Carry
  forward to the next prompt revision.
- **WRONG-PREMISE** items: assumes something not true. Skip with
  documented reasoning.

Empirical baseline: review remains the convergence mechanism; verify
each item against source before mutating the prompt.

---

## Halt protocol (when any phase's halt-condition fires)

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
- On operator guidance: (a) resume the failed step with the
  discrepancy resolved; (b) skip the phase per operator authorization
  (document in SESSION_LOG.md); (c) end early at Phase 6 close-out
  with the halt recorded.

Halt is not failure — it's the contract. **S34 anchor:** the Phase 3
HALT (carve-out named "concurrency coverage" but the underlying test
was sequential; production is multi-writer) is exactly the kind of
discrepancy this protocol exists to surface. It was resolved to
Path B and produced the race test. Apply the same discipline:
verify a carve-out / claim against the test BODY and the production
usage model before committing.

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

Run in order. Halt and surface to operator on any mismatch.

### Step 0.1 — Workspace + repo HEAD

```
git -C ~/crawler-audit rev-parse HEAD
# Expect: 27bd60b (S34 anchor-pin) OR this S35 prompt-drafting commit
# succeeding it OR a later commit if additional workspace doc edits /
# prompt revisions landed. If N commits ahead of 27bd60b, verify each
# via `git log --oneline 27bd60b..HEAD` against expected
# prompt-finalization / doc-edit patterns; surface the SHA delta and
# request authorization if anything is unexpected. (S20-S34 precedent:
# operator authorized continuation when 1-4 extra workspace commits
# were the strengthened prompts themselves.)

git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: eba6585 (S34 WA2.W8.adls-live-concurrency+ci).
#
# Tolerated delta: operator-side eval_data labeling commits between
# S34 close and S35 open (Sessions 8-34 precedent). Verify via
# `git show --stat <sha>` for every commit in eba6585..HEAD that each
# is strictly within eval_data/* (NO src/barcada_scraper/*, NO tests/*
# [INCLUDING the two Azurite test files], NO .github/* [INCLUDING
# live-integration.yml], NO scripts/*, NO docs/* touches); surface any
# non-eval_data delta for operator authorization before continuing.
```

### Step 0.2 — Tags (13 expected; unchanged from S30-S34 close)

```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort
# Expect 13 tags (UNCHANGED; S34 placed no tag per its 1.TAG = defer).
# Numbered so the count is unambiguous; NOTE there is NO week6-end —
# the workstream-0 week tags are 1/2/3/4-1-5/4/5/7 (7 week tags) PLUS
# workstream-0-end = 8 workstream-0-* tags total:
#    1. baseline-v0
#    2. pre-remediation-2026-05-19
#    3. workstream-0-end                          (placed S27 at a1c5636)
#    4. workstream-0-week1-end
#    5. workstream-0-week2-end
#    6. workstream-0-week3-end
#    7. workstream-0-week4-1-5-end
#    8. workstream-0-week4-end
#    9. workstream-0-week5-end
#   10. workstream-0-week7-end
#   11. workstream-a-week1-end
#   12. workstream-stage1-prestaged-flags-end     (operator-side; -> af6f1d4)
#   13. workstream-stage1-step3-end               (operator-side; -> d4f06b8)
# (8 workstream-0-* + baseline-v0 + pre-remediation + workstream-a-week1-end
#  + 2 operator-side stage1 tags = 13.)

git -C /Users/administrator/projects/barcada-scraper rev-list -n 1 workstream-0-end
# Expect: a1c5636… (UNCHANGED).

# NOTE: workstream-a-week2-end was OFFERED at S33 AND remained DEFERRED
# at S34 despite the CI wiring landing. If S35 declares W A.2 closed,
# that annotated tag remains appropriate (1.TAG).

# Tolerated delta: additional operator-side stage1-*/eval_data-* tags.
# For each new tag beyond the 13, verify the tagged commit is
# eval_data-only via `git show --stat <tag>`; if it points at any
# src/tests/.github/scripts/docs commit, HALT for authorization.
```

### Step 0.3 — Driver locked (with S16 + S27 + S28 exceptions)

```
cd /Users/administrator/projects/barcada-scraper
git diff dd64963..HEAD -- tests/runners/fixture_cascade/ \
    ':(exclude)tests/runners/fixture_cascade/test_fixture_fetcher.py' \
    ':(exclude)tests/runners/fixture_cascade/cascade.py' \
    ':(exclude)tests/runners/fixture_cascade/test_cost_journal_wiring.py'
# Expect: empty. The 3 excluded files have legitimate W5.X-prefix
# modifications (test_fixture_fetcher.py at 8d0fc0e/S16; cascade.py at
# a1c5636/S27 + 9afde57/S28; test_cost_journal_wiring.py at a1c5636/S27
# + ae9e627/S28). Any non-empty diff outside these 3 files = HALT.
# S29-S34 did NOT touch this surface.
```

### Step 0.4 — Fixture counts (use the Python rglob pattern, NOT bare find)

**UNCHANGED FROM S33/S34**: S34 shipped a test file + a CI workflow,
NOT a cassette. `cassette_count` and `exclusions_count` stay at **30**.

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

### Step 0.5 — Test-suite baseline (S35 canonical)

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
# Sub-totals (16 paths; ALL identical to S27-S34 close — BOTH Azurite
# tests are @pytest.mark.live + skip-by-default and are NOT in this
# invocation; the 33 synthetic_crawl tests are hermetic):
#   210 conformance + 52 driver + 99 baseline_v0 +
#    33 synthetic_crawl + 32 robots + 30 robots_gate +
#    30 robots_bypass_config + 43 cost_journal +
#    13 cost_journal_local + 19 cost_journal_adls +
#    35 robots_integration + 74 vmss_worker +
#   129 job_runner + 152 worker_loop +
#     7 robots_gate_integration + 12 worker_loop_persistence = 970
#
# Pinned in SESSION_LOG.md "Canonical S34-close baseline" block.
```

The sub-paths add up to 970. Any drift = halt. If the headline
mismatches, re-run each sub-path independently to localize.

**Narrower baselines**:
- 480 (S22 headline; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 944 (canonical 16-path minus 19 cost_journal_adls minus 7
  robots_gate_integration).

Whichever baseline is bound at Phase 1, hold it consistent across ALL
Phase 3 commits in S35. The cumulative-test-count gate never lets it
decrease except for a Q-*-authorized same-shape 1↔1 replacement.

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
# Expect: 3

.venv/bin/python -m tools.synthetic_crawl --help 2>&1 \
    | grep -oE '\b(record|replay)\b' | sort -u | wc -l
# Expect: 2
```

### Step 0.8 — Regression-protection sanity (any-candidate prereq)

```
.venv/bin/python -m pytest tests/baseline_v0/test_check.py \
    tests/baseline_v0/test_cli.py -k 'check' -q          # expect 30
.venv/bin/python -m pytest tests/baseline_v0/test_canary.py -q          # expect 17
.venv/bin/python -m pytest tests/baseline_v0/test_cli.py -k 'canary' -q # expect  6
.venv/bin/python -m pytest tests/synthetic_crawl/ -q                    # expect 33

.venv/bin/python -m pytest tests/scraper/test_robots.py -q                       # 32
.venv/bin/python -m pytest tests/scraper/test_robots_gate.py -q                  # 30
.venv/bin/python -m pytest tests/scraper/test_robots_bypass_config.py -q         # 30
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal.py -q     # 43
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal_local.py -q # 13
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal_adls.py -q  # 19
.venv/bin/python -m pytest tests/orchestrator/test_robots_integration.py -q        # 35
.venv/bin/python -m pytest tests/orchestrator/test_vmss_worker.py -q               # 74
.venv/bin/python -m pytest tests/orchestrator/test_job_runner.py -q                # 129
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop.py -q               # 152
.venv/bin/python -m pytest tests/orchestrator/test_robots_gate_integration.py -q   # 7
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop_persistence.py -q   # 12

.venv/bin/python -m pytest tests/runners/fixture_cascade/test_cost_journal_wiring.py -q  # 6
.venv/bin/python -m pytest tests/classifier/stage1/test_run_cascade.py tests/classifier/stage1/test_cost_tracker.py -q  # 32
```

### Step 0.9 — S25-S34 invariants + cassette-dir + S33/S34 live-test presence

**Coverage note**: equals S34's Step 0.9 plus a NEW check for the S34
deliverables. The env hook blocks inline `python -c` containing
`ast.parse` (S28) or Azure-credential-secrets references (S32/S33).

**PREFER the Write tool to stage the helper scripts, NOT the
`cat >…<<'PYEOF'` heredocs.** Empirically re-confirmed at S35
prompt-validation: the heredoc form for the (d-cont) AST script
tripped the safety hook ("Blocked: interpreter accessing secrets
file") even though the script touches no secrets — the hook matches
the heredoc command string, not the file. The heredoc blocks shown
below for (d-cont) and (e) are kept for reference, but if either
trips, re-create the SAME script via the Write tool and run it via
`.venv/bin/python <path>`. Run the S29 import check (e) as its OWN
Bash call (combining it with other `python -c` blocks also trips the
hook). If a script fails to STAGE, switch to the Write tool; if it
fails to EXECUTE (a real assertion fires), HALT.

```
# (a) S25-S30 public APIs unchanged (inline-safe; no ast.parse / secrets):
.venv/bin/python -c "
import inspect
from barcada_scraper.classifier.pipeline.cost_journal import (
    open_journal, JournalState, JournalAlreadyExistsError, CostJournal,
    update_with_retry, ShardRecord, OUTCOME_COMPLETED,
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
# S34 race test relies on these public symbols — assert they remain:
assert 'with_shard_appended' in dir(JournalState)
assert 'with_ceiling_raised' in dir(JournalState)
assert {'journal', 'mutator'} <= _params(update_with_retry)
assert {'shard_id','stage','outcome','cost_usd'} <= set(ShardRecord.__dataclass_fields__)
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
print('OK S24/S25 public APIs + S34 race-test public deps unchanged')
"

# (b) S26: CRAWLING_POLICY.md doc stability.
test "$(wc -l < docs/CRAWLING_POLICY.md)" = "77" && \
    test "$(wc -c < docs/CRAWLING_POLICY.md)" = "2519" || \
    { echo "HALT: CRAWLING_POLICY.md drifted"; exit 1; }
echo "OK docs/CRAWLING_POLICY.md unchanged (77 lines / 2519 bytes)"

# (c) S27+S28 per-tier wiring invariant smoke (all 8 slots populate).
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

# (d) S28 ShardResult split field presence.
.venv/bin/python -c "
from barcada_scraper.classifier.stage1.run import ShardResult
fields = set(ShardResult.__dataclass_fields__.keys())
assert 'llm_cost_usd' in fields and 'embedding_cost_usd' in fields and 'cost_usd' in fields
assert len(fields) == 14, f'{len(fields)}: {fields}'
print('OK S28 ShardResult 14 fields present')
"

# (d-cont.) S28 cascade.py Stage 1 invoker AST structure. Stage to a file
# and run via .venv/bin/python — the env hook blocks the inline
# `python -c` form when the source string contains 'ast.parse'.
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

# (e) S29 K-b smoke script existence + import-loads cleanly. Run this as
# its OWN standalone Bash call — combining it with other
# secrets-referencing `python -c` blocks trips the safety hook
# ("interpreter accessing secrets file"), per the S32/S33 LESSONS.
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

# (f) S31+S32 cassettes (10) + S33 Azurite deliverable + S34 deliverables.
#     Stage check_s35_deliverables.py via the Write tool and run it:
cat > /tmp/check_s35_deliverables.py <<'PYEOF'
import re
from pathlib import Path
root = Path('tests/fixtures/synthetic_crawls')
s31 = ('patagonia.com', 'deere.com', 'ford.com', 'pfizer.com', 'wholefoodsmarket.com')
s32 = ('propublica.org', 'apnews.com', 'c-span.org', 'eff.org', 'harvard.edu')
for d in s31 + s32:
    assert (root / d / 'cassette.yaml').exists(), f'missing cassette: {d}'
    assert (root / d / 'extract_hard_exclusions.json').exists(), f'missing sidecar: {d}'
# S33 primitive Azurite test + live marker.
prim = Path('tests/classifier/pipeline/test_cost_journal_adls_azurite.py')
assert prim.exists(), 'missing S33 Azurite test'
ptext = prim.read_text()
assert '@pytest.mark.live' in ptext and '--skipApiVersionCheck' in ptext
assert 'live:' in Path('pyproject.toml').read_text(), 'live marker not registered'
# S34 concurrency race test.
conc = Path('tests/classifier/pipeline/test_cost_journal_adls_azurite_concurrency.py')
assert conc.exists(), 'missing S34 concurrency race test'
ctext = conc.read_text()
assert '@pytest.mark.live' in ctext, 'S34 race test lost its live marker'
assert 'update_with_retry' in ctext and 'with_shard_appended' in ctext, 'S34 race test lost its CAS mutation'
assert '_BLOB_PORT = 10001' in ctext, 'S34 fixture lost its distinct port (would collide with S33 on 10000)'
assert '--skipApiVersionCheck' in ctext, 'S34 fixture lost the baked version-skew flag'
# S34 CI workflow.
wf = Path('.github/workflows/live-integration.yml')
assert wf.exists(), 'missing S34 live-integration CI workflow'
wtext = wf.read_text()
assert 'workflow_dispatch' in wtext, 'workflow lost its manual trigger'
assert re.search(r"cron: '0 6 \* \* \*'", wtext), 'workflow lost its nightly cron'
assert not re.search(r'^  push:', wtext, re.M), 'workflow MUST NOT be push-triggered (posture)'
assert 'pull_request' not in wtext, 'workflow MUST NOT be PR-triggered (posture)'
assert '-m live' in wtext and 'tests/classifier/pipeline/' in wtext, 'workflow lost its -m live dir selection'
print('OK S31+S32 cassettes (10) + S33 Azurite primitive + S34 race test + S34 CI workflow present (posture intact)')
PYEOF
.venv/bin/python /tmp/check_s35_deliverables.py
```

If any of 0.1-0.9 fail, HALT before doing any work.

**Optional Docker-gated check (NOT a halt condition)**: if Docker is
available locally, the operator MAY confirm BOTH live tests still pass
+ coexist:
```
.venv/bin/python -m pytest -m live tests/classifier/pipeline/ -q
# Expect: 2 passed, 209 deselected (needs Docker + the Azurite image;
# SKIPS cleanly if absent). Informational; Docker is NOT required for
# S35 unless the chosen scope is new ADLS live-test work.
```

---

## Required workspace reading (Session 35 first 10 minutes)

In this order:

1. **`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`** — full handoff
   state at S34 close. Lists scope candidates (A/D/E) with
   prerequisites. The S34 candidate is CLOSED; Candidate E is
   EXHAUSTED at 30. Note the explicit near-empty-warm-queue flag.

2. **`~/crawler-audit/SESSION_LOG.md`** Session 34 entry — the
   carve-out HALT → Path B narrative; the multi-writer finding; the
   negative-control teeth check; the CI workflow shape; the baseline
   re-pin (970 unchanged; +1 live test out-of-band).

3. **`~/crawler-audit/LESSONS.md`** — re-read sections relevant to the
   chosen candidate:
   - **Mandatory regardless of candidate**: the S34 fold "A carve-out
     claim must be verified against the test BODY, not its name/marker"
     + the asymmetric reject-cleanup pattern (S32 fold; informs the
     env-hook constraint on `rm -rf`/`find -delete`).
   - **If a NEW live-service candidate** (e.g., lease/SAS): the S33
     fold "A live-emulator fixture must tear down on setup-phase
     failure, and SDK-vs-emulator version skew is real" + S30
     posture-validation + S24/S29/S30/S33 public-API-only pattern.
     ALSO the S34 detail: a coexisting live fixture needs a DISTINCT
     port + container name (S33 holds 10000; S34 holds 10001).
   - **If Candidate A**: S29 prereq-audit fold + S22-S34
     "Plan-vs-reality at Phase 2" + S29 LOC additive-overhead-floor +
     AI/ML decision gating.
   - **Only if the operator elects plan-amendment to reopen E**: the
     3 S32 + 3 S31 cassette folds.

4. **`~/crawler-audit/BARCADA_CRAWLER_REMEDIATION_PLAN.md`** —
   chosen-scope section. READ-ONLY by default; the only exception is
   the plan-amendment session shape (explicit operator authorization
   to edit §4 W7's "~20-30" ceiling).

5. **`~/crawler-audit/CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 —
   only if Candidate A (barcada-drift) is chosen.

6. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   + the two live test files
   (`test_cost_journal_adls_azurite.py` +
   `test_cost_journal_adls_azurite_concurrency.py`)
   + `.github/workflows/live-integration.yml`
   + `scripts/smoke_test_adls_cost_journal.py` — only if a NEW
   ADLS live-test / CI candidate is chosen. READ-ONLY unless a Phase 2
   gate authorizes a specific file.

---

## Phase 1 — Scope resolution (no code; pre-design-gate)

**FIRST**: surface the scope-availability note (A blocked / D
operator-led / E exhausted / S34-candidate closed; NO self-contained
optional candidate remains). S35 may have no clearly-actionable
engineering scope without operator action. Then operator picks one.

### Three invocation shapes (S35 continues the empty-warm-queue condition)

- **Decided before invocation (cleaner).** Operator names the
  candidate when commissioning S35. Phase 1 CONFIRMS rather than
  elicits: skip the candidate-choice AskUserQuestion; still re-run the
  empirical prereq audit (for A: parquets + plist + AI/ML); proceed to
  that candidate's Phase 2 gate. If "reopen E", see plan-amendment.

- **Decided at Phase 1 (more flexible).** S35 opens, Phase 0 verifies,
  Phase 1 surfaces the empty-queue condition explicitly and elicits
  via AskUserQuestion. **Context-budget caveat**: a Phase 1 that
  resolves to "plan amendment needed" or "no actionable scope" is a
  no-ship session — surface that trade-off in the same AskUserQuestion.
  A "nothing actionable" close at Phase 6 with the decision recorded
  is a legitimate outcome, not a failure.

- **Plan-amendment session shape (reopen E).** Raise the §4 W7
  "~20-30" ceiling in BARCADA_CRAWLER_REMEDIATION_PLAN.md (READ-ONLY by
  default). That plan edit is itself the Phase 2/3 deliverable
  (explicit operator authorization; document in SESSION_LOG.md). Only
  AFTER the ceiling is amended + committed may a subsequent recording
  sub-surface proceed under the proven S31/S32 mechanics. Do NOT record
  any cassette under the current 30 ceiling.

### Candidate A — `barcada-drift` (AI/ML alignment + ≥2 parquets)

Per CLASSIFICATION_ADJACENT_PLAN.md §Item 8. Est ~300 LOC logic +
~70-100 LOC overhead ≈ **~370-400 LOC delivered**.

**Prerequisites:** 2+ `canary_runs/*.parquet` on operator's machine;
AI/ML responses on 4 §Item 8 decisions OR explicit operator-side
placeholder choices with "AI/ML-to-tune" notes.

**HALT IF** the 4 AI/ML decisions are not pre-resolved AND operator has
not authorized placeholders.

**Empirical prereq audit at S34 close** (carry-forward): 0 canary_runs
parquets; no barcada/canary/drift plist; no AI/ML responses. Re-run
these empirical checks at S35 Phase 1 BEFORE the candidate-choice
AskUserQuestion (S29 LESSONS). If unchanged, A remains blocked.

### Candidate D — Phase 4 PR-D operator-led labeling (operator territory)

Per plan §11 Risk Register. Stage 2 + Stage 3 labeling gates
PR-D/E/F/G. Operator-led; Claude Code's role limited to tooling.
W0-side unblocked at S27; still gated on operator-led labeling.

### Candidate E — Cassette corpus expansion (EXHAUSTED)

Reached the plan's **30 upper bound** at S32. **Not available** without
first amending the §4 W7 ceiling (made BEFORE any recording). Do NOT
add cassettes under the current plan. Mechanics proven (S31+S32).

### NEW candidate space (no warm carry-forward)

With the S34 candidate closed, any net-new scope (e.g., live lease/SAS
ADLS paths; container-level live coverage; a fresh tooling task) is a
FRESH candidate scoped at Phase 1/2 from first principles. Apply the
same hygiene: source-verify before option-set design; **verify any
carve-out against the actual test body it implies (S34 LESSONS)**;
default new external-service-backed tests to operator-smoke posture
unless a named carve-out justifies permanent/CI coverage (S30); if a
new live fixture must coexist with the S33/S34 fixtures, give it a
DISTINCT port + container name (S33=10000, S34=10001); size new scripts
with the ~70-100 LOC additive overhead floor.

### Sub-question 1.TAG — Tag at session close (pinned at Phase 1)

Independent of scope choice; resolved fully here at Phase 1.

- **Candidate A**: defer OR `barcada-drift-v0`.
- **Candidate D**: defer.
- **New W A.2-completing work** (e.g., a live-coverage extension): defer
  OR `workstream-a-week2-end` if the operator now considers W A.2 closed
  (OFFERED at S33, DEFERRED at S33 AND S34).

Phase 5 reads this resolution directly — no Phase 2 re-decision.

---

## Phase 2 — Design-gate elicitation (no code; AskUserQuestion)

Per chosen Phase 1 candidate. Source-verify at session-current HEAD per
the `[[verify-before-asking-discipline]]` AND the S22-S34
"Plan-vs-reality at Phase 2" + S25 "source-verify drives option-set
design" patterns BEFORE each AskUserQuestion batch.

**HALT IF** any Phase 2 decision would require modifications to
`src/barcada_scraper/` beyond what was Phase-2-authorized OR to the
W4.1.5 driver beyond the S16/S27/S28 exceptions OR to any S19-S34
deliverable (including the S33 Azurite test, the S34 concurrency test,
the S34 CI workflow, or re-recording/deleting any of the 30 cassettes)
— surface as a design-gate sub-question before patching.

### CRITICAL Phase 2 hygiene

Carry forward S26/S28/S29/S30/S34 hygiene verbatim: count each Q-*
option set (≤4 or tier/split); audit existing test pins for
by-design vs empirical; size new scripts with the ~70-100 LOC additive
overhead floor; default new external-service-backed tests to
operator-smoke posture unless a named carve-out justifies it; **and
when a carve-out names a behavior (concurrency, idempotency, failover),
point it at the specific test body that exercises it — or narrow the
wording to what the body actually does (S34 fold).**

### If Candidate A (barcada-drift)

Carry-forward (unchanged): Q-A.1 CLI namespace; Q-A.2 drift metric;
Q-A.3 alert threshold; Q-A.4 input contract; Q-A.5 output shape;
Q-A.6 test corpus. (Split into 2-3 sequential AskUserQuestion calls;
both the 4-options-per-question and 4-questions-per-call caps apply.)

### If Candidate D (Phase 4 PR-D tooling)

- **Q-D.1 Tooling shape**: batch validators / import scripts / hygiene
  tools. Operator-led design.

### If a NEW candidate (e.g., lease/SAS live coverage)

Design the gates from first principles at session time. Anchor on the
S33/S34 live-test shape (live marker, skip-by-default, Docker-gated,
self-reproducing fixture, distinct port if coexisting) and the S30
posture note (carve-out required to escalate beyond operator-smoke).
For any new live test, decide explicitly whether it joins the CI
workflow's `-m live` dir selection (it will be picked up automatically
if placed under `tests/classifier/pipeline/`) and keep the
skip-fail guard meaningful.

### Shared sub-questions (all candidates)

- **Q-SHARED.1 Commit shape**: per-module / per-sub-surface (S18-S34
  default; Recommended) vs single bundled commit (only when genuinely
  one self-contained sub-surface).

(Tag-at-close resolved at Phase 1 Sub-question 1.TAG.)

---

## Phase 3 — Implementation (per chosen commit shape, strict order)

### Non-interleaving rule (CRITICAL for bisectability)

If the chosen candidate has multiple sub-surfaces, complete each fully
before starting the next. Per S22-S34 precedent. If a mid-sub-surface
dependency emerges, HALT and surface as a design-gate sub-question.

### Per-commit checkpoint protocol (single source of truth)

At EVERY Phase 3 commit boundary, run these 6 steps IN ORDER:

**1. Combined suite**

```
.venv/bin/python -m pytest \
    <the canonical 16-path invocation from Step 0.5> \
    <new S35 test paths if any> -q
# A new @pytest.mark.live test stays OUT of the canonical headline
# unless a deliberate decision adds it (S33/S34 Option-1 posture). If
# it is placed under tests/classifier/pipeline/, it is auto-picked-up
# by the CI workflow's `-m live` selection but NOT by the canonical
# 16-path (which lists files explicitly).
```

Expected: previous_baseline + N new tests, all passing. If failing
tests are NOT a deliberate consequence of the surface-under-test →
HALT.

**Phase 0 grep-for-same-shape-tests sanity** (S25 LESSONS): before
Phase 3, grep the test tree for same-shape tests that pin contracts
the chosen scope will modify. If found and not in the prompt's explicit
replacement allowlist, surface at Phase 0/2.

**2. Ruff sanity (touched files only) + mid-implementation format check**

```
.venv/bin/ruff check <touched paths>
.venv/bin/ruff format --check <touched paths>
# (ruff is Python-only; a YAML/workflow-only change has no ruff-touched
# files — note that explicitly rather than asserting a clean ruff run
# on a non-Python file, per S34.)
```

**3. Verification table (build in chat per `[[double-check-before-commit]]`)**

Build a claim → reality → status table for every concrete claim in the
draft commit message. Any ✗ → fix the claim BEFORE staging. Distinguish
net-new tests from newly-in-invocation pre-existing tests (S23). For
exit-code claims use `cmd > /tmp/out 2> /tmp/err; echo "Exit: $?"`. For
new-file LOC claims use `wc -l` (S29). **For any live/concurrency test,
include a teeth check** (e.g., a negative control) in the table, not
just "it passes" (S34).

**4. `git status` check**

Only intended files staged; no surprise `eval_data/` or unauthorized
`src/` changes. Operator-side `eval_data/` modifications stay unstaged.

**5. "Confirm to commit?" presented to operator**

Include: verification table; commit message file location
(`/tmp/<id>-msg.txt`); file list to stage (M / A / D).

**6. After operator confirms**

Stage + commit + verify the new SHA (`git log --oneline -1`) + verify
combined suite still passes on the new HEAD.

### Cumulative test-count gate

Track combined-suite passing count at each commit boundary. The count
NEVER decreases between checkpoints. Authorized decreases ONLY for a
Q-*-authorized same-shape 1↔1 replacement (cite the authorization +
name replaced + replacement in the commit body). Baseline bound at
Phase 1: **970** (canonical 16-path). A new live-marked test does NOT
raise the canonical headline — verify it out-of-band per the S33/S34
pattern (`pytest -m live tests/classifier/pipeline/`).

---

## Phase 4 — Pre-push gate (whole-tree)

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # all files OK (do NOT assert a fixed N)
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

HALT IF any gate red. Never use `--no-verify`.

### eval_data WIP halt protocol (per LESSONS)

validate_consistency runs against working-tree state. Operator-WIP
edits to `eval_data/*` can fail the gate even though no S35 commit
touches eval_data. When this fires:
1. Confirm the failing row is operator-WIP (`git diff eval_data/`),
   not committed HEAD (`git show HEAD:eval_data/...`).
2. Confirm the S35 commits do not touch eval_data
   (`git diff origin/main..HEAD -- eval_data/`).
3. Surface to operator with the exact row + reason + diff.
4. Two paths: (a) operator-fix in WT, re-run gate; (b) stash eval_data
   WIP, push, restore.
5. Do NOT auto-fix locked-artifact content.

S20+S22 precedent: operator chose (a). S21/S23-S34 did not need this
protocol at push.

---

## Phase 5 — Push + tag

- Push to `origin/main` after operator confirms.
- Tag per Phase 1 Sub-question 1.TAG decision (or defer).

If a workstream-end tag is placed: include an annotated message naming
every sub-surface commit + mapping to plan bullets + listing
deferrals (mirror `workstream-a-week1-end` / `workstream-0-end`).

Note: workstream-0-end placed at S27. W A.1 closed at S22's
`workstream-a-week1-end`; W A.2 is the orchestrator-side robots work
(S23-S25) + the K-b script (S29) + K-b execution (S30) + the K-a
Azurite test (S33) + the K-a CI wiring + concurrency race test (S34).
The `workstream-a-week2-end` tag was OFFERED at S33 and DEFERRED at
S33 AND S34; if S35 declares W A.2 closed it remains appropriate.

---

## Phase 6 — Workspace close-out

- Append Session 35 entry to `~/crawler-audit/SESSION_LOG.md` including
  a **Canonical S35-close baseline** block with the exact pytest
  invocation + verified count (per S22-S34 LESSONS). **If the fixture
  count changes (only via a plan-ceiling revision reopening E), record
  the new count with the exact variable names `cassette_count == N` /
  `exclusions_count == N` as the S36 Phase 0 Step 0.4 forward note.**
  Otherwise pin `cassette_count == 30` / `exclusions_count == 30`.
- Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md` for Session
  36 — explicitly pin the S36 Phase 0 workspace anchor SHA per the
  S21-S34 post-audit pattern. After the close-out commit lands, expect
  **1-2 follow-up commits** pinning the actual SHA.
- Update `~/crawler-audit/LESSONS.md` with any new forward-applicable
  patterns.
- Workspace close-out: 1 primary commit + 1-2 follow-up commits. Push
  workspace after operator confirms.

Note: drafting the next-session prompt (`SESSION_36_PROMPT.md`) is NOT
a built-in Phase 6 step. Per S20→S34 precedent, prompt-drafting is
operator-commissioned between sessions. If the operator asks for it
explicitly at S35 close, draft it as a separate follow-up.

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
0. Phase 1 carve-out / justification recorded in chat (if it ships a
   permanent or external-service-backed test), **with the carve-out
   matched to the actual test body (S34)**.
1. Acceptance defined at the Phase 2 gate when the candidate is scoped.

### Shared (all candidates additionally satisfy)
- **S1.** Combined suite at session close: 970 baseline + N new tests,
  all passing. A new live-marked test stays out of the canonical
  headline (verified out-of-band; `pytest -m live tests/classifier/pipeline/`).
- **S2.** Pre-push gate green (incl. eval_data WIP halt protocol).
- **S3.** Tag placed per 1.TAG OR explicit defer.
- **S4.** Regression-protection checklist held (see Out-of-scope). In
  particular: ALL S21-S34 deliverables stay at their SHAs; their public
  APIs unchanged; the 5 S31 + 5 S32 cassettes stay at `06d67c4` /
  `cfa0ec1`; the S33 Azurite test + live marker stay at `f1cdce8`; the
  S34 concurrency test + CI workflow stay at `eba6585` (and the
  workflow stays OFF push/PR); per-sub-suite counts stay green;
  CRAWLING_POLICY.md 77 lines / 2519 bytes; the combined total stays at
  970 (or grows) unless a Q-* authorizes a same-shape 1↔1 replacement.

---

## Out-of-scope (no exceptions without operator authorization)

Per the regression-protection checklist. **S34 added two new locks**
(the concurrency race test + the CI workflow at `eba6585`); otherwise
unchanged from the S34 prompt.

**S19 deliverables:** `tools/baseline_v0/check.py`;
`tests/baseline_v0/test_check.py` (24 tests); 6 check-dispatch tests in
`tests/baseline_v0/test_cli.py`.

**S20 deliverables:** `tools/synthetic_crawl/` package (4 files);
`tools/baseline_v0/canary.py`; `canary-run` subparser;
`tests/synthetic_crawl/` (33); `tests/baseline_v0/test_canary.py` (17);
6 canary-dispatch tests; the original 20 cassettes + 20 sidecars at
`7f11879`; `scripts/launchd/` (5 files); `pyproject.toml` vcrpy>=8.1
dev entry; `.gitignore` canary_runs/.

**S21 deliverables:** `scraper/robots.py` (282 LOC; `34a59b6`);
`tests/scraper/test_robots.py` (32).

**S22 deliverables:** `scraper/robots_gate.py` (`ba87e7e`);
`tests/scraper/test_robots_gate.py` (30); `scraper/robots_bypass_config.py`
(`381ee89`); `tests/scraper/test_robots_bypass_config.py` (30); the S22
`cost_journal.py` additions at `1d9404e`; the S22 `test_cost_journal.py`
additions (14 new + 1 updated), EXCEPT the S25 Q-J.8-extension
replacement at `835a531`.

**S23 deliverables:** `orchestrator/robots_integration.py` (`279bb77`);
`tests/orchestrator/test_robots_integration.py` (35); `vmss_worker.py`
additions (`5eeaac7`); `job_runner.py` additions (`872527e`);
`scripts/vmss/cloud_init.template.yaml`.

**S24 deliverables:** the 3 worker_loop private helpers at `48c324a`;
the 5 retargeted test_stage2_pages_invoker_* fixtures;
`tests/orchestrator/test_worker_loop_persistence.py` at `aed7873` (12);
the 3 S24-added tests in test_robots_gate_integration.py.

**S25 deliverables:** `cost_journal_adls.py` at `835a531` (295 LOC;
EMPIRICALLY validated at S30 [K-b smoke], S33 [Azurite primitive], S34
[Azurite concurrency] — UNMODIFIED by any; the live tests inject the
production `_AzureBlobBackend` via the public `blob_backend=` seam);
`tests/classifier/pipeline/test_cost_journal_adls.py` at `835a531` (19
tests + DummyBlobBackend; the DEFAULT-run guard for the module).

**S26 deliverables:** `docs/CRAWLING_POLICY.md` at `2314f5e` (77 lines
/ 2519 bytes).

**S27 deliverables:** `cascade.py` per-tier wiring at `a1c5636`
(extended S28); `test_cost_journal_wiring.py` at `a1c5636` (modified
S28).

**S28 deliverables:** `classifier/stage1/run.py` at `776d203`
(ShardResult +2 fields); `test_run_cascade.py` at `776d203` (+1 test);
`cascade.py` Stage 1 invoker switch at `9afde57`;
`test_cost_journal_wiring.py` 1↔1 replacement at `ae9e627`.

**S29 deliverables:** `scripts/smoke_test_adls_cost_journal.py` at
`75a3937` (220 LOC).

**S30 deliverables:** No repo code changes (K-b-exec only); workspace
docs at `9d4691e` + `67a9c40`.

**S31 deliverables:**
`tests/fixtures/synthetic_crawls/{patagonia,deere,ford,pfizer,wholefoodsmarket}.com/`
at `06d67c4` — 10 files across 5 dirs. Do NOT re-record/delete without
Phase 2 authorization.

**S32 deliverables:**
`tests/fixtures/synthetic_crawls/{propublica.org,apnews.com,c-span.org,eff.org,harvard.edu}/`
at `cfa0ec1` — 10 files across 5 dirs. **Candidate E EXHAUSTED at 30;
any new cassette requires a plan-ceiling revision first.**

**S33 deliverables:**
- `tests/classifier/pipeline/test_cost_journal_adls_azurite.py` at
  `f1cdce8` (292 LOC; 1 `@pytest.mark.live` test + module-scoped
  Azurite fixture on port 10000 / container `barcada-azurite-katest`;
  baked `--skipApiVersionCheck`). Live-on-demand, NOT default-CI.
- The `live` marker registration in `pyproject.toml`
  `[tool.pytest.ini_options]` — load-bearing for `-m live`; do NOT
  remove.

**S34 deliverables (NEW LOCK):**
- `tests/classifier/pipeline/test_cost_journal_adls_azurite_concurrency.py`
  at `eba6585` — 337 LOC; 1 `@pytest.mark.live` multi-writer race test
  (12 threads, `update_with_retry` + `with_shard_appended`,
  no-lost-update assertion) + its OWN module-scoped Azurite fixture on
  a DISTINCT port 10000→**10001** / container `barcada-azurite-racetest`
  (so it coexists with the S33 fixture under one `-m live` run). Do NOT
  modify without Phase 2 authorization.
- `.github/workflows/live-integration.yml` at `eba6585` — CI workflow.
  `workflow_dispatch` + nightly `schedule` (cron `0 6 * * *`); **MUST
  NOT** be push/PR-triggered (live-on-demand posture per the S33
  framing). Runs `pytest -m live tests/classifier/pipeline/` with a
  skip-robust count-agnostic guard. Do NOT weaken the guard or the
  trigger posture without a deliberate Phase 2 decision.

**W4.1.5 driver orchestration:** `tests/runners/fixture_cascade/`
(except via W5.X-prefix commit — only S16/S27/S28 opened it).

**Baseline-v0 ground truth:** the committed `tests/fixtures/baseline-v0/`
snapshot at `9e9a1fb` (1213 files).

**Existing W6 sub-surface (S18):** `tools/baseline_v0/generate.py`,
`determinism.py`, the existing `generate` subparser.

**Schemas + plans (locked):** `expected.schema.json` v1.1;
`META_SCHEMA.md` v1.1; `meta.schema.json` v1.0; `stage1.schema.json`
v1.0; all 13 workstream tags at their placed SHAs;
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` (READ-ONLY);
`CLASSIFICATION_ADJACENT_PLAN.md` (UPDATED only when AI/ML decisions
land); `RECONCILIATION_2026-05-21.md`; `docs/phase4_implementation_plan.md`.

**Operator-owned territory:** all of `eval_data/` — per-row WIP edits
expected and unstaged (Sessions 8-34); inter-session operator-side
eval_data COMMITS tolerated per "Workspace HEAD delta tolerance" (verify
eval_data-only via `git show --stat`). 2 operator-side stage1 TAGS point
at eval_data-only commits.

**Production code:** `src/barcada_scraper/` — locked unless Phase 2
authorizes a specific module. S21-S25+S28 authorized. S26+S27+S29+S30+
S31+S32+S33+S34 added no new src/ authorizations (S34 was test + CI
only).

**Pipeline configs:** `configs/`.

**CI workflows:** `.github/workflows/` — `python-package.yml` and
`build-and-push-image.yml` are pre-existing; `live-integration.yml` is
the S34 lock. New workflows require a Phase 2 design-gate.

**Phase 4 work:** PR-D/E/F/G W0-side unblocked since S27; still gated
on operator-led Stage 2/3 labeling.

---

## Verify-before-asking discipline (strict rule from S19-S34)

Per `[[double-check-before-commit]]`: **ALWAYS verify every concrete
claim in the commit message against actual source/output BEFORE
staging.** Fixture names, file counts, exit codes, line counts, test
counts, helper names, smoke outcomes, SHA prefixes, regex matches, API
signatures, **and that a carve-out's named behavior is actually
exercised by the test body (S34)**. No claims by pattern-completion.
Build a verification table (claim → reality → status) and reconcile
before "Confirm to commit?".

Specific to S35:
- Before claiming combined suite count, re-run pytest.
- Before claiming ruff/format clean, re-run ruff against touched files
  (note when a change is YAML-only with no ruff-touched files).
- Before claiming a SHA prefix, verify via
  `git show --no-patch --format=%h <ref>`.
- Before claiming a new-file LOC count, run `wc -l`.
- For any concurrency/live test, demonstrate teeth (negative control),
  not just a green run.

Avoid bash pipe artifacts that mask Python exit codes:
`python_cmd 2>&1 | grep ... | tail` makes `$?` reflect tail's exit. Use
`> stdout.out 2> stderr.err; echo $?` or `${PIPESTATUS[0]}`.

LESSONS-folded discoveries worth re-applying:
- **A carve-out claim must be verified against the test BODY, not its
  name/marker; re-verify when CI-wiring an existing test (S34).**
- A live-emulator fixture must tear down on setup-phase failure
  (try/finally wrapping the WHOLE setup); SDK-vs-emulator version skew
  is real (use the emulator-side compatibility flag) (S33). A coexisting
  live fixture needs a DISTINCT port + container name (S34).
- Operator-smoke posture (K-b) vs permanent CI (needs a named carve-out)
  (S30); a permanent test shipped under Option 1 is live-on-demand, NOT
  default-CI (S33); wiring it to a workflow keeps it off push/PR unless
  deliberately escalated (S34).
- Plan-vs-reality at Phase 2 (S22); source-verify drives option-set
  design (S25; S28-S34).
- Test against public API surface only (S24; S29/S30/S33/S34).
- AskUserQuestion 4-option limit can silently truncate (S26).
- Empirical-vs-by-design distinction in test pins (S28).
- Phase 0 fixture-count commands need the Python rglob() pattern, NOT
  bare `find` (S28 post-close).
- Markdown-rendered shell commands may carry NBSP in whitespace-
  sensitive args; stage scripts to a file via the Write tool and
  byte-scan when exactness matters (re-confirmed S34: inline grep with
  quoted spaces silently failed; file-staged scripts + Python byte-scan
  worked).
- Operator-driven script LOC: ~70-100 LOC additive overhead floor (S29).
- Empirical Phase 1 prerequisite check before scope-narrow (S29; S30-S34
  re-validated — Candidate A unchanged).
- Reject-cassette cleanup is a two-step asymmetric pattern; `rm`/`find
  -delete` are env-hook-blocked — operator runs `! rm -rf` at close
  (S31; S32 confirmed; applies to any session).

---

## Commit hygiene (per LESSONS + S19-S34 additions)

- File-based commit messages at `/tmp/<id>-msg.txt`.
- Commit shape per Q-SHARED.1 (per-module default; single bundled commit
  only when the deliverable is genuinely one self-contained sub-surface,
  as the S34 race-test+CI-wiring pair was — coupled by intent).
- "Confirm to commit?" before EVERY commit. Pair with verification table
  (always) and `git diff --staged` (per triggers).
- Commit body includes: action ref, scope summary, file touches, test
  count delta (net-new vs newly-in-invocation per S23), plan reference,
  and — for any carve-out — the test-body match (S34). NO `Co-Authored-By`.
- Pre-push gate must run green. Never use `--no-verify`.
- Pre-push vermin: `git ls-files '*.py' | xargs vermin --target=3.10` to
  filter venv-internal false-positives.
- Mid-implementation ruff format-check, not only pre-push.
- For S19-S34-test/fixture/workflow modifications: explicit Phase 2
  authorization required; document the scope in the commit body.
- Workspace close-out (Phase 6) lands as its own commit, followed by
  1-2 follow-up commits pinning the anchor SHA for S36.

---

## Context-window awareness

S34 ran Phase 0 → Phase 6 in a single context window with 1 repo commit
(Phase 0 verify + Phase 1 scope + Phase 2 gates + a Phase 3 HALT
resolved to Path B [race test + negative control + CI workflow] +
close-out), comfortably within budget. S35 budget per scope:

- Candidate A: medium (~370-400 LOC); only if unblocked.
- Candidate D: small; operator-led.
- A NEW candidate (e.g., lease/SAS live coverage): size at Phase 2.

Strategies:
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-service-backed test, default to the S33/S34 fixture
  shape: unconditional try/finally teardown + idempotent self-healing
  pre-clean + skip-if-unavailable; expect an SDK-vs-emulator
  version-skew flag may be needed; use a DISTINCT port + container name
  if coexisting with the S33 (10000) / S34 (10001) fixtures; keep the
  test off the canonical headline (live marker, skip-by-default) unless
  a deliberate decision adds it.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before the chosen S35 scope closes, finish the
  in-flight sub-surface, then close session and refill the transition
  template for Session 36.

---

## Reporting in chat at session close

After all Session 35 commits land + push + close-out per the S13-34
pattern:

1. Commit SHA(s) of each S35 sub-surface.
2. Sub-surface(s) landed (per candidate).
3. Test count delta: 970 baseline → S35 close.
4. Driver suite count at S35 close (52/52 expected).
5. Files touched per sub-surface.
6. Tag dispositions (incl. any new tag per 1.TAG).
7. Per-tier cost-accounting wiring: CLOSED end-to-end since S28.
8. ADLSCostJournal status: K-b SHIP S29; K-b EXEC S30; K-a Azurite
   primitive S33; K-a CI wiring + multi-writer concurrency S34. Report
   S35's disposition if touched.
9. Any spend (LLM, infrastructure).
10. Verify-before-asking summary: source-verification findings.
11. Outstanding items for Session 36.
12. Tags state at S35 close.

Do not propose Phase 4 PR-D/E/F/G work unless Candidate D was chosen
and operator-led labeling is in flight.

---

## Carry-forward bakes (no amendment file needed)

All S34 close-out commits (`a6eef0f` primary + `27bd60b` anchor-pin)
plus the S34 disposition have been folded directly into this prompt —
S35 does not need a separate amendment file:

- **S34 close-out anchors** folded into Step 0.1 (workspace anchor =
  `27bd60b` + this prompt-drafting commit; repo anchor `eba6585` with
  operator-eval_data-commit tolerance), Step 0.2 (13 tags, unchanged),
  Step 0.4 (cassettes/exclusions stay 30), Step 0.5 (canonical 970),
  Step 0.9 (added the S34 deliverables presence + posture check via
  `check_s35_deliverables.py`).
- **1 NEW LESSONS section from S34** ("A carve-out claim must be
  verified against the test BODY, not its name/marker") referenced in
  the Verify-before-asking LESSONS list.
- **S34 candidate CLOSED** (K-a CI wiring + concurrency coverage)
  folded into the carry-forward list + Scope section + Out-of-scope's
  S34 deliverables (NEW LOCK).
- **Candidate E still EXHAUSTED** (30 reached) — requires a
  plan-ceiling revision first.

If new amendments arise pre-S35 open, walk them per the
reviewer-feedback hygiene pattern above.
