---
name: project-context-architect
description: Maintain file-based project context across sessions and agent handoffs. Use when resuming a project in a new chat, handing work to another coding agent, fixing stale documentation or conflicting TODOs, or organizing AGENTS.md and project state, architecture, and runbook docs. Manages project context, not business implementation.
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

- Start with applicable instructions and current project state once per session. Scope routine context reads and searches to those files and the relevant authority sections. Reuse unchanged sections, including in a long runbook. Refresh the target after another writer or a context gap. Consult current source or runtime evidence when the task requires it.
- Skip archives, superseded material and scratch notes in routine reads and searches. If the task or a current owner cites a live requirement, acceptance condition or needed evidence, read that passage wherever it lives. For an old issue, follow the evidence link from its decision or owner; if missing, search the likely archive by issue or symptom.
- Keep verified facts, plans and uncertainty distinct. Implementation does not establish intended product rules; source changes do not prove build, deployment or acceptance. Resolve conflicts with evidence appropriate to the claim; ask only when a material semantic choice remains unresolved.
- Preserve business behavior, project instructions, unrelated edits and valuable history. Check affected consumers before moving or rewriting a document. On a move or heading rename, search project docs, including history, for the old filename or anchor and keep inbound links working.
- Report routine progress in chat. Update changed facts in their owner and retire stale summaries. Save a separate report for a requested deliverable or lasting evidence that would otherwise be lost. Record a lasting choice and its reason in decisions. Cite shared project evidence by relative path and external originals by stable link or retrievable record ID.
- Check once per coherent batch of changes, not after each file write. Expand reading when ownership, evidence or dependencies are unclear; stop expanding once the affected claims are reconciled. A bounded check cannot establish whole-project readiness.
- Support cross-platform work through lightweight relay: the agent the user asks to take over handles integration for the current task, checks relevant changes and continues from existing state. Only known parallel work needs agreed file scopes and one integrator. Follow [relay guidance](references/maintenance.md#cross-platform-relay); do not introduce task boards, locks or approval steps for routine work.

## Completion and reporting

For routine maintenance, verify the changed claims, dependent summaries, diff and affected links. Use the existing project check when required by its workflow; for the bundled read-only checker or requested integration, see [project-checks.md](references/project-checks.md). A script may scan configured documents without loading their full contents into model context. Mechanical PASS does not verify factual truth.

Run the full [fresh-session test](references/fresh-session-test.md) after BOOTSTRAP or broad REFACTOR, and for requested handoff/milestone readiness. During narrow maintenance, recheck only affected handoff answers. Unresolved stale authority within scope means the work remains incomplete; report the concrete blocker without guessing.

Report the outcome, affected owners, verification scope and material uncertainty. Small updates need only a short paragraph; omit empty fields and unchanged read orders. For a broad audit, name the mode and use `GOOD` only when all seven handoff answers pass and no material conflict remains in the declared scope. Use `NEEDS_ATTENTION` for found defects and `NOT_ASSESSED` when full readiness was not tested. No authority impact means no authority edit; no mandatory no-op report is needed unless relevant to the request.
