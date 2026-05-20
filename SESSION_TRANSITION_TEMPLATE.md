# Session Transition Template — Handoff from Session 8 → Session 9

This file is the handoff document filled out at the end of one Claude
Code session for the next session to read first. Overwritten at each
transition (use git history to recover prior handoffs). Sessions 1-7
are summarized in SESSION_LOG.md; Session 8 close is in the most
recent SESSION_LOG.md entry.

Pair this with the latest entry in `SESSION_LOG.md`, with
`LESSONS.md`, and with the relevant section of
`BARCADA_CRAWLER_REMEDIATION_PLAN.md` to start a session cold and
be productive within ~10 minutes.

---

## Handoff metadata

- Outgoing session number: 8
- Closing date: 2026-05-20
- Outgoing session scope: Workstream 0 Week 3 first half (C5
  international + C22 nonprofit, 6 fixtures + 1 conformance test
  extension). Closes the C5 + C22 portion of Week 3. Session 8
  intentionally split per the §14 context-window discipline; C18
  and C7 carried forward to Session 9.
- Reason for transition: planned scope split (recommended in
  the Session 7 → 8 handoff), executed cleanly. Context at
  Session 8 close ~62% used — within the §14 threshold but the
  natural breakpoint between the C5 / C22 inverted-detector work
  and the C18 / C7 spec-revisiting work makes a session change
  the cleaner option.

---

## Repository state — `/Users/administrator/projects/barcada-scraper/`

- Branch: `main`
- Last commit SHA: `17e92f8`
- Last commit subject: `C5.d: extend test_fixture_conformance.py
  with international_business per-locale tests (Week 3 close)`
- Branch sync with `origin/main`: 0 commits ahead, 0 commits behind
- Tags (do NOT move):
  - `pre-remediation-2026-05-19` at `3cbb9b3` (nuclear-revert anchor)
  - `workstream-0-week1-end` at `4f9d23f` (Week 1 close)
  - `workstream-0-week2-end` at `e5d2f91` (Week 2 close)
  - **NO** workstream-0-week3-end tag yet — Week 3 only half-complete
    (C5 + C22 shipped, C18 + C7 pending). Tag at end of Session 9
    only after the full Week 3 scope lands.
- Pre-push gate state at HEAD: ALL CHECKS PASS (ruff check, ruff
  format --check, vermin --target=3.10-, validate_consistency for
  eval_data)
- Unstaged changes intentionally ignored across sessions (operator-
  side work in the locked tree):
    .claude/rules/code-correctness.md
    eval_data/README.md
    eval_data/TAXONOMY_GAP_LOG.md
    eval_data/stage1_labels.jsonl

---

## Workspace state — `/Users/administrator/crawler-audit/`

- Branch: `main`
- Last commit SHA: TBD (filled in after this session's transition
  commit pushes; will be one commit ahead of `0872e97` which was
  the most recent Session 7 commit)
- Last commit subject: Session 8 close: C5 + C22 Week 3 first
  half + SESSION_TRANSITION_TEMPLATE.md refill for Session 9
- Branch sync with `origin/main`: 0 commits ahead (after push)

---

## Active task list

The Session 8 task list (#1-#5) is fully complete:
- #1 C5.a (.de): siemens.de.html landed
- #2 C5.b (.jp): hitachi.co.jp.html landed
- #3 C5.c (.com.br): locaweb.com.br.html landed
- #4 C22.a-c (nonprofit): wikimediafoundation + doctorswithoutborders
  + synthetic_educational_organization all landed
- #5 conformance test extension (C5.d): COVERED + 3 per-locale
  test functions added; final test surface 17 failed / 161 passed
  / 2 skipped

Task state is session-local in Claude Code; it does NOT carry across
sessions.

Session 9 should TaskCreate fresh tasks on open for the rest of
Week 3:

- **C18.0 (NEW, prerequisite)**: Probe-before-lock prevalence
  probe of 4-6 modern SaaS marketing sites (Stripe, Notion, Linear,
  Vercel, HubSpot, Webflow) for JSON-LD `@type=Organization`,
  hreflang, canonical, and mega-menu presence. If `@type=Organization`
  prevalence is <50% (matching the 4 prior production-extinction
  patterns), escalate spec revision rather than locking. **Do not
  skip this step** — the probe-before-lock discipline applies to
  C18 with extra force given the 4 prior extinction findings.

- C18.a-e: 5 modern SaaS fixtures extending
  `tests/fixtures/html/legitimate_business/` with hreflang +
  canonical + JSON-LD Organization (or whatever the probe reveals
  as the dominant pattern) + mega-menu + blog link. Each
  per-fixture commit (C18.a, C18.b, ...).

- C7.a-c: 3 mega-menu fixtures into new
  `tests/fixtures/html/mega_menu/` with `aria-haspopup` +
  multi-column nested `<ul>` panels. Each per-fixture commit
  (C7.a, C7.b, C7.c).

- Conformance test update (mirror of C1.5 / C5.d): add `mega_menu`
  to COVERED, add `test_mega_menu_conformance` function asserting
  the audit's mega-menu markers (`aria-haspopup` + nested-ul
  density). legitimate_business already has a conformance test;
  C18 fixtures auto-pass via parametrize unless the per-locale
  hreflang check pattern from C5.d is also wanted for the i18n
  ones (operator decision at session open).

Suggested total: 8 fixtures + 1 conformance commit = 9 commits.
Closes Workstream 0 Week 3. Tag `workstream-0-week3-end` at the
final SHA where the pre-push gate is green.

---

## Outstanding operator-input requests blocking Session 9

None. Session 9 can begin C18.0 (probe-before-lock for modern SaaS
JSON-LD) immediately. The probe-before-lock discipline is now
established practice across both this session and Session 7 — apply
without re-asking, but surface findings if a 4th-or-5th production-
extinction emerges.

---

## Operator decisions made during Session 8 that are recorded
in SESSION_LOG.md + LESSONS.md

- **C5.a** — siemens.de picked. Real .de TLD, lang=de-DE, 39
  hreflangs (regional English only — no bare `hreflang="en"`),
  JSON-LD WebPage with nested Organization references.
- **C5.b** — hitachi.co.jp picked. Closes the bare-`hreflang="en"`
  gap left open by C5.a (siemens uses regional codes only).
- **C5.c** — locaweb.com.br picked. .com.br TLD probing was
  harder than .de or .co.jp — three .com.br banks/manufacturers
  bot-blocked, two largest Brazilian-content sites use .com TLDs.
  Locaweb won on archetype match (private B2B SaaS) + richest
  JSON-LD (3 blocks: FAQPage, WebSite/SearchAction, Organization).
- **C22.a/b** — wikimediafoundation.org and doctorswithoutborders.org
  picked (audit's named candidates).
- **C22.c** — Synthetic-with-real-markers per §11 fallback. Probe
  of 9 educational candidates found 0/9 shipping
  `@type=EducationalOrganization` in 2026 production — fourth
  production-extinction finding since Session 7. Synthetic
  authored with literal `@type=EducationalOrganization` schema.
- **New LESSONS.md entry**: "Synthetic-fixture HTML comments are
  regex-visible" — the C22.c WAF false-positive lesson.
- **Plan is read-only**: unchanged from Session 7 (memory:
  `feedback_remediation_plan_readonly.md`).

---

## Locked artifacts reminder (CRITICAL — do not modify)

- All of `eval_data/` — locked. Read-only context only. Includes
  `eval_data/canary_50_domains.txt`.
- `stage1.schema.json` v1.0 / 49 keywords — locked.
- `pre-remediation-2026-05-19` tag at `3cbb9b3` — do not retag or
  move.
- `workstream-0-week1-end` tag at `4f9d23f` — do not move.
- `workstream-0-week2-end` tag at `e5d2f91` — do not move.
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` — read-only, period. All
  deviations from the plan land in SESSION_LOG.md and LESSONS.md.
- The 17 fixtures on the Week 5 cleanup punch list (see
  SESSION_LOG.md Session 6 entry) — DO NOT touch in Session 9.

---

## Next concrete work unit

- **Action ID:** **C18.0** (prerequisite prevalence probe before
  any C18 capture). NOT a numbered audit candidate — this is the
  probe-before-lock step established as standing discipline.
- **Scope:** Probe 4-6 modern SaaS marketing sites (suggested:
  stripe.com, notion.so, linear.app, vercel.com, hubspot.com,
  webflow.com — vercel was already captured for C1.1.c so probe
  fresh or reuse). Report per-site:
    - JSON-LD `@type=Organization` presence
    - hreflang block presence
    - canonical link presence
    - mega-menu marker presence (aria-haspopup, multi-column
      nested ul)
- **Acceptance criteria:**
  - 4-6 candidate URLs probed with the retry-on-TLS-error policy
    per LESSONS.md (≥3 attempts on failure)
  - Per-site prevalence table presented to operator
  - **If JSON-LD @type=Organization prevalence is <50%**: STOP
    and escalate per LESSONS.md Step 6. Surface a spec-revision
    recommendation analogous to C1.1 / C1.2 / C1.3 / C1.4 / C22.c
    decisions. Do not proceed to C18.a until the operator decides
    on the revised spec.
  - **If prevalence is ≥50%**: proceed to C18.a candidate
    presentation as the standing pattern.
- **Files expected to be touched:** none (probe-only step;
  candidate captures land in /tmp/, not the repo)
- **Files NOT to be touched:** everything under `eval_data/`,
  `stage1.schema.json`, the tags, `BARCADA_CRAWLER_REMEDIATION_PLAN.md`,
  and the 17 Week-5 punch-list fixtures.

---

## Required reading (Session 9 first 10 minutes)

In this order:
1. **This file** (you're reading it).
2. **`LESSONS.md`** (workspace) — operator patterns and observed
   conventions, INCLUDING the new "Synthetic-fixture HTML comments
   are regex-visible" entry and the "Probe framework generation
   before locking a fixture spec" entry from Session 7.
3. **`SESSION_LOG.md` Session 8 entry** — what just shipped, the
   fourth production-extinction finding (EducationalOrganization
   0/9 in production), the C22.c synthetic-with-real-markers
   resolution, the 7 commits, the conformance test extension.
4. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §3 Week 3** — C18
   modern SaaS + C7 mega-menu specs. READ-ONLY.
5. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §11 Risk Register** —
   "Recapture tooling needs retry policy" still applies.
6. **`FIXTURE_AUDIT_REPORT.md` §12** — C7 (mega_menu) and C18
   (legitimate_business expansion) detailed specifications.
7. **`BARCADA_CRAWLER_REMEDIATION_PLAN.md` §14 Session Continuity
   Discipline** — referenced for Session 9 close-out cadence.

After reading, verify repo state:

```
git -C /Users/administrator/projects/barcada-scraper status
git -C /Users/administrator/projects/barcada-scraper log --oneline -3
```

Last commit SHA must be `17e92f8` (C5.d). If anything differs,
surface to operator before doing work.

Then begin C18.0 (the prevalence probe). DO NOT skip the probe —
the 4 prior extinction findings make this discipline non-optional.

---

## Risk register state (plan §11)

Recent additions (set during Session 4, applied through Session 8):
- "Recapture tooling needs retry policy" — STILL applies to every
  Session 9 capture.
- Forward-applicable lessons in LESSONS.md (plan is read-only, so
  they cannot land in §11 itself):
  - "Probe framework generation before locking a fixture spec"
    (Session 7) — applies to C18 with extra force.
  - "Synthetic-fixture HTML comments are regex-visible" (Session 8)
    — applies to C18 if synthetic fixtures are needed, and to all
    future synthetic capture work.

Open latent gap (Issue 3 from Week 2 audit erratum, unchanged):
- Project's ruff `select` does not include "C" (mccabe), so
  cyclomatic-complexity violations escape pre-push. Manual `ruff
  check --select C901 tests/scraper/test_fixture_conformance.py`
  in any conformance commit is the workaround until a project-
  config commit closes the gap.

No new risks escalated and unresolved by Session 8.

---

## Cost & schedule tracking

- Cost ceiling: $100 (operator-set 2026-05-19, alert at $50)
- Cost incurred Sessions 1-8: $0 (no LLM API calls; curl + pytest
  + handwritten synthetic only)
- Cost budget remaining: $100
- Schedule: 3 weeks elapsed of Workstream 0's 5-week budget.
  Weeks 1-2 complete; Week 3 ~60% complete (C5 + C22 shipped,
  C18 + C7 carried). Weeks 3 remainder, 4, 5 still ahead.

---

## Notes for Session 9

- **Conformance test red count at handoff is 17** (Week 5 punch
  list, unchanged from Week 1 close). Every Session 9 commit
  should verify the count stays at 17 unless the commit itself
  adds a known-failing fixture (which Week 3 work should not).
- **2 conformance tests SKIP** (empty parametrize for `soft_404/`
  and `empty_google_sites/`) — both await Week 5 C0.3-followup /
  C0.4-followup repopulation.
- **When Session 9 creates the first `mega_menu/` directory**,
  the catch-all `test_every_fixture_directory_has_a_test` WILL
  fail because COVERED doesn't include the new dir. Same dynamic
  as Session 7 C1.1.a and Session 8 C5.a. Add `mega_menu` to
  COVERED in the same commit OR roll into a Week-3-close
  conformance commit (mirror of C1.5 / C5.d).
- **File-based commit messages** still mandatory: heredocs break
  on apostrophes. Use `Write` to `/tmp/<action-id>-msg.txt`, then
  `git commit -F /tmp/...`. Pattern in LESSONS.md.
- **"Confirm to commit?" gating** before every commit — established
  pattern.
- **"Verify BEFORE asking for commit confirmation"** — Session 8
  hardened this discipline; the operator asked "did you double
  check your work?" multiple times. The standing rule is: every
  "Confirm to commit?" implies "and yes, the verification table
  was generated from the on-disk file by re-parsing it before
  drafting the message." Two precision errors caught in C5.a as
  a result of relaxing this; subsequent commits ran the full
  verification up-front.
- **Synthetic-fixture authoring** (if Session 9 needs one for C18):
  follow the LESSONS.md anti-trip discipline for the HTML comment
  header AND run `extract_hard_exclusions(html, "example.com")`
  before commit to verify `exclusion_reason=''`. Per-branch
  pattern sweep of `_RE_WAF_CHALLENGE`, `_RE_CLOUDFLARE_CHALLENGE`,
  `_RE_PARKING_JS`, etc. is the surest verification.
- **Shell cwd drift**: same warning as Session 8 — use absolute
  paths or `cd /Users/administrator/projects/barcada-scraper` at
  the start of each Bash chain.
- **Pre-push gate may include validate_consistency failure** from
  operator-side eval_data work. The 4 unstaged operator-side
  files in the locked tree are documented and routinely pass the
  gate; if the gate fails, STOP and ask the operator. Never use
  `--no-verify`.
- **Plan is read-only** — never edit
  `BARCADA_CRAWLER_REMEDIATION_PLAN.md`. Memory saved as
  `feedback_remediation_plan_readonly.md`.
- This template's structured fields will need refilling at
  Session 9 close. Read plan §14 again if uncertain.
