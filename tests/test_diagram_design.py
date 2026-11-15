"""Standalone packaging and local self-check coverage for Diagram Design."""

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "skills/diagram-design"


class DiagramDesignTests(unittest.TestCase):
    def test_standalone_bundle_records_provenance_and_notices(self):
        source = json.loads((ROOT / "sources.json").read_text())["skills"]["diagram-design"]
        self.assertEqual(source["repository"], "https://github.com/cathrynlavery/diagram-design")
        self.assertEqual(source["paths"], ["skills/diagram-design", "LICENSE", "THIRD_PARTY_LICENSES.md"])
        self.assertIn(source["revision"], (BUNDLE / "UPSTREAM.md").read_text())
        for resource in ("LICENSE", "THIRD_PARTY_LICENSES.md", "SKILL.md",
                         "assets/template-motion.html", "references/onboarding.md",
                         "scripts/self_check.py", "scripts/export_png.py"):
            self.assertTrue((BUNDLE / resource).is_file(), resource)
        self.assertIn("Cathryn Lavery", (BUNDLE / "LICENSE").read_text())
        self.assertIn("Tabler Icons", (BUNDLE / "THIRD_PARTY_LICENSES.md").read_text())
        self.assertIn("Standalone installation", (BUNDLE / "SKILL.md").read_text())

    def test_relative_markdown_links_stay_inside_bundle(self):
        self.assertTrue(BUNDLE.is_dir())
        for path in BUNDLE.rglob("*.md"):
            content = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
            for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", content):
                target = target.strip().split()[0].strip("<>").split("#")[0]
                if not target or ":" in target:
                    continue
                resolved = (path.parent / target).resolve()
                self.assertTrue(resolved.is_relative_to(BUNDLE.resolve()), str(path))
                self.assertTrue(resolved.exists(), f"{path}: {target}")

    def test_packaged_self_check_accepts_static_and_animated_examples(self):
        for name in ("example-architecture.html", "template-motion.html"):
            with self.subTest(asset=name):
                result = subprocess.run(
                    [sys.executable, str(BUNDLE / "scripts/self_check.py"),
                     str(BUNDLE / "assets" / name)],
                    capture_output=True, text=True, timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_self_check_rejects_invalid_input_without_changing_it(self):
        with tempfile.TemporaryDirectory(prefix="diagram-design-check-") as temp:
            path = Path(temp) / "invalid.html"
            content = b"<!doctype html><html><body>No diagram</body></html>"
            path.write_bytes(content)
            result = subprocess.run(
                [sys.executable, str(BUNDLE / "scripts/self_check.py"), str(path)],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertTrue(result.stdout + result.stderr)
            self.assertEqual(path.read_bytes(), content)


if __name__ == "__main__":
    unittest.main()
