# -*- coding: utf-8 -*-
"""策略与准则辨识题库回归测试"""

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
    get_bank,
    get_bank_label,
)


class TestConceptDrillBank(unittest.TestCase):
    def setUp(self):
        self.bank = get_bank(BANK_CONCEPT_DRILL)

    def test_bank_label(self):
        self.assertEqual(get_bank_label(BANK_CONCEPT_DRILL), "策略与准则辨识")

    def test_question_count_and_ids(self):
        questions = self.bank.ALL_QUESTIONS
        self.assertGreaterEqual(len(questions), 80)
        self.assertEqual(len(self.bank.MULTI_CHOICE_QUESTIONS), 0)
        ids = [q["id"] for q in questions]
        self.assertEqual(len(ids), len(set(ids)))
        for qid in ids:
            self.assertRegex(qid, r"^CD-S\d{3}$")

    def test_covers_7r_and_caf(self):
        keywords = {q["keyword"] for q in self.bank.ALL_QUESTIONS}
        for name in (
            "Rehost", "Replatform", "Refactor", "Repurchase",
            "Relocate", "Retire", "Retain",
            "Business", "People", "Governance", "Platform",
            "Security", "Operations",
            "Envision", "Align", "Launch", "Scale",
            "RTO", "RPO", "Pilot Light", "Warm Standby",
        ):
            self.assertIn(name, keywords, name)

    def test_each_question_is_single_choice_definition(self):
        letters = set("ABCD")
        for q in self.bank.ALL_QUESTIONS:
            opts = q["options"]
            self.assertEqual(len(opts), 4, q["id"])
            self.assertFalse(q.get("is_multi"))
            self.assertEqual(len(q["correct_answers"]), 1)
            self.assertIn(q["correct_answers"][0], letters)
            bodies = [o.split(". ", 1)[1] for o in opts]
            self.assertEqual(len(bodies), len(set(bodies)), q["id"])
            self.assertTrue(q["question"].strip())
            self.assertTrue(q["explanation"].strip())
            self.assertTrue(q.get("keyword"))
            self.assertIn(q["domain"], self.bank.DOMAINS)

    def test_isolated_from_other_banks(self):
        native = get_bank(BANK_NATIVE)
        ccp = get_bank(BANK_CLOUDCERTPREP)
        kd = get_bank(BANK_KEYWORD_DRILL)
        ids = {q["id"] for q in self.bank.ALL_QUESTIONS}
        self.assertFalse(ids & {q["id"] for q in native.ALL_QUESTIONS})
        self.assertFalse(ids & {q["id"] for q in ccp.ALL_QUESTIONS})
        self.assertFalse(ids & {q["id"] for q in kd.ALL_QUESTIONS})

    def test_domain_counts_sum_to_total(self):
        counted = sum(self.bank.get_domain_question_count(d) for d in self.bank.DOMAINS)
        self.assertEqual(counted, len(self.bank.ALL_QUESTIONS))

    def test_shuffle_preserves_correct_answer(self):
        q = self.bank.ALL_QUESTIONS[0]
        info = self.bank.shuffle_question_options(q)
        orig_letter = q["correct_answers"][0]
        orig_body = q["options"][ord(orig_letter) - ord("A")].split(". ", 1)[1]
        display_letter = info["display_correct_answers"][0]
        display_body = info["shuffled_options"][ord(display_letter) - ord("A")].split(". ", 1)[1]
        self.assertEqual(orig_body, display_body)


class TestConceptDrillProgressIsolation(unittest.TestCase):
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
        progress.update_question_stat("KD-S001", True, ["A"], bank_id=BANK_KEYWORD_DRILL)
        progress.update_question_stat("CD-S001", False, ["B"], bank_id=BANK_CONCEPT_DRILL)

        cd = progress.get_all_question_stats(bank_id=BANK_CONCEPT_DRILL)
        self.assertIn("CD-S001", cd)
        self.assertNotIn("CD-S001", progress.get_all_question_stats(bank_id=BANK_NATIVE))
        self.assertNotIn("CD-S001", progress.get_all_question_stats(bank_id=BANK_KEYWORD_DRILL))

    def test_sessions_use_concept_drill_key(self):
        progress.record_session("concept_drill:all", 10, 8, bank_id=BANK_CONCEPT_DRILL)
        with open(self.progress_file, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data["sessions"]), 0)
        self.assertEqual(len(data["concept_drill"]["sessions"]), 1)


if __name__ == "__main__":
    unittest.main()
