# Authority Model

Use this reference when deciding which document owns a fact, creating a missing authority document, or consolidating conflicting documents.

## Authority set

The set is deliberately small. BOOTSTRAP always establishes the agent convention file (by default `AGENTS.md`; see the naming rule below) and `PROJECT_STATE.md`. Create `ARCHITECTURE.md`, `DECISIONS.md`, and `RUNBOOK.md` only when their category has substantive current content. Existing projects receive only missing categories that are genuinely needed.

| Owner | Question it answers | Owns | Excludes |
|---|---|---|---|
| `AGENTS.md` | How should an AI agent work here? | Development protocol, review expectations, user constraints, prohibited behavior, new-session read protocol, authority-maintenance protocol | Current status, architecture narrative, sprint history |
| `PROJECT_STATE.md` | What is true now? | Overall status, current work, implemented capabilities, known issues, non-goals, next step, handoff capsule | Full history, long design rationale, duplicated commands |
| `ARCHITECTURE.md` | How is the current system composed? | Components, boundaries, dependency direction, state ownership, main data flows, codebase map, important entry points | Former architecture, speculative future design, sprint timeline |
| `DECISIONS.md` | Why do stable choices exist? | Accepted or explicitly superseded ADRs whose rationale matters later | Routine implementation details, status updates |
| `RUNBOOK.md` | How is the project operated? | Environment, variables, start/test/build commands, ports, verification, debug entry points, common operational failures | Product status and duplicated design material |

## Agent convention file naming

The development-protocol owner defaults to `AGENTS.md`, the cross-tool agent convention. Naming is a default, not a quota:

- Reuse a platform equivalent the project already maintains — `CLAUDE.md`, `COPILOT.md`, `GEMINI.md`, or another project-level agent instruction file — instead of creating a parallel `AGENTS.md`. Merge the two root protocols into that file and use its name wherever this skill says `AGENTS.md`.
- When the project has no equivalent, create `AGENTS.md`.
- Keep one canonical protocol owner. Preserve thin platform entry files when tooling requires them; they link or import that owner using the platform's supported mechanism instead of duplicating rules. Verify that the actual tools discover the owner; a filename substitution alone is not proof.
- Reports, read maps, and the fresh-session test name the file actually used.

## `README.md`

`README.md` is the human-facing entry page: explain what the project is, who it is for, and where to go next. It may summarize and link to authority, but it does not own volatile project status, detailed architecture, ADR rationale, or full operational commands.

## Optional authority

Add an optional owner only when the information is stable, substantial, and repeatedly needed:

- `DOMAIN.md` or `CONTEXT.md` owns domain vocabulary and meanings.
- `PRODUCT_RULES.md` owns durable product invariants and permission boundaries.
- `LEARNING_RULES.md` owns durable learning or pedagogical invariants.
- `CURRENT_SPRINT.md` owns a long, frequently changing execution contract only when `PROJECT_STATE.md > Current Work` is genuinely insufficient, such as a multi-person sprint with substantial acceptance criteria.

Prefer one existing filename when a repository already has an equivalent owner. Avoid parallel files such as both `DOMAIN.md` and `CONTEXT.md` unless they have visibly different ownership.

## One fact, one owner

Use the ownership table and optional categories above. Write the complete fact only in its owner. Other documents use a short contextual sentence and a relative link. A summary is a projection, not an independently maintained decision. A small category can remain in an existing suitable owner until its substance justifies a separate file.

## Maintaining current facts

Use [incremental maintenance](maintenance.md): read the affected section, verify evidence, locate dependent summaries, replace stale claims, and close the batch. Do not reread every authority file or create a delta artifact for each write. Broaden inspection only when dependencies or contradictions require it.

For volatile claims, identify the component/repository, environment, state, and verification evidence/date where relevant. Distinguish implemented source, built assets, loaded service, observed runtime and user acceptance. Evidence for one does not establish another. A mention of an adjacent deployment does not authorize access to it; respect task scope and mark unverified targets.

Architecture owns mechanisms and boundaries, the runbook owns repeatable operations, and project state owns current delivery and outstanding work. Keep one-off PIDs, test counts, backup manifests and migration receipts in evidence records. Closed issues leave Known Issues; completed tasks stop appearing as Current Work.

Keep L0 cheap to read. Review character count or estimated tokens, repeated claims and the effort to answer the seven handoff questions; line count alone hides long paragraphs. Split substantial L1 detail by stable responsibility and link to the relevant section. Do not add files merely to meet a numeric budget or push release history into CURRENT_SPRINT.md.

Before changing context files, inspect relevant consumers. If a prompt loader, CI job or runtime reads the file, a documentation edit may affect behavior. Preserve required paths, imports and runtime-facing content unless those behavior changes are part of the user's request.

## Category-aware conflict verification

For each conflict:

1. Identify its authority category.
2. Select evidence appropriate to that category:
   - runtime and configuration facts → current scripts, configuration, task runners, CI definitions, environment examples, or successful execution;
   - implementation state and entry points → current code, tests, and observed runtime behavior;
   - current work and delivery status → maintained project state, verified implementation progress, and explicit current user decisions;
   - architecture as implemented → current code and configuration, reconciled with accepted architectural decisions;
   - product invariants, permissions, and intended behavior → explicit current user decisions and their maintained authority owner; implementation is evidence only of whether the product currently conforms;
   - decision rationale → accepted ADRs or an explicit current user decision, not inference from code shape.
3. When edits are authorized, update the owner with verified truth and replace competing current-looking claims with a link, historical label, or explicit supersession marker. Otherwise report the proposed reconciliation.
4. Escalate a conflict that changes product meaning, permissions, or user-visible behavior when the evidence cannot settle it.

Observed implementation is evidence of implementation state, not automatically evidence of intended product truth. A buggy implementation that violates a maintained product rule is a defect signal, not permission to rewrite the rule.

Never synthesize incompatible claims into a compromise merely to close the conflict.

## Minimum document shapes

### Agent convention file (defaults to `AGENTS.md`)

Preserve existing project-specific instructions. Put the following protocols once in the project-root agent convention file (by default `AGENTS.md`; reuse the platform equivalent per the naming rule above); nested copies of that file may add local working rules but do not copy the root protocols.

Ensure the root file contains a concise section equivalent to:

```md
## New Session Protocol

L0 Orientation — read first:
1. `AGENTS.md`
2. `PROJECT_STATE.md`

L1 Task Context — then read only what the task requires:
- architecture → `ARCHITECTURE.md`
- rationale → `DECISIONS.md`
- operation → `RUNBOOK.md`
- domain terms → `DOMAIN.md` or `CONTEXT.md`
- stable product rules → `PRODUCT_RULES.md`

List only authority documents that exist and are relevant to this project.
Load history and broad source trees only when the current task provides a reason.
```

Also merge this event-driven write-back contract into the same root file:

```md
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
```

Merge semantically equivalent existing rules instead of appending a duplicate protocol.

### `PROJECT_STATE.md`

Use this compact present-tense structure:

```md
# Project State

Last Updated: YYYY-MM-DD

## Project
## Current Status
## Current Work
## Implemented
## Known Issues
## Non-goals
## Next
## New Session Handoff
```

The handoff is a navigation capsule: link to current work, constraints, Next and relevant L1 owners instead of restating volatile content. Use a short link list when enough; extra subheadings are optional.

Keep only constraints that affect decisions; no count quota. Keep detailed sprint narrative out of current authority.

Keep `New Session Handoff` compact and verify anchors after renaming/removing sections. Generated project protocols must work without this skill installed: include the short seven-question check above or link to an existing project-local definition, never a skill-relative path.

### `ARCHITECTURE.md`

Describe only deployed or currently implemented architecture. Include a compact map from important directories or modules to responsibilities. Split out a separate codebase map only when repository scale makes the combined file hard to use.

### `DECISIONS.md`

Create this file only when at least one decision has durable rationale worth preserving. For each real ADR use:

```md
## ADR-NNN — Title

Status: Accepted | Superseded
Date: YYYY-MM-DD

### Context
### Decision
### Reason
### Consequence
```

### `RUNBOOK.md`

Use commands verified against scripts, task runners, CI configuration, or a successful local run. Mark any unexecuted command as unverified rather than implying it was tested.

## Historical artifacts

Classify sprint reviews, phase reviews, bug-fix reviews, old prompts, migration plans, and replaced proposals as history when they no longer define current behavior. Place them under a suitable path such as:

```text
docs/history/
  sprints/
  reviews/
  bugfixes/
  superseded/
```

Add a visible header:

```md
> Historical artifact.
> Not authoritative for current project behavior.
```

When replaced, also add:

```md
Status: SUPERSEDED
Superseded by: [current owner or replacement](relative/path.md)
```

Keep root focused on the README and active authority files. Preserve historical artifacts and their useful context rather than deleting them.
