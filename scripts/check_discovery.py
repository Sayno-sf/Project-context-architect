"""Read-only release discovery checks; Python 3.10+, standard library only.

Default: offline package metadata and install instructions. --online additionally
checks public GitHub metadata and skills.sh search results, never installs.
Exit 0: hard checks pass (NOT_FOUND can remain diagnostic); 1: failed check;
2: an external check was unavailable. This does not test agent activation.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
NETWORK_ERRORS = (URLError, TimeoutError, OSError, ValueError)


def record(check: str, status: str, detail: str, **extra) -> dict:
    return {"check": check, "status": status, "detail": detail, **extra}


def canonical_source(value: str) -> str:
    value = value.strip().rstrip("/")
    if value.startswith("https://github.com/"):
        value = value[len("https://github.com/"):]
    if value.endswith(".git"):
        value = value[:-4]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value):
        raise ValueError("expected a GitHub owner/repository source")
    return value.casefold()


def local_checks(root: Path) -> tuple[list[dict], dict | None]:
    try:
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        front = re.match(r"\A---\n(.*?)\n---(?:\n|$)", skill, re.S)
        if not front:
            raise ValueError("missing SKILL.md frontmatter")
        # This package uses plain single-line name and description fields.
        fields = dict(re.findall(r"(?m)^(name|description): (.+)$", front[1]))
        name, description = fields.get("name", ""), fields.get("description", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            raise ValueError("invalid skill name")
        if not 1 <= len(description) <= 1024 or description in {"|", ">"}:
            raise ValueError("expected a single-line description of 1–1024 characters")
        plugin = json.loads((root / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        homepage = plugin["homepage"]
        if not isinstance(homepage, str) or not homepage.startswith("https://github.com/"):
            raise ValueError("plugin homepage must identify the canonical GitHub repository")
        source = canonical_source(homepage)
        if plugin.get("name") != name:
            raise ValueError("plugin and skill names disagree")
        metadata = json.loads((root / ".github/repository-metadata.json").read_text(encoding="utf-8"))
        if not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
            raise ValueError("repository description is empty")
        topics = metadata.get("topics")
        if (not isinstance(topics, list) or not 1 <= len(topics) <= 20
                or any(not isinstance(t, str) or not re.fullmatch(r"[a-z0-9-]{1,50}", t) for t in topics)
                or len(set(topics)) != len(topics)):
            raise ValueError("repository topics must be 1–20 distinct lowercase topic names")
        result = [record("package", "PASS", "Skill identity, description and repository metadata are valid.")]
        for filename in ("README.md", "README.en.md"):
            text = (root / filename).read_text(encoding="utf-8")
            commands = re.findall(r"(?m)^npx skills add (\S+) --skill (\S+)\s*$", text)
            found = any(canonical_source(repo) == source and selected == name for repo, selected in commands)
            result.append(record(filename, "PASS" if found else "FAIL",
                                 "Canonical explicit install command found." if found else "Canonical install command missing."))
        return result, {"source": source, "name": name, "metadata": metadata}
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return [record("package", "FAIL", str(exc))], None


def get_json(url: str) -> object:
    request = Request(url, headers={"User-Agent": "project-context-architect-discovery-check",
                                   "Accept": "application/json"})
    with urlopen(request, timeout=12) as response:
        body = response.read(2_000_001)
    if len(body) > 2_000_000:
        raise ValueError("response exceeds 2 MB")
    return json.loads(body.decode("utf-8"))


def search_check(payload: object, source: str, name: str, label: str, query: str) -> dict:
    if not isinstance(payload, dict) or not isinstance(payload.get("skills"), list):
        raise ValueError("search response has no skills array")
    hits = payload["skills"]
    for rank, item in enumerate(hits, 1):
        if (not isinstance(item, dict) or not isinstance(item.get("source"), str)
                or not isinstance(item.get("name"), str)
                or not isinstance(item.get("id", ""), str)):
            raise ValueError("search response contains a malformed result")
        try:
            same_source = canonical_source(item["source"]) == source
        except ValueError:
            same_source = False  # A legitimate non-GitHub source can occur in broad searches.
        same_skill = item["name"] == name or item.get("id", "").casefold() == f"{source}/{name}"
        if same_source and same_skill:
            return record(label, "PASS", "Canonical skill found in returned results.", query=query,
                          rank=rank, result_count=len(hits))
    return record(label, "NOT_FOUND", "Canonical skill absent from returned results; not proof of global absence.",
                  query=query, result_count=len(hits))


def online_checks(config: dict, fetch=get_json) -> list[dict]:
    source, name, expected = config["source"], config["name"], config["metadata"]
    results = []
    url = f"https://api.github.com/repos/{source}"
    try:
        actual = fetch(url)
        if (not isinstance(actual, dict) or not isinstance(actual.get("full_name"), str)
                or not isinstance(actual.get("topics"), list)
                or any(not isinstance(topic, str) for topic in actual["topics"])):
            raise ValueError("GitHub response is missing repository metadata")
        matches = (canonical_source(actual["full_name"]) == source
                   and actual.get("description") == expected["description"]
                   and set(expected["topics"]).issubset(actual["topics"]))
        results.append(record("github-metadata", "PASS" if matches else "FAIL",
                              "Description and expected topics match." if matches else "Repository identity, description or expected topics differ.", url=url))
    except NETWORK_ERRORS as exc:
        results.append(record("github-metadata", "UNAVAILABLE", str(exc), url=url))
    searches = [("exact-owner-search", name, source.split("/")[0]),
                ("scenario-project-context", "project context", None),
                ("scenario-agent-handoff", "agent handoff", None),
                ("scenario-documentation-drift", "documentation drift", None)]
    for label, query, owner in searches:
        params = {"q": query}
        if owner:
            params["owner"] = owner
        url = "https://skills.sh/api/search?" + urlencode(params)
        try:
            result = search_check(fetch(url), source, name, label, query)
            result["url"] = url
            results.append(result)
        except NETWORK_ERRORS as exc:
            results.append(record(label, "UNAVAILABLE", str(exc), query=query, url=url))
    return results


def exit_code(checks: list[dict], require_listed: bool = False) -> int:
    if any(c["status"] == "FAIL" or (require_listed and c["check"] == "exact-owner-search"
                                     and c["status"] == "NOT_FOUND") for c in checks):
        return 1
    if any(c["status"] == "UNAVAILABLE" for c in checks):
        return 2
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--require-listed", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.require_listed and not args.online:
        parser.error("--require-listed requires --online")
    checks, config = local_checks(args.root)
    if args.online and config is not None and not exit_code(checks):
        checks.extend(online_checks(config))
    code = exit_code(checks, args.require_listed)
    report = {"online_requested": args.online, "source": config["source"] if config else None,
              "checks": checks, "exit_code": code, "agent_activation": "NOT_ASSESSED"}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for c in checks:
            print(f"{c['status']}: {c['check']}: {c['detail']}")
        print("Agent activation and ranking outside returned results: NOT_ASSESSED")
    return code


if __name__ == "__main__":
    sys.exit(main())
