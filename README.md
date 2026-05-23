# Barcada Crawler Audit Workspace

Operational workspace for the audit and remediation of the barcada-scraper
crawler. Lives outside the repo by design — these are planning and audit
artifacts, not part of the codebase itself.

## Contents

- `AUDIT_DIRECTIVE.md` — Read-only audit directive (the "how" of the audit)
- `AUDIT_REPORT.md` — Full code audit report (2026-05-18)
- `FIXTURE_AUDIT_DIRECTIVE.md` — Read-only fixture audit directive
- `FIXTURE_AUDIT_REPORT.md` — Fixture quality audit report
- `BARCADA_CRAWLER_REMEDIATION_PLAN.md` — Consolidated 20-week plan
- `scripts/` — Workspace-side helper scripts (see [Scripts](#scripts))
- `working/` — Ephemeral scratch (gitignored)

## Usage

This workspace is read-write for planning documents and read-only with respect
to the audited repository. Claude Code sessions configured to audit
`/Users/administrator/projects/barcada-scraper` write only into this workspace,
never into the repo.

## Scripts

### `scripts/filter_stage1_labels.py`

Filters the eval label set
(`/Users/administrator/projects/barcada-scraper/eval_data/stage1_labels.jsonl`)
by field values and writes the matching records to a target file in the same
JSONL format (original key order preserved). Stdlib-only; no dependencies.

Available fields: `schema_version`, `domain`, `evaluation_split`, `label`,
`confidence`, `labeler_id`, `labeled_at`, `source`, `notes` (scalar), and
`rationale_keywords` (list).

Constraints are AND-ed together; comma-separated values within one constraint
are OR-ed:

- `-f/--filter FIELD=V1,V2` — keep where FIELD equals a value. For the list
  field `rationale_keywords`, keeps on any overlap (or all values present with
  `--match-all`).
- `-x/--exclude FIELD=V` — drop matching records.
- `-c/--contains FIELD=SUBSTR` — case-insensitive substring match (handy for
  `notes` / `domain`).
- `--list-fields` — print the fields and their value distributions, then exit.
- `--dry-run` — count matches without writing output.

```bash
# Discover the fields and value distributions
python3 scripts/filter_stage1_labels.py --list-fields

# Business rows in the train split → new file
python3 scripts/filter_stage1_labels.py -f label=business -f evaluation_split=train -o train_biz.jsonl

# Non-business rows tagged software_product
python3 scripts/filter_stage1_labels.py -f label=non-business -f rationale_keywords=software_product -o out.jsonl
```

`--input` defaults to the stage1 path but is overridable, so the same script
works on any JSONL label file. It refuses to overwrite an existing output
(without `--overwrite`) or the input file itself. Matched records are
re-serialized from parsed JSON, so output is semantically identical to the
source but not a byte-for-byte copy of each line.

## Updating the Plan

The remediation plan is a living document. Update it as workstreams complete,
findings evolve, or scope changes. Commit each update with a message
describing what changed and why.

## Re-running Audits

The audit directives are repeatable. Re-run them quarterly or after major
changes to the crawler. Each re-run produces an updated report; preserve
prior reports as historical record (rename with date suffix before
overwriting).

## When implementing the remediation plan, for each workstream, follow these steps
1. Open new chat session when starting a new work unit
2. Point at the plan and the specific workstream item
3. Discuss the approach in chat — what to do, what to avoid, acceptance criteria
4. Draft a Claude Code prompt together
5. Take the prompt to Claude Code in your CLI
6. Implement on a branch with the prompt as guidance
7. Come back to chat if you hit unexpected issues or need to review output
8. Merge when validated against baselines and tests
9. Update the plan if anything changed (effort estimates, scope, sequencing)
10. Update SESSION_LOG.md if you're keeping one
11. Commit and push the workspace
12. Close the session when the work unit is done

## Session handoff documents (added Session 11)

Three workspace-side documents carry remediation context across Claude Code
sessions:

- `SESSION_LOG.md` — chronological record, one entry per session. Captures
  scope, commits landed, operator decisions, deferred items, test surface
  changes, cost & schedule tracking. Append-only; never edit prior entries.
- `SESSION_TRANSITION_TEMPLATE.md` — cold-start handoff document. Overwritten
  at each session close with the next session's required reading list, repo
  state snapshot, active task list, locked artifacts reminder, deferred
  prose-only fixes register, and the next concrete work unit. Pair with
  the latest `SESSION_LOG.md` entry to be productive in ~10 minutes from
  cold.
- `LESSONS.md` — durable operator patterns and observed conventions
  (commit-message format, fixture-handling patterns, diagnostic patterns,
  discovery escalation, workstream/commit shape patterns, detector-precision
  findings, verify-before-asking discipline). Add a section only when a
  forward-applicable pattern surfaces that isn't already documented.

Reading order for a new session: `SESSION_TRANSITION_TEMPLATE.md` first,
then the latest `SESSION_LOG.md` entry, then `LESSONS.md`, then the
relevant section of `BARCADA_CRAWLER_REMEDIATION_PLAN.md`.
