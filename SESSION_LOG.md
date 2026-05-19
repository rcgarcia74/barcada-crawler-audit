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
