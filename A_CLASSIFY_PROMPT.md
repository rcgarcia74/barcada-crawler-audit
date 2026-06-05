# Session prompt — Candidate A-classify (barcada drift, classifier-prediction)

## WHAT THIS IS
#   Candidate A, CLASSIFY fork — the Item-8-as-written drift surface. Detects
#   drift in CLASSIFIER BEHAVIOR (predictions changing run-over-run), which
#   the fetch-health canary CANNOT surface. TWO-PART candidate; the FIRST
#   non-$0 one (recurring LLM spend — though <$1/run, so cost is a guardrail,
#   not a blocker); commission only after the Phase-0.COST gate clears.

## WHAT A-FETCH ALREADY SHIPPED (now a CONSTRAINT, not a hypothetical)
#   A-fetch landed the drift COMPARATOR as a subcommand (S39 @ 7bbdc74):
#     python -m tools.baseline_v0 drift --baseline PREV.parquet --current CURR.parquet
#   with: exit 0=no-drift / 1=drift / 2=input-or-schema-error; inner-join on
#   `domain` + appeared/disappeared reported separately; schema validated by
#   importing canary.PARQUET_COLUMNS + canary._make_dtypes() (require all 14,
#   reject missing/dtype-mismatch, TOLERATE EXTRAS); stdout table + --report
#   JSON; hermetic tests at tests/drift/test_drift.py (OUTSIDE the 16
#   canonical paths, tracked as a Step 0.8 sub-suite — headline stayed 970).
#   A-classify EXTENDS this surface; it does NOT build a parallel one.
#
#   The single most important reconciliation: A-fetch's comparator TOLERATES
#   EXTRA COLUMNS. That is exactly what makes the append-only producer change
#   below SAFE — a prediction-bearing parquet still validates as a fetch
#   parquet (the 14 are present; predictions are tolerated extras). This must
#   be PROVEN (run the A-fetch comparator against a prediction parquet), not
#   assumed.

## WHY IT IS A BIGGER COMMITMENT (source-verify — RE-VERIFY at Phase 0)
#   canary (tools/baseline_v0/canary.py) emits ONLY fetch-health: the 14-col
#   canary.PARQUET_COLUMNS (@ canary.py:66-81) — no is_business, confidence,
#   or any prediction column. So classifier-prediction drift is NOT
#   computable from current output. The producer extension is BIGGER than
#   "add a flag": the cascade entry (cascade.py:314 async _run_stage1(*,
#   parser_parquet, components, lr_bundle, thresholds, ...) / stage1/run.py:150
#   run_shard) consumes a PARSER PARQUET (parsed page features) + constructed
#   components, NOT raw HTML. AND it WRITES its predictions to a SEPARATE
#   output parquet (stage1/run.py:15,169 — "one shard in -> one
#   stage1_predictions/.../predictions.parquet out", atomic temp+rename) with
#   its own output_schema.SCHEMA. So PART 1 = fetch -> run the parser to build
#   the cascade's parser_parquet input -> load components (lr_bundle, embedder,
#   adjudicator) -> bridge sync->async (asyncio.run) -> run the ASYNC cascade
#   -> READ BACK the predictions.parquet it wrote -> select the prediction
#   fields -> append them to the canary rows. It routes each of the 50 domains
#   through the cascade and incurs RECURRING per-domain LLM spend. Everything
#   through A-fetch was $0; this is the first non-$0 candidate. Size the
#   producer for the full chain (parser + components + async cascade + output
#   read-back), not a flag.

## NOTE: canary.py is TOOLING (tools/), not src/ — no production lock applies
# to editing it. The classifier cascade it will CALL lives in src/ and is
# INVOKED, not modified (no src/ change this session).

## LABEL GATING (scope boundary)
#   Drift = behavior change → needs predictions, NOT labels:
#     - on the REAL prediction OUTPUTS (output_schema.py:103-124):
#       is_business-AGREEMENT (run-N vs run-N-1), KS on the `confidence`
#       distribution, and abstain-rate shift are LABEL-FREE and IN scope.
#       (signals_business_score is the Tier-1 rules INPUT, run.py:21,317 — NOT
#       a prediction; using it would measure INPUT drift, so it is OUT.)
#     - Brier / calibration drift needs predicted-probability + a TRUE LABEL,
#       so it is GATED on Stage 2/3 labeling (PR-D/E) and is OUT of scope.
#       Do NOT build a calibration metric this session.
#
# CHAT-SIDE ROLE: advisory/review-only. CC implements under phase governance
# and VERIFIES every claim against captured output BEFORE committing.

## Scope (two sequenced sub-surfaces)

**STATUS at S41 open: PART 2 is SHIPPED (S40 `3266bc4`); PART 1 is the remaining
work and is BLOCKED.** PART 2 (the classify-drift comparator + metrics) landed —
do NOT rebuild it. THIS session is PART 1 (the producer) ONLY, and only if its
unblock check clears (Open/carry-forward (a) — the worker_loop.py:193
parser_parquet partition must exist). If still blocked, no-ship. PART 2's
contract below is now reference (what the producer must FEED): the comparator
auto-detects PREDICTION_COLUMNS and computes is_business-agreement /
confidence-KS / abstain-|Δ| (gating) + lr_probability-KS / tier-mix /
model_version (report-only).

PART 1 — Producer extension: add an OPT-IN classifier leg to canary-run
(e.g. a `--classify` flag). The chain per domain is fetch (existing) -> run
the parser to assemble the cascade's parser_parquet input -> construct
components (lr_bundle, embedder, adjudicator) -> bridge sync->async
(asyncio.run) -> run the cascade at the agreed depth -> READ BACK the
predictions.parquet the cascade wrote (its own output_schema.SCHEMA) ->
APPEND the selected prediction columns. WITHOUT the flag, canary-run stays
exactly 14-col fetch-only (A-fetch comparator unaffected, zero LLM). WITH the
flag, output = the 14 fetch columns (unchanged, in order) + a separate
PREDICTION_COLUMNS set. NOTE the writer: _write_parquet hardcodes schema to
the 14 (schema={c: _PARQUET_DTYPES[c] for c in PARQUET_COLUMNS},
canary.py:193) — the --classify path needs its own assembled schema
(14 + PREDICTION_COLUMNS), not that dict. Incurs live LLM spend only when the
flag is used.

PART 2 — Classify-drift comparator: compute the agreed LABEL-FREE metric(s)
— is_business-agreement and/or KS on the `confidence` distribution and/or
abstain-rate shift (on the real output_schema.py:103-124 predictions) — over
two prediction-bearing parquets, REUSING A-fetch's comparator scaffold (the
inner-join, appeared/disappeared, exit-0/1/2 contract, --report shape). It
extends, not forks. KS is computable via scipy.stats.ks_2samp (scipy 1.17.1
is already a dependency — NO new dependency required; do not hand-roll KS).

OUT of scope: calibration/Brier (label-gated); live alert wiring + dashboard
(joint/prod); launchd kit install (production); ANY change to the 14
fetch columns or their order; making predictions mandatory (the flag keeps
fetch-only runs cheap).

## Phase 0 — Cold-start + source-verify re-confirm (halt-on-mismatch)

Run in order. HALT and surface to operator on ANY mismatch (the halt protocol
is the contract — do not mutate the repo/workspace after a halt). All anchors
below were VERIFIED green at the S40 close (2026-06-04) at repo `3266bc4` /
workspace `46f35fc`; if reality differs, the live tree wins — surface the delta.
(S40 SHIPPED PART 2 — the classify comparator; THIS session is PART 1 only, and
ONLY if the unblock check below clears. See Scope + Open/carry-forward.)

### Step 0.1 — Workspace + repo HEAD
```
git -C ~/crawler-audit rev-parse HEAD
# Expect: 46f35fc (S40 anchor-pin) OR 2cce09a (S40 primary close-out) OR a
# later prompt-drafting / doc-edit commit succeeding it. If N ahead of
# 46f35fc, verify each via `git log --oneline 46f35fc..HEAD`; surface any
# unexpected SHA. NOTE: the operator-side uncommitted edit to
# SESSION_36_PROMPT.md is still unstaged since S36 — tolerate it.

git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD
# Expect: 3266bc4 (S40 WA0.W7.classify-drift-comparator; parent 7bbdc74 = S39
# A-fetch). Tolerated delta: operator-side eval_data labeling commits between
# S40 close and S41 open — verify each commit in 3266bc4..HEAD is strictly
# eval_data/* via `git show --stat <sha>` (NO src/, NO tests/ [incl.
# tests/drift/], NO tools/baseline_v0/, NO .github/, NO docs/). Surface any
# non-eval_data delta.
```

### Step 0.2 — Tags (15 expected; +1 from S39 — S40 placed the part-scoped classify tag)
```
git -C /Users/administrator/projects/barcada-scraper tag -l | sort | wc -l   # Expect 15
git -C /Users/administrator/projects/barcada-scraper rev-list -n 1 workstream-0-end       # Expect a1c5636
git -C /Users/administrator/projects/barcada-scraper rev-list -n 1 adls-live-coverage-v0  # Expect d610f0b
git -C /Users/administrator/projects/barcada-scraper rev-list -n 1 barcada-drift-classify-part2-v0  # Expect 3266bc4
# barcada-drift-classify-part2-v0 is DELIVERABLE-SCOPED (PART 2), NOT
# workstream-closing — the drift workstream stays HALF-SHIPPED until PART 1.
# Place the workstream-closing tag (barcada-drift-classify-v0 / workstream-end)
# only IF this session ships PART 1 and the workstream is then complete. Do NOT
# place workstream-a-week2-end (superseded). Tolerated: operator-side
# stage1-*/eval_data-* tags pointing at eval_data-only commits.
```

### Step 0.3 — Driver locked (S16/S27/S28 exceptions only)
```
cd /Users/administrator/projects/barcada-scraper
git diff dd64963..HEAD -- tests/runners/fixture_cascade/ \
    ':(exclude)tests/runners/fixture_cascade/test_fixture_fetcher.py' \
    ':(exclude)tests/runners/fixture_cascade/cascade.py' \
    ':(exclude)tests/runners/fixture_cascade/test_cost_journal_wiring.py'
# Expect: empty. Any non-empty diff outside those 3 files = HALT. S29-S39 did
# NOT touch this surface.
```

### Step 0.4 — Fixture counts (Python rglob, NOT bare find; UNCHANGED)
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

### Step 0.5 — Canonical 16-path baseline (expect 970; UNCHANGED)
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
# Expect: 970 passed. The drift tests live in tests/drift/ (OUTSIDE this sweep)
# by deliberate disposition — do NOT add tests/drift/ to this 16-path.
# Combined cumulative-gate floor = 1026 (970 + the S38 guard 13 + drift 43).
```

### Step 0.6 — Manifest + schema invariants
```
.venv/bin/python -c "
import json
m = json.load(open('tests/fixtures/baseline-v0/manifest.json'))
assert m['schema_version'] == 'baseline-v0/0.1.0' and m['fixture_count'] == 202
assert m['llm_mode'] == 'real' and m['driver_sha'].startswith('521e363')
s = json.load(open('tests/fixtures/expected.schema.json'))
assert len(s['properties']['stage3_decision']['required']) == 18
print('OK manifest baseline-v0/0.1.0 + expected.schema.json v1.1 (18-col)')
"
```

### Step 0.7 — Sub-surface CLIs (drift ADDED at S39 — now FOUR baseline subcommands)
```
.venv/bin/python -m tools.baseline_v0 --help 2>&1 \
    | grep -oE '\b(generate|check|canary-run|drift)\b' | sort -u | wc -l
# Expect: 4 (NOT 3 — the S39 drift subcommand is registered).
.venv/bin/python -m tools.synthetic_crawl --help 2>&1 \
    | grep -oE '\b(record|replay)\b' | sort -u | wc -l
# Expect: 2
```

### Step 0.8 — Regression sub-suites + the TWO Step 0.8 default-run sub-suites
Run the S33-S38 regression set as in the S39 prompt's Step 0.8, PLUS pin the
two default-run sub-suites that sit OUTSIDE the 16-path:
```
.venv/bin/python -m pytest tests/classifier/llm/test_prompt_logger.py -q   # expect 13 (S38 guard)
.venv/bin/python -m pytest tests/drift/ -q                                 # expect 43 (S39 fetch 22 + S40 classify 21)
.venv/bin/python -m pytest tests/test_parquet_writer.py -q                 # expect 33
.venv/bin/python -m pytest tests/classifier/page_acquisition/test_page_storage.py -q  # expect 13
# Plus the cost-journal / robots / orchestrator sub-suites per the S39 0.8 list.
```

### Step 0.9 — Public-API invariants + S33-S38 ADLS + S39 drift deliverable presence
Run the S39 Step 0.9 invariant checks (a)-(f) (cost_journal / parquet /
page_storage / partitioned / prompt_logger public APIs; cascade AST; K-b smoke
220 LOC; CRAWLING_POLICY 77/2519; the SIX ADLS live tests + the S38 hermetic
guard present), PLUS the S39 drift deliverable:
```
.venv/bin/python -c "from tools.baseline_v0 import drift, drift_classify; \
print('OK drift', bool(drift.run_drift) and len(drift.EXCLUSION_FLAGS)==5); \
print('OK drift_classify (S40 PART 2)', len(drift_classify.PREDICTION_COLUMNS)==6 and bool(drift_classify.compute_classify_report))"
test -f tools/baseline_v0/drift.py && test -f tools/baseline_v0/drift_classify.py \
    && test -f tests/drift/test_drift.py && test -f tests/drift/test_drift_classify.py \
    && echo "OK drift + drift_classify (S39 fetch + S40 classify) files present"
# PART 2 KS dependency (scipy 1.17.1 verified present at S39 — de-risk before Phase 3):
.venv/bin/python -c "from scipy.stats import ks_2samp; print('OK scipy.stats.ks_2samp available')"
# drift._validate_schema must iterate ONLY over PARQUET_COLUMNS (tolerate
# extras) — this is also Step 0.B below, the A-classify compatibility anchor.
```

### Step 0.10 — Same-shape-test sweep (DEFERRED — not in the cold-start halt set; one-time, AFTER Phase 1 scope fixed, BEFORE Phase 3)
NOT part of the cold-start halt set (0.1-0.9). Once the A-classify scope is fixed, grep
the test tree for same-shape tests pinning the contracts the producer/comparator
will touch (esp. the 22 tests/drift/ A-fetch tests + canary's PARQUET_COLUMNS
assertions at tests/baseline_v0/test_canary.py). If found and NOT in an explicit
replacement allowlist, surface at Phase 1/2 — do NOT silently modify.

If any of 0.1-0.9 fail, HALT before doing any work.

---

## Required reading (before Step 0.A — 0.A/0.B/0.C inspect these very files)
- CLASSIFICATION_ADJACENT_PLAN.md Item 8 (all four decisions; metric #1 is
  SCOPE-DEFINING) + cascade/cost refs.
- canary.py (producer to extend) + the Stage 1/2/3 cascade entry module
  (cascade.py / stage1/run.py / stage1/output_schema.py — input AND output).
- A-fetch's shipped comparator + tests/drift/test_drift.py (the scaffold to
  EXTEND, the schema/exit contract to honor, the test LOCATION precedent).
- BARCADA_CRAWLER_REMEDIATION_PLAN.md cost-ceiling + Item-8 surface
  (READ-ONLY); LESSONS.md (baseline-bookkeeping; the test-placement rule —
  a default-run suite stays out of the headline ONLY if it lives outside the
  16 canonical sweep paths; auth-seam; tape-replay; threshold-defaults-are-
  provisional).

---

Then the A-classify-specific source-verify re-confirm steps:

### Step 0.A — Re-pin the frozen 14-col contract via the public tuple
Import canary.PARQUET_COLUMNS; assert len==14 and the names/order match.
The producer change APPENDS to these, never alters them. HALT on any drift.

### Step 0.B — Confirm the A-fetch comparator exists + tolerates extras
Confirm `python -m tools.baseline_v0 drift` is present (A-fetch shipped) and
re-read its schema-validation: it must REQUIRE the 14 and TOLERATE extras
(_validate_schema iterates ONLY over PARQUET_COLUMNS — extras are not
rejected). This is the compatibility A-classify depends on — if A-fetch
instead rejects extras, HALT (the append-only plan is unsafe and Phase 1 must
re-scope).

### Step 0.C — Source-verify the cascade entry seam AND its INPUT + OUTPUT contracts
Read the real Stage 1(->2->3) invocation API and BOTH what it CONSUMES and
what it PRODUCES (do NOT assume — read the call-site signature; the S36
auth-seam lesson generalizes to any reused production surface).
  - INPUT: the cascade takes a parser_parquet + constructed components
    (lr_bundle, embedder, adjudicator), NOT raw HTML — so PART 1 must
    assemble that input (run parser -> build components). Quote the entry
    signature with file:line.
  - OUTPUT: the cascade WRITES per-domain predictions to a separate parquet
    (stage1/run.py:15,169 -> stage1_predictions/.../predictions.parquet) with
    its own output_schema.SCHEMA. The producer READS THIS BACK and selects the
    prediction fields. VERIFIED (0.C, S39 commissioning) — the OUTPUT
    prediction fields are (output_schema.py:103-124): `is_business` (bool
    verdict, null on abstain), `confidence` (float, the unified final score),
    `lr_probability` (float, Tier-2 only), `abstain`/`abstain_reason`,
    `tier_decided`, `model_version`, `feature_schema_version`. CRITICAL:
    `signals_business_score` is the Tier-1 rules INPUT (run.py:21,317), NOT an
    output and NOT a prediction — do NOT target it (that would measure INPUT
    drift). There is NO `category` column (Stage 1 is binary business/non-
    business). `model_version` (git SHA at run time, run.py:31) is the drift-
    attribution signal — see 1.SCHEMA / 1.METRIC. Re-confirm at the live tree.
ALSO determine the $0-dev mechanism (load-bearing; the vcrpy-only-covers-fetch
detail lives in Step 0.D — do not restate it here). There are TWO spend legs,
BOTH on AsyncAzureOpenAI and NEITHER vcrpy-replayable:
  - the EMBEDDER — class `AzureOpenAIEmbedder` is DEFINED in
    classifier/llm/embedder.py:50 (its network client `AsyncAzureOpenAI` at
    embedder.py:42); it is CONSUMED by Stage-1 LR inference via
    classifier/stage1/embedding_generator.py:57 (import) / :101 (param), which
    holds the idempotent (domain, ml_text_hash) cache at
    embedding_generator.py:13,22. (Same leg, two layers — do not read the two
    filenames as two legs.)
  - the ADJUDICATOR (Stage 3) — client `AsyncAzureOpenAI` in
    classifier/llm/azure_openai_adjudicator.py:55.
Even the cheapest Stage-1 depth spends on the embedder (cache-miss). A $0-dev
mock plan MUST cover BOTH legs — mock the client in embedder.py:50 + the
adjudicator, OR inject fakes at the embedding_generator / cascade entry ABOVE
both. Verify these file:lines at source before placing the seam (live tree wins). Confirm EITHER (i) a warm cache for the dev
subset on the relevant leg(s) — the embedder has an idempotent
(domain, ml_text_hash) cache (embedding_generator.py:13,22), so warm-cache $0 is
viable for EMBEDDINGS at Stage-1 depth; the adjudicator cache must be verified
separately and warm-cache viability is therefore depth-dependent — OR (ii) a
clean mock seam covering BOTH legs (the test_canary.py-mocks-requests.get
pattern). If NEITHER a warm cache NOR a both-legs mock plan exists -> HALT (no $0
dev path; the session would burn live spend just to develop).

RUN 0.C AS A STANDALONE PRE-FLIGHT before commissioning A-classify (mirroring
the S39 pre-session canary-run source-verify), so a no-$0-path HALT surfaces
BEFORE the session opens, not mid-Phase-0.

### Step 0.D — Dev replay reality (vcrpy covers the FETCH leg ONLY)
vcrpy patches `requests`, so it replays the canary FETCH leg only. It does
NOT intercept the LLM/embedding legs — those run on AsyncAzureOpenAI/httpx
(azure_openai_adjudicator.py:55, embedder.py:42). So tapes alone do NOT make
a classify run free. The robust $0 dev path is MOCKING the cascade entry /
AsyncAzureOpenAI client in hermetic tests (the test_canary.py-mocks-
requests.get pattern), optionally combined with vcrpy for the fetch leg; the
LLM cache is a SECONDARY lever, valid only if Step 0.C proved it warm for the
dev subset. Do NOT rely on "wrap the run in vcr.use_cassette" for the LLM
legs — it will not replay them.

## Phase 0.COST — Spend gate (guardrail; standing tolerance pre-set)
Grounded estimate: a full 50-domain run is cheap — embeddings are cents
(cached), Stage-3 adjudication fires only on the rules-uncertain band (a
subset) at ~$0.01-0.02/domain, so full-depth is well under $1/run and
Stage-1-only is a few cents. Operator standing tolerance: **< $5/run is
pre-authorized** with a per-run confirm; a run estimated above $5 needs fresh
authorization; the **$100 cumulative ceiling** is the hard guard.

This session is $0 for CC: CC has NO Azure credentials, so CC builds + tests
entirely with client-mock + synthetic ($0). Any live execution is
OPERATOR-RUN on the laptop:
- Stage 1 (informational): present the full-depth ceiling vs headroom at
  Phase 0.
- Stage 2 (refined): AFTER Phase 2 depth is chosen, compute the refined
  per-run estimate and confirm it BEFORE the operator runs (i) the optional
  Phase-3 producer live SMOKE and (ii) any future operational run. Both are
  operator-executed; CC never runs a live cascade.

## Phase 1 — Scope resolution (no code)

### 1.SCHEMA — keep fetch-only cheap; predictions opt-in; PREDICTION_COLUMNS frozen
Decide: predictions appended ONLY under a `--classify` flag, via a SEPARATE
constant PREDICTION_COLUMNS appended after the 14 — NOT by extending
PARQUET_COLUMNS itself. Recommended, because extending PARQUET_COLUMNS would
force every canary run to emit predictions (mandatory LLM cost) AND would
make A-fetch's "require all 14" demand the prediction columns on every
parquet — breaking fetch-only runs. Keep the 14 frozen; predictions are an
additive, opt-in set.
DEFINE PREDICTION_COLUMNS as a frozen public tuple + dtype map (mirroring
canary.PARQUET_COLUMNS / canary._make_dtypes), a curated SUBSET of the
cascade's real output_schema.SCHEMA (output_schema.py:103-124, verified at
0.C): `is_business`, `confidence`, `lr_probability`, `abstain`, `tier_decided`,
`model_version`. (NOT signals_business_score — that is the Tier-1 rules INPUT,
not an output; NOT category — no such column.) Exported and asserted in tests,
so the classify comparator IMPORTS it as the source of truth exactly as A-fetch
imports PARQUET_COLUMNS. This makes "append-only" mechanically checkable and
prevents re-hardcoding. Include `model_version` deliberately (see 1.METRIC).
The set is FIXED (no depth-conditionality — there is no depth knob; see
1.CASCADE-NOTE).

### 1.NAMESPACE — extend the existing `drift` subcommand
A-fetch's `drift` subcommand exists. Decide how classify metrics attach:
(a) the same `drift` subcommand auto-detects prediction columns and adds the
classify metrics when present (RECOMMENDED — one cohesive surface, reuses the
join/exit scaffold, fetch metrics still run); (b) a sibling `drift --mode
classify`; (c) a separate subcommand. Reconcile with where A-fetch landed;
do NOT create a parallel comparator. NOTE option (a) BRANCHES the shipped
comparator — the existing tests/drift/ A-fetch suite MUST stay green
(fetch-only behavior byte-identical); guard it as a named acceptance row.

### 1.METRIC — report-only signals, gate direction, overlap + calibration posture
- **model_version (attribution; report-only).** predictions.parquet rows carry
  `model_version` (git SHA at run time, run.py:31). A prediction-drift alert's
  MOST LIKELY cause is a model/SHA change. The comparator MUST capture it per
  snapshot and surface a "baseline vs current model_version" line, so drift is
  attributable to "the model changed" vs "the world changed."
- **tier-mix shift (report-only).** `tier_decided` (output_schema.py:105) routes
  each domain to rules / lr / llm / abstained. Compute the run-over-run
  distribution (rules% / LR% / LLM% / abstained%) and report the deltas. Routing
  drift IS behavior drift AND an early cost signal — verdict + confidence can
  stay flat while routing shifts. Report-only floor (NOT gating); this is what
  consumes `tier_decided` (otherwise a carried-for-nothing column).
- **abstain gate direction = TWO-SIDED `|Δ|` > threshold.** Drift = behavior
  change in EITHER direction: an abstain DROP (model spuriously more decisive)
  is as much a behavior change as a rise. Gate on
  `|abstain_rate(current) - abstain_rate(baseline)|`, not a one-directional
  rise — keeping the gating set direction-agnostic, consistent with
  is_business-agreement (flip count) and confidence-KS (distribution distance).
- **OVERLAP (acknowledged, acceptable).** is_business-agreement and abstain-rate
  shift partially overlap — an abstain<->verdict change trips BOTH. Correlated,
  not orthogonal; redundant detection is acceptable and expected.
- **CALIBRATION posture.** All thresholds are PROVISIONAL + uncalibrated. The
  ~5-domain operator-run smoke does NOT calibrate them (too small — it only
  truth-checks the producer's output schema). Calibration is the FIRST real
  two-snapshot operational run (out of this session). Until then, alerts mean
  "look," not "act."

### 1.CASCADE-NOTE — there is NO operator depth knob (architecture fact)
`run_shard` (run.py:150) auto-routes EACH domain through Tiers 1-3 by
confidence (Tier 1 rules -> Tier 2 LR -> Tier 3 LLM adjudication, run.py:21-29)
and ALWAYS emits the same output_schema. There is no "Stage 1 / 1->2 / full"
operator choice and no category output. So depth is NOT a Phase-2 question.
Cost is whatever the full per-domain cascade costs (embeddings on cache-miss +
LLM adjudication only on the LR-uncertain band) — well under $1/run, a
non-constraint vs the < $5/run tolerance. The producer always constructs the
full component set (lr_bundle, embedder, adjudicator, thresholds, cost_tracker)
and calls the single async `run_shard` entry. NOTE the producer is sync
(canary_run is a requests loop) and run_shard is async — PART 1 needs an
asyncio bridge (asyncio.run) plus the component construction (the cli.py
`_run_stage1` wiring at cli.py:606-717 is the template); this shapes both the
producer and the PART 1 spike.

### 1.BASELINE — tests go in tests/drift/ (the rule that just bit at A-fetch)
New hermetic tests MUST live OUTSIDE the 16 canonical paths or they silently
fold into the 970 headline (A-fetch's test_drift.py was moved out of
tests/baseline_v0/ for exactly this). Place A-classify tests in tests/drift/
(extending the existing dir) and track as the Step 0.8 sub-suite's new
expect-N. Canonical stays 970; combined grows. Record all three numbers.

### 1.TAG — identity from first principles (S38 lesson)
e.g. `barcada-drift-classify-v0`, NOT a workstream letter. With A-classify,
the drift workstream (fetch + classify) may now be declarable closed — decide
whether this is the tag that closes it, or defer with a stated bar.

### Q-SHARED.1 — commit shape
TWO commits (producer extension; then comparator-classify-metrics), isolable
for bisectability — the producer change touches the shared canary.py the
A-fetch comparator depends on, so it must commit separately.

## Phase 2 — Design-gate elicitation (AskUserQuestion; 4 options/Q max)
(NO operator "cascade depth" choice exists — run_shard auto-routes each domain
through Tiers 1-3 [rules / LR / LLM adjudication, run.py:21-29] and always emits
the SAME output_schema; the old depth question is REMOVED. No category column is
produced — output_schema.py:97-127 — so per-category drift is OUT.)
1. **Label-free metric set (Item 8 #1) — on the REAL prediction OUTPUTS**
   (output_schema.py:103-124; verified at 0.C): (a) `is_business` AGREEMENT —
   run-N vs run-N-1 per common domain, fraction whose verdict flips (count an
   abstain<->verdict change as a flip; is_business is null on abstain, line
   103); (b) KS on the `confidence` distribution (confidence is the unified
   final-verdict score, line 104; via scipy.stats.ks_2samp, no new dep) — with
   an OPTIONAL secondary KS on `lr_probability` (line 110) over the LR-tier
   subset (report-only — sparse); (c) `abstain`-rate shift (line 106), gated
   TWO-SIDED as `|Δ|` (see 1.METRIC); (d) tier-mix shift — the run-over-run
   rules%/LR%/LLM%/abstained% distribution from `tier_decided` (line 105),
   REPORT-ONLY (routing/cost drift; see 1.METRIC). NOTE: `signals_business_score`
   is the Tier-1 rules INPUT (run.py:21,317), NOT a prediction and absent from
   the output — it is OUT (using it would measure INPUT drift, A-fetch's
   domain). per-category is OUT (no such column). Calibration/Brier DEFERRED
   (label-gated). `model_version` delta reported for attribution (1.METRIC),
   not gated.
2. **GATING (DECIDED — S39 operator).** GATE (exit 1) on: is_business-agreement
   drop + abstain-rate `|Δ|` (two-sided) + confidence-KS over threshold.
   REPORT-ONLY: lr_probability-KS (sparse), tier-mix shift, model_version delta.
3. **Thresholds + exit (Item 8 #2/#4), reconciled with A-fetch.** Same 0/1/2
   contract; same inner-join domain alignment + appeared/disappeared. Per-metric
   thresholds CLI-configurable; PROVISIONAL defaults (DECIDED — S39 operator):
   - verdict-flip rate > 0.05  (--max-verdict-flip-rate)
   - abstain-rate |Δ| > 0.05   (--max-abstain-rate-delta)
   - confidence-KS > 0.25      (--max-confidence-ks)
   N-DEPENDENCE WARNING on confidence-KS: the two-sample KS critical value at
   alpha=0.05 is ~1.36*sqrt((n+m)/(n*m)) ≈ 0.27 for n=m=50, so a KS threshold
   below ~0.27 FIRES ON SAMPLING NOISE at dev/smoke scale (n≈50). 0.25 is a
   provisional floor that is only meaningful at large production N; the
   threshold is N-sensitive and stays uncalibrated until a real two-snapshot run
   (the A-fetch --max-regressions lesson: don't imply calibration).
4. **Producer real-validation smoke scope (operator-run; PART 1 only).**
   Dev/test data is DETERMINED, not a choice: the comparator is tested on
   SYNTHETIC prediction parquets (controllability — you need known drift to
   assert detection), and the producer's hermetic test mocks BOTH cascade legs
   ($0, credless CI). The genuine choice is the size of the OPERATOR-RUN live
   smoke that truth-checks the producer against the REAL cascade output:
   ~5-domain subset (cheapest, fastest, RECOMMENDED) / all 50 (a full real
   prediction parquet, still < $1) / skip the smoke (mock-only — accept the
   unvalidated real-output-schema risk). Live capture is NOT a dev-data source
   for the test suite and is NOT CC-executed (CC has no creds). [S39: operator
   chose the operator-run smoke + laptop cadence.]
Operator confirms before code.

## Phase 3 — Implementation (strict order; verify before every commit)

### Build-time spike FIRST
PART 1 spike: run the `--classify` producer over a SMALL subset with the
cascade/LLM client MOCKED (no live spend; vcrpy may replay the fetch leg);
dump the resulting parquet columns; PROVE they equal
PARQUET_COLUMNS (14, unchanged, in order) + PREDICTION_COLUMNS appended. HALT
if any of the 14 changed. THEN run A-fetch's comparator against that
prediction parquet and confirm it still exits 0/1 on fetch metrics (tolerate-
extras holds in practice, not just in the source). PART 2 spike: classify
metric computes the expected number on a known-drift synthetic prediction
parquet; threshold flips the exit code.

### Ordered build
1. PART 1 producer extension: `--classify` flag; per domain fetch -> parser
   builds parser_parquet -> construct components -> asyncio.run the cascade ->
   read back predictions.parquet -> append PREDICTION_COLUMNS via an assembled
   (14 + predictions) schema (NOT the hardcoded PARQUET_COLUMNS dtype dict at
   canary.py:193). Fetch-only path (no flag) byte-for-byte unchanged.
2. PART 1 tests (hermetic, client-mock-backed [BOTH legs] — vcrpy optional for
   the fetch leg only; tests/drift/): assert schema is append-only (14 untouched
   + PREDICTION_COLUMNS present); assert the A-fetch comparator still validates
   a prediction parquet.
2b. PART 1 live SMOKE (OPERATOR-EXECUTED on the laptop; cost-gated per
   Phase-0.COST stage-2; scope per Q4, default ~5 domains; skip if Q4=skip).
   CC cannot run it (no creds): CC stages the exact command + the refined
   Phase-0.COST stage-2 per-run estimate; the OPERATOR CONFIRMS the estimate
   BEFORE running (explicit gate — do not run on the standing <$5 tolerance
   alone), THEN runs `--classify` over the subset and pastes back the produced
   parquet's column
   list, and CC pins PREDICTION_COLUMNS to the OBSERVED real schema + confirms
   append-only against reality (the 14 unchanged + predictions). This is the
   "build it real" truth-check; the hermetic mock test (step 2) stays for CI.
   Record the smoke's actual spend in the Phase-3 verification table.
3. PART 2 classify metrics on the `drift` subcommand (per 1.NAMESPACE);
   hermetic tests in tests/drift/ against synthetic prediction parquets.
   **Teeth — STRONGER than A-fetch (whose metrics all gated; here the
   report-only/gating SPLIT must itself be tested).** (a) two IDENTICAL
   prediction snapshots -> no drift -> exit 0; (b) injected drift in EACH
   GATING metric -> exit 1, asserted per-metric: a verdict flip past
   --max-verdict-flip-rate; an abstain |Δ| past --max-abstain-rate-delta
   (test BOTH directions — a rise AND a drop must each fire, per the two-sided
   gate); a confidence-distribution shift past --max-confidence-ks; (c) the
   **negative control** — a stub comparator that always returns "no drift" MUST
   FAIL assertion (b). (d) REPORT-ONLY/GATING SPLIT (the new requirement): inject
   a change in EACH report-only signal — tier-mix (rules%/LR%/LLM%/abstained%
   redistribution), lr_probability-KS, model_version — with all gating metrics
   held flat, and assert exit STAYS 0 while the report still SHOWS the moved
   value. Do NOT inherit A-fetch's teeth verbatim; this split case is mandatory.
   Also assert the model_version baseline-vs-current line appears in the report.

### Per-commit checkpoint protocol (IN ORDER, every boundary)
1. **Combined canonical suite** vs Phase-0 baseline; headline disposition per
   1.BASELINE (canonical stays 970; tests/drift/ expect-N grows). No silent
   drift.
2. **Ruff** check + format on touched files (one format pass on new files).
3. **Verification table — VERIFY BEFORE COMMITTING (operator requirement).**
   Rows backed by CAPTURED output only: file(s)+LOC (wc -l); test counts
   (-q/collect, verified not projected — the S37 13/16 lesson); **schema
   append-only PROOF** (produced parquet columns == PARQUET_COLUMNS [14,
   order-identical] + PREDICTION_COLUMNS, echoed from the parquet, not the
   code diff); **A-fetch-still-passes PROOF** (A-fetch comparator run against
   a prediction parquet, exit captured); classify-metric correctness on the
   spike fixture; BOTH teeth directions + negative control (paste the
   assertion error); exit contract 0/1/2 demonstrated; domain-join (mismatch
   fixture -> intersection-only, appeared/disappeared listed); **spend this
   commit** ($0 client-mock, or the authorized live figure); canonical
   headline vs baseline; ruff clean. Each row: Claim | Reality | Status.
   Unevidenced row = HALT.
4. **git status** — stage ONLY intended files (A). eval_data/* WIP + .claude
   lock UNSTAGED.
5. **Confirm to commit?** — gate. `-F /tmp/<id>-msg.txt`; NO -m; NO backticks
   in body; NO Co-Authored-By.
6. Post-commit: re-run step 1; confirm clean tree.

### Commit shape
TWO commits per Q-SHARED.1: producer extension first (the shared-canary
change), then the comparator classify metrics.

## Phase 4 — Pre-push gate (whole-tree)
Whole-tree ruff + canonical suite + vermin + consistency validator + a final
confirmation that NO live spend occurred beyond the Phase-0.COST
authorization. eval_data WIP halt protocol applies.

## Phase 5 — Push + tag
Push after operator confirms. Tag per 1.TAG (e.g. barcada-drift-classify-v0,
or the drift-workstream-closing tag if declared) at the post-comparator SHA,
or rationale-backed defer. Workspace commits land local-first.

## Phase 6 — Workspace close-out
SESSION_LOG entry with the unambiguous baseline split (canonical 970 /
tests/drift/ expect-N / combined) AND a RECORDED SPEND LINE. Prior cumulative
spend = $0 (every session through S39 recorded $0; A-classify is the FIRST
non-$0 candidate), so the session spend (CC dev $0 + any operator-run smoke
figure) IS the new running total — record it vs the $100 ceiling. Spend
tracking is load-bearing from here on. Fold LESSONS with causal framing: opt-in
prediction columns keep fetch-only runs cheap + A-fetch-compatible;
append-only discipline when a shipped comparator tolerates-but-depends-on the
frozen columns; vcrpy covers the fetch leg only (mock the LLM client for $0
dev); model_version is the primary prediction-drift attribution; cost-gate-
before-live-run. Refill transition template; anchor-pin.

## Acceptance criteria
- `--classify` producer emits PREDICTION_COLUMNS append-only over the 14
  frozen fetch columns (PROVEN from the parquet, not asserted); fetch-only
  path unchanged.
- A-fetch comparator still validates + correctly exits on a prediction
  parquet (PROVEN by running it).
- The existing tests/drift/ A-fetch suite (expect-N from S39) stays GREEN —
  fetch-only behavior byte-identical (named row; 1.NAMESPACE option (a)
  branches the shipped comparator, so guard it explicitly).
- Classify drift metric(s) computed on the `drift` surface with the 0/1/2
  contract + inner-join alignment; thresholds configurable + flagged
  provisional. model_version baseline-vs-current surfaced in the report.
- Hermetic client-mock-backed tests pass; BOTH teeth + negative control
  demonstrated; calibration metric correctly ABSENT (label-gated).
- Spend within Phase-0.COST authorization; close-out records the figure.
- Tests live in tests/drift/ (outside the 16-path); canonical stays 970.
- Every commit-message claim backed by captured verification-table output.

## Verify-before-committing discipline (operator requirement — load-bearing)
Same bidirectional rule as A-fetch, with three classify-specific teeth:
(1) append-only schema PROVEN by dumping the produced parquet's columns vs
PARQUET_COLUMNS + PREDICTION_COLUMNS — never from the code diff; (2) A-fetch
compatibility PROVEN by running its comparator on a prediction parquet; (3)
spend PROVEN by the actual run mode (client-mock=$0 or the authorized figure),
never assumed. RE-verify the cascade entry seam + its input/output contracts
(0.C) and A-fetch's tolerate-extras (0.B) against the live tree before relying
on them — if a prompt file:line is stale, the live tree wins. (Hard-won at S39
commissioning: the prediction OUTPUTS are is_business / confidence /
lr_probability / abstain [output_schema.py:103-124]; `signals_business_score`
is the Tier-1 rules INPUT [run.py:21,317], NOT a prediction — verifying the
field NAME is not enough, verify it is an OUTPUT.)

## Regression-protection / locked artifacts (do NOT break working code)

Full locked-artifact list: SESSION_TRANSITION_TEMPLATE.md "Locked artifact
reminders". The A-classify-CRITICAL locks (any breach = HALT):

- **The 14-col `canary.PARQUET_COLUMNS` is FROZEN — append-only.** The producer
  adds `PREDICTION_COLUMNS` AFTER the 14; it never alters the 14, their order,
  or their dtypes. Step 0.A re-pins this.
- **The fetch-only producer path (no `--classify`) must be BYTE-FOR-BYTE
  unchanged** — every existing canary-run consumer (and the A-fetch comparator's
  "require all 14") keeps working. PROVE the no-flag parquet is identical.
- **The shipped comparator is EXTENDED, not forked.** `tools/baseline_v0/
  drift.py` (S39 `7bbdc74`) + `drift_classify.py` (S40 PART 2 `3266bc4`) + the
  **43** `tests/drift/` tests (22 fetch `test_drift.py` + 21 classify
  `test_drift_classify.py`) must stay GREEN. Do NOT regress the
  require-14/tolerate-extras / inner-join / 0-1-2 contract, the fetch-only
  byte-identical behavior (classify is None when prediction columns absent), OR
  the PART-2 classify metrics + report-only/gating split.
- **The src/ classifier cascade is INVOKED, not MODIFIED.** No `src/` change
  this session. canary.py is TOOLING (editable under the Phase-2 gate); the
  cascade entry, `output_schema.SCHEMA`, embedder/adjudicator are read + called.
- **No change to:** the W4.1.5 driver (`tests/runners/fixture_cascade/`), the
  baseline-v0 snapshot (`9e9a1fb`), the schemas (`expected.schema.json` v1.1
  etc.), the 30 cassettes, the SIX ADLS live tests, the S38 hermetic guard, the
  CI workflow, or the `adls-live-coverage-v0` tag.
- **Canonical 16-path stays 970** (Step 0.5); the cumulative gate (combined
  **1026** + N new tests/drift/ tests) never decreases. New tests live in
  `tests/drift/` (outside the sweep) — re-run the 16-path ALONE post-placement
  to confirm 970 (the S39 directory-fact LESSON).
- **No live LLM spend** beyond an explicit Phase-0.COST authorization; default
  dev = client-mock ($0).

Per-commit checkpoint step 1 (combined canonical suite vs the Phase-0 baseline)
+ step 6 (re-run post-commit) enforce this every boundary. Any unexplained
count change or any of the above breaches = HALT, not a commit.

## Open / carry-forward
- PREREQUISITE — SATISFIED (and S40 SHIPPED PART 2). S39 + S40 Phase 6
  close-outs landed + pushed; the CURRENT anchors are repo `3266bc4` / workspace
  `46f35fc`, tag count 15, canonical 970 / combined **1026** / drift sub-suite
  **43**. PART 2 (the classify comparator) is DONE; THIS session is PART 1 only.
  Phase 0 above is fully enumerated at these S41 anchors — no dependency on
  reconstructing "standard 0.1-0.10". **ORDER: run the PART 1 UNBLOCK CHECK
  (next bullet, (a)) BEFORE any Phase 1 design work — if the worker_loop.py:193
  partition does not exist, PART 1 STAYS DEFERRED and this is a no-ship
  scope-resolution session (a legitimate outcome, like S39's empty-queue).**
- **PART 1 (the `--classify` producer) is DEFERRED — carry-forward (the
  classify comparator PART 2 shipped at repo `3266bc4`).** Source-verify at
  commissioning showed the cascade READS a pre-existing parser_parquet that the
  scraper stage has not produced yet. To commission PART 1 later:
  - **(a) UNBLOCK CHECK.** PART 1 unblocks only when the scraper stage produces
    a real parser_parquet partition at the worker_loop path
    (worker_loop.py:193 → `.../parser/crawl_date=X/shard=NNNNN/has_website=*/
    bot_blocked=*/data-<uuid>.parquet`). Verify that path EXISTS (and is
    populated) before commissioning PART 1; until then PART 1 stays deferred.
  - **(b) COST GATE APPLIES TO PART 1, not PART 2.** PART 2 shipped at $0
    (hermetic, no cascade). The entire Phase-0.COST machinery (full-depth
    ceiling, the < $5/run standing tolerance + per-run confirm, the stage-2
    refined re-gate before any live run) governs PART 1's producer runs — the
    first spend happens only when PART 1 runs the cascade. Re-read Phase-0.COST
    as a PART 1 gate.
  - **(c) PREDICTION_COLUMNS REAL-ARTIFACT RE-VERIFICATION — STANDING DEFERRED
    ACCEPTANCE GATE (E18; remediation-recorded, NOT yet met).** PART 1 was
    re-scoped to shape **B** and shipped as a CLASSIFY-NATIVE INPUT MODE (the
    comparator accepts a standalone predictions parquet: `domain` + the 6
    PREDICTION_COLUMNS, no fetch columns). `PREDICTION_COLUMNS` =
    (is_business, confidence, lr_probability, abstain, tier_decided,
    model_version) is pinned against the SOURCE SCHEMA
    `stage1/output_schema.py:103-124` — the authoritative definition, NOT stage3
    and NOT the 15-col May-09 **dev** sample. It has NOT been verified against a
    REAL PRODUCED partition because none exists yet (the producer is deferred).
    **GATE — before PART 1 is declared COMPLETE:** when a real Stage-1 partition
    exists (16-col post-PR-COST, real 12-char SHA `model_version`), DUMP its
    actual columns and confirm the 6 `PREDICTION_COLUMNS` + their dtypes match;
    if the cascade output schema has drifted, update
    `drift_classify.PREDICTION_COLUMNS` + its dtype map (and the comparator /
    tests) FIRST. Until then the classify-native mode ships against the
    schema-of-record, with this real-artifact confirmation explicitly OUTSTANDING.
  - **(d) RE-SCOPE FLAG.** If, at PART 1 commissioning, the producer's real path
    (scraper-stage-on-demand: HTML → parser_parquet) is still a large/unwired
    surface, RE-SCOPE rather than force an inline scraper integration. Cleaner
    options: have the producer CONSUME an existing parser_parquet partition
    (lightest; matches the decoupled scrape/classify architecture), or wait for
    a single-domain scraper entry. Decide at PART 1 Phase 1.
- Calibration/Brier drift stays GATED on Stage 2/3 labeling (PR-D/E) —
  revisit only after labels exist.
- Operational cadence = LAPTOP launchd, ~monthly, < $5/run (operator-confirmed,
  S39 discussion). The COMPARATOR (PART 2) is BUILT this session; the PRODUCER
  (PART 1) is deferred (see above). Enabling the scheduled laptop run is a
  post-ship DEPLOYMENT step via the existing scripts/launchd/ kit — NOT built
  here, and gated on PART 1 shipping first. Compute is local; the embedding +
  adjudication calls still go to Azure OpenAI (no fully-local option). Azure
  (VMSS) is overkill for 50 domains and is not the chosen target.
- Item 8 #3 (canary curation) is an AI-ML-team decision independent of this
  build.
- If A-classify closes the drift workstream (fetch + classify both shipped),
  decide the closing tag deliberately at 1.TAG rather than defer-by-reflex.
