"""Retrieve IME guidance and exercise the published JavaScript example."""

import csv
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
SKILL = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))
from core import search  # noqa: E402


class TestImeGuidance(unittest.TestCase):
    def test_quick_reference_includes_the_rule(self):
        text = (SKILL / "references/quick-reference.md").read_text(encoding="utf-8")
        self.assertIn("`ime-composition-enter`", text)

    def test_composition_queries_retrieve_the_rule_first(self):
        for query in ("IME composition Enter", "Korean input Enter submit",
                      "Japanese Chinese composition", "한글 IME Enter"):
            with self.subTest(query=query):
                result = search(query, domain="ux", max_results=3)
                self.assertEqual("IME Composition Enter", result["results"][0]["Issue"])

    def test_csv_example_preserves_ime_and_submission_paths(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node.js is required to execute the JavaScript example")
        with (SKILL / "data/ux-guidelines.csv").open(
                encoding="utf-8", newline="") as handle:
            row, = [row for row in csv.DictReader(handle)
                    if row["Issue"] == "IME Composition Enter"]
        runner = r"""
const vm = require('node:vm');
const assert = require('node:assert/strict');
const example = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
let handler, sent = 0;
const textarea = { addEventListener(type, fn) {
  assert.equal(type, 'keydown'); handler = fn;
} };
const form = { requestSubmit() { sent++; } };
vm.runInNewContext(example, {
  textarea, form,
  document: { querySelector(selector) {
    if (selector === '#message') return textarea;
    assert.equal(selector, '#message-form'); return form;
  } }
});
function key(overrides, expectedSent, expectedPrevented) {
  let prevented = false;
  const event = { key: 'Enter', shiftKey: false, ctrlKey: false, metaKey: false,
    altKey: false, repeat: false, isComposing: false, keyCode: 13,
    preventDefault() { prevented = true; }, ...overrides };
  const composing = event.isComposing, code = event.keyCode;
  Object.defineProperty(event, 'isComposing', { get() {
    assert.equal(prevented, true, 'Cancel handled Enter before the IME guard');
    return composing;
  } });
  Object.defineProperty(event, 'keyCode', { get() {
    assert.equal(prevented, true, 'Cancel handled Enter before the 229 guard');
    return code;
  } });
  handler(event);
  assert.equal(sent, expectedSent);
  assert.equal(prevented, expectedPrevented);
}
key({isComposing: true}, 0, true);
key({isComposing: false, keyCode: 229}, 0, true);
key({key: 'Process', keyCode: 229}, 0, false);
key({key: 'a', keyCode: 65}, 0, false);
key({shiftKey: true}, 0, false);
key({ctrlKey: true}, 0, false);
key({metaKey: true}, 0, false);
key({altKey: true}, 0, false);
key({}, 1, true);
key({repeat: true}, 1, true);
"""
        completed = subprocess.run(
            [node, "-e", runner], input=json.dumps(row["Code Example Good"]),
            text=True, capture_output=True, check=True,
        )
        self.assertEqual("", completed.stdout)


if __name__ == "__main__":
    unittest.main()
