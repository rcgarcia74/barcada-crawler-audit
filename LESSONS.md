# Lessons & Observed Conventions

Patterns and conventions observed during the barcada-scraper audit
and remediation work. Each entry: pattern statement, when it applies,
and the session/commit where it was established (so conversation
context can be recovered if needed).

This file is append-only. New conventions land at the bottom. Older
entries are not edited; if a convention evolves, write a new entry
that supersedes by referencing the older one.

Future Claude Code sessions: read this file in your first 10
minutes. It captures patterns that live in conversation memory of
prior sessions and would otherwise be lost across the transition.

---

## Operator interaction patterns

### "Confirm to commit?" before every commit

**Established:** Sessions 4-6 (every commit).

The operator does not auto-approve commits. After staging changes
and drafting a commit message, ALWAYS present the message and ask
"Confirm to commit?" before running `git commit`. This applies to
both repo and workspace commits. Project CLAUDE.md codifies this:
"Never commit or push automatically — always wait for my
confirmation."

### File-based commit messages, not heredocs

**Established:** Session 5 (during C0.3).

The pattern `git commit -m "$(cat <<'EOF' ... EOF)"` breaks on
apostrophes inside the message body (e.g., `audit's reading` fails
with shell EOF errors). Use the `Write` tool to put the commit
message in `/tmp/<action-id>-msg.txt`, then
`git commit -F /tmp/<action-id>-msg.txt && rm /tmp/<action-id>-msg.txt`.
This is the durable pattern for any non-trivial commit message.

### Commit message body must include

**Established:** Sessions 4-6.

- Action number reference (C0.1, C0.7a, C1.1.b, etc.)
- pytest result line (e.g., `pytest tests/scraper/test_*.py:
  43 passed in 0.49s`)
- For fixture changes: per-directory conformance check result
- Reference to plan section that owns this action (`Refs:
  BARCADA_CRAWLER_REMEDIATION_PLAN.md §3 Week N`)

### No `Co-Authored-By` line

**Established:** Session 5 (after C0.1 was committed with one).

Operator rule lives in `.claude/rules/code-correctness.md`. Do not
add `Co-Authored-By: ...` lines to commit messages. C0.1 (`96dcbfd`)
has one; all subsequent commits do not.

### Push-blocking pre-push gates require operator coordination

**Established:** Session 6 (Days 3-5 close).

The barcada-scraper repo's pre-push hook runs ruff check, ruff
format --check, vermin, and validate_consistency (eval_data) against
the working tree. Two consequences:

1. **Ruff format** can block on formatting that you thought was
   fine. Run `ruff format --check <file>` before assuming a commit
   is push-ready. C0.8-format-fix (`4f9d23f`) was a follow-up to
   C0.8 (`684a9ba`) because of this.

2. **validate_consistency** validates eval_data/ against
   `stage1.schema.json`. If the operator has in-progress unstaged
   edits to `stage1_labels.jsonl` that violate the schema (e.g.,
   missing `labeler_id`), the gate fails — even though those
   changes are not in your commits. STOP and ask the operator to
   fix or stash. NEVER use `--no-verify` without explicit operator
   authorization; the brief disallows it.

## Fixture-handling patterns

### Delete > Move when destination doesn't cleanly fit

**Established:** Session 6 (C0.7a `f51ca15`, C0.7d `7b9fa60`).

When an audit recommends moving a misclassified fixture to a
different directory, first verify the destination directory's
detector actually matches the fixture's content. If not (audit
hedges with "or new XXX/" alternatives), prefer DELETE rather than
relocating non-conformance to a different directory. The fresh
captures from later workstreams (C18 modern SaaS, C22 nonprofits,
etc.) will produce properly-conforming fixtures.

Worked examples:
- C0.7a: `spa_shell/bestmakeupsale.com.html` (51 B GMO parking
  script) — audit said `→ parking_redirect_targets/ or new
  parking_gmo/`. Neither cleanly fits. Decided: delete.
- C0.7d: `parking_errors/bestmactips.com.html` (Cloudflare 526) —
  audit said `→ cloudflare_challenge/ or new cloudflare_5xx/`.
  Doesn't match `_RE_CLOUDFLARE_CHALLENGE`. Decided: delete.

### Batch same-decision moves, per-file different-decision moves

**Established:** Session 5 (C0.5a/b/c/d split per-file) +
Session 6 (C0.7c batch).

- If multiple fixtures have the SAME decision (same move target,
  same reason), batch them into one commit. C0.7c (`4f8dc06`)
  moved 4 nginx-401 files in one commit because the decision was
  identical for all (same source dir, same target dir, same
  classification reasoning).
- If fixtures have DIFFERENT decisions (delete vs replace vs
  accept-with-notes), split per-file. C0.5a/b/c/d (`b7089eb`,
  `3dec85b`, `45bbe30`, `26771e9`) split because each file's
  resolution was different.

### Synthetic-with-real-markers fallback for capture failures

**Established:** Session 4 (plan §3 Week 5 + §11).

If real-domain capture fails for a fixture target (no production
examples available, persistent anti-bot block, persistent TLS
error after ≥3 retries), synthetic HTML with real detector markers
is an acceptable substitute — same pattern as the existing 20
`*_synthetic.html` files already in the corpus. Document
`capture_method: "synthetic_with_real_markers"` when meta.json
infrastructure lands (Week 4). Synthetic is not a permanent state;
flag for quarterly re-capture.

### Truncated-fixture audit pattern

**Established:** Session 5 (C0.5 truncation suspects).

Power-of-2 sizes (8192, 32768, 65536, 131072, 200000-byte caps)
strongly suggest hard byte ceilings during the original capture.
Before deleting, recapture and inspect the tail bytes. If the new
capture is a CLEAN page that ends with `</html>`, replace in place.
If the recapture reveals the fixture was misclassified (truncation
hid the true content type — e.g., truncated e-commerce site looks
like SPA shell), delete from the wrong directory; the fresh
capture goes to the correct directory in a later commit.

Worked examples (all from Session 5 C0.5 series):
- `spa_shell/shelterstoreau.com.html` (200000 B exact) — recapture
  revealed real e-commerce site, not SPA shell. Deleted (C0.5a).
- `parking_sale/shelvs.com.html` (32752 B) — recapture clean,
  still parking_sale. Replaced in place (C0.5c).
- `legitimate_business/sanmarcosflowershop.com.html` (32752 B) —
  first recapture attempt got transient TLS error, leading to
  initial "accept with notes" (C0.5d). Retry probe showed
  transient, recapture succeeded (C0.5d-followup).

## Diagnostic patterns

### Retry-on-connection-error policy (≥3 attempts)

**Established:** Session 5 (C0.5d → C0.5d-followup). Codified in
plan §11 Risk Register.

Single-attempt curl / network probes are NOT sufficient for
diagnosing whether a TLS, DNS, or connection failure is persistent
vs transient. Always retry ≥3 times before drawing a "persistent
breakage" conclusion.

Specific empirical case: a single TLS failure on
sanmarcosflowershop.com looked persistent, but 3-attempt probe
revealed 1 fail + 2 success (transient). The lesson: future
recapture tooling must build retry into the standard capture
flow, not as a one-off probe.

For Week 2 SPA hydration captures and any future capture work,
the pattern is:

```bash
for attempt in 1 2 3; do
  curl -sSL -A "$UA" -o "$out" "$url" && break
  sleep $((2 ** attempt))
done
```

(Plus appropriate exit-code checking.)

### Probe framework generation before locking a fixture spec

**Established:** Session 7 (C1.1 escalation, 2026-05-19).

Audit / plan fixture specifications that name a hydration marker
(`__NEXT_DATA__`, `window.__NUXT__`, `__APOLLO_STATE__`,
`__PRELOADED_STATE__`, etc.) can fossilize a pattern that has been
superseded by a subsequent major framework version. Before
sourcing fixtures for a framework-named directory, run an
empirical 4-6 candidate probe of well-known production sites for
that framework and verify the marker actually appears.

Worked example (Session 7 C1.1): the FIXTURE_AUDIT_REPORT.md §12
C1 spec targeted `__NEXT_DATA__` in CSR/ISR/SSR variants. A
6-site probe revealed 3/6 sites ship App Router RSC streaming
(`self.__next_f.push([...])`, no `__NEXT_DATA__`), 1/6 ships
`__NEXT_DATA__` only, 2/6 ship neither. Next.js 13 (October 2022)
made App Router the default; by 2026 the production ecosystem is
dominantly App Router. Spec was revised to a hybrid (1 Pages-
Router + 2 App-Router) per operator decision recorded in
SESSION_LOG.md Session 7.

Forward-applicable to C1.2 (Nuxt 2 `window.__NUXT__` vs Nuxt 3
`<script id="__NUXT_DATA__">`), C1.3 (Apollo Client 2 vs 3
state-streaming differences), C1.4 (`__PRELOADED_STATE__` vs
modern state-management libraries), and any future framework-
marker fixture work (Remix, Gatsby, SvelteKit, Astro, etc.).

The probe script (reuse from C1.1):

```bash
# /tmp/c1_probe.sh from Session 7 — retry-on-TLS-error capture.
# /tmp/c1_classify.py from Session 7 — parse the marker payload,
#   report shape (parses / bytes / variant signals).
for url in "${CANDIDATE_URLS[@]}"; do
  /tmp/c1_probe.sh "$url" "/tmp/probe_$(basename "$url").html"
  python3 /tmp/c1_classify.py "/tmp/probe_$(basename "$url").html"
done
```

Cost: 5-10 minutes per framework. Cost of skipping: shipping a
detector against an obsolete pattern that misses the dominant
production reality.

### Conformance check ritual after every fixture change

**Established:** Sessions 5-6.

After every fixture deletion, move, or replacement:

1. Run pytest on `tests/scraper/test_hard_exclusions.py` (sanity
   net; passes only mean nothing gross broke).
2. Manual or scripted grep of the affected directory against its
   detector's actual regex markers (from `placeholder.py` /
   `barriers.py`).
3. Report both results in the commit message.

Do NOT trust pytest alone — pre-C0.8 it only covers
`sorted(glob)[0]`-selected fixtures; even post-C0.8 only some
directories are parametrized. For full enumeration, use
`tests/scraper/test_fixture_conformance.py` (C0.9).

### Audit-spec vs. production-reality drift

**Established:** Session 9 (C7 mega-menu probe, 2026-05-20). Pattern
first observed in Session 7 (C1.1 Next.js App Router).

The fixture audit and remediation plan contain literal HTML / attribute
examples drawn from a point-in-time snapshot of the production
ecosystem. Two distinct cases of audit-named markers having drifted to
different production patterns have surfaced in two weeks:

**Drift case 1: Next.js hydration marker (Week 2 / Session 7 C1.1).**
The audit / plan C1 spec named `__NEXT_DATA__` as the Next.js
hydration marker. A 6-site probe of well-known Next.js production
sites revealed that App Router (introduced in Next.js 13, October
2022) had become the dominant pattern: 3 of 6 sites ship App-Router
RSC streaming (`self.__next_f.push([...])`, no `__NEXT_DATA__`), 1 of
6 ships `__NEXT_DATA__` only (Pages Router), 2 of 6 ship neither.
Resolution recorded in SESSION_LOG.md Session 7 entry: the C1 fixture
set was revised to a hybrid (1 Pages Router + 2 App Router) so the
detector has known-positive examples for both patterns.

**Drift case 2: C7 mega-menu ARIA marker (Week 3 / Session 9).**
The fixture audit §12 C7 example wording specified
`aria-haspopup="menu"` (literal value) for the Shopify-style mega-menu
slot. Probe of the audit's three named candidates (Shopify, Salesforce,
Microsoft) revealed:

| Site | aria-haspopup hits | values |
|---|--:|---|
| shopify.com | 1 | `"true"` (no literal `"menu"`) |
| salesforce.com | 11 | `"true"` (no literal `"menu"`) |
| microsoft.com | 0 | (none — uses aria-controls + aria-expanded instead) |

`aria-haspopup="true"` is the WAI-ARIA 1.1+ shorthand for
`aria-haspopup="menu"` — same semantic, different attribute value.
Both are valid markers indicating a button triggers a popup menu, but
the audit's literal example string is no longer dominant. The audit
itself anticipated three distinct mega-menu archetypes (Shopify-style /
Salesforce-style / Microsoft-style) with different attribute patterns —
the literal `aria-haspopup="menu"` was an illustrative wording for the
archetype, not a binding production marker. Resolution: Path C from
the Session 9 C7 escalation — conformance test asserts each fixture
exhibits at least one of (a) `aria-haspopup` with any non-false value,
or (b) `aria-expanded` + `aria-controls` cross-reference pattern.

**Meta-observation:** two audit-spec drift findings in two weeks
suggests the audit report's HTML examples were drawn from a sample now
~18+ months stale on frontend patterns (Next.js 13 + App Router landed
October 2022; WAI-ARIA 1.1's `aria-haspopup="true"` shorthand has been
in browser-default-recommended docs since 2017). Frontend ecosystems
evolve fast; literal-value examples in plans and audits decay rapidly.

**Forward-applicable discipline (NOT for Workstream 0):**

- **Future fixture-sourcing work should expect audit / plan examples
  to need production verification before adoption.** The
  probe-before-lock pattern (LESSONS.md "Probe framework generation
  before locking a fixture spec", established Session 7) is the
  mechanical implementation of this. Treat every literal HTML or
  attribute example in a plan / audit / spec document as
  illustrative-of-archetype, not binding-marker, until verified
  against current production.
- **At the natural Week 5 / end-of-Workstream-0 reassessment point,
  consider whether the audit report's HTML-example sections need a
  refresh pass before downstream workstreams (A.0 baseline scaffolding,
  B observability, C extraction) consume them.** The audit is
  read-only-archival per §14, so a refresh would land as a new
  document (e.g., `AUDIT_REPORT_HTML_EXAMPLES_REFRESH_2026.md`) rather
  than as edits to the original. Decision deferred to that
  retrospective; not in Workstream 0 scope.

Applies forward to: any future framework-marker fixture work (C1.2
Nuxt 2-vs-3, C1.3 Apollo 2-vs-3, C1.4 Redux / state-management, C2
Remix/Gatsby/SvelteKit/Astro, C7-C8 mega-menu variants, C9-C10 PII
positive/negative fixtures, C19 e-commerce schema, C20 LocalBusiness),
and to any audit literal-example wording that names specific HTML
attributes, JavaScript globals, JSON-LD types, or CSS class names.

**Append (Session 9 C7.c, 2026-05-20): the enterprise aria-controls
archetype is structurally concentrated in heavily-defended sites.**
The C7.c substitute-candidate round attempted 5 real enterprise sites
(Microsoft, GitHub, Adobe, IBM, Oracle) targeting the "aria-controls
cross-references" mega-menu archetype. All 5 failed at a 100% rate in
5 distinct failure modes: anti-bot CMS interstitial (Microsoft),
detector FP via FP-1/`dd.js` (GitHub), HTTP/2 INTERNAL_ERROR (Adobe),
structural marker-spec miss (IBM lacks aria-expanded), edge-firewall
stub (Oracle). Resolution was synthetic-with-real-markers per §11
fallback policy.

Implication: audit literal examples drawn from enterprise sites carry
implicit anti-bot-capture cost that the audit did not account for.
Future fixture-sourcing work targeting enterprise archetypes (e.g.,
C20 LocalBusiness with enterprise-tier firms, C21 manufacturing-
industry corporate sites, audit-future expansions naming Adobe /
Oracle / IBM / SAP / Microsoft / Salesforce as candidates) should
budget synthetic-with-real-markers as the **default** fallback rather
than the last resort. The probe-before-lock cost is unchanged
(synthetic substitutes still need to satisfy marker fidelity against
production-observed densities); but plan timelines should not assume
a 1:1 success rate on enterprise live-capture.

## Discovery escalation pattern

### Stop and report when plan contradicts repo reality

**Established:** Sessions 2-6 (multiple discoveries).

The plan and audit are point-in-time artifacts. If during execution
you discover the plan is wrong, oversimplified, or contradicts
current repo state, STOP and report. Do not silently work around
it. State the discovery, propose how the plan should update, and
wait for operator decision.

Examples from this project:
- Session 5 turn 1: `CLASSIFICATION_ADJACENT_PLAN.md` initially
  missing from workspace (operator provided).
- Session 5: Risk #6 (single-tenant guard) verified non-applicable
  to fixture capture scripts (removed from risk register).
- Session 5: `canary_50_domains.txt` lives in locked `eval_data/`
  (read-only consumable; not modifiable).
- Session 6: C0.5 truncation suspects revealed misclassification
  (shelterstoreau/shelterstores were not SPA shells; deleted
  rather than recaptured-in-place).
- Session 6: original SESSION_LOG.md content (in workspace commit
  `e3f5691`) was speculative; replaced with truth-of-record.

## Workstream / commit shape patterns

### Workstream tag at clean completion

**Established:** Session 6 (`workstream-0-week1-end` at `4f9d23f`).

At major workstream boundaries (end of a week within a workstream;
end of a full workstream), tag the HEAD with
`workstream-<#>-<phase>-end`. Tags supplement `SESSION_LOG.md` but
don't replace it. Tag at a SHA where the pre-push gate is GREEN
(passes ruff/format/vermin/validate_consistency); a tag at a
"milestone" commit that fails the gate is less useful than a tag
at the next commit where the gate is clean.

Tags are append-only; do not move them after creation.

### Empty directory acceptable as known-pending state

**Established:** Session 5 (C0.3, C0.4) + Session 6 (C0.9 skips).

A fixture directory emptied for cleanup and awaiting repopulation
is acceptable temporary state. `test_fixture_conformance.py`
handles empty directories gracefully (parametrize on `[]` →
1 skipped per pytest). Directory names persist via SESSION_LOG.md
documentation; physical empty-dir presence is not required (git
doesn't track empty dirs anyway).

Examples in current corpus:
- `soft_404/` — emptied by C0.3 (`3fa3228`); awaits Week 5
  C0.3-followup (6 conforming captures).
- `empty_google_sites/` — emptied by C0.4 (`7f3756b`); awaits
  Week 5 C0.4-followup (3 conforming captures).

### Defer prose-only schema fixes; bump only when machine schema changes

**Established:** Session 11 (Path-A finding + Flag A option b + Flag B
resolution; commit `9e1bda9` on `barcada-scraper`).

When a discrepancy surfaces between schema *prose* (human-readable
spec text) and repo reality, and the *machine* schema (`.schema.json`
constraints actually enforced by validators) is unaffected, do NOT
semver-bump the schema for the prose correction alone. Instead:

1. Apply the corrected behavior at the consuming layer (script,
   tooling, generator) per a documented operator decision.
2. Document the corrected behavior in the forward-applicable home
   (`SESSION_TRANSITION_TEMPLATE.md` for cold-start handoff; commit
   message for git-log visibility; `SESSION_LOG.md` for chronological
   record).
3. Track the prose discrepancy in a "Deferred prose-only fixes"
   register inside `SESSION_TRANSITION_TEMPLATE.md`.
4. Fold the prose correction into the *next* real schema bump's diff
   (the bump that's already changing machine constraints anyway).

Reasoning: a prose-only semver bump churns the locked artifact for
zero machine-validation effect, and the bump-cascade risk noted in
plan §11 (regeneration of all dependent files for schema changes)
applies to *machine* schema changes — text-only prose isn't load-
bearing for that cascade.

When NOT to defer: if the prose discrepancy actively misleads tooling
authoring (e.g., a future fixture-tooling script reads the prose as
truth and reproduces the bug), promote it to an inline correction in
the current locked artifact via the operator's approval. The deferred-
fix register is for low-risk wording bugs only.

Examples landed Session 11:
- META_SCHEMA.md §2.4 + §5 say C0.7c moved files INTO
  `parking_default_pages/`. Reality: C0.7c moved them OUT to
  `auth_403/`. Machine schemas are silent on directory→response
  mapping; prose-only.
- META_SCHEMA.md §2.4 line 93 strict reading says `captured_at` =
  first-add commit date. For `replaced_in_place` files this is
  semantically wrong (file content was rewritten in a later commit).
  Machine schema only says `format: date-time`; prose-only.
- META_SCHEMA.md §2.4 vocabulary list lacks
  `approximated_from_synthetic_invalid_fallback`. Machine schema is
  `additionalProperties: {type: string}` (accepts any string);
  prose-only.

All three deferred to the next real META_SCHEMA semver bump's diff.

### Conformance test lands with red builds; do not silence with xfail

**Established:** Session 6 (C0.9 `6dace7d`).

`test_fixture_conformance.py` enumerates every fixture and asserts
detector conformance. It is EXPECTED to have failures while the
corpus has known rot — those failures are the punch list for
future cleanup. Do NOT add `@pytest.mark.xfail` markers to silence
them. Each red is an action item visible in pytest output.

When fixture cleanup commits land in Week 5+, the failure count
should decrease toward zero. A new failure on a previously-passing
fixture IS a regression and should be investigated.

Current red count (Week 1 close): 17 failures across 5 directories.
See SESSION_LOG.md Session 6 entry for the per-fixture punch list.

### Synthetic-fixture HTML comments are regex-visible

**Established:** Session 8 (C22.c, 2026-05-20).

The parser detectors in `barcada_scraper/scraper/barriers.py`
(`_RE_WAF_CHALLENGE`, `_RE_CLOUDFLARE_CHALLENGE`, `_RE_GEO_BLOCK`,
`_RE_PARKING_JS`, `_RE_SOFT_404`, etc.) operate on the **flat** HTML
text — they do not skip `<!-- ... -->` blocks. Anything inside the
HTML comment header of a synthetic fixture (the documentation block
established in C1.3.b / C1.4.a / C1.4.b that explains probe-before-
lock results, capture method, and re-capture flag) is regex-visible
to the parser exactly as if it were body content.

Worked example (C22.c synthetic_educational_organization.html): the
comment header originally read
```
khanacademy is Akamai-blocked.
```
which tripped the `akamai.*blocked` branch of `_RE_WAF_CHALLENGE`
and made `extract_hard_exclusions` return
`exclusion_reason='waf_challenge'` — a false-positive WAF
classification on a fixture meant to pass the inverted
`legitimate_nonprofit/` detector. Fixed in-place by rewording to
```
khanacademy returns an Akamai bot-mitigation interstitial.
```
which carries the same diagnostic information without putting
"akamai" + "blocked" on the same line.

**Forward-applicable discipline:** when authoring a synthetic-
with-real-markers fixture, treat the HTML comment header with the
same anti-trip care as the body — phrase any references to
parking/anti-bot/WAF/Cloudflare/datacenter-error scenarios using
synonyms that do NOT match the `_RE_*` patterns. After writing the
synthetic, **always run `extract_hard_exclusions(html, "example.com")`
and verify `exclusion_reason=''` before committing**. A per-branch
pattern sweep (loop through every alternation of `_RE_WAF_CHALLENGE`
and check for matches) is the surest verification.

Applies forward to: C18 if Session 9 needs synthetic SaaS marketing
fixtures, C0.3-followup synthetic soft_404 captures (Week 5),
C0.4-followup synthetic empty_google_sites captures (Week 5), and
any future synthetic-fixture authoring work.

## Detector precision findings

### Verify-before-asking doubles as a detector-FP probe; modern SaaS HTML trips current detectors at meaningful rates

**Established:** Session 9 (C18.0 prevalence-probe verification step, 2026-05-20).

The Session 8 "verify-before-asking" discipline (run
`extract_hard_exclusions(html, "example.com")` and a per-branch detector
sweep on every candidate fixture before drafting the commit message) was
introduced to catch false positives in synthetic fixtures. Applied to
real production HTML during C18.0's 11-candidate probe of modern SaaS
marketing sites, it surfaced **detector false-positives in 4 of 11
candidates (~36%)** — none of which are actual challenge/WAF pages.

Two distinct detector bugs were discovered:

**FP 1: `dd.js` alternation in `_RE_WAF_CHALLENGE`** (`barriers.py:413`).
Intended to match DataDome's challenge script reference
(`https://js.datadome.co/dd.js`), but the bare alternation `dd\.js`
matches **any webpack/Gatsby chunk filename whose content-hash ends in
`dd.js`**. Empirically tripped by **4 of 12** modern enterprise/SaaS
candidates probed across Session 9 (initial 11-site C18.0 round plus
1 site added during C7.c substitute-candidate exhaustion):

| Site | Hits | Example chunk filename | Surfaced in |
|---|--:|---|---|
| stripe.com | 1 | `chunks/36822-16ae78e6a74311dd.js` (Next.js) | C18.0 |
| raycast.com | 16 | `chunks/6089-681ded3ed6a016dd.js` (Next.js) | C18.0 substitute pool |
| posthog.com | 1 | `templates-app-js-57625ccfa9cdb61501dd.js` (Gatsby) | C18.0 substitute pool |
| github.com | 1 | `fetch-utilities-18f7f90effa3f0dd.js` (Next.js) | C7.c substitute pool |

Empirical FP rate climbing as probe scope expands into enterprise: 3 of
11 SaaS marketing sites = 27% (C18.0 round); 4 of 12 enterprise-and-SaaS
combined = 33% (after C7.c). The hit rate trend is consistent with the
combinatorial argument: enterprise sites tend to ship more JS chunks,
each independently rolling the dice on whether its content-hash ends in
`dd`.

Content-hash chunk filenames are an effectively-random distribution of
hex characters. The probability of a 16-char hex hash ending in `dd` is
1/256 per chunk, so a multi-chunk SaaS marketing page will trip this
pattern with non-trivial frequency in production. The fix needs a
path/script-src anchor (e.g., `js\.datadome\.co/dd\.js` or
`["']https?://[^"']*datadome[^"']*dd\.js`), not just the bare filename.

**FP 2: `just\s+a\s+moment` alternation in `_RE_CLOUDFLARE_CHALLENGE`**
(`barriers.py:408`). Intended to match Cloudflare's literal interstitial
title "Just a moment..." but matches any body copy containing the
phrase. Tripped by linear.app whose marketing rhetoric reads "Launching
is just a moment in time." 1 of 11 candidates. The pattern needs
context anchoring (proximity to "cloudflare", inside a `<title>`
element, or near a `cf-` class) rather than the bare phrase.

**FP 3 (different flavor — matches but is correctly suppressed):
`(?:search|query|keyword).*no\s+results?\s+found` alternation in
`_RE_SOFT_404`** (`barriers.py:464`). Surfaced by C18.e snowflake.com
verification (2026-05-20). The greedy `.*` (no DOTALL, no non-greedy
quantifier) spans unbounded distance in compressed-JSON HTML where
newlines are sparse. Snowflake's homepage trips the pattern via two
anchors ~432 KB apart in the document:

- Anchor 1: `search` at offset 866,870, inside the substring
  `searchers"` — a key in the mega-nav JSON config (Snowflake runs an
  AEM/Sling-CMS site that ships site structure as inline JSON).
- Anchor 2: `no results found` at offset 1,299,314, inside an i18n
  strings block: `"no_results":"No results found"` — the translation
  string for the location-search component's empty-state UI.

Both anchors are inside legitimate component config / i18n strings;
neither indicates a soft-404 page. The detector code's downstream
guards (length + meaningful_content + structured_content checks,
parser.py `extract_hard_exclusions` step 5) correctly suppress this
raw regex match — `exclusion_reason` remains empty, `is_soft_404`
stays False — so the production crawler does NOT misclassify pages
like snowflake.com today.

This is a distinct category from FPs 1 and 2 above:

- FPs 1 & 2: regex matches AND propagates to `exclusion_reason` →
  detector breaks (production-precision regression today).
- FP 3: regex matches BUT downstream guards correctly suppress →
  detector works as designed, but the regex itself is looser than
  needed; future changes to the soft_404 downstream guards (e.g., a
  refactor that drops or relaxes the meaningful-content gate) could
  re-expose this match as a real false positive.

The fix is a non-greedy `(?:search|query|keyword).*?no\s+results?\s+found`
or a max-distance constraint (e.g., `.{0,500}` between anchors). Not
in Workstream 0 scope — same anti-pattern caveat as FPs 1 and 2.

### False-negative coverage gaps for anti-bot interstitials

**Established:** Session 9 (C7.c substitute-candidate round, 2026-05-20).

While the dd.js / just-a-moment / soft_404 findings above are false
**positives** (regex matches when it should not), C7.c surfaced a
distinct category of detector imprecision: false **negatives** —
real anti-bot interstitial responses that the existing 15 detector
branches do NOT match, allowing contaminated captures to pass
extract_hard_exclusions with `exclusion_reason=''`.

Three flavors observed during C7.c, none caught by any existing branch:

**FN 1: Microsoft "Your request has been blocked" CMS interstitial.**
microsoft.com returned an HTTP 200 response with body served by
Microsoft's mscom-data CMS template — title "Your request has been
blocked. This could be due to several reasons." The block-page body
ships ~12× aria-expanded markers on the standard Microsoft header
skeleton — IDENTICAL to the real homepage's marker count — so marker
counts cannot distinguish contaminated captures from real ones. The
title-sanity check during verify-before-asking was the cheapest
distinguishing signal; no body-content detector flagged it. Vocabulary
gap in the detectors: no alternation for "request has been blocked"
or "request has been refused" phrasing as a standalone signal.

**FN 2: Adobe HTTP/2 INTERNAL_ERROR.** adobe.com returned HTTP/2 stream
INTERNAL_ERROR after three retry attempts. curl exits with code 92; no
response body ever returned to extract. Caught only by retry-policy
exit-code handling at the capture layer, not by any body-content
detector — there is no body to inspect. This is a structurally
different failure mode from FN 1 (TCP/HTTP2-layer block vs.
application-layer interstitial) but produces the same operational
effect: the production crawler cannot reach adobe.com today.

**FN 3: Oracle fw_error_www edge-stub.** oracle.com returned a
1,450-byte minimal HTML body with title `fw_error_www` (Oracle's
edge firewall stub page). Below most reasonable body-size sanity
thresholds; not matched by any existing alternation. The page lacks
the markers that distinguish parking from anti-bot from real content,
because there's no real content to ship at all.

**Why these matter:** the production crawler's downstream classifier
operates on the assumption that pages reaching it with
`exclusion_reason=''` are real, classifiable content. Anti-bot block
pages with vendor-specific phrasing (Microsoft's CMS template, Oracle's
fw_error stub) silently feed contaminated samples into the
classification pipeline. The contaminated samples don't crash the
classifier — they just get incorrectly classified, distorting per-
domain metrics and downstream cost-per-useful-record measurements.

**Forward-applicable actions (NOT for Workstream 0):**

1. The focused detector-precision audit (forward action #1 in the
   Verify-before-asking entry above, owner ambiguous between
   Workstream B and C) should cover BOTH directions:
   - FP precision against legitimate HTML (the dd.js / just-a-moment
     / soft_404 cases above)
   - **NEW: FN coverage against vendor-specific block / interstitial
     pages** (the Microsoft / Oracle / Adobe-HTTP2 cases here)
2. Concrete starting alternations for the FN-coverage dimension:
   - `your request has been (blocked|refused|denied)` phrasing
   - `<title>fw_error` and similar edge-firewall stub markers
   - Body-size sanity check: HTTP 200 responses with body length
     under 2 KB combined with absent main content markers should
     trigger an "is_thin_response" informational flag
   - HTTP/2 INTERNAL_ERROR exit-code handling at the capture layer
     (separate from body-content detectors) should produce an
     "is_h2_refused" informational flag
3. Verify-before-asking discipline forward: title-sanity check
   ("does the title look like the expected page archetype?") and
   body-size sanity check ("is the byte size in the expected range
   for this candidate type?") are cheap pre-commit gates that catch
   the FN cases the detectors miss. Both should be standard steps
   in any future fixture-sourcing verify-before-asking script.

Applies forward to: every future fixture-sourcing round (C19
e-commerce, C20 LocalBusiness, C21 manufacturing, C0.3-followup
soft_404, C0.4-followup empty_google_sites, Workstream A.0 canary
wiring), and to the eventual detector-precision audit's scope.

### The deeper circularity: detector validation has only ever run against the corpus the detectors were curated to match

This finding is the audit-said-X-but-grep-found-Y pattern (Session 4)
operating one level deeper. The original Session 4 finding was that the
audit / plan made claims about the codebase that did not survive a
direct grep. The Session 9 finding is that **the detectors themselves
have never been spot-checked against the production corpus the crawler
actually operates on** — they have only been validated against the
fixture corpus, which by construction was assembled by humans who knew
what each detector was looking for. Fixtures conform to detectors; the
real production distribution does not have that property.

The verify-before-asking discipline accidentally functions as the first
production-corpus precision probe ever run on these detectors. The 36%
trip rate on 11 well-known modern SaaS marketing sites is not a
synthetic-fixture concern — it implies the production crawler is
currently mis-classifying a meaningful fraction of legitimate SaaS
domains as WAF or Cloudflare challenges, downstream of which the
classifier presumably routes them away from real categorization. That
is a production-precision regression hiding behind a green test suite.

**Forward-applicable actions (NOT for Workstream 0):**

1. **A focused detector-precision audit should be scheduled before
   locking detector behavior in any new workstream.** Ownership is
   ambiguous between Workstream B (cost & observability foundation —
   detector FPs are an observability concern because they distort
   per-tier block-rate metrics) and Workstream C (high-leverage
   extraction — detector FPs upstream block extraction from running on
   legitimate domains). Both workstreams have legitimate claims; flag
   for operator decision at the natural Workstream-0-close
   handoff. The audit itself: take 100–200 known-legitimate domains
   (the canary 50 + a sample of production validator passes), run
   them through the full hard-exclusion pipeline, and produce a
   per-alternation false-positive rate. Treat any alternation with
   >2% FP rate against legitimate traffic as needing a context anchor
   (`dd.js`, `just\s+a\s+moment`, `(?:search|query|keyword).*no\s+results?\s+found`
   are confirmed candidates from C18.0).
2. **Plan §11 Risk Register** carries forward a new latent risk:
   "Detector precision was validated against a curated fixture corpus,
   not the production distribution. Quarterly precision audits against
   the canary set should be added once the canary is stable in
   Workstream A.0." (Plan is read-only; risk gets recorded here +
   SESSION_LOG.md until the next plan revision opportunity arises.)
3. **Future fixture-sourcing work** (C18, C19, C20, C21 modern-
   business expansion; Workstream A.0 canary wiring) should treat
   verify-before-asking failures as **likely detector-precision
   signals**, not fixture-disqualification signals. Drop the
   candidate from the current fixture set, but log the trip in
   SESSION_LOG.md so the eventual precision audit has a starting
   dataset.

**Anti-pattern (do NOT do this):** fixing detector code as a
side-quest during a fixture commit. Workstream 0 is fixture-only.
Detector-code changes need to live in Workstream B/C with their own
test coverage, regression baselines, and operator review. C18.a–e
drop the FP-tripping candidates (stripe.com, linear.app, raycast.com,
posthog.com) and proceed with clean substitutes; barriers.py is
untouched.

---

## Verify-before-asking discipline

### The discipline named (Flag 2 resolution, Session 10)

**Established:** Session 10 (Flag 2 retrospective, 2026-05-20).

"Verify-before-asking" is the durable name for the operator-discipline
observed across Sessions 7-9. Three LESSONS.md sub-sections constitute
the evidence anchor:

- **"Probe framework generation before locking a fixture spec"** (S7,
  Diagnostic patterns, lines 186-227) — fixture-spec verification
  against current production patterns before locking a fixture set.
- **"Synthetic-fixture HTML comments are regex-visible"** (S8,
  Workstream / commit shape patterns, lines 423-465) — author-side
  verification that synthetic-fixture content does not inadvertently
  trip detector regexes.
- **"Detector precision findings"** with FPs 1-3 + FNs 1-3 +
  circularity meta-observation (S9, Detector precision findings,
  lines 467-696) — production-corpus verification that surfaces
  detector precision regressions hiding behind green test suites.

Pattern statement: before locking a fixture, schema, or commit,
verify the artifact against the on-disk reality (parse it, grep it,
run the relevant detector) rather than trusting prior assumption.
Surface discrepancies before drafting the next deliverable.

**Promotion decision (Flag 2, Session 10):** status quo (Option c).
Keeps the discipline anchored in LESSONS.md, propagated via plan §14
required-reading + operator-ratchet (next entry), not via plan-
amendment or CLAUDE.md / .claude/rules/ codification. Reason: three
weeks of evidence are all from Workstream 0 fixture-sourcing context;
promotion before forward-context evidence (Workstream A/B/C) would
codify a discipline that may need refinement when applied to
different work shapes. Reopening trigger documented in "Workstream
A/B/C trigger condition" entry below.

Options (a) plan-amendment-via-sibling-document and (b) CLAUDE.md /
.claude/rules/ codification were rejected with structural-risk
reasoning recorded in SESSION_LOG.md Session 10 entry. Do not
relitigate without new forward-context evidence per the trigger
condition below.

### Operator-ratchet as the propagation mechanism

**Established:** Session 10 (Flag 2 Option (c) execution constraint
#2, 2026-05-20).

Under Flag 2 Option (c) (status quo), the verify-before-asking
discipline propagates through sessions via two mechanisms:

1. **Plan §14 required-reading**: each new session opens by reading
   LESSONS.md among other artifacts (template lines 273-274). Future
   Claude Code sessions see the discipline named and anchored.

2. **Operator-ratchet**: in-session, the operator periodically asks
   "did you double check your work?" before commit confirmation.
   Each instance tightens the verification standard by forcing one
   more inspection layer.

Empirical pattern observed in Session 9 (SESSION_LOG.md S9 lines
1103-1114): the question was asked 4-5 times during Session 9, each
time surfacing 2-3 real gaps in the verification table the assistant
had drafted (SHA fabrication, full-block dump vs True-flag-only
filter, comment-text regex trip, missing parametrize-collection
check, missing post-format re-read, missing direct-helper-call
verification, missing negative-case coverage). Each iteration
tightened the verification standard.

Session 10 observation: when the assistant applies verify-before-
asking *proactively* (verification table generated pre-confirm,
anti-trip scan on test_purpose, content_length bit-exact match,
source_url ↔ canonical-link exact match, captured_at ↔ git author
date conversion check), the operator-ratchet does not need to fire
because the proactive verification catches what the ratchet would
have caught. The ratchet is a backstop, not the primary mechanism.

The operator-ratchet is operator-driven, not assistant-driven; status
quo (Flag 2 Option c) preserves this regime. Promotion to plan-
amendment or rule-codification would convert the discipline from
operator-driven to assistant-driven, which is a different regime
that the three weeks of Workstream 0 evidence does not yet support.

Forward-applicable: any session in any workstream. The operator's
"did you double check" question is not workstream-bounded.

### Workstream A/B/C trigger condition for reopening the promotion question

**Established:** Session 10 (Flag 2 Option (c) execution constraint
#3, 2026-05-20).

Flag 2 (Session 10) deferred promotion of verify-before-asking from
ad-hoc discipline to a named acceptance criterion. The three weeks
of evidence (Sessions 7-9) are all from Workstream 0 fixture-sourcing
context. The promotion question reopens — with broader evidence
base — when the discipline produces a finding outside Workstream 0.

**Trigger condition**: any of the following constitutes a "finding"
that warrants reopening the Flag 2 promotion question:

- **Workstream A** (compliance foundation, Weeks 8-9): a verify-
  before-asking instance surfaces a robots.txt parser bug, an
  identifiable-UA misconfiguration, or a governance-document
  inaccuracy that would otherwise have shipped.
- **Workstream A.0** (baseline scaffolding, Weeks 6-7): a verify-
  before-asking instance surfaces a baseline-v0 comparison-logic
  gap, a determinism violation, or a synthetic-crawl-tape replay
  divergence that would otherwise have shipped.
- **Workstream B** (cost & observability, Weeks 10-12): a verify-
  before-asking instance surfaces a metric-emission shape mismatch,
  a per-domain-budget calculation bug, or a detector-precision
  regression that would otherwise have shipped.
- **Workstream C** (high-leverage extraction, Weeks 13-16): a
  verify-before-asking instance surfaces a hydration-extraction
  marker miss, a mega-menu activation false-negative, or a Stage 3
  expected-output discrepancy that would otherwise have shipped.

When triggered, the promotion question reopens at the next natural
session boundary. **Reopening is not a commitment to promote — just
a trigger to revisit.**

**Anti-pattern**: do NOT reopen the promotion question on a
Workstream 0 finding (Week 4 expected-output generation, Week 5
punch-list cleanup, etc.). Workstream 0 evidence is already counted
in the original Flag 2 deferral; additional same-context evidence
does not change the evidence base.

### Close-out claims-by-analogy in handoff documents (Session 11 → Session 12-prep finding)

Close-out drafting consumes attention. Structural claims about prior
state (SHA lists, file lists, commit-message contents, tag
annotations) get written by pattern-completion rather than source-
verification. Failure mode: claim drifts from source, lands in a
handoff document, future sessions inherit the drift as ground truth.

**Mitigation**: every structural claim in a close-out or handoff
document is verified against the source before the document lands.
Verify recipe: `git log <SHA> --format=%B` and grep for the claimed
content, or equivalent for non-commit assertions.

**Trigger pattern**: any handoff or close-out document that names
specific SHAs, file paths, commit-message contents, or asserts
state ("X is staged in Y", "Z carries forward from W"). Apply the
recipe before the document is committed.

**Concrete instance (Session 11 close → Session 12-prep)**: the
SESSION_TRANSITION_TEMPLATE.md and the draft Session 12 prompt
claimed the Workstream C scope amendment flag was staged in commit
messages `9165791`, `8aafc45`, and `9e1bda9`. Verification showed
the flag is present in `9165791` and `8aafc45` only. The claim was
written by analogy during close-out drafting; a single
`git show --no-patch --format=%B 9e1bda9 | grep -i workstream.c`
would have caught it in seconds. Operator question triggered the
verification retroactively; correction landed in this commit.

### Verify-before-asking discipline (extension): the discipline applies to operator-issued state claims, not only to Claude Code's draft outputs

**Established:** Session 12 / Phase 4 reconciliation (2026-05-21).

The verify-before-asking discipline as originally named (Session 10
Flag 2 resolution) emphasized Claude Code's outputs being verified
before commit. The Session 11 close-out claims-by-analogy work
extended this to bidirectional verification of structural claims in
handoff documents. Session 12 extends it further: operator-issued
state claims about multi-PR multi-week work history also require
source verification, not acceptance from operator recall alone.

Specific instance: operator stated "Phase 4 has not been implemented
at all" in Session 12. The chat session accepted this and was
preparing to recommend a sequencing path on that basis. Claude Code
source verification then revealed four of eight Phase 4 PRs had
landed (PR-COST, PR-A, PR-B, PR-C — see
`~/crawler-audit/working/phase4_status_2026-05-21.md`). The
operator-recall claim was incorrect against source. Had the chat
proceeded with the recommendation without verification, the
operator-authorized plan amendment would have been wrong.

**The rule:** when the next decision depends on a multi-artifact
state claim (e.g., "X PRs have landed", "Y work units are
complete", "Z artifact exists"), verify against source before
locking the decision — even when the claim comes from the
operator. The operator may have context Claude Code lacks, but the
source-of-truth is the artifact itself, not the recall.

**Mechanism:** a targeted verification prompt to Claude Code that
asks narrow factual questions with explicit citation requirements.
Cost is modest (one session, no plan amendments). Benefit is
preventing plan-amendment-based-on-wrong-state, which is much more
expensive to unwind.

**See also:** "Verify-before-asking discipline anchor" (Session 10)
for the discipline-naming entry; "Close-out claims-by-analogy in
handoff documents" (Session 11 → Session 12-prep) for the
bidirectional structural-claim verification extension. This entry
completes the bidirectionality: discipline runs in both directions
(operator → Claude Code, Claude Code → operator).

### Driver-level input contracts: verify cascade input shape before scoping generation work

**Established:** Session 12 / Phase 4 reconciliation (2026-05-21).

The W4.2 work-unit scoping assumed that generating per-fixture
expected outputs was a configuration matter: run the cascade against
fixtures, capture outputs. This assumption was wrong against actual
driver code. Stage 2 consumes `pages.parquet` produced by
`FetcherSet` HTTP fetches; Stage 3 consumes three upstream parquets
(Stage 2 predictions, Stage 2 summaries, Stage 3 evidence cache) AND
fetches its own four T3 paths per domain (see
`~/crawler-audit/working/stage3_input_shape_2026-05-21.md`). No
fixture-input bypass exists at the driver level.

**The pattern:** before scoping any work unit that involves running
pipeline code against synthetic inputs (test fixtures, synthetic
crawls, replay cassettes), verify the driver-level input contract
at runtime-code source. The contract is what the run-driver
actually consumes — NOT what the audit's discovered-architecture
section described, NOT what the design-of-record document says the
cascade should look like, NOT what plan-authoring assumed. The
runtime code is the source of truth.

**Specific surfaces to verify:**

- Driver entry-point (`run.py` or equivalent): what files does it
  open at startup? Confirm via grep `read_parquet`, `pd.read_csv`,
  `open(...)`, Hive partition reads.
- Fetcher invocations: does the stage trigger live HTTP? At what
  seam? Confirm via grep for fetcher class names, URL request
  invocations.
- CLI flags: does a bypass / test-mode / input-parquet flag exist?
  Confirm via grep `argparse.add_argument`, CLI module reads.

**Trigger condition for verification:** before scoping a work unit
that will run pipeline against synthetic inputs, run a targeted
Claude Code verification with file:line citation requirements.

**Mitigation when bypass doesn't exist:** build the bypass as its
own work unit, NOT as side-effect engineering inside the work unit
that needs it. The bypass is foundation; the work unit that
consumes the bypass is consumer. Separate them. (See W4.1.5 /
W4.2 split in `RECONCILIATION_2026-05-21.md` and plan §3 Week 4
(W4.1.5) for the working example.)

**See also:** "Audit-spec vs. production-reality drift" (Session 9)
and "Verify-before-asking discipline" (Session 10). This pattern is
the input-contract-specific instance of those broader patterns.

### Always verify every concrete claim in commit messages before staging (strict rule)

**Established:** Session 19 operator codification (2026-05-22),
re-confirmed via Session 20 self-application.

Every concrete assertion in a draft commit message — fixture name,
file count, exit code, line count, test count, helper name, SHA
prefix, smoke outcome — must be verified against actual source or
runtime output BEFORE staging the commit. No claims by pattern-
completion or memory.

**The recipe:** build a verification table in chat with three
columns (claim | reality | status), trace each concrete assertion
to source (`wc -l`, `pytest -v`, `grep`, programmatic query,
direct file read, exit-code capture into a file), reconcile any
✗ before "Confirm to commit?" is sent to operator. If the operator
runs the "did you double check?" ratchet, the verification table
should already be in chat.

**Session 19 incident** (auth_403 vs empty_google_sites): the
draft commit message named `auth_403/griftdijk.net` as the
matching fixture in a 2-fixture smoke; the actual first-2
fixtures alphabetically were `empty_google_sites/atari_vw_
synthetic` (matched) and `spa_hydration_nuxt/backmarket.com`
(mismatched). The wrong name was written by pattern-completion;
corrected only when operator-ratchet fired.

**Session 20 re-application**: caught two real claims in real-
time during checkpoint protocol:
- Line-count claim mismatch (cli.py +56 LOC claim vs actual
  +63/-4) on canary-skeleton commit; corrected the message
  before staging.
- argparse test premise (test asserted "barcada-baseline-canary"
  string in --help text, but argparse doesn't show defaults
  unless explicitly formatted); test failed in pytest, rewrote
  to use parser.parse_args inspection instead.

Forward-applicable: every commit in every session. The
verification table is a 30-second cost; the propagation of a
wrong claim to a handoff document or post-session debugging is
much larger.

**Memory tag:** `[[double-check-before-commit]]` was extended
during Session 19 to codify the strict rule. Session 20 confirmed
the strict reading.

### Bash pipes mask Python exit codes; capture exit code to a file or use PIPESTATUS

**Established:** Session 19 (2026-05-22).

`python_cmd 2>&1 | grep ... | tail -5` makes `$?` reflect tail's
exit (almost always 0 if tail produced any output), not the Python
process's. This silently hides exit-code failures from verification
tables that depend on the actual exit code.

**Two safe patterns:**

```bash
# Pattern 1: capture into files, inspect echo $?
python_cmd > /tmp/out.txt 2> /tmp/err.txt; echo "Exit: $?"
cat /tmp/err.txt

# Pattern 2: PIPESTATUS array
python_cmd 2>&1 | tail -5; echo "Python exit: ${PIPESTATUS[0]}"
```

**When the rule binds:** any verification of CLI exit codes
(record-stub returns 2; check-mismatch returns 1; canary-run
input-error returns 2; etc.). Don't pipe through head/tail/grep
when the exit code is what you're verifying.

**Session 20 instance:** smoke-validating
`tools.synthetic_crawl record --domain x ...` first run reported
"Exit: 0" via `cmd | head -2; echo $?`; corrected via `cmd >
/tmp/out 2> /tmp/err; echo $?` to confirm actual exit 2.

Forward-applicable: any bash verification of Python exit codes
in any session.

### Mid-implementation ruff format-check, not only pre-push

**Established:** Session 19 retrospective on skeleton-commit
format drift (2026-05-22).

The pre-push hook runs `ruff format --check .` which catches
format violations at push time. But by then, the skeleton commit
that introduced the violation is structurally final; the format
fix has to land as a separate fixup commit or be bundled with the
next real-impl commit (which clouds the message).

**Cheaper:** run `ruff format --check <touched paths>` (and
`ruff check`) right after every code-touching Edit, not only as
the pre-push gate. Auto-format with `ruff format <touched
paths>` if it complains. Fold the format result into the same
commit as the code change.

**Session 19 instance:** the cassettes-skeleton-equivalent
(check sub-surface skeleton at b358a02) shipped with multi-line
`help=` strings that ruff format wanted collapsed. The fix
bundled into the next real-impl commit eca4ec0 with explicit
disclosure in the message.

**Session 20 application:** ran ruff check + format --check on
every touched path immediately after Edit/Write. Caught and
fixed format issues in cassettes-skeleton (sys unused import),
cassettes-driver (import sort order), tests/synthetic_crawl/
test_recorder.py (long line), canary.py (import sort order),
tests/baseline_v0/test_canary.py (one reformat) — all bundled
into their respective commits with no separate fixup commits.

Forward-applicable: any session in any workstream. Format the
file as soon as you change it, not at push time.

### Sibling-module style consistency over project-wide rule compliance for one-file additions

**Established:** Session 19 disclosure pattern on check.py
sibling consistency with generate.py (2026-05-22).

When adding a new module that sits alongside an existing module
(check.py alongside generate.py; canary.py alongside check.py +
generate.py; recorder.py alongside future synthetic_crawl
modules), match the sibling's style conventions even where they
technically violate a project-wide rule (.claude/rules/code-
readability.md says don't use `.get()`; existing generate.py uses
`.get()` in 2 places).

**Rationale:** diverging in the new module creates style
inconsistency with the immediate sibling and surfaces a partial
refactor without doing the full one. The project-wide rule
compliance can land as its own refactor scope across all
siblings simultaneously.

**Disclosure discipline:** when applying sibling consistency
that violates a project-wide rule, disclose explicitly in the
commit message body. Future readers (operator, future Claude
Code sessions, code-review tooling) see the trade-off was made
deliberately, not by oversight.

**Session 19 instance:** check.py inherited `.get()` x2 +
`.items()` x2 patterns from generate.py; disclosed in WA0.W7.
check commit message.

**Session 20 instance:** canary.py uses `.get()` in
`_build_exclusions_row` matching the pattern; recorder.py uses
inline `dict[str, Any]` matching the project's typing
conventions.

Forward-applicable: any one-file-addition next to existing
siblings in any session. Tracks rule-compliance trade-off
explicitly rather than silently diverging.

### Integration tests can self-seed via the module-under-test's siblings (or hand-rolled artifacts)

**Established:** Session 19 (test_check.py drives generate to
seed manifest, 2026-05-22). Reinforced Session 20 with hand-
rolled artifact variant.

For integration tests of a module that operates on a complex
artifact (manifest, parquet, vcrpy cassette), the cheapest
self-seeding pattern is:

1. **Sibling-seeded** (S19 pattern): the test drives the
   sibling module that produces the artifact to write it into
   a tmp_path, then runs the module-under-test against the
   seeded artifact. Catches future divergence between the two
   modules' shared invariants (e.g., S19 test_check.py drives
   generate(fake-mode, max_fixtures=1) to seed a manifest, then
   runs check() against it; one of the integration tests then
   re-runs check's own hash_canonical chain on the seeded
   component .json files to verify they match the manifest's
   per-entry _hash — catches generate ↔ check hash chain
   divergence).

2. **Hand-rolled artifact** (S20 variant): when no sibling
   exists yet to seed the artifact (or when seeding via sibling
   is too expensive — e.g., requires live HTTP), construct
   the artifact directly via the underlying library's
   internal API. For S20 cassettes: hand-roll a vcrpy YAML
   cassette using `vcr.serialize.serialize(cassette_dict,
   yamlserializer)` at the {"requests": [...], "responses":
   [...]} shape, then drive replay() against it twice for the
   byte-identical determinism gate.

**Why this beats mocking:** mocking the underlying library
(vcrpy itself, the cascade driver) couples the test to library
internals and breaks under library version bumps. Hand-rolled
or sibling-seeded artifacts exercise the real library code path.

**Trigger pattern:** any integration test where the module-
under-test consumes a complex artifact. Prefer real-artifact
seeding (sibling-driven OR hand-rolled) over mocking.

### Reviewer-feedback hygiene: verify each item against on-disk reality before applying

**Established:** Session 19 reviewer-feedback walkthrough
(2026-05-22). Reinforced Session 20 with mid-session amendment
file walkthrough.

External-reviewer feedback on a session prompt (or on a draft
PR description) arrives as a list of items. The temptation is
to apply each item as a command. The discipline is to walk each
item against the actual repo state before applying.

**Pattern:** for each item, source-verify the underlying claim
against on-disk reality (read the file the item references;
grep for the symbol; run the test the item claims is missing).
Classify the item as:

- **OBSOLETE**: the claim was already true at the SHA the
  reviewer flagged. Skip with documented reasoning.
- **VALID-applies-now**: the claim is true and the fix belongs
  in this session. Apply.
- **VALID-applies-later**: the claim is true but the fix
  belongs in a later session (e.g., the item bears on a sub-
  surface the current session's scope has deferred). Route
  to the deferred session's prompt as carry-forward.
- **WRONG-PREMISE**: the item assumes something that's not
  true (e.g., the reviewer assumed a SHA wasn't verified when
  cold-start verification already verified it). Skip with
  documented reasoning.

**Session 19 instance**: 11 reviewer items; 3 of 5 "must-fix"
were OBSOLETE (SHAs already verified), 5 completeness items
were VALID-applies-later (all bore on cassettes/canary which
that session's scope had deferred — became S20 prompt-
improvement inputs), 3 polish items were VALID-applies-now.

**Session 20 instance**: 12 amendment items
(session-20-prompt-amendments.md); applied 8 mid-session, skipped
1 (SR-4 would HALT spuriously as written), carried forward 3
(items applied to design decisions already made in Phase 1).
Each item walked against on-disk reality and prompt content
before disposition.

Forward-applicable: any session that receives external feedback
on the session prompt OR the draft commit/PR. Apply via on-disk
verification, not by pattern.

### Pre-push gate against operator-WIP territory: surface, don't auto-fix

**Established:** Session 20 (2026-05-23, eval_data WIP halt at
Phase 4).

The repo's pre-push hook runs `eval_data/scripts/
validate_consistency.py` against working-tree state. eval_data/
is operator-owned labeling territory (per plan §14 locked
artifacts list); a session's commits do not touch it.

But operator-WIP edits to `eval_data/*.jsonl` can introduce
schema violations (e.g., duplicate keywords in a row's
rationale_keywords array) that fail validate_consistency. The
pre-push gate then blocks the push even though the session's
commits are clean.

**Pattern when this fires:**

1. Confirm the failing row's content is in operator-WIP
   (`git diff eval_data/...`), not in committed HEAD
   (`git show HEAD:eval_data/...`).
2. Confirm the session's commits do not touch eval_data
   (`git diff origin/main..HEAD -- eval_data/`).
3. Surface to operator with:
   - The exact failing row + reason
   - Diff vs committed state showing it's WIP-only
   - Two paths: (a) operator-fix in working tree, then re-run
     gate; (b) stash eval_data WIP, push committed state, restore.
4. Do NOT auto-fix the locked-artifact content. Even if the
   fix is obviously correct (dedupe a duplicate), the
   ownership boundary is the gate.

**Session 20 instance**: stage1_labels.jsonl row 377 (bigid.com)
had duplicate "customer_logos" in operator-WIP rationale_keywords
(committed: 3 keywords; WIP: 7 with the duplicate). Surfaced
per the pattern; operator chose option (a), deduped manually,
gate re-ran clean.

Forward-applicable: any session where the pre-push validate_
consistency / similar runs against working-tree state and
operator-WIP intersects locked-artifact territory.

## Library-quirk patterns (S21 folding)

### Test-driven discovery of stdlib quirks

When wrapping a stdlib API, the first test run is the
documentation. Tests that fail on first run are often pointing
at undocumented stdlib behavior, not at typos. Pattern:

1. Verify the failure against stdlib doc/source (don't reflexively
   change the assertion).
2. Decide whether the quirk is:
   (a) a bug to work around at the parser layer (write a helper);
   (b) a contract to document at the test layer (rewrite the
       assertion + docstring to pin the real behavior).
3. The decision shapes whether the wrapper compensates or the
   test merely records.

Concrete S21 examples worked out in
`src/barcada_scraper/scraper/robots.py` + `tests/scraper/test_robots.py`:

- stdlib `RobotFileParser.crawl_delay()` checks `default_entry` (*)
  before named entries — masks specific-UA Crawl-delay. Worked
  around with `_crawl_delay_for(parser, user_agent)` iterating
  `parser.entries` to prefer the named entry.
- stdlib `applies_to(useragent)` strips input after `/` and
  substring-matches the bare bot name. Documented in the test
  docstring (robots.txt convention: name the bot without version).
- stdlib Disallow/Allow ordering is first-match-wins, not
  Google-style longest-match. Two paired tests document both
  directions.

Forward-applicable: any future stdlib-wrapper (urllib, xml.etree,
http.client, etc.). When a test fails on the first run, check the
stdlib source before assuming the test is wrong.

## Workspace HEAD delta tolerance (S21 folding)

Phase 0 workspace HEAD assertions should ALWAYS allow N-ahead
when the N commits match the expected between-session pattern:
prompt finalization, prompt amendments, template refills, doc
edits. Precedent:

- S20: 2 commits ahead of expected (strengthened prompt). Operator
  authorized continuation.
- S21: 3 commits ahead of expected (prompt amendments v3 + v4
  + initial 6 reviewer findings). Operator authorized continuation.

Pattern: prompt's Phase 0 Step 0.1 should explicitly accept
N-ahead when commit subjects match the expected pattern (avoids
spurious HALT each session). The S20 prompt already encoded
this; S21 reused it cleanly.

## Single-module Phase 3 commit collapse (S21 folding)

S20 precedent suggested skeleton -> impl -> tests (3 commits per
sub-surface). When a Phase 1 candidate ships a single new module
with no CLI dispatch and no second consumer, per-module commit
shape (Q-SHARED.1) collapses naturally to a single bundled
commit. S21 Candidate C (robots parser-only) shipped at
`34a59b6` as one commit: `src/barcada_scraper/scraper/robots.py`
+ `tests/scraper/test_robots.py`.

Forward-applicable: don't reach for 3-commit ceremony when the
sub-surface is one module + its tests. Skeleton/impl/tests
separation is justified when (a) the skeleton needs to land
first because tests of the impl depend on dispatch wiring, OR
(b) the impl is large enough that separating tests reduces
review cognitive load. Otherwise bundle.

## Explore-subagent + spot-check for Phase 2 source-verify (S21 folding)

The verify-before-asking discipline at Phase 2 design-gate
requires source-grounded answers — but reading 5-8 files in
the main session burns context. Pattern: delegate the multi-
file audit to an Explore subagent with a structured prompt
(citation-heavy summary; word-cap), then spot-check the 2-3
most LOAD-BEARING claims manually. Spot-checking everything
defeats the purpose; spot-checking nothing trusts subagent
output blindly.

S21 audit covered 8 items across 7 files; 3 spot-checks all
matched on-disk reality. Subagent summary: ~400 words; main-
session spot-checks: ~30 lines of Read/grep output. Time-to-
informed-design-gate: ~2 minutes vs ~10 minutes without
delegation.

Forward-applicable: any Phase 2 source-verify where the audit
naturally spans >3 files. Define "load-bearing claim" as one
that would change the question wording if wrong.

## Sibling-module style disclosure (S21 follow-up)

The `[[sibling-module-style-consistency]]` rule says match the
immediate sibling's conventions and disclose explicitly. S21
added `src/barcada_scraper/scraper/robots.py` matching
`english_alternative.py`'s short Barcada copyright header (not
the long multi-paragraph CLAUDE.md template) — but the commit
body did NOT explicitly disclose this choice. Minor improvement
opportunity: when sibling style differs from a project-wide
template, name the sibling in the commit body so reviewers
don't flag the deviation.

## Plan-vs-reality at Phase 2 source-verify (S22 folding)

When the remediation plan references a specific file or function
as an integration target, source-verify that the named entity
actually has the shape the plan describes BEFORE drafting Phase 2
questions. S22 prompt §5 Action #2 named `link_discovery.py` as
the robots integration site — Phase 2 source-verification at S22
open found the module is pure-function with no I/O ("this module
performs NO network I/O" right in the docstring), making the
plan's wording architecturally wrong.

Catching this in source-verify (BEFORE the AskUserQuestion went
out) let Q-F.1's option set reflect on-disk reality: "shim only"
became the recommended choice and "shim + worker_loop" became a
heavier alternative requiring async-bridge design. Had I asked
the question with the plan's wording verbatim, the operator's
likely answer would have been "integrate into link_discovery.py"
and the implementation would have hit the architectural mismatch
mid-Phase-3 — costing a HALT, a re-design, and a re-confirmation
round-trip.

Forward-applicable: any Phase 2 question that names a specific
file as an integration target. Verify the named file matches the
plan's described shape (signature, return type, I/O surface)
BEFORE drafting the question. If it doesn't, reframe the question
options so the design-gate vote reflects the real seam choices,
not the plan-as-written choices. Disclose the verification finding
to the operator in chat before the question batch so the operator
knows why the option list diverges from the plan.

## Implicit-authorization HALT for src/-locks (S22 folding)

When a design-gate question's answer implies touching a src/ file
NOT in the Out-of-scope clause's explicit allow-list, HALT for
operator authorization even when the implementation path seems
obvious. S22 Out-of-scope enumerated `scraper/robots_gate.py` and
`link_discovery.py` as authorized src/ touches; Q-F.3's "new
journal-level field" answer implies touching
`classifier/pipeline/cost_journal.py`, which the Out-of-scope
clause did NOT enumerate.

Rather than silently assuming the Q-F.3 answer implicitly
authorized the touch, surfaced as an explicit AskUserQuestion
step before commit 3 with three options (authorize / pivot to
separate-file approach / defer Q-F.3 entirely). Operator confirmed
"authorize" in <1 minute. Total cost: ~30 seconds of chat
overhead. Cost-if-wrong-assumption: a re-done commit, a
re-confirmation round-trip, and potentially a wrong-direction
sub-surface (e.g., separate audit JSON file when the operator
actually wanted journal-cohesive storage).

Forward-applicable: any design-gate answer whose implementation
requires touching a src/ file that the prompt's Out-of-scope
clause does NOT enumerate by name. The HALT is cheap; the
recovery from an unauthorized touch is not.

## Parallel-dataclass pattern across package boundaries (S22 folding)

When two packages need the same record shape but one shouldn't
depend on the other, define the dataclass twice (parallel
definitions) and let callers do field-by-field copy at the seam.
S22 has `robots_gate.BypassAuthorization` (scraper package) and
`cost_journal.BypassAuditEntry` (classifier/pipeline package)
with identical 7-field shapes. Compared alternatives:

  (a) Shared class in scraper, imported by cost_journal:
      cost_journal → scraper dependency (cross-package, wrong
      direction for the architecture where scraper outputs feed
      the classifier).
  (b) Shared class in cost_journal, imported by scraper:
      scraper → classifier dependency (also wrong direction;
      scraper shouldn't know about cost-journal).
  (c) Parallel definitions, trivial conversion at seam:
      no cross-package import; each module owns its dataclass;
      callers map field-by-field. ← S22 chose this.

The trivial-conversion cost is real but small (7-field copy at
the gate-to-journal boundary, in a single call site). The
no-cross-package-import benefit is real and durable (either
module can evolve its field set independently as long as the
seam-mapper is updated).

Forward-applicable: any cross-package audit-record shape where
the producer and the persister live in different sub-packages.
The parallel pattern is the right default when the shape is
small and stable; lifting to a shared types package is the right
choice when the shape grows large or many consumers emerge.

## Per-module commit shape scales to 4+ commits cleanly (S22 folding)

Q-SHARED.1's "per-module commits" choice can land 4 or more
distinct commits per session without losing bisectability or
clarity. S22 landed 4 commits (shim + loader + journal + docs);
each had its own verification table, its own commit-message file
at `/tmp/s22-c<N>-msg.txt`, its own "Confirm to commit?" gate.
If a downstream consumer breaks at any point, `git bisect` lands
on the right commit directly.

Compared to a bundled "shim + loader + journal + docs" single
commit (~750 LOC impl + ~1100 LOC tests + 200 LOC docs):

  - Single commit body would have been a 200-line summary,
    much harder for a reviewer to skim.
  - `git bisect` would land on the single commit and require
    manual investigation to find which sub-surface broke.
  - Cherry-picking one sub-surface to another branch would not
    be possible without intermediate untangling.

The per-commit overhead (4 verification tables, 4 commit-message
files, 4 confirm-cycles) was ~5 minutes of chat overhead total —
small relative to the implementation work.

Forward-applicable: when Q-SHARED.1 chooses per-module, do not
collapse sub-surfaces into a single commit even when context
pressure tempts it. The verification table + commit body
discipline scales sub-linearly; bisectability + reviewability
scale super-linearly the more commits there are.

## Phase-2 estimate-vs-actual disclosure in commit body (S22 folding)

When Phase 2 design-gate options cite a size estimate (e.g.,
"~1-2 KB" or "150-250 LOC") and the actual implementation
diverges, disclose the variance in the commit body with a brief
reason. S22 Q-F.6's "minimal-first" option cited ~1-2 KB; the
actual `docs/CRAWLING_POLICY.md` shipped at 8.1 KB. The commit
body disclosed: "robots-only but thorough; full-doc alternative
would have been mostly empty deferred sections."

The disclosure gives operators a calibration anchor for future
Q-F.6-shape decisions and a one-sentence summary of why the
estimate was off. Without the disclosure, future reviewers would
have to compute the variance themselves and guess at the reason.

Forward-applicable: any Phase 2 option whose label or description
includes a size or LOC estimate. If the actual ships more than
~2x the estimate (high or low), disclose in the commit body with
the reason. Saves a reviewer round-trip.

## Bisectability vs Phase-1-named commit shape (S23 folding)

Phase 1's commit-shape decision (Q-SHARED.1 per-module) is a plan,
not a hard contract. When implementation surfaces an architectural
constraint that forces atomic file-pairs across the Phase-1-named
boundary, surface for operator authorization to deviate — do NOT
pattern-apply the original Phase 1 wording.

S23 case: Phase 1 named commit 2 as "vmss_worker.py +
scripts/vmss/cloud_init.template.yaml". Implementation surfaced
that `render_cloud_init`'s strict-mode unsubstituted-placeholder
check (job_runner.py:743 — `if leftover: raise ValueError(...)`)
requires the template placeholder and the substitutions-dict entry
to land in the SAME commit. Splitting them would break
test_job_runner.py mid-sequence and fire the cumulative test-count
gate. Resolution: cloud-init template touch moved to commit 3 with
job_runner.py; operator authorized the deviation in a focused
AskUserQuestion presenting the three options (defer / bundle /
accept-temp-breakage).

Forward-applicable: any time the smallest atomic bisectable unit
straddles a Phase-1-named commit boundary, surface the trade-off
explicitly. Common triggers: strict-mode validators (template +
substitutions dict, schema + serializer, parser + grammar),
mutual-import-order constraints, lockstep config/code edits.
Indicator: a per-commit checkpoint that would fail mid-sequence
even though the end-of-sequence state is correct.

## Production-vs-test journal asymmetry (S23 folding)

When production code uses one journal API (e.g., append-only
writer callback) and tests need another (e.g., CostJournal with
read-modify-write semantics), explicitly defer durable-persistence
wiring to a follow-up commit AND disclose the deferral in the
touching commit's body. The integration test pins the deferred
contract via the test API, proving the end-to-end pipeline works
even though production still goes through a simpler intermediate.

S23 case: worker_loop.py uses an append-only `journal_writer`
callback (per-shard ShardOutcome lines). The S22 W A.2 work added
`with_robots_bypass_appended` to `JournalState`, which lives on
the read-modify-write `CostJournal` API — a different surface.
Wiring worker_loop to open a CostJournal handle from
config.cost_journal_url at worker boot is its own scope (~50-100
LOC of URL-parsing + run_id derivation + initial-state handling).
Resolution: commit 4 (worker_loop wiring) shipped a log-only
`bypass_audit_writer` closure in `scrape_stage2_pages_invoker`
that emits LOG.warning per bypass. Commit 5's tmp_path integration
test wired a real `LocalFSCostJournal`-backed writer via
`record_bypass_audit`, pinning the Q-G.4 contract end-to-end. The
production-durable-write follow-up was named in the carry-forward
list in SESSION_TRANSITION_TEMPLATE.md.

Forward-applicable: any time production code's existing journal/
persistence API doesn't match the durable contract a new feature
needs, AND opening the new API is its own scope, defer the
production-side wiring + pin the contract via the integration
test. Disclose the deferral explicitly so a future reviewer knows
the production path is a known intermediate, not an oversight.

## Source-verify line numbers per Phase 3 commit, not just at
   Phase 2 (S23 folding)

Line numbers in a > 1000 LOC file shift as commits land in the
same file. Phase 2 source-verification establishes initial
ground truth but doesn't guarantee freshness across subsequent
commits in the same session.

S23 case: Phase 2 source-survey via Explore subagent located the
3 pre-fetch sites in worker_loop.py at L2381 / L2300 / L2672 at
HEAD `4ec7b0a-1` (pre-commit-4). Before drafting commit 4's
edits, a re-survey ran at HEAD `872527e` (post-commit-3). The
numbers were unchanged THIS time (no commit between 1-3 touched
worker_loop.py), but the re-survey paid off by re-verifying the
import-block range + the `_acquire_one_domain_t1` body-start
position + the actual `await fetch(...)` syntax at each site,
all of which my edits referenced directly.

Forward-applicable: when a Phase 3 commit will touch a file
> 1000 LOC AND prior commits in the same session touched the
same file (or any file in the chain via imports), re-run the
Explore-subagent source-survey at session-current HEAD before
drafting edits. Cost: ~30 seconds of subagent time. Benefit:
catches stale line numbers + stale function names + stale call-
site shapes that would otherwise cause Edit-tool exact-match
failures or — worse — successful edits at the wrong location.

## Cumulative test-count gate with new-file invocation expansion (S23 folding)

When each per-module commit adds a NEW tests/foo/test_X.py path
to the suite invocation, the gate's "never decreases" rule must
be read as "the same path-set's count never decreases", not
"absolute count never decreases". The path-set grows each
commit; the absolute count jumps because pre-existing tests in
the newly-included file now appear in the gate.

S23 case: at commit 2 (vmss_worker), the invocation expanded
from 11 paths to 12 by adding tests/orchestrator/test_vmss_worker.py.
The combined count went 573 → 647 (+74). Of those +74, only +7
were S23-new tests (the new tests for the robots-bypass-config-
path field). The remaining +67 were pre-existing test_vmss_worker
tests that just joined the invocation. The gate's "never
decreases" invariant was preserved (573 ≤ 647), but a naive read
of "+74 tests this commit" would be wrong.

Forward-applicable: in commit messages, distinguish:
- "Net-new tests at commit N: X" (truly added this commit)
- "Pre-existing tests in newly-included path: Y"
- "Combined-suite invocation count: previous + X + Y"

This bookkeeping discipline preserves the test-count gate's
auditability across the per-module commit-chain growth pattern.
S23 used this format in every commit body; it scaled to 5
commits without confusion.

## False-premise verification questions during Phase 2 (S23 folding)

Operator may probe during Phase 2 (or any phase) with questions
referencing decisions that were NOT actually pinned on the
record. The right response is honest correction, not
confabulation — never invent an answer that "sounds plausible"
for a question whose premise is wrong.

S23 case: after Phase 2 batch 1 closed, operator asked: "What
did I answer for Q-G.1.1 cache invalidation policy? Also, for
1.TAG, was it defer vs workstream-a-week2-end?" Q-G.1.1 had
NEVER been asked (only Q-G.1 was on file). 1.TAG had been
answered "defer" with `workstream-a-week2-end` mentioned only as
an example inside one option's description, not as a separate
option. Both probes had false premises.

The right response is to:
1. State plainly that Q-G.1.1 was never asked — no answer on
   record.
2. Surface the related real gap (cache lifetime was not
   explicitly pinned at Q-G.1; only the per-acquisition-call
   ii-a lifetime was implicit).
3. Propose a default for the unpinned gap; ask if operator
   wants to confirm or override.
4. Correctly recall 1.TAG = "defer" and clarify the option-shape
   (workstream-a-week2-end was illustrative, not selected).

After honest correction, operator pinned the cache-lifetime
default explicitly ("per-_acquire_one_domain_t1 invocation, no
cross-call cache") and authorized Phase 3.

Forward-applicable: never confabulate answers for verification
questions whose premise doesn't match what was actually pinned.
Operators may test this deliberately. The honest "I didn't ask
that; here's what we did pin" pattern catches design-gate gaps
that would otherwise become implicit decisions at Phase 3 commit
time. False-premise questions are a feature, not an attack.

---

## Tightened-precondition test-fixture retargeting (S24 folding)

When a src/ change introduces a stricter precondition that
PRE-EXISTING tests fail under (because the old tests supplied
"harmless placeholder" values the old code never USED), the fix
is fixture retargeting in the SAME commit as the src change.
Never split src + fixture across commits, because the intermediate
state is RED and bisectability suffers.

S24 Candidate I example: the new `_open_cost_journal_for_worker`
helper enforces a Q-I.1 file://-only precondition on
`config.cost_journal_url`. The PRE-S23 test_stage2_pages_invoker_*
tests in `tests/orchestrator/test_worker_loop.py` (5 of them) hard-
coded `cost_journal_url="abfss://j@x.dfs.core.windows.net/c.jsonl"`
as a placeholder — the old code never opened that URL, so the
abfss:// string was harmless. With the new precondition, those 5
tests immediately regress at the helper's NotImplementedError
guard.

Resolution: commit 1 of S24 (`48c324a`) updated those 5 fixture
sites in the SAME commit as the src/ change. Each call to
`_config(...)` gained a `cost_journal_url=f"file://{tmp_path}/cost.jsonl"`
override. No test logic or assertions changed; only the
placeholder value. The commit body documents the change under a
"Test changes" section that names each of the 5 affected tests.

Forward-applicable: any time a src/ change tightens a previously
loose precondition, run the FULL pre-existing test suite first;
treat any new regressions as fixture-update territory (NOT
src-change-rollback territory) AS LONG AS the test SEMANTIC INTENT
is preserved. Bundle the fixture updates with the src change to
preserve bisectability. Document in the commit body. Surface to
operator only if the fixture update would change a test assertion
(not just an input placeholder) — that's a different conversation.

---

## Test against public API surface only (S24 folding)

When unit-testing helpers that consume a third-party class (here:
`LocalFSCostJournal`), probe IDENTITY via the public API, not
private construction args. Drafting tests against `journal.journal_dir`
and `journal.run_id` immediately AttributeError'd because those
fields are stored as `_journal_dir` / `_run_id` (private; no public
property exposes them under those names).

S24 Candidate I example: the unit tests for
`_open_cost_journal_for_worker` initially asserted on
`journal.journal_dir == tmp_path` and `journal.run_id == crawl_date`.
Both attribute accesses failed. The public surface that DOES
expose the relevant info is `.path` (a `Path` property returning
`<journal_dir>/run_<run_id>.json`). Re-targeting:

  assert journal.path.parent == tmp_path     # confirms journal_dir
  assert journal.path.name == "run_2026-05-23.json"  # confirms run_id

This test-API is also more durable: it survives any refactor that
renames the private fields (which is the kind of refactor LESSONS
encourages — private fields can change without breaking external
callers).

Forward-applicable: when writing tests for a helper that returns
or consumes a third-party class, prefer probing PUBLIC API
(properties, `__repr__` output, behavior under known inputs) over
the third-party's construction args or private attrs. The test
suite becomes invariant under internal refactors of the
third-party class.

---

## Q-I.7 "Both" test corpus shape works for small candidates (S24 folding)

For a 50-200 LOC src/ candidate, the "both" test corpus shape —
focused unit tests in a NEW file + appended end-to-end tests in
the existing integration file — gives strictly better coverage than
either alone. The unit file provides a stable abstraction layer
that survives integration-site refactors; the integration extension
verifies the production wiring against the same helpers.

S24 Candidate I shipped:
- `tests/orchestrator/test_worker_loop_persistence.py` (NEW; 325
  LOC; 12 unit tests organized by helper).
- 3 new end-to-end tests appended after the 4 S23 tests in
  `tests/orchestrator/test_robots_gate_integration.py` (drives
  `scrape_stage2_pages_invoker` with real fsspec + httpx [stubbed
  fetch_one + stub gate factory]).

The two surfaces have non-overlapping coverage:
- Unit tests monkeypatch single dependencies (e.g., monkeypatch
  `record_bypass_audit` to raise to test failure semantics) and
  assert on each helper's behavior in isolation. Run in <1s.
- Integration tests do NOT monkeypatch the helpers themselves;
  they monkeypatch the upstream sources (build_robots_gate,
  fetch_one) and observe the helpers' output against the on-disk
  journal state. Run in <3s.

Forward-applicable: for small-medium src/ candidates, default to
Q-I.7-style "Both" rather than single-file extension. Estimated
cost: ~30% more test LOC but ~10x faster mean-time-to-diagnose
when a regression lands (unit tests localize the broken helper;
integration tests confirm wiring intent).

---

## Q-I.6 "log + continue" closure-failure pattern (S24 folding)

When a write surface is BOTH on the latency-critical path AND
write-failure is compliance-only (not load-bearing for downstream
correctness), the canonical pattern is:

  def _writer(decision):
      if decision.bypass is None:
          return
      try:
          record_bypass_audit(journal=journal, decision=decision)
      except Exception:  # noqa: BLE001 — Q-I.6 log + continue
          LOG.exception(
              "robots_bypass audit persistence failed host=%s url=%s",
              decision.bypass.host,
              decision.bypass.url,
          )

The closure-failure pattern has three invariants:
1. Catches `Exception` (NOT bare `except:`) — silences crashes but
   not KeyboardInterrupt / SystemExit.
2. LOG.exception(...) captures the full traceback for post-hoc
   audit. Operators reading worker logs can still see what was
   dropped.
3. The closure returns normally on failure — the calling code
   (here: gate `evaluate` chain) cannot tell the audit write
   failed; the BYPASS_ALLOW fetch still proceeds.

The corresponding test pattern:

  monkeypatch.setattr(
      "barcada_scraper.orchestrator.worker_loop.record_bypass_audit",
      lambda **_: (_ for _ in ()).throw(RuntimeError("simulated outage")),
  )
  writer = _build_durable_bypass_writer(journal)
  with caplog.at_level(logging.ERROR, logger="vmss_worker.loop"):
      writer(decision)  # Must NOT raise
  assert any("authorized.test" in r.getMessage() for r in caplog.records)
  assert journal.read().state.robots_bypass_log == ()  # No partial state

Forward-applicable: when a write is on the latency-critical path
AND compliance-only, use log-and-continue. When it's load-bearing
for downstream correctness, RE-RAISE. The wrong choice in EITHER
direction is a bug: log-and-continue when load-bearing leaks
silent data loss; re-raise when compliance-only inverts the
availability priority. Decide at Phase 2 design-gate; test the
chosen semantics explicitly.

---

## Workspace HEAD delta tolerance — eval_data-only path (S24 folding)

The S22+S23 "Workspace HEAD delta tolerance" LESSONS pattern is
load-bearing across every session-open. S24 added a refinement:
operator-side commits between session-close and session-open are
tolerated ONLY when every affected path stays strictly within
`eval_data/`.

S24 Phase 0 confirmed the pattern: repo HEAD at S24 open was
`4bed9b9` (not the prompt's expected `6e6e4ca`), 1 commit ahead.
`git show --stat 4bed9b9` showed:

  eval_data/audits/step2_software_product_queue.jsonl  | 64 ----
  eval_data/audits/step3_professional_credentials_queue.jsonl | 21 +++++
  eval_data/stage1_labels.jsonl                        |  8 +--

All three paths are strictly under `eval_data/`. No src/, no
tests/, no scripts/, no docs/. The tolerance check passed cleanly;
S24 proceeded without HALT.

The procedural rule:
1. At Phase 0 Step 0.1, check `git log --oneline <expected>..HEAD`.
2. For each unexpected commit, run `git show --stat <sha>`.
3. If EVERY changed path is under `eval_data/` → tolerate, proceed.
4. If ANY path is outside `eval_data/` → HALT, surface to operator
   before continuing. This is a hidden src/ touch that may invalidate
   the session's assumptions.

Forward-applicable: this rule is mechanical — verify with `git show
--stat`, NEVER assume tolerance from commit subject lines alone
(commit subjects can be misleading; a "labeling cleanup" subject
could conceal a src/ touch). The path-stat is the authoritative
signal.
