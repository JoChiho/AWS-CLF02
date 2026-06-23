# -*- coding: utf-8 -*-
"""自定义练习抽题逻辑测试"""

import unittest
from unittest.mock import patch

from data import ALL_QUESTIONS, SINGLE_CHOICE_QUESTIONS
from data.custom_practice import (
    FILTER_ALL,
    FILTER_LOW_ACCURACY,
    FILTER_NEVER,
    SCOPE_ALL,
    SCOPE_SINGLE,
    get_practice_pool,
    select_custom_practice_questions,
)


class TestCustomPractice(unittest.TestCase):
    def setUp(self):
        self.stats = {
            "S01": {"correct_count": 3, "wrong_count": 1},
            "S02": {"correct_count": 1, "wrong_count": 4},
            "M01": {"correct_count": 0, "wrong_count": 2},
        }

    def test_pool_scope_single(self):
        pool = get_practice_pool(scope=SCOPE_SINGLE, stats=self.stats)
        self.assertEqual(len(pool), len(SINGLE_CHOICE_QUESTIONS))
        self.assertTrue(all(q["id"].startswith("S") for q in pool))

    def test_filter_never(self):
        pool = get_practice_pool(
            scope=SCOPE_ALL,
            filter_mode=FILTER_NEVER,
            stats=self.stats,
        )
        ids = {q["id"] for q in pool}
        self.assertNotIn("S01", ids)
        self.assertNotIn("S02", ids)
        self.assertNotIn("M01", ids)
        self.assertEqual(len(pool), len(ALL_QUESTIONS) - 3)

    def test_filter_low_accuracy(self):
        pool = get_practice_pool(
            scope=SCOPE_ALL,
            filter_mode=FILTER_LOW_ACCURACY,
            accuracy_threshold=70.0,
            stats=self.stats,
        )
        ids = {q["id"] for q in pool}
        self.assertIn("S02", ids)  # 20%
        self.assertIn("M01", ids)  # 0%
        self.assertNotIn("S01", ids)  # 75%

    def test_select_respects_count(self):
        result = select_custom_practice_questions(
            count=10,
            scope=SCOPE_ALL,
            filter_mode=FILTER_ALL,
        )
        self.assertEqual(result.actual_count, 10)
        self.assertEqual(len(result.questions), 10)
        self.assertIn("custom:n=10", result.mode)

    @patch("data.custom_practice.get_all_question_stats")
    def test_select_caps_when_pool_smaller(self, mock_stats):
        mock_stats.return_value = {"S01": {"correct_count": 1, "wrong_count": 0}}
        pool = get_practice_pool(
            scope=SCOPE_SINGLE,
            filter_mode=FILTER_NEVER,
            stats=mock_stats.return_value,
        )
        self.assertEqual(len(pool), len(SINGLE_CHOICE_QUESTIONS) - 1)

        result = select_custom_practice_questions(
            count=200,
            scope=SCOPE_SINGLE,
            filter_mode=FILTER_NEVER,
        )
        self.assertEqual(result.pool_size, len(SINGLE_CHOICE_QUESTIONS) - 1)
        self.assertEqual(result.actual_count, result.pool_size)


if __name__ == "__main__":
    unittest.main()