# Session 42 prompt — A-classify E18: PREDICTION_COLUMNS real-artifact re-pin (the ONLY open A-classify item)

**Drafted at S41 close (2026-06-05), operator-commissioned.** Mirrors the
S20/.../S41 prompt structure (7-phase, strict order, halt-on-mismatch). Scoped
NARROWLY to E18. Re-read on session open.

This prompt lives at `~/crawler-audit/SESSION_42_PROMPT.md`.

---

## WHAT THIS IS

A-classify is BUILT and SHIPPED on the `barcada-baseline drift` subcommand:
PART 2 (classify metrics, S40 `3266bc4`, tag `barcada-drift-classify-part2-v0`)
+ PART 1 (classify-native input mode, S41 `b41cf72`). The producer framing was
RETIRED — PART 1 landed as a comparator INPUT MODE that consumes a STANDALONE
predictions parquet (`domain` + the 6 PREDICTION_COLUMNS); there is NO
`--classify` producer and `canary.py` is UNTOUCHED.

**The ONLY open A-classify item is E18: re-pin the 6 `PREDICTION_COLUMNS`
against a REAL produced 16-col Stage-1 predictions partition with a real 12-char
SHA `model_version`.** They are currently pinned against the SOURCE SCHEMA
`src/barcada_scraper/classifier/stage1/output_schema.py:103-124` — the
authoritative definition, NOT stage3 and NOT the 15-col May-09 **dev** sample —
but never confirmed against a real produced artifact. This session clears that
gate IF a real partition exists, else records it still-deferred and closes.

This is NOT a build. It is a verification + (only if the schema drifted) a
tightly-scoped pin update. Do NOT rebuild PART 1/PART 2, do NOT build a
producer, do NOT touch `src/`.

Full gate text: `A_CLASSIFY_PROMPT.md` Open/carry-forward **(c)**.

---

## Scope

E18 ONLY. Repo HEAD at `b41cf72` (S41 classify-native input mode). Workspace
HEAD at `f10a7dc` (S41->S42 transition refill; succeeds the S41 close-out
`a0db876`).

The 6 pinned columns (`drift_classify.PREDICTION_COLUMNS`, S40, BYTE-IDENTICAL
since): `is_business, confidence, lr_probability, abstain, tier_decided,
model_version`. Their polars dtypes are `drift_classify.prediction_dtypes()`.

**Two possible outcomes, both legitimate:**
- **CLEARED** — a real 16-col partition exists, its columns + dtypes for the 6
  pinned fields MATCH; deliverable = a hermetic test that pins the real schema +
  a recorded confirmation; E18 closes; PART 1 / A-classify declared COMPLETE.
- **DRIFTED** — a real partition exists but the schema moved (renamed/re-typed a
  pinned column, or the SHA shape differs); deliverable = update
  `drift_classify.PREDICTION_COLUMNS` + `prediction_dtypes()` + the comparator
  branch(es) in `drift.py` + the affected tests, FIRST, with the per-commit
  checkpoint; then close E18.
- **DEFERRED (no-ship)** — no real 16-col partition exists (only the 15-col dev
  sample, or none). E18 stays deferred; record the decision; no code commit. A
  no-ship close at Phase 6 is NOT a failure.

---

## Halt protocol (when any phase's halt-condition fires)

```
HALT @ Phase N step S.s
Expected:    <claim from prompt>
Observed:    <actual reality from source/artifact>
Discrepancy: <one-line summary>
Surfacing to operator. Awaiting guidance.
```

After a halt: do NOT mutate repo/workspace, do NOT proceed, wait for operator
guidance. Halt is the contract. **S40 anchor:** the metric-field HALT (0.C —
signals_business_score is an INPUT not a prediction). **S41 anchor:** the
producer-dependency HALT (parser_parquet is a separate non-producing stage).
Apply the same discipline: verify the real-artifact schema at SOURCE before
re-pinning or declaring a match.

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

**Execution order (M1 — cheap decisive gate before expensive baseline):**
Run Step 0.1 (anchors) FIRST — you must trust the tree before trusting the
`find`. Then run **Phase 0.E18-UNBLOCK immediately** (below). Branch:
- **DEFER** (no real partition): skip Steps 0.3–0.6 (baseline/fixtures protect
  the per-commit checkpoint, and a no-ship makes NO commit — re-running them
  protects nothing; this is the project's "deterministically skippable Phase 0"
  lesson). Go to Phase 1 → record DEFERRED → Phase 6 workspace-only close.
- **PROCEED** (real partition found/provided): run Steps 0.3–0.6 (the baseline
  the per-commit checkpoint compares against), then Phase 1+.
Step 0.2 (tags) runs on either path (it's cheap and the close needs the count).

### Step 0.1 — Workspace + repo HEAD
```
git -C ~/crawler-audit rev-parse HEAD
# Expect: f10a7dc (S41->S42 transition refill) OR a later doc-edit commit
# succeeding it. Tolerate the unstaged SESSION_36_PROMPT.md (operator territory).

git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: b41cf72 (S41 WA0.W7.classify-native-input-mode). Parent 3266bc4 (S40).
# Tolerated delta: operator-side eval_data labeling commits in b41cf72..HEAD —
# verify each is strictly eval_data/* via `git show --stat`.
```

## Phase 0.E18-UNBLOCK — does a REAL produced partition exist? (BLOCKING; runs right after Step 0.1)

The gate needs ONE **genuine cascade-produced** Stage-1 partition
(`stage1_predictions/.../predictions.parquet`, written by
`src/barcada_scraper/classifier/stage1/run.py:15,169` with
`output_schema.SCHEMA`) that reflects the **current post-PR-COST 16-col schema**
(i.e. carries `llm_cached_input_tokens`, output_schema.py:118, + the cost/token
cols). NOT a synthetic/hand-authored test parquet, NOT stage3.

**Realness criterion (M2 — decouple `model_version` from the schema gate):**
the disqualifier is the SCHEMA, not the `model_version` VALUE. `model_version`
is one of the 6 pinned columns and is a `str` whether its value is a 12-char SHA
or `dev` — its value does NOT affect the schema pin. So:
- **GATE = a genuine cascade output carrying the current 16-col schema.** A
  16-col partition with `model_version == 'dev'` (legitimately produced OUTSIDE
  a git checkout — `_git_sha_or_dev()` fallback, run.py:639-651) **SATISFIES the
  schema gate.** Record the `dev` value as provenance; do NOT auto-defer on it.
- The 15-col May-09 dev sample is excluded because it is **pre-PR-COST (15-col)**,
  NOT because its `model_version` is `dev`. (Confirmed at S41 close:
  `~/Downloads/.../stage1_predictions_shard00003.parquet` — 15-col, missing
  `llm_cached_input_tokens`. All 6 pinned cols present with matching dtypes even
  there, so the pin is structurally sound; E18 is purely a PROVENANCE
  confirmation against a current-schema produced artifact.)

**Locate (bounded — N3):**
1. Local: `find /tmp /data <known-production-root> -path '*stage1_predictions*' -name '*.parquet' 2>/dev/null`
   (do NOT `find ~` unbounded; the only `~` candidate, the dev sample, is already
   known and excluded). For each hit: `pl.read_parquet(p).schema` → confirm 16
   cols incl. `llm_cached_input_tokens`; record the `model_version` value.
2. If none local: **surface and WAIT (M5).** Emit the no-find result and ask the
   operator for a real produced partition path (ADLS read needs creds CC lacks →
   operator runs the read or drops a local copy; S30 operator-run pattern, $0, no
   cascade run). Do NOT declare DEFERRED until the operator confirms none is
   available — the operator is in-loop and may hold one in ADLS.

**Outcomes:**
- A genuine 16-col partition found/provided → **PROCEED** (Step 0.3+ then Phase 1).
- 16-col but the operator confirms it is synthetic/not a real cascade output →
  not eligible; treat as no real partition.
- Operator confirms NO real produced partition exists (only the 15-col dev
  sample, or none) → **HALT-to-DEFER**: E18 stays deferred, no-ship. Do NOT
  manufacture an artifact, run the cascade, or accept the 15-col sample as the
  schema-of-record.

### Step 0.2 — Tags (15 expected; UNCHANGED from S41)
```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort | wc -l   # Expect 15
git -C /Users/administrator/projects/barcada-scraper rev-list -n 1 barcada-drift-classify-part2-v0  # Expect 3266bc4
# S41 placed NO new tag. The workstream-closing tag (barcada-drift-classify-v0 /
# a workstream-end tag) is placeable THIS session ONLY IF E18 clears and the
# drift workstream is then declared complete (Phase 5).
```

### Step 0.3 — Fixture counts (UNCHANGED)
```
.venv/bin/python -c "
from pathlib import Path
r = Path('tests/fixtures')
assert sum(1 for _ in (r/'html').rglob('*.html')) == 222
assert sum(1 for p in (r/'html').rglob('*.json') if '/expected/' in str(p)) == 202
assert sum(1 for _ in (r/'html').rglob('*.meta.json')) == 222
assert sum(1 for p in (r/'baseline-v0').rglob('*') if p.is_file()) == 1213
assert sum(1 for _ in (r/'synthetic_crawls').rglob('cassette.yaml')) == 30
assert sum(1 for _ in (r/'synthetic_crawls').rglob('extract_hard_exclusions.json')) == 30
print('OK fixtures 222/202/222/1213/30/30')
"
```

### Step 0.4 — Canonical baseline (expect 970; UNCHANGED)
Run the canonical 16-path invocation (per SESSION_TRANSITION_TEMPLATE.md
"Combined-suite-at-Session-open baseline"). Expect **970 passed**. The drift
tests live in `tests/drift/` (OUTSIDE the sweep).

### Step 0.5 — Step 0.8 sub-suites + combined floor
```
.venv/bin/python -m pytest tests/classifier/llm/test_prompt_logger.py -q   # expect 13
.venv/bin/python -m pytest tests/drift/ -q                                 # expect 62
# Combined floor = 1045 (970 + 13 + 62). The cumulative gate must NOT decrease
# (E18 may ADD a fixture/test; a same-shape 1<->1 dtype-pin replacement that
# changes a test is the only authorized non-increase, cited in the commit body).
```

### Step 0.6 — Drift deliverable + boundary presence
```
.venv/bin/python -c "from tools.baseline_v0 import drift, drift_classify; \
print('OK', len(drift_classify.PREDICTION_COLUMNS)==6 and bool(drift_classify.compute_classify_report) \
and bool(drift._reject_ambiguous_fetch_subset))"
git -C /Users/administrator/projects/barcada-scraper diff 3266bc4 --quiet -- tools/baseline_v0/drift_classify.py \
  && echo "drift_classify.py BYTE-IDENTICAL since S40 (boundary)"
git -C /Users/administrator/projects/barcada-scraper diff 3266bc4 --quiet -- src/ && echo "src/ UNCHANGED"
```

If any of 0.1-0.6 fail, HALT before doing any work.

---

## Phase 1 — Scope resolution + disposition determination (no code)

- **DEFER path:** Phase-0.E18-UNBLOCK found no real partition → no-ship. Record
  the decision; skip Phases 2–5; go to Phase 6 (workspace-only close, re-pin S43
  anchors). Done.
- **PROCEED path — CC DETERMINES the disposition here (it is a source-verify
  read, not an operator decision):** dump the real partition's schema
  (`pl.read_parquet(path).schema`) and compare the 6 pinned fields
  (`drift_classify.PREDICTION_COLUMNS` + `prediction_dtypes()`) against it AND
  against the live `output_schema.SCHEMA`. Produce the exact per-column
  name+dtype comparison table. From it, CC states:
  - **CLEARED** — all 6 names + dtypes match. (Expected: the dev sample already
    showed the 6 match; this confirms no post-PR-COST change touched them.)
  - **DRIFTED** — a pinned column was renamed/re-typed.
  Record the `model_version` value (SHA or `dev`) as provenance — NOT a
  disposition input.

The disposition is now KNOWN going into Phase 2; Phase 2 elicits only genuine
operator CHOICES, not determinations.

---

## Phase 2 — Design gate (AskUserQuestion; PROCEED path only)

The CLEARED/DRIFTED disposition and the `model_version` shape are already
DETERMINED at Phase 1 (source reads, not questions). Elicit only the genuine
choices:

- **Q-E18.1 Confirmation-fixture shape** — how to pin the real schema so the
  gate stays closed: (a) commit the partition's SCHEMA as a constant/fixture
  (names + dtypes only, no row data); (b) commit a tiny redacted partition
  (schema only) if a file fixture is preferred. Default (a) if the partition is
  sensitive.
- **Q-SHARED.1 Commit shape** — single self-contained commit (CLEARED: the pin
  test; DRIFTED: the pin update + tests).

Present the Phase-1 per-column comparison table alongside the questions so the
operator sees the determined disposition.

**HALT IF** the disposition would require a `src/` change, a `canary.py` change,
a producer, or any change beyond `drift_classify.py` + `drift.py` (classify
branch) + `tests/drift/` — surface as a design sub-question.

---

## Phase 3 — Implementation (only if unblocked; strict order)

### If CLEARED (match)
Add a hermetic test in `tests/drift/` that pins the real schema: the 6
PREDICTION_COLUMNS names + `prediction_dtypes()` equal the real partition's
schema (schema/dtypes only — no sensitive row data). This converts the deferred
E18 gate into a standing regression guard. No `drift_classify.py` change.

### If DRIFTED (mismatch)
**Guard (M4 — the S40 field-role trap, pointed at the one editable file):**
PREDICTION_COLUMNS stays the **6 behavioral fields ONLY**. The real partition
has 16 cols, but the other 10 — `llm_cached_input_tokens`, the cost/token
fields, `crawl_timestamp` — are NOT predictions; they are tolerated extras that
confirm the partition's PROVENANCE and must NEVER enter the pin. Re-pinning
"against the 16-col partition" means re-confirming the 6, not absorbing the cost
columns (that would repeat `signals_business_score`: a non-prediction field
mistaken for one).

Update, in this order, ONLY for a genuinely drifted pinned field:
`drift_classify.PREDICTION_COLUMNS` + `prediction_dtypes()` → the classify-native
dtype validation in `drift.py` (`_validate_classify_native_dtypes`) → the
affected `tests/drift/` builders + assertions. Keep the require-14 fetch path
BYTE-IDENTICAL and the B4b guard intact. `drift_classify.py` is editable ONLY
for this E18 pin.

### Per-commit checkpoint (every boundary)
1. Combined suite (canonical 16-path + the two Step 0.8 sub-suites) vs the
   Phase-0 baseline (970 / 1045). A new E18 test ADDS to the drift sub-suite.
2. Ruff check + format (touched files). Complexity < 15.
3. Verification table (claim -> reality -> status), every claim backed by
   captured output: the real-partition schema dump; the per-column match/mismatch;
   the new test count; canonical 970; combined floor; drift_classify byte-status;
   no src/. Any unevidenced row -> HALT.
4. git status — stage ONLY intended files; operator `eval_data/*` + `.claude`
   lock UNSTAGED.
5. "Confirm to commit?" — gate. `-F /tmp/<id>-msg.txt`; NO `-m`; NO backticks in
   body; NO `Co-Authored-By`.
6. Post-commit: re-run step 1; confirm clean tree.

---

## Phase 4 — Pre-push gate (whole-tree)
`ruff check .` + `ruff format --check .`, `vermin --target=3.10`,
`validate_consistency`. eval_data WIP halt protocol applies. Confirm no `src/`
delta and (if CLEARED) `drift_classify.py` still byte-identical.

---

## Phase 5 — Push + tag (after operator confirms)
- Push to `origin/main` after operator confirms.
- **Workstream-closing tag — placeable IF E18 CLOSES (CLEARED-match OR
  DRIFTED-fixed; both complete the workstream code).** Place
  `barcada-drift-classify-v0` at the E18 commit with an annotated message naming
  the milestones (`7bbdc74` S39 / `3266bc4` S40 / `b41cf72` S41 / this E18
  commit) and noting the operational cadence (scheduled run + diff) remains a
  deployment step. If E18 DEFERRED: place NO tag, no commit.

---

## Phase 6 — Workspace close-out
- Append the S42 entry to `SESSION_LOG.md` (the E18 disposition: CLEARED /
  DRIFTED / DEFERRED; the real-partition provenance; counts; tag).
- Refill `SESSION_TRANSITION_TEMPLATE.md` for S43 (repo/workspace anchors;
  canonical 970 / new combined floor; tag count; E18 status). Anchor-pin
  follow-up.
- Fold any LESSONS.
- Push workspace after operator confirms.

---

## Acceptance criteria
- **DEFERRED:** E18 still-deferred decision recorded; no repo commit; baselines
  re-pinned for S43.
- **CLEARED:** a hermetic test pins the 6 PREDICTION_COLUMNS + dtypes to the REAL
  partition schema; E18 closed; A-classify declared complete; combined floor
  re-derived + pinned (>= 1045).
- **DRIFTED:** PREDICTION_COLUMNS + dtype map + comparator + tests updated; all
  green; the same-shape change cited in the commit body; combined floor pinned.
- Shared: canonical 970 unchanged; the 22 fetch + the 62 drift tests green
  (zero deletions, except a cited same-shape pin replacement); ruff/format/vermin/
  validate clean; complexity < 15; NO `src/` change; NO producer; `canary.py`
  UNTOUCHED; require-14 fetch path byte-identical; B4b guard intact; every
  commit-message claim backed by captured output.

---

## Boundaries (load-bearing)
- E18 ONLY. No rebuild of PART 1/2, no producer, no `--classify` flag, no
  `canary.py` change, no `src/` change.
- `drift_classify.py` is editable ONLY to update the PREDICTION_COLUMNS pin /
  dtype map per E18 (the DRIFTED path); otherwise byte-identical.
- No cascade run, no Azure call, no spend this session. Reading a real partition
  is a $0 read; if it needs creds, the operator runs it (S30 pattern).
- Do NOT accept the 15-col May-09 dev sample or a synthetic test parquet as the
  schema-of-record; the gate requires a REAL produced **16-col current-schema**
  partition (the `model_version` VALUE is provenance, not the gate — see below).
- Verify-before-trust: dump the real artifact's schema and compare at SOURCE
  before re-pinning or declaring a match. The TREE/artifact wins over this
  prompt; if a file:line here is stale, the live tree wins.
- **`model_version` value is NEVER a gate disqualifier** (M2). The schema pin
  cares that `model_version` is a `str`, not whether its value is a SHA or `dev`.
  A 16-col current-schema partition with `model_version=='dev'` satisfies E18;
  record the value as provenance. The dev SAMPLE is excluded for being 15-col
  (pre-PR-COST), not for its `model_version`.
- **PREDICTION_COLUMNS stays the 6 behavioral fields** (M4). The cost/token/
  timestamp columns in a 16-col partition confirm provenance only; they must
  never be added to the pin. E18 is a provenance confirmation of the 6, not a
  re-derivation against all 16.
- **DEFERRED skips Phases 2–5** (N2): no repo commit, Phase 6 workspace-only.
  On CLEARED/DRIFTED, "A-classify COMPLETE" is recorded in SESSION_LOG **and**
  carry-forward (c) is marked CLOSED.
