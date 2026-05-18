# Fixture Quality Audit — Read-Only

## Critical Constraints

This is a READ-ONLY audit of fixture quality. Same constraints as the original
audit: no modifying any file in the repository. The only writes are to the
workspace at ~/crawler-audit/.

REPO_PATH: /Users/administrator/projects/barcada-scraper
WORKSPACE: ~/crawler-audit/
OUTPUT: ~/crawler-audit/FIXTURE_AUDIT_REPORT.md
WORKING NOTES: ~/crawler-audit/working/ (optional, use if needed for
checkpointing during the audit, but do not produce as deliverables)

## Core Insight to Apply Throughout

**Fixture directory names are not arbitrary categories — they are
specifications of what code path the fixture is supposed to test.**

For example:
- `cloudflare_challenge/` → fixtures here should trigger Cloudflare
  challenge detection in barriers.py
- `parking_godaddy_template/` → fixtures here should trigger the
  GoDaddy parking template detector in placeholder.py
- `soft_404/` → fixtures here should trigger soft_404 detection
- `legitimate_business/` → fixtures here should classify as is_business=true
- `spa_shell/` → fixtures here should trigger empty-SPA detection

Therefore, a CORRECT fixture is one that actually triggers the code path
its directory name implies. A fixture that does not trigger the expected
code path is either misclassified, stale, or broken — and should be flagged.

This is the central test of fixture quality throughout the audit.

## What you MAY do
- Read any file under REPO_PATH (fixtures, source code, configs, schemas,
  parquet files via pyarrow read APIs only — see Step 9)
- Run read-only git commands
- Read existing test files to determine fixture references
- Parse HTML with read-only tools (grep, awk, sed without -i, wc, head, tail)
- Use Python only for reading parquet files in Step 9, and only in
  read-only mode (no writes back, no execution of project code)

## What you MUST NOT do
- Modify, create, delete, or rename any file under REPO_PATH
- Run pytest, the scraper, the classifier, or any project code that
  imports the package (avoid __pycache__ writes)
- Install dependencies
- Make network requests (no live site comparisons)
- Use sudo

## Process

### Step 1: Handshake
a. State the fixture root path you will audit.
b. State the production parquet paths you will sample in Step 9 (ask the
   operator to provide these if not obvious from the repo).
c. Confirm you will not modify any fixture file or run any project code.
d. Acknowledge the "filenames are specifications" core insight.
e. Wait for operator confirmation.

### Step 2: Fixture Inventory

For each subdirectory under `tests/fixtures/html/`:
- Count of HTML files
- Total bytes
- Size distribution (min, p25, median, p75, max)
- File modification date range (confirm: April 25, 2026 is the capture date
  per operator)
- Presence of `expected/`, `meta.json`, `README.md` subdirectories or files
- List of file basenames (so the directory's contents are recorded)

### Step 3: Directory-Name-Implied Specification

For each fixture directory, determine the implied test specification:

a. Read the directory name and parse its intent. E.g., `cloudflare_challenge`
   implies "should trigger Cloudflare challenge detection."

b. Locate the code path in the codebase that implements that detection:
   - For barrier-style names: search barriers.py for matching detection
     functions or signature patterns
   - For parking variants: search placeholder.py for matching template
     detectors
   - For legitimate_*: search classifier/stage1/ for what is_business=true
     decisions require
   - For structural names (spa_shell, soft_404, etc.): find the relevant
     detector or extractor logic

c. Record for each directory:
   - Implied specification (what code path it should exercise)
   - Location of that code path (file:line)
   - Detection signature or markers the code path looks for
   - The "expected outcome" if a fixture in this directory is correct

This produces a table mapping directory → code path → detection signature.

### Step 4: Fixture-Spec Conformance Check

For each fixture HTML file in each directory:

a. Read the HTML content.
b. Check whether it contains the detection signature implied by its
   directory (from Step 3).
c. Classify each fixture as:
   - CONFORMS: contains the expected signature; would trigger the expected
     code path
   - DOES NOT CONFORM: missing the expected signature; would not trigger
     the expected code path
   - AMBIGUOUS: signature partially present or unclear

d. For DOES NOT CONFORM and AMBIGUOUS fixtures, attempt to identify what
   code path they would actually trigger (if any). They may belong in
   a different directory.

This is the central output of the audit. A directory where most fixtures
DO NOT CONFORM is broken.

### Step 5: Faithfulness Analysis

For each fixture, identify suspicious capture quality:

a. Suspiciously small files (<2KB) in non-error categories (legitimate_*,
   spa_shell, etc.) where small size suggests truncation or capture
   failure rather than the expected scenario.

b. Suspiciously round file sizes (e.g., exactly 200,000 bytes or other
   power-of-2 boundaries) suggesting buffer truncation.

c. Files lacking signs of real-world HTML:
   - No <head> or <body>
   - No DOCTYPE
   - No script tags (real pages have many)
   - No meta tags
   - "example.com" or "test.example" in content
   - Filename domain doesn't appear anywhere in content

d. Files that appear to be stubs, partial captures, or hand-written
   synthetics rather than real-world captures.

Report each flagged fixture with reason.

### Step 6: Discrimination Analysis

For each directory containing more than 2 fixtures:

a. Compare fixtures pairwise (or sample if many) for structural similarity:
   - Same domain pattern (multiple captures of same site?)
   - Same template (different domains but identical HTML structure?)
   - Same detection trigger (different content but trigger the same
     detector pattern?)

b. Flag redundant fixtures — those that would exercise the same code path
   as another fixture in the same directory with no meaningful variation.

c. For each directory, recommend:
   - Fixtures to keep (best representatives)
   - Fixtures redundant with others (could be removed)
   - Fixtures that should move to a different directory (misclassified)

### Step 7: Currency Analysis

a. Confirm the capture date range across all fixtures. Operator reports
   April 25, 2026, captures (within a 2-minute window). Verify this is
   accurate across the corpus.

b. For each fixture in cloudflare_challenge/ and similar anti-bot
   directories, check whether the markers in the fixture match the
   markers the current barriers.py code looks for. Specifically:
   - Read barriers.py to identify the exact strings, classes, or
     patterns it matches for each barrier type
   - Read each anti-bot fixture and check for those specific markers
   - Flag any fixture where the markers don't match (the detector won't
     fire on it)

c. Look for outdated web patterns in legitimate_* fixtures:
   - jQuery 1.x/2.x references
   - Old framework version strings (React 16, Vue 2, Angular 1.x/AngularJS)
   - http:// in src/href attributes (non-HTTPS)
   - Pre-2020 Bootstrap markers

d. Note that "outdated" is relative to capture date (Apr 2026) and what
   real-world B2B sites look like in early 2026.

### Step 8: Labeling Analysis

a. For each fixture directory, check for:
   - expected/ subdirectory
   - meta.json or capture_metadata.json
   - README.md describing the category

b. Operator confirms no expected outputs exist anywhere. Verify this
   across all directories.

c. Search for fixture references across test files:
   - Grep through tests/ for filenames of HTML fixtures
   - For each fixture, record: referenced by tests yes/no
   - Identify orphaned fixtures (present but never referenced by any test)
   - Identify well-used fixtures (referenced by multiple tests)

d. Per the operator's hint: filename + directory name together imply the
   test specification. Verify this by spot-checking:
   - For 10 randomly-selected fixtures, can you predict from
     directory + filename alone what test outcome should occur?
   - For ambiguous cases, note them.

### Step 9: Production Data Sampling

The operator has provided that production parquet outputs exist. Sample
them to determine the real production outcome distribution.

a. Look for parquet output paths. Candidates to check:
   - REPO_PATH/sample_classify_business_*.parquet (root-level samples)
   - Any data/ or outputs/ directories
   - Check docs/PIPELINE.md for documented output paths

b. If no sample files are accessible in the repo, report this and ask the
   operator to point to a sample directory.

c. For accessible sample parquet files, read using pyarrow in read-only
   mode (no writes back). Tally:
   - Distribution of is_business (true/false/null)
   - Distribution of Stage 2 tech_category (if present)
   - Distribution of Stage 3 partner_type (if present)
   - Distribution of failure modes (parking, bot_blocked, etc.) by
     reading whatever outcome/error fields exist
   - Distribution of fetch tier outcomes
   - Distribution of language_detected

d. Compute the production distribution.

e. Compare production distribution to fixture distribution from Step 2.
   For each production outcome category, compute:
   - Production frequency (% of records)
   - Fixture count
   - Fixture frequency (% of fixtures)
   - Coverage gap (production % - fixture %)
   - Severity: HIGH if production > 10% and fixture < 5%

### Step 10: Audit-Remediation Fixture Requirements

Cross-reference the Top 30 Actions from AUDIT_REPORT.md against fixture
coverage. The full AUDIT_REPORT.md is at ~/crawler-audit/AUDIT_REPORT.md.

For each of the following actions, determine fixture readiness:

- Action #1 (SPA hydration): Search fixtures for __NEXT_DATA__, __NUXT__,
  __APOLLO_STATE__, __PRELOADED_STATE__, Remix/Gatsby/SvelteKit payloads.
  Report count of fixtures with each.

- Action #2 (robots.txt): Are there fixtures of pages that have associated
  robots.txt files (perhaps stored alongside)?

- Action #4 (network interception): Are there fixtures of SPA pages that
  load content via XHR/fetch after initial HTML (judge by HTML having
  empty body + JS bundle references)?

- Action #5 (boilerplate fingerprinting): Are there fixtures grouped by
  domain (multiple pages of the same site for cross-page detection)?

- Action #10 (BreadcrumbList): Are there fixtures with JSON-LD
  BreadcrumbList markup?

- Action #13 (mega-menu activation): Are there fixtures with
  aria-haspopup, aria-expanded, role="menu", or large nav structures that
  would test mega-menu activation?

- Action #14 (sitemap/canonical): Are there fixtures with rel=canonical
  link tags? Are there separate sitemap.xml fixture files?

- Action #19 (PII detection): Are there fixtures with email addresses,
  phone numbers, SSNs, or other PII patterns (real or synthetic) for
  testing redaction?

- Action #20 (regional policy): Are there fixtures from non-US domains
  (TLDs like .de, .fr, .jp, .br, .cn) that would test region detection?

- Action #21 (per-domain crawl history + version stamping): Not fixture-
  blocking; skip.

For each action: PRESENT (sufficient fixtures), PARTIAL (some but
insufficient), ABSENT (no fixtures support this work).

### Step 11: Recommended Candidate Fixtures

For each gap identified in Steps 4, 5, 9, and 10, recommend specific
candidate fixtures to add. For each recommendation:

a. What category/directory it should go into (new or existing)
b. What characteristics it should have (size range, framework, content
   type, what code path it should trigger)
c. How to source it (capture from production parquet sample? hand-craft
   a synthetic? capture from a specific domain pattern?)
d. Why it matters (which audit action it unblocks, or which production
   gap it fills)
e. Priority: CRITICAL (blocks immediate audit work), HIGH (blocks
   Workstream B-D work), MEDIUM (improves robustness), LOW (nice to have)

Group recommendations into themes:
- SPA framework variants (for Action #1)
- Mega-menu samples (for Action #13)
- PII test fixtures (for Action #19)
- International/regional samples (for Action #20)
- Happy-path B2B diversity (general production coverage)
- Industry diversity (production coverage gap)
- Anti-bot freshness refreshes (any stale captures from Step 7)
- Edge cases (encoding, malformed, huge/tiny)

The output should be actionable: "add N fixtures of type X, sourced from Y,
priority Z."

## Output Format

The FIXTURE_AUDIT_REPORT.md should contain, in this order:

### 1. Read-Only Compliance Verification
- Pre-audit git status (verbatim)
- Pre-audit git rev-parse HEAD
- Post-audit git status (verbatim)
- Post-audit git rev-parse HEAD
- Confirmation no files modified
- List of commands skipped for safety

### 2. Executive Summary
- Total fixture count and category breakdown
- Overall corpus health rating (READY / NEEDS_WORK / BROKEN)
- Top 5 fixtures that don't conform to their directory's specification
- Top 5 gaps blocking audit-remediation work
- Top 5 highest-priority candidate fixtures to add

### 3. Fixture Inventory
Table per directory: Category | Files | Bytes | Size p50 | Size Range |
Date Range | Has expected/ | Has meta | Referenced by tests

### 4. Directory-Spec Mapping
Table per directory: Directory | Implied Spec | Code Path | Detection
Signature | Expected Outcome

### 5. Fixture-Spec Conformance
For each directory:
- Count CONFORMS / DOES NOT CONFORM / AMBIGUOUS
- List of non-conforming fixtures with reason
- List of fixtures that may belong in a different directory

### 6. Faithfulness Findings
- Suspiciously small fixtures (with sizes)
- Suspiciously round sizes (truncation suspects)
- Non-real-world captures (synthetic / stub / hand-written suspects)

### 7. Discrimination Findings
- Redundant fixtures within categories
- Categories with too many (recommend pruning)
- Categories with too few representatives

### 8. Currency Findings
- Capture date confirmation
- Anti-bot fixture detector-match: which fixtures still trigger current
  detection, which don't
- Outdated patterns in legitimate_* fixtures

### 9. Labeling Findings
- Count of fixtures with expected/ subdirectories (likely zero)
- Count of fixtures with meta files (likely zero)
- Count of fixtures referenced by tests vs. orphaned
- Map of fixture → test references

### 10. Production Distribution
- Outcome category distribution from sampled parquet output
- Comparison table: production % vs fixture % per category
- Coverage gaps with severity

### 11. Audit-Remediation Fixture Readiness
- Per-action assessment (PRESENT / PARTIAL / ABSENT)

### 12. Recommended Candidate Fixtures
- Grouped by theme
- Each with category, characteristics, source, rationale, priority
- Total count: how many fixtures need to be added before audit
  remediation can proceed

### 13. Prioritized Fixture Work Plan
- Ordered list of fixture additions/replacements/labeling work
- Estimated effort per item (low/medium/high)
- Dependencies (which actions are blocked by which fixture work)

## Final Instruction

After writing the report:
1. Run `git -C REPO_PATH status` and paste output in chat
2. Confirm pre and post match (or flag if not)
3. List top 10 findings from the report in chat
4. List top 10 recommended candidate fixtures in chat
5. Stop. Do not propose fixes or write any code.
