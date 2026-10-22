"""Check local inline Markdown links and ATX anchors, without network access.

Not a full Markdown parser: reference links and renderer-specific heading IDs
need human review. Explicit HTML id/name anchors are recognized. Fenced examples
and inline code are excluded.
"""
from __future__ import annotations
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


def prose(text: str) -> str:
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m[0].count("\n"), text, flags=re.S)
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            lines.append("")
            continue
        lines.append(line if fence is None else "")
    return "\n".join(lines)


def headings(text: str) -> list[str]:
    return [m[1].strip().rstrip("#").strip()
            for m in re.finditer(r"^#{1,6}\s+(.+)$", prose(text), re.M)]


def anchors(text: str) -> set[str]:
    counts, result = {}, set()
    for title in headings(text):
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        n = counts.get(slug, 0)
        counts[slug] = n + 1
        result.add(slug if n == 0 else f"{slug}-{n}")
    class ExplicitAnchors(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for key, value in attrs:
                if value and (key == "id" or (tag == "a" and key == "name")):
                    result.add(value)
    ExplicitAnchors().feed(prose(text))
    return result


def check_links(files: list[Path]) -> list[str]:
    failures = []
    for md in files:
        if not md.is_file():
            failures.append(f"missing document: {md}")
            continue
        text = prose(md.read_text(encoding="utf-8"))
        text = re.sub(r"(`+).*?\1", "", text)
        for match in re.finditer(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text):
            target = match[1].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            path = md.parent / unquote(parsed.path) if parsed.path else md
            if not path.exists():
                failures.append(f"{md}: broken link: {target}")
            elif parsed.fragment and path.suffix.lower() == ".md":
                if unquote(parsed.fragment) not in anchors(path.read_text(encoding="utf-8")):
                    failures.append(f"{md}: broken anchor: {target}")
    return failures
