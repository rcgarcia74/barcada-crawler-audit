# Reconciliation: Remediation Plan ↔ Phase 4 ↔ Pipeline Architecture

**Status:** Draft for operator review. Not a plan amendment until operator authorizes.
**Date:** 2026-05-21
**Author:** Operator-side chat session (Session 12 equivalent), produced under halt-and-reconcile pattern after W4.2 discovery findings surfaced plan-vs-architecture drift.
**Revision:** Second pass. Incorporates two Claude Code source-verification reports (Phase 4 PR status + Levers 2/3/7 status, Stage 3 input shape) that materially changed the recommendation from the first draft.
**Repo HEAD at verification:** `5513b4c68be542c01821326a70c40860266fc95b`
**Sources read in full:** `AUDIT_DIRECTIVE.md`, `AUDIT_REPORT.md`, `FIXTURE_AUDIT_REPORT.md` (exec summary only), `BARCADA_CRAWLER_REMEDIATION_PLAN.md`, `CLASSIFICATION_ADJACENT_PLAN.md` (Items 1–2 + grep), `SESSION_LOG.md` (structure + key passages), `LESSONS.md` (structure + voice samples), `SESSION_TRANSITION_TEMPLATE.md` (handoff sections), `session-12-prompt.md`, the pipeline architecture rationale document (operator-supplied, no workspace filename), `docs/phase4_implementation_plan.md` (in repo per audit citation; operator-supplied copy here), Claude Code's Phase 4 status verification (2026-05-21), Claude Code's Phase 4 Levers + W4.2 cost envelope verification (2026-05-21), Claude Code's Stage 3 input shape verification (2026-05-21).

---

## 1. Scope

What this document does:

- Identifies and corrects the plan-vs-architecture drift that surfaced when Session 12 attempted to begin W4.2.
- Lists corrections to claims that propagated through the chat conversation before source verification was available.
- Builds a dependency map between remediation-plan work units and Phase 4 PRs, grounded in source-verified current code state.
- Proposes a revised sequencing of Workstream 0 with a new work unit W4.1.5 (Fixture-Cascade Driver) inserted between current W4.1 (complete) and the existing W4.2 (paused).
- Lists the plan-amendment deltas that the operator authorizes by absorbing this reconciliation.
- Drafts a LESSONS.md entry for the new pattern surfaced.

What this document does NOT do:

- Amend `BARCADA_CRAWLER_REMEDIATION_PLAN.md`. That's a separate commit step that follows operator approval of this document.
- Resolve specifics of W4.1.5 implementation. The Session 13 prompt covers that.
- Touch any code, fixtures, or schema artifacts.
- Make irreversible decisions about Phase 4. Phase 4's measurement/validation half (PR-D through PR-G) is gated on operator-led Stage 2 + Stage 3 labeling, which is not currently scheduled. The infrastructure half (PR-COST, PR-A, PR-B, PR-C) is landed.

---

## 2. Corrections to Prior Chat Claims

The conversation that produced this reconciliation made several claims along the way that source documents disagreed with. They are listed here so they don't propagate forward, and to anchor the verify-before-asking pattern that produced the corrections.

### Claim 1 — Phase 4 implementation status

**Chat claim (early):** "Phase 4 is unimplemented; Stage 3 doesn't exist in code yet; Phase 4 builds Stage 3 from scratch."

**Source correction (Claude Code Phase 4 status verification):** Stage 3 exists. Four of eight Phase 4 PRs are fully implemented: PR-COST (cost journal enforcement + RUN_ID + single-tenant guard + list-runs CLI), PR-A (Stage 3 cascade scaffold + thresholds + output schema), PR-B (bot-blocked Hive partitioning + FEATURE_SCHEMA_VERSION = 5), PR-C (Pass 2b feature-flag-off + warm_cache + cached-token logging). The infrastructure half of Phase 4 is done. The measurement/validation half (PR-D operator-led labeling, PR-E lever 2/3/7 validation, PR-F Lever 4 parser pre-classifier, PR-G smoke + final docs) is blocked on PR-D which has not started.

### Claim 2 — Cost journal status

**Chat claim:** "PR-COST is implementing the cost journal."

**Source correction (Phase 4 status verification + AUDIT_REPORT.md line 92):** `cost_journal.py` existed at audit time as an immutable state machine. PR-COST extended it with enforcement (the audit characterized prior enforcement as advisory-only). Both statements were correct individually; the conversation conflated them.

### Claim 3 — Audit blindness to Phase 4 documents

**Chat claim:** "The audit didn't see the architecture document or `phase4_implementation_plan.md`."

**Source correction:** `AUDIT_REPORT.md` line 111 explicitly cites `docs/phase4_implementation_plan.md` and `tools/phase4_cost_reduction_directive.md` as documents containing scattered architecture content. The audit *did* see Phase 4 artifacts. The remediation plan absorbed the cost-reduction directive (plan §9 line 532) but did not incorporate the implementation plan's eight-PR sequence into its workstream design. The gap is between the *plan-authoring step* and the *implementation plan*, not between the *audit* and *Phase 4*.

### Claim 4 — Operator-recall reliability for multi-PR work history

**Operator claim:** "The eight PRs in `phase4_implementation_plan.md` have not been executed."

**Source correction (Phase 4 status verification):** Four PRs (PR-COST, PR-A, PR-B, PR-C) had been executed. The operator-recall claim was incorrect. The chat session accepted the operator-recall claim without source verification, which would have propagated the error into the Option-1 recommendation in the first reconciliation draft. The verify-before-asking discipline (LESSONS.md §"Verify-before-asking discipline") applies to operator-issued state claims, not only to Claude Code's draft outputs. Verification is bidirectional.

### Claim 5 — Stage 2 has no LR tier

**Chat claim (from Session 12 discovery):** "Stage 2 has no LR tier; Stage 2 is LLM-LLM."

**Source confirmation (AUDIT_REPORT.md §8 + Stage 3 input shape verification Q1):** Stage 2 has a two-pass LLM cascade — summarization (Pass 1) + classification (Pass 2). Lever 3 (drop Pass 1) is scheduled in PR-E and has not landed. Lever 2 (downgrade Stage 2 classifier from gpt-4.1-mini to gpt-4.1-nano) is also scheduled in PR-E and has not landed. The Session 12 discovery report was correct against current code. The architecture rationale document's description of post-Lever-3 single-pass Stage 2 is *target state*, not current state.

### Claim 6 — Architecture rationale document as source of current truth

**Chat claim (implicit, multiple turns):** The architecture rationale document describes the production pipeline.

**Source correction:** The architecture rationale document describes the v1 target state — the state Phase 4's eight PRs are designed to produce. Multiple specific details disagree with current code: Lever 3 single-pass Stage 2 (target), gpt-4.1-nano classification (target), gpt-4.1-mini Stage 3 primary (target), Lever 4 parser pre-classifier (target), Pass-1-summarization-dropped (target). Current code is closer to the audit's discovered architecture (§8 of AUDIT_REPORT.md), modified by the four landed Phase 4 PRs. The architecture rationale document should be treated as a *design-of-record for unimplemented work*, not as a description of current code.

### Claim 7 — Adapter scope at single layer

**Chat claim (after Stage 2 verification):** "A fixture-input adapter layer covers the FetcherSet bypass. W4.1.5 is a small work unit."

**Source correction (Stage 3 input shape verification):** Stage 3 reads three upstream artifacts (Stage 2 predictions parquet, Stage 2 summaries parquet, Stage 3 evidence cache parquet) AND fetches its own 4 T3 paths per domain. Stage 2 reads `pages.parquet`. Stage 1 reads parser-output parquet (parser runs against fetched HTML). End-to-end fixture-based pipeline execution requires *five* input surfaces to be either synthesized or bypassed: parser-output, pages.parquet, Stage 2 predictions, Stage 2 summaries, plus the FetcherSet bypass that Stage 2 and Stage 3 both consume. The "small W4.1.5" framing was wrong. The work unit is closer in scope to what plan §4 W6 originally scoped for `barcada-baseline generate`, pulled forward by 2 weeks.

---

## 3. The Core Misalignment, Restated

The plan, the audit, the architecture document, the Phase 4 implementation plan, and current code are each internally consistent. The misalignment is in how the plan composed them.

**What the audit found in code (May 2026, audit HEAD `be71d536`):** A working pipeline with Stage 1 (RULES + LR + LLM cascade), Stage 2 (page acquisition + summarization + classification), Stage 3 (evidence summarizer + primary classification, Pass 2b feature-flag-gated). Cost journal as immutable state machine with advisory-only enforcement. Most of the Top 30 audit-flagged gaps still present (no robots.txt, no SPA hydration, no PII handling, no structured logging, etc.).

**What current code has at HEAD `5513b4c6`:** Audit state + PR-COST + PR-A + PR-B + PR-C. Specifically: cost-journal enforcement (per-shard graceful stop, `cost_ceiling_stopped` outcome, RUN_ID, `--force-concurrent-run`, list-runs CLI); Stage 3 scaffold (`stage3/output_schema.py:112-140`, `stage3/run.py` with three input parquets); bot-blocked Hive partitioning at `schema/parquet_schema.py:73`, `FEATURE_SCHEMA_VERSION = 5`; Pass 2b feature-flagged off (`pipeline_config.yaml:28 stage3_secondary_enabled: false`), prompts as `Final[str]` with cached-token logging.

**What the architecture rationale document describes:** The post-Phase-4-completion target state. Current code is *partway* to that target. Specifically still missing: Lever 2 (Stage 2 classifier nano downgrade), Lever 3 (Stage 2 summarization removal), Lever 4 (parser pre-classifier tier), Lever 7 (Stage 3 primary mini downgrade), PR-G smoke test validation of cost projections.

**What the remediation plan assumed (in its read-only-period locked state):** Audit state, no awareness of Phase 4 PRs landing concurrently. Plan §3 W4 expected.json schema example (line 162–171) shows a `stage3_decision` field as if Stage 3 ran cleanly against fixtures. Plan §14 line 728 names "post-Stage-3-completion" as a v1.1 event for `stage1.schema.json` — implying Stage 3 wasn't complete from the plan-authoring perspective. The plan absorbed `tools/phase4_cost_reduction_directive.md` (cited at line 532 as reference) but not `docs/phase4_implementation_plan.md`.

**The drift, in one sentence:** The remediation plan was authored against the audit's snapshot of code state, but four Phase 4 PRs landed between audit and W4.2 open without being incorporated into the plan's workstream design — and the unimplemented half of Phase 4 (PR-D through PR-G) requires operator-led labeling that is not currently scheduled.

---

## 4. Dependency Map (Source-Verified)

For each remaining remediation-plan work unit and each Phase 4 PR, an assessment of cross-dependency. Conventions:

- **Phase-4-independent:** Can proceed against current code without waiting for unstarted Phase 4 PRs to ship. Not invalidated by future Phase 4 work.
- **Phase-4-influenced:** Can proceed, but scope/acceptance criteria need amendment given current Phase 4 state. Outputs may need minor regeneration if unstarted Phase 4 PRs eventually land.
- **Phase-4-aligned:** Specific Phase 4 PR has landed in a way that helps this remediation-plan unit. Plan unit scope can be tightened or simplified.

### 4.1 Remediation-plan work units

| Unit | Status | Phase 4 relationship | Reasoning |
|---|---|---|---|
| W0 W1 (fixture critical repairs) | COMPLETE (S5–S6) | Phase-4-independent | Fixture file hygiene. |
| W0 W2 (hydration fixtures) | COMPLETE (S7) | Phase-4-independent | Fixture authoring. |
| W0 W3 (C18 modern SaaS + C7 mega menu) | COMPLETE (S8–S9) | Phase-4-independent | Fixture authoring. |
| W0 W4.0 (META_SCHEMA lock) | COMPLETE (S10) | Phase-4-influenced | `expected/<domain>.json` schema (v1.0 locked) embeds a Stage 1/2/3 decision shape. Current code emits `tier_decided="parser_rule"` constant exists at `stage3/output_schema.py:53` but no code path assigns it (PR-F unstarted). META_SCHEMA prose-only fix register grows to absorb this and several other items from §6 below. |
| W0 W4.1 (bulk meta.json) | COMPLETE (S11) | Phase-4-independent | Pure provenance metadata. |
| **W0 W4.1.5 (fixture-cascade driver)** | **PROPOSED NEW WORK UNIT** | Phase-4-aligned | Engineering work to build the end-to-end fixture-cascade driver. Sits between W4.1 (complete) and W4.2 (paused). See §5 for scope. PR-A's `stage3/output_schema.py` and PR-B's bot-blocked partition are inputs that simplify the driver design (Phase 4 work *helps* this unit). |
| **W0 W4.2 (expected.json bulk)** | **PAUSED — REVISED SCOPE** | Phase-4-influenced | After W4.1.5 lands, W4.2 generates expected outputs using the driver. Cost envelope is $0.30 ballpark per Claude Code Q3 verification. Output lifetime is "until W A.0 W6 OR until Phase 4 PR-E lands, whichever comes first" — at which point a regeneration pass runs against post-Lever-2/3/7 cascade. |
| W0 W4.3 (test infrastructure) | NOT STARTED | Phase-4-independent | After W4.2 produces expected outputs, the comparison framework consumes them. Self-contained. |
| W0 W5 (multipage + edge case fixtures + soft_404 / empty_google_sites repopulation) | NOT STARTED | Phase-4-independent | Pure fixture authoring + deferred repopulation. |
| W A.0 W6 (snapshot generation CLI) | NOT STARTED | Phase-4-aligned | The `barcada-baseline generate` CLI wraps or extends the W4.1.5 cascade driver. Less new code needed at W6 than the plan originally scoped, because the driver already exists. |
| W A.0 W7 (synthetic crawl tapes + canary wiring) | NOT STARTED | Phase-4-influenced | VCR cassettes recorded against current code carry pre-Lever-2/3/7 cascade. Cassette regeneration needed if Phase 4 PR-E ever lands. |
| W A W8–W9 (robots.txt parser, UA fix, governance docs, anti-pattern cleanup) | NOT STARTED | Phase-4-independent | Compliance + docs. No Phase 4 collision. |
| W B W10–W12 (cost-per-useful-record metric, version stamping, efficiency flags, per-domain budgets, persistent strategy cache, structured JSON logging, metrics emission) | NOT STARTED | Phase-4-aligned | PR-COST landing materially helps Workstream B: cost journal extension exists, `cost_ceiling_stopped` outcome is in the parquet schema, RUN_ID propagation is wired. Workstream B builds on this rather than coordinating with a parallel refactor. Per-domain budget work (Action #8) extends an already-extended `cost_tracker.py`. PR-F's `TIER_PARSER_RULE` constant existing without an emitter is mildly relevant to the efficiency-flag catalog (Action #7); flag the tier in the catalog even though no fixture currently routes there. |
| W C W13–W16 (SPA hydration, network interception, mega-menu activation, HTML→Markdown, BreadcrumbList, boilerplate fingerprinting eval) | NOT STARTED | Phase-4-influenced | SPA hydration changes parser output → changes Stage 1/2 inputs → changes expected outputs. Mega-menu activation similarly. Action #11 HTML→Markdown intersects with PR-E (Lever 2/3/7 validation, which measures classifier accuracy on production text); coordinate timing if Phase 4 PR-E eventually unblocks. |
| W D W17–W19 (regional_policy.json, sitemap/canonical, content-hash dedup, region-aware proxy) | NOT STARTED | Phase-4-independent | Region/policy additions. No Phase 4 collision. |
| W E W20+ (CI regression gate, acceptance metric formula, drift detection) | NOT STARTED | Phase-4-influenced | CI gate compares against baseline-v0 (W A.0 W7 close). Baseline lifetime depends on Phase 4 PR-E status — if PR-E never lands, baseline-v0 is durable; if PR-E lands later, baseline regeneration becomes a Workstream E event. |

### 4.2 Phase 4 PRs

| PR | Status | Remediation-plan units it helps / blocks |
|---|---|---|
| PR-COST | ✅ Landed | Helps W B (cost-per-useful-record, per-domain budgets layer on top of journal extensions); helps W4.1.5 (driver can use enforcement for safety even on low-cost fixture runs). |
| PR-A | ✅ Landed | Helps W4.1.5 (Stage 3 output schema is settled; META_SCHEMA can reference actual column names); helps W4.2 (Stage 3 decision shape is known); helps W4.0 META_SCHEMA reconciliation. |
| PR-B | ✅ Landed | Helps W A.0 W6 (Hive partitioning by `bot_blocked` is part of the parquet schema baseline-v0 captures). Touches `parquet_schema.py:73`. |
| PR-C | ✅ Landed | Helps W4.2 (Pass 2b feature-flag-off means W4.2 expected outputs don't need a `secondary_partner_types` field; schema simplification). Helps W B (prompt-cache hygiene tracking gives observability work a foundation). |
| PR-D (operator-led labeling) | ❌ Not started | None — operator-led, separate from Workstream 0. Confirmed same as parallel Stage 1 labeling chat session for Stage 1, but Stage 2 + Stage 3 labeling is NOT currently scheduled. |
| PR-E | ❌ Blocked on PR-D | If eventually landed, triggers W4.2 expected-outputs regeneration + W A.0 W6 baseline regeneration. Until then, current cascade composition (pre-Lever-2/3/7) holds. |
| PR-F | ⚠ Partially implemented (constant only, no driver consult) | When fully landed, adds `tier_decided="parser_rule"` to W4.2 expected outputs; W B efficiency-flag catalog should reference. |
| PR-G | ⚠ Partially landed ($4,500 default; no smoke results) | When fully landed, W E acceptance criteria reference smoke-validated cost ceiling. Not a blocker for Workstream 0 close. |

### 4.3 The W4.2 / W A.0 W6 relationship (refined)

The plan describes two expected-outputs generation passes:

- **W4.2** (plan §3 W4 lines 162–173): per-fixture `expected/<domain>.json`, generated once, human-reviewed, committed.
- **W A.0 W6** (plan §4 lines 213–230): per-fixture expected outputs via `barcada-baseline generate`, "supersede the Week 4 expected outputs with machine-generated versions."

Two regeneration passes were always planned. The cascade-driver infrastructure was implicit in W A.0 W6's `barcada-baseline generate` design but not in W4.2's design. The proposed W4.1.5 work unit makes the cascade-driver explicit, builds it once, and both W4.2 and W A.0 W6 use it.

The cost of building the driver doesn't change — it was always going to be built at W6. W4.1.5 just builds it ~2 weeks earlier in the schedule.

---

## 5. The Revised Path Forward

### 5.1 W4.1.5 — Fixture-Cascade Driver (new work unit)

**Scope:** Build the engineering infrastructure that lets the full Stage 1 + Stage 2 + Stage 3 cascade run end-to-end against fixture HTML inputs without touching live HTTP or live LLM (LLM calls are real and counted against cost ceiling, but live HTTP is short-circuited).

**Engineering surfaces (per Stage 3 input shape verification Q4 Sub-option (i)):**

1. **Parser-output parquet construction from fixture HTML.** Adapter that takes fixture HTML files, synthesizes a fetched-page envelope (URL from fixture filename, status=200, content=HTML, etc.), runs the parser (`src/barcada_scraper/scraper/parser.py`) against the envelope, and writes a parser-output parquet row in the schema Stage 1 expects.

2. **FetcherSet bypass at the `fetcher_core` seam** (verified seam, Stage 3 verification Q3). A fixture-backed `FetcherSet` substitute that, when Stage 2 or Stage 3 requests any URL, returns the fixture HTML for that domain. Same adapter shape works for both stages because Stage 3 reuses Stage 2's `FetcherSet` type (`stage3/run.py:111-113`).

3. **End-to-end cascade driver script.** Orchestrates parser → Stage 1 → Stage 2 → Stage 3 against the fixture corpus, writes all intermediate parquets (parser output, Stage 1 predictions, Stage 2 predictions, Stage 2 summaries, Stage 3 predictions, pages.parquet outputs) and the consolidated `expected/<domain>.json` per fixture matching META_SCHEMA v1.0.

**Out of scope for W4.1.5:**

- Modifying pipeline code. The bypass is at adapter/seam level; production cascade code stays untouched.
- Eval-data labeling (PR-D territory).
- Mocking LLM calls. LLM calls fire for real against fixture-derived inputs; cost is $0.30 ballpark per Claude Code Q3.
- Coverage of tier-escalation paths (T1 → T2 → T3 promotion on `PROTECTION_ERROR_KINDS`). Per Stage 3 verification Q4 caveat, fixture runs return 200 unconditionally; tier-promotion logic is exercised only at W A.0 W7 synthetic-crawl-tape level if at all.

**Acceptance criteria:**

- Driver runs against 198-fixture corpus end-to-end without manual intervention.
- For each fixture, all five intermediate parquets exist and conform to current code's schemas.
- Per-fixture `expected/<domain>.json` produced and conforms to META_SCHEMA v1.0 (with the deferred prose-only fixes per §6).
- Driver writes a `RUN_ID`-stamped cost journal entry that the operator can inspect to confirm cost-envelope tracking.
- Total LLM cost across the corpus run lands within 3× of the $0.30 Claude Code estimate (orders-of-magnitude floor and ceiling; tighter validation deferred to actual run).
- Driver does not write outside the workspace + `tests/fixtures/html/*/expected/` directories.

**Tagging:**

`workstream-0-week4-1-5-end` tag at clean checkout target (per LESSONS.md Session 6 "Workstream tag at clean completion" and Session 6 "tag at clean SHA not milestone SHA" precedent). Annotation: "Fixture-cascade driver landed. Reusable at W A.0 W6 as `barcada-baseline generate` foundation. W4.2 expected-outputs generation begins on the next commit. Output lifetime: until W A.0 W6 OR until Phase 4 PR-E lands, whichever comes first."

### 5.2 W4.2 — Expected Outputs (revised scope)

**Scope:** With W4.1.5 landed, W4.2 runs the cascade driver against the 198-fixture corpus and produces `expected/<domain>.json` for each, then human-reviews and commits. This is what plan §3 Week 4 originally scoped, but now achievable because the driver exists.

**Cost expectation:** $0.30 LLM ballpark; well within the $100 Workstream 0 cost ceiling.

**Output durability:** "Until W A.0 W6 OR until Phase 4 PR-E lands, whichever comes first." This is the plan-aware shorter-than-original-design lifetime — explicit because Phase 4 Levers 2/3/7 will eventually change cascade behavior if PR-E ever ships. META_SCHEMA prose note documents this.

**Test surface invariant:** After W4.2 + W4.3 land, the conformance test surface advances from 17/169/2 (W5 punch list) to whatever the W4.3 framework reports against expected outputs. The 17 W5-punch-list fixtures don't change here; W5's repopulation of `soft_404/` and `empty_google_sites/` is what reduces the 17 count.

### 5.3 W4.3 — Test Infrastructure Update (unchanged scope)

Replace `exclusion_reason` assertions with `expected/<domain>.json` comparison. Self-contained after W4.2 produces the expected outputs.

### 5.4 W5 — Multipage + Edge Cases + Repopulation (unchanged scope)

Phase-4-independent fixture authoring. Can run in parallel with W4.1.5 if operator wants, but the operator pattern is one-work-unit-at-a-time, so likely sequenced after W4.3 close.

### 5.5 Workstream A.0 onward (refined)

W A.0 W6 builds `barcada-baseline generate` as a thin wrapper or extension over the W4.1.5 driver. Less new code needed than the plan originally implied. Baseline-v0 capture at W A.0 W7 close runs the same driver against the full corpus including any new W5-added fixtures.

Workstream A through E: refer to §4.1 dependency map. Workstream B becomes Phase-4-aligned because PR-COST is landed; the original "Phase-4-collision-heavy" framing from the first reconciliation draft was wrong.

### 5.6 What this DOESN'T require

- Doesn't require Phase 4 PR-D / PR-E / PR-F / PR-G to land first. Workstream 0 closes against current code state. If Phase 4 PR-D ever opens (Stage 2 + Stage 3 labeling), Phase 4's measurement half can proceed independently on its own timeline.
- Doesn't require breaking any operator-locked artifact discipline beyond the read-only-period break (already authorized) for absorbing this reconciliation into the plan.
- Doesn't require the 2026-06-16 AI/ML decision deadline (now flexible per operator confirmation) to be hit.
- Doesn't require a repo split.
- Doesn't require coordination with the parallel Stage 1 labeling session beyond the existing coordination (eval_data/ read-only from crawler side, pre-push hook enforcement).

---

## 6. Plan Amendment Deltas

These are the changes to `BARCADA_CRAWLER_REMEDIATION_PLAN.md` that the operator authorizes by absorbing this reconciliation. Read-only-period discipline already broken per operator authorization.

### 6.1 Required amendments

1. **§1 "Where the crawler is genuinely strong":** Add explicit acknowledgment of Phase 4's infrastructure half being landed (PR-COST + PR-A + PR-B + PR-C). Cite the source-verified status. Reframe the "deterministic-first classifier cascade" bullet to mention the Stage 3 scaffold + bot-blocked partition specifically.

2. **§1 "Where the gaps are real":** Note that Phase 4 measurement/validation half (PR-D through PR-G) is unstarted and gated on operator-led Stage 2 + Stage 3 labeling, which is not currently scheduled. Refer to `docs/phase4_implementation_plan.md` for the full PR sequence.

3. **§2 Plan Overview table:** Add a row "Phase 4 (cost reduction + infra)" with status "Infrastructure half landed; measurement half blocked on operator-led labeling." Reference `docs/phase4_implementation_plan.md` for PR-level detail. Mark as parallel-track to Workstream 0–E sequencing, not gating.

4. **§3 Week 4 — insert new W4.1.5 sub-section.** Per §5.1 of this reconciliation. Place between current "Week 4: Schema lock and per-fixture expected outputs" sub-sections (after W4.1 close, before W4.2). Scope, engineering surfaces, acceptance criteria, tagging, and what's out-of-scope per §5.1.

5. **§3 Week 4 — revise W4.2 sub-section.** Update the `expected/<domain>.json` shape example (currently line 162–171) to match current code's `stage3/output_schema.py:112-140` actual column names. Note the output-durability constraint ("until W A.0 W6 OR until Phase 4 PR-E lands"). Reference W4.1.5 as prerequisite.

6. **§4 Workstream A.0 W6 sub-section:** Update to reference the W4.1.5 driver as foundation. `barcada-baseline generate` becomes "thin wrapper / extension" rather than "new CLI from scratch."

7. **§6 Workstream B (Cost & Observability):** Add note that PR-COST has landed and several W B items (cost-per-useful-record, per-domain budgets, structured logging) build on the journal extension rather than coordinating with parallel refactor. Action #6 "useful record" definition should account for `cost_ceiling_stopped` + `cost_ceiling_global` outcomes already in parquet.

8. **§7 Workstream C:** Note that Action #11 (HTML→Markdown) coordinates with Phase 4 PR-E if PR-E ever opens (since PR-E measures classifier accuracy on production text).

9. **§11 Risk Register:** Add three new entries.
   - "Phase 4 infrastructure half landed concurrently with Workstream 0 without plan absorption" — describes the gap and references this reconciliation document.
   - "W4.2 expected-output lifetime constrained" — output is valid until W A.0 W6 OR Phase 4 PR-E lands, whichever comes first.
   - "Phase 4 measurement half blocked on operator-led labeling" — describes the PR-D dependency and notes that Stage 2 + Stage 3 labeling is not currently scheduled. Plan does not commit to a Phase 4 ship date.

10. **§13 Appendix Reference list:** Add the pipeline architecture rationale document (operator-supplied; needs workspace placement) and `docs/phase4_implementation_plan.md` to source documents.

11. **§14 Session Continuity Discipline durable artifacts:** Add `docs/phase4_implementation_plan.md` (in-repo) and the pipeline architecture rationale document (workspace placement TBD) to the durable artifacts list. Update the locked artifacts section to clarify that the plan was authored against audit-state code; current code is audit-state + landed Phase 4 PRs.

### 6.2 META_SCHEMA prose-only fixes (deferred register)

The META_SCHEMA v1.0 prose-only fix register grows. None of these requires a machine-schema bump (per LESSONS.md Session 11 "defer prose-only schema fixes" pattern); all fold into the next real machine-schema bump's diff. New entries:

- **(d) `tier_decided="parser_rule"` is a valid vocabulary entry.** PR-F partially landed adds the constant `TIER_PARSER_RULE = "parser_rule"` at `stage3/output_schema.py:53` but no code path currently emits it. META_SCHEMA prose should list `parser_rule` as a valid tier value for forward compatibility.

- **(e) `expected/<domain>.json` shape matches `stage3/output_schema.py:112-140` actual columns.** META_SCHEMA prose currently references a `stage3_decision: {partner_type, confidence, tier}` shape. Actual columns differ; reconcile against PR-A's schema.

- **(f) Output durability annotation.** META_SCHEMA prose should explicitly state that `expected/<domain>.json` outputs at W4.2 close have a known shorter-than-final lifetime: "until W A.0 W6 supersedes OR until Phase 4 PR-E lands, whichever comes first."

Combined with the three pre-existing deferred items (Path-A directory ref, replaced_in_place captured_at semantics, approximated_from_synthetic_invalid_fallback vocabulary), the register is now six entries. All fold into the eventual v1.1 bump.

### 6.3 SESSION_LOG.md Session 12 entry

To be authored as part of the operator-authorized plan amendment commit. Should:

- Document the W4.2 discovery-and-halt sequence (cascade-model drift surfaced, halt-and-reconcile pattern engaged).
- Record the two Claude Code source-verification reports as durable artifacts (workspace placement: `~/crawler-audit/working/phase4_status_2026-05-21.md`, `~/crawler-audit/working/phase4_current_state_2026-05-21.md`, `~/crawler-audit/working/stage3_input_shape_2026-05-21.md` — or wherever operator wants them).
- Record the seven chat-claim corrections (§2 above) as examples of the bidirectional verify-before-asking pattern.
- Reference this reconciliation document at `~/crawler-audit/RECONCILIATION_2026-05-21.md`.
- Note the W4.1.5 work-unit insertion as the next concrete step for Session 13.
- Record operator decisions: read-only-period break authorized, reconciliation document location, W4.1.5 + W4.2 sub-path-i sequencing, tagging at W4.1.5 close.

### 6.4 LESSONS.md additions

See §8 below for the draft entries.

---

## 7. Items for Explicit Operator Confirmation

Items 1–4 from the first reconciliation draft are resolved. Remaining:

1. **Reconciliation document location and lifecycle:** confirmed `/Users/administrator/crawler-audit/RECONCILIATION_2026-05-21.md`. Treated as one-shot historical record (per AUDIT_REPORT.md preservation convention), not a living document.

2. **Architecture rationale document placement:** The architecture rationale doc is operator-supplied and currently has no workspace home. It's referenced in this reconciliation as a design-of-record for unimplemented work. Should it be copied into `/Users/administrator/crawler-audit/` (e.g., as `PIPELINE_ARCHITECTURE_TARGET_STATE.md`) for durability, or does it live elsewhere that future sessions can access reliably?

3. **The three Claude Code source-verification reports:** Phase 4 PR status, Levers 2/3/7 + W4.2 cost envelope, Stage 3 input shape. The Stage-3-shape and cost-envelope reports were optionally writable to `~/crawler-audit/working/`. The Phase 4 PR status report wasn't asked to write a file but the contents are in chat. Want these preserved as durable workspace artifacts? Recommended: yes, all three preserved as `~/crawler-audit/working/phase4_status_2026-05-21.md`, `phase4_current_state_2026-05-21.md`, `stage3_input_shape_2026-05-21.md`, referenced from SESSION_LOG.md Session 12 entry.

---

## 8. Proposed LESSONS.md Entries

Two entries proposed. Voice and structure match existing LESSONS.md entries.

### 8.1 New pattern — verify-before-asking is bidirectional

```markdown
## Verify-before-asking discipline (extension)

### The discipline applies to operator-issued state claims, not only to Claude Code's draft outputs

**Established:** Session 12 / Phase 4 reconciliation (2026-05-21).

The verify-before-asking discipline as originally named (Session 10 Flag 2
resolution) emphasized Claude Code's outputs being verified before
commit. The Session 11 close-out claims-by-analogy work extended this to
bidirectional verification of structural claims in handoff documents.
Session 12 extends it further: operator-issued state claims about
multi-PR multi-week work history also require source verification, not
acceptance from operator recall alone.

Specific instance: operator stated "Phase 4 has not been implemented at
all" in Session 12. The chat session accepted this and was preparing to
recommend a sequencing path on that basis. Claude Code source
verification then revealed four of eight Phase 4 PRs had landed. The
operator-recall claim was incorrect against source. Had the chat
proceeded with the recommendation without verification, the
operator-authorized plan amendment would have been wrong.

**The rule:** When the next decision depends on a multi-artifact state
claim (e.g., "X PRs have landed", "Y work units are complete", "Z
artifact exists"), verify against source before locking the decision —
even when the claim comes from the operator. The operator may have
context Claude Code lacks, but the source-of-truth is the artifact
itself, not the recall.

**Mechanism:** A targeted verification prompt to Claude Code that asks
narrow factual questions with explicit citation requirements. Cost is
modest (one session, no plan amendments). Benefit is preventing
plan-amendment-based-on-wrong-state, which is much more expensive to
unwind.

**See also:** "Verify-before-asking discipline anchor" (Session 10) for
the discipline-naming entry; "Close-out claims-by-analogy" (Session 12
pre-Session-12) for the bidirectional structural-claim verification
extension.
```

### 8.2 New pattern — driver-level input contracts need verification before generation work

```markdown
## Driver-level input contracts

### Verify cascade input shape before scoping generation work

**Established:** Session 12 / Phase 4 reconciliation (2026-05-21).

The W4.2 work-unit scoping assumed that generating per-fixture expected
outputs was a configuration matter: run the cascade against fixtures,
capture outputs. This assumption was wrong against actual driver code.
Stage 2 consumes `pages.parquet` produced by `FetcherSet` HTTP fetches;
Stage 3 consumes three upstream parquets (Stage 2 predictions, Stage 2
summaries, Stage 3 evidence cache) AND fetches its own four T3 paths
per domain. No fixture-input bypass exists at the driver level.

**The pattern:** Before scoping any work unit that involves running
pipeline code against synthetic inputs (test fixtures, synthetic
crawls, replay cassettes), verify the driver-level input contract at
runtime-code source. The contract is what the run-driver actually
consumes — not what the audit's discovered-architecture section
described, not what the design-of-record document says the cascade
should look like, not what plan-authoring assumed. The runtime code is
the source of truth.

**Specific surfaces to verify:**
- Driver entry-point (run.py or equivalent): what files does it open at
  startup? Confirm via grep `read_parquet`, `pd.read_csv`, `open(...)`,
  Hive partition reads.
- Fetcher invocations: does the stage trigger live HTTP? At what seam?
  Confirm via grep for fetcher class names, URL request invocations.
- CLI flags: does a bypass / test-mode / input-parquet flag exist?
  Confirm via grep `argparse.add_argument`, CLI module reads.

**Trigger condition for verification:** Before scoping a work unit that
will run pipeline against synthetic inputs, run a targeted Claude Code
verification with file:line citation requirements.

**Mitigation when bypass doesn't exist:** Build the bypass as its own
work unit, not as side-effect engineering inside the work unit that
needs it. The bypass is foundation; the work unit that consumes the
bypass is consumer. Separate them. (See W4.1.5 / W4.2 split in
RECONCILIATION_2026-05-21.md for the working example.)

**See also:** "Audit-spec vs. production-reality drift" (Session 9) and
"Verify-before-asking discipline" (Session 10). This pattern is the
input-contract-specific instance of those broader patterns.
```

---

## 9. Next Concrete Step

After operator review of this document:

1. Authorize the plan amendment commit per §6.1–6.3. Coordinated as one logical commit (multiple files: `BARCADA_CRAWLER_REMEDIATION_PLAN.md`, `SESSION_LOG.md`, `LESSONS.md`). Could be split into two if size is unwieldy, but logically one operator-authorized amendment.

2. Stage the three Claude Code verification reports as workspace artifacts at `~/crawler-audit/working/` (or wherever operator prefers). Reference from SESSION_LOG.md Session 12 entry.

3. Place the architecture rationale document in workspace per §7 item 2.

4. Author the Session 13 prompt that:
   - Cold-starts against the reconciled plan state.
   - Points Session 13 at W4.1.5 (fixture-cascade driver) as the next concrete work unit.
   - Includes engineering-design guidance for the three W4.1.5 surfaces (parser-output adapter, FetcherSet bypass, end-to-end driver script).
   - Anchors verify-before-asking discipline updates per the new LESSONS.md entries.

5. Operator commits and pushes the workspace, then opens Session 13.

The W4.2 paused state is converted to "W4.1.5 next work unit, W4.2 follows W4.1.5 close."

---

*End of revised reconciliation document. Awaiting operator authorization to land plan amendment.*
