"""Checks screenplay.py's validation and renders.

    python3 screenplay_test.py
"""

import doctest
import json
import tempfile
import unittest
from pathlib import Path

import screenplay
from screenplay import check, narration_md, render, screenplay_txt

CONFIG = {"branch": "film", "language": "en", "target_duration_min": 1, "max_characters": 2, "max_locations": 1}
BIBLE = {"characters": [{"id": "lan", "name": "Lan"}], "locations": [{"id": "house", "name": "Old house"}]}
BEATS = {"beats": [{"name": "Hook", "tension_target": 6}]}
PLAY = {"title": "Comb", "scenes": [{
    "scene_id": 1, "heading": {"int_ext": "INT", "location_id": "house", "time": "NIGHT"},
    "beat": "Hook", "tension": 7, "characters": ["lan"], "est_duration_sec": 60,
    "elements": [
        {"type": "action", "text": "Lan brushes her hair."},
        {"type": "dialogue", "character": "lan", "emotion": "trembling", "text": "Who's there?"},
        {"type": "vo", "text": "She was not alone."},
    ],
}]}


def scene(**changes):
    return {"title": "Comb", "scenes": [{**PLAY["scenes"][0], **changes}]}


class CheckTest(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(check(CONFIG, PLAY, BIBLE, BEATS), [])

    def test_unknown_ids(self):
        errs = check(CONFIG, scene(characters=["ghost"], heading={"int_ext": "INT", "location_id": "well", "time": "NIGHT"}), BIBLE, BEATS)
        self.assertTrue(any("'well' is not in the bible" in e for e in errs))
        self.assertTrue(any("'ghost' is not in the bible" in e for e in errs))

    def test_tension_off_beat(self):
        self.assertTrue(any("tension" in e for e in check(CONFIG, scene(tension=2), BIBLE, BEATS)))

    def test_duration_off_target(self):
        self.assertTrue(any("15%" in e for e in check(CONFIG, scene(est_duration_sec=80), BIBLE, BEATS)))

    def test_bible_over_caps(self):
        bible = {**BIBLE, "locations": BIBLE["locations"] + [{"id": "well", "name": "Well"}]}
        self.assertTrue(any("max_locations" in e for e in check(CONFIG, PLAY, bible, BEATS)))

    def test_narration_needs_title_not_heading(self):
        cfg = {**CONFIG, "branch": "narration"}
        self.assertEqual(check(cfg, scene(heading=None, title="Intro"), BIBLE, {}), [])
        self.assertTrue(any("title" in e for e in check(cfg, scene(heading=None), BIBLE, {})))


class RenderTest(unittest.TestCase):
    def test_screenplay_layout(self):
        txt = screenplay_txt(CONFIG, PLAY, BIBLE)
        self.assertIn("SCENE 1. INT. OLD HOUSE - NIGHT", txt)
        self.assertIn(" " * 20 + "LAN\n" + " " * 10 + "(trembling)\n" + " " * 5 + "Who's there?", txt)
        self.assertIn(" " * 20 + "NARRATOR (V.O.)", txt)

    def test_narration_is_vo_only(self):
        md = narration_md(scene(title="The mirror"))
        self.assertIn("## ch01 - The mirror (~60 s, 4 words)", md)
        self.assertIn("She was not alone.", md)
        self.assertNotIn("brushes", md)

    def test_render_writes_files(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)
            (v / "02-adaptation").mkdir()
            (v / "03-script").mkdir()
            (v / "config.json").write_text(json.dumps({**CONFIG, "branch": "narration"}))
            (v / "02-adaptation/bible.json").write_text(json.dumps(BIBLE))
            (v / "03-script/screenplay.json").write_text(json.dumps(scene(heading=None, title="Intro")))
            names = [p.name for p in render(v)]
            self.assertEqual(names, ["screenplay.txt", "script.en.md"])


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(screenplay))
    return tests


if __name__ == "__main__":
    unittest.main()
