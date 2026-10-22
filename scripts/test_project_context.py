"""Real-project checker tests: scope, read-only behavior and review boundaries."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import check_project_context as checker


class ProjectChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="project-context-check-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "project"
        self.root.mkdir()
        self.write("AGENTS.md", "# Rules\n\n" + "\n\n".join(
            "## " + h + "\n\nRead [state](PROJECT_STATE.md#current-work)." for h in checker.PROTOCOL_SECTIONS))
        self.write("PROJECT_STATE.md", "# State\n\n" + "\n\n".join(
            "## " + h + "\n\nExplicit context." for h in checker.STATE_SECTIONS))

    def write(self, path, text):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def append(self, path, text):
        self.write(path, (self.root / path).read_text(encoding="utf-8") + "\n\n" + text)

    def codes(self, report):
        return {f["code"] for f in report["findings"]}

    def test_clean_project_does_not_claim_semantic_verification(self):
        report = checker.inspect(self.root)
        self.assertEqual("PASS", report["mechanical_status"])
        self.assertEqual("NOT_VERIFIED", report["semantic_status"])
        self.assertEqual(0, report["warnings"])

    def test_read_only_and_no_recursive_inventory(self):
        self.write("data/private.md", "[broken](MISSING.md)")
        def snapshot():
            return {str(p.relative_to(self.root)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in self.root.rglob("*") if p.is_file()}
        before = snapshot()
        report = checker.inspect(self.root)
        self.assertEqual(before, snapshot())
        self.assertNotIn("data/private.md", report["inspected_documents"])
        self.assertEqual(0, report["errors"])

    def test_missing_entry_and_missing_section(self):
        (self.root / "AGENTS.md").unlink()
        p = self.root / "PROJECT_STATE.md"
        self.write(p.name, p.read_text(encoding="utf-8").replace("## Current Work", "### Current Work"))
        self.assertTrue({"document-unreadable", "required-section"} <= self.codes(checker.inspect(self.root)))

    def test_empty_section_rejected(self):
        self.write("PROJECT_STATE.md", "\n".join("## " + h for h in checker.STATE_SECTIONS))
        self.assertIn("empty-section", self.codes(checker.inspect(self.root)))

    def test_link_and_anchor_errors(self):
        self.append("AGENTS.md", "[file](MISSING.md)\n[section](PROJECT_STATE.md#gone)")
        self.assertTrue({"broken-link", "broken-anchor"} <= self.codes(checker.inspect(self.root)))

    def test_protocol_import_checked(self):
        self.append("AGENTS.md", "@MISSING.md")
        self.assertIn("broken-import", self.codes(checker.inspect(self.root)))

    def test_explicit_html_anchor_is_valid(self):
        self.write("docs/evidence.md", '<a id="restart-verified"></a>\n## 已核验\nEvidence.')
        self.append("PROJECT_STATE.md", "[Evidence](docs/evidence.md#restart-verified)")
        self.assertEqual(0, checker.inspect(self.root)["errors"])

    def test_custom_renderer_anchor_requires_review_not_false_error(self):
        self.write("docs/evidence.md", "## Restart {#custom-id}\nEvidence.")
        self.append("PROJECT_STATE.md", "[Evidence](docs/evidence.md#custom-id)")
        report = checker.inspect(self.root)
        self.assertEqual(0, report["errors"])
        self.assertIn("anchor-unverified", self.codes(report))

    def test_neighbor_link_is_not_read(self):
        external = self.root.parent / "external.md"
        external.write_text("private", encoding="utf-8")
        self.append("AGENTS.md", "[external](../external.md#hidden)")
        reader = checker.read_document
        def scoped_read(path):
            self.assertTrue(path.resolve().is_relative_to(self.root))
            return reader(path)
        with patch.object(checker, "read_document", side_effect=scoped_read):
            report = checker.inspect(self.root)
        self.assertIn("external-link-unchecked", self.codes(report))
        self.assertEqual(0, report["errors"])

    def test_custom_names_and_chinese_headings(self):
        (self.root / "AGENTS.md").unlink()
        (self.root / "PROJECT_STATE.md").unlink()
        self.write("CLAUDE.md", "## 协作协议\n\n遵循用户要求。")
        self.write("docs/状态.md", "## 当前工作\n\n等待验收。")
        cfg = {"protocol": "CLAUDE.md", "state": "docs/状态.md", "documents": {
            "CLAUDE.md": ["协作协议"], "docs/状态.md": ["当前工作"]}}
        self.write("context-check.json", json.dumps(cfg))
        self.assertEqual(0, checker.inspect(self.root, "context-check.json")["errors"])

    def test_vendored_scripts_and_sample_config_work_without_skill_path(self):
        scripts = Path(checker.__file__).parent
        target = self.root / "tools/context"
        target.mkdir(parents=True)
        for name in ("check_project_context.py", "document_checks.py"):
            shutil.copyfile(scripts / name, target / name)
        shutil.copyfile(scripts.parent / "examples/integration/context-check.json", self.root / "context-check.json")
        result = subprocess.run([sys.executable, "-B", str(target / "check_project_context.py"),
                                 str(self.root), "--config", "context-check.json", "--json"],
                                cwd=self.root.parent, capture_output=True, text=True, encoding="utf-8", timeout=15)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("PASS", json.loads(result.stdout)["mechanical_status"])

    def test_config_cannot_escape_scope(self):
        self.write("context-check.json", json.dumps({"protocol": "../OTHER.md"}))
        with self.assertRaises(ValueError):
            checker.inspect(self.root, "context-check.json")

    def test_unknown_config_key_rejected(self):
        self.write("context-check.json", '{"limtis": {}}')
        with self.assertRaises(ValueError):
            checker.inspect(self.root, "context-check.json")

    def test_bloat_is_warning_even_with_few_lines(self):
        self.append("PROJECT_STATE.md", "长段落" * 5000)
        report = checker.inspect(self.root)
        self.assertEqual(0, report["errors"])
        self.assertIn("state-size", self.codes(report))

    def test_diary_and_repeated_paragraph(self):
        paragraph = "This is repeated implementation detail. " * 5
        self.append("PROJECT_STATE.md", paragraph + "\n\n" + paragraph)
        self.append("PROJECT_STATE.md", "\n".join(f"2026-10-{i:02} delivered another change" for i in range(1, 7)))
        self.assertTrue({"delivery-diary", "repeated-paragraph"} <= self.codes(checker.inspect(self.root)))

    def test_opposing_status_is_review_only_with_line_evidence(self):
        self.append("PROJECT_STATE.md", "`index-migration` 已完成。\n`index-migration` 未完成。")
        report = checker.inspect(self.root)
        self.assertEqual(0, report["errors"])
        item = next(f for f in report["findings"] if f["code"] == "status-review")
        self.assertIn("environment", item["message"])
        self.assertIn("index-migration", (self.root / item["path"]).read_text(encoding="utf-8").splitlines()[item["line"] - 1])

    def test_fences_and_negation_do_not_create_completed_status(self):
        self.append("PROJECT_STATE.md", "`index-migration` not yet completed.\n\n```\n`index-migration` completed.\n```")
        self.assertNotIn("status-review", self.codes(checker.inspect(self.root)))

    def test_different_environments_are_never_automatic_errors(self):
        self.append("PROJECT_STATE.md", "Personal `feature-one` deployed.\nTrial `feature-one` pending.")
        report = checker.inspect(self.root)
        self.assertEqual(0, report["errors"])
        self.assertEqual("NOT_VERIFIED", report["semantic_status"])

    def test_cli_exit_codes_and_json(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(0, checker.main([str(self.root), "--json"]))
        self.assertEqual("NOT_VERIFIED", json.loads(output.getvalue())["semantic_status"])
        self.append("PROJECT_STATE.md", "X" * 13000)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, checker.main([str(self.root)]))
            self.assertEqual(1, checker.main([str(self.root), "--strict-warnings"]))
            self.assertEqual(2, checker.main([str(self.root), "--config", "absent.json"]))
        self.append("AGENTS.md", "[missing](ABSENT.md)")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(1, checker.main([str(self.root)]))

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_baseline_growth_and_subdirectory_root(self):
        def run(*args):
            subprocess.run(["git", "-C", str(self.root), "-c", "commit.gpgsign=false",
                            "-c", f"core.hooksPath={self.root / 'no-hooks'}", *args], check=True, capture_output=True)
        run("init")
        nested = self.root / "nested"
        nested.mkdir()
        for name in ("AGENTS.md", "PROJECT_STATE.md"):
            shutil.copyfile(self.root / name, nested / name)
        run("add", ".")
        run("-c", "user.name=Context Test", "-c", "user.email=test@example.invalid", "commit", "-m", "baseline")
        self.append("PROJECT_STATE.md", "Growth content. " * 400)
        report = checker.inspect(self.root, baseline_ref="HEAD")
        self.assertIn("document-growth", self.codes(report))
        self.assertEqual(40, len(report["baseline_commit"]))
        self.assertEqual(0, checker.inspect(nested, baseline_ref="HEAD")["metrics"]["PROJECT_STATE.md"]["growth_chars"])
        with self.assertRaises(ValueError):
            checker.inspect(self.root, baseline_ref="does-not-exist")


if __name__ == "__main__":
    unittest.main()
