# Session 23 prompt — scope picked at Phase 1
# (W A.1 closed at S22; S23 chooses from W A.2 integration NEW
#  + carry-forwards A/B/D/E from S21/S22 + Candidate H docs-tightening)

**Drafted at Session 22 close (2026-05-23).** Mirrors the S20/S21/S22
prompt structure. Scope-agnostic at Phases 0/1; scope-specific design
gates at Phase 2 per chosen candidate. Strict 7-phase ordering with
halt-on-mismatch preserved.

This prompt should be invoked from `~/Downloads/session-23-prompt.md`
(operator-mirrored) or directly from
`~/crawler-audit/SESSION_23_PROMPT.md`. Re-read it on session open.

---

## Scope

Engineering session. Workstream sub-surfaces available after Session
22 closed `WA1.W8.*` (4 commits) and placed
`workstream-a-week1-end` at `fdc8a7a`:

- **W A.1 shipped fully** — parser (`scraper/robots.py` @
  `34a59b6`), gate shim (`scraper/robots_gate.py` @ `ba87e7e`),
  bypass-config loader (`scraper/robots_bypass_config.py` @
  `381ee89`), cost-journal audit-log field (`classifier/pipeline/
  cost_journal.py` partial @ `1d9404e`), and `docs/CRAWLING_POLICY.md`
  (@ `fdc8a7a`). NOT YET integrated into the orchestrator fetcher
  seam — `worker_loop` / `fetcher_core` consumption of `RobotsGate`
  is the deferred W A.2 work (S22 Q-F.1 explicitly chose the
  shim-only path because the production fetcher is async/httpx
  while `RobotsPolicy` is sync/requests; sync/async bridge is
  W A.2 territory).
- **W A.2 integration (NEW Candidate G)** — wires `RobotsGate`
  into the orchestrator's pre-fetch site, hands the
  `BypassAuthorization` to the cost journal via the new
  `with_robots_bypass_appended` method, loads the bypass sidecar
  at orchestrator startup. Resolves the sync-vs-async impedance
  mismatch. Closes the end-to-end W A.1 robots flow in production.
- **Per-tier cost-accounting wiring gap (Candidate B)** — carry-
  forward from S14; severity LOW; closing it would justify
  `workstream-0-end` tag.
- **barcada-drift (Candidate A)** — deferred per Q1.1=(A) at S20;
  still needs 4 AI/ML decisions per CLASSIFICATION_ADJACENT_PLAN.md
  §Item 8 AND 2+ `canary_runs/*.parquet` files (earliest natural
  date 2026-06-06 if the launchd installer has fired ≥2 Saturdays
  since S20 close).
- **Phase 4 PR-D tooling (Candidate D)** — operator-led labeling
  territory.
- **Cassette corpus expansion (Candidate E)** — current 20 is lower
  bound of plan's "~20-30".
- **CRAWLING_POLICY.md tightening (Candidate H; NEW small)** — S22
  doc shipped at 8.1 KB vs the Q-F.6 ~1-2 KB estimate; trim to
  ~2-3 KB while preserving essential robots contract. <50 LOC.

Operator chooses at Phase 1 which candidate Session 23 ships. Each
candidate has its own Phase 2 design-gate template.

**Sessions 13-22 precedent:** this session does NOT modify the
W4.1.5 driver orchestration at `tests/runners/fixture_cascade/`
(locked at `dd64963`). Does NOT modify `expected.schema.json` v1.1
/ `META_SCHEMA.md` v1.1. Does NOT modify the committed
`tests/fixtures/baseline-v0/` snapshot at `9e9a1fb`. Does NOT
modify the Session 19 `check` sub-surface code or the Session 20
cassettes/canary sub-surface code or the Session 21 `robots.py`
parser at `34a59b6` or its tests, OR the Session 22 deliverables:
`scraper/robots_gate.py` @ `ba87e7e`, `scraper/robots_bypass_config.py`
@ `381ee89`, the `BypassAuditEntry` + `robots_bypass_log` additions
to `classifier/pipeline/cost_journal.py` @ `1d9404e`, and
`docs/CRAWLING_POLICY.md` @ `fdc8a7a`. Does NOT modify production
code under `src/barcada_scraper/` UNLESS Phase 2 design-gate
explicitly authorizes a specific module.

Full regression-protection checklist in **Out-of-scope** at the end
of this prompt. Re-read it before any code lands.

---

## Reviewer-feedback hygiene (if this prompt is reviewed)

If an external reviewer (operator-invoked) flags items in this
prompt before Session 23 starts, walk each flagged item against
on-disk reality at HEAD `fdc8a7a` (repo) and `8e6a7de` (workspace)
BEFORE applying any change. Per S19/S20/S21/S22 pattern (LESSONS
"Reviewer-feedback hygiene"):

- **OBSOLETE** items: SHAs already verified, claims already true.
  Skip with documented reasoning.
- **VALID-applies-now** items: bear on this session's scope. Apply.
- **VALID-applies-later** items: bear on deferred scope. Carry
  forward to the next prompt revision.
- **WRONG-PREMISE** items: assumes something not true. Skip with
  documented reasoning.

Empirical baseline: at S19 review 3 of 5 "must-fix" items collapsed
under cold-start verification; at S20 review 1 of 12 amendments was
skipped because it would HALT spuriously (SR-4); at S21 post-close
audit 2 of 3 operator-feedback items required workspace-doc
corrections; at S22 post-close audit 2 of 3 operator-feedback items
required SESSION_LOG baseline-pin + template anchor-SHA fixes.
Do not pattern-apply; verify each.

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
decisions for A; W5.X-prefix auth for B; sync/async-bridge
decision not pre-resolved for G). Phase 2 halts catch hidden
scope expansion (especially implicit src/ touches not enumerated
in Out-of-scope per S22 LESSONS). Phase 3 halts catch regressions.
Phase 4 halts catch pre-push gate failures (incl. operator-WIP-in-
locked-tree).

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

Run in order. Halt and surface to operator on any mismatch.

### Step 0.1 — Workspace + repo HEAD

```
# Workspace at Session 23 start (Session 22 close-out + 2 follow-up
# commits, all pushed):
git -C ~/crawler-audit rev-parse HEAD
# Expect: 8e6a7de (S22 close-out follow-up 2: pin S23 baseline
# suite total + correct anchor SHA) OR a later commit if additional
# workspace doc edits landed post-S22-close. If N commits ahead,
# verify each prior commit's subject via
# `git log --oneline 8e6a7de..HEAD` against expected prompt-
# finalization / doc-edit patterns; surface the SHA delta and
# request authorization to proceed if anything is unexpected.
# (S20/S21/S22 precedent: operator authorized continuation when
# 2-3 extra workspace commits were the strengthened prompts themselves.)

# Repo at Session 22 final commit:
git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: fdc8a7a (WA1.W8.crawling-policy-doc)
```

### Step 0.2 — Tags (no change from S22 close)

```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort
# Expect 10 tags (unchanged from S22 close):
#   baseline-v0
#   pre-remediation-2026-05-19
#   workstream-0-week1-end
#   workstream-0-week2-end
#   workstream-0-week3-end
#   workstream-0-week4-1-5-end
#   workstream-0-week4-end
#   workstream-0-week5-end
#   workstream-0-week7-end
#   workstream-a-week1-end           <-- NEW S22 at fdc8a7a
```

### Step 0.3 — Driver locked

```
cd /Users/administrator/projects/barcada-scraper
git diff dd64963..HEAD -- tests/runners/fixture_cascade/ \
    ':(exclude)tests/runners/fixture_cascade/test_fixture_fetcher.py'
# Expect: empty (only test_fixture_fetcher.py changed via W5.X
# realign at 8d0fc0e in Session 16).
```

### Step 0.4 — Fixture counts (no change from S22 close)

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

### Step 0.5 — Test-suite baseline

```
.venv/bin/python -m pytest tests/scraper/test_fixture_conformance.py \
    tests/runners/fixture_cascade/ tests/baseline_v0/ \
    tests/synthetic_crawl/ tests/scraper/test_robots.py \
    tests/scraper/test_robots_gate.py \
    tests/scraper/test_robots_bypass_config.py -q
# Expect: 480 passed / 0 failed / 0 skipped
#         (= 210 conformance + 46 driver + 99 baseline_v0
#          + 33 synthetic_crawl + 32 robots + 30 robots_gate
#          + 30 robots_bypass_config = 480)
#
# Pinned in SESSION_LOG.md "Canonical S22-close baseline" block.
# Re-verified post-S22-close-out at HEAD fdc8a7a.
```

The sub-paths add up to the headline: 210 + 46 + 99 + 33 + 32 + 30
+ 30 = 480. Any drift = halt.

If the headline mismatches, re-run each sub-path independently to
localize which sub-suite drifted:

```
.venv/bin/python -m pytest tests/scraper/test_fixture_conformance.py -q     # expect 210
.venv/bin/python -m pytest tests/runners/fixture_cascade/ -q                # expect  46
.venv/bin/python -m pytest tests/baseline_v0/ -q                            # expect  99
.venv/bin/python -m pytest tests/synthetic_crawl/ -q                        # expect  33
.venv/bin/python -m pytest tests/scraper/test_robots.py -q                  # expect  32
.venv/bin/python -m pytest tests/scraper/test_robots_gate.py -q             # expect  30
.venv/bin/python -m pytest tests/scraper/test_robots_bypass_config.py -q    # expect  30
```

If S23 scope touches the cost journal, also use the broader suite
(adds classifier/pipeline tests; total 538):

```
.venv/bin/python -m pytest tests/scraper/test_fixture_conformance.py \
    tests/runners/fixture_cascade/ tests/baseline_v0/ \
    tests/synthetic_crawl/ tests/scraper/test_robots.py \
    tests/scraper/test_robots_gate.py \
    tests/scraper/test_robots_bypass_config.py \
    tests/classifier/pipeline/test_cost_journal.py \
    tests/classifier/pipeline/test_cost_journal_local.py \
    tests/classifier/pipeline/test_cost_journal_adls.py -q
# Expect: 538 passed (480 + 58 journal)
```

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

# S22 cost-journal field additions (14 new + 44 prior = 58 total)
.venv/bin/python -m pytest tests/classifier/pipeline/test_cost_journal.py -q
# Expect: 58 passed
```

### Step 0.9 — S22-shipped public API stability (Candidate G prereq)

```
# If Candidate G (W A.2 integration) is even possibly in scope,
# verify the PUBLIC integration contracts of all 4 S22-shipped
# modules match what landed at S22 close. A change to any of these
# between S22 close and S23 open would invalidate the W A.2
# integration design.
#
# Scope: only what W A.2 callers depend on:
#   RobotsGate(policy, bypass_config, honor_crawl_delay, clock).evaluate(url)
#     -> GateDecision(action, reason, crawl_delay, bypass)
#   BypassEntry(authorized_by, reason, expires_iso=None)
#   BypassAuthorization(host, url, user_agent, robots_reason,
#                       authorized_by, bypass_reason, authorized_at_iso)
#   GATE_ACTION_ALLOW / GATE_ACTION_SKIP / GATE_ACTION_BYPASS_ALLOW
#   DRIFT_SIGNAL_PREFIX = "robots_gate.drift_signal"
#   load_bypass_config(path) -> dict[str, BypassEntry]
#   loads_bypass_config(payload) -> dict[str, BypassEntry]
#   BypassConfigError(ValueError)
#   JournalState.with_robots_bypass_appended(entry) -> JournalState
#   JournalState.robots_bypass_log: tuple[BypassAuditEntry, ...]
#   BypassAuditEntry(host, url, user_agent, robots_reason,
#                    authorized_by, bypass_reason, authorized_at_iso)

.venv/bin/python -c "
import inspect
from barcada_scraper.scraper.robots_gate import (
    RobotsGate, GateDecision, BypassEntry, BypassAuthorization,
    GATE_ACTION_ALLOW, GATE_ACTION_SKIP, GATE_ACTION_BYPASS_ALLOW,
    DRIFT_SIGNAL_PREFIX, ALL_GATE_ACTIONS,
)
from barcada_scraper.scraper.robots_bypass_config import (
    load_bypass_config, loads_bypass_config, BypassConfigError,
    REQUIRED_FIELDS, OPTIONAL_FIELDS, ALLOWED_FIELDS,
)
from barcada_scraper.classifier.pipeline.cost_journal import (
    JournalState, BypassAuditEntry,
)

# RobotsGate constructor + evaluate signature
init_params = set(inspect.signature(RobotsGate.__init__).parameters)
assert {'self', 'policy', 'bypass_config', 'honor_crawl_delay', 'clock'} == init_params, init_params
evaluate_params = set(inspect.signature(RobotsGate.evaluate).parameters)
assert {'self', 'url'} == evaluate_params, evaluate_params

# Dataclass field sets
assert {f.name for f in GateDecision.__dataclass_fields__.values()} == \
    {'action', 'reason', 'crawl_delay', 'bypass'}, 'GateDecision drifted'
assert {f.name for f in BypassEntry.__dataclass_fields__.values()} == \
    {'authorized_by', 'reason', 'expires_iso'}, 'BypassEntry drifted'
assert {f.name for f in BypassAuthorization.__dataclass_fields__.values()} == \
    {'host', 'url', 'user_agent', 'robots_reason', 'authorized_by',
     'bypass_reason', 'authorized_at_iso'}, 'BypassAuthorization drifted'
assert {f.name for f in BypassAuditEntry.__dataclass_fields__.values()} == \
    {'host', 'url', 'user_agent', 'robots_reason', 'authorized_by',
     'bypass_reason', 'authorized_at_iso'}, 'BypassAuditEntry drifted'

# Module constants
assert GATE_ACTION_ALLOW == 'allow'
assert GATE_ACTION_SKIP == 'skip'
assert GATE_ACTION_BYPASS_ALLOW == 'bypass_allow'
assert DRIFT_SIGNAL_PREFIX == 'robots_gate.drift_signal'
assert ALL_GATE_ACTIONS == (GATE_ACTION_ALLOW, GATE_ACTION_SKIP, GATE_ACTION_BYPASS_ALLOW)
assert REQUIRED_FIELDS == ('authorized_by', 'reason')
assert OPTIONAL_FIELDS == ('expires_iso',)
assert ALLOWED_FIELDS == REQUIRED_FIELDS + OPTIONAL_FIELDS
assert issubclass(BypassConfigError, ValueError)

# Loader signatures
assert 'path' in set(inspect.signature(load_bypass_config).parameters)
assert 'payload' in set(inspect.signature(loads_bypass_config).parameters)

# JournalState new method + field
assert 'entry' in set(inspect.signature(JournalState.with_robots_bypass_appended).parameters)
s = JournalState.fresh(run_id='x', ceiling_usd=1.0)
assert s.robots_bypass_log == ()

print('OK all 4 S22-shipped public APIs unchanged from S22 close')
"
```

If any of 0.1-0.9 fail, HALT before doing any work.

---

## Required workspace reading (Session 23 first 10 minutes)

In this order:

1. **`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`** — full
   handoff state at S22 close. Lists 5 scope candidates (G new +
   A/B/D/E carry-forward + H new small) with prerequisites +
   estimated scope. The S23 scope choice at Phase 1 picks from these.

2. **`~/crawler-audit/SESSION_LOG.md`** Session 22 entry — what
   landed during W A.1 W8 integration (4 commits). The Phase 2
   plan-vs-reality finding (link_discovery.py is pure-function).
   The mid-Phase-3 implicit-authorization HALT for the cost_journal.py
   touch. The 5 forward-applicable patterns at the end.

3. **`~/crawler-audit/LESSONS.md`** — 5 new sections folded at S22
   close, at end of file. Locate via
   `grep -n '^## .*(S22 folding)' LESSONS.md`. Especially:
   - "Plan-vs-reality at Phase 2 source-verify" — directly applicable
     if Candidate G integrates `RobotsGate` (worker_loop is 2884 LOC;
     verify the actual pre-fetch site before drafting Phase 2 Q-G.1).
   - "Implicit-authorization HALT for src/-locks" — directly
     applicable. Q-G.* answers will likely require touching
     `orchestrator/worker_loop.py` or `classifier/page_acquisition/
     fetcher_core.py` — neither enumerated in S23 Out-of-scope.
     Surface for explicit authorization before commit, not after.
   - "Parallel-dataclass pattern across package boundaries" —
     applicable if Candidate G needs additional cross-package
     records.
   - "Per-module commit shape scales to 4+ commits cleanly" —
     Q-SHARED.1 likely chooses per-module again.
   - "Phase-2 estimate-vs-actual disclosure in commit body" —
     applicable to any candidate whose Phase 2 cites a LOC estimate.

4. **`~/crawler-audit/BARCADA_CRAWLER_REMEDIATION_PLAN.md`** —
   chosen-scope section per Phase 1 candidate choice. Plan is
   READ-ONLY.

5. **`~/crawler-audit/CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8
   — only if Candidate A (barcada-drift) is chosen.

6. **`~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md`** —
   only if Candidate B (per-tier cost-accounting retrofit) is
   chosen. READ-ONLY.

7. **`src/barcada_scraper/scraper/robots_gate.py`** at `ba87e7e` —
   only if Candidate G is chosen. The public API (`RobotsGate.evaluate`,
   `GateDecision`, `GATE_ACTION_*`) is what callers integrate
   against. Read top-to-bottom; ~339 LOC.

8. **`src/barcada_scraper/scraper/robots_bypass_config.py`** at
   `381ee89` — only if Candidate G is chosen. The loader the
   orchestrator will call at startup; ~178 LOC.

9. **`src/barcada_scraper/classifier/pipeline/cost_journal.py`** at
   `1d9404e` — only if Candidate G is chosen. The
   `with_robots_bypass_appended` method is what the integration
   calls per-bypass; the `update_with_retry` helper at L384 is
   what wraps it for ETag-conditional persistence; ~599 LOC total.

10. **`docs/CRAWLING_POLICY.md`** at `fdc8a7a` — only if Candidate
    G needs the operational defaults reference OR if Candidate H
    (doc tightening) is chosen. ~202 lines / 8.1 KB.

11. **`src/barcada_scraper/orchestrator/worker_loop.py`** — only
    if Candidate G is chosen. The integration site; ~2884 LOC.
    Use Explore subagent per S22 "Explore-subagent + spot-check"
    LESSONS pattern; do NOT attempt to read top-to-bottom.

12. **`src/barcada_scraper/classifier/page_acquisition/fetcher_core.py`**
    — only if Candidate G is chosen. The async/httpx fetcher path;
    `fetch_one` at L169.

---

## Phase 1 — Scope resolution (no code; pre-design-gate)

Operator picks one candidate. Candidates ordered by prerequisite-
readiness; each is independent.

### Candidate G — W A.2 worker_loop / fetcher_core integration (NEW; Recommended)

The natural follow-on to S22's shim-only ship. Wires `RobotsGate`
into the orchestrator's pre-fetch site so URLs are actually gated
before any HTTP request fires. Closes the end-to-end W A.1 flow
in production.

Scope (per BARCADA_CRAWLER_REMEDIATION_PLAN.md §5 Workstream A
Action #2 acceptance criteria, end-to-end):
- Resolve the sync-`RobotsPolicy` vs. async-`fetcher_core`
  impedance mismatch. Two paths:
  (i) async-wrap `RobotsPolicy.check` (or build an async sibling
      using `httpx.AsyncClient`),
  (ii) keep `RobotsPolicy` sync and call `RobotsGate.evaluate`
       from a sync boundary in `worker_loop` BEFORE entering
       the async fetcher path.
- Wire `RobotsGate.evaluate(url)` into the right pre-fetch site
  in `worker_loop._acquire_one_domain_t1` (or equivalent —
  verify at Phase 0/2 via Explore).
- Wire `load_bypass_config(path)` at orchestrator startup with
  a path supplied by CLI flag / env var / config-file entry
  (Phase 2 decision).
- Wire the cost-journal `with_robots_bypass_appended` call so
  every `GATE_ACTION_BYPASS_ALLOW` decision actually persists
  the audit record through the existing `update_with_retry`
  protocol.
- Integration tests: at least one full-pipeline test in
  `tmp_path` that constructs orchestrator + gate + journal,
  fires fetch against a synthetic disallow domain with a
  bypass configured, and asserts the audit record lands in
  the journal file.
- Skip-path drift-signal collection: optional — emit a structured
  drift-signal sink (file or in-memory) for future barcada-drift
  consumption.

Estimated 200-300 LOC (worker_loop touches + bypass-config CLI
plumbing + journal-write integration + tests).

**Prerequisites:**
- **All 4 S22-shipped APIs stable** (Phase 0 Step 0.9 verifies).
  HALT if any public API at `robots_gate.py`, `robots_bypass_config.py`,
  or `cost_journal.py` (the S22 additions) diverged from S22 close.
- **Sync/async path decision** — must be pre-resolved at Phase 2
  Q-G.1 before Phase 3 begins. The two paths have very different
  blast radius (path (i) touches `robots.py` + `robots_gate.py`,
  both of which are S21/S22 deliverables locked under Out-of-scope
  unless explicitly authorized; path (ii) keeps S21+S22 deliverables
  untouched and adds the integration entirely in `worker_loop`).
- **Worker_loop integration site verification** — `worker_loop.py`
  is 2884 LOC. Use Explore subagent to locate the actual pre-fetch
  call site(s) BEFORE drafting Q-G.2. Plan §5 wording about
  "link_discovery.py" was already shown wrong at S22; do not
  pattern-apply plan wording to S23 either.
- **Cost-journal write path verification** — `update_with_retry`
  in `cost_journal.py` is the ETag-conditional update helper.
  Q-G.4 must decide whether the bypass-write uses
  `update_with_retry(journal, lambda s: s.with_robots_bypass_appended(entry))`
  (correct shape) or some other helper. Source-verify the
  helper's signature before Q-G.4.
- **Explicit Phase 2 authorization for src/ touches not in Out-
  of-scope's allow-list**: any worker_loop / fetcher_core / robots.py
  / robots_gate.py / cost_journal.py touch beyond what Phase 2
  authorizes HALTs per the S22 "Implicit-authorization HALT for
  src/-locks" LESSONS pattern.

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
Session 23 AND operator has not authorized explicit placeholder
choices.

### Candidate B — Per-tier cost-accounting retrofit (closes Workstream 0)

The deferred-from-S14 per-tier cost-accounting wiring gap.
Currently severity LOW, carry-forward. Closing it would let
`workstream-0-end` tag be placed at the closing commit. Touches
the W4.1.5 driver area (`tests/runners/fixture_cascade/`) which
is locked except via W5.X-prefix commits per S16 precedent.
Estimated 100-200 LOC.

**Prerequisites:**
- Operator authorization at S23 Phase 1 for a W5.X-prefix commit
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

### Candidate H — CRAWLING_POLICY.md tightening pass (NEW small)

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

- **Candidate G** (W A.2 integration): defer (no workstream-end
  milestone closes at W A.2 alone) OR place a candidate-specific
  tag (e.g., `workstream-a-week2-end` if W A.2 is treated as a
  weekly milestone) — Phase 1 should resolve.
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
discipline]]` AND per S22 "Plan-vs-reality at Phase 2 source-verify"
LESSONS pattern BEFORE each AskUserQuestion batch.

**HALT IF** any Phase 2 decision would require modifications to
`src/barcada_scraper/` production code beyond what was Phase-2-
authorized (per S22 "Implicit-authorization HALT for src/-locks"
LESSONS pattern; surface as an explicit AskUserQuestion before
patching) OR to the W4.1.5 driver (except via W5.X-prefix per
Candidate B's auth) OR to any S19/S20/S21/S22 deliverable —
surface as a design-gate sub-question before patching.

### If Candidate G (W A.2 integration)

- **Q-G.1 Sync/async path**: (i) async-wrap `RobotsPolicy.check`
  (touches `robots.py` — S21 lock; requires explicit
  authorization) vs (ii) keep `RobotsPolicy` sync and call
  `RobotsGate.evaluate` from a sync boundary in `worker_loop`
  before entering async (Recommended — preserves S21+S22 locks)
  vs (iii) build a parallel async `RobotsPolicyAsync` class in
  `scraper/robots_async.py` (new file, no S21 lock; but
  increases surface).
- **Q-G.2 Integration site**: the actual pre-fetch site in
  `worker_loop`. Source-verify via Explore before drafting
  option list — DO NOT pattern-apply plan §5 wording.
- **Q-G.3 Bypass-config plumbing**: CLI flag on the orchestrator
  entry (Recommended — explicit per-invocation) vs env var
  (`BARCADA_ROBOTS_BYPASS_CONFIG=/path`) vs config-file entry
  in the existing pipeline config schema.
- **Q-G.4 Cost-journal write path**: wrap
  `journal.with_robots_bypass_appended` with `update_with_retry`
  (Recommended — uses existing ETag-conditional protocol) vs
  direct write (faster, no concurrency safety) vs batched-write-
  on-shard-close (fewer journal writes but loses per-bypass
  immediacy).
- **Q-G.5 Disallow-side action**: skip the URL + drift signal
  (matches S22 GATE_ACTION_SKIP default) vs skip + emit metric
  vs skip + write drift-signal sink to a file/directory for
  barcada-drift consumption.
- **Q-G.6 Crawl-delay enforcement**: forward S22's
  `honor_crawl_delay=False` default (Recommended — no behavior
  change at integration) vs flip to True (spec-compliant; slows
  crawls) vs operator-configurable via CLI flag.
- **Q-G.7 Bypass-config-missing behavior**: hard FileNotFoundError
  if path supplied (matches S22 loader behavior) vs soft fallback
  to empty config with WARNING log vs require explicit "no bypass"
  flag if config-path is unset.
- **Q-G.8 Test corpus shape**: in-process synthetic orchestrator +
  gate + journal in `tmp_path` (Recommended; deterministic; zero
  HTTP) vs cassette-derived integration (uses S20 corpus) vs both.

### If Candidate A (barcada-drift)

Carry-forward from S22 prompt (unchanged).
- Q-A.1 CLI namespace; Q-A.2 drift metric; Q-A.3 alert threshold;
  Q-A.4 input contract; Q-A.5 output shape; Q-A.6 test corpus.

### If Candidate B (per-tier cost-accounting retrofit)

Carry-forward from S22 prompt (unchanged).
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

- **Q-SHARED.1 Commit shape**: per-module (S18+19+20+21+22 default;
  Recommended) vs per-sub-surface bundled.

(Tag-at-close is resolved at Phase 1 Sub-question 1.TAG; Phase 5
reads that resolution directly without re-decision.)

---

## Phase 3 — Implementation (per-module commits, strict order)

Per Phase 2 commit-shape decision. Default = per-module. Each
commit must satisfy the 6-step per-commit checkpoint protocol
below.

### Non-interleaving rule (CRITICAL for bisectability)

If the chosen candidate has multiple sub-surfaces (e.g., Candidate
G has integration-shim + bypass-config-CLI + journal-write + tests
as potentially-separable surfaces), do NOT interleave. Complete
each sub-surface fully before starting the next. Per S22 precedent:
shim (commit 1) → loader (commit 2) → journal field (commit 3) →
docs (commit 4). NOT shim-1 → loader-1 → shim-2 → ….

If a mid-sub-surface dependency on the other sub-surface emerges,
HALT and surface as a design-gate sub-question before continuing —
the dependency may indicate a Phase 2 question was missed.

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
    <new S23 test paths if any> -q
```

If S23 scope touches the cost journal (Q-G.4 likely will),
include the journal-test paths too:

```
    tests/classifier/pipeline/test_cost_journal.py \
    tests/classifier/pipeline/test_cost_journal_local.py \
    tests/classifier/pipeline/test_cost_journal_adls.py
```

Expected: previous_baseline + N new tests, all passing. If failing
tests are NOT a deliberate consequence of the surface-under-test
→ HALT.

**2. Ruff sanity (touched files only) + mid-implementation format
check per LESSONS**

```
.venv/bin/ruff check <touched paths>
.venv/bin/ruff format --check <touched paths>
```

If unclean → run `ruff format <touched paths>` and re-test; fold
the format-fix into the commit (per S19+S20+S21+S22 pattern). This
is the LESSONS "Mid-implementation ruff format-check" discipline
applied to every Edit, not just pre-push.

**3. Verification table (build in chat per `[[double-check-before-
commit]]` strict rule)**

```
| Claim                          | Reality      | Status |
| ------------------------------ | ------------ | ------ |
| <every concrete claim in       | <verified    | ✓ / ✗  |
|  the draft commit message>     |  via source> |        |
```

Any ✗ → fix the claim in the commit message BEFORE staging.

For exit-code claims: use
`cmd > /tmp/out 2> /tmp/err; echo "Exit: $?"` to avoid the
bash-pipe-exit-code-masking pattern (LESSONS).

**4. `git status` check**

Only intended files staged; no surprise `eval_data/` or
unauthorized `src/barcada_scraper/` changes. Operator-side
`eval_data/` README + TAXONOMY_GAP_LOG + stage1_labels
modifications are expected to stay unstaged across sessions
(Sessions 8-22 precedent).

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
Phase 3 start                  : 480  (Session 22 close baseline)
After commit 1                 : >= 480 + N_commit_1_tests
After commit 2                 : >= 480 + N_commit_1_tests + N_commit_2_tests
...
```

**Rule**: the count NEVER decreases between checkpoints. A decrease
means a previously-passing test went red — regression. HALT.

If S23 scope touches the journal (most Candidate G paths will),
use 538 as the baseline instead of 480 (the broader suite).
Whichever baseline is chosen at commit 1, hold it consistent
across all subsequent commits in S23.

---

## Phase 4 — Pre-push gate (whole-tree)

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 347+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

HALT IF any gate red. Never use `--no-verify`.

### eval_data WIP halt protocol (per LESSONS)

validate_consistency runs against working-tree state. Operator-WIP
edits to `eval_data/*.jsonl` can introduce schema violations that
fail the gate even though no S23 commit touches eval_data.

When this fires:
1. Confirm the failing row's content is in operator-WIP
   (`git diff eval_data/...`), not in committed HEAD
   (`git show HEAD:eval_data/...`).
2. Confirm the S23 commits do not touch eval_data
   (`git diff origin/main..HEAD -- eval_data/`).
3. Surface to operator with the exact row + reason + diff vs
   committed state.
4. Two paths: (a) operator-fix in WT, then re-run gate;
   (b) stash eval_data WIP, push, restore.
5. Do NOT auto-fix locked-artifact content.

S20 precedent: operator chose (a). S21 + S22 did not need this
protocol at Phase 4 push, but S22 DID encounter the protocol
post-push during audit (operator chose (a) to fix). Patterns
codified in LESSONS "Pre-push gate against operator-WIP territory".

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

- Append Session 23 entry to `~/crawler-audit/SESSION_LOG.md`
  including a **Canonical S23-close baseline** block with the
  exact pytest invocation + verified test count (per S22 LESSONS
  "Pin the S23 baseline for Phase 0 Step 0.5"; without this, S24
  Phase 0 will infer from the "Combined headline" bullet and
  potentially HALT on accounting-mismatch).
- Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md` for
  Session 24 — explicitly pin the S24 Phase 0 workspace anchor SHA
  per S21+S22 post-audit pattern (LESSONS "Workspace HEAD delta
  tolerance"); do not omit. After the close-out commit lands,
  expect a 1-commit follow-up pinning the actual SHA — this
  follow-up commit's SHA is the canonical S24 anchor.
- Update `~/crawler-audit/LESSONS.md` with any new forward-
  applicable patterns surfaced this session.
- Single workspace commit at session close + 1 follow-up commit
  pinning the anchor SHA. Push workspace after operator confirms.

Note: drafting the next-session prompt (`SESSION_24_PROMPT.md`)
is NOT a built-in Phase 6 step. Per S20→S21, S21→S22, and S22→S23
precedent, prompt-drafting is an operator-commissioned activity
between sessions — not always-on close-out work. If the operator
asks for it explicitly at S23 close, draft it as a separate
follow-up; otherwise leave for the next session to either
operator-commission or scope out at S24 open.

---

## Acceptance criteria

**Per candidate (reduces if Phase 1 narrows scope):**

### Candidate G (W A.2 integration)

1. Sync/async path resolved per Q-G.1; if path (i) or (iii)
   chosen, the affected S21/S22 module is explicitly authorized.
2. `RobotsGate` wired into the worker_loop pre-fetch site per
   Q-G.2.
3. Bypass-config plumbing shipped per Q-G.3.
4. Cost-journal write path uses Q-G.4-chosen helper.
5. Disallow-side action implemented per Q-G.5.
6. Crawl-delay enforcement matches Q-G.6.
7. Bypass-config-missing behavior matches Q-G.7.
8. Test corpus per Q-G.8; at least one full-pipeline integration
   test in `tmp_path` asserting the audit record lands in the
   journal file.
9. Tag per 1.TAG (defer OR candidate-specific).

### Candidate A (barcada-drift)

Carry-forward from S22 prompt (unchanged):
1. `barcada-drift` (or `barcada-baseline drift`) CLI works against
   ≥2 canary_runs parquets.
2. Drift metric per Q-A.2 implemented + tested.
3. Alert threshold per Q-A.3 implemented + tested.
4. Output shape per Q-A.5 documented + tested.

### Candidate B (per-tier cost-accounting retrofit)

Carry-forward from S22 prompt (unchanged):
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

### Shared (all candidates)

5. Combined suite at session close: existing 480 baseline + N new
   tests, all passing. (Or 538 baseline if scope touches journal.)
6. Pre-push gate runs green (incl. eval_data WIP halt protocol
   applied if needed).
7. Tag placed per Phase 1 Sub-question 1.TAG OR explicit defer.
8. Regression-protection checklist held (see "Out-of-scope" below).
   In particular: ALL S21+S22 deliverables stay at the SHAs they
   landed at; their public APIs are unchanged. The 32 robots-parser
   tests stay 32/32 green; the 30 robots_gate tests stay 30/30
   green; the 30 robots_bypass_config tests stay 30/30 green; the
   58 cost_journal tests stay 58/58 green (or 59+ if S23 adds
   tests).

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
  public API at `34a59b6`). Candidate G CONSUMES this module's
  public API but MUST NOT MODIFY it unless Q-G.1 chooses path (i)
  AND operator explicitly authorizes the module touch via a
  follow-up AskUserQuestion. Default Q-G.1 path (ii) preserves
  this lock.
- `tests/scraper/test_robots.py` (32 tests; pins stdlib quirks).

**S22 deliverables (Session 22 W A.1 W8 integration sub-surfaces):**
- `src/barcada_scraper/scraper/robots_gate.py` (shim; 339 LOC;
  public API at `ba87e7e`). Candidate G CONSUMES the public API
  (`RobotsGate.evaluate`, `GateDecision`, `BypassEntry`,
  `BypassAuthorization`, `GATE_ACTION_*`, `ALL_GATE_ACTIONS`,
  `DRIFT_SIGNAL_PREFIX`) but MUST NOT MODIFY it. Any modification
  invalidates the W A.2 integration design and surfaces as a
  HALT at Phase 0 Step 0.9 (parser+gate+loader API surface
  stability check).
- `tests/scraper/test_robots_gate.py` (30 tests).
- `src/barcada_scraper/scraper/robots_bypass_config.py` (loader;
  178 LOC; public API at `381ee89`). Candidate G CONSUMES
  `load_bypass_config(path)` / `loads_bypass_config(payload)` /
  `BypassConfigError` but MUST NOT MODIFY them. Constants
  `REQUIRED_FIELDS` / `OPTIONAL_FIELDS` / `ALLOWED_FIELDS`
  similarly locked.
- `tests/scraper/test_robots_bypass_config.py` (30 tests).
- The S22 ADDITIONS to `src/barcada_scraper/classifier/pipeline/
  cost_journal.py` (`BypassAuditEntry` dataclass at L150-172;
  `JournalState.robots_bypass_log` field at L196; `with_robots_
  bypass_appended` method; `to_dict` / `from_dict` /
  `_replace` updates; `__all__` extension) are LOCKED at the
  shape that landed at `1d9404e`. Candidate G CONSUMES
  `with_robots_bypass_appended` but MUST NOT MODIFY the
  dataclass shape or the method signature. The pre-S22 portions
  of `cost_journal.py` (CostTotals, ShardRecord, CeilingHistoryEntry,
  the existing builders, retry helper, factory) remain locked as
  before. ADDING new fields/methods is allowed if Phase 2 design-
  gate explicitly authorizes (per S22 "Implicit-authorization
  HALT for src/-locks" LESSONS — surface explicit authorization
  before commit).
- The S22 ADDITIONS to `tests/classifier/pipeline/test_cost_journal.py`
  (14 new tests + 1 updated `test_to_dict_emits_canonical_keys`)
  are locked. Adding new tests is allowed; modifying the S22
  tests requires explicit authorization.
- `docs/CRAWLING_POLICY.md` (202 lines / 8.1 KB; at `fdc8a7a`).
  Candidate H is the ONLY candidate that may modify this file.
  Other candidates MUST NOT.

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
- All workstream tags at their placed SHAs (10 tags as of S22
  close; new tags only via Phase 5 explicit placement)
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` (READ-ONLY)
- `CLASSIFICATION_ADJACENT_PLAN.md` (UPDATED only when AI/ML
  decisions land)
- `RECONCILIATION_2026-05-21.md`
- `docs/phase4_implementation_plan.md` (Phase 4 governance
  reference)

**Operator-owned territory:**
- All of `eval_data/` — labeling-workstream territory; per-row WIP
  edits across sessions are expected and unstaged

**Production code:**
- `src/barcada_scraper/` — locked unless Phase 2 design-gate
  explicitly authorizes a specific module. S21 authorized
  `scraper/robots.py`; S22 authorized `scraper/robots_gate.py`,
  `scraper/robots_bypass_config.py`, AND (via mid-Phase-3 explicit
  operator authorization) the additive surface in
  `classifier/pipeline/cost_journal.py`. Those authorizations
  do NOT extend to other src/ modules or to further modifications
  of the authorized files beyond their landed S21/S22 shapes.
  Candidate G's worker_loop / fetcher_core touches MUST be
  explicitly authorized at Phase 2 per the S22 "Implicit-
  authorization HALT for src/-locks" LESSONS pattern.

**Pipeline configs:**
- `configs/`

**Phase 4 work:**
- Phase 4 PR-D/E/F/G work opens only when Workstream 0 fully
  closes AND operator-led Stage 2/3 labeling work begins

---

## Verify-before-asking discipline (strict rule from S19+S20+S21+S22)

Per `[[double-check-before-commit]]` memory: **ALWAYS verify every
concrete claim in the commit message against actual source/output
BEFORE staging.** Fixture names, file counts, exit codes, line
counts, test counts, helper names, smoke outcomes, SHA prefixes,
regex matches, API signatures. No claims by pattern-completion.
Build a verification table in chat (claim → reality → status) and
reconcile before "Confirm to commit?".

Specific to S23:

- Before each chosen-candidate-specific claim in a commit message,
  verify against the actual source / runtime output:
  - Candidate G: worker_loop integration site exists at the
    claimed line range; `RobotsGate` import succeeds at the
    new call site; cost-journal write actually persists by
    re-reading the journal file in a test.
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

LESSONS-folded discoveries from S21+S22 worth re-applying if S23
takes Candidate G:

- Plan-vs-reality at Phase 2 (S22 LESSONS): plan §5 wording said
  "integrate into `link_discovery.py`" but that module is pure-
  function. Plan §5 may also say "wire into worker_loop" without
  specifying which worker_loop function; source-verify the actual
  pre-fetch call site via Explore BEFORE drafting Q-G.2 options.
- Implicit-authorization HALT (S22 LESSONS): Q-G.* answers will
  likely require touching `worker_loop.py` and/or `fetcher_core.py`
  which are NOT in S23 Out-of-scope's authorized-touch list.
  Surface explicit authorization in Phase 2 BEFORE the commit,
  not as a HALT mid-Phase-3.
- Parallel-dataclass pattern (S22 LESSONS): the S22 separation
  between `BypassAuthorization` and `BypassAuditEntry` is the
  pattern to follow if S23 needs cross-package records.
- Per-module commit scaling (S22 LESSONS): S22 landed 4 commits
  cleanly; if S23 has 3-5 sub-surfaces, do not bundle.
- Phase-2 estimate-vs-actual disclosure (S22 LESSONS): if Q-G's
  options cite LOC estimates and actual diverges >2x, disclose
  in commit body with reason.
- stdlib `RobotFileParser` quirks (S21 LESSONS): if S23 integration
  reads `decision.crawl_delay`, the value already has S21's UA-
  specific-wins-over-wildcard logic applied. Don't second-guess it.
- stdlib `applies_to()` substring match (S21 LESSONS): `BarcadaCrawler/
  1.0` matches a robots `User-agent: BarcadaCrawler` rule. Pin in
  integration tests if relevant.

---

## Commit hygiene (per LESSONS + S19/S20/S21/S22 additions)

- File-based commit messages at `/tmp/<id>-msg.txt`.
- Per-module commits (Phase 3 commit shape unless Q-SHARED.1
  overrides).
- "Confirm to commit?" before EVERY commit. Pair with verification
  table (always) and `git diff --staged` (when appropriate per
  `[[double-check-before-commit]]` triggers).
- Commit body includes: action ref (e.g., `WA2.W8.integration` for
  Candidate G), scope summary, file touches, test count delta,
  plan reference. NO `Co-Authored-By`.
- Pre-push gate must run green. Never use `--no-verify`.
- Pre-push vermin: `git ls-files '*.py' | xargs vermin
  --target=3.10` to filter venv-internal pytest 3.14 false-
  positives.
- Mid-implementation ruff format-check, not only pre-push.
- Sibling-module style consistency for one-file additions — match
  the immediate sibling's conventions even where they technically
  violate project-wide rules; **disclose explicitly in the commit
  body** (S21+S22 LESSONS finding).
- For S22 surface modifications: if Phase 2 explicitly authorizes
  modifying the S22-landed shape of `cost_journal.py` additions
  (e.g., adding a new field to `BypassAuditEntry`), the commit
  body MUST explicitly disclose the modification with reason
  (S22 LESSONS "Implicit-authorization HALT" pattern).
- Workspace close-out (Phase 6) lands as its own commit at session
  close, followed by 1 follow-up commit pinning the anchor SHA
  for the next session (S21+S22 pattern).

---

## Context-window awareness

S22 ran across 4 commits + Phase 2 source-verification + 1
mid-Phase-3 HALT, well within context. S23 budget per scope:

- Candidate G: large (200-300 LOC + integration tests +
  worker_loop touches; worker_loop is 2884 LOC requiring Explore
  delegation for the integration-site audit). Likely needs
  3-5 per-module commits.
- Candidate A: medium-large (~300 LOC).
- Candidate B: small-medium (100-200 LOC; sensitive driver-area
  touch).
- Candidate D/E: small.
- Candidate H: very small (<50 LOC of doc edits; <30 minutes).

Strategies:
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore subagent
  per S21+S22 "Explore-subagent + spot-check" LESSONS pattern.
- For any live-HTTP corpus work (Candidate E), pilot with 1-3
  cassettes first per S18+S20 staged-rollout pattern.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before the chosen S23 scope closes,
  transition per "no mid-commit-batch transitions" — finish in-
  flight sub-surface, then close session and refill the transition
  template for Session 24.

---

## Reporting in chat at session close

After all Session 23 commits land + push + close-out per the
S13-22 pattern:

1. Commit SHA(s) of each S23 sub-surface.
2. Sub-surface(s) landed (per candidate).
3. Test count delta: 480 (or 538) baseline → S23 close.
4. Driver suite count at S23 close (46/46 expected unless
   Candidate B W5.X-prefix realigned).
5. Files touched per sub-surface.
6. Tag dispositions (incl. any new tag per 1.TAG).
7. Per-tier cost-accounting wiring gap disposition: patched
   (Candidate B) or carry-forward.
8. W A.2 integration disposition: shipped (Candidate G) or
   carry-forward.
9. Any spend (LLM, infrastructure, cassette-capture).
10. Robots.txt compliance log (if Candidate G did live work or
    Candidate E expanded the cassette corpus).
11. FP-curation log update (if Candidate E expanded the cassette
    corpus).
12. Verify-before-asking summary: any source-verification findings
    surfaced.
13. Outstanding items for Session 24.
14. Tags state at S23 close.

Do not propose Phase 4 PR-D/E/F/G work this session unless
Candidate D was chosen and operator-led labeling is in flight.

---

## Carry-forward bakes (no amendment file needed)

All S22 amendments (3 close-out commits: `dbba7bd` / `acf86c5` /
`8e6a7de`) plus the S22 post-close audit corrections have been
folded directly into this prompt — S23 does not need a separate
amendment file:

- **S22 close-out corrections** folded into Step 0.1 (workspace
  anchor `8e6a7de`), Step 0.5 (Canonical S22-close baseline 480
  pinned), Step 0.9 (S22-shipped public API stability check
  expanded to cover all 4 modules).
- **5 LESSONS sections from S22 close** referenced where they
  apply: Plan-vs-reality at Phase 2 (Phase 2 source-verify);
  Implicit-authorization HALT for src/-locks (Phase 2 HALT
  condition + Phase 3 commit-body discipline); Parallel-
  dataclass pattern (cross-package design); Per-module commit
  scaling (Phase 3 commit shape); Phase-2 estimate-vs-actual
  disclosure (commit hygiene).

If new amendments arise pre-S23 open, walk them per the reviewer-
feedback hygiene pattern in this prompt's "Reviewer-feedback
hygiene" section.
