"""Behavioral tests against real, isolated Git repositories; no network needed."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


inspector = load_module("inspect_upstream", ROOT / "skills/update-collected-skills/scripts/inspect_upstream.py")
validator = load_module("validate", ROOT / "scripts/validate.py")


class UpstreamReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="upstream review ")
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.upstream = self.folder / "upstream"
        self.root = self.folder / "collection"
        self.output = self.folder / "report"
        for directory in (self.upstream, self.root):
            directory.mkdir()
            self.git(directory, "init", "-b", "main")
            self.git(directory, "config", "user.name", "Fixture")
            self.git(directory, "config", "user.email", "fixture@example.invalid")
        self.write(self.upstream, "skills/example/SKILL.md", "---\nname: example\ndescription: Example\n---\nOriginal\n")
        self.write(self.upstream, "skills/example/remove.txt", "Remove me\n")
        self.write(self.upstream, "skills/example/rename.txt", "Identical long enough content for rename detection\n")
        self.write(self.upstream, "LICENSE", "Fixture license\n")
        self.write(self.upstream, "skills/excluded/SKILL.md", "Excluded\n")
        self.write(self.upstream, "skills/uncollected/SKILL.md", "Existing uncollected\n")
        self.base = self.commit(self.upstream)
        self.write(self.root, "skills/example/SKILL.md", "---\nname: example\ndescription: Example\n---\nLocal adaptation\n")
        self.write(self.root, "skills/example/LICENSE", "Fixture license\n")
        self.write(self.root, "skills/example/UPSTREAM.md", "Keep local adaptation\n")
        self.manifest = {
            "version": 1,
            "skills": {"example": {
                "repository": str(self.upstream), "revision": self.base,
                "paths": ["skills/example", "LICENSE"], "license": "Fixture",
                "local_path": "skills/example", "adaptation_notes": "skills/example/UPSTREAM.md",
            }},
            "excluded_skills": [{"repository": str(self.upstream), "path": "skills/excluded", "reason": "Intentional"}],
        }
        self.save_manifest()
        self.commit(self.root)

    def git(self, directory, *args):
        return subprocess.check_output(["git", *args], cwd=directory, stderr=subprocess.PIPE).decode().strip()

    def write(self, root, relative, text):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def commit(self, directory):
        self.git(directory, "add", ".")
        self.git(directory, "-c", "commit.gpgsign=false", "commit", "-m", "Fixture")
        return self.git(directory, "rev-parse", "HEAD")

    def save_manifest(self):
        self.write(self.root, "sources.json", json.dumps(self.manifest))

    def run_review(self, **kwargs):
        return inspector.inspect(self.root, self.output, **kwargs)

    def test_unchanged_revision_is_noop_and_preserves_local_adaptation(self):
        before = self.git(self.root, "status", "--porcelain")
        report = self.run_review()
        self.assertEqual(report["skills"][0]["target"], self.base)
        self.assertFalse(report["skills"][0]["upstream_changed"])
        self.assertEqual((self.output / "example/upstream.diff").read_bytes(), b"")
        self.assertIn("Local adaptation", (self.output / "example/local/SKILL.md").read_text())
        self.assertIn("Original", (self.output / "example/base/skills/example/SKILL.md").read_text())
        self.assertEqual(self.git(self.root, "status", "--porcelain"), before)

    def test_changes_candidates_renames_and_dirty_local_content_are_reported(self):
        self.write(self.upstream, "skills/example/SKILL.md", "Upstream replacement\n")
        (self.upstream / "skills/example/remove.txt").unlink()
        (self.upstream / "skills/example/rename.txt").rename(self.upstream / "skills/example/renamed.txt")
        self.write(self.upstream, "skills/new/SKILL.md", "New candidate\n")
        target = self.commit(self.upstream)
        self.write(self.root, "skills/example/SKILL.md", "Uncommitted local work\n")
        before = self.git(self.root, "diff")
        report = self.run_review()
        entry = report["skills"][0]
        self.assertTrue(entry["upstream_changed"])
        self.assertEqual(entry["base"], self.base)
        self.assertEqual(entry["target"], target)
        diff = (self.output / "example/upstream.diff").read_text()
        self.assertIn("deleted file mode", diff)
        self.assertIn("rename from", diff)
        self.assertIn("+Upstream replacement", diff)
        self.assertIn("SKILL.md", report["working_tree_status"])
        self.assertEqual((self.output / "example/local/SKILL.md").read_text(), "Uncommitted local work\n")
        self.assertEqual(self.git(self.root, "diff"), before)
        self.assertEqual({c["path"]: c["status"] for c in report["repositories"][0]["candidates"]}, {
            "skills/excluded/SKILL.md": "excluded", "skills/uncollected/SKILL.md": "uncollected", "skills/new/SKILL.md": "new",
        })

    def test_missing_revision_fails_without_report_or_collection_edits(self):
        self.manifest["skills"]["example"]["revision"] = "0" * 40
        self.save_manifest()
        before = self.git(self.root, "diff")
        with self.assertRaises(ValueError):
            self.run_review()
        self.assertFalse(self.output.exists())
        self.assertEqual(self.git(self.root, "diff"), before)

    def test_explicit_target_and_missing_upstream_path(self):
        for path in (self.upstream / "skills/example").iterdir():
            path.unlink()
        target = self.commit(self.upstream)
        report = self.run_review(targets={str(self.upstream): self.base})
        self.assertEqual(report["skills"][0]["target"], self.base)
        self.output = self.folder / "deleted-report"
        report = self.run_review()
        self.assertEqual(report["skills"][0]["target"], target)
        self.assertIn("skills/example", report["skills"][0]["target_snapshot"]["missing_paths"])
        self.assertTrue((self.root / "skills/example/SKILL.md").is_file())

    def test_symlinks_are_reported_without_following_them(self):
        (self.upstream / "skills/example/link").symlink_to("/etc/passwd")
        self.commit(self.upstream)
        (self.root / "skills/example/link").symlink_to("/etc/passwd")
        report = self.run_review()
        entry = report["skills"][0]
        self.assertEqual(entry["local_skipped"], ["link"])
        self.assertEqual(entry["target_snapshot"]["skipped"][0]["path"], "skills/example/link")
        self.assertFalse((self.output / "example/target/skills/example/link").exists())
        self.assertFalse((self.output / "example/local/link").exists())

    def test_refuses_invalid_scope_paths_and_overwriting_reports(self):
        with self.assertRaises(ValueError):
            self.run_review(selected=["unknown"])
        with self.assertRaises(ValueError):
            self.run_review(targets={"https://example.invalid/other": "HEAD"})
        with self.assertRaises(ValueError):
            inspector.inspect(self.root, self.root / "report")
        self.output.mkdir()
        (self.output / "keep").write_text("Keep")
        with self.assertRaises(ValueError):
            self.run_review()
        self.assertEqual((self.output / "keep").read_text(), "Keep")
        self.output = self.folder / "invalid-path-report"
        self.manifest["skills"]["example"]["paths"] = ["../outside"]
        self.save_manifest()
        with self.assertRaises(ValueError):
            self.run_review()
        self.assertFalse(self.output.exists())


class LocalSkillValidationTests(unittest.TestCase):
    def test_local_provenance_and_export_flag_are_required(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = root / "skills/maintenance"
            skill.mkdir(parents=True)
            record = {"local_path": "skills/maintenance", "internal": True}
            manifest = {"skills": {}, "local_skills": {"maintenance": record}}
            (root / "sources.json").write_text(json.dumps(manifest))
            header = "---\nname: maintenance\ndescription: Maintain the collection\n"
            entry = skill / "SKILL.md"
            for metadata, valid in (
                ("metadata:\n  internal: true\n", True),
                ("metadata:\n  internal: false\n", False),
                ("metadata:\n  internal: 'true'\n", False),
                ("internal: true\n", False),
                ("other:\n  internal: true\n", False),
                ("", False),
            ):
                with self.subTest(metadata=metadata), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    entry.write_text(header + metadata + "---\nMaintain\n")
                    self.assertEqual(validator.main(root), 0 if valid else 1)
            entry.write_text(header + "metadata:\n  internal: true\n---\nMaintain\n")
            record["revision"] = "0" * 40
            (root / "sources.json").write_text(json.dumps(manifest))
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(validator.main(root), 1)


if __name__ == "__main__":
    unittest.main()
