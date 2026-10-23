#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Unit tests for copy-templates.py — uses tempdirs, no real project touched.

Run: python3 scripts/tests/test-copy-templates.py
Exits non-zero on failure.
"""

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


def _load_copy_templates():
    here = Path(__file__).resolve().parent.parent
    spec = importlib.util.spec_from_file_location("copy_templates", here / "copy-templates.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ct = _load_copy_templates()


class CopyTemplatesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="bmad-cp-test-"))
        self.source = self.tmp / "templates"
        self.target = self.tmp / "project"
        self.source.mkdir()
        self.target.mkdir()
        # Build a representative source tree:
        #   templates/.claude/claude.md
        #   templates/.claude/rules/rule-a.md
        #   templates/.claude/rules/rule-b.md
        (self.source / ".claude").mkdir()
        (self.source / ".claude" / "claude.md").write_text("CLAUDE content\n")
        (self.source / ".claude" / "rules").mkdir()
        (self.source / ".claude" / "rules" / "rule-a.md").write_text("rule A\n")
        (self.source / ".claude" / "rules" / "rule-b.md").write_text("rule B\n")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ─── Basic mirroring ────────────────────────────────────────────────────

    def test_copy_into_empty_target_creates_all_files(self):
        result = ct.copy_templates(self.source, self.target, overwrite=False, dry_run=False)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["summary"]["copied_count"], 3)
        self.assertEqual(result["summary"]["skipped_count"], 0)
        self.assertEqual(result["summary"]["error_count"], 0)
        # Files exist with content preserved
        self.assertEqual((self.target / ".claude" / "claude.md").read_text(), "CLAUDE content\n")
        self.assertEqual((self.target / ".claude" / "rules" / "rule-a.md").read_text(), "rule A\n")
        self.assertEqual((self.target / ".claude" / "rules" / "rule-b.md").read_text(), "rule B\n")

    def test_creates_intermediate_directories(self):
        # Pre-flight: target/.claude does NOT exist yet — script must create it.
        self.assertFalse((self.target / ".claude").exists())
        ct.copy_templates(self.source, self.target, overwrite=False, dry_run=False)
        self.assertTrue((self.target / ".claude" / "rules").is_dir())

    # ─── Skip-existing safety ───────────────────────────────────────────────

    def test_skips_existing_files_by_default(self):
        # User has already customized claude.md — we must NOT clobber it.
        (self.target / ".claude").mkdir()
        (self.target / ".claude" / "claude.md").write_text("USER's customized content\n")

        result = ct.copy_templates(self.source, self.target, overwrite=False, dry_run=False)
        self.assertEqual(result["summary"]["copied_count"], 2)  # 2 rule files only
        self.assertEqual(result["summary"]["skipped_count"], 1)
        # User content preserved verbatim
        self.assertEqual((self.target / ".claude" / "claude.md").read_text(),
                         "USER's customized content\n")

    def test_skip_reason_is_informative(self):
        (self.target / ".claude").mkdir()
        (self.target / ".claude" / "claude.md").write_text("existing\n")
        result = ct.copy_templates(self.source, self.target, overwrite=False, dry_run=False)
        skipped = result["skipped"][0]
        self.assertEqual(skipped["source"], ".claude/claude.md")
        self.assertIn("--overwrite", skipped["reason"])

    # ─── --overwrite flag ───────────────────────────────────────────────────

    def test_overwrite_replaces_existing_files(self):
        (self.target / ".claude").mkdir()
        (self.target / ".claude" / "claude.md").write_text("OLD\n")

        result = ct.copy_templates(self.source, self.target, overwrite=True, dry_run=False)
        self.assertEqual(result["summary"]["copied_count"], 3)
        self.assertEqual(result["summary"]["skipped_count"], 0)
        self.assertEqual((self.target / ".claude" / "claude.md").read_text(), "CLAUDE content\n")

    # ─── --dry-run ──────────────────────────────────────────────────────────

    def test_dry_run_writes_nothing(self):
        result = ct.copy_templates(self.source, self.target, overwrite=False, dry_run=True)
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["summary"]["copied_count"], 3)
        # No files were actually written
        self.assertFalse((self.target / ".claude" / "claude.md").exists())
        self.assertFalse((self.target / ".claude" / "rules" / "rule-a.md").exists())
        # Action labels reflect intent
        actions = {entry["source"]: entry["action"] for entry in result["copied"]}
        self.assertEqual(actions[".claude/claude.md"], "would-create")

    def test_dry_run_with_existing_uses_would_overwrite_label(self):
        (self.target / ".claude").mkdir()
        (self.target / ".claude" / "claude.md").write_text("existing\n")
        result = ct.copy_templates(self.source, self.target, overwrite=True, dry_run=True)
        labels = {entry["source"]: entry["action"] for entry in result["copied"]}
        self.assertEqual(labels[".claude/claude.md"], "would-overwrite")

    # ─── --only-glob (rules-only refresh) ───────────────────────────────────

    def test_only_glob_copies_matching_files_only(self):
        # The "update rules" flow: refresh ONLY .claude/rules/*, ignore claude.md.
        result = ct.copy_templates(
            self.source, self.target, overwrite=False, dry_run=False,
            only_globs=[".claude/rules/*"],
        )
        self.assertEqual(result["summary"]["copied_count"], 2)  # rule-a, rule-b
        self.assertEqual(result["summary"]["skipped_count"], 0)  # claude.md not even considered
        self.assertTrue((self.target / ".claude" / "rules" / "rule-a.md").exists())
        self.assertFalse((self.target / ".claude" / "claude.md").exists())

    def test_only_glob_with_overwrite_glob_replaces_existing_rules(self):
        # Pre-existing (stale) rule + customized claude.md.
        (self.target / ".claude" / "rules").mkdir(parents=True)
        (self.target / ".claude" / "rules" / "rule-a.md").write_text("STALE rule A\n")
        (self.target / ".claude" / "claude.md").write_text("USER customized\n")

        result = ct.copy_templates(
            self.source, self.target, overwrite=False, dry_run=False,
            overwrite_globs=[".claude/rules/*"],
            only_globs=[".claude/rules/*"],
        )
        self.assertEqual(result["summary"]["copied_count"], 2)
        self.assertEqual(result["summary"]["skipped_count"], 0)
        # Stale rule refreshed from source...
        self.assertEqual((self.target / ".claude" / "rules" / "rule-a.md").read_text(), "rule A\n")
        # ...but the user's claude.md was never touched.
        self.assertEqual((self.target / ".claude" / "claude.md").read_text(), "USER customized\n")

    # ─── Edge cases ─────────────────────────────────────────────────────────

    def test_missing_source_dir_returns_error(self):
        bogus = self.tmp / "does-not-exist"
        result = ct.copy_templates(bogus, self.target, overwrite=False, dry_run=False)
        self.assertEqual(result["status"], "error")
        self.assertIn("does not exist", result["message"])

    def test_empty_source_dir_returns_ok_with_zero_copies(self):
        empty = self.tmp / "empty"
        empty.mkdir()
        result = ct.copy_templates(empty, self.target, overwrite=False, dry_run=False)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["summary"]["copied_count"], 0)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    sys.exit(0 if result.wasSuccessful() else 1)
