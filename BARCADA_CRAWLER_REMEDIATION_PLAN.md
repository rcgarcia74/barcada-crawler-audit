# Barcada Crawler Remediation Plan

**Status:** Draft v1.0
**Generated:** May 2026
**Repository:** `/Users/administrator/projects/barcada-scraper`
**Sources:** `AUDIT_REPORT.md`, `FIXTURE_AUDIT_REPORT.md`, spot-check verifications, design discussions

This document consolidates the remediation strategy for the barcada-scraper crawler based on two read-only audits and subsequent spot-check verifications. It supersedes individual findings by sequencing them into an executable plan with explicit prerequisites, scope corrections, and timeline.

---

## 1. Context and Honest Framing

### What barcada-scraper actually is

A specialized four-stage classification pipeline (domain validation → business classifier → technology sub-category → partner-type) with an Azure VMSS orchestrator. **English-first, USA-centric, B2B-focused.** Not a generic intent-extracting crawler.

This scope materially changes which audit findings apply. Sections of the original framework covering internationalization, label-to-intent matching, and multi-locale path dictionaries are largely out of scope for the current product. Findings under these sections are deferred unless international expansion is planned.

**PII detection and redaction (originally audit Action #19) is excluded from this plan by explicit scope decision.** The audit identified the absence of PII handling as a gap; this plan does not address it. Reasons may include: PII handling is owned by a separate team, classification inputs must not be modified by extraction-side redaction, or the work is deferred to a future cycle. If/when PII work is in scope, it should be addressed in a separate plan with AI/ML team review of input-modification implications.

### Where the crawler is genuinely strong

Acknowledged before listing gaps, because building on strengths matters:

- **Versioned schema discipline.** `feature_schema_version` stamped on every emitted record. Honest deferments documented in `DEFERRED_WORK.md`.
- **Sophisticated cost discipline.** Immutable cost journal with ETag-conditional writes. Per-tier rates with kill switches at 0.95× budget. Per-domain cost attribution via `_attribute_fetch_cost`. Deterministic-first classifier cascade (RULES → LR → LLM) with documented thresholds — and, post-PR-A landing (see Phase 4 bullet below), a Stage 3 cascade scaffold with thresholds and output schema settled, including bot-blocked Hive partitioning at the parquet boundary per PR-B.
- **Phase 4 infrastructure half landed.** PR-COST (cost journal enforcement + RUN_ID + single-tenant guard + list-runs CLI), PR-A (Stage 3 cascade scaffold + thresholds + output schema), PR-B (bot-blocked Hive partitioning + `FEATURE_SCHEMA_VERSION = 5`), PR-C (Pass 2b feature-flag-off + `warm_cache` + cached-token logging) are all implemented at HEAD `5513b4c6`. The audit's discovered architecture description (`AUDIT_REPORT.md` §8) modified by these four landed PRs is the current code state. See `docs/phase4_implementation_plan.md` for the eight-PR sequence; this plan is reconciled with current code via `RECONCILIATION_2026-05-21.md`.
- **Broad block detection.** Covers 14+ anti-bot vendors (Cloudflare, Akamai, DataDome, Imperva, PerimeterX, Wordfence, Sucuri, F5 Shape, Kasada, AWS WAF, Turnstile, hCaptcha, Arkose, Chinese geo-blocks). Well above industry norm.
- **Prompt cache awareness.** `cached_input_tokens` tracked per shard; 80% hit-rate target; documented warm-cache helper.
- **UA rotation strategy.** Random rotation in `fetcher.py`, deterministic per-host selection in `http_headers.py` — two legitimate strategies for different stages. Audit missed this; spot-check confirmed.
- **Operational maturity.** Resumable runs, single-tenant guards with 4-hour staleness window, structured Parquet output, Hive-partitioned by shard.
- **Cross-page boilerplate detection.** `detect_cross_page_banners()` in `text_cleaning.py` — used in production via `worker_loop.py`. Audit missed this; spot-check confirmed.
- **Extensive content hashing.** `sha256(ml_text)` for embedding cache, `sha256(content)` per domain for LLM cache (Stage 2 and Stage 3), used pervasively. Audit's "no content-hash dedup" claim was misleading.

### Where the gaps are real

Despite the strengths, real gaps remain:

- **Compliance.** No robots.txt parser anywhere. Domain validator UA masquerades as a browser without honest identification.
- **Observability.** Plain-text logging only; no Prometheus/StatsD; no trace_id propagation; no alert definitions.
- **Cost-per-useful-record KPI.** Cost is tracked, useful records are produced, but they're not joined into the framework's primary KPI.
- **Per-domain budgets.** Only global ceiling exists; one runaway domain can consume the whole budget.
- **SPA hydration extraction.** Zero of 197 fixtures contain `__NEXT_DATA__`, `__NUXT__`, `__APOLLO_STATE__`, etc. No hydration extraction in code either.
- **Interactive rendering.** Renderer is purely passive; no mega-menu activation, no hover/click/focus interaction.
- **Regional policy enforcement.** No `regional_policy.json`; no field-level emit rules per jurisdiction; no policy stamping on records.
- **Persistent strategy cache.** Per-domain tier learning is in-memory per shard, lost between runs.
- **Documentation artifacts.** `ARCHITECTURE.md`, `CRAWLING_POLICY.md`, `FAILURE_PATTERNS.md` don't exist as named files.
- **Phase 4 measurement/validation half unstarted.** PR-D (operator-led Stage 2 + Stage 3 labeling), PR-E (Lever 2/3/7 validation), PR-F (Lever 4 parser pre-classifier), and PR-G (smoke + final docs) are unstarted and gated on PR-D, which requires operator-led Stage 2 + Stage 3 labeling — not currently scheduled. See `docs/phase4_implementation_plan.md` for PR-level detail and `RECONCILIATION_2026-05-21.md` §4.2 for the per-PR dependency map.

### Where the fixture corpus reveals deeper issues

The fixture audit (`FIXTURE_AUDIT_REPORT.md`) found that the test infrastructure underneath the audit's findings was itself broken:

- **7% fixture utilization.** Of 197 HTML fixtures, only ~14 are referenced by tests, due to a `sorted(glob("*.html"))[0]` pattern that picks alphabetically-first file per directory.
- **Broken directory contracts.** `soft_404/` has 0 of 14 fixtures conforming to its detection spec. `empty_google_sites/` has 0 of 3.
- **One empty fixture being "tested".** `auth_403/grimsfairytales.net.html` is 0 bytes and is alphabetically first — meaning the auth_403 test is testing an empty string.
- **One actively misleading fixture.** `legitimate_nonprofit/wikipedia.org.html` is a 141-byte Wikipedia robots-policy rejection, not a non-profit homepage.
- **Truncation artifacts.** Multiple fixtures at suspicious round byte boundaries (200,000 exactly, 131,072 exactly, three unrelated at 32,752 exactly).
- **Production-fixture inversion.** Fixtures are 59% parking; production canary is 2% parking. Fixtures are 8% legitimate business; production "ok" is 68%.

This means the test/baseline foundation must be repaired before audit remediation can proceed safely.

---

## 2. Plan Overview

The remediation work is sequenced into six workstreams, each with explicit prerequisites:

| Workstream | Weeks | Purpose |
|---|---|---|
| 0: Fixture Foundation | 1-5 | Repair and rebuild the test corpus; fix the `sorted(glob)[0]` pattern; add provenance and expected outputs |
| Phase 4 (cost reduction + infra) | parallel | Infrastructure half landed (PR-COST/A/B/C); measurement half (PR-D/E/F/G) blocked on operator-led Stage 2 + Stage 3 labeling. Not currently scheduled. See `docs/phase4_implementation_plan.md`. |
| A.0: Baseline Scaffolding | 6-7 | Snapshot generation, comparison tooling, capture baseline-v0 |
| A: Compliance Foundation | 8-9 | robots.txt parser, identifiable UA, docs, anti-pattern cleanup |
| B: Cost & Observability | 10-12 | Cost-per-useful-record, per-domain budgets, structured logging, metrics |
| C: High-Leverage Extraction | 13-16 | SPA hydration, network interception, mega-menu activation, HTML→Markdown |
| D: Compliance Hardening | 17-19 | Regional policy, version stamping, sitemap/canonical, region-aware proxy routing |
| E: Quality Infrastructure | 20+ | CI regression gates, drift detection, acceptance criteria, ongoing |

Each workstream is structured so its outputs are validated against the baseline established by the previous workstream. Workstream 0 protects everything; Workstream A.0 protects the rest.

Phase 4 runs parallel-track to the Workstream 0–E sequence, not gating. The infrastructure half (PR-COST, PR-A, PR-B, PR-C) landed during the Workstream 0 read-only period and is reflected in current code at HEAD `5513b4c6`; the measurement half (PR-D–PR-G) is unstarted and not currently scheduled. Cross-references in specific workstream sections (notably §4 Workstream A.0 W6, §6 Workstream B, §7 Workstream C Action #11, and §11 Risk Register) acknowledge these dependencies where they materially affect work-unit scope.

---

## 3. Workstream 0: Fixture Foundation (Weeks 1-5)

**Why first:** Audit and baseline tooling assume fixtures represent meaningful, conforming behavior. Without trustworthy fixtures, regression detection is unreliable. The fixture audit found 7% utilization and multiple broken directories. Fix this before anything else.

### Week 1, Days 1-2: Critical Repairs

**Status: COMPLETED 2026-05-19.** Commits 96dcbfd, bef4b80, 3fa3228, 7f3756b, b7089eb, 3dec85b, 45bbe30, 26771e9, a156727 on `main`. Branch was 9 commits ahead of `origin/main` at completion of Days 1-2.

Embarrassing-if-discovered-publicly fixes (executed):

- **C0.1** (96dcbfd): Deleted `auth_403/grimsfairytales.net.html` (0 bytes). `auth_403/` retains 14 fixtures; 10 conform to 403/auth markers under a broad-grep check; alphabetically-first surviving file is `bestlyn.com.html` (real "403 Forbidden" page, 548 B).
- **C0.2** (bef4b80): Replaced `legitimate_nonprofit/wikipedia.org.html` (141 B robots-rejection) with `mozilla.org.html` (48,389 B real Mozilla Foundation homepage). Mozilla is tech-leaning; Week 3+ C22 expansion adds archetypal nonprofits for balance.
- **C0.3** (3fa3228): Resolved `soft_404/` — deleted all 14 non-conforming fixtures (0 of 14 matched detector markers under a first-2000-char length-guarded grep). 6 conforming captures scheduled for Week 5 (see C0.3-followup). Detector retains test coverage via inline synthetic HTML in 7 test files (`test_soft_404.py`, `test_barriers.py`, `test_refinements.py`, `test_check_domains_instrumentation.py`, `test_text_cleaning.py`, `test_validator_metrics.py`, and via name-reference in `test_hard_exclusions.py`).
- **C0.4** (7f3756b): Resolved `empty_google_sites/` — deleted all 3 non-conforming fixtures (Google-Sites-flavored `ppConfig` output but missing the editor-frontend SDK markers the detector requires: `sites-viewer-frontend` / `atari.vw.` / `normalizedPath.*view/`). 3 conforming captures scheduled for Week 5 (see C0.4-followup). Detector retains test coverage via inline synthetic HTML in 2 test files (`test_barriers.py` lines 1170-1175; `test_body_reserve.py` lines 439/457/480).
- **C0.5 truncation suspects** (5 files; resolved in commits b7089eb, 3dec85b, 45bbe30, 26771e9, a156727):
  - `spa_shell/shelterstoreau.com.html` (200,000 B exact): deleted (C0.5a). Recapture revealed misclassification — underlying domain is real e-commerce ("AU Outdoor Equipment..."), not an SPA shell. The truncation made it look SPA-ish. Fresh capture deferred to audit C18 (legitimate_business/ expansion).
  - `spa_shell/shelterstores.com.html` (131,072 B exact): deleted (C0.5b). Same misclassification ("Firesettle Camp Shop..."). Fresh capture deferred to audit C18.
  - `soft_404/ssptonline.com.html` (32,752 B): absorbed by C0.3 corpus reset.
  - `parking_sale/shelvs.com.html` (32,752 B): replaced in-place with fresh recapture (C0.5c). New capture is a clean HugeDomains landing (43,512 B); conforms to `parking_sale/` spec with 92 for-sale marker matches.
  - `legitimate_business/sanmarcosflowershop.com.html` (32,752 B): C0.5d (26771e9) initially "accepted with notes" based on a single TLS failure on first recapture attempt. **C0.5d-followup (a156727) diagnosed the TLS failure as transient** (3-attempt probe showed 1 fail + 2 success; openssl confirmed a valid GoDaddy cert chain) and replaced the fixture in-place with the fresh capture (485,599 B; following 301 redirect from `sanmarcosflowershop.com` to `flowersbyroberttaylor.com`). Lesson captured in Risk Register §11.

Net corpus change: 197 → 177 fixtures. Two directories (`soft_404/`, `empty_google_sites/`) currently empty; repopulation scheduled Week 5.

### Week 1, Days 3-5: Fix the Test Selection Pattern

The `sorted(glob("*.html"))[0]` pattern is the highest-leverage bug fix in the entire remediation plan. Fixing it potentially increases tested fixtures from ~14 to ~197 with no other changes.

- Grep `tests/` for `sorted(glob` and `sorted(.*glob` and similar selection patterns
- For each occurrence, refactor to one of:
  - Iterate all fixtures in the directory and apply the check to each
  - Explicitly name the fixture being tested (`_read_fixture("auth_403", "specific_case.html")`)
  - Use a fixture manifest with named test cases
- Re-run the test suite. Most tests should still pass; failing tests indicate fixtures that were silently broken under the old pattern

### Week 2: Critical Hydration Fixtures

These directly unblock Workstream C (the highest-impact extraction work):

- **Candidate #1:** 3 fixtures in new `spa_hydration_next/` with populated `__NEXT_DATA__` script blocks (CSR-only, ISR, full-SSR variants). Source: capture from real Next.js production sites or recent open-source examples.
- **Candidate #2:** 2 fixtures in new `spa_hydration_nuxt/` with `window.__NUXT__` or `<script id="__NUXT_DATA__">`.
- **Candidate #7:** 2 Apollo (`__APOLLO_STATE__`) + 2 Redux (`__PRELOADED_STATE__`) hydration fixtures.

For each, ensure the captured HTML contains the actual hydration payload, not just a shell. Test the capture by attempting to parse the payload — if it parses as JSON, it's a real hydration payload.

### Week 3: High-Priority Gap Fixtures

Closes the most damaging production-coverage gaps:

- **Candidate #5 (revised per operator decision 2026-05-19):** 3 international-TLD fixtures (1× .de, 1× .jp, 1× .com.br) in new `international_business/<locale>/` — unblocks Action #20 (regional policy) at ~85%. CCPA (US, IP-based not TLD-based) and PIPL (.cn) coverage are deferred regardless of fixture count and will be addressed in a separate work item with appropriate test infrastructure (geoip mocking for CCPA; dedicated .cn anti-bot handling for PIPL).
- **Candidate #6:** 3 mega-menu fixtures with `aria-haspopup` triggers + multi-column nested `<ul>` panels — unblocks Action #13 (mega-menu activation)
- **Candidate #4:** 5 modern SaaS fixtures in `legitimate_business/` with hreflang + canonical + JSON-LD Organization schema — addresses the 60-pp production-coverage gap
- **Candidate #22 (new, follow-up to C0.2 commit bef4b80):** 2-3 archetypal nonprofit fixtures extending `legitimate_nonprofit/`. Targets: Wikimedia Foundation, an `@type=EducationalOrganization` (e.g., khanacademy.org), and an archetypal philanthropy (e.g., doctorswithoutborders.org or worldwildlife.org). Closes the representation gap noted in C0.2 — mozilla.org is the tech-leaning corner of an otherwise underrepresented directory; C22 makes `legitimate_nonprofit/` a 4-5 fixture mix with proper representation across tech, education, and philanthropy archetypes. Each new capture should have JSON-LD Organization or NGO schema (closing the audit's noted JSON-LD-absent gap from mozilla.org).

### Week 4: Provenance and Expected Outputs

Per-fixture labeling. This is what turns "files exist" into "fixtures are tested with explicit expected outcomes":

For every fixture (existing + new):

```
tests/fixtures/html/<category>/<domain>.html               # the capture
tests/fixtures/html/<category>/<domain>.meta.json          # provenance
tests/fixtures/html/<category>/expected/<domain>.json      # expected outputs
```

**`meta.json` schema:**
```json
{
  "source_url": "https://example.com/",
  "captured_at": "2026-05-15T10:00:00Z",
  "capture_method": "playwright",
  "content_type": "text/html; charset=utf-8",
  "content_length": 45234,
  "encoding": "utf-8",
  "response_status": 200,
  "expected_outcome": "is_business=true, stage2_category=saas, stage3_partner=technology_partner",
  "test_purpose": "Tests legitimate B2B SaaS classification with Next.js hydration"
}
```

### Week 4 (W4.1.5): Fixture-Cascade Driver

**Status: PROPOSED — to be executed at Session 13.** Inserted per `RECONCILIATION_2026-05-21.md` §5.1 / §6.1 Edit 4 as a Phase-4-aligned engineering work unit between W4.1 (bulk meta.json, complete at `9e1bda9`) and W4.2 (expected outputs, scope-revised below).

**Scope:** Build the engineering infrastructure that lets the full Stage 1 + Stage 2 + Stage 3 cascade run end-to-end against fixture HTML inputs. No live HTTP. LLM calls fire for real (against fixture-derived inputs) and are counted against the $100 Workstream 0 cost ceiling.

**Three engineering surfaces** (per Stage 3 input shape verification 2026-05-21 Q4 Sub-option (i)):

1. **Parser-output parquet construction from fixture HTML.** Adapter that takes fixture HTML files, synthesizes a fetched-page envelope (URL from fixture filename, status=200, content=HTML), runs the parser against the envelope, and writes a parser-output parquet row in the schema Stage 1 expects.
2. **FetcherSet bypass at the `fetcher_core` seam** (verified seam, Stage 3 verification Q3). A fixture-backed `FetcherSet` substitute that, when Stage 2 or Stage 3 requests any URL, returns the fixture HTML for that domain. The same adapter shape works for both stages because Stage 3 reuses Stage 2's `FetcherSet` type at `stage3/run.py:111-113`.
3. **End-to-end cascade driver script.** Orchestrates parser → Stage 1 → Stage 2 → Stage 3 against the fixture corpus, writes all intermediate parquets (parser output, Stage 1 predictions, Stage 2 predictions, Stage 2 summaries, Stage 3 predictions, `pages.parquet` outputs), and the consolidated `expected/<domain>.json` per fixture matching META_SCHEMA v1.0.

**Out of scope for W4.1.5:**

- Modifying pipeline code. The bypass is at adapter/seam level; production cascade code stays untouched.
- Eval-data labeling (Phase 4 PR-D territory).
- Mocking LLM calls. LLM calls fire for real against fixture-derived inputs.
- Coverage of tier-escalation paths (T1 → T2 → T3 promotion on `PROTECTION_ERROR_KINDS`). Fixture runs return 200 unconditionally; tier-promotion logic is exercised only at W A.0 W7 synthetic-crawl-tape level, if at all.

**Acceptance criteria:**

- Driver runs against the 198-fixture corpus end-to-end without manual intervention.
- For each fixture, all five intermediate parquets exist and conform to current code's schemas.
- Per-fixture `expected/<domain>.json` produced and conforms to META_SCHEMA v1.0 (with the six deferred prose-only fixes per `SESSION_TRANSITION_TEMPLATE.md` "Deferred prose-only fixes" register).
- Driver writes a `RUN_ID`-stamped cost journal entry the operator can inspect to confirm cost-envelope tracking.
- Total LLM cost across the corpus run lands within 3× of the $0.30 Claude Code estimate (orders-of-magnitude floor and ceiling; tighter validation deferred to actual run).
- Driver does not write outside the workspace + `tests/fixtures/html/*/expected/` directories.

**Tagging:** `workstream-0-week4-1-5-end` at clean checkout target, per LESSONS.md Session 6 "Workstream tag at clean completion" and "tag at clean SHA not milestone SHA" pattern. Annotation: "Fixture-cascade driver landed. Reusable at W A.0 W6 as `barcada-baseline generate` foundation. W4.2 expected-outputs generation begins on the next commit. Output lifetime: until W A.0 W6 supersedes, OR until Phase 4 PR-E lands, whichever comes first."

### Week 4 (W4.2): Expected Outputs (revised scope)

**Prerequisite:** W4.1.5 must close before W4.2 opens. W4.2 runs the W4.1.5 fixture-cascade driver against the 198-fixture corpus and produces `expected/<domain>.json` per fixture; the driver does not yet exist at session-open and is built at W4.1.5.

**`expected/<domain>.json` schema:**
```json
{
  "parser_output": { ... full deterministic-serialized parser output ... },
  "barriers_verdict": null,
  "stage1_decision": {"is_business": true, "business_score": 0.91, "tier": "RULES"},
  "stage2_decision": {"tech_category": "saas", "confidence": 0.88, "tier": "LR"},
  "stage3_decision": {"partner_type": "technology_partner", "confidence": 0.82, "tier": "LLM"}
}
```

<!-- TODO Session 13 open: reconcile this schema example against
src/barcada_scraper/classifier/stage3/output_schema.py:112-140.
Verified at HEAD 5513b4c6 the repo schema exists; this absorption
session is out-of-scope for repo reads. -->

**Cost expectation:** $0.30 LLM ballpark per Claude Code Q3 verification 2026-05-21; well within $100 Workstream 0 cost ceiling. See `~/crawler-audit/working/phase4_current_state_2026-05-21.md` for the per-stage cost breakdown.

**Output durability:** W4.2 expected-output lifetime: until W A.0 W6 supersedes via baseline-v0 generation, OR until Phase 4 PR-E lands and Levers 2/3/7 change cascade behavior, whichever comes first. See §11 Risk Register for the lifetime-constraint risk entry.

Generate expected outputs once, human-review them, commit. Subsequent test runs compare against these.

### Week 5: Multipage Fixtures and Edge Cases

- **Candidate #3:** 20 fixtures (5 domains × 4 pages each) in new `multipage_boilerplate/<domain>/{home,about,pricing,products}.html` — enables Action #5 evaluation (does existing `detect_cross_page_banners()` cover what SimHash would?)
- **Candidate #10:** 3 multilingual parking fixtures (Cyrillic, CJK, Japanese) — closes detection coverage
- **C0.3-followup (new):** 6 conforming `soft_404/` captures with real `_RE_SOFT_404` / `_RE_EXPANDED_SOFT_404` markers (`did you mean`, `showing results for`, `no results found`, `popular searches`, `trending searches`, `people also search for`, `try a different search`). Repopulates the directory emptied by C0.3 in Week 1 Days 1-2.
- **C0.4-followup (new):** 3 conforming `empty_google_sites/` captures with real `sites-viewer-frontend` / `atari.vw.` / `normalizedPath.*view/` markers and `class="tyJCtd"` empty-content `<div>`s. Repopulates the directory emptied by C0.4 in Week 1 Days 1-2.
- **Synthetic-with-real-markers fallback policy (applies to C0.3-followup, C0.4-followup, and any future capture work):** real-domain captures are preferred. If real-domain sourcing fails (no current production examples available, persistent anti-bot blocks, or domain not in the production crawl yet), synthetic fixtures with real detector markers are acceptable substitution — same pattern as the existing 20 `*_synthetic.html` files in the corpus. Document the fallback explicitly in commit messages and (once Week 4 lands) in `meta.json` via a `capture_method: "synthetic_with_real_markers"` field. Synthetic substitution is not a permanent state; flag for re-capture in a future quarterly fixture refresh.
- Edge-case robustness fixtures:
  - 1 huge HTML fixture (>1MB) for memory/parsing stress
  - 1 tiny but legitimate fixture (<2KB, non-stub)
  - 1 malformed HTML fixture (unclosed tags)
  - 2 encoding-variant fixtures (Big5 or Shift-JIS, declared-vs-actual mismatch)

### Week 5 Deliverable

By end of Week 5:

- All 197 existing fixtures audited for conformance to directory specification
- All broken/empty/misleading fixtures replaced
- `sorted(glob)[0]` pattern eliminated from tests
- ~50 new fixtures added across hydration, mega-menu, international, multipage, edge cases
- Every fixture has `meta.json` and `expected/` outputs
- Test utilization at or near 100% (every fixture in a directory is tested)

This is the foundation everything else builds on.

---

## 4. Workstream A.0: Baseline Scaffolding (Weeks 6-7)

**Why second:** With trustworthy fixtures, baselines become meaningful. Without this scaffolding, every change in Workstreams A-E is a gamble.

### Three-Layer Baseline Architecture

1. **Unit-level fixture snapshots** — deterministic per-component behavior on each fixture
2. **Pipeline-level synthetic crawls** — deterministic end-to-end pipeline behavior on recorded "tapes"
3. **Live canary baseline** — non-deterministic real-world drift detection using `canary_50_domains.txt`

### Week 6: Snapshot Generation

Build a `barcada-baseline` CLI as a thin wrapper or extension over the W4.1.5 fixture-cascade driver (rather than a new CLI built from scratch). Per `RECONCILIATION_2026-05-21.md` §4.3 and §5.5, the cascade-driver infrastructure was implicit in W6's `barcada-baseline generate` design but became explicit at W4.1.5; W6 reuses it. Less new code is needed at W6 than the plan originally implied — the engineering surface narrows to the CLI surface, determinism normalization, and integration with the W A.0 W7 synthetic-crawl-tape capture, since the cascade-execution mechanics already exist.

Subcommand surface:

```
barcada-baseline generate --fixtures tests/fixtures/html/
```

For each fixture, runs the parser and writes:

- `expected/parser_output.json` — full parser dict, deterministically serialized
- `expected/parser_output.hash` — sha256 of canonical-serialized output
- `expected/text_extraction.txt` — extraction.py + text_cleaning.py output
- `expected/text_extraction.hash`
- `expected/barriers_verdict.json` — what barriers.py decided
- `expected/link_discovery.json` — URLs that would be enqueued

These supersede the Week 4 expected outputs with machine-generated versions (then human-reviewed before commit).

**Determinism requirements:** sorted dict keys, normalized floats (6 decimal places), canonical JSON serialization. Otherwise hashes drift on every run.

### Week 6-7: Comparison CLI

```
barcada-baseline check --fixtures tests/fixtures/html/
```

For each fixture, runs the pipeline, compares output to `expected/`, reports:

- Fixtures matching expected (count)
- Fixtures with mismatched hashes (count + diff for each)
- Exit code 0 if all match, non-zero on any mismatch

This is what runs in CI on every commit. It's also what an engineer runs locally before opening a PR.

### Week 7: Synthetic Crawl Tapes

For ~20-30 representative domains beyond the fixture set:

- Use `vcrpy` or similar to record full HTTP exchanges (request + response + headers + timing)
- Save cassettes per domain to `tests/fixtures/synthetic_crawls/<domain>/`
- Future pipeline runs replay from cassettes instead of hitting the network
- Capture baseline outcomes per domain (Stage 1 decision, costs, schema, errors)

This tests interactions between components that fixture-level tests miss.

### Week 7: Canary Wiring

```
barcada-baseline canary-run --domains canary_50_domains.txt --output canary_runs/<date>.parquet
```

Wire the unused `canary_50_domains.txt` to a scheduled job. Run weekly. Build a small trend dashboard showing per-domain agreement with last baseline run, cost per domain over time, anti-bot success rate.

### Tag Baseline-v0

After scaffolding works:

```
git tag baseline-v0 HEAD
barcada-baseline generate --fixtures tests/fixtures/html/
git add tests/fixtures/html/*/expected/
git commit -m "Capture baseline-v0 before audit remediation"
```

Every subsequent change is measured against `baseline-v0`.

---

## 5. Workstream A: Compliance Foundation (Weeks 8-9)

**Why now:** Compliance issues have legal and reputational risk. They're also cheap to address. Don't ship audit remediation without these.

### Items

**Action #2: robots.txt parser** (Severity: CRITICAL, ~300 LOC)

- Add `urllib.robotparser` based check before adding any URL to the queue in `link_discovery.py`
- Per-host cache of parsed robots.txt
- Respect `Crawl-delay` directive
- Make bypass an explicit per-domain configurable that logs an authorization marker into the cost journal
- Documentation in new `CRAWLING_POLICY.md`

**Action #12: Identifiable validator UA** (Severity: M, ~5 LOC + infrastructure)

- Change `check_domains.py:140` from `Mozilla/5.0 (compatible; Barcada/1.0)` to `BarcadaCrawler/1.0 (+https://barcada.io/crawler; crawler@barcada.io)`
- Remove the commented-out alternative on line 139 (misleading dead code)
- Create `barcada.io/crawler` page explaining the crawler
- Set up `crawler@barcada.io` mailbox with monitoring
- **Do not touch** `fetcher.py` UA rotation or `http_headers.py` deterministic-per-host selection — these are correct for their stages

**Action #9: Author governance documents** (1 day total)

- `ARCHITECTURE.md` — system structure, indexes into existing `docs/PIPELINE.md`, `docs/vmss_orchestrator_plan.md`, etc.
- `CRAWLING_POLICY.md` — robots.txt compliance, rate limits, AUP, identification policy, CAPTCHA policy (default skip), data retention
- `FAILURE_PATTERNS.md` — catalog of known failure modes and their remediations

**Anti-pattern cleanup**

- Fix bare `except Exception:` in `scraper/renderer.py:196-197` (blocks SPA failure taxonomy work in Workstream C)
- Move large data artifacts out of `scripts/` (5MB+ JSON files bloat the repo)

### Validation

Every change in Workstream A runs against baseline-v0:

```
barcada-baseline check --fixtures tests/fixtures/html/
```

Zero regressions on any fixture. Workstream A changes are mostly additive (robots.txt is a new check, UA changes affect only the validator path) so regressions should be rare.

---

## 6. Workstream B: Cost & Observability Foundation (Weeks 10-12)

**Why now:** Without these, all subsequent changes are flying blind. You can't know if Workstream C extraction improvements increased cost. You can't know if drift is occurring.

**Phase 4 note (added per `RECONCILIATION_2026-05-21.md` §6.1 Edit 7):** PR-COST has landed concurrent with Workstream 0 (cost journal enforcement + RUN_ID + single-tenant guard + list-runs CLI at HEAD `5513b4c6`). Several W B items — cost-per-useful-record (Action #6), per-domain budgets (Action #8), structured JSON logging (Action #16) — build on the PR-COST journal extensions rather than coordinating with a parallel refactor. The framing here changes from "Phase-4-collision-heavy" to "Phase-4-aligned"; the per-stage `cost_ceiling_stopped` / `cost_ceiling_global` outcomes and `RUN_ID` propagation are already in parquet. See `~/crawler-audit/working/phase4_status_2026-05-21.md` for PR-COST surface detail.

### Items

**Action #6: Cost-per-useful-record metric** (~50 LOC)

- Add `useful_records_count` and `cost_per_useful_record` to `PhaseSummary` dataclass in `phase_summary.py`
- Extend `compute_phase_summary` to read Stage 1 parquet output and count `is_business == True`
- Decide on null handling (abstained records): exclude from denominator, or count as not-useful
- "Useful record" definition should account for the `cost_ceiling_stopped` and `cost_ceiling_global` outcomes already in the parquet schema per PR-COST. Records emitted under these outcomes are not "useful" in the cost-effectiveness sense (the pipeline halted early); exclude them from the useful_records_count numerator. Document the definition explicitly in `compute_phase_summary`.
- This unlocks Section 14.7 cost discipline downstream

**Action #21: Version stamping** (~50 LOC)

- Add `crawler_version`, `policy_version`, `taxonomy_version` alongside existing `feature_schema_version`
- Stamp on every emitted record
- Schema bump (explicit, deliberate)
- Documented in `CHANGELOG.md`

**Action #7: Efficiency-flag catalog** (~150 LOC)

- Add 11-flag enum to a new `efficiency_flags.py`:
  - `RENDERED_WITHOUT_HYDRATION_ATTEMPT`
  - `TIER_OVER_ESCALATION`
  - `EXCESSIVE_PAGE_CRAWL`
  - `LOW_USEFUL_RECORD_RATE`
  - `LLM_OVERUSE`
  - `CACHE_MISS_RATE_HIGH`
  - `RENDER_TIMEOUT_PATTERN`
  - `RETRY_LOOP_DETECTED`
  - `BOILERPLATE_NOT_CACHED`
  - `DUPLICATE_PAGE_CRAWLED`
  - `OVER_BUDGET_WITHOUT_OVERRIDE`
- Emit per-record where applicable
- Roll up in `phase_summary.py`

**Action #8: Per-domain budgets** (~250 LOC)

- Extend `BandwidthTracker` to support per-domain budgets alongside per-stage budgets
- Add `max_pages`, `max_render_seconds`, `max_proxy_mb`, `max_llm_tokens`, `max_total_cost_usd`, `hard_kill_at` to a new domain-tier YAML (HIGH/STANDARD/LOW)
- Enforce in `cost_tracker.py` and `bandwidth_tracker.py` reusing the existing `kill_at_fraction` pattern
- Hook into existing `_attribute_fetch_cost`

**Action #3: Persistent strategy cache** (~200 LOC)

- Add per-domain Parquet or SQLite cache: `last_successful_tier`, `failed_tiers`, `last_failure_at`, `next_retry_after`
- Read at `promotion.py:assign_initial` to skip wasted T1 retries
- Write at end of each shard

**Action #16: Structured JSON logging** (~150 LOC)

- Replace `logging.basicConfig` with `python-json-logger` or equivalent
- Inject `run_id`, `shard_id`, `domain`, `stage` as structured fields via `LogRecord` extras
- `run_id` already exists in the cost journal — propagate it through logging
- Use `LoggerAdapter` for context propagation

**Action #17: Metrics emission** (~250 LOC)

- Prometheus or OpenTelemetry integration
- Per-stage counters and histograms
- Per-tier byte gauges
- Per-provider latency histograms
- Define alert thresholds (cost overrun, quality regression, drift) — documented in `docs/alerts.md`

### Validation

Each item runs against baseline-v0 + previous Workstream A changes. Specific things to watch:

- Cost-per-useful-record: schema bump, expected outputs need regeneration for fixtures with Stage 1 outcomes
- Version stamping: schema bump, expected outputs need regeneration
- Per-domain budgets: should not change behavior on fixtures (synthetic crawls are too small to hit budgets)
- Strategy cache: first run from cold cache should match baseline-v0; subsequent runs may differ (this is expected and acceptable)

---

## 7. Workstream C: High-Leverage Extraction (Weeks 13-16)

**Why now:** The highest-impact extraction improvements, gated on fixtures (Workstream 0), baseline (Workstream A.0), and observability (Workstream B) being in place.

### Items

**Action #1: SPA hydration extraction** (~200 LOC)

- New module `scraper/hydration_extractor.py`
- Framework detection from initial HTML (Next.js, Nuxt, Vue, Angular, Svelte, Remix, Gatsby)
- Payload extraction for each: `__NEXT_DATA__`, `window.__NUXT__`, `__APOLLO_STATE__`, `__PRELOADED_STATE__`, `__remixContext`, `data-sveltekit-fetched`
- Integrated into renderer before falling back to Playwright DOM scraping
- Where payload exists, emit structured data alongside (or instead of) DOM extraction
- Validated against the new `spa_hydration_*/` fixtures from Workstream 0

**Action #4: Network request interception** (~200 LOC)

- Extend `_route_handler` in `renderer.py` to log XHR/fetch URLs alongside its existing blocking behavior
- Capture into per-domain `discovered_apis.json`
- Subsequent crawls of the same domain can replay discovered APIs directly via HTTP instead of re-rendering
- Cost: significant render-cost reduction for API-driven SPAs

**Action #13: Mega-menu activation** (~200 LOC)

- Add hover/click/focus sweep for `aria-haspopup` and `aria-expanded` triggers in `renderer.py`
- Recursive activation up to 3-4 levels deep
- Desktop viewport (1440px) sweep + mobile viewport (375px) sweep
- Capture activated DOM and merge into menu extraction output
- Validated against the new `mega_menu/` fixtures

**Action #11: HTML→Markdown via Trafilatura** (~5-50 LOC)

- Set `output_format="markdown"` in `_TRAFILATURA_KW` in `extraction.py`
- Decide: global change (all consumers get markdown), or branched (LLM path gets markdown, LR-feature path stays plain text)
- Branched is cleaner but more code; global is simpler if `ml_text` doesn't come from Trafilatura output
- **Coordinates with Phase 4 PR-E** if PR-E ever opens (see `RECONCILIATION_2026-05-21.md` §6.1 Edit 8). PR-E measures classifier accuracy on production text and decides Levers 2/3/7; if PR-E lands first, Action #11 may need re-validation against PR-E's lever decisions (the cascade composition under post-Lever-2/3/7 inputs is different from the current cascade). PR-E is blocked on Phase 4 PR-D operator-led labeling, which is not currently scheduled — so this coordination is conditional, not gating.

**Action #5: Boilerplate fingerprinting evaluation** (deferred until eval complete)

- Compare existing `detect_cross_page_banners()` against SimHash/MinHash on the new `multipage_boilerplate/` fixtures
- If existing detector covers what SimHash would catch → close the audit finding as "implemented differently, sufficient"
- If SimHash adds meaningful recall → add ~250 LOC for the augmentation
- Severity already downgraded from H to M

**Action #10: BreadcrumbList extraction** (~50 LOC)

- Extend JSON-LD walker in `parser.py:4456-4831` to recognize `@type: BreadcrumbList`
- Emit as `crawl_meta.breadcrumb_trail`
- Provides cleanest section-intent signal

### Validation

Workstream C changes affect extraction output substantially. Every change requires:

- `barcada-baseline check` — expect diffs on relevant fixtures
- For each diff, classify as Improvement / Neutral / Regression
- Regenerate expected outputs only after operator confirms changes are intentional improvements
- Synthetic crawl comparison: classification outputs should not flip for previously-passing domains (cost may decrease, which is fine)

The risk profile of Workstream C is high. Trust the baseline.

---

## 8. Workstream D: Compliance Hardening (Weeks 17-19)

**Why now:** Regional policy and version stamping work depends on per-domain crawl history from Workstream B. Also depends on international fixtures from Workstream 0.

### Items

**Action #20: regional_policy.json** (~200 LOC + JSON config)

- Encode GDPR (EU), CCPA (California), LGPD (Brazil), PIPL (China) field-level rules
- Check policy before emit at `parquet_writer`
- Map TLDs and IP geolocation to applicable jurisdiction
- Validated against `international_business/` fixtures from Workstream 0

**Action #14: Sitemap.xml + canonical URL extraction** (~200 LOC)

- Add `sitemap_index.xml` parser at link-discovery time
- Add `<link rel="canonical">` reader to `parser.py`
- Use canonical for URL deduplication

**Action #22: Content-hash dedup at queue level** (~30 LOC)

- Compute `sha256(html_body)[:16]` per fetch (you already compute content hashes elsewhere — extend the pattern)
- Suppress duplicate-content URLs from the queue
- Reuses existing hashing infrastructure

**Action #15: Region-aware proxy routing** (~150 LOC)

- Add `region` field to `ProxyProvider.proxy_url(region=...)`
- Map TLD → preferred region (existing TLD→Accept-Language map in `fetcher.py:_ACCEPT_LANGUAGE_BY_TLD` is a starting point)
- Reduces geo-block rate on EU/JP/CN sites

### Validation

Workstream D is mostly additive (new fields, new checks). Existing fixtures should not regress. International fixtures should now produce the expected region routing and policy emit behavior.

---

## 9. Workstream E: Quality Infrastructure (Weeks 20+, Ongoing)

**Why ongoing:** These items tighten the quality feedback loop but don't gate other work. Implement as capacity allows.

### Items

**Action #25: CI regression gate** (1 day)

- Extend `.github/workflows/python-package.yml` with a `barcada-baseline check` step
- Fail PRs on regressions against `baseline-v0` (or current accepted baseline)
- Fail on schema drift not accompanied by version bump

**Action #24: Acceptance metric formula** (~60 LOC)

- Write `eval/acceptance_criteria.yaml` with explicit thresholds: `stage1_f1_min: 0.92`, `stage1_per_intent_recall_min: 0.85`, etc.
- Read in `metrics.py:compare` and exit non-zero on threshold violation
- Turn "manual interpretation" into a CI gate

**Action #18: Drift detection daemon** (~300 LOC)

- Schedule nightly re-crawl of `canary_50_domains.txt` via Azure Timer Trigger or cron
- Compute per-domain diff vs. last good baseline run
- Alert on regression > threshold
- Wire to the metrics dashboard from Workstream B

**Action #28: Failure clustering automation** (~300 LOC, defer until volume grows)

- Read results parquet, extract features (HTTP status, render mode, missing field, body size, framework)
- Cluster via DBSCAN or k-means
- Emit `failure_clusters.json`
- Currently manual analysis in `tools/phase4_cost_reduction_directive.md` is sufficient

**Action #23: Render-result cache** (~200 LOC)

- Cache by (url, viewport, locale)
- Parquet-backed
- TTL keyed on per-domain `re_crawl_frequency`

### Deferred or Skipped

The following audit actions are deferred indefinitely under current product scope:

- **Action #26: TLS-fingerprint-spoofing client** — defer until specific JA3/JA4 failures observed in block-detection logs
- **Action #27: Per-locale path-dictionary scaffold** — defer; English-first product
- **Action #29: HTTP/2 frame-order awareness** — defer until specific failures observed
- **Action #30: Microdata + Twitter Card extraction** — defer until evidence that target B2B sites use these without JSON-LD

The Section 9 items (label-to-intent matching cascade) are N/A under current product scope — barcada-scraper classifies domains to categories, not nav labels to intents.

---

## 10. Candidate Fixtures Reference

The 9 highest-priority fixtures pursued from the fixture audit (the audit identified 10; PII fixtures are excluded per scope decision):

### CRITICAL (blocks Workstream C)

1. **3 Next.js hydration fixtures** in `spa_hydration_next/`
   - CSR-only variant: `__NEXT_DATA__` with `runtimeConfig` but minimal `props`
   - ISR variant: `__NEXT_DATA__` with both `props.pageProps` and revalidation markers
   - Full-SSR variant: `__NEXT_DATA__` with complete `props.pageProps` data
   - Source: any modern Next.js-powered SaaS marketing site (verify with `view-source:` and search for `__NEXT_DATA__`)

2. **2 Nuxt hydration fixtures** in `spa_hydration_nuxt/`
   - One with inline `window.__NUXT__`
   - One with `<script id="__NUXT_DATA__">`

3. **2 Apollo + 2 Redux hydration fixtures** in `spa_hydration_apollo/` and `spa_hydration_redux/`
   - Apollo: `__APOLLO_STATE__` with normalized cache
   - Redux: `__PRELOADED_STATE__` with multiple reducers

### HIGH (blocks Workstream A, D)

4. **5 modern SaaS legitimate_business fixtures** in `legitimate_business/`
   - With hreflang, canonical, JSON-LD Organization schema
   - Different industries: fintech, healthtech, devtools, vertical SaaS, services
   - Closes the 60-pp production-coverage gap

5. **6 international-TLD fixtures** in `international_business/<locale>/`
   - 2× .de (Germany)
   - 2× .jp (Japan)
   - 1× .fr (France)
   - 1× .com.br (Brazil)
   - Unblocks Action #20 (regional policy) and per-locale eval

6. **3 mega-menu fixtures** in `mega_menu/`
   - With `aria-haspopup` triggers
   - Multi-column nested `<ul>` panels
   - At least one with mobile hamburger menu variant
   - Unblocks Action #13

### HIGH (blocks Workstream C, D)

7. **20 multipage boilerplate fixtures** in `multipage_boilerplate/<domain>/`
   - 5 domains × 4 pages each (home, about, pricing, products)
   - Enables Action #5 evaluation: does existing `detect_cross_page_banners()` cover SimHash use cases?

8. **6 soft_404 replacement fixtures** replacing the 14 broken fixtures
   - Real "search results" or "did you mean" or "showing results for" pages
   - Real "no results found" pages
   - Must contain markers from `_RE_SOFT_404` / `_RE_EXPANDED_SOFT_404`

### MEDIUM (cheap, closes detection coverage)

9. **3 multilingual parking fixtures** in `parking_multilingual/<script>/`
    - Cyrillic, CJK, Japanese variants
    - Detector handles these but no fixture exercises them today

### Each fixture requires

Per Workstream 0 Week 4:

- `<domain>.html` — the capture
- `<domain>.meta.json` — provenance (source URL, capture date, content-type, expected outcome)
- `expected/<domain>.json` — expected pipeline outputs (parser, barriers, classifier)

---

## 11. Risk Register

Risks worth tracking through the remediation:

### Concurrent operator activity

Both audits flagged git state changes during the audit window due to concurrent labeling work. This is acceptable for audits but **must not occur during baseline regeneration**. Establish a "baseline lockout" protocol: when regenerating expected outputs, no other commits to the repo.

### Fixture refresh decay

Fixtures captured April 25, 2026 will become stale over time. Anti-bot defenses change, framework versions change, page structures change. Plan for **quarterly fixture refresh** — re-capture a sample and check for conformance drift.

### Schema bumps cascade

Adding `useful_records_count`, `crawler_version`, `policy_version`, `taxonomy_version`, `efficiency_flags` all bump the schema. Expected outputs need regeneration with each bump. Plan schema bumps deliberately (batch them per workstream rather than scattered).

### LLM cost drift during baseline regeneration

Generating expected outputs requires running the full pipeline through fixtures, which exercises the classifier cascade including LLM calls. Budget for ~$50-200 of LLM cost during Week 4 of Workstream 0 for expected-output generation. After that, fixture tests use cached expected outputs and don't make LLM calls.

### `_load_training_data` `NotImplementedError`

Per the original audit's anti-patterns section, the train/serve mismatch gate is conceptual rather than enforced. This is honest deferment per `DEFERRED_WORK.md` but is a hidden risk. Decide explicitly: implement the gate during Workstream B (alongside version stamping), or downgrade the guarantee in `CHANGELOG.md`. Don't leave both options open.

### Production-canary distribution shift

The fixture audit found production canary at 2% parking, 68% "ok". If the canary's domain mix shifts (different vintage of zone-file inputs, different ad-hoc additions), the production-vs-fixture comparison breaks. Document the canary's source and version.

### Recapture tooling needs retry policy (new, lesson from C0.5d → C0.5d-followup, 2026-05-19)

Single-attempt curl is insufficient diagnostic when assessing whether a TLS or connection failure is persistent vs transient. During C0.5 audit, `sanmarcosflowershop.com.html` was initially "accepted with notes" based on one curl exit-35 (TLS internal error); subsequent diagnostic (3-attempt retry probe + openssl handshake verification) showed the failure rate was ~30% on a single attempt and the underlying TLS handshake actually works fine, prompting a follow-up replacement (C0.5d-followup, commit a156727).

**Mitigation for future capture work:** any future capture or recapture tooling (Week 2 SPA hydration captures, Week 3 international and SaaS captures, Week 5 `soft_404`/`empty_google_sites` repopulation, audit C22 nonprofit expansion, and the Week 4 `scripts/fixtures/regenerate_expected.py` script) must implement retry-on-connection-error policy (≥3 attempts with exponential backoff on TLS, DNS, connection-reset, and timeout failures) before drawing a persistence conclusion. This mirrors the production crawler's existing exponential-backoff retry pattern in `fetcher.py:316-318` and ensures fixture corpus health decisions are grounded in stable diagnostics rather than transient network conditions.

### Phase 4 infrastructure half landed concurrently with Workstream 0 without plan absorption (new, Session 12 reconciliation 2026-05-21)

The plan as originally authored (against audit-state code at HEAD `be71d536`) did not anticipate that the Phase 4 infrastructure half (PR-COST, PR-A, PR-B, PR-C per `docs/phase4_implementation_plan.md`) would land concurrently with Workstream 0's read-only period. By Session 12 open, current code (HEAD `5513b4c6`) was audit-state plus four landed Phase 4 PRs, and the plan-vs-code drift surfaced when Session 12 attempted to begin W4.2.

**Resolution:** The read-only-period discipline (per plan §14 and operator memory) was broken with explicit operator authorization for a one-time absorption of `RECONCILIATION_2026-05-21.md` into this plan. See `~/crawler-audit/RECONCILIATION_2026-05-21.md` for the full reconciliation framing, §3 for the drift's core misalignment, and §6.1 for the eleven coordinated plan amendments (including this entry). The locked artifacts list at §14 has been updated to clarify that the plan was authored against audit-state code; future sessions reading the plan should understand this distinction.

**Forward-applicable mitigation:** If new in-repo development sequences (Phase 4 PR-D through PR-G, or any successor multi-PR initiative) begin landing during a future Workstream 0–E read-only period, escalate before the work compounds. The audit-state ↔ current-code distinction should be stated explicitly in any future plan amendment that absorbs in-flight code changes.

### W4.2 expected-output lifetime constrained (new, Session 12 reconciliation 2026-05-21)

W4.2 expected/<domain>.json outputs produced under the cascade composition at HEAD `5513b4c6` (current code: audit state + landed Phase 4 PR-COST/A/B/C, with Levers 2/3/7 NOT applied — Stage 2 still two-pass with `gpt-4.1-mini` classifier, Stage 3 primary still `gpt-4.1`) have a plan-aware shorter-than-original-design lifetime. Output is valid until:

1. **W A.0 W6 supersedes** via baseline-v0 generation through the `barcada-baseline` CLI (which wraps the W4.1.5 fixture-cascade driver per §4 W6), OR
2. **Phase 4 PR-E lands** and Levers 2/3/7 change cascade behavior post-Lever-2/3/7 (which would invalidate cascade-output values across the corpus),

whichever comes first.

The META_SCHEMA prose-only fix register at `SESSION_TRANSITION_TEMPLATE.md` "Deferred prose-only fixes" tracks the durability annotation (item (f)) for fold-in at the next real META_SCHEMA semver bump per LESSONS.md "Defer prose-only schema fixes" pattern. The constraint is plan-aware, not surprise — surfaces explicitly so future-session expectations don't outrun the cascade composition the outputs were generated under.

### Phase 4 measurement half blocked on operator-led labeling (new, Session 12 reconciliation 2026-05-21)

Phase 4 PR-D (operator-led Stage 2 + Stage 3 labeling, prerequisite to PR-E lever validation, PR-F Lever 4 parser pre-classifier, and PR-G smoke + final docs) requires operator-led Stage 2 + Stage 3 labeling activity. Current operator labeling work is Stage 1 only (per the parallel labeling session referenced in workspace coordination). Stage 2 + Stage 3 labeling is NOT currently scheduled.

**Plan does not commit to a Phase 4 ship date.** If Stage 2/3 labeling never opens, Phase 4 PR-D/E/F/G remain unstarted indefinitely, and the architecture rationale document's target state (`~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md`) is not reached. The Workstream 0–E sequence closes against current code state regardless; the dependency map at `RECONCILIATION_2026-05-21.md` §4.1 / §4.2 details which Workstream 0–E units are Phase-4-independent, Phase-4-influenced, and Phase-4-aligned.

If Stage 2/3 labeling does eventually open and the measurement half progresses, W4.2 expected outputs and (if generated) the W A.0 W6 baseline-v0 will need regeneration on PR-E close.

---

## 12. Success Criteria

How to know the remediation is working:

### Quantitative metrics

- **Fixture utilization:** >95% of fixtures referenced by at least one test (was 7%)
- **Directory conformance:** 100% of fixtures conform to their directory specification (was 0% for `soft_404/` and `empty_google_sites/`)
- **Test coverage:** Coverage report shows >80% for `scraper/`, `classifier/`, `detection/`, `page_acquisition/` modules
- **Cost-per-useful-record:** Tracked as a first-class metric, with month-over-month trends visible
- **Block-rate per tier:** Tracked per fetch tier, with alerts on degradation
- **Drift detection:** Weekly canary runs produce < 5% per-domain agreement drift over 4 consecutive weeks

### Qualitative checks

- A new engineer can read `ARCHITECTURE.md` and understand the pipeline in 30 minutes
- A site operator can reach the team via `crawler@barcada.io` and get a response within 2 business days
- A robots.txt `Disallow: /` for a domain results in zero crawl activity for that domain within 24 hours
- An SPA-heavy domain (>50% of target pages requiring rendering) has hydration extraction succeed for >70% of pages
- A new audit finding can be reproduced by a Claude Code session reading `AUDIT_REPORT.md` + `FIXTURE_AUDIT_REPORT.md` + this plan

### Re-audit cadence

- **Quarterly fixture refresh** (capture new fixtures, check for conformance drift)
- **Semi-annual full audit** re-run (against the current Top 30 framework)
- **Annual scope review** (does the framework still match what barcada-scraper does?)

---

## 13. Appendix: Reference to Source Documents

- `~/crawler-audit/AUDIT_REPORT.md` — Original code audit, 798 lines, 30 prioritized actions
- `~/crawler-audit/FIXTURE_AUDIT_REPORT.md` — Fixture audit with conformance findings and 10 candidate fixtures
- `~/crawler-audit/AUDIT_DIRECTIVE.md` — Read-only audit directive that generated AUDIT_REPORT.md
- `~/crawler-audit/FIXTURE_AUDIT_DIRECTIVE.md` — Read-only fixture audit directive
- Spot-check verifications: documented in chat history, surfaced UA rotation existed, `detect_cross_page_banners()` existed, content hashing was pervasive
- `docs/phase4_implementation_plan.md` — in-repo source for the Phase 4 eight-PR cost-reduction and infrastructure sequence (cited by `AUDIT_REPORT.md` line 111). PR-COST, PR-A, PR-B, PR-C landed pre-Session-12 at HEAD `5513b4c6`; PR-D, PR-E, PR-F, PR-G unstarted and gated on operator-led labeling.
- `~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md` — design-of-record for unimplemented work; describes the post-Phase-4 target state (Stage 1 three-tier cascade, Stage 2 post-Lever-3 single-pass, Stage 3 two-pass with Pass 2b off). Do NOT use as source-of-truth for current code claims — current code is closer to `AUDIT_REPORT.md` §8 discovered architecture, modified by the four landed Phase 4 PRs.
- `~/crawler-audit/RECONCILIATION_2026-05-21.md` — Session 12 reconciliation document. Identifies and resolves the plan-vs-current-code drift surfaced when W4.2 was attempted. Authorizes the eleven §6.1 plan amendments absorbed in this revision. Historical record; not a governing document.
- `~/crawler-audit/working/phase4_status_2026-05-21.md` — Claude Code source-verification report (Phase 4 per-PR implementation status, 2026-05-21).
- `~/crawler-audit/working/phase4_current_state_2026-05-21.md` — Claude Code source-verification report (Levers 2/3/7 current state + W4.2 cost envelope ~$0.30, 2026-05-21).
- `~/crawler-audit/working/stage3_input_shape_2026-05-21.md` — Claude Code source-verification report (Stage 3 input contract: three upstream parquets + four T3 path fetches per domain; fixture-input adapter sub-option analysis).

For Claude Code prompts implementing specific actions, draft per-workstream prompts that reference this plan and the audit reports as context. Each prompt should:

1. State which workstream and action(s) it implements
2. Reference the relevant section of this plan
3. Specify acceptance criteria (baseline regression checks, fixture conformance, etc.)
4. Constrain scope (which files may be modified, which tests must pass)
5. Require regeneration of expected outputs when schema bumps occur

---

## 14. Session Continuity Discipline

A 20-week remediation executed across many Claude Code sessions requires explicit continuity discipline. Without it, each session reinvents wheels, loses prior decisions, and risks contradicting earlier operator choices. This section documents the artifacts, updating cadence, and transition mechanics that hold the work together.

### Durable artifacts

The team relies on a fixed set of documents and references. Treat these as authoritative; reconstruct nothing from memory.

**Workspace (`~/crawler-audit/`):**
- `AUDIT_REPORT.md` — code audit, 30 prioritized actions. Read-only; never edited after the fact.
- `FIXTURE_AUDIT_REPORT.md` — fixture quality audit, 10 candidate fixtures. Read-only.
- `CLASSIFICATION_ADJACENT_PLAN.md` — classification-adjacent items for AI/ML review. Updated only when AI/ML decisions land.
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` — this file; the operational plan. UPDATED inline as decisions land.
- `SESSION_LOG.md` — append-only chronological session log. Updated at end of each session/work unit.
- `LESSONS.md` — append-only forward-applicable patterns surfaced during the work. Updated as patterns are named.
- `SESSION_TRANSITION_TEMPLATE.md` — template filled out at session-end for the next session to read first.
- `AUDIT_DIRECTIVE.md`, `FIXTURE_AUDIT_DIRECTIVE.md` — historical directives used to produce the audit reports. Read-only.
- `README.md` — workspace overview.
- `PIPELINE_ARCHITECTURE_TARGET_STATE.md` — design-of-record for unimplemented work; describes the post-Phase-4 v1 target state. Read-only; do NOT treat as source-of-truth for current code claims.
- `RECONCILIATION_2026-05-21.md` — Session 12 reconciliation document. Archival historical record of the plan-vs-current-code reconciliation absorbed into this plan via §6.1; not a governing document.
- `working/phase4_status_2026-05-21.md`, `working/phase4_current_state_2026-05-21.md`, `working/stage3_input_shape_2026-05-21.md` — Claude Code source-verification reports underlying the reconciliation. Referenced by SESSION_LOG.md Session 12 entry.

**Repo (`~/projects/barcada-scraper/`):**
- Annotated git tags: `pre-remediation-2026-05-19` (nuclear-revert anchor), `baseline-v0` (Week 7, single tag at post-expected-outputs commit), and future workstream tags as agreed.
- Commit messages on `main` — each commit cites its action number (C0.1, C0.2, …) and serves as durable record. The git log IS part of the persistence; commit message bodies are the canonical "what and why."
- `CLAUDE.md`, `.claude/rules/*.md` — operator preferences and code rules. Honored every commit.
- `docs/phase4_implementation_plan.md` — in-repo governance reference for the Phase 4 eight-PR sequence. Do NOT modify under any circumstance until Phase 4 PR-D/E/F/G sequencing is operator-authorized.

**Locked artifacts (do not modify under any circumstance):**
- All of `eval_data/` — labeling-workstream territory (including `canary_50_domains.txt`, read-only consumable for Workstream A.0 canary wiring).
- `stage1.schema.json` v1.0 with 49 keywords — schema evolution is a labeling-workstream decision, post-Stage-3-completion, as a v1.1 event.
- The `pre-remediation-2026-05-19` tag — operator-created, do not retag or move.

**Plan-authoring context (Session 12 reconciliation, 2026-05-21):** This plan was originally authored against audit-state code (HEAD `be71d536`). Current code (HEAD verified 2026-05-21 at `5513b4c6`) is audit-state plus four landed Phase 4 PRs (PR-COST, PR-A, PR-B, PR-C per `docs/phase4_implementation_plan.md`). Future sessions reading the plan should understand this distinction: §1 "Where the crawler is genuinely strong" and §1 "Where the gaps are real" reflect the current-code framing post-PR-COST/A/B/C, but the plan body (Workstream 0–E) was scoped against audit-state and reconciled through `RECONCILIATION_2026-05-21.md` §3 (drift framing) and §6.1 (eleven amendment deltas absorbed in this revision). See §11 Risk Register entry "Phase 4 infrastructure half landed concurrently with Workstream 0 without plan absorption" for the resolution record.

### Updating discipline

| When | What to update | Why |
|---|---|---|
| Operator approves a decision | This plan (inline section update) + `SESSION_LOG.md` entry | Decisions decay if not recorded |
| A commit lands on `main` | `SESSION_LOG.md` (commit SHA + scope, in the current session entry) | Future sessions need a quick map of "what shipped" |
| A discovery contradicts the plan | This plan (revision) + `SESSION_LOG.md` (discovery flagged) + the commit message of the resolving commit | Step 6 discovery escalation requires durable record in three places |
| A risk materializes or a forward-applicable lesson is captured | §11 Risk Register + `SESSION_LOG.md` | Lessons must be visible to all future capture/code work, not just the session that learned them |
| A workstream begins or ends | `SESSION_LOG.md` entry + this plan's workstream status update | Mark progress against the 20-week plan |
| A session opens or closes | `SESSION_LOG.md` (new entry on open; close summary on close) + fill out `SESSION_TRANSITION_TEMPLATE.md` on close | Establish continuity context |

Never update:
- `AUDIT_REPORT.md` or `FIXTURE_AUDIT_REPORT.md` — these are point-in-time audits; their value is preservation.
- Older `SESSION_LOG.md` entries — corrections go in a new entry; old entries are historical.
- The `pre-remediation-2026-05-19` tag.

### Context-window awareness pattern (Claude Code)

Claude Code sessions have finite context. Larger contexts increase compaction risk and per-turn cost. To keep work reliable across sessions:

**Self-monitoring cadence (proactive, not on request):**
- Report estimated context usage at ~20%, ~40%, ~60% of available window.
- Report format: rough % used, recommendation (continue / transition), one-paragraph rationale.

**Transition triggers (any one is sufficient):**
- Context usage crosses ~50-60%.
- Natural workstream boundary reached (end of Workstream 0 Week 1; end of Workstream A; etc.).
- The work unit's character changes substantially (fixture cleanup → live capture work; documentation → code refactor; static fixtures → SPA hydration captures).
- Operator explicitly requests transition.

**Anti-patterns to avoid:**
- Mid-commit-batch transitions. Always finish in-progress sub-commits before handing off.
- "I have plenty of room" optimism without measurement.
- Carrying decisions in conversation memory instead of writing them to durable artifacts.
- Re-deriving state from full document re-reads when `SESSION_LOG.md` would summarize it in 30 seconds.

### Transition mechanics

When a session ends or transitions to a new one:

1. **Wrap in-progress work.** Finish any in-flight sub-commits and reach a clean git state. No half-done commits, no orphaned working-tree changes. If a sub-commit is mid-way and time is short, finish it; do not stop in the middle.
2. **Update `SESSION_LOG.md`.** Add or close the current session's entry with:
   - Final state (commits produced, workspace updates, decisions recorded)
   - Open items (what's queued for the next session)
   - Any operator decisions made that aren't yet in the plan body
3. **Fill out `SESSION_TRANSITION_TEMPLATE.md`** for the next session. The template captures:
   - Last commit SHA on repo `main`; last commit on workspace `main`
   - Active task list state
   - Outstanding operator decisions blocking the next work unit
   - Locked artifact reminders
   - Next concrete work unit (action ID + scope + acceptance criteria)
4. **Push everything.** Workspace commits to workspace origin; repo commits to repo origin. The next session reads from origin, not from local working trees.
5. **Tag at workstream boundaries** (optional but useful): `git tag workstream-0-week1-end <sha>` etc. Tags supplement `SESSION_LOG.md`; they don't replace it.

A new session starts by:
1. Reading `SESSION_TRANSITION_TEMPLATE.md` (current handoff state).
2. Reading the latest entry of `SESSION_LOG.md`.
3. Reading only the relevant section of this plan for the next work unit (not the whole plan).
4. Verifying repo state: `git -C ~/projects/barcada-scraper status` matches the transition template's "last commit SHA."
5. Verifying workspace state: same for `~/crawler-audit/`.
6. Picking up at the action ID specified in the transition template.

The aim: a Claude Code session opened cold should be productive within ~10 minutes of reading.

---

*End of remediation plan. Living document — update as workstreams complete and findings evolve.*
