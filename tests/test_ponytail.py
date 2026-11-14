"""Check the standalone Ponytail import and its documented debt scan."""

import json
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
NAMES = ["ponytail", "ponytail-review", "ponytail-audit", "ponytail-debt",
         "ponytail-gain", "ponytail-help"]


class PonytailTests(unittest.TestCase):
    def test_all_six_are_self_contained_public_imports(self):
        manifest = json.loads((ROOT / "sources.json").read_text())
        for name in NAMES:
            with self.subTest(skill=name):
                self.assertIn(name, manifest["skills"])
                source = manifest["skills"][name]
                self.assertEqual(source["repository"], "https://github.com/DietrichGebert/ponytail")
                bundle = ROOT / source["local_path"]
                self.assertIn(source["revision"], (bundle / "UPSTREAM.md").read_text())
                self.assertIn("Copyright (c) 2026 DietrichGebert", (bundle / "LICENSE").read_text())
                self.assertFalse((bundle / "hooks").exists())
                for doc in bundle.rglob("*.md"):
                    for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", doc.read_text()):
                        if "://" not in link and not link.startswith("#"):
                            target = (doc.parent / link.split("#", 1)[0]).resolve()
                            self.assertTrue(target.is_relative_to(bundle.resolve()), str(doc))
                            self.assertTrue(target.exists(), str(target))

    def test_gain_labels_bundled_evidence_and_help_omits_plugin_setup(self):
        gain = (ROOT / "skills/ponytail-gain/SKILL.md").read_text()
        self.assertIn("upstream-reported", gain)
        self.assertIn("not independently reproduced", gain)
        self.assertIn("references/benchmark.md", gain)
        help_text = (ROOT / "skills/ponytail-help/SKILL.md").read_text()
        self.assertIn("no lifecycle hooks", help_text)
        self.assertNotIn("/plugin marketplace update", help_text)
        self.assertNotIn("export PONYTAIL_DEFAULT_MODE", help_text)

    def test_debt_scan_includes_untracked_but_excludes_ignored_files(self):
        text = (ROOT / "skills/ponytail-debt/SKILL.md").read_text()
        command = re.search(r"`(git grep [^`]+)`", text)[1]
        with tempfile.TemporaryDirectory(prefix="ponytail-debt-") as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-q", temp], check=True)
            (root / ".gitignore").write_text("ignored.py\n")
            (root / "tracked.py").write_text("# shortcut: one worker, upgrade for parallel use\n")
            (root / "untracked.py").write_text("# ponytail: small input, stream large files\n")
            (root / "ignored.py").write_text("# shortcut: excluded\n")
            (root / "prose.md").write_text("The shortcut: convention names limits.\n")
            subprocess.run(["git", "add", "tracked.py", ".gitignore"], cwd=root, check=True)
            before = {p.name: p.read_bytes() for p in root.iterdir() if p.is_file()}
            result = subprocess.run(command, cwd=root, shell=True, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            self.assertEqual({line.split(":", 1)[0] for line in result.stdout.splitlines()},
                             {"tracked.py", "untracked.py"})
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir() if p.is_file()})
            for name in ("tracked.py", "untracked.py"):
                (root / name).write_text("# no debt markers\n")
            result = subprocess.run(command, cwd=root, shell=True, capture_output=True, text=True)
            self.assertEqual((result.returncode, result.stdout, result.stderr), (1, "", ""))
