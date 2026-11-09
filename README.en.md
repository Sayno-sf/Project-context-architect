# Project Context Architect

**Help AI coding assistants pick up a project in a new session.**

Keep project goals, current work, architecture entry points and operating instructions up to date. Retire stale status claims; review only affected content during routine updates.

[中文](README.md) | **English**

[![CI](https://github.com/Sayno-sf/Project-context-architect/actions/workflows/ci.yml/badge.svg)](https://github.com/Sayno-sf/Project-context-architect/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## When to use it

This is a skill for AI coding assistants that support local skills. Use it when:

- **New sessions lose the thread:** you keep explaining what the project does, where it stands and what comes next.
- **Documents disagree:** a feature is complete, but an old TODO, issue list or handoff summary still says it is pending.
- **Project notes keep accumulating:** current rules, past proposals and working notes are mixed together, with no clear source to trust.

The skill gives current facts a small set of clearly owned project files. Other summaries link to those owners. When a fact changes, it updates the original statement and affected summaries instead of appending another status log.

## Install

Choose your platform. Install the **complete repository directory**, preserving its contents. For a direct skill installation, name the directory `project-context-architect`.

### Codex

In Codex with local skill support, send:

```text
Use skill-installer to install project-context-architect from the root of:
https://github.com/Sayno-sf/Project-context-architect
Keep the complete directory. If already installed, back up the old copy before
updating it, and tell me the actual installation path.
```

### Claude Code

Run in your terminal:

```bash
claude plugin marketplace add Sayno-sf/Project-context-architect
claude plugin install project-context-architect@project-context-architect-marketplace
```

### Other assistants with local skill support

Download and extract a source archive from [Releases](https://github.com/Sayno-sf/Project-context-architect/releases). Name the complete directory `project-context-architect` and put it in your assistant's supported skills directory. Loading behavior depends on the platform.

Confirm that your assistant can discover the skill, then open the target project. See [PLUGIN.md](PLUGIN.md) for installation and validation details.

## First use

Copy one of these prompts into a session for your project. Describe the task in ordinary language; you do not need to memorize mode names.

### 1. Check without changing files

```text
Use project-context-architect to review this project's handoff documents, read-only.
Identify stale status, duplicated facts and missing entry points. Give file
locations and the smallest suggested repairs.
```

You get a report stating what was inspected. The check itself does not edit files or archive material.

### 2. Establish or organize project documents

```text
Use project-context-architect to establish or organize this project's handoff docs.
You may edit relevant documents. Preserve existing project rules and useful
history; do not change business code. Put current status, architecture and
operating instructions in suitable owners, and mark unsupported claims as uncertain.
```

The assistant reuses suitable documents, adds only needed content, and checks whether a new session can locate current work and the next step.

### 3. Update status after completing work

```text
Use project-context-architect to update project documents from the changes
verified in this session. Check only affected sections and dependent summaries.
Replace stale facts; if no facts changed, leave the documents untouched.
```

For example, a verified fix should no longer appear as pending in the issue list or next steps. Deployment still needs its own evidence. A routine update does not require rereading every file or running a full handoff review.

## Cross-platform relay

When you explicitly ask an agent on another platform to take over, it handles integration for the current task, using existing state and available work summaries. It checks relevant changes without requiring Git, role files or a repeated full acceptance review. For actual parallel work, briefly agree distinct file scopes and one integrator; sequence edits to shared files. This is a cooperation convention, not an enforced lock.

## What it creates or maintains

Project context defaults to `.architect/`; keep platform entry files such as `AGENTS.md` and the README at the root. Common responsibilities are:

| File | Responsibility |
|---|---|
| `AGENTS.md` or an existing equivalent | Working rules and what a new session reads first |
| `.architect/PROJECT_STATE.md` | Current status, active work, known issues and next steps |
| `.architect/ARCHITECTURE.md` | Current components, entry points, data flow and boundaries |
| `.architect/RUNBOOK.md` | Environment, startup, tests and troubleshooting |
| `.architect/DECISIONS.md` | Decision rationale worth preserving |

New projects start with a working-protocol entry and current state. Other files are created only when they have substantive content. During consolidation, move relevant context into `.architect/`, repair links and preserve project rules. History is preserved and labeled under `.architect/history/`; handoff summaries favor links over another copy of current status.

Browse the [fictional project example](examples/bootstrap/) to see the document shapes. Its features and verification claims illustrate the format; they are not measured results.

## Boundaries

- **Checks are read-only by default.** Edits and archival must fall within your request. This skill manages project context, not business implementation.
- **Document checks do not certify facts.** Scripts check structure, links and some suspicious wording. Meaning, product intent and live runtime state still require appropriate evidence.
- **Installation does not take over a project.** The skill does not monitor repositories in the background, replace existing project protocols or install CI automatically. Request those changes in the relevant project when needed.

## Further use

Routine work uses incremental maintenance. For explicit scopes, use `BOOTSTRAP` to establish a context system, `REFACTOR` to consolidate it, or `CHECK` to inspect it.

- [Incremental maintenance](references/maintenance.md) · [Document and fact ownership](references/authority-model.md)
- [BOOTSTRAP](references/bootstrap.md) · [REFACTOR](references/refactor.md) · [CHECK](references/check.md)
- [Seven questions for a full handoff review](references/fresh-session-test.md)

For a script-based check, run from this skill's directory (Python 3.10+, standard library only):

```bash
python -B scripts/check_project_context.py /path/to/project
```

The defaults expect conventional filenames and headings; configure equivalents when your project differs. See [real-project checks](references/project-checks.md) for configuration, result interpretation and optional CI integration.

For regression commands used to maintain this skill, see [scripts/README.md](scripts/README.md). The `verify_refactor.py` script accepts only refactored copies of the rehearsal fixture, not arbitrary projects.

[Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [MIT License](LICENSE)
