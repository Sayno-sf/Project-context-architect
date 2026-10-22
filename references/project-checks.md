# Real-project checks

Read this when running the mechanical checker or integrating checks into a project. Routine fact updates use [maintenance.md](maintenance.md); configuration and integration below are optional, not prerequisites for writing authority. The checker is read-only. Do not install hooks or alter CI during read-only CHECK.

## Run without installing into the project

From this skill's directory:

```bash
python -B scripts/check_project_context.py /path/to/project
python -B scripts/check_project_context.py /path/to/project --json
python -B scripts/check_project_context.py /path/to/project --baseline-ref HEAD
```

The checker reads only the configured authority documents and local Markdown link targets needed for anchor validation. It does not scan source, history or data trees recursively, access the network, run project commands, fetch Git refs, or write files. Outside-root links/imports are reported as unchecked and are not followed. Local symlinks cannot extend scope outside the project.

Its configured scan is separate from the agent's reading scope: consume the compact result and inspect relevant findings, not every scanned document. Run once after a batch when useful or required, not after each write. Existing unrelated findings do not authorize cleanup; report them separately from the result of a bounded update. A failing configured scan still cannot be reported as PASS.

Defaults require `AGENTS.md` and `PROJECT_STATE.md` with this skill's English H2 section names. Existing root architecture, runbook, decisions and domain/rule documents are checked when present. A repository with different filenames/headings should configure its equivalents, not rename sound documents just to pass.

## Configuration

Configuration is opt-in via `--config`; there is no hidden auto-discovery. Paths are relative to the project root and must remain within it. Copy and adapt the [sample config](../examples/integration/context-check.json) only when integration is requested. For example, a Chinese project can use:

```json
{
  "protocol": "CLAUDE.md",
  "state": "docs/项目状态.md",
  "documents": {
    "CLAUDE.md": ["协作协议", "维护协议"],
    "docs/项目状态.md": ["项目", "当前工作", "已实现", "已知问题", "下一步", "交接"]
  },
  "limits": {"state_chars": 12000, "l0_chars": 16000, "growth_chars": 2000, "growth_ratio": 0.3}
}
```

`documents` maps each required document to required, nonempty H2 headings; an empty list still checks existence, content and links. Include the protocol and state paths. Do not remove meaningful checks just to make an existing defect pass. Limits are review thresholds, not universal document-size targets. Growth warns only when both absolute and proportional thresholds are exceeded. `--baseline-ref` must resolve locally; omitted means no growth comparison. Use the PR base commit in CI; HEAD on a checked-out PR would compare the file to itself.

## Interpret the result

- **Errors:** missing/unreadable documents, missing/duplicate/empty required sections, missing local targets, broken ATX/explicit HTML anchors and missing local `@file.md` imports.
- **Review warnings:** large L0/state text, substantial growth, repeated paragraphs, multiple date-led state entries, a shared backticked identifier with pending/completed language, or unsupported/outside-root links. Heuristics may miss synonyms or flag legitimate environment differences. They never authorize automated rewriting.
- **Unverified:** factual truth, semantic consistency, intended product behavior, live deployment and whether the agent platform actually loads a convention file. The result always includes `semantic_status: NOT_VERIFIED`.

Exit code `0` means no mechanical errors, `1` means errors, and `2` means an invocation/configuration/baseline failure. Warnings do not block by default; `--strict-warnings` makes them exit `1` as well. JSON is printed to stdout without creating a report file. The Markdown subset is inline links, ATX headings and explicit HTML id/name anchors; reference-style links, custom renderer anchors and unusual syntax require manual verification.

## Project-local integration

When authorized, copy both `scripts/check_project_context.py` and `scripts/document_checks.py` together to a project-owned tools directory (for example `tools/context/`), preserving their filenames. Record the skill version in the project's existing tool provenance or runbook. Adapt the sample config to the project's existing owners and headings. Runtime checks then need neither this skill nor its installation path.

Put the exact command in the project's runbook, and reference it from its completion protocol:

```bash
python -B tools/context/check_project_context.py . --config context-check.json
```

Use this as a pre-commit **manual command** unless installing a hook is specifically requested. Do not overwrite an existing hook or change `core.hooksPath` merely to enable context checks. The command inspects the working tree, not the Git index; CI validates the committed snapshot.

Merge the [CI example](../examples/integration/context-check.yml) into the existing workflow when CI integration is requested. It checks the PR base for growth and intentionally starts without strict warnings. It assumes the two scripts have been copied to `tools/context/` and the config adapted. CI running is not equivalent to merge enforcement; required-check settings must be configured separately under the user's authorized repository policy.

Before recording integration as active, run the exact project command, verify the workflow parses, and confirm a CI run after publication. Mark unavailable CI/platform verification explicitly. Do not add this integration to adjacent projects outside the request.

## Handoff acceptance

For full handoff acceptance, answer all seven questions in [fresh-session-test.md](fresh-session-test.md) from the scoped documents with citations. Review warnings against their subject, environment and evidence; do not declare GOOD while material conflicts remain. A routine update checks only affected answers and does not claim full acceptance.

For independent acceptance, give a separate authorized session only the project snapshot, the task and the skill, without the author's expected answers. Ask it to locate current work, constraints, entry points and stop conditions and to report contradictions without editing. Record observed answers and source locations. If independent execution was not performed, report document-only self-check instead. Do not infer agent behavior from unit-test success.
