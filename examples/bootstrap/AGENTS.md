> Fictional example (`remindr`); illustrative claims, not measured test results.

# Agent Instructions

## Project rules

- Python 3.11+; dependencies limited to stdlib, Flask and PyYAML.
- Reminder sources stay under `reminders/` as YAML.
- Tests run offline. Development must not send real Slack/email messages.

## New Session Protocol

L0 Orientation — read first:
1. [AGENTS.md](AGENTS.md)
2. [PROJECT_STATE.md](PROJECT_STATE.md)

L1 Task Context — then read only what the task requires:
- architecture → [ARCHITECTURE.md](ARCHITECTURE.md)
- rationale → [DECISIONS.md](DECISIONS.md)
- operation → [RUNBOOK.md](RUNBOOK.md)

Load history and broad source trees only when the current task provides a reason.

## Authority Maintenance Protocol

Apply during authorized work that changes project facts. Read-only review reports proposed changes. If no authority fact changes, leave authority untouched.

### Incremental maintenance

1. Read L0 once per session, then only the L1 sections needed for the task. Reuse current context; refresh a target that may have changed before editing. Track Current Work only when the task changes the project's main work or Next.
2. For a changed fact, read its owner section, verify new evidence, and search active authority and known summaries for the subject, aliases and links. Follow known dependencies; an absent keyword match does not establish that no dependent summary exists. Expand only if ownership, evidence or impact is unclear. No full-file reread or permanent delta table is required for every write.
3. Update the owner in the same task and retire affected stale summaries, issues and Next entries. Codify an accepted user decision before work depends on it. Leave unrelated facts and history alone; link useful evidence instead of appending a delivery diary.
4. Keep source, build, loaded service and acceptance distinct. Label plans and unknowns; implementation alone cannot rewrite a product rule. Preserve existing rules and runtime consumers when moving or rewriting documents.
5. At the end of a coherent batch, inspect the diff, changed claims, dependent summaries and links. Run the documented project check if required by the workflow; review relevant findings without treating mechanical PASS as truth. Report unrelated failures separately; do not claim the whole scan passed. No per-write check or repeated unchanged report is needed.

Use existing owners: status/work/issues/Next in project state; mechanisms in architecture; repeatable commands in the runbook; durable rationale in decisions; constraints in their established rule owner. Create a separate owner only when its content warrants one. Keep handoff pointers compact rather than duplicating current status.

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
