# Classification-Adjacent Remediation Plan

**Status:** Draft for AI/ML team review
**Generated:** May 2026
**Owner:** Crawler engineering (proposing); AI/ML team (reviewing scope and approach)
**Source documents:** `AUDIT_REPORT.md`, `FIXTURE_AUDIT_REPORT.md`, `BARCADA_CRAWLER_REMEDIATION_PLAN.md`

---

## Purpose of This Document

The full crawler remediation plan covers six workstreams of changes to barcada-scraper. Some of those changes are purely extraction/parsing work (no contact with classification logic). Others touch classification code, classification schemas, or classification inputs/outputs in some way.

This document extracts only the **classification-adjacent items** and presents them for AI/ML team review before any implementation begins. The crawler engineering side will not proceed with these items without sign-off on:

1. Whether each item is in scope for AI/ML team ownership, crawler team ownership, or joint work
2. Whether the proposed approach is acceptable from an ML/data-science perspective
3. Whether the proposed schema changes are compatible with existing models and training pipelines
4. Whether the proposed input changes (e.g., PII redaction before classifier) could affect classification quality

The purely extraction items proceed independently and are not covered here.

---

## How Items Are Classified for Scope

For each item below, the level of classification-adjacency is rated:

- **Reads classifier outputs** — Consumes Stage 1/2/3 outputs without modifying classifier logic or schema. Lowest impact.
- **Annotates classifier outputs** — Adds metadata fields to records emitted by the classifier. Schema-additive, no logic change.
- **Filters classifier outputs** — Suppresses or modifies records based on policy. Output-modifying.
- **Modifies classifier inputs** — Changes what data the classifier sees (e.g., redaction before LLM call). Highest impact on classification quality.
- **Gates on classifier metrics** — Establishes pass/fail thresholds for classifier performance. Affects deployment workflow.
- **Monitors classifier behavior** — Observability over time. Read-only from classifier perspective.

---

## Item 1: Cost-Per-Useful-Record Metric

**Classification adjacency:** Reads classifier outputs

**What it does:**

Currently `phase_summary.py` aggregates `domains_processed` and `total_cost_usd` per phase but doesn't compute a cost-per-useful-record KPI. The proposed change reads Stage 1 output (`is_business` boolean) from the existing Parquet output and adds two new aggregate fields to `PhaseSummary`:

```python
useful_records_count: int
cost_per_useful_record: float
```

**Why it matters for the crawler:**

This is the primary cost-efficiency KPI the remediation plan uses to evaluate whether changes improve or degrade cost discipline. Without it, "did this change make us more efficient?" is unanswerable.

**Decision needed from AI/ML team:**

1. **Definition of "useful record":** The current proposal counts `is_business == True` as useful. Other reasonable definitions:
   - `is_business is not None` (decided, regardless of business=true/false — counts both positive and negative classifications as useful)
   - `is_business == True AND business_score > some_threshold` (counts only high-confidence positives)
   - Stage-2-or-3-classified records (deeper-pipeline-useful)

   Which definition is most aligned with what your team views as production value?

2. **Handling of abstentions:** `is_business` is `nullable=True` (null on abstain). Should abstentions count in the denominator (treating them as cost-incurred-but-no-output) or be excluded? This is partly a cost-attribution question and partly a "what does success look like" question.

3. **Per-stage breakdown:** Useful to also have `cost_per_useful_record_stage1`, `_stage2`, `_stage3` separately, or is the aggregate sufficient?

**Implementation surface:**

- `phase_summary.py` (crawler-owned): adds aggregation logic
- `cost_journal.py` (crawler-owned): no changes
- Stage 1 output schema (AI/ML-owned): no changes proposed
- New consumer-side metric, no producer-side changes

**Effort estimate:** ~50 LOC

---

## Item 2: Efficiency-Flag Catalog (Partial Classifier Touch)

**Classification adjacency:** Annotates classifier outputs (for the flags emitted at classifier points)

**What it does:**

Adds an enum of named efficiency flags emitted per record where applicable. Most flags are at the fetch/render stage (`RENDERED_WITHOUT_HYDRATION_ATTEMPT`, `TIER_OVER_ESCALATION`), but three involve the classifier:

- `LLM_OVERUSE` — emitted when the LLM tier was used and a deterministic tier could have handled the record (judgment call based on rule/LR coverage)
- `CACHE_MISS_RATE_HIGH` — emitted when prompt cache hit rate for a record's LLM calls is below threshold
- `LOW_USEFUL_RECORD_RATE` — emitted at shard level when the useful-record rate drops below threshold

**Why it matters for the crawler:**

Diagnostic clarity. Turns ad-hoc cost analysis into structured signals that can be aggregated and dashboarded.

**Decision needed from AI/ML team:**

1. **LLM_OVERUSE definition:** When can we say "the LLM tier was used unnecessarily"? Reasonable definitions:
   - Stage 1: `LLM_OVERUSE` if LR score was within X of business_max or non_business_min threshold (i.e., LR was actually confident and LLM was redundant)
   - Stage 2/3: similar threshold-based logic on LR or rule confidence

   These thresholds need ML team input — what's the false-positive rate of an LLM_OVERUSE flag at various thresholds?

2. **Where to emit flags:** Two options:
   - At the classifier itself (each stage emits its own efficiency flags). Cleaner attribution but requires changes to classifier code.
   - At a post-classifier consumer that reads outputs and computes flags. Decouples flagging from classification but is less expressive.

3. **Should `LLM_OVERUSE` block re-runs?** Or is it diagnostic only? A noisy flag is fine if it's just observed; a flag that gates retraining or production policy needs higher precision.

**Implementation surface:**

- New `efficiency_flags.py` (crawler-owned)
- Tagging points in classifier code (AI/ML-owned if option 1)
- Aggregation in `phase_summary.py` (crawler-owned)

**Effort estimate:** ~150 LOC, of which ~50 touches classifier code

**Possible scope split:** AI/ML team can own LLM-related flag emission while crawler team owns the catalog, taxonomy, and non-LLM flags.

---

## Item 3: PII Detection and Redaction

**Classification adjacency:** Modifies classifier inputs (highest impact)

**What it does:**

Adds PII detection (via `presidio-analyzer` or curated regex) over extracted text. Detected PII is either flagged in a `pii_findings` field or redacted from the text before it reaches the classifier, depending on `regional_policy.json` rules.

**Why it matters for the crawler:**

Compliance with GDPR, CCPA, LGPD, PIPL. Currently no PII handling exists; this is a real legal risk as the crawler scales to international or customer-facing deployment.

**Why this needs AI/ML team review:**

**Modifying classifier input is a classification-quality change, even if the classifier code isn't touched.** Specifically:

- Redacted PII may remove signal the classifier uses (e.g., contact info indicates a real business; redacting `support@example.com` may change classification confidence)
- Redaction tokens (`[EMAIL_REDACTED]`, `[PHONE_REDACTED]`) introduce new tokens the classifier hasn't seen in training
- Different regional policies may produce different redacted text for the same domain, potentially producing different classifications

**Decisions needed from AI/ML team:**

1. **Redaction vs. flagging:** Should PII be redacted from text before classifier consumption, or only flagged in metadata and left in text? Tradeoffs:
   - Redacting: complies with strict interpretations of GDPR/CCPA but changes classifier inputs
   - Flagging: preserves classifier inputs but may not satisfy strict compliance

2. **Redaction token strategy:** If we redact, what token format? Options:
   - Specific: `[EMAIL_REDACTED]`, `[PHONE_REDACTED]`, etc.
   - Generic: `[PII_REDACTED]` for all
   - Empty: strip without replacement

   Each affects classifier behavior differently. ML team should evaluate which is least disruptive.

3. **Retraining requirement:** If we redact, do existing classifiers need to be retrained on redacted data? Or can we apply redaction only at inference and accept some degradation?

4. **PII categories in scope:** Presidio detects many categories. Which matter for B2B classification?
   - Email addresses (likely matter — distinguishes real business from parking)
   - Phone numbers (matter)
   - Names (probably don't matter for B2B classification)
   - SSN/credit card (rare in B2B sites; safer to redact aggressively)
   - Addresses (matter for some industries)

5. **Validation strategy:** How do we validate that PII redaction doesn't degrade classification quality? Proposed:
   - Run classifier on labeled eval set with and without redaction
   - Compare F1, per-category recall, confidence distribution
   - Acceptable threshold: <X% F1 degradation (ML team to define X)

**Implementation surface:**

- New `pii_detection.py` (crawler or AI/ML-owned, TBD)
- Integration point in `text_cleaning.py` or `extraction.py` (crawler-owned)
- `regional_policy.json` lookup (crawler-owned)
- Classifier retraining if needed (AI/ML-owned)

**Effort estimate:** ~250 LOC for detection/redaction logic; retraining cost depends on ML team decision

---

## Item 4: Regional Policy Enforcement

**Classification adjacency:** Filters classifier outputs

**What it does:**

Defines per-region (GDPR, CCPA, LGPD, PIPL) rules for which fields can be emitted in classifier output records. Enforced at `parquet_writer` time — records that violate policy for their detected region either have specific fields nulled or are suppressed entirely.

**Why it matters for the crawler:**

Same compliance motivation as Item 3. The regional policy file is the rules-engine; PII redaction (Item 3) is one specific application.

**Decisions needed from AI/ML team:**

1. **Field-level rules:** Which output fields are sensitive in which regions? Examples that ML team should think through:
   - Stage 3 partner-type classification of a Chinese-jurisdiction domain — emit, redact, or suppress?
   - Stage 2 tech category for a German B2B SaaS — emit normally?
   - Per-domain crawl history with timestamps — sensitivity varies by region

2. **Confidence score emission:** Some compliance regimes treat algorithmic decisions about individuals as sensitive even when the decision target is a company. Does `business_score = 0.87` count as algorithmic decision-making?

3. **Reproducibility for legal review:** Some compliance regimes require explainability for emitted decisions. Are classifier outputs sufficiently explainable, or do we need to also emit feature contributions?

**Implementation surface:**

- New `regional_policy.json` (crawler-owned, with AI/ML input on field definitions)
- Enforcement at `parquet_writer` (crawler-owned)
- No changes to classifier code

**Effort estimate:** ~200 LOC + JSON config + legal review (separate)

---

## Item 5: Schema Version Stamping

**Classification adjacency:** Annotates classifier outputs (schema-additive)

**What it does:**

Adds three new version fields alongside the existing `feature_schema_version`:

```python
crawler_version: int        # version of crawler code
policy_version: int         # version of CRAWLING_POLICY.md / regional_policy.json
taxonomy_version: int       # version of classification taxonomy (Stage 2, Stage 3)
```

Stamped on every emitted record. Bumped explicitly on relevant changes.

**Why it matters for the crawler:**

Reproducibility and compliance. When a downstream consumer asks "what version of policy was in effect when this record was emitted?", today there's no answer. Also enables train/serve mismatch detection if/when the deferred `_load_training_data` work happens.

**Decisions needed from AI/ML team:**

1. **`taxonomy_version` ownership:** Bumped when? The taxonomy is in `configs/partner_type_definitions.yaml` and `configs/stage2_thresholds.yaml`. Reasonable bump triggers:
   - Adding/removing/renaming categories
   - Material threshold changes
   - Definitional changes to existing categories

   ML team should own when this bumps.

2. **Coupling with `feature_schema_version`:** Today `feature_schema_version` is bumped by parser changes. Should `taxonomy_version` bumps also force `feature_schema_version` bumps (or vice versa)? Or are they independent?

3. **Version compatibility matrix:** Eventually we'll need a matrix of which `taxonomy_version` is compatible with which `feature_schema_version`. ML team should drive this.

**Implementation surface:**

- New constants in respective config/code files
- Stamping logic at emit points (Stage 1/2/3 `run.py` files — AI/ML-owned)
- Schema additions to output schemas (joint)

**Effort estimate:** ~50 LOC, mostly schema definitions

---

## Item 6: Acceptance Metric Formula

**Classification adjacency:** Gates on classifier metrics

**What it does:**

Writes `eval/acceptance_criteria.yaml` with explicit thresholds for classifier metrics:

```yaml
stage1:
  f1_min: 0.92
  per_intent_recall_min: 0.85
stage2:
  category_f1_min: 0.80
  abstention_rate_max: 0.15
stage3:
  primary_partner_f1_min: 0.75
```

Read in `metrics.py compare` and exit non-zero on threshold violation. Becomes a CI gate.

**Why it matters for the crawler:**

Today thresholds are documented in `configs/stage*_thresholds.yaml` but aren't gated. A regression in Stage 1 F1 from 0.92 to 0.85 would be detected only on manual inspection. Gating turns regressions into actionable failures.

**Decisions needed from AI/ML team (these are entirely their call):**

1. **What thresholds to set:** This is a model-quality decision. Setting them too tight produces false alarms; too loose lets regressions through.

2. **Which metrics to gate on:** F1 is one option; per-class recall, abstention rate, calibration error, and others may matter. ML team should pick.

3. **Severity levels:** Should there be a "warn" threshold (degraded but acceptable) vs. "fail" threshold (block merge)? Or single-level gates?

4. **Per-locale or per-industry stratification:** A single global F1 can mask regressions in specific segments. Worth stratifying?

**Implementation surface:**

- New `eval/acceptance_criteria.yaml` (joint)
- Logic in `metrics.py compare` (joint)
- CI workflow modification (crawler-owned)

**Effort estimate:** ~60 LOC + threshold definitions

---

## Item 7: CI Regression Gate

**Classification adjacency:** Gates on classifier metrics

**What it does:**

Extends `.github/workflows/python-package.yml` to run `barcada-baseline check` and `metrics.py compare` against a baseline, failing the build if regressions exceed defined thresholds.

This depends on Item 6 (acceptance criteria) being defined.

**Why it matters for the crawler:**

Prevents quality drift between commits. Without it, a change that degrades classifier performance can merge silently.

**Decisions needed from AI/ML team:**

1. **Baseline reference:** What baseline does the gate compare against? Options:
   - Most recent tagged release
   - A frozen "production baseline" updated on a schedule
   - Per-PR comparison to the merge-base

2. **Failure mode:** Hard fail (block merge), or soft fail (require explicit override)? Soft fail with required approval from an AI/ML reviewer is common for ML-impacting PRs.

3. **Eval set used for the gate:** The same eval set used for development, or a held-out set? Held-out is more robust but requires labeling discipline.

**Implementation surface:**

- CI workflow update (crawler-owned)
- Baseline storage convention (joint)
- Override workflow (joint)

**Effort estimate:** 1 day setup

---

## Item 8: Drift Detection Daemon

**Classification adjacency:** Monitors classifier behavior

**What it does:**

Schedules nightly re-crawls of `canary_50_domains.txt` (currently unused). For each canary domain, computes per-record agreement with the last baseline run. Alerts on regression > threshold.

**Why it matters for the crawler:**

Catches drift in production that fixture-based tests don't surface. A site redesigning, an anti-bot defense changing, or a classifier behavior shift in deployment all show up here first.

**Decisions needed from AI/ML team:**

1. **Drift metric definition:** Per-domain agreement is one option. Others:
   - Score-distribution shift (KS test on `business_score`)
   - Calibration drift (Brier score vs. baseline)
   - Per-category prediction-rate shift

   Which is most actionable for the team?

2. **Alert threshold:** What level of drift triggers investigation vs. accepted variance?

3. **Canary curation:** Are the 50 canary domains representative? Should the canary set be refreshed periodically, or kept stable for trend continuity?

4. **Action on drift:** What's the response? Re-eval, retraining trigger, manual investigation?

**Implementation surface:**

- New `barcada-drift` CLI (crawler-owned)
- Scheduling via cron or Azure Timer Trigger (crawler-owned)
- Alert wiring (joint)
- Trend dashboard (joint)

**Effort estimate:** ~300 LOC

---

## Cross-Cutting Question: Train/Serve Mismatch Gate

The original audit's anti-patterns section flagged that `lr_train._load_training_data` is a `NotImplementedError` per `DEFERRED_WORK.md`. The `feature_schema_version` exists but the train/serve compatibility gate it enables is not enforced.

This is **AI/ML team territory** — the gate would check at training time that the training data's `feature_schema_version` matches the production schema, and refuse to train on incompatible data.

**Decision needed:**

1. Is this on the AI/ML team's roadmap?
2. If yes, when? It would affect Item 5 (version stamping) — the version fields are only fully useful once the gate exists.
3. If no, should the `feature_schema_version` claim be downgraded in `CHANGELOG.md` to reflect that it's currently advisory rather than enforced?

This isn't a crawler-side change but it affects how the crawler reports schema compliance.

---

## Summary Table

| Item | Adjacency Level | Crawler-Owned | AI/ML-Owned | Joint |
|------|----------------|---------------|-------------|-------|
| 1. Cost-per-useful-record | Reads outputs | Aggregation logic | Definition of "useful" | — |
| 2. Efficiency flags | Annotates outputs | Catalog, non-ML flags | LLM-specific flags | Tagging strategy |
| 3. PII detection/redaction | Modifies inputs | Plumbing | Retraining decision, validation | Redaction strategy |
| 4. Regional policy | Filters outputs | Engine, JSON | Sensitive-field definitions | — |
| 5. Version stamping | Annotates outputs | crawler_version, policy_version | taxonomy_version | Schema additions |
| 6. Acceptance metric | Gates on metrics | YAML format, CI integration | All thresholds | — |
| 7. CI regression gate | Gates on metrics | Workflow, infrastructure | — | Baseline strategy, override policy |
| 8. Drift detection | Monitors behavior | Scheduler, infrastructure | Drift metric, alert threshold | Dashboard, action runbook |
| 9. Train/serve gate | (Cross-cutting) | — | All | — |

---

## Proposed Process

The crawler team would like AI/ML team review and decision on the following before implementation:

### Per-item decisions

For each item above, AI/ML team to indicate:

- **IN SCOPE** — proceed as proposed
- **IN SCOPE WITH CHANGES** — proceed but adjust per ML team specification
- **OUT OF SCOPE** — defer or skip entirely
- **NEEDS DEEPER DISCUSSION** — requires meeting before deciding

### Joint working sessions

Where items are marked NEEDS DEEPER DISCUSSION, propose 30-minute working sessions per item with crawler engineering, AI/ML, and (where relevant) legal/compliance.

### Implementation sequencing

Once decisions are made, the crawler team will:

1. Update `BARCADA_CRAWLER_REMEDIATION_PLAN.md` with AI/ML-approved scope
2. Implement crawler-owned and joint items per the agreed sequencing
3. Coordinate with AI/ML team on schema bumps and retraining triggers
4. Validate against baseline-v0 (to be established before any of these items land)

### Documentation

All decisions made in this review should be captured in:

- A `CLASSIFICATION_INTERFACE_DECISIONS.md` under `docs/` in the repo
- Inline comments at the interface points (e.g., where the crawler reads `is_business`)
- Updates to `CHANGELOG.md` when each item ships

---

## Open Questions for AI/ML Team

A few questions that don't fit neatly into individual items but should be addressed:

1. **Is there a training pipeline currently producing models, or are deployed models static for now?** If static, several items (drift detection, train/serve gate) shift priority. If active, the schema concerns are more urgent.

2. **Who owns the labeled eval sets** (`eval_data/stage1_labels.jsonl`, etc.)? The fixture audit found these are being actively updated; need to know if that's AI/ML-team work or operator work.

3. **Are there current cases of classifier degradation in production** that any of these items would help diagnose? If yes, prioritize those.

4. **What's the AI/ML team's read on the `_load_training_data` deferment?** Acceptable indefinitely, or blocking something important?

5. **Are there confidential considerations** (model architectures, training data sources, prompt templates) that would make any item above need to be approached differently from a security or IP standpoint?

---

## What's Explicitly NOT in This Document

The following items from the full remediation plan are **purely extraction/parsing** and do not require AI/ML team review:

- robots.txt parser and compliance
- User-Agent identification
- SPA hydration payload extraction
- Network request interception
- Mega-menu interactive activation
- Cross-page boilerplate fingerprinting (existing detector evaluation)
- HTML→Markdown via Trafilatura
- Sitemap.xml + canonical URL extraction
- Content-hash deduplication at queue level
- Region-aware proxy routing
- TLS-fingerprint-spoofing client
- Structured JSON logging
- Prometheus/OpenTelemetry metrics
- Per-domain budgets
- Persistent strategy cache
- BreadcrumbList extraction

These will proceed on the crawler team's timeline independently of this review.

---

## Appendix: Source Document References

- `~/crawler-audit/AUDIT_REPORT.md` — Full code audit, 30 prioritized actions
- `~/crawler-audit/FIXTURE_AUDIT_REPORT.md` — Fixture quality audit, 10 candidate fixtures
- `~/crawler-audit/BARCADA_CRAWLER_REMEDIATION_PLAN.md` — Full 20-week remediation plan
- `/Users/administrator/projects/barcada-scraper/DEFERRED_WORK.md` — Existing deferment notes
- `/Users/administrator/projects/barcada-scraper/CHANGELOG.md` — Schema version history

AI/ML team should feel free to request access to any of the above for context, or ask the crawler team to summarize sections rather than reviewing the full documents.

---

*End of document. Please return with per-item decisions or schedule working sessions as needed.*
