# -*- coding: utf-8 -*-
"""题库数据完整性回归测试"""

import re
import unittest

from data import (
    ALL_QUESTIONS,
    SINGLE_CHOICE_QUESTIONS,
    MULTI_CHOICE_QUESTIONS,
    DOMAINS,
    QUESTION_BY_ID,
    get_domain_question_count,
)
from data import shuffle_question_options

OFFICIAL_DOMAINS = set(DOMAINS)
REQUIRED_FIELDS = {"id", "question", "options", "correct_answers", "explanation", "domain"}
_CN_SELECT_COUNT = {
    "一": 1, "两": 2, "二": 2, "三": 3, "四": 4, "五": 5,
    "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
}


def _parse_select_count(question: str) -> int | None:
    match = re.search(r"选择\s*([一二两三四五六七八九十\d]+)\s*项", question)
    if not match:
        return None
    token = match.group(1)
    if token.isdigit():
        return int(token)
    return _CN_SELECT_COUNT.get(token)


def _normalize_question_stem(question: str) -> str:
    stem = re.sub(r"（选择[^）]+）", "", question.strip())
    return re.sub(r"\s+", "", stem)


class TestQuestionBankIntegrity(unittest.TestCase):
    def test_total_question_count(self):
        self.assertEqual(len(SINGLE_CHOICE_QUESTIONS), 181)
        self.assertEqual(len(MULTI_CHOICE_QUESTIONS), 165)
        self.assertEqual(len(ALL_QUESTIONS), 346)

    def test_all_questions_have_required_fields(self):
        for q in ALL_QUESTIONS:
            missing = REQUIRED_FIELDS - set(q.keys())
            self.assertEqual(missing, set(), f"{q.get('id', '?')} missing {missing}")

    def test_question_ids_are_unique(self):
        ids = [q["id"] for q in ALL_QUESTIONS]
        self.assertEqual(len(ids), len(set(ids)), "duplicate question IDs found")

    def test_question_by_id_map_is_complete(self):
        self.assertEqual(len(QUESTION_BY_ID), len(ALL_QUESTIONS))
        for q in ALL_QUESTIONS:
            self.assertIs(QUESTION_BY_ID[q["id"]], q)

    def test_single_choice_classification(self):
        for q in SINGLE_CHOICE_QUESTIONS:
            self.assertEqual(
                len(q["correct_answers"]),
                1,
                f"{q['id']} in single_choice has {len(q['correct_answers'])} answers",
            )

    def test_weak_point_practice_questions_exist(self):
        for n in range(140, 166):
            qid = f"M{n}"
            self.assertIn(qid, QUESTION_BY_ID, qid)
            q = QUESTION_BY_ID[qid]
            self.assertGreaterEqual(len(q["correct_answers"]), 2, qid)

    def test_multi_choice_classification(self):
        for q in MULTI_CHOICE_QUESTIONS:
            self.assertGreaterEqual(
                len(q["correct_answers"]),
                2,
                f"{q['id']} in multi_choice has only {len(q['correct_answers'])} answer(s)",
            )

    def test_domains_are_official(self):
        for q in ALL_QUESTIONS:
            self.assertIn(q["domain"], OFFICIAL_DOMAINS, f"{q['id']} has invalid domain")

    def test_domain_counts_sum_to_total(self):
        total = sum(get_domain_question_count(d) for d in DOMAINS)
        self.assertEqual(total, len(ALL_QUESTIONS))

    def test_options_count_matches_answers(self):
        for q in ALL_QUESTIONS:
            options = q["options"]
            self.assertGreaterEqual(len(options), 4, f"{q['id']} has fewer than 4 options")
            for ans in q["correct_answers"]:
                self.assertIn(ans, {"A", "B", "C", "D", "E"}, f"{q['id']} invalid answer {ans}")

    def test_id_format(self):
        for q in SINGLE_CHOICE_QUESTIONS:
            self.assertRegex(q["id"], r"^S\d+$", f"bad single id: {q['id']}")
        for q in MULTI_CHOICE_QUESTIONS:
            self.assertRegex(q["id"], r"^M\d+$", f"bad multi id: {q['id']}")

    def test_explanations_are_non_empty(self):
        for q in ALL_QUESTIONS:
            self.assertTrue(q["explanation"].strip(), f"{q['id']} has empty explanation")

    def test_multi_wrong_analysis_never_uses_correct_letter(self):
        from gui.explanation_formatter import parse_explanation

        quote_re = re.compile(r"^「([A-E])\.\s*([^」]*)」")
        problems = []
        for q in MULTI_CHOICE_QUESTIONS:
            correct = set(q.get("correct_answers") or [])
            bodies = {}
            for opt in q.get("options") or []:
                m = re.match(r"^([A-E])\.\s*(.+)$", (opt or "").strip())
                if m:
                    bodies[m.group(1)] = m.group(2).strip()
            sec = parse_explanation(
                q.get("explanation") or "",
                options=q.get("options"),
                correct_answers=q.get("correct_answers"),
                question_text=q.get("question") or "",
            )
            covered = set()
            for block in sec.wrong_options:
                m = quote_re.match((block or "").strip())
                if not m:
                    continue
                letter, quoted = m.group(1), m.group(2).strip()
                if letter in correct:
                    problems.append(f"{q['id']}: 错误分析引用了正确选项 {letter}")
                    continue
                covered.add(letter)
                actual = bodies.get(letter, "")
                if quoted and actual and quoted[:10] not in actual and actual[:10] not in quoted:
                    problems.append(f"{q['id']}: {letter} 解析标题与选项正文不一致")
            missing = sorted(set(bodies) - correct - covered)
            if missing:
                problems.append(f"{q['id']}: 缺少错误选项 {missing}")
        self.assertEqual(problems, [], problems[:12])

    def test_multi_select_count_matches_correct_answers(self):
        mismatches = []
        for q in MULTI_CHOICE_QUESTIONS:
            expected = _parse_select_count(q["question"])
            actual = len(q["correct_answers"])
            if expected is not None and expected != actual:
                mismatches.append(f"{q['id']}: asks {expected}, answers {actual}")
        self.assertEqual(mismatches, [])

    def test_no_cross_bank_duplicate_stems(self):
        single_stems = {_normalize_question_stem(q["question"]): q["id"] for q in SINGLE_CHOICE_QUESTIONS}
        duplicates = []
        for q in MULTI_CHOICE_QUESTIONS:
            stem = _normalize_question_stem(q["question"])
            if stem in single_stems:
                duplicates.append((single_stems[stem], q["id"]))
        self.assertEqual(duplicates, [])


class TestShuffleQuestionOptions(unittest.TestCase):
    def test_shuffle_preserves_correctness_mapping(self):
        q = ALL_QUESTIONS[0]
        info = shuffle_question_options(q)
        self.assertEqual(len(info["shuffled_options"]), len(q["options"]))
        for display_letter in info["display_correct_answers"]:
            original = info["display_to_original"][display_letter]
            self.assertIn(original, q["correct_answers"])

    def test_shuffle_roundtrip(self):
        q = MULTI_CHOICE_QUESTIONS[0]
        info = shuffle_question_options(q)
        for orig, display in info["original_to_display"].items():
            self.assertEqual(info["display_to_original"][display], orig)


if __name__ == "__main__":
    unittest.main()