# Session Transition Template — Handoff from Session 11 → Session 12

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-10
are summarized in SESSION_LOG.md; Session 11 close is in the most
recent SESSION_LOG.md entry.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

---

## Handoff metadata

- Outgoing session number: 11
- Closing date: 2026-05-20
- Outgoing session scope: Open Workstream 0 Week 4 continuation
  (W4.1 bulk meta.json generation across the 198-fixture corpus).
  Resolved one divergence (Session 11 path-A finding: META_SCHEMA
  response_status recipe pre-C0.7c-stale) + three engineering-design
  flags surfaced during sample review (Flag A: synthetic source_url
  fallback shape; Flag B: replaced_in_place captured_at semantics;
  Flag C: sample size). Bulk landed at `9e1bda9`, pushed to
  origin/main.
- Reason for transition: natural seam at W4.1 close. W4.2
  (expected/<domain>.json generation) is a substantively different
  work unit — runs each fixture through the actual Stage 1/2
  pipeline, not pure scripted derivation; introduces LLM-call risk
  even at near-zero expected spend; cadence shifts from
  "engineering-design single-unit" back to "per-fixture verify-and-
  review." Session 11 close at ~70% context remaining is well above
  the 50% margin preferred for a parser-output deterministic-
  serialization pass.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `9e1bda9`
- Last commit subject: `W4.1: bulk meta.json generation across the 198-fixture corpus`
- Branch sync with `origin/main`: 0 commits ahead, 0 commits behind
  (pushed Session 11 close)
- Tags (do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3` (nuclear-revert anchor)
  - `workstream-0-week1-end` at `4f9d23f` (Week 1 close)
  - `workstream-0-week2-end` at `e5d2f91` (Week 2 close)
  - `workstream-0-week3-end` at `cf0c14c` (Week 3 close)
  - NO `workstream-0-week4-end` tag yet — W4 spans multiple sessions;
    tag lands at full W4 close (W4.3 complete) with required
    annotation per Flag 1 constraint #2.
- Pre-push gate state at HEAD: ALL CHECKS PASS (ruff check, ruff
  format --check, vermin --target=3.10-, validate_consistency for
  eval_data, jsonschema strict validation of all 198 meta.json)
- Unstaged changes intentionally ignored across sessions (operator-
  side work in the locked tree, unchanged since Session 8 close):
    .claude/rules/code-correctness.md
    eval_data/README.md
    eval_data/TAXONOMY_GAP_LOG.md
    eval_data/stage1_labels.jsonl

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA: TBD (filled in after Session 11 close commit
  pushes)
- Last commit subject: Session 11 close: SESSION_LOG.md Session 11
  append + LESSONS.md "Deferred prose-only schema fixes" section +
  SESSION_TRANSITION_TEMPLATE.md refill for Session 12
- Branch sync with `origin/main`: 0 commits ahead (after push)

---

## Active task list

The Session 11 task list (W4.1 bulk meta.json generation) is fully
complete:
- W4.1 generator script (`tests/fixtures/generate_meta_json.py`) +
  197 new `<domain>.meta.json` files landed at `9e1bda9`
- W4.0 worked example (twilio.com.meta.json) preserved unchanged
- Three engineering-design flags resolved (A: RFC 2606 `.invalid`
  fallback; B: replacement-commit date for captured_at; C: 10-fixture
  sample; see SESSION_LOG.md Session 11 entry)
- One divergence found-and-corrected via Session 11 path-A
  resolution (META_SCHEMA prose ↔ C0.7c reality)
- Three deferred META_SCHEMA prose-only fixes tracked for next real
  schema bump (see "Deferred prose-only fixes" section below)

Task state is session-local in Claude Code; it does NOT carry across
sessions.

Session 12 should TaskCreate fresh tasks on open. Suggested tasks:

- **W4.2 expected/<domain>.json generation across the corpus** (NEXT
  CONCRETE WORK UNIT). 198 fixtures need `expected/<domain>.json`
  files under `tests/fixtures/html/<category>/expected/`. Per W4.0
  schema + Flag 1 resolution: scripted generation that runs each
  fixture through the actual Stage 1/2 pipeline (RULES-first for
  Stage 1, LR-first for Stage 2 per plan §3 W4 example), serializes
  parser_output deterministically per plan §4 lines 232-234, and
  populates `stage3_decision` with the canonical sentinel triple per
  META_SCHEMA §3.1. Operator review of script output before bulk
  commit.

  Field-derivation recipes for `expected/<domain>.json` (per
  META_SCHEMA §3 + Flag 1 sentinel):
  - `schema_version`: `"1.0"`.
  - `parser_output`: deterministic-serialized output of the actual
    parser run against the fixture HTML. Per plan §4 lines 232-234,
    serialize as canonical JSON: sorted keys, fixed float precision,
    Unicode normalization where applicable. The Session 10 worked
    example carries a `_placeholder` marker (see twilio.com worked
    example); W4.2 replaces those with real parser output.
  - `barriers_verdict`: null or object per plan §3 W4 line 166;
    derived from `barriers.py` run against the fixture.
  - `stage1_decision`: object with `is_business`, `business_score`,
    `tier` per `expected.schema.json` required fields. Derived by
    running Stage 1 against the fixture; RULES tier when the
    rules engine fires, LR / LLM tier otherwise (LLM should not
    fire on Stage 1 — RULES + LR exhausts Stage 1 routing per plan).
  - `stage2_decision`: object with `tech_category`, `confidence`,
    `tier`. Derived by running Stage 2 against the fixture; LR
    tier when LR is confident, LLM tier when LR abstains. LLM
    calls expected to be rare; stop and escalate if Stage 2 LLM
    spend trends higher than near-zero before $50 alert threshold.
  - `stage3_decision`: canonical Flag 1 sentinel triple, fixed
    across all 198 fixtures at W4.2:
    `{"partner_type": "deferred_to_workstream_c", "confidence": null, "tier": "deferred"}`
    Real Stage 3 output lands when Workstream C regenerates these
    files.

  Acceptance criteria (W4.2):
  - 198 expected/<domain>.json files generated, one per .html in
    the corpus.
  - Each conforms to `tests/fixtures/expected.schema.json`
    (verifiable via jsonschema Draft7Validator).
  - `stage3_decision` carries the exact sentinel triple across all
    198 files.
  - Test surface invariant 17/169/2 preserved (expected/<domain>.json
    files invisible to `_iter_fixtures` `*.html` glob — verify the
    invariant after the bulk landing).
  - Pre-push gate green at the bulk commit SHA.
  - LLM cost stays near-zero per Flag 1 constraint #4.

- **W4.3 Test infrastructure** (may span into Session 13). Update
  `tests/scraper/test_fixture_conformance.py` to compare against
  `expected/<domain>.json` (replacing current "exclusion_reason must
  be empty" assertions with full comparison logic that respects the
  Stage 3 sentinel comparison-skip directive per Flag 1 constraint
  #5 semantic α). The sentinel string
  `"deferred_to_workstream_c"` should be codified as a named
  constant in the comparison code, not magic-string scattered.

- **W4 close + tag annotation**. At full W4 close (W4.3 complete),
  tag `workstream-0-week4-end` at the final green-gate SHA.
  Annotation must state per Flag 1 constraint #2 (verbatim):
  "Stage 3 expected-outputs deferred to Workstream C per Flag 1
  resolution; partial coverage at W4 close is intentional, not
  incomplete."

---

## Outstanding operator-input requests entering Session 12

**Workstream C scope amendment** flagged for operator authorization.
Carried forward from Session 10 + Session 11. Deferred Stage 3
expected-output generation lands in Workstream C scope per Flag 1
resolution; that's a plan-document amendment — read-only territory,
operator authorization required. Staged in commit messages `9165791`
and `8aafc45`; not re-staged in W4.1 `9e1bda9`. Operator decision
needed: re-stage in subsequent W4 commit messages, or treat as
staged-once-and-carried-via-workspace-handoff. Not a Session 12 W4.2
blocker; will matter at Workstream C scoping.

**W4.2 script preview** — once Session 12 drafts the W4.2 generation
script, present sample output for 5-10 representative fixtures
(particularly: 1 RULES-Stage-1, 1 LR-Stage-1, 1 RULES-Stage-2,
1 LR-Stage-2, plus a couple of exclusion-path fixtures) before bulk
commit. Per plan §3 W4 deliverable cadence: "Generate expected
outputs once, human-review them, commit."

---

## Operator decisions made during Session 11 (cross-ref to SESSION_LOG.md)

- **Session 11 path-A resolution** (META_SCHEMA prose ↔ C0.7c
  reality divergence): Truth-3-style corpus-wide correction in
  SESSION_TRANSITION_TEMPLATE.md + SESSION_LOG.md only;
  META_SCHEMA.md prose stays at v1.0 with the known wording bug;
  fold into next real schema bump's diff.
- **Flag A option (b)**: RFC 2606 `.invalid` TLD fallback
  (`https://<filename-stem>.invalid/`) for synthetic-variant
  fixtures with no canonical link. Real-domain capture fallbacks
  (`curl_with_retries`, `historical_unverified`, `replaced_in_place`)
  keep the bare-domain form unchanged.
- **Flag B option (a)**: use the C0.5x replacement commit's author
  date as `captured_at` for `replaced_in_place` files, not the
  original 1697bb5 add date. Semantic correctness — captured_at
  reflects when the *current* content was captured.
- **Flag C**: 10-fixture sample (8 required axes + 1 replaced_in_place
  surfaced during dry-run distribution check + 1 extra coverage).
  Operator declined expansion to one-per-category (≈26).
- **W4.1 bulk-commit shape**: single commit, not per-directory
  split. All 197 files generated by one script pass; share authoring
  provenance; per-directory commits would fragment the log without
  independent-revertability value.
- **Plan is read-only**: unchanged from prior sessions (memory:
  `feedback_remediation_plan_readonly.md`).

---

## Pattern note for Session 12 (engineering-design + verify-before-asking)

Session 11 W4.1 reinforced two patterns and surfaced one new one:

- **Engineering-design cadence with mid-stream operator
  decisions**: when single-unit drafting (e.g., the W4.1 generation
  script) surfaces multiple independent design questions during
  sample review, present each as a flagged decision rather than
  bundling into a single approval. Session 11 had three such
  flags (A/B/C); each was resolved independently before bulk
  authorization. The cadence is "draft → sample → flag any
  surprises → resolve flags → bulk → verify → confirm."

- **Verify-before-asking applied across distinct verification
  moments**: Session 11 applied the discipline at three
  independent points — pre-script verification (corpus shape +
  recipe alignment, surfaced the path-A divergence); pre-sample
  distribution check (capture_method enum coverage, surfaced the
  replaced_in_place trace-back bug); sample review (Flags A/B/C).
  The operator-ratchet fired once at "Confirm to commit?"; deeper
  double-check pass surfaced 0 new problems but provided full
  re-validation table.

- **NEW Session 11: deferred prose-only schema fixes** (LESSONS.md
  addition this session). When prose-only schema discrepancies
  surface and machine schemas are unaffected, defer the prose fix
  to the next real schema bump rather than semver-bumping for
  prose alone. See LESSONS.md "Defer prose-only schema fixes;
  bump only when machine schema changes" for the full pattern.

W4.2 expected/<domain>.json generation falls under engineering
design (single-unit script drafting). Session 12 should draft the
W4.2 generation script, run it against a sample of 5-10
representative fixtures across the routing tiers (RULES vs LR vs
exclusion paths), present sample output for operator review, then
run the full bulk generation after sample approval.

---

## Locked artifacts reminder (CRITICAL — do not modify)

- All of `eval_data/` — locked. Read-only context only. Includes
  `eval_data/canary_50_domains.txt`.
- `stage1.schema.json` v1.0 / 49 keywords — locked.
- `pre-remediation-2026-05-19` tag at `3cbb9b3` — do not retag or
  move.
- `workstream-0-week1-end` tag at `4f9d23f` — do not move.
- `workstream-0-week2-end` tag at `e5d2f91` — do not move.
- `workstream-0-week3-end` tag at `cf0c14c` — do not move.
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` — read-only, period. All
  deviations from the plan land in SESSION_LOG.md and LESSONS.md.
- The 17 fixtures on the Week 5 cleanup punch list (see
  SESSION_LOG.md Session 6 entry) — DO NOT touch in Session 12.
- `tests/fixtures/META_SCHEMA.md` + `tests/fixtures/meta.schema.json`
  + `tests/fixtures/expected.schema.json` — locked W4.0 schema
  artifacts. Schema bumps land via documented semver progression per
  META_SCHEMA §4, NOT via inline edits to v1.0. Three prose-only
  discrepancies tracked in the Deferred prose-only fixes section
  below — those fold into the next real schema bump, NOT into a
  prose-only bump.
- **NEW Session 11**: 197 new `<domain>.meta.json` files (commit
  `9e1bda9`) + `tests/fixtures/generate_meta_json.py` (the W4.1
  bulk-generation script). The meta.json files are not "locked"
  per se — they can be regenerated via `python tests/fixtures/
  generate_meta_json.py --bulk --force` if META_SCHEMA bumps and
  existing files go stale. But the W4.0 worked example
  (`legitimate_business/twilio.com.meta.json`) IS locked via the
  `PROTECTED_PRE_EXISTING_META` frozenset in the generator script;
  operator-protected. Do not modify it without operator
  authorization to update the protected set.

---

## Next concrete work unit

- **Action ID:** **W4.2** (expected/<domain>.json generation across
  the 198-fixture corpus per META_SCHEMA v1.0 + Flag 1 sentinel
  triple for stage3_decision).
- **Scope:** Author a Python generation script (analogous shape to
  `tests/fixtures/generate_meta_json.py`, possibly extending it as a
  second CLI mode, OR a separate `generate_expected_json.py` —
  Session 12 decides at draft time). Read each .html under
  `tests/fixtures/html/<category>/`, run it through the actual Stage
  1/2 pipeline, serialize parser_output deterministically, emit
  `<domain>.json` under `tests/fixtures/html/<category>/expected/`
  per META_SCHEMA §1. Run against 5-10-fixture sample first; present
  sample output to operator; bulk commit after sample approval.
- **Acceptance criteria:**
  - 198 expected/<domain>.json files generated.
  - Each conforms to `tests/fixtures/expected.schema.json` via
    jsonschema Draft7Validator strict validation.
  - `stage3_decision` carries the exact sentinel triple across all
    198 files.
  - Test surface invariant 17/169/2 preserved (`_iter_fixtures`
    globs `*.html` only; verify after bulk landing).
  - Pre-push gate green at the bulk commit SHA.
  - LLM cost stays near-zero per Flag 1 constraint #4. Stop and
    escalate before $50 alert threshold if actual spend trends
    higher.
  - W4.2 likely a single commit per Session 11 W4.1 precedent
    (single bulk-commit shape for atomic landing); operator may
    decide at sample-review time whether to split.
- **Files expected to be touched:** 198 new `<domain>.json` files
  under `tests/fixtures/html/<category>/expected/` (and
  `<category>/expected/` subdirectory creation). Plus the
  generation script (location TBD: either extend
  `tests/fixtures/generate_meta_json.py` or new
  `tests/fixtures/generate_expected_json.py`). Possibly a small
  refactor in the existing script if shared helpers are extracted.
- **Files NOT to be touched:** everything under `eval_data/`,
  `stage1.schema.json`, the tags, `BARCADA_CRAWLER_REMEDIATION_PLAN.md`,
  the 17 Week-5 punch-list fixtures, META_SCHEMA.md +
  meta.schema.json + expected.schema.json (locked W4.0 artifacts —
  no prose bumps for the deferred fixes), and the 198 W4.1
  meta.json files (those represent provenance, not expected
  outputs; no need to touch them in W4.2). The W4.0 worked example
  `legitimate_business/expected/twilio.com.json` already exists
  with a `_placeholder` parser_output — W4.2 either replaces it
  with real output or protects it like the meta.json was protected;
  operator decision at sample-review time.

---

## Required reading (Session 12 first 10 minutes)

In this order:
1. **This file** (you're reading it).
2. **`LESSONS.md`** — operator patterns and observed conventions.
   Pay particular attention to:
   - **NEW Session 11**: "Defer prose-only schema fixes; bump only
     when machine schema changes" — pattern for prose-only schema
     discrepancies that came out of W4.1.
   - "Verify-before-asking discipline" section — applies forward to
     W4.2 pre-sample verification + sample review + pre-commit
     verification.
   - "Detector precision findings" (FPs/FNs + deeper-circularity
     meta-observation) — W4.2 runs the actual Stage 1/2 pipeline on
     every fixture, so any detector-precision finding hits expected-
     output values. Manual review of any fixture where exclusion_
     reason fires when the category implies it shouldn't (e.g.,
     legitimate_* fixture tripping a parking detector).
   - "Synthetic-fixture HTML comments are regex-visible" — applies
     to synthetic fixtures' parser_output if comments leak into
     extracted text; verify by inspection during sample review.
3. **`SESSION_LOG.md` Session 11 entry** — W4.1 bulk commit
   `9e1bda9`, Flag A/B/C resolutions, path-A divergence finding,
   deferred prose-only fixes tracker, distribution numbers.
4. **`tests/fixtures/META_SCHEMA.md`** — schema spec for both
   meta.json and expected/<domain>.json. Re-read §3 (expected.json),
   §3.1 (sentinel values), and §4 (schema versioning policy). W4.2
   bulk generation operates against the expected.json half.
5. **`tests/fixtures/html/legitimate_business/expected/twilio.com.json`**
   — W4.0 worked example showing the structural shape (with
   `_placeholder` parser_output marker pending W4.2). Decide whether
   W4.2 overwrites it with real output or protects it like
   meta.json was protected.
6. **`tests/fixtures/generate_meta_json.py`** — the W4.1
   bulk-generation script. W4.2 may extend it as a second CLI mode
   or borrow its shape (CLI flags, idempotency via
   `PROTECTED_PRE_EXISTING_*`, in-script + jsonschema validation).
7. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §3 Week 4** — meta.json
   and expected-outputs spec (W4.0 deviations documented in
   META_SCHEMA.md). **READ-ONLY.**
8. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §14 Session Continuity
   Discipline** — referenced for Session 12 close-out cadence.

After reading, verify repo state:

```
git -C /Users/administrator/projects/barcada-scraper status
git -C /Users/administrator/projects/barcada-scraper log --oneline -5
git -C /Users/administrator/projects/barcada-scraper tag -l 'workstream-*'
find /Users/administrator/projects/barcada-scraper/tests/fixtures/html -name "*.meta.json" | wc -l
```

Expected:
- Last commit SHA: `9e1bda9` (W4.1 bulk meta.json).
- Recent commits include `8aafc45` (W4.0 worked example) and
  `9165791` (W4.0 schema lock).
- Tags: `pre-remediation-2026-05-19` + `workstream-0-week1-end` /
  `week2-end` / `week3-end`. NO `week4-end` tag yet.
- 198 `.meta.json` files under `tests/fixtures/html/`.
If anything differs, surface to operator before doing work.

Then begin W4.2 (expected/<domain>.json generation). Generate sample
first (5-10 representative fixtures spanning RULES / LR / exclusion-
path routing), present to operator, await sample approval before
bulk run.

---

## Risk register state (plan §11)

Recent additions (Sessions 4-11):
- "Recapture tooling needs retry policy" — STILL applies. W4.2
  likely no captures, but applies if any recapture is triggered.
- Forward-applicable lessons in LESSONS.md (plan is read-only, so
  they cannot land in §11 itself):
  - "Probe framework generation before locking a fixture spec"
    (Session 7)
  - "Synthetic-fixture HTML comments are regex-visible" (Session 8)
  - "Detector precision findings" with FPs and FNs (Session 9)
  - "Audit-spec vs. production-reality drift" (Session 9)
  - "Verify-before-asking discipline" (Session 10; header naming +
    operator-ratchet + A/B/C trigger condition)
  - **NEW Session 11**: "Defer prose-only schema fixes; bump only
    when machine schema changes" — pattern for prose-only schema
    discrepancies surfaced during W4.1; three concrete instances
    deferred this session (see Deferred prose-only fixes below).

Open latent gap (Issue 3 from Week 2 audit erratum, unchanged):
- Project's ruff `select` does not include "C" (mccabe), so
  cyclomatic-complexity violations escape pre-push. Manual
  `ruff check --select C901 <file>` in any code-modifying commit
  is the workaround until a project-config commit closes the gap.
  Session 11 W4.1 generator script was the first code-modifying
  commit since the gap was flagged; manual McCabe was applied and
  passed. Session 12 W4.2 generation script will be the second.

LLM cost drift risk (plan §11) — Session 11 update:
- W4.2 runs Stage 1/2 pipeline against every fixture; LLM tier
  fires only when LR abstains on Stage 2. Expected near-zero LLM
  cost per Flag 1 constraint #4. Stop and escalate if actual W4.2
  spend trends higher than near-zero before $50 alert threshold.
  Cost ceiling $100 untouched through Session 11 close ($0
  incurred); budget remaining $100.

No new risks escalated and unresolved by Session 11.

---

## Deferred prose-only fixes (fold into next real schema bump)

These are text-only inconsistencies in locked schema artifacts whose
machine-readable schemas are unaffected. Per operator Session 11
path-A resolution + LESSONS.md "Defer prose-only schema fixes; bump
only when machine schema changes" (Session 11 addition), prose
corrections are NOT semver-bumped on their own; they ride the next
real schema bump's diff so the locked-artifact churn stays minimal.

- **META_SCHEMA.md §2.4 line 95 + §5 line 149** (Session 11
  path-A finding): both say the C0.7c nginx-401 split lives in
  `parking_default_pages/`. Reality (verified Session 11 via commit
  `4f8dc06` + directory listings): C0.7c moved those 4 files OUT
  of `parking_default_pages/` INTO `auth_403/`, and
  `parking_default_pages/` now contains 2 uniform-200 fixtures
  (`grigolato.net.html` + `sanluishouston.com.html`). Corrected
  derivation lives in the `response_status` recipe in this template's
  Active task list section. Machine schemas (`meta.schema.json` +
  `expected.schema.json`) say nothing about directory-level response
  mapping — only the prose carries the bug.

  Fold into next real semver bump's diff: change `parking_default_pages/`
  → `auth_403/` in both §2.4 and §5 prose, name the 4 files inline.

- **META_SCHEMA.md §2.4 line 93 + §5 line 150** (Session 11 Flag B
  resolution): strict reading says `captured_at` derives from the
  file's first-add commit via `--diff-filter=A --follow`. For
  `replaced_in_place` files (parking_sale/shelvs.com.html via C0.5c
  + legitimate_business/sanmarcosflowershop.com.html via
  C0.5d-followup), `--follow` traces back to the original 1697bb5
  add commit, whose content no longer lives in the file. The
  W4.1 generator script extends the recipe: `replaced_in_place`
  files use the C0.5x replacement commit author date as
  captured_at. Machine schema only says `format: date-time`; prose
  carries the strict-reading-but-semantically-wrong rule.

  Fold into next real semver bump's diff: amend §2.4 line 93 to
  note that `replaced_in_place` files use the replacement commit
  date, not the original add date.

- **META_SCHEMA.md §2.4 vocabulary extension** (Session 11 Flag A
  option b): the `provenance_note` Recommended source-string
  vocabulary needs one new canonical value to cover synthetic-
  variant source_url fallbacks:
    - `approximated_from_synthetic_invalid_fallback` — `source_url`
      derived from `https://<filename-stem>.invalid/` per RFC 2606,
      used when a synthetic-variant fixture (`synthetic` or
      `synthetic_with_real_markers`) has no canonical link. Distinct
      from `approximated_from_bare_domain_fallback`, which remains the
      fallback for real-domain captures.
  Machine schema unaffected (provenance_note values are
  `additionalProperties: {type: string}`). Fold into next real semver
  bump's diff: add the new vocabulary entry to §2.4 list. Bulk
  generation script `tests/fixtures/generate_meta_json.py` already
  emits this value for the 20 pre-Session-1 synthetic fixtures (and
  any future synthetic-variant fixture without a canonical link).

---

## Cost & schedule tracking

- Cost ceiling: $100 (operator-set 2026-05-19, alert at $50)
- Cost incurred Sessions 1-11: $0 (no LLM API calls; curl + pytest
  + handwritten Python + handwritten synthetic + jsonschema
  validation only)
- Cost budget remaining: $100
- W4.2 expected spend: near-zero (RULES + LR for the corpus
  majority, LLM only at Stage 2 abstain tail). Stop and escalate
  if actual W4.2 spend trends higher than near-zero before $50
  alert threshold.
- Schedule: ~3 weeks elapsed of Workstream 0's 5-week budget.
  - Weeks 1-3 COMPLETE.
  - Week 4 OPEN: ~60% complete (W4.0 schema lock + W4.0 worked
    example + W4.1 bulk meta.json all DONE; W4.2 expected-output
    generation + W4.3 test infrastructure PENDING). Likely spans
    Sessions 12-13.
  - Week 5 still ahead.

---

## Notes for Session 12

- **Conformance test red count at handoff is 17** (Week 5 punch
  list, byte-stable through W4.1 landing). Every Session 12 commit
  should verify the count stays at 17 unless the commit itself
  deliberately changes test infrastructure (W4.3 may legitimately
  shift counts when expected.json comparison replaces "exclusion_
  reason must be empty" assertions — document any deliberate shift
  in commit message).
- **2 conformance tests SKIP** (empty parametrize for `soft_404/`
  and `empty_google_sites/`) — both await Week 5 C0.3-followup /
  C0.4-followup repopulation.
- **The Session-11-close test surface is 17 fail / 169 pass / 2 skip
  / 64 hard_exclusions pass.** Same as Session 10 close. W4.1
  landed without test surface drift.
- **File-based commit messages** still mandatory: heredocs break
  on apostrophes. Use `Write` to `/tmp/<action-id>-msg.txt`, then
  `git commit -F /tmp/...`. Pattern in LESSONS.md.
- **"Confirm to commit?" gating** before every commit — established
  pattern.
- **Verify-before-asking discipline** — NAMED (LESSONS.md Session 10)
  + REINFORCED Session 11 (path-A divergence + replaced_in_place
  trace-back bug both surfaced via proactive verification).
  Standard pre-commit verification set: file content re-read, schema
  conformance check (jsonschema strict, not just in-script),
  test surface invariant check, anti-trip scan on any synthetic
  test_purpose, byte-exact match for derived numeric fields,
  idempotency re-run, debug-artifact scan, scope-creep scan via
  `git status` outside bulk scope.
- **NEW Session 11 LESSONS.md addition**: "Defer prose-only schema
  fixes; bump only when machine schema changes" — applies forward
  to any W4.2 surprise where META_SCHEMA expected.json prose
  conflicts with reality but `expected.schema.json` machine
  constraints are unaffected.
- **Pre-push gate** may include validate_consistency failure from
  operator-side eval_data work. The 4 unstaged operator-side files
  in the locked tree are documented and routinely pass the gate;
  if the gate fails, STOP and ask the operator. Never use
  `--no-verify`.
- **Plan is read-only** — never edit
  `BARCADA_CRAWLER_REMEDIATION_PLAN.md`. Workstream C scope
  amendment (deferred Stage 3 expected-output generation) flagged in
  commit messages `9165791` and `8aafc45`; not re-staged in W4.1
  `9e1bda9`. Operator decision needed: re-stage in subsequent W4
  commit messages, or treat as staged-once-and-carried-via-workspace-
  handoff. Do not amend the plan document yourself.
- **Shell cwd drift**: use absolute paths or `cd /Users/administrator/
  projects/barcada-scraper` at the start of each Bash chain.
- **Workspace cwd**: when editing LESSONS.md / SESSION_LOG.md /
  this template, work in `/Users/administrator/crawler-audit/`.
- **W4 tag deferred**: NO `workstream-0-week4-end` tag at Session
  11 close; tag lands at full W4 close (W4.3 complete) with
  required annotation per Flag 1 constraint #2.
- **Flag 3 (W4 tag provenance)** still flagged, not a blocker —
  revisit at full W4 close.
- **W4.2 may extend or fork the generator script.** The W4.1
  `tests/fixtures/generate_meta_json.py` could grow a second CLI
  mode (`--bulk-expected`) or a sibling `generate_expected_json.py`
  could be created. Engineering-design decision at Session 12 draft
  time — present recommendation with tradeoffs (shared helpers
  argue for extension; separable purposes argue for sibling).
- **Worked-example handling**: the existing
  `tests/fixtures/html/legitimate_business/expected/twilio.com.json`
  carries a `_placeholder` parser_output marker (W4.0 schema-lock
  shape demo). W4.2 either replaces it with real parser output OR
  protects it via `PROTECTED_PRE_EXISTING_*` analogous to the
  meta.json protection. Operator decides at W4.2 sample-review
  time.
- This template's structured fields will need refilling at
  Session 12 close.
