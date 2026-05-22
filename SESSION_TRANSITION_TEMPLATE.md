# Session Transition Template — Handoff from Session 19 → Session 20

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-19 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 20 invocation prompt:** `~/crawler-audit/SESSION_20_PROMPT.md`
(finalized at Session 19 close; also at `~/Downloads/session-20-prompt.md`
for operator-invocation convenience). The prompt enforces 7-phase
strict ordering (Phase 0 cold-start verify → Phase 1 naming+scope →
Phase 2 design-gate → Phase 3 implementation → Phase 4 pre-push →
Phase 5 push+tag → Phase 6 close-out) with halt-on-mismatch
conditions at each phase. Pre-resolves 12 design-gate sub-questions
(Sub-question 1.1-1.2 + Q2.1-Q2.10) so Phase 2 elicitation is tight.

---

## Handoff metadata

- Outgoing session number: 19
- Closing date: 2026-05-22
- Outgoing session scope: W A.0 W7 baseline-v0 `check` sub-surface
  (W6-W7 boundary deliverable, carried forward from Session 18
  design-gate Q3). Cassettes + canary (the other two W7 sub-surfaces
  per plan §4 W7) were intentionally deferred at Session 19 Step A
  scope so their design surfaces (cassette tool, capture mode,
  robots.txt compliance, FP-aware corpus, determinism gate;
  barcada-drift naming) get their own session prompts. 3 repo
  commits + 1 workspace commit. LLM spend: $0 (integration tests
  use fake-mode generate; no real-mode cascade runs).
- Reason for transition: `check` sub-surface fully closed. Session 20
  picks up the remaining W A.0 W7 sub-surfaces: synthetic-crawl-tape
  capture and canary wiring. The Session 20 prompt should fold in the
  5 valid completeness items from the Session 19 reviewer-feedback
  review (see "Notes for Session 20" below).

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `467647e` (WA0.W7.check-tests).
- Last commit subject: "WA0.W7.check-tests: tests/baseline_v0/
  test_check.py + dispatch tests"
- Branch sync with `origin/main`: 0 commits ahead, 0 commits behind
  (verified at Session 19 close after push).
- Tags (do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3`
  - `workstream-0-week1-end` at `4f9d23f`
  - `workstream-0-week2-end` at `e5d2f91`
  - `workstream-0-week3-end` at `cf0c14c`
  - `workstream-0-week4-1-5-end` at `dd64963` (annotated `f9be833a`)
  - `workstream-0-week4-end` at `b2e2671` (annotated `c3c6fb74`)
  - `workstream-0-week5-end` at `ddd3cb0` (annotated `fc1ae2ff`,
    placed Session 16). Disposition deferred at Sessions 17, 18, 19.
  - `baseline-v0` at `9e9a1fb` (Session 18; annotated `7839c164`).
- Pre-push gate state at HEAD `467647e`: ALL CHECKS PASS (ruff +
  ruff format + vermin 3.10 target + validate_consistency).
- Unstaged changes intentionally ignored across sessions (operator-
  side work in the locked tree):
    eval_data/README.md
    eval_data/TAXONOMY_GAP_LOG.md
    eval_data/stage1_labels.jsonl
  Routinely unstaged through Sessions 8-19.
- Corpus: 222 .html fixtures (unchanged from Session 17 close).
- 202 expected.json files (unchanged).
- 222 meta.json files (unchanged).
- 1213 baseline-v0 files (202 fixtures × 6 components + manifest.json;
  unchanged from Session 18 close at `9e9a1fb`).
- NEW Session 19: `tools/baseline_v0/check.py` (~290 LOC after
  ruff format; 5 sub-helpers + `check()` at 7 decision points).
- NEW Session 19: `tests/baseline_v0/test_check.py` (24 tests:
  17 helper-unit + 3 validation-path + 4 integration).
- MODIFIED Session 19: `tools/baseline_v0/cli.py` (+`check`
  subparser + dispatch).
- MODIFIED Session 19: `tests/baseline_v0/test_cli.py` (+6
  check-dispatch tests).
- Combined test suite at HEAD `467647e`: 332 passed / 0 failed / 0
  skipped (210 conformance + 46 driver + 76 baseline_v0).

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 19 start: `25ee80b` (Session 18 close-out).
- Session 19 workspace commit: SESSION_LOG.md Session 19 append +
  this template refill (single workspace commit at session close).
- Branch sync with `origin/main`: depends on whether the close-out
  workspace commit is pushed (Sessions 13-18 precedent: pushed).

---

## Session 20 execution order (enforce strict sequence)

The phases below are sequential. Do NOT advance to Phase N+1 until
Phase N's halt-conditions clear. Cassettes and canary are independent
sub-surfaces inside Phases 2-3; either may be deferred at Phase 1
without blocking the other, but within each sub-surface the per-module
commit order is strict.

**Phase 0 — Cold-start verification (mandatory; halt-on-mismatch).**
   See "Required reading" block below for the exact commands.
   Expected: HEAD `467647e`, tags 8 (unchanged from S19 close),
   combined suite 332/0/0, driver-diff vs `dd64963` empty
   (excluding `test_fixture_fetcher.py`), 222 .html / 202
   expected.json / 222 meta.json / 1213 baseline-v0 files.
   HALT IF anything differs.

**Phase 1 — Naming + scope resolution (no code; pre-design-gate).**
   Resolve via AskUserQuestion BEFORE any Step A elicitation:
     (a) `barcada-drift` vs `barcada-baseline canary-run` naming +
         ownership (CLASSIFICATION_ADJACENT_PLAN.md §Item 8 has
         AI/ML team decisions outstanding). If unresolved, defer
         canary to a future session and proceed with cassettes
         only — do NOT commit to a CLI name that AI/ML may
         override.
     (b) Sub-surface scope: cassettes only / canary only / both /
         neither (defer all W7 remainder).
   HALT IF Phase 1(a) cannot be resolved without external AI/ML
   consultation — surface to operator before continuing.

**Phase 2 — Design-gate elicitation (no code; AskUserQuestion).**
   Surface in 2-3 batches as needed; each chosen sub-surface unlocks
   its own questions. Required pre-source-verification per
   `[[verify-before-asking-discipline]]`:
     - Re-read `tools/baseline_v0/cli.py` + `generate.py` at
       session-current HEAD to confirm the subparser + lazy-import
       dispatch pattern.
     - Re-read `tools/baseline_v0/check.py` at session-current HEAD
       to confirm any new sub-surface's helpers won't collide with
       the check surface (e.g., shared `COMPONENT_NAMES`, shared
       hash helpers).
     - Read `eval_data/canary_50_domains.txt` to confirm the 50
       vetted domain lines (read-only consumable; do NOT modify).
   Cassette sub-questions (if cassettes in scope):
     - Tool selection: vcrpy / mitmproxy export / custom.
     - Capture mode: network-only / capture-and-classify (cost:
       $0.20-$3.00 vs $6-$45 envelope).
     - Robots.txt compliance: per-domain pre-record check /
       restrict to canary_50 vetted subset / defer to post-W A
       robots-parser.
     - Corpus curation: must run `extract_hard_exclusions` against
       each candidate; either drop FP-tripping candidates or
       document which cassettes encode known FPs (LESSONS S9).
     - Module placement: `tools/synthetic_crawl/` namespace
       package / extension under `tools/baseline_v0/`.
     - Determinism gate: byte-identical replay across 2 runs /
       documented-exclusion list of non-deterministic fields.
   Canary sub-questions (if canary in scope):
     - Scheduler mechanism: GitHub Actions cron / server cron
       daemon / operator-driven manual.
     - Trend dashboard scope: full (3 metrics: agreement, cost,
       anti-bot) / minimal (1 metric).
   Shared sub-questions:
     - Commit shape: per-module / bundled / hybrid.
     - Tag at session close: `workstream-0-week7-end` at
       full-W7-close / `workstream-0-end` if cassettes + canary
       fully close W0 / defer all.
   HALT IF any decision would require modifications to
   `src/barcada_scraper/` production code OR to the W4.1.5
   driver — surface as design-gate before patching.

**Phase 3 — Implementation (per-module commits, strict order).**

   For cassettes (if in scope; each step its own commit + boundary
   verification):
     3.1 `WA0.W7.cassettes-skeleton` — subparser + dispatch +
         stub module. CLI surface validated end-to-end via --help.
         Combined-suite at boundary.
     3.2 `WA0.W7.cassettes-driver` — recording mode + replay
         mode. NO live HTTP yet; tested via mocked HTTP.
         Combined-suite at boundary.
     3.3 `WA0.W7.cassettes-tests` — unit (record/replay logic) +
         integration (mock-HTTP cassette round-trip).
         Combined-suite at boundary.
     3.4 `WA0.W7.cassettes-corpus-capture` — actual live recordings
         of the chosen N-domain corpus. Robots.txt compliance
         gate from Phase 2 enforced before each record.
         Cost-aware: halt + re-estimate if actual spend exceeds
         3× the Phase 2 budget envelope.

   For canary (if in scope):
     3.5 `WA0.W7.canary-skeleton` — subparser + dispatch + stub.
         CLI surface validated. Combined-suite at boundary.
     3.6 `WA0.W7.canary-impl` — parquet output + per-domain
         pipeline invocation. Combined-suite at boundary.
     3.7 `WA0.W7.canary-tests` — argparse + parsing + parquet
         output schema. Combined-suite at boundary.
     3.8 `WA0.W7.canary-scheduler` — GitHub Actions workflow OR
         cron config OR operator-doc per Phase 2 decision.
     3.9 `WA0.W7.canary-dashboard` — trend script/notebook per
         Phase 2 scope decision.

   At EVERY commit boundary:
     - Combined suite (conformance + driver + baseline_v0 +
       any new W7 test modules) green.
     - ruff check + format --check on touched files green.
     - `[[double-check-before-commit]]` strict rule: every
       concrete claim in the commit message verified against
       source/output BEFORE staging. Build verification table.
   HALT IF combined suite goes red and the new failure is NOT
   a deliberate consequence of the surface-under-test.

**Phase 4 — Pre-push gate (whole-tree).**
   - `ruff check .`                          → must be clean
   - `ruff format --check .`                 → must be clean
   - `git ls-files '*.py' | xargs vermin --target=3.10`
                                             → must hold 3.10 floor
   - `eval_data/scripts/validate_consistency.py`
                                             → 0 errors / 0 warnings
   HALT IF any gate red. Never use `--no-verify`.

**Phase 5 — Push + tag.**
   - Push to `origin/main` only after operator confirms.
   - Tag disposition per Phase 2's shared sub-question
     (`workstream-0-week7-end` / `workstream-0-end` / defer).

**Phase 6 — Workspace close-out.**
   - Append Session 20 entry to `~/crawler-audit/SESSION_LOG.md`.
   - Refill `~/crawler-audit/SESSION_TRANSITION_TEMPLATE.md`
     for Session 21.
   - Single workspace commit at session close (Sessions 13-19
     precedent). Push workspace after operator confirms.

---

## Regression-protection checklist (DO NOT BREAK)

The Session 19 `check` sub-surface is a load-bearing surface for
future Phase 4 PR-E CI-gate wiring. Session 20 cassette + canary
work MUST NOT regress it. Specifically:

**Code surfaces that must stay green** (not modify unless explicit
operator authorization at Phase 2 design-gate):

- `tools/baseline_v0/cli.py` — MAY add new subparsers (e.g.,
  `cassettes`, `canary-run`) following the same lazy-import
  dispatch pattern. MUST NOT alter the existing `generate` or
  `check` subparser argument shapes, defaults, or dispatch
  semantics.
- `tools/baseline_v0/check.py` — read-only this session.
- `tools/baseline_v0/generate.py` — read-only this session.
- `tools/baseline_v0/determinism.py` — read-only. Both cassettes
  and canary may IMPORT `canonical_json` + `hash_canonical`
  (analog of how `check.py` reuses them) but must not modify.

**Test surfaces that must stay green** (no edits to existing tests
unless authorized):

- `tests/baseline_v0/test_check.py` — 24 tests, all green at S19
  close. MUST stay 24/24 green through every S20 commit boundary.
- `tests/baseline_v0/test_generate.py` — 18 tests, unchanged.
- `tests/baseline_v0/test_cli.py` — 15 tests (9 generate + 6 check
  dispatch). Session 20 MAY add new tests for new subparsers
  (e.g., `test_cassettes_*`, `test_canary_*`) following the same
  pattern. MUST NOT modify the 15 existing tests.
- `tests/baseline_v0/test_determinism.py` — 19 tests, unchanged.
- `tests/runners/fixture_cascade/` — 46 driver tests. Driver
  TEST files may be realigned via W5.X-prefix commits per Session
  16 precedent ONLY IF cassette/canary work surfaces a driver-
  test brittleness; default position is "don't touch."
- `tests/scraper/test_fixture_conformance.py` — 210 conformance
  tests, unchanged.

**Fixture / manifest invariants**:

- `tests/fixtures/baseline-v0/manifest.json` — schema_version
  `baseline-v0/0.1.0`, fixture_count 202, llm_mode `real`,
  driver_sha `521e363466435c30deab7cdc63a73649c8de3bce`. Do NOT
  re-capture during Session 20 (would invalidate the check
  comparison surface). A future re-capture is a separate
  operator-authorized work unit.
- `tests/fixtures/baseline-v0/` per-component files (202 × 6 =
  1212 + manifest = 1213 total) — do NOT edit piecemeal.
- The 222 `.html` + 202 `expected.json` + 222 `meta.json`
  fixtures — corpus stable; do NOT add/remove/modify during
  Session 20 unless explicitly authorized.

**Subsystem boundaries** (enforced regardless of operator
authorization):

- `src/barcada_scraper/` — production code; out of scope for
  W A.0 W7 unless Phase 2 design-gate explicitly authorizes a
  specific module.
- `configs/` — pipeline configs; out of scope.
- `eval_data/` — locked tree; read-only consumable (e.g., reading
  `canary_50_domains.txt` is allowed; modifying is not).
- All Workstream 0 tags — locked; do NOT move.

**Cumulative test-count gate**: combined suite at S19 close is
332/0/0. Session 20 commits must keep `conformance + driver +
baseline_v0 + new_W7_test_modules` at ≥332 green throughout. A
single failing test that was passing at session open is a
regression — investigate immediately, do not advance phases.

---

## Active task list

The Session 19 task list (cold-start verify → required reading →
source-verify cli/generate → Step A → 3 commits → pre-push → push →
Step F → close-out) is fully complete. `check` sub-surface
substantively closed.

Suggested Session 20 tasks (W A.0 W7 remainder; the Session 20
prompt should pre-resolve the 5 reviewer-feedback gaps before
Step A):

- **Synthetic crawl tapes** (plan §4 W7 line 314-323).

  For ~20-30 representative domains beyond the fixture corpus:
  use `vcrpy` or similar to record full HTTP exchanges (request +
  response + headers + timing), save cassettes per domain to
  `tests/fixtures/synthetic_crawls/<domain>/`, capture baseline
  outcomes per domain. Larger design surface than `check`: tool
  selection, capture mode, robots.txt compliance, FP-aware corpus
  curation, determinism gate. See "Notes for Session 20" below
  for the explicit pre-Step-A decision list.

- **Canary wiring** (plan §4 W7 line 325-331; intersects with
  CLASSIFICATION_ADJACENT_PLAN.md §Item 8 `barcada-drift`).

  Wire `canary_50_domains.txt` (50 vetted lines; eval_data/, locked,
  read-only consumable) to a scheduled job. Weekly cron. Trend
  dashboard (per-domain agreement with last baseline, cost per
  domain over time, anti-bot success rate). The naming/ownership
  question (`barcada-baseline canary-run` per plan §4 vs.
  `barcada-drift` per CLASSIFICATION_ADJACENT_PLAN.md §Item 8 with
  AI/ML team decisions outstanding) should be surfaced at Step A
  before committing to the CLI shape.

- **Workstream 0 close tag** (post-cassettes + post-canary).

  After W A.0 W7 fully closes, the operator may place
  `workstream-0-end` at the W7 close commit. Three currently-deferred
  carry-forward tags supersede via that close:
    - `workstream-0-week5-end` (already at `ddd3cb0`, S16 close;
      deferred Sessions 17, 18, 19)
    - `workstream-0-week5-multipage-end` (operator-discretion at
      `e060e5f`, S17 multipage close; deferred Sessions 17, 18, 19)
    - `workstream-0-week7-end` (operator-discretion at the W7 full
      close commit)

- **Phase 4 PR-D/E/F/G** (forward look; NOT Session 20 scope
  unless operator explicitly opens it). Prerequisite: W A.0 W7
  close (including cassettes + canary).

Task state is session-local in Claude Code; it does NOT carry across
sessions. Session 20 should TaskCreate fresh tasks on open.

---

## Outstanding operator-input requests entering Session 20

**Material item — barcada-drift vs barcada-baseline canary-run
naming + ownership**: Plan §4 W7 line 327 specifies
`barcada-baseline canary-run --domains canary_50_domains.txt
--output canary_runs/<date>.parquet`. CLASSIFICATION_ADJACENT_PLAN.md
§Item 8 separately specifies a `barcada-drift` CLI (crawler-owned,
~300 LOC) with "Decisions needed from AI/ML team" (drift metric
definition, alert threshold, canary curation, action on drift).
These may merge under one umbrella, stay separate (canary-run for
data collection; drift for orchestration on top), or canary-run
defers entirely until AI/ML team alignment lands. Surface at
Session 20 Step A before committing to the CLI shape.

**Material item — cassette tool selection + capture mode + robots
compliance + corpus curation + determinism gate**: Plan §4 W7
line 318 names "vcrpy or similar" but the choices have meaningful
cost + design implications (see "Notes for Session 20" below for
the explicit pre-Step-A decision list).

**Material item — `workstream-0-week5-end` tag disposition
(deferred again at Session 19 Step F)**: The annotated tag remains
at `ddd3cb0` (Session 16 close), placed BEFORE the multipage_
boilerplate closure (Session 17 at `e060e5f`). Operator chose
`Defer all` at Session 19 Step F; the future `workstream-0-end`
tag (placed after W A.0 W7 fully closes) would supersede.

**Material item — per-tier cost-accounting wiring gap (W4.3.X
candidate, driver-locked)**: Carried forward from Session 14
surface + Sessions 15-19 deferred. W4.1.5 driver's cost-journal
`totals.stage{1_llm,1_embedding,...}_usd` fields not incremented;
per-row `stage3_decision.evidence_cost_usd` is $0; total cost
telemetry is intact. Driver-locked at `dd64963`. Session 19
disposition: DEFERRED (no operator request; check sub-surface
didn't need per-tier extrapolation). Severity: LOW. May surface
in Session 20 if cassette cost-shape comparison or canary trend
dashboard needs per-tier accounting.

**No other gates** between Session 20 open and W A.0 W7 cassettes
+ canary work.

---

## Operator decisions made during Session 19 (cross-ref to SESSION_LOG.md)

1. **Step A scope: check only** (Q1 narrowed to a single
   sub-surface). Cassettes + canary deferred to Session 20+ so
   their design surfaces get proper room.
2. **Check behavior on diff: Summary diff** (Q6 recommended).
   Per-fixture component breakdown on mismatch; exit 0/1/2
   semantics; suitable for future Phase 4 PR-E CI-gate consumption.
3. **Commit shape: Per-module** (Q7 recommended). 3 commits:
   skeleton -> real impl -> tests. Combined-suite at each boundary.
4. **Step F: Defer all tags**. No tags placed this session.
   `workstream-0-week5-end` (ddd3cb0), the hypothetical
   `workstream-0-week5-multipage-end` (e060e5f), and the
   hypothetical `workstream-0-week7-end` all remain deferred until
   the future `workstream-0-end` supersedes them.
5. **Always verify every claim in commit message before staging**
   (operator-codified mid-session after the auth_403/griftdijk.net
   vs empty_google_sites/atari_vw_synthetic claim error). Memory
   `[[double-check-before-commit]]` updated.

---

## Pattern notes for Session 20 (W A.0 W7 cassettes + canary)

- **Verify EVERY concrete claim in commit message before staging**
  (Session 19 finding, operator-codified). Fixture names, file
  counts, exit codes, line counts, test counts, helper names. No
  claims by pattern-completion. Build a verification table in chat
  (claim → reality → status) and reconcile before "Confirm to
  commit?". The operator-ratchet always surfaces something;
  operationalize as a self-check.

- **Bash pipe artifacts mask Python exit codes**. `python_cmd
  2>&1 | grep ... | tail` makes `$?` reflect tail's exit (always
  0 unless tail itself errors), not python's. Use `> stdout.out
  2> stderr.err; echo $?` or `${PIPESTATUS[0]}` when exit-code
  matters. Applied during Session 19 smoke verification.

- **Mid-implementation ruff format-check, not just pre-push**.
  Skeleton commit b358a02 shipped with multi-line `help=` strings
  that ruff format wanted collapsed. Run `ruff check + format
  --check` on touched files right after each code-touching Edit,
  not just before the first commit. Bundle cleanup into the
  follow-up commit message explicitly so future bisect understands
  cross-file touches.

- **Sibling-module style consistency over project-wide rule
  compliance for one-file additions** (Session 19 finding).
  check.py uses `.get()` x2 + `.items()` x2 matching generate.py's
  identical patterns, despite code-readability.md flagging both.
  Disclose in commit message; project-wide compliance lands as
  its own refactor scope.

- **Integration tests can self-seed via the module-under-test's
  siblings** (Session 19 pattern). test_check.py drives
  `generate(fake-mode, max_fixtures=1)` to write a real manifest
  in a temp dir, then runs check() against it. Cheaper than
  mocking the cascade; tighter coverage than synthetic-only unit
  tests; same fake-mode-zero-cost guarantee. The 4th sanity-gate
  test re-hashes the seeded component .json files with check.py's
  own canonical_json + hash_canonical chain to catch future
  divergence between generate <-> check hash chains.

- **Reviewer-feedback hygiene before applying** (Session 19
  finding). External-reviewer feedback arrives in N items. Walk
  each against actual repo state before pattern-applying. Verify
  every flagged SHA, file shape, claim against on-disk reality
  via cold-start verification or targeted greps. Many "must-fix"
  items collapse under verification; the valid completeness items
  often bear on sub-surfaces that scope decisions defer anyway.
  Route valid items to where they're load-bearing rather than
  bolting on to the current session.

- **Plan-spec interpretation room** (Session 18 finding, re-
  confirmed Session 19): plan §4 wording may diverge from runtime
  code's surface in ways needing a design-gate AskUserQuestion
  before implementation. For W7 cassettes, the "vcrpy or similar"
  framing + the "capture baseline outcomes per domain" framing
  both have multiple valid readings.

- **Background process + harness notification** (Session 18
  finding): long-running cascade or cassette-recording runs fit
  `Bash run_in_background` cleanly. Harness notifies on completion
  without polling.

- **Safety hook destructive-op workaround** (Session 18 finding):
  safety-check.sh blocks `rm -rf` even on untracked dirs. Ask
  operator to execute `! rm -rf <path>` in the chat (the `!`
  prefix executes inline). Don't bury in retry.

- **Manifest in-place metadata refresh** (Session 18 finding):
  when on-disk content is correct but metadata fields lag (e.g.,
  driver_sha post a small bug-fix commit), a one-shot manifest
  re-serialization beats spending another capture cycle's cost.

- **Wrapper-level vs cascade-level filtering** (Session 18
  finding): wrapper computes in-scope items first (path-aware,
  excludes multipage_boilerplate/), then passes stems as cascade's
  `fixture_filter` with `max_fixtures=None`. Wrapper owns "what's
  in scope"; cascade handles "process these stems".

- **Pricing-as-consistent-failure pattern** (Session 17 finding):
  still applies for any future fixture sourcing — default
  synthetic-with-real-markers for pricing pages.

- **Markdown-render NBSP corruption avoidance** (Session 17
  finding): for whitespace-sensitive shell commands or curl args,
  write to /tmp/ via Write tool and run via `bash /tmp/script.sh`
  rather than copy-pasting through markdown rendering.

- **Verify-before-asking discipline extension** (Sessions 12, 16,
  17, 18, 19): when operator references a SHA, file shape, fixture
  state, or prompt-prescribed layout, verify against current repo
  state BEFORE acting. Bidirectional: applies to operator-issued
  state claims as well as Claude Code outputs and external
  reviewer claims (Session 19 generalization).

- **Sub-agent delegation for analysis-heavy work**: Sessions 17 +
  18 used Explore subagent for cold-start required reading +
  source-verification of cascade.py/consolidate.py/cli.py/
  fixture_fetcher.py in one consolidated brief. Forward-applicable
  for any session requiring multi-file/source-tree analysis
  before design decisions.

- **Per-domain or per-subsurface decomposition with operator
  approval gates** (Sessions 6, 11, 16, 17, 18, 19 pattern). For
  Session 20's W A.0 W7 remainder, per-subsurface commits (e.g.
  `WA0.W7.cassettes-skeleton`, `WA0.W7.cassettes-driver`,
  `WA0.W7.cassettes-capture`, `WA0.W7.canary-skeleton`,
  `WA0.W7.canary-impl`, `WA0.W7.canary-scheduler`) is the natural
  shape.

- **Confirm-to-commit gating** before every commit (LESSONS
  anchor pattern; Sessions 4-19).

- **File-based commit messages** at `/tmp/<id>-msg.txt`; no
  `Co-Authored-By`.

- **Pre-push gate** must run green; never use `--no-verify`. Use
  `git ls-files '*.py' | xargs vermin --target=3.10` (not bare
  `vermin .`) to avoid venv-internal pytest 3.14 false-positives.

- **Driver-locked policy continues** at `dd64963`. Driver TEST
  files may be realigned via W5.X-prefix commits per Session 16
  precedent. Sessions 18 + 19 did not need a driver-test realign.

- **Conformance count discipline**: W A.0 check sub-surface
  close at 332 combined (210 conformance + 46 driver + 76
  baseline_v0). Any new reds in Session 20 should be either (a)
  deliberate (new W7 surface exposed issue) or (b) immediately
  investigated.

---

## Locked artifacts reminder (CRITICAL — do not modify)

- All of `eval_data/` — locked. Read-only context only.
- `stage1.schema.json` v1.0 / 49 keywords — locked.
- All Workstream 0 + baseline-v0 tags — locked
  (pre-remediation-2026-05-19 + workstream-0-week{1,2,3,4-1-5,4,5}-end
  + baseline-v0).
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` — read-only since Session
  12 absorption.
- `CLASSIFICATION_ADJACENT_PLAN.md` — read-only governance
  reference (decisions on Items 6 + 8 outstanding at AI/ML team).
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
- `tests/fixtures/baseline-v0/` subtree — locked at Session 18
  close (9e9a1fb). Future regenerations may overwrite, but the
  current snapshot is the canonical W6 baseline-v0 capture and
  should not be edited piecemeal.
- `tools/baseline_v0/` CLI module — production-style code surface.
  Session 19 added `check.py` + `check` subparser; Session 20 may
  add cassette-recording driver and `canary-run` subcommand (TBD
  per Step A naming decision) but should not refactor the existing
  surfaces without operator authorization.
- NEW Session 19: `tests/baseline_v0/test_check.py` (24 tests) —
  Session 20 may extend (e.g., real-mode integration test against
  the committed baseline-v0 manifest) but should not refactor.

---

## Next concrete work unit

- **Action ID:** **W A.0 W7 cassettes + canary** (plan §4 W7).
- **Scope:** synthetic-crawl-tape capture for ~20-30 representative
  domains beyond the fixture corpus; canary scheduler wiring against
  `canary_50_domains.txt`; trend dashboard. The Session 20 prompt
  should fold in the 5 reviewer-feedback gaps surfaced in Session 19
  (see "Notes for Session 20" below) before Step A elicitation.
- **Acceptance:** synthetic-crawl-tape cassettes recorded and
  replayable; canary scheduler runs against canary_50_domains.txt;
  trend dashboard renders the three metrics (agreement, cost,
  anti-bot success). Pre-push gate green.
- **Files expected to be touched:**
  - New module(s) under `tools/baseline_v0/` (e.g.
    `tools/baseline_v0/canary.py`) or a new namespace like
    `tools/synthetic_crawl/` for the cassette driver (Step A
    decision).
  - Tests under `tests/baseline_v0/` and/or
    `tests/synthetic_crawl/`.
  - New cassette files under `tests/fixtures/synthetic_crawls/`.
  - Canary scheduler config (GitHub Actions workflow file or cron
    daemon config — Step A decision).
- **Files NOT to be touched:**
  - All locked artifacts listed above.
  - The 222 existing .html fixtures (corpus stable).
  - The committed baseline-v0/ snapshot at 9e9a1fb (regenerations
    may overwrite, but not piecemeal-edit).
  - W4.1.5 driver internals — locked per W4.1.5 policy.
  - Production code under `src/barcada_scraper/` unless explicitly
    authorized at Session 20 design-gate.

After W A.0 W7 fully closes (1-2 sessions), Workstream 0 is done
and Workstream A (Compliance Foundation, plan §5) opens.

---

## Required reading (Session 20 first 10 minutes)

In this order:

1. **This file** (you're reading it).
2. **`SESSION_LOG.md` Session 19 entry** — what landed during the
   `check` sub-surface: 3 commits (b358a02 skeleton → eca4ec0 real
   + cli reflow → 467647e tests); the reviewer-feedback walk-through
   (3 of 5 "must-fix" items collapsed under cold-start verification);
   the auth_403-vs-empty_google_sites claim error caught by the
   double-check ratchet and the resulting always-verify rule.
3. **`LESSONS.md`** — operator patterns. Session 19 forward-
   applicable findings to fold in: claim-verification-before-commit
   strict rule, bash-pipe-exit-code-masking, mid-implementation
   ruff format-check, sibling-module style consistency rule,
   integration-tests-self-seed-via-siblings, reviewer-feedback
   hygiene.
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §4 Week 7** (cassettes
   + canary spec) + `CLASSIFICATION_ADJACENT_PLAN.md §Item 8`
   (barcada-drift naming question).
5. **`tools/baseline_v0/check.py` + `tests/baseline_v0/test_check.py`**
   at HEAD `467647e` — the Session 19 deliverable. Pattern for any
   future sub-surface that extends `tools/baseline_v0/`.

After reading, verify repo state:

```
git -C /Users/administrator/projects/barcada-scraper status
git -C /Users/administrator/projects/barcada-scraper log --oneline -8
git -C /Users/administrator/projects/barcada-scraper tag -l
find /Users/administrator/projects/barcada-scraper/tests/fixtures/html -name '*.html' -type f | wc -l
find /Users/administrator/projects/barcada-scraper/tests/fixtures/baseline-v0 -type f | wc -l
.venv/bin/python -m pytest tests/scraper/test_fixture_conformance.py tests/runners/fixture_cascade/ tests/baseline_v0/ -q
```

Expected:
- Last commit SHA: `467647e` (WA0.W7.check-tests).
- Tags include `baseline-v0` at 9e9a1fb (annotated 7839c164).
- 222 .html files.
- 1213 baseline-v0 files.
- Combined suite: 332 passed / 0 failed / 0 skipped.
- 0 ahead / 0 behind origin/main.
- Only operator-side eval_data/ files showing as unstaged.

If anything differs, surface to operator before doing work.

Then open W A.0 W7 cassettes + canary design discussion via
AskUserQuestion as the first design-gate. The 5 pre-Step-A
decisions to surface are listed in "Notes for Session 20" below.

---

## Risk register state (plan §11)

No new risks escalated and unresolved by Session 19.

Forward-applicable entries:

- "Recapture tooling needs retry policy" — STILL applies. Becomes
  load-bearing in Session 20 cassette recording: ≥3 retries on
  TLS/H2/refused-connection per LESSONS S5 + S9 patterns.
- "Phase 4 measurement half blocked on operator-led labeling" —
  STILL applies.
- "Cost-journal per-tier accounting gap" (Session 14 surface) —
  STILL applies. Session 19 disposition: DEFERRED. Severity: LOW.
- "W4.2 expected-output lifetime constrained" — RESOLVED at
  Session 18 close. baseline-v0 supersedes (consumer-level) at the
  9e9a1fb tag. Full file-system supersession happens at W A.0 W7 /
  Phase 4 PR-E consumer migration.
- "baseline-v0 metadata field freshness" (Session 18 surface) —
  STILL applies. Future regenerations should refresh driver_sha +
  generated_at in-place when content is unchanged.
- "Wrapper enumeration must match source-tree depth" (Session 18
  surface) — RESOLVED at Session 18 via the relative_to(fixture_root)
  pattern. Test coverage in tests/baseline_v0/test_generate.py::
  test_enumerate_single_page_handles_nested_category.

NEW Session 19 risk-register additions:

- "Cassette recording without robots.txt compliance" (LOW-MEDIUM):
  Plan §4 W7 chronology has the W A robots.txt parser AFTER W7.
  Recording 20-30 live captures of third-party domains in Session
  20 without robots.txt compliance is the exact compliance gap
  Workstream A is meant to close. Mitigation options (per Session
  19 reviewer-feedback review): (a) manually check robots.txt per
  candidate before recording; (b) restrict corpus to
  canary_50_domains.txt subset (vetted institutional domains:
  example.com, iana.org, python.org, wikipedia.org, mit.edu, etc.);
  (c) defer cassettes to post-Workstream A.
- "Cassette corpus may bake in detector FPs" (LOW): LESSONS S9
  documented ~36% FP rate on modern SaaS marketing sites
  (dd.js / just-a-moment / soft_404 patterns). If Session 20
  curates a "representative SaaS" cassette corpus, those FPs
  bake in as expected baseline. Later detector fixes then look
  like regressions against cassettes. Mitigation: run
  `extract_hard_exclusions` against each candidate before
  recording; either drop FP-tripping candidates or document
  which cassettes encode known FPs.
- "Cassette network-vs-capture mode cost variability" (LOW):
  network-only recording is ~$0 per cassette; capture-and-classify
  is ~$0.30-$1.50 per domain × 20-30 = $6-$45 total. Session 20
  Step A should pick mode explicitly and revise the budget
  envelope accordingly.

LLM cost drift risk (plan §11) — Session 19 update:
- Session 19 incurred $0 (no real-mode cascade runs).
- Cost incurred Sessions 1-19: $0.711 (unchanged).
- Cost budget remaining: $99.29.
- Session 20 estimated cost depends on cassette-capture mode
  (Step A decision; see risk register entry above).

---

## Deferred prose-only fixes register

**Status at Session 19 close: EMPTY.** No new prose-only fixes
surfaced in Session 19.

---

## Cost & schedule tracking

- Cost ceiling: $100 (operator-set 2026-05-19, alert at $50).
- Cost incurred Sessions 1-19: $0.711 (unchanged from S18 close).
- Cost budget remaining: $99.29.
- Session 19 actual spend: $0 (integration tests fake-mode only).
- Session 20 estimated spend: $0.20-$3.00 (cassette recording
  mode; replay free) OR $6-$45 (capture-and-classify mode);
  Step A decision.
- Schedule: 8 weeks elapsed of Workstream 0's 5-week budget
  (Workstream A.0 extends Workstream 0 by 2 weeks). W A.0 W6
  fully closed Session 18; W A.0 W7 check sub-surface fully
  closed Session 19. Cassettes + canary remain for Session 20+.

---

## Notes for Session 20

The Session 20 prompt should fold in these 5 reviewer-feedback
gaps from Session 19 BEFORE Step A:

1. **Cassette tool selection** (Step A sub-question): vcrpy
   (plan's named choice) vs mitmproxy export vs custom cassette
   format. Justification required if non-vcrpy.

2. **Cassette capture mode** (Step A sub-question): network-only
   (cassette is the artifact; baseline outcomes generated later
   from replay) vs capture-and-classify (cassette + pipeline
   outcomes in one pass). Cost envelope differs by 10-30×.
   Revise budget envelope per choice.

3. **Robots.txt compliance gate** (Step A sub-question or Step B
   prerequisite): pre-record per-domain robots.txt check, OR
   restrict to canary_50_domains.txt vetted subset, OR defer
   cassettes to post-Workstream A robots-parser-lands. The
   middle option is likely the cheapest path forward.

4. **Detector-FP-aware corpus curation** (Step A note attached
   to corpus-scope sub-question): run extract_hard_exclusions
   against each candidate before recording. Either drop
   FP-tripping candidates or document which cassettes encode
   known FPs (LESSONS S9 dd.js / just-a-moment / soft_404).

5. **Cassette replay determinism gate** (Step C requirement):
   replay-mode produces byte-identical pipeline outputs across
   two consecutive runs (analog of the baseline-v0
   byte-identical re-run gate in test_generate.py). If
   determinism isn't possible (e.g., timestamps in vcrpy
   cassettes), document the exclusion fields explicitly.

Plus the canary-specific naming question:

6. **barcada-drift vs barcada-baseline canary-run** (Step A
   sub-question): plan §4 W7 names `barcada-baseline canary-run`
   for data collection; CLASSIFICATION_ADJACENT_PLAN.md §Item 8
   names a separate `barcada-drift` CLI (crawler-owned, ~300 LOC)
   for drift detection orchestration with AI/ML team decisions
   outstanding. Resolve naming/ownership before committing to
   the CLI shape.

Other notes:

- **Conformance test red count entering Session 20: 0**
  (`check` sub-surface cleanly closed at 467647e). Any new reds
  in Session 20 should be immediately investigated.
- **0 conformance tests SKIP**.
- **File-based commit messages** still mandatory.
- **"Confirm to commit?" gating** before every commit, paired
  with the always-verify-every-claim discipline operator-codified
  in Session 19.
- **Verify-before-asking discipline**: bidirectional (operator,
  Claude Code, and external-reviewer claims; Session 19
  generalization). Apply to every SHA, file shape, fixture state,
  prompt-prescribed layout, reviewer-flagged "must-fix" item.
- **Combined-suite verification at every commit boundary**
  (Sessions 16-19 pattern). Run conformance + driver + baseline_v0
  suites at every commit boundary. ~45-50s runtime.
- **Pre-push gate** at Session 19 close passed cleanly. Routinely
  passes. Never use `--no-verify`. Use `git ls-files '*.py' |
  xargs vermin --target=3.10`.
- **Plan is read-only** — never edit
  `BARCADA_CRAWLER_REMEDIATION_PLAN.md`.
- **W5.X-prefix pattern**: driver-locked test changes are
  authorized via W5.X-prefix commits per Session 16 precedent.
  Sessions 18 + 19 did not need a driver-test realign.
- **Workspace cwd**: when editing LESSONS.md / SESSION_LOG.md /
  this template, work in `/Users/administrator/crawler-audit/`.
- **W5 tag pattern**: per Sessions 17-19 operator deferrals, the
  `workstream-0-week5-end` tag remains at `ddd3cb0` (S16 close).
  Workstream 0 NOT closed yet — W A.0 W7 cassettes + canary
  follows.
- **baseline-v0 ground truth durability**: the snapshot at
  `9e9a1fb` is the canonical W6 capture. The Session 19 `check`
  subcommand provides the comparison surface against it. Future
  Workstream A/B/C/D changes may produce diffs against this
  baseline (per `barcada-baseline check`); track intentional
  diffs as approved drift in the manifest or commit trail.
- **Safety hook destructive-op workaround**: the project's
  safety-check.sh blocks `rm -rf` even on untracked dirs. If a
  Session 20 step needs to clean up untracked output (e.g.
  intermediate cassette runs), ask the operator to execute
  `! rm -rf <path>` in the chat.
- **This template's structured fields will need refilling at
  Session 20 close.**
