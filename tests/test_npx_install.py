"""Exercise the public Skills CLI against a standalone copy of this collection."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class NpxInstallTests(unittest.TestCase):
    def test_selected_skills_install_without_siblings(self):
        self.assertIsNotNone(shutil.which("npx"), "Node.js/npm is required for installation tests")
        with tempfile.TemporaryDirectory(prefix="skills individual install ") as temp:
            source = Path(temp) / "collection"
            shutil.copytree(
                ROOT / "skills", source / "skills",
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "node_modules"),
            )
            entries = sorted((source / "skills").glob("*/SKILL.md"))
            self.assertTrue(entries)
            for entry in entries:
                with self.subTest(skill=entry.parent.name):
                    project = Path(temp) / f"consumer-{entry.parent.name}"
                    project.mkdir()
                    result = subprocess.run(
                        ["npx", "--yes", "skills@latest", "add", str(source),
                         "--skill", entry.parent.name,
                         "--agent", "claude-code", "codex", "cursor", "--yes"],
                        cwd=project,
                        env={**os.environ, "DO_NOT_TRACK": "1"},
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        text=True, timeout=180,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout)
                    for directory in (".agents/skills", ".claude/skills"):
                        installed_root = project / directory
                        self.assertEqual(
                            {path.name for path in installed_root.iterdir() if path.is_dir()},
                            {entry.parent.name}, result.stdout,
                        )
                        installed = installed_root / entry.parent.name
                        self.assertTrue(installed.resolve().is_relative_to(project.resolve()))
                        for path in entry.parent.rglob("*"):
                            relative = path.relative_to(entry.parent)
                            if path.is_file() and not any(part.startswith(".") for part in relative.parts):
                                self.assertEqual((installed / relative).read_bytes(), path.read_bytes())
            shutil.rmtree(source)
            for entry in entries:
                project = Path(temp) / f"consumer-{entry.parent.name}"
                for directory in (".agents/skills", ".claude/skills"):
                    self.assertTrue((project / directory / entry.parent.name / "SKILL.md").is_file())

    def test_install_complete_skills_for_all_three_hosts(self):
        self.assertIsNotNone(shutil.which("npx"), "Node.js/npm is required for installation tests")
        with tempfile.TemporaryDirectory(prefix="skills npx install ") as temp:
            source = Path(temp) / "collection"
            project = Path(temp) / "consumer"
            project.mkdir()
            # Test the public skills/ layout without this checkout's discovery links.
            shutil.copytree(
                ROOT / "skills", source / "skills",
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "node_modules"),
            )
            result = subprocess.run(
                ["npx", "--yes", "skills@latest", "add", str(source),
                 "--skill", "*", "--agent", "claude-code", "codex", "cursor", "--yes"],
                cwd=project,
                env={**os.environ, "DO_NOT_TRACK": "1"},
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=180,
            )
            self.assertEqual(result.returncode, 0, result.stdout)
            entries = sorted((source / "skills").glob("*/SKILL.md"))
            self.assertTrue(entries, "The collection must contain installable skills")
            for entry in entries:
                expected = {
                    path.relative_to(entry.parent): path.read_bytes()
                    for path in entry.parent.rglob("*") if path.is_file()
                }
                # The CLI may omit repository-only dotfiles; runtime resources must survive.
                expected = {path: data for path, data in expected.items()
                            if not any(part.startswith(".") for part in path.parts)}
                for agent, directory in {
                    "claude-code": ".claude/skills",
                    "codex": ".agents/skills",
                    "cursor": ".agents/skills",
                }.items():
                    with self.subTest(skill=entry.parent.name, agent=agent):
                        installed = project / directory / entry.parent.name
                        self.assertTrue(installed.is_dir(), result.stdout)
                        self.assertTrue(installed.resolve().is_relative_to(project.resolve()))
                        for relative, data in expected.items():
                            self.assertEqual((installed / relative).read_bytes(), data, str(relative))
            # Installed copies must remain usable without a local source clone.
            shutil.rmtree(source)
            for entry in entries:
                for directory in (".agents/skills", ".claude/skills"):
                    self.assertTrue((project / directory / entry.parent.name / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
