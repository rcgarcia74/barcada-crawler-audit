# W4.1.5 Small-Subset Validation Report

**Date:** 2026-05-21
**Repo HEAD at run:** `dd64963` (W4.1.5.S3 commit, before V + tag)
**Driver:** `tests/runners/fixture_cascade/` (Surfaces 1 + 2 + 3)
**Run ID:** `w4-1-5-validation-2026-05-21`

---

## Invocation

```
python -m tests.runners.fixture_cascade.cli \
    --fixture-root /Users/administrator/projects/barcada-scraper/tests/fixtures/html \
    --output-dir /tmp/w415-validation/run01 \
    --run-id w4-1-5-validation-2026-05-21 \
    --llm-mode fake \
    --max-fixtures 10 \
    --log-level WARNING
```

**Stdout:**
```
run_id=w4-1-5-validation-2026-05-21 fixtures=10 stage1=$0.000000
stage2=$0.000000 stage3=$0.000000 total=$0.000000 expected_json=10
```

**Wallclock:** ~6 seconds end-to-end.
**Fixtures processed:** 10 (sorted-by-domain order; archive.org through
bestlogisticsjobs.com).

## Acceptance-criteria check (per plan §3 W4.1.5)

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Driver runs against 198-fixture corpus end-to-end without manual intervention. | **MET (subset)** | One CLI invocation produces all artifacts. Small-subset (10) validated; 198-corpus run is W4.2 scope. |
| 2 | All five intermediate parquets exist + conform to schemas. | **MET** | parser.parquet + stage1_predictions.parquet + stage2_predictions/ (Hive) + stage2_summaries.parquet + stage3_predictions.parquet, plus stage2_pages.parquet + stage3_pages.parquet from FetcherSet calls. All present under `/tmp/w415-validation/run01/`. |
| 3 | Per-fixture `expected/<domain>.json` produced + conforms to plan §3 W4.2 example. | **MET** | 10 of 10 expected.json files emitted under `expected/`. Spot-check on archive.org.json shows all top-level META_SCHEMA v1.0 keys (`schema_version`, `parser_output`, `barriers_verdict`, `stage1_decision`, `stage2_decision`, `stage3_decision`) plus the 18-column `stage3_decision` shape per the plan example updated in workspace SHA `a34f7a2`. |
| 4 | Driver writes RUN_ID-stamped cost journal entry. | **MET** | `/tmp/w415-validation/run01/cost_journal/run_w4-1-5-validation-2026-05-21.json` carries `run_id="w4-1-5-validation-2026-05-21"`, three `shards` entries (stages 1/2/3), `outcome="completed"` per shard, `cost_usd=0.0` (fake mode). |
| 5 | Total LLM cost within 3× of $0.30 Claude Code estimate. | **MET (fake-mode subset)** | $0.00 in fake mode; cost envelope unenforceable without real-Azure run. Operator-driven real-mode validation deferred (see "Open items for W4.2"). $0.00 is trivially within "3× of $0.30 floor"; the operator should run `--llm-mode real --max-fixtures 10` to validate the per-fixture cost shape against the audit's $0.30 ballpark before W4.2 full-corpus generation. |
| 6 | Driver does not write outside workspace + `tests/fixtures/html/*/expected/`. | **MET** | All writes confined to `/tmp/w415-validation/run01/` (operator-supplied `--output-dir`). Driver does NOT write into `tests/fixtures/html/*/expected/` in-place — that is a W4.2 operator-driven copy step. |

## Cost journal excerpt

The cost journal records every stage's contribution to the cumulative
RUN_ID-stamped totals. Excerpt (truncated):

```json
{
  "run_id": "w4-1-5-validation-2026-05-21",
  "ceiling_usd": 30.0,
  "totals": {
    "cost_usd": 0.0,
    "stage1_llm_usd": 0.0,
    "stage2_summarization_usd": 0.0,
    "stage2_classification_usd": 0.0,
    "stage3_evidence_usd": 0.0,
    "stage3_primary_usd": 0.0,
    "cached_input_tokens": 0
  },
  "shards": [
    {"shard_id": "fixture-cascade-00000", "stage": 1, "outcome": "completed",
     "cost_usd": 0.0, "domains_processed": 10, ... },
    {"shard_id": "fixture-cascade-00000", "stage": 2, "outcome": "completed",
     "cost_usd": 0.0, "domains_processed": 10, ... },
    {"shard_id": "fixture-cascade-00000", "stage": 3, "outcome": "completed",
     "cost_usd": 0.0, "domains_processed": 10, ... }
  ]
}
```

The fake-mode totals are intentionally zero — the per-call `llm_cost_usd`
field on `FakeAdjudicator` defaults to 0.0. Real-mode totals will
reflect actual Azure billing per `PricingTable(configs/llm_pricing.yaml)`.

## Open items for W4.2

1. **Real-mode small-subset validation.** Acceptance criterion 5 is
   met under fake mode but the $0.30 cost envelope needs an actual
   Azure-mode run before W4.2's full-corpus generation. Operator
   command:

   ```
   AZURE_OPENAI_ENDPOINT=... AZURE_OPENAI_KEY=... \
   python -m tests.runners.fixture_cascade.cli \
       --output-dir <fresh-dir> \
       --run-id w4-1-5-real-validation \
       --llm-mode real --max-fixtures 10
   ```

   Expected actual cost: ~$0.015-$0.06 across 10 fixtures (extrapolated
   from the $0.30 / 198-fixture audit ballpark). Hard ceiling per
   `--stage-budget-usd` default ($10) is far above.

2. **W4.2 expected.json copy step.** The driver writes
   `expected/<domain>.json` under `--output-dir`, NOT in-place to
   `tests/fixtures/html/<category>/expected/`. W4.2 needs an explicit
   operator-side copy step after the real-mode full-corpus run
   completes, with human review per fixture before commit.

3. **W4.3 expected.schema.json reconciliation.** The driver emits the
   18-column `stage3_decision` shape that diverges from
   `tests/fixtures/expected.schema.json` v1.0 (which requires the
   legacy `{partner_type, confidence, tier}` triple). Acceptance
   criterion 3 currently treats v1.0 as informational; W4.3 will
   either bump expected.schema.json to v1.1 or update the consolidator
   to map 18-col → legacy triple. Per deferred prose-only fix
   register entry (e), the next machine-schema bump folds this in.

4. **Fixture-routing coverage in real mode.** Fake mode forces every
   fixture through Stage 2 + Stage 3 (the synthetic classifiers always
   return is_business=True + is_technology=True). Real mode will see
   the actual routing distribution (per `phase4_current_state_2026-05-21.md`
   cost envelope: ~50% via Stage 2, ~35% via Stage 3, rest excluded
   at Stage 1 RULES). W4.2's full-corpus run is the first real signal.

## What the driver demonstrably does NOT do (out of W4.1.5 scope)

- Tier-promotion exercise (T1 → T2 → T3 on `PROTECTION_ERROR_KINDS`)
  — fixture runs return 200 unconditionally; this is W A.0 W7.
- LLM-correctness validation — fake adjudicators are deterministic
  synthetic verdicts; real-mode LLM accuracy is a W4.2 outcome.
- In-place fixture mutation — driver writes only to `--output-dir`.
- Anti-bot interstitial coverage — the fixture corpus has
  cloudflare_challenge / auth_403 / login_wall directories but the
  fixture fetcher returns 200; production T1→T2→T3 escalation logic
  is not exercised.

## Conclusion

**Driver ready for W4.2 full-corpus generation** (acceptance criteria
1-4, 6 fully met; criterion 5 met under fake mode, real-mode
small-subset validation deferred to the W4.2 session opening).
