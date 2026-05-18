# Fixture Quality Audit — `tests/fixtures/html/`

**Repo under audit:** `/Users/administrator/projects/barcada-scraper`
**Fixture root:** `/Users/administrator/projects/barcada-scraper/tests/fixtures/html/`
**Audit date:** 2026-05-18
**Mode:** Read-only

---

## 1. Read-Only Compliance Verification

### Pre-audit state

`git -C /Users/administrator/projects/barcada-scraper status`:
```
On branch main
Your branch is ahead of 'origin/main' by 8 commits.
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

`git rev-parse HEAD`: `be71d5365adefac38db63e49b38c7d5754b5b426`

### Post-audit state

`git -C /Users/administrator/projects/barcada-scraper status`:
```
On branch main
Your branch is ahead of 'origin/main' by 9 commits.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   eval_data/TAXONOMY_GAP_LOG.md
	modified:   eval_data/stage1_labels.jsonl

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	eval_data/stage1_challenge.jsonl

no changes added to commit (use "git add" and/or "git commit -a")
```

`git rev-parse HEAD`: `d44f034be40273a001e37288e6871d5532fb2186`

### State delta — FLAGGED

Pre and post DO NOT match. HEAD advanced by one commit (`d44f034`: "Stage 1 directive hardening: §3.9 enum-load preflight + Step 3.5 full-enum awareness…"), and `eval_data/TAXONOMY_GAP_LOG.md` is now in the unstaged-modifications list. Both changes are consistent with concurrent eval-data operator activity in the `eval_data/` tree.

The auditor (and every spawned sub-agent) ran only read-only commands: `git status`, `git rev-parse HEAD`, `git log`, file reads via `Read` and `cat`/`head`, content searches via `grep`/`find` (without `-delete` or `-exec rm`), and parquet reads via `pyarrow` + `adlfs` in read-only mode. **No file under `/Users/administrator/projects/barcada-scraper` was written, modified, deleted, or renamed by the auditor.** Workspace writes were confined to `/Users/administrator/crawler-audit/`.

### Commands skipped for safety

1. `pytest`, `python -m barcada_scraper.*`, `barcada-classify`, `barcada-scrape`, `barcada-validate` (would write `__pycache__/`, `.pytest_cache/`, logs).
2. `pip install`, `uv sync`, `playwright install`, `npm install` (would write `.venv/`, lockfiles, caches).
3. `npm run build`, `next build`, `hatch build` (would write `dist/`, `build/`).
4. `ruff format`, `ruff check --fix`, `mypy` (formatter/linter write mode).
5. State-mutating git: `add`, `commit`, `checkout`, `merge`, `rebase`, `reset`, `stash`, `push`, `pull`, `fetch`.
6. Writes back to ADLS: only `fs.ls`, `ds.dataset.to_table` reads against `output/canary-20260509-175114/` were issued.
7. Reading `.env` contents (defensive — confirmed gitignored).

---

## 2. Executive Summary

- **Total fixtures:** **197 HTML files** across **23 directories**. Capture date: 2026-04-25 (concentrated 15:59–16:01, with a separate 16:28 cluster for synthetic fixtures).
- **Overall corpus health: NEEDS_WORK.** The corpus does its primary job for `test_hard_exclusions.py` (which only reads the first alphabetically-sorted fixture per directory), but it has substantial faithfulness problems behind that one file, severe production-distribution mismatch, and **near-zero coverage** for almost every audit-remediation work item in `AUDIT_REPORT.md` §5.
- **Operator hint confirmed:** `tests/scraper/test_hard_exclusions.py:26` reads only `sorted(...).glob("*.html")[0]`, so the contract per the test is that *every fixture in a directory must conform to the directory's detector*. The directory name is the spec.
- **Zero fixtures with SPA hydration payloads.** Across 197 files: `__NEXT_DATA__`=0, `window.__NUXT__`=0, `__APOLLO_STATE__`=0, `__PRELOADED_STATE__`=0, `__remixContext`=0, `data-sveltekit-fetched`=0, Gatsby markers=0. **Blocks Action #1** from the Top-30 (the highest-ROI audit-remediation item).
- **Zero non-Western-TLD fixtures.** 140 `.com`, 33 `.net`, 3 `.org`, 1 `.ca`, 20 explicit `_synthetic.html`. **Zero** `.de`, `.fr`, `.jp`, `.cn`, `.br`, `.es`, `.it`, `.nl`, `.uk`, `.ru`, `.au`. **Blocks Action #20** (regional policy testing).
- **One zero-byte fixture:** `auth_403/grimsfairytales.net.html` — the file exists but has length 0. This either crashes `_read_fixture` (it would read empty string) or returns an empty body that no detector fires on.
- **Top-1 misclassified category: `soft_404/`.** 0 of 14 fixtures contain any soft-404 marker from `_RE_SOFT_404` / `_RE_EXPANDED_SOFT_404` (`did you mean`, `showing results for`, `no results found`, `popular searches`, etc.). The directory is functionally broken.
- **Top-2 misclassified category: `empty_google_sites/`.** 0 of 3 fixtures contain `sites-viewer-frontend`, `atari.vw.`, `tyJCtd`, or `normalizedPath` — the markers `barriers.py` looks for in `is_empty_google_sites`.
- **`auth_403/grimsfairytales.net.html` is 0 bytes**, and **`auth_403/gripwellsports.net.html` is 44 KB of a real WordPress site titled "GRIP WELL SPORTS"** — these are at the head of the alphabetic sort but represent neither auth-walls nor 403 responses. The first one will be picked by `test_hard_exclusions.py` once `grim*` sorts before others.
- **Single-record capture problem in legitimate_*/** : `legitimate_nonprofit/wikipedia.org.html` is **141 bytes containing a robots-policy crawler-rejection message**, not the Wikipedia homepage. `legitimate_business/ssquaredassociates.com.html` is **150 bytes**, truncated mid-`<meta>` tag.
- **`spa_shell/bestmakeupsale.com.html` is 51 bytes** containing only `<script src=https://cf-oss.gname.net/e.js></script>` — `gname.net` is **GMO Internet's parking redirect**, not an SPA. **Misclassified**: belongs in `parking_redirect_targets/` or a new `parking_gmo/`.
- **`spa_shell/shelterstoreau.com.html` is exactly 200000 bytes** — power-of-near-2 cap. Last bytes end mid-script `…retur`. **Truncated capture.**
- **Heavy class imbalance vs production.** Fixtures: parking_* = 116/197 = **59%**. Production canary (50 records): `is_parked=0`, `is_for_sale=0`, `is_holding_page=0`, only `is_empty_page=4`. The vast majority of fixtures exercise paths that almost never fire in production; the 68% production "ok / status=ok" path has only ~16 legitimate fixtures.
- **Test coverage is shallow.** Only `tests/scraper/test_hard_exclusions.py` references the fixture tree. It reads exactly **one** HTML per directory — alphabetically first. The other ~174 fixtures (~88%) are orphans.

### Top 5 fixtures that do NOT conform to their directory's specification

1. **`soft_404/bestmarketdeal.com.html`** — A Wix-generated empty page. Contains `Wix.com Website Builder` but zero soft-404 markers. (And all 13 other soft_404 fixtures behave the same way — the directory is broken end to end.)
2. **`empty_google_sites/grimacers.net.html`** — Contains a generic minified JS bundle but none of the Google-Sites markers (`sites-viewer-frontend`, `atari.vw.`, `tyJCtd`, `normalizedPath`). Same for `ssptennis.com.html` and `ssquarefinancials.com.html`.
3. **`spa_shell/bestmakeupsale.com.html`** (51 bytes) — A single `<script>` tag pointing at `cf-oss.gname.net` (GMO Internet parking). Should be in `parking_redirect_targets/`, not `spa_shell/`.
4. **`auth_403/gripwellsports.net.html`** (44 KB) — Title "GRIP WELL SPORTS"; a working WordPress site, not a 403. Should likely be in `legitimate_business/` or removed.
5. **`legitimate_nonprofit/wikipedia.org.html`** (141 bytes) — A `Please respect our robot policy …` rejection notice, not the Wikipedia homepage. Should be in a new `bot_rejected_crawler_notice/` directory or removed; it is *actively misleading* as a legitimate-nonprofit example.

### Top 5 gaps blocking audit-remediation work

1. **SPA hydration-payload coverage = 0 fixtures.** Blocks `AUDIT_REPORT.md` Action #1.
2. **JSON-LD `BreadcrumbList` coverage = 1 fixture.** Blocks Action #10.
3. **Non-US-domain coverage = 0 fixtures** (excluding 3 `.org` US nonprofits and 1 `.ca` blog). Blocks Action #20 (regional policy) and prevents per-locale eval (`AUDIT_REPORT.md` §10.13).
4. **No same-domain multi-page captures.** Blocks Action #5 (cross-page boilerplate fingerprinting).
5. **No `robots.txt` fixtures stored alongside HTML.** Blocks Action #2 (robots.txt compliance enforcement tests).

### Top 5 highest-priority candidate fixtures to add

1. **5–8 fixtures with `__NEXT_DATA__` payloads** of varying sizes (CSR-only, ISR, full-hydration) in a new `spa_hydration_next/` directory. Source: capture `next.js`-built sites from production crawl runs. **Priority: CRITICAL**.
2. **3–5 fixtures with `window.__NUXT__` / `__APOLLO_STATE__` / `__PRELOADED_STATE__`** in `spa_hydration_nuxt/`, `spa_hydration_apollo/`, `spa_hydration_redux/`. **Priority: CRITICAL**.
3. **6–10 fixtures from non-US TLDs** (.de, .fr, .jp, .br, .cn, .ru, with at least 2 right-to-left .ae/.il) in a new `international_business/` directory. **Priority: HIGH** (regional policy + per-locale eval).
4. **Multi-page sets for 3–5 domains** (e.g., shopify.com captures of `/`, `/pricing`, `/products`, `/about`, `/partners`) in `multipage_boilerplate/` to enable cross-page fingerprint tests. **Priority: HIGH** (Action #5).
5. **A replacement set for `soft_404/`** with real search-results pages containing markers like "showing results for", "did you mean", "no results found". The current 14 files all need to be removed or relocated. **Priority: HIGH** (current directory is broken).

---

## 3. Fixture Inventory

| Category | Files | Bytes (total) | Min | Avg | Max | Capture date | `expected/` | `meta.json` | Referenced by tests |
|---|---:|---:|---:|---:|---:|---|:-:|:-:|:-:|
| auth_403 | 15 | 62,354 | 0 | 4,156 | 44,261 | 2026-04-25 | – | – | first only |
| cloudflare_challenge | 3 | 7,510 | 1,036 | 2,503 | 5,081 | 2026-04-25 | – | – | first only |
| empty_google_sites | 3 | 22,191 | 7,303 | 7,397 | 7,545 | 2026-04-25 | – | – | (not referenced) |
| legitimate_blog | 3 | 14,882 | 405 | 4,960 | 13,032 | 2026-04-25 | – | – | (not referenced) |
| legitimate_business | 10 | 406,826 | 150 | 40,682 | 125,907 | 2026-04-25 | – | – | first only |
| legitimate_nonprofit | 3 | 182,878 | 141 | 60,959 | 180,067 | 2026-04-25 | – | – | (not referenced) |
| login_wall | 13 | 122,949 | 738 | 9,457 | 45,030 | 2026-04-25 | – | – | (not referenced) |
| meta_refresh_parking | 3 | 687 | 229 | 229 | 229 | 2026-04-25 | – | – | first only |
| noindex_empty_title | 3 | 73,518 | 128 | 24,506 | 73,251 | 2026-04-25 (1 file 16:00; 2 synthetics 16:28) | – | – | first only |
| parking_builders | 3 | 8,925 | 171 | 2,975 | 4,377 | 2026-04-25 (2 captures 16:00; 1 synthetic 16:28) | – | – | (not referenced) |
| parking_builders_expired | 5 | 881 | 159 | 176 | 203 | 2026-04-25 16:28 (all synthetic) | – | – | first only |
| parking_cms | 5 | 742 | 128 | 148 | 178 | 2026-04-25 16:28 (all synthetic) | – | – | first only |
| parking_construction | 37 | 1,171,432 | 235 | 31,660 | 98,053 | 2026-04-25 (16:00 range) | – | – | first only |
| parking_control_panels | 5 | 1,699 | 132 | 339 | 1,155 | 2026-04-25 (4 synthetic 16:28; 1 capture 16:00) | – | – | first only |
| parking_default_pages | 6 | 3,637 | 581 | 606 | 701 | 2026-04-25 (16:00) | – | – | first only |
| parking_errors | 6 | 79,014 | 326 | 13,169 | 75,193 | 2026-04-25 (16:00) | – | – | (not referenced) |
| parking_hosting | 4 | 3,797 | 768 | 949 | 1,180 | 2026-04-25 (16:00) | – | – | (not referenced) |
| parking_multilingual | 3 | 476 | 145 | 158 | 175 | 2026-04-25 16:28 (all synthetic) | – | – | first only |
| parking_redirect_targets | 4 | 13,534 | 799 | 3,383 | 4,673 | 2026-04-25 (16:00) | – | – | (not referenced) |
| parking_registration | 10 | 100,017 | 749 | 10,001 | 58,463 | 2026-04-25 (16:00) | – | – | first only |
| parking_sale | 19 | 341,033 | 677 | 17,949 | 101,751 | 2026-04-25 (16:00) | – | – | first only |
| soft_404 | 14 | 86,309 | 370 | 6,164 | 32,752 | 2026-04-25 (16:00) | – | – | (not referenced) |
| spa_shell | 20 | 510,078 | 51 | 25,503 | 200,000 | 2026-04-25 (16:00) | – | – | first only |
| **TOTAL** | **197** | **3,217,376** | – | – | – | – | **0** | **0** | **~14 referenced** |

Notes:

- All fixtures captured **2026-04-25** (operator-confirmed). Real-domain captures concentrated 15:59–16:01; the 20 explicitly-named `_synthetic.html` files were created 16:28, a separate operation.
- **No `expected/` subdirectories, no `meta.json` / `capture_metadata.json`, no per-fixture README.md files exist anywhere under `tests/fixtures/html/`.** Confirmed via `find tests/fixtures/html -type d -name expected` (empty) and `find tests/fixtures/html -name "meta.json" -o -name "capture_metadata.json" -o -name "README.md"` (only the `meta_refresh_parking/` directory itself, not a meta file).
- **Test references:** `grep -rn "fixtures/html"` across `tests/` and `src/` returns exactly **one** active reference — `tests/scraper/test_hard_exclusions.py:21–26`, which reads the lexicographically-first `.html` from a directory. 14 of the 23 directories are reached (those tested by `test_hard_exclusions.py`). The other 9 directories — `empty_google_sites/`, `legitimate_blog/`, `legitimate_nonprofit/`, `login_wall/`, `parking_builders/`, `parking_errors/`, `parking_hosting/`, `parking_redirect_targets/`, `soft_404/` — are **not** referenced from anywhere in `tests/` or `src/`. They exist but nothing exercises them.

---

## 4. Directory → Implied Specification → Code Path

(Detector citations from `src/barcada_scraper/detection/placeholder.py` and `src/barcada_scraper/scraper/barriers.py`.)

| Directory | Implied spec | Detector code path | Detection signature (verbatim from regex) | Expected outcome |
|---|---|---|---|---|
| auth_403 | HTTP 403 / unauthorized body | `placeholder.py:939–944` `_RE_PARKING_ERRORS` (access-denied clauses) | `you\s+don.t\s+have\s+permission\s+to\s+access`, `access\s+to\s+this\s+resource.*(?:denied|forbidden|restricted)`, `permission\s+(?:denied|refused)` | `is_placeholder_with_detail → (True, "parking_errors:…")` |
| cloudflare_challenge | Cloudflare "Just a Moment" / IUAM interstitial | `placeholder.py:_RE_CLOUDFLARE_CHALLENGE`; `barriers.py:407–410` `_RE_CLOUDFLARE_CHALLENGE` | `attention\s+required.*cloudflare`, `just\s+a\s+moment`, `checking\s+your\s+browser`, `sorry.*you\s+have\s+been\s+blocked` | `classify_page_barrier → "cloudflare_challenge"`; `is_cloudflare_challenge=True` |
| empty_google_sites | Empty Google Sites custom-domain template | `barriers.py` `is_empty_google_sites` (~lines 1076–1098) | `sites-viewer-frontend`, `atari\.vw\.`, `normalizedPath.*view/`, `<div class="tyJCtd">.{0,50}</div>` | `is_empty_google_sites → True` |
| legitimate_blog | Real blog with structured content | Inverted — all parking/placeholder paths must NOT fire | None should match `PARKING_REGEX`, `_RE_CLOUDFLARE_CHALLENGE`, `_RE_WAF_CHALLENGE`. Must have `≥30` meaningful word tokens or non-generic `<title>≥20ch` + meta-desc `≥30ch` | `is_placeholder_with_detail → (False, "")` |
| legitimate_business | Real business site | Inverted — same as legitimate_blog | Same as above, plus should pass content + meta-description gate | `is_placeholder_with_detail → (False, "")`; `is_business=True` downstream |
| legitimate_nonprofit | Real nonprofit/NGO | Inverted — same gates as legitimate_business | Same | `(False, "")` |
| login_wall | Login/auth-wall blocking access | `check_domains.py:162–180` `AUTH_REGEX`; partial overlap with `placeholder.py:_RE_PARKING_ERRORS` | `type=["']password["']`, `name=["']password["']`, `basic\s+realm`, `www-authenticate`, `authentication\s+required`, `login\s+required` | Validator marks `rejection_reason="auth_wall"` |
| meta_refresh_parking | Meta-refresh redirect to `defaultsite` | `placeholder.py:_RE_META_REFRESH_PARKING` (~line 640) | `http-equiv=["']refresh["'][^>]*content=["'][^"']*defaultsite`, `content=["'][^"']*url=defaultsite` | `(True, "meta_refresh_parking")` |
| noindex_empty_title | `<meta robots noindex>` + empty `<title>` | `placeholder.py:_RE_NOINDEX` + `_RE_EMPTY_TITLE`, both must match | `<meta…name="robots"…content="…noindex…">` AND `<title>\s*</title>` | `(True, "noindex_empty_title")` |
| parking_builders | Wix/Squarespace/Shopify disconnected (Tier 2) | `placeholder.py:991–1008` `_RE_PARKING_BUILDERS` + secondary signal | `wix\.com.*(not\s+connected\|connect\s+it\|expired)`, `this\s+domain\s+isn.t\s+connected\s+to\s+a\s+website`, `store\s+is\s+(unavailable\|coming\s+soon).*shopify` | `(True, "parking_builders+<signal>:…")` (Tier 2: needs short body OR missing meta-desc OR empty title) |
| parking_builders_expired | Wix/SqSp/Shopify expired (Tier 1) | `placeholder.py:1071–1080` `_RE_PARKING_BUILDERS_EXPIRED` | `domain\s+used\s+to\s+be\s+connected\s+to\s+a\s+wix\s+website`, `reconnect\s+your\s+domain.*wix`, `this\s+domain\s+has\s+flown\s+away`, `this\s+(wix\|squarespace\|shopify)\s+site\s+has\s+expired` | `(True, "parking_builders_expired:…")` |
| parking_cms | WordPress/Laravel/Notion default install (Tier 2) | `placeholder.py:920–933` `_RE_PARKING_CMS` + secondary | `just\s+another\s+wordpress\s+site`, `welcome\s+to\s+wordpress`, `this\s+is\s+your\s+first\s+post`, `laravel\s+has\s+an\s+incredibly\s+rich\s+ecosystem`, `this\s+is\s+a\s+notion\s+page` | `(True, "parking_cms+<signal>:…")` |
| parking_construction | Under-construction/coming-soon (Tier 2) | `placeholder.py:777–810` `_RE_PARKING_CONSTRUCTION` + secondary | `under\s+constr[uc]+tion`, `check\s+back\s+(again\s+)?soon`, `getting\s+started`, `launching\s+soon`, `(website\|site\|page)\s+(is\s+)?(coming\|launching)\s+soon`, `en\s+maintenance` | `(True, "parking_construction+<signal>:…")` |
| parking_control_panels | cPanel/Plesk/DirectAdmin default page (Tier 1) | `placeholder.py:844–861` `_RE_PARKING_CONTROL_PANELS` | `(welcome\s+to\s+\|powered\s+by\s+\|hosted\s+by\s+)cpanel`, `cpanel\s+(login\|default\|web\s*disk)`, `plesk\s+(login\|default\|onyx\|obsidian)`, `directadmin`, `virtualmin`, `webmin`, `ispconfig` | `(True, "parking_control_panels:…")` |
| parking_default_pages | Nginx/Apache/IIS default landing (Tier 1) | `placeholder.py:812–842` `_RE_PARKING_DEFAULT_PAGES` | `it\s+works!`, `default\s+web\s+page`, `placeholder\s+page`, `(welcome\s+to\s+)?nginx[!/]`, `apache2?\s+(ubuntu\|debian\|default)`, `apache.*server\s+at`, `iis\b`, `lighttpd`, `openresty` | `(True, "parking_default_pages:…")` |
| parking_errors | CloudFront/Vercel/Netlify error responses (Tier 1) | `placeholder.py:935–989` `_RE_PARKING_ERRORS` | `403:\s+forbidden`, `generated\s+by\s+cloudfront`, `request\s+could\s+not\s+be\s+satisfied`, `error\s+code\s+5[23]\d`, `netlify.*not\s+found`, `heroku.*no\s+such\s+app`, Vercel token `[a-z]{3}[0-9]+::[a-z0-9]+-\d+-[a-f0-9]+` | `(True, "parking_errors:…")` |
| parking_hosting | IONOS/Strato/Gandi/DigitalOcean/Cloudways parking (Tier 1) | `placeholder.py:863–918` `_RE_PARKING_HOSTING` | `(powered\s+by\s+\|hosted\s+by\s+)ionos`, `ionos\s+(parking\|default…)`, `\bstrato\b`, `gandi`, `ovhcloud`, `digitalocean`, `cloudways.*not\s+authorized`, `spaceship` | `(True, "parking_hosting:…")` |
| parking_multilingual | Non-English parking phrases (Tier 2) | `placeholder.py:1010–1046` `_RE_PARKING_MULTILINGUAL` + secondary | Dutch `gereserveerd`/`geparkeerd`, German `im\s+aufbau`/`neue\s+internetpr…`, French `votre\s+domaine`/`en\s+construction`, Danish `her\s+flytter\s+snart`, Russian Cyrillic registrar, Chinese `域名暂时无法访问`, Japanese `お名前\.com` | `(True, "parking_multilingual+<signal>:…")` |
| parking_redirect_targets | Webmail / `defaultsite` JS-redirect / safebrowse (Tier 1) | `placeholder.py:1048–1064` `_RE_PARKING_REDIRECT_TARGETS` | `url=https?://webmail\.`, `window\.location.*webmail`, `redirecting\.\.\.`, `<title>redirecting`, `0;url=defaultsite`, `potential\s+threat\s+detected` | `(True, "parking_redirect_targets:…")` |
| parking_registration | Registrar landing / domain-suspended / not-yet-configured | `placeholder.py:PARKING_REGEX` lines 70–104 | `domain\s+(is\|name\s+is\|has\s+been)\s+registered`, `not\s+yet\s+connected`, `domain\s+not\s+configured`, `account\s+has\s+been\s+suspended`, `domain\s+suspended`, `hosted\s+at\s+\w+\.(com\|net\|org)` | `(True, "parking_registration:…")` or `parking_sale:…` |
| parking_sale | Domain for-sale page (Tier 1) | `placeholder.py:696–731` `_RE_PARKING_SALE` | `(domain\|site\|page\|website)\s+(is\|has\s+been)?\s+parked`, `(this\s+)?(domain\|website\|site)\s+(is\s+)?for\s+sale`, `buy\s+(this\s+)?domain`, `(make\|submit\|send\|enter)\s+an?\s+offer`, `domain\s+parking`, `premium\s+domain.*available`, `serious\s+offers\s+only` | `(True, "parking_sale:…")` |
| soft_404 | Search-results / soft-404 page | `placeholder.py:615–630` `_RE_SOFT_404` / `_RE_EXPANDED_SOFT_404` | `did\s+you\s+mean\s`, `showing\s+results?\s+for\s+["']`, `sponsored\s+(results?\|listings?\|links?)`, `popular\s+searches`, `trending\s+searches`, `people\s+also\s+search\s+for`, `no\s+results?\s+found.{0,50}(?:search\|query\|keyword)`, `try\s+(a\s+)?different\s+search` | `(True, "soft_404:…")` (first 2000 chars only) |
| spa_shell | JS-rendered shell (React/Vue/Angular/Next/Nuxt/Gatsby) | `placeholder.py:1522–1643` `_is_spa_shell` (Paths NS/B/A/C/D/E) | One of: `_RE_SPA_NOSCRIPT_MSG`, `_RE_SPA_FRAMEWORK_MOUNT` (`__next`, `__nuxt`, `__gatsby`, `data-reactroot`, `ng-app`), `_RE_SPA_MOUNT` (`app`, `root`, `__next`, …), `_RE_SPA_JS_MODULE` (`type="module"`), `_RE_SPA_JS_REQUIRED_BROAD` | `_is_spa_shell → True`; `is_spa_shell=True` |

---

## 5. Fixture-Spec Conformance

Counts derived by grepping each fixture against the verbatim detector signatures above. CONFORMS = at least one detector marker hits; DOES NOT CONFORM = zero hits despite the directory's spec; AMBIGUOUS = partial match (e.g., one of two required Tier-2 conditions) or marker present but in a wrong context. Tier 2 categories require a secondary signal (`short_body`, `no_meta_description`, `empty_title`, `insufficient_content`) — I treat a fixture as CONFORMS when its content matches the primary regex AND it is < 2 KB (an approximation for the secondary).

| Directory | Files | CONFORMS | DOES NOT CONFORM | AMBIGUOUS | Notes |
|---|---:|---:|---:|---:|---|
| **cloudflare_challenge** | 3 | **3** | 0 | 0 | All 3 contain `<title>Attention Required! \| Cloudflare</title>`. |
| **meta_refresh_parking** | 3 | **3** | 0 | 0 | All 3 identical 229-byte templates with `0;url=defaultsite`. |
| **noindex_empty_title** | 3 | **3** | 0 | 0 | All 3 contain both `<meta name="robots" content="…noindex…">` AND `<title></title>`. |
| **parking_redirect_targets** | 4 | **4** | 0 | 0 | All 4 contain `defaultsite` / `window.location` / safebrowse / webmail markers. |
| **parking_builders_expired** | 5 | **5** | 0 | 0 | All 5 synthetic with `wix.com … expired` / `flown away` / `reconnect`. |
| **parking_cms** | 5 | **5** | 0 | 0 | All 5 synthetic; matches `wordpress`/`laravel`/`notion`. |
| **parking_control_panels** | 5 | **5** | 0 | 0 | 4 synthetic + 1 real (`ssquaredmanagement.com`) — all match cpanel/plesk/directadmin/webmin. |
| **parking_multilingual** | 3 | **3** | 0 | 0 | But all 3 are Western European synthetics — covers only Dutch/French/German; **detector also handles** Danish/Russian/Chinese/Japanese, **0 fixtures** for those. |
| **parking_builders** | 3 | **3** | 0 | 0 | 1 synthetic (Shopify) + 2 real Wix captures (`grimpeur.net`, `shelvingofamerica.com`). |
| **parking_default_pages** | 6 | **5** | 1 | 0 | 5 match `nginx/1.24.0` etc. (via `nginx[!/]`). **`grigolato.net.html`** has no nginx/apache/iis marker. |
| **parking_redirect_targets** | (already counted) | – | – | – | – |
| **parking_hosting** | 4 | **1** | 3 | 0 | Only `grigat.net.html` matches `ionos` etc. **`shelteroccasions.com`, `sheltonplants.com`, `sheltownfarm.com`** have no hosting-brand markers. |
| **parking_construction** | 37 | **36** | 1 | 0 | All but **`ssrcllc.com.html`** match a "construction/coming-soon" phrase. |
| **parking_registration** | 10 | **3** | 7 | 0 | Only `bestlogisticsjobs`, `bestlyricshub`, `grinin.net` match registrar/suspended phrases. The other 7 (incl. `bestmacstuff`, `bestmacula`, `gritandwit`, `gritbornemann`, `sanmarcostudio`, `shelterlabel`, `ssroofingservices`) contain no registrar markers. |
| **parking_errors** | 6 | **1** | 5 | 0 | Only `ssresidential.com.html` matches. **`bestmactips.com.html`** is a Cloudflare 526 SSL-error page → detector for *that* lives in `_RE_WAF_CHALLENGE`, not `_RE_PARKING_ERRORS`. **`bestmarketingawards.com.html`**, **`grillteam.net.html`**, **`sanmarcosgrowers.com.html`**, **`ssrcplindia.com.html`** have no parking-errors markers. |
| **parking_sale** | 19 | **11** | 8 | 0 | Misses on `bestlodgeoptions`, `bestlodgz`, `grillseeker`, `grimoireofbabylon`, `sanmarinomed`, `sanmarinomedcenter`, `sheltonattorney`, `bestlodgz`. Some appear to be parked pages without the explicit "for sale" wording. |
| **auth_403** | 15 | **8** | 7 | 0 | **`grimsfairytales.net.html` is 0 bytes** (broken). **`gripwellsports.net.html` is 44 KB of a working WordPress site** (misclassified). `grigna.net.html`, `grillt.net.html`, `ssptjp.com.html`, `ssquaresemi.com.html` lack 403/auth wording. |
| **login_wall** | 13 | **7** | 6 | 0 | 6 fixtures (`bestlogicinc`, `sanluisfarmacias`, `sheltondowns`, `sheltondownsfarm`, `sheltonjbrown`, `shelvingsmart`) contain no password-input / auth-wall markers. |
| **spa_shell** | 20 | **~13** | ~4 | ~3 | Path D (≥2 script tags AND text < 200 chars AND body < 8 KB) catches the small ones. **`bestmakeupsale.com.html` 51 B with one GMO-parking script** would fail body-size guard. **`shelterstoreau.com.html`** is exactly 200,000 B with `has_nav=3` — likely passes detector by JS-module count but is **not a "shell"**; it's a truncated full page. **`sanmarinoiron.com.html`** has `has_nav=1`, **`shelterstores.com.html`** and **`shelterstoreau.com.html`** have `has_nav=3` — these 3 have semantic `<nav>` so Path B should *not* fire on them. |
| **soft_404** | 14 | **0** | **14** | 0 | **Entire directory is broken.** Zero fixtures contain `did you mean`, `showing results for`, `no results found`, `popular searches`, etc. Sample inspection of `bestmarketdeal.com.html` showed it is a Wix-generated empty page, not a search results page. |
| **empty_google_sites** | 3 | **0** | **3** | 0 | None contain `sites-viewer-frontend`, `atari.vw.`, `tyJCtd`, or `normalizedPath`. Sample of `grimacers.net.html` shows a generic minified JS page, not Google Sites. |
| **legitimate_business** | 10 | **6** | 4 | 0 | `ssquaredassociates.com.html` 150 B (truncated). `ssquaredbicycles.com.html` 8192 B (suspiciously exact 8 KiB; no `<title>`, no block tags). `grigionitaliano.net.html` 30 KB but no `<p>/<h>/<li>/<div>` block tags. `sanmarcosflowershop.com.html` 32752 B (close to 32 KiB; no block tags). |
| **legitimate_blog** | 3 | **2** | 0 | 1 | `danluu.com.html` is 405 B but Dan Luu's blog is intentionally minimal HTML — CONFORMS as edge case. `jvns.ca.html` 1.4 KB has `<title>Julia Evans</title>` and Hugo generator — CONFORMS. `simonwillison.net.html` CONFORMS. |
| **legitimate_nonprofit** | 3 | **2** | 1 | 0 | `redcross.org.html` 180 KB CONFORMS. `archive.org.html` 2.7 KB CONFORMS. **`wikipedia.org.html` 141 B is a robots-policy rejection notice, NOT the Wikipedia homepage**. |

**Aggregate:** Of 197 fixtures, **~127 (64%)** conform to their directory's spec, **~61 (31%)** do not, and **~9 (5%)** are ambiguous (mostly `spa_shell/` borderlines).

### List of fixtures that should move to a different directory

| Fixture | Currently in | Should move to | Reason |
|---|---|---|---|
| `spa_shell/bestmakeupsale.com.html` | spa_shell | `parking_redirect_targets/` (or new `parking_gmo/`) | 51-byte file containing only `<script src=https://cf-oss.gname.net/e.js></script>` — gname.net is GMO parking. |
| `auth_403/gripwellsports.net.html` | auth_403 | `legitimate_business/` (or remove) | 44 KB working WordPress site titled "GRIP WELL SPORTS"; no auth/403 markers anywhere. |
| `legitimate_nonprofit/wikipedia.org.html` | legitimate_nonprofit | new `bot_rejected_crawler_notice/` (or remove) | 141 B robots-policy reject message, not the Wikipedia homepage. |
| `parking_default_pages/sanmarcosdentists.com.html` (and 4 others 581 B) | parking_default_pages | `auth_403/` is a closer fit (`<title>401 Authorization Required</title>` + nginx footer) | These are nginx **401** pages, not nginx welcome pages. |
| `parking_errors/bestmactips.com.html` | parking_errors | `cloudflare_challenge/` (or new `cloudflare_5xx/`) | Cloudflare 526 SSL-error page — handled by `_RE_WAF_CHALLENGE` not `_RE_PARKING_ERRORS`. |
| `auth_403/grimsfairytales.net.html` (0 bytes) | auth_403 | **Delete or refresh.** Empty file. |

### List of fixtures whose directory should be reconsidered entirely

- **All 14 in `soft_404/`** — none match `_RE_SOFT_404` or `_RE_EXPANDED_SOFT_404`. Either the captures should be replaced with real search-results pages, or the directory should be renamed to describe what these fixtures actually are (sample `bestmarketdeal.com.html` is a Wix empty/coming-soon page, which could route to `parking_construction/`).
- **All 3 in `empty_google_sites/`** — none match the `is_empty_google_sites` detector signatures. Replace with real Google Sites captures (search for `sites-viewer-frontend` in production parser output to find candidates).

---

## 6. Faithfulness Findings

### Suspiciously small files (<2 KB in non-error categories)

| File | Size | Category | Concern |
|---|---:|---|---|
| `auth_403/grimsfairytales.net.html` | **0 B** | auth_403 | Empty file — broken capture |
| `auth_403/grigoleit.net.html` | 199 B | auth_403 | Probably a one-line 403 — small but plausible |
| `auth_403/gritcityheroes.net.html` | 199 B | auth_403 | Same |
| `auth_403/griftdijk.net.html` | 239 B | auth_403 | Same |
| `auth_403/ssquarerealty.com.html` | 358 B | auth_403 | Small |
| `legitimate_nonprofit/wikipedia.org.html` | **141 B** | legitimate_nonprofit | Robots-policy message, not the homepage |
| `legitimate_business/ssquaredassociates.com.html` | **150 B** | legitimate_business | Truncated mid-`<meta>` tag |
| `legitimate_business/sanluisfinancial.com.html` | 1,064 B | legitimate_business | Tiny for a "real business" |
| `legitimate_blog/danluu.com.html` | 405 B | legitimate_blog | Plausible — Dan Luu deliberately minimal |
| `spa_shell/bestmakeupsale.com.html` | **51 B** | spa_shell | One script tag only — actually GMO parking |
| `spa_shell/sheltonorthodontics.com.html` | 462 B | spa_shell | Small but probably valid SPA shell |

### Suspiciously round file sizes (truncation suspects)

| File | Size | Notes |
|---|---:|---|
| `spa_shell/shelterstoreau.com.html` | **200,000 B exactly** | Tail ends mid-script (`…retur`). Truncated at 200 KB cap. |
| `spa_shell/shelterstores.com.html` | **131,072 B exactly** | 128 KiB — power of 2. Likely truncated. |
| `legitimate_business/ssquaredbicycles.com.html` | 8,192 B exactly | 8 KiB — power of 2. No `<title>`, no block tags. Likely truncated. |
| `legitimate_business/sanmarcosflowershop.com.html` | 32,752 B | Close to 32,768 B (32 KiB); no block tags. Suspicious. |
| `soft_404/ssptonline.com.html` | 32,752 B | Same 32,752 B — exact-same byte count as the file above. Possibly same truncation logic. |
| `parking_sale/shelvs.com.html` | 32,752 B | Same. **Three fixtures at exactly 32,752 B is statistically improbable** — strong truncation signal. |
| `legitimate_business/bestmacnutcrackers.com.html` | 116,825 B | Not on a round boundary but block_tags=9 only — body is mostly script/style. |

The repetition of 32,752 B = 32,768 − 16 across three unrelated fixtures (`soft_404/ssptonline.com.html`, `parking_sale/shelvs.com.html`, `legitimate_business/sanmarcosflowershop.com.html`) strongly suggests these were captured against a hard 32 KiB ceiling (perhaps a defaulted `MAX_RESPONSE_BYTES` during the capture run, with a 16-byte epilogue for `</html>\n` or similar). Worth verifying against the production parser's 2 MB cap (`scraper/fetcher.py:139`).

### Files lacking signs of real-world HTML

- **`legitimate_nonprofit/wikipedia.org.html`** has no `<head>`, no `<body>`, no DOCTYPE, no script tags. It is a single-line robots-policy notice. **Synthetic-looking.**
- **`legitimate_business/ssquaredassociates.com.html`** has DOCTYPE + `<html>` + `<head>` but is truncated 7 lines in, mid-`<meta>`. **Incomplete capture.**
- All 20 `*_synthetic.html` files are explicitly hand-authored — they have minimal HTML (often no DOCTYPE) and average ~150 B. They are intentionally synthetic (the naming makes this explicit and acceptable for unit-test conformance) but they do not exercise the parser's heuristics that compare against real-world HTML byte distributions.
- `spa_shell/bestmakeupsale.com.html` lacks `<html>`, `<head>`, `<body>` — just a single `<script>` tag — looks synthetic but its filename suggests a real domain.

### `example.com` / `test.example` poisoning check

`grep -rli "example\.com\|test\.example" tests/fixtures/html/` returns **no matches** in fixture bodies. The string `example.com` appears only in `tests/scraper/test_hard_exclusions.py` as a synthetic domain arg passed to `extract_hard_exclusions(_read_fixture(...), "example.com")`. Fixtures themselves are clean.

### Filename-domain ↔ content-domain consistency

I spot-checked 10 fixtures by greping the filename's base domain inside the body. Issues:

- `legitimate_nonprofit/wikipedia.org.html` — does not contain "wikipedia" anywhere. (Domain mismatch.)
- `auth_403/gripwellsports.net.html` — *does* contain "gripwellsports" (it's actually that site's content, but unrelated to a 403).
- `spa_shell/bestmakeupsale.com.html` — does not contain "bestmakeupsale" (single script tag, GMO parking).
- The remaining 7 spot-checks were consistent.

---

## 7. Discrimination Findings

### Redundant fixtures within categories

- **`meta_refresh_parking/`** — all 3 fixtures are **identical 229-byte templates**. Likely the same `<meta http-equiv="refresh" content="0;url=defaultsite" />` page served by the same upstream. **Keep one** (e.g., `bestmacandcheese.com.html`), remove the other two as exact-duplicate exercise of the same code path.
- **`parking_default_pages/`** — 5 of 6 fixtures are exactly **581 B** and all share the nginx-401 template (`<title>401 Authorization Required</title>` + `<center>nginx/1.24.0</center>` + comment-padding). They are the same code path. **Keep one**, remove four. (The 6th, `grigolato.net.html`, is 701 B and does *not* match the nginx regex — separate issue.)
- **`parking_builders_expired/`** — 5 fixtures, all hand-synthetic, all 159–203 B. They cover Wix and Squarespace expired/reconnect/flown-away phrases — each *does* exercise a distinct clause of `_RE_PARKING_BUILDERS_EXPIRED`. **Not strictly redundant**, but they're all 16–28 lines of synthetic HTML; they don't exercise real-world WordPress/Shopify/Wix expired pages.
- **`parking_cms/`** — 5 hand-synthetic fixtures, three of them (`wordpress_welcome_synthetic.html`, `wordpress_first_post_synthetic.html`, `wordpress_just_another_synthetic.html`) cover three sentinel phrases in the WordPress branch. Slight overlap; could prune to 1 WordPress + 1 Laravel + 1 Notion (= 3) without losing coverage.
- **`parking_construction/`** has 37 files for what is essentially one detector clause. **Excessive.** 36 of 37 conform — but they all fire the same regex via the "under construction" / "coming soon" path. Reduce to ~6–8 fixtures with **structural** diversity (one bare-template, one 80 KB Wix-generated, one Shopify under-construction, one ngrok-tunneled, one branded coming-soon countdown, etc.).
- **`parking_sale/`** has 19 files. Several appear to share GoDaddy-Aftermarket templates. Reduce to ~6–8 with explicit diversity (Sedo, Dan.com, Afternic, GoDaddy direct, Hugedomains, generic "Make Offer" form).

### Categories with too many fixtures relative to discrimination they provide

| Category | Files | Recommend |
|---|---:|---|
| parking_construction | 37 | Reduce to **8** with structural diversity |
| parking_sale | 19 | Reduce to **8** with marketplace diversity |
| spa_shell | 20 | Keep, but **add framework-tagged subdirs** (see §11) |
| auth_403 | 15 | Reduce to **6**, **remove the 0-byte and the misclassified 44 KB WP site** |
| login_wall | 13 | Reduce to **6**, all containing actual password-input HTML |

### Categories with too few representatives

| Category | Files | Recommend |
|---|---:|---|
| cloudflare_challenge | 3 | Add 2–3 more covering DataDome, Akamai BMP, AWS WAF token (`_RE_WAF_CHALLENGE` covers these but the directory only has Cloudflare) |
| empty_google_sites | 3 | **All 3 are non-conforming.** Replace with 3 real captures. |
| legitimate_business | 10 | Expand to **15–20** with **industry diversity** (SaaS, e-commerce, professional services, manufacturing, healthcare). The current 10 are mostly random `.com`/`.net` captures from one sweep. |
| legitimate_blog | 3 | Add 2–3 from common platforms (Substack, Medium, WordPress.com, Ghost). |
| legitimate_nonprofit | 3 | **wikipedia.org needs replacement**; expand to 5 (.org diversity: education, healthcare, advocacy, religion). |
| parking_multilingual | 3 (synthetic, Western European only) | **Add real captures** covering Russian (Cyrillic), Chinese, Japanese, Danish — the detector handles them but no fixtures exercise that path. |

---

## 8. Currency Findings

### Capture date confirmation

Operator reports **April 25, 2026** within a 2-minute window. Confirmed:

- All 197 fixtures are dated **2026-04-25**.
- Real captures concentrate **15:59–16:01** (a ~2-minute window for the bulk of captures), consistent with a single capture run.
- The 20 `*_synthetic.html` files are dated **16:28** (a separate operator session, ~28 minutes later). This is consistent with the operator hand-authoring synthetic edge cases after the main capture finished.
- **No fixtures are stale relative to the audit's needs** as a function of age — they are 23 days old at audit time. Currency concerns below are about *content drift* relative to current detector code, not file age.

### Anti-bot detector ↔ fixture marker match

`barriers.py:407–447` was last touched as part of the v2.1 / BAR-01 / BAR-08 changes (visible in `parser.py` comments). The fixtures were captured on 2026-04-25, the audit framework date is 2026-05-18. Detector logic is current relative to the fixtures.

Per-fixture match (re-stated for completeness):

- **`cloudflare_challenge/` (3 fixtures):** all 3 hit `_RE_CLOUDFLARE_CHALLENGE` markers. ✓
- **`auth_403/` (15 fixtures):** 8 contain auth-wall language; 7 do not (including the 0-byte file and the misclassified `gripwellsports.net`). The detector would *not* fire on the 7 — the directory has a faithfulness problem, not a freshness problem.
- **`login_wall/` (13 fixtures):** 7 contain password-input markers; 6 do not. Same shape.
- **`empty_google_sites/`:** 0 of 3 contain the markers `is_empty_google_sites` looks for. **The detector has moved relative to the fixtures, or the fixtures never matched.** Either way the directory is broken.
- **`soft_404/`:** 0 of 14 contain markers. Same.

No additional WAF/anti-bot markers in `_RE_WAF_CHALLENGE` (Kasada `ks-cc`, F5 `shape.min.js`, AWS `aws-waf-token`, HUMAN/PerimeterX `px-captcha`) are exercised by any fixture in any directory. Per the directive's instruction to check: **none of the WAF-family signatures have fixtures**, despite the detector code already supporting them.

### Outdated patterns in `legitimate_*` fixtures

- `legitimate_business/bestlowrates.com.html` (76 KB): contains `jQuery v3.4.1` references (current as of mid-2024; acceptable). Has WordPress 5.x markers. No React/Vue.
- `legitimate_business/sanluisfloors.com.html` (126 KB): WordPress 6.x markers, no obvious old-jQuery.
- `legitimate_business/bestmacnutcrackers.com.html` (117 KB): also WordPress.
- `legitimate_blog/simonwillison.net.html`: hand-authored modern HTML. Current.
- `legitimate_blog/jvns.ca.html`: Hugo v0.135 (current).
- `legitimate_nonprofit/redcross.org.html`: React-style modern markup.

Overall: the legitimate_* fixtures lean **heavily WordPress** (~7 of 13 between business + blog + nonprofit). No fixture exercises a modern Next.js / Nuxt / Vue / Angular / SvelteKit *business* site. This is a coverage gap; not "outdated" per se, but skewed.

- **No `http://` (non-HTTPS) src/href patterns** found in spot-checks of the larger fixtures — captured material is HTTPS-era.
- **No `jQuery 1.x` / `jQuery 2.x`** references found in spot checks.

---

## 9. Labeling Findings

- **`expected/` subdirectories:** **0** (across all 23 directories). No fixture has a per-fixture expected-output artifact.
- **`meta.json` / `capture_metadata.json` files:** **0**. There is no recorded provenance for any fixture (e.g., source URL, captured-at, response-status, content-type, encoding, content-length, capture-tool). The mtime is the only timestamp signal.
- **README.md per directory:** **0**.
- **Tests referencing fixtures:**
  - `tests/scraper/test_hard_exclusions.py:21–26` — the **only** active reference, reading the lexicographically-first `.html` per directory via `sorted(...).glob("*.html")[0]`.
  - Specifically reached directories (via that test): `parking_sale`, `parking_registration`, `parking_construction`, `parking_default_pages`, `parking_control_panels`, `parking_builders_expired`, `parking_cms`, `parking_multilingual`, `cloudflare_challenge`, `meta_refresh_parking`, `noindex_empty_title`, `spa_shell`, `legitimate_business`, `parking_builders` (via test names) — **14 directories**.
  - Not reached by any test: `auth_403`, `empty_google_sites`, `legitimate_blog`, `legitimate_nonprofit`, `login_wall`, `parking_errors`, `parking_hosting`, `parking_redirect_targets`, `soft_404` — **9 directories**.
  - **By fixture count:** if `test_hard_exclusions.py` reads only the first per directory, exactly **14 fixtures** of 197 are actually exercised by the test suite. **183 fixtures (~93%) are orphans** from the test-suite perspective.

### Spot-check: can directory + filename predict the expected outcome?

I picked 10 fixtures at random and predicted the outcome from the path alone:

| Fixture | Predicted outcome | Verifiable from content | Match |
|---|---|---|---|
| `parking_sale/sanluisconnect.com.html` | `is_for_sale=True, is_parked=True, exclusion_reason="parking_sale"` | Contains `domain parking` text | ✓ |
| `cloudflare_challenge/bestlogicgames.com.html` | `is_cloudflare_challenge=True, exclusion_reason="cloudflare_challenge"` | Contains `Attention Required! \| Cloudflare` | ✓ |
| `parking_default_pages/grigolato.net.html` | `is_parked=True, is_holding_page=True, exclusion_reason="parking_default_pages"` | **No nginx/apache marker** — would not fire detector | ✗ (false positive prediction) |
| `legitimate_business/ssquaredassociates.com.html` | `is_parked=False, exclusion_reason=""` | Truncated mid-`<meta>`; 150 B — would trip `insufficient_content` | Ambiguous |
| `auth_403/grimsfairytales.net.html` | `is_parked=True` or `auth_wall` | **0 bytes** — detector would see empty string | ✗ (no signal) |
| `soft_404/bestmarketdeal.com.html` | `exclusion_reason="soft_404"` | Wix empty page; no soft-404 markers | ✗ |
| `parking_builders_expired/wix_expired_synthetic.html` | `is_parked=True, exclusion_reason="parking_builders_expired"` | Matches `this wix site has expired` | ✓ |
| `parking_multilingual/german_neue_internetpraesenz_synthetic.html` | `is_parked=True, exclusion_reason="parking_multilingual"` | Matches `neue internetpräsenz` clause | ✓ |
| `spa_shell/bestmakeupsale.com.html` | `is_spa_shell=True` | 51 B single script tag — **detector might fire via Path D**, but the file isn't really an SPA shell | Ambiguous |
| `legitimate_nonprofit/wikipedia.org.html` | `exclusion_reason=""` (legitimate) | 141 B robots message — would trip `insufficient_content` or `is_empty_page` | ✗ (false positive prediction) |

**Hit rate: 4/10 unambiguous matches.** The directory+filename heuristic fails on the ~31% of fixtures that don't conform, in a way that would silently corrupt any larger test suite built on the convention.

---

## 10. Production Distribution

ADLS sample: `abfss://output@barcadastorage.dfs.core.windows.net/canary-20260509-175114/`. The `canary-20260509/parser/...` prefix the operator initially supplied did **not** exist; the actual prefix is `canary-20260509-175114/parser/...`.

Sample sizes are small (canary scale, not full corpus):

- `parser`: 50 rows (domains)
- `stage1_predictions`: 50 rows
- `stage2_pages`: 339 rows (5–8 pages per domain that progressed)
- `stage2_predictions`: 50 rows
- `stage2_summaries`: 50 rows
- `stage3_predictions`: 16 rows
- `stage3_evidence`: 17 rows

This is **one canary day's output**, not representative of a multi-million-domain crawl. All caveats below are conditional on that.

### `parser.status` distribution (50 rows)

| Status | Count | % |
|---|---:|---:|
| ok | 34 | 68% |
| forbidden | 7 | 14% |
| dns_failure | 3 | 6% |
| empty | 2 | 4% |
| auth_wall | 1 | 2% |
| bot_blocked | 1 | 2% |
| parking | 1 | 2% |
| rate_limited | 1 | 2% |

### `hard_exclusions` flag distribution

All `parser` rows from the canary set:

| Flag | True | % |
|---|---:|---:|
| is_empty_page | 4 | 8% |
| is_parked | 0 | 0% |
| is_for_sale | 0 | 0% |
| is_holding_page | 0 | 0% |
| is_cloudflare_challenge | 0 | 0% |
| is_waf_challenge | 0 | 0% |
| is_geo_blocked | 0 | 0% |
| is_spa_shell | 0 | 0% |
| is_government | 0 | 0% |
| is_social_profile | 0 | 0% |
| is_url_shortener | 0 | 0% |
| is_dns_failed | 0 | 0% |
| is_unreachable | 0 | 0% |

### Stage 1 distribution

- `tier_decided`: rules=30, lr=2, llm=2, upstream_excluded=16
- `is_business`: True=18, False=16, None=16 (None = abstained)
- `abstain`: True=16 (all upstream_excluded), False=34

### Stage 2 distribution (50 rows)

- `tier_decided`: not_technology=23, abstained=15, llm=12
- `top_1_category`: Cloud Infrastructure & Services=3, Data Infra & Analytics=3, Enterprise Software (Vertical)=2, plus single hits for Communication Platforms, Cybersecurity, AI/ML, Finance & Billing, Developer Tools — and 38 None
- `page_acquisition_tier`: T1=50 (T2/T3 not exercised by this canary)
- `abstain_reason`: llm_failed=10, confidence_too_low=5

### Stage 3 distribution (16 rows)

- `primary_partner_type`: Independent Software Vendor=5, Distributor=1, Original Equipment Manufacturer=1, None=9
- `tier_decided`: abstained=9, llm=7

### Production language distribution

`crawl_meta.language_detected`: en=30, ja=1, pt=1, es=1, '<empty>'=18 (the 16 upstream_excluded + 2 empty/error).

### Comparison: production outcome % vs fixture count %

| Production outcome | Prod % | Fixture category(ies) | Fixture % | Coverage gap | Severity |
|---|---:|---|---:|---:|---|
| Legitimate site (status=ok, is_business indeterminate) | 68% | legitimate_business + blog + nonprofit | 8% (16/197) | **−60 pp** | **HIGH** |
| Forbidden / auth-wall | 16% (auth_wall+forbidden) | auth_403 + login_wall | 14% (28/197) | ≈0 pp | – |
| Parking (umbrella) | 2% (status=parking) | parking_* | 59% (116/197) | **+57 pp** | **HIGH (over-collected)** |
| Bot-blocked / cloudflare | 2% | cloudflare_challenge | 1.5% (3/197) | ≈0 pp | – |
| Empty | 4% | empty_google_sites + meta_refresh_parking + noindex_empty_title | 4.6% (9/197) | ≈0 pp | – |
| DNS failure / unreachable | 6% | — | 0% | **−6 pp** | MEDIUM |
| Rate limited | 2% | — | 0% | **−2 pp** | LOW |
| SPA-rendered (is_spa=True) | 0% (50/50 is_spa=False) | spa_shell | 10% (20/197) | **+10 pp** | MEDIUM (over-collected, but valid for testing) |

**Headline gaps:**

1. **Legitimate-site fixture coverage is 60 percentage points below production prevalence.** The fixture corpus is shaped for the parking-detection path; it would not catch a regression in the "ok / is_business" decision well.
2. **Parking-fixture density is 57 pp above production.** Parking detection is over-tested; replacing 50–60% of parking_* with legitimate_business variety would rebalance.
3. **No DNS-failure or unreachable fixtures.** Both are common production outcomes (~6%) but the corpus has zero coverage. Note: these are pre-fetch validator decisions, so an HTML fixture is moot; document the gap with `_read_fixture` doc.

---

## 11. Audit-Remediation Fixture Readiness

Cross-referenced against the Top 30 in `~/crawler-audit/AUDIT_REPORT.md`.

| Action | Title | Fixture readiness | Evidence |
|---|---|---|---|
| #1 | SPA hydration-payload extraction | **ABSENT** | `__NEXT_DATA__`=0, `window.__NUXT__`=0, `__APOLLO_STATE__`=0, `__PRELOADED_STATE__`=0, `__remixContext`=0, Gatsby=0, `data-sveltekit-fetched`=0 across all 197 fixtures |
| #2 | `robots.txt` parser + compliance | **ABSENT** | No `robots.txt` files stored alongside HTML; no `robots.txt` fixture directory; no test would receive a robots.txt body |
| #4 | Network-request interception (XHR/fetch logging) | **ABSENT** | An SPA fixture that loads content via XHR after initial HTML cannot be tested without a HAR; no HAR files exist |
| #5 | Cross-page boilerplate fingerprinting | **ABSENT** | No same-domain multi-page captures. `find … -name "*.html" \| sed 's/.html$//' \| sort \| uniq -c` shows every basename appears exactly once |
| #10 | JSON-LD `BreadcrumbList` extraction | **ABSENT (1 fixture)** | `grep -rl BreadcrumbList tests/fixtures/html/` → 1 match (`legitimate_business/sanluisfloors.com.html`). Insufficient for positive + negative test coverage |
| #13 | Mega-menu interactive activation | **PARTIAL** | `aria-haspopup`=15 fixtures, `aria-expanded`=17 fixtures, but `role="menu"`=0. Some support, but no dedicated `mega_menu/` directory with verified-rich nav structures |
| #14 | Sitemap.xml + canonical URL | **PARTIAL** | `rel="canonical"`=21 fixtures (covers canonical-extraction tests). **No `sitemap.xml` fixture files** anywhere |
| #19 | PII detection + redaction | **PARTIAL** | `mailto:`=17 fixtures, `tel:`=19 fixtures, US-phone-pattern `\d{3}-\d{3}-\d{4}`=6 fixtures. Sufficient for *positive-match* PII tests (real PII patterns exist in real captures). **Insufficient for redaction testing** — no fixture with synthetic SSN, credit card, address+name pairings; no fixture explicitly tagged for PII presence |
| #20 | Regional / non-US fixtures | **ABSENT** | TLD breakdown: 140 `.com`, 33 `.net`, 3 `.org`, 1 `.ca`, 20 synthetic. Zero `.de`, `.fr`, `.jp`, `.br`, `.cn`, `.es`, `.it`, `.nl`, `.uk`, `.ru`, `.au`. `parking_multilingual/` contains 3 *Western European synthetic* fixtures, **no real RTL, no real CJK, no Cyrillic** despite the detector handling all of them |
| #21 | Per-domain crawl history / policy-version stamping | Not fixture-blocking — skip per directive |

**Summary across the 10 audit-blocking items:**

- **ABSENT:** 5 (Actions 1, 2, 4, 5, 20)
- **PARTIAL:** 3 (Actions 13, 14, 19)
- **N/A (1 fixture only):** 1 (Action 10)
- **Skipped:** 1 (Action 21)

The fixture corpus is structurally unable to validate the work proposed in `AUDIT_REPORT.md` §5 without targeted additions.

---

## 12. Recommended Candidate Fixtures

Group by theme. For each recommendation: directory, characteristics, source, rationale, priority.

### SPA framework variants — for Action #1 (hydration-payload extraction)

| # | Add | Directory | Characteristics | Source | Why | Priority |
|--|--|--|--|--|--|--|
| C1 | 3 fixtures | new `spa_hydration_next/` | Next.js pages containing a populated `__NEXT_DATA__` `<script>` block of varying sizes (~5–50 KB JSON). Include one CSR-only, one ISR-style, one full-SSR. | Capture from production parser parquet rows where `metadata_meta_keywords` mentions Next or where raw HTML contains `__NEXT_DATA__`. | Direct unblocker for Action #1 — the highest-ROI audit item. | **CRITICAL** |
| C2 | 2 fixtures | new `spa_hydration_nuxt/` | Nuxt 3 pages with `<script id="__NUXT_DATA__">…</script>` or `window.__NUXT__`. | Production capture; if none in canary, synthesize from a known-Nuxt site (e.g., GitLab-marketing-style). | Same. | **CRITICAL** |
| C3 | 2 fixtures | new `spa_hydration_apollo/` | Pages with `window.__APOLLO_STATE__ = {...}`. | Production. | Same — Apollo Client is common on React stacks. | **HIGH** |
| C4 | 2 fixtures | new `spa_hydration_redux/` | Pages with `window.__PRELOADED_STATE__`. | Production. | Same. | **HIGH** |
| C5 | 2 fixtures | new `spa_hydration_remix_gatsby/` | One Remix (`__remixContext`), one Gatsby (`window.___INITIAL_PROPS___`). | Synthesize if no production samples — these are rarer. | Same; closes the framework-coverage gap. | MEDIUM |
| C6 | 1 fixture | new `spa_hydration_sveltekit/` | `data-sveltekit-fetched` attribute on a `<div>` or `<main>`. | Synthesize if needed. | Same. | MEDIUM |

### Mega-menu samples — for Action #13

| # | Add | Directory | Characteristics | Source | Why | Priority |
|--|--|--|--|--|--|--|
| C7 | 3 fixtures | new `mega_menu/` | One Shopify-style top nav with hover-activated mega panel (button with `aria-haspopup="menu"` + nested `<ul>`); one Salesforce-style multi-column mega menu; one Microsoft-style header with aria-controls cross-references. | Production parquet (look for rows with `signals_site_structure_dropdown_count > 5`) or known SaaS marketing sites. | Validates interactive-activation work; ties to nav-extraction regression. | **HIGH** |
| C8 | 2 fixtures | extend `mega_menu/` | Mobile-viewport mega menu HTML (375 px-width capture) that exposes the same hierarchy via a different DOM structure — for testing mobile-as-hierarchy-ground-truth (§7.6 of AUDIT_REPORT). | Mobile-specific captures (different UA) of the same Shopify/Salesforce sites. | Validates desktop-vs-mobile activation sweep. | MEDIUM |

### PII test fixtures — for Action #19

| # | Add | Directory | Characteristics | Source | Why | Priority |
|--|--|--|--|--|--|--|
| C9 | 3 fixtures | new `pii_positive/` | Pages containing realistic synthetic PII: a contact page with a name + email + phone + street address; a team page with employee names + LinkedIn handles; a footer with a US phone in `xxx-xxx-xxxx` form. **No real PII** — use `John Q. Tester / jtest@example.com / 555-0100-0123`. | Hand-author. Use 555-01XX numbers (RFC 5733 reserved test phones) and example.com emails. | Validates PII detection / redaction work. | **HIGH** |
| C10 | 2 fixtures | new `pii_negative/` | Pages that *look* like they have PII but don't (e.g., a press release mentioning an `incident@securitycorp.com` general inbox — a generic, not personal, address; a phone like 1-800-FLOWERS). | Hand-author. | Negative test for PII false positives. | MEDIUM |

### International / regional samples — for Action #20 + per-locale eval

| # | Add | Directory | Characteristics | Source | Why | Priority |
|--|--|--|--|--|--|--|
| C11 | 2 fixtures | new `international_business/de/` | Real German B2B site captures, .de TLD, German `<html lang="de">`. Include one with `<link rel="alternate" hreflang="en" href="..."/>` so the English-alternative path is exercised. | Production. | Regional policy + locale-stratified eval. | **HIGH** |
| C12 | 2 fixtures | new `international_business/jp/` | Real Japanese B2B site captures, `.co.jp` or `.jp` TLD. | Production. | Same. CJK script coverage. | **HIGH** |
| C13 | 2 fixtures | new `international_business/fr/` | Real French B2B site captures, `.fr` TLD. | Production. | Same. | MEDIUM |
| C14 | 2 fixtures | new `international_business/br/` | Real Brazilian B2B site captures, `.com.br`. Important because `crawl_meta.language_detected=pt` already appears in production (1/50). | Production. | LGPD-region coverage. | MEDIUM |
| C15 | 1 fixture | new `parking_multilingual/cyrillic/` | Real Russian-registrar parking page with Cyrillic phrases like `зарегистрирован и припаркован`. | Production or .ru-zone sample. | Detector covers it; no fixture exercises it. | MEDIUM |
| C16 | 1 fixture | new `parking_multilingual/cjk/` | Real Chinese-registrar parking page with `域名暂时无法访问`. | Production or .cn-zone sample. | Same. | MEDIUM |
| C17 | 1 fixture | new `parking_multilingual/jp/` | Real Japanese-registrar parking page with `お名前.com`. | Production. | Same. | MEDIUM |

### Happy-path B2B diversity — for production-coverage gap (legitimate_* under-represented)

| # | Add | Directory | Characteristics | Source | Why | Priority |
|--|--|--|--|--|--|--|
| C18 | 5 fixtures | extend `legitimate_business/` | 5 modern SaaS marketing sites (Stripe, Notion, Shopify-tier — *as type, not the specific companies*). Should have `<title>`, meta-desc ≥ 30 ch, JSON-LD `@type=Organization`, hreflang, canonical, mega-menu, blog link. | Production. | Closes the 60 pp production-coverage gap. | **HIGH** |
| C19 | 3 fixtures | extend `legitimate_business/` | 3 e-commerce sites with JSON-LD `Product` schema, `<meta property="og:type" content="product">`, structured pricing. | Production. | Diversity beyond SaaS. Many legitimate-business gates depend on `signals_jsonld_has_product_schema` (visible in parser schema). | **HIGH** |
| C20 | 2 fixtures | extend `legitimate_business/` | 2 professional-services sites (law firm, accounting firm) with JSON-LD `@type=LocalBusiness`. | Production. | LocalBusiness branch coverage. | MEDIUM |
| C21 | 2 fixtures | extend `legitimate_business/` | 2 manufacturing-industry sites with Schema.org `@type=Corporation` markup. | Production. | Industry diversity. | MEDIUM |
| C22 | 2 fixtures | extend `legitimate_nonprofit/` | 2 educational + 1 health-advocacy nonprofit, with `@type=NGO` / `@type=EducationalOrganization`. **Drop** `wikipedia.org.html` (non-conforming). | Production / well-known nonprofits. | Replaces broken fixture; covers `_RE_NONPROFIT` schema branches. | **HIGH** |

### Anti-bot freshness refreshes

| # | Add | Directory | Characteristics | Source | Why | Priority |
|--|--|--|--|--|--|--|
| C23 | 1 fixture | extend `cloudflare_challenge/` | DataDome challenge (`_RE_WAF_CHALLENGE` covers `datadome|dd\.js`). | Production where `status=bot_blocked` with DataDome in body. | Validates DataDome branch. | MEDIUM |
| C24 | 1 fixture | extend `cloudflare_challenge/` (or new `waf_akamai/`) | Akamai BMP / Reference-ID interstitial. | Production. | Same. | MEDIUM |
| C25 | 1 fixture | extend `cloudflare_challenge/` (or new `waf_perimeterx/`) | PerimeterX/HUMAN `px-captcha` body. | Production. | Same. | MEDIUM |
| C26 | 1 fixture | new `waf_kasada/` | Kasada `ks-cc` token in body. | Production. | Same. | LOW |

### Cross-page boilerplate samples — for Action #5

| # | Add | Directory | Characteristics | Source | Why | Priority |
|--|--|--|--|--|--|--|
| C27 | 5 directories × 4 pages = 20 fixtures | new `multipage_boilerplate/<domain>/{home,about,pricing,products}.html` | Same-domain captures of 4 pages each, for 5 domains. Pages must share a real header + footer (which is the boilerplate being fingerprinted) and have distinct main content. | Production capture (one domain per business type: SaaS, e-commerce, services, manufacturing, news). | Direct unblocker for Action #5 (cross-page SimHash). | **HIGH** |

### Edge cases

| # | Add | Directory | Characteristics | Source | Why | Priority |
|--|--|--|--|--|--|--|
| C28 | 1 fixture | new `edge_encoding/` | A page served as `Shift_JIS` or `GBK` with correct meta-charset declaration. | Production CJK or hand-author. | Encoding-detection (Action #14 of internal i18n list). | LOW |
| C29 | 1 fixture | new `edge_huge/` | A 1.8 MB page approaching the 2 MB `MAX_RESPONSE_BYTES` cap. | Production. | Validates non-truncation up to the cap. | LOW |
| C30 | 1 fixture | new `edge_malformed/` | Page with unclosed `<head>`, missing `<body>`, or other broken HTML. | Hand-author. | Validates parser robustness. | LOW |

### Total candidate count

- **CRITICAL: 7 fixtures** (C1–C2)
- **HIGH: ~16 fixtures** (C3–C4, C7, C9, C11–C12, C18–C19, C22, C27 set ~5 of 20)
- **MEDIUM: ~13 fixtures**
- **LOW: ~3 fixtures**
- **Recommended total to ADD: ~39 fixtures**, plus
- **Recommended REMOVALS / RELOCATIONS:**
  - Remove: `auth_403/grimsfairytales.net.html` (0 bytes), `legitimate_nonprofit/wikipedia.org.html` (robots-policy message)
  - Move: `spa_shell/bestmakeupsale.com.html` → `parking_redirect_targets/`; `auth_403/gripwellsports.net.html` → `legitimate_business/` or delete; 5 of 6 `parking_default_pages/` `*.html` 581-B files → `auth_403/` (nginx 401)
  - Prune redundant: `meta_refresh_parking/` from 3 → 1; `parking_default_pages/` from 6 → 2; `parking_construction/` from 37 → 8; `parking_sale/` from 19 → 8; `auth_403/` from 15 → 6; `login_wall/` from 13 → 6.

After remove/prune (~50–55 deletions) and add (~39 additions), the net corpus shifts from **197** to about **180** fixtures, but with substantially better discrimination and audit-remediation coverage.

---

## 13. Prioritized Fixture Work Plan

Ordered by `(impact ÷ effort)`. Effort: **L** = ≤ 2 hours, **M** = ≤ 1 day, **H** = > 1 day.

| # | Work item | Effort | Impact / unblocks | Dependencies |
|---|---|:-:|---|---|
| 1 | **Remove `auth_403/grimsfairytales.net.html`** (0 bytes) | L | Restores `test_hard_exclusions.py:_read_fixture("auth_403")` correctness (currently picks up the zero-byte file due to alphabetic sort). | None |
| 2 | **Remove `legitimate_nonprofit/wikipedia.org.html`** (robots-policy message) and replace with a real .org capture | L | `test_hard_exclusions.py` doesn't reference `legitimate_nonprofit` today, so no test breaks — but the fixture is actively misleading and may be picked up if a future test enumerates it. | None |
| 3 | **Replace `soft_404/` contents** with 6 real search-results pages | M | Currently 0/14 conform; the directory's contract is broken. Pick 6 real captures with markers like `did you mean`/`showing results for`/`no results found`. | Need production captures or synthesize. |
| 4 | **Replace `empty_google_sites/` contents** with 3 real Google Sites captures | M | Currently 0/3 conform; verify the `is_empty_google_sites` detector still has marker support. | Need real Google Sites empty-custom-domain captures. |
| 5 | **Add SPA hydration-payload fixtures** (C1, C2, C3, C4): 9 fixtures across `spa_hydration_{next,nuxt,apollo,redux}/` | M | **Blocks audit Action #1** (the single highest-ROI item). Each fixture is a 30 KB+ real HTML with the relevant `<script>` block. | Source from production parquet `parser.raw_html` or stage2_pages where present. |
| 6 | **Add 5 modern SaaS `legitimate_business/` fixtures (C18)** | M | Rebalances production-coverage gap from 8% → ~12%; tests is_business=True path with hreflang/canonical/JSON-LD/mega-menu. | Production. |
| 7 | **Add 5 multipage_boilerplate/ domains (C27, 4 pages each = 20 fixtures)** | H | **Blocks audit Action #5** (cross-page SimHash fingerprinting). | Production capture; need to verify the 4 pages all share a common header/footer. |
| 8 | **Add 6 international fixtures (C11–C14)** in `international_business/{de,jp,fr,br}/` | M | **Blocks audit Action #20** (regional policy enforcement); enables per-locale eval. | Production. |
| 9 | **Add 3 mega_menu/ fixtures (C7)** | M | **Blocks audit Action #13** (mega-menu interactive activation). | Production or known SaaS sites. |
| 10 | **Add 5 PII fixtures (C9–C10)** in `pii_positive/` + `pii_negative/` | L | **Unblocks audit Action #19** (PII detection / redaction). | Hand-author with safe synthetic PII. |
| 11 | **Prune `parking_construction/` from 37 → 8** with explicit structural diversity | L | Eliminates dilution; same code-path coverage with 22% the maintenance burden. | None. |
| 12 | **Prune `parking_sale/` from 19 → 8** with marketplace diversity | L | Same. | None. |
| 13 | **Prune `parking_default_pages/`** to 2 (one nginx-401, one apache default, one IIS) + move 4 of the 581-B files to `auth_403/` | L | Cleans up redundancy + addresses misclassification of nginx 401 pages. | None. |
| 14 | **Prune `auth_403/` from 15 → 6** by removing the 6 non-conforming files + the zero-byte file | L | Improves directory's signal-to-noise without losing coverage. | None. |
| 15 | **Prune `login_wall/` from 13 → 6** by removing the 6 non-conforming files | L | Same. | None. |
| 16 | **Move `spa_shell/bestmakeupsale.com.html`** → `parking_redirect_targets/` | L | Correct misclassification. | None. |
| 17 | **Move `auth_403/gripwellsports.net.html`** → `legitimate_business/` or delete | L | Same. | None. |
| 18 | **Add 3 multilingual parking fixtures (C15–C17)** for Cyrillic, CJK, JP | L | Exercises detector branches that currently have no fixtures. | Production. |
| 19 | **Add 1 BreadcrumbList fixture** to `legitimate_business/` | L | **Blocks audit Action #10**. | Hand-author or production. |
| 20 | **Add `meta.json`** alongside each fixture with source URL, captured-at, response-status, content-type, content-length, encoding | M | Adds provenance — eliminates the "is this fixture real?" question raised throughout this audit. Future-proofs subsequent audits. | Hand-fill from `git log` + memory for existing fixtures; auto-populate from `requests` response for new captures. |
| 21 | **Add `expected/` directory per fixture** with serialized `extract_hard_exclusions` output | H | Turns the corpus into a regression-safe asset; lets a future `test_fixture_regression.py` enumerate every fixture, not just the first. | Depends on items 1–4 being done first so no broken fixture poisons the expected outputs. |
| 22 | **Add a `tests/scraper/test_fixture_coverage.py`** that fails if any fixture in a directory does *not* trigger the directory's expected detector | M | Operationalizes the spec-equals-directory-name convention. Prevents future fixture rot. | Items 1–4. |
| 23 | **Add 1 fixture each for DataDome / Akamai / PerimeterX (C23–C25)** in `cloudflare_challenge/` (or rename to `waf_challenge/`) | M | Exercises WAF branches with no fixture today. | Production or synthesize. |
| 24 | **Add 1 SvelteKit, 1 Remix, 1 Gatsby fixture (C5–C6)** to `spa_hydration_*/` | M | Closes framework coverage gap. | Synthesize from minimal templates. |
| 25 | **Add edge-case fixtures (C28–C30)**: encoding, huge, malformed | M | Robustness margin. | Hand-author. |

### Critical-path summary

To unblock all currently-blocked audit-remediation actions, the minimum work is items **1–10 + 19** above:

- **6 fixture deletions / relocations** (items 1, 2, 13, 16, 17, partial 14/15)
- **~33 new fixtures** (items 3–10 + 18, 19)
- **Estimated effort:** 4–6 engineer-days (or one focused week)
- **Output:** corpus rebalances from ~31% non-conforming to <5% non-conforming; production gap closes from 60 pp to ~25 pp; every Top-30 audit item has at least one fixture to test against.

The high-effort, longer-term items (20–25) are foundational improvements (provenance metadata, expected-outputs directory, conformance test) that should follow the critical-path work.

---

*End of report. The fixture corpus is functional for the single test that consumes it (`test_hard_exclusions.py`) but is structurally inadequate for the audit-remediation work proposed in `AUDIT_REPORT.md` §5. See §1 for the state-delta flag and §13 for the prioritized work plan.*
