# Session Transition Template — Handoff from Session 20 → Session 21

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-20 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 21 invocation prompt:** `~/crawler-audit/SESSION_21_PROMPT.md`
(drafted at Session 20 close; mirrored at `~/Downloads/session-21-prompt.md`
for operator-invocation convenience). The prompt is scope-agnostic at
Phases 0/1 and elicits scope-specific design gates at Phase 2 per
chosen candidate. The 3 carry-forward S20 amendments (MF-1 driver_sha
prefix-match; MF-2 Q1.1(B) wording; SR-8 Phase 1 HALT tightening) are
baked into the prompt directly. Re-read it on session open.

---

## Handoff metadata

- Outgoing session number: 20
- Closing date: 2026-05-23
- Outgoing session scope: W A.0 W7 cassettes + canary — both
  remaining W7 sub-surfaces landed across 8 per-module commits
  + 1 annotated tag (`workstream-0-week7-end`). Cassettes shipped
  as new `tools/synthetic_crawl/` namespace package (vcrpy-based
  record/replay + 20-domain live cassette corpus + 33 tests).
  Canary shipped as `barcada-baseline canary-run` subcommand
  under existing CLI + launchd Saturday-9am kit + 23 tests.
  LLM spend: $0.
- Reason for transition: W A.0 W7 fully closed. Workstream 0 not
  yet fully closed — per-tier cost-accounting wiring gap remains
  DEFERRED (carry-forward, severity LOW; would justify `workstream-
  0-end` tag if patched). Session 21 scope candidates listed
  below; operator-discretion at S21 open.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `ea37102` (WA0.W7.canary-launchd-kit).
- Last commit subject: "WA0.W7.canary-launchd-kit: scripts/launchd/
  + README + .gitignore for runtime outputs"
- Branch sync with `origin/main`: 0 ahead / 0 behind (verified at
  Session 20 close after push).
- Tags (do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3`
  - `workstream-0-week1-end` at `4f9d23f`
  - `workstream-0-week2-end` at `e5d2f91`
  - `workstream-0-week3-end` at `cf0c14c`
  - `workstream-0-week4-1-5-end` at `dd64963` (annotated `f9be833a`)
  - `workstream-0-week4-end` at `b2e2671` (annotated `c3c6fb74`)
  - `workstream-0-week5-end` at `ddd3cb0` (annotated `fc1ae2ff`)
  - `baseline-v0` at `9e9a1fb` (annotated `7839c164`)
  - `workstream-0-week7-end` at `ea37102` (annotated; placed
    Session 20 per Q2.10)
- Pre-push gate state at HEAD `ea37102`: ALL CHECKS PASS (ruff +
  ruff format + vermin 3.10 + validate_consistency 0/0). Note:
  validate_consistency had to be operator-fixed mid-Session-20
  for a pre-existing eval_data WIP duplicate keyword in row 377
  (bigid.com); see LESSONS.md "Pre-push gate against operator-WIP
  territory".
- Unstaged changes intentionally ignored across sessions (operator-
  side work in the locked tree):
    eval_data/README.md
    eval_data/TAXONOMY_GAP_LOG.md
    eval_data/stage1_labels.jsonl
  Routinely unstaged through Sessions 8-20. Operator deduped
  row 377 mid-Session-20 (the dedupe edit is part of operator-WIP
  in stage1_labels.jsonl, not in any S20 commit).
- Corpus: 222 .html fixtures (unchanged from Session 17 close).
- 202 expected.json files (unchanged).
- 222 meta.json files (unchanged).
- 1213 baseline-v0 files (unchanged from Session 18 close at `9e9a1fb`).
- NEW Session 20: `tools/synthetic_crawl/` package (4 files; 233
  LOC at skeleton + 209 LOC in recorder.py after driver impl =
  ~390 LOC total).
- NEW Session 20: `tools/baseline_v0/canary.py` (274 LOC; 6
  helpers + canary_run() at 6 decision points).
- NEW Session 20: `tests/synthetic_crawl/` package (3 files;
  542 LOC; 33 tests).
- NEW Session 20: `tests/baseline_v0/test_canary.py` (354 LOC;
  17 tests).
- NEW Session 20: 20 cassettes + 20 sidecars at
  `tests/fixtures/synthetic_crawls/<domain>/` (4.6 MB).
- NEW Session 20: `scripts/launchd/` kit (5 files; 318 LOC).
- MODIFIED Session 20: `tools/baseline_v0/cli.py` (+canary-run
  subparser + dispatch; +63/-4).
- MODIFIED Session 20: `tests/baseline_v0/test_cli.py` (+6
  canary-dispatch tests; +103).
- MODIFIED Session 20: `pyproject.toml` (+vcrpy>=8.1 in
  `[project.optional-dependencies].dev`; +8).
- MODIFIED Session 20: `.gitignore` (+canary_runs/ entry; +5).
- Combined test suite at HEAD `ea37102`: 388 passed / 0 failed /
  0 skipped (210 conformance + 46 driver + 99 baseline_v0 + 33
  synthetic_crawl = 388).

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 20 start: `4f29bed` (S20 prompt
  finalization).
- Session 20 close-out workspace commits (2, both pushed to origin):
  - `1eb9947` "Session 20 close-out: SESSION_LOG.md append +
    LESSONS.md fold-in + TRANSITION refill" — SESSION_LOG.md S20
    append + LESSONS.md fold-in of S19+S20 patterns per SR-7 +
    this template's first-pass refill.
  - `dccab29` "Session 21 prompt drafted: scope-agnostic 7-phase
    template + transition pointer" — SESSION_21_PROMPT.md drafted
    + Downloads mirror + this template's pointer update.
- Last commit SHA at Session 21 start: `dccab29` (or later if
  additional workspace doc edits land before S21 open). The S21
  prompt's Phase 0 Step 0.1 expects `dccab29` as the starting
  workspace HEAD.
- Branch sync with `origin/main`: 0 ahead / 0 behind (verified at
  Session 20 close after both workspace commits pushed).

---

## Session 21 execution order (enforce strict sequence)

Same 7-phase shape as Session 20 (Phase 0 cold-start verify →
Phase 1 naming+scope → Phase 2 design-gate → Phase 3 impl →
Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out). Halt-
on-mismatch at every phase; never bypass `--no-verify`.

Session 21 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 20 entry.
3. Reading the LESSONS.md additions Session 20 landed
   (especially the 6 forward-applicable patterns folded per SR-7
   amendment).
4. Reading the relevant section of BARCADA_CRAWLER_
   REMEDIATION_PLAN.md for the chosen Session 21 scope (see
   "Notes for Session 21" below).
5. Running Phase 0 cold-start verification per the chosen S21
   prompt's protocol.

---

## Outstanding operator-input requests entering Session 21

1. **Session 21 scope choice** — pick from the candidates in
   "Notes for Session 21" below. The candidates are roughly
   ordered by readiness (most ready first); each has independent
   prerequisites listed.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*.jsonl` continue across sessions (Sessions 8-20
   precedent). The S20 row-377 dedupe is part of operator-WIP;
   operator may want to dedupe other rows pre-emptively before
   S21 opens to avoid Phase 4 pre-push halts.

3. **barcada-drift AI/ML alignment** — if operator wants to ship
   `barcada-drift` (CLASSIFICATION_ADJACENT_PLAN.md §Item 8) in
   S21, the 4 AI/ML team decisions (drift metric definition;
   alert threshold; canary curation; action-on-drift) need to
   be pre-resolved going into S21 or the prompt has to scope
   barcada-drift narrowly (e.g., per-domain agreement only as
   the placeholder metric, with explicit AI/ML-to-tune notes).

---

## Notes for Session 21

Suggested S21 scope candidates (operator picks at S21 open):

### Candidate A: `barcada-drift` skeleton (if AI/ML decisions ready)

Per CLASSIFICATION_ADJACENT_PLAN.md §Item 8. Consumes the
`canary_runs/<date>.parquet` artifacts the S20 launchd job
produces. Needs AI/ML team alignment on 4 decisions (drift
metric / alert threshold / canary curation / action-on-drift)
before the CLI shape can be committed to. Estimated ~300 LOC
per the plan estimate. Schema-compatible with S20's
`tools.baseline_v0.canary.PARQUET_COLUMNS` (stable tuple).

Prereqs:
- 2+ `canary_runs/*.parquet` files exist (the launchd job must
  have fired at least twice). At earliest 2026-06-06 (two
  Saturdays from S20 close at 2026-05-23) assuming operator
  installs the launchd kit immediately and the job runs cleanly.
- AI/ML team responses on §Item 8 decisions OR explicit
  operator-side placeholder choices with "AI/ML-to-tune" notes.

### Candidate B: Per-tier cost-accounting retrofit (closes Workstream 0)

The deferred-from-S14 per-tier cost-accounting wiring gap.
Currently severity LOW, carry-forward. Closing it would let
`workstream-0-end` tag be placed at the closing commit. Touches
the W4.1.5 driver area (tests/runners/fixture_cascade/) which
is locked except via W5.X-prefix commits per S16 precedent.
Estimated 100-200 LOC.

Prereqs:
- W5.X-prefix commit authorization at S21 Phase 1 design-gate.
- Decision on whether the retrofit touches stage1/2/3 cost
  fields, evidence_cost_usd, or both.

### Candidate C: W A robots.txt parser (W A.1)

Per plan §4 Week 8. The robots.txt parser the cassettes work
(Q2.3) intentionally pre-empted with a standalone
urllib.robotparser-based gate. W A.1 ships the production
robots parser used by `barcada-scrape` and the future
`barcada-drift`. Estimated 400-600 LOC across parser + tests +
integration.

Prereqs:
- Plan §4 W8 read at S21 Phase 1.
- Decision on whether to reuse the S20 cassette-side gate as
  a sibling-import or refactor both to a shared module.

### Candidate D: Phase 4 PR-D operator-led labeling (unblocked elsewhere)

Per plan §11 Risk Register entry "Phase 4 measurement half
blocked on operator-led labeling". Stage 2 + Stage 3 labeling
gates PR-D/E/F/G. This is operator territory; Claude Code
support would be limited to tooling around the labeling
workflow (validators, batch-import scripts, etc.) rather than
the labeling itself.

Prereqs:
- Operator-scheduled labeling effort.
- No code work for Claude Code unless tooling is requested.

### Candidate E: Cassette corpus expansion / additional fixtures

S20 shipped 20 cassettes from canary_50 known-good + tech
subsets. Plan §4 W7 line 314 cites "~20-30 representative
domains" — current 20 is the lower bound. Could expand to 30
adding more business-classification-interesting domains, OR
add cassettes for the bot-blocked / non-English / dead subsets
of canary_50 (each exercises a different code path in the
future replay-against-pipeline integration). Estimated zero
LLM cost; maybe ~30 min runtime.

Prereqs:
- Decision on which subset(s) to expand into.
- Operator review of S20's FP-curation log (archive.org +
  hashicorp.com flagged as SaaS-shell FPs — could drop or
  re-record under a different UA to investigate).

---

## Required reading (Session 21 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 20 entry — full 8-commit
   narrative; Phase 4 eval_data WIP halt + resolution;
   forward-applicable patterns.
3. **`LESSONS.md`** — operator patterns. Session 20 landed 7
   new sections (folded S19's 6 forward-applicable patterns
   per SR-7 amendment + 1 S20-specific eval_data-WIP-halt
   pattern). Read end-of-file additions.
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope
   section per Session 21 candidate choice. Plan is READ-ONLY.
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A (barcada-drift) is chosen.

---

## Outstanding items carried forward to Session 21+

1. **Per-tier cost-accounting wiring gap** — carry-forward
   from S14; severity LOW. Acceptance criterion 11 in S20
   prompt acknowledged this as DEFERRED. Closing it would
   justify `workstream-0-end` tag placement.

2. **`barcada-drift` CLI** — CLASSIFICATION_ADJACENT_PLAN.md
   §Item 8; 4 AI/ML team decisions outstanding (drift metric;
   alert threshold; canary curation; action-on-drift). S20
   shipped `barcada-baseline canary-run` as the data-collection
   layer per Q1.1 = (A); drift orchestration layer defers.

3. **S20 prompt-amendments carry-forward (3 items)** for the
   next prompt template revision:
   - MF-1 driver_sha prefix-match instead of full-SHA assertion
   - MF-2 Q1.1 option (B) wording cleanup
   - SR-8 Phase 1 HALT condition tightening (only option B
     blocks on AI/ML team)

4. **Cassette corpus expansion** — current 20 domains is lower
   bound of plan's "~20-30". Could expand or curate.

5. **Cassette-FP investigation** — archive.org + hashicorp.com
   flagged as SaaS-shell FPs in S20's FP-curation log. Could
   investigate whether these are detector misfires or genuine
   minimal-shell pages.

6. **launchd kit smoke-then-install** — operator should run
   `scripts/launchd/install_canary_schedule.sh` to enable the
   weekly job. The S20 commit ships files only; no launchctl
   bootstrap was invoked.

7. **Phase 4 PR-D/E/F/G** (forward look; not S20 scope) —
   opens after Workstream 0 fully closes AND operator-led
   Stage 2 + Stage 3 labeling work begins.

---

## Locked artifact reminders for Session 21

Carry-forward from Sessions 8-20:

- `eval_data/` — labeling-workstream territory. Operator-WIP
  edits across sessions are expected (Sessions 8-20 precedent).
  Pre-push validate_consistency runs against WT state; if it
  blocks on operator-WIP not introduced by the session, surface
  per LESSONS pattern (don't auto-fix).
- `stage1.schema.json` v1.0 with 49 keywords.
- `pre-remediation-2026-05-19` tag.
- `baseline-v0` tag at `9e9a1fb`.
- All `workstream-0-*` tags at their placed SHAs.
- `tests/runners/fixture_cascade/` — W4.1.5 driver locked at
  dd64963 except via W5.X-prefix commits.
- `tests/fixtures/baseline-v0/` snapshot — locked at `9e9a1fb`;
  re-capture not authorized.
- `tools/baseline_v0/check.py`, `generate.py`, `determinism.py`
  — Session 19 + 18 deliverables; locked.
- `tools/baseline_v0/canary.py` — Session 20 deliverable;
  locked at `aa405e3` impl + `7236575` tests.
- `tools/synthetic_crawl/` — Session 20 deliverable; locked
  at `abfe803` skeleton + `6b9a025` driver + `c8bc116` tests.
- `tests/fixtures/synthetic_crawls/` — Session 20 corpus; locked.
- `scripts/launchd/` — Session 20 deliverable; locked.
- `docs/phase4_implementation_plan.md` — Phase 4 PR-D/E/F/G
  governance reference; do NOT modify until Phase 4 work is
  operator-authorized.
- Production code under `src/barcada_scraper/` — locked unless
  Phase 2 design-gate explicitly authorizes a specific module.
- All `.claude/rules/*.md` and `CLAUDE.md` — operator
  preferences; honored every commit.

---

## Combined-suite-at-Session-21-open baseline

```
.venv/bin/python -m pytest \
    tests/scraper/test_fixture_conformance.py \
    tests/runners/fixture_cascade/ \
    tests/baseline_v0/ \
    tests/synthetic_crawl/ -q
# Expected: 388 passed / 0 failed / 0 skipped
```

Sub-totals: 210 conformance + 46 driver + 99 baseline_v0 + 33
synthetic_crawl. Cumulative-test-count gate (per S20 prompt):
the count NEVER decreases between commit boundaries; any
decrease indicates regression.

---

## Pre-push gate at Session 21 open

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 341+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

Note on gate 4: validate_consistency runs against working-tree
state; if operator-WIP in eval_data introduces a schema
violation between S20 close and S21 open, the gate will block
even though no S21 commit touches eval_data. Per LESSONS:
surface to operator with the row+detail, propose operator-fix
or stash-and-restore; do NOT auto-fix.

---

## Context-window awareness

Session 20 ran cleanly within context window. Session 21 should
budget similarly:

- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore
  subagent if any module audit requires reading >3 files.
- For any live-HTTP corpus work, pilot with 1-3 cassettes for
  early validation before full N-domain run (S18 + S20 staged-
  rollout pattern).

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S21 scope closes,
  transition per "no mid-commit-batch transitions" — finish
  in-flight sub-surface, then close session and refill the
  transition template for Session 22.

---

## Reporting in chat at session close

Same pattern as Sessions 13-20:

1. Commit SHA(s) of each Session 21 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 388 baseline → S21 close.
4. Driver suite count (46/46 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (including whether `workstream-0-end`
   lands if per-tier cost-accounting closes).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 20 handoff template. Refill at Session 21 close
for Session 22.
