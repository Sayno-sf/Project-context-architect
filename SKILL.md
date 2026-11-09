---
name: project-context-architect
description: Establish and maintain a project's smallest authoritative context. Use to create handoff docs, reconcile stale project facts, consolidate conflicting documentation, or check fresh-session readiness. Manages project context, not business implementation.
---

# Project Context Architect

Keep a small, current authority set: one fact per owner, links from summaries, history clearly separated. An explicit current user decision can supersede stale authority; record it in the owner during authorized maintenance. Old chat history is not current authority.

Default to `.architect/` for project state, architecture, operations, decisions and context history. Keep the project's agent entry file at its discoverable root location and link into that folder. Create only documents with substantive content; keep `.architect/` versioned when the project uses version control.

## Choose the scope

**Routine maintenance is the default for a bounded update.** Read the affected owner section, verify the new evidence, find dependent summaries, replace stale claims, and check the diff and links. Follow [incremental maintenance](references/maintenance.md). Do not turn a small update into a repository audit or require a full handoff test.

For broader requests, use one mode and read only its reference:

- **BOOTSTRAP** — establish a missing handoff system: [bootstrap.md](references/bootstrap.md).
- **REFACTOR** — consolidate scattered or conflicting context: [refactor.md](references/refactor.md).
- **CHECK** — inspect requested context or handoff readiness: [check.md](references/check.md). Read-only unless repairs are requested.

Honor explicit scope. A finding may justify a wider inspection; it does not authorize wider edits. Read [authority-model.md](references/authority-model.md) when assigning owners, creating documents, or resolving disputed ownership. Use the [fictional examples](examples/bootstrap/) only when a document's shape is unclear; do not load the whole example set for an ordinary edit.

## Working rules

- Read applicable project instructions and L0 (the convention file and current project state) once on entering a project/session. Reuse already-read context; refresh changed sections before editing, especially after another writer or a context gap. Read source and L1 documents only to settle relevant claims.
- Keep verified facts, plans and uncertainty distinct. Implementation does not establish intended product rules; source changes do not prove build, deployment or acceptance. Resolve conflicts with evidence appropriate to the claim; ask only when a material semantic choice remains unresolved.
- Change context artifacts within the request. Preserve business behavior, user instructions and unrelated edits. Before moving or substantially rewriting a document, inspect relevant runtime/load/build consumers and inbound links. Archive valuable history recoverably.
- Replace current claims in their owner and retire affected stale summaries. Leave unchanged facts alone. Commands belong in the runbook; durable rationale belongs in decisions. Do not create empty owners, per-task logs or permanent fact ledgers for compliance.
- Check once per coherent batch of changes, not after each file write. Expand reading when ownership, evidence or dependencies are unclear; stop expanding once the affected claims are reconciled. A bounded check cannot establish whole-project readiness.
- Support cross-platform work through lightweight relay: the agent the user asks to take over handles integration for the current task, checks relevant changes and continues from existing state. Only known parallel work needs agreed file scopes and one integrator. Follow [relay guidance](references/maintenance.md#cross-platform-relay); do not introduce task boards, locks or approval steps for routine work.

## Completion and reporting

For routine maintenance, verify the changed claims, dependent summaries, diff and affected links. Use the existing project check when required by its workflow; for the bundled read-only checker or requested integration, see [project-checks.md](references/project-checks.md). A script may scan configured documents without loading their full contents into model context. Mechanical PASS does not verify factual truth.

Run the full [fresh-session test](references/fresh-session-test.md) after BOOTSTRAP or broad REFACTOR, and for requested handoff/milestone readiness. During narrow maintenance, recheck only affected handoff answers. Unresolved stale authority within scope means the work remains incomplete; report the concrete blocker without guessing.

Report the outcome, affected owners, verification scope and material uncertainty. Small updates need only a short paragraph; omit empty fields and unchanged read orders. For a broad audit, name the mode and use `GOOD` only when all seven handoff answers pass and no material conflict remains in the declared scope. Use `NEEDS_ATTENTION` for found defects and `NOT_ASSESSED` when full readiness was not tested. No authority impact means no authority edit; no mandatory no-op report is needed unless relevant to the request.
