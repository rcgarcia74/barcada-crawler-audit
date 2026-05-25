# Session Transition Template — Handoff from Session 26 → Session 27

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-26 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

**Session 27 invocation prompt:** not yet drafted at S26 close.
Per the S20→S21..S25→S26 precedent, prompt-drafting is operator-
commissioned between sessions. If commissioned, draft as
`SESSION_27_PROMPT.md` mirroring the S20-S26 7-phase structure.
Anchors:
- Workspace HEAD: this follow-up commit's SHA (primary close-out
  is `6eff137`; the follow-up pinning this anchor IS this commit
  per S21-S25 self-reference precedent).
- Repo HEAD: `2314f5e` (S26 Commit 1 final).
- Canonical baseline: 964 tests (16-path invocation, unchanged
  from S25 close since S26 was doc-only).
- Narrower baseline (used at S26 for Candidate H): 938 tests
  (14-path invocation excluding test_cost_journal_adls.py +
  test_robots_gate_integration.py).
- Primary recommended scope: none — Candidate H closed at S26;
  S27 picks from carry-forwards A/B/D/E/K (J closed S25, H closed
  S26).
- Carry-forward candidates: A (barcada-drift; blocked on parquets),
  B (per-tier cost-accounting retrofit; warrants
  `workstream-0-end`), D (Phase 4 PR-D tooling), E (cassette
  corpus expansion), K (ADLSCostJournal live Azure smoke; NEW
  from S25 handoff).

---

## Handoff metadata

- Outgoing session number: 26
- Closing date: 2026-05-25
- Outgoing session scope: CRAWLING_POLICY.md tightening per S26
  Candidate H. 1 doc-only commit per Q-SHARED.1:
  `2314f5e WA1.W8.crawling-policy-tighten` (8102 -> 2519 bytes,
  69% reduction; -174 / +49 LOC; 938 narrower baseline preserved
  net-zero). Q-H.1 14% over the 2.2 KB cap due to Q-H.3 "both
  audiences" floor — documented in commit body.
  No tag placed (1.TAG = Defer; Candidate H is doc-only, no
  workstream milestone). LLM spend: $0.
- Reason for transition: S26 1-commit scope completed cleanly;
  Candidate H shipped end-to-end with documented Q-H.1 variance.
  Operator authorized Q-H.2-EXT mid-Phase-3 (op-defaults Notes
  col + References collapse) in one AskUserQuestion turn. No
  in-flight sub-surface.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `2314f5e` (WA1.W8.crawling-policy-tighten).
- Last commit subject: "WA1.W8.crawling-policy-tighten:
  docs/CRAWLING_POLICY.md (S26 Candidate H per Q-H.1 ~2 KB tight
  + Q-H.2 4-section trim + Q-H.2-EXT op-defaults Notes col +
  References collapse + Q-H.3 ops+compliance audience; 202 -> 77
  lines, 8102 -> 2519 bytes, 69% reduction; 938 narrower baseline
  preserved)".
- Branch sync with `origin/main`: 0 ahead / 0 behind (verified
  at S26 close after push at HEAD `2314f5e`).
- Tags (10 total; unchanged from S22-S25 close; do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3`
  - `workstream-0-week1-end` at `4f9d23f`
  - `workstream-0-week2-end` at `e5d2f91`
  - `workstream-0-week3-end` at `cf0c14c`
  - `workstream-0-week4-1-5-end` at `dd64963` (annotated)
  - `workstream-0-week4-end` at `b2e2671` (annotated)
  - `workstream-0-week5-end` at `ddd3cb0` (annotated)
  - `baseline-v0` at `9e9a1fb` (annotated)
  - `workstream-0-week7-end` at `ea37102` (annotated)
  - `workstream-a-week1-end` at `fdc8a7a` (annotated; placed S22)
- Pre-push gate state at HEAD `2314f5e`: ALL CHECKS PASS (ruff +
  ruff format + vermin 3.10 + validate_consistency 0/0).
- Pre-S26 unstaged operator territory (Sessions 8-26 precedent —
  expected to stay unstaged across sessions): `eval_data/README.md`,
  `eval_data/TAXONOMY_GAP_LOG.md`, `eval_data/stage1_labels.jsonl`.
  S26 saw NO new operator-side eval_data commits between S25 close
  and S26 open.
- Corpus: 222 .html fixtures (unchanged from S17 close).
- 202 expected.json files (unchanged).
- 222 meta.json files (unchanged).
- 1213 baseline-v0 files (unchanged from S18 close at `9e9a1fb`).
- MODIFIED Session 26 (Commit 1 SHA `2314f5e`):
    - `docs/CRAWLING_POLICY.md` (202 -> 77 lines; 8102 -> 2519
      bytes). Section trims:
        - Crawler identity (22 lines) folded into intro.
        - robots.txt compliance (55 -> 21 lines; preserved
          3-decision tree + first-match-wins + permissive-on-
          failure).
        - Bypass-config policy + 2 subsections (70 -> 21 lines;
          preserved principle + schema + audit-record + ETag
          persistence).
        - Operational defaults (13 -> 9 lines; Notes column
          dropped per Q-H.2-EXT).
        - Out-of-scope (22 -> 4 lines; single sentence + 1-line
          guidance).
        - References (9 -> 4 lines; inline semicolon collapse).
- (Unchanged from S25 close, all locked):
    - All S21-S25 deliverables (32 robots tests + 30 robots_gate +
      30 robots_bypass_config + 43 cost_journal + 13
      cost_journal_local + 19 cost_journal_adls + 35
      robots_integration + 74 vmss_worker + 129 job_runner + 152
      worker_loop + 7 robots_gate_integration + 12
      worker_loop_persistence).
    - `cost_journal_adls.py` (S25 full backend at `835a531`).
    - `_open_cost_journal_for_worker` body (S25 abfss:// dispatch
      at `aed7873`).
    - All scraper/orchestrator surfaces locked per Out-of-scope
      list in SESSION_26_PROMPT.md.
- Combined test suite at HEAD `2314f5e`:
    - **964 passed / 0 failed / 0 skipped** with the 16-path
      canonical invocation (S26 close = S25 close; S26 is
      doc-only, no test count delta).
    - **938 passed / 0 failed / 0 skipped** with the narrower
      14-path invocation used at S26 Phase 3 for Candidate H.
    - 480 / 538 narrower-baselines (S22 era) remain valid for
      future doc-only candidates that don't touch orchestrator
      or journal paths.

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 26 start: `2262eea` (S26 prompt v2
  M-1 arithmetic fix; 2 commits ahead of S25-close-pinned
  `8e6d836` due to prompt-drafting + v1->v2 reviewer-findings
  audit — matched the S20-S25 precedent for prompt-drafting
  between sessions). At S26 Phase 0 Step 0.1 this was tolerated
  under the "Workspace HEAD delta tolerance" pattern (both extra
  commits were SESSION_26_PROMPT.md / SESSION_TRANSITION_
  TEMPLATE.md edits only).
- Session 26 close-out workspace commits: 1 (this file's primary
  edit + SESSION_LOG entry + LESSONS S26 fold) + 1 expected
  follow-up pinning the anchor SHA for S27 Phase 0 Step 0.1.
- **Last commit SHA at Session 26 CLOSE: this commit (the
  follow-up pinning the anchor)**. S27 prompt's Phase 0 Step 0.1
  MUST anchor workspace expectation to THIS follow-up's SHA, NOT
  to the primary close-out (which this follow-up succeeds). Per
  S21-S25 LESSONS pattern "Workspace HEAD delta tolerance":
  tolerate N additional prompt-drafting / audit-correction
  commits between sessions; verify each is consistent with that
  pattern before continuing.
- Branch sync with `origin/main`: 0 ahead / 0 behind expected
  after Session 26 close push.

---

## Session 27 execution order (enforce strict sequence)

Same N-phase shape applies regardless of scope choice (Phase 0
cold-start verify → Phase 1 scope → Phase 2 design-gate → Phase 3
impl → Phase 4 pre-push → Phase 5 push+tag → Phase 6 close-out).
Halt-on-mismatch at every phase; never bypass `--no-verify`.

Session 27 starts cold by:

1. Reading this template (current handoff state).
2. Reading the SESSION_LOG.md Session 26 entry.
3. Reading the LESSONS.md additions Session 26 landed (2 new
   sections at end of file, "S26 folding" suffix).
4. Reading the relevant section of BARCADA_CRAWLER_
   REMEDIATION_PLAN.md for the chosen Session 27 scope (see
   "Notes for Session 27" below).
5. Reading the Session 27 prompt if one has been drafted, OR
   commissioning a fresh draft at S27 open.
6. Running Phase 0 cold-start verification per the prompt's
   protocol (or per the S26 prompt template if S27 prompt is
   not yet drafted).

---

## Outstanding operator-input requests entering Session 27

1. **Session 27 scope choice** — pick from the candidates in
   "Notes for Session 27" below. Candidate H closed at S26; the
   carry-forwards (A/B/D/E/K) remain. Candidate B specifically
   would close Workstream 0 and warrant `workstream-0-end` tag.

2. **Eval_data labeling continuity** — operator-WIP edits to
   `eval_data/*.jsonl` continue across sessions (Sessions 8-26
   precedent). S26 saw NO operator-side eval_data commits between
   S25 close and S26 open. validate_consistency stayed green
   throughout S26.

3. **barcada-drift AI/ML alignment** — unchanged from S21-S26
   handoffs. If operator wants to ship `barcada-drift` in S27,
   the 4 AI/ML team decisions need to be pre-resolved OR scoped
   narrowly with placeholders. Plus the prereq of 2+ parquet
   files (earliest natural date 2026-06-06).

4. **launchd kit installation** — unchanged. Operator should
   run `scripts/launchd/install_canary_schedule.sh` when ready
   to enable the weekly Saturday-9am canary job. Required
   prerequisite for Candidate A.

5. **Session 27 prompt draft commissioning** — operator decides
   whether to commission an S27 prompt between sessions or scope
   one at S27 open.

6. **Live Azure smoke for ADLSCostJournal** (Candidate K;
   carry-forward from S25 handoff) — S25 shipped ADLSCostJournal
   tested against DummyBlobBackend in-memory (Q-J.3 (c)). The
   production code path against real Azure / Azurite has never
   been exercised. A small operator-driven smoke test
   (write_initial + try_update + read against a sandbox
   container) would close the mock-vs-prod divergence risk.

---

## Notes for Session 27

Suggested S27 scope candidates (operator picks at S27 open):

### Candidate A (carry-forward): `barcada-drift` skeleton

Unchanged from S21-S26 handoffs. Per CLASSIFICATION_ADJACENT_PLAN.md
§Item 8. Consumes `canary_runs/<date>.parquet` artifacts.
**Blocked**: 2+ parquet files needed (launchd installer not yet
run as of S26 close; earliest natural date 2026-06-06).
Estimated ~300 LOC.

### Candidate B (carry-forward): Per-tier cost-accounting retrofit

Unchanged from S21-S26 handoffs. Closes Workstream 0; warrants
`workstream-0-end` tag. Touches W4.1.5 driver area (locked except
via W5.X-prefix commits). Estimated 100-200 LOC.

Now that Candidate J (abfss://) closed at S25, the cost-accounting
retrofit can plausibly use abfss:// CostJournal end-to-end in its
verification — though the per-tier wiring itself does not require
ADLS; LocalFSCostJournal still works.

### Candidate D (carry-forward): Phase 4 PR-D operator-led labeling

Unchanged. Tooling support only; labeling itself is operator
territory.

### Candidate E (carry-forward): Cassette corpus expansion

Unchanged from S22-S26 handoffs. S20 shipped 20 cassettes; plan's
upper bound is 30. Could expand or curate.

### Candidate K (carry-forward from S25): ADLSCostJournal live smoke

Optional operator-driven smoke against real Azure / Azurite to
close the mock-vs-prod divergence risk for the S25-shipped
ADLSCostJournal backend. Two flavors:
- **K-a: Azurite container** — Docker-backed integration test
  (~50-100 LOC + Docker setup).
- **K-b: Operator-driven sandbox smoke** — ~30 LOC Python
  script; no CI integration.

---

## Required reading (Session 27 first 10 minutes)

In this order:

1. **This template** (current handoff state).
2. **`SESSION_LOG.md`** Session 26 entry — 1-commit narrative;
   Q-H.1 through Q-H.3 + Q-H.2-EXT decisions; the AskUserQuestion
   4-option-limit pattern that drove the mid-Phase-3 extension.
3. **`LESSONS.md`** — 2 new sections appended at S26 close
   ("S26 folding" suffix): AskUserQuestion 4-option limit can
   silently truncate a Q-* option set / Size-target gates can
   collide with audience-coverage gates.
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md`** — chosen-scope
   section per Session 27 candidate choice. Plan is READ-ONLY.
5. **`CLASSIFICATION_ADJACENT_PLAN.md`** §Item 8 — only if
   Candidate A (barcada-drift) is chosen.
6. **`src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`**
   — only if Candidate B or K touches the ADLS backend.
7. **`docs/CRAWLING_POLICY.md`** — only if operator wants to
   review the S26-tightened version (now 77 lines / 2.52 KB).

---

## Outstanding items carried forward to Session 27+

1. **Per-tier cost-accounting wiring gap** — carry-forward from
   S14; severity LOW. Unchanged disposition.

2. **`barcada-drift` CLI** — CLASSIFICATION_ADJACENT_PLAN.md
   §Item 8; 4 AI/ML team decisions outstanding. Blocked also
   on 2+ canary_runs parquet files. Unchanged.

3. **Cassette corpus expansion** — current 20 domains is lower
   bound of plan's "~20-30". Unchanged.

4. **Cassette-FP investigation** — archive.org + hashicorp.com
   flagged as SaaS-shell FPs in S20's FP-curation log. Unchanged.

5. **launchd kit smoke-then-install** — Unchanged. Operator
   should run `scripts/launchd/install_canary_schedule.sh` to
   enable the weekly job. Required for Candidate A.

6. **Phase 4 PR-D/E/F/G** (forward look) — Unchanged. Opens
   after Workstream 0 fully closes AND operator-led Stage 2 +
   Stage 3 labeling work begins.

7. **CRAWLING_POLICY.md size** — CLOSED at S26 (2.52 KB).
   Removed from carry-forward.

8. **abfss:// CostJournal Phase 5 promotion** — CLOSED at S25.

9. **Live Azure smoke for ADLSCostJournal** (Candidate K) —
   carry-forward from S25→S26. Optional; not a session-scope
   blocker.

---

## Locked artifact reminders for Session 27

Carry-forward from Sessions 8-26:

- `eval_data/` — labeling-workstream territory. Operator-WIP
  edits across sessions are expected. Pre-push validate_
  consistency runs against WT state; surface per LESSONS pattern
  if blocked.
- `stage1.schema.json` v1.0 with 49 keywords.
- `pre-remediation-2026-05-19` tag.
- `baseline-v0` tag at `9e9a1fb`.
- All `workstream-0-*` tags at their placed SHAs (9 tags from
  S20 close; unchanged).
- `workstream-a-week1-end` tag at `fdc8a7a` (placed S22).
- `tests/runners/fixture_cascade/` — W4.1.5 driver locked at
  `dd64963` except via W5.X-prefix commits.
- `tests/fixtures/baseline-v0/` snapshot — locked at `9e9a1fb`.
- `tools/baseline_v0/check.py`, `generate.py`, `determinism.py`,
  `canary.py` — S18-20 deliverables; locked.
- `tools/synthetic_crawl/` package — S20 deliverable; locked.
- `tests/fixtures/synthetic_crawls/` — S20 corpus; locked.
- `scripts/launchd/` — S20 deliverable; locked.
- `src/barcada_scraper/scraper/robots.py` — S21 deliverable;
  locked at `34a59b6`.
- `tests/scraper/test_robots.py` — S21 deliverable; locked at
  `34a59b6`.
- `src/barcada_scraper/scraper/robots_gate.py` — S22 deliverable;
  locked at `ba87e7e`.
- `src/barcada_scraper/scraper/robots_bypass_config.py` — S22
  deliverable; locked at `381ee89`.
- `tests/scraper/test_robots_gate.py` — S22 deliverable.
- `tests/scraper/test_robots_bypass_config.py` — S22 deliverable.
- `src/barcada_scraper/classifier/pipeline/cost_journal.py` —
  S22-extended at `1d9404e`; S25 Q-J.8 extension touched ONLY
  the test file (1↔1 replacement); production file unchanged.
- `src/barcada_scraper/classifier/pipeline/cost_journal_local.py`
  — production local-FS backend; locked.
- `src/barcada_scraper/classifier/pipeline/cost_journal_adls.py`
  — full backend shipped at S25 SHA `835a531`. Public API:
  `ADLSCostJournal(journal_dir, run_id, credential=None,
  blob_backend=None)` with read / write_initial / try_update /
  exists / path. Locked.
- `tests/classifier/pipeline/test_cost_journal_adls.py` — 19
  tests locked at `835a531`. Includes `DummyBlobBackend`.
- **NEW S26 LOCK**:
  `docs/CRAWLING_POLICY.md` — tightened W A.1 doc at S26 SHA
  `2314f5e` (77 lines / 2.52 KB). Further trimming OR additions
  require Phase 2 design-gate authorization.
- `src/barcada_scraper/orchestrator/robots_integration.py` —
  S23 deliverable; locked at `279bb77`.
- `tests/orchestrator/test_robots_integration.py` — S23
  deliverable; locked at `279bb77`. 35 tests.
- The 4 S23 tests + 2 unchanged S24 tests + 1 S25-replaced test
  in `tests/orchestrator/test_robots_gate_integration.py` —
  locked at `aed7873`. 7 tests total.
- `src/barcada_scraper/orchestrator/vmss_worker.py` — S23
  additions locked at `5eeaac7`.
- `src/barcada_scraper/orchestrator/job_runner.py` — S23
  additions locked at `872527e`.
- `scripts/vmss/cloud_init.template.yaml` — S23 additions locked.
- The 3 module-level helpers in
  `src/barcada_scraper/orchestrator/worker_loop.py`:
  `_open_cost_journal_for_worker` (body modified at S25 SHA
  `aed7873` per Q-J.4 abfss:// dispatch; signature locked),
  `_ensure_journal_initialized` (locked at S24 SHA `48c324a`),
  `_build_durable_bypass_writer` (locked at S24 SHA `48c324a`).
- The S24 3-line wiring block in `scrape_stage2_pages_invoker`
  at `48c324a` (with adjacent comment updated at S25 SHA
  `aed7873`).
- `tests/orchestrator/test_worker_loop_persistence.py` — S24
  deliverable + 1 S25-replaced test; locked at `aed7873`. 12
  tests.
- The 5 S24-retargeted test_stage2_pages_invoker_* fixtures in
  `tests/orchestrator/test_worker_loop.py` — landed at `48c324a`.
  Do NOT revert to abfss://.
- `docs/phase4_implementation_plan.md` — Phase 4 governance
  reference; do NOT modify until Phase 4 work is operator-
  authorized.
- Production code under `src/barcada_scraper/` — locked unless
  Phase 2 design-gate explicitly authorizes a specific module.
  S21+S22+S23+S24+S25 authorized: `scraper/robots.py`,
  `scraper/robots_gate.py`, `scraper/robots_bypass_config.py`,
  `classifier/pipeline/cost_journal.py` (additive only),
  `classifier/pipeline/cost_journal_adls.py` (S25 skeleton →
  full backend),
  `orchestrator/robots_integration.py` (new),
  `orchestrator/vmss_worker.py` (additive),
  `orchestrator/job_runner.py` (additive),
  `orchestrator/worker_loop.py` (additive: S23 gate wiring +
  S24 durable persistence helpers + S25 abfss:// guard removal
  in 1 helper body). S26 added no new src/ authorizations
  (doc-only).
- All `.claude/rules/*.md` and `CLAUDE.md` — operator preferences;
  honored every commit.

---

## Combined-suite-at-Session-27-open baseline

Canonical (16 paths; mirrors S25-close = S26-close invocation,
since S26 was doc-only):

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
    tests/classifier/pipeline/test_cost_journal_adls.py \
    tests/orchestrator/test_robots_integration.py \
    tests/orchestrator/test_vmss_worker.py \
    tests/orchestrator/test_job_runner.py \
    tests/orchestrator/test_worker_loop.py \
    tests/orchestrator/test_robots_gate_integration.py \
    tests/orchestrator/test_worker_loop_persistence.py -q
# Expected: 964 passed / 0 failed / 0 skipped
```

Sub-totals: 210 conformance + 46 driver + 99 baseline_v0 + 33
synthetic_crawl + 32 robots + 30 robots_gate + 30 robots_bypass_config
+ 43 cost_journal + 13 cost_journal_local + 19 cost_journal_adls +
35 robots_integration + 74 vmss_worker + 129 job_runner + 152
worker_loop + 7 robots_gate_integration (4 S23 + 2 S24-unchanged
+ 1 S25-replaced) + 12 worker_loop_persistence (11 S24-unchanged
+ 1 S25-replaced) = 964.

Cumulative-test-count gate: the count NEVER decreases between
commit boundaries.

Narrower baselines (still valid for S27 candidates that don't
exercise the new ADLS test paths):
- 480 (S22 headline suite; no orchestrator/, no journal)
- 538 (S22 headline + journal-suite)
- 938 (S25-equivalent narrower; 16-path minus
  test_cost_journal_adls.py's 19 + test_robots_gate_integration.py's
  7 — for Candidate-H-style doc-only candidates; used at S26
  Phase 3).

Choose at Phase 0 Step 0.5 per Candidate selection.

---

## Pre-push gate at Session 27 open

```
.venv/bin/ruff check .                                   # All checks passed!
.venv/bin/ruff format --check .                          # 351+ files OK
git ls-files '*.py' | xargs .venv/bin/vermin --target=3.10
                                                         # Minimum required 3.10
.venv/bin/python eval_data/scripts/validate_consistency.py
                                                         # 0 errors / 0 warnings
```

Note on gate 4: validate_consistency runs against working-tree
state; if operator-WIP in eval_data introduces a schema violation
between S26 close and S27 open, the gate will block even though
no S27 commit touches eval_data. Per LESSONS: surface to operator
with the row+detail, propose operator-fix or stash-and-restore;
do NOT auto-fix.

---

## Context-window awareness

Session 26 ran across 1 commit + Phase 2 source-verification +
1 mid-Phase-3 Q-H.2-EXT HALT-and-extend (resolved in one
AskUserQuestion turn) + Phase 6 close-out, comfortably within
context. Session 27 budget per chosen candidate:

- Candidate A (barcada-drift): only if launchd job has run ≥2
  times AND AI/ML decisions ready. Estimated ~300 LOC.
- Candidate B (per-tier cost-accounting): touches W4.1.5 area;
  more careful Phase 0 verification needed. Estimated 100-200 LOC.
- Candidate D (Phase 4 PR-D tooling): operator-led; tooling only.
- Candidate E (cassette corpus expansion): depends on operator
  curation choices.
- Candidate K (ADLSCostJournal live smoke): K-a ~50-100 LOC +
  Docker; K-b ~30 LOC operator-driven.

Strategies (unchanged from S20-S26 prompts):
- Use Edit over Write for small additions.
- Delegate multi-file design-of-record analysis to Explore.
- For any live-HTTP corpus work, pilot 1-3 before full N-domain.
- Source-verify line numbers per Phase 3 commit, not just at
  Phase 2 (S23 LESSONS pattern).
- Test against public API surface only — probe `.path` /
  behavior, not private attrs (S24 LESSONS pattern).
- Source-verify facts behind option-set design BEFORE
  AskUserQuestion drafts (S25 LESSONS pattern).
- Grep for same-shape tests outside the prompt's explicit
  allowlist at Phase 0 (S25 LESSONS Q-J.8 extension lesson).
- **NEW S26 LESSONS**: at Phase 2, count the prompt's Q-*
  option set; if any single Q-* enumerates >4 options, tier the
  question or split the AskUserQuestion call rather than
  silently narrowing. AND: cross-check quantitative-vs-
  qualitative Q-* gates for joint-feasibility BEFORE Phase 3
  starts — size targets can collide with coverage requirements.

Self-monitor cadence:
- Report estimated context usage at ~30%, ~60%.
- If usage crosses ~70% before chosen S27 scope closes,
  transition per "no mid-commit-batch transitions".

---

## Reporting in chat at session close

Same pattern as Sessions 13-26:

1. Commit SHA(s) of each Session 27 sub-surface.
2. Sub-surfaces landed.
3. Test count delta: 964 baseline → S27 close.
4. Driver suite count (46/46 expected unless realigned).
5. Files touched per surface.
6. Tag dispositions (e.g., does S27 warrant a new tag?
   Candidate B alone — closing Workstream 0 — warrants
   `workstream-0-end`; A/D/E/K do not).
7. Carry-forward dispositions.
8. Any spend (LLM, infrastructure).
9. Any new LESSONS patterns to fold in.

---

End of Session 26 handoff template. Refill at Session 27 close
per Phase 6 close-out protocol.
