# Session 21 prompt — scope picked at Phase 1
# (W A.0 W7 fully closed at S20; Workstream 0 close OR forward-
#  W A.1 / barcada-drift / corpus expansion open as S21 scope)

**Drafted at Session 20 close (2026-05-23).** Bakes in the 3
carry-forward amendments from the S20 amendments file (MF-1
driver_sha prefix-match; MF-2 Q1.1(B) wording; SR-8 Phase 1 HALT
tightening) and the 7 LESSONS sections that landed at S20 close.
Invoke from `~/Downloads/session-21-prompt.md` (mirror of this
file).

This prompt is scope-agnostic at Phases 0/1 and elicits scope-
specific design gates at Phase 2. Operator picks at Phase 1 from
five pre-resolved candidates. Strict 7-phase ordering with halt-
on-mismatch is preserved from the S20 prompt.

---

## Scope

Engineering session. Workstream 0 sub-surfaces remaining after
Session 20 closed W A.0 W7:

- **W7 fully closed** — check (S19), cassettes (S20), canary
  (S20) all shipped. `workstream-0-week7-end` tag placed at
  `ea37102`.
- **Per-tier cost-accounting wiring gap** — carry-forward from
  S14; severity LOW; closing it would justify
  `workstream-0-end` tag.
- **barcada-drift** — deferred per Q1.1=(A) at S20; needs 4
  AI/ML decisions per CLASSIFICATION_ADJACENT_PLAN.md §Item 8
  before CLI shape can be committed to.
- **W A.1 robots.txt parser** — plan §4 W8; W A opens after
  W A.0 fully closes.
- **Cassette corpus expansion** — current 20 is lower bound of
  plan's "~20-30" range.

Operator chooses at Phase 1 which candidate Session 21 ships.
Choices and prerequisites are in **Phase 1 — Scope resolution**
below. Each candidate has its own Phase 2 design-gate template.

**Sessions 13-20 precedent:** this session does NOT modify the
W4.1.5 driver orchestration at `tests/runners/fixture_cascade/`
(locked at `dd64963`). Does NOT modify `expected.schema.json`
v1.1 / `META_SCHEMA.md` v1.1 (locked at W4.3 close). Does NOT
modify the committed `tests/fixtures/baseline-v0/` snapshot at
`9e9a1fb`. Does NOT modify the Session 19 `check` sub-surface
code or the Session 20 cassettes/canary sub-surface code
(`tools/synthetic_crawl/`, `tools/baseline_v0/canary.py`,
`tests/synthetic_crawl/`, `tests/baseline_v0/test_canary.py`,
`tests/fixtures/synthetic_crawls/`, `scripts/launchd/`). Does
NOT modify production code under `src/barcada_scraper/` UNLESS
Phase 2 design-gate explicitly authorizes a specific module.

Full regression-protection checklist in **Out-of-scope** at the
end of this prompt. Re-read it before any code lands.

---

## Reviewer-feedback hygiene (if this prompt is reviewed)

If an external reviewer (operator-invoked) flags items in this
prompt before Session 21 starts, walk each flagged item against
on-disk reality at HEAD `ea37102` BEFORE applying any change.
Per S19/S20 pattern (LESSONS "Reviewer-feedback hygiene"):

- **OBSOLETE** items: SHAs already verified, claims already
  true. Skip with documented reasoning.
- **VALID-applies-now** items: bear on this session's scope.
  Apply.
- **VALID-applies-later** items: bear on deferred scope. Carry
  forward to the next prompt revision.
- **WRONG-PREMISE** items: assumes something not true. Skip
  with documented reasoning.

Empirical baseline: at S19 review, 3 of 5 "must-fix" items
collapsed under cold-start verification. At S20 review, 1 of 12
amendments was skipped because it would HALT spuriously (SR-4).
Do not pattern-apply.

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
  (b) Skip the phase per operator authorization (rare;
      document the skip in SESSION_LOG.md).
  (c) End the session early at Phase 6 close-out with the halt
      recorded in SESSION_LOG.md.

Halt is not failure — it's the contract. Phase 0 halts catch
stale state. Phase 1 halts catch unresolved scope-blockers
(AI/ML decisions for Candidate A; W5.X-prefix authorization for
Candidate B). Phase 2 halts catch hidden scope expansion. Phase
3 halts catch regressions. Phase 4 halts catch pre-push gate
failures (incl. operator-WIP-in-locked-tree; see LESSONS).

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

Run in order. Halt and surface to operator on any mismatch.

### Step 0.1 — Workspace + repo HEAD

```
# Workspace at Session 21 start (Session 20 close-out + S21
# prompt-draft commits). Both SHAs are recorded under
# SESSION_TRANSITION_TEMPLATE.md "Workspace state" section:
git -C ~/crawler-audit rev-parse HEAD
# Expect: dccab29 (S21 prompt-draft commit, the most recent at
# S20 close) OR a later commit if additional workspace doc edits
# landed post-S20-close. If N commits ahead, verify each prior
# commit's subject via `git log --oneline dccab29..HEAD` against
# expected prompt-finalization / doc-edit patterns; surface the
# SHA delta and request authorization to proceed if anything is
# unexpected. (S20 precedent: operator authorized continuation
# when 2 extra workspace commits were the strengthened S20 prompt
# itself.)

# Repo at Session 20 final commit:
git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: ea37102 (WA0.W7.canary-launchd-kit)
```

### Step 0.2 — Tags

```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort
# Expect 9 tags:
#   baseline-v0
#   pre-remediation-2026-05-19
#   workstream-0-week1-end
#   workstream-0-week2-end
#   workstream-0-week3-end
#   workstream-0-week4-1-5-end
#   workstream-0-week4-end
#   workstream-0-week5-end
#   workstream-0-week7-end          (NEW S20)
```

### Step 0.3 — Driver locked

```
cd /Users/administrator/projects/barcada-scraper
git diff dd64963..HEAD -- tests/runners/fixture_cascade/ \
    ':(exclude)tests/runners/fixture_cascade/test_fixture_fetcher.py'
# Expect: empty (only test_fixture_fetcher.py changed via W5.X
# realign at 8d0fc0e in Session 16).
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

find tests/fixtures/synthetic_crawls -name 'cassette.yaml' | wc -l
# Expect: 20    (NEW S20 cassette corpus)

find tests/fixtures/synthetic_crawls -name 'extract_hard_exclusions.json' | wc -l
# Expect: 20    (NEW S20 sidecar corpus)
```

### Step 0.5 — Test-suite baseline

```
.venv/bin/python -m pytest tests/scraper/test_fixture_conformance.py \
    tests/runners/fixture_cascade/ tests/baseline_v0/ \
    tests/synthetic_crawl/ -q
# Expect: 388 passed / 0 failed / 0 skipped
#         (= 210 conformance + 46 driver + 99 baseline_v0 + 33 synthetic_crawl)
```

The sub-paths add up to the headline: 210 conformance + 46 driver
+ 99 baseline_v0 + 33 synthetic_crawl = 388. Any drift = halt.

If the headline count mismatches, re-run each sub-path
independently to localize which sub-suite drifted:

```
.venv/bin/python -m pytest tests/scraper/test_fixture_conformance.py -q   # expect 210
.venv/bin/python -m pytest tests/runners/fixture_cascade/ -q              # expect  46
.venv/bin/python -m pytest tests/baseline_v0/ -q                          # expect  99
.venv/bin/python -m pytest tests/synthetic_crawl/ -q                      # expect  33
```

### Step 0.6 — Manifest + schema invariants

```
.venv/bin/python -c "
import json
m = json.load(open('tests/fixtures/baseline-v0/manifest.json'))
assert m['schema_version'] == 'baseline-v0/0.1.0', m['schema_version']
assert m['fixture_count'] == 202, m['fixture_count']
assert m['llm_mode'] == 'real', m['llm_mode']
# Per MF-1 amendment (baked into S21): assert prefix not full SHA.
assert m['driver_sha'].startswith('521e363'), m['driver_sha']
print(f'OK manifest baseline-v0/0.1.0; driver_sha prefix {m[\"driver_sha\"][:7]}')

s = json.load(open('tests/fixtures/expected.schema.json'))
assert len(s['properties']['stage3_decision']['required']) == 18
print('OK expected.schema.json v1.1 (18-col stage3 shape)')
"
```

### Step 0.7 — Existing sub-surface CLIs all work

The patterns below use `grep -oE` (ERE alternation; portable across
BSD grep on macOS and GNU grep on Linux) + `sort -u | wc -l` to
count distinct subcommand matches rather than matching lines (which
would miscount on argparse's single-line `{a,b,c}` usage rendering).
`\b` word-boundary in ERE avoids substring traps (e.g., `check`
matching `--check`, `record` matching `recorder`).

```
.venv/bin/python -m tools.baseline_v0 --help 2>&1 \
    | grep -oE '\b(generate|check|canary-run)\b' | sort -u | wc -l
# Expect: 3 (distinct subcommands: generate, check, canary-run)

.venv/bin/python -m tools.synthetic_crawl --help 2>&1 \
    | grep -oE '\b(record|replay)\b' | sort -u | wc -l
# Expect: 2 (distinct subcommands: record, replay)
```

Alternatively, rely on Step 0.8's dispatch-test counts as a stronger
behavioral check — those pytest collects exercise the full
argparse + dispatch stack and would fail loudly if a subcommand
were missing.

### Step 0.8 — Regression-protection sanity

```
# S19 check sub-surface tests (30 total: 24 test_check + 6 test_cli check-dispatch)
.venv/bin/python -m pytest tests/baseline_v0/test_check.py \
    tests/baseline_v0/test_cli.py -k 'check' -q
# Expect: 30 passed (per acceptance criterion 12 MF-3-corrected count)

# S20 canary sub-surface tests (23 total: 17 test_canary + 6 test_cli canary-dispatch)
.venv/bin/python -m pytest tests/baseline_v0/test_canary.py \
    tests/baseline_v0/test_cli.py -k 'canary' -q
# Expect: 23 passed

# S20 cassettes sub-surface tests (33 total in tests/synthetic_crawl/)
.venv/bin/python -m pytest tests/synthetic_crawl/ -q
# Expect: 33 passed
```

If any of 0.1-0.8 fail, HALT before doing any work.

---

## Required workspace reading (Session 21 first 10 minutes)

In this order:

1. **`~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`** — full
   handoff state at S20 close. Lists 5 scope candidates (A-E)
   with prerequisites + estimated scope. The S21 scope choice
   at Phase 1 picks from these.

2. **`~/crawler-audit/SESSION_LOG.md`** Session 20 entry — what
   landed during cassettes + canary (8 commits + 1 tag). The
   Phase 4 eval_data WIP halt + resolution. The 6 forward-
   applicable patterns at the end.

3. **`~/crawler-audit/LESSONS.md`** — 7 new sections folded at
   S20 close (lines 994 onward). Especially:
   - "Always verify every concrete claim in commit messages
     before staging (strict rule)" — extends `[[double-check-
     before-commit]]`.
   - "Bash pipes mask Python exit codes" — use
     `> stdout 2> stderr; echo $?` or `${PIPESTATUS[0]}`.
   - "Mid-implementation ruff format-check" — not only pre-push.
   - "Sibling-module style consistency" — disclose when applied.
   - "Integration tests can self-seed via the module-under-
     test's siblings (or hand-rolled artifacts)".
   - "Reviewer-feedback hygiene".
   - "Pre-push gate against operator-WIP territory: surface,
     don't auto-fix".

4. **`~/crawler-audit/BARCADA_CRAWLER_REMEDIATION_PLAN.md`**
   — chosen-scope section per Phase 1 candidate choice. Plan
   is READ-ONLY.

5. **`~/crawler-audit/CLASSIFICATION_ADJACENT_PLAN.md`** §Item
   8 — only if Candidate A (barcada-drift) is chosen.

6. **`~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md`** —
   only if Candidate B (per-tier cost-accounting retrofit) is
   chosen. Provides the post-Phase-4 target-state cost-envelope
   baseline against which per-tier accounting fields should be
   designed. READ-ONLY; do NOT use as current-code source-of-
   truth — see `BARCADA_CRAWLER_REMEDIATION_PLAN.md` §13 for
   the "design-of-record vs current-code" framing.

7. **Repo source pertinent to Phase 2 design-gate** — varies by
   chosen candidate; spelled out in each Phase 2 sub-section
   below.

---

## Phase 1 — Scope resolution (no code; pre-design-gate)

Operator picks one candidate. Candidates roughly ordered by
prerequisite-readiness; each is independent.

### Candidate A — `barcada-drift` (depends on AI/ML team alignment)

Per `CLASSIFICATION_ADJACENT_PLAN.md` §Item 8. Consumes the
`canary_runs/<date>.parquet` artifacts the S20 launchd job
produces. Estimated ~300 LOC per plan estimate.

**Prerequisites:**
- 2+ `canary_runs/*.parquet` files exist on operator's machine
  (the launchd job must have fired at least twice). Earliest
  natural date: 2026-06-06 (two Saturdays from S20 close at
  2026-05-23) assuming operator installs the launchd kit
  immediately and the job runs cleanly.
- AI/ML team responses on 4 §Item 8 decisions OR explicit
  operator-side placeholder choices with "AI/ML-to-tune" notes.

**HALT IF** the 4 AI/ML decisions (drift metric / alert threshold
/ canary curation / action-on-drift) are not pre-resolved going
into Session 21 AND operator has not authorized explicit
placeholder choices. Per SR-8 amendment baked into S21: only
this candidate blocks on AI/ML team availability. Default
fallback on no-pre-resolution: defer to another session and pick
a different candidate.

### Candidate B — Per-tier cost-accounting retrofit (closes Workstream 0)

The deferred-from-S14 per-tier cost-accounting wiring gap.
Currently severity LOW, carry-forward. Closing it would let
`workstream-0-end` tag be placed at the closing commit.
Touches the W4.1.5 driver area (`tests/runners/fixture_cascade/`)
which is locked except via W5.X-prefix commits per S16 precedent.
Estimated 100-200 LOC.

**Prerequisites:**
- Operator authorization at S21 Phase 1 for a W5.X-prefix commit
  touching the W4.1.5 driver. Without this auth, the candidate
  HALTs at Phase 1.
- Decision on whether the retrofit touches stage{1,2,3}_*_usd
  driver cost fields, per-row stage3_decision.evidence_cost_usd,
  or both.

### Candidate C — W A.1 robots.txt parser (W A opens)

Per plan §4 Week 8 Action #2 (Severity: CRITICAL, plan-anchored
estimate **~300 LOC** for the parser proper). Sub-question 1.C-SCOPE
(below) pins parser-only vs full-W8 scope at Phase 1 so Phase 6
acceptance criteria are unambiguous before Phase 3 starts (mirrors
the Sub-question 1.TAG pattern).

**Prerequisites:**
- Plan §4 W8 read at S21 Phase 1.
- Decision on whether to reuse the S20 cassette-side gate as a
  sibling-import or refactor both to a shared module
  (`tools/common/robots.py` or similar).
- Decision on parser library choice — stdlib
  `urllib.robotparser` (used by S20 cassette gate) vs more
  featureful third-party (e.g., `robotexclusionrulesparser`,
  `reppy`). Stdlib is the cheap baseline.

#### Sub-question 1.C-SCOPE — Parser-only vs Full-W8 (pinned at Phase 1)

Pinned here so acceptance criteria at Phase 6 are unambiguous and
Phase 2 design-gate doesn't need to re-decide. Two options:

- **Parser-only (Recommended for cost-first / context-window-first
  sessions)**: ships the production robots parser + tests; integration
  with `barcada-scrape`'s fetcher seam deferred to a follow-on
  session. Total scope: ~300 parser + ~150 tests = **~450 LOC**.
  Phase 6 acceptance: items 1, 2, 3 (parser + crawl-delay + test
  corpus); item 4 (integration) is explicitly deferred and
  documented in SESSION_LOG.md as a Session 22+ carry-forward.
- **Full-W8**: ships parser + tests + integration this session.
  Total scope: ~300 parser + ~150 tests + ~150 integration =
  **~600 LOC**. Phase 6 acceptance: all 4 items (parser, crawl-
  delay, test corpus, integration). Larger session; higher
  context-window risk; matches plan §4 W8 in one shot.

Phase 5 + Acceptance criteria read this pinned scope directly.

### Candidate D — Phase 4 PR-D operator-led labeling (mostly operator territory)

Per plan §11 Risk Register entry "Phase 4 measurement half
blocked on operator-led labeling". Stage 2 + Stage 3 labeling
gates PR-D/E/F/G.

**Prerequisites:**
- Operator-scheduled labeling effort.
- Claude Code's role limited to tooling around the labeling
  workflow (validators, batch-import scripts, eval_data hygiene
  tooling). If operator does not want tooling support, this
  candidate has no Session 21 deliverable.

### Candidate E — Cassette corpus expansion / additional fixtures

S20 shipped 20 cassettes from canary_50 known-good + tech
subsets. Plan §4 W7 line 314 cites "~20-30 representative
domains" — current 20 is the lower bound. Could expand toward
30 with more business-classification-interesting domains, OR
add cassettes for the bot-blocked / non-English / dead subsets
of canary_50.

**Prerequisites:**
- Decision on which subset(s) to expand into.
- Operator review of S20's FP-curation log (archive.org +
  hashicorp.com flagged as SaaS-shell FPs; stripe.com WAF) —
  could drop those, re-record under different UA, or keep
  as-is.

### Sub-question 1.TAG — Tag at session close (pinned at Phase 1)

Independent of scope choice; resolved fully here at Phase 1 so
Phase 5 has an unambiguous tag decision. Options per scope:

- **Candidate A** (barcada-drift): defer tag OR place candidate-
  specific (e.g., `barcada-drift-v0` at the closing commit) per
  operator choice.
- **Candidate B** (per-tier cost-accounting): if per-tier
  accounting fully closes Workstream 0, place `workstream-0-end`.
  Otherwise defer.
- **Candidate C** (W A.1 robots parser): if the full plan §4 W8
  Action #2 scope ships (parser + tests + integration), place
  `workstream-a-week1-end`. If only the parser ships (deferred
  integration), defer the tag.
- **Candidate D** (Phase 4 PR-D tooling): defer (tooling is a
  carry-forward enabler, not a workstream boundary).
- **Candidate E** (cassette corpus expansion): defer (corpus
  growth doesn't open or close a workstream boundary).

Phase 5 reads this resolution directly — no Phase 2 re-decision.

---

## Phase 2 — Design-gate elicitation (no code; AskUserQuestion)

Per chosen Phase 1 candidate. Each candidate has its own
sub-block. Source-verify at session-current HEAD per
`[[verify-before-asking-discipline]]` before each AskUserQuestion
batch (re-read the modules the chosen scope will touch; confirm
the lazy-import + dispatch pattern is unchanged; confirm any
helper signatures the new module will reuse).

**HALT IF** any Phase 2 decision would require modifications to
`src/barcada_scraper/` production code OR to the W4.1.5 driver
(except via W5.X-prefix per Candidate B's auth) OR to any S19/S20
deliverable — surface as a design-gate sub-question before
patching.

### If Candidate A (barcada-drift)

- **Q-A.1 CLI namespace**: separate `barcada-drift` binary (per
  CLASSIFICATION_ADJACENT_PLAN.md §Item 8) vs `barcada-baseline
  drift` subcommand under existing CLI (sibling of canary-run).
- **Q-A.2 Drift metric**: per-AI/ML decision OR placeholder
  (per-domain agreement vs last run is the cheapest placeholder).
- **Q-A.3 Alert threshold**: per-AI/ML decision OR placeholder
  (operator-tunable; default 10% per-domain change).
- **Q-A.4 Input contract**: how does drift surface enumerate
  the canary_runs/ parquets? (Latest 2 / all-history / explicit
  --before/--after CLI args.)
- **Q-A.5 Output shape**: JSON to stdout / parquet to file /
  alert-only-on-threshold-cross.
- **Q-A.6 Test corpus**: hand-rolled parquet fixtures (per
  S20 hand-rolled-cassette pattern) vs cassette+canary self-
  seed (drives canary_run against cassettes to produce parquet,
  then drives drift against the parquets).

### If Candidate B (per-tier cost-accounting retrofit)

- **Q-B.1 Scope of fields**: which stage{1,2,3}_*_usd journal
  fields get populated? (per-stage breakdown vs aggregate-only).
- **Q-B.2 Backfill behavior**: re-run W6 baseline-v0 generation
  to regenerate manifest with per-tier costs (~$0.21 spend;
  within remaining budget $99.29 → $99.08; well below $100
  ceiling) vs document that the existing manifest is per-tier-
  cost-unaware vs both.
- **Q-B.3 Test approach**: real-mode 1-fixture integration test
  vs fake-mode synthetic cost values.
- **Q-B.4 W5.X-prefix commit shape**: single squash commit vs
  per-module breakdown.
- **Q-B.5 Workstream-0-end tag**: place at the closing commit
  OR defer until per-tier accounting is consumed by some
  downstream surface.

### If Candidate C (W A.1 robots.txt parser)

- **Q-C.1 Helper consolidation**: refactor S20 cassette gate
  to import from new shared module vs leave cassette gate as
  standalone (canary already reuses cassette gate per S20).
- **Q-C.2 Parser library**: stdlib urllib.robotparser (cheap
  baseline; what S20 uses) vs third-party (more featureful;
  new dep).
- **Q-C.3 Integration with `barcada-scrape`**: where does the
  parser plug in? Pre-fetch gate vs in-flight middleware.
- **Q-C.4 Disallow handling**: skip the fetch (current S20
  cassette behavior) vs fetch-anyway-with-warning vs both
  modes (operator-tunable).
- **Q-C.5 Crawl-delay support**: honor `Crawl-delay` directive
  vs ignore (S20 cassette gate ignores).
- **Q-C.6 Test corpus**: synthetic robots.txt fixtures vs the
  S20 cassette corpus (every cassette has a real robots.txt
  fetch implicit in its recording).

### If Candidate D (Phase 4 PR-D tooling)

- **Q-D.1 Tooling shape**: batch validators / import scripts /
  hygiene tools. Operator-led design.

### If Candidate E (cassette corpus expansion)

- **Q-E.1 Target count**: 30 (plan's upper bound) vs 25 vs
  stay at 20.
- **Q-E.2 Subset focus**: bot-blocked (exercise recover-bot-
  blocked) vs non-English (exercise PR-H English-alternative
  fetch) vs more business-classification-interesting domains.
- **Q-E.3 FP re-investigation**: re-record archive.org +
  hashicorp.com under a different UA to test the SaaS-shell-FP
  hypothesis OR drop them OR keep as-is with documented
  caveat.

### Shared sub-questions (all candidates)

- **Q-SHARED.1 Commit shape**: per-module (S18+19+20 default;
  Recommended) vs per-sub-surface bundled.

(Tag-at-close is resolved at Phase 1 Sub-question 1.TAG; Phase 5
reads that resolution directly without re-decision.)

---

## Phase 3 — Implementation (per-module commits, strict order)

Per Phase 2 commit-shape decision. Default = per-module. Each
commit must satisfy the 6-step per-commit checkpoint protocol
below.

### Non-interleaving rule (CRITICAL for bisectability)

If the chosen candidate has multiple sub-surfaces (e.g.,
Candidate A drift CLI + drift tests + drift integration), do
NOT interleave. Complete each sub-surface fully before starting
the next. Per S20 precedent: cassettes (4 commits) → canary
(4 commits). NOT cassette-1 → canary-1 → cassette-2 → …

If a mid-sub-surface dependency on the other sub-surface emerges,
HALT and surface as a design-gate sub-question before continuing
— the dependency may indicate a Phase 2 question was missed.

### Per-commit checkpoint protocol (single source of truth)

At EVERY Phase 3 commit boundary, run these 6 steps IN ORDER:

**1. Combined suite**

```
.venv/bin/python -m pytest \
    tests/scraper/test_fixture_conformance.py \
    tests/runners/fixture_cascade/ \
    tests/baseline_v0/ \
    tests/synthetic_crawl/ \
    <new S21 test paths if any> -q
```

Expected: previous_baseline + N new tests, all passing. If
failing tests are NOT a deliberate consequence of the surface-
under-test → HALT.

**2. Ruff sanity (touched files only) + mid-implementation
format-check per LESSONS**

```
.venv/bin/ruff check <touched paths>
.venv/bin/ruff format --check <touched paths>
```

If unclean → run `ruff format <touched paths>` and re-test;
fold the format-fix into the commit (per S19+S20 pattern).
This is the LESSONS "Mid-implementation ruff format-check"
discipline applied to every Edit, not just pre-push.

**3. Verification table (build in chat per `[[double-check-
before-commit]]` strict rule)**

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
`src/barcada_scraper/` changes. Operator-side `eval_data/`
README + TAXONOMY_GAP_LOG + stage1_labels modifications are
expected to stay unstaged across sessions (Sessions 8-20
precedent).

**5. "Confirm to commit?" presented to operator**

Include in chat:
- Verification table from step 3
- Commit message file location (`/tmp/<id>-msg.txt`)
- File list to stage (M / A / D)

**6. After operator confirms**

Stage + commit + verify the new SHA landed (`git log --oneline -1`)
+ verify combined suite still passes on the new HEAD (re-run
step 1 once if there's any doubt; otherwise trust the pre-commit
run since file state hasn't changed).

This 6-step protocol applies UNIFORMLY to every commit in Phase
3 (and Phase 6's workspace close-out commit). Mechanical; do not
skip steps.

### Cumulative test-count gate

Track combined-suite passing count at each commit boundary:

```
Phase 3 start                  : 388  (Session 20 close baseline)
After commit 1                 : >= 388 + N_commit_1_tests
After commit 2                 : >= 388 + N_commit_1_tests + N_commit_2_tests
...
```

**Rule**: the count NEVER decreases between checkpoints. A
decrease means a previously-passing test went red — regression.
HALT.

---

## Phase 4 — Pre-push gate (whole-tree)

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 341+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

HALT IF any gate red. Never use `--no-verify`.

### eval_data WIP halt protocol (per LESSONS)

validate_consistency runs against working-tree state. operator-
WIP edits to `eval_data/*.jsonl` can introduce schema violations
that fail the gate even though no S21 commit touches eval_data.

When this fires:
1. Confirm the failing row's content is in operator-WIP
   (`git diff eval_data/...`), not in committed HEAD
   (`git show HEAD:eval_data/...`).
2. Confirm the S21 commits do not touch eval_data
   (`git diff origin/main..HEAD -- eval_data/`).
3. Surface to operator with the exact row + reason + diff vs
   committed state.
4. Two paths: (a) operator-fix in WT, then re-run gate;
   (b) stash eval_data WIP, push, restore.
5. Do NOT auto-fix locked-artifact content.

S20 precedent: operator chose (a). Patterns codified in
LESSONS "Pre-push gate against operator-WIP territory".

---

## Phase 5 — Push + tag

- Push to `origin/main` after operator confirms.
- Tag per Phase 1 Sub-question 1.TAG decision (or defer).

If `workstream-0-end` is placed (Candidate B closes Workstream
0): include annotated message summarizing all W0 weeks
(W1-W4, W4.1.5, W4.3, W5, W6, W7 + the per-tier cost-accounting
closure).

---

## Phase 6 — Workspace close-out

- Append Session 21 entry to `~/crawler-audit/SESSION_LOG.md`
  (Sessions 13-20 precedent format).
- Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md` for
  Session 22.
- Update `~/crawler-audit/LESSONS.md` with any new forward-
  applicable patterns surfaced this session.
- Single workspace commit at session close. Push workspace
  after operator confirms.

---

## Acceptance criteria

**Per candidate (reduces if Phase 1 narrows scope):**

### Candidate A (barcada-drift)

1. `barcada-drift` CLI (or `barcada-baseline drift` per Q-A.1)
   works against ≥2 canary_runs parquets.
2. Drift metric per Q-A.2 implemented + tested.
3. Alert threshold per Q-A.3 implemented + tested.
4. Output shape per Q-A.5 documented + tested.

### Candidate B (per-tier cost-accounting retrofit)

1. Per-tier cost fields populated per Q-B.1 scope.
2. Backfill behavior per Q-B.2 executed.
3. Test coverage per Q-B.3 in place.
4. `workstream-0-end` tag placed if per-tier accounting fully
   closes the gap (Q-B.5).

### Candidate C (W A.1 robots.txt parser)

Items 1-3 are unconditional. Item 4 is conditional on the
Sub-question 1.C-SCOPE pinning at Phase 1.

1. Production robots parser ships under chosen namespace.
2. Crawl-delay handling per Q-C.5.
3. Test corpus per Q-C.6.
4. **If Sub-question 1.C-SCOPE = Full-W8**: integration with
   `barcada-scrape`'s fetcher seam per Q-C.3 ships this session.
   **If 1.C-SCOPE = Parser-only**: integration deferral is
   explicitly documented in the SESSION_LOG.md Session 21 entry
   as a Session 22+ carry-forward; acceptance item 4 is
   considered satisfied by the documented deferral.

### Candidate D (Phase 4 PR-D tooling)

1. Tooling shape per Q-D.1.

### Candidate E (cassette corpus expansion)

1. Cassette count grows to Q-E.1 target.
2. FP re-investigation per Q-E.3 if applicable.

### Shared (all candidates)

5. Combined suite at session close: existing 388 baseline + N
   new tests, all passing.
6. Pre-push gate runs green (incl. eval_data WIP halt protocol
   applied if needed).
7. Tag placed per Phase 1 Sub-question 1.TAG OR explicit defer.
8. Regression-protection checklist held:
   - 30 check-surface tests (24 test_check + 6 test_cli check-
     dispatch) stay 30/30 green.
   - 23 canary-surface tests (17 test_canary + 6 test_cli
     canary-dispatch) stay 23/23 green.
   - 33 cassettes-surface tests in tests/synthetic_crawl/ stay
     33/33 green.
   - 20 cassettes + 20 sidecars at tests/fixtures/synthetic_
     crawls/ unmodified.
   - tools/baseline_v0/check.py / generate.py / determinism.py
     / canary.py unmodified.
   - tools/synthetic_crawl/ package unmodified.
   - scripts/launchd/ unmodified.
   - tests/runners/fixture_cascade/ unmodified (except via W5.X-
     prefix commit per Candidate B's explicit auth).
   - tests/fixtures/baseline-v0/ snapshot unmodified.
   - src/barcada_scraper/ unmodified (except via Phase 2 design-
     gate auth for a specific module).

---

## Out-of-scope (no exceptions without operator authorization)

Per the regression-protection checklist:

**S19 deliverables (Sessions 19 check sub-surface):**
- `tools/baseline_v0/check.py`
- `tests/baseline_v0/test_check.py` (24 tests)
- 6 check-dispatch tests in `tests/baseline_v0/test_cli.py`

**S20 deliverables (Sessions 20 cassettes + canary sub-surfaces):**
- `tools/synthetic_crawl/` package (4 files: __init__.py,
  __main__.py, cli.py, recorder.py)
- `tools/baseline_v0/canary.py`
- `canary-run` subparser additions in `tools/baseline_v0/cli.py`
- `tests/synthetic_crawl/` package (3 files: __init__.py,
  test_cli.py, test_recorder.py; 33 tests)
- `tests/baseline_v0/test_canary.py` (17 tests)
- 6 canary-dispatch tests in `tests/baseline_v0/test_cli.py`
- `tests/fixtures/synthetic_crawls/` (40 files: 20 cassette.yaml
  + 20 extract_hard_exclusions.json)
- `scripts/launchd/` (5 files: plist template + install/uninstall
  scripts + wrapper + README)
- `pyproject.toml` vcrpy>=8.1 entry in dev extras
- `.gitignore` canary_runs/ entry

**W4.1.5 driver orchestration (locked since W4.1.5 close):**
- `tests/runners/fixture_cascade/` (except via W5.X-prefix
  commit with explicit operator auth — only Candidate B opens
  this with Q-B.4 W5.X-prefix decision)

**Baseline-v0 ground truth:**
- The committed `tests/fixtures/baseline-v0/` snapshot at
  `9e9a1fb` (1213 files)

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
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` (READ-ONLY per §14)
- `CLASSIFICATION_ADJACENT_PLAN.md` (UPDATED only when AI/ML
  decisions land)
- `RECONCILIATION_2026-05-21.md`
- `docs/phase4_implementation_plan.md` (Phase 4 governance
  reference; not modified until Phase 4 work is operator-
  authorized)

**Operator-owned territory:**
- All of `eval_data/` — labeling-workstream territory; per-row
  WIP edits across sessions are expected and unstaged

**Production code:**
- `src/barcada_scraper/` — locked unless Phase 2 design-gate
  explicitly authorizes a specific module

**Pipeline configs:**
- `configs/`

**Phase 4 work:**
- Phase 4 PR-D/E/F/G work opens only when Workstream 0 fully
  closes AND operator-led Stage 2/3 labeling work begins

---

## Verify-before-asking discipline (strict rule from S19+S20)

Per `[[double-check-before-commit]]` memory (operator-codified
S19; re-confirmed S20): **ALWAYS verify every concrete claim in
the commit message against actual source/output BEFORE staging.**
Fixture names, file counts, exit codes, line counts, test counts,
helper names, smoke outcomes, SHA prefixes, regex matches. No
claims by pattern-completion. Build a verification table in chat
(claim → reality → status) and reconcile before "Confirm to
commit?".

Specific to S21:

- Before each chosen-candidate-specific claim in a commit
  message, verify against the actual source / runtime output:
  per-domain agreement values (Candidate A); cost-journal field
  presence (Candidate B); robots parser output (Candidate C);
  cassette counts (Candidate E).
- Before claiming combined suite count, re-run pytest.
- Before claiming ruff/format clean, re-run ruff against the
  touched files.
- Before claiming a SHA prefix in a commit message body
  (e.g., "matches W4.1.5 commit 521e363"), verify the prefix
  is correct via `git show --no-patch --format=%h <ref>`.

Avoid bash pipe artifacts that mask Python exit codes
(LESSONS): `python_cmd 2>&1 | grep ... | tail` makes `$?`
reflect tail's exit. Use `> stdout.out 2> stderr.err; echo $?`
or `${PIPESTATUS[0]}` when exit-code matters.

---

## Commit hygiene (per LESSONS + S19/S20 additions)

- File-based commit messages at `/tmp/<id>-msg.txt`.
- Per-module commits (Phase 3 commit shape unless Q-SHARED.1
  overrides).
- "Confirm to commit?" before EVERY commit. Pair with
  verification table (always) and `git diff --staged` (when
  appropriate per `[[double-check-before-commit]]` triggers).
- Commit body includes: action ref (e.g.,
  `WA0.W7.cost-accounting-retrofit` for Candidate B), scope
  summary, file touches, test count delta, plan reference. NO
  `Co-Authored-By`.
- Pre-push gate must run green. Never use `--no-verify`.
- Pre-push vermin: `git ls-files '*.py' | xargs vermin
  --target=3.10` to filter venv-internal pytest 3.14 false-
  positives.
- Mid-implementation ruff format-check, not only pre-push (S19
  finding; reinforced S20).
- Sibling-module style consistency for one-file additions —
  match the immediate sibling's conventions even where they
  technically violate project-wide rules; disclose explicitly.
- Workspace close-out (Phase 6) lands as its own commit at
  session close.

---

## Context-window awareness

S20 ran cleanly within window with 8 repo commits + 1 tag +
1 workspace commit. S21 budget similar.

Strategies:

- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore
  subagent if any module audit requires reading >3 files.
- For any live-HTTP corpus work (Candidate E), pilot with 1-3
  cassettes first per S18+S20 staged-rollout pattern.

Self-monitor cadence:

- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before the chosen S21 scope closes,
  transition per "no mid-commit-batch transitions" — finish
  in-flight sub-surface, then close session and refill the
  transition template for Session 22.

---

## Reporting in chat at session close

After all Session 21 commits land + push + close-out per the
S13-20 pattern:

1. Commit SHA(s) of each S21 sub-surface.
2. Sub-surface(s) landed (per candidate).
3. Test count delta: 388 baseline → S21 close.
4. Driver suite count at S21 close (46/46 expected unless
   Candidate B W5.X-prefix realigned).
5. Files touched per sub-surface.
6. Tag dispositions (incl. `workstream-0-end` if Candidate B
   closed it).
7. Per-tier cost-accounting wiring gap disposition: patched
   (Candidate B) or carry-forward.
8. Any spend (LLM, infrastructure, cassette-capture).
9. Robots.txt compliance log (if Candidate C did live work).
10. FP-curation log update (if Candidate E expanded the
    cassette corpus).
11. Verify-before-asking summary: any source-verification
    findings surfaced.
12. Outstanding items for Session 22.
13. Tags state at S21 close.

Do not propose Phase 4 PR-D/E/F/G work this session unless
Candidate D was chosen and operator-led labeling is in flight.

---

## Carry-forward from S20 amendments (baked into this prompt)

The 3 amendments S20 carried forward have been folded directly
in here, so S21 does not need a separate amendment file:

- **MF-1** (driver_sha prefix-match): Step 0.6 above already
  asserts `m['driver_sha'].startswith('521e363')` rather than
  the full 40-char hash.
- **MF-2** (Q1.1 option B wording cleanup): obsolete; Q1.1 is
  not in S21 scope. Filed.
- **SR-8** (Phase 1 HALT condition tightening): Phase 1
  Candidate A above explicitly scopes the HALT to "AI/ML
  decisions not pre-resolved AND no operator-authorized
  placeholders." Other candidates do not block on AI/ML.

If new amendments arise pre-S21 open, walk them per the
reviewer-feedback hygiene pattern in this prompt's "Reviewer-
feedback hygiene" section.
