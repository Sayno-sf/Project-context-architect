# CHECK

Inspect the requested context without changing it. Use a bounded check for a named fact or document; use a full handoff check when asked about fresh-session or milestone readiness. CHECK does not automatically become REFACTOR.

## Inspect proportionally

Use L0 Orientation (`AGENTS.md` and `PROJECT_STATE.md`, or established equivalents) and follow only the L1 pointers needed for the scope. Reuse already-read context. For a disputed claim, apply [category-aware verification](authority-model.md#category-aware-conflict-verification).

Look for defects relevant to the request:

- competing owners, stale status or plans presented as implemented;
- old designs or history still presented as current;
- missing links, invalid commands or changed entry points;
- bloated L0 or a read map requiring broad history/source reads;
- duplicated protocols, forced no-op writes, or a completion rule that leaves affected facts stale.

A narrow fact check does not need a protocol overhaul. When evidence exposes a wider problem, report its consequence and the smallest repair; expand inspection only as needed to understand it.

## Repairs

Read-only findings name the owner, evidence and proposed repair. When repairs are requested, correct verified stale claims and their dependent summaries, preserve project-specific rules, and leave sound documents unchanged. Archive only history within the requested cleanup. Report broader restructuring or unresolved product choices instead of silently expanding the edit.

## Verify and report

For narrow checks, verify the affected claims and links using [incremental maintenance](maintenance.md), without its write steps. For handoff readiness, use the full [fresh-session test](fresh-session-test.md) and available [mechanical checks](project-checks.md). Do not install scripts, configuration or hooks during read-only CHECK.

State the inspected scope, result and remaining limits. Use `GOOD` only after the full handoff test passes with no material conflict in scope; use `NEEDS_ATTENTION` for concrete defects and `NOT_ASSESSED` for full readiness when only a narrow check was performed. An audit can finish while readiness remains `NEEDS_ATTENTION`.
