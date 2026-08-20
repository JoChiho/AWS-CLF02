# -*- coding: utf-8 -*-
"""用户进度持久化回归测试"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import data.progress as progress


class TestProgressPersistence(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.progress_file = Path(self._tmpdir.name) / "user_data.json"
        self._patch = patch.object(progress, "PROGRESS_FILE", self.progress_file)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        self._tmpdir.cleanup()

    def test_load_returns_default_when_missing(self):
        data = progress.load_progress()
        self.assertEqual(data["version"], 1)
        self.assertEqual(data["sessions"], [])
        self.assertEqual(data["question_stats"], {})
        self.assertEqual(data["preferences"], {})
        self.assertIn("cloudcertprep", data)
        self.assertIn("keyword_drill", data)

    def test_practice_font_scale_persistence(self):
        self.assertEqual(progress.get_practice_font_scale(), 1.0)
        progress.set_practice_font_scale(1.15)
        self.assertEqual(progress.get_practice_font_scale(), 1.15)
        data = progress.load_progress()
        self.assertEqual(data["preferences"]["practice_font_scale"], 1.15)

    def test_record_session_persists_and_trims(self):
        for i in range(12):
            progress.record_session("all", 10, i, duration_sec=60, answered=10)

        data = progress.load_progress()
        self.assertEqual(len(data["sessions"]), 10)
        self.assertEqual(data["sessions"][0]["correct"], 11)

    def test_record_session_accuracy_uses_answered_count(self):
        progress.record_session("single", 50, 8, answered=10)
        session = progress.get_recent_sessions(1)[0]
        self.assertEqual(session["accuracy"], 80.0)
        self.assertEqual(session["answered"], 10)
        self.assertEqual(session["total"], 50)

    def test_update_question_stat_tracks_correct_and_wrong(self):
        progress.update_question_stat("S01", True, ["A"])
        progress.update_question_stat("S01", False, ["B"])
        stat = progress.get_question_stats("S01")
        self.assertEqual(stat["correct_count"], 1)
        self.assertEqual(stat["wrong_count"], 1)
        self.assertEqual(stat["last_answer"], ["B"])

    def test_wrong_question_ids_sorted_by_error_rate(self):
        progress.update_question_stat("S01", True, ["A"])
        progress.update_question_stat("S01", False, ["B"])
        progress.update_question_stat("S01", False, ["C"])
        progress.update_question_stat("M01", False, ["A"])
        progress.update_question_stat("M01", True, ["A", "B"])

        wrong_ids = progress.get_wrong_question_ids()
        self.assertIn("S01", wrong_ids)
        self.assertIn("M01", wrong_ids)
        self.assertEqual(wrong_ids[0], "S01")

    def test_accuracy_trend_no_data(self):
        trend = progress.get_accuracy_trend()
        self.assertEqual(trend["count"], 0)
        self.assertEqual(trend["trend"], "no_data")

    def test_accuracy_trend_with_sessions(self):
        progress.record_session("all", 10, 7, answered=10)
        progress.record_session("all", 10, 9, answered=10)
        trend = progress.get_accuracy_trend()
        self.assertEqual(trend["count"], 2)
        self.assertEqual(trend["latest"], 90.0)
        self.assertIsNotNone(trend["avg"])

    def test_corrupted_file_returns_default(self):
        self.progress_file.write_text("{not valid json", encoding="utf-8")
        data = progress.load_progress()
        self.assertEqual(data["sessions"], [])

    def test_clear_all_progress(self):
        progress.record_session("all", 5, 3)
        self.assertTrue(progress.clear_all_progress())
        self.assertFalse(self.progress_file.exists())


if __name__ == "__main__":
    unittest.main()