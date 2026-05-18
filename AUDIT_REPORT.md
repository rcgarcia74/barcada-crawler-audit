# Crawler Repository Audit — barcada-scraper

**Repository under audit:** `/Users/administrator/projects/barcada-scraper`
**Audit workspace:** `/Users/administrator/crawler-audit/`
**Audit date:** 2026-05-18
**Mode:** Read-only, single session
**Framework:** Sections 1–15 of `AUDIT_DIRECTIVE.md`

---

## 1. Read-Only Compliance Verification

### Pre-audit state

`git -C /Users/administrator/projects/barcada-scraper status`:
```
On branch main
Your branch is ahead of 'origin/main' by 6 commits.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   eval_data/stage1_labels.jsonl

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	eval_data/stage1_challenge.jsonl

no changes added to commit (use "git add" and/or "git commit -a")
```

`git -C ... rev-parse HEAD`:
```
cb149c19b6c94cc5a41864d99fd5e45a83b8eaad
```

### Post-audit state

`git -C /Users/administrator/projects/barcada-scraper status`:
```
On branch main
Your branch is ahead of 'origin/main' by 8 commits.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	eval_data/stage1_challenge.jsonl

nothing added to commit but untracked files present (use "git add" to track)
```

`git -C ... rev-parse HEAD`:
```
be71d5365adefac38db63e49b38c7d5754b5b426
```

### ⚠ State delta — FLAGGED

The pre- and post-audit states **do not match**. HEAD advanced by two commits and the `eval_data/stage1_labels.jsonl` modification was committed:

```
e51a93f Stage 1 directive: add Pattern 28 (request_demo evidence-driven default); log batch 1 mid-run decisions.
be71d53 Stage 1 main loop: append rows 11-64 (166→220 total, 54 rows).
```

**Attribution:** Both commits are eval-data work (adding labeled rows + a directive Pattern). They are consistent with concurrent operator activity in `eval_data/`, not with audit activity. The auditor **did not** run `git add`, `git commit`, `git checkout`, `git reset`, `git stash`, `git push`, `git pull`, `git fetch`, `git rebase`, `git merge`, or any other state-mutating git command. The auditor only ran `git status`, `git rev-parse HEAD`, and `git log` (read-only). No files under `/Users/administrator/projects/barcada-scraper` were written, created, deleted, or renamed by the auditor or any spawned agent — the only writes were inside the workspace at `/Users/administrator/crawler-audit/`.

**Operator should verify** the two commits with `git -C /Users/administrator/projects/barcada-scraper show e51a93f` and `git -C /Users/administrator/projects/barcada-scraper show be71d53` to confirm they are expected concurrent work.

### Commands skipped for safety

Per the pre-flight rules, the auditor declined to run:

1. `npm install` / `pip install` / `uv sync` / `playwright install` (would write under repo: `.venv/`, `node_modules/`, lockfile changes, `~/.cache/ms-playwright`)
2. `pytest` / `tox` / `python -m barcada_scraper.metrics ...` / any `barcada-*` console script (executes code; writes `__pycache__/`, `.pytest_cache/`, logs)
3. `npm run build` / `next build` / `hatch build` / `python -m build` (writes `dist/`, `build/`, `.next/`)
4. `ruff format` / `ruff check --fix` / `mypy` / any formatter or linter in write mode
5. `git add` / `git commit` / `git checkout` / `git merge` / `git rebase` / `git stash` / `git reset` / `git push` / `git pull` / `git fetch` (state-mutating)
6. Running scrapers, validators, or classifiers against any live domain (would generate network traffic, write logs/journals, and exercise paid proxy APIs)
7. Reading `.env` contents (defensive — confirmed gitignored at `.gitignore` line containing `.env` only)

---

## 2. Executive Summary

Barcada-scraper is a four-stage pipeline (domain validation → business classifier → content scraper → classifier-feature data prep) with a self-managed Azure VMSS orchestrator. Compared to the audit framework — which describes a general-purpose intent-extracting crawler — barcada-scraper is a **specialized, English-first, USA-centric B2B classifier** rather than a generic intent crawler. Several framework sections (intent-label resolution, multi-locale, regional legal policy) are largely out of scope of the current product, and the gaps below reflect that scope rather than implementation oversight in many cases.

**Biggest strengths:**

- **Mature parser with versioned schema.** `src/barcada_scraper/scraper/parser.py` (≈5,800 lines) drives a versioned v2.1 Parquet output with explicit `feature_schema_version` gate (`CHANGELOG.md:7,52`). JSON-LD walker covers ~120 LocalBusiness subtypes and 12+ typed booleans (`CHANGELOG.md:101–113`).
- **Disciplined cost journal + LLM cache tracking.** `src/barcada_scraper/classifier/pipeline/cost_journal.py` is an immutable, append-only state machine with ETag-conditional writes, three explicit outcomes (`completed | cost_ceiling_stopped | not_reached`), and per-stage cost roll-ups; `configs/llm_pricing.yaml:22–26` documents Azure prompt-cache rates; `bandwidth_journal.parquet` tracks `cached_input_tokens` per shard.
- **Strong block detection on the HTML side.** `src/barcada_scraper/scraper/barriers.py:407–447` and `src/barcada_scraper/detection/placeholder.py:561–577` cover Cloudflare, Akamai, Incapsula, Imperva, DataDome, PerimeterX/HUMAN, Wordfence, Sucuri/Cloudproxy, F5 Shape, Kasada, AWS WAF token, Cloudflare Turnstile, hCaptcha challenge widgets, and Chinese-language geo-block phrases.
- **Tier-cascade classifier with deterministic-first routing.** Stage 1 uses RULES → LR (calibrated) → LLM (uncertain band only), keeping LLM calls bounded; `configs/stage1_thresholds.yaml` documents the gates.
- **Provider-agnostic proxy abstraction.** `src/barcada_scraper/classifier/page_acquisition/proxy_provider.py:48–78` defines a structural `ProxyProvider` Protocol; credentials enforced from env vars only (lines 122–154); YAML is credential-free by design.
- **Test fixtures cover real failure modes.** `tests/fixtures/html/` contains 23 named scenario buckets including `cloudflare_challenge/`, `login_wall/`, `soft_404/`, `meta_refresh_parking/`, `spa_shell/`, and 12 parking subtypes — all deterministic static HTML.
- **Concurrent-write safety on the cost journal.** ETag-conditional writes with exponential-backoff retries (`cost_journal.py:59` `DEFAULT_RETRY_DELAYS_MS = (50, 100, 200, 400, 800)`).
- **`DEFERRED_WORK.md` exists and is honest** about what is intentionally not implemented (e.g., `lr_train._load_training_data`'s `NotImplementedError`).

**Biggest gaps:**

- **No robots.txt parser anywhere.** No `urllib.robotparser`, no `Crawl-delay` honoring, no per-domain authorization model. This is the single largest compliance gap (section 3.7, 15.2).
- **No SPA hydration-payload extraction.** Renderer does not attempt `__NEXT_DATA__`, `__NUXT__`, `__APOLLO_STATE__`, `__PRELOADED_STATE__`, Remix/Gatsby/SvelteKit equivalents (section 6.2). This is the **highest-leverage missing capability** — for the SPA fraction (~2–5% of domains) the parser sees the rendered shell only.
- **No persistent per-domain strategy learning.** `promotion.py:34–38` keeps tier-state in-memory per shard, so a domain that escalated to T3 yesterday starts at T1 again today (sections 3.2, 4.3).
- **No domain reputation cache.** A domain that failed yesterday is fetched again today with no cooldown (section 2.1).
- **No region- or locale-aware strategy.** TLD-based `Accept-Language` is set (`fetcher.py:_ACCEPT_LANGUAGE_BY_TLD`) but proxy region, tier defaults, anti-bot priors, and path dictionaries are English-only / region-agnostic (sections 3.9, 4.3, 10.3, 10.6, 10.9).
- **No PII detection, regional legal policy, or audit trail of policy decisions.** `regional_policy.json` does not exist; GDPR/CCPA/LGPD/PIPL not encoded (sections 15.4, 15.5, 15.6).
- **No structured cost-per-useful-record metric.** Cost journal has per-shard `cost_usd` and `domains_processed` but no `useful_records` field — making the framework's primary cost KPI uncomputable (section 12.2).
- **No automated drift detection or nightly re-crawl** (sections 11.6, 12.11). Quality drift relies on operator-initiated `metrics.py compare`.
- **No structured logging, Prometheus/StatsD metrics, or alert definitions** (sections 13.1, 13.2, 13.5). Logs are plain-text via `logging.basicConfig`.
- **No `SCRAPER_SPEC.md` / `CRAWLING_POLICY.md` / `FAILURE_PATTERNS.md` / `ARCHITECTURE.md` files exist** as named artifacts. Their content is partially embedded in `README.md`, `CHANGELOG.md`, `docs/PIPELINE.md`, `docs/phase4_implementation_plan.md`, `docs/vmss_*` plans, and `tools/phase4_cost_reduction_directive.md`, but never centralized (section 1.1).

---

## 3. Coverage Matrix

Legend — **F**=Full, **P**=Partial, **M**=Missing, **N/A**=Not applicable to current product scope. Severity — **C**=Critical, **H**=High, **M**=Medium, **L**=Low.

| Item | Pattern | Status | File evidence | Severity |
|---|---|---|---|---|
| 1.1a | `SCRAPER_SPEC.md` | M | (none — content scattered in `README.md`, `parser.py` docstrings, `CHANGELOG.md`) | M |
| 1.1b | `CRAWLING_POLICY.md` | M | (none — no AUP doc) | H |
| 1.1c | `FAILURE_PATTERNS.md` | M | (closest: `docs/validator_final_summary.md`, eval_data clusters) | M |
| 1.1d | `ARCHITECTURE.md` | M | (closest: `docs/PIPELINE.md`, `docs/phase4_implementation_plan.md`, `docs/vmss_orchestrator_plan.md`) | M |
| 1.1e | `CHANGELOG.md` | F | `CHANGELOG.md:1–196` | – |
| 1.1f | README explaining architecture/entry points | F | `README.md:1–300+` | – |
| 1.2a | Hierarchical intent taxonomy | P | `src/barcada_scraper/classifier/stage2/taxonomy.py` (23 tech sub-categories, flat); `configs/partner_type_definitions.yaml` (17 partner types, flat) | M |
| 1.2b | `PATH_DICTIONARY.json` / canonical path catalog | P | `src/barcada_scraper/classifier/page_acquisition/path_lists.py:55–118` (Python dicts, not JSON; English only) | M |
| 1.2c | Per-locale path dictionaries (not translations) | M | (none) | H |
| 1.2d | Strong vs weak label distinctions | M | (none) | M |
| 1.3a | `CRAWLING_POLICY.md` referenced in code | M | (no robots.txt parser; no rate-limit policy module) | H |
| 1.3b | `regional_policy.json` (GDPR/CCPA/LGPD/PIPL) | M | (none) | H |
| 1.3c | Domain blocklist for opted-out sites | P | `check_domains.py:443–550` parking domains (~150 patterns); no opt-out blocklist | M |
| 2.1a | DNS check before fetch | F | `src/barcada_scraper/domain_validator/check_domains.py:882–935` (async aiodns) | – |
| 2.1b | HEAD verifies 200 + content-length | F | `src/barcada_scraper/classifier/page_acquisition/fallback.py:79–167` ("~60% bandwidth saved") | – |
| 2.1c | Parked-domain detection (1KB probe) | F | `src/barcada_scraper/detection/placeholder.py` (shared module) | – |
| 2.1d | Domain reputation cache (N-day cooldown) | M | (none — in-memory promotion only) | H |
| 2.1e | Redirect-chain limit | F | `src/barcada_scraper/scraper/fetcher.py` `max_redirects=10` | – |
| 2.2a | Domains queued vs crawled metric | P | `src/barcada_scraper/orchestrator/phase_summary.py:76–97` (shard counts, no queue-skip metric) | M |
| 2.2b | Cost-per-domain pre vs post-filter | M | (no pre/post-filter cost separation) | M |
| 3.1.T0 | Polite plain HTTP w/ realistic headers | F | `src/barcada_scraper/scraper/fetcher.py:57–66`; `azure_fetcher.py` | – |
| 3.1.T1 | Plain HTTP + residential proxy | F | `src/barcada_scraper/classifier/page_acquisition/residential_proxy_fetcher.py` | – |
| 3.1.T2 | TLS-fingerprint-spoofing client (curl_cffi, tls-client) | M | (none — `aiohttp` and `httpx`; no JA3/JA4 spoof) | H |
| 3.1.T3 | Playwright + stealth | P | `src/barcada_scraper/scraper/renderer.py:66–220` (plain Playwright; no `playwright-stealth` / `undetected-playwright`) | M |
| 3.1.T4 | Playwright + residential proxy + behavioral | M | (no behavioral sim; no proxy passthrough in renderer) | M |
| 3.1.T5 | Commercial unblocker | P | `src/barcada_scraper/scraper/proxy_fetcher.py:29–40,89–100` (ZenRows + ScrapingBee, retry-only) | – |
| 3.1.T6 | Skip / mark unscrapeable | P | After T3 + paid retry, marked `bot_blocked`/`forbidden`; no permanent unscrapeable flag | M |
| 3.2a | Per-domain successful tier cached (persistent) | M | `promotion.py:34–38` in-memory per shard only | H |
| 3.2b | Per-domain failed tiers tracked (persistent) | M | (in-memory only) | H |
| 3.2c | Per-domain best proxy region learned | M | (no region selection logic) | M |
| 3.2d | Per-domain observed rate-limit tracked | M | (none) | M |
| 3.2e | Periodic re-validation of cached strategy | M | (no cache to re-validate) | L |
| 3.3a | HTML markers (cf-chl-bypass, "Just a moment") | F | `src/barcada_scraper/scraper/barriers.py:407–410` | – |
| 3.3b | Suspicious body length | F | `src/barcada_scraper/classifier/page_acquisition/fetcher_core.py:130–152` | – |
| 3.3c | Block-suggesting titles | F | `barriers.py:411–438` covers "automated access", "bot detection", "Access Denied" variants | – |
| 3.3d | 403/429/503 patterns | F | `fetcher_core.py:135–136`; `fetcher.py:432–437` | – |
| 3.3e | Redirect-to-login/verify/captcha detection | F | `barriers.py:682–702` `detect_redirect` | – |
| 3.3f | CAPTCHA iframe detection (reCAPTCHA/hCaptcha/Turnstile/Arkose) | P | `barriers.py:425–427`, `placeholder.py:568–569` (Turnstile, hCaptcha widget IDs, generic challenge); no Arkose marker | L |
| 3.3g | Identical response across distinct URLs (challenge signature) | M | (none) | M |
| 3.3h | Structured verdict `OK\|SOFT_BLOCK\|HARD_BLOCK\|CHALLENGE\|RATE_LIMIT` | P | `barriers.py:667–679` returns `cloudflare_challenge\|waf_challenge\|geo_block\|None`; `page_schema.py:110–129` adds `ERROR_RATE_LIMITED`, `ERROR_CLOUDFLARE`, `ERROR_WAF` — but not unified 5-state enum | M |
| 3.4a | TLS fingerprint awareness (JA3/JA4) | M | (none) | M |
| 3.4b | HTTP/2 frame/header ordering awareness | P | `fetcher.py:230–256,611–631` — HTTP/1.1 fallback when H2 short-body, ALPN forcing; not active fingerprint control | L |
| 3.4c | Client that spoofs browser fingerprints | M | (none — plain `aiohttp`/`httpx`) | M |
| 3.5a | Mouse movement sim | M | – | L |
| 3.5b | Realistic scroll behavior | M | – | L |
| 3.5c | Typing cadence | M | – | L |
| 3.5d | Randomized timing | P | `check_domains.py` `random.uniform(0.5,1.5)` jitter on retries | – |
| 3.6a | Per-domain token bucket | P | Per-host RPS lock (`residential_proxy_fetcher.py:144–153`); no formal token bucket | M |
| 3.6b | Jitter on request timing | F | `_global_sem` + `jitter_ms` (residential_proxy_fetcher.py:79,151) | – |
| 3.6c | Exponential backoff 1→2→4→8 capped | F | `fetcher.py:316–318` `min(2**attempt, 30)` | – |
| 3.6d | Concurrent connection cap per domain | F | Per-host locks (`_host_locks`) + global semaphore | – |
| 3.6e | Honor `Retry-After` | F | `fetcher.py:432–437` `_retry_wait` (60s cap) | – |
| 3.7a | Robots.txt parser | **M** | (none — grep returns 0 matches in src/) | **C** |
| 3.7b | Robots.txt compliance enforced in code | **M** | (none) | **C** |
| 3.7c | User-Agent + contact email | P | `check_domains.py:140` `Mozilla/5.0 (compatible; Barcada/1.0)` — no contact email | M |
| 3.7d | `Crawl-delay` respected | M | (none) | H |
| 3.8a | Default skip CAPTCHA | P | Implicit — `classify_page_barrier` returns `waf_challenge`, no solver; not documented policy | M |
| 3.8b | Explicit authorization to solve | M | (no authz model) | M |
| 3.8c | No model training to defeat CAPTCHAs | F | (no such code; `tools/phase4_*` doc explicitly avoids it) | – |
| 3.8d | Policy enforced in code | M | (no policy module) | M |
| 3.9a | Regional anti-bot strategy awareness | M | (none) | M |
| 3.9b | Region-specific tier defaults | M | (none) | M |
| 3.9c | Region-specific failure tracking | M | (none) | M |
| 3.10a | `BOT_BLOCK_IP_REPUTATION` | M | – | M |
| 3.10b | `BOT_BLOCK_TLS_FINGERPRINT` | M | – | M |
| 3.10c | `BOT_BLOCK_JS_CHALLENGE` | P | `page_schema.py:110–129` `ERROR_CLOUDFLARE` (proxy) | M |
| 3.10d | `BOT_BLOCK_CAPTCHA` | P | `ERROR_WAF` (proxy) | M |
| 3.10e | `BOT_BLOCK_BEHAVIORAL` | M | – | L |
| 3.10f | `BOT_BLOCK_GEO` | F | `barriers.py:439–447` `_RE_GEO_BLOCK` | – |
| 3.10g | `BOT_BLOCK_RATE` | F | `ERROR_RATE_LIMITED` | – |
| 3.10h | `BOT_BLOCK_UNKNOWN` | F | `ERROR_OTHER` | – |
| 3.10i | Routing logic to remediation | P | `promotion.py:93–133` — escalate to T3 after 2 protection failures, no per-type routing | M |
| 4.1 | `ProxyProvider` uniform interface | F | `proxy_provider.py:48–78` | – |
| 4.1b | `get_proxy(region, sticky_session_id?)` | P | `proxy_url()` only — no region or session args | M |
| 4.1c | `report_success / report_failure` callbacks | M | (no telemetry callbacks on Provider) | M |
| 4.1d | `current_balance()` + `list_supported_regions()` | M | (no balance/regions API) | L |
| 4.1e | No direct provider API calls outside abstraction | F | All fetchers use `proxy_url()` only | – |
| 4.2a | Failover ladder primary→backup→DC→unblocker→skip | P | T1→T3 / T2→T3, then ZenRows/ScrapingBee retry pass; no "skip after N failures" flag | M |
| 4.2b | Tier escalation by failure type | P | Only "protection signature" triggers (`promotion.py:55,93–133`) | M |
| 4.2c | Skip threshold | M | (none) | M |
| 4.3a | Per-domain provider selection from telemetry | M | Cheapest-first at startup (`proxy_provider.py:291`); no per-domain adaptation | M |
| 4.3b | Preferred provider per domain cached | M | – | M |
| 4.3c | Per-provider per-domain success rate | M | – | M |
| 4.4a | Sticky session support | M | `proxy_provider.py:56–58` explicitly stateless ("rotation is the provider's job server-side") | M |
| 4.4b | Per-request rotation | F | Stateless `proxy_url()` rotates server-side | – |
| 4.4c | Session selection rules | M | – | L |
| 4.4d | Session release on completion | M | – | L |
| 4.5a | Credentials in secrets manager | P | Env vars (`_load_provider_from_env`, `proxy_provider.py:122–154`); no Doppler/Infisical/AWS SM integration | M |
| 4.5b | Credentials encrypted/redacted in logs | P | Implicit via httpx URL masking; no explicit redaction filter | M |
| 4.5c | IP allowlisting | M | (no allowlist API) | L |
| 4.6a | Resource blocking at browser level | F | `renderer.py:49–58,215–220` blocks image/font/stylesheet/media/texttrack/manifest | – |
| 4.6b | Gzip/Brotli negotiated | F | `fetcher.py:60` `Accept-Encoding: gzip, deflate, br` | – |
| 4.6c | HEAD requests | F | `fallback.py:79–167` (60% savings) | – |
| 4.6d | Early bailout on non-HTML | F | `parser.py:1612–1651` `_NON_PAGE_EXTENSIONS`; `fetcher.py:139` 2MB cap | – |
| 4.7a | Latency p50/p95 tracked | M | (none) | M |
| 4.7b | Success rate per provider | M | (no per-provider counters) | M |
| 4.7c | Per-region success rate | M | – | M |
| 4.7d | Error distribution per provider | M | – | M |
| 4.7e | Auto-traffic-shift on degradation | M | – | M |
| 4.8a | Provider-level concurrency cap | F | `max_concurrent=30 (DC)` / `15 (RES)` | – |
| 4.8b | Per-domain concurrency cap | F | Per-host locks | – |
| 4.8c | Interaction managed | F | Both are composed | – |
| 4.9a | No premium-only dependency | F | All providers `enabled: false` by default in YAML | – |
| 4.9b | Backup provider configured | F | Multiple providers per tier in YAML | – |
| 4.9c | Datacenter for cheap domains | F | T2 routes to DC providers | – |
| 4.9d | Mobile proxy bounded | N/A | (no mobile proxy use) | – |
| 4.10a | Provider IP sourcing documented | P | YAML inline comments only | L |
| 4.10b | AUP review documented | M | (none) | M |
| 4.10c | Provider performance dashboard | M | (bandwidth_journal exists; no dashboard) | L |
| 5.1a | Sitemap.xml-first discovery | M | (no XML sitemap parser) | H |
| 5.1b | Robots.txt parsing | M | (none) | H |
| 5.1c | Hreflang link extraction | F | `parser.py:455–571` | – |
| 5.1d | Internal-link fallback | F | `link_discovery.py:1–100` | – |
| 5.2a | URL normalization | F | `link_discovery.py:175,319,414`; `parser.py:2413–2458` | – |
| 5.2b | Tracking params stripped | F | `parser.py:1590–1609` (utm_*, fbclid, gclid, msclkid, dclid, ref, source, mc_cid, _ga, _gl) | – |
| 5.2c | Session params stripped | P | Generic query strip in `link_discovery.py:239–240`; named session params (`sid`, `phpsessid`, `sessionid`) not explicit | M |
| 5.2d | Pagination duplicate detection | P | Trailing-slash normalization; no `?page=N` family dedup | M |
| 5.2e | Hash route resolution | F | `link_discovery.py:240` fragment strip | – |
| 5.2f | Canonical URL extraction | P | Same-host check in parser; no `<link rel=canonical>` explicit lookup at queue stage | M |
| 5.2g | Case-sensitive path preservation | F | Implicit (no lowercasing) | – |
| 5.2h | Trailing slash normalization | F | `link_discovery.py:175` `path.rstrip('/') or '/'` | – |
| 5.3a | Crawl depth cap per domain | F | `path_lists.py:55–118` (8 T1/T2 paths, 4 T3 paths) | – |
| 5.3b | Per-intent target page lists | F | `path_lists.py` (about, products, solutions, services, customers, pricing, industries) | – |
| 5.3c | Pagination cap | P | No explicit handling; relies on fixed path lists | L |
| 5.3d | Skip archive/date URLs | P | `link_discovery.py:78–102` blocklist (no date pattern) | L |
| 5.3e | Skip search results | F | `link_discovery.py:94` `/search` blocked | – |
| 5.4a | Canonical URL dedup | P | Trailing slash + tracking strip only | M |
| 5.4b | Content-hash dedup | M | (none) | M |
| 5.4c | Cross-locale variant linking | P | Hreflang extracted but variants not explicitly linked | M |
| 6.1a | SPA detection: <5KB body | F | `detection/placeholder.py:1522–1643` (Path C/D thresholds) | – |
| 6.1b | Empty `#root`/`#app`/`[data-reactroot]` | F | `_RE_SPA_MOUNT` (`placeholder.py:495–498`) | – |
| 6.1c | Framework fingerprints (Next/Nuxt/Vue/Angular/Svelte/Remix) | P | `_RE_SPA_FRAMEWORK_MOUNT` covers `__next`, `__nuxt`, `__gatsby`, `data-reactroot`, `ng-app` (placeholder.py:532–534); Vue, Svelte, Remix less explicit | M |
| 6.1d | Wappalyzer-style tech detect | M | (none) | L |
| 6.1e | Per-domain SPA decision cached | M | (no cache across runs) | M |
| 6.2a | `__NEXT_DATA__` extraction | **M** | (no grep match) | **H** |
| 6.2b | `window.__NUXT__` | **M** | – | **H** |
| 6.2c | `window.___INITIAL_PROPS___` (Gatsby) | M | – | M |
| 6.2d | `window.__remixContext` | M | – | M |
| 6.2e | `data-sveltekit-fetched` | M | – | M |
| 6.2f | `window.__APOLLO_STATE__`, `__PRELOADED_STATE__` | **M** | – | **H** |
| 6.2g | Hydration-first enforcement before render | **M** | (renderer goes straight to Playwright) | **H** |
| 6.3a | T1 `domcontentloaded` | F | `renderer.py:176` | – |
| 6.3b | T2 networkidle 500ms | M | – | M |
| 6.3c | T3 custom readiness selectors | M | – | M |
| 6.3d | T4 mutation observer w/ quiet period | M | – | M |
| 6.3e | T5 fixed wait logged | P | `renderer.py:181–188` polling loop (500ms × 10) | L |
| 6.3f | No bare sleep() in production | F | All waits purpose-driven | – |
| 6.4a | XHR/fetch logging during render | M | (only resource blocking) | H |
| 6.4b | GraphQL/REST API identification | M | – | H |
| 6.4c | API endpoint discovery + persistence | M | – | H |
| 6.4d | `discovered_apis.json` | M | – | M |
| 6.5a | Resource blocking | F | `renderer.py:49–58,215–220` | – |
| 6.5b | WebGL/audio/video disabled | P | Media route blocked; WebGL/audio not explicit | L |
| 6.5c | Browser context reuse across pages | F | `renderer.py:98–105` page pool | – |
| 6.5d | Render budget per page | P | 10s timeout + 5s poll (fixed; no per-domain budget) | M |
| 6.5e | Render result caching | M | (none) | M |
| 6.6a..g | SPA failure taxonomy entries | M | Generic exception only (`renderer.py:196–197`) | M |
| 6.7a | Route discovery — sitemap-first | M | (no sitemap parser) | H |
| 6.7b | Next.js `buildManifest.js` extraction | M | – | M |
| 6.7c | Router config in JS bundles | M | – | M |
| 6.7d | Hydration internal links | M | (no hydration extraction) | H |
| 6.7e | Path probing fallback | F | `path_lists.py` fixed paths | – |
| 6.8 | Render reconciliation (two-render compare) | M | (none) | M |
| 7.1a..d | `<nav>`, role=navigation, header/footer, aria-label | F | `parser.py:1322–1413,2590–2615,3091–3320` | – |
| 7.1e | role=menu/menubar/menuitem | F | `parser.py:1366–1369` | – |
| 7.1f | Multiple nav regions extracted separately | F | `parser.py:3241–3291` | – |
| 7.2a | Top viewport + link density | F | `parser.py:3263–3290` | – |
| 7.2b | Bottom DOM column structure | F | Footer column scan at `parser.py:3188–3227` | – |
| 7.2c | Sticky/fixed detection | M | – | L |
| 7.2d | Spatial link clustering | P | `parser.py:3283` max parent-counts | – |
| 7.3a | Tree structure, not flat | F | `parser.py:2052–2070`, `3292–3306` (3-level nesting) | – |
| 7.3b | DOM nesting (li>ul) | F | Recursive descent | – |
| 7.3c | aria-expanded / aria-controls | F | `parser.py:1374,2105,2128` | – |
| 7.3d | Visual indentation | M | (DOM-only) | L |
| 7.3e | Heading hierarchy in mega menus | F | `parser.py:1395` | – |
| 7.4a | Top nav mega menu activation | F | `parser.py:1374–1375,2288` | – |
| 7.4b | Mega menu column-aware | F | `parser.py:2219–2227` | – |
| 7.4c | Footer column extraction | F | `parser.py:3188–3227` | – |
| 7.4d | Sidebar nav | P | Covered by mobile-merged candidates | – |
| 7.4e | Breadcrumbs | P | Class-based only (`parser.py:1413`); no JSON-LD `BreadcrumbList` extraction | M |
| 7.4f | Mobile menu | F | `parser.py:3250–3258` | – |
| 7.4g | Utility nav | F | Merged at `parser.py:3241–3248` | – |
| 7.5a | Trigger detection (aria-expanded etc.) | F | `parser.py:1374–1375` | – |
| 7.5b | Hover sweep | **M** | (parser is static-DOM; no Playwright interaction) | **H** for SPA mega menus |
| 7.5c | Click sweep | M | – | H for SPA mega menus |
| 7.5d | Focus+Enter sweep | M | – | M |
| 7.5e | Desktop 1440 + mobile 375 viewport sweep | M | – | M |
| 7.5f | State reset between attempts | M | – | L |
| 7.6 | Mobile menu as hierarchy source | F | `parser.py:3250–3258` (NAV-02) | – |
| 7.7a | `nav aria-label="Breadcrumb"` | P | Class-based catch-all only | M |
| 7.7b | `ol.breadcrumb` | M | (not by name) | L |
| 7.7c | JSON-LD `BreadcrumbList` preferred | M | (not specialized despite full JSON-LD support elsewhere) | M |
| 8.1a | `<main>`, role=main, `<article>` | F | Trafilatura primary (`extraction.py:114–162`) | – |
| 8.1b | Readability-style fallback | F | Trafilatura uses jusText-style heuristics | – |
| 8.1c | Visual density and clustering | P | Trafilatura implicit | – |
| 8.2a..g | Cross-page boilerplate fingerprinting | **M** | `text_cleaning.py:411–484` is per-page pattern matching, NOT cross-page frequency hashing | **H** |
| 8.3a | getBoundingClientRect zero-dim filter | M | (static parsing; Playwright doesn't post-eval) | M |
| 8.3b | display:none filter | F | `parser.py:97–100,3384` `_RE_HIDDEN_INLINE_STYLE` | – |
| 8.3c | visibility:hidden filter | F | Same regex | – |
| 8.3d | opacity:0 filter | M | – | L |
| 8.3e | Offscreen positioning filter | M | – | L |
| 8.3f | aria-hidden="true" filter | F | `parser.py:3380` | – |
| 8.4a | script/style/noscript/template/[hidden] | F | `parser.py:3363`; `extraction.py:106–108` | – |
| 8.4b | nav/header/footer | F | `parser.py:3365` | – |
| 8.4c | Cookie banner / consent UI | P | Decorative class regex (`parser.py:1296–1299`) catches some | M |
| 8.4d | Newsletter / signup form | P | Form stripped, not flagged | L |
| 8.4e | Social share buttons | M | – | L |
| 8.4f | Back-to-top | P | Covered by decorative classes | L |
| 8.4g | Search form / search bar | F | Form strip in `extraction.py:107` | – |
| 8.4h | Language switcher | M | – | M |
| 8.4i | Chat widgets (Intercom/Drift/Zendesk) | **M** | (no markers) | M |
| 8.4j | Related/popular/recommended | P | Link-density filter implicit | M |
| 8.4k | Ads/sponsored | M | – | L |
| 8.4l | Popups/modals | M | – | L |
| 8.5a | Carousel detection (role=region+aria-roledescription) | P | `swiper`/carousel class strip only (`parser.py:1297`) | M |
| 8.5b | Tab detection (role=tablist) | M | – | M |
| 8.5c | Accordion detection (`<details>`, .accordion) | M | – | M |
| 8.5d | Active vs all-panel extraction | M | – | M |
| 8.6a | Similarity hashing (SimHash/MinHash) | **M** | (none) | M |
| 8.6b | Block-level dedup threshold | P | Exact line dedup only (`text_cleaning.py:456–484`) | M |
| 8.6c | Keep-first-occurrence rule | F | `text_cleaning.py:456` | – |
| 8.7a | Link density >0.5 | M | (no post-extraction check) | M |
| 8.7b | Text density | P | Trafilatura implicit; BS4 fallback chosen if 3× larger | L |
| 8.7c | Position-based boundaries | M | – | L |
| 8.8 | Per-intent allowlists | M | (no intent-specific extraction) | H |
| 8.9 | Distillation profiles per-intent | M | (single 8KB cap only) | H |
| 8.10 | Two-pass cleaning | F | `extraction.py` Trafilatura vs BS4 + `text_cleaning.py` 9-step | – |
| 8.11a | HTML→Markdown | M | (plain text output) | M |
| 8.11b | Headings preserved | P | Trafilatura implicit | – |
| 8.11c | Lists preserved | P | – | – |
| 8.11d | Tables preserved | M | `extraction.py:90–96` `include_tables=False` | M |
| 8.11e | Images replaced with alt text | M | `include_images=False` | L |
| 8.11f | Links preserved | M | `include_links=False` | M |
| 8.11g | Whitespace collapsed | F | `text_cleaning.py` | – |
| 8.12a | JSON-LD parsing (~120 types incl. Product/Org/Article/Review/FAQPage/BreadcrumbList/HowTo/Recipe/Event) | F | `parser.py:4456–4831`; flag set in `CHANGELOG.md:101–113` | – |
| 8.12b | Microdata parsing | M | (none) | M |
| 8.12c | OpenGraph | P | `parser.py:5741–5743` og:title/description/type | M |
| 8.12d | Twitter Card | M | (none) | L |
| 8.12e | Emitted as separate output from prose | F | Top-level `jsonld` block (per CHANGELOG) | – |
| 8.13a | Link density on output | M | – | M |
| 8.13b | Repetition check (100+ char 3× in output) | P | Line-level dedup only | M |
| 8.13c | Length check vs intent minimum | P | `_MIN_TEXT_LENGTH=200` global (`extraction.py:145–162`) | M |
| 8.13d | Stop-word ratio | M | – | L |
| 8.13e | Structural loss check | M | – | M |
| 9.* | Label-to-intent matching cascade (T1 dict / T2a synonyms / T2b embeddings / T2c WordNet / T3 LLM) | **N/A / M** | Product is **domain classification**, not nav-label intent matching. Stage 1/2/3 classifier resolves *domains* to *categories*, not *labels* to *intents*. The parser does normalize labels (`parser.py:1914–1941`) but there is no intent taxonomy keyed to nav labels. | N/A (scope) — but **if the goal is generic intent extraction, this is C** |
| 9.1 | Tier1 dictionary match — Unicode NFC, whitespace, decorative strip | P | `parser.py:1914–1941`; no article/stop-word strip, no plural normalization | M (for the limited intent use) |
| 9.2 | Curated synonym lists | M | (none) | M |
| 9.3 | Embedding similarity | P | `embedder.py` text-embedding-3-small used for *domain* features, not intent centroids; not multilingual | M |
| 9.4 | WordNet candidate gen | M | – | L |
| 9.5 | LLM fallback | P | LLM tier exists for *classification* (gpt-4.1-nano/mini/4.1), not for label resolution | – |
| 9.6 | Three-signal confidence (label/URL/destination) | M | – | M |
| 9.7 | Destination signal catalogs | M | – | M |
| 9.8 | Position weighting | P | `parser.py:3478–3480` header/footer dedup; no weights | M |
| 9.9 | Negative-match list | P | `parser.py:1944–1973` `_is_noise_label` (noise only) | M |
| 9.10 | Industry conditioning | P | Stage 2 pre-classifies tech vs non-tech; not used for nav labels | M |
| 9.11 | Novel label handling | M | – | M |
| 9.12 | Learning loop | M | `llm/prompt_logger.py` logs cost only, not for synonym mining | M |
| 9.13 | Per-locale maintenance | M | – | M |
| 10.1 | Locale discovery (hreflang/lang/switcher/sitemap) | P | Hreflang done (`parser.py:455–490`); HTML `<html lang>` not extracted; no sitemap | M |
| 10.2 | Locale crawl scope per domain | P | English-alt fallback (`english_alternative.py`); no per-domain scope file | M |
| 10.3 | Geo-routing per domain | P | TLD→Accept-Language (`fetcher.py:_ACCEPT_LANGUAGE_BY_TLD`); no proxy region routing | M |
| 10.4a | chardet/charset-normalizer | M | (relies on aiohttp defaults) | M |
| 10.4b | NFC normalization | F | `parser.py:1924`, `check_domains.py:24` | – |
| 10.4c | Per-page language detection | F | `parser.py:271–330` cld3 → pycld2 → langdetect | – |
| 10.4d | Original + normalized stored | P | `crawl_meta.language_detected/confidence` | – |
| 10.5a | CJK tokenization (jieba/MeCab/KoNLPy) | M | – | M |
| 10.5b | RTL awareness | M | – | M |
| 10.5c | Mixed-script handling | M | – | M |
| 10.6 | Per-locale path dictionaries | M | `path_lists.py:55–91` English only | H |
| 10.7a | JSON-LD / schema.org | F | `parser.py:213–224, 4456–4831` | – |
| 10.7b | OpenGraph | P | `parser.py:5741–5743` | – |
| 10.7c | External links (LinkedIn/GitHub/Twitter) | P | Signals exist; not as cross-domain identity hash | M |
| 10.7d | Email/phone country codes | M | – | M |
| 10.7e | Address microdata | P | `org_address_locality` extracted | – |
| 10.7f | Currency symbols/ISO | M | – | M |
| 10.7g | Wappalyzer | M | – | L |
| 10.8 | LLM extraction in native language | P | `english_alternative.py:142` mentions translation, no enforced native-lang prompting | M |
| 10.9 | Per-region anti-bot | M | – | M |
| 10.10 | Regional legal policy (GDPR/CCPA/LGPD/PIPL) | **M** | (none) | **H** |
| 10.11 | SPA × i18n | M | – | M |
| 10.12 | Cross-regional entity resolution | M | – | M |
| 10.13 | Locale-stratified eval | M | `eval_data/README.md` lacks per-locale stratification | H |
| 10.14 | Native-speaker validation queue | M | – | M |
| 11.1 | Golden set (100–500+ stratified) | P | `eval_data/stage1_labels.jsonl` (220 rows; modified mid-audit), `stage2_labels.jsonl`, `stage3_labels.jsonl`, `canary_50_domains.txt` | M |
| 11.1b | Stratified by locale | M | Not documented | M |
| 11.1c | Stratified by intent / site-type / complexity | P | Stage stratification only (business/tech/partner) | M |
| 11.2 | Acceptance metric composite formula | P | `metrics.py:255–303` precision/recall/F1; thresholds in `configs/stage1_thresholds.yaml`; no explicit composite formula or tolerance bands | M |
| 11.3 | Eval runner scripted | F | `barcada-classify` console scripts; `metrics.py:764–932` `compare`/`diagnose` CLI; `evaluate.py` per stage | – |
| 11.3b | nav_recall/footer_recall etc. metrics | F | `metrics.py:215–252` | – |
| 11.3c | Per-intent precision/recall | P | Per-stage only | M |
| 11.3d | Per-locale separate scoring | M | – | M |
| 11.4 | Fixture-based tests (static, SPA, mega-menu, mobile, parked, bot-blocked) | F | `tests/fixtures/html/` 23 directories (cloudflare_challenge, login_wall, auth_403, soft_404, spa_shell, meta_refresh_parking, 12 parking subtypes, etc.) | – |
| 11.4b | SPA fixtures (Next/React/Vue/Angular/CSR/ISR) | P | `spa_shell/` (~22 captured shells; not framework-tagged) | M |
| 11.4c | Raw HTML + hydration payloads + HAR | P | HTML yes; hydration payloads no (none extracted); HAR no | M |
| 11.4d | Deterministic, not live-network | F | Static files | – |
| 11.5 | Regression test infra on every change | P | Diff in `metrics.py:346–397`; no CI gate found | M |
| 11.5b | Zero-regression policy | P | `CLAUDE.md` policy lines exist; not enforced automatically | M |
| 11.6 | Drift detection (nightly re-crawl) | M | – | M |
| 11.7 | Classifier-loop validation | P | Per-stage evals exist; no bi-directional extraction↔classifier feedback | M |
| 12.1 | Cost telemetry per crawl, stage breakdown | F | `cost_journal.py` (`ShardRecord`, `CostTotals` with per-stage USD; outcome `completed/cost_ceiling_stopped/not_reached`) | – |
| 12.2 | Cost per useful record | **M** | `phase_summary.py:76–97` has cost_usd + domains_processed, no useful_records | **H** |
| 12.3 | Per-domain budgets w/ hard kill 2× | M | Global ceiling only (`cost_journal.ceiling_usd`) | H |
| 12.4 | Per-stage budgets within a crawl | P | `bandwidth_tracker.py:65–100` (T1/T2/T3 + `stage_budget_usd`, kill @ 0.95) | – |
| 12.4b | LLM token budget per task | M | Global cost_tracker only | M |
| 12.5 | Daily/weekly/monthly caps | M | No time-window roll-up | M |
| 12.6 | Domain value tiering (HIGH/STD/LOW) | M | – | M |
| 12.7 | Efficiency flags (11-entry enum) | M | (none) | H |
| 12.8a | Deterministic-first (LLM as fallback) | F | Stage 1 RULES → LR → LLM cascade | – |
| 12.8b | LLM aggressive caching | F | Azure prompt cache; `cached_input_tokens` tracked; ≥80% hit-rate target | – |
| 12.8c | Batched calls | F | `stage1/run.py` batches | – |
| 12.8d | Cheapest capable model per task | F | gpt-4.1-nano / mini / 4.1 routing | – |
| 12.8e | Token budgets per task type | P | (max_cost_usd, not max_tokens) | M |
| 12.8f | Distilled (not raw HTML) sent to LLM | F | `ml_text` (≤2048 bytes; section markers) per `CHANGELOG.md:94–98` | – |
| 12.9 | Storage lifecycle | M | (no compression-on-write, no hot/warm/cold) | M |
| 12.10a | Failure-type-aware retry | P | (only protection-signature triggers escalation) | M |
| 12.10b | Three-strikes permanent backoff | M | – | M |
| 12.10c | Resumable/checkpointable | F | `--resume-run-id` in `docs/PIPELINE.md:104–118`; `cost_journal` replays | – |
| 12.11 | Re-crawl (adaptive, ETag, If-Modified-Since) | **M** | (none) | M |
| 12.12 | Cost dashboards (op/diag/strat) | P | `phase_summary.json` + `metrics.py` text summaries; no Grafana | M |
| 13.1 | Structured logging (trace IDs, stage tags, fields) | P | `logging.basicConfig` plain text; no trace_id field; run_id exists but not in log lines | H |
| 13.2 | Metrics emission (Prometheus/StatsD) | **M** | (none) | H |
| 13.3 | Failure taxonomy complete catalog | P | `page_schema.py:110–129` error_kinds; `barriers.py` barrier types; not unified | M |
| 13.3b | Routing logic to remediation | P | `promotion.py:93–133` (T1/T2 → T3 only) | M |
| 13.4 | Dashboards / configs | P | `phase_summary.json`, `metrics.py` text; no vendor configs | M |
| 13.5 | Alert definitions | M | – | H |
| 13.6 | Per-domain health tracking | M | (per-shard only) | M |
| 14.1 | Failure clustering (root cause + features) | P | Manual analysis in `docs/validator_final_summary.md`; no auto-cluster output | M |
| 14.1b | `failure_clusters.json` | M | – | M |
| 14.2 | Cluster prioritization (impact/effort) | P | Manual in `tools/phase4_cost_reduction_directive.md` | – |
| 14.2b | `improvement_backlog.json` | M | – | L |
| 14.3 | Automated patching (headless Claude) | M | – | L |
| 14.4 | Validation gauntlet (unit/fixture/cluster/full/cost/determinism/stat sig) | P | Unit + fixture present; no automatic gauntlet on patches | M |
| 14.5 | Auto-merge guardrails | M | – | L |
| 14.6 | Plateau detection | M | – | L |
| 14.7 | Cost-aware loop (cost-adjusted composite) | P | Phase 4 directive measures cost-per-lever manually | M |
| 14.8 | Multi-strategy ensembling (CSS/JSON-LD/PW/LLM reconcile) | **M** | Sequential pipeline only | M |
| 14.9 | Continuous golden-set growth | P | Eval data exists, human-labeled only; no daily prod sample auto-routing | M |
| 14.10 | Loop observability (score over time, plateau indicator) | M | – | L |
| 15.1a | Secrets manager integration | M | Env vars only | M |
| 15.1b | No creds in code | F | All env-var sourced | – |
| 15.1c | No creds in env vars committed | F | `.env` gitignored | – |
| 15.1d | Redacted in logs/telemetry | P | Implicit; no explicit filter | M |
| 15.2a | Robots.txt parser | **M** | (none) | **C** |
| 15.2b | Compliance enforced in code | **M** | (none) | **C** |
| 15.2c | Crawl-delay honored | M | – | H |
| 15.2d | Bypass requires authorization | M | – | M |
| 15.3a | Default skip CAPTCHA enforced in code | P | Implicit via no-solver presence; not a documented gate | M |
| 15.3b | Override requires documented authz | M | – | M |
| 15.3c | No automated solving without authz | F | (no solver dependency) | – |
| 15.3d | No CAPTCHA-defeating model training | F | (no such training) | – |
| 15.4 | PII detection + redaction + regional rules + audit | **M** | (none) | **H** |
| 15.5 | `regional_policy.json` + field-level emit rules | **M** | (none) | **H** |
| 15.6a | What/when/under-what-policy crawl log | P | Cost journal + bandwidth journal track runs; no policy version stamp per crawl record | M |
| 15.6b | Per-domain crawl history | M | – | M |
| 15.6c | Policy version tracked per crawl | M | `feature_schema_version` and `TAXONOMY_VERSION` exist but not a "policy version" | M |
| 15.6d | Compliance reporting | M | – | M |

---

## 4. Detailed Findings

### Section 1 — Foundation & Specifications

**Status:** PARTIAL. The codebase has rich docs but not at the named-artifact level the framework expects.

- `README.md` (`README.md:1–300+`) is large and describes the four-stage pipeline, CLI flags, and operational examples — but is mostly user-facing. There is **no `SCRAPER_SPEC.md`, `CRAWLING_POLICY.md`, `FAILURE_PATTERNS.md`, or `ARCHITECTURE.md`** (grep returned zero matches). [**Severity: M**]
- `CHANGELOG.md:1–196` is exemplary: explicit `feature_schema_version` versioning, dated entries, removal/addition/change sections. [**Strength**]
- `DEFERRED_WORK.md:1–52` is an honest ledger of intentional `NotImplementedError`s — a pattern worth promoting elsewhere. [**Strength**]
- `docs/PIPELINE.md`, `docs/phase4_implementation_plan.md`, `docs/vmss_orchestrator_plan.md`, `docs/vmss_runbook.md` together cover operator + architecture content, but at ~150KB+ across separate files. A single `ARCHITECTURE.md` index would be helpful. [**Severity: M**]
- **Taxonomies are flat** (`stage2/taxonomy.py` 23 categories; `configs/partner_type_definitions.yaml` 17 partner types). There is no parent/child intent hierarchy. [**Severity: M**]
- **No `PATH_DICTIONARY.json`** — closest equivalent is `src/barcada_scraper/classifier/page_acquisition/path_lists.py:55–118` (Python literals). Per-locale paths absent. [**Severity: H**]
- **No `regional_policy.json`** — no encoded GDPR/CCPA/LGPD/PIPL rules. [**Severity: H**]

**Recommended actions:** Author `ARCHITECTURE.md` (index of existing docs), `CRAWLING_POLICY.md` (robots.txt stance, rate-limit policy, UA + contact), and `FAILURE_PATTERNS.md` (cluster catalog with fixes). Move taxonomy YAMLs/JSONs to a `docs/taxonomy/` directory with explicit parent/child linkage.

### Section 2 — Domain Triage

**Status:** PARTIAL.

- DNS pre-check: full. `domain_validator/check_domains.py:882–935` uses async aiodns with retry + www fallback. [**Strength**]
- HEAD precheck: full. `classifier/page_acquisition/fallback.py:79–167`; comment claims ~60% bandwidth savings. [**Strength**]
- Parked detection: full. `detection/placeholder.py` is shared between validator and parser (re-extracted in v2 refactor — `CHANGELOG.md:172–179`). [**Strength**]
- **Domain reputation cache: MISSING.** Failed domains can be retried on every run. Add a parquet/SQLite cache keyed on domain with `last_failed_at`, `failure_kind`, and `next_retry_after`. [**Severity: H**]
- Redirect cap: `max_redirects=10` (`scraper/fetcher.py`). Default is reasonable; consider lowering for unknown-tier-1 domains.
- **Triage metrics: PARTIAL.** `phase_summary.py:76–97` exposes shard-level counts; queued-vs-crawled visibility and cost-per-domain pre/post-filter not separated. [**Severity: M**]

### Section 3 — Fetching Strategy & Anti-Bot

**Status:** PARTIAL — strong block detection, weak strategy learning, no robots.txt.

- **3-tier ladder, not 7.** T1=Azure egress; T2=datacenter proxy; T3=residential proxy; ZenRows/ScrapingBee as a paid-API retry pass (`scraper/proxy_fetcher.py:29–40,89–100`). No TLS-fingerprint client (`curl_cffi`, `tls-client`), no `playwright-stealth`/`undetected-playwright`. [**Severity: H** for sites that gate on JA3/JA4]
- **Block detection is the codebase's strongest area.** `scraper/barriers.py:407–447`:
  - Cloudflare challenge: `_RE_CLOUDFLARE_CHALLENGE` (lines 407–410)
  - WAF coverage: Akamai, DataDome, Incapsula/Imperva, Sucuri/Cloudproxy, Wordfence, DDoS-Guard, Kasada (`ks-cc`), PerimeterX/HUMAN, F5 Shape (`shape.min.js`), AWS WAF token (`barriers.py:411–438`)
  - CAPTCHA widgets: Cloudflare Turnstile, hCaptcha widget IDs, generic challenge wording (lines 424–429)
  - Geo-block: English + Chinese phrases (lines 439–447) [**Strength**]
- **No `robots.txt` parser anywhere** in the codebase. Grep across `src/` and `*.py` returns zero `robotparser`/`robots.txt` (the only "robots" occurrence is `<meta name="robots" content="noindex">` detection at `barriers.py:487`). [**Severity: C** for compliance]
- **No User-Agent contact email.** `check_domains.py:140` uses `"Mozilla/5.0 (compatible; Barcada/1.0)"` — generic Mozilla impersonation with no operator contact. The crawler is not identifiable to webmasters. [**Severity: M**]
- **Anti-bot taxonomy is partial.** `classifier/page_acquisition/page_schema.py:110–129` has `ERROR_RATE_LIMITED`, `ERROR_CLOUDFLARE`, `ERROR_WAF`, etc., but no IP-reputation, TLS-fingerprint, or behavioral subtypes; routing logic at `promotion.py:93–133` only escalates on "protection signature", not per-type. [**Severity: M**]
- **No per-domain strategy learning across runs.** Tier state is in-memory per shard (`promotion.py:34–38`). A domain that needed T3 yesterday starts at T1 again today. [**Severity: H** — easy to fix]
- Rate-limiting is adequate: per-host RPS lock + global semaphore + jitter (`residential_proxy_fetcher.py:79,144–153`), exponential backoff (`fetcher.py:316–318`), `Retry-After` honored (`fetcher.py:432–437`). [**Strength**]

### Section 4 — Proxy Integration

**Status:** PARTIAL → mostly FULL on architecture, MISSING on telemetry.

- **`ProxyProvider` Protocol is clean.** `classifier/page_acquisition/proxy_provider.py:48–78` — runtime-checkable Protocol with `name`, `cost_per_gb_usd`, `proxy_url()`. Frozen dataclass implementations. Credentials are env-only (`_load_provider_from_env`, lines 122–154); YAML cannot leak credentials. [**Strength**]
- **No `get_proxy(region, sticky_session_id?)`**, no `report_success/report_failure`, no `current_balance()`. Provider is stateless ("rotation is the provider's job server-side" — lines 56–58). For non-sticky sessions this is fine; for multi-page coherent crawls (mega-menu activation) it removes an axis of optimization. [**Severity: M**]
- Failover is `T1→T3` or `T2→T3` (`promotion.py:13–55`) plus a separate paid-API retry pass for `bot_blocked`/`forbidden` outputs. No "skip after N residential failures" terminal state. [**Severity: M**]
- Cheapest-first selection is at startup only (`proxy_provider.py:291`); per-domain provider learning absent. [**Severity: M**]
- Bandwidth controls are strong: `Accept-Encoding: gzip, deflate, br` (`fetcher.py:60`), 2MB response cap (`fetcher.py:139`), HEAD precheck (~60% saved per comments), non-page extension blocklist (`parser.py:1612–1651`). [**Strength**]
- **No pool-health metrics.** No p50/p95 latency tracking, no per-provider success-rate gauge, no auto-traffic-shift. `bandwidth_journal.parquet` tracks bytes + cached tokens, not latency or success-rate. [**Severity: M**]
- No documented AUP review per provider. [**Severity: L**]

### Section 5 — Discovery & Crawl Strategy

**Status:** PARTIAL.

- **No `sitemap.xml` parser anywhere.** Discovery is link-graph from homepage + path-list probing (`path_lists.py` for known canonical paths like `/about`, `/products`). For a B2B-classifier this is intentional (the homepage + 8 canonical pages give enough signal), but for an intent crawler it's a hard gap. [**Severity: H**]
- **No `robots.txt` parsing** (already flagged in §3.7).
- Hreflang extraction is full (`parser.py:455–571`) including `x-default` fallback. [**Strength**]
- URL normalization is comprehensive: `utm_*`, `fbclid`, `gclid`, `msclkid`, `dclid`, `ref`, `source`, `referrer`, `mc_cid`, `mc_eid`, `_ga`, `_gl` all stripped (`parser.py:1590–1609`); trailing slash + fragment normalized at dedup (`link_discovery.py:175,240`). [**Strength**]
- **No named session-param stripping** (`sid`, `phpsessid`, `sessionid`). Generic query-strip kicks in only at dedup. [**Severity: M**]
- Crawl scope is hard-coded paths (`path_lists.py:55–118`) — 8 paths for T1/T2, 4 for T3. No pagination handling, no archive/date pattern filter (search results blocked at `link_discovery.py:94`). [**Severity: L**]
- **No content-hash dedup.** Trailing-slash dedup only; identical content under different URLs not detected. [**Severity: M**]
- **No `<link rel="canonical">` extraction at queue stage.** Parser handles same-host check but doesn't proactively read the canonical and route. [**Severity: M**]

### Section 6 — Rendering & SPA

**Status:** PARTIAL — high-leverage gap on hydration extraction.

- **SPA detection is excellent.** `detection/placeholder.py:1522–1643` has a 6-branch algorithm: noscript-fallback, framework-mount-without-nav, strict/relaxed empty shells, script-count fallback, decoy-SPA branch. Mount patterns cover `__next`, `__nuxt`, `__gatsby`, `data-reactroot`, `ng-app` (`placeholder.py:532–534`). [**Strength**]
- **Hydration payload extraction is MISSING.** Zero matches for `__NEXT_DATA__`, `__NUXT__`, `__APOLLO_STATE__`, `__PRELOADED_STATE__`, `__remixContext`, `data-sveltekit-fetched`, `___INITIAL_PROPS___`. The renderer goes straight to Playwright (`scraper/renderer.py:66–220`). For Next.js / Nuxt / Gatsby / Apollo sites this is the **single biggest ROI miss**: hydration payloads can give the full nav + product catalog without paying for render. [**Severity: H — highest individual ROI fix in the audit**]
- **Wait strategy is T1 + T5 only.** `renderer.py:176` `wait_until="domcontentloaded"` then `renderer.py:181–188` polling loop (500ms × 10 = 5s max). No `networkidle`, no custom-selector wait, no `MutationObserver` quiet-period. [**Severity: M**]
- **No network interception.** Resource blocking only (`renderer.py:49–58,215–220`); XHR/fetch are not logged, no API endpoint discovery, no `discovered_apis.json`. For SPAs that load nav via API this is a real miss. [**Severity: H**]
- **No render reconciliation** (two-render compare, personalization stripping). [**Severity: M**]
- **No SPA failure taxonomy** — generic `except Exception` at `renderer.py:196–197`. [**Severity: M**]
- Render efficiency is good: page-pool reuse, resource blocking, 10s timeout. No (url, viewport, locale) result cache. [**Severity: M**]

### Section 7 — Menu Extraction

**Status:** FULL on static-DOM extraction; PARTIAL on SPA-interactive extraction.

- Landmark detection covers `<nav>`, `role=navigation`, header/footer, `aria-label="*nav*"`, `role=menu/menubar/menuitem`. [**Strength**] (`parser.py:1322–1413`)
- Hierarchy: 3-level nesting, `aria-expanded`/`aria-controls`, mega-menu column-aware (`parser.py:2052–2070,2219–2227,3292–3306`). [**Strength**]
- Footer column extraction with section headers (`parser.py:3188–3227`). [**Strength**]
- Mobile menu merged into header with dedup (NAV-02 comment at `parser.py:3250–3258`). [**Strength**]
- **Mega-menu activation is static-only.** The parser reads `aria-expanded` state from rendered HTML but never *triggers* a hover/click/focus to expand hidden menus. For sites whose mega menu requires interaction to render, only the visible top labels are captured. [**Severity: H** for SPA sites]
- **Breadcrumbs are class-based only.** No JSON-LD `BreadcrumbList` specialization, despite the parser handling ~120 LocalBusiness JSON-LD subtypes elsewhere. [**Severity: M**]
- No desktop-1440 + mobile-375 viewport sweep (`renderer.py:60–62` uses one UA only).

### Section 8 — Content Extraction

**Status:** FULL on basic, MISSING on cross-page boilerplate fingerprinting (high leverage).

- **Trafilatura primary + BeautifulSoup fallback** with allow/deny lists and 3× size preference rule (`extraction.py:114–162,177–208`). Two-pass cleaning (`text_cleaning.py` 9-step). [**Strength**]
- **Cross-page boilerplate fingerprinting is MISSING.** `text_cleaning.py:411–484` applies a per-page hardcoded 52-pattern blocklist + line-level dedup. No block-level hashing, no SimHash/MinHash, no frequency-across-N-pages threshold. For multi-page per-domain crawls this is the cleanest leverage point. [**Severity: H**]
- Render-aware filters cover `display:none`, `visibility:hidden`, `aria-hidden="true"` (`parser.py:3380,3384`). Missing: `opacity:0`, offscreen positioning, `getBoundingClientRect` zero-dim (static parsing only). [**Severity: M**]
- Structural-pattern detection is weak. Carousels are stripped by class (`parser.py:1297` `swiper`/carousel); no `role=region+aria-roledescription=carousel`, no tabs (`role=tablist`), no accordion (`<details>`, `.accordion`). For B2B SaaS pricing pages with tab-style plan comparisons, this loses content. [**Severity: M**]
- **JSON-LD extraction is the codebase's other strongest area.** `parser.py:4456–4831` parses every `<script type="application/ld+json">` block, walks `@graph` arrays, recognizes ~120 LocalBusiness subtypes (per `CHANGELOG.md:101–113`), and produces 12+ typed booleans. [**Strength**]
- No Microdata. OpenGraph partial (`og:title/description/type`). No Twitter Card. [**Severity: M**]
- **Output is plain text, not Markdown.** `extraction.py:90–96` sets `include_tables=False, include_links=False, include_images=False`. For downstream LLM consumption this discards structural signal. [**Severity: M**]
- **No per-intent allowlists or distillation profiles.** Single 8KB cap globally (`MAX_TEXT_LENGTH=8_000`). [**Severity: H** for general intent extraction]

### Section 9 — Label-to-Intent Matching

**Status:** Largely N/A to the current product, with a few in-scope partials.

The framework's Section 9 describes a tier-cascade for resolving raw navigation labels (e.g., the German word "Lösungen") to a global intent taxonomy. Barcada-scraper is **domain classification** software: it resolves *domains* to *business/non-business → technology sub-category → partner type*. Nav labels are *features* that feed Stage 1 LR + LLM tier, not entities that get resolved to a separate intent taxonomy.

Within that scope:

- Tier-1 normalization in `parser.py:1914–1941` does NFC, decorative char strip, whitespace collapse, 60-char truncation. **No article/stop-word strip, no plural normalization.** [**Severity: M**]
- No curated synonym lists, no per-locale synonyms, no strong/weak label split. [**Severity: M** for B2B-scope intent matching]
- Embeddings are used for *domain* classification (`embedder.py`, `text-embedding-3-small`), not for label→intent centroid lookup. Not multilingual. [**Severity: M**]
- LLM tier is for *classification*, not *label resolution*. [**N/A**]
- `parser.py:1944–1973` `_is_noise_label` filters noise (image filenames, emails, phone numbers); not a true domain/industry-conditional negative-match list. [**Severity: L**]

### Section 10 — Internationalization

**Status:** PARTIAL — English-first design with some i18n touchpoints.

- Hreflang extraction: full (`parser.py:455–571`). [**Strength**]
- Language detection: full chain (`parser.py:271–330` cld3 → pycld2 → langdetect). [**Strength**]
- NFC normalization: full (`parser.py:1924`, `check_domains.py:24`). [**Strength**]
- TLD→`Accept-Language` mapping: partial (`fetcher.py:_ACCEPT_LANGUAGE_BY_TLD`). [**Strength**]
- **`<html lang>` attribute is not extracted.** [**Severity: M**]
- **Path lists are English-only** (`path_lists.py:55–91`). No `de:/partner`, `fr:/partenaires`, `ja:/パートナー`. [**Severity: H** for a true multi-locale crawler; **L** for the current B2B US scope]
- **No CJK tokenization, no RTL awareness, no mixed-script handling.** [**Severity: M**]
- **No regional legal policy.** `regional_policy.json` does not exist; GDPR/CCPA/LGPD/PIPL rules are not encoded. [**Severity: H**]
- **No locale-stratified eval.** `eval_data/` is not stratified by locale. The framework's "no 98% claim without each locale at 98%" cannot be honored. [**Severity: H** for global-scope claims]
- No cross-regional entity resolution (`sameAs`, whois match). [**Severity: M**]

### Section 11 — Validation & Evaluation

**Status:** PARTIAL → FULL on infrastructure, MISSING on drift detection.

- **Eval data is real.** `eval_data/stage1_labels.jsonl` (220 rows post-audit; this is the file that was committed during the audit window — see compliance section), `stage2_labels.jsonl`, `stage3_labels.jsonl`, `canary_50_domains.txt`, `partner_type_anchors.jsonl`. [**Strength**]
- **Metrics module is real.** `metrics.py:255–303` computes precision/recall/F1; `metrics.py:215–252` extracts nav-recall and footer-count signals; `metrics.py:346–397` `generate_diff` does regression detection (nav_delta < 0, classification_flips); `metrics.py:764–873` writes summary.txt + CSVs. `tests/test_metrics.py` has 60+ unit tests. [**Strength**]
- **Fixtures are real and deterministic.** `tests/fixtures/html/` 23 directories: `cloudflare_challenge/`, `login_wall/`, `auth_403/`, `soft_404/`, `noindex_empty_title/`, `meta_refresh_parking/`, `empty_google_sites/`, `legitimate_business/`, `legitimate_blog/`, `legitimate_nonprofit/`, `spa_shell/`, plus 12 parking subtypes. [**Strength**]
- **SPA fixtures are not framework-tagged.** `spa_shell/` ≈22 captured shells, no per-framework subdirs (Next/React/Vue/Angular/CSR/ISR). [**Severity: M**]
- **No hydration payload fixtures, no HAR files.** [**Severity: M**]
- **No CI regression gate.** Diff lives in `metrics.py:475–481` action items but requires human interpretation. No `.github/workflows/` gate found. [**Severity: M**]
- **Drift detection: MISSING.** No nightly re-crawl scheduler, no boilerplate-fingerprint staleness alarm, no ETag/If-Modified-Since change probe. [**Severity: M**]
- **Acceptance metric formula is implicit.** Thresholds are tuning parameters (`stage1_thresholds.yaml`), not stated acceptance criteria like `F1 ≥ 0.92 AND precision ≥ 0.97`. [**Severity: M**]
- **No per-intent or per-locale eval split.** [**Severity: M**]

### Section 12 — Cost Control

**Status:** PARTIAL → FULL on cost telemetry, MISSING on per-domain budgets + efficiency-flag catalog.

- **`cost_journal.py` is mature production code.** Immutable `JournalState` with `with_*` mutators, ETag-conditional writes, exponential-backoff retries (`DEFAULT_RETRY_DELAYS_MS = (50, 100, 200, 400, 800)` at line 59), three outcomes (`completed | cost_ceiling_stopped | not_reached`), `ceiling_history` audit. [**Strength**]
- **`CostTotals` has per-stage USD breakdown:** stage1_llm, stage1_embedding, stage2_summarization, stage2_classification, stage2_fetch, stage3_evidence, stage3_primary, stage3_secondary, cached_input_tokens. [**Strength**]
- **`bandwidth_tracker.py:65–100`** has per-tier (T1/T2/T3) byte counters, `stage_budget_usd`, and a kill-switch at 0.95× budget. [**Strength**]
- **Cost-per-useful-record is uncomputable.** `phase_summary.py:76–97` has `cost_usd` + `domains_processed`, but no `useful_records` field. Per-domain "useful" is also not defined. [**Severity: H**]
- **No per-domain budgets, no domain value tiering (HIGH/STANDARD/LOW), no hard kill at 2×.** Only global ceiling. [**Severity: H**]
- **No daily/weekly/monthly caps.** Cost journal tracks per run; no calendar-window roll-up. [**Severity: M**]
- **Efficiency flag catalog: MISSING.** Zero matches for `TIER_OVER_ESCALATION`, `EXCESSIVE_PAGE_CRAWL`, `LLM_OVERUSE`, `RENDER_TIMEOUT_PATTERN`, `RETRY_LOOP_DETECTED`, `BOILERPLATE_NOT_CACHED`, `DUPLICATE_PAGE_CRAWLED`, `OVER_BUDGET_WITHOUT_OVERRIDE`, `CACHE_MISS_RATE_HIGH`, `LOW_USEFUL_RECORD_RATE`, `RENDERED_WITHOUT_HYDRATION_ATTEMPT`. [**Severity: H** — easy structured-anomaly tagging win]
- LLM cost control is strong: deterministic-first cascade, Azure prompt-cache awareness, `cached_input_tokens` tracking, ≥80% hit-rate target documented in `docs/PIPELINE.md:64`, cheapest-model routing (gpt-4.1-nano/mini/4.1 per task), distilled `ml_text` (≤2048 bytes) instead of raw HTML (`CHANGELOG.md:94–98`). [**Strength**]
- Storage lifecycle is missing (no compression-on-write, no hot/warm/cold/delete tiering, no content-hash dedup). [**Severity: M**]
- Re-crawl is missing (no adaptive frequency, no ETag, no If-Modified-Since). [**Severity: M**]

### Section 13 — Observability

**Status:** PARTIAL on logging, MISSING on metrics + alerts.

- Logging is `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")` (multiple CLIs). Plain text only. **No trace_id field, no JSON-formatted lines, no log aggregation context.** A `run_id` exists (`docs/PIPELINE.md:96–98`) but is not propagated into log lines. [**Severity: H** for production observability]
- **No Prometheus, no StatsD, no metrics exposition.** Zero matches. `bandwidth_journal.parquet` is the closest analogue — operator must run `pyarrow.parquet.read_table` to inspect. [**Severity: H**]
- **No alert definitions, no thresholds for cost/quality/drift.** [**Severity: H**]
- Failure taxonomy is partial: `page_schema.py:110–129` `ERROR_*` enum on the fetch side; `barriers.py` returns `cloudflare_challenge|waf_challenge|geo_block`; `check_domains.py` validator has ~15 rejection_reasons. **No unified failure-type → remediation mapping.** [**Severity: M**]
- Dashboards are not vendor-shipped: `phase_summary.py` writes JSON; `metrics.py:536–647` writes a text summary. No Grafana/Kibana/CloudWatch config files. [**Severity: M**]
- **No per-domain health tracking** (success rate over time, cost over time, strategy change log). All journals are per-shard. [**Severity: M**]

### Section 14 — Improvement Loop

**Status:** PARTIAL — manual loop documented; no automation.

- Failure clustering is **manual**, in `docs/validator_final_summary.md` (4 residual FN clusters). No `failure_clusters.json` automatic output. [**Severity: M**]
- Cluster prioritization is **manual**, in `tools/phase4_cost_reduction_directive.md` (8 levers ranked by $ savings). No `improvement_backlog.json`. [**Severity: M**]
- **No automated patching.** [**Severity: L** — appropriate for the current product stage]
- Validation gauntlet is **partial**: unit tests + fixture tests exist; eval runners exist (`stage1/evaluate.py`); no automated combined gauntlet on patches. [**Severity: M**]
- **No plateau detection, no auto-merge guardrails, no rolling slope.** [**Severity: L**]
- Cost-aware iteration is **manually** documented (`phase4_cost_reduction_directive.md` reports baseline $35,236 → target $7,756, 78% reduction). [**Strength** for discipline, but no automation]
- **No multi-strategy ensembling.** Pipeline is sequential Stage 1 → 2 → 3, not parallel CSS/JSON-LD/Playwright/LLM with reconciliation. [**Severity: M** for last-2% accuracy]
- Golden set is hand-labeled with rubric (`eval_data/eval_data_labeling_playbook_v1.2.md`); **no daily prod-sample auto-routing.** [**Severity: M**]

### Section 15 — Security & Compliance

**Status:** PARTIAL — credentials handled well; robots.txt and PII handling absent.

- `.env` is gitignored. No hardcoded credentials in code. All proxy/Azure secrets read from env at construction (`proxy_provider.py:122–154`). [**Strength**]
- **No secrets-manager integration** (Doppler, Infisical, AWS Secrets Manager). Env-var-only is acceptable for local/dev; for shared production deployment a secret-manager pull is recommended. [**Severity: M**]
- **No `robots.txt` parser** — see §3.7. Repeated here because it's both a Section 3 anti-bot item and a Section 15 compliance item. [**Severity: C**]
- **No `Crawl-delay` honoring.** [**Severity: H**]
- CAPTCHA: no automated solver, no model training to defeat — these are the *correct* posture but enforced by *absence* rather than by a documented policy gate. [**Severity: M**]
- **No PII detection or redaction.** Comments at `parser.py:337` reference GDPR / privacy-policy detection, but only for noise classification of "privacy policy" link labels — not actual PII recognition. [**Severity: H**]
- **No `regional_policy.json`** — no field-level emit rules per region. [**Severity: H**]
- **Audit trail is partial.** `cost_journal/run_{RUN_ID}.json` records what was crawled and when; `bandwidth_journal.parquet` records cost. But there is no per-domain policy-version stamp ("what policy was in effect when X was crawled"), no per-domain crawl-history table, no compliance-reporting view. [**Severity: M**]

---

## 5. Top 30 Prioritized Actions

Ordered by (impact ÷ effort). "Effort" assumes a competent Python engineer working in this codebase.

1. **Implement SPA hydration-payload extraction.** Extract `__NEXT_DATA__`, `window.__NUXT__`, `window.__APOLLO_STATE__`, `window.__PRELOADED_STATE__`, Gatsby/Remix/SvelteKit variants in the renderer *before* falling back to Playwright DOM scraping. Where present, these payloads give the full nav + product graph for ~50% of modern marketing sites. Add to `scraper/renderer.py` between line 176 and the polling loop at 181. **Effort:** ~150–250 LOC + fixtures. **Impact:** Highest single item in the audit. (Sections 6.2, 6.7) [**Severity: H**]
2. **Add a `robots.txt` parser + compliance enforcement.** Use `urllib.robotparser` (stdlib) plus an internal cache keyed on `host`. Check before adding any URL to the queue in `link_discovery.py`; respect `Crawl-delay`. Make bypass an explicit per-domain configurable that logs an authorization marker into the cost journal. **Effort:** ~300 LOC + tests. **Impact:** Closes the largest compliance gap. (Sections 3.7, 15.2) [**Severity: C**]
3. **Persistent per-domain strategy cache** (Parquet or SQLite). Track `last_successful_tier`, `failed_tiers`, `last_failure_at`, `next_retry_after`. Read at `promotion.py:assign_initial` to skip wasted T1 retries. **Effort:** ~200 LOC + journal extension. **Impact:** Cost reduction for repeat crawls; closes Sections 2.1d, 3.2, 4.3. [**Severity: H**]
4. **Network-request interception during render.** Capture XHR/fetch URLs into a per-domain `discovered_apis.json`. Replay discovered APIs on subsequent crawls instead of re-rendering. **Effort:** ~200 LOC (Playwright `route` already used at `renderer.py:215`; extend to log). **Impact:** Cost reduction for API-driven SPAs; closes 6.4. [**Severity: H**]
5. **Cross-page boilerplate fingerprinting.** Block-level SimHash over the first N crawled pages of each domain; emit fingerprints to a per-domain Parquet; mask matching blocks at extraction time. Replace the per-page 52-pattern blocklist in `text_cleaning.py:411–484`. **Effort:** ~400 LOC + tests. **Impact:** Quality + cost gain — the highest item in §8. [**Severity: H**]
6. **Cost-per-useful-record metric.** Define `useful_records` in `phase_summary.py` (e.g., `domain.is_business == true AND nav_count ≥ 5 AND content_text_len ≥ 500`). Emit `cost_per_useful_record` per shard + per run. **Effort:** ~100 LOC. **Impact:** Unblocks Sections 12.2 and 14.7 cost discipline. [**Severity: H**]
7. **Structured efficiency-flag catalog.** Add the 11-flag enum from §12.7 to `page_schema.py` or a new `efficiency_flags.py`. Emit per-record. Build a roll-up in `phase_summary.py`. **Effort:** ~150 LOC + tagging at flag points. **Impact:** Diagnostic clarity; turns ad-hoc tuning into structured work. [**Severity: H**]
8. **Per-domain budgets with hard-kill at 2×.** Add `max_pages`, `max_render_seconds`, `max_proxy_mb`, `max_llm_tokens`, `max_total_cost_usd`, `hard_kill_at` to a domain-tier YAML (HIGH/STANDARD/LOW). Enforce in `cost_tracker.py` + `bandwidth_tracker.py`. **Effort:** ~250 LOC. **Impact:** Stops a runaway domain from consuming the global ceiling. [**Severity: H**]
9. **Author `ARCHITECTURE.md`, `CRAWLING_POLICY.md`, `FAILURE_PATTERNS.md`.** Index-style docs in `docs/` linking into existing files; promote `DEFERRED_WORK.md`'s honesty pattern to the policy docs. **Effort:** 1 day total. **Impact:** Foundation for onboarding + audits; the missing named artifacts. [**Severity: M**]
10. **JSON-LD `BreadcrumbList` extraction.** The parser already handles ~120 JSON-LD types; specialized BreadcrumbList → `crawl_meta.breadcrumb_trail`. **Effort:** ~50 LOC in `parser.py:4456–4831`. **Impact:** Cleanest section-intent signal. [**Severity: M**]
11. **HTML→Markdown output mode.** Switch Trafilatura `output_format="markdown"` for the LLM-consumption path; keep plain text for the LR-feature path. **Effort:** ~80 LOC + downstream consumer test. **Impact:** Structural signal preservation for Stage 2/3 LLM. [**Severity: M**]
12. **`User-Agent` with contact email + policy URL.** Change `Mozilla/5.0 (compatible; Barcada/1.0)` (`check_domains.py:140`) to `BarcadaCrawler/1.0 (+https://barcada.io/crawler; crawler@barcada.io)`. **Effort:** trivial. **Impact:** Webmaster identifiability + ethics. [**Severity: M**]
13. **Mega-menu interactive activation (Playwright).** Add hover/click/focus sweep for `aria-haspopup` triggers in `renderer.py`, capture activated DOM, merge into menu extraction. **Effort:** ~200 LOC + fixtures. **Impact:** Recovers hidden mega-menu content on JS-only sites. (§7.5) [**Severity: H**]
14. **Sitemap.xml + canonical-URL extraction.** Add `sitemap_index.xml` parser + `<link rel=canonical>` reader at link-discovery time. **Effort:** ~200 LOC. **Impact:** Improves discovery quality + dedup. (§5.1, 5.2f, 5.4) [**Severity: M**]
15. **Region-aware proxy routing.** Add `region` field to `ProxyProvider.proxy_url(region=...)`; map TLD → preferred region. **Effort:** ~150 LOC. **Impact:** Reduces geo-block on EU/JP/CN sites. (§3.9, 4.3, 10.3) [**Severity: M**]
16. **Structured JSON logging with trace_id + run_id propagation.** Replace `logging.basicConfig` with `python-json-logger`; inject `run_id`, `shard_id`, `domain`, `stage` as structured fields. **Effort:** ~150 LOC. **Impact:** Production observability. [**Severity: H**]
17. **Prometheus / OpenTelemetry metrics emission.** Per-stage counters, per-tier byte gauges, per-provider latency histograms. **Effort:** ~250 LOC + dashboard. **Impact:** Real-time visibility. [**Severity: H**]
18. **Drift detection daemon.** Nightly re-crawl of N previously-passing domains; compute per-domain diff vs. last good run; alert on regression. **Effort:** ~300 LOC + cron/Azure timer trigger. **Impact:** Quality early-warning. (§11.6) [**Severity: M**]
19. **PII detection + redaction.** `presidio-analyzer` or a stricter regex on extracted text; emit `pii_findings` field; redact per `regional_policy.json` (next item). **Effort:** ~250 LOC. **Impact:** Closes a real privacy-compliance gap. (§15.4) [**Severity: H**]
20. **`regional_policy.json` + field-level emit rules.** Encode GDPR/CCPA/LGPD/PIPL rules; check before emit at `parquet_writer`. **Effort:** ~200 LOC + JSON + ToS review. **Impact:** Regulatory compliance. (§10.10, 15.5) [**Severity: H**]
21. **Per-domain crawl history + policy-version stamp.** Add `policy_version`, `taxonomy_version`, `crawler_version` to every emitted record + a per-domain audit log. **Effort:** ~100 LOC + Parquet schema bump. **Impact:** Compliance reporting + reproducibility. (§15.6) [**Severity: M**]
22. **Content-hash dedup.** Compute `sha256(text)[:16]` per page; suppress duplicate-content URLs from the queue. **Effort:** ~50 LOC. **Impact:** Cost reduction. (§5.4b, 12.9) [**Severity: M**]
23. **Render-result cache by (url, viewport, locale).** Parquet-backed; TTL keyed on per-domain `re_crawl_frequency`. **Effort:** ~200 LOC. **Impact:** Cost reduction. (§6.5e) [**Severity: M**]
24. **Acceptance metric formula codified.** Write `eval/acceptance_criteria.yaml` with explicit thresholds (e.g., `stage1_f1_min: 0.92`, `stage1_per_intent_recall_min: 0.85`). Read in `metrics.py:compare` and exit non-zero on failure. **Effort:** ~80 LOC. **Impact:** Turns "manual interpretation" into a CI gate. (§11.2) [**Severity: M**]
25. **CI regression gate.** GitHub Actions workflow that runs `metrics.py compare` vs. golden + exits non-zero on regression > threshold. **Effort:** 1 day. **Impact:** Prevents quality drift between commits. (§11.5) [**Severity: M**]
26. **TLS-fingerprint-spoofing client option.** Add `curl_cffi` integration as a T2.5 tier between datacenter and residential. **Effort:** ~200 LOC + dependency. **Impact:** Closes some JA3/JA4-gated sites without paying for residential. (§3.1.T2, 3.4) [**Severity: M**]
27. **Per-locale path-dictionary scaffold.** Even if not used immediately, structure `path_lists.py` so a `path_lists_de.py`, `path_lists_ja.py` can be added without refactor. **Effort:** ~100 LOC refactor. **Impact:** Future-proofs international expansion. (§1.2c, 10.6) [**Severity: L**]
28. **Failure clustering automation.** Job that reads results parquet, extracts features (HTTP status, render mode, missing field, body size, framework), clusters via DBSCAN/k-means, emits `failure_clusters.json`. **Effort:** ~300 LOC. **Impact:** Turns operator-reading into actionable backlog. (§14.1) [**Severity: M**]
29. **HTTP/2 frame-order / header-order awareness.** At minimum, document the current state. Long-term, switch to `httpx[http2]` with a curated header order. **Effort:** investigative; full fix ~300 LOC. **Impact:** Defeats some H2-fingerprint gates. (§3.4) [**Severity: L**]
30. **Microdata + Twitter Card extraction.** Round out structured data coverage. **Effort:** ~150 LOC in `parser.py`. **Impact:** Quality on B2B sites that ship microdata. (§8.12) [**Severity: L**]

---

## 6. Anti-Patterns Found

- **Generic Mozilla User-Agent.** `domain_validator/check_domains.py:140` uses `"Mozilla/5.0 (compatible; Barcada/1.0)"`. The "Mozilla/5.0 (compatible; ...)" preamble masquerades as a browser; for a polite crawler the preferred form is `"BarcadaCrawler/1.0 (+https://barcada.io/crawler; crawler@barcada.io)"`. [§3.7c]
- **Implicit CAPTCHA policy via absence-of-solver.** The codebase declines to solve CAPTCHAs because there is no solver dependency — not because a policy module enforces it. Make this explicit: a `policy.captcha.skip_default: true` config + a refusal point in the fetch path. [§15.3]
- **In-memory promotion state across shards/runs.** `promotion.py:34–38` comments explicitly note the lack of cross-run persistence. Recurring waste on stable problem domains. [§3.2]
- **Bare `except Exception:` in renderer.** `scraper/renderer.py:196–197` swallows all render failures into a single error path, preventing the SPA-failure taxonomy. [§6.6]
- **Wide-character regex hand-rolled in placeholder detection.** `_RE_GEO_BLOCK` at `barriers.py:439–447` mixes English + Chinese phrases in one regex. As more locales are added this will become unmaintainable; consider per-locale named groups or a YAML-driven phrasebook. [§3.3, 10.5]
- **`scripts/` carries large data artifacts in-tree.** `scripts/nav_crawl_combined.json` (~5MB), `scripts/sourced_domains.json` (~2.4MB), `scripts/nav_crawl_results.json` (~570KB), `scripts/nav_analysis_report.txt` (~286KB). These would normally live in object storage; checking them into the repo bloats clones. [General hygiene]
- **`feature_schema_version` mentioned in `CHANGELOG.md:54` and Section 9 of `parser.py:line 76` (per comments) but the **drift gate is not enforced at train time**: `lr_train._load_training_data` raises `NotImplementedError` per `DEFERRED_WORK.md:14`. Honest deferment, but currently the train/serve mismatch gate is conceptual. [§1.1e]
- **Sample artifacts checked into top-level.** `sample_classify_business_*.json` and `sample_classify_business_*.parquet` are repo-root files. Move to `tests/fixtures/samples/` or `docs/samples/`. [Hygiene]

---

## 7. Strengths

These are the items where the codebase is on or above the framework's bar:

- **Schema versioning discipline.** `CHANGELOG.md` is exemplary: dated, explicit `feature_schema_version` integer, Added/Changed/Removed sections, every removal documented (e.g., `metadata_signals.jsonld_type` → top-level `jsonld` block at `CHANGELOG.md:128–134`). [§1.1e]
- **Honest deferment.** `DEFERRED_WORK.md:1–52` documents the `_load_training_data` `NotImplementedError` with rationale, unblocking criteria, and follow-up scope. Beats undocumented TODOs everywhere. [§1.1]
- **Block-detection breadth.** `barriers.py:407–447` and `placeholder.py:561–577` cover Cloudflare, Akamai, DataDome, Incapsula/Imperva, Sucuri/Cloudproxy, Wordfence, DDoS-Guard, Kasada, PerimeterX/HUMAN, F5 Shape, AWS WAF, Cloudflare Turnstile, hCaptcha widget IDs, and Chinese geo-block phrases — well above industry norm. [§3.3]
- **Proxy abstraction.** `proxy_provider.py:48–78` Protocol-based, credentials forced into env vars, frozen dataclasses, runtime-checkable. Tests can mock trivially. [§4.1]
- **Deterministic-first classifier cascade.** `stage1` RULES → LR (calibrated) → LLM (uncertain band) with explicit thresholds in `configs/stage1_thresholds.yaml`. LLM cost grows only with band-2-to-7 records, not with corpus size. [§12.8]
- **Cost journal as immutable state machine.** `cost_journal.py` with `with_*` mutators, ETag-conditional writes, exponential-backoff retries, three explicit outcomes, `ceiling_history` audit. Production-grade. [§12.1]
- **Prompt-cache awareness.** `cached_input_tokens` column in `bandwidth_journal.parquet`; `configs/llm_pricing.yaml:22–31` documents the 50% cached-input rate and 80% target hit rate; `warm_cache(n=3)` helper documented in `docs/PIPELINE.md:78–91`. [§12.8b]
- **Test fixtures real and diverse.** 23 scenario directories under `tests/fixtures/html/`, deterministic static HTML. [§11.4]
- **Hreflang extraction first-class.** `parser.py:455–571` including `x-default` fallback. [§5.1c]
- **URL normalization comprehensive.** Twelve tracking-param families stripped (`parser.py:1590–1609`); trailing slash and fragment normalized at dedup. [§5.2b]
- **JSON-LD walker covers ~120 LocalBusiness subtypes.** `parser.py:4456–4831` walks `@graph` arrays, recognizes Restaurant, Hotel, Dentist, Bakery, AutoRepair, etc.; emits 12 typed booleans. [§8.12a]
- **Shared placeholder detection between validator and parser.** `detection/placeholder.py` is reused upstream + downstream, with the v2 refactor verified byte-for-byte against 197 fixtures (`CHANGELOG.md:172–179`). [§2.1c]
- **Resumable runs.** `--resume-run-id` honors prior `cost_ceiling_stopped` shards and continues under the same `RUN_ID` journal (`docs/PIPELINE.md:104–118`). [§12.10c]
- **Single-tenant guard.** Concurrent-run detection at startup with a 4-hour staleness window (`docs/PIPELINE.md:125–135`). [§12.10c]

---

## 8. Discovered Architecture

The actual architecture is a **batched, sharded, classifier pipeline** with a self-managed VMSS orchestrator — not a generic crawler.

**Stage A — Domain Validation (`barcada_scraper.domain_validator.check_domains`)**
Reads ICANN zone files / text / CSV / retry CSV. Async aiodns DNS resolution (concurrency 500). HTTP HEAD/GET probe with shared `detection/placeholder.py` for parking/placeholder detection. Outputs `results.csv`, `retry.csv` (transient failures), `spa_candidates.csv` (empty_spa for Phase B). Phase B optionally renders empty-spa domains via Playwright in a split-container topology.

**Stage 1 — Business Classifier (`barcada_scraper.classifier.stage1`)**
RULES tier (rules.business_min=8, non_business_max=1) → LR tier (calibrated, low=0.40, high=0.65) → LLM tier (gpt-4.1-nano, abstain_below=0.55). Inputs are `ml_text` (≤2048 bytes, 7-section positional format from `parser.py`) + numeric features. Output: is_business + business_score + confidence.

**Stage 2 — Technology Sub-Category Classifier (`stage2`)**
Page-acquisition layer first (HEAD precheck → T1 Azure egress → T2 datacenter proxy → T3 residential proxy, escalating on protection signature). Then summarization (LLM batched) + classification into 23 technology sub-categories. Default model: gpt-4.1-mini.

**Stage 3 — Partner-Type Classifier (`stage3`)**
Evidence summarizer (gpt-4.1) → primary partner-type classification (gpt-4.1 default) → optional secondary partner-type multi-label (gated by `stage3_secondary_enabled` feature flag; off for v1 per Lever 1 of Phase 4 Cost Reduction Directive). 17 partner types.

**Content scraper (`barcada_scraper.scraper.cli`, separate path)**
Async aiohttp fetcher → parser (≈5,800-line `parser.py`) → Parquet writer. Optional Playwright SPA rendering. Optional paid-API retry (ZenRows / ScrapingBee) for `bot_blocked`/`forbidden`.

**Orchestrator (`barcada_scraper.orchestrator.vmss_*`)**
Self-managed Azure VMSS shard-claim worker. Alternative to Azure Batch when batch quota unavailable. Heartbeat, work-queue, shard-partition, phase-summary modules.

**Cost & telemetry**
`bandwidth_journal.parquet` (per-shard fetch + cached-token totals) + `cost_journal/run_{RUN_ID}.json` (immutable global-cost audit with ETag-conditional writes). LLM prompts logged to `prompt_logger`. No Prometheus/StatsD; no dashboard except plain-text `metrics.py` summary.txt.

**Storage**
Parquet output, Hive-partitioned `crawl_date=YYYY-MM-DD/shard=NNNNN/data.parquet`. 100 shards by `sha256(domain)[:8] %% 100`. ADLS Gen2 `abfss://` and local `file://` both via fsspec dispatch.

**What's notably absent**
No robots.txt parser. No persistent per-domain strategy cache. No SPA hydration-payload extraction. No structured logging or metrics emission. No regional policy. No PII detection. No per-domain budgets. No drift detection.

---

## 9. Recommended Next Audits

1. **Live anti-bot evaluation.** This audit was static; an authorized live run against a 20-domain mixed-difficulty sample (5 Cloudflare-protected, 5 Akamai/DataDome, 5 SPA-heavy, 5 plain) would validate the block-detection coverage and the T1/T2/T3 escalation thresholds empirically.
2. **Cost re-audit after the per-domain-budget + efficiency-flag items land** (actions 7, 8). Measure cost-per-useful-record over a real corpus and compare to the Phase 4 directive's $7,756 target.
3. **Compliance / legal audit.** Once `regional_policy.json`, the robots.txt enforcer, and PII redaction are in place, route to legal review specifically for GDPR/CCPA (existing-customer geographies) and PIPL (planned-expansion geography).
4. **Eval-set sufficiency audit.** Specifically: is the 220-row `stage1_labels.jsonl` large enough for the LR's 70/10/20 split? Power-analysis at the per-intent / per-locale level. Run after the proposed per-locale stratification (action 27) is at least scoped.
5. **Re-audit Section 6 (Rendering) and Section 8 (Content) after hydration extraction and boilerplate fingerprinting land.** Those are the two highest-leverage gaps; verify they produced measurable composite-score lift.
6. **VMSS orchestrator audit.** Out of scope here. Crash-recovery, queue-claim safety under network partitions, idle worker reclamation. `docs/vmss_orchestrator_plan.md` outlines the design; an audit against that document specifically would close the operations loop.
7. **`scripts/` cleanup audit.** Many large data files and one-off scripts (`crawl_supplemental.py`, `analyze_nav_patterns.py`, etc.) — separate ad-hoc-tools from production scripts; move data artifacts out of the repo.

---

*End of report. Workspace artifacts under `/Users/administrator/crawler-audit/working/`. No files under `/Users/administrator/projects/barcada-scraper` were written, modified, deleted, or renamed by the auditor. See §1 for the state-delta flag.*
