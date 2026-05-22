# Session Transition Template — Handoff from Session 18 → Session 19

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-18 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

---

## Handoff metadata

- Outgoing session number: 18
- Closing date: 2026-05-22
- Outgoing session scope: W A.0 W6 baseline-v0 CLI scaffolding. Built
  `tools/baseline_v0/` as a thin wrapper over the W4.1.5 cascade
  driver; landed the Hybrid 3-pair baseline-v0 snapshot across 202
  single-page fixtures (multipage_boilerplate skipped per Session 17
  Option-3); placed annotated tag `baseline-v0` at the W6 close
  commit. 5 repo commits + 1 workspace commit. LLM spend: $0.447
  total (two captures during Step D; bug fix between them).
- Reason for transition: W A.0 W6 fully closed. Session 19 picks up
  W A.0 W7 synthetic-crawl-tape capture + canary wiring per plan
  §4 W7. May also extend `barcada-baseline` with the `check`
  subcommand at the W6-W7 boundary (deferred from Session 18
  design-gate Q3).

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `9e9a1fb` (WA0.W6.baseline-v0-capture).
- Last commit subject: "WA0.W6.baseline-v0-capture: 202-fixture
  parallel snapshot at tests/fixtures/baseline-v0/"
- Branch sync with `origin/main`: 0 commits ahead, 0 commits behind
  (verified at Session 18 close after push).
- Tags (do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3`
  - `workstream-0-week1-end` at `4f9d23f`
  - `workstream-0-week2-end` at `e5d2f91`
  - `workstream-0-week3-end` at `cf0c14c`
  - `workstream-0-week4-1-5-end` at `dd64963` (annotated `f9be833a`)
  - `workstream-0-week4-end` at `b2e2671` (annotated `c3c6fb74`)
  - `workstream-0-week5-end` at `ddd3cb0` (annotated `fc1ae2ff`,
    placed Session 16). Disposition deferred at Sessions 17-18.
  - `baseline-v0` at `9e9a1fb` (NEW Session 18; annotated `7839c164`).
- Pre-push gate state at HEAD `9e9a1fb`: ALL CHECKS PASS (ruff +
  ruff format + vermin 3.10 target + validate_consistency).
- Unstaged changes intentionally ignored across sessions (operator-
  side work in the locked tree):
    eval_data/README.md
    eval_data/TAXONOMY_GAP_LOG.md
    eval_data/stage1_labels.jsonl
  Routinely unstaged through Sessions 8-18.
- Corpus: 222 .html fixtures (unchanged from Session 17 close).
- 202 expected.json files (UNCHANGED — baseline-v0 supersession is
  consumer-level only; W4.3.D conformance keeps reading these until
  explicit migration at W7 or Phase 4 PR-E).
- 222 meta.json files (unchanged).
- NEW: tests/fixtures/baseline-v0/ subtree with 1213 files (202
  fixtures × 6 components + 1 manifest.json), ~6.4 MB.
- NEW: tools/baseline_v0/ namespace package (CLI module).
- NEW: tests/baseline_v0/ test module (46 tests).
- Combined test suite at HEAD `9e9a1fb`: 302 passed / 0 failed / 0
  skipped (210 conformance + 46 driver + 46 baseline_v0).

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 18 start: `f8b3995` (Session 17 close-out).
- Session 18 workspace commit: SESSION_LOG.md Session 18 append +
  this template refill (single workspace commit at session close).
- Branch sync with `origin/main`: depends on whether the close-out
  workspace commit is pushed (Session 13-17 precedent: pushed).

---

## Active task list

The Session 18 task list (Step A → cli-skeleton → generate +
determinism → tests → fix-nested-category → baseline-v0 capture →
pre-push gate → push → tag → close-out) is fully complete. W A.0 W6
substantively closed.

Suggested Session 19 tasks:

- **W A.0 W7 synthetic-crawl-tape capture** (plan §4 W7).

  For ~20-30 representative domains beyond the fixture corpus:
  use `vcrpy` (or similar) to record full HTTP exchanges (request +
  response + headers + timing), save cassettes per domain to
  `tests/fixtures/synthetic_crawls/<domain>/`, and capture baseline
  outcomes per domain (Stage 1 decision, costs, schema, errors).
  This tests interactions between components that fixture-level
  tests miss.

- **W A.0 W7 canary wiring** (plan §4 W7).

  Wire the unused `canary_50_domains.txt` to a scheduled job. Run
  weekly. Build a small trend dashboard showing per-domain
  agreement with last baseline run, cost per domain over time,
  anti-bot success rate.

- **`barcada-baseline check` subcommand** (carry-forward from
  Session 18 design-gate Q3; W6-W7 boundary).

  Extend the CLI with `barcada-baseline check --fixtures
  tests/fixtures/html/ --baseline tests/fixtures/baseline-v0/`.
  Reuse the generate pipeline but compare per-component hashes
  against the committed baseline-v0 manifest. Exit 0 on match,
  exit non-zero with diff summary on mismatch. Pairs with the
  Phase 4 PR-E CI-gate wiring downstream.

  **Session 19 Step A design-gate elicitation** (suggested if W7 is
  decomposed):
  1. Ordering: ship `check` first (small surface, can land in 1 day)
     vs synthetic crawl tapes first (larger surface, tooling
     selection decision) vs both in parallel.
  2. vcrpy vs alternative (e.g. mitmproxy export, custom cassette
     format). vcrpy is the plan's named choice; alternatives need
     justification.
  3. Synthetic-crawl-tape corpus scope: which 20-30 domains? Reuse
     canary_50_domains.txt subset, or a fresh list?
  4. Canary scheduler: GitHub Actions cron, cron daemon, or
     operator-driven manual run for now?

- **Phase 4 PR-E CI-gate wiring (forward look; NOT Session 19
  scope per the W6 → W7 sequence unless operator explicitly opens
  it).** Pre-requisite: W A.0 W7 close.

Task state is session-local in Claude Code; it does NOT carry across
sessions. Session 19 should TaskCreate fresh tasks on open.

---

## Outstanding operator-input requests entering Session 19

**Material item — workstream-0-week5-end tag disposition (deferred
again at Session 18 Step F)**: The annotated tag remains at `ddd3cb0`
(Session 16 close), placed BEFORE the multipage_boilerplate closure
(Session 17 at `e060e5f`). Operator chose `Defer (recommended)` at
Session 18; the future workstream-0-end tag (placed after W A.0 W7
closes) would supersede.

**Material item — per-tier cost-accounting wiring gap (W4.3.X
candidate, driver-locked)**: Carried forward from Session 14 surface
+ Sessions 15-18 deferred. W4.1.5 driver's cost-journal `totals.
stage{1_llm,1_embedding,...}_usd` fields not incremented; per-row
`stage3_decision.evidence_cost_usd` is $0; total cost telemetry
is intact. Driver-locked at `dd64963`. Session 18 disposition:
DEFERRED (no operator request; baseline-v0 capture didn't need
per-tier extrapolation). Severity: LOW. May surface in W A.0 W7 if
the synthetic-crawl-tape cost-shape comparison needs per-tier
accounting.

**Material item — `barcada-baseline check` subcommand design**: see
suggested Session 19 task above. Deferred from Session 18 Step A
design-gate Q3 ("generate only at W6").

**No other gates** between Session 19 open and W A.0 W7 work.

---

## Operator decisions made during Session 18 (cross-ref to SESSION_LOG.md)

1. **Output shape: Hybrid 3-pair** (parser_output + barriers_verdict
   + stage_decisions, each with .hash sibling). Not the plan-
   faithful 6-file shape (text_extraction + link_discovery deferred).
2. **CLI placement: tools/baseline_v0/** (namespace package; no
   src/barcada_scraper/ surface change).
3. **Subcommand surface at W6: generate only** (`check` deferred).
4. **Multipage_boilerplate: Skip entirely** (Session 17 Option-3
   carry-forward; manifest documents the skip).
5. **Output location: tests/fixtures/baseline-v0/** (parallel
   subtree; existing expected/<domain>.json files untouched).
6. **baseline-v0 tag: At W6 close** (placed at 9e9a1fb).
7. **Schema definition: Implicit / freeform** (no
   baseline-v0.schema.json yet; defer formalization to W7+).
8. **Commit shape: Per-module** (4 W6 commits + 1 fix commit).
9. **LLM mode: real** (Azure OpenAI; $0.211 total for the
   committed capture).
10. **Step F (workstream-0-week5-end disposition): Defer**
    (carry-forward from Session 17).

---

## Pattern note for Session 19 (W A.0 W7)

- **Combined-suite verification at every commit boundary** (NEW
  Session 16 pattern, re-confirmed Sessions 17 and 18). Run BOTH
  driver suite + conformance suite + baseline_v0 suite at every
  fixture-affecting or CLI-affecting commit. Worth ~45-50s of test
  runtime per commit to avoid multi-commit verify-after-the-fact
  reconciliation.

- **Plan-spec interpretation room** (NEW Session 18 finding):
  plan §4 prose may diverge from the runtime code's surface shape
  in ways that need a design-gate AskUserQuestion before
  implementation. For W A.0 W7, the vcrpy cassette format vs
  synthetic-crawl-tape semantics likely needs the same treatment.

- **Background process + harness notification** (NEW Session 18
  finding): long-running cascade or capture runs (~10-15 min wall
  time at 202 fixtures real mode) fit Bash run_in_background
  cleanly. The harness notifies on completion without polling.

- **Safety hook blocks destructive ops on untracked dirs**
  (Session 18 finding): the project's safety-check.sh blocks
  `rm -rf` even on untracked fixture output dirs. Workaround: ask
  the operator to execute `! rm -rf <path>` in the chat (the `!`
  prefix executes inline). Don't bury in tool error retry.

- **Wrapper-level filtering vs cascade-level** (NEW Session 18
  finding): when wrapping the cascade, compute the in-scope fixture
  list path-aware at the wrapper, then pass stems as cascade's
  `fixture_filter` with `max_fixtures=None`. The wrapper owns the
  "what's in scope" decision; the cascade handles "process these
  specific stems".

- **Pricing-as-consistent-failure pattern** (Session 17 finding):
  still applies for any future fixture sourcing — default
  synthetic-with-real-markers for pricing pages.

- **Markdown-render NBSP corruption avoidance** (Session 17
  finding): when shell commands have numeric flag arguments or
  whitespace-sensitive syntax, write to /tmp/ via Write tool and
  run via `bash /tmp/script.sh`. Avoid copy-pasting curl commands
  through markdown rendering.

- **Verify-before-asking discipline extension** (Sessions 12, 16,
  17, 18): when operator references a SHA, file shape, fixture
  state, or prompt-prescribed layout, verify against current repo
  state BEFORE acting. Session 18 surfaced the plan-§4-W6-vs-
  cascade-output-shape mismatch via this discipline.

- **Sub-agent delegation for analysis-heavy work**: Session 18
  used Explore subagent for cold-start required reading +
  source-verification of cascade.py/consolidate.py/cli.py/
  fixture_fetcher.py in one consolidated brief. Forward-applicable
  for any session requiring multi-file/source-tree analysis before
  design decisions.

- **Per-domain or per-subsurface decomposition with operator
  approval gates** (Sessions 6, 11, 16, 17, 18 pattern). For
  Session 19's W A.0 W7 work, per-subsurface commits (e.g.
  `WA0.W7.check`, `WA0.W7.vcrpy-driver`, `WA0.W7.canary-wiring`)
  is the natural shape.

- **Confirm-to-commit gating** before every commit (LESSONS anchor
  pattern; Sessions 4-18).

- **File-based commit messages** at /tmp/<id>-msg.txt; no
  Co-Authored-By.

- **Pre-push gate** must run green; never use `--no-verify`. Use
  `git ls-files '*.py' | xargs vermin --target=3.10` (not bare
  `vermin .`) to avoid venv-internal pytest 3.14 false-positives.

- **Driver-locked policy continues** at `dd64963`. Driver TEST
  files may be realigned via W5.X-prefix commits per Session 16
  precedent. Session 18 did not need a driver-test realign.

- **Conformance count discipline**: W A.0 W6 close at 302 combined
  (210 conformance + 46 driver + 46 baseline_v0). Any new reds in
  Session 19 should be either (a) deliberate (new W7 surface
  exposed issue) or (b) immediately investigated.

---

## Locked artifacts reminder (CRITICAL — do not modify)

- All of `eval_data/` — locked. Read-only context only.
- `stage1.schema.json` v1.0 / 49 keywords — locked.
- All Workstream 0 + baseline-v0 tags — locked (pre-remediation-
  2026-05-19 + workstream-0-week{1,2,3,4-1-5,4,5}-end +
  baseline-v0).
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` — read-only since Session
  12 absorption.
- `tests/fixtures/META_SCHEMA.md` + `meta.schema.json` v1.0 +
  `expected.schema.json` v1.1 — locked at W4.3 close (Session 15
  commit `7728bdf`). Further bumps require operator authorization.
- W4.2 expected.json files at `cc2ba2c` + Session 16 W5 additions
  at `ddd3cb0` — valid until W A.0 W7 / Phase 4 PR-E consumer-side
  migration supersedes per output durability constraint.
- W4.1.5 driver at `tests/runners/fixture_cascade/` locked at
  `dd64963`. Driver TEST files may be realigned via W5.X-prefix
  commits per Session 16 precedent.
- `tests/scraper/test_fixture_conformance.py` — extended Session 17
  (5 new test_multipage_boilerplate_<domain>_conformance functions
  + COVERED update). W4.3.D helpers (_HARD_EXCLUSION_KEYS /
  _expected_parser_output / _block) unchanged.
- `docs/phase4_implementation_plan.md` — governance reference; do
  NOT modify until Phase 4 PR-D/E/F/G is operator-authorized.
- `~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md` —
  workspace design-of-record; read-only.
- `~/crawler-audit/RECONCILIATION_2026-05-21.md` — archival
  historical record; do not edit.
- NEW: `tests/fixtures/baseline-v0/` subtree — locked at Session 18
  close (9e9a1fb). Future regenerations may overwrite, but the
  current snapshot is the canonical W6 baseline-v0 capture and
  should not be edited piecemeal.
- NEW: `tools/baseline_v0/` CLI module — production-style code
  surface; Session 19 may extend (e.g. add `check` subcommand)
  but should not refactor the existing surfaces without operator
  authorization.

---

## Next concrete work unit

- **Action ID:** **W A.0 W7 synthetic-crawl-tape capture + canary
  wiring** (plan §4 W7).
- **Scope:** vcrpy or alternative cassette-recording tool for ~20-30
  representative domains beyond the fixture corpus; cassettes per
  domain at `tests/fixtures/synthetic_crawls/<domain>/`. Capture
  baseline outcomes per domain. Canary scheduler wiring for
  `canary_50_domains.txt`. May also extend `barcada-baseline check`
  subcommand at the W6-W7 boundary.
- **Acceptance:** synthetic-crawl-tape cassettes recorded and
  replayable; canary scheduler runs against the unused
  canary_50_domains.txt; (if check is in scope) `barcada-baseline
  check` works against the baseline-v0 manifest, exit codes
  correctly indicate match/mismatch.
- **Files expected to be touched:**
  - New module(s) under `tools/baseline_v0/` (if check lands here)
    or a new module like `tools/synthetic_crawl/` for the cassette
    driver.
  - Tests under `tests/baseline_v0/` (for check) and/or
    `tests/synthetic_crawl/`.
  - New cassette files under `tests/fixtures/synthetic_crawls/`.
  - Canary scheduler config (GitHub Actions workflow file?).
- **Files NOT to be touched:**
  - All locked artifacts listed above.
  - The 222 existing .html fixtures (corpus stable).
  - The committed baseline-v0/ snapshot at 9e9a1fb (regenerations
    may overwrite, but not piecemeal-edit).
  - W4.1.5 driver internals (cli.py, cascade.py, parser_compose.py,
    consolidate.py, fixture_fetcher.py main code) — locked per
    W4.1.5 policy.
  - Production code under `src/barcada_scraper/` unless explicitly
    authorized at Session 19 design-gate.

After W A.0 W7 closes (1-2 sessions), Workstream 0 is fully done
and Workstream A (Compliance Foundation, plan §5) opens.

---

## Required reading (Session 19 first 10 minutes)

In this order:

1. **This file** (you're reading it).
2. **`SESSION_LOG.md` Session 18 entry** — what landed during W6
   baseline-v0 scaffolding (Hybrid output shape; tools/baseline_v0/
   namespace package; nested-category bug + fix; full 202-fixture
   capture in real mode; baseline-v0 tag at 9e9a1fb).
3. **`LESSONS.md`** — operator patterns and observed conventions.
   Session 18 forward-applicable findings to fold into LESSONS:
   plan-spec interpretation room, background-process notification,
   safety-hook destructive-op workaround, manifest in-place refresh
   vs full re-run, wrapper-level vs cascade-level filtering.
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §4 Week 7** (W A.0 W7
   synthetic crawl tapes + canary wiring spec).
5. **`tools/baseline_v0/`** at HEAD `9e9a1fb` — the CLI module that
   W7's `check` subcommand (if in scope) extends.
6. **`tests/fixtures/baseline-v0/manifest.json`** at HEAD `9e9a1fb`
   — the manifest format the `check` subcommand reads.

After reading, verify repo state:

```
git -C /Users/administrator/projects/barcada-scraper status
git -C /Users/administrator/projects/barcada-scraper log --oneline -6
git -C /Users/administrator/projects/barcada-scraper tag -l
find /Users/administrator/projects/barcada-scraper/tests/fixtures/html -name '*.html' -type f | wc -l
find /Users/administrator/projects/barcada-scraper/tests/fixtures/baseline-v0 -type f | wc -l
.venv/bin/python -m pytest tests/scraper/test_fixture_conformance.py tests/runners/fixture_cascade/ tests/baseline_v0/ -q
```

Expected:
- Last commit SHA: `9e9a1fb` (WA0.W6.baseline-v0-capture).
- Tags include `baseline-v0` at 9e9a1fb (annotated 7839c164).
- 222 .html files.
- 1213 baseline-v0 files (202 fixtures × 6 components + manifest).
- Combined suite: 302 passed / 0 failed / 0 skipped.
- 0 ahead / 0 behind origin/main.
- Only operator-side eval_data/ files showing as unstaged.

If anything differs, surface to operator before doing work.

Then open W A.0 W7 design discussion: cassette tool (vcrpy vs
alternative), corpus scope (which 20-30 domains), canary scheduler,
whether to bundle `check` subcommand at the W6-W7 boundary or land
it as a separate sub-surface. Likely present via AskUserQuestion as
the first design-gate question after Session 19 cold-start.

---

## Risk register state (plan §11)

No new risks escalated and unresolved by Session 18.

Forward-applicable entries:

- "Recapture tooling needs retry policy" — STILL applies.
- "Phase 4 measurement half blocked on operator-led labeling" —
  STILL applies.
- "Cost-journal per-tier accounting gap" (Session 14 surface) —
  STILL applies. Session 18 disposition: DEFERRED. Severity: LOW.
- "W4.2 expected-output lifetime constrained" — RESOLVED at
  Session 18 close. baseline-v0 supersedes (consumer-level) at the
  9e9a1fb tag. The existing expected.json files remain in place
  per the parallel-subtree design; W4.3.D conformance still reads
  them. Full file-system supersession happens at W A.0 W7 / Phase 4
  PR-E consumer migration.

NEW Session 18 risk-register additions (low-severity):

- "baseline-v0 metadata field freshness": the manifest's driver_sha
  + generated_at can drift if downstream regeneration runs against
  a later HEAD. Session 18 used an in-place manifest refresh
  pattern to keep these accurate; document this in future
  re-capture playbooks.
- "Wrapper enumeration must match source-tree depth": Session 18's
  `_enumerate_single_page_fixtures` initially assumed depth-2 flat
  layout; failed on the 3 depth-3 `international_business/<locale>/`
  fixtures. Future fixture-walking code should default to relative-
  path-based category attribution.

LLM cost drift risk (plan §11) — Session 18 update:
- Session 18 incurred $0.447 total (two captures during Step D).
- Cost incurred Sessions 1-18: $0.263658 + $0.447 = $0.711.
- Cost budget remaining: $99.29.
- W A.0 W7 estimated cost depends on cassette-capture strategy.
  Recording-mode vcrpy invocations call live endpoints once per
  cassette; replay-mode is free. Rough estimate: $0.01-$0.10 per
  cassette × 20-30 cassettes = $0.20-$3.00 total. Stop and escalate
  if actual spend trends >3× original $1.00 ballpark.

---

## Deferred prose-only fixes register

**Status at Session 18 close: EMPTY.** No new prose-only fixes
surfaced in Session 18.

Future deferred prose-only fixes (if any surface in Session 19+)
should be tracked here per the LESSONS.md "Defer prose-only schema
fixes; bump only when machine schema changes" pattern.

---

## Cost & schedule tracking

- Cost ceiling: $100 (operator-set 2026-05-19, alert at $50).
- Cost incurred Sessions 1-18: $0.711.
- Cost budget remaining: $99.29.
- Session 18 actual spend: $0.447 (two captures during Step D).
- W A.0 W7 estimated spend: $0.20-$3.00 (cassette recording mode
  for 20-30 domains; replay is free).
- Schedule: 7 weeks elapsed of Workstream 0's 5-week budget
  (Workstream A.0 extends Workstream 0 by 2 weeks). W A.0 W6 fully
  closed this session. Session 19 opens W A.0 W7 (final
  Workstream 0 sub-task).

---

## Notes for Session 19

- **Conformance test red count entering Session 19: 0** (W6
  cleanly closed). Any new reds in Session 19 should be immediately
  investigated.
- **0 conformance tests SKIP**.
- **File-based commit messages** still mandatory.
- **"Confirm to commit?" gating** before every commit.
- **Verify-before-asking discipline** — bidirectional. Sessions
  12, 16, 17, 18 patterns. For W A.0 W7 scaffolding, source-verify
  the chosen cassette tool's API surface BEFORE designing the
  wrapper. Re-read relevant `tools/baseline_v0/` modules at
  session-current HEAD before launching the design-gate
  AskUserQuestion.
- **Combined-suite verification at every commit boundary**
  (Sessions 16-18 pattern). Run conformance + driver + baseline_v0
  suites at every commit boundary. ~45-50s runtime.
- **Pre-push gate** at Session 18 close passed cleanly. Routinely
  passes. Never use `--no-verify`. Use `git ls-files '*.py' |
  xargs vermin --target=3.10`.
- **Plan is read-only** — never edit
  `BARCADA_CRAWLER_REMEDIATION_PLAN.md`.
- **W5.X-prefix pattern**: driver-locked test changes are
  authorized via W5.X-prefix commits per Session 16 precedent.
  Session 18 did not need a similar realign. Session 19 may
  surface a need if W7 wrapper interactions expose driver-test
  brittleness.
- **Workspace cwd**: when editing LESSONS.md / SESSION_LOG.md /
  this template, work in `/Users/administrator/crawler-audit/`.
- **W5 tag pattern**: per Sessions 17-18 operator deferrals, the
  `workstream-0-week5-end` tag remains at `ddd3cb0` (Session 16
  close). Multipage closure (Session 17, `e060e5f`) and W6 close
  (Session 18, `9e9a1fb`) NOT separately tagged with a week5
  marker. Workstream 0 NOT closed yet — W A.0 W7 follows.
- **W4.2 + W5 ground truth durability**: the cumulative
  expected.json set at `ddd3cb0` (202 files) remains valid through
  Session 18 close. baseline-v0 supersedes at the consumer level
  via the parallel-subtree design; full migration happens
  downstream.
- **baseline-v0 ground truth durability**: the snapshot at
  `9e9a1fb` is the canonical W6 capture. Future Workstream A/B/C/D
  changes may produce diffs against this baseline (per
  `barcada-baseline check`, once that subcommand lands); track
  intentional diffs as approved drift in the manifest or commit
  trail.
- **Safety hook destructive-op workaround**: the project's
  safety-check.sh blocks `rm -rf` even on untracked dirs. If a
  Session 19 step needs to clean up untracked output (e.g.
  intermediate cassette runs), ask the operator to execute
  `! rm -rf <path>` in the chat.
- **This template's structured fields will need refilling at
  Session 19 close.**
