# -*- coding: utf-8 -*-
"""模拟考试抽题与计分回归测试"""

import unittest

from data import DOMAINS
from data.mock_exam import (
    allocate_domain_counts,
    select_mock_exam_questions,
    score_mock_exam,
    raw_percent_to_scaled_score,
    MOCK_EXAM_QUESTION_COUNT,
    AWS_SCALED_PASS_SCORE,
    AWS_SCALED_SCORE_MIN,
    AWS_SCALED_SCORE_MAX,
)


class TestMockExamSelection(unittest.TestCase):
    def test_allocate_domain_counts_sums_to_65(self):
        counts = allocate_domain_counts(65)
        self.assertEqual(sum(counts.values()), 65)
        for domain in DOMAINS:
            self.assertIn(domain, counts)
            self.assertGreater(counts[domain], 0)

    def test_allocate_matches_official_weights_approximately(self):
        counts = allocate_domain_counts(65)
        self.assertEqual(counts["Technology and Services"], 22)
        self.assertEqual(counts["Security and Compliance"], 19)
        self.assertEqual(counts["Cloud Concepts"], 16)
        self.assertEqual(counts["Billing, Pricing, and Support"], 8)

    def test_select_returns_65_unique_questions(self):
        questions = select_mock_exam_questions()
        self.assertEqual(len(questions), MOCK_EXAM_QUESTION_COUNT)
        ids = [q["id"] for q in questions]
        self.assertEqual(len(ids), len(set(ids)))

    def test_select_domain_distribution(self):
        questions = select_mock_exam_questions()
        expected = allocate_domain_counts(65)
        actual = {d: 0 for d in DOMAINS}
        for q in questions:
            actual[q["domain"]] += 1
        self.assertEqual(actual, expected)


class TestMockExamScoring(unittest.TestCase):
    def _sample_questions(self, n=3):
        return select_mock_exam_questions()[:n]

    def test_pass_at_70_percent(self):
        questions = self._sample_questions(10)
        answers = {i: q["correct_answers"][:] for i, q in enumerate(questions)}
        # 7 correct out of 10
        for i in range(7, 10):
            answers[i] = ["Z"]  # wrong if Z not in correct

        # simpler: 7 correct, 3 empty
        answers = {i: questions[i]["correct_answers"][:] for i in range(7)}
        result = score_mock_exam(questions, answers)
        self.assertEqual(result["correct_count"], 7)
        self.assertEqual(result["percentage"], 70.0)
        self.assertEqual(result["scaled_score"], AWS_SCALED_PASS_SCORE)
        self.assertTrue(result["passed"])

    def test_fail_below_pass_line(self):
        questions = self._sample_questions(10)
        answers = {i: questions[i]["correct_answers"][:] for i in range(6)}
        result = score_mock_exam(questions, answers)
        self.assertEqual(result["correct_count"], 6)
        self.assertEqual(result["percentage"], 60.0)
        self.assertLess(result["scaled_score"], AWS_SCALED_PASS_SCORE)
        self.assertFalse(result["passed"])

    def test_unanswered_counts_as_wrong(self):
        questions = self._sample_questions(2)
        answers = {0: questions[0]["correct_answers"][:]}
        result = score_mock_exam(questions, answers)
        self.assertEqual(result["correct_count"], 1)
        self.assertEqual(result["answered_count"], 1)
        self.assertEqual(len(result["wrong_items"]), 1)
        self.assertTrue(result["wrong_items"][0].get("unanswered"))


class TestAwsScaledScore(unittest.TestCase):
    def test_scale_anchors(self):
        self.assertEqual(raw_percent_to_scaled_score(0), AWS_SCALED_SCORE_MIN)
        self.assertEqual(raw_percent_to_scaled_score(70), AWS_SCALED_PASS_SCORE)
        self.assertEqual(raw_percent_to_scaled_score(100), AWS_SCALED_SCORE_MAX)

    def test_just_below_and_above_pass(self):
        self.assertLess(raw_percent_to_scaled_score(69), AWS_SCALED_PASS_SCORE)
        self.assertGreater(raw_percent_to_scaled_score(71), AWS_SCALED_PASS_SCORE)

    def test_clamps_out_of_range(self):
        self.assertEqual(raw_percent_to_scaled_score(-10), AWS_SCALED_SCORE_MIN)
        self.assertEqual(raw_percent_to_scaled_score(140), AWS_SCALED_SCORE_MAX)


if __name__ == "__main__":
    unittest.main()