# Session 20 prompt — DRAFT — Workstream A.0 Week 7 remainder
# (cassettes + canary)

**STATUS: DRAFT.** Drafted at Session 19 close (2026-05-22) with
fresh context. Operator should review, refine, and invoke as the
Session 20 prompt. Copy or symlink into `~/Downloads/session-20-prompt.md`
when ready.

This prompt pre-resolves the 6 design-gate sub-questions surfaced
during Session 19's reviewer-feedback review (cassette tool /
capture mode / robots compliance / corpus curation / determinism
gate / barcada-drift naming) so Phase 2 elicitation is tight.
It also enforces strict phase ordering per the regression-
protection checklist landed in `SESSION_TRANSITION_TEMPLATE.md`
at Session 19 close.

---

## Scope

Engineering session. Two W A.0 W7 sub-surfaces remain after Session 19
landed the `check` sub-surface:

1. **Synthetic Crawl Tapes** (plan §4 Week 7, line 314-323).
   Record full HTTP exchanges for ~20-30 representative domains
   beyond the fixture corpus using `vcrpy` or similar; cassettes per
   domain at `tests/fixtures/synthetic_crawls/<domain>/`; future
   pipeline runs replay from cassettes instead of hitting the
   network.

2. **Canary Wiring** (plan §4 Week 7, line 325-331). Wire
   `eval_data/canary_50_domains.txt` to a scheduled job; build a
   trend dashboard showing per-domain agreement with last baseline
   run, cost per domain over time, anti-bot success rate.

Operator chooses at Phase 1 whether to land both, one, or defer
both (e.g. if `barcada-drift` naming requires AI/ML team
consultation that can't happen in this session).

**Sessions 13-19 precedent:** this session does NOT modify the
W4.1.5 driver orchestration at `tests/runners/fixture_cascade/`
(locked at `dd64963`). Does NOT modify `expected.schema.json` v1.1
/ `META_SCHEMA.md` v1.1 (locked at W4.3 close). Does NOT modify
the committed `tests/fixtures/baseline-v0/` snapshot at `9e9a1fb`.
Does NOT modify the Session 19 `check` sub-surface code
(`tools/baseline_v0/check.py`, `tests/baseline_v0/test_check.py`,
the 6 check-dispatch tests in `tests/baseline_v0/test_cli.py`).
Does NOT modify production code under `src/barcada_scraper/`
UNLESS Phase 2 design-gate explicitly authorizes a specific module.

Full regression-protection checklist is in
`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`. Re-read it before
any code lands.

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

Run in order. Halt and surface to operator on any mismatch.

### Step 0.1 — Workspace + repo HEAD

```
# Workspace at Session 19 close-out commit:
git -C ~/crawler-audit rev-parse HEAD
# Expect: 868f141 (Session 19 close-out)

# Repo at Session 19 final commit:
git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: 467647e (WA0.W7.check-tests)
```

If HEADs differ, halt — workspace or repo may have advanced post-S19.

### Step 0.2 — Tags

```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort
# Expect 8 tags:
#   baseline-v0
#   pre-remediation-2026-05-19
#   workstream-0-week1-end
#   workstream-0-week2-end
#   workstream-0-week3-end
#   workstream-0-week4-1-5-end
#   workstream-0-week4-end
#   workstream-0-week5-end
```

### Step 0.3 — Driver locked

```
cd /Users/administrator/projects/barcada-scraper
git diff dd64963..HEAD -- tests/runners/fixture_cascade/ \
    ':(exclude)tests/runners/fixture_cascade/test_fixture_fetcher.py'
# Expect: empty (only test_fixture_fetcher.py changed via W5.X realign
# at 8d0fc0e in Session 16).
```

### Step 0.4 — Fixture counts

```
find tests/fixtures/html -name '*.html' -type f | wc -l
# Expect: 222

find tests/fixtures/html -path '*/expected/*.json' -type f | wc -l
# Expect: 202

find tests/fixtures/html -name '*.meta.json' -type f | wc -l
# Expect: 222

find tests/fixtures/baseline-v0 -type f | wc -l
# Expect: 1213
```

### Step 0.5 — Test-suite baseline

```
.venv/bin/python -m pytest tests/scraper/test_fixture_conformance.py \
    tests/runners/fixture_cascade/ tests/baseline_v0/ -q
# Expect: 332 passed / 0 failed / 0 skipped
```

The S19 close baseline is 210 conformance + 46 driver + 76
baseline_v0 = 332. Any drift = halt.

### Step 0.6 — Manifest + schema invariants

```
.venv/bin/python -c "
import json
m = json.load(open('tests/fixtures/baseline-v0/manifest.json'))
assert m['schema_version'] == 'baseline-v0/0.1.0', m['schema_version']
assert m['fixture_count'] == 202, m['fixture_count']
assert m['llm_mode'] == 'real', m['llm_mode']
assert m['driver_sha'] == '521e363466435c30deab7cdc63a73649c8de3bce'
print('OK manifest baseline-v0/0.1.0; check sub-surface comparison gate valid')

s = json.load(open('tests/fixtures/expected.schema.json'))
assert len(s['properties']['stage3_decision']['required']) == 18
print('OK expected.schema.json v1.1 (18-col stage3 shape)')
"
```

### Step 0.7 — check sub-surface still works

```
.venv/bin/python -m tools.baseline_v0 check --help > /dev/null && echo OK
# Expect: OK
```

If any of 0.1-0.7 fail, HALT before doing any work.

---

## Required workspace reading (Session 20 first 10 minutes)

In this order:

1. **`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`** —
   especially the "Session 20 execution order" + "Regression-
   protection checklist" sections landed at Session 19 close.

2. **`~/crawler-audit/SESSION_LOG.md`** Session 19 entry — what
   landed during `check` (3 commits b358a02 → eca4ec0 → 467647e);
   the auth_403-vs-empty_google_sites claim-error retrospective;
   the always-verify-claim strict rule operator-codified mid-
   session; the 5 forward-applicable patterns at the end.

3. **`~/crawler-audit/LESSONS.md`** — operator patterns. Session
   19 forward-applicable findings should be folded into LESSONS
   (claim-verification-before-commit strict rule;
   bash-pipe-exit-code-masking; mid-implementation ruff format-
   check; sibling-module style consistency; integration-tests-
   self-seed-via-siblings; reviewer-feedback hygiene).

4. **`~/crawler-audit/BARCADA_CRAWLER_REMEDIATION_PLAN.md`** §4
   Week 7 (cassettes + canary; READ-ONLY) and §11 Risk Register
   (the 3 new Session 19 entries: cassette robots compliance;
   cassette FP corpus; cassette network-vs-capture mode cost).

5. **`~/crawler-audit/CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8
   (`barcada-drift` CLI; ~300 LOC; crawler-owned with joint AI/ML
   decisions). The naming/ownership question is Phase 1's first
   sub-question.

6. **`tools/baseline_v0/`** at HEAD `467647e` — re-read
   `cli.py` (argparse subparser + lazy-import dispatch pattern;
   the new cassettes/canary subcommands slot in the same way the
   Session 19 `check` subparser did) + `check.py` (5-helper
   structure to mirror) + `determinism.py` (canonical_json +
   hash_canonical to reuse if cassette outcomes need hashing).

7. **`tests/baseline_v0/test_check.py`** at HEAD `467647e` — the
   pattern for any new sub-surface's tests: helper unit tests +
   validation-path tests + integration tests that self-seed via
   siblings.

---

## Phase 1 — Naming + scope resolution (no code; pre-design-gate)

### Sub-question 1.1 — `barcada-drift` vs `barcada-baseline canary-run`

Plan §4 W7 (line 327) specifies:

```
barcada-baseline canary-run --domains canary_50_domains.txt
    --output canary_runs/<date>.parquet
```

CLASSIFICATION_ADJACENT_PLAN.md §Item 8 separately specifies:

> New `barcada-drift` CLI (crawler-owned), ~300 LOC, with
> joint-with-AI/ML alert wiring + trend dashboard. Decisions
> needed from AI/ML team:
>   1. Drift metric definition (per-domain agreement /
>      score-distribution shift / calibration drift / per-category
>      prediction-rate shift)
>   2. Alert threshold
>   3. Canary curation (50 domains representative? refresh
>      periodically?)
>   4. Action on drift (re-eval / retraining trigger / manual)

These overlap. Three plausible resolutions:

**(A) Same surface under different names.** `barcada-baseline
canary-run` (data collection: per-domain pipeline invocation +
parquet output) and `barcada-drift` (drift detection orchestration
on top of canary-run output) are two layers of one stack.
Session 20 ships `canary-run` per the plan; `barcada-drift`
follows later when AI/ML team decisions land.

**(B) Two separate surfaces under separate CLIs.** Build
`barcada-drift` directly under its own namespace; `barcada-
baseline canary-run` is superseded. Requires Session 20 commit
to a name AI/ML hasn't authorized — risky.

**(C) Defer canary entirely.** Ship cassettes only this session;
canary opens after AI/ML team alignment.

Surface as the first Phase 1 AskUserQuestion.

### Sub-question 1.2 — Sub-surface scope

Given 1.1's resolution:

- **Cassettes + canary**: both land this session. Largest scope.
- **Cassettes only**: ship cassettes; canary deferred (e.g., if
  1.1 → option C).
- **Canary only**: ship canary; cassettes deferred (less common;
  cassettes have larger design surface so this would be unusual).
- **Defer both**: end Session 20 early at Phase 0 + Phase 1
  scope-resolution only; substantive work waits for Session 21.

**HALT IF** 1.1 cannot resolve without external AI/ML consultation
that can't happen in this session. Default to deferring canary
and continuing with cassettes only.

---

## Phase 2 — Design-gate elicitation (no code; AskUserQuestion)

Surface in 2-3 AskUserQuestion batches. Each chosen sub-surface
from Phase 1 unlocks its own questions.

Pre-source-verify at session-current HEAD per
`[[verify-before-asking-discipline]]`:

- Re-read `tools/baseline_v0/cli.py` to confirm the subparser
  pattern is unchanged from Session 19 close.
- Re-read `tools/baseline_v0/check.py` to confirm shared symbols
  (`COMPONENT_NAMES`, `canonical_json`, `hash_canonical`) the
  new sub-surfaces may import.
- Read first 10 lines of `eval_data/canary_50_domains.txt` to
  confirm the 50-line format (comment-stripped count == 50).

### Cassette sub-questions (if cassettes in scope)

**Q2.1 — Cassette tool selection.**

- **vcrpy (Recommended; plan's named choice)**: Python-native,
  YAML cassette format, well-known ecosystem. Standard for
  HTTP-replay testing.
- **mitmproxy export**: heavier dependency; more featureful
  (TLS interception, full-protocol capture). Justify only if
  vcrpy's HTTP-level capture is insufficient for the project's
  needs.
- **Custom cassette format**: highest design surface; only
  justify if both above can't handle the use case.

**Q2.2 — Cassette capture mode.**

- **Network-only (Recommended for cost-first)**: record HTTP
  exchanges; baseline outcomes computed later by replaying
  through the pipeline. Cost envelope: $0 per cassette during
  recording; pipeline runs are zero-cost on replay (vcrpy
  intercepts all HTTP). Total: ~$0 for recording + ~$0.20-$3.00
  for one-time baseline-outcome pass through cascade in
  fake/real mode.
- **Capture-and-classify**: record HTTP AND run cascade
  classification simultaneously. Baseline outcomes per domain
  land at the same time as the cassette. Cost: $0.30-$1.50 per
  domain × 20-30 = $6-$45. 2-15× higher than network-only.
- **Hybrid**: record network-only for cassettes, then run
  pipeline in fake mode on replay for synthetic baseline
  outcomes (zero LLM cost). Equivalent to network-only with an
  explicit pipeline-pass step.

**Q2.3 — Robots.txt compliance approach.**

Plan §4 W7 chronology has the W A robots.txt parser landing
AFTER W7. Live HTTP recording in Session 20 without robots.txt
compliance is the exact compliance gap Workstream A is meant
to close. Three options:

- **Per-domain pre-record robots.txt check (Recommended)**:
  before each recording, fetch and parse `<domain>/robots.txt`,
  refuse to record if the User-Agent's path is disallowed.
  Standalone helper, no Workstream A dependency. Documented in
  the cassette metadata.
- **Restrict corpus to canary_50 vetted subset**: the 50
  canary domains are well-known institutional (example.com,
  iana.org, python.org, mit.edu, wikipedia.org, etc.). Most
  have permissive robots.txt. Bypass the per-domain check by
  curating only domains operator has pre-cleared. Faster but
  more constrained.
- **Defer cassettes to post-W A**: cassette work waits for the
  robots.txt parser to land in Workstream A. Cleanest
  compliance-wise; postpones cassette delivery.

**Q2.4 — Corpus scope + FP curation.**

LESSONS S9 documented ~36% FP rate on modern SaaS marketing
sites (`dd.js`, `just-a-moment`, `(?:search|query|keyword).*no
results found` patterns in `barriers.py`). If cassette corpus
includes modern-SaaS candidates, those FPs bake into the
"expected" baseline; later detector fixes look like regressions.

- **Canary_50 subset (e.g., 20-30 of 50)** + run
  `extract_hard_exclusions` on each before recording to
  identify FP-tripping candidates. Drop FPs OR document
  cassettes-that-encode-known-FPs in a sidecar file. Smallest
  curation cost.
- **Fresh curated 20-30-domain list** across SaaS / marketplace
  / agency / content. Higher FP risk; same `extract_hard_
  exclusions` gate required. Larger curation surface.
- **Cross-product with the existing fixture corpus**: re-record
  cassettes for known-tested fixtures so the cassette → pipeline
  outcomes can be cross-checked against the committed
  baseline-v0 manifest. Lowest design risk; least novel
  coverage.

**Q2.5 — Cassette module placement.**

- **New `tools/synthetic_crawl/` namespace package
  (Recommended)**: parallel to `tools/baseline_v0/`. Isolates
  recording/replay surface from baseline-v0 logic. Matches plan
  §4 W7's separate-bullet framing.
- **Extension inside `tools/baseline_v0/` as
  `tools/baseline_v0/cassettes.py` + subcommand**: tighter
  coupling. Simpler if cassette outputs feed the same generate/
  check pipeline directly.

**Q2.6 — Cassette determinism gate.**

- **Byte-identical replay across 2 runs (Recommended)**: analog
  of `test_generate_integration_byte_identical_rerun` in
  `tests/baseline_v0/test_generate.py`. Two replay-mode runs of
  the same cassette must produce identical pipeline output.
- **Documented-exclusion list of non-deterministic fields**:
  if some fields (e.g., timestamps, request IDs) are
  intentionally non-deterministic, list them explicitly and
  exclude from the determinism check.

### Canary sub-questions (if canary in scope)

**Q2.7 — Canary scheduler mechanism.**

- **GitHub Actions cron (Recommended)**: cleanest; integrates
  with existing CI; no additional infra. Schedule weekly per
  plan §4 W7 line 331.
- **Server cron daemon**: more flexibility; requires operator-
  managed infrastructure.
- **Operator-driven manual run for now**: defer scheduler
  wiring; just ship the `canary-run` subcommand. Operator
  invokes weekly manually.

**Q2.8 — Trend dashboard scope.**

- **Full (3 metrics)**: per-domain agreement with last
  baseline run, cost per domain over time, anti-bot success
  rate. Per plan §4 W7 line 331.
- **Minimal (1 metric)**: per-domain agreement only; cost +
  anti-bot deferred. Smaller surface for this session.

### Shared sub-questions

**Q2.9 — Commit shape.**

- **Per-module (Recommended)**: matches Sessions 18 + 19
  patterns. For cassettes: 4 commits (skeleton → driver → tests
  → corpus-capture). For canary: 4-5 commits (skeleton → impl
  → tests → scheduler → dashboard). Per Sessions 11-19 LESSONS.
- **Per-sub-surface bundled**: 1-2 commits per sub-surface.
  Tighter git log; harder to bisect.

**Q2.10 — Tag at session close.**

- **`workstream-0-week7-end` at full-W7-close (Recommended if
  both cassettes + canary land)**: marks W7 complete; W0 still
  has potential follow-ups (per-tier cost-accounting wiring
  gap if not patched).
- **`workstream-0-end` at full-W7-close**: marks Workstream 0
  fully closed; appropriate ONLY if cassettes + canary fully
  close all W A.0 work AND no carry-forwards.
- **Defer all**: cassettes + canary land but no tag placed;
  future tag supersedes.

**HALT IF** any Phase 2 decision would require modifications to
`src/barcada_scraper/` production code OR to the W4.1.5 driver —
surface as a design-gate sub-question before patching.

---

## Phase 3 — Implementation (per-module commits, strict order)

Per Phase 2's commit-shape decision. The default (per-module)
sequence is:

### Cassettes (if in scope)

1. **`WA0.W7.cassettes-skeleton`** — subparser in `tools/baseline_v0/
   cli.py` (or new `tools/synthetic_crawl/cli.py` per Q2.5);
   stub module returning exit-2; argparse + dispatch validated
   via `--help`. NO functional logic; CLI surface only.
   Combined-suite at boundary: 332/0/0.

2. **`WA0.W7.cassettes-driver`** — recording mode + replay
   mode. NO live HTTP yet — exercise with mocked HTTP
   (`respx` or `requests-mock`). Cyclomatic complexity per
   helper <15.
   Combined-suite at boundary: 332/0/0.

3. **`WA0.W7.cassettes-tests`** — unit (helpers) + validation-
   path (missing-cassette returns exit-2) + integration (mock-
   HTTP round-trip: record → replay → byte-identical assertion
   per Q2.6).
   Combined-suite at boundary: 332 + N new tests, all passing.

4. **`WA0.W7.cassettes-corpus-capture`** — actual live
   recordings of the chosen N-domain corpus (Q2.4). Each
   recording preceded by the robots.txt compliance gate from
   Q2.3. Cost-aware: halt + re-estimate if actual spend exceeds
   3× the Q2.2 budget envelope.
   Combined-suite at boundary: previous + N new cassette
   artifacts (file count grows; no test count change unless
   integration tests reference real cassettes).

### Canary (if in scope)

5. **`WA0.W7.canary-skeleton`** — subparser + stub returning
   exit-2; CLI surface validated.
   Combined-suite at boundary.

6. **`WA0.W7.canary-impl`** — parquet output to
   `canary_runs/<date>.parquet`; per-domain pipeline invocation.
   Combined-suite at boundary.

7. **`WA0.W7.canary-tests`** — argparse + canary-file parsing
   + parquet output schema validation.
   Combined-suite at boundary.

8. **`WA0.W7.canary-scheduler`** — GitHub Actions workflow
   (`.github/workflows/canary.yml`) OR cron config OR operator-
   doc per Q2.7.
   Combined-suite at boundary (no Python tests affected unless
   workflow shape requires test changes).

9. **`WA0.W7.canary-dashboard`** — trend script/notebook per
   Q2.8 scope.
   Combined-suite at boundary.

### At every commit boundary

- **Combined suite** (conformance + driver + baseline_v0 + new
  W7 test modules) green.
- **ruff check + format --check** on touched files green.
- **`[[double-check-before-commit]]` strict rule**: every
  concrete claim in commit message verified against source/
  output BEFORE staging. Build verification table in chat.
- **`[[git-status-before-wrap]]` partial application**: git
  status to confirm only intended files staged.

HALT IF combined suite goes red and the new failure is NOT a
deliberate consequence of the surface-under-test.

---

## Phase 4 — Pre-push gate (whole-tree)

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 332+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

HALT IF any gate red. Never use `--no-verify`.

---

## Phase 5 — Push + tag

- Push to `origin/main` after operator confirms.
- Tag per Q2.10 decision (or defer).

---

## Phase 6 — Workspace close-out

- Append Session 20 entry to `~/crawler-audit/SESSION_LOG.md`
  (Sessions 13-19 precedent format).
- Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md` for
  Session 21.
- Single workspace commit at session close. Push workspace
  after operator confirms.

---

## Acceptance criteria

**For W A.0 W7 cassettes (full scope; reduce if Phase 1 narrows)**:

1. Cassette-recording driver works against the chosen N-domain
   corpus; cassettes at `tests/fixtures/synthetic_crawls/
   <domain>/` (or chosen subtree per Q2.5).
2. Replay-mode integration test confirms byte-identical
   pipeline output across 2 consecutive runs per Q2.6.
3. Robots.txt compliance gate enforced per Q2.3 — every
   committed cassette has documented compliance.
4. Detector-FP curation per Q2.4 — every committed cassette
   has documented `extract_hard_exclusions` outcome at record
   time.

**For W A.0 W7 canary (full scope; reduce if Phase 1 narrows)**:

5. `barcada-baseline canary-run` (or `barcada-drift` per Q1.1)
   CLI works against `eval_data/canary_50_domains.txt`;
   produces a parquet output file at `canary_runs/<date>.parquet`.
6. Scheduler wiring (Q2.7) committed.
7. Trend dashboard (Q2.8) committed.

**Shared**:

8. Combined suite at session close: existing 332 baseline + N
   new tests across the new sub-surfaces, all passing.
9. Pre-push gate runs green.
10. Tag placed per Q2.10 OR explicit defer.
11. Per-tier cost-accounting wiring gap remains DEFERRED unless
    explicitly authorized (carry-forward; severity LOW).
12. Regression-protection checklist held: the 24 `test_check`
    tests stay 24/24 green; `tools/baseline_v0/check.py` and
    `generate.py` and `determinism.py` not modified.

---

## Out-of-scope (no exceptions without operator authorization)

[Per the regression-protection checklist in
SESSION_TRANSITION_TEMPLATE.md, summarized:]

- The W4.1.5 driver orchestration code at
  `tests/runners/fixture_cascade/`.
- The committed `tests/fixtures/baseline-v0/` snapshot at
  `9e9a1fb`.
- The Session 19 `check` sub-surface code (cli.py existing
  arguments, check.py entirely, test_check.py 24 tests,
  test_cli.py 6 check-dispatch tests).
- Existing `generate` subparser in cli.py + generate.py +
  determinism.py.
- All locked artifacts (eval_data/, stage1.schema.json,
  expected.schema.json v1.1, META_SCHEMA.md v1.1,
  meta.schema.json v1.0, all workstream tags, plan, classification
  plan, RECONCILIATION, etc.).
- Production code under `src/barcada_scraper/` (unless Phase 2
  authorizes a specific module).
- Pipeline configs in `configs/`.
- Phase 4 PR-D/E/F/G work (opens after Workstream 0 fully
  closes).

---

## Verify-before-asking discipline (strict rule from Session 19)

Per `[[double-check-before-commit]]` memory (operator-codified
during Session 19): **ALWAYS verify every concrete claim in the
commit message against actual source/output BEFORE staging.**
Fixture names, file counts, exit codes, line counts, test
counts, helper names, smoke outcomes. No claims by pattern-
completion. Build a verification table in chat (claim → reality
→ status) and reconcile before "Confirm to commit?".

Specific to Session 20:

- Before each `extract_hard_exclusions` claim in the cassette
  corpus curation log, run the function and inspect output.
- Before each cost-projection claim, verify the actual per-
  domain cost via a 1-2-domain pilot run before fanning out.
- Before each cassette determinism claim, run the byte-identical
  replay test against the actual cassette, not against a mock.
- Before each commit message lists a fixture name or domain,
  verify against the actual cassette filename or corpus list.
- Before claiming combined suite count, re-run pytest.
- Before claiming ruff/format clean, re-run ruff against the
  touched files.

Avoid bash pipe artifacts that mask Python exit codes:
`python_cmd 2>&1 | grep ... | tail` makes `$?` reflect tail's
exit. Use `> stdout.out 2> stderr.err; echo $?` or
`${PIPESTATUS[0]}` when exit-code matters.

---

## Commit hygiene (per LESSONS.md + Session 19 additions)

- File-based commit messages at `/tmp/<id>-msg.txt`.
- Per-module commits (Phase 3 commit shape unless Q2.9 overrides).
- "Confirm to commit?" before EVERY commit. Pair with
  verification table (always) and `git diff --staged` (when
  appropriate per `[[double-check-before-commit]]` triggers).
- Commit body includes: action ref (`WA0.W7.cassettes-skeleton`,
  `WA0.W7.canary-impl`, etc.), scope summary, file touches,
  test count delta, plan reference. NO `Co-Authored-By`.
- Pre-push gate must run green. Never use `--no-verify`.
- Pre-push vermin: `git ls-files '*.py' | xargs vermin
  --target=3.10` to filter venv-internal pytest 3.14 false-
  positives.
- Mid-implementation ruff format-check, not just pre-push (S19
  finding: skeleton commits with multi-line `help=` strings
  shipped pre-format-clean only if pre-push ran).
- Sibling-module style consistency for one-file additions
  (e.g., new cassette/canary helpers should match generate.py +
  check.py conventions even where they technically violate
  project-wide rules; disclose explicitly).
- Workspace close-out (Phase 6) lands as its own commit at
  session close.

---

## Context-window awareness

Session 20 spans CODE + DESIGN + LIVE-HTTP + COST-VARIABLE work.
Strategies:

- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore
  subagent if cassette-tool API audit requires reading >3 files.
- For cassette-corpus capture, pilot with 1-3 cassettes for
  early validation before full N-domain run (Session 18
  staged-rollout pattern).

Self-monitor cadence:

- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before W A.0 W7 closes, transition per
  "no mid-commit-batch transitions" — finish in-flight sub-
  surface, then close session and refill the transition template
  for Session 21. Defer remaining W7 work to a fresh session.

---

## Reporting in chat at session close

After all Session 20 commits land + push + close-out per the
Session 13-19 pattern:

1. Commit SHA(s) of each Session 20 sub-surface (cassettes
   skeleton/driver/tests/capture; canary skeleton/impl/tests/
   scheduler/dashboard — whichever landed).
2. Sub-surfaces landed (cassettes; canary; both; etc.).
3. Test count delta: Session 19 baseline (332/0/0) → Session 20
   close.
4. Driver suite count at Session 20 close (46/46 expected
   unless realigned).
5. Files touched per surface: new CLI modules, new tests, any
   conformance test changes, cassette corpus, scheduler config.
6. Tag dispositions (`workstream-0-week7-end` if placed;
   `workstream-0-end` if Workstream 0 fully closes; carry-
   forward tag dispositions).
7. Per-tier cost-accounting wiring gap disposition: patched or
   carry-forward.
8. Cassette-capture spend vs the Q2.2-decided budget envelope.
9. Robots.txt compliance log: per-cassette pre-record outcome.
10. Detector-FP curation log: per-cassette
    `extract_hard_exclusions` outcome.
11. Verify-before-asking summary: any source-verification
    findings surfaced during Session 20.
12. Outstanding items for Session 21 / next workstream.
13. Tags state at Session 20 close (all prior + any new
    W7-era markers).

Do not propose Phase 4 PR-D/E/F/G work this session. Phase 4
opens in its own session after Workstream 0 fully closes.
