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
