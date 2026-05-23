# Session Transition Template — Handoff from Session 22 → Session 23

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-22 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 23 invocation prompt:** to be drafted at operator request
between sessions per S20→S21 and S21→S22 precedent. Drafting the
next-session prompt is operator-commissioned, NOT a built-in Phase 6
step. If the operator does not commission a draft, Session 23 can
either operator-commission at S23 open or scope out a fresh prompt
at S23 open.

---

## Handoff metadata

- Outgoing session number: 22
- Closing date: 2026-05-23
- Outgoing session scope: W A.1 W8 integration (Candidate F per
  S22 Phase 1). 4 per-module commits per Q-SHARED.1:
  `ba87e7e WA1.W8.robots-gate-shim`,
  `381ee89 WA1.W8.robots-bypass-config-loader`,
  `1d9404e WA1.W8.cost-journal-bypass-log`,
  `fdc8a7a WA1.W8.crawling-policy-doc`. Closes W A.1 fully.
  Annotated tag `workstream-a-week1-end` placed at `fdc8a7a`.
  LLM spend: $0.
- Reason for transition: S22 4-commit scope completed cleanly;
  W A.1 closed with tag placed. No in-flight sub-surface. The
  natural follow-ons are (a) W A.2 worker_loop / fetcher_core
  integration of `RobotsGate` (closes the orchestrator wiring
  S22 explicitly deferred at Q-F.1), or (b) the carry-forward
  candidates from S21/S22 (per-tier cost-accounting / barcada-
  drift / Phase 4 PR-D tooling / cassette corpus expansion).

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `fdc8a7a` (WA1.W8.crawling-policy-doc).
- Last commit subject: "WA1.W8.crawling-policy-doc:
  docs/CRAWLING_POLICY.md (minimal-first scope per S22 Q-F.6;
  robots compliance only)"
- Branch sync with `origin/main`: 0 ahead / 0 behind (verified at
  Session 22 close after push).
- Tags (10 total; do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3`
  - `workstream-0-week1-end` at `4f9d23f`
  - `workstream-0-week2-end` at `e5d2f91`
  - `workstream-0-week3-end` at `cf0c14c`
  - `workstream-0-week4-1-5-end` at `dd64963` (annotated)
  - `workstream-0-week4-end` at `b2e2671` (annotated)
  - `workstream-0-week5-end` at `ddd3cb0` (annotated)
  - `baseline-v0` at `9e9a1fb` (annotated)
  - `workstream-0-week7-end` at `ea37102` (annotated)
  - **NEW S22**: `workstream-a-week1-end` at `fdc8a7a`
    (annotated; placed S22). Closes W A.1 (parser S21 +
    integration S22).
- Pre-push gate state at HEAD `fdc8a7a`: ALL CHECKS PASS (ruff +
  ruff format + vermin 3.10 + validate_consistency 0/0).
- Unstaged changes intentionally ignored across sessions
  (operator-side work in the locked tree):
    eval_data/README.md
    eval_data/TAXONOMY_GAP_LOG.md
    eval_data/stage1_labels.jsonl
  Routinely unstaged through Sessions 8-22. No eval_data WIP halt
  fired at S22 Phase 4 (rows remained schema-valid).
- Corpus: 222 .html fixtures (unchanged from S17 close).
- 202 expected.json files (unchanged).
- 222 meta.json files (unchanged).
- 1213 baseline-v0 files (unchanged from S18 close at `9e9a1fb`).
- NEW Session 22:
    - `src/barcada_scraper/scraper/robots_gate.py` (339 LOC;
      shim wrapping `RobotsPolicy` with bypass + drift signal +
      configurable Crawl-delay).
    - `src/barcada_scraper/scraper/robots_bypass_config.py`
      (178 LOC; per-domain JSON sidecar loader).
    - `tests/scraper/test_robots_gate.py` (427 LOC; 30 tests).
    - `tests/scraper/test_robots_bypass_config.py` (299 LOC;
      30 tests).
    - `docs/CRAWLING_POLICY.md` (202 lines / 8.1 KB; robots
      compliance only per Q-F.6 minimal-first).
- MODIFIED Session 22:
    - `src/barcada_scraper/classifier/pipeline/cost_journal.py`
      (+50 LOC; new `BypassAuditEntry` dataclass + new
      `JournalState.robots_bypass_log` field + new
      `with_robots_bypass_appended` method + serialization +
      back-compat from_dict).
    - `tests/classifier/pipeline/test_cost_journal.py` (+208
      LOC; 14 new tests + 1 existing updated for new dict key).
- (Unchanged from S21 close, all locked):
    - `src/barcada_scraper/scraper/robots.py` (282 LOC; S21
      parser; public API at `34a59b6`)
    - `tests/scraper/test_robots.py` (32 tests; pins stdlib
      quirks)
    - `tools/synthetic_crawl/` package (4 files)
    - `tools/baseline_v0/canary.py` (274 LOC)
    - `tests/synthetic_crawl/` package (3 files; 33 tests)
    - `tests/baseline_v0/test_canary.py` (17 tests + 6 dispatch)
    - `tests/fixtures/synthetic_crawls/` (20 cassettes + 20
      sidecars)
    - `scripts/launchd/` kit (5 files)
- Combined test suite at HEAD `fdc8a7a`:
    - 538 passed / 0 failed / 0 skipped when the test list
      includes classifier/pipeline/test_cost_journal*.
    - 480 passed / 0 failed / 0 skipped when restricted to the
      S22 prompt's headline suite paths
      (scraper/test_fixture_conformance + runners/fixture_cascade
      + baseline_v0 + synthetic_crawl + scraper/test_robots +
      scraper/test_robots_gate + scraper/test_robots_bypass_config
      = 210 + 46 + 99 + 33 + 32 + 30 + 30 = 480).
    - For S23 Phase 0 baseline, use 480 (matches the headline-
      suite convention from S22 prompt + adds the 2 new S22
      sub-surfaces). 538 is the broader figure including
      classifier/pipeline ride-along — useful when S23 touches
      cost_journal.py or related modules.

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 22 start: `190e75b` (S22 prompt
  audit; 2 commits ahead of the prompt's expected `332f390` due
  to between-session prompt-drafting + audit work; authorized at
  Phase 0 per S20/S21 precedent).
- Session 22 close-out workspace commits will be 1 (pushed):
  workspace SESSION_LOG.md append + LESSONS.md fold-in
  (5 new sections) + this template refilled.
- **Last commit SHA at Session 22 CLOSE: `acf86c5`** (S22 close-
  out follow-up; pins the workspace anchor SHA for S23). The
  immediate parent `dbba7bd` is the original close-out commit
  (SESSION_LOG append + LESSONS fold-in + this template's first-
  pass refill); `acf86c5` is the post-audit follow-up commit
  that pinned this SHA. **S23 prompt's Phase 0 Step 0.1 MUST
  anchor workspace expectation to `acf86c5`**, NOT chain forward
  from `190e75b` (S22 start; would spuriously surface a
  3-commit-delta HALT on S23 open) and NOT from `dbba7bd` (would
  surface a 1-commit-delta HALT). Workspace HEAD delta tolerance
  (LESSONS) handles N prompt-drafting commits between sessions,
  but the anchor itself should always point at the most recent
  close-out commit.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected
  after Session 22 close push.

---

## Session 23 execution order (enforce strict sequence)

Same N-phase shape applies regardless of scope choice (Phase 0
cold-start verify → Phase 1 scope → Phase 2 design-gate → Phase 3
impl → Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 23 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 22 entry.
3. Reading the LESSONS.md additions Session 22 landed (5 new
   sections at end of file, "S22 folding" suffix).
4. Reading the relevant section of BARCADA_CRAWLER_
   REMEDIATION_PLAN.md for the chosen Session 23 scope (see
   "Notes for Session 23" below).
5. Reading the Session 23 prompt if one has been drafted, OR
   commissioning a fresh draft at S23 open.
6. Running Phase 0 cold-start verification per the prompt's
   protocol (or per the S22 prompt template if S23 prompt is
   not yet drafted).

---

## Outstanding operator-input requests entering Session 23

1. **Session 23 scope choice** — pick from the candidates in
   "Notes for Session 23" below. W A.1 closed at S22; the
   natural follow-on is W A.2 (orchestrator wiring of
   `RobotsGate` into `worker_loop` / `fetcher_core`), but the
   carry-forward candidates A/B/D/E are also available.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*.jsonl` continue across sessions (Sessions 8-22
   precedent). S22 had no eval_data WIP halt; rows remained
   schema-valid throughout.

3. **barcada-drift AI/ML alignment** — unchanged from S21/S22
   handoff. If operator wants to ship `barcada-drift` in S23,
   the 4 AI/ML team decisions need to be pre-resolved OR scoped
   narrowly with placeholders.

4. **launchd kit installation** — S20 shipped
   `scripts/launchd/install_canary_schedule.sh` as files-only;
   operator should run the installer when ready to enable the
   weekly Saturday-9am canary job. Required prerequisite for
   Candidate A (barcada-drift needs 2+ canary_runs/*.parquet
   artifacts to exist; earliest natural date 2026-06-06 from
   S22 close).

5. **Session 23 prompt draft commissioning** — operator decides
   whether to commission a S23 prompt between sessions or scope
   one at S23 open.

---

## Notes for Session 23

Suggested S23 scope candidates (operator picks at S23 open):

### Candidate G (NEW): W A.2 worker_loop / fetcher_core integration

The natural follow-on to S22's shim-only Q-F.1 choice. Wires
`barcada_scraper.scraper.robots_gate.RobotsGate` into the
orchestrator so URLs are actually gated before fetch_one fires.

Scope:
- Resolve the sync-RobotsPolicy vs. async-fetcher_core impedance
  mismatch (S22 Q-F.1 explicitly deferred this). Two paths:
  (a) make `RobotsPolicy.check` async (or add an async wrapper)
      that uses `httpx.AsyncClient` instead of `requests`,
  (b) keep `RobotsPolicy` sync and call it from worker_loop
      BEFORE entering the async fetcher path (cleaner if the
      crawl-queue is already async/sync at the right boundary).
- Wire `RobotsGate.evaluate(url)` into the right pre-fetch site
  in `worker_loop._acquire_one_domain_t1` (or wherever the
  per-URL fetch decision is made today; verify at S23 Phase 0).
- Wire the bypass-config loader: a CLI flag or env var pointing
  at the per-domain JSON sidecar, loaded once at orchestrator
  startup, handed to the `RobotsGate` constructor.
- Wire the cost-journal `with_robots_bypass_appended` call so
  every `GATE_ACTION_BYPASS_ALLOW` decision actually persists
  the audit record (not just emits the in-memory
  `BypassAuthorization`).
- Tests: at least one integration test that constructs a
  full orchestrator pipeline + gate + journal in tmp_path,
  fires a fetch against a domain with a Disallow + a bypass
  configured, and asserts the bypass entry lands in the journal.

Estimated 200-300 LOC (worker_loop touches + tests).

Prereqs:
- W4.1.5 driver lock at `dd64963` still holds (no W5.X-prefix
  conflict expected).
- S22 deliverables locked: `robots_gate.py`, `robots_bypass_config.py`,
  `cost_journal.py` modifications, `CRAWLING_POLICY.md`. Any
  v1.1 change to those modules between S22 close and S23 open
  invalidates the integration design.
- Decision on which sync/async path (above) before Phase 3.

### Candidate A (carry-forward): `barcada-drift` skeleton

Unchanged from S22 handoff. Per CLASSIFICATION_ADJACENT_PLAN.md
§Item 8. Consumes `canary_runs/<date>.parquet` artifacts.
**Blocked**: 2+ parquet files needed (launchd installer not yet
run as of S22 close; earliest natural data 2026-06-06).
Estimated ~300 LOC.

### Candidate B (carry-forward): Per-tier cost-accounting retrofit

Unchanged from S21/S22 handoff. Closes Workstream 0; warrants
`workstream-0-end` tag. Touches W4.1.5 driver area (locked
except via W5.X-prefix commits). Estimated 100-200 LOC.

### Candidate D (carry-forward): Phase 4 PR-D operator-led labeling

Unchanged. Tooling support only; labeling itself is operator
territory.

### Candidate E (carry-forward): Cassette corpus expansion

Unchanged from S22 handoff. S20 shipped 20 cassettes; plan's
upper bound is 30. Could expand or curate.

### Candidate H (NEW small): CRAWLING_POLICY.md tightening pass

Q-F.6's "minimal-first" estimate cited ~1-2 KB; S22 shipped
8.1 KB. If operator prefers a tighter doc, a small follow-up
session could trim the doc to ~2-3 KB while preserving the
essential robots-compliance contract. Estimated <50 LOC of
doc changes; no code.

---

## Required reading (Session 23 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 22 entry — 4-commit narrative;
   the plan-vs-reality finding at Phase 2; the mid-Phase-3
   implicit-authorization HALT; 5 forward-applicable patterns.
3. **`LESSONS.md`** — 5 new sections appended at S22 close
   (Plan-vs-reality at Phase 2 / Implicit-authorization HALT /
   Parallel-dataclass pattern / Per-module commit scaling /
   Phase-2 estimate-vs-actual disclosure).
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope
   section per Session 23 candidate choice. Plan is READ-ONLY.
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A (barcada-drift) is chosen.
6. **`src/barcada_scraper/scraper/robots_gate.py`** — only if
   Candidate G (W A.2 integration) is chosen. Public API
   (`RobotsGate.evaluate`, `GateDecision`, `BypassEntry`,
   `BypassAuthorization`, `GATE_ACTION_*`) is what worker_loop
   consumes.
7. **`src/barcada_scraper/orchestrator/worker_loop.py`** — only
   if Candidate G is chosen. The integration site; ~2884 LOC.
8. **`src/barcada_scraper/classifier/page_acquisition/fetcher_core.py`**
   — only if Candidate G is chosen. The async/httpx fetcher
   path; `fetch_one` at line 169.
9. **`docs/CRAWLING_POLICY.md`** — only if Candidate H is chosen
   (doc tightening) or Candidate G needs the operational defaults
   reference.

---

## Outstanding items carried forward to Session 23+

1. **Per-tier cost-accounting wiring gap** — carry-forward from
   S14; severity LOW. Unchanged disposition.

2. **`barcada-drift` CLI** — CLASSIFICATION_ADJACENT_PLAN.md
   §Item 8; 4 AI/ML team decisions outstanding. Blocked also
   on 2+ canary_runs parquet files. Unchanged.

3. **W A.2 robots-gate integration** — NEW from S22. S22 Q-F.1
   shipped the shim only; worker_loop / fetcher_core wiring
   deferred to W A.2 where the sync/async bridge can be
   designed. See Candidate G above.

4. **Cassette corpus expansion** — current 20 domains is lower
   bound of plan's "~20-30". Unchanged.

5. **Cassette-FP investigation** — archive.org + hashicorp.com
   flagged as SaaS-shell FPs in S20's FP-curation log. Unchanged.

6. **launchd kit smoke-then-install** — Unchanged. Operator
   should run `scripts/launchd/install_canary_schedule.sh` to
   enable the weekly job. Required for Candidate A.

7. **Phase 4 PR-D/E/F/G** (forward look) — Unchanged. Opens
   after Workstream 0 fully closes AND operator-led Stage 2 +
   Stage 3 labeling work begins.

8. **CRAWLING_POLICY.md size** — NEW from S22. Doc shipped at
   8.1 KB vs the Q-F.6 ~1-2 KB estimate. See Candidate H above
   if a tightening pass is desired.

---

## Locked artifact reminders for Session 23

Carry-forward from Sessions 8-22:

- `eval_data/` — labeling-workstream territory. Operator-WIP
  edits across sessions are expected. Pre-push validate_
  consistency runs against WT state; surface per LESSONS pattern
  if blocked.
- `stage1.schema.json` v1.0 with 49 keywords.
- `pre-remediation-2026-05-19` tag.
- `baseline-v0` tag at `9e9a1fb`.
- All `workstream-0-*` tags at their placed SHAs (9 tags from
  S20 close; unchanged).
- **NEW**: `workstream-a-week1-end` tag at `fdc8a7a` (placed
  S22; do not move).
- `tests/runners/fixture_cascade/` — W4.1.5 driver locked at
  `dd64963` except via W5.X-prefix commits.
- `tests/fixtures/baseline-v0/` snapshot — locked at `9e9a1fb`.
- `tools/baseline_v0/check.py`, `generate.py`, `determinism.py`,
  `canary.py` — S18-20 deliverables; locked.
- `tools/synthetic_crawl/` package — S20 deliverable; locked.
- `tests/fixtures/synthetic_crawls/` — S20 corpus; locked.
- `scripts/launchd/` — S20 deliverable; locked.
- `src/barcada_scraper/scraper/robots.py` — S21 deliverable;
  locked at `34a59b6`. W A.2 integration consumes the module's
  public API but does not modify it.
- `tests/scraper/test_robots.py` — S21 deliverable; locked at
  `34a59b6`.
- **NEW**: `src/barcada_scraper/scraper/robots_gate.py` — S22
  deliverable; locked at `ba87e7e`. W A.2 integration consumes
  the public API (`RobotsGate.evaluate`, `GateDecision`,
  `BypassEntry`, `GATE_ACTION_*`) but does not modify the shim.
- **NEW**: `src/barcada_scraper/scraper/robots_bypass_config.py` —
  S22 deliverable; locked at `381ee89`.
- **NEW**: `tests/scraper/test_robots_gate.py` — S22 deliverable;
  locked at `ba87e7e`.
- **NEW**: `tests/scraper/test_robots_bypass_config.py` — S22
  deliverable; locked at `381ee89`.
- **PARTIAL NEW**: `src/barcada_scraper/classifier/pipeline/cost_journal.py`
  — S22 touched (BypassAuditEntry + robots_bypass_log + builder).
  The new public API is locked at `1d9404e`. Pre-S22 surfaces
  (CostTotals, ShardRecord, CeilingHistoryEntry, the existing
  builder methods, retry helper, etc.) remain locked as before.
- **NEW**: `docs/CRAWLING_POLICY.md` — S22 deliverable; locked at
  `fdc8a7a`. Future additions (W A.2+) extend the "Out of scope"
  block's deferred sections as they land in code.
- `docs/phase4_implementation_plan.md` — Phase 4 governance
  reference; do NOT modify until Phase 4 work is operator-
  authorized.
- Production code under `src/barcada_scraper/` — locked unless
  Phase 2 design-gate explicitly authorizes a specific module.
  S21+S22 authorized `scraper/robots.py`, `scraper/robots_gate.py`,
  `scraper/robots_bypass_config.py`, and (via S22 mid-Phase-3
  explicit operator authorization) the `BypassAuditEntry` +
  `robots_bypass_log` additions to
  `classifier/pipeline/cost_journal.py`. No other src/ module is
  authorized.
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-23-open baseline

Headline suite (mirrors S22 prompt convention + adds S22's 2 new
sub-surfaces):

```
.venv/bin/python -m pytest \
    tests/scraper/test_fixture_conformance.py \
    tests/runners/fixture_cascade/ \
    tests/baseline_v0/ \
    tests/synthetic_crawl/ \
    tests/scraper/test_robots.py \
    tests/scraper/test_robots_gate.py \
    tests/scraper/test_robots_bypass_config.py -q
# Expected: 480 passed / 0 failed / 0 skipped
```

Sub-totals: 210 conformance + 46 driver + 99 baseline_v0 + 33
synthetic_crawl + 32 robots + 30 robots_gate + 30
robots_bypass_config = 480. Cumulative-test-count gate: the
count NEVER decreases between commit boundaries.

Broader suite (incl. classifier/pipeline ride-along, useful when
S23 touches cost_journal.py):

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
    tests/classifier/pipeline/test_cost_journal_adls.py -q
# Expected: 538 passed / 0 failed / 0 skipped
```

---

## Pre-push gate at Session 23 open

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 347+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

Note on gate 4: validate_consistency runs against working-tree
state; if operator-WIP in eval_data introduces a schema violation
between S22 close and S23 open, the gate will block even though
no S23 commit touches eval_data. Per LESSONS: surface to operator
with the row+detail, propose operator-fix or stash-and-restore;
do NOT auto-fix.

---

## Context-window awareness

Session 22 ran within context window across 4 commits + Phase 2
source-verification + 1 mid-Phase-3 HALT. Session 23 budget per
chosen candidate:

- Candidate G (W A.2 integration): worker_loop is 2884 LOC; even
  with Explore delegation, this is a heavier session than S22.
  Budget for ~200-300 LOC + integration tests + per-module
  commits.
- Candidate B (per-tier cost-accounting): touches W4.1.5 area;
  more careful Phase 0 verification needed.
- Candidate A (barcada-drift): only if launchd job has run ≥2
  times AND AI/ML decisions ready.
- Candidate H (doc tightening): very small; <30 minutes.

Strategies (unchanged from S20-S22 prompts):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-HTTP corpus work, pilot 1-3 before full N-domain.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S23 scope closes,
  transition per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-22:

1. Commit SHA(s) of each Session 23 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 480 baseline → S23 close.
4. Driver suite count (46/46 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (e.g., does S23 warrant a new tag?
   Unlikely for Candidate G alone — that's W A.2, not yet a
   workstream-end milestone).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 22 handoff template. Refill at Session 23 close
for Session 24.
