# BOOTSTRAP

Use this mode for a new or early project that lacks a coherent project-memory and handoff system.

## Establish evidence

Inspect the project instructions, README, file tree, manifests, configuration, real entry points, and automation definitions. Capture the user's stated goal as intent, while using repository evidence for claims about what is implemented or runnable.

Before writing, be able to state:

- what the project is;
- what exists now versus what is planned;
- the current architectural skeleton and main entry points;
- how the repository currently starts, tests, and builds;
- the durable constraints explicitly supplied by the user or repository;
- what remains unknown.

When repository evidence cannot establish intent, ask the user the minimal question set:

1. What problem is this project solving, and for whom?
2. What is actually working today, versus planned?
3. What constraints or boundaries must never be crossed?

Ask only what the evidence cannot answer; never ask what the repository already states.

## Create the minimum authority

Read [authority-model.md](authority-model.md); consult a relevant [example](../examples/bootstrap/) only if the desired shape is unclear. Create or adapt:

1. the agent convention file (`AGENTS.md` by default; reuse a platform equivalent the project already maintains — see the naming rule in authority-model.md)
2. `.architect/PROJECT_STATE.md`

Create the following only when their authority category already has substantive content:

- `.architect/ARCHITECTURE.md` — meaningful implemented components, boundaries, ownership, data flow, or codebase map need a dedicated owner;
- `.architect/DECISIONS.md` — at least one accepted decision has durable rationale worth preserving;
- `.architect/RUNBOOK.md` — real environment, start, test, build, validation, or debugging instructions exist.

Keep initial files short. Represent a missing category through absence, not an empty document created for symmetry. `.architect/PROJECT_STATE.md` may point only to authority files that exist.

Create an optional authority document only when the evidence already demonstrates its need. Keep current work in `.architect/PROJECT_STATE.md` unless a substantial execution contract justifies `.architect/CURRENT_SPRINT.md`.

In the project-root convention file, adapt the two protocols from [authority-model.md](authority-model.md): read-on-demand orientation and incremental write-back, with the seven questions reserved for full handoff checks. Preserve existing project rules and keep root protocols out of nested copies.

## Verify handoff

For actual-project checks and requested project-local integration, follow [project-checks.md](project-checks.md). Do not claim a CI gate is active merely because a workflow was written. Preserve existing tools and conventions.

Run the fresh-session test from [fresh-session-test.md](fresh-session-test.md). Also check:

- every created authority file answers its own question without absorbing a neighbor's category;
- every conditional authority file has substantive content that justifies its existence;
- the root agent convention file preserves existing working rules and contains one copy each of the new-session and authority-maintenance protocols;
- the maintenance protocol permits no-op tasks to leave authority documents untouched and requires affected authority to be current before completion;
- `.architect/PROJECT_STATE.md` distinguishes implemented capabilities from plans;
- an existing `.architect/RUNBOOK.md` labels commands accurately as verified or unverified;
- links among authority files resolve.

BOOTSTRAP is complete only when the minimum authority is usable today and contains no invented future state.
