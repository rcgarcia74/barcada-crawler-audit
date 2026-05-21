# Stage 3 Input Shape Verification

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

## Q1 — Stage 3 input source

**Stage 3 consumes THREE separate inputs at startup, plus its own
freshly-fetched pages.**

The three inputs read at the top of `run_shard`:

| Input | Path arg | Read at | Shape |
|---|---|---|---|
| Stage 2 predictions (Hive-partitioned by `is_technology`) | `stage2_predictions_path` | `stage3/run.py:177` via `_read_stage2_partition` | `pyarrow.dataset.HivePartitioning(is_technology=bool)` if dir; falls back to `pl.read_parquet(path)` if file. Reader at `run.py:376-405`. |
| Stage 2 summaries cache (CompanyDescription parquet) | `stage2_summaries_path` | `stage3/run.py:178` via `read_summaries(...)` | Stage 2 summarizer-pass cache (the `descriptions: dict[str, CompanyDescription]` dict). Passed into both `summarize_evidence_shard` (line 261) and `classify_domains` (line 303). |
| Stage 3 evidence cache | `evidence_cache_path` | `stage3/run.py:274` via `read_evidence(...)` | Parquet cache of prior Pass-1 results (content-hash keyed, per `evidence_summarizer.py:80-105`). |

A fourth input — the parser parquet for `bot_blocked` partition routing
— is mentioned in the docstring (`run.py:25`) but is NOT actually read in
the PR-A scaffold. `_initial_tier_for_stage3(_row)` at `run.py:408-416`
is hard-coded to return `T1` unconditionally with comment "PR-B will
swap this to consult the parser's bot_blocked column". So parser parquet
is plan-staged but not consumed at HEAD.

The Hive partitioning explicitly handles both `is_technology=true`
(eligible) and `is_technology=false` (carry-through as
`upstream_abstained`) so the cumulative output is one row per Stage 2
input.

## Q2 — Outbound HTTP from Stage 3

**(b) Stage 3 triggers additional outbound HTTP fetches.** It is NOT
extract-from-already-fetched-pages.

For every `is_technology=true` eligible domain, Stage 3 fetches the T3
path list — 4 pages per domain — via `_acquire_pages_stage3` at
`stage3/run.py:210` and `_acquire_for_domain_t3` at `run.py:468-504`.
Page-acquisition runs BEFORE Pass 1 evidence summarization and writes
its own `pages_output_path` parquet (`run.py:227`).

The T3 path list (from `page_acquisition/path_lists.py:107-118`):

```
products    /products, /product, /platform
solutions   /solutions, /solution, /use-cases
customers   /customers, /case-studies, /clients
industries  /industries, /industries-served, /industry, /markets
```

Citations of HTTP-fetching code Stage 3 invokes:

- `stage3/run.py:74` `from ...page_acquisition.fetcher_core import FetchResult`
- `stage3/run.py:113` `FetcherSet = stage2_run.FetcherSet` (Stage 2
  type reused)
- `stage3/run.py:210` `await _acquire_pages_stage3(...)`
- `stage3/run.py:490` `await try_fallback_paths(domain, page_name,
  fallback_paths, fetcher, ...)` — the actual fetch invocation per page.

The URL list per domain is the static `T3_PAGE_PATHS` dict — NOT derived
dynamically from homepage signals. Stage 3 doesn't look for a "Become a
Partner" link on the homepage; it just attempts the four canonical slug
families above with fallback variants, then routes the resulting HTML
into the evidence-summarizer prompt's `[products]` / `[solutions]` /
`[customers]` / `[industries]` slots (verified in
`stage3/llm_prompts.py:327-351` `EVIDENCE_USER_TEMPLATE`).

## Q3 — Stage 3 fetcher wiring

**Stage 3 reuses Stage 2's `FetcherSet` type and the same per-domain
T1/T2/T3 tier abstractions.**

Citation: `stage3/run.py:111-113`:

```python
# Reuse Stage 2's FetcherSet; the tier abstractions are identical
# across Stage 2 and Stage 3.
FetcherSet = stage2_run.FetcherSet
```

The fetchers: `FetcherSet` parameter is passed into `run_shard` at line
149. The CLI instantiates the `FetcherSet` (one instance shared with
Stage 2 conceptually — though each stage's CLI dispatch builds its own
when invoked separately) and hands it in.

**Important for adapter scoping:** because Stage 3 reuses Stage 2's
`FetcherSet` type and tier abstractions but instantiates the fetchers
fresh per CLI invocation, a bypass that swaps `FetcherSet` for a
fixture-backed equivalent would need to apply at both stages
independently — though the same adapter shape would work for both. The
`fetcher_core` / fetchers protocol is the natural seam.

Per-stage cost-tracking flag is present: `cli.py:273-278`
`--stage3-budget-usd` default `2500.0` (Stage 2 has
`--stage2-budget-usd` with same default at `cli.py:240`). These feed
the `BandwidthTracker`, not the LLM `cost_tracker`.

## Q4 — Minimum fixture-input adapter shape

Stage 3's input contract has four surfaces. From a single fixture HTML
file, an adapter would need to produce:

1. **`stage2_predictions/is_technology={true,false}/`** Hive-partitioned
   parquet with at minimum the columns Stage 3 reads at `run.py:177`,
   `403-404`: `domain`, `is_technology` (bool), `abstain` (bool),
   `crawl_timestamp` (string), plus whatever downstream rows use (the
   eligible-row reader at `run.py:197` does `row["domain"]`;
   `_emit_upstream_abstained` at `_emit_upstream_abstained(...)` reads
   more columns from the carry-through partition — full column list per
   `stage2/output_schema.py:97-167`).

2. **`stage2_summaries/.../summaries.parquet`** with a
   `CompanyDescription`-shaped row per domain (the parquet schema is
   whatever `stage2.summarizer.read_summaries` consumes). The evidence
   prompt's `{company_description}` and `{primary_activity}` slots
   (`stage3/llm_prompts.py:330-334`) come from this; without it, the
   Pass-1 prompt has empty fields.

3. **Stage 3 fetched pages for the four T3 slugs** (`/products`,
   `/solutions`, `/customers`, `/industries`). Either:
   - Adapter pre-populates `pages_output_path` and Stage 3 reads from
     there (no such read path exists — Stage 3 writes `pages.parquet`
     after fetching, doesn't read pre-staged pages), OR
   - The `FetcherSet` itself is mocked at the `fetcher_core` seam to
     return fixture HTML for any T3-path URL.

4. **`evidence_cache_path`** can be missing (cache-miss path is the
   normal flow) or pre-populated (cache-hit path skips Pass 1 LLM).

**Sub-option (i) doesn't cleanly apply.** Sub-option (i) was "run Stage
2 end-to-end against fixtures, then run Stage 3 against Stage 2's
output." Running Stage 2 against fixtures requires:

- A Stage 2 `FetcherSet` bypass (the prior verification confirmed none
  exists), AND
- A Stage 1 parser-parquet input (Stage 1 doesn't fetch but consumes
  `parser_output` Parquet, which requires running the parser against
  fixture HTML — also engineering work).

So Sub-option (i) is "bypass at Stage 2 fetcher level plus
parser-output Parquet construction from fixture HTML." The "single
bypass at Stage 2's input level" framing in the prompt is correct only
if the parser-output-shape adapter is treated as part of the Stage 2
bypass.

**Sub-option (ii) is cleaner for Stage 3 specifically.** Synthesize:

- A `stage2_predictions` row stub per fixture (every fixture →
  `is_technology=true`, `abstain=false`; or per category mapping per
  `generate_meta_json.py:175-186` `CATEGORY_TECH` — `saas` for
  `legitimate_business` / `mega_menu` / `spa_*`; `nonprofit` for
  `legitimate_nonprofit`; etc.).
- A `stage2_summaries` row stub per fixture with a minimal
  `CompanyDescription` (could be parser-derived heuristically or
  stubbed to empty/sentinel values).
- A `FetcherSet` mock that returns the fixture HTML for ANY URL
  (every `/products`, `/solutions`, `/customers`, `/industries`
  request returns the same fixture HTML).

That third piece is genuinely the only fetcher hook needed — but it's
a runtime mock, not a parquet-stage. Sub-option (ii) effectively
becomes: "synthesize Stage 2 outputs + mock the `FetcherSet`."

**Columns hard or impossible to synthesize from fixture HTML alone:**

- `crawl_timestamp` (string) — synthesizable as a sentinel
  (`"1970-01-01T00:00:00Z"`).
- `model_version` (carries forward from Stage 2 predictions) —
  synthesizable as sentinel.
- Stage 2's `top_3_category` and confidences feeding
  `is_technology=true` decisions — synthesizable per category mapping
  (`legitimate_business` → `saas`, etc.) but the decision is
  fabricated, not pipeline-derived. **This means W4.2 expected outputs
  would carry a fabricated Stage 2 decision even before reaching
  Stage 3 — distinct from the Flag-1 Stage-3 sentinel, and a new
  question for operator-side scoping.**
- Page-fetch metadata (`http_status`, `response_size_bytes`, fetch
  latency, `error_kind`) — synthesizable as `200` / `len(html)` / `0`
  / `none`, but tier promotion logic (`PromotionTracker`) reacts to
  `error_kind` in `PROTECTION_ERROR_KINDS` (`run.py:500-503`); a
  fixture run never triggers protection-error promotion, so T2/T3
  escalation paths would be untested in W4.2 expected outputs.

## Q5 — Existing bypass mechanisms

**Does not exist.** Stage 3 has no `--no-fetch`, `--test-mode`,
`--input-parquet`, `--from-fixture`, or equivalent CLI flag.

Verified by grep across `src/barcada_scraper/classifier/cli.py`: the
only Stage-3-specific argparse entries are:

- `--evidence-deployment` (`cli.py:246-249`)
- `--primary-deployment` (`cli.py:251-257`)
- `--secondary-deployment` (`cli.py:259-266`)
- `--stage3-thresholds` (`cli.py:268-272`)
- `--stage3-budget-usd` (`cli.py:274-278`) — fetch-bandwidth cap, not
  a fetch bypass
- `--stage3-secondary-enabled` (`cli.py:280-290`) — Pass 2b gate per
  PR-C, unrelated to fetching

Same conclusion as the prior Stage 2 verification: the bypass for
fixture-based W4.2 generation is engineering work, not a configuration
toggle. Stage 3 is, if anything, more demanding than Stage 2 because
of the additional upstream-output dependencies (Stage 2 predictions
partition + Stage 2 summaries cache), not just the page-acquisition
bypass.

## Out-of-scope observations

1. **Pass 2b semantic at PR-A scaffold:** `stage3/run.py:32-33`
   docstring says "PR-A always runs it when a secondary adjudicator
   is supplied, None skips it." This is the PR-A baseline; the PR-C
   gate (`stage3_secondary_enabled` config flag +
   `--stage3-secondary-enabled` CLI flag) was added later and is
   consulted at `cli.py:1012-1019` to decide whether to construct the
   secondary adjudicator. So Pass 2b is properly off by default at
   HEAD; not contradicted by the docstring.

2. **Stage 3 reads Stage 2 summaries even for `is_technology=false`
   rows** — `read_summaries(...)` at line 178 loads the full cache
   regardless of partition. This is irrelevant for fixture-input
   adapter shape but worth noting: the summaries cache must cover
   every domain that appears in `stage2_predictions`, not just the
   `is_technology=true` subset, if a future adapter wants per-fixture
   full carry-through behavior. The carry-through emitter
   (`_emit_upstream_abstained` at `run.py:181`) does not look up the
   description, though; the cache load is harmless for the
   carry-through rows.

3. **`pages.parquet` schema** lives at
   `page_acquisition/page_schema.py` (imported at
   `stage3/run.py:76-81`, not read for this audit but cited because
   any adapter that pre-populates pages would need to conform to its
   schema).

---

**HEAD at verification:** `5513b4c68be542c01821326a70c40860266fc95b`

**Verify-before-asking identified the following uncertainties:**

- Q4 Sub-option (i) characterization: I treat Stage 1 parser-output
  Parquet construction as part of "the Stage 2 bypass" rather than a
  third independent surface. An operator scoping the adapter may want
  to call this out as a distinct surface — parser-output Parquet shape
  is its own input contract and was not part of this Q1-Q5 scope.
- Stage 2 summaries cache shape: I cite `read_summaries(...)` but did
  not read its parquet schema this session. If adapter scoping needs
  the exact column list, that's a separate read of
  `stage2/summarizer.py`.
