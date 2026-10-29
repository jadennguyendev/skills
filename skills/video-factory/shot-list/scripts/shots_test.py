"""Checks shots.py's prompt assembly and shot list checks.

    python3 shots_test.py
"""

import doctest
import json
import tempfile
import unittest
from pathlib import Path

import shots
from shots import build, check, prompts

CONFIG = {"production_tool": "none", "max_clip_sec": 8}
BIBLE = {
    "style_guide": {"prefix_en": "Cinematic horror film still.", "atmosphere_en": "Eerie, quiet.", "negative_en": "cartoon"},
    "characters": [{"id": "lan", "visual_en": "A Vietnamese woman in her early 20s, long black hair"}],
    "locations": [{"id": "house", "description_en": "Old wooden house, dark pillars"}],
    "entity": {"stages": {"shadow": {"visual_en": "a faint long-haired figure in the mirror"}}},
}
PLAY = {"scenes": [{
    "scene_id": 5, "heading": {"int_ext": "INT", "location_id": "house", "time": "NIGHT"}, "est_duration_sec": 10,
    "elements": [
        {"type": "action", "text": "Lan brushes her hair."},
        {"type": "sound", "text": "A lullaby."},
        {"type": "dialogue", "character": "lan", "text": "Who's there?"},
    ],
}]}
WIDE = {"shot_id": "5A", "scene_id": 5, "order": 1, "location_id": "house", "characters": ["lan"],
        "script_elements": [0], "duration_sec": 6, "shot_size": "WS", "angle": "eye level", "entity_stage": "none"}
FACE = {"shot_id": "5B", "scene_id": 5, "order": 2, "location_id": "house", "characters": ["lan"],
        "script_elements": [2], "duration_sec": 4, "shot_size": "CU", "angle": "eye level", "needs_lipsync": True}


class CheckTest(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(check(CONFIG, PLAY, BIBLE, {"shots": [WIDE, FACE]}), [])

    def test_uncovered_element_and_short_total(self):
        errs = check(CONFIG, PLAY, BIBLE, {"shots": [WIDE]})
        self.assertIn("scene 5: element 2 (dialogue) has no shot", errs)
        self.assertTrue(any("over 10% off" in e for e in errs))

    def test_lipsync_required_on_visible_speaker(self):
        errs = check(CONFIG, PLAY, BIBLE, {"shots": [WIDE, {**FACE, "needs_lipsync": False}]})
        self.assertTrue(any("needs_lipsync" in e for e in errs))

    def test_limits(self):
        errs = check(CONFIG, PLAY, BIBLE, {"shots": [{**WIDE, "duration_sec": 9, "entity_stage": "full"}, FACE]})
        self.assertTrue(any("max_clip_sec" in e for e in errs))
        self.assertTrue(any("entity_stage 'full'" in e for e in errs))

    def test_repeated_framing(self):
        errs = check(CONFIG, PLAY, BIBLE, {"shots": [WIDE, {**FACE, "shot_size": "WS"}]})
        self.assertTrue(any("back to back" in e for e in errs))


class PromptTest(unittest.TestCase):
    def test_formula_copies_bible_verbatim(self):
        shot = {**WIDE, "shot_size": "MCU", "lens": "50mm", "subject_action": "brushing her hair",
                "entity_stage": "shadow", "camera_move": "slow dolly in", "motion_note": "the candle flickers"}
        image, negative, motion, refs = prompts(shot, BIBLE)
        self.assertEqual(image, "Cinematic horror film still. Medium close-up, eye level, 50mm. "
                                "A Vietnamese woman in her early 20s, long black hair, brushing her hair. "
                                "Old wooden house, dark pillars. A faint long-haired figure in the mirror. Eerie, quiet.")
        self.assertEqual((negative, motion), ("cartoon", "Slow dolly in. The candle flickers."))
        self.assertEqual(refs, {"characters": ["refs/char_lan.png"], "location": "refs/loc_house.png",
                                "entity": "refs/entity_shadow.png"})

    def test_build_only_prompts_for_ai_gen(self):
        for tool, has_prompt in (("none", False), ("ai-gen", True)):
            with tempfile.TemporaryDirectory() as d:
                v = Path(d)
                for rel, obj in (("config.json", {**CONFIG, "production_tool": tool}), ("03-script/screenplay.json", PLAY),
                                 ("02-adaptation/bible.json", BIBLE), ("04-shots/shotlist.json", {"shots": [WIDE, FACE]})):
                    (v / rel).parent.mkdir(exist_ok=True)
                    (v / rel).write_text(json.dumps(obj))
                build(v)
                sheet = json.loads((v / "04-shots/shotlist.json").read_text())
                self.assertEqual("image_prompt" in sheet["shots"][0], has_prompt)
                self.assertTrue((v / "04-shots/shotlist.csv").read_text().startswith("shot_id,"))


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(shots))
    return tests


if __name__ == "__main__":
    unittest.main()
