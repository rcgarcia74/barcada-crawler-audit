# Session prompt — Candidate A-classify (barcada drift, classifier-prediction)

## WHAT THIS IS
#   Candidate A, CLASSIFY fork — the Item-8-as-written drift surface. Detects
#   drift in CLASSIFIER BEHAVIOR (predictions changing run-over-run), which
#   the fetch-health canary CANNOT surface. TWO-PART, SPENDY candidate; must
#   NOT be commissioned without the explicit Phase-0.COST gate clearing.

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
#   canary.PARQUET_COLUMNS (@ canary.py:66-81) — no signals_business_score,
#   category, or prediction column. So classifier-prediction drift is NOT
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
#     - prediction-AGREEMENT (run-N vs run-N-1) and KS on the
#       signals_business_score distribution are LABEL-FREE and IN scope.
#     - Brier / calibration drift needs predicted-probability + a TRUE LABEL,
#       so it is GATED on Stage 2/3 labeling (PR-D/E) and is OUT of scope.
#       Do NOT build a calibration metric this session.
#
# CHAT-SIDE ROLE: advisory/review-only. CC implements under phase governance
# and VERIFIES every claim against captured output BEFORE committing.

## Scope (two sequenced sub-surfaces)

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
— prediction agreement and/or KS on signals_business_score — over two
prediction-bearing parquets, REUSING A-fetch's comparator scaffold (the
inner-join, appeared/disappeared, exit-0/1/2 contract, --report shape). It
extends, not forks. KS is computable via scipy.stats.ks_2samp (scipy 1.17.1
is already a dependency — NO new dependency required; do not hand-roll KS).

OUT of scope: calibration/Brier (label-gated); live alert wiring + dashboard
(joint/prod); launchd kit install (production); ANY change to the 14
fetch columns or their order; making predictions mandatory (the flag keeps
fetch-only runs cheap).

## Phase 0 — Cold-start + source-verify re-confirm (halt-on-mismatch)

Fill generic anchors from SESSION_TRANSITION_TEMPLATE.md at invocation (NOT
guessed). Run standard 0.1-0.10, PLUS:

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
    prediction fields. Quote the OUTPUT schema field names with file:line and
    confirm the actual prediction-field name (it is `signals_business_score`
    @ run.py:317 / __init__.py:13 — NOT `business_score`; verify against the
    live tree). Note the rows also carry `model_version` (git SHA at run time,
    run.py:31) — see 1.SCHEMA / 1.METRIC for why it matters.
ALSO determine the $0-dev mechanism (this is load-bearing — see Step 0.D):
the classifier uses AsyncAzureOpenAI (openai/httpx), NOT requests, so vcrpy
does NOT replay the LLM legs. Confirm EITHER (i) an LLM RESPONSE CACHE exists
on the cascade path AND is warm for the dev subset (quote file:line), OR
(ii) a clean mock seam for the cascade entry / AsyncAzureOpenAI client
exists (mirroring how test_canary.py mocks requests.get). If NEITHER a warm
cache NOR a client-mock plan exists -> HALT (there is no $0 dev path and the
session would burn live spend just to develop).

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

## Required reading (early — before Phase 0.COST)
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

## Phase 0.COST — Spend gate (BLOCKING; two-stage, before any live run)
Cascade depth is a Phase-1/2 decision, so Phase 0 can only bound the UPPER
limit: compute the FULL-DEPTH ceiling = 50 domains x full 1->2->3 token cost
x intended cadence; present it + remaining headroom vs the $100 ceiling. Then
AFTER Phase 2 (depth chosen), compute a REFINED estimate at the chosen depth
and re-gate immediately BEFORE the first authorized live run. Default dev
path = client-MOCK ($0, per Step 0.D), NOT tapes-for-LLM; live runs are a
SEPARATE, explicitly-authorized step. Do NOT execute a single live cascade
run until the operator confirms the refined estimate.

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
cascade's output_schema.SCHEMA — e.g. signals_business_score, is_business,
category (only if depth >= Stage 2), model_version — exported and asserted in
tests, so the classify comparator IMPORTS it as the source of truth exactly
as A-fetch imports PARQUET_COLUMNS. This makes "append-only" mechanically
checkable and prevents re-hardcoding. Include `model_version` deliberately
(see 1.METRIC).

### 1.NAMESPACE — extend the existing `drift` subcommand
A-fetch's `drift` subcommand exists. Decide how classify metrics attach:
(a) the same `drift` subcommand auto-detects prediction columns and adds the
classify metrics when present (RECOMMENDED — one cohesive surface, reuses the
join/exit scaffold, fetch metrics still run); (b) a sibling `drift --mode
classify`; (c) a separate subcommand. Reconcile with where A-fetch landed;
do NOT create a parallel comparator. NOTE option (a) BRANCHES the shipped
comparator — the existing tests/drift/ A-fetch suite MUST stay green
(fetch-only behavior byte-identical); guard it as a named acceptance row.

### 1.METRIC — model_version is the primary drift-attribution signal
predictions.parquet rows carry `model_version` (git SHA at run time,
run.py:31). A prediction-drift alert's MOST LIKELY cause is a model/SHA
change, not genuine input drift. The classify comparator MUST capture
model_version per snapshot and surface a "baseline vs current model_version"
line in the report, so a drift alert is immediately attributable to "the
model changed" vs "the world changed." Without it, prediction drift is
uninterpretable. This is informational context on the report, not itself a
gating metric.

### 1.CASCADE-DEPTH — cost vs metric richness (the genuine tension)
Stage 1 only (cheapest; signals_business_score + KS feasible) vs Stage 1->2
(adds category -> per-category rate metric) vs full 1->2->3 (most expensive).
Deeper = richer drift signal AND higher recurring spend AND more components
to construct. Operator trade, not a silent default. NOTE the producer is
sync (canary_run is a requests loop) and the cascade is async — PART 1 needs
an asyncio bridge (asyncio.run) plus the component-construction setup
(lr_bundle, embedder, adjudicator) the chosen depth requires; this shapes
both the producer and the PART 1 spike.

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
1. **Cascade depth** (Stage 1 / 1->2 / full) — sets cost + computable metrics.
2. **Label-free metric set (Item 8 #1)** — prediction agreement (run-over-run
   per-domain), KS on signals_business_score distribution (via
   scipy.stats.ks_2samp; no new dep), per-category rate shift (only if depth
   >= Stage 2). Calibration/Brier explicitly DEFERRED. model_version delta is
   reported for attribution (1.METRIC), not gated.
3. **Thresholds + exit (Item 8 #2/#4), reconciled with A-fetch.** Same 0/1/2
   contract; same inner-join domain alignment + appeared/disappeared. Per-
   metric thresholds CLI-configurable; defaults flagged PROVISIONAL —
   uncalibrated until real prediction snapshots exist (the A-fetch
   --max-regressions lesson: don't imply calibration).
4. **Dev data source** — client-MOCK ($0 dev, RECOMMENDED — mocks the cascade
   entry / AsyncAzureOpenAI client per Step 0.D, optionally vcrpy for the
   fetch leg) vs warm-cache replay (only if Step 0.C proved the cache warm for
   the dev subset) vs one authorized live capture to seed real prediction
   parquets (Phase-0.COST-gated). Tapes alone do NOT cover the LLM legs.
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
2. PART 1 tests (hermetic, client-mock-backed — vcrpy optional for the fetch
   leg only; tests/drift/): assert schema is append-only (14 untouched +
   PREDICTION_COLUMNS present); assert the A-fetch comparator still validates
   a prediction parquet.
3. PART 2 classify metrics on the `drift` subcommand (per 1.NAMESPACE);
   hermetic tests in tests/drift/ against synthetic prediction parquets.
   **Teeth (bidirectional, mirroring A-fetch):** (a) two IDENTICAL
   prediction snapshots -> no drift -> exit 0; (b) injected prediction drift
   -> detected -> exit 1; plus the **negative control** — a stub comparator
   that always returns "no drift" MUST FAIL assertion (b). Reverse teeth: a
   change in a NON-gating column must NOT flip the exit. Also assert the
   model_version line appears in the report.

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
tests/drift/ expect-N / combined) AND a RECORDED SPEND LINE (dev $0 vs any
authorized live figure; running total vs $100 — first non-$0 candidate, so
spend tracking is load-bearing). Fold LESSONS with causal framing: opt-in
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
on them — if a prompt file:line is stale, the live tree wins (the prediction
field is `signals_business_score`, not `business_score` — confirm at source).

## Open / carry-forward
- PREREQUISITE (blocking cold-start): S39 Phase 6 close-out must land FIRST —
  it refills SESSION_TRANSITION_TEMPLATE.md, pins the post-A-fetch repo SHA
  (7bbdc74), and records the drift baseline (canonical 970 / tests/drift/
  expect-22 / combined 1005). A-classify Phase 0 cannot cold-start cleanly
  until that exists. Do NOT commission A-classify until S39 is closed.
- Calibration/Brier drift stays GATED on Stage 2/3 labeling (PR-D/E) —
  revisit only after labels exist.
- Live recurring runs + the launchd kit are a PRODUCTION step, after the
  daemon ships and after deployment — not this dev session.
- Item 8 #3 (canary curation) is an AI-ML-team decision independent of this
  build.
- If A-classify closes the drift workstream (fetch + classify both shipped),
  decide the closing tag deliberately at 1.TAG rather than defer-by-reflex.
