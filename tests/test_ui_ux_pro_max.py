"""Public CLI checks for the portable UI/UX Pro Max skill bundle."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL_SOURCE = REPOSITORY / "skills" / "ui-ux-pro-max"


class UiUxProMaxCliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scratch = tempfile.TemporaryDirectory(prefix="ui-ux-pro-max-")
        cls.scratch_root = Path(cls.scratch.name)
        cls.skill_dir = cls.scratch_root / "installed skills" / "ui ux pro max"
        shutil.copytree(SKILL_SOURCE, cls.skill_dir)
        cls.script = cls.skill_dir / "scripts" / "search.py"

    @classmethod
    def tearDownClass(cls):
        cls.scratch.cleanup()

    def run_cli(self, *arguments, cwd):
        return subprocess.run(
            [sys.executable, str(self.script), *arguments],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_domain_and_stack_search_work_from_arbitrary_cwd_and_spaced_skill_path(self):
        with tempfile.TemporaryDirectory(prefix="unrelated project ") as raw_cwd:
            domain = self.run_cli(
                "dashboard accessibility keyboard focus",
                "--domain", "ux", "--json", cwd=raw_cwd,
            )
            stack = self.run_cli(
                "component state management", "--stack", "react", "--json", cwd=raw_cwd,
            )
            self.assertEqual(0, domain.returncode, domain.stderr)
            self.assertEqual(0, stack.returncode, stack.stderr)
            self.assertEqual("ux", json.loads(domain.stdout)["domain"])
            self.assertGreater(json.loads(domain.stdout)["count"], 0)
            self.assertEqual("react", json.loads(stack.stdout)["stack"])
            self.assertGreater(json.loads(stack.stdout)["count"], 0)

    def test_design_system_generation_uses_local_resources_and_does_not_write_by_default(self):
        with tempfile.TemporaryDirectory(prefix="no-write project ") as raw_cwd:
            result = self.run_cli(
                "therapy clinic appointment booking", "--design-system", "--json",
                "--project-name", "Therapy Clinic", cwd=raw_cwd,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(result.stdout)
            self.assertIsNone(payload["persistence"])
            self.assertIn("design_system", payload)
            self.assertFalse((Path(raw_cwd) / "design-system").exists())

    def test_persistence_creates_requested_files_and_preserves_existing_master(self):
        with tempfile.TemporaryDirectory(prefix="external output ") as raw_output:
            output = Path(raw_output)
            master = output / "design-system" / "therapy-clinic" / "MASTER.md"
            master.parent.mkdir(parents=True)
            original = "# Existing approved decisions\nDo not replace.\n"
            master.write_text(original, encoding="utf-8")

            skipped = self.run_cli(
                "therapy clinic appointment booking", "--design-system", "--json",
                "--project-name", "Therapy Clinic", "--persist", "--output-dir", str(output),
                cwd=self.scratch_root,
            )
            self.assertEqual(0, skipped.returncode, skipped.stderr)
            self.assertEqual("skipped_exists", json.loads(skipped.stdout)["persistence"]["status"])
            self.assertEqual(original, master.read_text(encoding="utf-8"))

        with tempfile.TemporaryDirectory(prefix="authorized output ") as raw_output:
            output = Path(raw_output)
            persisted = self.run_cli(
                "therapy clinic appointment booking", "--design-system", "--json",
                "--project-name", "Therapy Clinic", "--persist", "--output-dir", str(output),
                cwd=self.scratch_root,
            )
            self.assertEqual(0, persisted.returncode, persisted.stderr)
            payload = json.loads(persisted.stdout)
            self.assertEqual("success", payload["persistence"]["status"])
            self.assertTrue((output / "design-system" / "therapy-clinic" / "MASTER.md").is_file())

            existing = output / "design-system" / "therapy-clinic" / "MASTER.md"
            existing.write_text("# Prior content\n", encoding="utf-8")
            forced = self.run_cli(
                "therapy clinic appointment booking", "--design-system", "--json",
                "--project-name", "Therapy Clinic", "--persist", "--force",
                "--output-dir", str(output), cwd=self.scratch_root,
            )
            self.assertEqual(0, forced.returncode, forced.stderr)
            self.assertNotEqual("# Prior content\n", existing.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
