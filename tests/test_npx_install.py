"""Exercise the public Skills CLI against a standalone copy of this collection."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "sources.json").read_text())
PUBLIC_SKILLS = set(MANIFEST["skills"])
INTERNAL_SKILLS = set(MANIFEST.get("local_skills", {}))


def cli_env():
    return {**{key: value for key, value in os.environ.items()
               if key != "INSTALL_INTERNAL_SKILLS"}, "DO_NOT_TRACK": "1"}


def public_entries(source):
    return [entry for entry in sorted((source / "skills").glob("*/SKILL.md"))
            if entry.parent.name in PUBLIC_SKILLS]


class NpxInstallTests(unittest.TestCase):
    def test_selected_skills_install_without_siblings(self):
        self.assertIsNotNone(shutil.which("npx"), "Node.js/npm is required for installation tests")
        with tempfile.TemporaryDirectory(prefix="skills individual install ") as temp:
            source = Path(temp) / "collection"
            shutil.copytree(
                ROOT / "skills", source / "skills",
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "node_modules"),
            )
            entries = public_entries(source)
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
                        env=cli_env(),
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
            self.assert_public_listing(source, project)
            result = subprocess.run(
                ["npx", "--yes", "skills@latest", "add", str(source),
                 "--skill", "*", "--agent", "claude-code", "codex", "cursor", "--yes"],
                cwd=project,
                env=cli_env(),
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=180,
            )
            self.assertEqual(result.returncode, 0, result.stdout)
            entries = public_entries(source)
            self.assertTrue(entries, "The collection must contain installable skills")
            self.assert_public_install(project, result.stdout)
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

    def assert_public_listing(self, source, project):
        result = subprocess.run(
            ["npx", "--yes", "skills@latest", "add", str(source), "--list"],
            cwd=project, env=cli_env(), stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, timeout=180,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        for name in PUBLIC_SKILLS:
            self.assertIn(name, result.stdout)
        for name in INTERNAL_SKILLS:
            self.assertNotIn(name, result.stdout)

    def assert_public_install(self, project, output):
        for directory in (".agents/skills", ".claude/skills"):
            installed = project / directory
            self.assertEqual({p.name for p in installed.iterdir() if p.is_dir()}, PUBLIC_SKILLS, output)
            for name in INTERNAL_SKILLS:
                self.assertFalse((installed / name).exists(), output)

    def test_internal_skill_excluded_with_development_links(self):
        self.assertIsNotNone(shutil.which("npx"), "Node.js/npm is required for installation tests")
        self.assertIn("update-collected-skills", INTERNAL_SKILLS)
        with tempfile.TemporaryDirectory(prefix="skills linked install ") as temp:
            source = Path(temp) / "collection"
            project = Path(temp) / "consumer"
            project.mkdir()
            shutil.copytree(
                ROOT / "skills", source / "skills",
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "node_modules"),
            )
            for directory in (".agents/skills", ".claude/skills"):
                shutil.copytree(ROOT / directory, source / directory, symlinks=True)
                for name in INTERNAL_SKILLS:
                    link = source / directory / name
                    self.assertTrue(link.is_symlink())
                    self.assertEqual(link.resolve(), (source / "skills" / name).resolve())
                    self.assertTrue((link / "SKILL.md").is_file())
            self.assert_public_listing(source, project)
            result = subprocess.run(
                ["npx", "--yes", "skills@latest", "add", str(source),
                 "--skill", "*", "--agent", "claude-code", "codex", "cursor", "--yes"],
                cwd=project, env=cli_env(), stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, timeout=180,
            )
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assert_public_install(project, result.stdout)


if __name__ == "__main__":
    unittest.main()
