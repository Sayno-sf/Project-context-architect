"""Read-only, scoped context checks for real projects (Python 3.10+, stdlib).

No network, writes, source execution or recursive repository inventory. Exit 0
means mechanical checks passed, not that prose is true. Review warnings and the
document-only handoff questions separately. See references/project-checks.md.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

from document_checks import anchors, prose

STATE_SECTIONS = ["Project", "Current Status", "Current Work", "Implemented",
                  "Known Issues", "Non-goals", "Next", "New Session Handoff"]
PROTOCOL_SECTIONS = ["New Session Protocol", "Authority Maintenance Protocol"]
LIMITS = {"state_chars": 12000, "l0_chars": 16000,
          "growth_chars": 2000, "growth_ratio": 0.3}
MAX_BYTES = 2_000_000
LINK = re.compile(r'\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)')
PENDING = re.compile(r"\b(?:pending|in progress|not (?:yet )?(?:complete[d]?|implemented|deployed))\b|未完成|尚未|待完成|待迁移|正在进行", re.I)
DONE = re.compile(r"\b(?:completed|implemented|deployed)\b|已完成|已迁移|已发布", re.I)


def inside(root: Path, name: str) -> Path:
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"path outside project scope: {name}")
    return path


def read_document(path: Path) -> str:
    if path.stat().st_size > MAX_BYTES:
        raise ValueError(f"document exceeds {MAX_BYTES} byte inspection limit: {path.name}")
    return path.read_text(encoding="utf-8-sig")


def configuration(root: Path, config: str | None) -> dict:
    raw = {}
    if config:
        raw = json.loads(read_document(inside(root, config)))
    if not isinstance(raw, dict) or set(raw) - {"protocol", "state", "documents", "limits"}:
        raise ValueError("config supports only protocol, state, documents and limits")
    protocol = raw.get("protocol", "AGENTS.md")
    state = raw.get("state", ".architect/PROJECT_STATE.md")
    if not all(isinstance(x, str) and x.endswith(".md") for x in (protocol, state)) or protocol == state:
        raise ValueError("protocol and state must be distinct Markdown paths")
    docs = raw.get("documents")
    if docs is None:
        docs = {protocol: PROTOCOL_SECTIONS, state: STATE_SECTIONS}
        for name in ("ARCHITECTURE.md", "RUNBOOK.md", "DECISIONS.md",
                     "CONTEXT.md", "DOMAIN.md", "PRODUCT_RULES.md", "LEARNING_RULES.md",
                     "CURRENT_SPRINT.md"):
            path = f".architect/{name}"
            if (root / path).exists():
                docs[path] = []
    if not isinstance(docs, dict) or not {protocol, state} <= docs.keys():
        raise ValueError("documents must map paths to required H2 headings and include protocol/state")
    for name, sections in docs.items():
        if not isinstance(name, str) or not name.endswith(".md"):
            raise ValueError("document paths must end in .md")
        inside(root, name)
        if not isinstance(sections, list) or not all(isinstance(s, str) and s.strip() for s in sections):
            raise ValueError(f"required headings must be a string list: {name}")
        if len(sections) != len(set(sections)):
            raise ValueError(f"duplicate configured headings: {name}")
    extra = raw.get("limits", {})
    if not isinstance(extra, dict) or set(extra) - LIMITS.keys():
        raise ValueError("unknown limits setting")
    limits = LIMITS | extra
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or v <= 0 for v in limits.values()):
        raise ValueError("limits must be positive numbers")
    return {"protocol": protocol, "state": state, "documents": docs, "limits": limits}


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=10)


def inspect(root: Path, config: str | None = None, baseline_ref: str | None = None) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError("project root is not a directory")
    cfg = configuration(root, config)
    findings = []
    texts = {}
    metrics = {}

    def add(level, code, path, message, line=None):
        findings.append(dict(level=level, code=code, path=path, line=line, message=message))

    for name, required in cfg["documents"].items():
        path = inside(root, name)
        try:
            text = read_document(path)
        except (OSError, UnicodeError, ValueError) as exc:
            add("error", "document-unreadable", name, str(exc))
            continue
        texts[name] = text
        metrics[name] = {"chars": len(text), "lines": len(text.splitlines())}
        body = prose(text)
        sections = list(re.finditer(r"(?m)^## (.+?)\s*$", body))
        for heading in required:
            matches = [m for m in sections if m[1] == heading]
            if len(matches) != 1:
                add("error", "required-section", name, f"Expected one H2 section: {heading}; found {len(matches)}")
            else:
                m = matches[0]
                following = next((s.start() for s in sections if s.start() > m.start()), len(body))
                content = re.sub(r"(?m)^#{1,6} .*?$", "", body[m.end():following]).strip()
                if not content:
                    add("error", "empty-section", name, f"Required section has no prose: {heading}")
        if not body.strip():
            add("error", "empty-document", name, "Document is empty")

        # Check destinations without following links into neighboring repos.
        visible = re.sub(r"(`+).*?\1", "", body)
        for match in LINK.finditer(visible):
            target = match[1].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            dest = path.parent / unquote(parsed.path) if parsed.path else path
            if not dest.resolve().is_relative_to(root):
                add("warning", "external-link-unchecked", name, f"Outside project; not read: {target}")
                continue
            if not dest.exists():
                add("error", "broken-link", name, f"Missing target: {target}")
            elif parsed.fragment and dest.suffix.lower() == ".md":
                try:
                    target_text = read_document(dest)
                    if unquote(parsed.fragment) not in anchors(target_text):
                        if re.search(r"\{#[^}]+\}|(?m:^.+\n[=-]{3,}\s*$)", prose(target_text)):
                            add("warning", "anchor-unverified", name, f"Target uses unsupported heading syntax; validate manually: {target}")
                        else:
                            add("error", "broken-anchor", name, f"Missing section anchor: {target}")
                except (OSError, UnicodeError, ValueError) as exc:
                    add("error", "anchor-unreadable", name, str(exc))
        if re.search(r"\]\[[^\]]*\]|(?m:^\s*\[[^\]]+\]:)", visible, re.I):
            add("warning", "markdown-review", name, "Reference links need manual validation")
        for match in re.finditer(r"(?m)^@([^\s]+\.md)\s*$", body):
            target = path.parent / match[1]
            if not target.resolve().is_relative_to(root):
                add("warning", "external-import-unchecked", name, f"Outside project; not read: {match[1]}")
            elif not target.is_file():
                add("error", "broken-import", name, f"Missing protocol import: {match[1]}")

    limits = cfg["limits"]
    state = cfg["state"]
    state_text = texts.get(state, "")
    l0_chars = sum(len(texts.get(n, "")) for n in (cfg["protocol"], state))
    if len(state_text) > limits["state_chars"]:
        add("warning", "state-size", state, f"{len(state_text)} chars exceeds review threshold {limits['state_chars']}; inspect diary/detail growth")
    if l0_chars > limits["l0_chars"]:
        add("warning", "l0-size", state, f"L0 contains {l0_chars} chars; review threshold {limits['l0_chars']}")
    dated = re.findall(r"(?m)^\s*(?:[-*] )?\d{4}-\d{2}-\d{2}[^\n]*", prose(state_text))
    if len(dated) >= 5:
        add("warning", "delivery-diary", state, f"{len(dated)} date-led entries; review whether history is accumulating in current state")

    paragraphs = defaultdict(list)
    statuses = defaultdict(lambda: {"pending": [], "done": []})
    for name, text in texts.items():
        body = prose(text)
        for para in re.split(r"\n\s*\n", body):
            normalized = re.sub(r"\s+", " ", para).strip()
            if len(normalized) >= 100:
                paragraphs[normalized].append(name)
        for line_no, line in enumerate(body.splitlines(), 1):
            # Candidate only: an identifier may refer to different environments.
            pending = bool(PENDING.search(line))
            done = bool(DONE.search(PENDING.sub("", line)))
            for subject in set(re.findall(r"`([A-Za-z][A-Za-z0-9_.:-]{2,99})`", line)):
                if pending:
                    statuses[subject]["pending"].append((name, line_no))
                if done:
                    statuses[subject]["done"].append((name, line_no))
    for locations in paragraphs.values():
        if len(locations) > 1:
            add("warning", "repeated-paragraph", locations[0], f"Repeated substantial prose in: {', '.join(locations)}")
    for subject, states in statuses.items():
        if states["pending"] and states["done"]:
            positions = states["pending"] + states["done"]
            if len(set(positions)) > 1:
                add("warning", "status-review", positions[0][0], f"Identifier {subject} occurs with pending and completed language at {positions}; compare subject/environment/evidence, not dates alone", positions[0][1])

    baseline = None
    if baseline_ref:
        if baseline_ref.startswith("-"):
            raise ValueError("baseline ref cannot start with '-'")
        result = git(root, "rev-parse", "--verify", "--end-of-options", baseline_ref + "^{commit}")
        if result.returncode:
            raise ValueError("baseline ref does not resolve to a commit in this repository")
        baseline = result.stdout.decode().strip()
        prefix = git(root, "rev-parse", "--show-prefix").stdout.decode().strip()
        for name, text in texts.items():
            old = git(root, "show", f"{baseline}:{prefix}{Path(name).as_posix()}")
            if old.returncode:
                add("warning", "baseline-file-unavailable", name, "No readable file at baseline; growth not compared")
                continue
            if len(old.stdout) > MAX_BYTES:
                add("warning", "baseline-file-unavailable", name, "Baseline exceeds inspection limit; growth not compared")
                continue
            old_text = old.stdout.decode("utf-8-sig")
            before = len(old_text.replace("\r\n", "\n"))
            growth = len(text) - before
            metrics[name].update(baseline_chars=before, growth_chars=growth)
            if growth > limits["growth_chars"] and growth / max(before, 1) > limits["growth_ratio"]:
                add("warning", "document-growth", name, f"Grew by {growth} chars from {before}; review append-only updates and obsolete claims")

    errors = sum(f["level"] == "error" for f in findings)
    warnings = sum(f["level"] == "warning" for f in findings)
    return {"mechanical_status": "FAIL" if errors else "PASS", "semantic_status": "NOT_VERIFIED",
            "root": str(root), "inspected_documents": list(texts), "baseline_commit": baseline,
            "metrics": metrics, "l0_chars": l0_chars, "errors": errors, "warnings": warnings,
            "findings": findings,
            "limitations": "No truth, deployment or platform-discovery verification. Inline links, ATX headings and explicit HTML anchors only; outside-root links are not followed. Heuristics may miss or overflag prose."}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--config", help="project-relative JSON config; not auto-discovered")
    parser.add_argument("--baseline-ref", help="existing Git commit/ref; no fetch or checkout")
    parser.add_argument("--json", action="store_true", help="print JSON to stdout; never write a report")
    parser.add_argument("--strict-warnings", action="store_true", help="also exit 1 for review warnings")
    args = parser.parse_args(argv)
    try:
        report = inspect(args.root, args.config, args.baseline_ref)
    except (ValueError, OSError, UnicodeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"error": str(exc), "semantic_status": "NOT_VERIFIED"}, ensure_ascii=True))
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=True, indent=2))
    else:
        print(f"Mechanical checks: {report['mechanical_status']}; errors={report['errors']}; warnings={report['warnings']}")
        print("Semantic truth and runtime state: NOT_VERIFIED")
        for item in report["findings"]:
            print(f"{item['level'].upper()} {item['code']} {item['path']}: {item['message']}")
        print(report["limitations"])
    return int(bool(report["errors"] or (args.strict_warnings and report["warnings"])))


if __name__ == "__main__":
    sys.exit(main())
