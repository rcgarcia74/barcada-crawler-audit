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
