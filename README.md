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
- `working/` — Ephemeral scratch (gitignored)

## Usage

This workspace is read-write for planning documents and read-only with respect
to the audited repository. Claude Code sessions configured to audit
`/Users/administrator/projects/barcada-scraper` write only into this workspace,
never into the repo.

## Updating the Plan

The remediation plan is a living document. Update it as workstreams complete,
findings evolve, or scope changes. Commit each update with a message
describing what changed and why.

## Re-running Audits

The audit directives are repeatable. Re-run them quarterly or after major
changes to the crawler. Each re-run produces an updated report; preserve
prior reports as historical record (rename with date suffix before
overwriting).
