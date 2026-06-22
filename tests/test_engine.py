# -*- coding: utf-8 -*-
"""CLI 引擎与持久化对接回归测试"""

import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import data.progress as progress
from core.engine import persist_round_result
from data import SINGLE_CHOICE_QUESTIONS


class TestPersistRoundResult(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.progress_file = Path(self._tmpdir.name) / "user_data.json"
        self._patch = patch.object(progress, "PROGRESS_FILE", self.progress_file)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        self._tmpdir.cleanup()

    def test_persist_records_session_and_question_stats(self):
        questions = SINGLE_CHOICE_QUESTIONS[:3]
        answers = {
            0: ["A"],
            1: ["B"],
            2: questions[2]["correct_answers"][:],
        }

        result = persist_round_result("cli:all", questions, answers, time.time())

        self.assertTrue(result["saved"])
        self.assertEqual(result["answered_count"], 3)
        self.assertEqual(result["correct_count"], 1)

        sessions = progress.get_recent_sessions(1)
        self.assertEqual(sessions[0]["mode"], "cli:all")
        self.assertEqual(sessions[0]["answered"], 3)
        self.assertEqual(sessions[0]["correct"], 1)

        qid = questions[2]["id"]
        stat = progress.get_question_stats(qid)
        self.assertEqual(stat["correct_count"], 1)

    def test_persist_skips_unanswered_questions(self):
        questions = SINGLE_CHOICE_QUESTIONS[:2]
        answers = {0: questions[0]["correct_answers"][:]}

        result = persist_round_result("cli:all", questions, answers, time.time())

        self.assertEqual(result["answered_count"], 1)
        self.assertEqual(result["correct_count"], 1)
        self.assertAlmostEqual(result["percentage"], 100.0)


if __name__ == "__main__":
    unittest.main()