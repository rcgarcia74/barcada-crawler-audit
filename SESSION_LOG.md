# Session Log

Chronological record of audit and remediation sessions. Each entry:
header (date, scope), key decisions, commits produced (workspace +
repo), open questions, next work unit.

The most recent entry is at the bottom (append-only). Older entries
are not edited after the fact; corrections are made via a new entry
that supersedes.

---

## Session 1 — Initial workspace setup (~2026-05-17 to 2026-05-18, pre-audit)

Scope: Establish the audit workspace separate from the repo. Draft
the consolidated remediation plan.

Decisions:
- Workspace lives at `/Users/administrator/crawler-audit/`, distinct
  from the repo at `/Users/administrator/projects/barcada-scraper/`.
  Workspace is its own git repo; commits and pushes are independent.
- PII work scope-decision: excluded from the remediation plan. PII
  handling needs separate AI/ML review.

Workspace commits:
- `2d9d38a` Add consolidated remediation plan v1.0
- `3f0389f` Remove PII work from remediation plan

Next: Run the code audit against the repo.

---

## Session 2 — Code audit (2026-05-18, read-only)

Scope: Static analysis of `barcada-scraper` against AUDIT_DIRECTIVE.md
Sections 1-15. Read-only mode (no repo writes by the auditor).

Output: `AUDIT_REPORT.md` (798 lines, 30 prioritized actions).

Findings summary:
- Strengths: schema versioning discipline, immutable cost journal with
  ETag writes, anti-bot detection breadth (14+ vendors), deterministic-
  first classifier cascade (RULES → LR → LLM).
- Critical gaps: no robots.txt parser; no SPA hydration extraction;
  no per-domain budgets; no cost-per-useful-record KPI; no structured
  logging or metrics emission.
- Section 5 lists the Top 30 actions ordered by impact ÷ effort.

State delta flagged (auditor did not cause): HEAD advanced by 2
commits during audit window (`e51a93f`, `be71d53` — operator eval_data
work running in parallel).

Next: Run the fixture audit.

---

## Session 3 — Fixture audit (2026-05-18, read-only)

Scope: Static analysis of `tests/fixtures/html/` (197 HTML files,
23 directories). Read-only mode.

Output: `FIXTURE_AUDIT_REPORT.md` (654 lines, 10 candidate fixtures).

Findings summary:
- 7% fixture utilization due to `sorted(glob)[0]` pattern in
  `tests/scraper/test_hard_exclusions.py:26`.
- Broken directory contracts: `soft_404/` 0/14 conform; `empty_google_
  sites/` 0/3 conform.
- One 0-byte fixture (`auth_403/grimsfairytales.net.html`); one
  141 B misleading fixture (`legitimate_nonprofit/wikipedia.org.html`,
  Wikipedia robots-rejection page).
- 5 truncation suspects at suspicious round byte boundaries (200000,
  131072, three at 32752).
- Production-distribution mismatch: 59% parking fixtures vs 2%
  production parking; 8% legitimate fixtures vs 68% production "ok".
- 10 candidate fixtures (C1-C10) recommended in §12 of the report;
  the audit's broader "candidates" list extends to C30.

State delta flagged: HEAD advanced by 1 commit during audit window
(`d44f034` — operator eval_data work).

Next: Synthesize audit findings into an actionable remediation plan.

---

## Session 4 — Plan consolidation, classification-adjacent split, plan revisions (2026-05-19)

Scope: Build the operational remediation plan. Split classification-
touching items into a separate document for AI/ML review.

Outputs:
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` (Draft v1.0): six workstreams
  (0, A.0, A, B, C, D, E), explicit prerequisites, 20-week timeline.
- `CLASSIFICATION_ADJACENT_PLAN.md`: 9 classification-adjacent items
  for AI/ML team review.

Workspace commits:
- `e3f5691` Remediation plan and session log (bundles plan + this
  session log + earlier ad-hoc edits made during the Claude Code
  session by Claude's Edit tool — including Days-1-2 status updates,
  Week 3 C22 addition, Week 5 followup additions, §11 risk register
  addition for the recapture retry-policy lesson).

Decisions during the Claude Code session that revised the plan:
- Risk #6 (single-tenant guard) removed — verified non-applicable to
  fixture capture scripts (`single_tenant_guard.py` wires into
  `classifier/cli.py`, not into Playwright/curl captures).
- Baseline-v0 tagging: single tag at post-expected-outputs commit;
  no `tag -f`.
- Launch scenarios stated as 3 options ((a) ship as-is, (b) Workstream
  0+A, (c) Workstream 0+A.0+A). Option (c) selected; no firm launch
  date; reassess at A.0 completion.
- Candidate #5 (international fixtures): revised from 6 to 3 (1× .de,
  1× .jp, 1× .com.br). Action #20 testable at ~85% with 3; CCPA and
  PIPL deferred regardless of fixture count.
- AI/ML decision deadline 2026-06-16 for classification-adjacent
  Items 1, 2, 5. If undecided, Workstream B reorders to follow C.
- Schema bumps batched per workstream.
- Cost ceiling $100, alert at $50.
- Synthetic-with-real-markers fallback acceptable for any future
  capture work where real-domain sourcing fails. Documented in plan
  §3 Week 5.
- C22 added to Week 3+: 2-3 archetypal nonprofits for
  `legitimate_nonprofit/` (Wikimedia Foundation, an
  EducationalOrganization, an archetypal philanthropy).
- Fixture capture scripts must use bulk_writer.py-style branch guard
  and retry-on-connection-error policy (≥3 attempts).
- Co-Authored-By line is not added to commits (operator preference,
  recorded in `.claude/rules/code-correctness.md`).

Next: Execute Workstream 0 Week 1 Days 1-2 critical repairs.

---

## Session 5 — Workstream 0 Week 1 Days 1-2 execution (2026-05-19)

Scope: 5 critical-repair actions (C0.1-C0.5) on the barcada-scraper
repo. Sub-commits as needed for "small, action-numbered, individually
revertable" discipline.

Pre-work: Operator created `pre-remediation-2026-05-19` tag at
`3cbb9b3` and pushed to origin — nuclear-revert anchor for all
Workstream 0+ work.

Repo commits (9 total, all on `main`, all pushed to origin):
- `96dcbfd` C0.1: delete auth_403/grimsfairytales.net.html (0-byte)
- `bef4b80` C0.2: replace legitimate_nonprofit/wikipedia.org.html
  with mozilla.org (48,389 B real Mozilla Foundation homepage)
- `3fa3228` C0.3: empty soft_404/ — delete 14 non-conforming
- `7f3756b` C0.4: empty empty_google_sites/ — delete 3 non-conforming
- `b7089eb` C0.5a: delete spa_shell/shelterstoreau.com.html
  (misclassified-via-truncation; real domain is e-commerce, not SPA)
- `3dec85b` C0.5b: delete spa_shell/shelterstores.com.html (same)
- `45bbe30` C0.5c: replace parking_sale/shelvs.com.html with fresh
  recapture (HugeDomains landing, 43,512 B, 92 for-sale markers)
- `26771e9` C0.5d: accept legitimate_business/sanmarcosflowershop.com.
  html truncation (later revised — see followup)
- `a156727` C0.5d-followup: replace sanmarcosflowershop.com.html
  (485,599 B fresh capture; TLS was transient, not persistent;
  followed 301 to flowersbyroberttaylor.com)

pytest `tests/scraper/test_hard_exclusions.py`: 43 passed after each
commit (sanity net; not a regression check, see §11).

Net corpus state: 197 → 177 fixtures.

Discoveries during execution:
- `shelterstoreau.com.html` and `shelterstores.com.html` were
  misclassified as SPA shells because truncation made them look
  script-heavy / content-light. Recapture revealed they are real
  e-commerce sites with semantic `<nav>` (audit had noted has_nav=3).
  Fresh captures deferred to audit C18 (legitimate_business/
  expansion).
- `sanmarcosflowershop.com` TLS failure on first attempt was
  transient (3-attempt probe: 1 fail, 2 success). Lesson captured in
  plan §11 Risk Register: future capture tooling must implement
  retry-on-connection-error policy (≥3 attempts) before drawing a
  persistence conclusion.

Decisions during execution:
- soft_404/ and empty_google_sites/ resolved as REPLACE (not REMOVE):
  Stage A deletion done in C0.3/C0.4; repopulation scheduled Week 5
  (C0.3-followup, C0.4-followup; synthetic-with-real-markers
  fallback acceptable).
- Mozilla.org accepted as the legitimate_nonprofit/ replacement
  despite being tech-leaning; audit C22 expansion (Week 3+) adds
  archetypal nonprofits to balance the directory mix.

Workspace updates this session:
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` edited inline (via Claude
  Code Edit calls) to reflect Days-1-2 status, Week 3 C22 addition,
  Week 5 followup additions, §11 risk register addition. Commit
  bundled into `e3f5691` by operator-side tooling.

Open items entering Days 3-5:
- C0.7a-d (audit §6 relocations): delete bestmakeupsale, delete
  gripwellsports, batch-move 4 nginx-401 files to auth_403/, delete
  bestmactips.
- C0.8: refactor `sorted(glob)[0]` → `_iter_fixtures()` with
  `@pytest.mark.parametrize`.
- C0.9: add `tests/scraper/test_fixture_conformance.py` (red builds
  expected per §11 Risk #3, the fixture-rot acceptance window).

Next: C0.7a (delete spa_shell/bestmakeupsale.com.html).

---

## Session 6 — Workstream 0 Week 1 Days 3-5 execution + Week 1 close (2026-05-19)

Scope: 7 commits to close out Workstream 0 Week 1 — 4 audit §6
fixture relocations (C0.7a-d) + sorted(glob)[0] refactor (C0.8) +
new directory-spec conformance test (C0.9, lands with expected red
builds per Risk #3) + 1 format follow-up (C0.8-format-fix).

Repo commits (7 total, all on `main`, all pushed to origin):
- `f51ca15` C0.7a: delete spa_shell/bestmakeupsale.com.html (51 B
  GMO parking, non-conforming). Per-operator decision: delete rather
  than move to parking_redirect_targets/ — audit hedged on
  destination and neither parking_redirect_targets/ nor a
  hypothetical parking_gmo/ cleanly matches the fixture content.
- `650d06d` C0.7b: delete auth_403/gripwellsports.net.html (44 KB
  real WordPress site, misclassified). Delete rather than move to
  legitimate_business/ — 24-day-old capture; fresh modern-WP
  fixtures coming via audit C18 in Week 3+.
- `4f8dc06` C0.7c: batch-move 4 nginx-401 files from
  parking_default_pages/ to auth_403/ (sanmarcosdentists,
  sanmarcosflower, sanmarcosforsale, sanmarcoshouse). All four
  retain "401 Authorization Required" title; parking_default_pages/
  now 2/2 conform (grigolato IIS + sanluishouston nginx-welcome).
- `7b9fa60` C0.7d: delete parking_errors/bestmactips.com.html
  (Cloudflare 526 SSL error). Per-operator decision: delete rather
  than move to cloudflare_challenge/ — Cloudflare 5xx errors don't
  match _RE_CLOUDFLARE_CHALLENGE (targets JS interstitials).
- `684a9ba` C0.8: refactor sorted(glob)[0] → _iter_fixtures() in
  test_hard_exclusions.py; parametrize 8 high-conformance directory
  tests (cloudflare_challenge, meta_refresh_parking,
  noindex_empty_title, parking_builders_expired, parking_cms,
  parking_control_panels, parking_multilingual,
  parking_default_pages). Test count 43 → 64 passed.
- `6dace7d` C0.9: add tests/scraper/test_fixture_conformance.py.
  Enumerates every fixture in every directory; asserts each matches
  its directory's detector. **Lands with 17 red builds**
  (acceptable per Risk #3 fixture-rot acceptance window). Result:
  145 passed + 17 failed + 2 skipped.
- `4f9d23f` C0.8-format-fix: ruff format follow-up to C0.8
  (collapsed 3-line `extract_hard_exclusions(...)` calls to single-
  line; pre-push gate caught the format mismatch). Pure formatting;
  no logic change. pytest still 64 passed.

Annotated tag created: `workstream-0-week1-end` at `4f9d23f`
(pushed to origin). Pre-push gate is green at this SHA; pushable
state. Tag location flagged to operator (operator preferred 6dace7d
literally, but 4f9d23f was retained because it's the last fully-
green commit).

Test surface change:
  test_hard_exclusions.py: 43 → 64 passing (parametrized 8 dirs)
  test_fixture_conformance.py: NEW, 162 collected
  Fixture utilization for the HTML corpus: ~7% → near-100%

──────── Week 5 cleanup punch list (17 failing fixtures) ────────

spa_shell/ (3 of 17):
  sanmarinoiron.com — audit-noted has_nav=1, ambiguous SPA/full
  sheltrise.com — body fails SPA detector paths
  ssronghua.com — body fails SPA detector paths

auth_403/ (7 of 17):
  bestlyn.com — bare nginx-403, no "permission denied" phrasing
  bestmacclub.com — same bare-403 pattern
  grigna.net — audit-identified non-conformer
  sanmaolv.com — bare-4xx pattern
  ssptjp.com — audit-identified non-conformer
  ssquaresemi.com — audit-identified non-conformer
  ssrcbank.com — bare-4xx pattern
  (NOTE: the 4 nginx-401 files moved in by C0.7c DO pass the
   conformance check, likely via a secondary detector path.)

legitimate_business/ (4 of 10):
  sanluisfinancial.com — 1064 B, "tiny for a real business"
  sheltonestates.com — body fails legitimacy gates
  ssquaredassociates.com — 150 B truncated mid-meta
  ssquaredbicycles.com — 8192 B suspiciously round, no block tags

legitimate_blog/ (2 of 3):
  danluu.com — 405 B intentionally minimal (audit said edge-case
    CONFORMS but strict test treats as insufficient_content)
  jvns.ca — 1.4 KB Hugo minimal

legitimate_nonprofit/ (1 of 3):
  archive.org — audit said this CONFORMS as a 2.7 KB nonprofit;
    failure warrants Week 5 investigation

────────────── End-of-Week-1 net state ──────────────

Repo: 16 commits ahead of `pre-remediation-2026-05-19` (9 from
Days 1-2 + 7 from Days 3-5), all pushed to origin/main.
Tag `workstream-0-week1-end` created at `4f9d23f` (pushed).

Fixture corpus: 197 → 175 fixtures (rough count; +1 mozilla.org,
-14 soft_404, -3 empty_google_sites, -1 zero-byte grimsfairytales,
-1 141-byte wikipedia, -2 misclassified spa_shell, -1 GMO parking,
-1 misclassified WP, -1 Cloudflare 526, -0 truncation suspects
resolved in place via C0.5c/C0.5d-followup, 4 nginx-401 moved
within corpus = net zero).

Pre-push validation passes at HEAD: ruff check/format/vermin/
eval_data validation all green at 4f9d23f.

──────── Discovery during Days 3-5 execution ────────

- Two of the C0.5 truncation suspects (shelterstoreau,
  shelterstores) were misclassified-via-truncation — they're real
  e-commerce sites that the truncation made look SPA-like. Fresh
  captures deferred to audit C18.
- sanmarcosflowershop.com TLS failure on first C0.5d attempt was
  transient; C0.5d-followup replaced in-place after retry probe.
  Lesson captured in plan §11 Risk Register and now in LESSONS.md.
- Operator's initial SESSION_LOG.md content (in workspace commit
  e3f5691) was speculative and inaccurate; replaced with truth-of-
  record entries in workspace commit 2e21c2d.

──────── Operator decisions made during Days 3-5 ────────

- C0.7a/C0.7d disposition: DELETE rather than move when audit
  hedged on destination directory and detector wouldn't fire on
  the fixture's actual content in either bucket. Pattern recorded
  in LESSONS.md.
- C0.7c commit shape: batch 4 nginx-401 moves into one commit
  (same decision, same target). Pattern recorded in LESSONS.md.
- C0.8 parametrize policy: only directories with 100% audit-
  confirmed conformance, to keep pytest green. Low-conformance
  directories surface their rot via C0.9 conformance test instead.
- C0.9 lands with red builds (17 failures); xfail markers NOT
  added. Each red is a Week 5 cleanup action item.
- Tag at 4f9d23f (not 6dace7d) — retained at HEAD after operator
  reviewed trade-off (4f9d23f has clean pre-push gate; 6dace7d
  would have ruff format check failing).

──────── Workspace updates this session ────────

- (this commit, SHA TBD) SESSION_LOG.md Session 6 entry +
  SESSION_TRANSITION_TEMPLATE.md fill for Week 2 + LESSONS.md
  create (transition prep for Session 7).

──────── Open items entering Week 2 ────────

- C1 series (Week 2): 9 SPA hydration captures across 4 new
  directories (3 Next.js, 2 Nuxt, 2 Apollo, 2 Redux). Audit
  candidates C1-C4.
- All Week 2 captures MUST use retry-on-TLS-error policy ≥3
  attempts per LESSONS.md / plan §11 Risk Register.
- Update test_fixture_conformance.py COVERED set when each new
  spa_hydration_*/ directory lands; consider adding hydration-
  payload-specific conformance assertions (e.g., parseable JSON
  in __NEXT_DATA__).
- Week 5 punch list (17 fixtures above) is reserved for Week 5;
  Session 7 should NOT touch these — they're tracked, intentional
  reds.

Next session prompt: see SESSION_TRANSITION_TEMPLATE.md.
Next concrete work: C1.1 (3 Next.js hydration captures into new
spa_hydration_next/ directory).

---

## Session 7 — Workstream 0 Week 2 open + C1.1 scope revision (2026-05-19)

Scope: Begin Week 2 SPA hydration captures (C1.1-C1.5, 9 fixtures
total per plan §3 Week 2). First action C1.1 (3 Next.js hydration
fixtures into new spa_hydration_next/).

──────── Discovery: __NEXT_DATA__ is no longer canonical ────────

Before capturing any C1.1 fixture, an empirical probe of 6
well-known Next.js production marketing sites revealed that the
plan §3 Week 2 / FIXTURE_AUDIT_REPORT.md §12 C1 specification
(Next.js sites containing `__NEXT_DATA__` script blocks, in CSR /
ISR / full-SSR variants) targets a near-extinct pattern. Probe
results (UA `Mozilla/5.0 (compatible; Barcada/1.0)`,
retry-on-TLS-error policy per LESSONS.md, all single-attempt OK):

| Site         |   Bytes | `__NEXT_DATA__` | `__next_f.push` (RSC) | Variant            |
|--------------|--------:|----------------:|----------------------:|--------------------|
| nextjs.org   |  305 KB |               0 |                    30 | App Router         |
| vercel.com   |  935 KB |               0 |                   101 | App Router         |
| hashnode.com |  457 KB |               0 |                    41 | App Router         |
| supabase.com |  387 KB |     1 (299 B)   |                     0 | Pages Router CSR   |
| tldraw.com   |   13 KB |               0 |                     0 | Not Next.js        |
| railway.app  |   101 B |               — |                     — | UA-blocked (404)   |

Root cause: Next.js 13 (October 2022) made App Router the default.
App Router emits hydration as RSC streaming
(`<script>self.__next_f.push([...])</script>`), **not**
`__NEXT_DATA__`. The CSR / ISR / full-SSR taxonomy is a
Pages-Router concept; App Router's data-fetching uses Server
Components with no equivalent client-visible distinction. By
2026 the production ecosystem is dominantly App Router.

The plan and audits (May 2026) are entirely silent on this
migration — `grep` across workspace + scraper code returned zero
mentions of "App Router", "RSC", or `__next_f`. AUDIT_REPORT.md
Action #1 and the original C1 spec target only `__NEXT_DATA__`.

Per LESSONS.md Step-6 escalation pattern, stopped before any
fixture capture and surfaced to operator.

──────── Operator decision (hybrid, recorded 2026-05-19) ────────

C1.1 revised scope (3 fixtures total in `spa_hydration_next/`):
- **1 Pages-Router** fixture with `__NEXT_DATA__`: supabase.com
  (CSR-only variant, 299 B payload). Covers legacy long-tail.
- **2 App-Router** fixtures with RSC streaming: nextjs.org
  (30 `__next_f.push` calls) and vercel.com (101 calls). Covers
  the modern majority.

Rationale: matches the production reality the eventual Action #1
detector will need to handle, keeps Week 2 budget at 9 fixtures,
and gives Pages-Router coverage via supabase without forcing a
hunt for ISR/SSR Pages-Router examples that may no longer exist.

──────── Same probe-before-lock discipline applies to C1.2-C1.4 ────────

By operator-discussed extension of the C1.1 decision, the
probe-before-lock discipline applies forward to:
- **C1.2 (Nuxt):** Nuxt 2 used `window.__NUXT__`; Nuxt 3
  (November 2022) uses `<script id="__NUXT_DATA__" type=
  "application/json">`. Probe 4-6 candidates before sourcing.
- **C1.3 (Apollo):** Apollo Client 3 sometimes embeds state
  under `window.__APOLLO_STATE__`, sometimes streams via custom
  dispatcher keys. Probe before locking.
- **C1.4 (Redux):** `window.__PRELOADED_STATE__` is the classic
  SSR pattern; many production React apps have migrated to
  Zustand, Jotai, or RSC-native state. Probe before locking.

Codified as a LESSONS.md "Diagnostic patterns" entry this session.

──────── Workspace updates this session ────────

- SESSION_LOG.md: this entry.
- LESSONS.md: new "Probe framework generation before locking
  fixture spec" entry under "Diagnostic patterns".
- (NOT updated: BARCADA_CRAWLER_REMEDIATION_PLAN.md — operator
  treats this as read-only, period.)

──────── Open items / next concrete work ────────

- C1.1.a: capture supabase.com.html into new
  tests/fixtures/html/spa_hydration_next/ (1 Pages-Router
  CSR-only fixture).
- C1.1.b: nextjs.org.html (1 App-Router RSC fixture).
- C1.1.c: vercel.com.html (1 App-Router RSC fixture).
- Then C1.2 (Nuxt) — apply probe-before-lock discipline.
- Then C1.3 (Apollo), C1.4 (Redux) — same.
- Then C1.5 (extend test_fixture_conformance.py: COVERED set +
  hydration-payload assertions for all 4 new directories).

──────── Session 7 close: Workstream 0 Week 2 complete (2026-05-20) ─

Workstream 0 Week 2 (Critical SPA Hydration Fixtures) is complete.
12 commits landed across the workspace + repo. The "probe-before-
lock" discipline established by C1.1's App Router discovery was
applied to all 4 framework directories and surfaced 3 more
production-extinction findings (Nuxt 2, Apollo SSR, Redux SSR).
Net Week 2 fixtures added: 10 (3 Next.js + 3 Nuxt + 2 Apollo +
2 Redux), spanning real production captures and §11 synthetic-
with-real-markers fallbacks. (Total Session 7 repo commits is 11
— 10 fixture-add commits plus the C1.5 conformance test
extension; an earlier draft of this entry conflated "commits" and
"fixtures" as 11 each. See Week 2 audit erratum below.)

Workspace commits this session (~/crawler-audit/):
- `29d1bed` Session 7 open: C1.1 scope revision + LESSONS
  framework-probe pattern (this session opener; SESSION_LOG +
  LESSONS.md updates only — plan stayed untouched per operator
  correction "BARCADA_CRAWLER_REMEDIATION_PLAN.md is read-only,
  period.")
- (this commit, SHA TBD) Session 7 close: workstream-0-week2-end
  narrative + SESSION_TRANSITION_TEMPLATE.md refill for Session 8.

Repo commits this session (`barcada-scraper`, all on `main`, all
pushed):

| #  | SHA       | Action  | Fixture / file                              |
|----|-----------|---------|---------------------------------------------|
|  1 | `5f30ce8` | C1.1.a  | spa_hydration_next/supabase.com.html        |
|  2 | `1754854` | C1.1.b  | spa_hydration_next/nextjs.org.html          |
|  3 | `b4740f6` | C1.1.c  | spa_hydration_next/vercel.com.html          |
|  4 | `630f30e` | C1.2.a  | spa_hydration_nuxt/nuxt.com.html            |
|  5 | `7b7ae21` | C1.2.b  | spa_hydration_nuxt/backmarket.com.html      |
|  6 | `ec60142` | C1.2.c  | spa_hydration_nuxt/gitlab.com.html          |
|  7 | `5bf52db` | C1.3.a  | spa_hydration_apollo/coursera.org.html      |
|  8 | `f2b1e7e` | C1.3.b  | spa_hydration_apollo/synthetic_devtools_marketing.html |
|  9 | `871cad8` | C1.4.a  | spa_hydration_redux/synthetic_blog_minimal.html |
| 10 | `a616555` | C1.4.b  | spa_hydration_redux/synthetic_ecommerce_heavy.html |
| 11 | `e5d2f91` | C1.5    | tests/scraper/test_fixture_conformance.py extend |

Annotated tag created and pushed: `workstream-0-week2-end` at
`e5d2f91` (the C1.5 commit; pre-push gates GREEN at this SHA).

──────── Per-action operator decisions made during Session 7 ───

- **C1.1 (Next.js)** — operator chose **Hybrid** (1 Pages-Router
  CSR-only + 2 App-Router RSC). Empirical 6-site probe found 3/6
  App Router, 1/6 Pages Router, 2/6 neither. The CSR/ISR/SSR
  taxonomy in the audit/plan is a Pages-Router concept; App Router
  uses RSC streaming via `self.__next_f.push([…])`. Plan/audit
  were silent on the Next.js 13 (Oct 2022) App Router migration —
  3.5 years of un-flagged production drift.
- **C1.2 (Nuxt)** — operator chose **All three: nuxt.com +
  backmarket.com + gitlab.com**, expanding C1.2 from 2 → 3
  fixtures (Week 2 budget 9 → 10 originally, ultimately 11 with
  the C1.4 synthetics). Empirical 6-site probe found Nuxt 2
  effectively extinct; all 3 Nuxt-shipping sites use Nuxt 3's
  `<script id="__NUXT_DATA__" type="application/json">`. The
  C2 spec's `window.__NUXT__` OR `<script id="__NUXT_DATA__">`
  "or" clause is satisfied by Nuxt 3 alone — observed `window.
  __NUXT__` markers are backwards-compat aliases, NOT Nuxt 2
  evidence.
- **C1.3 (Apollo)** — operator chose **Hybrid: coursera.org real +
  1 synthetic**. Empirical 13-site probe found 1/13 (≈7.7%) hit
  rate for non-empty `__APOLLO_STATE__`; expedia.com ships the
  marker but seeds an empty `{}` cache. Apollo Client SSR cache
  extraction is essentially a legacy opt-in pattern in 2026.
  Synthetic C1.3.b authored with Apollo Client v3 normalization
  (ROOT_QUERY, __ref, __typename, "Type:id" keys); 12,057 B HTML
  with 6,981 B parseable cache.
- **C1.4 (Redux)** — operator chose **Both synthetic**. Empirical
  12-site probe found **0/12** hit rate for `__PRELOADED_STATE__`,
  `__INITIAL_STATE__`, OR loose `window.initialState`. Redux SSR
  state extraction is genuinely extinct in 2026 production
  marketing/consumer surfaces — modern React SSR uses RSC
  streaming, cookies, or post-hydration fetch. Two synthetics
  authored: minimal blog (4,972 B, 2,129 B state) and heavy RTK +
  RTK-Query e-commerce (12,489 B, 9,408 B state).
- **Workspace correction (Session 7 turn 12 ~)**: operator clarified
  that `BARCADA_CRAWLER_REMEDIATION_PLAN.md` is treated as
  read-only despite its §14 "UPDATED inline" wording. All
  deviations from the plan land in SESSION_LOG.md and LESSONS.md
  only. Memory saved as `feedback_remediation_plan_readonly.md`.

──────── Test surface change (repo) ─────────────────────────────

  test_hard_exclusions.py:        64 passed (unchanged)
  test_fixture_conformance.py:    155 passed → 219 passed
                                  (+64 = 11 new spa_hydration_*
                                  parametrize cases + 53 from
                                  internal restructuring of
                                  parametrize id resolution after
                                  catch-all flip — actually +10
                                  parametrize cases and +1 catch-
                                  all flip; the rest were already
                                  in the count baseline pre-C1.1.a)
  test_fixture_conformance.py:    18 failed → 17 failed
                                  (catch-all flipped from FAIL to
                                  PASS; the remaining 17 are the
                                  Week 5 punch list, unchanged from
                                  Week 1 close)
  test_fixture_conformance.py:    2 skipped (soft_404/ and
                                  empty_google_sites/, unchanged)

  Total: 64 + 219 + 17 + 2 = 302 collected. Up from 64 + 208 + 18 +
  2 = 292 at Week 1 close — net +10 new conformance assertions, all
  green.

──────── Workspace updates this session ─────────────────────────

- LESSONS.md (in `29d1bed`): new "Probe framework generation before
  locking a fixture spec" entry under Diagnostic patterns, codifying
  the empirical probe-before-source discipline used across C1.1-C1.4.
- SESSION_LOG.md (this entry, this commit): full Session 7 narrative
  + open items for Week 3.
- SESSION_TRANSITION_TEMPLATE.md (this commit): refilled for Session
  8 (Week 3 high-priority gap fixtures: C5 international + C18
  modern SaaS + C22 nonprofit + C7 mega-menu).
- BARCADA_CRAWLER_REMEDIATION_PLAN.md: NOT updated (read-only per
  operator). Deviations from the plan are captured here and in
  LESSONS.md only.

──────── Discoveries summary (production-extinction findings) ───

The probe-before-lock discipline surfaced a coherent pattern across
all 4 framework directories: **the audit's fixture specifications,
written May 2026, describe hydration patterns that the production
ecosystem has substantially or completely moved past in 2024-2026**.

| Framework | Marker spec'd by audit          | Hit rate (live probe) | Pivot              |
|-----------|----------------------------------|-----------------------|--------------------|
| Next.js   | `__NEXT_DATA__`                  | 1/6 (16%)             | Hybrid w/ App Router |
| Nuxt      | `window.__NUXT__` OR `__NUXT_DATA__` | 3/6 (50%, all Nuxt 3) | Nuxt 3 only       |
| Apollo    | `__APOLLO_STATE__`               | 1/13 (7.7%)           | 1 real + 1 synth   |
| Redux     | `__PRELOADED_STATE__`            | 0/12 (0%)             | 2 synth            |

Forward implication: AUDIT_REPORT.md Action #1 (hydration extraction)
will need to target App Router RSC streaming as a first-class
pattern, not just `__NEXT_DATA__`. The detector designed against
just the legacy markers would miss the dominant modern production
reality. The 10 fixtures from C1.1-C1.4 give the eventual Action #1
detector the full pattern surface to test against. Codified in
LESSONS.md "Probe framework generation before locking a fixture
spec" for forward-applicable use in C5+, C18+, C22+, and any future
framework-marker fixture work.

──────── Open items entering Week 3 ─────────────────────────────

Week 3 work per plan §3 (high-priority gap fixtures, "closes the
most damaging production-coverage gaps"):
- C5 (international): 3 fixtures (.de, .jp, .com.br) — revised
  per operator decision 2026-05-19 (was 6). Action #20 unblocked
  at ~85%.
- C18 (modern SaaS): 5 fixtures extending `legitimate_business/`
  with hreflang + canonical + JSON-LD Organization schema. Closes
  the 60-pp production-coverage gap.
- C22 (nonprofit expansion): 2-3 archetypal nonprofits extending
  `legitimate_nonprofit/` — Wikimedia, EducationalOrganization,
  philanthropy.
- C7 (mega-menu): 3 mega-menu fixtures with `aria-haspopup` +
  multi-column nested `<ul>`. Unblocks Action #13.

Total Week 3: 13-14 fixtures. Larger than Week 2's 11; consider
splitting across Sessions 8 + 9 at a natural breakpoint (e.g., C5
+ C22 in Session 8, C18 + C7 in Session 9), or proceed in one
session if Session 8 has the headroom.

All Week 3 captures must follow:
- LESSONS.md retry-on-TLS-error policy (≥3 attempts).
- LESSONS.md probe-before-lock discipline (verify the spec's
  marker still dominates production before sourcing — applies
  especially to C18's "hreflang + canonical + JSON-LD Organization"
  assumption: does modern SaaS marketing still ship JSON-LD
  Organization at the same rate the audit assumed?).
- LESSONS.md per-fixture commit discipline (C5.a, C5.b, C5.c,
  C18.a-e, etc.).

Week 5 punch list (17 failing fixtures from C0.9 + the 2 skipped
empty directories) remains untouched. Do NOT touch in Week 3.

Next session prompt: see SESSION_TRANSITION_TEMPLATE.md.
Next concrete work: choose Week 3 first action (C5.a recommended:
1× .de international B2B capture with hreflang alternates).

──────── Week 2 audit erratum (2026-05-20, post-close) ─────────

Operator requested a Week 2 quality double-check immediately
after the Session 7 close commit (workspace f41570b). The audit
verified all 10 fixtures parse to documented payload sizes, the
17 Week 5 punch list reds were unchanged, pre-push gates were
green, the plan was untouched, and the conformance test passed
all .claude/rules/ scans (no isinstance / dict.get / .items() /
global / import * / mutable-defaults / == None|True|False). Three
issues were surfaced:

1. **Cyclomatic complexity violation** (real, fixed):
   `_balanced_brace_json` in
   `tests/scraper/test_fixture_conformance.py` had McCabe
   complexity 11, exceeding the .claude/rules/code-quality.md
   "≤10 decision points → refactor" trigger (ruff C901:
   "11 > 10"). The C1.5 commit message (e5d2f91) claimed 8
   decision points — this was a measurement error. Pre-push gates
   missed it because the project's ruff `select = ["E", "F", "W",
   "I"]` (pyproject.toml) does not include "C" (mccabe).

   **Fix:** repo commit `b56df6e` (C1.5-followup) extracted the
   try/except into a new `_parse_json_slice(html, start, end)`
   helper. `_balanced_brace_json` now returns
   `_parse_json_slice(html, start, i)` on brace match. Complexity
   after refactor (verified by `ruff check --select C901`):
     _balanced_brace_json:  10  (was 11)
     _parse_json_slice:      2  (NEW)
   Tests + gates re-ran clean: 17 failed (Week 5 punch list,
   unchanged), 219 passed, 2 skipped.

2. **Fixture count off-by-one** (documentation, fixed inline):
   Actual fixture count is **10** (3 + 3 + 2 + 2), not 11. Wrong
   number appears in repo commit messages `a616555` (C1.4.b: "11
   hydration captures total") and `e5d2f91` (C1.5: "11 fixtures,
   C1.1-C1.4") — both immutable. Same error appeared in
   SESSION_LOG.md (2 places) and SESSION_TRANSITION_TEMPLATE.md
   (1 place); all three workspace occurrences corrected inline in
   this errata commit. The Session 7 commit table (11 rows above)
   is **correct** as a commit list — 10 fixture adds plus 1
   conformance test extension = 11 commits. The conflation was
   between commits and fixtures.

3. **Pre-push gate gap** (latent, deferred):
   The project's ruff `select` list does not include "C"
   (mccabe), so future cyclomatic-complexity violations will not
   be caught by pre-push. Adding C901 (and possibly all "C"
   selectors) to the project's ruff configuration would close
   this gap. Surfaced here but **not implemented in this
   erratum** — operator decision (2026-05-20) was to fix Issues
   1 + 2 only and flag Issue 3 separately for a future
   project-config commit.

Updated Session 7 repo commit count (post-erratum):
  12 commits total — the 11 in the table above plus
  `b56df6e` C1.5-followup. workstream-0-week2-end tag remains at
  `e5d2f91` (does not move; tags are append-only).

Updated repo head: b56df6e.

---

## Session 8 — Workstream 0 Week 3 partial (C5 + C22) (2026-05-20)

Scope: First half of Workstream 0 Week 3 per the operator-suggested
Session 8 / Session 9 split. Covers audit C5 (3 international-TLD
fixtures: .de, .jp, .com.br) and audit C22 (3 archetypal-nonprofit
fixtures). C18 modern SaaS + C7 mega-menu deferred to Session 9.

──────── Repo commits this session (`barcada-scraper`, all on `main`,
        all pushed to origin) ───────────────────────────────────

| #  | SHA       | Action  | Fixture / file                                         |
|----|-----------|---------|--------------------------------------------------------|
|  1 | `cc9c3b3` | C5.a    | international_business/de/siemens.de.html              |
|  2 | `d0f0f70` | C5.b    | international_business/jp/hitachi.co.jp.html           |
|  3 | `51d14f5` | C5.c    | international_business/br/locaweb.com.br.html          |
|  4 | `fbb0200` | C22.a   | legitimate_nonprofit/wikimediafoundation.org.html      |
|  5 | `273765e` | C22.b   | legitimate_nonprofit/doctorswithoutborders.org.html    |
|  6 | `79cf9a4` | C22.c   | legitimate_nonprofit/synthetic_educational_organization.html |
|  7 | `17e92f8` | C5.d    | tests/scraper/test_fixture_conformance.py extend       |

Repo head at session close: `17e92f8`.

──────── Per-action operator decisions made during Session 8 ─────

- **C5.a (.de)** — operator chose **siemens.de**. 6 candidates
  probed (sap.de blocked, siemens.de, bosch.de, trumpf.com/de_DE
  off-TLD, personio.de blocked, continental.com/de-de off-TLD).
  siemens.de wins on combination of real .de TLD, lang=de-DE,
  39 hreflangs, and parseable JSON-LD WebPage with nested
  Organization references. Trade-off: siemens.de uses regional
  English codes (en-us, en-gb) only — no bare `hreflang="en"`
  (the literal audit C11 example wording). Functionally
  equivalent for any detector that branches on
  `hreflang.startswith("en")`. C5.b (hitachi) later closed the
  bare-en gap.

- **C5.b (.jp)** — operator chose **hitachi.co.jp**. 6 candidates
  probed; hitachi.co.jp uniquely combines real .co.jp TLD,
  lang=ja-JP, 33 hreflangs **including the bare `hreflang="en"`
  form** the audit spec example referenced literally, and a
  parseable JSON-LD Organization + PostalAddress. NEC was 404,
  Rakuten was CDN-blocked.

- **C5.c (.com.br)** — operator chose **locaweb.com.br**. Two-
  round probe (12 candidates total): three .com.br banks /
  manufacturers (itau, bradesco, gerdau) returned anti-bot or WAF
  pages; the largest Brazilian-content sites (totvs.com, vale.com)
  use .com TLDs not .com.br. Second round surfaced three viable
  .com.br candidates (locaweb, petrobras, braskem). Locaweb won
  on archetype match ("Brazilian B2B" — private hosting/SaaS, not
  state-owned conglomerate or consumer telco) and richest JSON-LD
  coverage (3 blocks: FAQPage with 6 Question/Answer pairs +
  WebSite/SearchAction + Organization/PostalAddress/2x
  ContactPoint).

- **C22.a (Wikimedia)** — operator picked the audit's named
  candidate. wikimediafoundation.org as captured ships JSON-LD
  WebPage with nested Organization plus 5 multilingual hreflangs
  (ar-001, en-US, es-419, fr-FR, pt-BR). Auto-passes
  legitimate_nonprofit's existing inverted conformance test.

- **C22.b (philanthropy)** — operator picked the audit's named
  candidate. doctorswithoutborders.org as captured ships JSON-LD
  with 2x Organization + WebPage + BreadcrumbList, real
  humanitarian content (MSF x26, medical x15, donate x9), and an
  active "[URGENT] MSF responds to Middle East conflict" banner
  confirming the capture is current production content.

- **C22.c (EducationalOrganization)** — operator chose
  **synthetic-with-real-markers** per §11 fallback policy after
  probe-before-lock surfaced a production-extinction finding
  (next section). Synthetic "OpenLearning Initiative" authored
  with literal `@type=EducationalOrganization` schema + canonical
  nonprofit homepage structure (~9.2 KB). All PII safe (RFC 5733
  555-0100 phones, example.org emails, generic placeholder
  postal address).

──────── Discovery: @type=EducationalOrganization is extinct in
        2026 production (probe-before-lock, third occurrence) ─────

Production-extinction pattern confirmed for the third Schema.org
sub-type targeted by the May-2026 audit / plan. Probe of 9
educational candidates (khanacademy, mit, stanford, harvard, yale,
princeton, columbia, oxford, edx) found:

| Schema.org type           | Hits / 9 | Comment                          |
|---------------------------|---------:|----------------------------------|
| EducationalOrganization   |   0/9 (0%) | extinct                          |
| CollegeOrUniversity       |   0/9 (0%) | extinct                          |
| Organization (generic)    |   2/9 (22%) | Harvard + edX only               |
| No Schema.org markup      |   7/9 (78%) | dominant                         |

khanacademy was Akamai-bot-mitigation-gated. The
EducationalOrganization sub-type named by audit C22 / plan §3
Week 3 ("e.g., khanacademy.org") is no longer detectable in
production marketing surfaces.

Operator decision: synthetic-with-real-markers, mirroring C1.3.b
(Apollo legacy 7.7%) and C1.4.a/b (Redux SSR 0% extinct). The
detector under audit Action #20 + any future EducationalOrganization
branch has a known-positive sample to test against. Synthetic
flagged for quarterly re-capture review.

This is the **fourth** production-extinction finding surfaced by
probe-before-lock since Session 7 (after Next.js Pages Router,
Nuxt 2, Apollo SSR, Redux SSR). The pattern is now well-established
and applies forward to C18 modern SaaS work (Session 9).

──────── Discovery: synthetic-fixture HTML comments are themselves
        regex-visible (new lesson, codified in LESSONS.md) ────────

While verifying C22.c (synthetic_educational_organization.html),
extract_hard_exclusions returned exclusion_reason='waf_challenge'
on the synthetic — an unexpected red. Root cause: the synthetic's
HTML comment header (which documented the probe-before-lock
results) contained the phrase "khanacademy is Akamai-blocked" —
the substring "Akamai" + "blocked" on one line tripped the
`akamai.*blocked` branch of `_RE_WAF_CHALLENGE`. The parser regex
is flat on the full document and does not skip HTML comments.

Fixed in-place by rewording the comment to "khanacademy returns
an Akamai bot-mitigation interstitial" (same information, no
regex match). Verified by per-branch pattern sweep that no other
_RE_WAF_CHALLENGE, _RE_CLOUDFLARE_CHALLENGE, or _RE_GEO_BLOCK
branch matches.

Lesson codified in LESSONS.md under Diagnostic patterns:
**"Synthetic-fixture HTML comments are regex-visible — apply the
same anti-trip discipline to comment headers as to body content."**
Forward-applicable to all future synthetic-with-real-markers work
(C18 if Session 9 needs synthetic SaaS marketing fixtures;
C0.3-followup / C0.4-followup in Week 5; any synthetic capture
work in Workstream A.0+).

──────── Test surface change (repo) ─────────────────────────────

  test_hard_exclusions.py:        64 passed (unchanged)
  test_fixture_conformance.py:
    Pre-Session-8 (after b56df6e):  17 failed, 154 passed, 2 skipped
    Post-C22.c (before conformance commit): 18 failed, 157 passed,
        2 skipped (catch-all flipped to FAIL on first C5.a fixture
        adding the uncovered international_business dir; +3 passes
        from C22.a/b/c auto-joining the parametrized
        legitimate_nonprofit inverted detector)
    Post-Session-8 (after 17e92f8): 17 failed, 161 passed, 2 skipped
        (catch-all flipped back to PASS via COVERED update; +3
        passes from 3 new test_international_business_*
        conformance functions; punch list of 17 unchanged)

  Failure list at session close is EXACTLY the 17 Week-5 punch-list
  reds. Byte-for-byte diff verified at every commit point.

──────── Workspace updates this session ─────────────────────────

- SESSION_LOG.md: this entry (this commit).
- LESSONS.md: new "Synthetic-fixture HTML comments are regex-
  visible" entry under Diagnostic patterns (this commit).
- SESSION_TRANSITION_TEMPLATE.md: refilled for Session 9 (C18
  modern SaaS + C7 mega-menu — second half of Week 3).
- BARCADA_CRAWLER_REMEDIATION_PLAN.md: NOT updated (read-only per
  operator).

──────── Cost & schedule tracking ───────────────────────────────

- Cost incurred Sessions 1-8: $0 (no LLM API calls; curl + pytest
  + handwritten synthetic only). Cost ceiling $100 untouched.
- Schedule: 3 weeks elapsed of Workstream 0's 5-week budget.
  Weeks 1-2 complete; Week 3 ~60% complete (C5 + C22 = 7 of 7
  Session-8-scoped commits, ~6 of ~14 Week-3 fixtures shipped).
  Weeks 3 (remainder, Session 9) - 5 still ahead.

──────── Operator-interaction note (Session 8 pattern) ──────────

During this session the operator repeatedly asked "did you double
check your work?" before each commit confirmation (C5.a, C5.b,
later commits implicitly). The discipline established:
verification table must be generated from the on-disk fixture by
re-parsing it BEFORE drafting the commit message, not after. Two
precision errors caught in the C5.a draft as a result (false
`hreflang="en"` claim, misleading "4 JSON-LD sibling types"
wording when in fact 1 block with 4 nested types). For all
subsequent commits, full verification (file properties + extracted
JSON-LD + extract_hard_exclusions + per-branch detector sweep +
gates + punch-list diff + hard_exclusions regression check) was
done up-front. Documented behavior; no LESSONS.md entry needed
(the rule is already in CLAUDE.md and code-quality.md).

──────── Open items entering Session 9 ──────────────────────────

Week 3 remaining (Session 9 scope):
- C18 (modern SaaS): 5 fixtures extending legitimate_business/
  with hreflang + canonical + JSON-LD Organization + mega-menu.
  **Apply probe-before-lock discipline up-front**: based on the
  4 prior production-extinction findings (Next.js, Nuxt, Apollo,
  Redux, EducationalOrganization), verify JSON-LD Organization
  prevalence in modern SaaS marketing (Stripe, Notion, Linear,
  Vercel, HubSpot, Webflow) before sourcing candidates. If
  prevalence <50%, escalate spec revision rather than locking
  the fixture set against a near-extinct marker.
- C7 (mega-menu): 3 fixtures into new mega_menu/ with
  aria-haspopup + multi-column nested <ul> panels.
- Total Session 9: 8 fixtures + 1 conformance test extension
  (legitimate_business already covered; mega_menu adds new
  COVERED entry + conformance function).

Week 5 punch list (17 fixtures) remains untouched — tracked
intentional reds, scheduled for Week 5.

Pre-push gate gap (Issue 3 from the Week 2 audit erratum)
remains open: project's ruff `select` does not include "C"
(mccabe), so cyclomatic-complexity violations are caught only
by manual `ruff check --select C901` (which Session 8's
conformance commit did manually). Tracked for a future
project-config commit.

Next session prompt: see SESSION_TRANSITION_TEMPLATE.md.
Next concrete work: C18 prevalence probe (4-6 modern SaaS
marketing candidates) before sourcing any C18.a fixture.

## Session 9 — Workstream 0 Week 3 close (C18 + C7) (2026-05-20)

Scope: Second half of Workstream 0 Week 3. Closes the C18 modern-SaaS
candidate (5 fixtures, hybrid 3+2 spec per Path A operator decision)
and the C7 mega-menu candidate (3 fixtures, Path C marker spec). Adds
the Week-3-close conformance test extension for mega_menu. Tag
`workstream-0-week3-end` lands at `cf0c14c`.

──────── Repo commits this session (`barcada-scraper`, all on `main`,
        all pushed to origin) ───────────────────────────────────

|  # | SHA       | Action  | Fixture / file                                                       |
|---:|-----------|---------|----------------------------------------------------------------------|
|  1 | `e3ef6b7` | C18.a   | legitimate_business/twilio.com.html                                  |
|  2 | `6c4a7f3` | C18.b   | legitimate_business/hubspot.com.html                                 |
|  3 | `0c7dc65` | C18.c   | legitimate_business/webflow.com.html                                 |
|  4 | `c67fc71` | C18.d   | legitimate_business/notion.so.html                                   |
|  5 | `70d5190` | C18.e   | legitimate_business/snowflake.com.html                               |
|  6 | `659f32d` | C7.a    | mega_menu/shopify.com.html (new directory)                           |
|  7 | `0e4cb10` | C7.b    | mega_menu/salesforce.com.html                                        |
|  8 | `ef91cb2` | C7.c    | mega_menu/synthetic_microsoft_style_aria_controls.html               |
|  9 | `cf0c14c` | C7.d    | tests/scraper/test_fixture_conformance.py extend (mega_menu COVERED) |

Repo head at session close: `cf0c14c`.
Tag `workstream-0-week3-end` created at `cf0c14c` (annotated).

──────── Workspace commits this session (`crawler-audit`) ────────

| # | SHA       | Scope                                                                                |
|--:|-----------|--------------------------------------------------------------------------------------|
| 1 | `3e55a3d` | LESSONS.md: detector precision FPs surfaced by C18.0 (FP 1 dd.js, FP 2 just-a-moment) |
| 2 | `081b54e` | LESSONS.md: C7 mega-menu drift + snowflake FP 3 + B/C ownership flag                  |
| 3 | (this commit) | Session 9 close: LESSONS.md amendments (3 staged findings) + SESSION_LOG.md + SESSION_TRANSITION_TEMPLATE.md refill |

──────── Per-action operator decisions made during Session 9 ─────

- **Path A (C18 hybrid spec)** — operator selected 3+2 hybrid
  (3 structured-data-rich + 2 modern-minimal) over Paths B/C
  after C18.0 prevalence probe surfaced 67% jsonld_org prevalence
  (above the 50% extinction threshold). Recommended candidates:
  stripe.com + hubspot.com + webflow.com (structured-data-rich) +
  notion.so + linear.app (modern-minimal).

- **C18 substitute candidates after verify-before-asking FP
  catches** — stripe.com tripped `_RE_WAF_CHALLENGE` via the
  `dd.js` alternation (false positive on Next.js webpack chunk
  filename); linear.app tripped `_RE_CLOUDFLARE_CHALLENGE` via the
  `just\s+a\s+moment` alternation (false positive on body marketing
  copy "Launching is just a moment in time"). Operator approved
  substituting twilio.com for stripe.com and snowflake.com for
  linear.app. LESSONS.md "Detector precision findings" entry
  (3e55a3d) captures both FPs with concrete byte offsets.

- **Path C (C7 mega-menu spec relaxation)** — operator selected
  Path C (operator-spec at Session-9 mid-point): the conformance
  test accepts either (a) aria-haspopup with any non-false value
  OR (b) aria-expanded + aria-controls cross-reference pattern.
  Density thresholds deferred to Week 4 with expected-outputs
  work per the Validation Strength Gradient. Audit's literal
  `aria-haspopup="menu"` example value was illustrative-of-
  archetype, not binding. LESSONS.md "Audit-spec vs. production-
  reality drift" entry (081b54e) captures the drift.

- **Path B (C7.c synthetic-with-real-markers)** — operator
  selected Path B after 5 real-domain candidates failed in 5
  distinct ways during the C7.c substitute round (Microsoft anti-
  bot CMS interstitial; GitHub `dd.js` FP — 4th instance of the
  same logged bug; Adobe HTTP/2 INTERNAL_ERROR; IBM marker-spec
  miss; Oracle fw_error_www edge-stub). Synthetic
  `synthetic_microsoft_style_aria_controls.html` authored with
  enterprise-realistic marker density (10× aria-expanded + 10×
  aria-controls, 10 distinct target IDs).

──────── Discoveries surfaced this session ───────────────────────

**Four production-precision findings**, all expanding on prior
patterns:

1. **Three detector FPs catch contaminated fixture candidates.**
   FP 1 (`dd.js`) tripped 4 of 12 modern enterprise/SaaS sites
   (33% — Stripe, Raycast, PostHog, GitHub). FP 2 (`just a moment`)
   tripped 1 of 11 (Linear). FP 3 (`_RE_SOFT_404` greedy span
   between `search` and `no results found` anchors) tripped 1 of
   16 (Snowflake — different category: matches but is correctly
   suppressed by parser downstream guards). Resolution: drop the
   FP-tripping candidates from C18; document for the eventual
   Workstream B-or-C precision audit.

2. **Three false-negative anti-bot patterns silent to detectors.**
   Microsoft's "Your request has been blocked" CMS interstitial
   (HTTP 200 + block-page body); Adobe's HTTP/2 INTERNAL_ERROR
   (TCP/HTTP2-layer refusal, no body); Oracle's 1,450-byte
   fw_error_www edge-stub. None match any of the 15 existing
   detector branches. Verify-before-asking title-sanity check
   was the cheapest distinguishing signal for FN 1.

3. **Audit-spec vs. production-reality drift on C7 ARIA markers
   (Week 3 occurrence; Next.js App Router was Week 2's instance).**
   `aria-haspopup="menu"` literal value absent in 0/3 audit-named
   candidates; Shopify/Salesforce ship `"true"` (WAI-ARIA 1.1+
   shorthand); Microsoft uses aria-expanded+aria-controls only.
   Two drift findings in two weeks suggests audit HTML examples are
   ~18+ months stale on frontend patterns.

4. **Enterprise aria-controls archetype is structurally
   concentrated in heavily-defended sites.** 5/5 enterprise
   substitute candidates (Microsoft, GitHub, Adobe, IBM, Oracle)
   failed in 5 distinct ways during C7.c sourcing — 100% real-
   capture failure rate on enterprise targets. Synthetic-with-real-
   markers per §11 fallback was the resolution.

The deeper meta-finding: verify-before-asking has now surfaced
spec/reality mismatches in **three consecutive weeks** (Week 2
Next.js App Router; Week 3 detector FPs + C7 ARIA markers; Week 3
anti-bot FNs). That's a rate, not a fluke. Open meta-question
flagged for Week 3 retrospective: should verify-before-asking be
promoted from ad-hoc discipline to a named Workstream 0
acceptance criterion alongside the 1:1:1 success metrics? Not
actioned in Session 9; carried into Session 10 transition template.

──────── Test surface change (repo) ─────────────────────────────

  test_hard_exclusions.py:        64 passed (unchanged across
                                  Session 9; same baseline as
                                  Session 8 close)
  test_fixture_conformance.py:
    Pre-Session-9 (17e92f8):       17 failed, 161 passed, 2 skipped
    Through C18.a-e (70d5190):     17 failed, 166 passed, 2 skipped
                                   (+5 passes from C18.a-e auto-
                                    joining the parametrized
                                    test_legitimate_business_conformance)
    After C7.a (659f32d):          18 failed, 165 passed, 2 skipped
                                   (catch-all flipped to FAIL on
                                    `['mega_menu']` not in COVERED;
                                    -1 from pass→fail movement)
    Through C7.b/c (ef91cb2):      18 failed, 165 passed, 2 skipped
                                   (no test added by new fixtures;
                                    catch-all still failing)
    After C7.d (cf0c14c):          17 failed, 169 passed, 2 skipped
                                   (catch-all back to PASS via
                                    COVERED update; +3 new
                                    test_mega_menu_conformance
                                    parametrize IDs all pass)

  Failure list at session close is EXACTLY the 17 Week-5 punch-
  list reds. Byte-for-byte diff verified at every commit point.

──────── Workspace updates this session ─────────────────────────

- LESSONS.md commit 1 (3e55a3d, mid-C18.0): new section
  "## Detector precision findings" with FPs 1 and 2 + the
  circularity meta-observation + forward-applicable actions.
- LESSONS.md commit 2 (081b54e, between C18.e and C7.a): C7
  audit-spec drift + snowflake FP 3 (the matches-but-suppressed
  flavor) + Workstream-B-or-C ownership ambiguity flag in the
  forward-action list.
- LESSONS.md commit 3 (this commit, Session 9 close): the three
  staged findings from the C7.c commit message body — GitHub
  joining the dd.js FP table, new sub-section "False-negative
  coverage gaps for anti-bot interstitials" (FNs 1/2/3), and the
  append to the audit-spec-drift entry capturing the enterprise-
  concentration finding.
- SESSION_LOG.md: this entry.
- SESSION_TRANSITION_TEMPLATE.md: refilled for Session 10
  (Workstream 0 Week 4 — provenance / expected outputs).
- BARCADA_CRAWLER_REMEDIATION_PLAN.md: NOT updated (read-only
  per operator).

──────── Cost & schedule tracking ───────────────────────────────

- Cost incurred Sessions 1-9: $0 (no LLM API calls in the work
  itself — all probes via curl with retry policy, all verification
  via pytest + handwritten Python, the C7.c synthetic
  handwritten). Cost ceiling $100 untouched.
- Schedule: 3 weeks elapsed of Workstream 0's 5-week budget.
  Weeks 1-3 COMPLETE; Weeks 4-5 still ahead.
  - Week 3 total: 14 fixtures + 2 conformance extensions = 16
    commits across Sessions 8 + 9 (7 in S8, 9 in S9).
  - Tag `workstream-0-week3-end` annotated at `cf0c14c`.

──────── Operator-interaction notes (Session 9 patterns) ────────

- "Did you double check your work?" asked **four times** during
  Session 9 (after C18.a draft, after C18.b draft, after C7.a
  draft, after C7.c draft, after C7.d draft — actually five
  times). Each time surfaced 2-3 real gaps in the verification
  table the assistant had drafted: SHA fabrication (C7.c),
  full block dump vs True-flag-only filter (C18.b), comment-text
  trip on the Path-C marker A regex (C7.c synthetic — fixed
  before commit), missing parametrize-collection check (C18.b),
  missing post-format re-read (C7.d), missing direct-helper-call
  verification (C7.d), missing negative-case coverage (C7.d).
  Each iteration tightened the verification standard. The
  operator's "did you double check" question functions as a
  ratchet: forcing one more inspection layer before each
  commit confirm.

- Two Step 6 escalations executed cleanly:
    - C18.0 / C18.a-e: stripe + linear FPs surfaced before
      sourcing the C18 set → Path A (substitute) approved.
    - C7.c: 5/5 enterprise substitute failures surfaced → Path B
      (synthetic) approved.
  Both escalations preserved the audit's intent (3+2 hybrid for
  C18, 3 archetypes for C7) while adapting the specific
  candidates to production reality.

──────── Open items entering Session 10 ──────────────────────────

Workstream 0 Week 4 (provenance + expected outputs):
- Per-fixture `meta.json` (source_url, captured_at,
  capture_method, content_type, content_length, encoding,
  response_status, expected_outcome, test_purpose).
- Per-fixture `expected/<domain>.json` (parser_output,
  barriers_verdict, stage1/2/3 decisions). Generate once,
  human-review, commit. Subsequent test runs compare against
  these.
- Plan §3 Week 4 budget notes $50-200 LLM cost during this
  workstream for expected-output generation. First substantial
  cost expenditure of the remediation.
- 197-ish current fixture corpus needs meta.json + expected
  outputs each → ~400+ new files in tests/fixtures/html/.

Open meta-question flagged for Week 3 retrospective:
- Promote verify-before-asking from ad-hoc discipline to a
  named Workstream 0 acceptance criterion? 3 weeks of evidence
  (3 distinct spec/reality mismatch findings) suggests yes;
  operator decision deferred.
- Three LESSONS.md sub-sections now anchor the discipline:
  "Probe framework generation before locking a fixture spec"
  (S7), "Synthetic-fixture HTML comments are regex-visible"
  (S8), "Detector precision findings" with FPs and FNs (S9).
  All cite verify-before-asking implicitly or explicitly.
- A promotion would land as either a plan §3 acceptance-
  criteria addition (plan is read-only; would need a new
  document) or as a CLAUDE.md / .claude/rules/ codification.
  Decision shape deferred to operator at Week 3 retro.

Pre-push gate gap (Issue 3 from the Week 2 audit erratum)
remains open: project's ruff `select` does not include "C"
(mccabe), so cyclomatic-complexity violations are caught only
by manual `ruff check --select C901`. Session 9's C7.d
conformance commit did this manually. Tracked for a future
project-config commit.

Week 5 punch list (17 fixtures) remains untouched — tracked
intentional reds, scheduled for Week 5.

Next session prompt: see SESSION_TRANSITION_TEMPLATE.md.
Next concrete work: Workstream 0 Week 4 — meta.json schema
locked, per-fixture meta.json generation across the corpus
(~197 fixtures), expected-outputs generation (this is where
the $50-200 LLM cost lands).

---

## Session 10 — Carried-item resolution + W4.0 schema lock (2026-05-20)

Scope: Open Workstream 0 Week 4 with the three carried items from
Session 9 close (Flag 1 cost ceiling, Flag 2 verify-before-asking
promotion, Flag 3 W4 tag provenance). Land the W4.0 meta.json +
expected.json schema lock plus a worked-example pair (twilio.com)
per plan §3 Week 4. No workstream-0-week4-end tag at session close
(W4 spans multiple sessions; tag lands at full W4 close).

──────── Repo commits this session (`barcada-scraper`, both on
        `main`, both pushed to origin) ──────────────────────────────

| # | SHA       | Action                  | Files                                                                                              |
|--:|-----------|-------------------------|----------------------------------------------------------------------------------------------------|
| 1 | `9165791` | W4.0-schema-lock        | tests/fixtures/META_SCHEMA.md + tests/fixtures/meta.schema.json + tests/fixtures/expected.schema.json |
| 2 | `8aafc45` | W4.0-worked-example-twilio | tests/fixtures/html/legitimate_business/twilio.com.meta.json + tests/fixtures/html/legitimate_business/expected/twilio.com.json |

Repo head at session close: `8aafc45`.

──────── Workspace commits this session (`crawler-audit`) ────────

| # | SHA       | Scope |
|--:|-----------|-------|
| 1 | (this commit) | Session 10 close: SESSION_LOG.md Session 10 append + LESSONS.md "Verify-before-asking discipline" section (Flag 2 resolution constraints — header naming + operator-ratchet + A/B/C trigger) + SESSION_TRANSITION_TEMPLATE.md refill for Session 11 |

──────── Flag 1 (cost ceiling reconciliation): RESOLVED →
        Option (c), defer Stage 3 LLM calls ────────────────────────

Selected sub-option (c): expected-output generation defers Stage 3
LLM calls and generates only Stage 1/2 expected outputs in W4. Stage
3 expected-output generation lands in Workstream C scope.

Reasoning: (i) the asymmetric-baseline con for option (c) was weaker
than initially framed — plan §6 lines 313-385 was read in full and
confirmed Workstream B's expected-output regeneration needs are
Stage 1-specific (Action #6 cost-per-useful-record) and
stage-agnostic (Action #21 version stamping); the only Workstream B
item touching Stage 3 is LLM_OVERUSE in Action #7, which is new
flag emission rather than a change to Stage 3 decision logic. (ii)
The Stage 3 baseline gap becomes load-bearing in Workstream C
(Weeks 13-16) per §7, where extraction work substantially changes
Stage 3 inputs and "trust the baseline" matters most. Option (c)
explicitly aligns Stage 3 regeneration with Workstream C ownership.
(iii) Option (a) doubles operator's prior spend authorization on
an unvalidated $50-200 estimate (current spend $0); option (b) adds
W4.2 engineering scope the plan didn't budget and introduces
schema-shape risk from Haiku-tier abstain divergence from production
cascade.

Four execution constraints (carried forward; verbatim per operator
Flag 1 resolution):

1. **W4.0 schema lock must explicitly accommodate deferred Stage 3
   fields.** Two sub-options presented at W4.0 schema review: (i)
   include `stage3_decision` field with explicit
   `"deferred_to_workstream_c"` sentinel value, OR (ii) omit
   `stage3_decision` from schema v1.0 with documented note that
   schema v1.1 (Workstream C) will add it. Operator selected (i) at
   W4.0 review (this session).

2. **W4 close documentation must be explicit.** SESSION_LOG.md
   Session 10 close + the eventual workstream-0-week4-end tag
   annotation must state: "Stage 3 expected-outputs deferred to
   Workstream C per Flag 1 resolution; partial coverage at W4 close
   is intentional, not incomplete." (This entry satisfies the
   SESSION_LOG.md portion. The tag annotation lands at full W4
   close.)

3. **Workstream C scope amendment flagged for operator
   authorization.** Deferred Stage 3 expected-output generation lands
   in Workstream C scope. That's a plan-document amendment — read-
   only territory, operator authorization required. Staged in the
   W4.0 schema-lock commit message (9165791) and the worked-example
   commit message (8aafc45) for operator handling. Plan document NOT
   amended by assistant.

4. **Cost ceiling remains $100, alert at $50.** Option (c) is
   expected to keep W4.2 spend at near-zero (RULES + LR routing for
   the corpus majority, LLM only at Stage 1/2 abstain tail). No
   ceiling change needed. If actual W4.2 spend trends higher than
   near-zero during execution, stop and escalate before crossing $50
   alert threshold.

Additional Flag 1 sub-options surfaced at W4.0 schema review:

- **Constraint #1 sub-options (i)/(ii)**: operator selected (i) —
  include stage3_decision field with sentinel.
- **Constraint #5 sentinel semantic**: operator selected semantic
  (α) — comparison-skip directive. Workstream A.0 baseline-v0
  comparison logic treats `"deferred_to_workstream_c"` as
  comparison-skip directive; sentinel string to be codified as a
  named constant in baseline-v0 implementation, not a magic-string
  scattered through files.

──────── Flag 2 (verify-before-asking promotion): RESOLVED →
        Option (c), status quo ────────────────────────────────────

Selected sub-option (c): status quo. Keep verify-before-asking
discipline anchored in LESSONS.md only; rely on plan §14 required-
reading discipline + operator-ratchet to propagate it. No new
sibling document (option a rejected). No CLAUDE.md edit or
.claude/rules/ addition (option b rejected).

Five-bullet reasoning (verbatim per operator Flag 2 resolution):

1. Three LESSONS.md sub-sections already anchor the discipline (S7
   probe-framework-generation at lines 186-227, S8 synthetic-HTML-
   comments at lines 423-465, S9 detector-precision-findings at
   lines 467-696).

2. Template §14 already lists LESSONS.md in required reading
   (template lines 273-274) — propagation mechanism exists, no new
   infrastructure needed.

3. Three weeks of evidence are all from Workstream-0 fixture-
   sourcing context; promoting to acceptance-criterion or code-rule
   tier before forward-context evidence (Workstream B detector-
   precision audit, Workstream C extraction work) would codify a
   discipline that may need refinement when applied to different
   work shapes.

4. Operator-driven ratchet ("did you double check your work?")
   remains the enforcement mechanism. Not gated.

5. Options (a) and (b) carried structural risks that weighed against
   promotion at this evidence stage: option (a) would establish
   "operator-discipline items can become sibling plans" as a
   precedent, eroding the read-only-period boundary on
   BARCADA_CRAWLER_REMEDIATION_PLAN.md established at S7 turn 12;
   option (b) had unverified loading reliability in the workspace
   context (crawler-audit/ CLAUDE.md state was Session-10-inference,
   no direct source), and a verification discipline that itself
   loads unreliably is self-defeating. Option (c) preserves
   optionality: if verify-before-asking produces a finding in
   Workstream A, B, or C, the promotion question reopens with
   broader evidence base.

Four execution constraints on Option (c) (landed this commit as
LESSONS.md additions):

1. **LESSONS.md anchor reinforcement** — new header entry naming
   "verify-before-asking" as the discipline and cross-referencing the
   three sub-sections (S7, S8, S9) as evidence.
2. **Operator-ratchet pattern documentation** — entry naming "did
   you double check" question as the propagation mechanism under
   option (c).
3. **Workstream A/B/C trigger condition** — entry documenting the
   trigger: if verify-before-asking produces a finding in Workstream
   A, B, or C, the promotion question reopens with broader evidence
   base. Not a commitment to promote — just a trigger to revisit.
4. **No new sibling document, no CLAUDE.md edit, no .claude/rules/
   addition.** Status quo means status quo.

──────── Flag 3 (W4 tag provenance): FLAGGED, not blocker ──────────

Flag 3 was surfaced at Session 10 open per operator instruction;
acknowledged as proceed-anyway. No action this session. Revisit at
full W4 close.

──────── W4.0 schema design and lock ─────────────────────────────

Single-unit engineering work: drafted META_SCHEMA.md + meta.schema.json
+ expected.schema.json + worked-example pair as a batch for operator
review. Two operator corrections applied to the draft mid-review:

- **Correction A**: sub-option (i) pro overclaimed Flag 1 constraint
  #2 ("automatically satisfied by in-data sentinel"). Workstream-
  level deferred-by-design documentation still applies independently
  of per-fixture sentinel. Corrected in the schema spec rationale.

- **Correction B**: `schema_version: const "1.0"` blocked the
  independent versioning the rationale claimed (any v1.x bump would
  fail const validation). Two fix options presented: replace const
  with pattern OR rename to scope-specific fields. Operator selected
  pattern fix: `{"type": "string", "pattern": "^1\\.[0-9]+$"}` on
  both meta.schema.json and expected.schema.json. Preserves field
  name, eval_data/stage1.schema.json precedent (semver string), and
  symmetry across both schemas; allows independent v1.x progression.

Batch resolutions on review items #1-#8 (all approved or resolved):

1. File location & shape: 3 files — META_SCHEMA.md + meta.schema.json
   + expected.schema.json under tests/fixtures/. APPROVED.
2. expected_outcome shape: structured JSON object, deviates from plan
   §3 W4 free-text example. APPROVED, deviation documented.
3. stage3_decision handling: sub-option (i) — include with sentinel.
4. Sentinel semantic for baseline-v0: semantic (α) — comparison-skip
   directive. Sentinel string to be codified as named constant in
   Workstream A.0 baseline-v0 implementation.
5. Empty-directory handling: no stub files; META_SCHEMA.md "Pending
   directories" section pointer. APPROVED.
6. capture_method enum: DROP `playwright` (no Session 5-9 capture
   used it; reserve via semver bump for future SPA hydration work).
7. Anti-trip discipline scope: VERIFIED regex-isolated. meta.json is
   not flat-scanned by extract_hard_exclusions; _iter_fixtures globs
   `*.html` only. Anti-trip discipline codified as future-proofing-
   only per operator instruction.
8. `historical_unverified` capture_method: APPROVED as catch-all for
   pre-Session-1 fixtures + any other corpus fixtures whose origin
   isn't recoverable.

Two corpus-wide truths landed in META_SCHEMA.md (§5 Historical
capture limitations):

- **Truth 1 (source_url)**: original capture URL not preserved by
  `curl -o`. For historical captures (W3 and earlier, ~196 of 198
  fixtures), accept `<link rel="canonical">` URL as source_url
  proxy; fall back to bare-domain form when no canonical. Forward
  W5+ captures: extend tooling to preserve actual URL via
  `curl -w "%{url_effective}"` — flagged as **Workstream A.12
  tooling item, NOT W4 scope**.
- **Truth 2 (content_type, encoding, response_status)**: response
  headers not preserved for historical captures. Use plan §3 W4
  defaults (`"text/html; charset=utf-8"`, `"utf-8"`); derive
  response_status from directory category. Mark approximated fields
  with `provenance_note`.

`provenance_note` field added to meta.schema.json: optional object
keyed by approximated-field-name with string value naming the
approximation source. Operator confirmed structured-object
interpretation (per-field granularity preserved across ~196
historical-capture fixtures) over flat-string single-field form.

Item #7 verification result (verbatim, for record):
- `tests/scraper/test_fixture_conformance.py:30-38`: `_iter_fixtures(category)`
  returns `sorted((FIXTURES / category).glob("*.html"))`. Strict .html
  filter; .meta.json files not enumerated.
- `tests/scraper/test_fixture_conformance.py:50`: only path passed to
  `extract_hard_exclusions` is `path.read_text(encoding="utf-8")`
  from the .html path.
- All other `extract_hard_exclusions` call sites (crawler.py:629,
  test_hard_exclusions.py) take HTML bodies.
- No `meta.json` references in src/ or tests/ that touch fixture
  metadata.

──────── Pattern distinction (single-line note per operator request) ─

Carried-item resolution (Flag 1, Flag 2) used pre-staged options
from SESSION_TRANSITION_TEMPLATE.md with Session-10-authored
pros/cons grounded in source files — operator-authority decisions
routed through batch review of three discrete option sets.
Engineering design (W4.0 schema spec + worked example) used single-
unit drafting with recommended approaches, source-cited tradeoffs,
and batch review at completion — operator review at the artifact
level, not the per-decision level.

──────── Test surface change (repo) ─────────────────────────────

  test_hard_exclusions.py:        64 passed (unchanged across
                                  Session 10; same baseline as
                                  Session 9 close).
  test_fixture_conformance.py:
    Pre-Session-10 (cf0c14c):     17 failed, 169 passed, 2 skipped
    Post-Commit-1 (9165791):      17 failed, 169 passed, 2 skipped
                                  (.md + 2 .schema.json files;
                                   _iter_fixtures globs *.html only,
                                   no test surface change)
    Post-Commit-2 (8aafc45):      17 failed, 169 passed, 2 skipped
                                  (.meta.json + expected/*.json
                                   files; same invisibility from
                                   _iter_fixtures)

  Failure list at session close is EXACTLY the 17 Week-5 punch-list
  reds. Byte-for-byte stable across both commits.

──────── Workspace updates this session ─────────────────────────

- SESSION_LOG.md: this entry.
- LESSONS.md: new "## Verify-before-asking discipline" section with
  three sub-entries (anchor + operator-ratchet + A/B/C trigger) per
  Flag 2 Option (c) execution constraints.
- SESSION_TRANSITION_TEMPLATE.md: refilled for Session 11
  (Workstream 0 Week 4 continuation — W4.1 bulk meta.json generation
  next).
- BARCADA_CRAWLER_REMEDIATION_PLAN.md: NOT updated (read-only per
  operator). Workstream C scope amendment (deferred Stage 3 expected-
  output generation) flagged in commit messages for operator
  handling, not assistant-amended.

──────── Cost & schedule tracking ───────────────────────────────

- Cost incurred Sessions 1-10: $0. No LLM API calls in Session 10
  itself (schema design + drafting + manual verification + curl +
  grep + pytest). Cost ceiling $100 untouched. Budget remaining:
  $100.
- Schedule: 3 weeks elapsed of Workstream 0's 5-week budget. Weeks
  1-3 COMPLETE; Week 4 OPEN (~25% complete with W4.0 schema lock
  done; W4.1 bulk generation + W4.2 expected-output generation
  pending). Weeks 4-5 still ahead.
- W4 likely spans 2-3 sessions per template line 129; Session 10
  closes the schema-lock unit at the natural seam.

──────── Operator-interaction notes (Session 10 patterns) ───────

- "Did you double check your work?" not explicitly asked this
  session — verify-before-asking discipline was applied proactively
  before each commit confirmation (verification table generated
  pre-confirm, anti-trip scan on test_purpose, content_length
  bit-exact match check, source_url ↔ canonical-link exact match
  check, captured_at ↔ git author date conversion check). Operator-
  ratchet did not need to fire because the proactive verification
  caught what the ratchet would have caught.

- Two Step 6 escalations executed cleanly:
  - Pros/cons-not-staged drift on Flag 1 (and again on Flag 2) →
    surfaced before authoring, operator authorized author-with-
    provenance pattern.
  - Item #7 verification surfaced regex-isolation cleanly →
    proceeded under future-proofing interpretation per operator
    pre-conditional.

- Two corrections applied to the schema draft mid-review (Correction
  A and Correction B). Both surfaced by operator review, not by
  assistant self-review. Pattern: assistant's verify-before-asking
  catches mechanical errors (file paths, byte counts, regex trips);
  operator review catches semantic errors (overclaim of constraint
  satisfaction, const-vs-pattern semantics). Different verification
  layers catch different failure modes.

──────── Open items entering Session 11 ─────────────────────────

Workstream 0 Week 4 continuation:

- **W4.1 bulk meta.json generation across the corpus** (next concrete
  work unit). 198 fixtures need meta.json files. Per W4.0 schema +
  Truth 1/2: scripted generation reading each fixture's .html,
  extracting content_length via os.path.getsize(), deriving
  captured_at via git log --diff-filter=A --follow --format=%aI,
  source_url from `<link rel="canonical">` with bare-domain fallback,
  capture_method per session-log mapping (W0 Sessions 5+ are
  curl_with_retries; pre-Session-1 are historical_unverified;
  synthetic-with-real-markers fixtures identifiable by filename
  prefix), content_type and encoding from plan default, response_status
  from directory-category mapping. Operator review of script output
  before bulk commit.

- **W4.2 expected/<domain>.json generation** (Stage 1/2 only per
  Flag 1 resolution; Stage 3 via canonical sentinel triple).
  Expected near-zero LLM cost (RULES + LR for the corpus majority).
  Stop and escalate if actual spend trends higher than near-zero
  before $50 alert threshold.

- **W4.3 Test infrastructure** (may span into Session 12). Update
  conformance tests to compare against expected/<domain>.json
  (replacing the current "exclusion_reason must be empty" style
  assertions with full comparison). May or may not be Week 4 vs
  Week 5 work depending on operator preference.

- **W4 close + tag annotation**. At full W4 close, tag
  `workstream-0-week4-end` at the final green-gate SHA. Annotation
  must state: "Stage 3 expected-outputs deferred to Workstream C
  per Flag 1 resolution; partial coverage at W4 close is intentional,
  not incomplete." (Per Flag 1 constraint #2.)

- **Workstream C scope amendment** flagged for operator authorization.
  Pending operator handling outside session work.

Carried items status:

- Flag 1 (cost ceiling reconciliation): RESOLVED Session 10 →
  Option (c) defer Stage 3 to Workstream C.
- Flag 2 (verify-before-asking promotion): RESOLVED Session 10 →
  Option (c) status quo. Trigger condition documented in LESSONS.md
  for forward reopening.
- Flag 3 (W4 tag provenance): still flagged, not a blocker. Revisit
  at full W4 close.

Pre-push gate gap (Issue 3 from the Week 2 audit erratum) remains
open: project's ruff `select` does not include "C" (mccabe), so
cyclomatic-complexity violations are caught only by manual
`ruff check --select C901`. Tracked for a future project-config
commit.

Week 5 punch list (17 fixtures) remains untouched — tracked
intentional reds, scheduled for Week 5.

Next session prompt: see SESSION_TRANSITION_TEMPLATE.md.
Next concrete work: Workstream 0 W4.1 — bulk meta.json generation
across the 198-fixture corpus per the META_SCHEMA v1.0 lock landed
this session.

---

## Session 11 — W4.1 bulk meta.json generation (2026-05-20)

Scope: Open Workstream 0 Week 4 continuation. Draft and run the bulk-
generation script per W4.0 schema + Truth 1/2 field-derivation
recipes; sample-review → bulk commit cadence per plan §3 W4 deliverable
guidance. Pre-script verification surfaced one divergence between the
documented recipe and repo reality (see below); operator authorized
path-A correction landing in SESSION_TRANSITION_TEMPLATE.md +
SESSION_LOG.md without semver-bumping META_SCHEMA.md prose.

──────── Pre-script verification finding (path-A correction landed) ─

Cross-check of `response_status` field-derivation recipe (Session-10
SESSION_TRANSITION_TEMPLATE.md lines 124-131 + META_SCHEMA.md §2.4
line 95 + META_SCHEMA.md §5 line 149) against commit `4f8dc06` (C0.7c,
2026-05-19, Session 5/6 boundary) revealed an audit-spec-vs-production
drift (LESSONS.md §S9 pattern):

- **Documented recipe**: "401 for the 4 nginx-401 fixtures moved
  INTO `parking_default_pages/` by C0.7c". Implied directory split
  inside `parking_default_pages/`.
- **C0.7c commit reality**: commit message reads "batch-move 4
  nginx-401 files FROM `parking_default_pages/` TO `auth_403/`".
  Post-move state (verified Session 11 by `ls`): `auth_403/` contains
  17 fixtures (13 conforming-403 + 4 401-flavored auth markers);
  `parking_default_pages/` contains 2 uniform-200 fixtures
  (`grigolato.net.html` IIS welcome + `sanluishouston.com.html`
  nginx welcome).
- **Consequence for W4.1 script**: per-file 401-vs-403 split lives
  in `auth_403/`, not `parking_default_pages/`. The 4 files needing
  `response_status: 401`: `sanmarcosdentists.com.html`,
  `sanmarcosflower.com.html`, `sanmarcosforsale.com.html`,
  `sanmarcoshouse.com.html`. Remaining 13 in `auth_403/` get 403.
  `parking_default_pages/` is uniform 200.

Operator authorized **path A**: apply Truth-3-style corpus-wide
correction in Session 11 only; update SESSION_TRANSITION_TEMPLATE.md
recipe (forward-applicable, prevents Session 12+ rediscovery); leave
META_SCHEMA.md prose at v1.0 with the known wording bug; track the
deferred prose-only fix for fold-in at the next real semver bump.
Rationale: machine-readable schemas (`meta.schema.json` +
`expected.schema.json`) carry no directory→response_status mapping —
only the prose carries the bug, so no functional artifact is broken.
A v1.0 → v1.1 prose-only bump would churn the locked artifact for a
text fix that affects no machine validation.

Workspace changes landed this finding:
- SESSION_TRANSITION_TEMPLATE.md `response_status` recipe
  (corrected: `auth_403/` per-file 401 split; `parking_default_pages/`
  uniform 200; includes explicit "CORRECTED RECIPE (Session 11)" note
  to mark the prior wording as known-stale).
- SESSION_TRANSITION_TEMPLATE.md new "Deferred prose-only fixes"
  section (tracks META_SCHEMA.md §2.4 + §5 wording bug for fold-in at
  next real semver bump).
- SESSION_LOG.md this entry (chronological record of the finding).
- META_SCHEMA.md NOT updated (prose-only deferred per operator).
- meta.schema.json + expected.schema.json NOT updated (unaffected).

──────── Flag A resolution: option (b) — RFC 2606 .invalid fallback ─

During sample-review of W4.1 script output, three design questions
surfaced (Flags A/B/C). Flag A: for synthetic-variant fixtures with no
canonical link, the bare-domain fallback `https://<filename-stem>/`
produces structurally-valid-but-semantically-meaningless URIs (e.g.,
`https://wordpress_welcome_synthetic/`). Operator selected option (b):
use RFC 2606 reserved-TLD form `https://<filename-stem>.invalid/`.

Real-domain capture fallbacks (curl_with_retries, historical_unverified,
replaced_in_place) keep the bare-domain form unchanged — the filename
stem IS a real registered domain in those cases.

Implementation in `tests/fixtures/generate_meta_json.py`:
- new helper `synthetic_invalid_url(html_path) -> str`
- `derive_source_url(html_path, html, capture_method)` now branches on
  capture_method when canonical is absent: synthetic-variants → .invalid
  fallback; others → bare-domain fallback
- new provenance_note vocabulary value
  `approximated_from_synthetic_invalid_fallback` (distinct from
  `approximated_from_bare_domain_fallback`); tracked as a deferred
  prose-only fix in SESSION_TRANSITION_TEMPLATE.md for fold-in at the
  next real META_SCHEMA semver bump (machine schema unaffected;
  provenance_note values are `additionalProperties: {type: string}`)

Affects 20 pre-Session-1 synthetic fixtures (filename stems with
underscores) and any future synthetic-variant fixture authored without
a canonical link. The 5 synthetic_with_real_markers fixtures retain
their canonical links (typically `.test` TLD per RFC 2606) and are
unaffected.

──────── Flag B resolution: option (a) — replacement-commit date ──

For the 2 replaced_in_place files (parking_sale/shelvs.com.html via
C0.5c, legitimate_business/sanmarcosflowershop.com.html via
C0.5d-followup), `--diff-filter=A --follow` traces back to the
original 1697bb5 add commit — but that commit's content no longer
lives in the file. META_SCHEMA section 2.4 line 93's strict reading
would use 1697bb5's author date as captured_at; that's semantically
wrong (it would point at content the file no longer contains).
Operator selected option (a): use the C0.5x replacement commit's
author date instead, so captured_at reflects when the *current*
content was captured.

Tracked as a deferred prose-only fix in SESSION_TRANSITION_TEMPLATE.md
for fold-in at the next real META_SCHEMA semver bump. Machine schema
unaffected (captured_at is just `format: date-time`).

──────── Flag C resolution: 10-fixture sample (kept as-is) ────────

10 fixtures covered the 8 required coverage axes plus the
replaced_in_place case surfaced during the pre-bulk distribution
check. Operator declined expansion to one-per-category (≈26). Sample
review was clean (0 validation errors across 10).

──────── W4.1 bulk run (commit `9e1bda9`, pushed to origin/main) ──

Bulk-generation script `tests/fixtures/generate_meta_json.py` ran in
a single pass against all 198 fixtures. 197 new `<domain>.meta.json`
files written (the W4.0 worked example
`legitimate_business/twilio.com.meta.json` was protected and skipped).
Re-run was a no-op (197 skipped-exists confirms idempotency).

Verification before commit (operator-ratchet fired once mid-stream;
deeper double-check pass executed; 0 problems surfaced):
- Strict jsonschema (Draft7Validator) validation of all 198
  meta.json files: 0 violations
- 8-fixture cross-capture_method spot check (one per enum value
  plus locale-subdir + C0.7c 401 override + 2 replaced_in_place):
  0 problems
- Visual read of `shelvs.com.meta.json` (replaced_in_place via
  C0.5c): captured_at = 2026-05-19T19:43:41Z (replacement commit
  date, not original 1697bb5 add) — Flag B resolution applied
  correctly
- Visual read of `synthetic_blog_minimal.meta.json` (C1.4.a
  synthetic_with_real_markers): canonical `https://barebones-blog.test/`
  preserved via RFC 2606 `.test` TLD; no .invalid fallback triggered
- Anti-trip discipline validation passed on all 25 synthetic-variant
  fixtures (`synthetic` + `synthetic_with_real_markers`)
- Test surface invariant 17/169/2 held byte-for-byte across the
  198-file landing (meta.json files invisible to
  `_iter_fixtures *.html` glob, confirming Session 10 item #7
  regex-isolation verification)
- Idempotency confirmed via re-run: 197 skipped-exists, 1
  skipped-protected, 0 written
- No debug artifacts in the generator script (0 matches for
  `breakpoint()`, `pdb.`, bare `except:`, debug prints)
- No scope creep: 4 unstaged operator-side files in the locked tree
  (.claude/rules/code-correctness.md, eval_data/*) remained
  unstaged across the entire bulk operation

Pre-push gate at `9e1bda9` (commit SHA):
- ruff check                                    PASS
- ruff check --select C901 (manual McCabe)      PASS
- ruff format --check                           PASS
- vermin --target=3.10-                         PASS (informational
                                                only)
- validate_consistency.py                       PASS (0/0)
- pytest test_fixture_conformance               17 fail / 169 pass /
                                                2 skip (byte-exact)
- pytest test_hard_exclusions                   64 pass (unchanged)
- jsonschema strict validation                  0 schema violations

Push: `8aafc45..9e1bda9 main -> main`. Pre-push hook green.

──────── Three META_SCHEMA prose-only fixes deferred ─────────────

All three fold into the next real META_SCHEMA semver bump's diff
(per Session 11 operator path-A stance — no semver bump for prose
discrepancies whose machine schemas are unaffected). Tracked in
SESSION_TRANSITION_TEMPLATE.md "Deferred prose-only fixes" section.

1. Directory reference fix (Session 11 path-A finding, divergence
   surface). META_SCHEMA section 2.4 line 95 + section 5 line 149
   say the C0.7c nginx-401 split lives in `parking_default_pages/`;
   actually C0.7c moved those 4 files out to `auth_403/`.

2. replaced_in_place captured_at semantics extension (Flag B
   resolution). META_SCHEMA section 2.4 line 93 strict reading uses
   the first-add commit date; for replaced_in_place files, the
   replacement commit date is semantically correct.

3. Vocabulary extension (Flag A option b resolution). New canonical
   value `approximated_from_synthetic_invalid_fallback` added to the
   provenance_note Recommended source-string vocabulary.

──────── Distribution (corpus-wide truths) ───────────────────────

capture_method:
  curl_with_retries           20  (W0 Sessions 5+ real captures)
  historical_unverified      151  (pre-Session-1, commit 1697bb5)
  synthetic                   20  (pre-Session-1, commit ae3eb77)
  synthetic_with_real_markers  5  (C1.3.b, C1.4.a/b, C7.c, C22.c)
  replaced_in_place            2  (C0.5c, C0.5d-followup)

response_status:
  200                        181  (all non-auth_403/ categories
                                   including the 2 remaining
                                   `parking_default_pages/` fixtures)
  401                          4  (C0.7c-moved files in auth_403/)
  403                         13  (remaining auth_403/ fixtures)

source_url provenance:
  approximated_from_canonical_html_link             41
  approximated_from_bare_domain_fallback           137
  approximated_from_synthetic_invalid_fallback      20

──────── Test surface change (repo) ──────────────────────────────

  test_hard_exclusions.py:        64 passed (unchanged across
                                  Session 11; same baseline as
                                  Session 10 close).
  test_fixture_conformance.py:
    Pre-Session-11 (`8aafc45`):   17 failed, 169 passed, 2 skipped
    Post-commit (`9e1bda9`):       17 failed, 169 passed, 2 skipped
                                  (198 .meta.json files; invisible
                                   to `_iter_fixtures` `*.html` glob)

  Failure list at session close is EXACTLY the 17 Week-5 punch-list
  reds. Byte-for-byte stable across the W4.1 bulk landing.

──────── Workspace updates this session ──────────────────────────

- SESSION_LOG.md: this entry.
- SESSION_TRANSITION_TEMPLATE.md: corrected response_status recipe
  + new "Deferred prose-only fixes" section + refilled for
  Session 12.
- LESSONS.md: new "Deferred prose-only schema fixes" entry under the
  "Workstream / commit shape patterns" section (forward-applicable
  pattern surfaced this session; not previously in LESSONS.md).
- META_SCHEMA.md NOT updated (three deferred prose-only fixes per
  operator path-A stance).
- meta.schema.json + expected.schema.json NOT updated (unaffected
  by the prose discrepancies).
- BARCADA_CRAWLER_REMEDIATION_PLAN.md NOT updated (read-only per
  operator). Workstream C scope amendment (deferred Stage 3
  expected-output generation) still flagged for operator handling
  outside session work — carried forward to Session 12.

──────── Operator-interaction notes (Session 11 patterns) ────────

- Verify-before-asking discipline applied proactively before every
  commit confirmation: divergence found at pre-script verification
  (path-A finding); bug surfaced in capture_method derivation at
  pre-sample distribution check (replaced_in_place files traced to
  1697bb5 via --follow); sample-review surfaced three independent
  design questions (Flags A/B/C) before bulk authorization.

- Operator-ratchet fired twice this session, both at "Confirm to
  commit?" gating boundaries:
  1. At the W4.1 repo commit gate. Deeper-verification pass
     executed: 8-fixture cross-enum spot check, idempotency re-run,
     debug-artifact scan, scope-creep scan, visual read of 2
     generated meta.json files, full pre-push gate replay. 0 new
     problems surfaced. Operator confirmed commit after the
     deeper-check report.
  2. At the workspace close-out commit gate (this entry). Deeper-
     verification pass executed: Session 11 subsection structure
     check (12 subsections present), SHA cross-reference check
     across 4 files (SESSION_LOG, SESSION_TRANSITION_TEMPLATE,
     LESSONS, /tmp commit-msg), verbatim Flag 1 #2 quote check
     across 3 files, deferred-fix entry count (3 present), Week 4
     progress percentage cross-check (~60% consistent across both
     docs), LESSONS.md placement check (under Workstream / commit
     shape patterns), template TBD scan (2 intentional, 0 stale),
     vocabulary value cross-reference (all 3 files reference
     `approximated_from_synthetic_invalid_fallback`), pytest
     re-run (17/233/2 stable). 0 new problems surfaced.
  Pattern observation (forward-applicable): operator-ratchet
  propagates to ALL commit boundaries within a session, not just
  the primary work commit. Pre-commit verification discipline
  applies equally to workspace bookkeeping commits.

- Three operator decisions during W4.1:
  1. Path A: corpus-wide correction in SESSION_TRANSITION_TEMPLATE.md
     + SESSION_LOG.md only; META_SCHEMA.md prose stays at v1.0 with
     known bug; fold into next real schema bump.
  2. Flag A option (b): RFC 2606 `.invalid` TLD fallback for
     synthetic-variant fixtures with no canonical.
  3. Flag B option (a): use replacement commit date as captured_at
     for replaced_in_place files, not the original add date.
  4. Flag C: 10-fixture sample (no expansion to per-category).

──────── Open items entering Session 12 ──────────────────────────

Workstream 0 Week 4 continuation:

- **W4.2 expected/<domain>.json generation** (next concrete work
  unit). Stage 1/2 only per Flag 1 resolution; Stage 3 via canonical
  sentinel triple. Expected near-zero LLM cost (RULES + LR for the
  corpus majority). Stop and escalate if actual spend trends higher
  than near-zero before $50 alert threshold.

- **W4.3 Test infrastructure**. Update conformance tests to compare
  against expected/<domain>.json (replacing current
  "exclusion_reason must be empty" assertions with full comparison
  logic that respects the Stage 3 sentinel comparison-skip directive
  per Flag 1 constraint #5 semantic α).

- **W4 close + tag annotation**. At full W4 close (W4.3 complete),
  tag `workstream-0-week4-end` at the final green-gate SHA.
  Annotation must state per Flag 1 constraint #2: "Stage 3
  expected-outputs deferred to Workstream C per Flag 1 resolution;
  partial coverage at W4 close is intentional, not incomplete."

- **Workstream C scope amendment** (carried forward from Session 10
  + Session 11). Still pending operator handling outside session
  work; not a Session 12 W4.2 blocker.

Carried items status:

- Flag 1 (cost ceiling reconciliation): RESOLVED Session 10 →
  Option (c) defer Stage 3 to Workstream C.
- Flag 2 (verify-before-asking promotion): RESOLVED Session 10 →
  Option (c) status quo. Trigger condition documented for forward
  reopening.
- Flag 3 (W4 tag provenance): still flagged, not a blocker. Revisit
  at full W4 close.

Three new META_SCHEMA prose-only fixes added to deferred-fixes
tracker this session; fold into next real schema bump's diff.

Pre-push gate gap (Issue 3 from Week 2 audit erratum) remains open:
project's ruff `select` does not include "C" (mccabe). Workaround
this session: manual `ruff check --select C901` on the new
generator script. First Session-11 code-modifying commit; the gap
held without incident because manual McCabe was applied.

──────── Cost & schedule tracking ────────────────────────────────

- Cost incurred Sessions 1-11: $0. No LLM API calls in Session 11
  itself (W4.1 was pure scripted derivation + git log + grep +
  pytest + jsonschema validation). Cost ceiling $100 untouched.
  Budget remaining: $100.
- Schedule: ~3 weeks elapsed of Workstream 0's 5-week budget. Weeks
  1-3 COMPLETE; Week 4 OPEN (~60% complete with W4.0 schema lock
  done + W4.1 bulk meta.json done; W4.2 expected-output generation
  + W4.3 test infrastructure pending). Weeks 4-5 still ahead. W4
  likely spans 2-3 sessions per Session 10 prediction; Session 11
  closes the W4.1 unit at a natural seam (bulk meta.json landed and
  pushed; W4.2/W4.3 are distinct work units).

Next session prompt: see SESSION_TRANSITION_TEMPLATE.md.
Next concrete work: Workstream 0 W4.2 — expected/<domain>.json
generation across the 198-fixture corpus per META_SCHEMA v1.0 +
Flag 1 sentinel triple for stage3_decision.

──────── Correction (added Session 12-prep) ──────────────────────

The SESSION_TRANSITION_TEMPLATE.md and the draft Session 12 prompt
(at `/tmp/session-12-prompt.md`) claimed the Workstream C scope
amendment flag was staged in commit messages `9165791`, `8aafc45`,
and `9e1bda9`. Verification against git log (`git show --no-patch
--format=%B <SHA>` for each) shows the flag is present in `9165791`
and `8aafc45` only; `9e1bda9` does not carry it. The claim was
written by analogy during Session 11 close-out drafting without
source verification.

Three locations corrected with strengthened wording:
- SESSION_TRANSITION_TEMPLATE.md line ~175 (Outstanding operator-
  input requests section)
- SESSION_TRANSITION_TEMPLATE.md line ~568 (Notes for Session 12,
  "Plan is read-only" bullet)
- `/tmp/session-12-prompt.md` line ~38 (Outstanding operator-
  authorization items section of the Session 12 cold-start prompt)

Strengthened wording (applied at all three): "Staged in commit
messages `9165791` and `8aafc45`; not re-staged in W4.1 `9e1bda9`.
Operator decision needed: re-stage in subsequent W4 commit messages,
or treat as staged-once-and-carried-via-workspace-handoff."

Finding logged in LESSONS.md under the existing "Verify-before-
asking discipline" section as a new sub-section:
"Close-out claims-by-analogy in handoff documents." Codifies the
failure mode (structural claims written by pattern-completion
rather than source-verification during close-out drafting), the
mitigation recipe (`git log <SHA> --format=%B` + grep, or
equivalent), and the trigger pattern (any handoff or close-out
document naming specific SHAs / file paths / commit-message
contents / asserted state).

Trigger surfaced by operator question during Session 12 prompt
review. Verify-before-asking applied retroactively to the prompt
caught the propagated error in two more locations than the original
question. Demonstrates the pattern: a single targeted check against
source can unearth multi-location drift.

## Session 12 — W4.2 discovery, halt-and-reconcile, plan absorption (2026-05-21)

Scope: Open Workstream 0 W4.2 (expected/<domain>.json generation
across 198-fixture corpus). Discovery during pre-script verification
surfaced a cascade-model drift between the W4.2 framing in the plan +
SESSION_TRANSITION_TEMPLATE.md (Stage 1 RULES + Stage 2 LR + Stage 3
sentinel triple, near-zero LLM cost) and current code's actual
cascade composition. Operator paused W4.2; halt-and-reconcile
pattern engaged. Session closes with the resulting reconciliation
absorbed into BARCADA_CRAWLER_REMEDIATION_PLAN.md per
`RECONCILIATION_2026-05-21.md` §6.1.

──────── W4.2 discovery sequence (cascade-model drift surfaced) ──

Pre-script verification of the W4.2 generation script against
current code surfaced three findings that contradicted the W4.2
scope as carried forward from Session 11:

1. **Stage 1 LLM tier fires.** The cascade is RULES + LR + LLM
   (three-tier), not RULES + LR alone. Per `AUDIT_REPORT.md` §8 and
   current code at HEAD `5513b4c6`, the Stage 1 LLM tail
   (`gpt-4.1-nano`) fires on LR-uncertain residual (~5-10 fixtures
   per Claude Code Q3 cost envelope verification).
2. **Stage 2 has no LR tier.** Stage 2 is two-pass LLM
   (summarization Pass 1 + classification Pass 2), not LR-first.
   Pass 1 (`gpt-4.1-nano` summarizer) fires unconditionally on
   every eligible row; Pass 2 (`gpt-4.1-mini` classifier) consumes
   the summary. The architecture rationale document's "Lever 3
   removed Pass 1" framing is TARGET state, NOT current state
   (Lever 3 is gated on Phase 4 PR-E, which has not landed).
3. **Stage 2 fires outbound HTTP.** Stage 2 consumes
   `pages.parquet` produced by `FetcherSet` HTTP fetches; the
   fixture HTML is not in that shape. Running Stage 2 against
   fixtures requires a `FetcherSet` bypass at the `fetcher_core`
   seam, which does not exist in current code.

Stage 3 input shape verification (Q1–Q5 by Claude Code) further
surfaced that Stage 3 reads THREE upstream parquets (Stage 2
predictions, Stage 2 summaries, Stage 3 evidence cache) AND fetches
its own four T3 paths per domain via the reused Stage 2 `FetcherSet`
type at `stage3/run.py:111-113`. End-to-end fixture-based cascade
execution requires FIVE input surfaces to be synthesized or bypassed:
parser-output parquet, `pages.parquet`, Stage 2 predictions, Stage 2
summaries, plus the FetcherSet bypass.

The "small W4.1.5" framing that surfaced briefly during chat was
wrong; the work unit is closer in scope to what plan §4 W6 originally
scoped for `barcada-baseline generate`, pulled forward by ~2 weeks.

──────── Path-A/B/C/D elicitation + operator pause ──────────────

Claude Code session-side enumerated four candidate paths during the
halt:

- **Path A:** Mock LLM calls so W4.2 runs at $0 cost; ship sentinel
  triple for Stage 3 only. Rejected: validates the script not the
  cascade; defers the real cost-envelope question to a future
  unblock.
- **Path B:** Extend the meta.json sentinel pattern to all cascade
  decisions; emit a fully-sentinelled `expected/<domain>.json` per
  fixture. Rejected: defeats W4.2's purpose (expected outputs are
  for comparison testing, not provenance).
- **Path C:** Build a parser-output → Stage 1 fixture driver only;
  defer Stage 2/3 to a later work unit. Rejected: leaves W4.2
  outputs incomplete; W4.3 test-infra cannot validate cascade
  end-to-end against partial expected outputs.
- **Path D (sub-path-i):** Build the full fixture-cascade driver
  (parser-output adapter + FetcherSet bypass + end-to-end
  orchestrator) as a Phase-4-aligned engineering work unit;
  W4.2 then runs against the driver. Accepted by operator after
  reconciliation pass.

Operator paused W4.2 and authorized a reconciliation pass before
selecting a path.

──────── Reconciliation pass (operator-side, with two CC reports) ─

Operator-side reading covered: all workspace documents (audit
reports, plan, classification-adjacent plan, SESSION_LOG.md,
LESSONS.md, SESSION_TRANSITION_TEMPLATE.md), the Phase 4
implementation plan (`docs/phase4_implementation_plan.md` per audit
citation at line 111), and an operator-supplied pipeline
architecture rationale document. Identified plan-vs-architecture
drift: the architecture rationale describes v1 target state (the
state Phase 4's eight PRs are designed to produce), NOT current
code. Current code is closer to `AUDIT_REPORT.md` §8 discovered
architecture, modified by four landed Phase 4 PRs.

Two Claude Code source-verification reports landed during the
session (durable artifacts preserved at `~/crawler-audit/working/`):

1. **`phase4_status_2026-05-21.md`** — Per-PR status of the Phase 4
   eight-PR sequence. PR-COST, PR-A, PR-B, PR-C fully implemented;
   PR-D not started (operator-led labeling missing); PR-E blocked
   on PR-D; PR-F partially implemented (constant only, no driver
   consult); PR-G partially implemented ($4,500 default + docs
   stub).
2. **`phase4_current_state_2026-05-21.md`** — Levers 2/3/7 current
   state (NOT applied) + W4.2 cost envelope (~$0.30 LLM ballpark
   per current-cascade-composition fixture-corpus distribution).
3. **`stage3_input_shape_2026-05-21.md`** — Stage 3 input contract
   (three upstream parquets + four T3 path fetches) + fixture-input
   adapter sub-option analysis (sub-options (i) and (ii) bypass
   surfaces).

──────── Seven chat-claim corrections (verify-before-asking pattern) ─

The chat that produced the reconciliation made seven claims along
the way that source documents disagreed with. Listed here as
worked examples of the bidirectional verify-before-asking pattern
(LESSONS.md §"Verify-before-asking discipline" + Session 11
"Close-out claims-by-analogy"). Full text in
`RECONCILIATION_2026-05-21.md` §2.

1. "Phase 4 is unimplemented; Stage 3 doesn't exist in code yet."
   Source: Stage 3 exists at HEAD; four PRs landed.
2. "PR-COST is implementing the cost journal." Source: cost journal
   existed at audit time as immutable state machine; PR-COST
   extended it with enforcement.
3. "The audit didn't see the architecture document or
   `phase4_implementation_plan.md`." Source: `AUDIT_REPORT.md`
   line 111 explicitly cites Phase 4 docs. The gap is between the
   plan-authoring step and the implementation plan, not between
   audit and Phase 4.
4. "The eight PRs have not been executed" (operator recall claim).
   Source: four PRs (PR-COST, PR-A, PR-B, PR-C) had been executed.
   Bidirectional: verify-before-asking applies to operator-issued
   state claims too, not only Claude Code outputs.
5. "Stage 2 has no LR tier; Stage 2 is LLM-LLM." Source confirmed:
   Stage 2 is two-pass LLM (summarization + classification). The
   architecture rationale's single-pass framing is target state,
   not current state.
6. "The architecture rationale document describes the production
   pipeline." Source: it describes v1 target state. Multiple
   details (Lever 3 single-pass Stage 2, gpt-4.1-nano
   classification, gpt-4.1-mini Stage 3 primary, Lever 4 parser
   pre-classifier, Pass-1-dropped) are target, not current.
7. "A fixture-input adapter layer covers the FetcherSet bypass.
   W4.1.5 is a small work unit." Source: Stage 3 reads three
   upstream parquets AND fetches four T3 paths per domain. The
   work unit is closer in scope to W6 `barcada-baseline generate`.

──────── Operator decisions made during Session 12 ──────────────

1. **Read-only-period discipline broken with explicit operator
   authorization** for this absorption. One-shot exception; future
   plan amendments resume the read-only convention unless
   explicitly re-authorized.
2. **Reconciliation document location:** `~/crawler-audit/
   RECONCILIATION_2026-05-21.md`. Treated as one-shot historical
   record (per AUDIT_REPORT.md preservation convention), not a
   living document.
3. **Sequencing:** W4.1.5 (fixture-cascade driver) inserted between
   W4.1 (complete) and W4.2 (paused). Path-D sub-path (i): real
   end-to-end driver, NOT mock-LLM or sentinel-extension. W4.2
   follows W4.1.5 close.
4. **Tagging at W4.1.5 close** per existing tagging discipline
   (LESSONS.md "Workstream tag at clean completion" + "tag at
   clean SHA not milestone SHA"). Tag name:
   `workstream-0-week4-1-5-end`. Annotation specifies W4.2
   expected-outputs generation begins on the next commit, with
   the durability constraint (until W A.0 W6 OR Phase 4 PR-E
   lands).
5. **Architecture rationale document placement:**
   `~/crawler-audit/PIPELINE_ARCHITECTURE_TARGET_STATE.md`. Marked
   as design-of-record for unimplemented work; do NOT use as
   source-of-truth for current code.
6. **Three verification reports preserved as durable workspace
   artifacts** at `~/crawler-audit/working/phase4_status_2026-05-21.md`,
   `phase4_current_state_2026-05-21.md`, `stage3_input_shape_2026-05-21.md`.

──────── Drift correction during absorption (Edits 4 + 5 sub-naming) ─

Verify-before-asking during the absorption pass surfaced one
structural drift in `RECONCILIATION_2026-05-21.md` §6.1: Edits 4
and 5 referenced "the existing W4.1 close text" and "the existing
W4.2 sub-section" as if they were structural elements of plan §3
Week 4. They are not; plan §3 Week 4 was monolithic prose with no
W4.0/W4.1/W4.2/W4.3 sub-headings. The W4.0/W4.1/W4.1.5/W4.2/W4.3
naming is a session-convention used in SESSION_LOG.md and
SESSION_TRANSITION_TEMPLATE.md but had never landed in the plan
document prior to this session.

Operator authorized Option 2 + refinement: Edit 4 inserted a new
`### Week 4 (W4.1.5): Fixture-Cascade Driver` heading at the
insertion point; Edit 5 added a new `### Week 4 (W4.2): Expected
Outputs (revised scope)` heading at the revision point. No
retroactive W4.0/W4.1/W4.3 headings were added. Full Week 4
sub-naming harmonization deferred to a separate operator-authorized
edit if desired.

This drift correction is the durable record per the LESSONS.md
"bidirectional claims-by-analogy" pattern: when a reconciliation's
"currently says" claim disagrees with actual plan content, the
correction lands as part of the absorption's reporting, not as a
silent reconcile in favor of one or the other.

During absorption, verify-before-asking surfaced a second conflict:
the three Claude Code verification reports
(`phase4_status_2026-05-21.md`, `phase4_current_state_2026-05-21.md`,
`stage3_input_shape_2026-05-21.md`) were placed at `working/` per
the absorption prompt's deliverable 4, but `.gitignore` line 2
excluded `working/` as "Ephemeral working notes from Claude Code
sessions". Without resolution, the plan §13 Appendix references
would dangle. Operator authorized Option 2: whitelist the three
named reports in `.gitignore` with a provenance comment block
referencing `RECONCILIATION_2026-05-21.md`. The pattern required
one further refinement during application: a top-level directory
exclusion (`working/`) cannot be re-included via file-level
negation in gitignore semantics; the rule was changed to
`working/*` so that per-file `!working/<name>.md` negations take
effect. `git check-ignore --verbose` confirmed the three reports
match the negation rules. Default ephemeral behavior of `working/`
is preserved (subsequent files under `working/` remain ignored
unless explicitly whitelisted).

──────── Plan absorption landed: eleven §6.1 amendments ─────────

Coordinated edits applied to BARCADA_CRAWLER_REMEDIATION_PLAN.md
per `RECONCILIATION_2026-05-21.md` §6.1:

1. §1 "Where the crawler is genuinely strong": Phase 4
   infrastructure-half bullet + reframed cascade bullet.
2. §1 "Where the gaps are real": Phase 4 measurement-half
   gating bullet.
3. §2 Plan Overview table: new "Phase 4 (cost reduction + infra)"
   row + parallel-track sentence after table.
4. §3 Week 4: inserted new `### Week 4 (W4.1.5): Fixture-Cascade
   Driver` sub-section between meta.json and expected.json
   discussions.
5. §3 Week 4: added `### Week 4 (W4.2): Expected Outputs (revised
   scope)` heading + prerequisite reference + TODO comment on
   schema example (repo out of scope this session) + durability
   annotation + cost expectation.
6. §4 W6: `barcada-baseline generate` reframed as thin wrapper /
   extension over W4.1.5 driver.
7. §6 Workstream B: top-of-section Phase 4 / PR-COST note +
   Action #6 useful-record definition referencing
   `cost_ceiling_stopped` / `cost_ceiling_global`.
8. §7 Action #11 (HTML→Markdown): Phase 4 PR-E coordination note.
9. §11 Risk Register: three new entries (Phase 4 absorption gap,
   W4.2 lifetime constraint, Phase 4 measurement half blocked).
10. §13 Appendix: added `docs/phase4_implementation_plan.md`,
    `PIPELINE_ARCHITECTURE_TARGET_STATE.md`,
    `RECONCILIATION_2026-05-21.md`, three verification reports.
11. §14 Session Continuity Discipline: extended durable artifacts
    list + new plan-authoring-context note (audit-state HEAD
    `be71d536` vs. current-code HEAD `5513b4c6`).

──────── META_SCHEMA prose-only register grows to six entries ───

Three new entries added to the deferred prose-only register per
`RECONCILIATION_2026-05-21.md` §6.2 (no machine-schema bump,
per LESSONS.md "Defer prose-only schema fixes" pattern):

- (d) `tier_decided="parser_rule"` valid vocabulary entry
  (PR-F partial: constant exists at `stage3/output_schema.py:53`,
  no driver consult).
- (e) `expected/<domain>.json` shape reconciliation against
  `stage3/output_schema.py:112-140` actual columns.
- (f) Output durability annotation:
  "until W A.0 W6 supersedes OR until Phase 4 PR-E lands,
  whichever comes first."

Combined with the three pre-existing entries from Session 11
(Path-A directory ref, replaced_in_place captured_at semantics,
approximated_from_synthetic_invalid_fallback vocabulary), the
register is now six entries. All fold into the eventual v1.1
machine-schema bump's diff.

──────── Workspace changes landed this session ─────────────────

- `BARCADA_CRAWLER_REMEDIATION_PLAN.md`: eleven §6.1 amendments
  applied (one coordinated commit).
- `SESSION_LOG.md`: this entry.
- `LESSONS.md`: two new entries appended (§8.1 verify-before-
  asking extension; §8.2 driver-level input contracts).
- `SESSION_TRANSITION_TEMPLATE.md`: refilled for Session 13 with
  W4.1.5 as next concrete work unit, six-item deferred prose-only
  register, locked-artifact reminders extended.
- `RECONCILIATION_2026-05-21.md`: placed in workspace (operator
  authorship; preserved as archival historical record).
- `PIPELINE_ARCHITECTURE_TARGET_STATE.md`: placed in workspace
  (operator-supplied design-of-record for unimplemented work).
- `working/phase4_status_2026-05-21.md`,
  `working/phase4_current_state_2026-05-21.md`,
  `working/stage3_input_shape_2026-05-21.md`: three Claude Code
  source-verification reports preserved.

Repo (`/Users/administrator/projects/barcada-scraper/`) NOT
modified this session. Session 12 is governance-only; repo HEAD
remains at `5513b4c6` (the four-PR-landed current code).

──────── Operator-interaction notes (Session 12 patterns) ──────

- Verify-before-asking applied bidirectionally: operator-recall
  claim about Phase 4 not being implemented was contradicted by
  Claude Code source verification (four PRs landed). Pattern
  named in LESSONS.md §8.1 addition this session.
- Driver-level input contracts: W4.2 scoping assumed configuration-
  toggle work; pre-script verification revealed it requires
  driver-level adapter engineering. Pattern named in LESSONS.md
  §8.2 addition this session.
- Halt-and-reconcile cadence: discovery → halt → enumerate paths
  → reconcile pass with source verification → operator-authorized
  absorption. The cadence preserved the read-only-period
  discipline by making the break explicit, one-shot, and
  documented.
- Drift correction during absorption (Edits 4/5 sub-naming):
  operator authorized Option 2 + refinement before the edits
  landed. Documented as part of this entry per
  bidirectional-claims-by-analogy pattern.

──────── Open items entering Session 13 ───────────────────────

- **W4.1.5 fixture-cascade driver** (next concrete work unit).
  Three engineering surfaces per plan §3 Week 4 (W4.1.5):
  parser-output adapter, FetcherSet bypass at `fetcher_core` seam,
  end-to-end cascade orchestrator. Tag `workstream-0-week4-1-5-end`
  at clean checkout target.
- **W4.2 expected outputs** follows W4.1.5 close. Cost envelope
  ~$0.30 per Claude Code Q3 verification. Output durability:
  until W A.0 W6 OR Phase 4 PR-E lands, whichever comes first.
- **W4.3 test infrastructure** follows W4.2 close.
- **W5 multipage + edge cases + repopulation** follows W4.3 close.
- **Workstream C scope amendment** carried-forward flag: now
  superseded by the §11 Risk Register entries added this session.
  The original Workstream C scope amendment (deferred Stage 3
  expected-output generation) is absorbed into the wider Phase 4
  reconciliation; the §11 lifetime-constraint entry covers
  forward-applicable surface.

Carried items status:

- Flag 1 (cost ceiling reconciliation): superseded — W4.2 now
  runs against the W4.1.5 driver with cost envelope ~$0.30 per
  CC Q3 verification, well within the $100 ceiling.
- Flag 2 (verify-before-asking promotion): RESOLVED Session 10
  → Option (c) status quo, EXTENDED Session 12 (bidirectional
  pattern; see LESSONS.md §8.1 addition this session).
- Flag 3 (W4 tag provenance): superseded — W4 close pattern
  shifts to W4.1.5 / W4.2 / W4.3 sub-tags rather than a single
  W4 tag.

──────── Cost & schedule tracking ─────────────────────────────

- Cost incurred Sessions 1-12: $0. Session 12 is governance-only
  (no LLM calls; no repo modifications). Cost ceiling $100
  untouched. Budget remaining: $100.
- Schedule: ~3-4 weeks elapsed of Workstream 0's 5-week budget.
  Weeks 1-3 COMPLETE; Week 4 OPEN (W4.0 done, W4.1 done; W4.1.5
  PROPOSED for Session 13; W4.2/W4.3 follow). Session 12 added a
  work unit (W4.1.5) inside Week 4; the budget pressure increases
  but the cascade-driver work was always implicit in W6 — pulled
  forward, not net-new. Weeks 4-5 may extend ~1 week beyond the
  original 5-week plan; revisit at W4.3 close.

Next session prompt: see SESSION_TRANSITION_TEMPLATE.md.
Next concrete work: Workstream 0 W4.1.5 — fixture-cascade driver
per plan §3 Week 4 (W4.1.5) + `RECONCILIATION_2026-05-21.md` §5.1.

## Session 13 — W4.1.5 fixture-cascade driver landed (2026-05-21)

Scope: Built the W4.1.5 fixture-cascade driver per plan §3 Week 4
(W4.1.5) and `RECONCILIATION_2026-05-21.md` §5.1. Three engineering
surfaces under `tests/runners/fixture_cascade/`; small-subset
validation against 10 fixtures in fake mode confirmed acceptance
criteria 1-4 + 6; annotated tag placed at clean checkout SHA;
pushes landed clean.

──────── Cold-start verification at session open ───────────────

- Workspace HEAD `ce7e8e94` matched outgoing template.
- `reconciliation-2026-05-21-absorbed` tag at `ce7e8e9` confirmed.
- Repo HEAD `5513b4c6` matched outgoing template + the three
  verification reports (`phase4_status_2026-05-21.md`,
  `phase4_current_state_2026-05-21.md`,
  `stage3_input_shape_2026-05-21.md` all present).
- Plan §3 Week 4 (W4.1.5) heading confirmed at line 167; W4.2
  TODO comment at lines 212-215 located for resolution.

──────── Absorption TODO resolved (W4.1.5.T) ───────────────────

Workspace commit `a34f7a2`. Reconciled the plan §3 W4.2
`expected/<domain>.json` schema example against
`src/barcada_scraper/classifier/stage3/output_schema.py:112-140`
(verified at repo HEAD `5513b4c6`). Replaced the legacy
`stage3_decision: {partner_type, confidence, tier}` triple with
the full 18-column shape (identity / verdict / control / evidence
/ cost telemetry / page-acquisition / provenance). Added
explanatory line listing valid `tier_decided` values (`llm`,
`parser_rule`, `abstained`, `upstream_abstained`, `cost_ceiling`)
per `ALL_TIERS` + cross-reference to deferred prose-only fix
register entry (e) for the META_SCHEMA v1.0 /
`expected.schema.json` divergence.

Operator chose "Full 18-col rendition" via AskUserQuestion preview
before commit. The legacy v1.0 conformance gap is now an explicit
documented divergence rather than implicit; folds into the next
machine-schema bump.

──────── Three engineering surfaces ────────────────────────────

Pre-engineering: ran a Claude Code source-verification subagent
against all three surfaces at session-current repo HEAD. Confirmed
no module changed since the Session 12 verification SHA. Audit
identified key gotchas:

- No reusable parser-composition entry point in the production
  parser; the driver must re-implement the call sequence from
  `crawler.crawl_domain:527-683` at the test-runner layer.
- `FetcherSet` lives at `stage2/run.py:138`, NOT in `fetcher_core.py`
  as the verification report's section heading implied.
- Stage 1's `_read_shard` is single-file-only (no Hive support); the
  driver must write parser parquet via `pa.Table.from_pylist` direct,
  bypassing the production `PartitionedShardWriter` Hive layout.
- Five fake adjudicators needed for full cascade coverage (Stage 1
  LLM, Stage 2 summarizer + classifier, Stage 3 evidence + primary).
- Stage 3 results dataclass uses `total_cost_usd` not
  `primary_cost_usd`; corrected during integration testing.
- The fixture corpus has 198 files including 3 nested at
  `international_business/<locale>/<domain>.html`; `rglob` over
  `glob('*/*.html')` was needed for full coverage. Surfaced via a
  test assertion failing on count 195 vs 198.

Operator approved a four-question design sketch via AskUserQuestion
before any code-modifying commits:
- Driver location: `tests/runners/fixture_cascade/`.
- LLM mode: `--llm-mode={fake,real}` flag with fake default.
- LRBundle: synthesized always-uncertain (predict_proba=0.50) with
  `synthetic_lr_used: true` annotation in expected.json (META_SCHEMA
  v1.0 allows extra fields per Draft 7 default).
- expected.json shape: 18-col stage3_decision; skip v1.0
  expected.schema.json validation (deferred fix (e)).

**Surface 1 (`W4.1.5.S1`, repo `d337fb5`)**: parser-output adapter
in `parser_compose.py` + 18 unit tests. Mirrors the 8-call parser
composition from `crawler.py:527-683` minus IO/SPA/barrier/multi-page
branches. Writes a single-file parser parquet that Stage 1's
`_read_shard` consumes. Real-fixture round-trip on hubspot.com
captured-HTML confirms `flatten_record` + `pa.Table.from_pylist`
matches FEATURE_SCHEMA_VERSION=5 SCHEMA.

**Surface 2 (`W4.1.5.S2`, repo `02ac0e8`)**: fixture-backed
`FetcherSet` substitute in `fixture_fetcher.py` + 19 unit tests.
Duck-typed protocol matching the three production tier fetchers
(`fetch`, `head`, `aclose`, `provider_name`). One instance wired
into all three FetcherSet tiers via `build_fixture_fetcher_set`.
Missing-fixture path returns `ERROR_OTHER` (deliberately NOT in
`PROTECTION_ERROR_KINDS` so tier promotion stays static). Real
corpus index covers all 198 fixtures via `rglob`.

**Surface 3 (`W4.1.5.S3`, repo `dd64963`)**: end-to-end cascade
orchestrator in `cascade.py` + CLI in `cli.py` + consolidator in
`consolidate.py` + fakes in `fakes.py` + 9 integration tests.
PR-COST cost journal opened with `JournalState.fresh()` +
`update_with_retry` pattern per `cli._record_shard_completion`.
Three stage `run_shard` calls back-to-back; consolidator walks the
4 per-stage parquets and emits per-fixture expected.json with
META_SCHEMA v1.0 top-level keys + 18-col stage3_decision.

Total test surface at Session 13 close: **46/46 PASSED** across
all three surface test modules. Lint + format + McCabe (C901) clean.

──────── Small-subset validation (W4.1.5.V, workspace `c528a47`) ──

Ran `python -m tests.runners.fixture_cascade.cli --output-dir
/tmp/w415-validation/run01 --run-id w4-1-5-validation-2026-05-21
--llm-mode fake --max-fixtures 10` against the real corpus.

Result:
- 10 fixtures processed (sorted-by-domain order: archive.org
  through bestlogisticsjobs.com).
- ~6 seconds wallclock; $0.00 cost (fake mode).
- All 5 intermediate parquets present + stage2_pages.parquet +
  stage3_pages.parquet.
- 10/10 `expected/<domain>.json` files emitted matching the plan §3
  W4.2 shape.
- Cost journal `run_w4-1-5-validation-2026-05-21.json` carries
  3 stage shard records (`stage=1/2/3`, `outcome="completed"`).

Acceptance criteria coverage:
- (1) end-to-end without manual intervention: MET (subset).
- (2) five intermediate parquets exist + conform: MET.
- (3) per-fixture expected.json shape: MET (18-col stage3_decision).
- (4) RUN_ID-stamped cost journal: MET.
- (5) cost within 3× of $0.30: MET under fake mode; real-mode
  small-subset validation deferred to operator before W4.2
  full-corpus generation.
- (6) no writes outside output_dir: MET.

Durable report at `working/w4_1_5_small_subset_validation_2026-05-21.md`,
whitelisted in workspace `.gitignore` alongside the three Session 12
verification reports.

──────── Tag placement + push ─────────────────────────────────

Annotated tag `workstream-0-week4-1-5-end` (tag SHA `f9be833a`)
placed on repo `main` at `dd64963` per plan §3 W4.1.5 + LESSONS.md
"tag at clean SHA not milestone SHA" — the Surface 3 commit is the
clean checkout target after small-subset validation confirmed
acceptance criteria 1-4 + 6. Annotation: "Fixture-cascade driver
landed. Reusable at W A.0 W6 as `barcada-baseline generate`
foundation. W4.2 expected-outputs generation begins on the next
commit. Output lifetime: until W A.0 W6 OR until Phase 4 PR-E
lands, whichever comes first."

Push gate:
- Repo `git push origin main`: clean. Pre-push gate (ruff +
  vermin --target=3.10- + validate_consistency) all PASS.
- Repo `git push origin workstream-0-week4-1-5-end`: clean.
- Workspace `git push origin main`: clean.

Operator initially chose "Hold" on the push gate AskUserQuestion,
then explicitly authorized push in the follow-up message. No
`--no-verify` used.

──────── Operator decisions made during Session 13 ────────────

1. **Plan example shape** (TODO resolution): full 18-column
   rendition. Decided via AskUserQuestion preview before commit.
2. **Driver location**: `tests/runners/fixture_cascade/` (sibling
   to tests/fixtures/, clearly test-runner-side).
3. **LLM-mode wiring**: both fake + real modes via `--llm-mode`
   CLI flag.
4. **LRBundle**: synthesized always-uncertain (`predict_proba=0.50`).
   Operator refinement: annotate LR/LLM-tier rows as
   `synthetic_lr_used: true` in expected.json. Confirmed v1.0
   META_SCHEMA allows the additional field; no register bump
   needed.
5. **expected.json shape**: 18-col stage3_decision; skip v1.0
   expected.schema.json validation at W4.1.5 (deferred fix (e)).
6. **W4.2 worked-example handling deferred**: the
   `legitimate_business/expected/twilio.com.json` `_placeholder`
   resolution moves to W4.2 sample-review time (overwrite vs.
   protect).
7. **Push hold-then-confirm**: initial Hold, then authorized.

──────── Patterns reinforced this session ─────────────────────

- **Surface-by-surface decomposition with operator approval gates**:
  three engineering surfaces, each landed as one commit after
  "Confirm to commit?" approval. Same shape as the W4.1 commit
  cadence (Session 11) and the absorption-pass commits (Session 12).
- **Verify-before-asking on schemas**: production schema details
  (BusinessVerdict's `classification` field vs. `is_business`;
  PartnerEvidence's `primary_business_model` field; PartnerVerdictPrimary's
  `partner_type` not `primary_partner_type`) only surfaced via
  source reads; copying my own first-draft fake adjudicator shapes
  would have failed at integration-test time. The mid-stream
  corrections landed before pytest runs against the real schemas.
- **Driver-level input contracts** (LESSONS.md Session 12 entry):
  Stage 1's single-file parquet reader vs. Stage 2's directory-aware
  reader; Stage 3's three-input contract; FetcherSet's duck-typed
  protocol. All confirmed at session-current HEAD via the
  pre-engineering subagent audit, before any code lands.
- **Halt-on-discovery**: the `extract_text_from_html` tuple-return
  surfaced as a test failure; the 195-vs-198 corpus count surfaced
  via assertion. Both corrected at first-failure rather than
  silently accommodated.

No new LESSONS.md entries this session — all observed patterns
were instances of previously-established discipline.

──────── Workspace changes landed this session ────────────────

- `BARCADA_CRAWLER_REMEDIATION_PLAN.md`: plan §3 W4.2 schema
  example reconciled (one continuation-of-absorption commit
  `a34f7a2`).
- `working/w4_1_5_small_subset_validation_2026-05-21.md`: durable
  validation artifact created.
- `.gitignore`: whitelisted the validation report.
- `SESSION_LOG.md`: this entry.
- `SESSION_TRANSITION_TEMPLATE.md`: refilled for Session 14 with
  W4.2 as next concrete work unit.

Repo changes:
- `tests/runners/__init__.py` + `tests/runners/fixture_cascade/`
  package (parser_compose / fixture_fetcher / fakes / consolidate /
  cascade / cli + matching test_* modules) — across three commits
  W4.1.5.S1/S2/S3 (`d337fb5` → `02ac0e8` → `dd64963`).
- Annotated tag `workstream-0-week4-1-5-end` placed at `dd64963`
  (the Surface 3 commit = clean checkout target per LESSONS Session
  6 "tag at clean SHA not milestone SHA").
- `README.md` updated at `5449ba6` — post-tag doc hygiene per
  CLAUDE.md "After commit and push, update README immediately".
  New `### Fixture-cascade driver (W4.1.5)` subsection under the
  existing `## Testing & fixture corpus` heading covers invocation
  modes, output layout, tag SHA reference, and W4.2 durability
  constraint. The README commit lands AFTER the tag (the tag
  marks the work-unit close; doc hygiene is a follow-up
  operation, not part of the tagged work).

Test count at Session 13 close: parent suite green; conformance
suite red count steady at 17 (Week 5 punch list), 169 pass, 2 skip,
64 hard_exclusions pass — same as Session 11/12 close.

──────── Cost & schedule tracking ─────────────────────────────

- Cost incurred Sessions 1-13: $0. Session 13 ran only in fake
  mode; no Azure calls. Budget remaining: $100.
- Schedule: ~4 weeks elapsed of Workstream 0's 5-week budget.
  - Weeks 1-3 COMPLETE.
  - Week 4 IN PROGRESS: W4.0 done, W4.1 done, **W4.1.5 DONE**;
    W4.2 PROPOSED for Session 14; W4.3 follows.
  - Week 5 ahead.
  - Per Session 12 framing, W4.1.5 pulled cascade-driver
    engineering forward from W A.0 W6 by ~2 weeks. Net schedule
    impact tracked at W4.3 close.

Next session prompt: see SESSION_TRANSITION_TEMPLATE.md.
Next concrete work: Workstream 0 W4.2 — full-corpus expected.json
generation via the W4.1.5 fixture-cascade driver in real mode, per
plan §3 Week 4 (W4.2) + the open items in the Session 13 validation
report.

---

## Session 14 — W4.2 expected-outputs generation across 198-fixture corpus (2026-05-21)

Scope: Operator-driven generation session. Ran the W4.1.5
fixture-cascade driver (tagged `workstream-0-week4-1-5-end` at
`dd64963`) in `--llm-mode real` against the full 198-fixture corpus,
human-reviewed the resulting per-fixture `expected/<domain>.json`,
copied them into `tests/fixtures/html/<category>/expected/`, and
landed one coordinated commit at `cc2ba2c` per plan §3 Week 4 (W4.2).

──────── Cold-start verification at session open ───────────────

- Workspace HEAD `e60bee7` matched outgoing template.
- `reconciliation-2026-05-21-absorbed` tag at `ce7e8e9` confirmed.
- Repo HEAD `5449ba6` matched outgoing template.
- Annotated tag `workstream-0-week4-1-5-end` confirmed at `dd64963`
  (tag SHA `f9be833a`).
- Driver intact at `tests/runners/fixture_cascade/` (no diff vs
  `dd64963`).
- Driver test suite: **46/46 passed** in 29.83s.
- All four required workspace verification reports present
  (`phase4_status`, `phase4_current_state`, `stage3_input_shape`,
  `w4_1_5_small_subset_validation`).

──────── Step A: Real-mode small-subset validation ─────────────

**Step A v1** (sorted-by-domain first-10): operator ran
```
.venv/bin/python -m tests.runners.fixture_cascade.cli \
    --output-dir /tmp/w4-2-real-validation \
    --run-id w4-2-real-validation-2026-05-21 \
    --llm-mode real --max-fixtures 10
```
Result: $0.00226 total, 13.4s wallclock. Under-exercised cascade
(8/10 routed to Stage 1 RULES `is_business=False`; 1 fired Stage 2
LLM — backmarket.com → `not_technology`; 0 fired Stage 3 LLM). The
literal halt thresholds passed (total < $0.18, no exception, output
NOT identical to fake-mode), but the cost-shape gate's purpose
(validate Stage 3 extrapolation) wasn't met because Stage 3 didn't
fire at all.

Operator chose to re-run Step A with a curated diverse subset that
would exercise Stage 2 + Stage 3 LLM tiers.

**Step A v2** (10 curated fixtures spanning legitimate_business /
mega_menu / legitimate_nonprofit / international_business):
twilio.com, hubspot.com, snowflake.com, notion.so, webflow.com,
salesforce.com, shopify.com, mozilla.org, wikimediafoundation.org,
siemens.de. Result: $0.10656 total, 48s wallclock, 6 Stage 3 LLM
verdicts (twilio/hubspot/salesforce/notion/shopify/webflow all → ISV
with confidence ≥0.9). Per-call Stage 3 primary cost averaged
$0.0142 (Q3 ballpark $0.00470, 3× higher — within material caveats
±25% per-call + ±50% if cache miss). Full-corpus extrapolation ~$0.65
(below $0.90 halt threshold).

Notable side observations from Step A v2 (carry forward to commit
message):
- Per-tier cost-accounting gap: cost_journal `totals.stageN_*_usd`
  fields all $0; shard-level `cost_usd` is authoritative. Per-row
  `evidence_cost_usd` is $0 for all rows. Driver-locked policy
  applies; not a W4.2 blocker.
- Stage 1 false-negatives: 4 of 10 (mozilla, snowflake, wikimedia,
  siemens) returned `is_business=False` at RULES tier
  (signals_business_score below threshold). Documented current
  cascade behavior, NOT a driver bug.

Operator approved proceeding to Step B.

──────── Step B: Full-corpus 198-fixture run ───────────────────

Operator ran:
```
.venv/bin/python -m tests.runners.fixture_cascade.cli \
    --output-dir /tmp/w4-2-full-corpus \
    --run-id w4-2-full-corpus-2026-05-21 \
    --llm-mode real
```
No `--max-fixtures` cap. Driver enumerated all 198 fixtures via
`rglob` (including the 3 nested `international_business/<locale>/`
fixtures).

Result:
- **Total cost: $0.26345** — within Q3 audit ballpark ($0.30); below
  $0.90 halt threshold (3× ballpark).
- Stage 1 shard: $0.00473.
- Stage 2 shard: $0.04992.
- Stage 3 shard: $0.20880.
- Wallclock: 117s (~2 min) — well below 5-15min estimate;
  `max_concurrent_*=5` concurrency carried.
- 198/198 expected.json emitted under `/tmp/w4-2-full-corpus/expected/`.
- All five intermediate parquets produced (parser, stage1_predictions,
  stage2_summaries, stage2_predictions/, stage3_predictions) plus
  bandwidth/cache parquets.
- `cost_journal.shards`: 3 entries (stage 1/2/3, all `outcome="completed"`).
- `halted: false`, no exception raised.

──────── Step C: Per-fixture human review ──────────────────────

Routing distribution (real-mode, 198 fixtures across 29 categories):
- **175 fixtures**: Stage 1 RULES → `is_business=False` → upstream-
  abstained through Stage 2 + 3.
- **23 fixtures**: Stage 1 → `is_business=True` → Stage 2 fires.
- **17 fixtures**: Stage 2 classified as Technology → Stage 3 fires.
- **12 fixtures**: Stage 3 returned an LLM verdict (the other 5
  abstained at the evidence step).

All 12 Stage 3 LLM verdicts are "Independent Software Vendor" (11) or
"Reseller" (1), confidence ≥0.75. Spot-check verified semantically
defensible against fixture HTML for: twilio, hubspot, salesforce,
notion, shopify, webflow, gitlab, locaweb.com.br, synthetic_devtools_
marketing, synthetic_microsoft_style_aria_controls, sanluisconnect.com
(Reseller — HTML actually advertises "ResellerPanel Affiliate"),
sanmarcosoutlook.com (ISV — HTML is actually Pair Domains marketing).

Stage 1 false-negative cluster against directory taxonomy:
- legitimate_business: 7 of 15 FN (snowflake, grigionitaliano,
  sanluisfinancial, ssquared* x3, sheltonestates, ssroklahoma)
- legitimate_nonprofit: 6 of 6 FN (all — mozilla, redcross,
  doctorswithoutborders, archive.org, wikimediafoundation,
  synthetic_educational_organization)
- legitimate_blog: 3 of 3 FN (danluu, jvns.ca, simonwillison)
- international_business: 1 of 3 FN (siemens.de)
- Total: **17 of 27 "legitimate*" fixtures route to is_business=False**.

Most FN cases have low/negative `signals_business_score` OR
`crawl_meta_homepage_text_length=0` (parser couldn't extract text from
JS-rendered shells). Reflects current signals engine behavior; tracked
under known-FN signals design decisions per project memory.

Four fixture-taxonomy/content mismatches surfaced:
1. parking_sale/sanluisconnect.com → Stage 3 Reseller (HTML
   actually advertises a reseller affiliate program).
2. parking_sale/sanmarcosoutlook.com → Stage 3 ISV (HTML is actually
   Pair Domains' marketing page, not a parked domain).
3. spa_shell/sanmarinoiron.com → `is_business=True` (5912 chars of
   real metalworking business content despite spa_shell directory).
4. auth_403/grilloresources.net → `is_business=True` (parser tagged
   as `parking_errors` with bus_score=8 on the 403 HTML; signals
   engine quirk).

None of these are driver-bug-suspected. The cascade verdicts are
semantically correct against the actual HTML content; the fixture
filenames/categories may need W5-era recategorization.

Conformance category counts cross-verified: all 29 categories match
the expected fixture counts (e.g. parking_construction n=37,
auth_403 n=17, legitimate_business n=15, etc.). 198 total.

──────── Step D: Copy into fixture tree ────────────────────────

Python-driven copy from `/tmp/w4-2-full-corpus/expected/<domain>.json`
into the matching `tests/fixtures/html/<category>/expected/<domain>.json`,
using `rglob` to locate the source `.html` file's parent directory.

Result:
- 198 files copied.
- 0 skipped.
- 1 file overwritten: `legitimate_business/expected/twilio.com.json`
  (the W4.0 schema-lock placeholder replaced with W4.2 driver output
  per operator decision — overwrite, not protect).
- 28 new `expected/` directories created (one per category, plus the
  3 nested `international_business/<locale>/expected/`).

Conformance-enumerator finding (W4.3 visibility): the current
`tests/scraper/test_fixture_conformance.py:38` uses
`sorted((FIXTURES / category).glob("*.html"))` (single-level glob).
The 3 nested `international_business/<locale>/expected/<domain>.json`
files are NOT discovered by this enumeration. W4.3 will need to make
the enumeration `rglob`-aware OR restructure the parametrize.

──────── Step E: One coordinated commit + push ─────────────────

Repo commit `cc2ba2c` ("W4.2: 198 expected.json files generated via
fixture-cascade driver (real-mode)"). File-based commit message at
`/tmp/W4.2-msg.txt`, body covers: action ref W4.2, per-category
fixture counts (29 categories totaling 198), routing distribution,
total LLM cost breakdown, twilio.com overwrite decision, Stage 1 FN
cluster characteristic, fixture-taxonomy/content mismatches, per-tier
cost-accounting wiring gap surface, nested-fixture conformance
enumerator concern, plan ref §3 W4.2, pytest 46/46 driver-suite
confirmation, pre-push gate status.

Pre-push gate ran clean (ruff + ruff format + vermin 3.10 target +
validate_consistency 0 errors/0 warnings). `git push origin main`
landed `5449ba6..cc2ba2c`. No `--no-verify` used.

**No tag at W4.2 close** per Session 12 sequencing decision (the
`workstream-0-week4-1-5-end` tag at `dd64963` marks the Week 4
engineering milestone; W4.2 + W4.3 land without their own tags).

──────── Verify-before-asking double-check at session close ────

15-check verification battery (operator-requested "double check your
work") ALL PASS:
- Commit SHA `cc2ba2c` == HEAD == origin/main.
- 198 expected.json files on disk == 198 in the commit.
- Driver locked: `git diff dd64963..HEAD -- tests/runners/fixture_cascade/`
  = empty.
- Production code untouched: `git diff dd64963..HEAD -- src/ configs/`
  = empty.
- eval_data NOT in commit (locked artifact preserved).
- Tags unchanged: `workstream-0-week4-1-5-end → dd64963` still.
- No new tag at W4.2 close (only `workstream-0-week4-1-5-end` in
  week4 family).
- All 29 categories' fixture counts match commit message exactly.
- Twilio.com overwrite verified: `_placeholder=False`, 168-key
  parser_output, 18-key stage3 with primary="Independent Software
  Vendor" / tier="llm" / confidence=0.92.
- 198 .html ↔ 198 expected.json (no orphans either direction).
- Cost-journal numbers match commit message exactly.
- Conformance test count unchanged: 17 fail / 169 pass / 2 skip.
- 12 Stage 3 LLM verdicts on disk (matches commit msg claim).
- Final repo state: only eval_data unstaged (locked-artifact);
  branch sync clean.

──────── Operator decisions made during Session 14 ─────────────

1. **Step A v1 → v2 re-run**: operator chose diverse-subset re-run
   when v1 sorted-by-domain sample under-exercised the cascade.
2. **Step B authorization**: approved proceeding to full-corpus run
   after v2 demonstrated semantically real LLM verdicts and a
   defensible per-call cost shape (within 3× of $0.30 ballpark).
3. **Twilio.com.json overwrite (vs protect)**: operator chose
   overwrite. The W4.0 `_w4_note` anticipated this supersession
   ("Real parser_output generated in W4.2 by running ... through
   the parser"). Overwritten verbatim with the W4.2 cascade verdict.
4. **Step C → D authorization**: operator reviewed the Stage 1 FN
   cluster + the 4 fixture-taxonomy/content mismatches and chose
   to land all 198 expected.json files as-is (documenting current
   cascade behavior). No driver-bug-suspected cases. Fixture
   recategorization deferred to W5.
5. **Push authorization**: direct approval after confirm-to-commit
   (no Hold/re-authorize round-trip).
6. **Tag policy clarification at close**: when operator said "don't
   forget to tag" at close-out time, surfaced as conflict with the
   W4.2 prompt's "no tag at W4.2 close" policy. Operator chose
   "Ignore my request" — honoring the prompt's no-tag policy. No
   W4.2 tag placed.

──────── Patterns reinforced this session ─────────────────────

- **Sample review before bulk** (Session 11 W4.1 analog): two-step
  Step A subset validation before the 198-fixture bulk run.
- **One coordinated commit for bulk** (Session 11 W4.1 + LESSONS.md):
  198 expected.json files in a single commit at `cc2ba2c`.
- **Confirm-to-commit gating** before the W4.2 commit.
- **Verify-before-asking discipline**: per-fixture cascade verdicts
  cross-checked against source HTML (Internet Archive empty SPA
  shell, Pair Domains in parking_sale, ResellerPanel affiliate
  copy in sanluisconnect HTML); cost numbers cross-verified against
  the cost journal at commit time; 15-check verification battery at
  close.
- **Driver-locked policy**: W4.1.5 driver at `dd64963` unchanged
  through W4.2. Cost-journal per-tier accounting gap surfaced but
  not patched (driver-locked).
- **Plan-as-read-only**: BARCADA_CRAWLER_REMEDIATION_PLAN.md
  unchanged this session.
- **Operator-ratchet at close**: operator's "don't forget to tag"
  instruction conflicted with the W4.2 prompt's no-tag policy;
  surfaced via AskUserQuestion rather than silently overriding
  either side. Operator chose to honor the prompt.

No new LESSONS.md entries this session — all observed patterns were
instances of previously-established discipline.

──────── Workspace changes landed this session ────────────────

- `SESSION_LOG.md`: this entry (Session 14 append).
- `SESSION_TRANSITION_TEMPLATE.md`: refilled for Session 15 with
  W4.3 as next concrete work unit (test infrastructure update; gating
  design question = expected.schema.json v1.0 → v1.1 bump vs
  consolidator-mapping path).

Repo changes:
- 198 new `tests/fixtures/html/<category>/expected/<domain>.json`
  files (one coordinated commit `cc2ba2c`).
- 28 new `expected/` directories created.
- One pre-existing file overwritten:
  `legitimate_business/expected/twilio.com.json` (W4.0 placeholder
  → W4.2 cascade verdict).
- Pushed to `origin/main` at `5449ba6..cc2ba2c`.
- **No new repo tag at W4.2 close** per Session 12 sequencing
  decision.

Test counts at Session 14 close (verified):
- Driver suite (`tests/runners/fixture_cascade/`): 46/46 pass.
- Conformance suite (`tests/scraper/test_fixture_conformance.py`):
  17 fail, 169 pass, 2 skip (unchanged from Session 13 close;
  Week 5 punch list).
- Hard-exclusions suite: 64 pass (steady).

──────── Cost & schedule tracking ─────────────────────────────

- Cost incurred Session 14: **$0.26345** (W4.2 full-corpus real-mode
  generation; first session with non-zero Azure spend).
- Cost incurred Sessions 1-14 total: **$0.26345**.
- Budget remaining: **$99.74**.
- Schedule: ~4.5 weeks elapsed of Workstream 0's 5-week budget.
  - Weeks 1-3 COMPLETE.
  - Week 4 IN PROGRESS: W4.0 done, W4.1 done, W4.1.5 done, **W4.2
    DONE** this session; W4.3 PROPOSED for Session 15.
  - Week 5 ahead.

Next session prompt: see `SESSION_TRANSITION_TEMPLATE.md`.
Next concrete work: Workstream 0 W4.3 — replace `exclusion_reason`
assertions with `expected/<domain>.json` comparison logic in
`tests/scraper/test_fixture_conformance.py`. Gating design question:
schema bump v1.0 → v1.1 (path a) vs consolidator-mapping (path b).
Conformance enumerator must shift from `.glob("*.html")` to `rglob`
(or equivalent) to discover the 3 nested
`international_business/<locale>/expected/<domain>.json` files.

## Session 15 — W4.3 test-infrastructure update (2026-05-21)

Scope: Engineering session. Bumped `tests/fixtures/expected.schema.json`
v1.0 → v1.1 to match the 18-column `stage3_decision` shape that landed
across the 198-fixture corpus at W4.2 commit `cc2ba2c`, folded in the
six deferred prose-only fixes (a)-(f) from the SESSION_TRANSITION_
TEMPLATE.md register into META_SCHEMA.md, and augmented the conformance
suite's directory-semantic assertions with a hard_exclusions drift
check against the W4.2-committed parser_output slice. Two repo commits
(`7728bdf` W4.3.B + `b2e2671` W4.3.D); one workspace commit (this
SESSION_LOG entry + SESSION_TRANSITION_TEMPLATE refill); one operator-
authorized capstone tag `workstream-0-week4-end` at `b2e2671`.

──────── Cold-start verification at session open ───────────────

- Workspace HEAD `a50c044` matched outgoing template (Session 14 close).
- Annotated tag `reconciliation-2026-05-21-absorbed` at `ce7e8e9`
  confirmed untouched.
- Repo HEAD `cc2ba2c` matched outgoing template (W4.2 close).
- Annotated tag `workstream-0-week4-1-5-end` confirmed at `dd64963`
  (annotated tag SHA `f9be833a`).
- 198 expected.json files present on disk.
- Driver intact at `tests/runners/fixture_cascade/` (zero diff vs
  `dd64963`).
- Driver suite at session open: 46/46 passed (29.83s).
- Conformance suite at session open: 17 failed, 169 passed, 2 skipped
  (Week 5 punch list byte-stable from Session 14 close).
- Schema-shape divergence source-verified:
  - `expected.schema.json` v1.0 stage3_decision.required = legacy
    triple `[partner_type, confidence, tier]`.
  - `src/barcada_scraper/classifier/stage3/output_schema.py:109-142`
    SCHEMA = 18-col stage3_predictions parquet shape.
  - `twilio.com.json` committed expected.json carries the 18-col shape
    (primary_partner_type="Independent Software Vendor", tier_decided=
    "llm", 168-key parser_output). Validates against v1.1 but NOT v1.0.

──────── Step A: Schema-shape resolution (design-gate) ─────────

Operator chose path (a) — schema bump v1.0 → v1.1 — over path (b)
adapter (test-side OR driver-side variant). Rationale: cleanest semantic
alignment with the 18-col shape already landed at W4.2; no test-side
indirection; no driver-locked-policy breach. Path (b) driver-side variant
would have required regenerating the 198 expected.json files (W4.2
ground-truth lock would have been breached); path (b) test-side variant
would have left the v1.0 schema-vs-data divergence permanently visible.

──────── Step B: Schema bump + META_SCHEMA prose realignment ───

Commit `7728bdf` W4.3.B. Two files touched:

- `tests/fixtures/expected.schema.json`:
  - stage3_decision.required: legacy triple → 18-col list (domain,
    crawl_timestamp, primary_partner_type, primary_confidence,
    secondary_partner_types, tier_decided, abstain, abstain_reason,
    rationale, upstream_abstained, evidence_summary, fetch_cost_usd,
    evidence_cost_usd, primary_classification_cost_usd, secondary_
    classification_cost_usd, pages_acquired, model_version,
    taxonomy_version).
  - description rewritten to reference output_schema.py:109-142 and
    ALL_TIERS at 60-66.
  - schema_version pattern unchanged (`^1\.[0-9]+$` accepts both
    "1.0" and "1.1"). The 198 W4.2 files declare "1.0" but conform
    to v1.1 shape — historical artifact documented in §4.

- `tests/fixtures/META_SCHEMA.md`:
  - Header version line: meta.schema.json v1.0; expected.schema.json
    v1.1 (W4.3 bump 2026-05-21).
  - §2.4 deferred fix (a): nginx-401 partition reference corrected
    (C0.7c moved files OUT of parking_default_pages/ TO auth_403/ at
    commit 4f8dc06).
  - §2.4 deferred fix (b): replaced_in_place captured_at caveat added
    (git log --diff-filter=A returns ORIGINAL add-commit date).
  - §2.4 deferred fix (c): approximated_from_synthetic_invalid_fallback
    vocabulary entry added.
  - §3: rewritten with 18-col stage3_decision field-by-field table;
    includes deferred fix (d) tier_decided="parser_rule" vocab and
    deferred fix (f) output durability annotation.
  - §3.1: reframed as historical W4.0 design, superseded W4.3.
  - §4: current-state subsection added explaining the v1.1 state and
    the "schema_version": "1.0" historical artifact.
  - §5 line 149: nginx-401 + replaced_in_place fixes (mirroring §2.4).
  - §8: worked example rewritten — twilio.com.json now carries real
    W4.2 cascade outputs, not the W4.0 placeholder + sentinel.

All six deferred prose-only fixes (a)-(f) cleared from the register.

Validation: 198/198 expected.json files validate cleanly against the
v1.1 schema via jsonschema 4.26.0 (verified exhaustively).

Test counts at W4.3.B close: driver 46 passed; conformance 17/169/2
unchanged.

──────── Step C: rglob enumerator change (SKIPPED) ─────────────

Source-verification at cold-start showed the 3 nested international_
business/<locale>/ fixtures are ALREADY discoverable via the existing
per-locale parametrize functions (test_international_business_{de,jp,br}_
conformance at lines 402/418/434 of the conformance test). pytest
`--collect-only` confirmed all 3 currently collect; baseline shows all
3 currently PASS. The Session 14 handoff's predicted count shift
17/169/2 → 17/172/2 was an incorrect premise. Step C skipped per
operator decision after the verify-before-asking finding was surfaced.

──────── Step D: Conformance test augmentation ─────────────────

Commit `b2e2671` W4.3.D. One file touched: `tests/scraper/test_fixture_
conformance.py`.

Verify-before-asking finding surfaced during Step D scope elicitation:
the prompt's recommended "verdict-only" comparison option (compare
stage1/2/3_decision against committed expected.json) required running
the cascade, but the prompt also prohibited live LLM calls. AskUserQuestion
surfaced the tension; operator chose parser-level comparison instead.

Second verify-before-asking finding (Step D semantics correction): a
pure drift-test against committed expected.json would flip ALL 17 W5-
punch-list reds to green, because the W4.2 cascade-driver captured the
same parser output the live parser produces today (verified by inspecting
sanmarinoiron.com and archive.org committed expected.json directly).
AskUserQuestion surfaced this; operator chose "Augment, don't replace"
— keep the directory-semantic assertion (preserving the 17 reds) AND
add the drift check as a regression detector on top.

Implementation:
- Added `_HARD_EXCLUSION_KEYS` tuple (20 keys returned by extract_hard_
  exclusions, each mapping to parser_output["hard_exclusions_<key>"]
  in the consolidator-flattened expected.json).
- Added `_expected_parser_output(path)` helper that resolves
  tests/fixtures/html/<category>/expected/<domain>.json (or
  <category>/<locale>/expected/<domain>.json for nested locales) and
  returns the parser_output dict, or None when no expected.json
  exists (login_wall is validator-side).
- Extended `_block(path)` to run the drift check after computing
  extract_hard_exclusions. The drift check iterates the 20 keys and
  asserts live == committed-W4.2 with a diagnostic referencing
  commit cc2ba2c.
- Refactored test_international_business_{de,jp,br}_conformance to
  use _block(path) instead of extract_hard_exclusions(html, ...) inline,
  picking up the drift check uniformly.

Drift==zero across all 198 fixtures verified before refactor (placeholder-
domain output byte-identical to committed parser_output slice).

Test counts at W4.3.D close (acceptance criteria):
- Driver suite: 46 passed.
- Conformance suite: 17 failed, 169 passed, 2 skipped.
- 17 W5-punch-list red identities BYTE-IDENTICAL against Session 14
  baseline (verified via diff between /tmp/w4-3-baseline-reds.txt and
  /tmp/w4-3-close-reds.txt).

──────── Pre-push gate resolution ─────────────────────────────

Pre-push gate (ruff check / ruff format / vermin 3.10 / validate_
consistency) ran clean on the W4.3 surfaces. Initial validate_consistency
failed: row 102 of eval_data/stage1_labels.jsonl (thethinkacademy.com)
had duplicate 'testimonials' in rationale_keywords (introduced in
operator's unstaged work since Session 14 close, NOT by W4.3 commits).
Per LESSONS Session 6 "Push-blocking pre-push gates require operator
coordination": surfaced to operator with 4 disposition options.
Operator chose "fix row 102 manually, then rerun gate". Operator
deduplicated to `['testimonials', 'contact_sales', 'consumer_customers']`;
validate_consistency re-ran clean. Push to origin/main:
`cc2ba2c..b2e2671` landed. No `--no-verify` used.

──────── Capstone tag ─────────────────────────────────────────

Operator-authorized override of the Session 12 "no Week 4 sub-tag"
sequencing decision: placed annotated tag `workstream-0-week4-end` at
`b2e2671` (W4.3.D close). Annotation covers all of Week 4 (W4.0/W4.1/
W4.1.5/W4.2/W4.3), output durability constraints, Week 5 ahead, and
the cumulative cost-budget state ($0.26345 incurred / $99.74 remaining).
Tag pushed to origin.

──────── Operator decisions made during Session 15 ─────────────

1. Step A: path (a) schema bump v1.0 → v1.1 (over path (b) adapter).
2. Step C: skipped (operator agreed with source-verification finding
   that the 3 nested fixtures are already discoverable).
3. Step D comparison granularity: parser-level (over verdict-only
   cascade or hash-based).
4. Step D semantics correction (mid-session): "augment, don't replace"
   (over pure replacement that would flip 17 reds, or W4.3 halt).
5. META_SCHEMA scope: full path (a) bundle — all 6 deferred prose-only
   fixes (a)-(f) folded in (over minimum-scope or schema-only).
6. Pre-push gate resolution: operator-side fix (row 102 dedup), not
   stash / not --no-verify / not session-defer.
7. Week 4 capstone tag: PLACED at b2e2671 (overrode Session 12 "no
   sub-tag" sequencing decision; operator chose Week 4 marked complete).
8. Per-tier cost-accounting wiring gap (W4.3.X candidate): DEFERRED
   (low severity; total cost telemetry intact; per-tier breakdown is
   nice-to-have for future cost-envelope work).

──────── Patterns reinforced this session ─────────────────────

- **Verify-before-asking discipline (extension)** (LESSONS Session 12):
  surfaced FOUR distinct source-verification findings BEFORE acting on
  the prompt's premises:
  1. The 3 nested international_business fixtures are already
     discoverable (Step C premise incorrect).
  2. The W4.2 expected.json captures the broken state for all 17 W5
     reds (pure drift-test would flip them green).
  3. extract_hard_exclusions is fully domain-independent (placeholder
     "example.com" produces byte-identical output to actual-domain
     calls across all 198 fixtures).
  4. The schema_version pattern accepts both "1.0" and "1.1" — the
     198 W4.2 files don't need regeneration to validate against v1.1.
- **Driver-level input contracts** (LESSONS Session 12): re-read
  consolidate.py at session-current HEAD before scoping the schema
  bump, which surfaced that stage1_decision and stage2_decision are
  already in v1.0 triple shape (only stage3_decision diverged).
- **Confirm-to-commit gating** before W4.3.B, W4.3.D, and the
  workspace close-out commit.
- **File-based commit messages** at /tmp/W4.3.B-msg.txt and
  /tmp/W4.3.D-msg.txt.
- **No `Co-Authored-By`**.
- **Pre-push gate** ran clean on the W4.3 surfaces; resolved the
  operator-side blocker via operator action rather than --no-verify.
- **Push-blocking pre-push gates require operator coordination**
  (LESSONS Session 6) — surfaced the eval_data/ row 102 issue with
  4 disposition options instead of silently retrying.
- **Plan-as-read-only**: BARCADA_CRAWLER_REMEDIATION_PLAN.md unchanged
  this session.

No new LESSONS.md entries this session — all observed patterns were
instances of previously-established discipline.

──────── Workspace changes landed this session ────────────────

- `SESSION_LOG.md`: this entry (Session 15 append).
- `SESSION_TRANSITION_TEMPLATE.md`: refilled for Session 16 with W5 as
  next concrete work unit.

Repo changes:
- W4.3.B commit `7728bdf` (tests/fixtures/expected.schema.json +
  tests/fixtures/META_SCHEMA.md).
- W4.3.D commit `b2e2671` (tests/scraper/test_fixture_conformance.py).
- Annotated tag `workstream-0-week4-end` placed at `b2e2671` and
  pushed to origin.
- Pushed to origin/main: `cc2ba2c..b2e2671`.

Test counts at Session 15 close (verified):
- Driver suite (`tests/runners/fixture_cascade/`): 46/46 pass.
- Conformance suite (`tests/scraper/test_fixture_conformance.py`):
  17 fail, 169 pass, 2 skip (unchanged from Session 14 close;
  Week 5 punch list byte-stable in identity).
- 198/198 expected.json files validate clean against v1.1 schema.

──────── Cost & schedule tracking ─────────────────────────────

- Cost incurred Session 15: $0 (test-infrastructure refactor only;
  no LLM calls).
- Cost incurred Sessions 1-15 total: $0.26345 (all from W4.2 in
  Session 14).
- Budget remaining: $99.74.
- Schedule: Week 4 COMPLETE this session (all of W4.0/W4.1/W4.1.5/
  W4.2/W4.3 landed). Week 5 ahead.

Next session prompt: see `SESSION_TRANSITION_TEMPLATE.md`.
Next concrete work: Workstream 0 Week 5 — multipage_boilerplate
fixtures, multilingual parking, soft_404 + empty_google_sites
repopulation, edge-case robustness fixtures, and closure of the 17
W5-punch-list conformance reds via fixture work (NOT test-
infrastructure work; W4.3 closed the test-infrastructure surface).

## Session 16 — Workstream 0 Week 5 fixture-content closure (2026-05-21)

Scope: Engineering + fixture-sourcing session. Landed 5 of 6 W5
sub-surfaces per plan §3 Week 5 fixture-content scope. 8 repo
commits + 1 workspace commit + 1 annotated tag (`workstream-0-week5-
end` at `ddd3cb0`). LLM spend: $0.000208 (one Stage 1 LLM call in
the edge-case batch; all other sub-surfaces parser-level abstention).
Multipage_boilerplate (20 fixtures, plan §3 W5 line 241) deferred
to Session 17 per mid-session shape decision driven by context
budget.

──────── Cold-start verification at session open ───────────────

- Workspace HEAD `a42f982` matched outgoing template (Session 15 close).
- Repo HEAD `b2e2671` (W4.3.D conformance drift check).
- Tags verified: workstream-0-week4-end at b2e2671, workstream-0-
  week4-1-5-end at dd64963, reconciliation-2026-05-21-absorbed at
  ce7e8e9.
- 198 expected.json + 198 .html fixtures on disk.
- Driver intact at tests/runners/fixture_cascade/ (zero diff vs dd64963).
- Driver suite at session open: 46/46 passed.
- Conformance suite at session open: 17 failed / 169 passed / 2 skipped
  (the W5 punch list + the 2 empty-directory skips).
- Schema at v1.1 (18-col stage3); META_SCHEMA at v1.1 prose.

──────── Step A: W5 design-gate elicitation ────────────────────

Operator chose all four recommended options:
1. Ordering: Natural (C0.3+C0.4 repop → 17-red closure → new fixtures).
2. Sourcing: Real preferred, synthetic-with-real-markers DEFAULT.
3. Regeneration: Incremental per-batch (preserves W4.2 ground truth
   at cc2ba2c; defers full corpus regen to W A.0 W6 baseline-v0).
4. 17-red closure: Per-fixture decision (replace/recategorize/delete).

──────── Sub-surface 1: W5.C0.3-followup (commit 3ebbcf6) ──────

Repopulated soft_404/ with 6 synthetic-with-real-markers fixtures
(one per _RE_SOFT_404 alternation). Verify-before-asking surfaced
two findings:
1. soft_404 detail prefix routes to is_empty_page=True (not
   is_parked); the legacy test_soft_404_conformance assertion
   `is_parked is True` was inconsistent. Operator chose Option B:
   assertion realignment to `exclusion_reason == "soft_404"` (more
   semantically precise than the alternative is_empty_page).
2. _RE_EXPANDED_SOFT_404 (popular_searches / trending_searches /
   people_also_search_for) is defined twice in barriers.py but
   NEVER wired into is_placeholder_with_detail — dead-letter in the
   modern detection path. Documented in commit body; out-of-scope
   for W5 fixture work.

Test delta: 17/169/2 → 17/175/1 (+6 soft_404 fixtures, -1 skip).
Cost: $0 (all 6 parser-level abstention).

──────── Sub-surface 2: W5.C0.4-followup (commit 343f1f7) ──────

Repopulated empty_google_sites/ with 3 synthetic-with-real-markers
fixtures (one per _RE_GOOGLE_SITES alternation:
sites-viewer-frontend / atari.vw. / normalizedPath.*view/).
test_empty_google_sites_conformance calls is_empty_google_sites
directly (no _block indirection, no assertion realignment needed
this batch).

Test delta: 17/175/1 → 17/178/0 (+3, -1 skip). Both empty-directory
skips cleared. Cost: $0.

──────── Sub-surface 3: W5 17-red closure (5 commits) ──────────

Explore subagent produced per-fixture disposition table for 17 reds.
Operator chose: convert all 4 REPLACE candidates to DELETE (real-
domain recapture with JS execution is Playwright-tier, out-of-scope
per W4.1.5 driver lock); jvns.ca → spa_shell/ recategorize; 5
commits one per affected directory.

Disposition tally: 13 DELETE + 4 RECATEGORIZE.

Commits:
- W5.red-closure-spa_shell (dcfcdf3): sanmarinoiron→legit_business
  + 2 deletes. 17→14/179.
- W5.red-closure-auth_403 (917af20): 2 recategorizes
  (ssptjp→legit_business, ssquaresemi→spa_shell) + 5 deletes.
  14→7/181.
- W5.red-closure-legitimate_business (d4e9f67): 4 deletes (all
  REPLACE→DELETE conversions). 7→3/181.
- W5.red-closure-legitimate_blog (225bec5): jvns.ca→spa_shell +
  danluu delete. 3→1/182.
- W5.red-closure-legitimate_nonprofit (145d2eb): archive.org
  delete. 1→0/182.

All 17 W5-punch-list reds closed via fixture-content work. Cost: $0
(no cascade runs; existing expected.json moved with recategorized
fixtures; drift check passes on byte-identical .html pre/post move).

──────── Sub-surface 4: W5.multilingual (commit 2b518b2) ────────

Added 3 parking_multilingual fixtures (Russian, Chinese, Japanese).
Each <1000 bytes → Tier 2 short_body secondary signal → parking_
multilingual detail prefix → is_parked=True.

Test delta: 0/182/0 → 0/185/0. Cost: $0.

Pre-push gate blocked initially on operator-side eval_data/
stage1_labels.jsonl row 161 (rationale_keywords too long, Session
15-precedent operator-side blocker). Operator fixed manually;
gate cleared.

──────── Sub-surface 5: W5.X-driver-test-realign (commit 8d0fc0e) ──

Latent verify-before-asking finding: I had been running ONLY
test_fixture_conformance.py during the 17-red closure work, not
the combined driver+conformance suites. test_real_corpus_index_
covers_198_fixtures (tests/runners/fixture_cascade/test_fixture_
fetcher.py:309) asserts len(index) >= 198; after the 17-red
closure deletes pushed corpus to 196 (commit d4e9f67), the
assertion broke. Surfaced after W5.multilingual landed and I ran
the combined suite.

Operator-authorized as its own W5.X commit (per cold-start
"its own commit, not bundled with W5 fixture work" pattern for
driver-locked-but-needs-realignment changes). Floor lowered
from 198 to 195. Driver suite restored: 45/1 → 46/0.

──────── Sub-surface 6: W5.edge-case (commit ddd3cb0) ──────────

Added 5 edge-case robustness fixtures to a new edge_case_robustness/
directory:
- huge_html_synthetic.html (1.13 MB; soft_404 marker for parser
  abstention while still stressing _extract_text on the full body)
- tiny_with_meaningful_content_synthetic.html (1.2 KB, Refinement 4
  positive-signal path)
- malformed_unclosed_tags_synthetic.html (unclosed tags; routes to
  empty_page after regex-strip)
- big5_declared_utf8_actual_synthetic.html (declared-vs-actual
  encoding mismatch)
- shiftjis_declared_utf8_actual_synthetic.html (mirror for Japanese)

Huge fixture generated via inline Python in Bash (not Write tool)
to avoid adding ~1MB of content to main conversation context — a
context-discipline pattern worth noting for future large-fixture
work.

New conformance test: test_edge_case_robustness_conformance —
shape-correctness + drift check via _block helper. Asserts all 20
_HARD_EXCLUSION_KEYS present in the extract_hard_exclusions output;
the drift check enforces value-stability against the cascade-
captured expected.json. COVERED set updated to include
edge_case_robustness.

Cascade run: $0.000208 (1 Stage 1 LLM call across 3 escalating
fixtures; embedding + completion roundtrip). 2 of 5 fixtures
parser-level abstention; 3 escalated to Stage 1 then classified
non-business early.

Test delta: 0/185/0 → 0/190/0 conformance; 46/0 driver; combined
236/0/0.

──────── Multipage_boilerplate deferral ─────────────────────────

Session-shape AskUserQuestion at mid-session: operator chose
"multilingual + edge-case + close-out, defer multipage". Plan §3
W5 line 241 spec (20 fixtures = 5 domains × 4 pages) is heavier
than fits remaining context. Carried forward to Session 17 as
W5 carry-forward, with W A.0 W6 to follow per operator's
next-session framing decision.

──────── Operator decisions made during Session 16 ─────────────

1. Step A all 4 recommended options (Natural ordering, real-preferred
   sourcing, incremental regen, per-fixture red closure).
2. soft_404 assertion realignment: Option B (exclusion_reason ==
   "soft_404") over is_empty_page or detector wiring or deferral.
3. 17-red 4 REPLACE → DELETE conversion (over synthetic substitution,
   real-domain recapture, or REPLACE-deferral).
4. jvns.ca → spa_shell (detector signal alignment over DELETE).
5. 5 per-directory red-closure commits over 1 bundled or 17 per-
   fixture commits.
6. Pre-push gate row 161 resolution: operator-side fix (Session 15
   precedent).
7. W5.X-driver-test-realign authorized as its own commit (test in
   driver directory needs corpus-reality alignment).
8. Session shape: multilingual + edge-case + close-out; defer
   multipage_boilerplate.
9. W5 capstone tag PLACED at ddd3cb0 (operator authorized).
10. Session 17 framing: multipage_boilerplate first (as W5 carry-
    forward), then W A.0 W6.

──────── Patterns reinforced this session ─────────────────────

- Verify-before-asking discipline (LESSONS S12): caught two major
  issues — the soft_404 assertion mismatch BEFORE authoring fixtures,
  and (less elegantly) the driver-test corpus-count assertion AFTER
  the 17-red closure work was already committed.
- Sub-agent delegation for per-fixture analysis: Explore subagent
  produced the 17-red disposition table in one focused call,
  preserving main-context budget.
- Context-discipline for large fixtures: generating the 1.13 MB huge
  fixture via inline Python in Bash kept it out of main conversation
  context.
- LESSONS S6 push-blocking pre-push gate: row 161 eval_data/ blocker
  resolved via operator-side fix (no --no-verify).
- LESSONS S8 synthetic-fixture HTML comment regex-visibility: all
  Session 16 fixture comment headers reviewed for anti-trip.
- W5.X-prefix for driver-locked-but-authorized changes (analogous
  to the W4.3.X deferred per-tier cost-accounting patch).

──────── New LESSONS entry candidate ──────────────────────────

"Combined-suite verification at every fixture-affecting commit":
during the 17-red closure work I ran only test_fixture_conformance.py
after each commit, not the combined driver+conformance suite. The
test_real_corpus_index_covers_198_fixtures driver-suite assertion
broke latent at commit d4e9f67 (corpus dropped to 196) and was only
surfaced after W5.multilingual landed. Forward discipline: run
BOTH suites (driver + conformance) at every fixture-affecting
commit, not just the directly-affected one. Costs 30-40s of test
runtime; saves a multi-commit verify-after-the-fact reconciliation
cycle.

──────── Workspace changes landed this session ────────────────

- SESSION_LOG.md: this entry (Session 16 append).
- SESSION_TRANSITION_TEMPLATE.md: refilled for Session 17 (multipage
  carry-forward, then W A.0 W6).

Repo changes (8 commits + 1 tag):
- W5.C0.3-followup 3ebbcf6
- W5.C0.4-followup 343f1f7
- W5.red-closure-spa_shell dcfcdf3
- W5.red-closure-auth_403 917af20
- W5.red-closure-legitimate_business d4e9f67
- W5.red-closure-legitimate_blog 225bec5
- W5.red-closure-legitimate_nonprofit 145d2eb
- W5.multilingual 2b518b2
- W5.X-driver-test-realign 8d0fc0e
- W5.edge-case ddd3cb0
- Tag: workstream-0-week5-end at ddd3cb0

Pushed to origin/main: b2e2671..ddd3cb0; tag also pushed.

Test counts at Session 16 close (verified):
- Conformance: 190 passed / 0 failed / 0 skipped
- Driver suite: 46 passed / 0 failed
- Combined: 236 passed / 0 failed / 0 skipped
- All 198/198 (+ new W5 additions) expected.json validate against v1.1 schema
- Corpus: 202 .html fixtures (was 198 at W4.1)

──────── Cost & schedule tracking ─────────────────────────────

- Session 16 LLM spend: $0.000208 (W5.edge-case 1 Stage 1 call).
- Sessions 1-16 cumulative: $0.263658.
- Budget remaining: $99.736.
- Schedule: Week 5 substantially complete (5 of 6 sub-surfaces).
  Session 17 = W5 wrap-up (multipage_boilerplate, 20 fixtures,
  estimated $0.026 marginal cost), then W A.0 W6 baseline-v0
  scaffolding.

Next session prompt: see `SESSION_TRANSITION_TEMPLATE.md`.
Next concrete work: W5.multipage_boilerplate as W5 carry-forward,
then W A.0 W6 baseline-v0 CLI scaffolding per plan §4 W6.
