"""Structural self-check for the project-context-architect skill.

Checks (deterministic only):
  1. required files exist
  2. local Markdown links and section anchors resolve, including examples
  3. every .md/.py/.yaml/.json file is strict UTF-8 without BOM
  4. frontmatter and distribution metadata have the supported structure

Exit code 0 = all pass, 1 = any failure. Pure stdlib, no dependencies.
"""

from __future__ import annotations

import re
import json
from document_checks import check_links as document_links
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "SKILL.md",
    "references/authority-model.md",
    "references/bootstrap.md",
    "references/check.md",
    "references/project-checks.md",
    "references/maintenance.md",
    "scripts/check_project_context.py",
    "scripts/test_project_context.py",
    "examples/integration/context-check.json",
    "examples/integration/context-check.yml",
    "references/refactor.md",
    "references/fresh-session-test.md",
    "examples/README.md",
    "examples/bootstrap/AGENTS.md",
    "examples/bootstrap/.architect/PROJECT_STATE.md",
    "examples/bootstrap/.architect/DECISIONS.md",
    "examples/bootstrap/.architect/RUNBOOK.md",
    "fixtures/README.md",
    "fixtures/messy/README.md",
    "fixtures/messy/AGENTS.md",
    "fixtures/messy/PROJECT_STATE.md",
    "fixtures/messy/summarize.py",
    "fixtures/messy/app.py",
    "fixtures/messy/requirements.txt",
    "fixtures/messy/tests/test_summarize.py",
    "agents/openai.yaml",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "scripts/document_checks.py",
    "scripts/test_validation.py",
    "examples/bootstrap/.architect/ARCHITECTURE.md",
    "PLUGIN.md",
    "scripts/README.md",
    # 发布配套
    "README.md",
    "README.en.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    ".gitignore",
    ".github/workflows/ci.yml",
]


def check_required() -> list[str]:
    return [f"missing required file: {p}" for p in REQUIRED_FILES if not (ROOT / p).exists()]


def check_links() -> list[str]:
    files = [p for p in ROOT.rglob("*.md")
             if "fixtures/messy/" not in p.relative_to(ROOT).as_posix() and ".git" not in p.parts]
    return document_links(files)


def check_encoding() -> list[str]:
    problems = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".md", ".py", ".yaml", ".yml", ".json", ".txt"}:
            continue
        raw = p.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            problems.append(f"{p.relative_to(ROOT)}: BOM present (expected no BOM)")
            continue
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError as e:
            problems.append(f"{p.relative_to(ROOT)}: not UTF-8 ({e})")
    return problems


def check_metadata() -> list[str]:
    problems = []
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    fm = re.match(r"\A---\n(.*?)\n---", skill, re.S)
    if not fm or not re.search(r"(?m)^name: project-context-architect$", fm[1]) or not re.search(r"(?m)^description: \S", fm[1]):
        problems.append("SKILL.md: missing or invalid name/description frontmatter")
    try:
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return problems + [f"distribution JSON: {exc}"]
    if not isinstance(market, dict) or not isinstance(plugin, dict):
        return problems + ["distribution manifests must be JSON objects"]
    if not market.get("name") or not isinstance(market.get("owner"), dict) or not market["owner"].get("name"):
        problems.append("marketplace requires name and owner.name")
    entries = market.get("plugins", [])
    if not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict) or entries[0].get("name") != plugin.get("name") or entries[0].get("source") != "./":
        problems.append("marketplace must reference this root plugin by matching name and ./ source")
    if plugin.get("name") != "project-context-architect" or plugin.get("skills") != ["./"]:
        problems.append("plugin must declare the root skill via skills: [./]")
    version = plugin.get("version", "")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        problems.append("plugin requires a semantic version")
    elif f"## [{version}]" not in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"):
        problems.append("plugin version missing from CHANGELOG.md")
    if (ROOT / "marketplace.json").exists():
        problems.append("obsolete duplicate root marketplace.json")
    return problems


def main() -> int:
    failures = check_required()
    if not failures:
        failures = check_links() + check_encoding() + check_metadata()
    if failures:
        for f in failures:
            print(f"FAIL: {f}")
        print(f"\n{len(failures)} problem(s) found.")
        return 1
    print("lint_skill: ALL CHECKS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
