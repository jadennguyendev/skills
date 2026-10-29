"""Checks view.py's renderers and that the page only carries tabs for files that exist.

    python3 view_test.py
"""

import doctest
import json
import tempfile
import unittest
from pathlib import Path

import view


class BuildTest(unittest.TestCase):
    def test_tabs_and_review_copy(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)
            (v / "01-story").mkdir()
            (v / "config.json").write_text(json.dumps({"title": "Comb <1>", "language": "en", "review_language": "vi"}))
            (v / "01-story/story.md").write_text("# One\n\nShe *waited*.")
            (v / "01-story/story.vi.md").write_text("# Một\n\nCô ấy *đợi*.")
            page = view.build(v)
        self.assertIn("<title>Comb &lt;1&gt;</title>", page)
        self.assertIn(">Story<", page)
        self.assertNotIn(">Shot list<", page)
        self.assertIn('class="has-vi"', page)
        self.assertIn("<em>đợi</em>", page)
        self.assertIn("EN / VI", page)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(view))
    return tests


if __name__ == "__main__":
    unittest.main()
