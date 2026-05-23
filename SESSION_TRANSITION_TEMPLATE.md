# Session Transition Template — Handoff from Session 21 → Session 22

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-21 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 22 invocation prompt:** `~/crawler-audit/SESSION_22_PROMPT.md`
(drafted at Session 21 close; mirrored at
`~/Downloads/session-22-prompt.md` for operator-invocation
convenience). The prompt is scope-agnostic at Phases 0/1 and elicits
scope-specific design gates at Phase 2 per chosen candidate. The
S21 carry-forward corrections (workspace Phase 0 anchor pinned to
`332f390`; parser-API stability HALT-condition baked into Step 0.9;
Candidate F prereqs include Q-C.4 deferred-from-S21 framing) are
folded directly. Re-read it on session open. Candidate F (W A.1
integration) is the natural follow-on; A/B/D/E carry forward
unchanged from S21 prompt.

---

## Handoff metadata

- Outgoing session number: 21
- Closing date: 2026-05-23
- Outgoing session scope: W A.1 W8 robots.txt parser (Parser-only
  scope per Sub-question 1.C-SCOPE). One per-module commit
  (`34a59b6 WA1.W8.robots-parser`) shipping
  `src/barcada_scraper/scraper/robots.py` (282 LOC) + 32 tests in
  `tests/scraper/test_robots.py` (368 LOC). API: `RobotsPolicy`
  per-host-cached parser exposing
  `check(url) -> (allowed, reason, crawl_delay)`. Integration with
  `link_discovery.py` + cost-journal bypass marker DEFERRED to
  Session 22+ per Parser-only scope. LLM spend: $0.
- Reason for transition: S21 single-commit scope completed cleanly;
  no in-flight sub-surface. Workstream 0 close + the 4 remaining
  S20-handoff candidates (A barcada-drift / B per-tier cost-
  accounting / D Phase 4 PR-D tooling / E cassette corpus
  expansion) are unchanged carry-forward. NEW carry-forward: Full-
  W8 integration to ship `link_discovery.py` consumption of
  `RobotsPolicy` + cost-journal bypass marker (W8 plan bullets
  4-5), which closes W A.1 fully and unblocks
  `workstream-a-week1-end` tag placement.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `34a59b6` (WA1.W8.robots-parser).
- Last commit subject: "WA1.W8.robots-parser:
  src/barcada_scraper/scraper/robots.py + tests/scraper/test_robots.py
  (parser-only scope per S21 1.C-SCOPE)"
- Branch sync with `origin/main`: 0 ahead / 0 behind (verified at
  Session 21 close after push).
- Tags (do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3`
  - `workstream-0-week1-end` at `4f9d23f`
  - `workstream-0-week2-end` at `e5d2f91`
  - `workstream-0-week3-end` at `cf0c14c`
  - `workstream-0-week4-1-5-end` at `dd64963` (annotated `f9be833a`)
  - `workstream-0-week4-end` at `b2e2671` (annotated `c3c6fb74`)
  - `workstream-0-week5-end` at `ddd3cb0` (annotated `fc1ae2ff`)
  - `baseline-v0` at `9e9a1fb` (annotated `7839c164`)
  - `workstream-0-week7-end` at `ea37102` (annotated; placed S20)
  - **NO new tag at S21 close** (deferred per 1.TAG; Parser-only
    scope does not warrant `workstream-a-week1-end`).
- Pre-push gate state at HEAD `34a59b6`: ALL CHECKS PASS (ruff +
  ruff format + vermin 3.10 + validate_consistency 0/0).
- Unstaged changes intentionally ignored across sessions (operator-
  side work in the locked tree):
    eval_data/README.md
    eval_data/TAXONOMY_GAP_LOG.md
    eval_data/stage1_labels.jsonl
  Routinely unstaged through Sessions 8-21. No eval_data WIP halt
  fired at S21 Phase 4 (rows remained schema-valid).
- Corpus: 222 .html fixtures (unchanged from Session 17 close).
- 202 expected.json files (unchanged).
- 222 meta.json files (unchanged).
- 1213 baseline-v0 files (unchanged from Session 18 close at `9e9a1fb`).
- NEW Session 21: `src/barcada_scraper/scraper/robots.py` (282 LOC).
  Production `RobotsPolicy` parser; per-host cache; Crawl-delay
  honored; stdlib `urllib.robotparser` backed; injectable fetcher
  for testability.
- NEW Session 21: `tests/scraper/test_robots.py` (368 LOC; 32 tests).
- (Unchanged from S20 close, all locked):
    - `tools/synthetic_crawl/` package (4 files)
    - `tools/baseline_v0/canary.py` (274 LOC)
    - `tests/synthetic_crawl/` package (3 files; 33 tests)
    - `tests/baseline_v0/test_canary.py` (17 tests + 6 dispatch)
    - `tests/fixtures/synthetic_crawls/` (20 cassettes + 20 sidecars)
    - `scripts/launchd/` kit (5 files)
- Combined test suite at HEAD `34a59b6`: 420 passed / 0 failed /
  0 skipped (210 conformance + 46 driver + 99 baseline_v0 + 33
  synthetic_crawl + 32 robots = 420).

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 21 start: `0640939` (S21 prompt-
  amendment v4; 3 commits ahead of the prompt's expected `dccab29`
  due to between-session prompt-amendment work; authorized at
  Phase 0 per S20 precedent).
- Session 21 close-out workspace commits (1, pushed):
  - `635b4a4` "Session 21 close-out: SESSION_LOG.md append +
    LESSONS.md fold-in + TRANSITION refill" — SESSION_LOG.md
    S21 append +222; LESSONS.md +102 across 5 new sections;
    this template refilled.
- **Last commit SHA at Session 21 CLOSE: `635b4a4`.** S22 prompt's
  Phase 0 Step 0.1 MUST anchor workspace expectation to `635b4a4`,
  NOT chain forward from `dccab29` or `0640939` (which would
  spuriously surface a 4-commit-delta HALT on S22 open).
- Branch sync with `origin/main`: 0 ahead / 0 behind (verified
  at Session 21 close after push).

---

## Session 22 execution order (enforce strict sequence)

Same N-phase shape applies regardless of scope choice (Phase 0
cold-start verify → Phase 1 scope → Phase 2 design-gate → Phase 3
impl → Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 22 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 21 entry.
3. Reading the LESSONS.md additions Session 21 landed (5 new
   sections at end of file).
4. Reading the relevant section of BARCADA_CRAWLER_
   REMEDIATION_PLAN.md for the chosen Session 22 scope (see
   "Notes for Session 22" below).
5. Reading `~/crawler-audit/SESSION_22_PROMPT.md` end-to-end
   (drafted at S21 close; ~1027 lines). It encodes the strict
   7-phase ordering with halt-on-mismatch, the 9-step Phase 0
   verification (incl. Step 0.9 parser API surface stability
   check for Candidate F), the per-candidate Phase 2 design-gate
   templates (F new + A/B/D/E carry-forward), and the full
   regression-protection checklist locking S19/S20/S21
   deliverables.
6. Running Phase 0 cold-start verification per that prompt's
   protocol.

---

## Outstanding operator-input requests entering Session 22

1. **Session 22 scope choice** — pick from the candidates in
   "Notes for Session 22" below. The S21-handoff candidates
   A/B/D/E carry forward (Candidate C now shipped); a NEW
   candidate F (Full-W8 integration of `RobotsPolicy`) opened
   this session.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*.jsonl` continue across sessions (Sessions 8-21
   precedent). S21 had no eval_data WIP halt; rows remained
   schema-valid throughout.

3. **barcada-drift AI/ML alignment** — unchanged from S21
   handoff. If operator wants to ship `barcada-drift` in S22,
   the 4 AI/ML team decisions (drift metric / alert threshold
   / canary curation / action-on-drift) need to be pre-resolved
   OR scoped narrowly with placeholders.

4. **launchd kit installation** — S20 shipped
   `scripts/launchd/install_canary_schedule.sh` as files-only;
   operator should run the installer when ready to enable the
   weekly Saturday-9am canary job. Required prerequisite for
   Candidate A (barcada-drift needs 2+ `canary_runs/*.parquet`
   artifacts to exist).

---

## Notes for Session 22

Suggested S22 scope candidates (operator picks at S22 open):

### Candidate F (NEW): Full-W8 integration of `RobotsPolicy`

The natural follow-on to S21's Parser-only ship. Closes
acceptance criterion 4 from the S21 Candidate C set and warrants
the `workstream-a-week1-end` tag at the closing commit.

Scope (per W8 plan §5 Action #2 bullets 4-5):
- Integrate `barcada_scraper.scraper.robots.RobotsPolicy` into
  `link_discovery.py` (or equivalent fetcher seam) — gate URLs
  before they enter the crawl queue.
- Cost-journal authorization-marker: when a per-domain bypass is
  configured, log the explicit authorization to the cost journal
  so audit trails capture "this fetch ignored robots.txt because
  …". Plan calls for "explicit per-domain configurable that logs
  an authorization marker."
- `CRAWLING_POLICY.md` documentation (W8 plan bullet 5) —
  separate document or section per operator preference.
- Tests: integration tests against fixtures/cassettes; bypass-
  marker tests against cost-journal asserter.

Estimated 150-250 LOC (parser already exists; this is wiring +
docs + tests).

Prereqs:
- **Parser API surface stability** between S21 close and S22 open.
  The integration design assumes the S21-shipped public API at
  `34a59b6` (`RobotsPolicy(user_agent, timeout, fetcher).check(url)
  -> RobotsDecision(allowed, reason, crawl_delay)` + frozen
  `RobotsFetchResult` + `RobotsFetcher` type alias +
  `DEFAULT_ROBOTS_TIMEOUT = 10.0`) holds unchanged. If any patch
  to `src/barcada_scraper/scraper/robots.py` lands before S22
  open (e.g., a v1.1 parser change), the integration design
  needs re-derivation at S22 Phase 2 — surface as a HALT at
  Phase 0 if the file's SHA differs from `34a59b6`'s tree.
- **Q-C.4 deferred-from-S21**: S21 chose the pure check API
  ("returns `(allowed, reason, crawl_delay)`; caller decides
  skip vs warn") and explicitly deferred the bypass mechanism's
  cost-journal coupling. S22 Phase 2 design-gate MUST resume
  this as a *known carry-forward* (not a fresh question): how
  the bypass-config mechanism couples to the existing cost-
  journal authorization-marker surface, and where the marker
  literal is written (per-row in stage{1,2,3}_decision? a new
  journal field?).
- Decision on bypass-config mechanism (env var / config file /
  CLI flag / per-domain JSON) — pre-resolves the bypass surface
  before the cost-journal coupling lands.
- Decision on where the integration plugs in (existing fetcher
  seam location must be source-verified at Phase 0; candidates
  are `link_discovery.py` per plan §5 Action #2 OR a new shim
  module if `link_discovery.py` lives in a less-touchable area).
- `CRAWLING_POLICY.md` content scope (full vs minimal-first).

### Candidate A: `barcada-drift` skeleton (if AI/ML decisions ready)

Unchanged from S21 handoff. Per CLASSIFICATION_ADJACENT_PLAN.md
§Item 8. Consumes `canary_runs/<date>.parquet` artifacts the S20
launchd job produces. Needs AI/ML team alignment on 4 decisions
OR explicit placeholders. Estimated ~300 LOC. **Now blocked also
by**: 2+ parquet files needing to exist (launchd installer not
yet run as of S21 close; earliest natural data 2026-06-06).

### Candidate B: Per-tier cost-accounting retrofit (closes Workstream 0)

Unchanged from S21 handoff. The deferred-from-S14 per-tier cost-
accounting wiring gap. Currently severity LOW, carry-forward.
Closing it would let `workstream-0-end` tag be placed at the
closing commit. Touches the W4.1.5 driver area (locked except
via W5.X-prefix commits). Estimated 100-200 LOC.

### Candidate D: Phase 4 PR-D operator-led labeling (operator territory)

Unchanged from S21 handoff. Tooling support only; labeling
itself is operator territory.

### Candidate E: Cassette corpus expansion / additional fixtures

Unchanged from S21 handoff. S20 shipped 20 cassettes; plan's
upper bound is 30. Could expand or curate.

---

## Required reading (Session 22 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 21 entry — single-commit narrative;
   the 2 mid-implementation stdlib-quirk test failures and
   resolutions; 5 forward-applicable patterns.
3. **`LESSONS.md`** — 5 new sections appended at S21 close
   ("Library-quirk patterns" / "Workspace HEAD delta tolerance" /
   "Single-module Phase 3 commit collapse" / "Explore-subagent +
   spot-check for Phase 2 source-verify" / "Sibling-module style
   disclosure").
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope
   section per Session 22 candidate choice. Plan is READ-ONLY.
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A (barcada-drift) is chosen.
6. **`src/barcada_scraper/scraper/robots.py`** — only if Candidate
   F (Full-W8 integration) is chosen. The API surface
   (`RobotsPolicy.check`, `RobotsDecision`) is what callers
   integrate against.

---

## Outstanding items carried forward to Session 22+

1. **Per-tier cost-accounting wiring gap** — carry-forward from
   S14; severity LOW. Unchanged disposition.

2. **`barcada-drift` CLI** — CLASSIFICATION_ADJACENT_PLAN.md
   §Item 8; 4 AI/ML team decisions outstanding. Unchanged.

3. **W A.1 robots.txt parser integration** — NEW from S21.
   `RobotsPolicy` ships at `src/barcada_scraper/scraper/robots.py`
   but is not yet consumed by `link_discovery.py` /
   `barcada-scrape` fetcher seam. Bypass mechanism +
   cost-journal authorization marker (W8 plan bullets 4-5)
   pending. Closing this places `workstream-a-week1-end` tag.

4. **`CRAWLING_POLICY.md` document** — W8 plan bullet 5; not yet
   authored. Likely lands as part of Candidate F.

5. **Cassette corpus expansion** — current 20 domains is lower
   bound of plan's "~20-30". Unchanged.

6. **Cassette-FP investigation** — archive.org + hashicorp.com
   flagged as SaaS-shell FPs in S20's FP-curation log. Unchanged.

7. **launchd kit smoke-then-install** — Unchanged from S21
   handoff. Operator should run
   `scripts/launchd/install_canary_schedule.sh` to enable the
   weekly job. Required for Candidate A.

8. **Phase 4 PR-D/E/F/G** (forward look) — Unchanged. Opens
   after Workstream 0 fully closes AND operator-led Stage 2 +
   Stage 3 labeling work begins.

---

## Locked artifact reminders for Session 22

Carry-forward from Sessions 8-21:

- `eval_data/` — labeling-workstream territory. Operator-WIP
  edits across sessions are expected. Pre-push validate_
  consistency runs against WT state; surface per LESSONS pattern
  if blocked.
- `stage1.schema.json` v1.0 with 49 keywords.
- `pre-remediation-2026-05-19` tag.
- `baseline-v0` tag at `9e9a1fb`.
- All `workstream-0-*` tags at their placed SHAs (9 tags total
  at S21 close; unchanged from S20).
- `tests/runners/fixture_cascade/` — W4.1.5 driver locked at
  dd64963 except via W5.X-prefix commits.
- `tests/fixtures/baseline-v0/` snapshot — locked at `9e9a1fb`.
- `tools/baseline_v0/check.py`, `generate.py`, `determinism.py`,
  `canary.py` — S18-20 deliverables; locked.
- `tools/synthetic_crawl/` package — S20 deliverable; locked.
- `tests/fixtures/synthetic_crawls/` — S20 corpus; locked.
- `scripts/launchd/` — S20 deliverable; locked.
- **NEW**: `src/barcada_scraper/scraper/robots.py` — S21
  deliverable; locked at `34a59b6`. Future Full-W8 integration
  consumes this module's public API but does not modify it.
- **NEW**: `tests/scraper/test_robots.py` — S21 deliverable;
  locked at `34a59b6`.
- `docs/phase4_implementation_plan.md` — Phase 4 governance
  reference; do NOT modify until Phase 4 work is operator-
  authorized.
- Production code under `src/barcada_scraper/` — locked unless
  Phase 2 design-gate explicitly authorizes a specific module.
  S21 authorized `scraper/robots.py`; that authorization does
  not extend to other src/ modules.
- All `.claude/rules/*.md` and `CLAUDE.md` — operator
  preferences; honored every commit.

---

## Combined-suite-at-Session-22-open baseline

```
.venv/bin/python -m pytest \
    tests/scraper/test_fixture_conformance.py \
    tests/runners/fixture_cascade/ \
    tests/baseline_v0/ \
    tests/synthetic_crawl/ \
    tests/scraper/test_robots.py -q
# Expected: 420 passed / 0 failed / 0 skipped
```

Sub-totals: 210 conformance + 46 driver + 99 baseline_v0 + 33
synthetic_crawl + 32 robots = 420. Cumulative-test-count gate:
the count NEVER decreases between commit boundaries.

---

## Pre-push gate at Session 22 open

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 343+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

Note on gate 4: validate_consistency runs against working-tree
state; if operator-WIP in eval_data introduces a schema
violation between S21 close and S22 open, the gate will block
even though no S22 commit touches eval_data. Per LESSONS:
surface to operator with the row+detail, propose operator-fix
or stash-and-restore; do NOT auto-fix.

---

## Context-window awareness

Session 21 ran well within context window (single-commit scope;
Explore subagent + spot-checks at Phase 2; minimal mid-
implementation iteration). Session 22 should budget per chosen
candidate:

- Candidate F (Full-W8 integration): likely ~150-250 LOC + docs.
  Single mid-sized session.
- Candidate B (per-tier cost-accounting): touches W4.1.5 area;
  more careful Phase 0 verification needed.
- Candidate A (barcada-drift): only if launchd job has run ≥2
  times AND AI/ML decisions ready.

Strategies (unchanged from S21 prompt):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-HTTP corpus work, pilot 1-3 before full N-domain.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S22 scope closes,
  transition per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-21:

1. Commit SHA(s) of each Session 22 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 420 baseline → S22 close.
4. Driver suite count (46/46 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (including whether `workstream-a-week1-end`
   lands if Candidate F closes W A.1).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 21 handoff template. Refill at Session 22 close
for Session 23.
