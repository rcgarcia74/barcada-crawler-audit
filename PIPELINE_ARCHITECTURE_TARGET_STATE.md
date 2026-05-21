# Pipeline Architecture — Target State (v1 design-of-record)

**Date:** 2026-05-21 (workspace placement); content is pre-existing
operator-supplied rationale, original authorship date unknown.
**Status:** Design-of-record for UNIMPLEMENTED work. Describes the v1
target state — what the eight Phase 4 PRs are designed to produce — NOT
what current code does.
**Provenance:** Operator-supplied content via chat, no prior workspace
filename. Placed at this path per `RECONCILIATION_2026-05-21.md` §7
item 2 as a durable workspace artifact.

**Important — do NOT use this document as source-of-truth for current
code claims.** Current code is the audit's discovered architecture
(`AUDIT_REPORT.md` §8) modified by four landed Phase 4 PRs (PR-COST,
PR-A, PR-B, PR-C). Lever 2 (Stage 2 classifier nano downgrade), Lever 3
(Stage 2 summarization removal), Lever 4 (parser pre-classifier tier),
and Lever 7 (Stage 3 primary mini downgrade) are NOT applied in current
code. See `phase4_current_state_2026-05-21.md` for source-verified
current state.

This document describes what the pipeline is intended to look like
AFTER Phase 4 PR-D through PR-G land and the levers are applied.

---

## Stage 1: Binary business classification

**Goal:** Determine whether a domain represents a commercial business
(label: `business`) or not (label: `non-business`).

**Architecture:** Three-tier cascade. A domain enters at Tier 1 and
progressively moves to more expensive tiers only if earlier tiers don't
decide with confidence.

### Tier 1: Rules engine

The parser extracts ~30 boolean and numeric signals from the homepage
during scraping. The rules engine combines these into a `business_score`
and confidence rating. Examples of the signals (from your scraper
Parquet schema):

- `signals_legal_has_terms` / `has_privacy_policy` / `has_cookie_policy`
- `signals_commercial_has_pricing` / `has_cart_checkout` /
  `has_demo_trial`
- `signals_business_identity_has_company_address` / `has_phone_e164` /
  `has_dba` / `has_ein_or_vat`
- `signals_business_presence_has_about_page` / `has_team_page` /
  `has_careers_page`
- `signals_trust_has_company_suffix` / `has_case_studies` /
  `has_testimonials`
- `signals_jsonld_has_organization_schema` / `has_localbusiness_schema`
  / `has_product_schema`
- `signals_noncommercial_has_nonprofit_keyword` /
  `has_donate_unambiguous` / `has_blog_indicators`
- 20+ others

These signals roll up into a `business_score` (numeric) and `confidence`
(high/low). Per our prior discussion, ~85-90% of domains get a
high-confidence call from rules alone, ~10-15% are low-confidence and
need further classification.

**Decision rule at Tier 1:**

- `confidence: high` → accept Tier 1's call (business or non-business),
  no further classification
- `confidence: low` → escalate to Tier 2

### Tier 2: Logistic Regression with embeddings

For low-confidence domains, run a trained LR model that takes:

- ~15 parser features (the booleans and numerics from Tier 1)
- Plus an embedding of the domain's `ml_text` field via
  `text-embedding-3-small` (1536 dimensions)

Combined feature vector: ~1,551 dimensions. LR is trained on labeled
data (your eval set) and outputs a probability of being a business.

**Decision rule at Tier 2:**

- LR probability ≥ 0.65 → confident business
- LR probability ≤ 0.40 → confident non-business
- LR probability in [0.40, 0.65] → uncertain, escalate to Tier 3

This means roughly 5% of total traffic (the LR uncertainty band of the
original 10-15% Tier 1 low-confidence) hits Tier 3.

### Tier 3: LLM adjudication (gpt-4.1-nano)

For the ~5% genuinely ambiguous cases, send to `gpt-4.1-nano` with a
structured prompt asking "is this a business?" The LLM returns a binary
call with reasoning.

**Why gpt-4.1-nano:** cheapest LLM. The cascade is designed so the
expensive LLM only runs on hard cases. Per the cost projections, this
is ~$42 for all 15M Tier 3 calls across the corpus.

**Cost cascade for Stage 1 at 50M domain scale:**

- Tier 1 (rules): essentially free, runs on all 50M
- Tier 2 (LR + embeddings): ~$38 one-time for embeddings on 5-7.5M
  low-confidence domains
- Tier 3 (LLM): ~$42 on the ~750K final ambiguous cases

**Total Stage 1 cost:** ~$80. The whole pipeline is engineered around
having rules catch 85%+ to avoid sending everything to expensive LLMs.

---

## Stage 2: Technology sub-category classification

**Goal:** For domains where Stage 1 = business, determine
`is_technology=true|false`. For Tech businesses, assign one of the 23
sub-categories (Cybersecurity, Cloud Infrastructure & Services, AI/ML,
etc.).

**Architecture:** Two-pass LLM-driven. Originally a three-pass design
(with summarization), but Lever 3 dropped Pass 1.

### Pass 1 (REMOVED per Lever 3): Summarization

Original design called for `gpt-4.1-mini` to first summarize each
domain's parser output into a structured summary. This was the most
expensive part of the original cost projection (~$19,152 of the $35K
total).

Lever 3 dropped this. The classifier now reads parser output directly
without a summarization preprocessing step. Saves $10-15K. Validated on
50 domains during cost reduction phase.

### Pass 2 (current): Classification

A single LLM call to `gpt-4.1-mini` (originally) or `gpt-4.1-nano` (per
Lever 2's potential downgrade) that takes:

- Parser-extracted features: `title`, `meta description`, `homepage_text`,
  `ml_text` (truncated)
- Structured signals: navigation, products, services, partners list from
  parser
- The 23-category taxonomy embedded in the system prompt
- Boundary case rules for the 7 canonical disambiguation pairs

The LLM returns:

- `is_technology` (boolean)
- `primary_subcategory` (one of 23, or null if not Tech)
- `confidence` (high/medium/low)
- Reasoning (logged but not stored in output)

### Why no rules engine at Stage 2

Unlike Stage 1, Stage 2 doesn't have a rules-engine first tier. Reasons:

1. **23-way classification is too granular for rules.** Distinguishing
   "Observability" from "Data Infrastructure" requires nuanced semantic
   understanding — keyword presence doesn't suffice.
2. **Boundary cases dominate.** The 7 canonical disambiguation pairs
   (Cybersecurity vs Cloud Infra, SIEM vs APM, etc.) require contextual
   judgment that rules can't easily encode.
3. **LLM accuracy is acceptable.** `gpt-4.1-mini` hitting 85-90% on
   Stage 2 is good enough; rules would max out at 50-60% accuracy at
   23-way classification.

### Stage 2 cost

Per the cost validation work:

- Original baseline (with summarization): $19,152 (summarization) +
  $5,496 (classification) = $24,648
- After Lever 3 (no summarization): $5,496 → potentially $3,000-5,000
  with prompt caching
- After Lever 2 (`gpt-4.1-nano` for classification): $1,500-2,500

**Combined:** Stage 2 at ~$3,000-5,000 in the final cost projection,
down from $24,648 baseline.

### Stage 2 cost ceiling and fetch budget

Stage 2 has a per-shard `--stage2-budget-usd` flag for fetch budget
(bandwidth tracker halts at 0.95× of budget). This catches runaway
scraping costs separately from LLM costs.

---

## Stage 3: Partner-type classification

**Goal:** For domains where Stage 2 = `is_technology=true`, determine
which of 17 partner types they are (Distributor, Technology Partner,
ISV, System Integrator, etc.).

**Architecture:** Two-pass LLM-driven, with Pass 2b feature-flagged off
for v1.

### Pass 1: Evidence gathering

Single LLM call to `gpt-4.1-mini` that extracts partner-type evidence
from the domain's parser output:

- Looks for partner program signals (Partner Portal, Partner Login,
  Become a Partner)
- Identifies revenue model indicators (license vs. services vs. referral
  commissions)
- Detects deployment vs. development vs. reselling signals
- Extracts the partner ecosystem the domain participates in
- Outputs a structured evidence summary

The evidence summary feeds Pass 2.

### Pass 2a: Primary partner type classification

Single LLM call to `gpt-4.1` (or `gpt-4.1-mini` per Lever 7) that takes:

- The evidence summary from Pass 1
- The 17-partner-type taxonomy
- Boundary case rules (Distributor vs Reseller vs Wholesaler, SI vs
  Implementation Specialist vs Consultant, etc.)
- Parser-extracted partner signals

Returns:

- `primary_partner_type` (one of 17)
- `industry` (must match Stage 2's `primary_subcategory` exactly)
- `confidence` (high/medium/low)
- Reasoning (logged)

### Pass 2b (DISABLED per Lever 1): Secondary partner types multi-label

The original design called for a third pass that identified additional
partner type associations beyond the primary. Accenture might be
primarily System Integrator with secondaries Consultants & Advisors and
Implementation Specialist.

Lever 1 disabled this for v1. Two reasons:

1. Cost savings of ~$5,238
2. Adds complexity to evaluation; Pass 2a primary type captures the
   dominant partner identity

Pass 2b returns when v1.1 launches. The eval data schema retains
`secondary_partner_types` as an optional empty array for v1 to allow
forward-compatible evolution.

### Stage 3 cost reductions

- Original baseline: Pass 1 ($1,866) + Pass 2a `gpt-4.1` ($3,404) +
  Pass 2b ($5,238) = $10,508
- After Lever 1 (no Pass 2b): $5,270
- After Lever 4 (cap LLM to high-confidence band): $3,500-4,000
- After Lever 7 (Pass 2a downgrade to `gpt-4.1-mini`): $2,500-3,000

**Stage 3 at ~$2,500-3,000 in the final projection.**

### Stage 3 cost ceiling and budget

Like Stage 2, Stage 3 has a per-shard `--stage3-budget-usd` flag for
fetch budget. Also has `--no-stage3-secondary-enabled` to control Pass
2b (default off for v1).

---

## The cascade economics

The three stages form a funnel that narrows the universe at each step:

```
Stage 1: 50M domains in
         ↓ (rules-driven for 85-90%, LR for 10%, LLM for 5%)
         ~15M businesses out

Stage 2: 15M businesses in
         ↓ (single LLM call per domain)
         ~1.5M Technology businesses out

Stage 3: 1.5M Technology businesses in
         ↓ (Pass 1 evidence + Pass 2a classification)
         ~1.5M with partner types (most Tech businesses get a partner type)
```

The pipeline is intentionally designed so cheap operations (rules) run
on everything, expensive operations (LLM Pass 2a at `gpt-4.1`) run on
the narrowest subset.

## Total pipeline cost projection

After all six cost reduction levers:

| Stage | Cost | What happens |
|---|---|---|
| Stage 1 | ~$80 | Rules + LR + nano LLM cascade across 50M domains |
| Stage 2 | ~$3,000-5,000 | Single LLM call per business |
| Stage 3 | ~$2,500-3,000 | Two-pass LLM on Tech businesses |
| Embeddings (one-time) | ~$38 | `text-embedding-3-small` for LR features |
| Parser costs (out of scope here) | ~$2,000-3,000 | Scraping, bot mitigation proxies |
| **Total pipeline** | **~$7,500-11,000** | All-in for 50M domain corpus |

This is down from the original projection of ~$35K LLM cost.

---

## Architectural decisions specific to each stage

### Stage 1: Why a cascade

The cascade exists because:

- 85% of domains are obvious (clearly business or clearly not — parked,
  blogs, .gov)
- LLM at 50M scale is prohibitively expensive without filtering
- LR with embeddings is much cheaper than LLM but more accurate than
  rules alone
- The combination achieves rules-engine accuracy on easy cases and LLM
  accuracy on hard cases at a fraction of the cost

### Stage 2: Why single-pass LLM

The 23-category taxonomy doesn't lend itself to cascade because:

- Rules can't reliably distinguish 23 categories (vs. 2 at Stage 1)
- LR at 23-way classification needs much more training data than you
  can practically produce
- LLM accuracy at 85-90% is adequate for the use case
- Single-pass is cheaper than multi-pass when you don't need ensembling

### Stage 3: Why two-pass

Partner type classification is harder than industry classification
because:

- Partner type signals are often in specific page sections (Partners
  page, Partner Portal, footer)
- Evidence is fragmented (some on homepage, some on partner-program
  pages)
- Multiple partner types can apply (the Pass 2b problem, deferred to
  v1.1)

The Pass 1 evidence extraction structures the disorder before Pass 2a
makes the call. This gives better accuracy than single-pass on the same
model.

---

## What the eval data validates

For each stage, the eval data evaluates a specific thing:

**Stage 1 eval validates:**

- The cascade as a whole (does the final business/non-business call
  match the ground truth label?)
- Tier 1 rules accuracy in isolation (analyzed via cascade metadata
  showing which tier decided)
- Tier 2 LR accuracy on the uncertainty band
- Tier 3 LLM adjudication accuracy

The pipeline outputs a `classification_path` field telling you which
tier decided — useful for measuring tier-specific accuracy.

**Stage 2 eval validates:**

- `is_technology=true|false` precision (binary call)
- `primary_subcategory` accuracy across the 23 categories
- Boundary case handling (the 7 disambiguation pairs)

**Stage 3 eval validates:**

- `primary_partner_type` accuracy across 17 partner types
- `industry` field consistency with Stage 2
- Boundary case handling (Distributor/Reseller/Wholesaler triangle,
  SI/IS/Consultant triangle)

The eval framework computes accuracy per stage and per tier (for Stage
1), with confusion matrices for Stage 2 and Stage 3.

---

## What's NOT in the pipeline that you might have expected

A few things worth noting are deliberately excluded:

**No human-in-the-loop fallback at runtime.** When the LLM is uncertain,
it abstains (mark as `cost_ceiling_skipped` or similar) rather than
asking a human. Customers can correct labels post-classification, but
it's not blocking.

**No fine-tuned models.** All LLMs are base Azure OpenAI deployments. No
custom fine-tuning for partner classification. Reason: cost and
complexity outweigh accuracy gains for v1.

**No multi-language handling at the LLM level.** Stage 2 and Stage 3
prompts assume English. Non-English content gets passed to the LLM raw
— the LLM handles translation implicitly. Per your decision, eval
labels are English-only with `confidence: low` for non-English sites
that are ambiguous.

**No real-time updates.** The pipeline runs in batch mode against a
snapshot of the corpus. Domains don't get re-classified continuously.
The customer-facing app shows snapshot data with timestamps.

---

## Where the design might shift in v1.1

Based on what we discussed during cost reduction:

**Stage 2:** Pass 1 summarization might come back if accuracy on
long-form Tech sites suffers without it. Currently dropped (Lever 3),
but it's a candidate to restore if eval shows quality regression.

**Stage 3:** Pass 2b (secondary partner types) returns in v1.1. The
schema already accommodates this with optional `secondary_partner_types`
field.

**Stage 1:** LR threshold tuning. Currently [0.40, 0.65] for LLM
dispatch. If LLM costs are higher than projected, raise the band. If
accuracy suffers, widen it.

**Embeddings:** Possible swap from `text-embedding-3-small` to MiniLM
(self-hosted) for cost reduction. Architecture supports this via
`embeddings/model=*/` partition in ADLS.
