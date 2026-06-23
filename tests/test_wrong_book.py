# -*- coding: utf-8 -*-
"""错题本增强功能回归测试"""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import data.progress as progress
from data.progress import (
    MASTER_STREAK_REQUIRED,
    get_wrong_book_entries,
    set_question_mastered,
)


class TestWrongBookEnhancements(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.progress_file = Path(self._tmpdir.name) / "user_data.json"
        self._patch = patch.object(progress, "PROGRESS_FILE", self.progress_file)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        self._tmpdir.cleanup()

    def test_auto_master_after_consecutive_correct(self):
        progress.update_question_stat("S01", False, ["B"])
        progress.update_question_stat("S01", True, ["A"])
        stat = progress.get_question_stats("S01")
        self.assertFalse(stat["mastered"])

        progress.update_question_stat("S01", True, ["A"])
        stat = progress.get_question_stats("S01")
        self.assertTrue(stat["mastered"])
        self.assertEqual(stat["consecutive_correct"], MASTER_STREAK_REQUIRED)

    def test_wrong_resets_mastered_streak(self):
        progress.update_question_stat("S02", False, ["B"])
        for _ in range(MASTER_STREAK_REQUIRED):
            progress.update_question_stat("S02", True, ["A"])
        self.assertTrue(progress.get_question_stats("S02")["mastered"])

        progress.update_question_stat("S02", False, ["C"])
        stat = progress.get_question_stats("S02")
        self.assertFalse(stat["mastered"])
        self.assertEqual(stat["consecutive_correct"], 0)

    def test_mastered_hidden_by_default(self):
        progress.update_question_stat("S03", False, ["B"])
        set_question_mastered("S03", True)
        entries = get_wrong_book_entries()
        self.assertEqual([e["id"] for e in entries], [])

        entries_with = get_wrong_book_entries(include_mastered=True)
        self.assertEqual(len(entries_with), 1)
        self.assertTrue(entries_with[0]["mastered"])

    def test_domain_filter(self):
        progress.update_question_stat("S01", False, ["B"])
        progress.update_question_stat("M01", False, ["A"])

        cloud_entries = get_wrong_book_entries(domain="Cloud Concepts")
        ids = {e["id"] for e in cloud_entries}
        self.assertTrue(ids.issubset({"S01", "M01"}))
        self.assertGreaterEqual(len(cloud_entries), 1)

    def test_manual_unmaster(self):
        progress.update_question_stat("S04", False, ["B"])
        set_question_mastered("S04", True)
        set_question_mastered("S04", False)
        entries = get_wrong_book_entries()
        self.assertEqual(len(entries), 1)
        self.assertFalse(entries[0]["mastered"])


if __name__ == "__main__":
    unittest.main()