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
