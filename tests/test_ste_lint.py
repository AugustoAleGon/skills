"""Public CLI regression checks for the adapted ASD-STE100 import."""

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
LINTER = ROOT / "skills/asd-ste100/scripts/ste-lint.py"


class SteLintTests(unittest.TestCase):
    def run_linter(self, text, *args):
        result = subprocess.run(
            [sys.executable, str(LINTER), "--json", *args],
            input=text, text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.stderr, "")
        return result.returncode, json.loads(result.stdout)

    def test_frontmatter_is_not_prose_and_preserves_locations(self):
        text = "---\nname: x\ndescription: robust; scalable\n---\nThe job is robust.\n"
        code, report = self.run_linter(text)
        self.assertEqual(code, 1)
        self.assertEqual(report["words"], 4)
        self.assertEqual(
            [(finding["line"], finding["rule"]) for finding in report["violations"]],
            [(5, "marketing-adjective")],
        )

    def test_repeated_disable_flags_accumulate(self):
        text = "a; b. " + " ".join(["word"] * 30) + ".\n"
        code, report = self.run_linter(text, "--disable", "semicolon",
                                       "--disable", "long-sentence")
        self.assertEqual((code, report["count"], report["violations"]), (0, 0, []))

    def test_single_disable_flag_keeps_comma_separated_rules(self):
        code, report = self.run_linter("The robust system; runs.\n", "--disable",
                                       "semicolon,marketing-adjective")
        self.assertEqual((code, report["count"], report["violations"]), (0, 0, []))

    def test_baseline_changes_exit_status_not_findings(self):
        code, report = self.run_linter("The system; runs.\n")
        allowed_code, allowed = self.run_linter("The system; runs.\n", "--baseline", "1")
        self.assertEqual((code, allowed_code), (1, 0))
        self.assertEqual(report["violations"], allowed["violations"])
        self.assertEqual(report["count"], 1)

    def test_modal_adverbs_and_wrapped_code_do_not_raise_findings(self):
        for text in ("The job may already have failed.\n", "Use `a;\nb` now.\n"):
            with self.subTest(text=text):
                code, report = self.run_linter(text)
                self.assertEqual((code, report["count"], report["violations"]), (0, 0, []))

    def test_code_spans_do_not_hide_prose_across_blocks(self):
        cases = (
            ("Use ` as the literal delimiter.\n# Important\n"
             "Do not continue; stop.\nUse ` again.\n", 3),
            ("Use ` as the literal delimiter.\n- Do not continue; stop.\n"
             "- Use ` again.\n", 2),
            ("Use ` as the literal delimiter.\n~~~\nsample\n~~~\n"
             "Do not continue; stop.\nUse ` again.\n", 5),
        )
        for text, line in cases:
            with self.subTest(line=line):
                code, report = self.run_linter(text)
                self.assertEqual(code, 1)
                self.assertEqual(
                    [(v["line"], v["rule"]) for v in report["violations"]],
                    [(line, "semicolon")],
                )


if __name__ == "__main__":
    unittest.main()
