# Session Transition Template — Handoff from Session 10 → Session 11

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-9
are summarized in SESSION_LOG.md; Session 10 close is in the most
recent SESSION_LOG.md entry.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

---

## Handoff metadata

- Outgoing session number: 10
- Closing date: 2026-05-20
- Outgoing session scope: Open Workstream 0 Week 4. Resolve the
  three carried items from Session 9 close (Flag 1 cost ceiling,
  Flag 2 verify-before-asking promotion, Flag 3 W4 tag provenance).
  Land the W4.0 meta.json + expected.json schema lock plus a worked-
  example pair (twilio.com) per plan §3 Week 4. Flag 1 → Option (c)
  defer Stage 3 to Workstream C. Flag 2 → Option (c) status quo with
  LESSONS.md additions landing this session. Flag 3 stays flagged.
- Reason for transition: natural seam at W4.0 schema-lock close.
  W4.1 (bulk meta.json generation across 198 fixtures) is a
  substantially different work unit; per-fixture verification +
  operator-review-of-script-output cadence warrants fresh context.
  Session 10 close at ~25% context remaining is below the 50% margin
  preferred for a 198-file generation pass.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `8aafc45`
- Last commit subject: `W4.0-worked-example-twilio: twilio.com.meta.json + expected/twilio.com.json`
- Branch sync with `origin/main`: 0 commits ahead, 0 commits behind
- Tags (do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3` (nuclear-revert anchor)
  - `workstream-0-week1-end` at `4f9d23f` (Week 1 close)
  - `workstream-0-week2-end` at `e5d2f91` (Week 2 close)
  - `workstream-0-week3-end` at `cf0c14c` (Week 3 close)
  - NO `workstream-0-week4-end` tag yet — W4 spans multiple sessions;
    tag lands at full W4 close (operator decision Session 10).
- Pre-push gate state at HEAD: ALL CHECKS PASS (ruff check, ruff
  format --check, vermin --target=3.10-, validate_consistency for
  eval_data)
- Unstaged changes intentionally ignored across sessions (operator-
  side work in the locked tree, unchanged since Session 8 close):
    .claude/rules/code-correctness.md
    eval_data/README.md
    eval_data/TAXONOMY_GAP_LOG.md
    eval_data/stage1_labels.jsonl

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA: TBD (filled in after Session 10 close commit
  pushes)
- Last commit subject: Session 10 close: SESSION_LOG.md Session 10
  append + LESSONS.md "Verify-before-asking discipline" section +
  SESSION_TRANSITION_TEMPLATE.md refill for Session 11
- Branch sync with `origin/main`: 0 commits ahead (after push)

---

## Active task list

The Session 10 task list (carried-item resolution + W4.0 schema lock)
is fully complete:
- Flag 1 (cost ceiling) — RESOLVED → Option (c), defer Stage 3 to
  Workstream C
- Flag 2 (verify-before-asking promotion) — RESOLVED → Option (c)
  status quo; LESSONS.md additions landed
- Flag 3 (W4 tag provenance) — still flagged, not a blocker, revisit
  at full W4 close
- W4.0 schema lock — META_SCHEMA.md + meta.schema.json +
  expected.schema.json landed (`9165791`)
- W4.0 worked example — twilio.com.meta.json + expected/twilio.com.json
  landed (`8aafc45`)

Task state is session-local in Claude Code; it does NOT carry across
sessions.

Session 11 should TaskCreate fresh tasks on open for Workstream 0
Week 4 continuation. Suggested tasks:

- **W4.1 bulk meta.json generation across the corpus** (NEXT
  CONCRETE WORK UNIT). 198 fixtures need meta.json files. Per W4.0
  schema + Truth 1/2: scripted generation reading each fixture's
  .html, deriving fields per the conventions documented in
  `tests/fixtures/META_SCHEMA.md` §2 and §5. Operator review of
  script output before bulk commit.

  Field-derivation recipes (per META_SCHEMA §2.4 + §5):
  - `source_url`: `<link rel="canonical">` from .html;
    `https://<bare-domain-from-filename>/` fallback when no
    canonical. provenance_note:
    `approximated_from_canonical_html_link` or
    `approximated_from_bare_domain_fallback`.
  - `captured_at`: `git log --diff-filter=A --follow --format=%aI <path>`
    converted to UTC ISO 8601 with Z suffix. provenance_note:
    `approximated_from_git_log_author_date`.
  - `capture_method`: per session-log mapping. W0 Sessions 5+
    captures with `curl -sSL -A "..."` pattern →
    `curl_with_retries`. Pre-Session-1 corpus (origin not
    recoverable) → `historical_unverified`. Synthetic fixtures
    identifiable by filename prefix (`synthetic_*` or
    `*_synthetic*`) → `synthetic` or `synthetic_with_real_markers`
    depending on documented marker-fidelity discipline.
  - `content_type`: `"text/html; charset=utf-8"` default for HTML
    fixtures. provenance_note: `approximated_from_plan_default`.
  - `content_length`: `os.path.getsize(<path>)`. Directly observed
    (no provenance_note needed).
  - `encoding`: `"utf-8"` default. provenance_note:
    `approximated_from_plan_default`. (Week 5 encoding-variant
    fixtures will deviate per plan §3 W5 line 186.)
  - `response_status`: derive from directory category. 200 for
    `legitimate_*`, `parking_*`, `mega_menu/`, `spa_hydration_*/`,
    `international_business/`, `meta_refresh_parking/`,
    `noindex_empty_title/`, `cloudflare_challenge/`, `login_wall/`,
    `spa_shell/`. 403 for `auth_403/`. 401 for the 4 nginx-401
    fixtures moved into `parking_default_pages/` by C0.7c (need
    per-file split; see C0.7c commit `4f8dc06` for the file list).
    provenance_note: `approximated_from_directory_category`.
  - `expected_outcome`: structured JSON per META_SCHEMA §2.2; values
    derived from directory category + Flag 1 sentinel triple for
    stage3_partner.
  - `test_purpose`: free-text per fixture; if `capture_method` is
    synthetic-variant, apply META_SCHEMA §2.3 anti-trip discipline
    (future-proofing).

- **W4.2 expected/<domain>.json generation** (Stage 1/2 only per
  Flag 1 resolution). Per-fixture expected pipeline outputs.
  parser_output deterministic-serialized per plan §4 lines 232-234.
  Stage 1 + Stage 2 decisions derived by running each fixture
  through the actual pipeline (Stage 1 RULES-first, Stage 2 LR-first
  per plan §3 W4 example). Stage 3 populated with canonical sentinel
  triple per META_SCHEMA §3.1. Expected near-zero LLM cost; stop and
  escalate if spend trends higher than near-zero before $50 alert
  threshold.

- **W4.3 Test infrastructure** (may span into Session 12). Update
  conformance tests to compare against expected/<domain>.json
  (replacing current "exclusion_reason must be empty" assertions
  with full comparison logic that respects the Stage 3 sentinel
  comparison-skip directive per Flag 1 constraint #5 semantic α).

- **W4 close + tag annotation**. At full W4 close, tag
  `workstream-0-week4-end` at the final green-gate SHA. Annotation
  must state (per Flag 1 constraint #2, verbatim):
  "Stage 3 expected-outputs deferred to Workstream C per Flag 1
  resolution; partial coverage at W4 close is intentional, not
  incomplete."

---

## Outstanding operator-input requests blocking Session 11

**W4.1 script preview** — operator review of the bulk-generation
script output (sample meta.json files for ~5-10 representative
fixtures from different categories) before bulk commit. Per
plan §3 W4 deliverable cadence: "Generate expected outputs once,
human-review them, commit."

**Workstream C scope amendment** flagged for operator authorization.
Deferred Stage 3 expected-output generation lands in Workstream C
scope per Flag 1 resolution; that's a plan-document amendment —
read-only territory, operator authorization required. Staged in the
W4.0-schema-lock commit message (`9165791`) and the worked-example
commit message (`8aafc45`) for operator handling outside session
work. Not a Session 11 blocker for W4.1; will matter at Workstream C
scoping.

---

## Operator decisions made during Session 10 (cross-ref to SESSION_LOG.md)

- **Flag 1 (cost ceiling reconciliation)**: Option (c), defer Stage 3
  LLM calls; Stage 3 expected-output generation lands in Workstream C
  scope. Four execution constraints carried forward (see SESSION_LOG.md
  Session 10 entry).
- **Flag 2 (verify-before-asking promotion)**: Option (c), status quo.
  Five-bullet reasoning + four execution constraints (LESSONS.md
  additions landed this session) in SESSION_LOG.md.
- **W4.0 schema review batch resolutions** (items #1-#8): all
  resolved this session; recorded in SESSION_LOG.md Session 10 entry.
- **Two corrections to the W4.0 draft**: Correction A (sub-option (i)
  pro overclaim) + Correction B (const-vs-pattern schema_version
  fix). Both applied before schema-lock commit.
- **Truth 1 + Truth 2**: corpus-wide truths for historical-capture
  source_url + content_type/encoding/response_status, landed in
  META_SCHEMA.md §5.
- **provenance_note structured-object form**: per-field granularity
  preserved across ~196 historical-capture fixtures.
- **stage3_decision sub-option (i)** (include with sentinel) +
  sentinel semantic (α) (comparison-skip directive).
- **capture_method enum drop `playwright`**: reserved for future
  semver bump when actual Playwright captures land.
- **historical_unverified catch-all**: for pre-Session-1 corpus +
  fixtures whose origin isn't recoverable.
- **Plan is read-only**: unchanged from prior sessions (memory:
  `feedback_remediation_plan_readonly.md`).

---

## Pattern note for Session 11 (carried-item resolution vs engineering design)

Session 10 established a clear pattern distinction observed by the
operator:

- **Carried-item resolution** (operator-authority decisions like
  Flag 1 cost ceiling, Flag 2 discipline promotion): pre-staged
  options from `SESSION_TRANSITION_TEMPLATE.md` (verbatim source-of-
  truth) + Session-N-authored pros/cons grounded in source files
  with rigorous provenance citation. No preferred path proposed.
  Operator decides among the staged options.

- **Engineering design** (schema design, script design, anything
  where Claude Code drafts a recommended approach): single-unit
  drafting with all field-by-field decisions integrated, recommended
  approaches with source-cited tradeoffs, batch operator review at
  the artifact level. Operator can correct individual decisions but
  the default cadence is artifact-level review, not per-decision
  pre-approval.

W4.1 bulk meta.json generation falls under engineering design.
Session 11 should draft the W4.1 generation script as a single unit,
run it against a sample of 5-10 representative fixtures, present
the sample meta.json files for operator review, then run the full
bulk generation after sample approval.

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
  SESSION_LOG.md Session 6 entry) — DO NOT touch in Session 11.
- **NEW Session 10**: `tests/fixtures/META_SCHEMA.md` +
  `tests/fixtures/meta.schema.json` + `tests/fixtures/expected.schema.json`
  are the locked W4.0 schema artifacts. Schema bumps land via
  documented semver progression per META_SCHEMA §4, NOT via inline
  edits to v1.0.

---

## Next concrete work unit

- **Action ID:** **W4.1** (bulk meta.json generation across the
  198-fixture corpus per META_SCHEMA v1.0).
- **Scope:** Author the bulk-generation script (likely Python,
  reading each .html under `tests/fixtures/html/<category>/`,
  emitting `<domain>.meta.json` alongside per the field-derivation
  recipes in the Active task list above). Run against a 5-10-fixture
  sample first; present sample output to operator for review; bulk
  commit after sample approval.
- **Acceptance criteria:**
  - 198 meta.json files generated, one per .html in the corpus.
  - Each meta.json conforms to `tests/fixtures/meta.schema.json`
    (verifiable via JSON Schema validator).
  - `provenance_note` annotations correctly applied to approximated
    fields per META_SCHEMA §2.4 vocabulary.
  - Test surface invariant 17/169/2 preserved (_iter_fixtures globs
    `*.html` only; .meta.json invisible to conformance tests).
  - Pre-push gate green at the bulk commit SHA.
  - Bulk commit may be split into per-directory commits if operator
    prefers per-category review cadence; OR single bulk commit if
    operator prefers atomic landing. Operator decides at sample-
    review time.
- **Files expected to be touched:** 198 new `<domain>.meta.json`
  files under `tests/fixtures/html/<category>/`. Plus the bulk-
  generation script (location TBD — possibly
  `tests/fixtures/generate_meta_json.py` or `scripts/fixtures/`).
  Possibly an update to `tests/fixtures/META_SCHEMA.md` if the bulk-
  generation surfaces edge cases the schema didn't anticipate (e.g.,
  unusual directory categories not in the response_status mapping).
- **Files NOT to be touched:** everything under `eval_data/`,
  `stage1.schema.json`, the tags, `BARCADA_CRAWLER_REMEDIATION_PLAN.md`,
  the 17 Week-5 punch-list fixtures, and the W4.0 schema artifacts
  themselves (META_SCHEMA.md + meta.schema.json + expected.schema.json
  are locked; schema bumps require semver progression per
  META_SCHEMA §4).

---

## Required reading (Session 11 first 10 minutes)

In this order:
1. **This file** (you're reading it).
2. **`LESSONS.md`** — operator patterns and observed conventions.
   Pay particular attention to:
   - **NEW Session 10**: "Verify-before-asking discipline" section
     (header naming + operator-ratchet + A/B/C trigger condition) —
     Flag 2 Option (c) execution constraints; the discipline now
     has a durable name.
   - "Detector precision findings" (FPs 1/2/3 + FNs 1/2/3 +
     deeper-circularity meta-observation) — the W4.2 expected-output
     generation can hit these same detectors. Manual review of any
     expected outputs where `exclusion_reason != ''` recommended.
   - "Synthetic-fixture HTML comments are regex-visible" — applies to
     any synthetic fixture's meta.json `test_purpose` field if that
     field passes through any regex check (currently future-
     proofing-only per Session 10 item #7 verification).
3. **`SESSION_LOG.md` Session 10 entry** — Flag 1 / Flag 2 / W4.0
   schema-lock + worked-example resolutions and the two commits
   (`9165791`, `8aafc45`).
4. **`tests/fixtures/META_SCHEMA.md`** — NEW W4.0 deliverable, the
   schema spec for both meta.json and expected/<domain>.json. Read
   §2 (meta.json), §3 (expected.json), §5 (historical capture
   limitations), §3.1 (sentinel values) carefully. W4.1 bulk
   generation operates against this schema.
5. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §3 Week 4** — meta.json
   and expected-outputs spec (W4.0 deviations documented in
   META_SCHEMA.md). **READ-ONLY.**
6. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §14 Session Continuity
   Discipline** — referenced for Session 11 close-out cadence.

After reading, verify repo state:

```
git -C /Users/administrator/projects/barcada-scraper status
git -C /Users/administrator/projects/barcada-scraper log --oneline -5
git -C /Users/administrator/projects/barcada-scraper tag -l 'workstream-*'
```

Expected:
- Last commit SHA: `8aafc45` (W4.0-worked-example-twilio).
- Recent commits include `9165791` (W4.0-schema-lock).
- Tags: `pre-remediation-2026-05-19` + `workstream-0-week1-end` /
  `week2-end` / `week3-end`. NO `week4-end` tag yet.
If anything differs, surface to operator before doing work.

Then begin W4.1 (bulk meta.json generation). Generate sample first
(5-10 representative fixtures across different categories), present
to operator, await sample approval before bulk run.

---

## Risk register state (plan §11)

Recent additions (Sessions 4-10):
- "Recapture tooling needs retry policy" — STILL applies to every
  Session 11 capture (likely none in W4.1, but applies if any
  recapture is triggered).
- Forward-applicable lessons in LESSONS.md (plan is read-only, so
  they cannot land in §11 itself):
  - "Probe framework generation before locking a fixture spec"
    (Session 7)
  - "Synthetic-fixture HTML comments are regex-visible" (Session 8)
  - "Detector precision findings" with FPs and FNs (Session 9)
  - "Audit-spec vs. production-reality drift" (Session 9)
  - **NEW Session 10**: "Verify-before-asking discipline" (header
    naming + operator-ratchet + A/B/C trigger condition). The
    discipline is the durable name for the operator-pattern observed
    across S7-S9; promotion deferred per Flag 2 Option (c); reopens
    on Workstream A/B/C finding per the documented trigger
    condition.

Open latent gap (Issue 3 from Week 2 audit erratum, unchanged):
- Project's ruff `select` does not include "C" (mccabe), so
  cyclomatic-complexity violations escape pre-push. Manual
  `ruff check --select C901 <file>` in any code-modifying commit
  is the workaround until a project-config commit closes the gap.
  W4.1 bulk-generation script is the first Session-11 code-modifying
  candidate; apply the manual check.

LLM cost drift risk (plan §11) — Session 10 update:
- Flag 1 resolution (Option c) defers Stage 3 LLM calls to
  Workstream C. W4.2 expected-output generation runs through Stage
  1/2 only — expected near-zero LLM cost. Stop and escalate if
  actual W4.2 spend trends higher than near-zero before $50 alert
  threshold. Cost ceiling $100 untouched and unchanged.

No new risks escalated and unresolved by Session 10.

---

## Cost & schedule tracking

- Cost ceiling: $100 (operator-set 2026-05-19, alert at $50)
- Cost incurred Sessions 1-10: $0 (no LLM API calls; curl + pytest
  + handwritten Python + handwritten synthetic only)
- Cost budget remaining: $100
- Cost-vs-plan inconsistency from Session 9: RESOLVED at Session 10
  Flag 1 Option (c) — Stage 3 deferred to Workstream C; W4.2 expected
  spend near-zero
- Schedule: 3 weeks elapsed of Workstream 0's 5-week budget.
  - Weeks 1-3 COMPLETE.
  - Week 4 OPEN: ~25% complete (W4.0 schema lock done; W4.1 +
    W4.2 + W4.3 pending). Likely spans Sessions 11-12.
  - Week 5 still ahead.

---

## Notes for Session 11

- **Conformance test red count at handoff is 17** (Week 5 punch
  list, unchanged from Week 1 close). Every Session 11 commit
  should verify the count stays at 17 unless the commit itself
  deliberately changes test infrastructure (W4.3 may legitimately
  shift counts when expected.json comparison replaces "exclusion_
  reason must be empty" assertions — document any deliberate shift
  in commit message).
- **2 conformance tests SKIP** (empty parametrize for `soft_404/`
  and `empty_google_sites/`) — both await Week 5 C0.3-followup /
  C0.4-followup repopulation.
- **The Session-10-close test surface is 17 fail / 169 pass / 2 skip.**
- **File-based commit messages** still mandatory: heredocs break
  on apostrophes. Use `Write` to `/tmp/<action-id>-msg.txt`, then
  `git commit -F /tmp/...`. Pattern in LESSONS.md.
- **"Confirm to commit?" gating** before every commit — established
  pattern.
- **Verify-before-asking discipline** — NOW NAMED (LESSONS.md
  Session 10 addition). Proactive application by the assistant
  catches what the operator-ratchet would catch; ratchet is a
  backstop, not the primary mechanism. Standard pre-commit
  verification set: file content re-read, schema conformance check,
  test surface invariant check, anti-trip scan on any synthetic
  test_purpose, byte-exact match for derived numeric fields.
- **Three LESSONS.md sub-sections to apply forward in W4.1**:
  detector precision findings (don't trust raw extract_hard_exclusions
  output for expected_outcome generation without manual review);
  audit-spec drift (don't trust plan literal examples for meta.json
  field values without verification); synthetic comments are regex-
  visible (anti-trip on test_purpose field, future-proofing per
  Session 10 item #7 verification).
- **Pre-push gate** may include validate_consistency failure from
  operator-side eval_data work. The 4 unstaged operator-side files
  in the locked tree are documented and routinely pass the gate;
  if the gate fails, STOP and ask the operator. Never use
  `--no-verify`.
- **Plan is read-only** — never edit
  `BARCADA_CRAWLER_REMEDIATION_PLAN.md`. Workstream C scope
  amendment (deferred Stage 3 expected-output generation) flagged in
  commit messages `9165791` and `8aafc45` for operator handling;
  do not amend the plan document yourself.
- **Shell cwd drift**: use absolute paths or `cd /Users/administrator/
  projects/barcada-scraper` at the start of each Bash chain.
- **Workspace cwd**: when editing LESSONS.md / SESSION_LOG.md /
  this template, work in `/Users/administrator/crawler-audit/`.
- **W4 tag deferred**: NO `workstream-0-week4-end` tag at Session
  10 close; tag lands at full W4 close (W4.3 complete) with
  required annotation per Flag 1 constraint #2.
- **Flag 3 (W4 tag provenance)** still flagged, not a blocker —
  revisit at full W4 close.
- This template's structured fields will need refilling at
  Session 11 close.
