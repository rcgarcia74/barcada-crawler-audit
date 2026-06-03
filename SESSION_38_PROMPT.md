# Session 38 prompt — scope picked at Phase 1
# (S37 closed a NEW candidate at repo f4e0a4a — fresh live ADLS
#  coverage for the PartitionedShardWriter Hive write_to_dataset path
#  [the SECOND half of output/parquet_writer.py, after S35's single-file
#  ShardWriter leg]. With S37 closed, output/parquet_writer.py is now
#  FULLY live-covered (both halves). That candidate is now CLOSED. S38
#  enters with the SAME near-empty warm-candidate queue as S33/.../S37:
#  A blocked / D operator-led / E exhausted. The fresh-candidate space has
#  NARROWED to ONE uncovered adlfs write surface [prompt_logger] plus the
#  lease/SAS cost-journal paths.)

**Drafted at Session 37 close (2026-06-03), operator-commissioned.**
Mirrors the S20/.../S36/S37 prompt structure. Scope-agnostic at
Phases 0/1; scope-specific design gates at Phase 2 per chosen
candidate. Strict 7-phase ordering with halt-on-mismatch preserved.

This prompt should be invoked from `~/crawler-audit/SESSION_38_PROMPT.md`.
Re-read it on session open.

---

## Scope

Engineering session. Repo HEAD at `f4e0a4a`
(WA2.W8.adls-live-partitioned-writer; S37). Workspace HEAD at the S37
close-out chain `bf52f8d` (primary close-out) + `965b55e` (anchor-pin)
+ `1a1d722` (forward notes) + any later prompt-drafting commit (see
Step 0.1). **Workstream 0 fully closed at S27 via the `workstream-0-end`
tag at `a1c5636`**.

Carry-forward candidates entering S38:

- **barcada-drift (Candidate A)** — deferred since S20; still needs
  4 AI/ML decisions per CLASSIFICATION_ADJACENT_PLAN.md §Item 8 AND
  2+ `canary_runs/*.parquet` files. **S37 re-confirmed empirically**
  that the launchd installer has NOT been run (no plist in
  `~/Library/LaunchAgents/`; 0 `canary_runs` parquets on disk). Same
  state as S29-S37 close. **Remains BLOCKED.**

- **Phase 4 PR-D tooling (Candidate D)** — operator-led labeling
  territory. W0-side unblocked since S27; still gated on
  operator-led Stage 2/3 labeling.

- **Cassette corpus expansion (Candidate E) — EXHAUSTED.** S32 grew
  the corpus to 30, the plan's stated upper bound (§4 W7
  "~20-30 representative domains"). **No further +N is available
  without first amending the plan ceiling** (a Phase 1/2 or
  plan-revision decision). Do NOT add cassettes under the current
  plan.

- **Parquet ShardWriter adlfs live coverage (S35 candidate) — CLOSED
  at S35** (`f80ccdc`, port 10002). NOT a carry-forward.

- **page_storage adlfs live coverage (S36 candidate) — CLOSED at S36**
  (`25c3696`, port 10003). NOT a carry-forward.

- **PartitionedShardWriter Hive adlfs live coverage (S37 candidate) —
  CLOSED at S37** (`f4e0a4a`, port 10004). The Hive
  `write_to_dataset(filesystem=fs)` path is now live-tested against
  Azurite via adlfs with the explicit `storage_options=` seam
  (`test_partitioned_shard_writer_adls_azurite.py`). **NOT a
  carry-forward.** With this, **`output/parquet_writer.py` is FULLY
  live-covered (both the single-file ShardWriter AND the Hive
  PartitionedShardWriter halves).**

**No new carry-forward introduced by S37.** The S37 deliverable was a
single commit (1 new live test file); the canonical 970 test count is
unchanged.

**Scope-availability note (IMPORTANT):** with A blocked, D
operator-led, E exhausted, and the S35+S36+S37 candidates now closed,
S38 may have **no clearly-actionable engineering scope** unless the
operator (a) unblocks A, (b) begins D labeling, (c) authorizes a
plan-ceiling revision to reopen E, or (d) commissions a NEW candidate.
**The remaining fresh-candidate space has narrowed to:**
  - `classifier/llm/prompt_logger.py` (the LAST uncovered adlfs write
    surface — fsspec `wb` single JSONL object via
    `PromptLogger.flush()`; **auth seam is ENV-resolved**, S36-style:
    `flush()` calls `fsspec.url_to_fs(self._output_url)` URL-only at
    line 118 with NO `storage_options` kwarg, then `fs.open(path,'wb')`
    at line 126);
  - lease/SAS/container-level **cost-journal** live paths (the
    azure-storage-blob SDK stack — NOT yet tested; only shared-key is).
    ONLY scope toward lease/SAS if source shows production constructs
    one (S34 anti-trap).
There is NO self-contained warm candidate remaining; each of the above
is a FRESH candidate scoped at Phase 2 from first principles. Surface
this at Phase 1 before the candidate-choice AskUserQuestion.

**S36+S37 auth-seam lesson — apply before scoping ANY adlfs candidate:**
read the production call site's SIGNATURE first. S35's `ShardWriter` and
S37's `PartitionedShardWriter` take an explicit `storage_options=` kwarg;
S36's `page_storage.write_pages` took NONE and resolved auth from
`AZURE_STORAGE_CONNECTION_STRING` in the environment. **`prompt_logger`
matches the S36 env-resolved shape** (`fsspec.url_to_fs(url)` URL-only) —
verify at source, do not assume.

**S37 container-creation lesson — apply before scoping ANY
write_to_dataset / write_dataset adlfs candidate:** pyarrow's
multi-partition `write_to_dataset` issues one `create_dir` per partition;
adlfs's `create_container` is NON-idempotent, so the 2nd partition raises
`ContainerAlreadyExists` → `ValueError` unless the container pre-exists.
Pre-create the container via `fs.mkdir` (catch `FileExistsError`) in the
fixture, and make the build-time spike WRITE MULTIPLE PARTITIONS against a
FRESH container to expose the race. (prompt_logger writes a single object,
not a partitioned dataset, so this specific trap does not apply to it —
but it WILL apply to any future `write_dataset` surface.)

Operator chooses at Phase 1 which candidate Session 38 ships.
Each candidate has its own Phase 2 design-gate template.

**Sessions 13-37 precedent:** this session does NOT modify the
W4.1.5 driver orchestration at `tests/runners/fixture_cascade/`
(locked at `dd64963` for original files; `cascade.py` extended at
`a1c5636`/S27 + `9afde57`/S28; `test_cost_journal_wiring.py` added at
`a1c5636`/S27 + modified at `ae9e627`/S28). Does NOT modify
`expected.schema.json` v1.1 / `META_SCHEMA.md` v1.1. Does NOT modify
the committed `tests/fixtures/baseline-v0/` snapshot at `9e9a1fb`.
Does NOT modify the Session 19-37 deliverables. Does NOT modify the
S31 cassette deliverables at `06d67c4` or the S32 cassette
deliverables at `cfa0ec1` — never re-records or deletes any of the
30. Does NOT modify the **S33 deliverable** at `f1cdce8`
(`test_cost_journal_adls_azurite.py` + the `live` marker in
`pyproject.toml`). Does NOT modify the **S34 deliverables** at
`eba6585` (`test_cost_journal_adls_azurite_concurrency.py` +
`.github/workflows/live-integration.yml`). Does NOT modify the **S35
deliverable** at `f80ccdc` (`test_parquet_writer_adls_azurite.py`).
Does NOT modify the **S36 deliverable** at `25c3696`
(`test_page_storage_adls_azurite.py`). Does NOT modify the **S37
deliverable** at `f4e0a4a` (`test_partitioned_shard_writer_adls_azurite.py`).

Does NOT modify production code under `src/barcada_scraper/` UNLESS
Phase 2 design-gate explicitly authorizes a specific module. Of the
S38 candidates: Candidate A would add a NEW `barcada-drift` module
(new file, not a modification of locked code); Candidate D is
tooling-only; the NEW adlfs-surface candidates are test-only (they
inject only public seams into already-locked production modules).

Full regression-protection checklist in **Out-of-scope** at the end
of this prompt. Re-read it before any code lands.

---

## Reviewer-feedback hygiene (if this prompt is reviewed)

If an external reviewer (operator-invoked) flags items in this prompt
before Session 38 starts, walk each flagged item against on-disk
reality at the workspace HEAD and repo HEAD `f4e0a4a`, BEFORE applying
any change. Per S19-S37 pattern:

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
was sequential). **S35 anchor:** the build-time validation spike caught
the adlfs `makedirs`-no-op gotcha BEFORE the test was committed. **S36
anchor:** the operator-flagged "forced env-var auth" challenge was
resolved at SOURCE before committing. **S37 anchor:** the build-time spike
caught adlfs's non-idempotent `create_container` across partitions BEFORE
the test body landed — fixed in-Phase-3 with a container pre-`mkdir`, not
surfaced as a post-commit HALT. Apply the same discipline: validate any
external-service interaction AND any auth-seam claim AND any
directory/container-creation semantics against the real source/emulator
before committing claims about it.

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

Run in order. Halt and surface to operator on any mismatch.

### Step 0.1 — Workspace + repo HEAD

```
git -C ~/crawler-audit rev-parse HEAD
# Expect: 1a1d722 (S37 forward notes) OR 965b55e (S37 anchor-pin) OR
# bf52f8d (S37 primary close-out) OR this S38 prompt-drafting commit
# succeeding it OR a later commit if additional workspace doc edits /
# prompt revisions landed. If N commits ahead of 1a1d722, verify each via
# `git log --oneline 1a1d722..HEAD` against expected prompt-finalization /
# doc-edit patterns; surface the SHA delta and request authorization if
# anything is unexpected. (S20-S37 precedent: operator authorized
# continuation when 1-4 extra workspace commits were the strengthened
# prompts themselves.)
#
# NOTE: SESSION_36_PROMPT.md carries an uncommitted operator-side edit left
# unstaged since S36 close. It may still be in the working tree at S38 open
# — tolerate it; it is operator territory.

git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: f4e0a4a (S37 WA2.W8.adls-live-partitioned-writer).
#
# Tolerated delta: operator-side eval_data labeling commits between
# S37 close and S38 open (Sessions 8-37 precedent). Verify via
# `git show --stat <sha>` for every commit in f4e0a4a..HEAD that each
# is strictly within eval_data/* (NO src/barcada_scraper/*, NO tests/*
# [INCLUDING the five Azurite live-test files], NO .github/*
# [INCLUDING live-integration.yml], NO scripts/*, NO docs/* touches);
# surface any non-eval_data delta for operator authorization before
# continuing.
```

### Step 0.2 — Tags (13 expected; unchanged from S30-S37 close)

```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort
# Expect 13 tags (UNCHANGED; S37 placed no tag per its 1.TAG = defer).
# NOTE there is NO week6-end — the workstream-0 week tags are
# 1/2/3/4-1-5/4/5/7 (7 week tags) PLUS workstream-0-end = 8
# workstream-0-* tags total:
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

git -C /Users/administrator/projects/barcada-scraper rev-list -n 1 workstream-0-end
# Expect: a1c5636… (UNCHANGED).

# CRITICAL (operator note at S37 close + S38 review): `workstream-a-week2-end`
# was OFFERED at S33 AND DEFERRED SIX TIMES (S33-S37) and is likely the WRONG
# tag name for the S33-S37 ADLS live-test cluster. BUT do NOT pre-assume a
# replacement letter either — the cluster is CROSS-WORKSTREAM (cost-journal
# S33/S34 = plan Workstream B; parquet S35/S37 = scraper output; page_storage
# S36 = Stage-2 acquisition), so `workstream-b-*` may be as wrong as the
# `-a-` name. Do NOT default-defer a SEVENTH time. See Sub-question 1.TAG: the
# off-session tag-taxonomy decision MUST be resolved at S38 Phase 1 (scope the
# cluster to the FIVE ADLS live tests only [robots/K-b excluded]; correct tag
# identity WITHOUT pre-assuming a workstream letter; + the bar that closes the
# cluster), not deferred by reflex.

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
# S29-S37 did NOT touch this surface.
```

### Step 0.4 — Fixture counts (use the Python rglob pattern, NOT bare find)

**UNCHANGED FROM S33/S34/S35/S36/S37**: S37 shipped a live test file, NOT a
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

### Step 0.5 — Test-suite baseline (S38 canonical)

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
# Sub-totals (16 paths; ALL identical to S27-S37 close — ALL FIVE
# Azurite live tests are @pytest.mark.live + skip-by-default and are
# NOT in this invocation; the 33 synthetic_crawl tests are hermetic):
#   210 conformance + 52 driver + 99 baseline_v0 +
#    33 synthetic_crawl + 32 robots + 30 robots_gate +
#    30 robots_bypass_config + 43 cost_journal +
#    13 cost_journal_local + 19 cost_journal_adls +
#    35 robots_integration + 74 vmss_worker +
#   129 job_runner + 152 worker_loop +
#     7 robots_gate_integration + 12 worker_loop_persistence = 970
#
# Pinned in SESSION_LOG.md "Canonical S37-close baseline" block.
```

The sub-paths add up to 970. Any drift = halt. If the headline
mismatches, re-run each sub-path independently to localize.

**Narrower baselines**:
- 480 (S22 headline; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 944 (canonical 16-path minus 19 cost_journal_adls minus 7
  robots_gate_integration).

Whichever baseline is bound at Phase 1, hold it consistent across ALL
Phase 3 commits in S38. The cumulative-test-count gate never lets it
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

# S35+S37 sub-surface (parquet writer hermetic suite — 33 file:// tests,
# 14 of which exercise PartitionedShardWriter; the default-run guard the
# S35 AND S37 live tests complement; unchanged):
.venv/bin/python -m pytest tests/test_parquet_writer.py -q              # expect 33

# S36 sub-surface (page_storage hermetic suite):
.venv/bin/python -m pytest tests/classifier/page_acquisition/test_page_storage.py -q  # expect 13
```

### Step 0.9 — S25-S37 invariants + cassette-dir + S33/S34/S35/S36/S37 live-test presence

**Coverage note**: equals S37's Step 0.9 plus a NEW check for the S37
deliverable. The env hook blocks inline `python -c` containing
`ast.parse` (S28) or Azure-credential-secrets references (S32/S33).

**PREFER the Write tool to stage the helper scripts, NOT the
`cat >…<<'PYEOF'` heredocs.** Empirically re-confirmed S33-S37: the
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

# (a3) S36 page_storage public API unchanged (inline-safe; the S36 live
# test depends on these public symbols, AND write_pages STILL takes no
# credential/storage_options param [env-resolved auth seam]):
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

# (a4) S37 PartitionedShardWriter public API unchanged (inline-safe; the
# S37 live test depends on the explicit storage_options= kwarg AND the
# partition_root property [the teeth surface]):
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

# (b) S26: CRAWLING_POLICY.md doc stability.
test "$(wc -l < docs/CRAWLING_POLICY.md)" = "77" && \
    test "$(wc -c < docs/CRAWLING_POLICY.md)" = "2519" || \
    { echo "HALT: CRAWLING_POLICY.md drifted"; exit 1; }
echo "OK docs/CRAWLING_POLICY.md unchanged (77 lines / 2519 bytes)"

# (c) S27+S28 per-tier wiring invariant smoke — stage to a file via Write
#     tool; run via .venv/bin/python (re-use S37's check body verbatim).

# (d) S28 ShardResult split field presence (inline-safe):
.venv/bin/python -c "
from barcada_scraper.classifier.stage1.run import ShardResult
fields = set(ShardResult.__dataclass_fields__.keys())
assert 'llm_cost_usd' in fields and 'embedding_cost_usd' in fields and 'cost_usd' in fields
assert len(fields) == 14, f'{len(fields)}: {fields}'
print('OK (d) S28 ShardResult 14 fields present')
"

# (d-cont.) S28 cascade.py Stage 1 invoker AST structure — stage via Write
#     tool (hook blocks inline ast.parse). Re-use S37's check_wiring body
#     (asserts _journal_record_with_breakdown + with_stage_cost_added +
#     with_shard_appended + update_with_retry present; _run_stage1 routes
#     via stage1_run.run_shard).

# (e) S29 K-b smoke script existence + AST parse — own Bash call (secrets).
#     Re-use S37's check body (220 LOC; main() defined; ast.parse OK).

# (f) S31+S32 cassettes (10) + S33 Azurite primitive + S34 race test +
#     S34 CI workflow + S35 parquet adlfs test + S36 page_storage adlfs
#     test + S37 partitioned adlfs test. Stage check_s38_deliverables.py
#     via the Write tool and run it:
```

Stage the following as `check_s38_deliverables.py` via the Write tool
(NOT a heredoc) and run `.venv/bin/python <path>`:

```python
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
assert '@pytest.mark.live' in ctext
assert 'update_with_retry' in ctext and 'with_shard_appended' in ctext
assert '_BLOB_PORT = 10001' in ctext, 'S34 fixture lost its distinct port'
assert '--skipApiVersionCheck' in ctext
# S34 CI workflow (posture).
wf = Path('.github/workflows/live-integration.yml')
assert wf.exists(), 'missing S34 live-integration CI workflow'
wtext = wf.read_text()
assert 'workflow_dispatch' in wtext
assert re.search(r"cron: '0 6 \* \* \*'", wtext)
assert not re.search(r'^  push:', wtext, re.M), 'workflow MUST NOT be push-triggered'
assert 'pull_request' not in wtext, 'workflow MUST NOT be PR-triggered'
assert '-m live' in wtext and 'tests/classifier/pipeline/' in wtext
# S35 parquet ShardWriter adlfs live test.
pq = Path('tests/classifier/pipeline/test_parquet_writer_adls_azurite.py')
assert pq.exists(), 'missing S35 parquet adlfs live test'
qtext = pq.read_text()
assert '@pytest.mark.live' in qtext
assert '_BLOB_PORT = 10002' in qtext, 'S35 fixture lost its distinct port'
assert 'barcada-azurite-parquet' in qtext
assert 'ShardWriter' in qtext and 'abfss://' in qtext
assert 'AzureBlobFileSystem' in qtext
assert '--skipApiVersionCheck' in qtext
# S36 page_storage adlfs live test.
ps = Path('tests/classifier/pipeline/test_page_storage_adls_azurite.py')
assert ps.exists(), 'missing S36 page_storage adlfs live test'
stext = ps.read_text()
assert '@pytest.mark.live' in stext
assert '_BLOB_PORT = 10003' in stext
assert 'barcada-azurite-pages' in stext
assert 'write_pages' in stext and 'abfss://' in stext
assert 'AZURE_STORAGE_CONNECTION_STRING' in stext
assert 'AzureBlobFileSystem' in stext
assert '--skipApiVersionCheck' in stext
# S37 PartitionedShardWriter adlfs live test.
pp = Path('tests/classifier/pipeline/test_partitioned_shard_writer_adls_azurite.py')
assert pp.exists(), 'missing S37 partitioned adlfs live test'
pptext = pp.read_text()
assert '@pytest.mark.live' in pptext, 'S37 test lost its live marker'
assert '_BLOB_PORT = 10004' in pptext, 'S37 fixture lost its distinct port (collides with S33-S36)'
assert 'barcada-azurite-partitioned' in pptext, 'S37 fixture lost its distinct container name'
assert 'PartitionedShardWriter' in pptext and 'write_to_dataset' in pptext, 'S37 test lost its Hive write_to_dataset drive'
assert 'HivePartitioning' in pptext, 'S37 test lost its dataset read-back'
assert 'storage_options=storage_options' in pptext, 'S37 test lost its explicit storage_options seam'
assert 'AzureBlobFileSystem' in pptext, 'S37 test lost its teeth (negative-control assertion)'
assert 'abfss://' in pptext
assert 'setup_fs.mkdir' in pptext, 'S37 test lost its container pre-mkdir (the non-idempotent create_container fix)'
assert '--skipApiVersionCheck' in pptext, 'S37 fixture lost the baked version-skew flag'
print('OK (f) S31+S32 cassettes (10) + S33 primitive + S34 race+CI + S35 parquet + S36 page_storage + S37 partitioned adlfs tests present (posture intact)')
```

If any of 0.1-0.9 fail, HALT before doing any work.

**Optional Docker-gated check (NOT a halt condition)**: if Docker is
available locally, the operator MAY confirm ALL FIVE live tests still
pass + coexist:
```
.venv/bin/python -m pytest -m live tests/classifier/pipeline/ -q
# Expect: 5 passed, 209 deselected (needs Docker + the Azurite image;
# SKIPS cleanly if absent). Ports S33=10000 / S34=10001 / S35=10002 /
# S36=10003 / S37=10004. Informational; Docker is NOT required for S38
# unless the chosen scope is new live-test work.
```

### Step 0.10 — Same-shape-test sweep (one-time; pre-implementation; NOT per-commit)

**Timing**: this is NOT part of the cold-start halt set (0.1-0.9). It
depends on the chosen scope, so run it ONCE the Phase 1 scope is fixed
and BEFORE Phase 3 begins — never inside the per-commit checkpoint loop.

```
# (S25 LESSONS) grep the test tree for same-shape tests that pin the
# contracts the chosen scope will modify (e.g. an existing hermetic test
# of the surface a new live test exercises, or a sibling that asserts a
# signature the scope changes). For prompt_logger: confirm whether a
# hermetic test of PromptLogger.flush() exists (the file:// default-run
# guard the new live test would complement, NOT replace).
```

If a same-shape test is found AND it is NOT in this prompt's explicit
replacement allowlist (Out-of-scope locks), do NOT silently modify or
replace it — surface it at Phase 1/2 as a design-gate sub-question
before writing any code. For a new live test of an already-covered
surface, confirm the new test ADDS coverage rather than
duplicating/replacing the hermetic guard.

---

## Required workspace reading (Session 38 first 10 minutes)

In this order:

1. **`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`** — full handoff
   state at S37 close. Lists scope candidates (A/D/E) with
   prerequisites + the named fresh-candidate adlfs surfaces. The
   S35+S36+S37 candidates are CLOSED; Candidate E is EXHAUSTED at 30.
   Note the explicit near-empty-warm-queue flag AND the **"S38 forward
   notes" section** (parquet completeness boundary + the tag-taxonomy
   correction that MUST be settled at Phase 1).

2. **`~/crawler-audit/SESSION_LOG.md`** Session 37 entry — the
   partitioned-path container-creation finding (non-idempotent
   create_container across partitions; fixture pre-mkdir fix); the
   explicit-storage_options auth seam; the negative-control teeth; the
   build-time spike; the 970 baseline re-pin; the operator tag-taxonomy
   note.

3. **`~/crawler-audit/LESSONS.md`** — re-read sections relevant to the
   chosen candidate:
   - **Mandatory regardless of candidate**: the S37 fold "the
     makedirs-no-op gotcha is SHARPER on the partitioned write_to_dataset
     path" + the S36 fold "Survey the AUTH seam, not just the client
     stack" + the S35 fold "adlfs is a SEPARATE ADLS write stack from the
     azure-storage-blob SDK" + the S34 fold "A carve-out claim must be
     verified against the test BODY".
   - **If a NEW live-service candidate**: the S33 fold (live-emulator
     teardown + version skew) + the S35 fold (survey by client stack;
     teeth = AzureBlobFileSystem + blob-relative path read back via a
     FRESH handle; DISTINCT port — 10000-10004 taken, so use 10005+) +
     the S36 fold (read the call-site signature to find the auth seam;
     clear_instance_cache before a URL-only resolution) + the S37 fold
     (pre-mkdir the container for write_dataset paths; multi-partition
     spike) + S30 posture-validation + the
     S24/S29/S30/S33/S34/S35/S36/S37 public-API-only pattern.
   - **If Candidate A**: S29 prereq-audit fold + S22-S37
     "Plan-vs-reality at Phase 2" + S29 LOC additive-overhead-floor +
     AI/ML decision gating.
   - **Only if the operator elects plan-amendment to reopen E**: the
     3 S32 + 3 S31 cassette folds.

4. **`~/crawler-audit/BARCADA_CRAWLER_REMEDIATION_PLAN.md`** —
   chosen-scope section. READ-ONLY by default; the only exception is
   the plan-amendment session shape (explicit operator authorization
   to edit §4 W7's "~20-30" ceiling). **ALSO read the FULL workstream
   taxonomy** if the tag-taxonomy decision (1.TAG) is being settled — to
   determine where the cross-workstream S33-S37 ADLS cluster maps (the
   cost-journal tests are Workstream B; the parquet + page_storage tests
   are NOT), or whether it warrants its own cross-cutting identity. Do NOT
   pre-assume `workstream-b-*` (Finding M).

5. **`~/crawler-audit/CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 —
   only if Candidate A (barcada-drift) is chosen.

6. For a NEW adlfs-surface candidate, the relevant production module +
   its hermetic test:
   - prompt_logger: `src/barcada_scraper/classifier/llm/prompt_logger.py`
     (the `PromptLogger.flush()` `fsspec.url_to_fs(url)` URL-only +
     `fs.open(path,'wb')` single-JSONL path; ENV-resolved auth) + any
     hermetic test of it + the S36 page_storage live test (closest
     ENV-resolved precedent).
   - cost journal lease/SAS: `cost_journal_adls.py` + the S33/S34 tests.
   - parquet (REFERENCE for explicit-storage_options shape):
     `src/barcada_scraper/output/parquet_writer.py` + the S35/S37 live
     tests.
   READ-ONLY unless a Phase 2 gate authorizes a specific file.

---

## Phase 1 — Scope resolution (no code; pre-design-gate)

**FIRST**: surface the scope-availability note (A blocked / D
operator-led / E exhausted / S35+S36+S37 candidates closed; NO
self-contained warm candidate remains; the named adlfs surfaces are
FRESH candidates — only prompt_logger + lease/SAS remain). S38 may have
no clearly-actionable engineering scope without operator action. Then
operator picks one.

### Three invocation shapes (S38 continues the empty-warm-queue condition)

- **Decided before invocation (cleaner).** Operator names the
  candidate when commissioning S38. Phase 1 CONFIRMS rather than
  elicits: skip the candidate-choice AskUserQuestion; still re-run the
  empirical prereq audit (for A: parquets + plist + AI/ML; for a fresh
  adlfs candidate: source-verify the surface is genuinely uncovered AND
  read its auth seam); proceed to that candidate's Phase 2 gate.

- **Decided at Phase 1 (more flexible).** S38 opens, Phase 0 verifies,
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
  sub-surface proceed under the proven S31/S32 mechanics.

### Candidate A — `barcada-drift` (AI/ML alignment + ≥2 parquets)

Per CLASSIFICATION_ADJACENT_PLAN.md §Item 8. Est ~300 LOC logic +
~70-100 LOC overhead ≈ **~370-400 LOC delivered**.

**Prerequisites:** 2+ `canary_runs/*.parquet` on operator's machine;
AI/ML responses on 4 §Item 8 decisions OR explicit operator-side
placeholder choices with "AI/ML-to-tune" notes.

**HALT IF** the 4 AI/ML decisions are not pre-resolved AND operator has
not authorized placeholders.

**Empirical prereq audit at S37 close** (carry-forward): 0 canary_runs
parquets; no barcada/canary/drift plist; no AI/ML responses. Re-run
these empirical checks at S38 Phase 1 BEFORE the candidate-choice
AskUserQuestion (S29 LESSONS). If unchanged, A remains blocked.

### Candidate D — Phase 4 PR-D operator-led labeling (operator territory)

Per plan §11 Risk Register. Stage 2 + Stage 3 labeling gates
PR-D/E/F/G. Operator-led; Claude Code's role limited to tooling.
W0-side unblocked at S27; still gated on operator-led labeling.

### Candidate E — Cassette corpus expansion (EXHAUSTED)

Reached the plan's **30 upper bound** at S32. **Not available** without
first amending the §4 W7 ceiling (made BEFORE any recording). Do NOT
add cassettes under the current plan. Mechanics proven (S31+S32).

### NEW candidate space (remaining uncovered adlfs surfaces — NARROWED)

With the S35+S36+S37 candidates closed, only ONE adlfs write surface
remains uncovered, plus the lease/SAS cost-journal paths:

- **prompt_logger adlfs leg** — `PromptLogger.flush()` writes a single
  JSONL object via `fsspec.url_to_fs(self._output_url)` (URL-only,
  line 118) + `fs.open(path, 'wb')` (line 126). **Auth seam =
  ENV-resolved (S36-style, NOT explicit-kwarg).** Mirror the S36
  page_storage live test (env-var `AZURE_STORAGE_CONNECTION_STRING`,
  clear_instance_cache) on port 10005. Single object, NOT a partitioned
  dataset — so the S37 multi-partition create_container trap does NOT
  apply; but the S35 makedirs-no-op fold (mkdir the container first
  before `open('wb')`) DOES.
- **cost-journal lease/SAS live paths** — the azure-storage-blob SDK
  stack; only shared-key is live-tested (S33/S34). ONLY scope toward
  lease/SAS if source shows production constructs one (S34 anti-trap).

Apply the same hygiene: source-verify before option-set design;
**read the call-site SIGNATURE to find the auth seam (S36 fold)**;
**verify any carve-out against the actual test body it implies (S34)**;
**survey coverage by CLIENT STACK (S35)**; **pre-mkdir the container for
any write_dataset path + multi-partition spike (S37)**; default new
external-service-backed tests to operator-smoke / live-on-demand posture
unless a named carve-out justifies CI (S30); if a new live fixture must
coexist with the S33-S37 fixtures, give it a DISTINCT port + container
name (10000/10001/10002/10003/10004 taken → use 10005+); size new
scripts with the ~70-100 LOC additive overhead floor.

### Sub-question 1.TAG — Tag at session close (pinned at Phase 1)

**This is NO LONGER a routine defer.** The operator flagged at S37 close
that `workstream-a-week2-end` (OFFERED+DEFERRED six times, S33-S37) is
likely the WRONG tag name for the S33-S37 ADLS live-test cluster.
**Resolve the tag-taxonomy decision explicitly at S38 Phase 1, do not
default-defer a seventh time:**

**FIRST — scope the cluster explicitly (Finding N, operator S38 review).**
S37's AskUserQuestion lumped W A.2 as "orchestrator robots + K-b +
Azurite primitive + …". That was too broad. **The cluster is HEREBY
SCOPED to the five ADLS live tests only — S33 (`f1cdce8`), S34
(`eba6585`), S35 (`f80ccdc`), S36 (`25c3696`), S37 (`f4e0a4a`). The
S23-S25 orchestrator-robots work and the S29/S30 K-b smoke
script/execution are EXCLUDED** — they are genuinely different work with
their own history, and must NOT be silently folded into this tag. Any
annotated tag placed for this cluster names ONLY the five live-test
commits.

1. **Correct tag identity — do NOT pre-assume a workstream letter
   (Finding M, operator S38 review).** Read
   BARCADA_CRAWLER_REMEDIATION_PLAN.md and note the cluster SPANS plan
   workstreams: the cost-journal live tests (S33/S34) map to plan
   Workstream B (Cost & Observability, W10-12), BUT the parquet-output
   live tests (S35/S37) are scraper-output infra and page_storage (S36)
   is Stage-2 page acquisition — **neither is cleanly Workstream B.**
   Pre-steering toward `workstream-b-*` would repeat the original
   `workstream-a-week2-end` error with a different letter. Evaluate
   whether the cluster maps to any SINGLE workstream tag at all, or
   whether a five-ADLS-test cross-cutting set warrants its OWN dedicated
   identity (e.g. `adls-live-coverage-*`) rather than a `workstream-N`
   lineage. Do NOT assume `workstream-b-*`. NOTE: the commit-subject
   prefix `WA2.W8.*` is a SEPARATE established convention
   (operator-flagged at S35/S36) and is NOT the tag name — do not
   conflate, and do not rewrite pushed commit subjects.
2. **The bar that CLOSES the cluster** — `output/parquet_writer.py` is
   now FULLY live-covered (both halves) as of S37, the natural parquet
   completeness boundary. Decide whether the cluster closes at the
   current coverage (cost-journal + parquet + page_storage) or stays open
   until prompt_logger + lease/SAS are also covered. Define the closing
   bar so the tag can be placed with a clear rationale.

Options at Phase 1:
- **Candidate A**: defer OR `barcada-drift-v0`.
- **Candidate D**: defer.
- **A NEW adlfs-surface candidate (or a no-ship session)**: resolve the
  tag-taxonomy decision above. If the operator settles the identity +
  closing bar AND considers the cluster closed, place the CORRECTLY-NAMED
  annotated tag (the name from the 1.TAG resolution — a cross-cutting
  `adls-live-coverage-*`-style identity or whatever the plan reconciliation
  yields; NOT a pre-assumed `workstream-b-*`) over the FIVE live-test
  commits only, rather than `workstream-a-week2-end`. If the operator
  wants the cluster to stay open (e.g. until prompt_logger lands), record
  that decision + the closing bar explicitly and defer with a rationale
  (NOT a reflex defer).

Phase 5 reads this resolution directly — no Phase 2 re-decision.

---

## Phase 2 — Design-gate elicitation (no code; AskUserQuestion)

Per chosen Phase 1 candidate. Source-verify at session-current HEAD per
the `[[verify-before-asking-discipline]]` AND the S22-S37
"Plan-vs-reality at Phase 2" + S25 "source-verify drives option-set
design" patterns BEFORE each AskUserQuestion batch.

**HALT IF** any Phase 2 decision would require modifications to
`src/barcada_scraper/` beyond what was Phase-2-authorized OR to the
W4.1.5 driver beyond the S16/S27/S28 exceptions OR to any S19-S37
deliverable (including the S33 Azurite test, the S34 concurrency test,
the S34 CI workflow, the S35 parquet adlfs test, the S36 page_storage
adlfs test, the S37 partitioned adlfs test, or re-recording/deleting any
of the 30 cassettes) — surface as a design-gate sub-question before
patching.

### CRITICAL Phase 2 hygiene

Carry forward S26/S28/S29/S30/S34/S35/S36/S37 hygiene verbatim: count
each Q-* option set (≤4 or tier/split); audit existing test pins for
by-design vs empirical; size new scripts with the ~70-100 LOC additive
overhead floor; default new external-service-backed tests to
live-on-demand posture unless a named carve-out justifies it; **when a
carve-out names a behavior (concurrency, atomicity, idempotency,
failover), point it at the specific test body that exercises it — or
narrow the wording to what the body actually does (S34 fold)**;
**demonstrate teeth via a negative control, not just a green run (S34/S35
fold)**; **read the production call-site SIGNATURE to determine the auth
seam before designing the auth option (S36 fold)**; and **for any
write_dataset path, pre-create the container + spike multiple partitions
(S37 fold)**.

### If Candidate A (barcada-drift)

Carry-forward (unchanged): Q-A.1 CLI namespace; Q-A.2 drift metric;
Q-A.3 alert threshold; Q-A.4 input contract; Q-A.5 output shape;
Q-A.6 test corpus. (Split into 2-3 sequential AskUserQuestion calls;
both the 4-options-per-question and 4-questions-per-call caps apply.)

### If Candidate D (Phase 4 PR-D tooling)

- **Q-D.1 Tooling shape**: batch validators / import scripts / hygiene
  tools. Operator-led design.

### If a NEW adlfs-surface candidate (prompt_logger / lease-SAS)

Design the gates from first principles at session time, anchored on the
**S36 (env-resolved) / S35+S37 (explicit-kwarg) live-test shapes**:
- Live marker, skip-by-default, Docker-gated, self-reproducing fixture
  with unconditional try/finally teardown + self-healing pre-clean,
  baked `--skipApiVersionCheck`, DISTINCT port 10005+ + container name.
- **AUTH SEAM (S36): read the production call site's signature.** For
  prompt_logger, `flush()` calls `fsspec.url_to_fs(self._output_url)`
  URL-only (no `storage_options`) → ENV-resolved: set
  `AZURE_STORAGE_CONNECTION_STRING` (via `monkeypatch.setenv`) and clear
  the adlfs instance cache before the production call (S36 pattern).
  Verify which, do not assume.
- Container creation via `fs.mkdir` (catch `FileExistsError`), NOT
  `makedirs(..., exist_ok=True)` which silently no-ops (S35 fold). For a
  write_dataset path also heed the S37 multi-partition create_container
  trap (N/A for prompt_logger's single-object write, but verify).
- Teeth: assert the resolved fs is `AzureBlobFileSystem` AND a
  blob-relative path; read the artifact back through a FRESH adlfs
  handle; demonstrate the negative control fails on a `file://` fallback
  (LocalFileSystem + absolute path).
- Decide explicitly whether it joins the CI workflow's `-m live` dir
  selection (auto-picked-up if placed under
  `tests/classifier/pipeline/`) and keep the skip-fail guard meaningful.

### Shared sub-questions (all candidates)

- **Q-SHARED.1 Commit shape**: per-module / per-sub-surface (S18-S37
  default; Recommended) vs single bundled commit (only when genuinely
  one self-contained sub-surface, as the S35+S36+S37 single live test
  files were).

(Tag-at-close resolved at Phase 1 Sub-question 1.TAG.)

---

## Phase 3 — Implementation (per chosen commit shape, strict order)

### Non-interleaving rule (CRITICAL for bisectability)

If the chosen candidate has multiple sub-surfaces, complete each fully
before starting the next. Per S22-S37 precedent. If a mid-sub-surface
dependency emerges, HALT and surface as a design-gate sub-question.

### Build-time validation spike (carry the S35/S36/S37 emphasis)

For any external-service-backed test, BEFORE writing the final test
body: stand up the emulator and drive the REAL production code through
it in a throwaway spike (staged via the Write tool). Confirm the URL
form, the auth mechanism (kwarg vs env — S36), the resolved-fs type,
the directory/container-creation semantics (S35 makedirs-no-op; S37
non-idempotent create_container across partitions — drive MULTIPLE
partitions against a FRESH container if the path is a write_dataset),
and a full round-trip (write → read back via a FRESH handle). This
catches version-skew and API-semantic gotchas inside Phase 3 instead of
as a post-commit HALT. Tear the spike container down (it is `--rm`;
`docker stop` auto-removes — note that the agent's Bash `rm -f` is
env-hook-blocked, but `docker stop` and in-fixture `docker rm -f` are
fine). Clean up the spike script after (it must NOT be committed).

### Per-commit checkpoint protocol (single source of truth)

At EVERY Phase 3 commit boundary, run these 6 steps IN ORDER:

**1. Combined suite**

```
.venv/bin/python -m pytest \
    <the canonical 16-path invocation from Step 0.5> \
    <new S38 test paths if any> -q
# A new @pytest.mark.live test stays OUT of the canonical headline
# unless a deliberate decision adds it (S33/S34/S35/S36/S37 Option-1
# posture). If placed under tests/classifier/pipeline/, it is
# auto-picked-up by the CI workflow's `-m live` selection but NOT by the
# canonical 16-path. Verify a new live test out-of-band:
# `pytest -m live tests/classifier/pipeline/` (expect 5 + N).
```

Expected: previous_baseline + N new tests, all passing. If failing
tests are NOT a deliberate consequence of the surface-under-test →
HALT.

**2. Ruff sanity (touched files only) + mid-implementation format check**

```
.venv/bin/ruff check <touched paths>
.venv/bin/ruff format --check <touched paths>
# (ruff is Python-only; a YAML/workflow-only change has no ruff-touched
# files — note that explicitly rather than asserting a clean ruff run
# on a non-Python file, per S34. A new Python test file WILL likely need
# `ruff format` once — S35/S36/S37 each reformatted once. Apply it,
# re-check, re-run the test.)
```

**3. Verification table (build in chat per `[[double-check-before-commit]]`)**

Build a claim → reality → status table for every concrete claim in the
draft commit message. Any ✗ → fix the claim BEFORE staging. Distinguish
net-new tests from newly-in-invocation pre-existing tests (S23). For
exit-code claims use `cmd > /tmp/out 2> /tmp/err; echo "Exit: $?"`. For
new-file LOC claims use `wc -l` AFTER any ruff-format pass (S29; S35's
LOC dropped 317→309 after format; S37 reformatted to 389). **For any
live test, include a teeth check** (a negative control demonstrated to
FAIL on the wrong path) in the table, not just "it passes" (S34/S35/S37).

**4. `git status` check**

Only intended files staged; no surprise `eval_data/` or unauthorized
`src/` changes. Operator-side `eval_data/` modifications stay unstaged.

**5. "Confirm to commit?" presented to operator**

Include: verification table; commit message file location
(`/tmp/<id>-msg.txt`); file list to stage (M / A / D). Confirm the
commit subject's workstream label reconciles with the decision record
(`WA2.W8.*` is the established commit-prefix for this surface family —
S35/S36/S37 operator-flagged this; verify against prior commits +
SESSION_LOG before committing). Commit message uses `-F` (no `-m`
fallback) and contains NO backticks in the body (S35 fold). NO
`Co-Authored-By`.

**6. After operator confirms**

Stage + commit + verify the new SHA (`git log --oneline -1`) + verify
combined suite still passes on the new HEAD.

### Cumulative test-count gate

Track combined-suite passing count at each commit boundary. The count
NEVER decreases between checkpoints. Authorized decreases ONLY for a
Q-*-authorized same-shape 1↔1 replacement (cite the authorization +
name replaced + replacement in the commit body). Baseline bound at
Phase 1: **970** (canonical 16-path). A new live-marked test does NOT
raise the canonical headline — verify it out-of-band per the
S33/S34/S35/S36/S37 pattern (`pytest -m live tests/classifier/pipeline/`).

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
edits to `eval_data/*` can fail the gate even though no S38 commit
touches eval_data. When this fires:
1. Confirm the failing row is operator-WIP (`git diff eval_data/`),
   not committed HEAD (`git show HEAD:eval_data/...`).
2. Confirm the S38 commits do not touch eval_data
   (`git diff origin/main..HEAD -- eval_data/`).
3. Surface to operator with the exact row + reason + diff.
4. Two paths: (a) operator-fix in WT, re-run gate; (b) stash eval_data
   WIP, push, restore.
5. Do NOT auto-fix locked-artifact content.

S20+S22 precedent: operator chose (a). S21/S23-S37 did not need this
protocol at push (the gate ran clean).

---

## Phase 5 — Push + tag

- Push to `origin/main` after operator confirms.
- Tag per Phase 1 Sub-question 1.TAG decision (the tag-taxonomy
  resolution — the correctly-named tag from the 1.TAG resolution if the
  cluster is declared closed, OR an explicit rationale-backed defer; NOT a
  reflex `workstream-a-week2-end` defer, and NOT a pre-assumed
  `workstream-b-*` either).

If a tag is placed: include an annotated message naming
every sub-surface commit + mapping to plan bullets + listing
deferrals (mirror `workstream-a-week1-end` / `workstream-0-end`). If the
S33-S37 ADLS cluster tag is placed, scope it to the FIVE ADLS live-test
commits ONLY — `f1cdce8` S33, `eba6585` S34, `f80ccdc` S35, `25c3696`
S36, `f4e0a4a` S37 — and EXCLUDE the S23-S25 robots + S29/S30 K-b history
(Finding N: those were loosely lumped into the S37 "W A.2" framing but are
genuinely different work). Cite the parquet completeness boundary as part
of the closing rationale.

Note: workstream-0-end placed at S27. W A.1 closed at S22's
`workstream-a-week1-end`. The ADLS live-test cluster (S33-S37) is the
subject of the pending tag-taxonomy decision (1.TAG).

---

## Phase 6 — Workspace close-out

- Append Session 38 entry to `~/crawler-audit/SESSION_LOG.md` including
  a **Canonical S38-close baseline** block with the exact pytest
  invocation + verified count (per S22-S37 LESSONS). **If the fixture
  count changes (only via a plan-ceiling revision reopening E), record
  the new count with the exact variable names `cassette_count == N` /
  `exclusions_count == N` as the S39 Phase 0 Step 0.4 forward note.**
  Otherwise pin `cassette_count == 30` / `exclusions_count == 30`.
- Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md` for Session
  39 — explicitly pin the S39 Phase 0 workspace anchor SHA per the
  S21-S37 post-audit pattern. After the close-out commit lands, expect
  **1-2 follow-up commits** pinning the actual SHA. **Carry forward the
  tag-taxonomy resolution** (what was decided at S38, or what remains
  pending) so S39 inherits a settled answer rather than the drift.
- Update `~/crawler-audit/LESSONS.md` with any new forward-applicable
  patterns.
- Workspace close-out: 1 primary commit + 1-2 follow-up commits. Push
  workspace after operator confirms.

Note: drafting the next-session prompt (`SESSION_39_PROMPT.md`) is NOT
a built-in Phase 6 step. Per S20→S37 precedent, prompt-drafting is
operator-commissioned between sessions. If the operator asks for it
explicitly at S38 close, draft it as a separate follow-up.

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

### A NEW adlfs-surface (or lease/SAS) candidate
0. Phase 1 carve-out / justification recorded in chat (the surface is
   genuinely uncovered by the EXISTING client-stack coverage), **with
   the carve-out matched to the actual test body (S34), the auth seam
   read from source (S36), a demonstrated negative-control teeth check
   (S35), and the container-creation semantics validated in a spike
   (S37)**.
1. Acceptance defined at the Phase 2 gate when the candidate is scoped.

### Shared (all candidates additionally satisfy)
- **S1.** Combined suite at session close: 970 baseline + N new tests,
  all passing. A new live-marked test stays out of the canonical
  headline (verified out-of-band; `pytest -m live tests/classifier/pipeline/`
  → 5 + N passed).
- **S2.** Pre-push gate green (incl. eval_data WIP halt protocol).
- **S3.** Tag-taxonomy decision (1.TAG) resolved — cluster scoped to the
  five ADLS live tests (robots/K-b excluded), correctly-named tag placed
  (no pre-assumed `workstream-b-*`) OR explicit rationale-backed defer
  (NOT a reflex defer).
- **S4.** Regression-protection checklist held (see Out-of-scope). In
  particular: ALL S21-S37 deliverables stay at their SHAs; their public
  APIs unchanged; the 5 S31 + 5 S32 cassettes stay at `06d67c4` /
  `cfa0ec1`; the S33 Azurite test + live marker stay at `f1cdce8`; the
  S34 concurrency test + CI workflow stay at `eba6585` (workflow stays
  OFF push/PR); the S35 parquet adlfs test stays at `f80ccdc` (port
  10002); the S36 page_storage adlfs test stays at `25c3696` (port
  10003, env-var auth); the S37 partitioned adlfs test stays at `f4e0a4a`
  (port 10004, explicit storage_options, write_to_dataset/HivePartitioning
  drive, container pre-mkdir, AzureBlobFileSystem teeth intact);
  per-sub-suite counts stay green; CRAWLING_POLICY.md 77 lines / 2519
  bytes; the combined total stays at 970 (or grows) unless a Q-*
  authorizes a same-shape 1↔1 replacement.

---

## Out-of-scope (no exceptions without operator authorization)

Per the regression-protection checklist. **S37 added one new lock**
(the PartitionedShardWriter adlfs live test at `f4e0a4a`); otherwise
unchanged from the S37 prompt.

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

**S34 deliverables:**
- `tests/classifier/pipeline/test_cost_journal_adls_azurite_concurrency.py`
  at `eba6585` (337 LOC; 1 `@pytest.mark.live` multi-writer race test
  on a DISTINCT port 10001 / container `barcada-azurite-racetest`). Do
  NOT modify without Phase 2 authorization.
- `.github/workflows/live-integration.yml` at `eba6585` — CI workflow.
  `workflow_dispatch` + nightly `schedule` (cron `0 6 * * *`); **MUST
  NOT** be push/PR-triggered. Runs `pytest -m live tests/classifier/pipeline/`
  with a skip-robust count-agnostic guard. Do NOT weaken the guard or
  the trigger posture without a deliberate Phase 2 decision.

**S35 deliverables:**
- `tests/classifier/pipeline/test_parquet_writer_adls_azurite.py` at
  `f80ccdc` — 309 LOC; 1 `@pytest.mark.live` test driving the
  production `output/parquet_writer.py::ShardWriter` against Azurite via
  `adlfs.AzureBlobFileSystem` (shared-key connection string via the
  explicit `storage_options=` kwarg) on a DISTINCT port 10002 /
  container `barcada-azurite-parquet`. Teeth: resolved fs is
  `AzureBlobFileSystem` + blob-relative `final_path`, read back via a
  FRESH adlfs handle. Auto-joins the CI workflow's `-m live` dir
  selection. `tests/test_parquet_writer.py` (33 hermetic file:// tests)
  remains the default-run guard.

**S36 deliverables:**
- `tests/classifier/pipeline/test_page_storage_adls_azurite.py` at
  `25c3696` — 343 LOC; 1 `@pytest.mark.live` test driving the
  production `classifier/page_acquisition/page_storage.py::write_pages`
  against Azurite via `adlfs.AzureBlobFileSystem` on a DISTINCT port
  10003 / container `barcada-azurite-pages`. **AUTH SEAM: `write_pages`
  takes NO `storage_options` kwarg; the test authenticates adlfs via the
  `AZURE_STORAGE_CONNECTION_STRING` env var (`monkeypatch.setenv`).**
  Teeth: resolved fs is `AzureBlobFileSystem` + blob-relative path, read
  back via a FRESH adlfs handle; negative control = a `file://` fallback
  resolves to `LocalFileSystem` with an absolute path. Auto-joins the CI
  workflow's `-m live` dir selection. `tests/classifier/page_acquisition/
  test_page_storage.py` (13 hermetic file:// tests) remains the
  default-run guard for the module.

**S37 deliverables (NEW LOCK):**
- `tests/classifier/pipeline/test_partitioned_shard_writer_adls_azurite.py`
  at `f4e0a4a` — 389 LOC; 1 `@pytest.mark.live` test driving the
  production `output/parquet_writer.py::PartitionedShardWriter` Hive
  `pq.write_to_dataset(filesystem=fs, partition_cols=...)` path against
  Azurite via `adlfs.AzureBlobFileSystem` on a DISTINCT port 10004 /
  container `barcada-azurite-partitioned` (coexists with S33=10000 +
  S34=10001 + S35=10002 + S36=10003 under one `-m live` run). **AUTH SEAM
  (same as S35): explicit `storage_options=` kwarg.** The body writes
  three records deriving three Hive partitions, then reads the dataset
  back via a FRESH adlfs handle with `pyarrow.dataset.HivePartitioning`.
  **Container is pre-created via `fs.mkdir` (catch `FileExistsError`)** —
  required because pyarrow's multi-partition `write_to_dataset` hits
  adlfs's non-idempotent `create_container` (the S37 finding). Teeth:
  resolved fs is `AzureBlobFileSystem` + blob-relative `partition_root`;
  negative control = a `file://` writer resolves to `LocalFileSystem`
  with an absolute path. Auto-joins the CI workflow's `-m live` dir
  selection. Do NOT modify without Phase 2 authorization. **With S37,
  `output/parquet_writer.py` is FULLY live-covered (both ShardWriter and
  PartitionedShardWriter halves) via the public `storage_options=` seam;
  the module is UNMODIFIED — keep it that way.**

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
expected and unstaged (Sessions 8-37); inter-session operator-side
eval_data COMMITS tolerated per "Workspace HEAD delta tolerance" (verify
eval_data-only via `git show --stat`). 2 operator-side stage1 TAGS point
at eval_data-only commits.

**Production code:** `src/barcada_scraper/` — locked unless Phase 2
authorizes a specific module. S21-S25+S28 authorized. S26+S27+S29+S30+
S31+S32+S33+S34+S35+S36+S37 added no new src/ authorizations (S35+S36+S37
were test only).

**Pipeline configs:** `configs/`.

**CI workflows:** `.github/workflows/` — `python-package.yml` and
`build-and-push-image.yml` are pre-existing; `live-integration.yml` is
the S34 lock. New workflows require a Phase 2 design-gate.

**Phase 4 work:** PR-D/E/F/G W0-side unblocked since S27; still gated
on operator-led Stage 2/3 labeling.

---

## Verify-before-asking discipline (strict rule from S19-S37)

Per `[[double-check-before-commit]]`: **ALWAYS verify every concrete
claim in the commit message against actual source/output BEFORE
staging.** Fixture names, file counts, exit codes, line counts, test
counts, helper names, smoke outcomes, SHA prefixes, regex matches, API
signatures, **that a carve-out's named behavior is actually exercised
by the test body (S34)**, **that the negative-control teeth fail on the
wrong path (S35)**, **that the auth seam claim matches the production
call-site signature (S36)**, and **that the container/directory-creation
semantics match what the emulator does (S37)**. No claims by
pattern-completion. Build a verification table (claim → reality →
status) and reconcile before "Confirm to commit?".

Specific to S38:
- Before claiming combined suite count, re-run pytest.
- Before claiming ruff/format clean, re-run ruff against touched files
  (note when a change is YAML-only with no ruff-touched files).
- Before claiming a SHA prefix, verify via
  `git show --no-patch --format=%h <ref>`.
- Before claiming a new-file LOC count, run `wc -l` (AFTER any
  ruff-format pass).
- For any live test, demonstrate teeth (a negative control that FAILS
  on the wrong path), not just a green run.
- For any adlfs auth claim, show the production call-site signature
  (kwarg vs env-resolved).
- For any write_dataset path, show the spike's multi-partition
  container-creation result.
- Before committing, confirm the subject's `WA2.W8.*` workstream label
  reconciles with the decision record (commit-prefix convention, distinct
  from the tag-taxonomy decision).

Avoid bash pipe artifacts that mask Python exit codes:
`python_cmd 2>&1 | grep ... | tail` makes `$?` reflect tail's exit. Use
`> stdout.out 2> stderr.err; echo $?` or `${PIPESTATUS[0]}`.

LESSONS-folded discoveries worth re-applying:
- **The makedirs-no-op gotcha is SHARPER on the partitioned
  write_to_dataset path: pyarrow's per-partition create_dir hits adlfs's
  non-idempotent create_container (S37).** Pre-create the container via
  `fs.mkdir` (catch `FileExistsError`); spike MULTIPLE partitions against
  a FRESH container to expose it.
- **Survey the AUTH seam, not just the client stack — an adlfs write
  surface may resolve credentials from the URL + environment (no
  `storage_options` kwarg) (S36).** Read the call-site signature; clear
  the fsspec instance cache before a URL-only resolution.
- **adlfs is a SEPARATE ADLS write stack from the azure-storage-blob
  SDK — survey coverage by client stack (S35).** adlfs
  `makedirs(container, exist_ok=True)` silently no-ops; use `mkdir`
  (catch `FileExistsError`). Teeth = `AzureBlobFileSystem` +
  blob-relative path + read-back via a FRESH handle.
- **A carve-out claim must be verified against the test BODY, not its
  name/marker; re-verify when CI-wiring an existing test (S34).**
- A live-emulator fixture must tear down on setup-phase failure
  (try/finally wrapping the WHOLE setup); SDK-vs-emulator version skew
  is real (use the emulator-side compatibility flag) (S33). A coexisting
  live fixture needs a DISTINCT port + container name (S34/S35/S36/S37:
  10000/10001/10002/10003/10004 taken → 10005+).
- A build-time spike against the real emulator catches API-semantic
  gotchas inside Phase 3 instead of as a post-commit HALT (S35/S36/S37).
- Operator-smoke posture (K-b) vs permanent CI (needs a named carve-out)
  (S30); a permanent test shipped under Option 1 is live-on-demand, NOT
  default-CI (S33); wiring it to a workflow keeps it off push/PR unless
  deliberately escalated (S34).
- Plan-vs-reality at Phase 2 (S22); source-verify drives option-set
  design (S25; S28-S37).
- Test against public API surface only (S24; S29/S30/S33/S34/S35/S36/S37).
- AskUserQuestion 4-option limit can silently truncate (S26).
- Empirical-vs-by-design distinction in test pins (S28).
- Phase 0 fixture-count commands need the Python rglob() pattern, NOT
  bare `find` (S28 post-close).
- Markdown-rendered shell commands may carry NBSP / the env hook blocks
  secrets-referencing inline `python -c`; stage scripts to a file via
  the Write tool when exactness matters (S34/S35/S36/S37).
- Operator-driven script LOC: ~70-100 LOC additive overhead floor (S29).
- Empirical Phase 1 prerequisite check before scope-narrow (S29; S30-S37
  re-validated — Candidate A unchanged).
- Reject-cassette cleanup is a two-step asymmetric pattern; `rm`/`find
  -delete` are env-hook-blocked — operator runs `! rm -rf` at close
  (S31; S32 confirmed; S35 re-confirmed: an agent-side `docker rm -f`
  pre-clean tripped the destructive-op hook, but `docker stop` and
  in-fixture `docker rm -f` run fine).
- **Tag-taxonomy drift: `workstream-a-week2-end` is the wrong name for
  the S33-S37 ADLS live-test cluster (operator note, S37 close) — but the
  cluster is CROSS-WORKSTREAM (cost-journal S33/S34 = plan Workstream B;
  parquet S35/S37 = scraper output; page_storage S36 = Stage-2
  acquisition), so do NOT pre-assume `workstream-b-*` either; it may
  warrant its own cross-cutting identity (Finding M, S38 review). Scope
  the cluster to the FIVE ADLS live tests only — robots/K-b excluded
  (Finding N, S38 review). Settle the identity + closing bar at S38 Phase
  1, do not default-defer (see Sub-question 1.TAG).**

---

## Commit hygiene (per LESSONS + S19-S37 additions)

- File-based commit messages at `/tmp/<id>-msg.txt`; commit with `-F`
  (no `-m` fallback); NO backticks in the body (S35 fold).
- Commit shape per Q-SHARED.1 (per-module default; single bundled commit
  only when the deliverable is genuinely one self-contained sub-surface,
  as the S35+S36+S37 single live test files were).
- "Confirm to commit?" before EVERY commit. Pair with verification table
  (always) and `git diff --cached --stat` (confirm exactly the intended
  file count before committing — S35 fold).
- Commit body includes: action ref, scope summary, file touches, test
  count delta (net-new vs newly-in-invocation per S23), plan reference,
  and — for any carve-out — the test-body match + the demonstrated teeth
  + the auth-seam source-verification + (for write_dataset) the
  container-creation finding (S34/S35/S36/S37). NO `Co-Authored-By`.
- Pre-push gate must run green. Never use `--no-verify`.
- Pre-push vermin: `git ls-files '*.py' | xargs vermin --target=3.10` to
  filter venv-internal false-positives.
- Mid-implementation ruff format-check, not only pre-push.
- For S19-S37-test/fixture/workflow modifications: explicit Phase 2
  authorization required; document the scope in the commit body.
- Workspace close-out (Phase 6) lands as its own commit, followed by
  1-2 follow-up commits pinning the anchor SHA for S39.

---

## Context-window awareness

S37 ran Phase 0 → Phase 6 in a single context window with 1 repo commit
(Phase 0 verify + Phase 1 scope + Phase 2 source-verify + operator design
confirmation + Phase 3 impl with a build-time spike that caught the
container-creation race + close-out + the operator's two forward notes
folded in), comfortably within budget. S38 budget per scope:

- Candidate A: medium (~370-400 LOC); only if unblocked.
- Candidate D: small; operator-led.
- A NEW adlfs-surface candidate (prompt_logger / lease-SAS):
  small-to-medium; size at Phase 2; mirror the S36 (env-resolved) or
  S35/S37 (explicit-kwarg) single-live-test shape.

Strategies:
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-service-backed test, default to the S33/S34/S35/S36/S37
  fixture shape: unconditional try/finally teardown + idempotent
  self-healing pre-clean + skip-if-unavailable; expect an
  SDK-vs-emulator version-skew flag may be needed; use a DISTINCT port +
  container name (10005+) if coexisting; container creation via `mkdir`
  not `makedirs(exist_ok=True)`; for a write_dataset path pre-mkdir the
  container + spike multiple partitions; read the call-site signature for
  the auth seam (kwarg vs env); keep the test off the canonical headline
  (live marker, skip-by-default) unless a deliberate decision adds it;
  run a build-time spike before writing the final body.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before the chosen S38 scope closes, finish the
  in-flight sub-surface, then close session and refill the transition
  template for Session 39.

---

## Reporting in chat at session close

After all Session 38 commits land + push + close-out per the S13-37
pattern:

1. Commit SHA(s) of each S38 sub-surface.
2. Sub-surface(s) landed (per candidate).
3. Test count delta: 970 baseline → S38 close.
4. Driver suite count at S38 close (52/52 expected).
5. Files touched per sub-surface.
6. Tag dispositions (incl. the tag-taxonomy resolution per 1.TAG).
7. Per-tier cost-accounting wiring: CLOSED end-to-end since S28.
8. Live ADLS coverage status: K-b SHIP S29; K-b EXEC S30; K-a Azurite
   primitive S33; K-a CI wiring + multi-writer concurrency S34; parquet
   ShardWriter adlfs leg S35; page_storage adlfs leg S36; PartitionedShardWriter
   Hive adlfs leg S37 (parquet_writer.py FULLY covered). Report S38's
   disposition if touched.
9. Any spend (LLM, infrastructure).
10. Verify-before-asking summary: source-verification findings.
11. Outstanding items for Session 39.
12. Tags state at S38 close (incl. the tag-taxonomy resolution).

Do not propose Phase 4 PR-D/E/F/G work unless Candidate D was chosen
and operator-led labeling is in flight.

---

## Carry-forward bakes (no amendment file needed)

All S37 close-out commits (`bf52f8d` primary + `965b55e` anchor-pin +
`1a1d722` forward notes) plus the S37 disposition have been folded
directly into this prompt — S38 does not need a separate amendment file:

- **S37 close-out anchors** folded into Step 0.1 (workspace anchor =
  `1a1d722`/`965b55e`/`bf52f8d` + this prompt-drafting commit; repo anchor
  `f4e0a4a` with operator-eval_data-commit tolerance), Step 0.2 (13
  tags, unchanged + the tag-taxonomy CRITICAL note), Step 0.4
  (cassettes/exclusions stay 30), Step 0.5 (canonical 970), Step 0.8
  (the parquet hermetic 33-test sub-suite covers PartitionedShardWriter),
  Step 0.9 (added the S37 deliverable presence + posture check via
  `check_s38_deliverables.py` + the (a4) PartitionedShardWriter
  public-API check).
- **1 NEW LESSONS section from S37** ("the makedirs-no-op gotcha is
  sharper on the partitioned write_to_dataset path") referenced in the
  Verify-before-asking LESSONS list.
- **S37 candidate CLOSED** (PartitionedShardWriter adlfs leg) folded into
  the carry-forward list + Scope section + Out-of-scope's S37 deliverable
  (NEW LOCK). **parquet_writer.py now FULLY live-covered (both halves).**
- **Candidate E still EXHAUSTED** (30 reached) — requires a
  plan-ceiling revision first.
- **NEW candidate space NARROWED** — only `prompt_logger` (ENV-resolved
  auth, S36-style) + lease/SAS cost-journal paths remain adlfs-uncovered.
- **Tag-taxonomy decision ELEVATED** — `workstream-a-week2-end` is the
  wrong name for the S33-S37 ADLS cluster (operator note, S37 close). S38
  review (Findings M + N) sharpened this: (M) the cluster is
  CROSS-WORKSTREAM, so do NOT pre-assume `workstream-b-*` — it may warrant
  its own cross-cutting identity; (N) scope the cluster to the FIVE ADLS
  live tests only (robots/K-b excluded — they were loosely lumped into the
  S37 "W A.2" framing). Sub-question 1.TAG must settle the scope + the
  correct tag identity + the closing bar at Phase 1, not default-defer a
  seventh time.

If new amendments arise pre-S38 open, walk them per the
reviewer-feedback hygiene pattern above.
