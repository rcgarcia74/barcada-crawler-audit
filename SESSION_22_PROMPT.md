# Session 22 prompt — scope picked at Phase 1
# (W A.1 W8 robots parser shipped S21 in Parser-only scope;
#  W A.1 full close via Candidate F integration open as S22 scope,
#  alongside A/B/D/E carry-forwards from S20→S21)

**Drafted at Session 21 close (2026-05-23).** Bakes in the post-S21
follow-up corrections: workspace Phase 0 anchor pinned to a specific
SHA; Candidate F prereqs include parser-API-stability HALT-condition
and Q-C.4 deferred-from-S21 carry-forward framing. Invoke from
`~/Downloads/session-22-prompt.md` (mirror of this file).

This prompt is scope-agnostic at Phases 0/1 and elicits scope-specific
design gates at Phase 2. Operator picks at Phase 1 from five pre-
resolved candidates. Strict 7-phase ordering with halt-on-mismatch is
preserved from the S20/S21 prompts.

---

## Scope

Engineering session. Workstream sub-surfaces remaining after Session
21 closed `WA1.W8.robots-parser` (Parser-only):

- **W A.1 parser-only shipped** — `src/barcada_scraper/scraper/
  robots.py` at S21 commit `34a59b6`. `RobotsPolicy.check(url) ->
  RobotsDecision(allowed, reason, crawl_delay)`. 32 tests. NOT YET
  integrated with `link_discovery.py`; bypass/cost-journal coupling
  deferred (Q-C.4 carry-forward).
- **W A.1 integration (NEW Candidate F)** — wires `RobotsPolicy`
  into the fetcher seam + ships `CRAWLING_POLICY.md` + cost-journal
  bypass marker. Closes W A.1 fully → `workstream-a-week1-end` tag.
- **Per-tier cost-accounting wiring gap (Candidate B)** — carry-
  forward from S14; severity LOW; closing it would justify
  `workstream-0-end` tag.
- **barcada-drift (Candidate A)** — deferred per Q1.1=(A) at S20;
  still needs 4 AI/ML decisions per CLASSIFICATION_ADJACENT_PLAN.md
  §Item 8 AND 2+ canary_runs parquets to exist (launchd installer
  must have fired ≥2 Saturdays).
- **Phase 4 PR-D tooling (Candidate D)** — operator-led labeling
  territory.
- **Cassette corpus expansion (Candidate E)** — current 20 is lower
  bound of plan's "~20-30".

Operator chooses at Phase 1 which candidate Session 22 ships. Each
candidate has its own Phase 2 design-gate template.

**Sessions 13-21 precedent:** this session does NOT modify the
W4.1.5 driver orchestration at `tests/runners/fixture_cascade/`
(locked at `dd64963`). Does NOT modify `expected.schema.json` v1.1
/ `META_SCHEMA.md` v1.1. Does NOT modify the committed
`tests/fixtures/baseline-v0/` snapshot at `9e9a1fb`. Does NOT
modify the Session 19 `check` sub-surface code or the Session 20
cassettes/canary sub-surface code or the Session 21 `robots.py`
parser at `src/barcada_scraper/scraper/robots.py` (`34a59b6`) and
its `tests/scraper/test_robots.py`. Does NOT modify production code
under `src/barcada_scraper/` UNLESS Phase 2 design-gate explicitly
authorizes a specific module.

Full regression-protection checklist in **Out-of-scope** at the end
of this prompt. Re-read it before any code lands.

---

## Reviewer-feedback hygiene (if this prompt is reviewed)

If an external reviewer (operator-invoked) flags items in this
prompt before Session 22 starts, walk each flagged item against
on-disk reality at HEAD `34a59b6` BEFORE applying any change. Per
S19/S20/S21 pattern (LESSONS "Reviewer-feedback hygiene"):

- **OBSOLETE** items: SHAs already verified, claims already true.
  Skip with documented reasoning.
- **VALID-applies-now** items: bear on this session's scope. Apply.
- **VALID-applies-later** items: bear on deferred scope. Carry
  forward to the next prompt revision.
- **WRONG-PREMISE** items: assumes something not true. Skip with
  documented reasoning.

Empirical baseline: at S19 review 3 of 5 "must-fix" items collapsed
under cold-start verification; at S20 review 1 of 12 amendments
was skipped because it would HALT spuriously (SR-4); at S21 post-
close audit 2 of 3 operator-feedback items required workspace-doc
corrections (S22 Phase 0 anchor pin + Candidate F missing prereqs).
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
decisions for A; W5.X-prefix auth for B; Q-C.4-deferred-carry-
forward not pre-resolved for F). Phase 2 halts catch hidden scope
expansion. Phase 3 halts catch regressions. Phase 4 halts catch
pre-push gate failures (incl. operator-WIP-in-locked-tree).

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

Run in order. Halt and surface to operator on any mismatch.

### Step 0.1 — Workspace + repo HEAD

```
# Workspace at Session 22 start (Session 21 close-out + S21 follow-
# up correction commits, all pushed):
git -C ~/crawler-audit rev-parse HEAD
# Expect: 332f390 (S21 close-out follow-up: pin S22 Phase 0 anchor
# + Candidate F missing prereqs) OR a later commit if additional
# workspace doc edits landed post-S21-close. If N commits ahead,
# verify each prior commit's subject via
# `git log --oneline 332f390..HEAD` against expected prompt-
# finalization / doc-edit patterns; surface the SHA delta and
# request authorization to proceed if anything is unexpected.
# (S20/S21 precedent: operator authorized continuation when 2-3
# extra workspace commits were the strengthened prompts themselves.)

# Repo at Session 21 final commit:
git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: 34a59b6 (WA1.W8.robots-parser)
```

### Step 0.2 — Tags (no change from S21 close)

```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort
# Expect 9 tags (unchanged from S21 close):
#   baseline-v0
#   pre-remediation-2026-05-19
#   workstream-0-week1-end
#   workstream-0-week2-end
#   workstream-0-week3-end
#   workstream-0-week4-1-5-end
#   workstream-0-week4-end
#   workstream-0-week5-end
#   workstream-0-week7-end
# No new tag at S21 close (Parser-only deferred 1.TAG).
```

### Step 0.3 — Driver locked

```
cd /Users/administrator/projects/barcada-scraper
git diff dd64963..HEAD -- tests/runners/fixture_cascade/ \
    ':(exclude)tests/runners/fixture_cascade/test_fixture_fetcher.py'
# Expect: empty (only test_fixture_fetcher.py changed via W5.X
# realign at 8d0fc0e in Session 16).
```

### Step 0.4 — Fixture counts (no change from S21 close)

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
    tests/synthetic_crawl/ tests/scraper/test_robots.py -q
# Expect: 420 passed / 0 failed / 0 skipped
#         (= 210 conformance + 46 driver + 99 baseline_v0
#          + 33 synthetic_crawl + 32 robots = 420)
```

The sub-paths add up to the headline: 210 + 46 + 99 + 33 + 32 = 420.
Any drift = halt.

If the headline mismatches, re-run each sub-path independently to
localize which sub-suite drifted:

```
.venv/bin/python -m pytest tests/scraper/test_fixture_conformance.py -q   # expect 210
.venv/bin/python -m pytest tests/runners/fixture_cascade/ -q              # expect  46
.venv/bin/python -m pytest tests/baseline_v0/ -q                          # expect  99
.venv/bin/python -m pytest tests/synthetic_crawl/ -q                      # expect  33
.venv/bin/python -m pytest tests/scraper/test_robots.py -q                # expect  32
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

### Step 0.8 — Regression-protection sanity (Candidate F prereq)

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
```

### Step 0.9 — Parser API surface stability (Candidate F prereq)

```
# If Candidate F is even possibly in scope, verify the parser
# PUBLIC integration contract matches the S21-shipped surface
# BEFORE Phase 2 design-gate elicitation. A change to the
# integration surface between S21 close and S22 open would
# invalidate the Candidate F design.
#
# Scope: only what integration callers depend on per the Scope
# section above:
#   RobotsPolicy(user_agent=...).check(url) -> RobotsDecision(
#     allowed, reason, crawl_delay)
# Internals (DEFAULT_ROBOTS_TIMEOUT default value, RobotsFetchResult
# field shape, RobotsFetcher type alias, timeout/fetcher optional
# kwargs) are INTENTIONALLY NOT checked — those can legitimately
# change in a v1.1 patch (e.g., bumping the default timeout) without
# invalidating Candidate F. Over-asserting here risks spurious
# HALTs of the SR-4 shape (gate fails for a reason unrelated to
# the design contract).
.venv/bin/python -c "
from barcada_scraper.scraper.robots import RobotsDecision, RobotsPolicy
import inspect
# RobotsDecision public field set (caller reads .allowed, .reason, .crawl_delay)
assert {f.name for f in RobotsDecision.__dataclass_fields__.values()} == \
    {'allowed', 'reason', 'crawl_delay'}, 'RobotsDecision fields drifted'
# RobotsPolicy.check exposes a callable with a url positional arg
check_params = set(inspect.signature(RobotsPolicy.check).parameters)
assert {'self', 'url'} <= check_params, \
    f'RobotsPolicy.check signature drifted: {check_params}'
# RobotsPolicy can be constructed with user_agent (integration callers MUST)
init_params = set(inspect.signature(RobotsPolicy.__init__).parameters)
assert 'user_agent' in init_params, \
    f'RobotsPolicy.__init__ missing user_agent: {init_params}'
print('OK parser public integration contract unchanged from S21 @ 34a59b6')
"
```

If any of 0.1-0.9 fail, HALT before doing any work.

---

## Required workspace reading (Session 22 first 10 minutes)

In this order:

1. **`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`** — full
   handoff state at S21 close. Lists 5 scope candidates (F-new +
   A-B-D-E carry-forward) with prerequisites + estimated scope.
   The S22 scope choice at Phase 1 picks from these.

2. **`~/crawler-audit/SESSION_LOG.md`** Session 21 entry — what
   landed during W A.1 W8 robots-parser (1 commit). The 2 mid-
   implementation stdlib-quirk test failures + resolutions. The
   5 forward-applicable patterns at the end.

3. **`~/crawler-audit/LESSONS.md`** — 5 new sections folded at S21
   close, at end of file. Locate via
   `grep -n '^## .*(S21 folding)\|^## .*(S21 follow-up)' LESSONS.md`
   (line numbers shift with any pre-pend; rely on the grep, not a
   pinned line ref). Especially:
   - "Library-quirk patterns" / "Test-driven discovery of stdlib
     quirks" — directly applicable if Candidate F integrates
     `RobotsPolicy` (same parser; same quirks).
   - "Workspace HEAD delta tolerance" — already encoded in Step
     0.1 above.
   - "Single-module Phase 3 commit collapse".
   - "Explore-subagent + spot-check for Phase 2 source-verify".
   - "Sibling-module style disclosure".

4. **`~/crawler-audit/BARCADA_CRAWLER_REMEDIATION_PLAN.md`** —
   chosen-scope section per Phase 1 candidate choice. Plan is
   READ-ONLY.

5. **`~/crawler-audit/CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8
   — only if Candidate A (barcada-drift) is chosen.

6. **`~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md`** —
   only if Candidate B (per-tier cost-accounting retrofit) is
   chosen. READ-ONLY.

7. **`src/barcada_scraper/scraper/robots.py`** at `34a59b6` — only
   if Candidate F is chosen. The public API (`RobotsPolicy.check`,
   `RobotsDecision`) is what callers integrate against. Read top-
   to-bottom; ~280 LOC.

8. **`tests/scraper/test_robots.py`** at `34a59b6` — only if
   Candidate F is chosen. Documents stdlib quirks via pinned
   tests; use as integration-test scaffold reference.

9. **Repo source pertinent to Phase 2 design-gate** — varies by
   chosen candidate; spelled out in each Phase 2 sub-section below.

---

## Phase 1 — Scope resolution (no code; pre-design-gate)

Operator picks one candidate. Candidates roughly ordered by
prerequisite-readiness; each is independent.

### Candidate F — W A.1 integration (closes Workstream A Week 1) (NEW; Recommended)

The natural follow-on to S21's Parser-only ship. Closes acceptance
criterion 4 from the S21 Candidate C set and warrants the
`workstream-a-week1-end` tag at the closing commit.

Scope (per W8 plan §5 Action #2 bullets 4-5 + plan bullet 5
documentation):
- Integrate `barcada_scraper.scraper.robots.RobotsPolicy` into
  `link_discovery.py` (or equivalent fetcher seam — verify at
  Phase 0) — gate URLs before they enter the crawl queue.
- Cost-journal authorization-marker: when a per-domain bypass is
  configured, log the explicit authorization to the cost journal
  so audit trails capture "this fetch ignored robots.txt because
  …" (plan bullet 4).
- `CRAWLING_POLICY.md` documentation (plan bullet 5).
- Integration tests (fixtures or cassettes) + bypass-marker tests
  against cost-journal asserter.

Estimated 150-250 LOC (parser already exists; this is wiring +
docs + tests).

**Prerequisites:**
- **Parser API surface stability** (Phase 0 Step 0.9 verifies).
  HALT if the public API at `src/barcada_scraper/scraper/robots.py`
  diverged from S21 ship (the integration design depends on the
  exact signatures).
- **Q-C.4 deferred-from-S21 framing**: S21 chose pure check API
  + deferred bypass/cost-journal coupling. Phase 2 here MUST
  resume that as a *known carry-forward*, not open it as a
  fresh question. The Phase 2 Q-F.* questions below pre-encode
  this framing.
- Decision on where the integration plugs in (existing fetcher
  seam location — `link_discovery.py` per plan, OR a shim if
  that module sits in less-touchable territory).
- Decision on bypass-config mechanism (env var / config file /
  CLI flag / per-domain JSON).
- `CRAWLING_POLICY.md` scope (full vs minimal-first).

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
Session 22 AND operator has not authorized explicit placeholder
choices. Per SR-8 (baked into S21 prompt, carried forward): only
this candidate blocks on AI/ML team availability.

### Candidate B — Per-tier cost-accounting retrofit (closes Workstream 0)

The deferred-from-S14 per-tier cost-accounting wiring gap.
Currently severity LOW, carry-forward. Closing it would let
`workstream-0-end` tag be placed at the closing commit. Touches
the W4.1.5 driver area (`tests/runners/fixture_cascade/`) which
is locked except via W5.X-prefix commits per S16 precedent.
Estimated 100-200 LOC.

**Prerequisites:**
- Operator authorization at S22 Phase 1 for a W5.X-prefix commit
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

### Sub-question 1.TAG — Tag at session close (pinned at Phase 1)

Independent of scope choice; resolved fully here at Phase 1 so
Phase 5 has an unambiguous tag decision. Options per scope:

- **Candidate F** (W A.1 integration): if integration ships + docs
  land + tests pass, place `workstream-a-week1-end` at the closing
  commit. Otherwise defer.
- **Candidate A** (barcada-drift): defer OR place candidate-
  specific (e.g., `barcada-drift-v0`).
- **Candidate B** (per-tier cost-accounting): if it fully closes
  Workstream 0, place `workstream-0-end`. Otherwise defer.
- **Candidate D** (Phase 4 PR-D tooling): defer.
- **Candidate E** (cassette corpus expansion): defer.

Phase 5 reads this resolution directly — no Phase 2 re-decision.

---

## Phase 2 — Design-gate elicitation (no code; AskUserQuestion)

Per chosen Phase 1 candidate. Each candidate has its own sub-block.
Source-verify at session-current HEAD per `[[verify-before-asking-
discipline]]` before each AskUserQuestion batch.

**HALT IF** any Phase 2 decision would require modifications to
`src/barcada_scraper/` production code beyond what was Phase-2-
authorized (i.e., for Candidate F: integration into `link_
discovery.py` OR a new shim; NOT modifications to the S21-shipped
`robots.py`) OR to the W4.1.5 driver (except via W5.X-prefix per
Candidate B's auth) OR to any S19/S20/S21 deliverable — surface as
a design-gate sub-question before patching.

### If Candidate F (W A.1 integration)

- **Q-F.1 Integration site**: integrate into `link_discovery.py`
  per plan (verify the module exists + its function shape at
  Phase 0) vs a new shim module `src/barcada_scraper/scraper/
  robots_gate.py` that wraps `RobotsPolicy` for the fetcher seam
  vs both.
- **Q-F.2 Bypass-config mechanism**: per-domain JSON sidecar
  (auditable; requires new file format; **Recommended** — plan
  §4 W8 Action #2 bullet 4 reads "an explicit per-domain
  configurable", which favors structured per-domain shapes) vs
  config file entry (structured; requires config-schema edits;
  also satisfies "per-domain" if keyed on domain) vs env var
  (cheap, but does NOT support per-domain scoping cleanly) vs
  CLI flag (per-invocation, no persistence; also does NOT
  support per-domain scoping cleanly).
- **Q-F.3 Cost-journal coupling** (Q-C.4 deferred-from-S21):
  where does the bypass authorization-marker land in the cost
  journal? Options: new field on `stage3_decision` /
  `evidence_cost_usd` siblings OR new journal-level field OR
  per-row diagnostic in an existing free-text field.
- **Q-F.4 Disallow handling at integration**: skip URL silently
  (matches `RobotsPolicy.check.allowed==False`) vs log + skip vs
  log + skip + emit drift signal for future barcada-drift.
- **Q-F.5 Crawl-delay honoring**: actually sleep on
  `decision.crawl_delay` (correct, but slows crawls) vs record
  the value but don't sleep (faster, but spec-incompliant) vs
  operator-configurable.
- **Q-F.6 CRAWLING_POLICY.md scope**: full doc per W8 plan
  bullet 5 (robots compliance + rate limits + AUP + ID policy
  + CAPTCHA + retention; ~5-10 KB) vs minimal-first (robots
  compliance only; ~1-2 KB; defer other sections).
- **Q-F.7 Test corpus shape**: synthetic robots.txt + injectable
  fetcher (matches S21 `test_robots.py` pattern) vs cassette-
  derived integration (uses S20 corpus) vs both.

### If Candidate A (barcada-drift)

Carry-forward from S21 prompt (unchanged).
- Q-A.1 CLI namespace; Q-A.2 drift metric; Q-A.3 alert threshold;
  Q-A.4 input contract; Q-A.5 output shape; Q-A.6 test corpus.

### If Candidate B (per-tier cost-accounting retrofit)

Carry-forward from S21 prompt (unchanged).
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

### Shared sub-questions (all candidates)

- **Q-SHARED.1 Commit shape**: per-module (S18+19+20+21 default;
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
F has integration + docs + tests as potentially-separable
surfaces), do NOT interleave. Complete each sub-surface fully
before starting the next. Per S20 precedent: cassettes (4 commits)
→ canary (4 commits). NOT cassette-1 → canary-1 → cassette-2 → ….

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
    <new S22 test paths if any> -q
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
the format-fix into the commit (per S19+S20+S21 pattern). This is
the LESSONS "Mid-implementation ruff format-check" discipline
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
(Sessions 8-21 precedent).

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
Phase 3 start                  : 420  (Session 21 close baseline)
After commit 1                 : >= 420 + N_commit_1_tests
After commit 2                 : >= 420 + N_commit_1_tests + N_commit_2_tests
...
```

**Rule**: the count NEVER decreases between checkpoints. A decrease
means a previously-passing test went red — regression. HALT.

---

## Phase 4 — Pre-push gate (whole-tree)

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 343+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

HALT IF any gate red. Never use `--no-verify`.

### eval_data WIP halt protocol (per LESSONS)

validate_consistency runs against working-tree state. Operator-WIP
edits to `eval_data/*.jsonl` can introduce schema violations that
fail the gate even though no S22 commit touches eval_data.

When this fires:
1. Confirm the failing row's content is in operator-WIP
   (`git diff eval_data/...`), not in committed HEAD
   (`git show HEAD:eval_data/...`).
2. Confirm the S22 commits do not touch eval_data
   (`git diff origin/main..HEAD -- eval_data/`).
3. Surface to operator with the exact row + reason + diff vs
   committed state.
4. Two paths: (a) operator-fix in WT, then re-run gate;
   (b) stash eval_data WIP, push, restore.
5. Do NOT auto-fix locked-artifact content.

S20 precedent: operator chose (a). S21 did not need this protocol.
Patterns codified in LESSONS "Pre-push gate against operator-WIP
territory".

---

## Phase 5 — Push + tag

- Push to `origin/main` after operator confirms.
- Tag per Phase 1 Sub-question 1.TAG decision (or defer).

If `workstream-a-week1-end` is placed (Candidate F closes W A.1):
include annotated message summarizing the W A.1 work — S21 parser
ship + S22 integration + docs + cost-journal bypass marker.

If `workstream-0-end` is placed (Candidate B closes Workstream 0):
include annotated message summarizing all W0 weeks (W1-W4, W4.1.5,
W4.3, W5, W6, W7 + the per-tier cost-accounting closure).

---

## Phase 6 — Workspace close-out

- Append Session 22 entry to `~/crawler-audit/SESSION_LOG.md`
  (Sessions 13-21 precedent format).
- Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md` for
  Session 23 — explicitly pin the S23 Phase 0 workspace anchor SHA
  per S21 post-audit pattern (LESSONS "Workspace HEAD delta
  tolerance"); do not omit.
- Update `~/crawler-audit/LESSONS.md` with any new forward-
  applicable patterns surfaced this session.
- Single workspace commit at session close. Push workspace after
  operator confirms.

Note: drafting the next-session prompt (`SESSION_23_PROMPT.md`)
is NOT a built-in Phase 6 step. Per S20→S21 and S21→S22
precedent, prompt-drafting is an operator-commissioned activity
between sessions — not always-on close-out work. If the operator
asks for it explicitly at S22 close, draft it as a separate
follow-up; otherwise leave for the next session to either
operator-commission or scope out at S23 open.

---

## Acceptance criteria

**Per candidate (reduces if Phase 1 narrows scope):**

### Candidate F (W A.1 integration)

1. `RobotsPolicy` integrated into the chosen fetcher seam per
   Q-F.1.
2. Bypass-config mechanism shipped per Q-F.2.
3. Cost-journal authorization-marker landed per Q-F.3 (resumes
   Q-C.4 deferred-from-S21 carry-forward).
4. Disallow handling per Q-F.4.
5. Crawl-delay honoring per Q-F.5.
6. `CRAWLING_POLICY.md` per Q-F.6 scope.
7. Test corpus per Q-F.7.
8. `workstream-a-week1-end` tag placed if items 1-6 ship cleanly.

### Candidate A (barcada-drift)

Carry-forward from S21 prompt (unchanged):
1. `barcada-drift` (or `barcada-baseline drift`) CLI works against
   ≥2 canary_runs parquets.
2. Drift metric per Q-A.2 implemented + tested.
3. Alert threshold per Q-A.3 implemented + tested.
4. Output shape per Q-A.5 documented + tested.

### Candidate B (per-tier cost-accounting retrofit)

Carry-forward from S21 prompt (unchanged):
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

### Shared (all candidates)

5. Combined suite at session close: existing 420 baseline + N new
   tests, all passing.
6. Pre-push gate runs green (incl. eval_data WIP halt protocol
   applied if needed).
7. Tag placed per Phase 1 Sub-question 1.TAG OR explicit defer.
8. Regression-protection checklist held (see "Out-of-scope" below).
   In particular: 32 robots-parser tests stay 32/32 green; the
   parser module's public API at `src/barcada_scraper/scraper/
   robots.py` is unchanged (Candidate F integrates with it but
   does not modify it).

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
  public API at `34a59b6`). Candidate F INTEGRATES with this
  module's public API but MUST NOT MODIFY it. A v1.1 parser change
  is a separate sub-surface that would invalidate the Candidate F
  integration design — surface at Phase 0 Step 0.9.
- `tests/scraper/test_robots.py` (32 tests; pins stdlib quirks).

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
- All workstream tags at their placed SHAs
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
  `scraper/robots.py`; that authorization does NOT extend to other
  src/ modules. S22 Candidate F may authorize a new shim module
  (e.g., `scraper/robots_gate.py`) AND/OR a touch to
  `link_discovery.py` (verify the file exists at Phase 0); any
  other src/ touch HALTs.

**Pipeline configs:**
- `configs/`

**Phase 4 work:**
- Phase 4 PR-D/E/F/G work opens only when Workstream 0 fully
  closes AND operator-led Stage 2/3 labeling work begins

---

## Verify-before-asking discipline (strict rule from S19+S20+S21)

Per `[[double-check-before-commit]]` memory: **ALWAYS verify every
concrete claim in the commit message against actual source/output
BEFORE staging.** Fixture names, file counts, exit codes, line
counts, test counts, helper names, smoke outcomes, SHA prefixes,
regex matches, API signatures. No claims by pattern-completion.
Build a verification table in chat (claim → reality → status) and
reconcile before "Confirm to commit?".

Specific to S22:

- Before each chosen-candidate-specific claim in a commit message,
  verify against the actual source / runtime output:
  - Candidate F: integration site exists; `RobotsPolicy` import
    succeeds; bypass-config mechanism's docstring lines; cost-
    journal field names verified against the on-disk journal
    schema.
  - Candidate B: per-tier cost-journal field presence.
  - Candidate E: cassette counts post-record.
- Before claiming combined suite count, re-run pytest.
- Before claiming ruff/format clean, re-run ruff against the
  touched files.
- Before claiming a SHA prefix in a commit message body, verify the
  prefix is correct via `git show --no-patch --format=%h <ref>`.

Avoid bash pipe artifacts that mask Python exit codes (LESSONS):
`python_cmd 2>&1 | grep ... | tail` makes `$?` reflect tail's exit.
Use `> stdout.out 2> stderr.err; echo $?` or `${PIPESTATUS[0]}`
when exit-code matters.

LESSONS-folded discoveries from S21 worth re-applying if S22 takes
Candidate F:
- stdlib `RobotFileParser.crawl_delay()` returns `default_entry`
  (*) delay first; specific-UA Crawl-delay only reached if no `*`
  delay exists. S21 worked around at the parser layer via
  `_crawl_delay_for(parser, user_agent)`. If S22 integration sleeps
  on `decision.crawl_delay`, verify the parser is actually
  returning the specific-UA value when applicable (don't re-
  discover from scratch).
- stdlib `applies_to()` strips input after `/` and substring-
  matches the bare bot name. If the production UA at integration
  time is `BarcadaCrawler/1.0`, robots.txt rules naming
  `BarcadaCrawler` will match.
- stdlib Disallow/Allow ordering is first-match-wins. Pin in
  integration tests if behavior matters at the policy level.

---

## Commit hygiene (per LESSONS + S19/S20/S21 additions)

- File-based commit messages at `/tmp/<id>-msg.txt`.
- Per-module commits (Phase 3 commit shape unless Q-SHARED.1
  overrides).
- "Confirm to commit?" before EVERY commit. Pair with verification
  table (always) and `git diff --staged` (when appropriate per
  `[[double-check-before-commit]]` triggers).
- Commit body includes: action ref (e.g., `WA1.W8.integration` for
  Candidate F), scope summary, file touches, test count delta,
  plan reference. NO `Co-Authored-By`.
- Pre-push gate must run green. Never use `--no-verify`.
- Pre-push vermin: `git ls-files '*.py' | xargs vermin
  --target=3.10` to filter venv-internal pytest 3.14 false-
  positives.
- Mid-implementation ruff format-check, not only pre-push.
- Sibling-module style consistency for one-file additions — match
  the immediate sibling's conventions even where they technically
  violate project-wide rules; **disclose explicitly in the commit
  body** (S21 follow-up LESSONS finding).
- Workspace close-out (Phase 6) lands as its own commit at session
  close.

---

## Context-window awareness

S21 ran lean (single commit + 1 follow-up). S22 budget per scope:

- Candidate F: medium (150-250 LOC + docs + integration tests +
  per-module commits). Should fit cleanly.
- Candidate A: medium-large (~300 LOC).
- Candidate B: small-medium (100-200 LOC; sensitive driver-area
  touch).
- Candidate D/E: small.

Strategies:
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore subagent
  per S21 "Explore-subagent + spot-check" LESSONS pattern.
- For any live-HTTP corpus work (Candidate E), pilot with 1-3
  cassettes first per S18+S20 staged-rollout pattern.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before the chosen S22 scope closes,
  transition per "no mid-commit-batch transitions" — finish in-
  flight sub-surface, then close session and refill the transition
  template for Session 23.

---

## Reporting in chat at session close

After all Session 22 commits land + push + close-out per the
S13-21 pattern:

1. Commit SHA(s) of each S22 sub-surface.
2. Sub-surface(s) landed (per candidate).
3. Test count delta: 420 baseline → S22 close.
4. Driver suite count at S22 close (46/46 expected unless
   Candidate B W5.X-prefix realigned).
5. Files touched per sub-surface.
6. Tag dispositions (incl. `workstream-a-week1-end` if Candidate F
   closed it OR `workstream-0-end` if Candidate B closed it).
7. Per-tier cost-accounting wiring gap disposition: patched
   (Candidate B) or carry-forward.
8. W A.1 integration disposition: shipped (Candidate F) or carry-
   forward.
9. Any spend (LLM, infrastructure, cassette-capture).
10. Robots.txt compliance log (if Candidate F did live work or
    Candidate E expanded the cassette corpus).
11. FP-curation log update (if Candidate E expanded the cassette
    corpus).
12. Verify-before-asking summary: any source-verification findings
    surfaced.
13. Outstanding items for Session 23.
14. Tags state at S22 close.

Do not propose Phase 4 PR-D/E/F/G work this session unless
Candidate D was chosen and operator-led labeling is in flight.

---

## Carry-forward bakes (no amendment file needed)

All S21 amendments (3 commits between sessions: `161efda` /
`1f83fab` / `0640939`) plus the S21 post-close audit corrections
(`332f390`) have been folded directly into this prompt — S22 does
not need a separate amendment file:

- **S21 follow-up corrections** folded into Step 0.1 (workspace
  anchor `332f390`), Step 0.9 (parser API stability check),
  Candidate F prereqs (parser API stability + Q-C.4 deferred-from-
  S21 framing).
- **5 LESSONS sections from S21 close** referenced where they
  apply: Library-quirk patterns (verify-before-asking S22-
  specific); Workspace HEAD delta tolerance (Step 0.1); Single-
  module commit collapse (Phase 3); Explore + spot-check (Phase 2);
  Sibling-module style disclosure (Commit hygiene).

If new amendments arise pre-S22 open, walk them per the reviewer-
feedback hygiene pattern in this prompt's "Reviewer-feedback
hygiene" section.
