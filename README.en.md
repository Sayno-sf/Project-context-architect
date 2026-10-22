# Project Context Architect

> Maintain a project's **smallest authoritative context**: a small, explicit, current set of repository files that lets any fresh session understand the project without inheriting chat history or reading the entire repository.

[中文](README.md) | **English**

## What this is

The most common problem AI agents hit in long-lived projects is **fragmented context**: facts scattered across chat history, outdated design docs, overturned decisions, and old notes that still look alive. This project proposes a governance layer — **minimum authority**:

- A small set of repository files with explicit responsibilities, owning the current truth.
- **One fact, one owner**: every current fact belongs to exactly one authority document; everything else links to it.
- **Current truth and history separated**: history is archived and labeled "non-authoritative" and never participates in handoff judgments.
- **Category-aware conflict verification**: conflicts are verified with category-appropriate evidence, not inferred from implementation.
- **Authority completion gate**: a task is not complete while affected authority remains stale.

It manages **project context**, not business implementation.

## Three modes

| Mode | When to use | Output |
|---|---|---|
| **BOOTSTRAP** | A new or early project lacks a handoff system | Minimal authority set (`AGENTS.md` + `PROJECT_STATE.md`, plus `ARCHITECTURE.md` / `DECISIONS.md` / `RUNBOOK.md` when justified) |
| **REFACTOR** | An established project's context is scattered, duplicated, stale, or contradictory | Single authority ownership + archived history + a converged handoff |
| **CHECK** | Inspect named facts/documents or handoff readiness | Read-only result; a narrow check does not establish full readiness |

Mode selection: choose the least expansive mode that fits. A CHECK may recommend REFACTOR; it never silently expands into one.

Small updates use [incremental maintenance](references/maintenance.md) directly: read the affected section, verify evidence, find dependent summaries, replace stale facts, then review the batch diff and links. Reuse current session context; no full-file reread for each write, and no write-back when facts are unchanged.

The full seven-question test is for BOOTSTRAP, broad REFACTOR or requested handoff/milestone acceptance. Contradictions, unclear ownership or uncertain impact trigger wider relevant reading first. CHECK stays read-only unless repairs are requested. Full readiness is `NOT_ASSESSED` after a narrow check, `NEEDS_ATTENTION` when defects remain, and `GOOD` only after full handoff verification in the declared scope. Source, build, loaded service and acceptance remain separate claims.

## Quick start

### Install (recommended)

**Installation semantics**: the whole `project-context-architect/` directory is one complete skill unit — `SKILL.md` is the entry point; `references/`, `examples/`, `fixtures/`, and `scripts/` are its resource subdirectories. To install, copy the **entire directory** into your agent's skills root (keeping the directory name `project-context-architect`) — do not flatten its internal files. Directory contents:

| Layer | Contents | Required at runtime |
|---|---|---|
| Runtime core | `SKILL.md`, `references/`, `examples/`, `agents/openai.yaml` | Core and Codex metadata |
| Rehearsal & regression | `fixtures/`, `scripts/` (pure stdlib, no dependencies) | Optional |
| Release layer | README.md, LICENSE, CHANGELOG.md, CONTRIBUTING.md, .github/, .gitignore, PLUGIN.md, .claude-plugin/ | Not required at runtime; may be skipped |

Then use it in your projects:

- New project: ask your agent to run **BOOTSTRAP**
- Messy existing project: **REFACTOR**
- Before handoff: **CHECK**

#### One-shot install prompt (copy and send to any agent)

Copy the whole block below to your agent (Claude Code, Codex, or any skills-capable assistant):

```text
Please install the project-context-architect skill (project minimum-authority context governance).

1. Get the source (choose one):
   - Repository: git clone https://github.com/lhq418899-sketch/Project-context-architect.git
   - Local: use this directory on my machine: <fill in the source directory path>
2. Install: copy the entire directory (SKILL.md plus the references/, examples/, fixtures/, scripts/ subdirectories) as one complete skill unit into your skills root, keeping the directory name project-context-architect. Do not flatten internal files or scatter them elsewhere.
3. If your platform supports plugin marketplaces (e.g. Claude Code), you may instead use:
   claude plugin marketplace add lhq418899-sketch/Project-context-architect
   claude plugin install project-context-architect@project-context-architect-marketplace
4. If you use OpenAI Codex with local skill support, install via the official skill-installer or copy to your skills dir:
   Ask the built-in skill-installer to install from https://github.com/lhq418899-sketch/Project-context-architect
   (or copy the whole directory to ~/.codex/skills/)
5. Verify: SKILL.md exists with complete frontmatter; if Python 3 is available, run python scripts/lint_skill.py and python scripts/check_fixture.py — both should pass.
6. Tell me where it was installed and the verification result.
```

Other distribution channels (official directory / self-hosted marketplace / plugin install): see [PLUGIN.md](PLUGIN.md).

### Concepts and execution details

- Authority model, file naming, and one-fact-one-owner: [references/authority-model.md](references/authority-model.md)
- Mode execution details: [references/bootstrap.md](references/bootstrap.md), [references/refactor.md](references/refactor.md), [references/check.md](references/check.md)
- Fresh-session readiness test (7 questions): [references/fresh-session-test.md](references/fresh-session-test.md)
- Golden examples (fictional project): [examples/bootstrap/](examples/bootstrap/)
- Deliberately broken rehearsal project: [fixtures/messy/](fixtures/messy/)

## Repository layout

```
project-context-architect/
├── SKILL.md                    # main skill (three-mode entry + shared operating contract)
├── references/                 # authority model / mode details / fresh-session test
├── examples/bootstrap/         # golden examples (fictional project, do not copy)
├── fixtures/messy/             # deliberately broken rehearsal project (regression fixture)
├── scripts/                    # deterministic validation scripts (pure stdlib)
├── agents/openai.yaml          # Codex-side interface config
├── .claude-plugin/plugin.json  # Claude plugin metadata
├── .claude-plugin/marketplace.json # marketplace manifest
└── PLUGIN.md                   # plugin distribution guide
```

## Check real projects

```bash
python -B scripts/check_project_context.py /path/to/project
python -B scripts/check_project_context.py /path/to/project --baseline-ref HEAD --json
```

Mechanical errors fail the check; growth, repetition and candidate status contradictions require review. The script does not certify semantic truth or deployment. Custom paths/headings are configurable. With authorization, copy the two standalone scripts into a project and integrate its existing CI without depending on a local skill installation.

See [configuration, integration and acceptance](references/project-checks.md). Existing projects do not automatically receive new protocols or CI gates.

## Regression tests

Run after every change (no dependencies required):

```bash
python scripts/lint_skill.py        # structure: files, links/anchors, encoding, package metadata
python scripts/check_fixture.py     # confirm the rehearsal fixture is still deliberately broken
python -B -m unittest discover -s scripts -p "test_*.py"
python scripts/verify_refactor.py <dir>  # structural acceptance of a REFACTOR result
```

See [scripts/README.md](scripts/README.md). The repository includes CI configuration for lint, fixture checks and regression tests on push / PR; remote success requires an observed run (see [.github/workflows/ci.yml](.github/workflows/ci.yml)).

## Language policy

The project's documents are **bilingual, Chinese-first**: the core execution files (`SKILL.md`, `references/`, `examples/`) stay in English to keep agent triggering and execution consistent across platforms, while human-facing distribution and contribution docs are Chinese-first. This English README is a translation for international readers. Contributions of further translations are welcome.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © 2026 lhq418899-sketch
