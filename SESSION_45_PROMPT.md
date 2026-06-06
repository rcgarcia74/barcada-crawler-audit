# Session 45 prompt — 3b: per-shard union helper + RUNBOOK/coverage reconcile (drift cadence)

**Drafted at S44 close (2026-06-06), operator-commissioned.** Mirrors the
S20/.../S44 prompt structure (7-phase, strict order, halt-on-mismatch). Re-read on
session open. Lives at `~/crawler-audit/SESSION_45_PROMPT.md`.

---

## WHAT THIS IS

The S44 cascade-run exposed that the drift cadence is **sharded reality**: a real run
hash-scatters domains across N `shard=NNNNN` partitions (`shard_id_for_domain =
int(sha256(d.lower())[:8],16) % 100`), but the RUNBOOK uses a singular `--shard` and
`check_drift_coverage` reads a single `--predictions` parquet. CC reconciled this
**manually** in `/tmp` for the run-1 capture (loop Stage 1 over every produced shard →
`pl.concat` into one `_union/predictions.parquet` → coverage). **S45 productizes that
union step and reconciles the RUNBOOK** — the operator-confirmed design is a **standalone
union helper** (materialize `_union/predictions.parquet`), keeping the already-shipped
`check_drift_coverage.py` and `drift.py` **byte-stable** (the union is a real bankable
artifact those tools then consume unchanged).

This is the **(3a-done → 3b)** scope. 3a shipped at S44 (`b95df00`, the `is_valid_domain`
recall fix). 3b is **$0, tools-only** (additive `tools/baseline_v0/` + `tests/drift/`).

**Not a tuning change. Not a baseline change.** Run-1 stays FROZEN at its 52 classified
domains (`model_version 9f6f66d5e726`, banked in ADLS
`abfss://output@barcadastorage.dfs.core.windows.net/drift-run1/`). The union helper is
how FUTURE multi-shard snapshots get materialized; it does not touch run-1.

**Load-bearing:** do not break a confirmed-working feature. Canonical **970** and combined
floor **1077** must NEVER decrease (new tests ADD in `tests/drift/`). The live tree wins
over this prompt.

---

## Anchors (S45 cold start — verify, do not trust)

- Repo HEAD: **`b95df00`** (S44 post-close domain_validator recall fix; +176/-11, 2 files).
  Parent `9f6f66d` (S43 drift-cadence-kit). Tolerate operator-side `eval_data/*` commits in
  `b95df00..HEAD` (verify each via `git show --stat`).
- Workspace HEAD: `6d7e266` (S44 validator-fix record) or a later doc-edit.
- Tags: **16** (`barcada-drift-classify-v0` @ `ba09669`; no S43/S44 tag).
- Canonical 16-path: **970**. Combined floor: **1077** (970 + 13 prompt_logger + 94 drift).
- Drift sub-suite: **94** (22 fetch + 21 S40 classify + 13 classify-native + 6 S41
  remediation + 3 S42 E18 pin + 29 S43 cadence). S45 ADDS to this (union tests).
- domain_validator suite: **385** (354 pre-existing + 31 from b95df00) — OUTSIDE the 970/1077
  tracked floors; informational.
- Fixtures: html 222 / expected 202 / meta 222 / baseline 1213 / cassettes 30 / exclusions 30.
- run-1 baseline: CAPTURED + banked (ADLS `drift-run1/`), `model_version 9f6f66d5e726`,
  52 domains, Layer-1 PASS — FROZEN; S45 does not touch it.

---

## Halt protocol

```
HALT @ Phase N step S.s
Expected:    <claim from prompt>
Observed:    <actual reality from source/artifact>
Discrepancy: <one-line summary>
Surfacing to operator. Awaiting guidance.
```

After a halt: do NOT mutate, do NOT proceed, wait. **Verify-before-trust**: read the
file/source before building on a claim; the live tree wins over this prompt.

---

## Phase 0 — Cold-start verification (mandatory; halt-on-mismatch)

### 0.1 — HEADs
```
git -C ~/crawler-audit rev-parse HEAD                                  # Expect 6d7e266 (or later doc-edit)
git -C /Users/administrator/projects/barcada-scraper rev-parse HEAD    # Expect b95df00; parent 9f6f66d
```
### 0.2 — Tags (16)
```
git -C /Users/administrator/projects/barcada-scraper tag -l | wc -l                       # Expect 16
git -C /Users/administrator/projects/barcada-scraper rev-list -n 1 barcada-drift-classify-v0   # Expect ba09669
```
### 0.3 — Fixtures (UNCHANGED)
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
### 0.4 — Canonical baseline (expect 970)
Run the canonical 16-path invocation (per SESSION_TRANSITION_TEMPLATE.md). Expect **970
passed**. Drift tests live in `tests/drift/` (OUTSIDE the sweep).
### 0.5 — Sub-suites + combined floor
```
.venv/bin/python -m pytest tests/classifier/llm/test_prompt_logger.py -q   # expect 13
.venv/bin/python -m pytest tests/drift/ -q                                 # expect 94 (pre-S45)
# Combined floor = 1077. Must NOT decrease; S45 union tests ADD to tests/drift/.
```
### 0.6 — Deliverable + boundary presence
```
.venv/bin/python -c "from tools.baseline_v0 import drift, drift_classify, select_drift_domains, check_drift_coverage; print('kit OK')"
git -C /Users/administrator/projects/barcada-scraper diff 3266bc4 --quiet -- tools/baseline_v0/drift_classify.py && echo "drift_classify.py BYTE-IDENTICAL since S40"
git -C /Users/administrator/projects/barcada-scraper diff b95df00 --quiet -- src/ && echo "src/ UNCHANGED since b95df00"
# Confirm the S44 validator fix is in: the 3 recovered domains validate.
.venv/bin/python -c "from barcada_scraper.domain_validator.check_domains import is_valid_domain; print('validator-fix OK', all(is_valid_domain(d) for d in ['nessis.ca','theeethereal.com','octagoncybersecurity.ng']))"
```

If any of 0.1–0.6 fail, HALT.

---

## Phase 1 — Scope confirmation (operator-led; no code)

Scope is **3b**: a standalone per-shard union helper + RUNBOOK/coverage reconcile.
**HALT IF** the chosen approach would require: a `src/` change, a `canary.py` /
`drift.py` / `drift_classify.py` / `check_drift_coverage.py` byte change (the union is a
SEPARATE helper; those stay byte-stable), the launchd scheduler, a Stage 2/3 drift
surface, an Azure/cascade run, editing `BARCADA_CRAWLER_REMEDIATION_PLAN.md` or
`docs/phase4_implementation_plan.md`.

---

## Phase 2 — Design gate (AskUserQuestion; genuine choices only)
Settled at S44 close: **standalone union helper** (not glob-mode on shipped tools).
Remaining genuine choices to elicit: helper module name + CLI shape (standalone
`python -m tools.baseline_v0.<name>` vs a `barcada-baseline` subcommand); exact union
output path convention (`crawl_date=<d>/_union/predictions.parquet`); model_version
uniformity — RECOMMEND **hard-fail** (exit 2), not warn: a union spanning multiple
model_versions is not a valid single-snapshot (a snapshot is one model's output); a
mixed-version union is a corrupt baseline and must error, not warn-and-proceed (operator
may override to warn, but the default is hard-fail); commit shape.

---

## Phase 3 — Implementation (strict order) + per-commit checkpoint

**Deliverable (4 parts):**
1. **Union helper** — `tools/baseline_v0/union_drift_shards.py` (standalone, $0, offline):
   reads a `stage1_predictions/crawl_date=<d>/` root, globs `shard=*/predictions.parquet`,
   `pl.concat` (vertical) → writes `crawl_date=<d>/_union/predictions.parquet`.
   **Disjointness guard (load-bearing):** concat-without-dedup is valid ONLY because the
   shard hash partitions each domain into exactly one shard. The helper MUST verify this
   post-concat: assert NO duplicate `domain` values in the unioned frame. A duplicate means
   the disjointness assumption broke (a re-run, a mis-glob, or overlapping crawl_dates) →
   exit 2 with a clear "duplicate domain across shards — union invalid" message. Do NOT
   silently dedup or fan out (the S41 duplicate-domain fan-out corrupted verdict rates).
   Validates: ≥1 shard found (else exit 2); schema carries `domain` + the 6
   `PREDICTION_COLUMNS` (reuse `drift_classify.PREDICTION_COLUMNS` — the E18 pin);
   `model_version` set across shards MUST be uniform → if >1 distinct value, exit 2
   "mixed model_version — union is not a valid snapshot" (per Phase-2 hard-fail default;
   warn only if the operator explicitly overrode). Reports row count + shard count + the
   (single) `model_version`. Exit 0 success / 2 input error. Barcada copyright header (2026).
2. **RUNBOOK reconcile** — `tools/baseline_v0/drift_cadence/RUNBOOK.md`: replace the
   singular-`--shard` Step 2 with the per-shard reality (loop `barcada-classify run`
   over every produced shard; note `barcada-classify` is single-shard and a manual loop
   needs `--force-concurrent-run` because a completed single-shard run does not self-halt;
   `barcada-validate` is stale → use `python -m barcada_scraper.domain_validator.check_domains`;
   LR bundle is ADLS-resident). Add a Step 2.union (run the helper). Point Step 3 coverage
   + Step 5 diff at the `_union/predictions.parquet`.
3. **Tests** — `tests/drift/test_union_drift_shards.py` (hermetic, multi-shard synthetic
   parquets): union of N shards → concatenated rowset; schema-validation (missing column →
   error); no-shards / empty → exit 2; duplicate `domain` across two synthetic shards →
   exit 2 (disjointness guard fires, no silent dedup/fan-out); mixed model_version across
   shards → exit 2 (hard-fail); idempotent overwrite; both happy + failure + false paths.
4. **Real-baseline reproduction check** — verify the helper, run over run-1's ACTUAL
   shards, yields the IDENTICAL 52-domain set banked at ADLS `drift-run1/`
   (domain-for-domain; row count 52; `model_version 9f6f66d5e726`). This pins the
   productized union against the real frozen baseline, not just synthetic fixtures.
   **Mechanism:** run-1's shards are ADLS-resident; if CC cannot read ADLS ($0/no-creds),
   this is an OPERATOR-RUN verification (S30 pattern) — the operator runs the helper over
   the real shards (or provides the run-1 domain list) and confirms the 52-domain match.
   The criterion stands regardless of who executes it; do NOT skip it because the artifact
   is remote.

At EVERY commit boundary:
1. Combined suite vs Phase-0 baseline; new tests ADD in `tests/drift/`; re-run the
   canonical 16-path ALONE to confirm **970** (unchanged).
2. Ruff check + format (touched files). Complexity < 15.
3. Verification table (claim → reality → status), every claim backed by captured output.
4. `git status` — stage ONLY intended files; operator `eval_data/*`, the `.claude` lock,
   `SESSION_36_PROMPT.md` UNSTAGED. Barcada copyright header on any new source file.
5. "Confirm to commit?" — `-F /tmp/<id>-msg.txt`; NO `-m`; NO backticks; NO `Co-Authored-By`.
6. Post-commit: re-run step 1; clean tree.

---

## Phase 4 — Pre-push gate (whole-tree)
`ruff check .` + `ruff format --check .`, `vermin --target=3.10-` (src tests scripts tools),
`eval_data/scripts/validate_consistency.py`. **eval_data WIP halt protocol applies** — the
pre-push hook runs validate_consistency on the working tree, so any operator labeling error
(e.g. a duplicate keyword) BLOCKS the push; surface to the operator, do NOT edit eval_data.
Confirm no `src/` delta; `check_drift_coverage.py` / `drift.py` / `drift_classify.py` /
`canary.py` byte-identical.

---

## Phase 5 — Push + tag (after operator confirms)
- Push `origin/main` after operator confirms.
- Tag: NO new tag for the union helper (operational tooling, not a code milestone) unless
  the operator explicitly wants a deliverable tag.

---

## Phase 6 — Workspace close-out
- `SESSION_LOG.md` S45 entry: union helper + RUNBOOK reconcile; counts; spend ($0 CC).
- Refill `SESSION_TRANSITION_TEMPLATE.md` for S46 (anchors; 970 / new combined floor; tag
  count; run-1 baseline status; 3b shipped). Anchor-pin follow-up.
- Fold any LESSONS. Push workspace after operator confirms.

---

## Regression & correctness enforcement (load-bearing — applies all session)
- **Never break confirmed-working features.** Canonical **970** and combined floor **1077**
  must NEVER decrease (re-derive at Phase 0; union tests ADD in `tests/drift/`).
- **"Outside the 16-path" is a DIRECTORY fact** (S39): keep new tests in `tests/drift/`;
  re-run the 16-path alone post-placement to confirm 970.
- **No `src/` change** (3b is tools-only). **Byte-stable:** `check_drift_coverage.py`,
  `drift.py`, `drift_classify.py`, `canary.py` — the union is a SEPARATE helper.
- **Boundaries:** do NOT edit `BARCADA_CRAWLER_REMEDIATION_PLAN.md` or
  `docs/phase4_implementation_plan.md`. No producer; no Stage 2/3 drift surface (Stage-1
  guard — 7th occurrence); no launchd scheduler (deferred). CC does NO Azure / NO cascade
  run / NO spend (the cascade is operator-run; CC verifies on hermetic producer output).
- **run-1 baseline FROZEN** at its 52 (`model_version 9f6f66d5e726`); 3b does not touch it.
  Not a tuning change → does not trigger run-2.
- **Test every change** (happy + failure + false paths); mock real-world data; run tests
  before marking complete.
- **Verify-before-trust / source-verify the premise.** The live tree is authoritative.

---

## Acceptance criteria
- Phase 0 green (970 / 1077 / 16 tags / fixtures / kit + validator-fix present) before work.
- Union helper ships in `tools/baseline_v0/`, additive; consumes a real per-shard
  partition (hermetic fixtures) and materializes `_union/predictions.parquet` that
  `check_drift_coverage` + `drift` read UNCHANGED.
- RUNBOOK reconciled to the per-shard reality (loop + union + guard note + stale-validate
  note); singular `--shard` examples replaced.
- **Reproduction pin (mandatory):** the helper over run-1's real shards reproduces the
  banked 52-domain set exactly (domain-for-domain, 52 rows, `model_version 9f6f66d5e726`)
  — verified by CC or operator-run (S30). Synthetic fixtures alone do NOT satisfy this;
  without it the productized union is not proven to match the baseline run-2 will diff against.
- All green: canonical 970 unchanged, combined floor not decreased (union tests add),
  ruff/format/vermin/validate clean, complexity < 15, no `src/` change, the four named
  tools byte-identical, every commit-message claim backed by captured output.
- If no-ship: decision recorded in SESSION_LOG; baselines re-pinned for S46; no commit.
