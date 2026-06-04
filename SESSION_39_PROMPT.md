# Session 39 prompt — scope picked at Phase 1
# (S38 closed the prompt_logger adlfs candidate at repo d610f0b — fresh
#  live ADLS coverage for PromptLogger.flush() [the LAST uncovered adlfs
#  WRITE surface] PLUS the module's first hermetic default-run guard. S38
#  also placed the cross-cutting `adls-live-coverage-v0` tag, CLOSING the
#  S33-S38 ADLS live-test cluster. With prompt_logger closed, EVERY adlfs
#  write surface in the codebase now has live coverage. S39 enters with a
#  TRULY empty actionable queue: A blocked / D operator-led / E exhausted /
#  lease-SAS an anti-trap [S38 grep-confirmed] / NO fresh adlfs candidate
#  remains. S39 is most likely a no-ship scope-resolution session unless the
#  operator unblocks A, begins D labeling, amends the E ceiling, or
#  commissions a genuinely new candidate.)

**Drafted at Session 38 close (2026-06-03), operator-commissioned.**
Mirrors the S20/.../S37/S38 prompt structure. Scope-agnostic at
Phases 0/1; scope-specific design gates at Phase 2 per chosen
candidate. Strict 7-phase ordering with halt-on-mismatch preserved.

This prompt should be invoked from `~/crawler-audit/SESSION_39_PROMPT.md`.
Re-read it on session open.

---

## Scope

Engineering session. Repo HEAD at `d610f0b`
(WA2.W8.adls-live-prompt-logger; S38). Workspace HEAD at the S38
close-out chain `a27bb8d` (primary close-out) + `4943d94` (anchor-pin) +
`685ed13` (baseline-clarity follow-up) + any later prompt-drafting commit
(see Step 0.1). **Workstream 0 fully closed at S27 via the
`workstream-0-end` tag at `a1c5636`.** **The S33-S38 ADLS live-test
cluster fully closed at S38 via the `adls-live-coverage-v0` tag at
`d610f0b`.**

Carry-forward candidates entering S39:

- **barcada-drift (Candidate A)** — deferred since S20; still needs
  4 AI/ML decisions per CLASSIFICATION_ADJACENT_PLAN.md §Item 8 AND
  2+ `canary_runs/*.parquet` files. **S38 re-confirmed empirically**
  that the launchd installer has NOT been run (`~/canary_runs/` absent;
  0 drift parquets on disk; no plist in `~/Library/LaunchAgents/`). Same
  state as S29-S38 close. **Remains BLOCKED.**

- **Phase 4 PR-D tooling (Candidate D)** — operator-led labeling
  territory. W0-side unblocked since S27; still gated on
  operator-led Stage 2/3 labeling.

- **Cassette corpus expansion (Candidate E) — EXHAUSTED.** S32 grew
  the corpus to 30, the plan's stated upper bound (§4 W7
  "~20-30 representative domains"). **No further +N is available
  without first amending the plan ceiling** (a Phase 1/2 or
  plan-revision decision). Do NOT add cassettes under the current plan.

- **The S33-S38 ADLS live-test cluster — CLOSED + TAGGED at S38.** Every
  adlfs WRITE surface now has live coverage: cost-journal S33/S34, parquet
  ShardWriter S35, page_storage S36, PartitionedShardWriter S37,
  prompt_logger S38 (ports 10000-10005). The cross-cutting
  `adls-live-coverage-v0` tag (at `d610f0b`) closes the cluster. **NOT a
  carry-forward.**

- **lease/SAS cost-journal live paths — ANTI-TRAP (S38-confirmed).** S38
  settled this empirically: `grep -ciE 'lease|sas'
  src/.../cost_journal_adls.py` = 0 — production constructs NO lease or
  SAS. A live test of a behavior the production code never performs has
  nothing to cover. **Do NOT scope it unless/until production grows a
  lease/SAS construct.**

**No new carry-forward introduced by S38.** The S38 deliverable was two
commits (1 hermetic guard + 1 live test). The canonical 970 test count is
unchanged; the combined count is 983 (970 + the 13-test hermetic guard).

**Scope-availability note (IMPORTANT):** with A blocked, D operator-led,
E exhausted, the ADLS cluster CLOSED, and lease/SAS an anti-trap, **S39
has NO clearly-actionable engineering scope** unless the operator (a)
unblocks A, (b) begins D labeling, (c) authorizes a plan-ceiling revision
to reopen E, or (d) commissions a NEW candidate. **There is no remaining
low-cost test-only ADLS candidate.** Surface this empty-queue condition at
Phase 1 before any candidate-choice AskUserQuestion. A no-ship close at
Phase 6 with the decision recorded is a LEGITIMATE outcome, not a failure.

**S36+S38 auth-seam lesson — apply before scoping ANY adlfs candidate (if
one ever reappears):** read the production call site's SIGNATURE first.
S35's `ShardWriter` and S37's `PartitionedShardWriter` take an explicit
`storage_options=` kwarg; S36's `page_storage.write_pages` and S38's
`prompt_logger.flush()` took NONE and resolved auth from
`AZURE_STORAGE_CONNECTION_STRING` in the environment (URL-only
`fsspec.url_to_fs`). Verify at source, do not assume.

**S35+S37 container-creation lesson — apply before scoping ANY
write_dataset / write_to_dataset adlfs candidate (if one ever reappears):**
adlfs's `makedirs(container, exist_ok=True)` silently no-ops; use
`fs.mkdir` (catch `FileExistsError`). For a multi-partition
`write_to_dataset`, pyarrow's per-partition `create_dir` hits adlfs's
non-idempotent `create_container` — pre-create the container in the fixture
and spike MULTIPLE partitions against a FRESH container to expose the race.

**S38 URL-construction lesson:** when a test resolves an fsspec URL
containing `key=value` segments (Hive partitions, `crawl_date=`, `shard=`),
build the URL by plain string concatenation (matching production), NOT
`Path.as_uri()` — `as_uri()` percent-encodes `=` to `%3D` and fsspec does
NOT decode it back.

Operator chooses at Phase 1 which candidate Session 39 ships (or that S39
is a no-ship session). Each candidate has its own Phase 2 design-gate
template.

**Sessions 13-38 precedent:** this session does NOT modify the
W4.1.5 driver orchestration at `tests/runners/fixture_cascade/`
(locked at `dd64963` for original files; `cascade.py` extended at
`a1c5636`/S27 + `9afde57`/S28; `test_cost_journal_wiring.py` added at
`a1c5636`/S27 + modified at `ae9e627`/S28). Does NOT modify
`expected.schema.json` v1.1 / `META_SCHEMA.md` v1.1. Does NOT modify
the committed `tests/fixtures/baseline-v0/` snapshot at `9e9a1fb`.
Does NOT modify the Session 19-38 deliverables. Does NOT modify the
S31 cassette deliverables at `06d67c4` or the S32 cassette
deliverables at `cfa0ec1` — never re-records or deletes any of the
30. Does NOT modify the S33 deliverable at `f1cdce8`, the S34
deliverables at `eba6585`, the S35 deliverable at `f80ccdc`, the S36
deliverable at `25c3696`, the S37 deliverable at `f4e0a4a`, or the **S38
deliverables** at `094a12f` (hermetic guard) + `d610f0b` (prompt_logger
adlfs live test). Does NOT delete/move the `adls-live-coverage-v0` tag.

Does NOT modify production code under `src/barcada_scraper/` UNLESS
Phase 2 design-gate explicitly authorizes a specific module. Of the
S39 candidates: Candidate A would add a NEW `barcada-drift` module
(new file, not a modification of locked code); Candidate D is
tooling-only.

Full regression-protection checklist in **Out-of-scope** at the end
of this prompt. Re-read it before any code lands.

---

## Reviewer-feedback hygiene (if this prompt is reviewed)

If an external reviewer (operator-invoked) flags items in this prompt
before Session 39 starts, walk each flagged item against on-disk
reality at the workspace HEAD and repo HEAD `d610f0b`, BEFORE applying
any change. Per S19-S38 pattern:

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
was sequential). **S35 anchor:** the build-time spike caught the adlfs
`makedirs`-no-op gotcha BEFORE commit. **S36 anchor:** the
operator-flagged "forced env-var auth" challenge resolved at SOURCE
before committing. **S37 anchor:** the build-time spike caught adlfs's
non-idempotent `create_container` across partitions in-Phase-3.
**S38 anchor:** a Phase-3 TEST bug (`Path.as_uri()` percent-encoding `=`
in a `shard=NNNNN` segment) was caught + fixed inside Phase 3 — the
production code was correct; the fix was the faithful string-concat URL
form. Apply the same discipline: validate any external-service
interaction AND any auth-seam claim AND any URL/encoding assumption AND
any directory/container-creation semantics against the real
source/emulator before committing claims about it.

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

Run in order. Halt and surface to operator on any mismatch.

### Step 0.1 — Workspace + repo HEAD

```
git -C ~/crawler-audit rev-parse HEAD
# Expect: 685ed13 (S38 baseline-clarity follow-up) OR 4943d94 (S38
# anchor-pin) OR a27bb8d (S38 primary close-out) OR this S39
# prompt-drafting commit succeeding it OR a later commit if additional
# workspace doc edits / prompt revisions landed. If N commits ahead of
# 685ed13, verify each via `git log --oneline 685ed13..HEAD` against
# expected prompt-finalization / doc-edit patterns; surface the SHA delta
# and request authorization if anything is unexpected. (S20-S38 precedent:
# operator authorized continuation when 1-4 extra workspace commits were
# the strengthened prompts themselves.)
#
# NOTE: SESSION_36_PROMPT.md carries an uncommitted operator-side edit left
# unstaged since S36 close. It may still be in the working tree at S39 open
# — tolerate it; it is operator territory.

git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: d610f0b (S38 WA2.W8.adls-live-prompt-logger). Its parent 094a12f
# is the S38 hermetic guard.
#
# Tolerated delta: operator-side eval_data labeling commits between
# S38 close and S39 open (Sessions 8-38 precedent). Verify via
# `git show --stat <sha>` for every commit in d610f0b..HEAD that each
# is strictly within eval_data/* (NO src/barcada_scraper/*, NO tests/*
# [INCLUDING the six Azurite live-test files + the hermetic guard], NO
# .github/* [INCLUDING live-integration.yml], NO scripts/*, NO docs/*
# touches); surface any non-eval_data delta for operator authorization
# before continuing.
```

### Step 0.2 — Tags (14 expected; +1 from S37's 13)

```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort
# Expect 14 tags. The S38 deliverable ADDED `adls-live-coverage-v0`:
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
#   14. adls-live-coverage-v0                      (placed S38 at d610f0b)

git -C /Users/administrator/projects/barcada-scraper rev-list -n 1 workstream-0-end
# Expect: a1c5636… (UNCHANGED).
git -C /Users/administrator/projects/barcada-scraper rev-list -n 1 adls-live-coverage-v0
# Expect: d610f0b… (the S38 prompt_logger adlfs live-test commit).

# NOTE: `workstream-a-week2-end` is NOT placed and is SUPERSEDED — the
# S33-S38 ADLS cluster tag-taxonomy was RESOLVED at S38 with the
# cross-cutting `adls-live-coverage-v0` (NOT a workstream-letter tag;
# Findings M+N). Do NOT re-offer `workstream-a-week2-end` or any
# `workstream-b-*` for this cluster.

# Tolerated delta: additional operator-side stage1-*/eval_data-* tags.
# For each new tag beyond the 14, verify the tagged commit is
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
# modifications. Any non-empty diff outside these 3 files = HALT.
# S29-S38 did NOT touch this surface.
```

### Step 0.4 — Fixture counts (use the Python rglob pattern, NOT bare find)

**UNCHANGED FROM S33/.../S38**: S38 shipped two test files, NOT a
cassette. `cassette_count` and `exclusions_count` stay at **30**.

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

### Step 0.5 — Test-suite baseline (S39 canonical)

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
# CRITICAL: the canonical 16-path is UNCHANGED from S27-S38 close. The S38
# hermetic guard (tests/classifier/llm/test_prompt_logger.py, 13 tests) is
# NOT in this 16-path — it is tracked as a Step 0.8 sub-suite (see 0.8).
# Step 0.5 STILL expects 970, NOT 983. Do NOT treat the combined 983 as the
# Step 0.5 baseline.
#
# Sub-totals (16 paths; ALL identical to S27-S38 close — ALL SIX Azurite
# live tests are @pytest.mark.live + skip-by-default and NOT in this run):
#   210 conformance + 52 driver + 99 baseline_v0 + 33 synthetic_crawl +
#    32 robots + 30 robots_gate + 30 robots_bypass_config + 43 cost_journal +
#    13 cost_journal_local + 19 cost_journal_adls + 35 robots_integration +
#    74 vmss_worker + 129 job_runner + 152 worker_loop +
#     7 robots_gate_integration + 12 worker_loop_persistence = 970
```

The sub-paths add up to 970. Any drift = halt. If the headline
mismatches, re-run each sub-path independently to localize.

**Combined baseline (16-path + the S38 hermetic guard) = 983** (970 + 13):
this is the cumulative-gate floor for S39, NOT the Step 0.5 canonical
number. See Step 0.8 for the guard's standalone pin.

**Narrower baselines**:
- 480 (S22 headline; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 944 (canonical 16-path minus 19 cost_journal_adls minus 7
  robots_gate_integration).

Whichever baseline is bound at Phase 1, hold it consistent across ALL
Phase 3 commits in S39. The cumulative-test-count gate never lets it
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
.venv/bin/python -m pytest tests/orchestrator/test_job_runner.py -q               # 129
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop.py -q              # 152
.venv/bin/python -m pytest tests/orchestrator/test_robots_gate_integration.py -q   # 7
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop_persistence.py -q   # 12

.venv/bin/python -m pytest tests/runners/fixture_cascade/test_cost_journal_wiring.py -q  # 6
.venv/bin/python -m pytest tests/classifier/stage1/test_run_cascade.py tests/classifier/stage1/test_cost_tracker.py -q  # 32

# S35+S37 parquet hermetic suite (33 file:// tests; the default-run guard
# the S35+S37 live tests complement; unchanged):
.venv/bin/python -m pytest tests/test_parquet_writer.py -q              # expect 33

# S36 page_storage hermetic suite:
.venv/bin/python -m pytest tests/classifier/page_acquisition/test_page_storage.py -q  # expect 13

# S38 prompt_logger hermetic guard (NEW Step 0.8 sub-suite — the module's
# first default-run coverage; file:// LocalFileSystem; NO live marker):
.venv/bin/python -m pytest tests/classifier/llm/test_prompt_logger.py -q  # expect 13
```

### Step 0.9 — S25-S38 invariants + cassette-dir + S33-S38 live-test presence

**Coverage note**: equals S38's Step 0.9 plus a NEW check for the TWO S38
deliverables. The env hook blocks inline `python -c` containing
`ast.parse` (S28) or Azure-credential-secrets references (S32/S33).

**PREFER the Write tool to stage the helper scripts, NOT the
`cat >…<<'PYEOF'` heredocs.** Empirically re-confirmed S33-S38: the
heredoc form for any AST / secrets-referencing script trips the safety
hook even though the script touches no real secret. Re-create the SAME
script via the Write tool and run it via `.venv/bin/python <path>`. Run
any secrets-referencing import check as its OWN Bash call. If a script
fails to STAGE, switch to the Write tool; if it fails to EXECUTE (a real
assertion fires), HALT.

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
print('OK (a) S24/S25 public APIs unchanged')
"

# (a2) S35 parquet ShardWriter public API unchanged (inline-safe):
.venv/bin/python -c "
import inspect
from barcada_scraper.output.parquet_writer import (
    ShardWriter, PartitionedShardWriter, write_records_to_shards,
    write_records_to_shards_partitioned, shard_id_for_domain,
    storage_options_from_env, DEFAULT_FLUSH_EVERY,
)
sw = inspect.signature(ShardWriter.__init__)
kwargs = set(sw.parameters) - {'self'}
assert {'output_dir', 'crawl_date', 'shard_id', 'storage_options'} <= kwargs, kwargs
for prop in ('final_path', 'records_written'):
    assert isinstance(getattr(ShardWriter, prop), property), prop
print('OK (a2) S35 parquet ShardWriter public API + storage_options seam unchanged')
"

# (a3) S36 page_storage public API unchanged (inline-safe; env-resolved seam):
.venv/bin/python -c "
import inspect
from barcada_scraper.classifier.page_acquisition import page_storage, page_schema
params = list(inspect.signature(page_storage.write_pages).parameters)
assert params == ['rows', 'output_path'], params
assert page_storage.__all__ == ['write_pages'], page_storage.__all__
assert hasattr(page_schema, 'empty_row')
assert len(page_schema.SCHEMA) == 17, len(page_schema.SCHEMA)
print('OK (a3) S36 page_storage write_pages public API (no storage_options kwarg) unchanged')
"

# (a4) S37 PartitionedShardWriter public API unchanged (inline-safe):
.venv/bin/python -c "
import inspect
from barcada_scraper.output.parquet_writer import PartitionedShardWriter, write_records_to_shards_partitioned
kw = set(inspect.signature(PartitionedShardWriter.__init__).parameters) - {'self'}
assert {'output_dir', 'crawl_date', 'shard_id', 'flush_every', 'storage_options'} <= kw, kw
for prop in ('records_written', 'partition_root'):
    assert isinstance(getattr(PartitionedShardWriter, prop), property), prop
wk = set(inspect.signature(write_records_to_shards_partitioned).parameters)
assert {'records', 'output_dir', 'crawl_date', 'flush_every', 'storage_options'} <= wk, wk
print('OK (a4) S37 PartitionedShardWriter public API + storage_options seam + partition_root property unchanged')
"

# (a5) S38 prompt_logger public API unchanged (inline-safe; the S38 live
# test + hermetic guard depend on these public symbols, AND flush() STILL
# resolves auth URL-only [env-resolved seam, no storage_options kwarg]):
.venv/bin/python -c "
import inspect
from barcada_scraper.classifier.llm.prompt_logger import PromptLogger, prompt_log_url
init = set(inspect.signature(PromptLogger.__init__).parameters) - {'self'}
assert {'output_url', 'phase', 'shard_id', 'worker_id'} <= init, init
assert 'storage_options' not in init and 'credential' not in init, init
assert isinstance(getattr(PromptLogger, 'buffered'), property)
for m in ('log', 'flush'):
    assert callable(getattr(PromptLogger, m)), m
plu = set(inspect.signature(prompt_log_url).parameters)
assert {'blob_output_url', 'phase', 'crawl_date', 'shard_id'} <= plu, plu
assert PromptLogger.__module__.endswith('prompt_logger')
print('OK (a5) S38 prompt_logger public API (env-resolved seam; no storage_options) unchanged')
"

# (b) S26: CRAWLING_POLICY.md doc stability.
test "$(wc -l < docs/CRAWLING_POLICY.md)" = "77" && \
    test "$(wc -c < docs/CRAWLING_POLICY.md)" = "2519" || \
    { echo "HALT: CRAWLING_POLICY.md drifted"; exit 1; }
echo "OK docs/CRAWLING_POLICY.md unchanged (77 lines / 2519 bytes)"

# (c) S27+S28 per-tier wiring + (d-cont.) cascade AST — stage via Write tool
#     (hook blocks inline ast.parse). Assert _journal_record_with_breakdown +
#     _run_stage1 funcs exist; with_stage_cost_added + with_shard_appended +
#     update_with_retry + run_shard tokens present in cascade.py.

# (d) S28 ShardResult split field presence (inline-safe):
.venv/bin/python -c "
from barcada_scraper.classifier.stage1.run import ShardResult
fields = set(ShardResult.__dataclass_fields__.keys())
assert 'llm_cost_usd' in fields and 'embedding_cost_usd' in fields and 'cost_usd' in fields
assert len(fields) == 14, f'{len(fields)}: {fields}'
print('OK (d) S28 ShardResult 14 fields present')
"

# (e) S29 K-b smoke script existence + AST parse — own Bash call (secrets).
#     Stage via Write tool; assert exists + ast.parse OK + main() defined +
#     220 LOC.

# (f) S31+S32 cassettes (10) + S33 primitive + S34 race+CI + S35 parquet +
#     S36 page_storage + S37 partitioned + S38 prompt_logger live test +
#     hermetic guard. Stage check_s39_deliverables.py via the Write tool
#     and run it.
```

Stage the following as `check_s39_deliverables.py` via the Write tool
(NOT a heredoc) and run `.venv/bin/python <path>` (then move it OUT of the
repo tree via `mv <path> /tmp/` — `rm`/`os.remove` are env-hook-blocked,
S38-confirmed):

```python
import re
from pathlib import Path
root = Path('tests/fixtures/synthetic_crawls')
s31 = ('patagonia.com', 'deere.com', 'ford.com', 'pfizer.com', 'wholefoodsmarket.com')
s32 = ('propublica.org', 'apnews.com', 'c-span.org', 'eff.org', 'harvard.edu')
for d in s31 + s32:
    assert (root / d / 'cassette.yaml').exists(), f'missing cassette: {d}'
    assert (root / d / 'extract_hard_exclusions.json').exists(), f'missing sidecar: {d}'
# S33 primitive + live marker.
prim = Path('tests/classifier/pipeline/test_cost_journal_adls_azurite.py')
assert prim.exists()
ptext = prim.read_text()
assert '@pytest.mark.live' in ptext and '--skipApiVersionCheck' in ptext
assert 'live:' in Path('pyproject.toml').read_text()
# S34 concurrency + CI workflow.
conc = Path('tests/classifier/pipeline/test_cost_journal_adls_azurite_concurrency.py')
assert conc.exists()
ctext = conc.read_text()
assert '@pytest.mark.live' in ctext and '_BLOB_PORT = 10001' in ctext
assert 'update_with_retry' in ctext and 'with_shard_appended' in ctext
wf = Path('.github/workflows/live-integration.yml')
assert wf.exists()
wtext = wf.read_text()
assert 'workflow_dispatch' in wtext and re.search(r"cron: '0 6 \* \* \*'", wtext)
assert not re.search(r'^  push:', wtext, re.M) and 'pull_request' not in wtext
assert '-m live' in wtext and 'tests/classifier/pipeline/' in wtext
# S35 parquet.
pq = Path('tests/classifier/pipeline/test_parquet_writer_adls_azurite.py')
assert pq.exists()
qtext = pq.read_text()
assert '@pytest.mark.live' in qtext and '_BLOB_PORT = 10002' in qtext
assert 'barcada-azurite-parquet' in qtext and 'ShardWriter' in qtext
assert 'AzureBlobFileSystem' in qtext and 'abfss://' in qtext
# S36 page_storage.
ps = Path('tests/classifier/pipeline/test_page_storage_adls_azurite.py')
assert ps.exists()
stext = ps.read_text()
assert '@pytest.mark.live' in stext and '_BLOB_PORT = 10003' in stext
assert 'barcada-azurite-pages' in stext and 'write_pages' in stext
assert 'AZURE_STORAGE_CONNECTION_STRING' in stext and 'AzureBlobFileSystem' in stext
# S37 partitioned.
pp = Path('tests/classifier/pipeline/test_partitioned_shard_writer_adls_azurite.py')
assert pp.exists()
pptext = pp.read_text()
assert '@pytest.mark.live' in pptext and '_BLOB_PORT = 10004' in pptext
assert 'barcada-azurite-partitioned' in pptext
assert 'write_to_dataset' in pptext and 'HivePartitioning' in pptext
assert 'storage_options=storage_options' in pptext and 'setup_fs.mkdir' in pptext
# S38 prompt_logger live test (NEW).
pl = Path('tests/classifier/pipeline/test_prompt_logger_adls_azurite.py')
assert pl.exists(), 'missing S38 prompt_logger adlfs live test'
pltext = pl.read_text()
assert '@pytest.mark.live' in pltext, 'S38 live test lost its live marker'
assert '_BLOB_PORT = 10005' in pltext, 'S38 fixture lost its distinct port (collides with S33-S37)'
assert 'barcada-azurite-prompts' in pltext, 'S38 fixture lost its distinct container name'
assert 'PromptLogger' in pltext and 'prompt_log_url' in pltext, 'S38 test lost its production drive'
assert 'AZURE_STORAGE_CONNECTION_STRING' in pltext, 'S38 test lost its env-resolved auth seam'
assert 'AzureBlobFileSystem' in pltext, 'S38 test lost its positive teeth'
assert 'LocalFileSystem' in pltext, 'S38 test lost its demonstrated negative control'
assert 'setup_fs.mkdir' in pltext, 'S38 test lost its container pre-mkdir'
assert '--skipApiVersionCheck' in pltext
# S38 prompt_logger hermetic guard (NEW).
hg = Path('tests/classifier/llm/test_prompt_logger.py')
assert hg.exists(), 'missing S38 prompt_logger hermetic guard'
hgtext = hg.read_text()
# Assert no live-marker DECORATOR (a `^\s*@pytest.mark.live` line) -- NOT the
# mere string, which the module docstring legitimately references by name.
assert not re.search(r'^\s*@pytest\.mark\.live', hgtext, re.M), 'hermetic guard must NOT carry a live-marker decorator'
assert 'prompt_log_url' in hgtext and 'PromptLogger' in hgtext
print('OK (f) S31+S32 cassettes + S33 primitive + S34 race+CI + S35 parquet + S36 page_storage + S37 partitioned + S38 prompt_logger live+hermetic present (posture intact)')
```

If any of 0.1-0.9 fail, HALT before doing any work.

**Optional Docker-gated check (NOT a halt condition)**: if Docker is
available locally, the operator MAY confirm ALL SIX live tests still
pass + coexist:
```
.venv/bin/python -m pytest -m live tests/classifier/pipeline/ -q
# Expect: 6 passed, 209 deselected. Ports S33=10000 / S34=10001 /
# S35=10002 / S36=10003 / S37=10004 / S38=10005. Informational; Docker is
# NOT required for S39 unless the chosen scope is new live-test work.
```

### Step 0.10 — Same-shape-test sweep (one-time; pre-implementation; NOT per-commit)

**Timing**: NOT part of the cold-start halt set (0.1-0.9). Run it ONCE the
Phase 1 scope is fixed and BEFORE Phase 3 — never inside the per-commit
checkpoint loop. Grep the test tree for same-shape tests that pin the
contracts the chosen scope will modify. If a same-shape test is found AND
it is NOT in this prompt's explicit replacement allowlist, do NOT silently
modify/replace it — surface it at Phase 1/2 as a design-gate sub-question.

---

## Required workspace reading (Session 39 first 10 minutes)

In this order:

1. **`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`** — full handoff
   state at S38 close. Lists scope candidates (A/D/E) with prerequisites.
   The ADLS cluster is CLOSED + TAGGED; lease/SAS is an anti-trap; NO fresh
   adlfs candidate remains. Note the explicit empty-actionable-queue flag.

2. **`~/crawler-audit/SESSION_LOG.md`** Session 38 entry — the ENV-resolved
   auth seam; the as_uri-encoding test-bug finding; the hermetic-guard
   design gate (the module had zero tests); the cross-cutting tag
   resolution; the count split (970 canonical / 13 hermetic / 983 combined).

3. **`~/crawler-audit/LESSONS.md`** — the FIVE new "S38 folding" sections
   (as_uri percent-encodes `=`; live-only test of a zero-test module;
   lease/SAS anti-trap grep; cross-workstream tag identity; baseline
   bookkeeping). Plus the S33-S37 folds if a live-service scope is somehow
   chosen.

4. **`~/crawler-audit/BARCADA_CRAWLER_REMEDIATION_PLAN.md`** —
   chosen-scope section. READ-ONLY by default; the only exception is the
   plan-amendment session shape (explicit operator authorization to edit
   §4 W7's "~20-30" ceiling).

5. **`~/crawler-audit/CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 —
   only if Candidate A (barcada-drift) is chosen.

---

## Phase 1 — Scope resolution (no code; pre-design-gate)

**FIRST**: surface the scope-availability note (A blocked / D
operator-led / E exhausted / ADLS cluster CLOSED+tagged / lease-SAS an
anti-trap / NO fresh adlfs candidate remains). **S39 most likely has no
clearly-actionable engineering scope** without operator action. Then
operator picks one (or declares a no-ship session).

### Three invocation shapes (S39 continues the empty-queue condition)

- **Decided before invocation (cleaner).** Operator names the candidate
  when commissioning S39. Phase 1 CONFIRMS rather than elicits: skip the
  candidate-choice AskUserQuestion; still re-run the empirical prereq audit
  (for A: parquets + plist + AI/ML); proceed to that candidate's Phase 2
  gate.

- **Decided at Phase 1 (more flexible).** S39 opens, Phase 0 verifies,
  Phase 1 surfaces the empty-queue condition explicitly and elicits via
  AskUserQuestion. **Context-budget caveat**: a Phase 1 that resolves to
  "plan amendment needed" or "no actionable scope" is a no-ship session —
  surface that trade-off in the same AskUserQuestion. A "nothing
  actionable" close at Phase 6 with the decision recorded is a legitimate
  outcome, not a failure.

- **Plan-amendment session shape (reopen E).** Raise the §4 W7 "~20-30"
  ceiling in BARCADA_CRAWLER_REMEDIATION_PLAN.md (READ-ONLY by default).
  That plan edit is itself the Phase 2/3 deliverable (explicit operator
  authorization; document in SESSION_LOG.md). Only AFTER the ceiling is
  amended + committed may a subsequent recording sub-surface proceed under
  the proven S31/S32 mechanics.

### Candidate A — `barcada-drift` (AI/ML alignment + ≥2 parquets)

Per CLASSIFICATION_ADJACENT_PLAN.md §Item 8. Est ~300 LOC logic +
~70-100 LOC overhead ≈ **~370-400 LOC delivered**.

**Prerequisites:** 2+ `canary_runs/*.parquet` on operator's machine;
AI/ML responses on 4 §Item 8 decisions OR explicit operator-side
placeholder choices with "AI/ML-to-tune" notes.

**HALT IF** the 4 AI/ML decisions are not pre-resolved AND operator has
not authorized placeholders.

**Empirical prereq audit at S38 close** (carry-forward): `~/canary_runs/`
absent; 0 drift parquets; no barcada/canary/drift plist; no AI/ML
responses. Re-run these empirical checks at S39 Phase 1 BEFORE the
candidate-choice AskUserQuestion (S29 LESSONS). If unchanged, A remains
blocked.

### Candidate D — Phase 4 PR-D operator-led labeling (operator territory)

Per plan §11 Risk Register. Stage 2 + Stage 3 labeling gates
PR-D/E/F/G. Operator-led; Claude Code's role limited to tooling.
W0-side unblocked at S27; still gated on operator-led labeling.

### Candidate E — Cassette corpus expansion (EXHAUSTED)

Reached the plan's **30 upper bound** at S32. **Not available** without
first amending the §4 W7 ceiling (made BEFORE any recording). Do NOT
add cassettes under the current plan. Mechanics proven (S31+S32).

### NO fresh adlfs candidate remains

The S33-S38 ADLS write cluster is CLOSED + TAGGED. Every adlfs write
surface (cost-journal, parquet both halves, page_storage, prompt_logger)
has live coverage. The lease/SAS path is an anti-trap (S38 grep-confirmed:
production constructs none). **Do NOT manufacture an ADLS candidate.** A
genuinely new ADLS surface would have to appear in production first; if
it does, default to the S33-S38 live-fixture shape (distinct port 10006+,
read the auth seam from the call-site signature, pre-mkdir the container,
demonstrate negative-control teeth, build-time spike first) and it would
extend the cluster as `adls-live-coverage-v1`.

### Sub-question 1.TAG — Tag at session close (RESOLVED at S38)

**The S33-S38 ADLS cluster tag-taxonomy is SETTLED.** S38 placed the
cross-cutting `adls-live-coverage-v0` annotated tag at `d610f0b` over the
SIX ADLS live-test commits (robots/K-b excluded), NOT a workstream-letter
tag. Do NOT re-open this; do NOT re-offer `workstream-a-week2-end` or any
`workstream-b-*`. If S39 ships a NEW tagged surface, decide its tag
identity at Phase 1 from first principles (e.g. `barcada-drift-v0` for
Candidate A); otherwise there is NO tag decision at S39 close.

Phase 5 reads this resolution directly — no Phase 2 re-decision.

---

## Phase 2 — Design-gate elicitation (no code; AskUserQuestion)

Per chosen Phase 1 candidate. Source-verify at session-current HEAD per
the `[[verify-before-asking-discipline]]` AND the S22-S38
"Plan-vs-reality at Phase 2" + S25 "source-verify drives option-set
design" patterns BEFORE each AskUserQuestion batch.

**HALT IF** any Phase 2 decision would require modifications to
`src/barcada_scraper/` beyond what was Phase-2-authorized OR to the
W4.1.5 driver beyond the S16/S27/S28 exceptions OR to any S19-S38
deliverable (including the six Azurite live tests, the S38 hermetic guard,
the S34 CI workflow, the `adls-live-coverage-v0` tag, or
re-recording/deleting any of the 30 cassettes) — surface as a design-gate
sub-question before patching.

### CRITICAL Phase 2 hygiene

Carry forward S26/S28/S29/S30/S34/S35/S36/S37/S38 hygiene verbatim: count
each Q-* option set (≤4 or tier/split); audit existing test pins for
by-design vs empirical; size new scripts with the ~70-100 LOC additive
overhead floor; default new external-service-backed tests to
live-on-demand posture unless a named carve-out justifies it; when a
carve-out names a behavior, point it at the specific test body that
exercises it (S34 fold); demonstrate teeth via a negative control (S34/S35
fold); read the production call-site SIGNATURE to determine the auth seam
(S36/S38 fold); for any write_dataset path, pre-create the container +
spike multiple partitions (S37 fold); for any module with ZERO existing
tests, surface "add a hermetic default-run guard?" as a Phase 2
sub-question (S38 fold); and decide explicitly whether a new default-run
test goes INTO a canonical-headline path or a NEW Step 0.8 sub-suite, and
record all three baseline numbers (S38 baseline-bookkeeping fold).

### If Candidate A (barcada-drift)

Carry-forward (unchanged): Q-A.1 CLI namespace; Q-A.2 drift metric;
Q-A.3 alert threshold; Q-A.4 input contract; Q-A.5 output shape;
Q-A.6 test corpus. (Split into 2-3 sequential AskUserQuestion calls;
both the 4-options-per-question and 4-questions-per-call caps apply.)

### If Candidate D (Phase 4 PR-D tooling)

- **Q-D.1 Tooling shape**: batch validators / import scripts / hygiene
  tools. Operator-led design.

### Shared sub-questions (all candidates)

- **Q-SHARED.1 Commit shape**: per-module / per-sub-surface (S18-S38
  default; Recommended) vs single bundled commit (only when genuinely
  one self-contained sub-surface).

(Tag-at-close RESOLVED at S38; no S39 re-decision unless a NEW tagged
surface ships.)

---

## Phase 3 — Implementation (per chosen commit shape, strict order)

### Non-interleaving rule (CRITICAL for bisectability)

If the chosen candidate has multiple sub-surfaces, complete each fully
before starting the next. Per S22-S38 precedent. If a mid-sub-surface
dependency emerges, HALT and surface as a design-gate sub-question.

### Build-time validation spike (carry the S35/S36/S37/S38 emphasis)

For any external-service-backed test, BEFORE writing the final test
body: stand up the emulator and drive the REAL production code through
it in a throwaway spike (staged via the Write tool). Confirm the URL
form (string-concat vs as_uri — S38), the auth mechanism (kwarg vs env —
S36/S38), the resolved-fs type, the directory/container-creation
semantics (S35 makedirs-no-op; S37 non-idempotent create_container), and
a full round-trip (write → read back via a FRESH handle). This catches
version-skew and API-semantic gotchas inside Phase 3 instead of as a
post-commit HALT. Tear the spike container down (`docker stop`
auto-removes with `--rm`; the agent's Bash `rm -f`/`os.remove` is
env-hook-blocked, but `docker stop` and in-fixture `docker rm -f` are
fine). Move the spike script OUT of the repo tree via `mv <path> /tmp/`
after (it must NOT be committed).

### Per-commit checkpoint protocol (single source of truth)

At EVERY Phase 3 commit boundary, run these 6 steps IN ORDER:

**1. Combined suite**

```
.venv/bin/python -m pytest \
    <the canonical 16-path invocation from Step 0.5> \
    tests/classifier/llm/test_prompt_logger.py \
    <new S39 test paths if any> -q
# Baseline = 983 (970 canonical + 13 S38 hermetic guard). A new
# @pytest.mark.live test stays OUT of the headline unless a deliberate
# decision adds it. Verify a new live test out-of-band:
# `pytest -m live tests/classifier/pipeline/` (expect 6 + N).
```

Expected: previous_baseline + N new tests, all passing. If failing
tests are NOT a deliberate consequence of the surface-under-test → HALT.

**2. Ruff sanity (touched files only) + mid-implementation format check**

```
.venv/bin/ruff check <touched paths>
.venv/bin/ruff format --check <touched paths>
# (ruff is Python-only; a YAML/workflow-only change has no ruff-touched
# files — note that explicitly. A new Python test file WILL likely need
# `ruff format` once — S35/S36/S37 each reformatted once; S38's hermetic
# guard reformatted once, the live test did not. Apply it, re-check,
# re-run the test.)
```

**3. Verification table (build in chat per `[[double-check-before-commit]]`)**

Build a claim → reality → status table for every concrete claim in the
draft commit message. Any ✗ → fix the claim BEFORE staging. Distinguish
net-new tests from newly-in-invocation pre-existing tests (S23). For
exit-code claims use `cmd > /tmp/out 2> /tmp/err; echo "Exit: $?"`. For
new-file LOC claims use `wc -l` AFTER any ruff-format pass. **For any
live test, include a teeth check** (a negative control demonstrated to
FAIL on the wrong path) in the table, not just "it passes" (S34/S35/S38).

**4. `git status` check**

Only intended files staged; no surprise `eval_data/` or unauthorized
`src/` changes. Operator-side `eval_data/` modifications stay unstaged.
Throwaway helper scripts (`check_*`, `spike_*`) must be moved to `/tmp/`,
NOT committed.

**5. "Confirm to commit?" presented to operator**

Include: verification table; commit message file location
(`/tmp/<id>-msg.txt`); file list to stage (M / A / D). Confirm the
commit subject's label reconciles with the decision record (the
`WA2.W8.*` prefix is the established commit-prefix for the ADLS surface
family — only reuse it if the surface genuinely belongs to that family;
Candidate A/D get their own appropriate prefix). Commit message uses `-F`
(no `-m` fallback) and contains NO backticks in the body (S35 fold). NO
`Co-Authored-By`.

**6. After operator confirms**

Stage + commit + verify the new SHA (`git log --oneline -1`) + verify
combined suite still passes on the new HEAD.

### Cumulative test-count gate

Track combined-suite passing count at each commit boundary. The count
NEVER decreases between checkpoints. Authorized decreases ONLY for a
Q-*-authorized same-shape 1↔1 replacement (cite the authorization +
name replaced + replacement in the commit body). Baseline bound at
Phase 1: **983** (canonical 16-path 970 + the S38 hermetic guard 13). A
new live-marked test does NOT raise the headline — verify it out-of-band
(`pytest -m live tests/classifier/pipeline/`).

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
edits to `eval_data/*` can fail the gate even though no S39 commit
touches eval_data. When this fires:
1. Confirm the failing row is operator-WIP (`git diff eval_data/`),
   not committed HEAD (`git show HEAD:eval_data/...`).
2. Confirm the S39 commits do not touch eval_data
   (`git diff origin/main..HEAD -- eval_data/`).
3. Surface to operator with the exact row + reason + diff.
4. Two paths: (a) operator-fix in WT, re-run gate; (b) stash eval_data
   WIP, push, restore.
5. Do NOT auto-fix locked-artifact content.

S20+S22 precedent: operator chose (a). S21/S23-S38 ran the gate clean.

---

## Phase 5 — Push + tag

- Push to `origin/main` after operator confirms.
- Tag per Phase 1 (no ADLS tag decision remains — the cluster is closed
  and tagged `adls-live-coverage-v0`). If a NEW candidate ships a tagged
  milestone (e.g. `barcada-drift-v0`), place it with an annotated message
  naming every sub-surface commit + mapping to plan bullets + listing
  deferrals. Do NOT place `workstream-a-week2-end` or any `workstream-b-*`.

Note: workstream-0-end placed at S27. W A.1 closed at S22's
`workstream-a-week1-end`. The ADLS live-test cluster CLOSED at S38's
`adls-live-coverage-v0`.

---

## Phase 6 — Workspace close-out

- Append Session 39 entry to `~/crawler-audit/SESSION_LOG.md` including
  a **Canonical S39-close baseline** block with the exact pytest
  invocation + verified count. **Record the count split unambiguously**
  (S38 baseline-bookkeeping fold): canonical 16-path Step 0.5 count;
  any new Step 0.8 sub-suite (path + expect-N); combined cumulative-gate
  count. If the fixture count changes (only via a plan-ceiling revision
  reopening E), record the new `cassette_count == N` /
  `exclusions_count == N`. Otherwise pin `cassette_count == 30` /
  `exclusions_count == 30`.
- Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md` for Session
  40 — explicitly pin the S40 Phase 0 workspace anchor SHA per the
  S21-S38 post-audit pattern. After the close-out commit lands, expect
  **1-2 follow-up commits** pinning the actual SHA.
- Update `~/crawler-audit/LESSONS.md` with any new forward-applicable
  patterns.
- Workspace close-out: 1 primary commit + 1-2 follow-up commits. Push
  workspace after operator confirms.

Note: drafting the next-session prompt (`SESSION_40_PROMPT.md`) is NOT
a built-in Phase 6 step. Per S20→S38 precedent, prompt-drafting is
operator-commissioned between sessions. If the operator asks for it
explicitly at S39 close, draft it as a separate follow-up.

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

### No-ship session
1. Empty-queue condition surfaced at Phase 1; operator decision recorded
   in SESSION_LOG.md; no repo commit; baselines re-pinned for S40.

### Shared (all candidates additionally satisfy)
- **S1.** Combined suite at session close: 983 baseline + N new tests,
  all passing. A new live-marked test stays out of the canonical headline
  (verified out-of-band; `pytest -m live tests/classifier/pipeline/`
  → 6 + N passed).
- **S2.** Pre-push gate green (incl. eval_data WIP halt protocol).
- **S3.** Regression-protection checklist held (see Out-of-scope). In
  particular: ALL S21-S38 deliverables stay at their SHAs; their public
  APIs unchanged; the 5 S31 + 5 S32 cassettes stay at `06d67c4` /
  `cfa0ec1`; the S33 Azurite test + live marker stay at `f1cdce8`; the
  S34 concurrency test + CI workflow stay at `eba6585` (workflow OFF
  push/PR); the S35 parquet test stays at `f80ccdc` (port 10002); the
  S36 page_storage test stays at `25c3696` (port 10003, env auth); the
  S37 partitioned test stays at `f4e0a4a` (port 10004); the S38
  prompt_logger live test stays at `d610f0b` (port 10005, env auth,
  negative-control teeth, container pre-mkdir) + the hermetic guard stays
  at `094a12f` (13 tests, no live marker); the `adls-live-coverage-v0`
  tag stays at `d610f0b`; CRAWLING_POLICY.md 77 lines / 2519 bytes; the
  combined total stays at 983 (or grows) unless a Q-* authorizes a
  same-shape 1↔1 replacement.

---

## Out-of-scope (no exceptions without operator authorization)

Per the regression-protection checklist. **S38 added TWO new locks**
(the prompt_logger hermetic guard at `094a12f` + the prompt_logger adlfs
live test at `d610f0b`) and ONE new tag lock (`adls-live-coverage-v0`);
otherwise unchanged from the S38 prompt.

**S19-S37 deliverables:** unchanged — see the S38 prompt's Out-of-scope
for the full per-session list (`tools/baseline_v0/`, `tools/synthetic_crawl/`,
`scraper/robots*.py`, `orchestrator/*`, `cost_journal*.py`,
`output/parquet_writer.py`, `page_storage.py`, the 30 cassettes, the S33
Azurite primitive, the S34 race test + `live-integration.yml`, the S35
parquet adlfs test, the S36 page_storage adlfs test, the S37
PartitionedShardWriter adlfs test, etc.). ALL stay at their placed SHAs
with public APIs unchanged.

**S38 deliverables (NEW LOCKS):**
- `tests/classifier/llm/test_prompt_logger.py` at `094a12f` — 282 LOC;
  13 hermetic `file://` tests; the module's first default-run guard;
  NO live marker; CI-visible. Do NOT modify without Phase 2 authorization.
- `tests/classifier/pipeline/test_prompt_logger_adls_azurite.py` at
  `d610f0b` — 358 LOC; 1 `@pytest.mark.live` test driving the production
  `classifier/llm/prompt_logger.py::PromptLogger.flush()` against Azurite
  via `adlfs.AzureBlobFileSystem` on a DISTINCT port 10005 / container
  `barcada-azurite-prompts`. **AUTH SEAM: ENV-resolved** — `flush()`
  resolves auth via `fsspec.url_to_fs(output_url)` URL-only (no
  `storage_options`), so the test authenticates adlfs via
  `AZURE_STORAGE_CONNECTION_STRING` (`monkeypatch.setenv`). URL built via
  the production `prompt_log_url()` helper. Container pre-`mkdir` (catch
  `FileExistsError`). Teeth: resolved fs is `AzureBlobFileSystem` +
  blob-relative path, read back via a FRESH handle; negative control =
  `file://` resolves to `LocalFileSystem` + absolute path. Auto-joins the
  CI workflow's `-m live` dir selection. Do NOT modify without Phase 2
  authorization. **Production `prompt_logger.py` is UNMODIFIED — keep it
  that way.** With S38, EVERY adlfs write surface has live coverage.
- `adls-live-coverage-v0` annotated tag at `d610f0b` — cross-cutting;
  names the SIX ADLS live-test commits (S33-S38); robots/K-b excluded.
  Do NOT delete/move. Do NOT place `workstream-a-week2-end` (superseded).

**W4.1.5 driver orchestration:** `tests/runners/fixture_cascade/`
(except via W5.X-prefix commit — only S16/S27/S28 opened it).

**Baseline-v0 ground truth:** the committed `tests/fixtures/baseline-v0/`
snapshot at `9e9a1fb` (1213 files).

**Schemas + plans (locked):** `expected.schema.json` v1.1;
`META_SCHEMA.md` v1.1; `meta.schema.json` v1.0; `stage1.schema.json`
v1.0; all 14 tags at their placed SHAs;
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` (READ-ONLY);
`CLASSIFICATION_ADJACENT_PLAN.md` (UPDATED only when AI/ML decisions
land); `RECONCILIATION_2026-05-21.md`; `docs/phase4_implementation_plan.md`.

**Operator-owned territory:** all of `eval_data/` — per-row WIP edits
expected and unstaged (Sessions 8-38); inter-session operator-side
eval_data COMMITS tolerated (verify eval_data-only via `git show --stat`).
2 operator-side stage1 TAGS point at eval_data-only commits.

**Production code:** `src/barcada_scraper/` — locked unless Phase 2
authorizes a specific module. S21-S25+S28 authorized; S26+S27+S29-S38
added no new src/ authorizations (S35-S38 were test-only).

**Pipeline configs:** `configs/`.

**CI workflows:** `.github/workflows/` — `python-package.yml`,
`build-and-push-image.yml` pre-existing; `live-integration.yml` is the
S34 lock (the `-m live` selection auto-picks up the six live tests; do
NOT weaken the trigger posture or guard). New workflows require a Phase 2
design-gate.

**Phase 4 work:** PR-D/E/F/G W0-side unblocked since S27; still gated
on operator-led Stage 2/3 labeling.

---

## Verify-before-asking discipline (strict rule from S19-S38)

Per `[[double-check-before-commit]]`: **ALWAYS verify every concrete
claim in the commit message against actual source/output BEFORE
staging.** Fixture names, file counts, exit codes, line counts, test
counts, helper names, smoke outcomes, SHA prefixes, regex matches, API
signatures, that a carve-out's named behavior is exercised by the test
body (S34), that the negative-control teeth fail on the wrong path (S35),
that the auth seam matches the production call-site signature (S36/S38),
that the container/directory-creation semantics match the emulator (S37),
and that a test URL with `key=value` segments is built by string-concat
not `as_uri()` (S38). No claims by pattern-completion. Build a
verification table (claim → reality → status) and reconcile before
"Confirm to commit?".

Specific to S39:
- Before claiming combined suite count, re-run pytest (baseline 983).
- Before claiming ruff/format clean, re-run ruff against touched files.
- Before claiming a SHA prefix, verify via
  `git show --no-patch --format=%h <ref>`.
- Before claiming a new-file LOC count, run `wc -l` (AFTER any
  ruff-format pass).
- For any live test, demonstrate teeth (a negative control that FAILS
  on the wrong path), not just a green run.
- For any adlfs auth claim, show the production call-site signature
  (kwarg vs env-resolved).

Avoid bash pipe artifacts that mask Python exit codes:
`python_cmd 2>&1 | grep ... | tail` makes `$?` reflect tail's exit. Use
`> stdout.out 2> stderr.err; echo $?` or `${PIPESTATUS[0]}`.

LESSONS-folded discoveries worth re-applying (S33-S38):
- Survey ADLS coverage by CLIENT STACK + read the AUTH seam from the
  call-site signature (S35/S36/S38).
- Pre-create the container via `fs.mkdir` for any adlfs write path; spike
  multiple partitions for write_to_dataset (S35/S37).
- Build test URLs with `key=value` segments by string-concat, NOT
  `Path.as_uri()` (S38).
- A carve-out claim must be verified against the test BODY (S34).
- A live-emulator fixture tears down on setup-phase failure; SDK-vs-
  emulator version skew is real (use `--skipApiVersionCheck`); distinct
  port + container per coexisting fixture (10000-10005 taken → 10006+).
- For a module with ZERO tests, a live-only test leaves no default-run
  coverage — add a hermetic guard (S38).
- Baseline bookkeeping: a new default-run test outside the canonical
  16-path does NOT raise the headline — record canonical / sub-suite /
  combined as three explicit numbers (S38).
- Confirm a lease/SAS candidate is real by grepping production FIRST
  (S38 anti-trap).
- The `rm -f`/`rm -rf`/`find -delete`/`os.remove` forms are
  env-hook-blocked — move throwaway helpers OUT of the repo tree via
  `mv <path> /tmp/`; operator runs destructive cleanup via `! rm ...`;
  in-fixture `docker rm -f` runs fine (S38).

---

## Commit hygiene (per LESSONS + S19-S38 additions)

- File-based commit messages at `/tmp/<id>-msg.txt`; commit with `-F`
  (no `-m` fallback); NO backticks in the body (S35 fold).
- Commit shape per Q-SHARED.1 (per-module default; single bundled commit
  only when the deliverable is genuinely one self-contained sub-surface).
- "Confirm to commit?" before EVERY commit. Pair with verification table
  (always) and `git diff --cached --stat` (confirm exactly the intended
  file count before committing — S35 fold).
- Commit body includes: action ref, scope summary, file touches, test
  count delta (net-new vs newly-in-invocation per S23), plan reference,
  and — for any carve-out — the test-body match + the demonstrated teeth
  + the auth-seam source-verification + (for write_dataset) the
  container-creation finding. NO `Co-Authored-By`.
- Pre-push gate must run green. Never use `--no-verify`.
- Pre-push vermin: `git ls-files '*.py' | xargs vermin --target=3.10`.
- Mid-implementation ruff format-check, not only pre-push.
- For S19-S38-test/fixture/workflow modifications: explicit Phase 2
  authorization required; document the scope in the commit body.
- Workspace close-out (Phase 6) lands as its own commit, followed by
  1-2 follow-up commits pinning the anchor SHA for S40.

---

## Context-window awareness

S38 ran Phase 0 → Phase 6 in a single context window with 2 repo commits
(Phase 0 verify + Phase 1 scope + Phase 2 source-verify + operator design
confirmation + Phase 3 impl with a build-time spike + a Phase-3 test-bug
fix + close-out + a baseline-clarity follow-up), comfortably within
budget. S39 budget per scope:

- Candidate A: medium (~370-400 LOC); only if unblocked.
- Candidate D: small; operator-led.
- No-ship session: small (Phase 0 verify + Phase 1 record + close-out).

Strategies:
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-service-backed test (unlikely at S39 — cluster closed),
  default to the S33-S38 fixture shape; distinct port 10006+; read the
  call-site signature for the auth seam; build-time spike before the
  final body.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before the chosen S39 scope closes, finish the
  in-flight sub-surface, then close session and refill the transition
  template for Session 40.

---

## Reporting in chat at session close

After all Session 39 commits land + push + close-out (or a no-ship
resolution is recorded) per the S13-38 pattern:

1. Commit SHA(s) of each S39 sub-surface (or "no repo commit — no-ship").
2. Sub-surface(s) landed (per candidate).
3. Test count delta: 970 canonical / 983 combined → S39 close.
4. Driver suite count at S39 close (52/52 expected).
5. Files touched per sub-surface.
6. Tag dispositions (the ADLS cluster is closed + tagged
   `adls-live-coverage-v0`; any NEW tag if a new surface shipped).
7. Per-tier cost-accounting wiring: CLOSED end-to-end since S28.
8. Live ADLS coverage status: cluster CLOSED at S38 (every adlfs write
   surface covered; `adls-live-coverage-v0` at `d610f0b`). Report S39's
   disposition if touched.
9. Any spend (LLM, infrastructure).
10. Verify-before-asking summary: source-verification findings.
11. Outstanding items for Session 40.
12. Tags state at S39 close (14 + any new).

Do not propose Phase 4 PR-D/E/F/G work unless Candidate D was chosen
and operator-led labeling is in flight.

---

## Carry-forward bakes (no amendment file needed)

All S38 close-out commits (`a27bb8d` primary + `4943d94` anchor-pin +
`685ed13` baseline-clarity) plus the S38 disposition have been folded
directly into this prompt — S39 does not need a separate amendment file:

- **S38 close-out anchors** folded into Step 0.1 (workspace anchor =
  `685ed13`/`4943d94`/`a27bb8d` + this prompt-drafting commit; repo anchor
  `d610f0b` with operator-eval_data-commit tolerance), Step 0.2 (14
  tags incl. the NEW `adls-live-coverage-v0`; `workstream-a-week2-end`
  superseded), Step 0.4 (cassettes/exclusions stay 30), Step 0.5
  (canonical 970, combined 983, the count-split caveat), Step 0.8 (the
  NEW prompt_logger hermetic guard expect-13 sub-suite), Step 0.9 (added
  the (a5) prompt_logger public-API check + the S38 live-test + hermetic
  guard presence checks via `check_s39_deliverables.py`).
- **5 NEW LESSONS sections from S38** (as_uri encoding; live-only test of
  a zero-test module; lease/SAS anti-trap; cross-workstream tag identity;
  baseline bookkeeping) referenced in the Verify-before-asking LESSONS
  list.
- **S38 candidate CLOSED** (prompt_logger adlfs leg + hermetic guard)
  folded into the carry-forward list + Scope section + Out-of-scope's S38
  deliverables (NEW LOCKS). **Every adlfs write surface now live-covered;
  the ADLS cluster is CLOSED + TAGGED.**
- **Candidate E still EXHAUSTED** (30 reached) — requires a plan-ceiling
  revision first.
- **lease/SAS is an ANTI-TRAP** (S38 grep-confirmed) — do NOT scope it.
- **Tag-taxonomy RESOLVED** — `adls-live-coverage-v0` placed at S38;
  1.TAG is no longer a pending decision.

If new amendments arise pre-S39 open, walk them per the
reviewer-feedback hygiene pattern above.
