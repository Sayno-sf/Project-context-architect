# Incremental maintenance

Start with the intended use. A progress update belongs in the conversation. If a project fact changed, use the steps below on the affected section. If the user asked for a report or a finding needs a durable evidence record, reuse an existing report or save the useful original once. A phase ending on its own calls for no new file.

1. **Locate.** Read the current owner section with enough surrounding context to understand its subject and environment. Reuse recent observations, but refresh the target before editing if it may have changed. If no old claim exists, use the established owner for that category.
2. **Verify.** Establish what the new evidence supports. A newer date does not settle a conflict; source, build, loaded service and acceptance are separate claims. Keep missing evidence explicit.
3. **Find affected summaries.** Search active owners and known entry summaries (including README when relevant) for the subject, aliases and links. Follow active dependencies in the read map, including a cited requirement or acceptance record inside a phase report. Read the relevant passages. Include Current Work, Known Issues, Next or handoff only when they depend on the changed fact.
4. **Reconcile.** Replace the owner's old claim and retire stale projections in the same authorized task. Link useful evidence/history instead of appending dated status paragraphs. Do not rewrite unrelated facts or historical statements merely because the same term appears there.
5. **Close the batch.** Review the diff (or a before/after snapshot without Git), affected links and handoff answers. If a local checker is required, run it at the workflow checkpoint, not after every edit. Stop when the changed facts have one owner, their known projections agree, and material unknowns are explicit.

For example, closing a verified migration updates its state entry and any issue/Next summary that still says pending. It does not require rereading the whole architecture or runbook unless the migration changed those facts.

For a move or heading rename, search project docs, including hidden `.architect/history/`, for the old filename or anchor. Check matching links relative to their referring files. Update affected links or preserve a compatible target, then verify they resolve. An exact lookup needs only matching lines.

Expand reading when evidence conflicts or ownership or impact is unclear. If the impact still cannot be bounded, report the limit and propose a broader audit.

Full seven-question review is for BOOTSTRAP, broad REFACTOR, or requested handoff/milestone readiness. Ordinary work rechecks only affected answers. No authority change means no maintenance write or maintenance-specific check; existing project-required checks still apply.

## Cross-platform relay

- **Take over naturally.** When the user asks another agent to continue, that agent takes integration responsibility for the current task. Use existing project state and available work summaries; keep verified results, unfinished work and Next current when handing off. Do not assume access to another platform's chat or require a separate handoff artifact.
- **Check relevant changes.** Compare task-relevant claims with current files. Expand only for contradictions, missing evidence or other writers' changes. Reuse applicable verification when its inputs and environment have not changed; do not repeat all prior tests or the full handoff review merely because the platform changed. Git is optional.
- **Coordinate only actual parallel work.** Briefly agree distinct file scopes and one integrator. Executors may update their scoped technical docs; the integrator reconciles overall state. If scopes overlap, agree one writer or sequence the edits. Sequential work needs no registration, lock, role file or extra approval. These are cooperation rules, not enforced concurrency protection.

