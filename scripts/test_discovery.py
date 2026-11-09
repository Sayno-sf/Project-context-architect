"""Discovery regression cases without network requests or installation."""
import json
import tempfile
import unittest
from pathlib import Path
from urllib.error import URLError

from check_discovery import local_checks, online_checks, search_check, exit_code

SOURCE = "example/context-kit"
NAME = "project-context-architect"
META = {"description": "Project context and handoffs", "topics": ["agent-skills"]}
CONFIG = {"source": SOURCE, "name": NAME, "metadata": META}


class DiscoveryTests(unittest.TestCase):
    def test_other_repository_with_same_name_is_not_a_match(self):
        result = search_check({"skills": [{"name": NAME, "source": "other/context-kit"}]}, SOURCE, NAME, "exact-owner-search", NAME)
        self.assertEqual(result["status"], "NOT_FOUND")
        self.assertEqual(exit_code([result]), 0)
        self.assertEqual(exit_code([result], require_listed=True), 1)

    def test_canonical_source_case_and_url_variants_match(self):
        for source in ["Example/Context-Kit", "https://github.com/Example/Context-Kit.git"]:
            with self.subTest(source=source):
                result = search_check({"skills": [{"name": NAME, "source": source}]}, SOURCE, NAME, "query", NAME)
                self.assertEqual(result["status"], "PASS")

    def test_same_repo_wrong_skill_is_not_a_match(self):
        result = search_check({"skills": [{"name": "another-skill", "source": SOURCE}]}, SOURCE, NAME, "query", NAME)
        self.assertEqual(result["status"], "NOT_FOUND")

    def test_stable_id_can_identify_display_named_result(self):
        result = search_check({"skills": [{"name": "Project Context Architect", "id": f"{SOURCE}/{NAME}", "source": SOURCE}]}, SOURCE, NAME, "query", NAME)
        self.assertEqual(result["status"], "PASS")

    def test_missing_array_is_not_an_empty_search(self):
        for payload in [{}, {"error": "rate limited"}, {"skills": None}, {"skills": ["bad"]},
                        {"skills": [{"name": NAME, "source": SOURCE, "id": None}]}]:
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    search_check(payload, SOURCE, NAME, "query", NAME)

    def test_unavailable_service_is_not_not_found(self):
        def unavailable(_url):
            raise URLError("offline")
        results = online_checks(CONFIG, fetch=unavailable)
        self.assertEqual({c["status"] for c in results}, {"UNAVAILABLE"})
        self.assertEqual(exit_code(results), 2)

    def test_valid_empty_search_is_diagnostic_and_metadata_drift_fails(self):
        def fetch(url):
            if "api.github.com" in url:
                return {"full_name": SOURCE, "description": "outdated", "topics": []}
            return {"skills": []}
        results = online_checks(CONFIG, fetch=fetch)
        self.assertEqual(results[0]["status"], "FAIL")
        self.assertTrue(all(c["status"] == "NOT_FOUND" for c in results[1:]))
        self.assertEqual(exit_code(results), 1)

    def test_online_success_requires_no_install_requests(self):
        urls = []
        def fetch(url):
            urls.append(url)
            if "api.github.com" in url:
                return {"full_name": SOURCE, **META}
            return {"skills": [{"name": NAME, "source": SOURCE}]}
        results = online_checks(CONFIG, fetch=fetch)
        self.assertTrue(all(c["status"] == "PASS" for c in results))
        self.assertEqual(exit_code(results, require_listed=True), 0)
        self.assertEqual(len(urls), 5)
        self.assertTrue(all("/api/search?" in url or "/repos/" in url for url in urls))

    def test_local_validation_is_read_only_and_rejects_wrong_install_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".claude-plugin").mkdir()
            (root / ".github").mkdir()
            (root / "SKILL.md").write_text(f"---\nname: {NAME}\ndescription: Maintain context across sessions.\n---\n", encoding="utf-8")
            (root / ".claude-plugin/plugin.json").write_text(json.dumps({"name": NAME, "homepage": f"https://github.com/{SOURCE}"}), encoding="utf-8")
            (root / ".github/repository-metadata.json").write_text(json.dumps(META), encoding="utf-8")
            for filename in ["README.md", "README.en.md"]:
                (root / filename).write_text(f"npx skills add {SOURCE} --skill {NAME}\n", encoding="utf-8")
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            checks, config = local_checks(root)
            self.assertEqual(exit_code(checks), 0)
            self.assertEqual(config["source"], SOURCE)
            after = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            self.assertEqual(before, after)
            (root / "README.en.md").write_text(f"npx skills add other/context-kit --skill {NAME}\n", encoding="utf-8")
            self.assertEqual(exit_code(local_checks(root)[0]), 1)


if __name__ == "__main__":
    unittest.main()
