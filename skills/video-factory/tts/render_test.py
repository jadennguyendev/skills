"""Checks render.py's plan validation and assembly without loading any model.

    "$(uv tool dir)/mlx-audio/bin/python" render_test.py
"""

import doctest
import unittest

import numpy as np

import render
from render import SR, assemble, rms, validate

PLAN = {
    "narrator": {"voice": "Ryan"},
    "characters": {"demon": {"ref_audio": "voices/demon.wav"}},
    "segments": [
        {"text": "The house was empty."},
        {"speaker": "demon", "text": "Get out!", "exaggeration": 1.0, "pause_after": 1.0},
        {"text": "She ran."},
    ],
}


class RenderTest(unittest.TestCase):
    def test_valid_plan(self):
        self.assertEqual(validate(PLAN), [])

    def test_exaggeration_out_of_range(self):
        plan = {**PLAN, "segments": [{"speaker": "demon", "text": "No.", "exaggeration": 3}]}
        self.assertEqual(validate(plan), ["segment 1: exaggeration must be 0.25-2.0"])

    def test_assemble_timeline_and_loudness(self):
        narration = np.full(SR, 0.1, dtype=np.float32)
        loud = np.full(SR // 2, 0.5, dtype=np.float32)
        audio, timeline = assemble(PLAN, [narration, loud, narration])

        self.assertEqual([(s["start"], s["end"]) for s in timeline],
                         [(0.0, 1.0), (1.35, 1.85), (2.85, 3.85)])
        self.assertEqual(timeline[1]["speaker"], "demon")
        self.assertEqual(len(audio), round(3.85 * SR))
        demon = audio[round(1.35 * SR):round(1.85 * SR)]
        self.assertAlmostEqual(rms(demon), 0.1, places=4)


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(render))
    return tests


if __name__ == "__main__":
    unittest.main()
