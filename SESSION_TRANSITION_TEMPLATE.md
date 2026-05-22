# Session Transition Template — Handoff from Session 17 → Session 18

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-17 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

---

## Handoff metadata

- Outgoing session number: 17
- Closing date: 2026-05-22
- Outgoing session scope: W5.multipage_boilerplate closure (the
  final W5 sub-surface deferred at Session 16). 20 fixtures across
  5 domains (3 success + 2 gap probes); 9 real curl captures + 11
  synthetic-with-real-markers; snowflake.com → atlassian.com swap
  surfaced mid-session via SPA-shell finding. 6 repo commits + 1
  workspace commit. LLM spend: $0 (Option-3 design-gate decision
  skipped the cascade-driver run; the $0.026 estimate dropped to
  zero). Pushed to origin/main.
- Reason for transition: Workstream 0 Week 5 fully closed (all 6
  sub-surfaces landed). Session 18 picks up W A.0 W6 baseline-v0
  scaffolding per plan §4 W6 + RECONCILIATION_2026-05-21.md §4.3
  + §5.5.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `e060e5f` (W5.multipage-webflow).
- Last commit subject: "W5.multipage-webflow: 4 synthetic gap-probe fixtures"
- Branch sync with `origin/main`: 0 commits ahead, 0 commits behind
  (verified at Session 17 close after push).
- Tags (do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3`
  - `workstream-0-week1-end` at `4f9d23f`
  - `workstream-0-week2-end` at `e5d2f91`
  - `workstream-0-week3-end` at `cf0c14c`
  - `workstream-0-week4-1-5-end` at `dd64963` (annotated `f9be833a`)
  - `workstream-0-week4-end` at `b2e2671` (annotated `c3c6fb74`)
  - `workstream-0-week5-end` at `ddd3cb0` (annotated `fc1ae2ff`,
    placed Session 16). Note: this tag points at the Session 16
    close SHA, NOT at Session 17 multipage closure. Operator may
    decide whether to place a separate `workstream-0-week5-
    multipage-end` at `e060e5f` or amend the week5 annotation.
- Pre-push gate state at HEAD `e060e5f`: ALL CHECKS PASS (ruff +
  ruff format + vermin 3.10 target + validate_consistency).
- Unstaged changes intentionally ignored across sessions (operator-
  side work in the locked tree):
    eval_data/README.md
    eval_data/TAXONOMY_GAP_LOG.md
    eval_data/stage1_labels.jsonl
  Routinely unstaged through Sessions 8-17. validate_consistency
  passes cleanly at Session 17 close (0 errors / 0 warnings).
- Corpus: 222 .html fixtures (W5.multipage_boilerplate adds 20:
  hubspot 4 + notion 4 + atlassian 4 + twilio 4 + webflow 4 in 5
  domain subdirectories under multipage_boilerplate/).
- 202 expected.json (UNCHANGED — multipage_boilerplate intentionally
  has no expected.json per Option-3 design-gate decision; cascade-
  driver run was skipped because detect_cross_page_banners() runs
  at the page_acquisition layer, upstream of cascade execution).
- 222 meta.json (+20 multipage; one per .html fixture).
- Combined test suite at HEAD `e060e5f`: 256 passed / 0 failed / 0
  skipped (210 conformance + 46 driver).

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 17 start: `cdaa0a1` (Session 16 close-out).
- Session 17 workspace commit: this template refill + SESSION_LOG.md
  Session 17 append landed as the single workspace commit of Session 17.
- Branch sync with `origin/main`: depends on whether the close-out
  workspace commit is pushed (Session 13-16 precedent: pushed).

---

## Active task list

The Session 17 task list (Step A → curl captures → SPA-shell finding →
atlassian swap → synthetic synthesis → conformance test → 6 commits →
pre-push gate → push → close-out) is fully complete. Workstream 0
Week 5 substantively closed.

Suggested Session 18 tasks:

- **W A.0 W6 baseline-v0 scaffolding** (plan §4 Weeks 6-7, item #1
  "barcada-baseline generate" CLI as thin wrapper over the W4.1.5
  cascade driver per RECONCILIATION_2026-05-21.md §4.3 + §5.5).

  Build the `barcada-baseline` CLI as a thin wrapper over the
  W4.1.5 cascade driver (rather than a new CLI built from scratch).
  Less new code than the plan originally implied — the engineering
  surface narrows to CLI surface, determinism normalization, and
  integration with the W A.0 W7 synthetic-crawl-tape capture, since
  the cascade-execution mechanics already exist at the W4.1.5
  driver locked at `dd64963`.

  This is the FIRST sub-task that SUPERSEDES the W4.2 + W5
  expected.json files per the output durability constraint (plan
  §11 risk register). The Session 17 close commit `e060e5f` is the
  cumulative baseline against which W A.0 W6's baseline-v0
  generation runs (note: the multipage_boilerplate corpus has no
  expected.json yet; W A.0 W6 may choose to skip multipage or
  generate baseline-v0 for it).

  **Session 18 Step A design-gate elicitation** (suggested):
  1. CLI placement: top-level `bin/barcada-baseline` script vs
     new `tools/baseline_v0/` module vs `src/barcada_scraper/cli/`
     (latter would touch production code, requires authorization).
  2. Subcommand surface: `generate` only, or `generate` + `check`
     at W6 close.
  3. Determinism normalization scope: sorted dict keys + normalized
     floats + canonical JSON serialization; per-stage hashes; etc.
  4. Multipage_boilerplate handling: include in baseline-v0
     generation (would need cascade adaptation for nested layout
     OR per-domain stem fix) OR explicitly skip.

- **W A.0 W7 synthetic-crawl-tape capture** (forward look; NOT
  Session 18 scope per the W6 → W7 sequence).

Task state is session-local in Claude Code; it does NOT carry across
sessions. Session 18 should TaskCreate fresh tasks on open.

---

## Outstanding operator-input requests entering Session 18

**Material item — workstream-0-week5-end tag disposition**: The
annotated tag remains at `ddd3cb0` (Session 16 close), placed BEFORE
the multipage_boilerplate closure. Two options for Session 18 (or
deferred):
1. Place a separate `workstream-0-week5-multipage-end` at `e060e5f`
   to mark the carry-forward closure.
2. Move the annotation message on `workstream-0-week5-end` to
   acknowledge multipage closure without moving the tag SHA.
3. Leave as-is; workstream-0 close tag (if placed) would supersede.

**Material item — per-tier cost-accounting wiring gap (W4.3.X
candidate, driver-locked)**: Carried forward from Session 14 surface
+ Sessions 15-17 deferred. W4.1.5 driver's cost-journal
`totals.stage{1_llm,1_embedding,...}_usd` fields not incremented;
per-row `stage3_decision.evidence_cost_usd` is $0; total cost
telemetry is intact. Driver-locked at `dd64963`; needs operator
authorization to patch. **Session 17 disposition: DEFERRED** (no
operator request to revisit; Session 17 had $0 LLM spend per Option-3
so cost accounting wasn't load-bearing). Severity: LOW. May surface
in W A.0 W6 if per-tier cost extrapolation becomes load-bearing for
baseline-v0 cost-shape comparison.

**Material item — W A.0 W6 CLI design surface**: see suggested
Session 18 task above. Surface via AskUserQuestion at Session 18 open.

**No other gates** between Session 18 open and W A.0 W6 work.

---

## Operator decisions made during Session 17 (cross-ref to SESSION_LOG.md)

1. **Domain selection: 5 in-corpus C18 SaaS** (hubspot, notion,
   snowflake, twilio, webflow). Claude Code recommendation aligned
   with Claude Desktop's suggestion.
2. **Banner pattern: combination 3 success + 2 gap probes**.
3. **Commit shape: 6 commits** (5 per-domain + 1 conformance).
4. **Layout-vs-driver incompatibility → Option 3** (no cascade run,
   no expected.json under multipage_boilerplate/). Drift coverage
   loss accepted; parser-only-snapshot follow-up deferred.
5. **Real captures preferred** (Session 16 sourcing policy carries
   forward); synthetic-with-real-markers fallback for failures.
6. **Snowflake → atlassian.com swap** (snowflake static-curl returns
   SPA shells, no nav signal). Out-of-corpus swap.
7. **Atlassian /pricing synthesized** (atlassian's pricing lives
   under per-product paths; /pricing returns 404).
8. **6-commit order reversal: conformance FIRST, then 5 per-domain**
   (preserves combined-suite green at every commit boundary).

---

## Pattern note for Session 18 (W A.0 W6)

- **Combined-suite verification at every commit boundary** (NEW
  Session 16 pattern, re-confirmed Session 17). Run BOTH driver
  suite and conformance suite at every commit. Worth ~30-40s of
  test runtime per commit to avoid multi-commit verify-after-
  the-fact reconciliation.

- **Pricing-as-consistent-failure pattern** (NEW Session 17 finding):
  modern SaaS marketing /pricing pages consistently fail static-
  curl capture (SPA / WAF / 404) even on SSR-friendly sites.
  Default to synthetic-with-real-markers for pricing pages.

- **Markdown-render NBSP corruption avoidance** (NEW Session 17
  finding): when shell commands have numeric flag arguments or
  whitespace-sensitive syntax, write to /tmp/ via Write tool
  (bytes-on-disk = clean ASCII) and run via `bash /tmp/script.sh`.
  Avoid copy-pasting curl commands with `--retry N`, `--max-time N`,
  case-statement bodies, or other whitespace-sensitive constructs
  through markdown rendering.

- **Working-tree-vs-git-tree visibility for pytest**: pytest's
  filesystem glob discovers fixtures present on disk regardless of
  git tracking state. Combined-suite count at a commit boundary
  reflects the FULL working tree, not the git-tracked subset.
  Per-commit message verification should say "at this commit
  boundary" not "after this commit adds N tests".

- **Verify-before-asking discipline extension** (Sessions 12, 16,
  17): when operator references a SHA, file shape, fixture state,
  or prompt-prescribed layout, verify against current repo state
  BEFORE acting. Session 17 surfaced the driver stem-uniqueness
  incompatibility (Option-3 design-gate) via this discipline.

- **Sub-agent delegation for analysis-heavy work**: Session 17
  used Explore subagent for cold-start required reading +
  source-verification of detect_cross_page_banners() in one
  consolidated brief. Forward-applicable for any session requiring
  multi-file/source-tree analysis before design decisions.

- **Per-domain decomposition with operator approval gates**
  (Sessions 6, 11, 16, 17 pattern). For Session 18's W A.0 W6
  baseline-v0 work, per-subcommand commits (action ref `WA0.W6.
  generate`, `WA0.W6.check`) is a reasonable shape; one bundled
  W6 capstone is the alternative per LESSONS commit hygiene.

- **Confirm-to-commit gating** before every commit (LESSONS anchor
  pattern; Sessions 4-17).

- **File-based commit messages** at /tmp/<id>-msg.txt; no
  Co-Authored-By.

- **Pre-push gate** must run green; never use `--no-verify`. Watch
  for operator-side eval_data/ blockers (Sessions 15-17 precedent;
  validate_consistency cleanly at S17 close after S16 manual fixes).
  Use `git ls-files '*.py' | xargs vermin --target=3.10` (not bare
  `vermin .`) to avoid venv-internal pytest 3.14 false-positives.

- **Driver-locked policy continues** at `dd64963`. Driver TEST
  files (in same directory) may be realigned via W5.X-prefix
  commits when corpus reality shifts under operator-authorized
  changes (Session 16 W5.X-driver-test-realign precedent at
  `8d0fc0e`; Session 17 did not need a similar realign — corpus
  count assertion `len(index) >= 195` holds at 206 even with the
  16 duplicate-stem shadowing from the multipage layout).

- **Conformance count discipline**: W5 closed at 0/210/0 conformance
  + 46/46 driver = 256/0/0 combined. Any new reds in Session 18
  should be either (a) deliberate (new W6 surface exposed issue)
  or (b) immediately investigated.

---

## Locked artifacts reminder (CRITICAL — do not modify)

- All of `eval_data/` — locked. Read-only context only.
- `stage1.schema.json` v1.0 / 49 keywords — locked.
- All Workstream 0 tags — locked (pre-remediation-2026-05-19 +
  workstream-0-week{1,2,3,4-1-5,4,5}-end). The week5 tag remains
  at `ddd3cb0`; Session 18 operator may add a separate marker for
  the multipage closure at `e060e5f`.
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` — read-only since Session
  12 absorption.
- `tests/fixtures/META_SCHEMA.md` + `meta.schema.json` v1.0 +
  `expected.schema.json` v1.1 — locked at W4.3 close (Session 15
  commit `7728bdf`). Further bumps require operator authorization.
- W4.2 expected.json files at `cc2ba2c` + Session 16 W5 additions
  at `ddd3cb0` — valid until W A.0 W6 baseline-v0 supersedes per
  output durability constraint.
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

---

## Next concrete work unit

- **Action ID:** **W A.0 W6 baseline-v0 scaffolding** (plan §4 W6,
  RECONCILIATION_2026-05-21.md §4.3 + §5.5).
- **Scope:** Build `barcada-baseline generate` as thin wrapper over
  W4.1.5 cascade driver. Determinism normalization (sorted dict
  keys, normalized floats, canonical JSON). Integration prep for
  W A.0 W7 synthetic-crawl-tape capture.
- **Acceptance:** `barcada-baseline generate --fixtures tests/
  fixtures/html/` produces deterministic byte-identical output on
  re-run. Existing conformance + driver suites stay green
  (256/0/0). baseline-v0 outputs at a session-determined location
  (likely `tests/fixtures/baseline-v0/` per plan §4 W6 line ~).
- **Files expected to be touched:**
  - New CLI module at `tools/baseline_v0/` or `bin/barcada-baseline`
    (placement TBD via Session 18 Step A).
  - Possibly small additions to driver public API if W4.1.5 needs
    a re-entrant integration hook (driver code itself locked;
    additive only if absolutely required, design-gate first).
  - Tests for the new CLI surface.
- **Files NOT to be touched:**
  - All locked artifacts listed above.
  - The 222 existing .html fixtures (multipage corpus stable).
  - W4.1.5 driver internals (cli.py, cascade.py, parser_compose.py,
    consolidate.py, fixture_fetcher.py main code) — locked per W4.1.5
    policy.
  - Production code under `src/barcada_scraper/` unless explicitly
    authorized at Session 18 design-gate.

After W A.0 W6 closes (1-2 sessions), W A.0 W7 (synthetic-crawl-
tape capture + canary wiring) opens.

---

## Required reading (Session 18 first 10 minutes)

In this order:

1. **This file** (you're reading it).
2. **`SESSION_LOG.md` Session 17 entry** — what landed during W5
   carry-forward (multipage_boilerplate closure; Option-3 design-
   gate; snowflake → atlassian swap; pricing-as-consistent-failure
   finding; markdown-NBSP curl-friction pattern).
3. **`LESSONS.md`** — operator patterns and observed conventions.
   Session 17 forward-applicable findings to fold into LESSONS:
   pricing-as-consistent-failure, NBSP-render-corruption, working-
   tree-vs-git-tree pytest visibility.
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §4 Weeks 6-7** (W A.0
   baseline scaffolding spec).
5. **`RECONCILIATION_2026-05-21.md` §4.3 + §5.5** (W A.0 W6 as thin
   wrapper over W4.1.5 driver, NOT from-scratch CLI).
6. **`tests/runners/fixture_cascade/cli.py`** at HEAD `e060e5f` —
   the W4.1.5 driver CLI that W A.0 W6 will wrap.
7. **`tests/runners/fixture_cascade/cascade.py`** — driver
   orchestration; W A.0 W6's `barcada-baseline generate` will call
   into this (or expose it via a public API hook).

After reading, verify repo state:

```
git -C /Users/administrator/projects/barcada-scraper status
git -C /Users/administrator/projects/barcada-scraper log --oneline -8
git -C /Users/administrator/projects/barcada-scraper tag -l 'workstream-*'
find /Users/administrator/projects/barcada-scraper/tests/fixtures/html -name '*.html' -type f | wc -l
.venv/bin/python -m pytest tests/scraper/test_fixture_conformance.py tests/runners/fixture_cascade/ -q
```

Expected:
- Last commit SHA: `e060e5f` (W5.multipage-webflow).
- Tags include `workstream-0-week5-end` at `ddd3cb0` (annotated;
  not moved during Session 17 multipage closure).
- 222 .html files.
- Combined suite: 256 passed / 0 failed / 0 skipped.
- 0 ahead / 0 behind origin/main.
- Only operator-side eval_data/ files showing as unstaged.

If anything differs, surface to operator before doing work.

Then open W A.0 W6 design discussion: CLI placement, subcommand
surface, determinism normalization scope, multipage_boilerplate
handling. Likely present via AskUserQuestion as the first design-
gate question after Session 18 cold-start verification.

---

## Risk register state (plan §11)

No new risks escalated and unresolved by Session 17.

Forward-applicable entries:

- "Recapture tooling needs retry policy" — STILL applies.
- "Phase 4 measurement half blocked on operator-led labeling" —
  STILL applies.
- "Cost-journal per-tier accounting gap" (Session 14 surface) —
  STILL applies. Session 17 disposition: DEFERRED. Severity: LOW.
  May surface in W A.0 W6 if per-tier cost extrapolation becomes
  load-bearing for baseline-v0 cost-shape comparison.
- "W4.2 expected-output lifetime constrained" — STILL applies.
  W4.2 + W5 outputs valid until W A.0 W6 baseline-v0 supersedes
  OR Phase 4 PR-E lands. Tag `workstream-0-week5-end` annotation
  documents this constraint extension.

NEW Session 17 risk register additions (low-severity):
- "Snowflake.com on SPA-shell list" (operator memory
  [[confirmed-spa-domains]] update). Static-curl returns 170KB
  HTML with 15-23 body chars across home/about/pricing/products.
- "Modern SaaS /pricing as consistent-failure pattern" — 3 of 3
  attempted real-curl captures of pricing pages failed (SPA / WAF
  / 404). Forward fixture sourcing should default synthetic for
  pricing pages.

LLM cost drift risk (plan §11) — Session 17 update:
- Session 17 incurred $0 (Option-3 design-gate eliminated the
  $0.026 cascade-driver run).
- Cost incurred Sessions 1-17: $0.263658 total.
- Cost budget remaining: $99.736.
- W A.0 W6 baseline-v0 generation estimated cost depends on regen
  strategy (full corpus regen ~$0.30; incremental ~$0.03).
- Stop and escalate if actual spend trends >3× original $0.30
  estimate (>$0.90); not triggered.

---

## Deferred prose-only fixes register

**Status at Session 17 close: EMPTY.** W4.3 commit `7728bdf` cleared
all six original entries (a)-(f). No new prose-only fixes surfaced
in Sessions 16-17.

Future deferred prose-only fixes (if any surface in Session 18+)
should be tracked here per the LESSONS.md "Defer prose-only schema
fixes; bump only when machine schema changes" pattern.

---

## Cost & schedule tracking

- Cost ceiling: $100 (operator-set 2026-05-19, alert at $50).
- Cost incurred Sessions 1-17: $0.263658.
- Cost budget remaining: $99.736.
- Session 17 actual spend: $0.
- W A.0 W6 estimated spend depending on baseline-v0 regen strategy:
  $0.03-$0.30.
- Schedule: 5 weeks elapsed of Workstream 0's 5-week budget. W5
  fully closed this session (all 6 sub-surfaces). Session 18 opens
  W A.0 W6 baseline-v0 (Week 6 of overall remediation).

---

## Notes for Session 18

- **Conformance test red count entering Session 18: 0** (W5
  cleanly closed including multipage carry-forward). Any new reds
  in Session 18 should be immediately investigated.
- **0 conformance tests SKIP**.
- **File-based commit messages** still mandatory.
- **"Confirm to commit?" gating** before every commit.
- **Verify-before-asking discipline** — bidirectional. Sessions
  12, 16, 17 patterns. For W A.0 W6 CLI scaffolding, source-verify
  the W4.1.5 driver's public API surface BEFORE designing the
  wrapper. Re-read `tests/runners/fixture_cascade/cli.py` +
  `cascade.py` at session-current HEAD before launching the design-
  gate AskUserQuestion.
- **Combined-suite verification at every commit boundary**
  (NEW Session 16 pattern, re-confirmed Session 17). Run BOTH
  driver suite + conformance suite at every commit boundary.
- **Pre-push gate** at Session 17 close passed cleanly. Routinely
  passes. Never use `--no-verify`. Use `git ls-files '*.py' |
  xargs vermin --target=3.10` to skip venv-internal pytest 3.14
  noise.
- **Plan is read-only** — never edit
  `BARCADA_CRAWLER_REMEDIATION_PLAN.md`.
- **W5.X-prefix pattern**: driver-locked test changes are
  authorized via W5.X-prefix commits per Session 16 precedent.
  Session 17 did not need a similar realign. Session 18 may surface
  a need if W A.0 W6 wrapper exposes driver-test brittleness.
- **Workspace cwd**: when editing LESSONS.md / SESSION_LOG.md / this
  template, work in `/Users/administrator/crawler-audit/`.
- **W5 tag pattern**: per Session 17 operator deferral, the
  `workstream-0-week5-end` tag remains at `ddd3cb0` (Session 16
  close). Multipage closure (Session 17, `e060e5f`) NOT separately
  tagged yet. Workstream 0 NOT closed yet — W A.0 W6/W7 follows.
- **W4.2 + W5 ground truth durability**: the cumulative expected.
  json set at `ddd3cb0` (202 files) is the W A.0 W6 baseline-v0
  input. Multipage_boilerplate corpus has no expected.json per
  Option-3 design-gate (drift coverage loss accepted). W A.0 W6
  baseline-v0 generation will SUPERSEDE the 202-fixture expected.
  json baseline per output durability constraint.
- **This template's structured fields will need refilling at
  Session 18 close.**
