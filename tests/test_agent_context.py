"""Check the independently installable context pack resources."""

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "skills/agent-context"


class AgentContextPackagingTests(unittest.TestCase):
    def test_import_is_registered_with_exact_english_source_paths(self):
        source = json.loads((ROOT / "sources.json").read_text())["skills"]["agent-context"]
        self.assertRegex(source["revision"], r"^[0-9a-f]{40}$")
        self.assertIn("arkandia/skills/agent-context/templates/en", source["paths"])
        self.assertFalse(any("templates/es" in path for path in source["paths"]))
        self.assertIn(source["revision"], (BUNDLE / "UPSTREAM.md").read_text())
        self.assertIn("Manuel Zapata", (BUNDLE / "LICENSE").read_text())

    def test_all_output_templates_are_bundled_without_host_specific_stub(self):
        self.assertEqual({p.name for p in (BUNDLE / "templates").iterdir()}, {"en"})
        templates = BUNDLE / "templates/en"
        self.assertEqual(
            {p.name for p in templates.glob("*.md.template")},
            {f"{name}.md.template" for name in (
                "AGENTS", "architecture", "business", "data-model",
                "infrastructure", "target-user", "design",
            )},
        )
        for name in ("README.md", "adr-template.md"):
            self.assertTrue((templates / "adrs" / name).is_file())

    def test_runtime_reference_links_remain_inside_installable_bundle(self):
        docs = [BUNDLE / "SKILL.md", *sorted((BUNDLE / "references").glob("*.md"))]
        self.assertGreater(len(docs), 1)
        for doc in docs:
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", doc.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                with self.subTest(doc=doc.name, target=target):
                    path = (doc.parent / target.split("#", 1)[0]).resolve()
                    self.assertTrue(path.is_relative_to(BUNDLE.resolve()))
                    self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
