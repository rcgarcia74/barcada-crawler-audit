# Session 27 prompt — scope picked at Phase 1
# (S26 closed Candidate H; S27 chooses from carry-forwards
#  A/B/D/E/K)

**Drafted at Session 26 close (2026-05-25).** Mirrors the
S20/S21/S22/S23/S24/S25/S26 prompt structure. Scope-agnostic at
Phases 0/1; scope-specific design gates at Phase 2 per chosen
candidate. Strict 7-phase ordering with halt-on-mismatch
preserved.

This prompt should be invoked from `~/Downloads/session-27-prompt.md`
(operator-mirrored) or directly from
`~/crawler-audit/SESSION_27_PROMPT.md`. Re-read it on session open.

---

## Scope

Engineering session. Workstream sub-surfaces available after
Session 26 closed Candidate H (1 commit + 1 close-out correction
folded post-operator-review). Repo HEAD at `2314f5e` without a
new tag (1.TAG=defer):

- **Candidate H shipped fully (S26)** — CRAWLING_POLICY.md
  tightened from 8.1 KB to 2.52 KB (69% reduction; 202 → 77
  lines). Q-H.1 ±10% size target landed 14% over cap; variance
  was initially misframed as a Q-H.1-vs-Q-H.3 "intrinsic gate
  collision" but operator review post-S26-close corrected the
  framing — the variance is a downstream consequence of the
  Phase 2 `AskUserQuestion` 4-option truncation, not an
  independent collision. The consolidated LESSONS entry covers
  both surface effects.

- **barcada-drift (Candidate A)** — deferred per Q1.1=(A) at S20;
  still needs 4 AI/ML decisions per CLASSIFICATION_ADJACENT_PLAN.md
  §Item 8 AND 2+ `canary_runs/*.parquet` files (earliest natural
  date 2026-06-06 if the launchd installer has fired ≥2 Saturdays
  since S20 close).

- **Per-tier cost-accounting wiring gap (Candidate B)** — carry-
  forward from S14; severity LOW; closing it would justify
  `workstream-0-end` tag. Now that S25 closed Candidate J, the
  per-tier wiring could optionally exercise abfss:// CostJournal
  end-to-end during verification (but doesn't require it;
  LocalFSCostJournal still works).

- **Phase 4 PR-D tooling (Candidate D)** — operator-led labeling
  territory.

- **Cassette corpus expansion (Candidate E)** — current 20 is lower
  bound of plan's "~20-30".

- **ADLSCostJournal live Azure smoke (Candidate K)** — carry-
  forward from S25 → S26 → S27. S25 shipped against
  `DummyBlobBackend` in-memory (Q-J.3 (c)); no production code
  path has been exercised against real Azure. A small operator-
  driven smoke test (write_initial + try_update + read against a
  sandbox container) would close the mock-vs-prod divergence
  risk. NOT a session-scope blocker on its own; can be folded
  into Candidate B's verification if B is chosen.

Operator chooses at Phase 1 which candidate Session 27 ships.
Each candidate has its own Phase 2 design-gate template.

**Sessions 13-26 precedent:** this session does NOT modify the
W4.1.5 driver orchestration at `tests/runners/fixture_cascade/`
(locked at `dd64963`). Does NOT modify `expected.schema.json` v1.1
/ `META_SCHEMA.md` v1.1. Does NOT modify the committed
`tests/fixtures/baseline-v0/` snapshot at `9e9a1fb`. Does NOT
modify the Session 19 `check` sub-surface code or the Session 20
cassettes/canary sub-surface code or the Session 21 `robots.py`
parser at `34a59b6` or its tests, OR the Session 22 deliverables
(`scraper/robots_gate.py` @ `ba87e7e`,
`scraper/robots_bypass_config.py` @ `381ee89`, the `cost_journal.py`
S22 additions at `1d9404e`), OR the Session 23 deliverables
(`orchestrator/robots_integration.py` @ `279bb77`,
`orchestrator/vmss_worker.py` additions at `5eeaac7`,
`orchestrator/job_runner.py` additions at `872527e`,
`scripts/vmss/cloud_init.template.yaml` additions at `872527e`,
`orchestrator/worker_loop.py` S23 additions at `4ec7b0a`, the
integration test file's 4 S23 tests at `6e6e4ca`), OR the Session 24
deliverables (the 3 new module-level helpers in `worker_loop.py`
at `48c324a`, the 12 unit tests in `test_worker_loop_persistence.py`
at `00d5b38`, the 3 new tests appended to
`test_robots_gate_integration.py` at `aa23712`, the 5 retargeted
test_stage2_pages_invoker_* fixtures in `test_worker_loop.py` at
`48c324a`), OR the Session 25 deliverables
(`cost_journal_adls.py` full backend at `835a531`,
`test_cost_journal_adls.py` 19-test expansion at `835a531`,
the 3 1↔1 same-shape test replacements at `835a531` + `aed7873`,
the `_open_cost_journal_for_worker` body-only abfss:// dispatch
at `aed7873`), OR the Session 26 deliverable
(`docs/CRAWLING_POLICY.md` tightened at `2314f5e`; 77 lines /
2519 bytes; Candidate H is the ONLY candidate that may modify
this file, and only with explicit Phase 2 authorization).

Does NOT modify production code under `src/barcada_scraper/`
UNLESS Phase 2 design-gate explicitly authorizes a specific
module.

Full regression-protection checklist in **Out-of-scope** at the
end of this prompt. Re-read it before any code lands.

---

## Reviewer-feedback hygiene (if this prompt is reviewed)

If an external reviewer (operator-invoked) flags items in this
prompt before Session 27 starts, walk each flagged item against
on-disk reality at workspace HEAD `c0458dc` and repo HEAD
`2314f5e` (or whatever HEAD the operator's machine carries),
BEFORE applying any change. Per S19-S26 pattern (LESSONS
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
8 findings (B-1, M-1, M-2, S-1, S-2, N-1, N-2, N-3); at S25 v1→v2
cycle resolved 6 findings (M-2, S-1, S-2, S-3, N-1, N-2) and
skipped 1 WRONG-PREMISE + 1 defer-to-implementation; at S26 v1→v2
resolved 1 (M-1 narrower-baseline arithmetic); at S26 post-close
1 operator-review correction (the Q-H.1-vs-Q-H.3 collision
misframing collapsed into the truncation lesson). Review remains
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
halts catch hidden scope expansion (per S22-S26 "Implicit-
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
# Workspace at Session 27 start. S26 close-out landed across 3
# workspace commits: 6eff137 (primary close-out) + 03cadd3
# (follow-up pinning S27 Phase 0 workspace anchor) + c0458dc
# (post-close LESSONS correction folding the misframed Q-H.1/
# Q-H.3 collision into the AskUserQuestion 4-option-limit
# truncation lesson per operator review). The anchor-pinning
# follow-up was the ORIGINAL anchor (S25-style); the correction
# pushed workspace HEAD past it to c0458dc.
git -C ~/crawler-audit rev-parse HEAD
# Expect: c0458dc (S26 close-out correction) OR a later commit
# if additional workspace doc edits landed post-S26-close. If N
# commits ahead, verify each prior commit's subject via
# `git log --oneline c0458dc..HEAD` against expected prompt-
# finalization / doc-edit patterns; surface the SHA delta and
# request authorization to proceed if anything is unexpected.
# (S20-S26 precedent: operator authorized continuation when 2-3
# extra workspace commits were the strengthened prompts
# themselves.)

# Repo at Session 26 final commit:
git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: 2314f5e (WA1.W8.crawling-policy-tighten) — the
# canonical end-of-S26 ship SHA.
#
# Tolerated delta: operator-side eval_data labeling commits between
# S26 close and S27 open are expected (Sessions 8-26 precedent).
# Per the S22-folded "Workspace HEAD delta tolerance" LESSONS
# pattern: tolerate N additional commits as long as EACH commit's
# stat is strictly within eval_data/* (no src/barcada_scraper/*
# touches, no tests/* touches, no scripts/* touches, no docs/*
# touches). Verify via `git show --stat <sha>` for every commit in
# 2314f5e..HEAD; surface any non-eval_data delta for operator
# authorization before continuing.
```

### Step 0.2 — Tags (no change from S26 close)

```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort
# Expect 10 tags (unchanged from S22-S26 close; S26 did not
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

### Step 0.4 — Fixture counts (no change from S26 close)

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

### Step 0.5 — Test-suite baseline (S27 canonical)

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
# Expect: 964 passed / 0 failed / 0 skipped
#
# Sub-totals (16 paths; unchanged from S25/S26 close since S26
# was doc-only):
#   210 conformance + 46 driver + 99 baseline_v0 +
#    33 synthetic_crawl + 32 robots + 30 robots_gate +
#    30 robots_bypass_config + 43 cost_journal +
#    13 cost_journal_local + 19 cost_journal_adls +
#    35 robots_integration + 74 vmss_worker +
#   129 job_runner + 152 worker_loop +
#     7 robots_gate_integration (4 S23 + 2 S24-unchanged + 1 S25-replaced) +
#    12 worker_loop_persistence (11 S24-unchanged + 1 S25-replaced) = 964
#
# Pinned in SESSION_LOG.md "Canonical S26-close baseline" block.
# Re-verified post-S26-close-out at HEAD 2314f5e: 964 passed in
# ~52s. The 964 count is invariant under operator-side eval_data
# commits between S26 and S27 (eval_data is not in the invocation).
```

The sub-paths add up to the headline: 210 + 46 + 99 + 33 + 32 + 30
+ 30 + 43 + 13 + 19 + 35 + 74 + 129 + 152 + 7 + 12 = 964. Any drift
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
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal_adls.py -q      # expect  19
.venv/bin/python -m pytest tests/orchestrator/test_robots_integration.py -q            # expect  35
.venv/bin/python -m pytest tests/orchestrator/test_vmss_worker.py -q                   # expect  74
.venv/bin/python -m pytest tests/orchestrator/test_job_runner.py -q                    # expect 129
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop.py -q                   # expect 152
.venv/bin/python -m pytest tests/orchestrator/test_robots_gate_integration.py -q       # expect   7
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop_persistence.py -q       # expect  12
```

**Narrower baselines** (valid for S27 candidates that don't
exercise the new ADLS test paths):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 938 (S26-equivalent narrower for doc-only candidates; 16-path
  minus the 19 cost_journal_adls + the 7 robots_gate_
  integration). Canonical 14-path invocation:

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
  # Expect: 938 passed / 0 failed / 0 skipped
  # Sub-totals (14 paths; 210 + 46 + 99 + 33 + 32 + 30 + 30 + 43 +
  #   13 + 35 + 74 + 129 + 152 + 12 = 938).
  ```

Whichever baseline is bound at Phase 1, hold it consistent across
ALL Phase 3 commits in S27 — do not switch mid-session.

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
```

### Step 0.9 — S25-shipped + S26-shipped public API + doc stability (any-candidate prereq)

```
# Verify the S25 deliverables match what landed at S25 close, and
# the S26 CRAWLING_POLICY.md tightening matches its landed shape.
# A change to any of these between S26 close and S27 open would
# invalidate carry-forward candidate assumptions. Run unconditionally
# at every S27 cold start.

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

print('OK all S24-shipped + S25-shipped public APIs unchanged from S25 close')
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
# Note the explicit `|| { ... exit 1; }` clauses below: the
# Phase 0 contract is fail-loud-and-halt, so any drift here must
# terminate the script. Earlier drafts used `&& ... || echo HALT`
# which printed the HALT message but exited 0, letting Step 0.9
# continue running — fixed per the operator-S26-close review.
test "$(wc -l < docs/CRAWLING_POLICY.md)" = "77" && \
    test "$(wc -c < docs/CRAWLING_POLICY.md)" = "2519" || \
    { echo "HALT: CRAWLING_POLICY.md drifted from S26-landed shape (expected 77 lines / 2519 bytes)"; exit 1; }
echo "OK docs/CRAWLING_POLICY.md unchanged from S26 close (77 lines / 2519 bytes)"

# Verify the load-bearing content still present:
grep -q "BypassAuthorization" docs/CRAWLING_POLICY.md && \
    grep -q "first-match-wins" docs/CRAWLING_POLICY.md && \
    grep -q "ETag-" docs/CRAWLING_POLICY.md && \
    grep -q "authorized_by" docs/CRAWLING_POLICY.md || \
    { echo "HALT: CRAWLING_POLICY.md load-bearing content missing (one of: BypassAuthorization / first-match-wins / ETag- / authorized_by)"; exit 1; }
echo "OK CRAWLING_POLICY.md load-bearing content (audit record / first-match / ETag / sidecar schema) all present"
```

If any of 0.1-0.9 fail, HALT before doing any work.

---

## Required workspace reading (Session 27 first 10 minutes)

In this order:

1. **`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`** — full
   handoff state at S26 close. Lists scope candidates (A/B/D/E/K
   carry-forward) with prerequisites + estimated scope. The S27
   scope choice at Phase 1 picks from these.

2. **`~/crawler-audit/SESSION_LOG.md`** Session 26 entry — what
   landed during Candidate H (1 commit + 1 close-out correction
   post-operator-review). The S26 disposition paragraph
   explicitly documents the LESSONS reframing.

3. **`~/crawler-audit/LESSONS.md`** — 1 new consolidated section
   folded at S26 close (revised post-operator-review from the
   original 2-section fold), at end of file. Locate via
   `grep -n '^## .*(S26 folding)' LESSONS.md`. Read with care:
   - "AskUserQuestion 4-option limit can silently truncate a Q-*
     option set" — covers BOTH downstream surface effects:
     (#1) Q-H.2-EXT round-trip latency forcing mid-Phase-3
     extension; (#2) Q-H.1 14% size-target variance landing
     because the late-arriving extension trims couldn't drive
     a fresh structural rethink. Includes explicit anti-pattern
     warning against generalizing the variance to "intrinsic
     gate collision".

4. **`~/crawler-audit/BARCADA_CRAWLER_REMEDIATION_PLAN.md`** —
   chosen-scope section per Phase 1 candidate choice. Plan is
   READ-ONLY.

5. **`~/crawler-audit/CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8
   — only if Candidate A (barcada-drift) is chosen.

6. **`~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md`** —
   only if Candidate B (per-tier cost-accounting retrofit) is
   chosen. READ-ONLY.

7. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   — only if Candidate B or K touches the ADLS backend. 295 LOC.
   The full Phase 5 backend shipped at S25 SHA `835a531`. Reference
   for the public API contract (`read` / `write_initial` /
   `try_update` / `exists` + `path`).

8. **`tests/classifier/pipeline/test_cost_journal_adls.py`** at
   `835a531` — only if Candidate B or K touches ADLS testing. 19
   tests against `DummyBlobBackend` in-memory. Reference for the
   test posture if Candidate K wants to expand to real Azure.

9. **`docs/CRAWLING_POLICY.md`** at S26 SHA `2314f5e` — only if
   operator wants to review the S26-tightened version (77 lines /
   2.52 KB). Locked at this SHA; further modification requires
   Phase 2 design-gate authorization.

10. **`src/barcada_scraper/orchestrator/worker_loop.py`** lines
    around the `_open_cost_journal_for_worker` helper — only if
    Candidate B / K touches the dispatch. Body modified at S25
    SHA `aed7873` (abfss:// guard removed; abfss:// dispatch
    uses string `rsplit('/', 1)` to extract journal_dir per
    Q-J.4 — pathlib collapse hazard source-verified at S25 Phase 2).
    Source-verify line numbers at session-current HEAD before
    drafting commit edits; the file is ~3000+ LOC post-S25 and
    line numbers shift as commits land.

---

## Phase 1 — Scope resolution (no code; pre-design-gate)

Operator picks one candidate. Candidates ordered by prerequisite-
readiness; each is independent.

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
Session 27 AND operator has not authorized explicit placeholder
choices.

### Candidate B — Per-tier cost-accounting retrofit (closes Workstream 0)

The deferred-from-S14 per-tier cost-accounting wiring gap.
Currently severity LOW, carry-forward. Closing it would let
`workstream-0-end` tag be placed at the closing commit. Touches
the W4.1.5 driver area (`tests/runners/fixture_cascade/`) which
is locked except via W5.X-prefix commits per S16 precedent.
Estimated 100-200 LOC.

**Prerequisites:**
- Operator authorization at S27 Phase 1 for a W5.X-prefix commit
  touching the W4.1.5 driver. Without this auth, the candidate
  HALTs at Phase 1.
- Decision on whether the retrofit touches stage{1,2,3}_*_usd
  driver cost fields, per-row stage3_decision.evidence_cost_usd,
  or both.
- Decision on whether to OPTIONALLY exercise abfss:// CostJournal
  end-to-end during verification (Candidate K folded in) or stick
  with LocalFSCostJournal-only verification.

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

### Candidate K — ADLSCostJournal live Azure smoke (carry-forward from S25)

S25 shipped ADLSCostJournal against `DummyBlobBackend` in-memory
(Q-J.3 (c)). No production code path has been exercised against
real Azure. A small operator-driven smoke test would close the
mock-vs-prod divergence risk.

Two flavors at Phase 2:
- **K-a: Azurite container** — write a one-off integration test
  that spins up an Azurite Docker container and exercises
  `write_initial` → `try_update` → `read` → ETag conflict path
  against a real Azure-compatible blob service. ~50-100 LOC.
- **K-b: Operator-driven sandbox smoke** — operator runs a small
  Python script against their own Azure sandbox container; Claude
  Code provides the script + interprets the output. ~30 LOC; no
  CI integration.

**Prerequisites:**
- K-a: Docker available locally; Azurite image pullable.
- K-b: Operator has an Azure sandbox container; willingness to
  exercise it manually.

**Recommended posture:** K-b if quick mock-vs-prod sanity is the
goal; K-a if a permanent CI safety net is desired. Either way,
this is NOT a session-scope blocker on its own — Candidate B or D
or E is a better primary scope.

### Sub-question 1.TAG — Tag at session close (pinned at Phase 1)

Independent of scope choice; resolved fully here at Phase 1 so
Phase 5 has an unambiguous tag decision. Options per scope:

- **Candidate A** (barcada-drift): defer OR place candidate-
  specific (e.g., `barcada-drift-v0`).
- **Candidate B** (per-tier cost-accounting): if it fully closes
  Workstream 0, place `workstream-0-end`. Otherwise defer.
- **Candidate D** (Phase 4 PR-D tooling): defer.
- **Candidate E** (cassette corpus expansion): defer.
- **Candidate K** (ADLS live smoke): defer.

Phase 5 reads this resolution directly — no Phase 2 re-decision.

---

## Phase 2 — Design-gate elicitation (no code; AskUserQuestion)

Per chosen Phase 1 candidate. Each candidate has its own sub-
block. Source-verify at session-current HEAD per `[[verify-
before-asking-discipline]]` AND per S22-S26 "Plan-vs-reality at
Phase 2 source-verify" + S25-folded "Phase 2 source-verify drives
option-set design, not just gates" LESSONS patterns BEFORE each
AskUserQuestion batch.

**HALT IF** any Phase 2 decision would require modifications to
`src/barcada_scraper/` production code beyond what was Phase-2-
authorized (per S22-S26 "Implicit-authorization HALT for src/-
locks" LESSONS pattern; surface as an explicit AskUserQuestion
before patching) OR to the W4.1.5 driver (except via W5.X-prefix
per Candidate B's auth) OR to any S19-S26 deliverable — surface
as a design-gate sub-question before patching.

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

Do NOT silently narrow. Silent narrowing surfaces as BOTH the
Phase 3 HALT-and-extend cycle AND the downstream structural-
hardening variance (per S26 LESSONS). The round-trip is not a
costless recovery — by the time the missing authorization
arrives, the implementation has often already committed to
assumptions that constrain how much further trim is practical.

### If Candidate A (barcada-drift)

Carry-forward from S22-S26 prompts (unchanged).
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

### If Candidate B (per-tier cost-accounting retrofit)

Carry-forward from S22-S26 prompts (unchanged).
- Q-B.1 scope of fields; Q-B.2 backfill behavior; Q-B.3 test
  approach; Q-B.4 W5.X-prefix commit shape; Q-B.5
  workstream-0-end tag; Q-B.6 abfss:// vs LocalFSCostJournal-
  only verification.

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

### If Candidate K (ADLSCostJournal live smoke)

- **Q-K.1 Smoke flavor**: K-a Azurite container (permanent CI
  safety net) vs K-b operator-driven sandbox (one-off mock-vs-prod
  sanity).
- **Q-K.2 Auth posture** (K-a only): connection-string auth vs
  shared-key auth vs DefaultAzureCredential (Azurite supports all
  three; connection-string is the simplest for CI).
- **Q-K.3 Test scope** (K-a only): full ETag-conflict matrix
  (write_initial race + try_update race + ETag advance) vs single
  happy-path round-trip.
- **Q-K.4 New file vs append**: new file
  `tests/classifier/pipeline/test_cost_journal_adls_azurite.py`
  vs append to `test_cost_journal_adls.py` with a `pytest.mark.live`
  marker.
- **Q-K.5 CI integration**: mark as `live` and skip-by-default in
  the canonical 16-path invocation, OR add a 17th path to the
  invocation that runs only when Docker/Azurite is available.

### Shared sub-questions (all candidates)

- **Q-SHARED.1 Commit shape**: per-module (S18-S26 default;
  Recommended) vs per-sub-surface bundled.

(Tag-at-close is resolved at Phase 1 Sub-question 1.TAG; Phase 5
reads that resolution directly without re-decision.)

---

## Phase 3 — Implementation (per-module commits, strict order)

Per Phase 2 commit-shape decision. Default = per-module. Each
commit must satisfy the 6-step per-commit checkpoint protocol
below.

### Non-interleaving rule (CRITICAL for bisectability)

If the chosen candidate has multiple sub-surfaces (Candidate B
likely does: per-tier accounting fields + backfill + W5.X-prefix
driver realignment), do NOT interleave. Complete each sub-surface
fully before starting the next. Per S22-S26 precedent.

If a mid-sub-surface dependency on the other sub-surface emerges,
HALT and surface as a design-gate sub-question before continuing
— the dependency may indicate a Phase 2 question was missed. See
S23-folded LESSONS "Bisectability vs Phase-1-named commit shape",
S24-folded "Tightened-precondition test-fixture retargeting", and
S25-folded "Q-J.8 explicit allowlist may be incomplete; HALT-and-
extend pattern" for patterns.

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
    <new S27 test paths if any> -q
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
the format-fix into the commit (per S19-S26 pattern).

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
sessions (Sessions 8-26 precedent).

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
Phase 3 start                  : 964  (Session 26 close baseline)
After commit 1                 : >= 964 + N_commit_1_tests
After commit 2                 : >= 964 + N_commit_1_tests + N_commit_2_tests
...
```

**Rule**: the count NEVER decreases between checkpoints. A
decrease means a previously-passing test went red — regression.
HALT.

**Authorized decreases**: only if a Q-* AskUserQuestion at Phase 2
explicitly authorized a same-shape test replacement (e.g.,
Q-J.8-style 1↔1 replacement preserving net-zero count). The
commit body MUST cite the authorization + name the replaced test
+ name the replacement.

Baseline pre-resolved at Phase 1 per Phase 0 Step 0.5: 964 is the
canonical S27 baseline for any candidate that touches the
orchestrator sub-surface OR the journal subsurface (Candidates B
+ K definitely; A possibly; D/E likely not). Whichever baseline
is bound at Phase 1, hold it consistent across ALL Phase 3
commits in S27 — do not switch mid-session.

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
fail the gate even though no S27 commit touches eval_data.

When this fires:
1. Confirm the failing row's content is in operator-WIP
   (`git diff eval_data/...`), not in committed HEAD
   (`git show HEAD:eval_data/...`).
2. Confirm the S27 commits do not touch eval_data
   (`git diff origin/main..HEAD -- eval_data/`).
3. Surface to operator with the exact row + reason + diff vs
   committed state.
4. Two paths: (a) operator-fix in WT, then re-run gate;
   (b) stash eval_data WIP, push, restore.
5. Do NOT auto-fix locked-artifact content.

S20+S22 precedent: operator chose (a). S21/S23/S24/S25/S26 did
not need this protocol at Phase 4 push.

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

- Append Session 27 entry to `~/crawler-audit/SESSION_LOG.md`
  including a **Canonical S27-close baseline** block with the
  exact pytest invocation + verified test count (per S22-S26
  LESSONS "Pin the baseline for the next session's Phase 0
  Step 0.5"; without this, S28 Phase 0 will infer from the
  "Combined headline" bullet and potentially HALT on
  accounting-mismatch).
- Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md` for
  Session 28 — explicitly pin the S28 Phase 0 workspace anchor
  SHA per S21-S26 post-audit pattern (LESSONS "Workspace HEAD
  delta tolerance"); do not omit. After the close-out commit
  lands, expect **1-2 follow-up commits** pinning the actual
  SHA (S21 needed 1; S22 needed 2 — the second pinned the
  canonical baseline test count discovered during audit;
  S23/S24/S25/S26 needed 1 plus optional post-close correction).
- Update `~/crawler-audit/LESSONS.md` with any new forward-
  applicable patterns surfaced this session.
- Workspace close-out: 1 primary commit + 1-2 follow-up commits
  pinning the anchor SHA and any audit-surfaced corrections.
  Push workspace after operator confirms.

Note: drafting the next-session prompt (`SESSION_28_PROMPT.md`)
is NOT a built-in Phase 6 step. Per S20→S21..S26→S27 precedent,
prompt-drafting is operator-commissioned between sessions — not
always-on close-out work. If the operator asks for it explicitly
at S27 close, draft it as a separate follow-up; otherwise leave
for the next session to either operator-commission or scope out
at S28 open.

---

## Acceptance criteria

**Per candidate (reduces if Phase 1 narrows scope):**

### Candidate A (barcada-drift)

Carry-forward from S22-S26 prompts (unchanged):
1. `barcada-drift` (or `barcada-baseline drift`) CLI works
   against ≥2 canary_runs parquets.
2. Drift metric per Q-A.2 implemented + tested.
3. Alert threshold per Q-A.3 implemented + tested.
4. Output shape per Q-A.5 documented + tested.

### Candidate B (per-tier cost-accounting retrofit)

Carry-forward from S22-S26 prompts (unchanged):
1. Per-tier cost fields populated per Q-B.1 scope.
2. Backfill behavior per Q-B.2 executed.
3. Test coverage per Q-B.3 in place.
4. `workstream-0-end` tag placed if per-tier accounting fully
   closes the gap (Q-B.5).
5. Q-B.6: if abfss:// verification opted in, ADLSCostJournal
   end-to-end smoke runs green during retrofit verification.

### Candidate D (Phase 4 PR-D tooling)

1. Tooling shape per Q-D.1.

### Candidate E (cassette corpus expansion)

1. Cassette count grows to Q-E.1 target.
2. FP re-investigation per Q-E.3 if applicable.

### Candidate K (ADLS live smoke)

1. K-a: Azurite-backed integration test passes locally + (if
   Q-K.5 includes CI) in CI; mock-vs-prod divergence empirically
   closed for the operations covered.
2. K-b: Operator-driven sandbox script produces the expected
   write_initial → try_update → read trace; any divergence from
   DummyBlobBackend behavior captured in a new LESSONS section
   for S28 to fold.

### Shared (all candidates additionally satisfy)

Items numbered S1-S4 to avoid collision with candidate-specific
numbering.

- **S1.** Combined suite at session close: existing 964 baseline
  + N new tests, all passing. For narrower-baseline candidates,
  the baseline is the chosen narrower count + N new.
- **S2.** Pre-push gate runs green (incl. eval_data WIP halt
  protocol applied if needed).
- **S3.** Tag placed per Phase 1 Sub-question 1.TAG OR explicit
  defer.
- **S4.** Regression-protection checklist held (see "Out-of-scope"
  below). In particular:
  - ALL S21-S26 deliverables stay at the SHAs they landed at;
    their public APIs are unchanged.
  - Per-sub-suite test counts stay green (or grow): 32 robots-
    parser / 30 robots_gate / 30 robots_bypass_config / 43
    cost_journal / 13 cost_journal_local / 19 cost_journal_adls
    / 35 robots_integration / 74 vmss_worker / 129 job_runner /
    152 worker_loop / 7 robots_gate_integration (4 S23 +
    2 S24-unchanged + 1 S25-replaced) / 12
    worker_loop_persistence (11 S24-unchanged + 1 S25-replaced).
  - `docs/CRAWLING_POLICY.md` stays at 77 lines / 2519 bytes
    unchanged from S26 SHA `2314f5e` (verified at Phase 0
    Step 0.9).
  - The combined total stays at 964 (or grows) unless a Q-*
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
  S25 Q-J.8-extension replacement at SHA `835a531` which is now
  the canonical contract for that 1 test.

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
  `aed7873` per Q-J.4 abfss:// dispatch; SIGNATURE locked at
  S24 — modifying the signature requires explicit Phase 2
  authorization), `_ensure_journal_initialized` (LOCKED at S24),
  `_build_durable_bypass_writer` (LOCKED at S24).
- The 3-line wiring block in `scrape_stage2_pages_invoker` at
  `48c324a`. The adjacent comment was updated at S25 `aed7873`
  to note Phase 5 shipped; further comment edits do not affect
  the locked wiring.
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
  Candidate B and K may CONSUME `ADLSCostJournal` but MUST NOT
  modify the public API signatures without explicit Phase 2
  authorization. Candidate K (live smoke) may ADD a separate
  test file under `tests/classifier/pipeline/` but MUST NOT
  modify `cost_journal_adls.py` itself.
- `tests/classifier/pipeline/test_cost_journal_adls.py` at S25
  SHA `835a531` (19 tests + the `DummyBlobBackend` helper class).
  Locked. Candidate K may import `DummyBlobBackend` (it's a
  module-level class) but MUST NOT modify the test file.
- The S25 Q-J.8-extension replacement in
  `tests/classifier/pipeline/test_cost_journal.py` at SHA
  `835a531` (`test_open_journal_abfss_routes_to_adls_journal`).
  Locked.
- The body-only modification to
  `src/barcada_scraper/orchestrator/worker_loop.py`'s
  `_open_cost_journal_for_worker` at S25 SHA `aed7873` (abfss://
  guard removed; abfss:// dispatch via string `rsplit('/', 1)`).
  Signature locked at S24; body further-modifiable ONLY under
  explicit Phase 2 authorization.
- The S25 invoker-site comment update at SHA `aed7873`. The
  locked S24 wiring block is unchanged; only the adjacent
  comment was updated.

**S26 deliverables (Session 26 W A.1 W8 sub-surface — NEW for S27
lock-list):**
- `docs/CRAWLING_POLICY.md` at S26 SHA `2314f5e` (77 lines /
  2519 bytes; the W A.1 robots-compliance doc tightened from
  8.1 KB to 2.52 KB; preserves 3-decision tree + first-match-
  wins + sidecar schema + BypassAuthorization audit record +
  ETag-conditional persistence note + 6-row Operational defaults
  table). Candidate H closed at S26; no candidate at S27 should
  modify this doc unless Phase 2 design-gate explicitly
  authorizes further tightening, extension, or rewrite.

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
- All workstream tags at their placed SHAs (10 tags as of S26
  close; new tags only via Phase 5 explicit placement)
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` (READ-ONLY)
- `CLASSIFICATION_ADJACENT_PLAN.md` (UPDATED only when AI/ML
  decisions land)
- `RECONCILIATION_2026-05-21.md`
- `docs/phase4_implementation_plan.md` (Phase 4 governance
  reference)

**Operator-owned territory:**
- All of `eval_data/` — labeling-workstream territory; per-row WIP
  edits across sessions are expected and unstaged (Sessions 8-26
  precedent). S22→S26 inter-session operator-side eval_data
  COMMITS are tolerated per the "Workspace HEAD delta tolerance"
  LESSONS pattern — verify they're eval_data-only via
  `git show --stat <sha>` for each commit in the delta.

**Production code:**
- `src/barcada_scraper/` — locked unless Phase 2 design-gate
  explicitly authorizes a specific module. S21-S25 authorized:
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
  helper body). S26 added no new src/ authorizations (doc-only).
  Those authorizations do NOT extend to other src/ modules or
  to further modifications of the authorized files beyond their
  landed S21-S26 shapes.

**Pipeline configs:**
- `configs/`

**Phase 4 work:**
- Phase 4 PR-D/E/F/G work opens only when Workstream 0 fully
  closes AND operator-led Stage 2/3 labeling work begins.

---

## Verify-before-asking discipline (strict rule from S19-S26)

Per `[[double-check-before-commit]]` memory: **ALWAYS verify
every concrete claim in the commit message against actual source/
output BEFORE staging.** Fixture names, file counts, exit codes,
line counts, test counts, helper names, smoke outcomes, SHA
prefixes, regex matches, API signatures. No claims by pattern-
completion. Build a verification table in chat (claim → reality →
status) and reconcile before "Confirm to commit?".

Specific to S27:

- Before each chosen-candidate-specific claim in a commit message,
  verify against the actual source / runtime output:
  - Candidate A: barcada-drift CLI invocation produces the
    expected output shape against ≥2 parquets.
  - Candidate B: per-tier cost-journal field presence; W5.X
    driver realignment landed correctly.
  - Candidate D: tooling smoke produces expected output.
  - Candidate E: cassette count post-record; FP-curation log
    updated.
  - Candidate K: K-a Azurite container produces the expected
    412 on race-loser write_initial; K-b operator-driven script
    output captured verbatim.
- Before claiming combined suite count, re-run pytest.
- Before claiming ruff/format clean, re-run ruff against the
  touched files.
- Before claiming a SHA prefix in a commit message body, verify
  the prefix is correct via `git show --no-patch --format=%h <ref>`.

Avoid bash pipe artifacts that mask Python exit codes (LESSONS):
`python_cmd 2>&1 | grep ... | tail` makes `$?` reflect tail's
exit. Use `> stdout.out 2> stderr.err; echo $?` or
`${PIPESTATUS[0]}` when exit-code matters.

LESSONS-folded discoveries from S22-S26 worth re-applying:

- **Plan-vs-reality at Phase 2** (S22 LESSONS): plan §5 wording
  may name a module/site that doesn't match the actual code
  shape. Verify the actual integration site via Explore BEFORE
  drafting Q-* options.

- **Phase 2 source-verify drives option-set design** (S25 LESSONS):
  for any candidate touching a new SDK / external system / language
  feature, verify the underlying facts BEFORE drafting AskUserQuestion
  options. If a fact-check would invalidate one or more options,
  the question structure is misleading the operator. Re-shape the
  option set first, then ask.

- **Implicit-authorization HALT** (S22-S26 LESSONS): Q-*
  answers may require touching files NOT in S27 Out-of-scope's
  authorized-touch list (e.g., introducing a new helper module
  for ADLS-specific live smoke). Surface explicit authorization
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

- **Test against public API surface only** (S24 LESSONS): tests
  should probe behavior via the public surface (e.g., for
  ADLSCostJournal: `read` / `write_initial` / `try_update` /
  `exists` + `.path`). Avoid asserting on private attrs.

- **Source-verify line numbers per Phase 3 commit** (S23
  LESSONS): worker_loop.py is now ~3000+ LOC post-S25; the
  `_open_cost_journal_for_worker` helper line numbers shift as
  commits land. Re-Explore at session-current HEAD before
  drafting commit edits.

- **AskUserQuestion 4-option limit can silently truncate a Q-*
  option set** (S26 LESSONS): count the Q-* option set BEFORE
  drafting AskUserQuestion calls. If >4 mutually-exclusive
  options, tier the question or split horizontally. Truncation
  has TWO downstream surface effects (round-trip latency +
  structural-hardening variance); both are forward-applicable.
  Do NOT generalize size-target variances downstream of
  truncation into "intrinsic gate collisions" — the proximate
  cause is truncation, not the gates themselves.

---

## Commit hygiene (per LESSONS + S19-S26 additions)

- File-based commit messages at `/tmp/<id>-msg.txt`.
- Per-module commits (Phase 3 commit shape unless Q-SHARED.1
  overrides).
- "Confirm to commit?" before EVERY commit. Pair with verification
  table (always) and `git diff --staged` (when appropriate per
  `[[double-check-before-commit]]` triggers).
- Commit body includes: action ref (e.g., `WA2.W8.per-tier-accounting`
  or `WK.adls-live-smoke` — operator picks the prefix at Phase 1),
  scope summary, file touches, test count delta (with net-new vs
  newly-in-invocation pre-existing distinction per S23 LESSONS),
  plan reference. NO `Co-Authored-By`.
- Pre-push gate must run green. Never use `--no-verify`.
- Pre-push vermin: `git ls-files '*.py' | xargs vermin
  --target=3.10` to filter venv-internal pytest 3.14 false-
  positives.
- Mid-implementation ruff format-check, not only pre-push.
- For S24/S25/S26-test modifications: explicit Phase 2
  authorization required; document the modification scope
  explicitly in the commit body (per S22-S26 LESSONS "Implicit-
  authorization HALT" pattern).
- Workspace close-out (Phase 6) lands as its own commit at session
  close, followed by 1 follow-up commit pinning the anchor SHA
  for the next session (S21-S26 pattern). S26 demonstrated that a
  POST-close-out correction commit is sometimes necessary
  (operator-review-driven LESSONS reframing); when this happens,
  the new HEAD supersedes the anchor-pinning follow-up, and
  S28 Phase 0 will need to tolerate the additional commit per
  the Workspace HEAD delta tolerance pattern.

---

## Context-window awareness

S26 ran across 1 commit + Phase 2 source-verification + 1 mid-
Phase-3 Q-H.2-EXT HALT-and-extend + Phase 6 close-out + 1 post-
close LESSONS correction (operator-review-driven), well within
context. S27 budget per scope:

- Candidate A: medium-large (~300 LOC).
- Candidate B: small-medium (100-200 LOC; sensitive driver-area
  touch).
- Candidate D/E: small.
- Candidate K-a: medium (~50-100 LOC + Docker setup).
- Candidate K-b: very small (~30 LOC; operator-driven).

Strategies:
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore
  subagent per S22-S26 "Explore-subagent + spot-check" LESSONS
  pattern.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before the chosen S27 scope closes,
  transition per "no mid-commit-batch transitions" — finish
  in-flight sub-surface, then close session and refill the
  transition template for Session 28.

---

## Reporting in chat at session close

After all Session 27 commits land + push + close-out per the
S13-26 pattern:

1. Commit SHA(s) of each S27 sub-surface.
2. Sub-surface(s) landed (per candidate).
3. Test count delta: 964 (or 480/538/938) baseline → S27 close.
4. Driver suite count at S27 close (46/46 expected unless
   Candidate B W5.X-prefix realigned).
5. Files touched per sub-surface.
6. Tag dispositions (incl. any new tag per 1.TAG).
7. Per-tier cost-accounting wiring gap disposition: patched
   (Candidate B) or carry-forward.
8. ADLSCostJournal live-smoke disposition: shipped (Candidate K)
   or carry-forward.
9. Any spend (LLM, infrastructure, cassette-capture).
10. Robots.txt compliance log (if Candidate E expanded the
    cassette corpus).
11. FP-curation log update (if Candidate E expanded the cassette
    corpus).
12. Verify-before-asking summary: any source-verification
    findings surfaced.
13. Outstanding items for Session 28.
14. Tags state at S27 close.

Do not propose Phase 4 PR-D/E/F/G work this session unless
Candidate D was chosen and operator-led labeling is in flight.

---

## Carry-forward bakes (no amendment file needed)

All S26 close-out commits (`6eff137` primary + `03cadd3` anchor
follow-up + `c0458dc` post-operator-review LESSONS correction)
plus the S26 post-close verification have been folded directly
into this prompt — S27 does not need a separate amendment file:

- **S26 close-out corrections** folded into Step 0.1 (workspace
  anchor `c0458dc`; repo anchor `2314f5e` with operator-eval_data-
  commit tolerance), Step 0.5 (Canonical S26-close baseline 964
  pinned with 16-path invocation + sub-totals; 938 narrower for
  doc-only candidates), Step 0.9 (S24+S25 public API stability
  PLUS new S26 CRAWLING_POLICY.md doc-stability check at 77
  lines / 2519 bytes).
- **1 LESSONS section from S26 close (the result of a
  deletion-and-merge per operator review post-S26-close: the
  originally-folded second section "Size-target gates can
  collide with audience-coverage gates" was DELETED as misframed,
  and the surviving section "AskUserQuestion 4-option limit can
  silently truncate a Q-* option set" was BROADENED to cover
  both downstream surface effects (Q-H.2-EXT round-trip latency
  + Q-H.1 14% size-target variance) PLUS an explicit anti-
  pattern warning against generalizing the variance to an
  "intrinsic gate collision")** referenced where it applies: at
  Phase 2 "CRITICAL Phase 2 hygiene from S26 LESSONS" (apply
  BEFORE every AskUserQuestion call) AND at the Verify-before-
  asking section's LESSONS-folded-discoveries list.

If new amendments arise pre-S27 open, walk them per the reviewer-
feedback hygiene pattern in this prompt's "Reviewer-feedback
hygiene" section.
