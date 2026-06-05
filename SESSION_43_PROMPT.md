# Session 43 prompt — candidate (a): drift operational cadence (untuned-baseline capture)

**Operator-commissioned at S43 (2026-06-05).** Scope (a) CHOSEN from the S43
menu. Mirrors the S20/.../S42 prompt structure (7-phase, strict order,
halt-on-mismatch). Re-read on session open.

This prompt lives at `~/crawler-audit/SESSION_43_PROMPT.md`.

---

## WHAT THIS IS

A-classify drift CODE is COMPLETE (`barcada-drift-classify-v0` @ `ba09669`).
Candidate (a) — drift **operational cadence** — is the remaining drift item: a
DEPLOYMENT/operator activity, not a new comparator. The comparator already ships
(the `drift` subcommand, classify-native input mode). This session stands up the
**repeatable snapshot→diff cadence** and captures the **untuned baseline** (run 1).

**Build/run split (load-bearing):**
- **CC ($0):** select the domain subset from the operator's list file; build the
  repeatable snapshot→diff recipe + any thin wiring + tests. NO Azure, NO cascade
  run, NO spend.
- **Operator (S30 operator-run pattern):** run the cascade on the selected
  domains to produce the snapshot parquet; cover the (cents-scale) spend. CC
  stages the EXACT command; the operator runs it.

**STAGE-1 GUARD (anti-trap — the stage1-vs-stage3 confusion, 4th occurrence):**
The drift comparator consumes **`stage1_predictions`** — the 6 `is_business`
PREDICTION_COLUMNS. The drift deliverable this session is **Stage 1 ONLY**.
Running the full cascade to Stage 2/3 is fine for pipeline exercise / to produce
those outputs, but **do NOT build a Stage 2/3 drift surface.** "Tech companies so
the cascade goes all the way" is about exercising tiers, NOT about monitoring
Stage 2/3.

**CADENCE PHASE (load-bearing):** the model is UNTUNED. During tuning, snapshots
are taken **per tuning change (event-driven)**, NOT on a timer. So this session
builds the repeatable MANUAL recipe and **DEFERS the launchd scheduler** to the
stable (post-tuning, post-labeling) phase. Thresholds stay **provisional /
look-don't-act** — this session calibrates NOTHING; run 1 is the untuned
starting point, attributable by `model_version` SHA.

---

## Anchors (S43 cold start — verify, do not trust)

- Repo HEAD: `ba09669` (S42 E18 pin). Parent `b41cf72` (S41).
- Workspace HEAD: `48ef090` (S42 anchor-pin). Tags: **16**
  (`barcada-drift-classify-v0` @ `ba09669`).
- Canonical 16-path: **970**. Combined floor: **1048** (970 + 13 + 65 drift).
- Fixtures: html 222 / expected 202 / meta 222 / baseline 1213 / cassettes 30 /
  exclusions 30.

---

## Halt protocol
```
HALT @ Phase N step S.s
Expected:    <claim from prompt>
Observed:    <actual reality from source/artifact>
Discrepancy: <one-line summary>
Surfacing to operator. Awaiting guidance.
```
After a halt: do NOT mutate, do NOT proceed, wait. **Verify-before-trust** (S41
four-correction / S42 hard-coded-writer lessons): read the file/source before
building on a claim; the live tree wins over this prompt.

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

Run 0.1/0.2 first (cheap anchors). Then — because the cascade RUN is operator-
gated and may not complete in-session — surface the Phase-0.COST gate (below)
and the domain-file source-verify BEFORE the ~80s baseline. Run the full baseline
(0.3–0.6) once scope + the operator's run intent are confirmed (i.e. before any
commit at Phase 3).

### Step 0.1 — HEADs
```
git -C ~/crawler-audit rev-parse HEAD                 # Expect 48ef090 (or later doc-edit)
git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD   # Expect ba09669; parent b41cf72
# Tolerate operator-side eval_data/* commits in ba09669..HEAD (verify each via git show --stat).
```
### Step 0.2 — Tags (16)
```
git -C /Users/administrator/projects/barcada-scraper tag -l | wc -l   # Expect 16
git -C /Users/administrator/projects/barcada-scraper rev-list -n 1 barcada-drift-classify-v0   # Expect ba09669
```
### Steps 0.3–0.6 (run on the build path; see ordering note above)
- 0.3 fixtures 222/202/222/1213/30/30.
- 0.4 canonical 16-path → **970**.
- 0.5 `tests/classifier/llm/test_prompt_logger.py` → 13 ; `tests/drift/` → 65 ;
  combined floor **1048** (must not decrease).
- 0.6 `from tools.baseline_v0 import drift, drift_classify` imports;
  `drift_classify.py` byte-identical since `3266bc4`; `src/` unchanged since
  `ba09669`; `canary.py` untouched.

If any of 0.1–0.6 fail, HALT.

---

## Phase 0.COST — spend gate (BLOCKING; (a) is the first non-$0 path)
CC's work is $0. The OPERATOR's cascade run is the spend. Estimate + get explicit
sign-off BEFORE the operator runs:
- Rules-tier domains = $0 (no embeddings, no LLM). Cost accrues only on the
  escalated subset (LR embeddings + LLM adjudication) and, if the full cascade
  runs, Stage 2 (`gpt-4.1-mini`) + Stage 3 LLM on the tech subset.
- For ~50–100 domains with ~10–15% escalation, expect **well under $1** total
  (per the architecture cost model: Stage 1 ≈ $80 / 50M; Stage 2/3 per-domain
  fractions of a cent). Compute the concrete figure from the selected count +
  expected escalation; record it; the operator confirms. No run until confirmed.

---

## Phase 1 — Scope confirmation + run-shape (operator-led; no code)

1. Confirm (a). Confirm the **build/run split** and the **Stage-1 guard** above.
2. **Domain-list file:** the operator provides the path. **Source-verify it
   FIRST** — `pl.read_parquet`/`read_csv`/inspect: what columns? Is there a
   category/type/industry field usable to ensure technology-company
   representation? If NO such signal exists, surface it (do not silently guess
   tech-ness from domain strings) and ask the operator how tech domains are
   identified in the list.
3. **Run shape (operator choice, present consequences):**
   - **Stage-1-only run** — cheapest, fully sufficient for the drift deliverable
     (the comparator only needs `stage1_predictions`).
   - **Full cascade (Stage 1→2→3)** — the operator's "all the way"; exercises
     every stage, yields Stage 2/3 outputs too, slightly higher (still <$1).
   Default = whatever the operator wants for coverage; the drift deliverable
   consumes Stage 1 regardless.
4. **Selection target:** ~50–100 domains, deliberately spanning likely
   business-score bands with enough technology companies that the escalated tiers
   (LR/LLM) and — if full cascade — Stage 2/3 are exercised. **Coverage is
   VERIFIED POST-RUN** (CC cannot compute `signals_business_score` without the
   parser): selection is best-effort from the file's signal; the real check is
   the run's `tier_decided` distribution + stage presence. If run 1 comes back
   all-rules (the dev-sample failure), re-select and re-run.

**HALT IF** the scope would require a `src/` change, a `canary.py` change, a
Stage 2/3 drift surface, or editing `BARCADA_CRAWLER_REMEDIATION_PLAN.md`.

---

## Phase 2 — Design gate (AskUserQuestion; genuine choices only)
- **Q1 Run shape** — Stage-1-only vs full cascade (Phase 1.3).
- **Q2 Selection method** — by the file's category field (if present) vs an
  operator-supplied tech sublist vs operator-curated 50–100 (present what the
  file actually supports, from the Phase-1 source-verify).
- **Q3 Snapshot convention** — how snapshots are named/stored for the diff
  (recommend: `model_version` SHA + run-date in the path/filename, so the diff is
  attributable and `model_version` changes per tuning iteration). Schema/dtype
  pin from E18 already guards the columns.
- **Q4 Commit shape** — single self-contained commit (selection script + recipe +
  tests + runbook).
Present the Phase-1 source-verified file findings + the cost estimate alongside.

---

## Phase 3 — Implementation (strict order) + per-commit checkpoint

CC's $0 deliverables (keep MODEST — the comparator ships; do NOT reimplement
diffing or build a scheduler):
1. **Domain selection** — read the operator's list, select ~50–100 ensuring
   technology representation per Q2, write the selected subset (a committed
   input artifact). Tests for the selection logic (hermetic, mocked list).
2. **Snapshot→diff recipe** — a runbook + any thin wrapper: how the operator runs
   the cascade on the selected domains, where the `stage1_predictions` output
   lands, how it's named (Q3), and the exact `barcada-baseline drift <snap-N-1>
   <snap-N>` invocation (classify-native auto-detected). NO new comparator code.
3. **Post-run coverage check** — a documented (and if cheap, scripted) check that
   reads a run's `stage1_predictions` and reports the `tier_decided` distribution
   + (full cascade) stage2/3 presence, so coverage is confirmed before the
   baseline is accepted.

Per-commit checkpoint (every boundary):
1. Combined suite vs Phase-0 baseline (**970 / 1048**); new tests ADD. Keep new
   tests OUT of the canonical 16-path dirs (S39 directory lesson) — `tests/drift/`
   or another non-swept dir; re-run the 16-path alone to confirm 970.
2. Ruff check + format; complexity < 15.
3. Verification table (claim → reality → status), every claim backed by captured
   output. Any unevidenced row → HALT.
4. git status — stage ONLY intended files; operator `eval_data/*`, the
   `.claude` lock, `SESSION_36_PROMPT.md` UNSTAGED. Barcada copyright header
   (current year) on any new source file.
5. "Confirm to commit?" — `-F /tmp/<id>-msg.txt`; NO `-m`; NO backticks; NO
   `Co-Authored-By`.
6. Post-commit: re-run step 1; clean tree.

---

## Operator-run interlude (outside CC; after CC's commit)
The operator runs the staged cascade command on the selected domains → produces
the run-1 `stage1_predictions` snapshot (the untuned baseline). CC does NOT run
it. If the operator runs it in-session, CC then runs the Phase-3.3 coverage check
on the real output and confirms the comparator loads it clean (classify-native).
If not run in-session, the baseline capture + coverage confirmation carries to a
follow-up; CC's recipe + selection still ship as a complete $0 deliverable.

---

## Phase 4 — Pre-push gate (whole-tree)
`ruff check .` + `ruff format --check .`, `vermin --target=3.10-`,
`validate_consistency`. eval_data WIP halt protocol applies. Confirm no
unintended `src/` delta; `drift_classify.py`/`canary.py` untouched.

---

## Phase 5 — Push + tag (after operator confirms)
- Push `origin/main` after operator confirms.
- Tag: (a) is operational cadence, not a code-workstream milestone — place NO new
  workstream tag unless the operator wants a deliverable tag for the cadence kit.
  No tag on a recipe-only commit by default.

---

## Phase 6 — Workspace close-out
- `SESSION_LOG.md` S43 entry: scope (a); the selection + recipe shipped; run shape
  chosen; **run-1 disposition** (captured untuned baseline / deferred to operator
  follow-up); coverage result if run; counts; spend (operator-run figure or
  "$0 CC, operator-run pending").
- Refill `SESSION_TRANSITION_TEMPLATE.md` for S44: anchors; 970 / new combined
  floor; tag count; **cadence status** (recipe shipped; baseline captured? thresholds
  still provisional/uncalibrated; launchd scheduler DEFERRED to stable phase).
- Fold LESSONS (e.g. cadence-is-event-driven-during-tuning; coverage-verified-
  post-run).
- Push workspace after operator confirms.

---

## Boundaries (load-bearing)
- (a) operational cadence ONLY. NO new comparator code (it ships). NO Stage 2/3
  drift surface (Stage-1 guard). NO launchd scheduler this session (deferred to
  stable phase). NO `src/` change; `drift_classify.py` byte-identical; `canary.py`
  untouched.
- CC does NO Azure / NO cascade run / NO spend. The operator runs the cascade
  (S30 pattern); CC stages the exact command.
- Thresholds remain PROVISIONAL / look-don't-act; this session calibrates nothing.
  `model_version` must change per tuning iteration (snapshot attribution).
- Selection tech-coverage is best-effort pre-run; tier/stage coverage is VERIFIED
  POST-RUN from `tier_decided` + stage presence. Do not claim coverage from
  selection alone.
- Canonical 970 + combined floor 1048 must NEVER decrease. Verify-before-trust:
  source-verify the domain-list file's schema before building selection.
```
