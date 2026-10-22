"""Regression tests for preservation, navigation and package validation.

Use temporary fixture copies. These tests do not prove model behavior or
semantic conflict resolution; see fixtures/README.md for behavioral rehearsal.
"""
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import json

from document_checks import check_links
from verify_refactor import FIXTURE, HISTORY, STATE_SECTIONS, verify
import lint_skill


class RefactorValidation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="context-validation-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        shutil.copytree(FIXTURE, self.root)
        hist = self.root / "docs/history"
        hist.mkdir(parents=True)
        for rel in HISTORY:
            old = self.root / rel
            text = old.read_text(encoding="utf-8")
            (hist / old.name).write_text("> Historical artifact.\n> Not authoritative for current project behavior.\n\n" + text, encoding="utf-8")
            old.unlink()
        self.write("AGENTS.md", "# Rules\n## New Session Protocol\nRead state.\n## Authority Maintenance Protocol\nMaintain facts.\n")
        self.write("PROJECT_STATE.md", "Last Updated: 2026-10-22\n" + "\n".join("## " + s + "\nExample." for s in STATE_SECTIONS))
        self.write("README.md", "# Example\n[State](PROJECT_STATE.md#current-work)\n")

    def write(self, rel, text):
        (self.root / rel).write_text(text, encoding="utf-8")

    def test_valid_fixture_copy(self):
        self.assertEqual([], verify(self.root))

    def test_each_archive_is_required(self):
        for rel in HISTORY:
            with self.subTest(rel=rel):
                p = self.root / "docs/history" / Path(rel).name
                content = p.read_bytes()
                p.unlink()
                self.assertTrue(any("expected one archived copy" in s for s in verify(self.root)))
                p.write_bytes(content)

    def test_archive_content_must_survive(self):
        self.write("docs/history/TODO-old.md", "> Not authoritative for current project behavior.\nLost original content.\n")
        self.assertTrue(any("content changed or lost" in s for s in verify(self.root)))

    def test_function_names_do_not_prove_preservation(self):
        self.write("summarize.py", '# load_reminders render_digest\nraise RuntimeError("broken")\n')
        self.assertTrue(any("business file changed" in s for s in verify(self.root)))

    def test_tests_cannot_be_deleted(self):
        (self.root / "tests/test_summarize.py").unlink()
        self.assertTrue(any("test_summarize.py" in s for s in verify(self.root)))

    def test_requirements_cannot_be_changed(self):
        self.write("requirements.txt", "unrequested-package\n")
        self.assertTrue(any("requirements.txt" in s for s in verify(self.root)))

    def test_gemini_is_supported(self):
        (self.root / "AGENTS.md").rename(self.root / "GEMINI.md")
        self.assertEqual([], verify(self.root))

    def test_custom_owner(self):
        (self.root / "AGENTS.md").rename(self.root / "TEAM.md")
        self.assertEqual([], verify(self.root, convention="TEAM.md"))

    def test_adapter_is_allowed_but_duplicate_owner_is_not(self):
        self.write("CLAUDE.md", "@AGENTS.md\n")
        self.assertEqual([], verify(self.root))
        shutil.copyfile(self.root / "AGENTS.md", self.root / "CLAUDE.md")
        self.assertTrue(any("canonical protocol owner" in s for s in verify(self.root)))

    def test_missing_anchor_is_rejected(self):
        self.write("README.md", "[Work](PROJECT_STATE.md#missing-work)\n")
        self.assertTrue(any("broken anchor" in s for s in verify(self.root)))

    def test_missing_file_is_rejected(self):
        self.write("README.md", "[Architecture](MISSING.md)\n")
        self.assertTrue(any("broken link" in s for s in verify(self.root)))

    def test_fenced_headings_do_not_satisfy_required_sections(self):
        self.write("PROJECT_STATE.md", "```md\nLast Updated: 2026-10-22\n" + "\n".join("## " + s for s in STATE_SECTIONS) + "\n```\n")
        self.assertTrue(any("missing section" in s for s in verify(self.root)))

    def test_handoff_subheading_cannot_replace_current_work(self):
        p = self.root / "PROJECT_STATE.md"
        text = p.read_text(encoding="utf-8").replace("## Current Work", "### Current Work")
        p.write_text(text, encoding="utf-8")
        self.assertTrue(any("missing section: Current Work" in s for s in verify(self.root)))

    def test_fenced_examples_are_not_document_links(self):
        self.write("README.md", "# Example\n```md\n[Example](MISSING.md)\n```\n[Self](#example)\n")
        self.assertEqual([], check_links([self.root / "README.md"]))

    def test_duplicate_heading_anchor(self):
        self.write("README.md", "# Same\n# Same\n[Second](#same-1)\n")
        self.assertEqual([], check_links([self.root / "README.md"]))


class DistributionValidation(unittest.TestCase):
    def test_missing_marketplace_owner_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix="context-package-") as tmp:
            root = Path(tmp)
            (root / ".claude-plugin").mkdir()
            for rel in ["SKILL.md", "CHANGELOG.md", ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"]:
                shutil.copyfile(lint_skill.ROOT / rel, root / rel)
            with patch.object(lint_skill, "ROOT", root):
                self.assertEqual([], lint_skill.check_metadata())
                p = root / ".claude-plugin/marketplace.json"
                data = json.loads(p.read_text(encoding="utf-8"))
                del data["owner"]
                p.write_text(json.dumps(data), encoding="utf-8")
                self.assertTrue(any("owner.name" in s for s in lint_skill.check_metadata()))


if __name__ == "__main__":
    unittest.main()
