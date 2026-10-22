# Fresh-Session Test

Run the full checklist after BOOTSTRAP or broad REFACTOR, and for requested handoff/milestone readiness. Routine updates and narrow CHECKs recheck only affected answers; they do not establish full readiness.

## How to run

Perform a document-only walkthrough, not an independent fresh-session experiment. Support answers only from L0 (the project convention file and current state) and its named L1 links. Prior source knowledge, chat and memory cannot fill a missing answer. Record file/section or line evidence and check relevant links and anchors; reuse still-current excerpts instead of rereading unchanged files.

For release validation of this skill, use a separate context with only the skill, task and permitted repository files when independent execution is available and authorized. Do not supply expected answers or suspected defects. Otherwise label the result a self-check; do not claim independent handoff validation.

## Questions

For full readiness, ask all seven. A missing or contradictory answer fails that gate. A clearly documented absence is valid for a category that does not yet exist; it is not valid for an existing but undocumented capability.

1. **Identity** — What is this project, in one sentence, and who is it for?
2. **Status** — What is the current status, and what work is in progress right now?
3. **Entry point** — Without opening source, where does execution start? What is the main entry point and start command? A new/non-runnable project may explicitly say none exists yet; do not invent one.
4. **Architecture** — How is the current system composed (components, boundaries, main data flow, state ownership)? A project with no implementation may explicitly say so and separate plans from current facts.
5. **Constraints** — What hard constraints, permissions, or non-goals must a fresh session not violate?
6. **Next** — What is the next step, and what is the stop condition for current work?
7. **Task context** — Where are architecture and operations owned? Follow existing links to their owners, which may be sections rather than dedicated files. If a category has no substance yet, state that explicitly; do not create empty documents to pass.

## Pass / fail

Run available mechanical checks using [project-checks.md](project-checks.md), but keep their result separate from these semantic answers. A script PASS cannot fill an unsupported answer or establish live deployment.

- **Pass** — all seven questions answered from L0 (plus named L1) alone, with no contradiction between files.
- **Fail** — any question requires reading source code, chat history, `docs/history/`, or a document not listed in the read map; or two authority files give conflicting answers.

## Repair discipline

In read-only work, report the failed question and smallest repair without editing. When repairs are requested, fix only the exposed defect and recheck affected answers and links. State inspected scope and unverified environments; document consistency does not prove a running service.
