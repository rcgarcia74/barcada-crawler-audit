# Session 24 prompt — scope picked at Phase 1
# (W A.2 closed at S23; S24 chooses from Candidate I new
#  + carry-forwards A/B/D/E/H from S22/S23)

**Drafted at Session 23 close (2026-05-23).** Mirrors the
S20/S21/S22/S23 prompt structure. Scope-agnostic at Phases 0/1;
scope-specific design gates at Phase 2 per chosen candidate. Strict
7-phase ordering with halt-on-mismatch preserved.

This prompt should be invoked from `~/Downloads/session-24-prompt.md`
(operator-mirrored) or directly from
`~/crawler-audit/SESSION_24_PROMPT.md`. Re-read it on session open.

---

## Scope

Engineering session. Workstream sub-surfaces available after Session
23 closed `WA2.W8.*` (5 commits) and left repo HEAD at `6e6e4ca`
without a new tag (1.TAG=defer):

- **W A.2 shipped fully** — robots_integration helpers
  (`orchestrator/robots_integration.py` @ `279bb77`), vmss_worker
  env-var leg (`orchestrator/vmss_worker.py` @ `5eeaac7`),
  job_runner CLI + cloud-init plumbing (`orchestrator/job_runner.py`
  + `scripts/vmss/cloud_init.template.yaml` @ `872527e`), worker_loop
  3-site gate wiring (`orchestrator/worker_loop.py` @ `4ec7b0a`),
  in-process tmp_path integration test (`tests/orchestrator/
  test_robots_gate_integration.py` @ `6e6e4ca`). The orchestrator
  pipeline now evaluates URLs against robots.txt at all three pre-
  fetch sites in `_acquire_one_domain_t1`; SKIP emits a row with
  `error_kind="ROBOTS_DISALLOW"`; BYPASS_ALLOW invokes a per-shard
  `bypass_audit_writer` callback and lets the fetch through. The
  production writer in `scrape_stage2_pages_invoker` is log-only
  (LOG.warning per BYPASS_ALLOW); durable persistence to
  `JournalState.robots_bypass_log` via `update_with_retry` is the
  S23 explicit deferral — see Candidate I.

- **Candidate I (NEW; Recommended)** — durable bypass-audit
  persistence in worker_loop. Closes the S23 deferral: opens a
  `CostJournal` handle from `config.cost_journal_url` at worker
  boot and replaces the log-only `_bypass_audit_writer` with a real
  one that calls `record_bypass_audit(journal=journal,
  decision=decision)`. The integration-test contract was already
  pinned at S23 commit 5 via `LocalFSCostJournal` in `tmp_path`;
  Candidate I extends that contract to production.

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

Operator chooses at Phase 1 which candidate Session 24 ships. Each
candidate has its own Phase 2 design-gate template.

**Sessions 13-23 precedent:** this session does NOT modify the
W4.1.5 driver orchestration at `tests/runners/fixture_cascade/`
(locked at `dd64963`). Does NOT modify `expected.schema.json` v1.1 /
`META_SCHEMA.md` v1.1. Does NOT modify the committed
`tests/fixtures/baseline-v0/` snapshot at `9e9a1fb`. Does NOT modify
the Session 19 `check` sub-surface code or the Session 20
cassettes/canary sub-surface code or the Session 21 `robots.py`
parser at `34a59b6` or its tests, OR the Session 22 deliverables
(`scraper/robots_gate.py` @ `ba87e7e`, `scraper/robots_bypass_config.py`
@ `381ee89`, the cost_journal.py S22 additions at `1d9404e`,
`docs/CRAWLING_POLICY.md` at `fdc8a7a`), OR the Session 23
deliverables (`orchestrator/robots_integration.py` @ `279bb77`,
`orchestrator/vmss_worker.py` additions at `5eeaac7`,
`orchestrator/job_runner.py` additions at `872527e`,
`scripts/vmss/cloud_init.template.yaml` additions at `872527e`,
`orchestrator/worker_loop.py` additions at `4ec7b0a`, and the
integration test file at `6e6e4ca`). Does NOT modify production
code under `src/barcada_scraper/` UNLESS Phase 2 design-gate
explicitly authorizes a specific module.

Full regression-protection checklist in **Out-of-scope** at the end
of this prompt. Re-read it before any code lands.

---

## Reviewer-feedback hygiene (if this prompt is reviewed)

If an external reviewer (operator-invoked) flags items in this
prompt before Session 24 starts, walk each flagged item against
on-disk reality at HEAD `6e6e4ca` (repo canonical end-of-S23 ship)
or whatever HEAD the operator's machine carries (operator-side
eval_data labeling commits may have advanced the repo HEAD post-
S23-close per the S22→S23 precedent), AND at workspace HEAD
`8f8e51f`, BEFORE applying any change. Per S19/S20/S21/S22/S23
pattern (LESSONS "Reviewer-feedback hygiene"):

- **OBSOLETE** items: SHAs already verified, claims already true.
  Skip with documented reasoning.
- **VALID-applies-now** items: bear on this session's scope. Apply.
- **VALID-applies-later** items: bear on deferred scope. Carry
  forward to the next prompt revision.
- **WRONG-PREMISE** items: assumes something not true. Skip with
  documented reasoning.

Empirical baseline: at S19 review 3 of 5 "must-fix" items collapsed
under cold-start verification; at S20 review 1 of 12 amendments was
skipped because it would HALT spuriously (SR-4); at S21+S22 post-
close audit 2 of 3 operator-feedback items required workspace-doc
corrections; at S23 post-close audit no reviewer feedback was
solicited (5-commit shape verified cleanly). Do not pattern-apply;
verify each.

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
state. Phase 1 halts catch unresolved scope-blockers (AI/ML
decisions for A; W5.X-prefix auth for B; cost_journal-URL parsing
decision for I). Phase 2 halts catch hidden scope expansion (per
S22+S23 "Implicit-authorization HALT for src/-locks" — any src/
touch not enumerated in Out-of-scope's allow-list surfaces here).
Phase 3 halts catch regressions. Phase 4 halts catch pre-push gate
failures (incl. operator-WIP-in-locked-tree).

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

Run in order. Halt and surface to operator on any mismatch.

### Step 0.1 — Workspace + repo HEAD

```
# Workspace at Session 24 start (Session 23 close-out: primary
# commit + 1 follow-up pinning the S24 anchor SHA, all pushed):
git -C ~/crawler-audit rev-parse HEAD
# Expect: 8f8e51f (S23 close-out follow-up: pin S24 Phase 0
# workspace anchor SHA) OR a later commit if additional workspace
# doc edits landed post-S23-close. If N commits ahead, verify each
# prior commit's subject via `git log --oneline 8f8e51f..HEAD`
# against expected prompt-finalization / doc-edit patterns;
# surface the SHA delta and request authorization to proceed if
# anything is unexpected. (S20/S21/S22/S23 precedent: operator
# authorized continuation when 2-3 extra workspace commits were
# the strengthened prompts themselves.)

# Repo at Session 23 final commit:
git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: 6e6e4ca (WA2.W8.robots-gate-integration-test) — the
# canonical end-of-S23 ship SHA.
#
# Tolerated delta: operator-side eval_data labeling commits between
# S23 close and S24 open are expected (Sessions 8-23 precedent;
# at S23 open the repo had 2fc4d8e on top of fdc8a7a, a single
# eval_data-only commit). Per the S23-folded "Workspace HEAD delta
# tolerance" LESSONS pattern: tolerate N additional commits as
# long as EACH commit's stat is strictly within eval_data/* (no
# src/barcada_scraper/* touches, no tests/* touches, no scripts/*
# touches, no docs/* touches). Verify via `git show --stat <sha>`
# for every commit in 6e6e4ca..HEAD; surface any non-eval_data
# delta for operator authorization before continuing.
```

### Step 0.2 — Tags (no change from S23 close)

```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort
# Expect 10 tags (unchanged from S22 close; S23 did not place a tag):
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

### Step 0.4 — Fixture counts (no change from S23 close)

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

### Step 0.5 — Test-suite baseline (S24 canonical)

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
    tests/orchestrator/test_robots_gate_integration.py -q
# Expect: 932 passed / 0 failed / 0 skipped
#
# Sub-totals (15 paths):
#   210 conformance + 46 driver + 99 baseline_v0 +
#    33 synthetic_crawl + 32 robots + 30 robots_gate +
#    30 robots_bypass_config + 43 cost_journal +
#    13 cost_journal_local + 2 cost_journal_adls +
#    35 robots_integration + 74 vmss_worker (67 pre-S23 + 7 new) +
#   129 job_runner (121 pre-S23 + 8 new) +
#   152 worker_loop (146 pre-S23 + 6 new) +
#     4 robots_gate_integration = 932
#
# Pinned in SESSION_LOG.md "Canonical S23-close baseline" block.
# Re-verified post-S23-close-out at HEAD 6e6e4ca: 932 passed in
# ~48s. The 932 count is invariant under operator-side eval_data
# commits between S23 and S24 (eval_data is not in the invocation).
```

The sub-paths add up to the headline: 210 + 46 + 99 + 33 + 32 + 30
+ 30 + 43 + 13 + 2 + 35 + 74 + 129 + 152 + 4 = 932. Any drift = halt.

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
.venv/bin/python -m pytest tests/orchestrator/test_robots_gate_integration.py -q       # expect   4
```

**Narrower baselines** (valid for S24 candidates that don't exercise
the orchestrator sub-surface — H is the clearest example):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)

Whichever baseline is bound at Phase 1, hold it consistent across
ALL Phase 3 commits in S24 — do not switch mid-session.

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

# S22 cost-journal additions tests (43 in test_cost_journal.py)
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal.py -q
# Expect: 43 passed
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal_local.py -q
# Expect: 13 passed
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal_adls.py -q
# Expect: 2 passed

# S23 W A.2 sub-surface tests (NEW for S24):
.venv/bin/python -m pytest tests/orchestrator/test_robots_integration.py -q
# Expect: 35 passed
.venv/bin/python -m pytest tests/orchestrator/test_vmss_worker.py -q
# Expect: 74 passed (67 pre-S23 + 7 S23 new)
.venv/bin/python -m pytest tests/orchestrator/test_job_runner.py -q
# Expect: 129 passed (121 pre-S23 + 8 S23 new)
.venv/bin/python -m pytest tests/orchestrator/test_worker_loop.py -q
# Expect: 152 passed (146 pre-S23 + 6 S23 new)
.venv/bin/python -m pytest tests/orchestrator/test_robots_gate_integration.py -q
# Expect: 4 passed
```

### Step 0.9 — S23-shipped public API stability (Candidate I prereq)

```
# If Candidate I (durable bypass-audit persistence) is even possibly
# in scope, verify the PUBLIC integration contracts of all S23
# deliverables match what landed at S23 close. A change to any of
# these between S23 close and S24 open would invalidate the
# Candidate-I design.
#
# Scope: only what Candidate I callers depend on:
#   robots_integration.build_robots_gate(user_agent, bypass_config)
#   robots_integration.prewarm_robots_for_url(gate, url)
#   robots_integration.make_robots_disallow_row_fields(decision)
#   robots_integration.record_bypass_audit(journal, decision)
#   robots_integration.load_bypass_config_or_empty(path)
#   robots_integration.ROBOTS_DISALLOW_ERROR_KIND == "ROBOTS_DISALLOW"
#   WorkerConfig.robots_bypass_config_path (str field, default "")
#   JobRunArgs.robots_bypass_config_path (str field, default "")
#   render_cloud_init kwarg robots_bypass_config_path
#   render_cloud_init substitutes "BARCADA_ROBOTS_BYPASS_CONFIG"
#   _acquire_one_domain_t1 accepts kwargs bypass_config, bypass_audit_writer
#   scripts/vmss/cloud_init.template.yaml has the placeholder + -e line
#   (re-anchored Candidate I prerequisites: all S22 surfaces from S23 prompt's Step 0.9)

.venv/bin/python -c "
import inspect
from barcada_scraper.orchestrator.robots_integration import (
    ROBOTS_DISALLOW_ERROR_KIND,
    build_robots_gate,
    prewarm_robots_for_url,
    make_robots_disallow_row_fields,
    record_bypass_audit,
    load_bypass_config_or_empty,
)
from barcada_scraper.orchestrator.vmss_worker import WorkerConfig
from barcada_scraper.orchestrator.job_runner import JobRunArgs, render_cloud_init
from barcada_scraper.orchestrator.worker_loop import _acquire_one_domain_t1

# S23 robots_integration public surface — stable identifiers.
assert ROBOTS_DISALLOW_ERROR_KIND == 'ROBOTS_DISALLOW'

# Function-signature subset checks (SUBSET <= to tolerate v1.1 kwarg
# growth that adds optional parameters; STRICT EQUALITY where shape
# divergence would invalidate Candidate I's design).
def _params(fn): return set(inspect.signature(fn).parameters)
assert {'user_agent', 'bypass_config'} <= _params(build_robots_gate), build_robots_gate
assert {'gate', 'url'} <= _params(prewarm_robots_for_url), prewarm_robots_for_url
assert 'decision' in _params(make_robots_disallow_row_fields)
assert {'journal', 'decision'} <= _params(record_bypass_audit), record_bypass_audit
assert 'path' in _params(load_bypass_config_or_empty)

# WorkerConfig field — Candidate I reads this to know where the
# bypass config lives + which journal URL the worker uses.
wc_fields = {f.name for f in WorkerConfig.__dataclass_fields__.values()}
assert 'robots_bypass_config_path' in wc_fields, wc_fields
assert 'cost_journal_url' in wc_fields, wc_fields  # Candidate I parses this

# JobRunArgs — operator-side CLI flag mirror.
jra_fields = {f.name for f in JobRunArgs.__dataclass_fields__.values()}
assert 'robots_bypass_config_path' in jra_fields, jra_fields

# render_cloud_init kwarg + substitution survive.
rci_params = _params(render_cloud_init)
assert 'robots_bypass_config_path' in rci_params, rci_params

# _acquire_one_domain_t1 accepts the S23-added kwargs.
acq_params = _params(_acquire_one_domain_t1)
assert {'bypass_config', 'bypass_audit_writer'} <= acq_params, acq_params

print('OK all S23-shipped public APIs unchanged from S23 close')
"

# Verify the cloud-init template still has the S23-added placeholder
# + the -e BARCADA_ROBOTS_BYPASS_CONFIG line. Any drift here breaks
# the operator-CLI → worker-env propagation chain.
grep -q '${BARCADA_ROBOTS_BYPASS_CONFIG}' scripts/vmss/cloud_init.template.yaml \
    && echo 'OK cloud_init.template.yaml placeholder present' \
    || (echo 'FAIL placeholder missing'; exit 1)

grep -q '\-e BARCADA_ROBOTS_BYPASS_CONFIG=\${BARCADA_ROBOTS_BYPASS_CONFIG}' \
    scripts/vmss/cloud_init.template.yaml \
    && echo 'OK cloud_init.template.yaml -e line present' \
    || (echo 'FAIL -e line missing'; exit 1)
```

If any of 0.1-0.9 fail, HALT before doing any work.

---

## Required workspace reading (Session 24 first 10 minutes)

In this order:

1. **`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`** — full
   handoff state at S23 close. Lists 6 scope candidates (I new +
   A/B/D/E/H carry-forward) with prerequisites + estimated scope.
   The S24 scope choice at Phase 1 picks from these.

2. **`~/crawler-audit/SESSION_LOG.md`** Session 23 entry — what
   landed during W A.2 W8 integration (5 commits). The mid-Phase-3
   bisectability adjustment (cloud-init template moved from
   commit 2 to commit 3). The production-vs-test journal asymmetry
   that drove the deferral named here as Candidate I. The 5
   forward-applicable patterns at the end.

3. **`~/crawler-audit/LESSONS.md`** — 5 new sections folded at S23
   close, at end of file. Locate via
   `grep -n '^## .*(S23 folding)' LESSONS.md`. Especially:
   - "Bisectability vs Phase-1-named commit shape" — applicable if
     Candidate I needs file-pairs across the Phase-1-named
     boundary (e.g., a new helper module + its caller in worker_loop).
   - "Production-vs-test journal asymmetry" — DIRECTLY APPLICABLE.
     Candidate I closes this gap, but the close-out itself surfaces
     a similar pattern: the LocalFSCostJournal path used in tmp_path
     tests does not map cleanly to abfss:// for Azure deployments.
     Decision on how to handle abfss:// at worker boot is a Phase 2
     question.
   - "Source-verify line numbers per Phase 3 commit, not just at
     Phase 2" — applicable if Candidate I needs to touch
     `worker_loop.py` (still 2884+ LOC after S23's +109 wiring;
     re-verify with Explore before drafting edits).
   - "Cumulative test-count gate with new-file invocation expansion"
     — applicable if Candidate I adds a new test file. Per-commit
     bookkeeping should distinguish net-new tests from newly-in-
     invocation pre-existing tests.
   - "False-premise verification questions during Phase 2" — apply
     to ALL design-gate elicitations; do not confabulate.

4. **`~/crawler-audit/BARCADA_CRAWLER_REMEDIATION_PLAN.md`** —
   chosen-scope section per Phase 1 candidate choice. Plan is
   READ-ONLY.

5. **`~/crawler-audit/CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8
   — only if Candidate A (barcada-drift) is chosen.

6. **`~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md`** —
   only if Candidate B (per-tier cost-accounting retrofit) is
   chosen. READ-ONLY.

7. **`src/barcada_scraper/orchestrator/robots_integration.py`** at
   `279bb77` — only if Candidate I is chosen. The public API
   (`record_bypass_audit`, `build_robots_gate`,
   `load_bypass_config_or_empty`, etc.) is what Candidate I
   integrates against. Read top-to-bottom; ~244 LOC.

8. **`src/barcada_scraper/orchestrator/worker_loop.py`** — only
   if Candidate I is chosen. The integration site is the
   `_bypass_audit_writer` closure inside `scrape_stage2_pages_invoker`
   (post-S23 it's a log-only LOG.warning; Candidate I replaces it
   with a durable writer). The function is ~2884+ LOC; use Explore
   per the S23 "Source-verify line numbers per Phase 3 commit"
   LESSONS pattern.

9. **`src/barcada_scraper/classifier/pipeline/cost_journal.py`** at
   `1d9404e` — only if Candidate I is chosen. `open_journal` (the
   factory) + `LocalFSCostJournal` / `ADLSCostJournal` (the latter
   is a Phase 5 skeleton per the code; this affects Candidate I's
   abfss:// handling decision).

10. **`tests/orchestrator/test_robots_gate_integration.py`** at
    `6e6e4ca` — only if Candidate I is chosen. The S23 commit-5
    integration test pins the contract Candidate I extends to
    production. Read top-to-bottom; ~331 LOC.

11. **`docs/CRAWLING_POLICY.md`** at `fdc8a7a` — only if Candidate H
    (doc tightening) is chosen.

---

## Phase 1 — Scope resolution (no code; pre-design-gate)

Operator picks one candidate. Candidates ordered by prerequisite-
readiness; each is independent.

### Candidate I — Durable bypass-audit persistence in worker_loop (NEW; Recommended)

The natural follow-on to S23's log-only `_bypass_audit_writer`.
Opens a `CostJournal` handle at worker boot from
`config.cost_journal_url` and replaces the log-only closure with a
real durable writer that calls
`record_bypass_audit(journal=journal, decision=decision)`. Closes
the S23 explicit deferral and matches the Q-G.4 contract pinned by
the S23 commit-5 integration test.

Scope:
- Parse `config.cost_journal_url` into a `journal_dir` + `run_id`
  pair (or use `open_journal` directly if the URL is parsable).
  Two URL shapes to handle: `file://` (local FS) and `abfss://`
  (Azure Data Lake Storage). The latter is currently a Phase 5
  SKELETON in `cost_journal.py:ADLSCostJournal` — Phase 2 decides
  whether Candidate I requires ADLS-skeleton completion (significant
  scope expansion) or scopes to `file://` only with explicit ADLS
  deferral (smaller scope; documented deferral).
- Handle the "journal not yet initialized" case at worker boot:
  call `j.exists()`; if False, decide whether the worker writes
  initial (`j.write_initial(JournalState.fresh(...))`) or HALTs
  with "journal must be initialized by orchestrator first". Phase 2
  decision.
- Replace `_bypass_audit_writer` in
  `scrape_stage2_pages_invoker` with a closure that calls
  `record_bypass_audit(journal=journal, decision=decision)`.
- Coordination with the existing per-shard outcome journal_writer:
  the per-shard append-only writer (current worker_loop pattern)
  and the durable CostJournal handle are TWO DIFFERENT WRITES to
  the SAME journal file/URL. Phase 2 decides whether they conflict
  (ETag-conditional `try_update` would fail if the append-only
  writer's last write hasn't been read), OR whether they target
  different sections of the journal structure (the
  per-shard outcome goes to `JournalState.shards`; the bypass goes
  to `JournalState.robots_bypass_log`). Likely the second — but
  source-verify.
- Tests: extend the S23 integration test (or add a parallel) driving
  `scrape_stage2_pages_invoker` end-to-end with a real
  LocalFSCostJournal-backed worker. Assert that
  `journal.read().state.robots_bypass_log` carries the audit entry
  after a BYPASS_ALLOW fires.

Estimated 50-100 LOC (URL→handle parser + boot init logic + writer
replacement + tests).

**Prerequisites:**
- **All S23 public APIs stable** (Phase 0 Step 0.9 verifies). HALT
  if any drifted.
- **abfss:// scope decision** — must be pre-resolved at Phase 2
  Q-I.1 before Phase 3 begins. The two paths have very different
  blast radius:
  (a) file:// only with abfss:// HALTed at worker boot
      (~30-50 LOC; scoped to Candidate I; abfss:// follow-up
      candidate);
  (b) file:// + abfss:// both supported, requiring completion of
      the ADLSCostJournal Phase 5 skeleton (~150-250 LOC; expands
      scope significantly).
- **Journal init coordination** — must be pre-resolved at Phase 2
  Q-I.2. Two paths:
  (a) Worker calls `write_initial` if journal doesn't exist
      (worker takes ownership of init; orchestrator-side init
      becomes optional);
  (b) Worker HALTs if journal doesn't exist; orchestrator MUST
      init first.
- **Per-shard outcome / bypass-log conflict resolution** — must be
  source-verified at Phase 2 Q-I.3. Whether the existing
  `make_blob_journal_writer` append-only writer touches the same
  `JournalState` as `with_robots_bypass_appended`. If yes, there's
  a real concurrency issue to design around. If no (the append-
  only writer writes a SEPARATE blob log, not `JournalState`), the
  two write surfaces are independent and the design is simpler.
- **Explicit Phase 2 authorization for src/ touches not in Out-of-
  scope's allow-list**: any worker_loop / cost_journal touch
  beyond what Phase 2 authorizes HALTs per the S22+S23 "Implicit-
  authorization HALT for src/-locks" LESSONS pattern.

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
Session 24 AND operator has not authorized explicit placeholder
choices.

### Candidate B — Per-tier cost-accounting retrofit (closes Workstream 0)

The deferred-from-S14 per-tier cost-accounting wiring gap.
Currently severity LOW, carry-forward. Closing it would let
`workstream-0-end` tag be placed at the closing commit. Touches
the W4.1.5 driver area (`tests/runners/fixture_cascade/`) which
is locked except via W5.X-prefix commits per S16 precedent.
Estimated 100-200 LOC.

**Prerequisites:**
- Operator authorization at S24 Phase 1 for a W5.X-prefix commit
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
- Operator decision on which sections to trim and which to preserve.

Estimated <50 LOC of doc changes; no code; <30 minutes.

### Sub-question 1.TAG — Tag at session close (pinned at Phase 1)

Independent of scope choice; resolved fully here at Phase 1 so
Phase 5 has an unambiguous tag decision. Options per scope:

- **Candidate I** (durable persistence): defer (closing the S23
  deferral alone does not close a workstream-week milestone) OR
  place a candidate-specific tag if operator decides this commit
  warrants one — Phase 1 should resolve.
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

Per chosen Phase 1 candidate. Each candidate has its own sub-block.
Source-verify at session-current HEAD per `[[verify-before-asking-
discipline]]` AND per S22+S23 "Plan-vs-reality at Phase 2 source-
verify" LESSONS pattern BEFORE each AskUserQuestion batch.

**HALT IF** any Phase 2 decision would require modifications to
`src/barcada_scraper/` production code beyond what was Phase-2-
authorized (per S22+S23 "Implicit-authorization HALT for src/-
locks" LESSONS pattern; surface as an explicit AskUserQuestion
before patching) OR to the W4.1.5 driver (except via W5.X-prefix
per Candidate B's auth) OR to any S19/S20/S21/S22/S23 deliverable
— surface as a design-gate sub-question before patching.

### If Candidate I (durable bypass-audit persistence)

- **Q-I.1 abfss:// scope**: (a) file:// only with abfss:// HALTed
  at worker boot (Recommended — preserves Candidate I as small
  scope; abfss:// follow-up candidate); (b) file:// + abfss://
  both supported, requiring ADLSCostJournal Phase 5 skeleton
  completion (~150-250 LOC scope expansion); (c) abfss:// only
  (assumes production path; HALTs on `file://` URL — rejected
  unless operator deliberately switches to abfss-only deployment).
- **Q-I.2 Journal-init coordination**: (a) Worker calls
  `write_initial(JournalState.fresh(...))` if `j.exists()` is
  False (Recommended — worker is self-bootstrapping); (b) Worker
  HALTs at boot if journal doesn't exist (Orchestrator-must-init
  semantics; cleaner separation but adds operational dependency);
  (c) Worker writes a sentinel state and trusts orchestrator to
  reconcile (most complex; not recommended).
- **Q-I.3 Per-shard outcome / bypass-log conflict**: source-verify
  at Phase 2 whether the existing `make_blob_journal_writer`
  append-only writer in worker_loop.py:2814 writes to the same
  JournalState surface as the CostJournal handle would. Two
  outcomes:
  (a) They write to SEPARATE journal blobs (the per-shard writer
      writes a `.jsonl` ledger; the CostJournal writes the
      `run_<run_id>.json` state file). Design: independent writes,
      no conflict. (Likely the actual shape — source-verify.)
  (b) They write to the SAME JournalState (the per-shard outcome
      lands in `JournalState.shards` via the CostJournal). Design:
      every BYPASS_ALLOW write must coordinate with the per-shard
      outcome write via `update_with_retry`'s mutator chain.
- **Q-I.4 Writer construction site**: (a) Build the writer inside
  `scrape_stage2_pages_invoker` (Recommended — matches the S23
  log-only pattern; minimal change); (b) Hoist to module level as
  a factory function returning a writer closure; (c) Add a NEW
  helper in `orchestrator/robots_integration.py` (e.g.,
  `make_durable_bypass_writer(journal: CostJournal)`).
- **Q-I.5 Boot-time CostJournal handle scope**: (a) Open once per
  invoker invocation (per-shard); close at shard end (Recommended
  — matches existing invoker pattern); (b) Open once per worker
  process and share across shards (requires lifecycle management).
- **Q-I.6 Failure semantics**: when `record_bypass_audit` raises
  (e.g., journal-write fails after exponential retry exhausts),
  (a) Log + continue (drop the audit entry; matches S23 log-only
  current state's tolerance — Recommended); (b) Re-raise and let
  the BYPASS_ALLOW path fail (stricter; could halt the shard);
  (c) Buffer in memory + retry at shard close.
- **Q-I.7 Test corpus shape**: (a) Extend the S23 integration test
  with a new test driving `scrape_stage2_pages_invoker` (not just
  `_acquire_one_domain_t1` direct) end-to-end with a real
  LocalFSCostJournal-backed writer in tmp_path; (b) Add a new
  test file `tests/orchestrator/test_worker_loop_persistence.py`
  (separates persistence integration from gate-wiring integration).

### If Candidate A (barcada-drift)

Carry-forward from S22+S23 prompts (unchanged).
- Q-A.1 CLI namespace; Q-A.2 drift metric; Q-A.3 alert threshold;
  Q-A.4 input contract; Q-A.5 output shape; Q-A.6 test corpus.

### If Candidate B (per-tier cost-accounting retrofit)

Carry-forward from S22+S23 prompts (unchanged).
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

- **Q-SHARED.1 Commit shape**: per-module (S18+19+20+21+22+23
  default; Recommended) vs per-sub-surface bundled.

(Tag-at-close is resolved at Phase 1 Sub-question 1.TAG; Phase 5
reads that resolution directly without re-decision.)

---

## Phase 3 — Implementation (per-module commits, strict order)

Per Phase 2 commit-shape decision. Default = per-module. Each
commit must satisfy the 6-step per-commit checkpoint protocol
below.

### Non-interleaving rule (CRITICAL for bisectability)

If the chosen candidate has multiple sub-surfaces (e.g., Candidate I
may have URL-parser + writer-replacement + tests as potentially-
separable surfaces), do NOT interleave. Complete each sub-surface
fully before starting the next. Per S22+S23 precedent.

If a mid-sub-surface dependency on the other sub-surface emerges,
HALT and surface as a design-gate sub-question before continuing —
the dependency may indicate a Phase 2 question was missed. See
S23-folded LESSONS "Bisectability vs Phase-1-named commit shape"
for the pattern: if the smallest atomic bisectable unit straddles
a Phase-1-named commit boundary, surface for operator
authorization to deviate; do NOT pattern-apply Phase 1 wording.

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
    <new S24 test paths if any> -q
```

Expected: previous_baseline + N new tests, all passing. If failing
tests are NOT a deliberate consequence of the surface-under-test
→ HALT.

If Candidate H or another non-orchestrator candidate is chosen,
narrower invocations (480 / 538 baselines) are valid — see Phase 0
Step 0.5 "Narrower baselines" note.

**2. Ruff sanity (touched files only) + mid-implementation format
check per LESSONS**

```
.venv/bin/ruff check <touched paths>
.venv/bin/ruff format --check <touched paths>
```

If unclean → run `ruff format <touched paths>` and re-test; fold
the format-fix into the commit (per S19+S20+S21+S22+S23 pattern).
This is the LESSONS "Mid-implementation ruff format-check"
discipline applied to every Edit, not just pre-push.

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
`eval_data/` README + TAXONOMY_GAP_LOG + stage1_labels
modifications are expected to stay unstaged across sessions
(Sessions 8-23 precedent; S23 saw operator deviations where
eval_data was committed inter-session — Candidate-I commits MUST
NOT include eval_data changes).

**5. "Confirm to commit?" presented to operator**

Include in chat:
- Verification table from step 3
- Commit message file location (`/tmp/<id>-msg.txt`)
- File list to stage (M / A / D)

**6. After operator confirms**

Stage + commit + verify the new SHA landed (`git log --oneline -1`)
+ verify combined suite still passes on the new HEAD.

This 6-step protocol applies UNIFORMLY to every commit in Phase 3
(and Phase 6's workspace close-out commit). Mechanical; do not
skip steps.

### Cumulative test-count gate

Track combined-suite passing count at each commit boundary:

```
Phase 3 start                  : 932  (Session 23 close baseline)
After commit 1                 : >= 932 + N_commit_1_tests
After commit 2                 : >= 932 + N_commit_1_tests + N_commit_2_tests
...
```

**Rule**: the count NEVER decreases between checkpoints. A decrease
means a previously-passing test went red — regression. HALT.

Baseline pre-resolved at Phase 1 per Phase 0 Step 0.5: 932 is the
canonical S24 baseline for any candidate that touches the
orchestrator sub-surface (Candidate I definitely; Candidates B/E
likely; Candidate H not). Whichever baseline is bound at Phase 1,
hold it consistent across ALL Phase 3 commits in S24 — do not
switch mid-session.

---

## Phase 4 — Pre-push gate (whole-tree)

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 350+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

HALT IF any gate red. Never use `--no-verify`.

### eval_data WIP halt protocol (per LESSONS)

validate_consistency runs against working-tree state. Operator-WIP
edits to `eval_data/*.jsonl` can introduce schema violations that
fail the gate even though no S24 commit touches eval_data.

When this fires:
1. Confirm the failing row's content is in operator-WIP
   (`git diff eval_data/...`), not in committed HEAD
   (`git show HEAD:eval_data/...`).
2. Confirm the S24 commits do not touch eval_data
   (`git diff origin/main..HEAD -- eval_data/`).
3. Surface to operator with the exact row + reason + diff vs
   committed state.
4. Two paths: (a) operator-fix in WT, then re-run gate;
   (b) stash eval_data WIP, push, restore.
5. Do NOT auto-fix locked-artifact content.

S20+S22 precedent: operator chose (a). S21 + S23 did not need this
protocol at Phase 4 push.

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

- Append Session 24 entry to `~/crawler-audit/SESSION_LOG.md`
  including a **Canonical S24-close baseline** block with the
  exact pytest invocation + verified test count (per S22+S23
  LESSONS "Pin the S24 baseline for Phase 0 Step 0.5"; without
  this, S25 Phase 0 will infer from the "Combined headline"
  bullet and potentially HALT on accounting-mismatch).
- Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md` for
  Session 25 — explicitly pin the S25 Phase 0 workspace anchor
  SHA per S21+S22+S23 post-audit pattern (LESSONS "Workspace HEAD
  delta tolerance"); do not omit. After the close-out commit
  lands, expect **1-2 follow-up commits** pinning the actual SHA
  (S21 needed 1; S22 needed 2 — the second pinned the canonical
  baseline test count discovered during audit; S23 needed 1).
  The most recent follow-up commit's SHA is the canonical S25
  anchor; no hard ceiling on follow-up count, but each should
  narrow toward a fully self-contained handoff (no remaining
  placeholders or unverified claims).
- Update `~/crawler-audit/LESSONS.md` with any new forward-
  applicable patterns surfaced this session.
- Workspace close-out: 1 primary commit + 1-2 follow-up commits
  pinning the anchor SHA and any audit-surfaced corrections.
  Push workspace after operator confirms.

Note: drafting the next-session prompt (`SESSION_25_PROMPT.md`)
is NOT a built-in Phase 6 step. Per S20→S21, S21→S22, S22→S23,
S23→S24 precedent, prompt-drafting is an operator-commissioned
activity between sessions — not always-on close-out work. If the
operator asks for it explicitly at S24 close, draft it as a
separate follow-up; otherwise leave for the next session to
either operator-commission or scope out at S25 open.

---

## Acceptance criteria

**Per candidate (reduces if Phase 1 narrows scope):**

### Candidate I (durable bypass-audit persistence)

1. abfss:// scope resolved per Q-I.1; if file://-only chosen,
   abfss:// HALT path implemented + tested.
2. Journal-init coordination per Q-I.2 implemented; if
   worker-self-bootstrapping chosen, `write_initial` invoked when
   `j.exists()` returns False.
3. Per-shard outcome / bypass-log conflict resolved per Q-I.3 —
   either confirmed independent writes or coordinated via
   `update_with_retry` mutator chain.
4. Writer construction per Q-I.4; the production
   `_bypass_audit_writer` closure in `scrape_stage2_pages_invoker`
   replaced (or augmented) to call `record_bypass_audit`.
5. CostJournal handle scope per Q-I.5.
6. Failure semantics per Q-I.6 implemented + tested.
7. Test corpus per Q-I.7; at least one full-pipeline test driving
   `scrape_stage2_pages_invoker` with a real LocalFSCostJournal-
   backed writer + asserting persistence to
   `JournalState.robots_bypass_log`.
8. The S23 commit-5 integration test still passes unchanged
   (Candidate I extends the contract; does not replace or
   regress it).
9. Tag per 1.TAG (defer OR candidate-specific).

### Candidate A (barcada-drift)

Carry-forward from S22+S23 prompts (unchanged):
1. `barcada-drift` (or `barcada-baseline drift`) CLI works against
   ≥2 canary_runs parquets.
2. Drift metric per Q-A.2 implemented + tested.
3. Alert threshold per Q-A.3 implemented + tested.
4. Output shape per Q-A.5 documented + tested.

### Candidate B (per-tier cost-accounting retrofit)

Carry-forward from S22+S23 prompts (unchanged):
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

- **S1.** Combined suite at session close: existing 932 baseline
  + N new tests, all passing (Candidate I expectation). For
  narrower-baseline candidates (H), the baseline is the chosen
  narrower count + N new.
- **S2.** Pre-push gate runs green (incl. eval_data WIP halt
  protocol applied if needed).
- **S3.** Tag placed per Phase 1 Sub-question 1.TAG OR explicit
  defer.
- **S4.** Regression-protection checklist held (see "Out-of-scope"
  below). In particular: ALL S21+S22+S23 deliverables stay at the
  SHAs they landed at; their public APIs are unchanged. The 32
  robots-parser tests stay 32/32 green; the 30 robots_gate tests
  stay 30/30 green; the 30 robots_bypass_config tests stay 30/30
  green; the 43 cost_journal tests stay 43/43 green; the 13
  cost_journal_local + 2 cost_journal_adls tests stay 13/13 +
  2/2 green; the 35 robots_integration tests stay 35/35 green
  (or grow if Candidate I adds tests there with explicit
  authorization); the 74 vmss_worker + 129 job_runner + 152
  worker_loop tests stay green (or grow); the 4 integration
  tests stay 4/4 green (or grow).

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
  public API at `34a59b6`). Candidate I CONSUMES this module's
  public API via RobotsGate but MUST NOT MODIFY it.
- `tests/scraper/test_robots.py` (32 tests; pins stdlib quirks).

**S22 deliverables (Session 22 W A.1 W8 integration sub-surfaces):**
- `src/barcada_scraper/scraper/robots_gate.py` (shim; 339 LOC;
  public API at `ba87e7e`). Candidate I CONSUMES the public API
  but MUST NOT MODIFY it.
- `tests/scraper/test_robots_gate.py` (30 tests).
- `src/barcada_scraper/scraper/robots_bypass_config.py` (loader;
  178 LOC; public API at `381ee89`). Candidate I CONSUMES the
  loader but MUST NOT MODIFY it.
- `tests/scraper/test_robots_bypass_config.py` (30 tests).
- The S22 ADDITIONS to `src/barcada_scraper/classifier/pipeline/
  cost_journal.py` (`BypassAuditEntry` dataclass; `JournalState.
  robots_bypass_log` field; `with_robots_bypass_appended` method;
  `to_dict` / `from_dict` / `_replace` updates; `__all__`
  extension) are LOCKED at the shape that landed at `1d9404e`.
  Candidate I CONSUMES `with_robots_bypass_appended` +
  `update_with_retry` + `open_journal` + `LocalFSCostJournal` /
  `ADLSCostJournal` but MUST NOT MODIFY their landed S22 shapes.
  ADLSCostJournal's Phase-5 SKELETON status is the design point
  Q-I.1 navigates. The pre-S22 portions of `cost_journal.py`
  (CostTotals, ShardRecord, CeilingHistoryEntry, the existing
  builders, retry helper, factory) remain locked as before.
  ADDING new helpers (e.g., a URL→handle parser) within or
  alongside `cost_journal.py` is allowed only if Phase 2 design-
  gate explicitly authorizes the touch.
- The S22 ADDITIONS to `tests/classifier/pipeline/test_cost_journal.py`
  (14 new tests + 1 updated `test_to_dict_emits_canonical_keys`)
  are locked. Adding new tests is allowed; modifying the S22
  tests requires explicit authorization.
- `docs/CRAWLING_POLICY.md` (202 lines / 8.1 KB; at `fdc8a7a`).
  Candidate H is the ONLY candidate that may modify this file.
  Other candidates MUST NOT.

**S23 deliverables (Session 23 W A.2 sub-surfaces — NEW for S24
lock-list):**
- `src/barcada_scraper/orchestrator/robots_integration.py`
  (244 LOC; public API at `279bb77`: `build_robots_gate`,
  `prewarm_robots_for_url`, `make_robots_disallow_row_fields`,
  `record_bypass_audit`, `load_bypass_config_or_empty`,
  `ROBOTS_DISALLOW_ERROR_KIND`). Candidate I CONSUMES
  `record_bypass_audit` and may ADD a new helper here (e.g.,
  `make_durable_bypass_writer(journal)` per Q-I.4 option (c))
  IF Phase 2 explicitly authorizes. Modifying the S23-landed
  public surface beyond additive growth requires explicit
  authorization.
- `tests/orchestrator/test_robots_integration.py` (35 tests at
  `279bb77`). Locked at the landed shape; adding new tests is
  allowed.
- The S23 ADDITIONS to `src/barcada_scraper/orchestrator/
  vmss_worker.py` (`WorkerConfig.robots_bypass_config_path` field
  + env reader at `5eeaac7`). Locked at the landed shape;
  Candidate I CONSUMES the field but does NOT modify it (the
  field already carries the path Candidate I reads).
- The S23 ADDITIONS to `tests/orchestrator/test_vmss_worker.py`
  (7 new tests at `5eeaac7`). Locked; adding new tests is allowed.
- The S23 ADDITIONS to `src/barcada_scraper/orchestrator/
  job_runner.py` (`JobRunArgs.robots_bypass_config_path` field +
  `--robots-bypass-config` CLI flag + `render_cloud_init` kwarg
  + `BARCADA_ROBOTS_BYPASS_CONFIG` substitution + both call sites
  at `872527e`). Locked at the landed shape. Candidate I does NOT
  modify these (the operator-CLI → worker-env chain is
  established; Candidate I is the worker-side terminal consumer).
- The S23 ADDITIONS to `tests/orchestrator/test_job_runner.py`
  (8 new tests at `872527e`). Locked; adding new tests is allowed.
- The S23 ADDITIONS to `scripts/vmss/cloud_init.template.yaml`
  (placeholder + -e line at `872527e`). Locked.
- The S23 ADDITIONS to `src/barcada_scraper/orchestrator/
  worker_loop.py` at `4ec7b0a`: the imports block additions, the
  new `bypass_config` + `bypass_audit_writer` kwargs on
  `_acquire_one_domain_t1`, the gate construction + prewarm
  helper, the 3-site gate wiring, and the
  `scrape_stage2_pages_invoker` `load_bypass_config_or_empty`
  call. The kwargs' public shape on `_acquire_one_domain_t1` is
  LOCKED — Candidate I REPLACES the production
  `_bypass_audit_writer` closure body in
  `scrape_stage2_pages_invoker` with a durable one, but MUST
  preserve the kwargs' shape so the integration test at
  `tests/orchestrator/test_robots_gate_integration.py` continues
  to pass.
- The S23 ADDITIONS to `tests/orchestrator/test_worker_loop.py`
  (6 new tests at `4ec7b0a`). Locked; adding new tests is allowed.
- `tests/orchestrator/test_robots_gate_integration.py` (NEW file
  at `6e6e4ca`; 4 tests). LOCKED at the landed shape. Candidate I
  MUST NOT modify the existing 4 tests; adding new tests in this
  file (or a new parallel file) is allowed per Q-I.7.

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
- All workstream tags at their placed SHAs (10 tags as of S23
  close; new tags only via Phase 5 explicit placement)
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` (READ-ONLY)
- `CLASSIFICATION_ADJACENT_PLAN.md` (UPDATED only when AI/ML
  decisions land)
- `RECONCILIATION_2026-05-21.md`
- `docs/phase4_implementation_plan.md` (Phase 4 governance
  reference)

**Operator-owned territory:**
- All of `eval_data/` — labeling-workstream territory; per-row WIP
  edits across sessions are expected and unstaged (Sessions 8-23
  precedent). S22→S23 + S23→S24 inter-session operator-side
  eval_data COMMITS are tolerated per the "Workspace HEAD delta
  tolerance" LESSONS pattern — verify they're eval_data-only via
  `git show --stat <sha>` for each commit in the delta.

**Production code:**
- `src/barcada_scraper/` — locked unless Phase 2 design-gate
  explicitly authorizes a specific module. S21 authorized
  `scraper/robots.py`; S22 authorized `scraper/robots_gate.py`,
  `scraper/robots_bypass_config.py`, AND (via mid-Phase-3 explicit
  operator authorization) the additive surface in
  `classifier/pipeline/cost_journal.py`; S23 authorized
  `orchestrator/robots_integration.py` (new), additive surfaces
  in `orchestrator/vmss_worker.py`, `orchestrator/job_runner.py`,
  `orchestrator/worker_loop.py`. Those authorizations do NOT
  extend to other src/ modules or to further modifications of
  the authorized files beyond their landed S21/S22/S23 shapes.
  Candidate I's `worker_loop.py` `_bypass_audit_writer`-closure
  replacement is allowed (additive: replaces the closure body
  in `scrape_stage2_pages_invoker`; preserves all other
  worker_loop.py surfaces). Any other worker_loop.py / fetcher_
  core.py / robots_integration.py touch beyond what Phase 2
  authorizes HALTs per the S22+S23 "Implicit-authorization HALT
  for src/-locks" LESSONS pattern.

**Pipeline configs:**
- `configs/`

**Phase 4 work:**
- Phase 4 PR-D/E/F/G work opens only when Workstream 0 fully
  closes AND operator-led Stage 2/3 labeling work begins

---

## Verify-before-asking discipline (strict rule from S19+S20+S21+S22+S23)

Per `[[double-check-before-commit]]` memory: **ALWAYS verify every
concrete claim in the commit message against actual source/output
BEFORE staging.** Fixture names, file counts, exit codes, line
counts, test counts, helper names, smoke outcomes, SHA prefixes,
regex matches, API signatures. No claims by pattern-completion.
Build a verification table in chat (claim → reality → status) and
reconcile before "Confirm to commit?".

Specific to S24:

- Before each chosen-candidate-specific claim in a commit message,
  verify against the actual source / runtime output:
  - Candidate I: `open_journal` factory works with the
    parsed-from-URL inputs; worker-side `j.exists()` + `j.read()`
    + `update_with_retry` paths exercise correctly; the S23
    integration test still passes alongside the new one.
  - Candidate B: per-tier cost-journal field presence.
  - Candidate E: cassette counts post-record.
  - Candidate H: doc byte count post-trim matches Q-H.1 target.
- Before claiming combined suite count, re-run pytest.
- Before claiming ruff/format clean, re-run ruff against the
  touched files.
- Before claiming a SHA prefix in a commit message body, verify the
  prefix is correct via `git show --no-patch --format=%h <ref>`.

Avoid bash pipe artifacts that mask Python exit codes (LESSONS):
`python_cmd 2>&1 | grep ... | tail` makes `$?` reflect tail's exit.
Use `> stdout.out 2> stderr.err; echo $?` or `${PIPESTATUS[0]}`
when exit-code matters.

LESSONS-folded discoveries from S22+S23 worth re-applying if S24
takes Candidate I:

- Plan-vs-reality at Phase 2 (S22 LESSONS): plan §5 wording said
  "integrate into `link_discovery.py`" but that module is pure-
  function. Verify the actual integration site via Explore BEFORE
  drafting Q-I.* options. The S23 worker_loop.py touches established
  the integration seam at `scrape_stage2_pages_invoker`'s
  `_bypass_audit_writer` closure — confirm this is unchanged at
  S24 Phase 0.
- Implicit-authorization HALT (S22+S23 LESSONS): Q-I.* answers
  may require touching `worker_loop.py` and/or `cost_journal.py`
  (e.g., for the abfss:// → handle parser) which are NOT in S24
  Out-of-scope's authorized-touch list. Surface explicit
  authorization in Phase 2 BEFORE the commit, not as a HALT
  mid-Phase-3.
- Bisectability vs Phase-1-named commit shape (S23 LESSONS):
  Candidate I likely has 2-3 sub-surfaces (URL→handle parser /
  writer-replacement / tests). If an architectural constraint
  forces atomic file-pairs that span the Phase-1-named boundary,
  surface for operator authorization to deviate (per S23
  commit-2 precedent).
- Production-vs-test journal asymmetry (S23 LESSONS): the
  Candidate I work IS the resolution of this asymmetry for the
  bypass-audit path. Apply the pattern carefully — make sure the
  durable path doesn't accidentally break the existing
  per-shard-outcome append-only writer.
- Source-verify line numbers per Phase 3 commit (S23 LESSONS):
  worker_loop.py is now ~2993 LOC post-S23 (~2884 pre-S23 +
  ~109 S23 additions); re-Explore at session-current HEAD
  before drafting commit edits.
- Cumulative test-count gate with new-file invocation expansion
  (S23 LESSONS): bookkeeping discipline still applies in commit
  bodies.
- Frozen-dataclass field tests pin cross-package contracts
  (implicit S23 pattern): if Candidate I adds new dataclass
  fields, mirror the `FrozenInstanceError` + `__dataclass_fields__`
  introspection pattern.

---

## Commit hygiene (per LESSONS + S19/S20/S21/S22/S23 additions)

- File-based commit messages at `/tmp/<id>-msg.txt`.
- Per-module commits (Phase 3 commit shape unless Q-SHARED.1
  overrides).
- "Confirm to commit?" before EVERY commit. Pair with verification
  table (always) and `git diff --staged` (when appropriate per
  `[[double-check-before-commit]]` triggers).
- Commit body includes: action ref (e.g., `WA2.W8.bypass-persistence`
  or `WI.bypass-persistence` for Candidate I — operator picks the
  prefix at Phase 1), scope summary, file touches, test count
  delta (with net-new vs newly-in-invocation pre-existing
  distinction per S23 LESSONS), plan reference. NO `Co-Authored-By`.
- Pre-push gate must run green. Never use `--no-verify`.
- Pre-push vermin: `git ls-files '*.py' | xargs vermin
  --target=3.10` to filter venv-internal pytest 3.14 false-
  positives.
- Mid-implementation ruff format-check, not only pre-push.
- Sibling-module style consistency for one-file additions — match
  the immediate sibling's conventions even where they technically
  violate project-wide rules; **disclose explicitly in the commit
  body** (S21+S22 LESSONS finding).
- For S23 surface modifications: if Phase 2 explicitly authorizes
  modifying the S23-landed shape of `robots_integration.py` (e.g.,
  adding a new public helper per Q-I.4 option (c)), the commit
  body MUST explicitly disclose the modification with reason
  (S22+S23 LESSONS "Implicit-authorization HALT" pattern).
- Workspace close-out (Phase 6) lands as its own commit at session
  close, followed by 1 follow-up commit pinning the anchor SHA
  for the next session (S21+S22+S23 pattern).

---

## Context-window awareness

S23 ran across 5 commits + Phase 2 source-verification + 2
Explore-subagent surveys + 1 mid-Phase-3 bisectability adjustment,
well within context. S24 budget per scope:

- Candidate I: small-medium (50-100 LOC + tests + CostJournal
  handle plumbing). Likely needs 2-3 per-module commits.
- Candidate A: medium-large (~300 LOC).
- Candidate B: small-medium (100-200 LOC; sensitive driver-area
  touch).
- Candidate D/E: small.
- Candidate H: very small (<50 LOC of doc edits; <30 minutes).

Strategies:
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore subagent
  per S22+S23 "Explore-subagent + spot-check" LESSONS pattern.
- For any live-HTTP corpus work (Candidate E), pilot with 1-3
  cassettes first per S18+S20 staged-rollout pattern.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before the chosen S24 scope closes,
  transition per "no mid-commit-batch transitions" — finish
  in-flight sub-surface, then close session and refill the
  transition template for Session 25.

---

## Reporting in chat at session close

After all Session 24 commits land + push + close-out per the
S13-23 pattern:

1. Commit SHA(s) of each S24 sub-surface.
2. Sub-surface(s) landed (per candidate).
3. Test count delta: 932 (or 480/538) baseline → S24 close.
4. Driver suite count at S24 close (46/46 expected unless
   Candidate B W5.X-prefix realigned).
5. Files touched per sub-surface.
6. Tag dispositions (incl. any new tag per 1.TAG).
7. Per-tier cost-accounting wiring gap disposition: patched
   (Candidate B) or carry-forward.
8. Durable bypass-audit persistence disposition: shipped
   (Candidate I) or carry-forward.
9. Any spend (LLM, infrastructure, cassette-capture).
10. Robots.txt compliance log (if Candidate I did live work or
    Candidate E expanded the cassette corpus).
11. FP-curation log update (if Candidate E expanded the cassette
    corpus).
12. Verify-before-asking summary: any source-verification findings
    surfaced.
13. Outstanding items for Session 25.
14. Tags state at S24 close.

Do not propose Phase 4 PR-D/E/F/G work this session unless
Candidate D was chosen and operator-led labeling is in flight.

---

## Carry-forward bakes (no amendment file needed)

All S23 amendments (close-out commit `8d99c98` + follow-up
`8f8e51f`) plus the S23 post-close verification have been folded
directly into this prompt — S24 does not need a separate amendment
file:

- **S23 close-out corrections** folded into Step 0.1 (workspace
  anchor `8f8e51f`; repo anchor `6e6e4ca` with operator-eval_data-
  commit tolerance), Step 0.5 (Canonical S23-close baseline 932
  pinned with 15-path invocation + sub-totals), Step 0.9 (S23-
  shipped public API stability check covers all 5 S23 modules +
  the cloud-init template artifacts).
- **5 LESSONS sections from S23 close** referenced where they
  apply: Bisectability vs Phase-1-named commit shape (Phase 3
  non-interleaving rule); Production-vs-test journal asymmetry
  (Candidate I IS the resolution; Q-I.1 navigates the residual
  abfss:// asymmetry); Source-verify line numbers per Phase 3
  commit (Phase 2 + Phase 3 source-verify); Cumulative test-count
  gate with new-file invocation expansion (Phase 3 commit body
  discipline); False-premise verification questions during
  Phase 2 (verify-before-asking discipline).

If new amendments arise pre-S24 open, walk them per the reviewer-
feedback hygiene pattern in this prompt's "Reviewer-feedback
hygiene" section.
