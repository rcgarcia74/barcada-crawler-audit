# Session Transition Template — Handoff from Session 15 → Session 16

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-11
are summarized in SESSION_LOG.md; Sessions 12-15 are in the most
recent SESSION_LOG.md entries.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

---

## Handoff metadata

- Outgoing session number: 15
- Closing date: 2026-05-21
- Outgoing session scope: W4.3 test-infrastructure update. Bumped
  `tests/fixtures/expected.schema.json` v1.0 → v1.1 to match the 18-col
  `stage3_decision` shape landed at W4.2 commit `cc2ba2c`; folded all
  six deferred prose-only fixes (a)-(f) into META_SCHEMA.md; augmented
  the conformance suite's directory-semantic assertions with a
  hard_exclusions drift check against the W4.2-committed parser_output
  slice. Two repo commits (`7728bdf` W4.3.B + `b2e2671` W4.3.D);
  operator-authorized capstone tag `workstream-0-week4-end` at
  `b2e2671`. Pushed to origin/main.
- Reason for transition: natural seam at W4.3 close per plan §3 Week 4
  boundary. Week 5 (multipage + edge cases + repopulation + 17-red
  closure) is a distinct work unit with no overlapping engineering
  surface; W4.3's test-infrastructure refactor closed cleanly.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `b2e2671` (W4.3.D conformance drift check).
- Last commit subject: "W4.3.D: conformance tests augment exclusion_
  reason assertions with expected.json drift check"
- Prior W4.3 commit: `7728bdf` (W4.3.B schema bump + META_SCHEMA prose).
- Branch sync with `origin/main`: 0 commits ahead, 0 commits behind
  (verified at Session 15 close after push).
- Tags (do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3` (nuclear-revert anchor)
  - `workstream-0-week1-end` at `4f9d23f`
  - `workstream-0-week2-end` at `e5d2f91`
  - `workstream-0-week3-end` at `cf0c14c`
  - `workstream-0-week4-1-5-end` at `dd64963` (annotated tag SHA
    `f9be833a`). Annotation covers W A.0 W6 reusability + W4.2 output
    lifetime constraints.
  - `workstream-0-week4-end` at `b2e2671` (annotated, **NEW Session 15**;
    operator-authorized override of Session 12 "no Week 4 sub-tag"
    sequencing decision). Annotation covers W4.0/W4.1/W4.1.5/W4.2/W4.3
    closure, output durability, Week 5 ahead, and cost-budget state.
- Pre-push gate state at HEAD `b2e2671`: ALL CHECKS PASS (ruff + ruff
  format + vermin 3.10 target + validate_consistency).
- Unstaged changes intentionally ignored across sessions (operator-side
  work in the locked tree, ongoing labeling activity):
    eval_data/README.md
    eval_data/stage1_labels.jsonl
  These two files have been routinely unstaged through Sessions 8-15.
  Session 15 surfaced a temporary validate_consistency failure on row
  102 of stage1_labels.jsonl (duplicate 'testimonials' in operator's
  unstaged work); operator deduplicated to resolve the pre-push gate.
  Per Session 14 close + Session 15 push: `validate_consistency` passes
  cleanly (532 stage1 rows + 460 partner_type anchors).

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA at Session 15 start: `a50c044` (Session 14 close-out).
- Session 15 in `/Users/administrator/crawler-audit/`: this template
  refill + SESSION_LOG.md Session 15 append landed as the workspace's
  single commit of the session.
- Branch sync with `origin/main`: depends on whether the close-out
  workspace commit is pushed (Session 13 + 14 precedent: pushed).

---

## Active task list

The Session 15 task list (cold-start → Step A → B → C (skipped) → D →
E → close-out) is fully complete:

- **Step 1 cold-start verification**: COMPLETE. Workspace HEAD `a50c044`,
  repo HEAD `cc2ba2c`, all tags verified, 198 expected.json on disk,
  driver intact, both test suites at baseline.
- **Step A schema-shape design-gate**: COMPLETE. Operator chose path
  (a) schema bump v1.0 → v1.1.
- **Step B schema bump + META_SCHEMA prose**: COMPLETE. Commit `7728bdf`.
  Six deferred prose-only fixes (a)-(f) cleared from the register.
- **Step C rglob enumerator change**: SKIPPED per operator decision after
  source-verification finding (the 3 nested international_business
  fixtures are already discoverable via existing per-locale parametrize;
  the prompt's expected count shift 169 → 172 was an incorrect premise).
- **Step D conformance test augmentation**: COMPLETE. Commit `b2e2671`.
  "Augment, don't replace" semantics preserved the 17 W5-punch-list
  reds while adding the hard_exclusions drift check.
- **Step E validation pass**: COMPLETE. 46/46 driver + 17/169/2
  conformance with byte-identical W5-red identities against Session
  14 baseline.
- **Pre-push gate resolution**: COMPLETE. Initial validate_consistency
  failure on row 102 (operator-side unstaged work) surfaced via
  AskUserQuestion; operator deduplicated and gate ran clean.
- **Push**: COMPLETE. `cc2ba2c..b2e2671` landed at origin/main; tag
  `workstream-0-week4-end` pushed.
- **Workspace close-out**: this commit.

Task state is session-local in Claude Code; it does NOT carry across
sessions. Session 16 should TaskCreate fresh tasks on open.

Suggested Session 16 tasks:

- **Workstream 0 Week 5** (NEXT CONCRETE WORK UNIT, per plan §3 Week 5).

  Week 5 closes Workstream 0 with fixture-content work. The scope per
  plan §3 W5:

  1. **multipage_boilerplate** (Candidate #3): 20 fixtures (5 domains
     × 4 pages each) in new `multipage_boilerplate/<domain>/{home,
     about,pricing,products}.html`. Enables Action #5 evaluation
     (does existing `detect_cross_page_banners()` cover what SimHash
     would?).
  2. **Multilingual parking** (Candidate #10): 3 multilingual parking
     fixtures (Cyrillic, CJK, Japanese) to close detection coverage.
  3. **C0.3-followup**: 6 conforming `soft_404/` captures (`did you mean`,
     `showing results for`, `no results found`, `popular searches`,
     `trending searches`, `people also search for`, `try a different
     search` markers). Repopulates the directory emptied by C0.3 in
     Week 1 Days 1-2.
  4. **C0.4-followup**: 3 conforming `empty_google_sites/` captures
     (`sites-viewer-frontend` / `atari.vw.` / `normalizedPath.*view/`
     markers and `class="tyJCtd"` empty-content `<div>`s). Repopulates
     the directory emptied by C0.4 in Week 1 Days 1-2.
  5. **Edge-case robustness fixtures**: 1 huge HTML fixture (>1MB) for
     memory/parsing stress; 1 tiny but legitimate fixture (<2KB, non-
     stub); 1 malformed HTML fixture (unclosed tags); 2 encoding-
     variant fixtures (Big5 or Shift-JIS, declared-vs-actual mismatch).
  6. **17 W5-punch-list conformance reds closure**: the 17 conformance
     reds preserved through W4.3 close are the Week 5 fixture-replacement
     punch list. Per Session 14 + W4.3 documentation, these are
     fixture-content concerns (e.g., sanmarinoiron.com's parser tags
     it as non-spa_shell when the directory implies spa_shell; archive.
     org's parser tags it as empty_page when the directory implies
     legitimate_nonprofit). Closure pattern: either replace the .html
     with a conforming capture, OR recategorize the fixture into its
     actual-content directory, OR delete the fixture if neither
     applies. Each closure should re-run the conformance suite to
     verify the red count decreases monotonically toward zero.
  7. **Synthetic-with-real-markers fallback policy applies** (per
     plan §3 W5): real-domain captures are preferred; if real-domain
     sourcing fails, synthetic fixtures with real detector markers
     are acceptable substitution. Document `capture_method:
     "synthetic_with_real_markers"` in the per-fixture meta.json.

  **W5 acceptance criteria** (per plan §3 W5 Deliverable):

  - All 197 existing fixtures audited for conformance to directory
    specification.
  - All broken/empty/misleading fixtures replaced.
  - `sorted(glob)[0]` pattern eliminated from tests (already done at
    C0.9 / Session 6; verify still clean).
  - ~50 new fixtures added across hydration, mega-menu, international,
    multipage, edge cases (much of this already landed in Sessions 7-9;
    Week 5 mostly adds multipage + multilingual + edge-case).
  - Every fixture has `meta.json` and `expected/` outputs (need to
    extend meta.json + expected.json generation to cover the new W5
    fixtures via the W4.1.5 driver).
  - Test utilization at or near 100% (every fixture in a directory is
    tested).

  **W5 prerequisite verification**: the W4.1.5 cascade driver at
  `tests/runners/fixture_cascade/` (locked at `dd64963`) is reusable
  for generating expected.json files for new W5 fixtures via real-mode
  cascade execution (same pattern as W4.2). Each new fixture batch
  needs a corresponding meta.json (extending the W4.1 bulk-generation
  pattern at commit `9e1bda9`) and a cascade-driver run to produce
  the expected.json (extending the W4.2 pattern at commit `cc2ba2c`).

  **W5 cost expectation**: each new fixture added to the corpus
  contributes a small marginal LLM cost to expected.json regeneration.
  Per Session 14 W4.2 actual ($0.26345 for 198 fixtures), the marginal
  cost is ~$0.0013/fixture (real-mode cascade, mostly Stage 1 abstains
  for legitimate-* / parking_* shapes; higher for the few legitimate-
  business fixtures that escalate to Stage 3). For ~50 new W5
  fixtures: estimate $0.05-0.10 marginal LLM cost. Operator may
  decide whether to regenerate W4.2 + W5 together (1 cascade run for
  ~248 fixtures, $0.30-0.35 total) or only run cascade against the
  new fixtures (incremental commit).

- **Phase 4 PR-D through PR-G** (NOT in Workstream 0 scope; gated on
  operator-led Stage 2 + Stage 3 labeling per §11 Risk Register
  entry "Phase 4 measurement half blocked on operator-led labeling").

---

## Outstanding operator-input requests entering Session 16

**Material item — per-tier cost-accounting wiring gap (driver-locked)**:
Carried forward from Session 14 surface + Session 15 W4.3 close. The
W4.1.5 driver's cost-journal `totals.stage{1_llm,1_embedding,2_
summarization,2_classification,3_evidence,3_primary}_usd` fields are
NOT incremented (all $0.0 in the W4.2 run journal). `totals.cost_usd`
and per-shard `cost_usd` reconcile correctly, so total spend
telemetry is accurate. Per-row `stage3_decision.evidence_cost_usd`
is also $0 for all rows ($0.0237 gap between sum-of-per-row primary+
evidence cost and the Stage 3 shard total). Driver-locked at `dd64963`;
patch requires operator authorization. Severity: LOW. **Session 15
disposition: DEFERRED** (operator declined W4.3.X patch). Carry forward
to Session 16 only if operator decides to authorize a future cleanup
pass; otherwise this remains a low-severity ongoing gap documented in
LESSONS.md and risk-registered in §11.

**Material item — 4 fixture-taxonomy/content mismatches from W4.2**:
Surfaced during Session 14 Step C human review:
1. `parking_sale/sanluisconnect.com.html` → Stage 3 Reseller (HTML
   actually advertises a reseller affiliate program, not a parked
   sale page).
2. `parking_sale/sanmarcosoutlook.com.html` → Stage 3 ISV (HTML is
   actually Pair Domains' marketing page, not a parked domain).
3. `spa_shell/sanmarinoiron.com.html` → `is_business=True` (5912 chars
   of real metalworking business content despite spa_shell directory).
4. `auth_403/grilloresources.net.html` → `is_business=True` (parser
   tagged as `parking_errors` with bus_score=8 on the 403 HTML;
   signals engine quirk).
None of these are driver-bug-suspected. The cascade verdicts are
semantically correct against the actual HTML content. **Disposition:
deferred to W5 recategorization** (per Session 14 + Session 15
close). At Session 16 open, operator may choose to handle these
inline with W5 fixture-replacement work OR keep them as documentation
of current cascade behavior.

**No other gates** between Session 16 open and Week 5 work.

---

## Operator decisions made during Session 15 (cross-ref to SESSION_LOG.md)

1. **Step A path (a) schema bump v1.0 → v1.1** (over path (b) test-side
   adapter or driver-side adapter).
2. **Step C rglob enumerator change SKIPPED** (operator agreed with
   source-verification finding that the 3 nested fixtures are already
   discoverable).
3. **Step D comparison granularity: parser-level** (over verdict-only
   cascade or hash-based).
4. **Step D semantics correction (mid-session): "augment, don't replace"**
   (over pure replacement that would flip 17 reds, or W4.3 halt).
5. **META_SCHEMA scope: full path (a) bundle** — all 6 deferred prose-only
   fixes (a)-(f) folded in.
6. **Pre-push gate resolution: operator-side fix** for row 102
   (deduplicated 'testimonials' in eval_data/stage1_labels.jsonl).
   Not stash; not --no-verify; not session-defer.
7. **Week 4 capstone tag PLACED at b2e2671** (overrode Session 12 "no
   sub-tag" sequencing decision).
8. **Per-tier cost-accounting wiring gap (W4.3.X candidate): DEFERRED**
   (low severity; total cost telemetry intact; per-tier breakdown is
   nice-to-have for future cost-envelope work).

---

## Pattern note for Session 16 (Week 5 fixture work)

W5 is fixture-content work touching `tests/fixtures/html/<category>/`
and likely `tests/fixtures/html/<category>/expected/<domain>.json`
(if new fixtures are added). The patterns from Sessions 6-15:

- **Per-fixture decomposition with operator approval gates**
  (Session 6 C0.5 / C0.7 pattern; Session 11 W4.1 + W4.2 pattern).
  W5 has multiple surfaces: multipage_boilerplate (20 new fixtures),
  multilingual parking (3 new), C0.3-followup repopulation (6 new),
  C0.4-followup repopulation (3 new), edge-case fixtures (5 new),
  17 W5-punch-list red closures (each fixture per-file). Each batch
  could land as its own commit; alternatively bundle by closure-type
  (e.g., one commit per directory).

- **Synthetic-with-real-markers fallback as default for enterprise**
  (LESSONS Session 9 C7.c). For W5 captures where real-domain sourcing
  fails (anti-bot, edge firewall stubs, HTTP/2 INTERNAL_ERROR), the
  synthetic fallback is acceptable. Document `capture_method:
  "synthetic_with_real_markers"` in meta.json.

- **Verify-before-asking on every new fixture**: run extract_hard_
  exclusions on each new .html to confirm no detector FP (LESSONS
  Session 8 anti-trip discipline). Also verify the HTML comment header
  doesn't trip detector regexes (LESSONS Session 8 _RE_WAF / _RE_
  CLOUDFLARE patterns).

- **Confirm-to-commit gating** before every commit (LESSONS.md anchor
  pattern; Sessions 4-15).

- **File-based commit messages** at /tmp/<id>-msg.txt; no Co-Authored-By.

- **Pre-push gate** must run green; never use `--no-verify`. Watch for
  operator-side eval_data/ blockers (Session 15 precedent).

- **Driver-locked policy continues**: the W4.1.5 driver at
  `tests/runners/fixture_cascade/` remains locked at `dd64963`. W5
  fixture-content work should use the driver as-is for expected.json
  regeneration; do NOT modify driver code unless operator explicitly
  authorizes the per-tier cost-accounting W4.3.X patch.

- **Conformance count discipline**: the 17 reds at W4.3 close are the
  Week 5 punch list. Each W5 fixture replacement / recategorization /
  deletion should decrease the red count monotonically. A new red on a
  previously-passing fixture IS a regression and should be investigated.

- **W4.3 drift check propagates to new fixtures automatically**: any
  new fixture added under tests/fixtures/html/<category>/ that has an
  accompanying expected/<domain>.json will get the hard_exclusions
  drift check via the extended `_block(path)` helper. New fixtures
  must satisfy BOTH the directory-semantic assertion AND drift==zero
  against their committed expected.json. Drift==zero is automatic for
  fresh-from-driver generation since the cascade-driver-generated
  expected.json is by construction a snapshot of the live parser
  output on that fixture.

- **expected.schema.json now v1.1**: any new expected.json files added
  in W5 must conform to the v1.1 18-col stage3 shape. The W4.1.5
  cascade driver already emits this shape, so generation via the
  driver is forward-compatible. If new fixtures get expected.json
  generated outside the driver (manual / synthetic), they must match
  the v1.1 schema or validation fails.

---

## Locked artifacts reminder (CRITICAL — do not modify)

- All of `eval_data/` — locked. Read-only context only.
- `stage1.schema.json` v1.0 / 49 keywords — locked.
- All Workstream 0 tags — locked (pre-remediation-2026-05-19 +
  workstream-0-week1/2/3-end + workstream-0-week4-1-5-end +
  **workstream-0-week4-end at b2e2671 NEW Session 15**).
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` — read-only as of Session 12
  absorption close. Session 13's W4.1.5.T plan-update was a
  continuation-of-absorption authorized inline. The file is CLOSED
  to further amendments going forward unless operator re-authorizes
  another halt-and-reconcile.
- The 17 W5-punch-list fixtures — **W5 ACTIVELY MODIFIES these as the
  fixture-replacement punch list**. The "do not touch" applied through
  W4.3 close; W5 explicitly opens this surface.
- `tests/fixtures/META_SCHEMA.md` + `tests/fixtures/meta.schema.json` +
  `tests/fixtures/expected.schema.json` — **expected.schema.json
  bumped to v1.1 at W4.3 (Session 15 commit `7728bdf`); META_SCHEMA.md
  prose realigned with all 6 deferred fixes folded in at the same
  commit**. meta.schema.json remains at v1.0. The W4.0 schema-lock
  posture extends forward at v1.1 for expected and v1.0 for meta;
  further bumps require operator authorization.
- 197 `<domain>.meta.json` files (commit `9e1bda9`) +
  `tests/fixtures/generate_meta_json.py`. W4.0 worked-example META
  protection unchanged.
- 198 `<domain>.expected.json` files (commit `cc2ba2c`). The W4.2
  ground truth. W4.3 schema bump validated all 198 against v1.1 with
  zero modifications. Regeneration only via the W4.1.5 driver + a
  new W4.x operator-driven generation cycle.
- `tests/runners/fixture_cascade/` — the W4.1.5 driver, locked at
  `dd64963`. Driver-bug-suspected discovery during W5 requires
  operator authorization to patch. Per-tier cost-accounting wiring
  gap (W4.3.X) DEFERRED per Session 15 close.
- `tests/scraper/test_fixture_conformance.py` — extended at W4.3.D
  (Session 15 commit `b2e2671`) with the hard_exclusions drift check.
  W5 may add new parametrized tests for new fixture directories (e.g.,
  multipage_boilerplate, multilingual_parking) but should not change
  the existing test-helper surface unless operator authorizes.
- `docs/phase4_implementation_plan.md` — governance reference; do
  NOT modify until Phase 4 PR-D/E/F/G sequencing is
  operator-authorized.
- `~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md` — workspace
  design-of-record; read-only.
- `~/crawler-audit/RECONCILIATION_2026-05-21.md` — archival
  historical record; do not edit.
- `~/crawler-audit/working/w4_1_5_small_subset_validation_2026-05-21.md`
  — durable validation artifact; whitelisted in workspace
  `.gitignore`. Read-only.

---

## Next concrete work unit

- **Action ID:** **W5** (Week 5 fixture-content work — multipage +
  multilingual parking + soft_404 repopulation + empty_google_sites
  repopulation + edge-case robustness + 17 W5-punch-list red closures).
- **Scope:** see "Active task list" above. The fixture-replacement
  surface opens this session; the W5-punch-list reds are actively
  closed via fixture work (NOT test infrastructure — that closed at
  W4.3).
- **Acceptance criteria:** see "Active task list" → "W5 acceptance
  criteria" above (per plan §3 W5 Deliverable).
- **Files expected to be touched:**
  - `tests/fixtures/html/multipage_boilerplate/<domain>/{home,about,
    pricing,products}.html` (new directory + 20 new fixtures).
  - `tests/fixtures/html/parking_multilingual/<lang>.html` (3 new).
  - `tests/fixtures/html/soft_404/<domain>.html` (6 new; repopulates
    empty dir).
  - `tests/fixtures/html/empty_google_sites/<domain>.html` (3 new;
    repopulates empty dir).
  - `tests/fixtures/html/<edge_case_dir>/<domain>.html` (5 new edge-
    case fixtures, possibly under existing dirs or new edge_case_*).
  - 17 W5-punch-list fixture .html files (replace / recategorize / delete).
  - Accompanying `<domain>.meta.json` and `expected/<domain>.json` for
    every new or replaced fixture (via the W4.1.5 driver for expected;
    via the W4.1 generate_meta_json pattern for meta).
  - `tests/scraper/test_fixture_conformance.py` — possibly add new
    parametrize functions for multipage_boilerplate / multilingual /
    edge-case directories (the existing test_every_fixture_directory_
    has_a_test catch-all will surface uncovered directories).
- **Files NOT to be touched:**
  - The 198 W4.2-committed expected.json files (unless their .html is
    actively replaced as part of W5; then regenerate the expected.json
    via the driver in the same commit).
  - The 197 W4.1 meta.json files (unless their .html is actively
    replaced; same regeneration pattern).
  - `eval_data/`, `stage1.schema.json` (locked artifacts).
  - The W4.1.5 driver at `tests/runners/fixture_cascade/` (unless
    operator authorizes the per-tier cost-accounting W4.3.X patch).
  - `BARCADA_CRAWLER_REMEDIATION_PLAN.md` (read-only).
  - `docs/phase4_implementation_plan.md` (governance reference).
  - Production code under `src/barcada_scraper/`.
  - `tests/fixtures/expected.schema.json` v1.1 + META_SCHEMA.md
    (W4.3 close; further bumps need operator authorization).
  - `tests/fixtures/meta.schema.json` v1.0 (would need a bump if W5
    adds new meta.json fields beyond v1.0 vocabulary).

---

## Required reading (Session 16 first 10 minutes)

In this order:

1. **This file** (you're reading it).
2. **`LESSONS.md`** — operator patterns and observed conventions.
   No new entries added at Session 15 (all observed patterns were
   instances of previously-established discipline). The Session 12
   entries "Verify-before-asking discipline (extension)" and
   "Driver-level input contracts" both apply forward. The Session 6
   "Push-blocking pre-push gates require operator coordination" entry
   was reinforced this session.
3. **`SESSION_LOG.md` Session 15 entry** — what landed during the
   W4.3 test-infrastructure update (Step A path-a decision, Step B
   schema bump + META_SCHEMA prose, Step C skip rationale, Step D
   augment-vs-replace semantics, Step E validation, pre-push gate
   resolution, capstone tag placement).
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §3 Week 5** sub-section
   (line 239 onward) — the W5 fixture work spec. **READ-ONLY.**
5. **`tests/fixtures/META_SCHEMA.md`** v1.1 (Session 15 W4.3.B
   commit `7728bdf`) — the updated prose, especially §3 (18-col
   stage3 field table) and §3.1 (historical sentinel framing).
6. **`tests/scraper/test_fixture_conformance.py`** at HEAD `b2e2671`
   — the augmented `_block(path)` helper with drift check, the
   `_HARD_EXCLUSION_KEYS` tuple, and the `_expected_parser_output`
   helper.
7. **`tests/runners/fixture_cascade/cli.py`** — the W4.1.5 driver
   CLI. Session 16 will reuse this for generating expected.json files
   for new W5 fixtures (same pattern as W4.2).
8. **The 17 W5-punch-list fixtures** at their current .html paths
   — to scope the closure approach (replace / recategorize / delete).

After reading, verify repo state:

```
git -C /Users/administrator/projects/barcada-scraper status
git -C /Users/administrator/projects/barcada-scraper log --oneline -5
git -C /Users/administrator/projects/barcada-scraper tag -l 'workstream-*'
find /Users/administrator/projects/barcada-scraper/tests/fixtures/html -path '*/expected/*.json' -type f | wc -l
find /Users/administrator/projects/barcada-scraper/tests/fixtures/html -name '*.html' -type f | wc -l
.venv/bin/python -m pytest tests/scraper/test_fixture_conformance.py -q
.venv/bin/python -m pytest tests/runners/fixture_cascade/ -q
```

Expected:
- Last commit SHA: `b2e2671` (the W4.3.D conformance drift-check commit).
- Tags include `workstream-0-week4-1-5-end` at `dd64963` and
  `workstream-0-week4-end` at `b2e2671`.
- 198 expected.json files on disk (W4.2 ground truth at `cc2ba2c`,
  unmodified by W4.3).
- 198 .html files on disk (no W5 additions yet).
- 0 ahead / 0 behind origin/main.
- Only `eval_data/README.md` + `eval_data/stage1_labels.jsonl` showing
  as unstaged changes (locked, operator-side work).
- Conformance suite: 17 fail, 169 pass, 2 skip (Week 5 punch list
  byte-stable through W4.3 close).
- Driver suite: 46 passed.

If anything differs, surface to operator before doing work.

Then open the W5 design discussion: which W5 batch to land first
(multipage_boilerplate seeded by 5 domains, or C0.3/C0.4 followup
repopulation, or 17-red closure, or edge-case fixtures). Likely
present via AskUserQuestion as the first design-gate question after
Session 16 cold-start verification.

---

## Risk register state (plan §11)

No new risks escalated and unresolved by Session 15.

Forward-applicable entries (unchanged from Session 14 close):

- "Recapture tooling needs retry policy" — STILL applies.
- "Phase 4 infrastructure half landed concurrently with Workstream 0
  without plan absorption" — RESOLVED by Session 12 absorption.
- "W4.2 expected-output lifetime constrained" — STILL applies.
  W4.2 outputs (commit `cc2ba2c`) + W4.3 v1.1 schema (commit `7728bdf`)
  valid until W A.0 W6 OR Phase 4 PR-E lands, whichever comes first.
  The new `workstream-0-week4-end` tag annotation at `b2e2671`
  documents this constraint.
- "Phase 4 measurement half blocked on operator-led labeling" —
  STILL applies. PR-D requires Stage 2 + Stage 3 labeling.
- "Cost-journal per-tier accounting gap" (Session 14 surface) — STILL
  applies. Session 15 disposition: DEFERRED. Severity: LOW.
- Forward-applicable lessons in LESSONS.md.

LLM cost drift risk (plan §11) — Session 15 update:
- Session 15 incurred $0 (test-infrastructure refactor only).
- Cost incurred Sessions 1-15: $0.26345 total (all from W4.2 in
  Session 14).
- Cost budget remaining: $99.74.
- W5 estimated marginal LLM cost: $0.05-0.10 for ~50 new fixtures
  (only the ~5 that escalate to Stage 3 contribute meaningfully).
  Operator may decide whether to regenerate the W4.2 corpus + W5 new
  fixtures together (~$0.30-0.35 single run) or only run cascade
  against W5 new fixtures (incremental, lower marginal cost).
- Stop and escalate if actual spend trends >3× original $0.30 estimate
  (>$0.90); not triggered at Session 15 close.

---

## Deferred prose-only fixes register

**Status at Session 15 close: ALL CLEARED.** The W4.3.B commit
`7728bdf` folded all six entries (a)-(f) into META_SCHEMA.md as part
of the v1.1 schema bump per LESSONS.md "Defer prose-only schema fixes;
bump only when machine schema changes". The register is empty at
Session 16 open.

Future deferred prose-only fixes (if any surface in Session 16+)
should be tracked here following the same pattern: enumerate during
the session that surfaces them; defer until the next real machine-
schema change; fold in at that bump.

---

## Cost & schedule tracking

- Cost ceiling: $100 (operator-set 2026-05-19, alert at $50).
- Cost incurred Sessions 1-15: $0.26345.
- Cost budget remaining: $99.74.
- W5 estimated spend: $0.05-0.35 depending on regeneration strategy
  (see Risk register entry above).
- Schedule: ~4.7 weeks elapsed of Workstream 0's 5-week budget.
  - Weeks 1-3 COMPLETE.
  - Week 4 COMPLETE this session (W4.0/W4.1/W4.1.5/W4.2/W4.3 all
    landed; capstone tag placed at b2e2671).
  - Week 5 ahead.
  - Per Session 12 framing, W4.1.5 pulled cascade-driver engineering
    forward from W A.0 W6 by ~2 weeks. Weeks 4-5 may run ~1 week
    beyond the original budget; W A.0 W6 recovers the time.

---

## Notes for Session 16

- **Conformance test red count entering Session 16: 17** (Week 5
  punch list, byte-stable through W4.3 close). W5 fixture work
  closes these reds — each closure decreases the count by ≥1.
- **2 conformance tests still SKIP** (empty parametrize for
  `soft_404/` and `empty_google_sites/`) — both await Week 5
  C0.3-followup / C0.4-followup repopulation, which IS Session 16
  scope per plan §3 W5.
- **File-based commit messages** still mandatory. Pattern: Write to
  `/tmp/<id>-msg.txt`, then `git commit -F /tmp/...`.
- **"Confirm to commit?" gating** before every commit.
- **Verify-before-asking discipline** — bidirectional. Source of
  truth is the artifact, not the recall. For W5, every new fixture
  should be verified via extract_hard_exclusions before commit (per
  LESSONS Session 8 anti-trip discipline).
- **Pre-push gate** at Session 15 close included validate_consistency
  (532 stage1 rows + 460 partner anchor rows OK) after operator
  resolved the row 102 dup. Routinely passes. Never use `--no-verify`.
  Watch for operator-side eval_data/ work-in-progress blockers.
- **Plan is read-only** — never edit
  `BARCADA_CRAWLER_REMEDIATION_PLAN.md`. The Session 13 W4.1.5.T
  update was a continuation-of-absorption per the inline TODO; no
  further edits absent operator re-authorization.
- **Shell cwd drift**: use absolute paths or `cd /Users/administrator/
  projects/barcada-scraper` at the start of each Bash chain.
- **Workspace cwd**: when editing LESSONS.md / SESSION_LOG.md / this
  template, work in `/Users/administrator/crawler-audit/`.
- **W4 tag pattern**: per Session 15 operator decision (overriding
  the Session 12 "no Week 4 sub-tag" sequencing), Week 4 is now
  capstone-tagged at `workstream-0-week4-end` (`b2e2671`). Week 5
  may follow the same pattern at its close (`workstream-0-week5-end`)
  if operator chooses; the Session 12 sequencing decision is
  effectively obsolete after the Session 15 override.
- **W5 driver-locked policy**: the W4.1.5 driver at
  `tests/runners/fixture_cascade/` remains locked at `dd64963`. If
  W5 fixture work surfaces a driver bug, the patch is a separate
  W5.X-prefixed commit with its own confirm-to-commit gate. Per-tier
  cost-accounting wiring gap (W4.3.X) remains DEFERRED.
- **W4.2 + W4.3 ground truth durability**: the 198 expected.json
  files at `cc2ba2c` + the v1.1 schema at `7728bdf` ARE the W5
  comparison baseline. W5 fixture replacements that change .html
  content MUST also regenerate the corresponding expected.json via
  the W4.1.5 driver in the same commit (otherwise the conformance
  drift check at W4.3.D will fire).
- **Augment-don't-replace semantics for conformance tests**: any new
  W5 parametrize functions for new fixture directories should follow
  the W4.3.D pattern — directory-semantic assertion first (preserving
  the test's intent), drift check via `_block(path)` after (catches
  parser regressions). The `_block(path)` helper auto-applies the
  drift check; just call it from the new test.
- **This template's structured fields will need refilling at
  Session 16 close.**
