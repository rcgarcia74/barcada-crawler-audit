# Crawler Repository Audit — Comprehensive, Read-Only

## Critical Constraints

This is a READ-ONLY audit. You will not modify, create, delete, or rename any
file inside the repository being audited. The audit runs from this workspace
directory (~/crawler-audit/), which is OUTSIDE the repository. Your only
filesystem writes go to this workspace, never to the repo.

### Repository under audit
REPO_PATH: /Users/administrator/projects/barcada-scraper

### Audit workspace
WORKSPACE: ~/crawler-audit/
FINAL REPORT: ~/crawler-audit/AUDIT_REPORT.md
WORKING NOTES (optional): ~/crawler-audit/working/

### What you MAY do
- Read any file under REPO_PATH (cat, view, head, tail, less)
- List any directory under REPO_PATH (ls, find without -delete)
- Run read-only git commands AGAINST REPO_PATH:
  git -C REPO_PATH log, status, diff, show, branch, blame
- Run pattern searches: grep, ripgrep, ag (read-only)
- Read manifest files (package.json, requirements.txt, pyproject.toml, etc.)
- Write files INSIDE WORKSPACE only

### What you MUST NOT do
- Modify, create, delete, or rename any file under REPO_PATH
- Run git commands against REPO_PATH that change state (add, commit, checkout,
  merge, reset, stash, push, pull, fetch, rebase)
- Run package managers that write (npm install, pip install, cargo build, make,
  npm run build)
- Run formatters or linters in fix/write mode
- Execute the crawler itself or its test suites (these may write logs/caches)
- Run any tool that creates artifacts under REPO_PATH (.next/, dist/, build/,
  __pycache__/, node_modules/, .pytest_cache/)
- Modify persistent environment variables
- Use sudo

### Uncertainty rule
If unsure whether a command writes to REPO_PATH, do not run it. Note skipped
commands in the report under "Commands skipped for safety."

### Pre-flight self-check (before every command)
1. Does this write any file under REPO_PATH?
2. Does this change git state in REPO_PATH?
3. Does this trigger build/cache artifacts under REPO_PATH?
If any answer is "yes" or "unsure," do not run it.

## Process

### Step 1: Handshake (do this first, wait for confirmation)
a. State the REPO_PATH you understood.
b. State the WORKSPACE path you will write to.
c. List 5 specific commands you will NOT run during this audit.
d. Wait for my confirmation before proceeding.

### Step 2: Capture starting state
Run `git -C REPO_PATH status` and `git -C REPO_PATH rev-parse HEAD`.
Save verbatim output for the report's compliance section.

### Step 3: Systematic audit
For each section below, gather evidence by reading files and running read-only
commands. Use ~/crawler-audit/working/notes.md for checkpointing if needed.
Never write intermediate files to REPO_PATH.

### Step 4: Capture ending state
Run `git -C REPO_PATH status` and `git -C REPO_PATH rev-parse HEAD` again.
Compare to starting state. Flag any differences prominently.

### Step 5: Write the report
Write the complete audit report exactly once to:
~/crawler-audit/AUDIT_REPORT.md

### Step 6: Final verification
Run `git -C REPO_PATH status` one final time. Include output in the chat.

## Comprehensive Audit Framework

For every finding, cite specific file:line evidence. Vague findings without
citations are not acceptable. If you can't find evidence for a pattern, mark
it MISSING with a note about where you looked.

---

### Section 1: Foundation and Specifications

1.1 Documentation artifacts
- SCRAPER_SPEC.md or equivalent defining extraction targets explicitly
- CRAWLING_POLICY.md covering robots.txt, rate limits, identification, AUP
- FAILURE_PATTERNS.md cataloging known failure modes and their fixes
- ARCHITECTURE.md or equivalent explaining system structure
- CHANGELOG.md showing iterative improvements
- README explaining the architecture and entry points

1.2 Vocabulary resources
- Intent taxonomy with hierarchical parent/child relationships
- PATH_DICTIONARY.json or equivalent canonical path catalog
- Per-locale path dictionaries (not just translations)
- Strong vs weak label distinctions

1.3 Policy resources
- CRAWLING_POLICY.md actually referenced in code (not just documented)
- regional_policy.json or equivalent for GDPR/CCPA/LGPD/PIPL
- Domain blocklist for sites that have opted out

---

### Section 2: Domain Triage

2.1 Pre-fetch decisions
- DNS check before fetch (NXDOMAIN skip)
- HEAD request to verify 200 + reasonable content-length
- Parked domain detection (1KB partial fetch + pattern check)
- Domain reputation cache (once failed, don't retry for N days)
- Redirect chain limit (skip after N hops)

2.2 Triage metrics
- Domains queued vs domains crawled (skip rate visibility)
- Cost-per-domain pre-filtered vs post-filter

---

### Section 3: Fetching Strategy and Anti-Bot

3.1 Tiered fetching architecture
- Tier 0: polite plain HTTP with realistic headers
- Tier 1: plain HTTP + residential proxy
- Tier 2: TLS-fingerprint-spoofing client (curl_cffi, tls-client)
- Tier 3: Playwright with stealth (playwright-stealth, undetected-playwright)
- Tier 4: Playwright + residential proxy + behavioral simulation
- Tier 5: Commercial unblocker (ScrapingBee, ZenRows, Bright Data unblocker)
- Tier 6: Skip / mark unscrapeable

3.2 Strategy learning and caching
- Per-domain successful tier cached
- Per-domain failed tiers tracked
- Per-domain best proxy region learned
- Per-domain observed rate limit tracked
- Periodic re-validation of cached strategy

3.3 Block detection
- HTML content markers (cf-chl-bypass, "Just a moment...", "Checking your browser")
- Suspicious body length (<1KB for content-rich domain)
- Block-suggesting titles (Access Denied, Forbidden, Robot or human?)
- Status code handling: 403, 429, 503 patterns
- Redirect-to-login/verify/captcha detection
- CAPTCHA iframe detection (reCAPTCHA, hCaptcha, Turnstile, Arkose)
- Identical response across distinct URLs (challenge page signature)
- Structured verdict: OK | SOFT_BLOCK | HARD_BLOCK | CHALLENGE | RATE_LIMIT

3.4 TLS and HTTP/2 fingerprinting
- TLS fingerprint awareness (JA3/JA4)
- HTTP/2 frame ordering / header order awareness
- Client library that spoofs real browser fingerprints

3.5 Behavioral simulation (Tier 4+)
- Mouse movement simulation
- Realistic scroll behavior
- Typing cadence for forms
- Randomized timing between actions

3.6 Rate limiting
- Per-domain token bucket (default 1 req per 2s for unknown)
- Jitter on request timing
- Exponential backoff on 429/503 (1s → 2s → 4s → 8s capped)
- Concurrent connection cap per domain (default 2-4)
- Honor Retry-After headers

3.7 Robots.txt and identification
- Robots.txt parser
- Robots.txt compliance enforced in code (not just documented)
- User-Agent identification with contact email
- Respect of Crawl-delay directive

3.8 CAPTCHA policy
- Default: skip CAPTCHA-challenged domains
- Explicit authorization required for solving
- No model training to defeat CAPTCHAs
- Policy enforced in code, not just documented

3.9 Per-region anti-bot strategy
- Awareness of regional differences (China, Russia, EU, Japan, LatAm)
- Region-specific tier defaults
- Region-specific failure patterns tracked

3.10 Anti-bot failure taxonomy
- BOT_BLOCK_IP_REPUTATION
- BOT_BLOCK_TLS_FINGERPRINT
- BOT_BLOCK_JS_CHALLENGE
- BOT_BLOCK_CAPTCHA
- BOT_BLOCK_BEHAVIORAL
- BOT_BLOCK_GEO
- BOT_BLOCK_RATE
- BOT_BLOCK_UNKNOWN
- Routing logic from each failure type to specific remediation

---

### Section 4: Proxy Integration

4.1 Provider abstraction
- ProxyProvider uniform interface
- get_proxy(region, sticky_session_id?) → ProxyConfig
- report_success / report_failure callbacks
- current_balance() and list_supported_regions() methods
- No direct provider API calls outside the abstraction

4.2 Failover ladder
- Primary residential → backup residential → datacenter → unblocker → skip
- Each tier escalation triggered by specific failure types
- Skip threshold to avoid runaway retries

4.3 Per-domain provider selection
- Selection learned from telemetry, not hardcoded
- Per-domain preferred provider cached
- Per-domain fallback provider tracked
- Per-domain success rate per provider tracked

4.4 Session management
- Sticky session support (same IP for N minutes)
- Per-request rotation support
- Session selection rules (sticky for multi-page crawls, rotating for one-offs)
- Session release on completion (don't hold longer than needed)

4.5 Authentication
- Credentials in secrets manager (not env vars or code)
- Credentials encrypted/redacted in logs
- IP allowlisting supported where provider allows

4.6 Bandwidth controls
- Resource blocking at browser level (images, fonts, video, analytics, ads)
- Gzip/brotli compression negotiated
- HEAD requests where possible (liveness, redirect resolution)
- Early bailout on non-HTML Content-Type

4.7 Pool health monitoring
- Latency per request tracked (rolling p50/p95)
- Success rate per provider tracked
- Per-region success rate tracked
- Error type distribution tracked
- Auto-traffic-shift on degradation

4.8 Concurrency
- Provider-level concurrency cap
- Per-domain concurrency cap
- Interaction between the two managed correctly

4.9 Provider strategy
- No premium-only dependency
- Backup provider configured
- Datacenter tier available for cheap-eligible domains
- Mobile proxy use bounded to specific high-value cases

4.10 Compliance
- Provider IP sourcing documented
- AUP review for use case permissions
- Provider performance dashboard

---

### Section 5: Discovery and Crawl Strategy

5.1 Discovery sources
- Sitemap.xml-first discovery
- Robots.txt parsing
- Hreflang link extraction
- Internal link crawl as fallback

5.2 URL handling
- URL normalization before queue insertion
- Tracking param stripping (utm_*, ref, source, fbclid, gclid, mc_cid)
- Session param stripping (sid, sessionid, phpsessid)
- Pagination duplicate detection
- Hash route resolution
- Canonical URL extraction (<link rel="canonical">)
- Case-sensitive path preservation
- Trailing slash normalization

5.3 Crawl scope
- Crawl depth cap per domain (default 2-3)
- Per-intent target page lists
- Pagination handling (cap at first N pages or skip)
- Skip archive/date-based URL patterns by default
- Skip search result pages

5.4 Deduplication
- Canonical URL-based dedup
- Content-hash-based dedup
- Cross-locale variant linking (not duplication)

---

### Section 6: Rendering and SPA Handling

6.1 SPA detection (before render)
- Initial HTML body size analysis (<5KB indicator)
- Empty root div detection (#root, #app, [data-reactroot])
- Framework fingerprints (Next.js, Nuxt, Vue, Angular, Svelte, Remix)
- Wappalyzer-style tech detection
- Per-domain SPA decision cached

6.2 Hydration payload extraction (highest leverage)
- __NEXT_DATA__ script tag extraction (Next.js)
- window.__NUXT__ extraction (Nuxt)
- window.___INITIAL_PROPS___ (Gatsby)
- window.__remixContext (Remix)
- data-sveltekit-fetched (SvelteKit)
- window.__APOLLO_STATE__, window.__PRELOADED_STATE__ (generic)
- Hydration-first enforcement before any render
- Preferred over rendering when payload available

6.3 Tiered wait strategies
- Tier 1: domcontentloaded
- Tier 2: networkidle (500ms quiet)
- Tier 3: custom readiness selectors
- Tier 4: mutation observer with quiet period
- Tier 5: fixed wait (last resort, logged)
- Escalation only on lower-tier failure
- No bare sleep() calls in production paths

6.4 Network request interception
- XHR/fetch logging during render
- Meaningful request identification (GraphQL, REST returning JSON)
- API endpoint discovery and persistence
- Discovered API replay on subsequent crawls
- discovered_apis.json or equivalent per domain

6.5 Render efficiency
- Resource blocking (images, fonts, video, analytics, ads, tracking)
- WebGL/audio/video disabled
- Browser context reuse across pages of same domain
- Render budget per page (kill at N seconds)
- Render result caching by (url, viewport, locale)

6.6 SPA-specific failure taxonomy
- SPA_HYDRATION_TIMEOUT
- SPA_HYDRATION_PAYLOAD_MISSING
- SPA_MENU_NOT_ACTIVATED
- SPA_INFINITE_SCROLL_INCOMPLETE
- SPA_API_CALL_FAILED
- SPA_ROUTE_MANIFEST_PARSE_FAILED
- SPA_HYDRATION_INSTABILITY

6.7 Route discovery
- Sitemap-first
- Build manifest extraction (Next.js _next/static/.../buildManifest.js)
- Router config in JS bundles (React Router, Vue Router)
- Hydration payload internal links
- Path probing as fallback only

6.8 Render reconciliation
- Two-render comparison for high-value pages
- Personalization marker stripping for comparison
- Instability flagging when renders differ materially
- Lower confidence assignment to unstable domains

---

### Section 7: Menu Extraction

7.1 Landmark detection
- <nav> elements
- role="navigation"
- <header>, <footer>
- aria-label="Main navigation" etc.
- role="menu", "menubar", "menuitem"
- Multiple nav regions extracted separately

7.2 Heuristic fallback
- Top viewport position with link density
- Bottom DOM region with column structure
- Sticky/fixed-position element detection
- Spatial link clustering

7.3 Hierarchy extraction
- Tree structure, not flat list
- DOM nesting (li > ul) parsing
- aria-expanded / aria-controls handling
- Visual indentation in rendered layout
- Heading hierarchy in mega menus
- Class naming convention awareness
- Visual hierarchy preferred when DOM/visual disagree

7.4 Per-menu routines
- Top nav: mega menu activation, hover/click/focus
- Mega menu: column-aware, category headers, featured content, CTAs
- Footer: column extraction with section headers
- Sidebar nav
- Breadcrumbs (semantic, microdata, JSON-LD BreadcrumbList preferred)
- Mobile menu (used as hierarchy ground truth)
- Utility nav (login, search, language)

7.5 Mega menu activation
- Trigger detection (aria-expanded, aria-haspopup, aria-controls)
- Hover sweep
- Click sweep
- Focus + Enter sweep
- Recursive activation for multi-level
- Desktop viewport sweep (1440px)
- Mobile viewport sweep (375px)
- State reset between attempts

7.6 Mobile menu as hierarchy source
- Mobile menu rendered explicitly when desktop hierarchy ambiguous
- Mobile menu hierarchy mapped to desktop labels
- Used as ground truth for hierarchy disputes

7.7 Breadcrumbs
- nav aria-label="Breadcrumb" detection
- ol.breadcrumb class detection
- JSON-LD BreadcrumbList preferred (cleanest)
- Schema.org microdata
- Used as site-map signal for section intent

---

### Section 8: Content Extraction

8.1 Main content identification
- <main>, role="main", <article> semantic detection
- Readability-style algorithm fallback
- Visual density and clustering (rendered layout)
- Inverse extraction via cross-page boilerplate

8.2 Cross-page boilerplate fingerprinting (highest leverage)
- Block-level hashing (not whole-page)
- Shingled / fuzzy hash matching
- Frequency tracking across N pages per domain
- Threshold-based boilerplate classification (default 30%)
- Per-domain fingerprint cached
- Periodic recomputation on detected site changes
- Locale-stable detection via structure hashing

8.3 Render-aware filtering
- getBoundingClientRect zero-dimension filter
- Computed display:none filter
- visibility:hidden filter
- opacity:0 filter (carousel hidden slides)
- Offscreen positioning filter (left:-9999px etc.)
- aria-hidden="true" filter

8.4 Selector-based stripping
- script, style, noscript, template, [hidden]
- nav, [role=navigation], header, footer, breadcrumb, toc, sidebar
- Cookie banner / consent UI
- Newsletter / signup form
- Social share buttons
- Back-to-top, scroll-to-top
- Search form / search bar
- Language switcher
- Chat widgets (Intercom, Drift, Zendesk markers)
- Related / popular / recommended widgets
- Ads / sponsored
- Popups / modals

8.5 Structural pattern detection
- Carousel detection (role=region + aria-roledescription=carousel, swiper-slide, slick-slide classes)
- Tab detection (role=tablist, tabpanel, aria-selected)
- Accordion detection (<details>, aria-expanded, .accordion classes)
- Active panel extraction by default
- All-panel extraction override for pricing-like intents

8.6 Within-page deduplication
- Similarity hashing (SimHash, MinHash, normalized hash)
- Block-level dedup threshold (e.g., 0.9 similarity)
- Keep-first-occurrence rule
- Per-content-type threshold tuning

8.7 Density filtering
- Link density threshold (drop >0.5)
- Text density threshold
- Position-based boundaries (between first H1 and "related" marker)

8.8 Per-intent allowlists
- Per-intent structural patterns preserved
- Discarded blocks logged for review
- Multi-intent emission for homepages

8.9 Distillation profiles
- Per-intent preserve list
- Per-intent strip list
- Per-intent signal keywords
- Per-intent max_output_chars cap

8.10 Two-pass cleaning
- Pass 1: liberal negative filtering (strip aggressively)
- Pass 2: conservative positive selection (intent-allowlist match)

8.11 Output normalization
- HTML to Markdown conversion
- Headings preserved as hierarchy (#, ##, ###)
- Lists preserved
- Tables preserved as Markdown tables
- Images replaced with alt text (or removed)
- Links preserved with anchor text + URL
- Whitespace collapsed
- Within-block repetition deduplicated

8.12 Structured data extraction (preferred over HTML)
- JSON-LD parsing (Product, Organization, Article, Review, FAQPage, BreadcrumbList, HowTo, Recipe, Event)
- Microdata parsing
- OpenGraph extraction
- Twitter Card metadata
- Emitted as separate output from prose

8.13 Post-extraction validators
- Link density check on output (flag >0.3 in 500-char window)
- Repetition check (flag if 100+ char substring appears 3+ times)
- Length check vs intent minimum signal threshold
- Stop-word ratio check (low signal warning)
- Structural loss check (missing headings where expected)

---

### Section 9: Label-to-Intent Matching

9.1 Tier 1: Dictionary match
- Lowercase normalization
- Punctuation stripping
- Emoji and decorative char stripping
- Whitespace collapse
- Article and stop word stripping (for matching only)
- Decorative prefix/suffix stripping (→, ›, "View")
- Unicode NFC normalization
- Plural handling

9.2 Tier 2a: Curated synonym lists
- Per-intent synonym groups
- Per-locale synonym lists (not translations)
- Separate from strong/weak labels
- Confirmed via destination signals before high confidence

9.3 Tier 2b: Embedding similarity
- Multilingual embedding model (text-embedding-3-small, embed-multilingual-v3, bge-m3)
- Per-intent centroid pre-computed from strong labels
- Per-locale centroids (preferred over single global)
- Cosine similarity threshold (e.g., 0.75)
- Embedding cache by label hash

9.4 Tier 2c: Linguistic resources
- WordNet as candidate-generation source for curation (not runtime)
- Human filter for B2B relevance before promotion

9.5 Tier 3: LLM fallback
- Sibling labels included in prompt
- Position included in prompt
- Industry hint included
- Site language included
- Response cached by (label, url, sibling_labels_hash)
- Batching of multiple labels per call
- Cheapest capable model selected per task

9.6 Three-signal confidence scoring
- Label signal (strong/weak/none)
- URL signal (strong/weak/none)
- Destination signal (present/absent)
- ≥2 agreement required for high confidence
- Single-signal flagged for review or LLM verification

9.7 Destination signal catalogs
- Per-intent destination signals defined
- Language-agnostic preferred (logos, layouts, currency, structured data)
- Language-specific where needed
- Locale variants of destination signals

9.8 Position weighting
- Top nav weight vs footer weight differentiated
- aria-label and title attribute usage as supplementary
- Breadcrumb labels distinguished from nav labels

9.9 Negative-match list
- Terms looking right but reliably aren't
- Domain/industry-conditional
- Maintained alongside synonym lists

9.10 Industry conditioning
- Pre-classify domain industry from homepage signals
- Industry-specific synonym priors
- Industry-specific negative matches

9.11 Novel label handling
- Emit unresolved labels with destination-based fallback intent
- NOVEL_LABEL flag for review
- Surface novel labels in dashboard for synonym mining

9.12 Learning loop
- All LLM resolutions logged with context
- Frequency-based promotion to candidate synonym list
- Human review queue with bounded volume
- Promoted synonyms re-tested against eval set
- Re-compute embeddings on dictionary changes

9.13 Per-locale maintenance
- Coverage metric per locale and per intent
- Native-speaker validation for non-English additions
- Prioritization based on coverage gaps

---

### Section 10: Internationalization

10.1 Locale discovery
- hreflang link extraction (first-class)
- Language switcher UI detection
- URL pattern detection (/en/, /de-DE/, ?locale=fr_FR, subdomains)
- <html lang> attribute
- Sitemap variants per locale
- Output: locales_discovered.json per domain

10.2 Locale crawl scope
- Canonical locale + target markets default
- Per-domain scope decision documented
- Explicit cost recognition for multi-locale crawls

10.3 Geo-routing
- Per-domain preferred proxy region
- TLD-based region heuristics (.de → Germany, .co.jp → Japan)
- Regional retry on suspected geo-content variation
- Cost recognition for geo-routed proxies

10.4 Encoding and Unicode
- Encoding detection (chardet/charset-normalizer, not header trust)
- Unicode NFC normalization
- Per-page language detection (fasttext, langdetect)
- Original + normalized text stored

10.5 Script handling
- CJK tokenization (jieba, MeCab, KoNLPy)
- RTL awareness (Arabic, Hebrew)
- Mixed-script handling (kanji + hiragana + katakana + Latin)

10.6 Per-locale path dictionaries
- /partners equivalents per locale (de: /partner, fr: /partenaires, ja: /パートナー)
- Native non-translated entries
- Coverage tracked per locale

10.7 Language-agnostic signals prioritized
- JSON-LD / schema.org
- OpenGraph / Twitter Cards
- External links (LinkedIn, GitHub, Twitter handles)
- Email and phone country codes
- Address microdata
- Currency symbols and ISO codes
- Technology fingerprints (Wappalyzer)

10.8 LLM extraction in native language
- Original-language HTML to LLM (no pre-translation)
- Locale context provided
- Few-shot examples in target language
- Aggressive caching by content hash

10.9 Per-region anti-bot
- China: in-country proxies, specialized tools, often skip
- Russia: Yandex defenses, Cyrillic CAPTCHAs
- EU: cookie wall friction
- Japan: legacy layouts, Playwright often required
- Brazil/LatAm: generally easier but Cloudflare rising
- Per-region success rate tracked separately

10.10 Regional legal policy
- GDPR (EU) considerations enforced in code
- CCPA (California) considerations
- LGPD (Brazil) considerations
- PIPL (China) — strict, assume cannot scrape PII
- Local-language ToS awareness
- regional_policy.json checked before emit

10.11 SPA × i18n
- Multi-locale hydration payload check
- Translation API discovery (next-intl, react-i18next, vue-i18n)
- Accept-Language header probing for hybrid SSR
- Locale URL pattern probing
- Render reuse across locales per domain

10.12 Cross-regional entity resolution
- Domain-to-entity mapping (example.com / .de / .co.jp same company?)
- Whois match (when not privacy-masked)
- Logo/favicon hash match
- Shared social handles
- Cross-linking ("Visit our German site")
- Schema.org sameAs property
- Identical product/solution structures

10.13 Locale-stratified evaluation
- Golden set stratified by locale (40% en, 15% de, 15% ja, 10% fr, 10% es, 10% other)
- Composite score tracked per locale
- Per-locale acceptance threshold
- No global 98% claim without each locale at 98%

10.14 Native-speaker validation queue
- Sample of non-English crawls routed for label validation
- Translation service or contractor pipeline
- Validation feeds back to synonym/dictionary growth

---

### Section 11: Validation and Evaluation

11.1 Golden set
- 100-500+ domains with expected outputs
- Stratified by locale (per 10.13)
- Stratified by intent
- Stratified by site type (B2B SaaS, e-commerce, news, etc.)
- Stratified by complexity (static, SPA, anti-bot)
- Weighted by domain importance

11.2 Acceptance metric
- Composite score formula explicitly defined
- Per-field accuracy vs per-domain accuracy distinction
- Tolerance bands documented
- Confidence-adjusted scoring

11.3 Eval runner
- Scripted execution (npm run scrape:evaluate or equivalent)
- Scores: nav_recall, footer_recall, partner_path_recall, business_signal_precision/recall, duplicate_url_rate, broken_url_rate, spa_success_rate, false_positive_rate, false_negative_rate
- Per-intent precision/recall
- Per-locale separate scoring
- Composite score output

11.4 Fixture-based tests
- /tests/fixtures/static/, /spa/, /mega-menu/, /mobile-menu/, /parked/, /bot-blocked/
- SPA-specific fixtures (nextjs_static_nav, react_mega_menu, vue_hamburger_mobile, angular_router, csr_only, hybrid_isr)
- Raw HTML, hydration payloads, HAR files, expected output
- Deterministic, not live-network

11.5 Regression test infrastructure
- Run on every code change
- Zero-regression policy
- Diff-based regression on fixed page set

11.6 Drift detection
- Nightly re-crawl of previously-passing domains
- Alert on per-domain accuracy drop
- Boilerplate fingerprint staleness detection
- Site redesign detection

11.7 Classifier-loop validation
- Downstream classifier performance tracked
- Improvements in extraction must improve classifier accuracy
- Mismatch between extraction metrics and classifier metrics flagged

---

### Section 12: Cost Control

12.1 Cost telemetry
- Structured cost record per crawl
- Stage breakdown: triage, fetch, render, extract, llm, storage
- Per-stage duration, bytes, cost USD
- Outcome status: SUCCESS / PARTIAL / FAILED
- Useful records produced

12.2 Primary metric
- Cost per useful record (not cost per page)
- Tracked per domain
- Tracked per intent
- Tracked over time (should decrease)

12.3 Per-domain budgets
- max_pages
- max_render_seconds
- max_proxy_mb
- max_llm_tokens
- max_total_cost_usd
- hard_kill_at: 2x budget
- Breach logged with stage breakdown
- High-value override mechanism

12.4 Per-stage budgets within a crawl
- fetch budget (time, bytes)
- render budget (time, memory)
- extract budget (time)
- llm_calls budget (cost)
- total page budget
- Stage breach surfaced as actionable signal

12.5 Daily/weekly/monthly caps
- Alert at 50%, 80%, 100% of budget
- Hard kill at 120%
- Per-service caps (LLM, proxy, unblocker)
- Per-region caps

12.6 Domain value tiering
- HIGH_VALUE / STANDARD / LOW_VALUE
- Differentiated budgets per tier
- Monthly review of expensive domain list

12.7 Efficiency flags
- RENDERED_WITHOUT_HYDRATION_ATTEMPT
- TIER_OVER_ESCALATION
- EXCESSIVE_PAGE_CRAWL
- LOW_USEFUL_RECORD_RATE
- LLM_OVERUSE
- CACHE_MISS_RATE_HIGH
- RENDER_TIMEOUT_PATTERN
- RETRY_LOOP_DETECTED
- BOILERPLATE_NOT_CACHED
- DUPLICATE_PAGE_CRAWLED
- OVER_BUDGET_WITHOUT_OVERRIDE

12.8 LLM cost control
- LLM as fallback only (deterministic-first)
- Aggressive caching by content hash
- Batched calls where related
- Model selection per task (cheapest capable)
- Token budgets per task type
- Distilled content (not raw HTML) sent to LLM

12.9 Storage lifecycle
- Compression at rest
- Deduplication by content hash
- Hot → warm → cold → delete lifecycle
- Sample-based retention for older data
- Log aggregation above N days

12.10 Retry strategy
- Failure-type-aware retry policy
- Exponential backoff with cap
- Tier escalation on retry (not just retry count)
- Three-strikes rule for permanent backoff
- Resumable/checkpointable pipelines

12.11 Re-crawl strategy
- Adaptive frequency per domain (faster if content changes often)
- Conditional requests (If-Modified-Since, ETag)
- Demand-driven crawling
- Cheap "change detection" probe before full re-crawl

12.12 Cost dashboards
- Operational: daily spend, trend, records, cost per record
- Diagnostic: per-domain outliers, efficiency flag distribution, stage breakdown
- Strategic: cost per category, ROI, trend per stage

---

### Section 13: Observability

13.1 Structured logging
- Per-crawl trace IDs
- Stage tagging on every log line
- Structured fields (not plain strings)
- Severity levels appropriate

13.2 Metrics emission
- Prometheus, StatsD, or equivalent
- Per-stage counters and histograms
- Per-domain gauges where appropriate

13.3 Failure taxonomy (complete catalog)
- All taxonomy entries from anti-bot, SPA, cleaning, etc.
- Routing logic from each failure type to remediation
- Frequency tracking per failure type

13.4 Dashboards or dashboard configs
- Cost dashboards (per 12.12)
- Quality dashboards (composite score, per-locale, per-intent)
- Anti-bot dashboards (block rate per tier, tier distribution)
- Per-domain strategy drift dashboards

13.5 Alert definitions
- Cost budget breaches
- Quality regression alerts
- Drift detection alerts
- Per-provider degradation alerts

13.6 Per-domain health tracking
- Success rate over time
- Cost over time
- Strategy changes over time
- Audit log of significant events

---

### Section 14: Improvement Loop

14.1 Failure clustering
- Cluster failures by root cause pattern (not just by failure type)
- Feature extraction per failure (HTTP status, render mode, DOM characteristics, missing field, error type, response size, JS framework)
- Similarity clustering or rule-based grouping
- failure_clusters.json output

14.2 Cluster prioritization
- Impact estimate per cluster (score lift if resolved)
- Effort estimate per cluster (LoC, files touched, risk)
- Sort by impact ÷ effort
- improvement_backlog.json maintained

14.3 Automated patching
- Headless Claude Code or equivalent integration
- Structured prompt template per cluster
- Constraints: file scope, no fixture regression, regression test required
- Predicted impact analysis required
- ESCALATE option for impossible-without-regression cases

14.4 Validation gauntlet
- Unit tests (zero regressions)
- Fixture tests (all golden fixtures pass)
- Cluster eval (target cluster domains now pass)
- Full eval (composite score up, not down)
- Cost check (cost per record stable or down)
- Determinism check (eval re-runs match)
- Statistical significance check on improvements
- Reject if any check fails

14.5 Auto-merge guardrails
- Score floor (never merge if composite drops)
- Confidence interval on improvement
- Rollback automation if production drift detected
- Human review queue for first-week auto-merges

14.6 Plateau detection
- Score per iteration tracked
- Rolling slope monitored
- Stop loop if 5 consecutive iterations move score <0.001
- Escalation to human

14.7 Cost-aware loop
- Cost as first-class metric alongside accuracy
- Cost-adjusted composite score formula
- Weight policy (cost vs accuracy)
- Strict cost discipline at high accuracy

14.8 Multi-strategy ensembling (for last 2%)
- CSS-selector extractor
- JSON-LD extractor
- Playwright-rendered DOM extractor
- LLM-based extractor
- Reconciliation logic (≥2 agree → emit)
- Disagreement → flag for review
- All-fail → EXTRACTION_FAILED with reason

14.9 Continuous golden-set growth
- Daily production sample (e.g., 50 random crawls)
- Human labeling queue / UI
- Promotion criteria for golden set additions
- Adversarial additions (hard cases) prioritized
- Golden set version tracked

14.10 Loop observability
- Composite score over time
- Score per cluster
- Patch success rate
- Time per iteration
- Cost per iteration
- Plateau indicator

---

### Section 15: Security and Compliance

15.1 Credential handling
- Secrets manager integration (Doppler, Infisical, AWS Secrets Manager, etc.)
- No credentials in code
- No credentials in env vars committed to repo
- Credentials redacted in logs and telemetry

15.2 Robots.txt enforcement
- Parser exists
- Compliance enforced in code (not just documented)
- Crawl-delay honored
- Bypass requires explicit per-domain authorization

15.3 CAPTCHA policy
- Default skip enforced in code
- Override requires documented authorization
- No automated CAPTCHA solving without authorization
- No CAPTCHA-defeating model training

15.4 PII handling
- PII detection in extracted content
- PII redaction or filtering per policy
- Regional rules applied (GDPR PII strictness)
- Audit trail of PII handling

15.5 Regional legal policy
- regional_policy.json or equivalent
- Field-level emit rules per region
- GDPR, CCPA, LGPD, PIPL considerations encoded
- ToS in local language awareness

15.6 Audit trail
- What was crawled, when, under what policy
- Per-domain crawl history
- Policy version tracked
- Compliance reporting capability

---

## Report Structure

The AUDIT_REPORT.md must contain, in this order:

### 1. Read-Only Compliance Verification (FIRST)
- Pre-audit git status (verbatim)
- Pre-audit git rev-parse HEAD (verbatim)
- Post-audit git status (verbatim)
- Post-audit git rev-parse HEAD (verbatim)
- Confirmation that pre and post match (or prominent flag if not)
- List of commands skipped for safety

### 2. Executive Summary
10-15 bullets identifying the biggest gaps and biggest strengths.
Pull from across all 15 sections, not just one.

### 3. Coverage Matrix
Table: Pattern | Status (FULL / PARTIAL / MISSING / N/A) | File Evidence | Severity
One row per item in the framework above (will be 200+ rows).

### 4. Detailed Findings
For each of Sections 1-15, a subsection containing:
- Status summary (paragraph)
- Specific findings (bulleted, with file:line citations)
- Severity rating per finding (CRITICAL / HIGH / MEDIUM / LOW)
- Recommended actions per finding

### 5. Top 30 Prioritized Actions
Numbered list, ordered by (estimated impact / estimated effort).
For each: what to do, where in the repo, why it matters, rough effort estimate.

### 6. Anti-Patterns Found
Code smells, hardcoded values, or patterns that work against design principles.
Cite locations.

### 7. Strengths
What the codebase does well, with citations. This matters — don't only report problems.

### 8. Discovered Architecture
A brief description of the actual architecture you found, regardless of whether
it matches expectations. Helps me reconcile what we discussed vs what's there.

### 9. Recommended Next Audits
What this audit didn't cover or what should be re-audited after fixes.

---

## Final Instruction

After writing the report:
1. Run `git -C REPO_PATH status` and paste output in chat
2. Confirm in chat: "Pre-audit and post-audit git status match" (or flag if not)
3. List in chat: the top 10 findings from the report
4. Stop. Do not propose code changes. Do not offer to fix anything.

The purpose of this session is exclusively to produce the read-only audit report.
