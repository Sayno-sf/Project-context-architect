> Fictional example (`remindr`); illustrative claims, not measured test results.

# Agent Instructions

## Project rules

- Python 3.11+; dependencies limited to stdlib, Flask and PyYAML.
- Reminder sources stay under `reminders/` as YAML.
- Tests run offline. Development must not send real Slack/email messages.

## New Session Protocol

L0 Orientation — read first:
1. [AGENTS.md](AGENTS.md)
2. [PROJECT_STATE.md](.architect/PROJECT_STATE.md)

L1 Task Context — then read only what the task requires:
- architecture → [ARCHITECTURE.md](.architect/ARCHITECTURE.md)
- rationale → [DECISIONS.md](.architect/DECISIONS.md)
- operation → [RUNBOOK.md](.architect/RUNBOOK.md)

Read L0 once per session and reuse unchanged sections. Skip archives, superseded material and scratch notes in routine searches and reads. If the task or a current owner cites a requirement, sign-off or evidence needed now, read that passage even in a phase report. For an old issue, follow its decision or issue link, or search the likely archive by symptom if the link fails. Read source when needed.

## Authority Maintenance Protocol

Report routine progress in the conversation. Before writing project documentation, check whether a verified fact changed in an existing owner, the task calls for a document, or original evidence needs to be preserved for later use. If none apply, finish in chat. Read-only review reports proposed changes.

### Incremental maintenance

1. Refresh the affected section before editing if it may have changed. Track Current Work only when the task changes the project's main work or Next.
2. For a changed fact, read its owner section, verify new evidence, and search active authority and known summaries for the subject, aliases and links. Follow known dependencies; an absent keyword match does not establish that no dependent summary exists. Expand only if ownership, evidence or impact is unclear. No full-file reread or permanent delta table is required for every write.
3. Update the owner in the same task and retire affected stale summaries, issues and Next entries. Codify an accepted user decision before work depends on it. Leave unrelated facts and history alone; link useful evidence instead of appending a delivery diary.
4. Distinguish source, build, loaded service and acceptance. Label plans and unknowns. Implementation alone cannot change product rules. Preserve runtime consumers. For a file move or heading rename, search project docs, including history, for the old filename or anchor and verify affected links after the edit.
5. At the end of a coherent batch, inspect the diff, changed claims, dependent summaries and links. Run the documented project check if required by the workflow; review relevant findings without treating mechanical PASS as truth. Report unrelated failures separately; do not claim the whole scan passed. No per-write check or repeated unchanged report is needed.

Keep status in project state, mechanisms in architecture, commands in the runbook and constraints in their rule owner. Record a lasting choice and its reason in decisions. Link shared evidence by relative path, or cite the external original by stable URL or retrievable record ID. A recurring fault can link to evidence from its issue or runbook entry. Keep handoff pointers compact.

### Cross-platform relay

- **Take over naturally.** When the user asks another agent to continue, that agent takes integration responsibility for the current task. Use existing project state and available work summaries; keep verified results, unfinished work and Next current when handing off. Do not assume access to another platform's chat or require a separate handoff artifact.
- **Check relevant changes.** Compare task-relevant claims with current files. Expand only for contradictions, missing evidence or other writers' changes. Reuse applicable verification when its inputs and environment have not changed; do not repeat all prior tests or the full handoff review merely because the platform changed. Git is optional.
- **Coordinate only actual parallel work.** Briefly agree distinct file scopes and one integrator. Executors may update their scoped technical docs; the integrator reconciles overall state. If scopes overlap, agree one writer or sequence the edits. Sequential work needs no registration, lock, role file or extra approval. These are cooperation rules, not enforced concurrency protection.

### Full handoff check

After establishing or broadly reorganizing context, or when handoff/milestone readiness is requested, answer all seven from L0 and its named L1 links with file/section evidence:

1. Project and audience.
2. Current status and work.
3. Entry point and start command.
4. Components, data flow and state ownership.
5. Hard constraints and non-goals.
6. Next action and stop condition.
7. Existing owners/links for architecture and operations.

A category with no implementation/content yet may be explicitly absent; an existing capability needs a documented owner. Missing or contradictory answers fail readiness. Ordinary maintenance rechecks only affected answers and does not claim full readiness. Affected stale authority remains incomplete; report material uncertainty without guessing. Document review is a self-check unless an independent session actually performed acceptance.
