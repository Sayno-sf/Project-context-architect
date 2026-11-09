"""Acceptance checks for a REFACTOR copy of fixtures/messy, never a generic repo.

Checks preservation against the original fixture, links and document shape.
Does not certify semantics, user intent, platform loading or runtime state.
History filenames stay stable in this rehearsal; prepend labels and repair
links while retaining substantive content. This script never edits files.
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from document_checks import check_links, headings, prose

FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "messy"
CONVENTION_CANDIDATES = ("AGENTS.md", "CLAUDE.md", "COPILOT.md", "GEMINI.md")
HISTORY = ("sprint-review-2026-Q1.md", "TODO-old.md", "architecture-notes.md",
           "docs/old-prompts/prompt-2026-05.md")
STATE_SECTIONS = ("Project", "Current Status", "Current Work", "Implemented",
                  "Known Issues", "Non-goals", "Next", "New Session Handoff")
PROTOCOLS = ("New Session Protocol", "Authority Maintenance Protocol")


def history_body(text: str) -> str:
    # A move may change relative link destinations, but not original text.
    return re.sub(r"(\]\()[^)]+\)", r"\1<target>)", text).strip()


def verify(root: Path, baseline: Path = FIXTURE, convention: str | None = None) -> list[str]:
    if not root.is_dir():
        return [f"not a directory: {root}"]
    failures = []
    names = list(CONVENTION_CANDIDATES)
    if convention:
        if Path(convention).name != convention or not convention.endswith(".md"):
            return ["--convention must name a root Markdown file"]
        if convention not in names:
            names.append(convention)
    present = [root / name for name in names if (root / name).is_file()]
    owners = [p for p in present if any(h in headings(p.read_text(encoding="utf-8")) for h in PROTOCOLS)]
    if len(owners) != 1:
        failures.append("expected one canonical protocol owner")
    else:
        owner = owners[0]
        hs = headings(owner.read_text(encoding="utf-8"))
        for h in PROTOCOLS:
            if hs.count(h) != 1:
                failures.append(f"{owner.name}: expected exactly one {h}")
        for adapter in present:
            if adapter != owner:
                text = adapter.read_text(encoding="utf-8")
                link = re.search(r"\]\((?:\./)?" + re.escape(owner.name) + r"\)", text)
                imp = re.search(r"(?m)^@(?:\./)?" + re.escape(owner.name) + r"\s*$", text)
                if not (link or imp):
                    failures.append(f"{adapter.name}: adapter must reference {owner.name}")

    state = root / ".architect/PROJECT_STATE.md"
    if not state.is_file():
        failures.append(".architect/PROJECT_STATE.md missing")
    else:
        text = state.read_text(encoding="utf-8")
        hs = re.findall(r"(?m)^## (.+?)\s*$", prose(text))
        for section in STATE_SECTIONS:
            if hs.count(section) != 1:
                failures.append(f".architect/PROJECT_STATE.md missing section: {section} (or duplicated top-level section)")
        if not re.search(r"(?m)^Last Updated: \d{4}-\d{2}-\d{2}", text):
            failures.append(".architect/PROJECT_STATE.md missing dated Last Updated")

    for rel in HISTORY:
        original = baseline / rel
        if not original.is_file():
            failures.append(f"baseline history missing: {rel}")
            continue
        if (root / rel).exists():
            failures.append(f"history still at original location: {rel}")
        hits = list((root / ".architect" / "history").rglob(Path(rel).name))
        if len(hits) != 1:
            failures.append(f"expected one archived copy: {rel}; found {len(hits)}")
            continue
        text = hits[0].read_text(encoding="utf-8")
        if not re.search(r"(?im)^>\s*Not authoritative for current project behavior\.", text):
            failures.append(f"archive lacks explicit non-authoritative label: {rel}")
        if not history_body(text).endswith(history_body(original.read_text(encoding="utf-8"))):
            failures.append(f"archived content changed or lost: {rel}")

    for original in baseline.rglob("*"):
        if original.is_file() and original.suffix != ".md":
            rel = original.relative_to(baseline)
            target = root / rel
            if not target.is_file() or target.read_bytes() != original.read_bytes():
                failures.append(f"business file changed or missing: {rel}")

    if not (root / "README.md").is_file():
        failures.append("README.md missing")
    docs = list(root.rglob("*.md"))
    for doc in docs:
        if not doc.read_text(encoding="utf-8").strip():
            failures.append(f"empty document: {doc.relative_to(root)}")
    failures.extend(check_links(docs))
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dir", type=Path, help="refactored copy of fixtures/messy")
    parser.add_argument("--convention", help="custom root protocol filename")
    args = parser.parse_args()
    failures = verify(args.dir.resolve(), convention=args.convention)
    for failure in failures:
        print(f"FAIL: {failure}")
    if failures:
        return 1
    print("verify_refactor: STRUCTURE AND PRESERVATION PASS")
    print("Semantics, seven-question answers and platform loading still need review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
