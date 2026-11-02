"""Packaging invariants for the portable Vercel skill imports."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


class VercelImportTests(unittest.TestCase):
    bundles = {
        "vercel-react-native-skills": {
            "required": ("rules/_sections.md", "rules/_template.md", "references/full-guide.md", "references/upstream-metadata.json", "README.md"),
            "runtime_resource": "rules/list-performance-virtualize.md",
        },
        "vercel-composition-patterns": {
            "required": ("rules/_sections.md", "rules/_template.md", "references/full-guide.md", "references/upstream-metadata.json", "README.md"),
            "runtime_resource": "rules/architecture-compound-components.md",
        },
        "web-design-guidelines": {
            "required": (),
            "runtime_resource": None,
        },
        "writing-guidelines": {
            "required": (),
            "runtime_resource": None,
        },
    }

    def test_each_import_is_a_standalone_portable_bundle(self):
        for name, bundle in self.bundles.items():
            with self.subTest(skill=name):
                root = SKILLS / name
                self.assertTrue((root / "SKILL.md").is_file())
                self.assertTrue((root / "UPSTREAM.md").is_file())
                self.assertTrue((root / "LICENSE").is_file())
                for relative in bundle["required"]:
                    self.assertTrue((root / relative).is_file(), relative)
                if bundle["runtime_resource"]:
                    self.assertTrue((root / bundle["runtime_resource"]).is_file())

                entry = (root / "SKILL.md").read_text()
                self.assertRegex(entry, r"(?m)^name: [a-z0-9-]+$")
                self.assertRegex(entry, r"(?m)^description:\s*\S")
                self.assertNotIn("CLAUDE_PLUGIN_ROOT", entry)
                self.assertNotIn("WebFetch", entry)
                self.assertNotRegex(entry, r"\]\(metadata\.json(?:#|\))")

    def test_relative_markdown_resources_resolve_from_their_files(self):
        link_pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
        for name in self.bundles:
            root = SKILLS / name
            for path in root.rglob("*.md"):
                content = path.read_text()
                content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
                for target in link_pattern.findall(content):
                    target = target.strip().split()[0].strip("<>")
                    if not target or target.startswith(("https://", "http://", "mailto:", "#")):
                        continue
                    relative = target.split("#", 1)[0]
                    if relative:
                        self.assertTrue((path.parent / relative).resolve().is_file(), f"{path.relative_to(root)} -> {target}")

    def test_live_guideline_skills_preserve_fresh_fetch_and_host_neutral_failure_behavior(self):
        expected = {
            "web-design-guidelines": "https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md",
            "writing-guidelines": "https://raw.githubusercontent.com/vercel-labs/writing-guidelines/main/command.md",
        }
        for name, source in expected.items():
            entry = (SKILLS / name / "SKILL.md").read_text()
            with self.subTest(skill=name):
                self.assertIn(source, entry)
                self.assertIn("fresh", entry.lower())
                self.assertIn("network", entry.lower())
                self.assertNotIn("WebFetch", entry)
                self.assertNotIn("Claude", entry)


if __name__ == "__main__":
    unittest.main()
