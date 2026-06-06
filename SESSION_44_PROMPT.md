# Session 44 prompt — cold-start + run-1 baseline branch (drift cadence shipped S43)

**Drafted at S43 close (2026-06-05), operator-commissioned.** Mirrors the
S20/.../S43 prompt structure (7-phase, strict order, halt-on-mismatch). Re-read on
session open.

This prompt lives at `~/crawler-audit/SESSION_44_PROMPT.md`.

---

## WHAT THIS IS

A-classify drift is COMPLETE (S42, `barcada-drift-classify-v0` @ `ba09669`) and
the **drift operational-cadence KIT shipped S43** (`9f6f66d`): the domain
selector, the two-layer coverage check, and the operator RUNBOOK. The kit is the
instrument; **the paid baseline capture is an OPERATOR-RUN** and was deferred out
of S43.

S44 therefore BRANCHES on a single question resolved in Phase 0.BASELINE-CHECK:
**has the operator run the full cascade on the 75 selected domains yet** (does a
run-1 `stage1_predictions` baseline exist)?
- **Branch A — baseline captured:** confirm it with the two-layer coverage check,
  bank it + the Stage-2/3 partitions with their `model_version` SHA, and (if the
  operator wants) ship a tiny $0 run-manifest helper + stage the run-2 diff
  invocation for later (not executed — one snapshot cannot drift). This is a
  $0/verification session.
- **Branch B — not yet run:** the cadence kit is complete and waiting; S44 is
  either a no-ship "operator runs it now" hand-off, or a fresh operator-led scope
  (e.g. D labeling). Pick with the operator; do not manufacture a baseline.

Build/run split is UNCHANGED: CC is $0/offline; the cascade run is operator-run
(S30 pattern). Thresholds stay **provisional / look-don't-act**; the launchd
scheduler stays **DEFERRED** to the stable (post-tuning) phase. Drift surface is
**Stage 1 ONLY** (the stage1-vs-stage3 guard — 5th occurrence).

**Load-bearing:** do not break a confirmed-working feature. Canonical **970** and
combined floor **1077** must NEVER decrease. The live tree wins over this prompt.

---

## Anchors (S44 cold start — verify, do not trust)

- Repo HEAD: `9f6f66d` (S43 drift-cadence-kit). Parent `ba09669` (S42 E18 pin).
- Workspace HEAD: `ee97f0c` (S43 anchor-pin). Parent `783d04e` (S43 close-out).
- Tags: **16** (`barcada-drift-classify-v0` @ `ba09669`; no S43 tag).
- Canonical 16-path: **970**. Combined floor: **1077** (970 + 13 prompt_logger +
  94 drift).
- Drift sub-suite: **94** (22 fetch + 21 S40 classify + 13 classify-native + 6 S41
  remediation + 3 S42 E18 pin + 29 S43 cadence).
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
four-correction / S42 hard-coded-writer / S43 hermetic-recipe lessons): read the
file/source before building on a claim; the live tree wins over this prompt.

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

Run 0.1/0.2 first (cheap anchors), then the cheap presence gate
(0.6 + 0.BASELINE-CHECK) before the ~80s canonical baseline — the disposition may
make 0.3/0.4 a no-ship-skippable cost (Branch B / fresh scope decides at Phase 1).

### Step 0.1 — HEADs
```
git -C ~/crawler-audit rev-parse HEAD                 # Expect ee97f0c (or later doc-edit)
git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD   # Expect 9f6f66d; parent ba09669
# Tolerate operator-side eval_data/* commits in 9f6f66d..HEAD (verify each via git show --stat).
```
### Step 0.2 — Tags (16)
```
git -C /Users/administrator/projects/barcada-scraper tag -l | wc -l   # Expect 16
git -C /Users/administrator/projects/barcada-scraper rev-list -n 1 barcada-drift-classify-v0   # Expect ba09669
```
### Step 0.3 — Fixtures (UNCHANGED)
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
### Step 0.4 — Canonical baseline (expect 970)
Run the canonical 16-path invocation (per the SESSION_TRANSITION_TEMPLATE.md
"Combined-suite-at-Session-open baseline" block). Expect **970 passed**. The drift
tests live in `tests/drift/` (OUTSIDE the sweep).
### Step 0.5 — Sub-suites + combined floor
```
.venv/bin/python -m pytest tests/classifier/llm/test_prompt_logger.py -q   # expect 13
.venv/bin/python -m pytest tests/drift/ -q                                 # expect 94
# Combined floor = 1077. Must NOT decrease.
```
### Step 0.6 — Deliverable + boundary + S43 kit presence
```
.venv/bin/python -c "from tools.baseline_v0 import drift, drift_classify; \
print('OK', len(drift_classify.PREDICTION_COLUMNS)==6 and bool(drift._reject_ambiguous_fetch_subset))"
.venv/bin/python -c "from tools.baseline_v0 import select_drift_domains, check_drift_coverage; print('kit OK')"
test -f tools/baseline_v0/drift_cadence/run1_domains.txt && echo "run1 selection PRESENT"
git -C /Users/administrator/projects/barcada-scraper diff 3266bc4 --quiet -- tools/baseline_v0/drift_classify.py \
  && echo "drift_classify.py BYTE-IDENTICAL since S40"
git -C /Users/administrator/projects/barcada-scraper diff 9f6f66d --quiet -- src/ && echo "src/ UNCHANGED since S43"
```

If any of 0.1–0.6 fail, HALT.

---

## Phase 0.BASELINE-CHECK — does a run-1 stage1_predictions baseline exist? (BLOCKING)

The cadence kit's value completes when a real run-1 baseline is captured. Resolve
which branch S44 is on BEFORE the canonical baseline (it may be skippable).

1. **Locate (operator path first):** ASK the operator for the run-1
   `stage1_predictions` path — they ran it and know where it is. Only if they
   can't supply it, fall back to a bounded search of a known root:
   `find <OUTPUT_ROOT> /tmp -path '*stage1_predictions*' -name 'predictions.parquet' 2>/dev/null`
   (`<OUTPUT_ROOT>` must be a real path — if unknown, ask rather than guess). An
   ADLS-resident baseline needs the operator to drop a local copy or run the read
   (S30, $0).
2. **If a candidate is found/provided — confirm it is the real run-1 baseline:**
   ```
   python -m tools.baseline_v0.check_drift_coverage \
       --predictions <run1>/stage1_predictions/.../predictions.parquet \
       --stage2 <run1>/stage2_summaries/.../summaries.parquet \
       --stage3 <run1>/stage3_predictions/.../predictions.parquet
   ```
   - Exit 0 (Layer 1 escalation present, NOT all-rules) + `model_version` recorded
     -> **Branch A**.
   - Exit 1 (all-rules) -> the baseline is degenerate; surface "re-select
     (`--seed`) + re-run" to the operator; treat as no usable baseline yet.
   - **Layer roles (explicit):** Layer 1 (Stage-1 tier spread / not all-rules)
     GATES the branch — it determines whether the run-1 baseline is valid for the
     drift purpose. Layer 2 (Stage-2/3 populated) is RECORDED, NOT gating. A run
     with Layer 1 PASS but a sparse/empty Stage 3 is STILL **Branch A** for the
     Stage-1 baseline — bank what Stage 2/3 produced, and record "Stage 3 sparse"
     as a NOTE + a future-re-run flag (the banked-artifact quality is degraded,
     not the baseline). Sparse Layer 2 NEVER forces Branch B or a re-select; only
     a Layer-1 all-rules failure (Exit 1) does.
3. **If none exists / operator confirms not run -> Branch B.** Do NOT manufacture
   a baseline, run the cascade, or accept a synthetic/dev parquet as run-1.

---

## Phase 1 — Scope resolution (operator-led; no code)

- **Branch A (baseline captured):** confirm the two-layer coverage result + the
  `model_version` SHA. **MANDATORY (regardless of whether any code ships): record
  in SESSION_LOG the banked artifact paths — the run-1 stage1_predictions
  partition AND the produced stage2/stage3 partitions — each with its
  `model_version` SHA.** This is the durable output of the full-cascade run (the
  real artifact a future Stage-2/3 drift comparator will need; do not let it be
  lost). Then resolve with the operator whether S44 also ships a small $0
  deliverable: (i) a run-manifest helper that records each banked partition's
  path + SHA programmatically; and/or (ii) staging/documenting the run-2 diff
  invocation (`drift --baseline run1 --current run2`) for when run-2 exists — do
  NOT execute a diff this session; one snapshot cannot drift. Both are additive
  `tools/` + `tests/drift/` only. If the operator wants only the baseline
  confirmed + banked (no new code), S44 is a $0 verification + close-out
  (workspace-log commit only).
- **Branch B (not run):** either (a) hand off "operator runs the cascade now" and
  close S44 as a no-ship wait, or (b) pick a fresh operator-led scope (D Phase-4
  PR-D tooling — gated on operator labeling; or another candidate). Source-verify
  any fresh-scope premise before scoping (S41/S42/S43 anti-traps).
  Before the operator asserts D is unblocked, CC SHOULD source-check whether
  labeling artifacts actually exist (inspect the eval_data path) — the same
  bidirectional verify-before-trust applied everywhere else; do not rely on
  assertion alone for a cheaply-checkable fact.

**HALT IF** the chosen scope would require a `src/` change, a `canary.py` change,
a Stage 2/3 drift surface, the launchd scheduler, or editing
`BARCADA_CRAWLER_REMEDIATION_PLAN.md`.

---

## Phase 2 — Design gate (AskUserQuestion; genuine choices only)
Elicit only real choices (manifest shape; whether to stage/document the run-2
diff invocation — not execute, one snapshot cannot drift; commit shape). Present
the Phase-0.BASELINE-CHECK coverage result alongside.

---

## Phase 3 — Implementation (strict order) + per-commit checkpoint
Keep MODEST — the comparator + the cadence kit already ship; do NOT reimplement
diffing, the coverage check, or build a scheduler. At EVERY commit boundary:
1. Combined suite vs Phase-0 baseline (**970 / 1077**); new tests ADD. Keep new
   tests in `tests/drift/` (or another non-swept dir — S39 directory lesson);
   re-run the canonical 16-path ALONE to confirm 970.
2. Ruff check + format (touched files). Complexity < 15.
3. Verification table (claim -> reality -> status), every claim backed by captured
   output. Any unevidenced row -> HALT.
4. git status — stage ONLY intended files; operator `eval_data/*`, the `.claude`
   lock, `SESSION_36_PROMPT.md` UNSTAGED. Barcada copyright header (current year)
   on any new source file.
5. "Confirm to commit?" — `-F /tmp/<id>-msg.txt`; NO `-m`; NO backticks; NO
   `Co-Authored-By`.
6. Post-commit: re-run step 1; clean tree.

---

## Phase 4 — Pre-push gate (whole-tree)
`ruff check .` + `ruff format --check .`, `vermin --target=3.10-`,
`eval_data/scripts/validate_consistency.py`. eval_data WIP halt protocol applies.
Confirm no unintended `src/` delta; `drift_classify.py` / `canary.py` untouched.

---

## Phase 5 — Push + tag (after operator confirms)
- Push `origin/main` after operator confirms.
- Tag: place NO new tag for cadence/baseline/manifest work (operational, not a
  code milestone) unless the operator explicitly wants a deliverable tag.

---

## Phase 6 — Workspace close-out
- `SESSION_LOG.md` S44 entry: branch taken (A captured / B pending-or-fresh);
  baseline provenance + coverage result if confirmed; counts; spend.
- Refill `SESSION_TRANSITION_TEMPLATE.md` for S45 (anchors; 970 / new combined
  floor; tag count; baseline status). Anchor-pin follow-up.
- Fold any LESSONS.
- Push workspace after operator confirms.

---

## Regression & correctness enforcement (load-bearing — applies all session)
- **Never break confirmed-working features.** Canonical **970** and combined
  floor **1077** must NEVER decrease (re-derive at Phase 0).
- **"Outside the 16-path" is a DIRECTORY fact** (S39): a test in a swept dir
  silently joins the 970 headline. Keep keep-the-headline-stable tests in
  `tests/drift/`; re-run the 16-path alone post-placement.
- **No `src/` change** unless the chosen scope explicitly requires it; if it does,
  check ALL consumers for side effects before committing.
- **Boundaries:** do NOT edit `BARCADA_CRAWLER_REMEDIATION_PLAN.md` (deviations ->
  SESSION_LOG + LESSONS only). `drift_classify.py` byte-identical; `drift.py` /
  `canary.py` untouched unless a scope explicitly targets them. No producer; no
  Stage 2/3 drift surface; no launchd scheduler (deferred).
- **CC does NO Azure / NO cascade run / NO spend.** The operator runs the cascade
  (S30); CC stages the exact command and verifies on hermetic producer output.
- **Test every change** (happy + failure + false paths); run tests before marking
  complete; mock real-world data.
- **Verify-before-trust / source-verify the premise.** The live tree is
  authoritative over this prompt; if a `file:line` here is stale, the tree wins.

---

## Acceptance criteria
- Phase 0 green (970 / 1077 / 16 tags / fixtures / kit present) before any work.
- Branch resolved with the operator (A baseline-confirmed-and-banked / B
  pending-or-fresh) at Phase 0.BASELINE-CHECK + Phase 1.
- **Branch A:** the run-1 baseline confirmed (Layer 1 pass) + the banked artifact
  paths (stage1 + stage2/3) and their `model_version` SHA RECORDED in SESSION_LOG
  — mandatory even on a no-code close.
- If a build ships: all green, canonical 970 unchanged, combined floor not
  decreased, ruff/format/vermin/validate clean, complexity < 15, no unintended
  `src/` change, every commit-message claim backed by captured output.
- If no-ship: decision recorded in SESSION_LOG; baselines re-pinned for S45; no
  commit.
