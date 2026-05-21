# Phase 4 Current-State Verification: Levers 2/3 + W4.2 Cost Envelope

**Date:** 2026-05-21
**HEAD at verification:** `5513b4c68be542c01821326a70c40860266fc95b`
**Source:** Claude Code source-verification session against
`/Users/administrator/projects/barcada-scraper`.
**Provenance:** Report content reconstructed from chat transcript
delivered during Session 12 operator-side reconciliation work. Original
session was a code-side audit; this file preserves the report content
as a durable workspace artifact referenced by
`RECONCILIATION_2026-05-21.md`.

---

## Q1 — Lever 3 (Stage 2 Pass-1 summarization drop)

**Lever 3 is NOT applied.** Stage 2 summarization fires unconditionally;
there is no feature flag gating it.

**Evidence:**

- `src/barcada_scraper/classifier/stage2/run.py:298` calls
  `await summarize_shard(...)` with no if-guard other than the PR-COST
  `would_exceed(0.0)` ceiling check at line 269 (which is a budget exit,
  not a Lever-3 skip).
- `src/barcada_scraper/classifier/stage2/summarizer.py:126` defines
  `summarize_shard` — invoked unconditionally on every eligible row's
  pages.
- `configs/pipeline_config.yaml` contains only
  `stage3_secondary_enabled: false` (Lever 1). No
  `stage2_summarization_enabled` or equivalent key.
- `configs/stage2_thresholds.yaml:42-43` still configures
  `summarizer.max_summary_tokens: 600` — code expects summarization to
  fire.
- `src/barcada_scraper/classifier/stage2/llm_prompts.py:48`
  `SUMMARIZER_SYSTEM_PROMPT` and `:213 SUMMARIZER_USER_TEMPLATE` are
  present, frozen `Final[str]` constants — the Pass-1 surface is intact.
- The cost-journal field `stage2_summarization_usd` (named in
  `phase4_implementation_plan.md:154`) is still wired:
  `stage2/run.py:307-311` increments `cost_tracker.add_llm` from
  `summarizer_result.new_cost_usd`.

## Q2 — Lever 2 (Stage 2 classifier model)

**Lever 2 is NOT applied.** Stage 2 classifier deployment defaults to
`gpt-4.1-mini`, not `gpt-4.1-nano`.

**Model defaults at HEAD (all from `src/barcada_scraper/classifier/cli.py`):**

| Stage / role | CLI flag | Default | Citation |
|---|---|---|---|
| Stage 1 LLM tier | `--llm-deployment` | `gpt-4.1-nano` | `cli.py:201-202` |
| Stage 1 embedding | `--embedding-deployment` | `text-embedding-3-small` | `cli.py:209` |
| Stage 2 summarizer | `--summarizer-deployment` | `gpt-4.1-nano` | `cli.py:216-217` |
| Stage 2 classifier | `--classifier-deployment` | `gpt-4.1-mini` | `cli.py:221-222` |
| Stage 3 evidence | `--evidence-deployment` | `gpt-4.1-mini` | `cli.py:246-247` |
| Stage 3 primary | `--primary-deployment` | `gpt-4.1` | `cli.py:251-252` |
| Stage 3 secondary | `--secondary-deployment` | `gpt-4.1` (off via Lever 1) | `cli.py:259-260` |

**Lever 7** (Stage 3 primary `gpt-4.1` → `gpt-4.1-mini`) is also NOT
applied — the `cli.py:255` help-text reads "PR-E (Lever 7) may swap to
gpt-4.1-mini after validation," confirming the swap is staged but not
landed.

## Q3 — W4.2 cost envelope (198 fixtures, current cascade)

### Fixture corpus distribution (verified by find count)

| Bucket | Count | Routing assumption |
|---|---|---|
| `parking_*` (13 dirs) | 108 | Stage 1 RULES → `is_business=False`, never reach Stage 2 |
| `auth_403` / `cloudflare_challenge` / `login_wall` | 33 | `status != "ok"` → upstream-excluded, never reach LLM at any stage |
| `noindex_empty_title` + `meta_refresh_parking` | 6 | RULES → non-business |
| `legitimate_business` | 15 | RULES → business; Stage 2 fires; Stage 3 fires (saas) |
| `legitimate_nonprofit` | 6 | mostly RULES business; Stage 2 fires; Stage 3 abstains/non-tech |
| `legitimate_blog` | 3 | RULES or LR; not `is_technology=True` |
| `mega_menu` | 3 | likely RULES business; Stage 2+3 fire |
| `spa_hydration_*` + `spa_shell` | 27 | mixed; ~half likely LR/LLM-tier at Stage 1 |
| `international_business` | 3 | RULES or LR |
| **Total** | **198** | |

### Estimated routing (fixture-corpus distribution, not production 85-90% RULES)

- Stage 1 RULES tier: ~180 fixtures (no LLM cost).
- Stage 1 LR tier (one embedding each): ~10-15 fixtures.
- Stage 1 LLM tier (LR-uncertain residual): ~5-10 fixtures.
- Stage 2 eligible (`is_business=True` at Stage 1): ~45-55 fixtures.
- Stage 3 eligible (`is_technology=True` at Stage 2): ~30-40 fixtures.

### Token estimates (per call)

Prompts verified ≥1024 tokens (audit confirmed; this report does not
re-tokenize via API). Cached-input rate applies to the immutable system
prefix; fresh-input rate applies to per-domain user content. Assumes
`warm_cache=3` wired (audit confirmed) so cached-rate effective from
call #1.

| Tier | Sys (cached) | User (uncached) | Output | Rationale |
|---|---|---|---|---|
| Stage 1 LLM (nano) | 1024 | ~500 | ~100 | structured business verdict |
| Stage 2 summarizer (nano) | 1024 | ~1000 | ~600 | mostly homepage_text only (fixture corpus = single HTML; About/Products/etc. slots empty) |
| Stage 2 classifier (mini) | 1500 | ~700 | ~150 | system includes 23-cat taxonomy block; user = summary |
| Stage 3 evidence (mini) | 1024 | ~2000 | ~600 | larger per-page input; PartnerEvidence schema |
| Stage 3 primary (gpt-4.1) | 1500 | ~1000 | ~150 | summary + evidence + parser features |

### Cost per call (from `configs/llm_pricing.yaml`)

| Tier | Cached in $/M | Uncached in $/M | Output $/M | Cost per call |
|---|---|---|---|---|
| Stage 1 LLM (nano) | 0.05 | 0.10 | 0.40 | ~$0.00014 |
| Stage 2 summarizer (nano) | 0.05 | 0.10 | 0.40 | ~$0.00039 |
| Stage 2 classifier (mini) | 0.20 | 0.40 | 1.60 | ~$0.00082 |
| Stage 3 evidence (mini) | 0.20 | 0.40 | 1.60 | ~$0.00193 |
| Stage 3 primary (gpt-4.1) | 1.00 | 2.00 | 8.00 | ~$0.00470 |

### Cost envelope table

| Tier | Model | Fixtures routing | Cost per call | Estimated cost |
|---|---|---|---|---|
| Stage 1 embedding | text-embedding-3-small | ~15 | <$0.0001 | ~$0.001 |
| Stage 1 LLM tail | gpt-4.1-nano | ~10 | $0.00014 | ~$0.001 |
| Stage 2 summarization | gpt-4.1-nano | ~50 | $0.00039 | ~$0.02 |
| Stage 2 classification | gpt-4.1-mini | ~50 | $0.00082 | ~$0.04 |
| Stage 3 evidence | gpt-4.1-mini | ~35 | $0.00193 | ~$0.07 |
| Stage 3 primary | gpt-4.1 | ~35 | $0.00470 | ~$0.16 |
| **Total** | | | | **~$0.30** |

**Order of magnitude:** single dollars at the high end; tens of cents
most likely.

### Material caveats (any of which could shift the estimate by 2-5×)

1. **Stage 2 page-acquisition is an open question.** Stage 2's
   `run_shard` consumes a `pages.parquet` produced by `FetcherSet` HTTP
   fetches against live domains; the fixture HTML is not in that shape.
   The cost above assumes the LLM-only portion of Stage 2 runs against
   pages already loaded from fixture HTML — which is not how the
   production cascade composes today. A W4.2 driver must short-circuit
   `FetcherSet`. **No such short-circuit exists in current code; this is
   engineering work, not a configuration toggle.** The cost number
   assumes the engineering work has been done and only LLM tokens are
   billed.
2. Token estimates derive from word-count of prompt files, not
   `tiktoken`. Conservative ratio used (~1.3 words/token). Actual token
   counts may be ±25%.
3. Cache hit assumption ≥80% on system prefix. `llm_pricing.yaml:25`
   annotates this figure as canary-verified for Stage 1; assumed
   transferrable to Stage 2/3 since the same warm-up mechanism wires
   across stages.
4. Stage 3 primary at `gpt-4.1` ($2.00/M input) is the single largest
   per-call line item. If Lever 7 lands (`gpt-4.1` → `gpt-4.1-mini`),
   the Stage 3 primary row drops 5×, taking total to ~$0.20.
5. Fixture corpus skew: 54% parking + 17% auth/cloudflare/login = 71%
   never enter Stage 2 at all. Production canary ratios (8% legitimate
   business per the audit) would have routed proportionally more
   domains into Stage 2/3 and inflated the per-fixture average; the
   W4.2 number is genuinely lower than a per-domain production
   extrapolation.
6. Stage 3 secondary is off (Lever 1 / PR-C confirmed). Re-enabling
   would roughly double Stage 3 costs.

---

**HEAD at verification:** `5513b4c68be542c01821326a70c40860266fc95b`

**Verify-before-asking identified the following uncertainties:**

- Q3 caveat 1: Stage 2 page-acquisition short-circuit doesn't exist in
  current code. The $0.30 estimate is "LLM tokens only, assuming the
  driver runs"; it is NOT "what a fixture-based W4.2 driver would cost
  end-to-end" because no such driver exists. Operator-side scoping
  should treat this as the LLM-cost ceiling under the assumption that
  engineering work to bypass `FetcherSet` is done separately.
- Q3 token counts are word-count-derived approximations, not
  `tiktoken`-measured. ±25% on per-call cost; ±50% on total feasible
  if cache hit rate is materially below 80%.
