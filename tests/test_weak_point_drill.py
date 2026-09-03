# -*- coding: utf-8 -*-
"""薄弱点突击题库回归测试"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import data.progress as progress
from data.banks import (
    BANK_CLOUDCERTPREP,
    BANK_CONCEPT_DRILL,
    BANK_KEYWORD_DRILL,
    BANK_NATIVE,
    BANK_WEAK_POINT_DRILL,
    get_bank,
    get_bank_label,
)


class TestWeakPointDrillBank(unittest.TestCase):
    def setUp(self):
        self.bank = get_bank(BANK_WEAK_POINT_DRILL)

    def test_bank_label(self):
        self.assertEqual(get_bank_label(BANK_WEAK_POINT_DRILL), "薄弱点突击")

    def test_question_count_and_ids(self):
        questions = self.bank.ALL_QUESTIONS
        self.assertGreaterEqual(len(questions), 20)
        self.assertGreaterEqual(len(self.bank.MULTI_CHOICE_QUESTIONS), 3)
        ids = [q["id"] for q in questions]
        self.assertEqual(len(ids), len(set(ids)))
        for q in questions:
            if q.get("is_multi"):
                self.assertRegex(q["id"], r"^WP-M\d{3}$")
            else:
                self.assertRegex(q["id"], r"^WP-S\d{3}$")

    def test_each_question_shape(self):
        for q in self.bank.ALL_QUESTIONS:
            opts = q["options"]
            self.assertGreaterEqual(len(opts), 4, q["id"])
            self.assertTrue(q["question"].strip(), q["id"])
            self.assertTrue(q["explanation"].strip(), q["id"])
            self.assertTrue(q.get("topic"), q["id"])
            self.assertIn(q["domain"], self.bank.DOMAINS)
            self.assertIn("重点考点", q["explanation"])
            bodies = [o.split(". ", 1)[1] for o in opts]
            self.assertEqual(len(bodies), len(set(bodies)), q["id"])
            letters = [o[0] for o in opts]
            for ans in q["correct_answers"]:
                self.assertIn(ans, letters)
            if q.get("is_multi"):
                self.assertGreaterEqual(len(q["correct_answers"]), 2)
            else:
                self.assertEqual(len(q["correct_answers"]), 1)

    def test_covers_required_topics(self):
        topics = {q["topic"] for q in self.bank.ALL_QUESTIONS}
        required = {
            "AWS Direct Connect",
            "AWS Service Catalog",
            "AWS Audit Manager",
            "Amazon Inspector",
            "AWS Config",
            "Amazon Inspector / AWS Config",
            "AWS 专业服务",
            "AWS 合作伙伴网络",
            "迁移评估",
            "AWS Compute Optimizer",
            "性能效率",
        }
        missing = required - topics
        self.assertFalse(missing, missing)

    def test_isolated_from_other_banks(self):
        others = [
            get_bank(BANK_NATIVE),
            get_bank(BANK_CLOUDCERTPREP),
            get_bank(BANK_KEYWORD_DRILL),
            get_bank(BANK_CONCEPT_DRILL),
        ]
        wp_ids = {q["id"] for q in self.bank.ALL_QUESTIONS}
        for other in others:
            self.assertFalse(wp_ids & {q["id"] for q in other.ALL_QUESTIONS})

    def test_domain_counts_sum_to_total(self):
        counted = sum(self.bank.get_domain_question_count(d) for d in self.bank.DOMAINS)
        self.assertEqual(counted, len(self.bank.ALL_QUESTIONS))

    def test_not_clones_of_source_stems(self):
        forbidden = [
            "哪些 AWS 服务或功能需要互联网服务提供商",
            "AWS Service Catalog 提供什么",
            "哪项 AWS 服务通过自动收集 AWS 使用和活动的证据",
        ]
        stems = " ".join(q["question"] for q in self.bank.ALL_QUESTIONS)
        for text in forbidden:
            self.assertNotIn(text, stems)


class TestWeakPointProgressIsolation(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.progress_file = Path(self._tmpdir.name) / "user_data.json"
        self._patch = patch.object(progress, "PROGRESS_FILE", self.progress_file)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        self._tmpdir.cleanup()

    def test_stats_isolated(self):
        progress.update_question_stat("S01", True, ["A"], bank_id=BANK_NATIVE)
        progress.update_question_stat("WP-S001", False, ["B"], bank_id=BANK_WEAK_POINT_DRILL)
        wp = progress.get_all_question_stats(bank_id=BANK_WEAK_POINT_DRILL)
        native = progress.get_all_question_stats(bank_id=BANK_NATIVE)
        self.assertIn("WP-S001", wp)
        self.assertNotIn("WP-S001", native)
        self.assertNotIn("S01", wp)

    def test_sessions_use_weak_point_key(self):
        progress.record_session("weak_point_drill:all", 10, 8, bank_id=BANK_WEAK_POINT_DRILL)
        with open(self.progress_file, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data["sessions"]), 0)
        self.assertEqual(len(data["weak_point_drill"]["sessions"]), 1)


if __name__ == "__main__":
    unittest.main()
