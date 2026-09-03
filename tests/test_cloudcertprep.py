# -*- coding: utf-8 -*-
"""CloudCertPrep 题库与进度隔离回归测试"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import data.progress as progress
from data.banks import BANK_CLOUDCERTPREP, BANK_NATIVE, get_bank
from data.cloudcertprep.domains import DOMAINS, MOCK_EXAM_DOMAIN_WEIGHTS


class TestCloudCertPrepBank(unittest.TestCase):
    def setUp(self):
        self.bank = get_bank(BANK_CLOUDCERTPREP)

    def test_bank_has_questions_when_imported(self):
        total = len(self.bank.ALL_QUESTIONS)
        self.assertGreaterEqual(
            total,
            50,
            "请先运行 tools/import_cloudcertprep.py 生成题库",
        )
        if total >= 1000:
            self.assertEqual(total, 1050)
            self.assertEqual(len(self.bank.SINGLE_CHOICE_QUESTIONS), 829)
            self.assertEqual(len(self.bank.MULTI_CHOICE_QUESTIONS), 221)

    def test_question_ids_use_ccp_prefix(self):
        for q in self.bank.ALL_QUESTIONS[:20]:
            self.assertRegex(q["id"], r"^CCP-[SM]\d+$")

    def test_questions_have_required_fields(self):
        required = {
            "id", "question", "options", "correct_answers",
            "explanation", "domain", "source",
        }
        for q in self.bank.ALL_QUESTIONS[:30]:
            missing = required - set(q.keys())
            self.assertEqual(missing, set(), f"{q['id']} missing {missing}")

    def test_single_vs_multi_classification(self):
        for q in self.bank.SINGLE_CHOICE_QUESTIONS[:20]:
            self.assertEqual(len(q["correct_answers"]), 1)
            self.assertFalse(q.get("is_multi", False))
        for q in self.bank.MULTI_CHOICE_QUESTIONS[:20]:
            self.assertGreaterEqual(len(q["correct_answers"]), 2)
            self.assertTrue(q.get("is_multi", True))

    def test_domains_are_official(self):
        for q in self.bank.ALL_QUESTIONS[:50]:
            self.assertIn(q["domain"], DOMAINS)

    def test_not_mixed_with_native_bank(self):
        native = get_bank(BANK_NATIVE)
        native_ids = {q["id"] for q in native.ALL_QUESTIONS}
        ccp_ids = {q["id"] for q in self.bank.ALL_QUESTIONS}
        self.assertEqual(native_ids & ccp_ids, set())

    def test_mock_exam_weights(self):
        self.assertEqual(sum(MOCK_EXAM_DOMAIN_WEIGHTS.values()), 100)

    def test_multi_wrong_analysis_never_uses_correct_letter(self):
        import re
        from gui.explanation_formatter import parse_explanation

        quote_re = re.compile(r"^「([A-E])\.\s*([^」]*)」")
        problems = []
        for q in self.bank.MULTI_CHOICE_QUESTIONS:
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
                    problems.append(
                        f"{q['id']}: {letter} 解析标题与选项正文不一致"
                    )
            missing = sorted(set(bodies) - correct - covered)
            if missing:
                problems.append(f"{q['id']}: 缺少错误选项 {missing}")
        self.assertEqual(problems, [], problems[:12])


class TestCloudCertPrepProgressIsolation(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.progress_file = Path(self._tmpdir.name) / "user_data.json"
        self._patch = patch.object(progress, "PROGRESS_FILE", self.progress_file)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        self._tmpdir.cleanup()

    def test_native_and_cloudcertprep_stats_are_isolated(self):
        progress.update_question_stat("S01", True, ["A"], bank_id=BANK_NATIVE)
        progress.update_question_stat("CCP-S001", False, ["B"], bank_id=BANK_CLOUDCERTPREP)

        native_stats = progress.get_all_question_stats(bank_id=BANK_NATIVE)
        ccp_stats = progress.get_all_question_stats(bank_id=BANK_CLOUDCERTPREP)

        self.assertIn("S01", native_stats)
        self.assertNotIn("CCP-S001", native_stats)
        self.assertIn("CCP-S001", ccp_stats)
        self.assertNotIn("S01", ccp_stats)

    def test_sessions_stored_under_cloudcertprep_key(self):
        progress.record_session("single", 10, 8, bank_id=BANK_CLOUDCERTPREP)
        with open(self.progress_file, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data["sessions"]), 0)
        self.assertEqual(len(data["cloudcertprep"]["sessions"]), 1)

    def test_font_scale_per_bank(self):
        progress.set_practice_font_scale(1.2, bank_id=BANK_NATIVE)
        progress.set_practice_font_scale(0.9, bank_id=BANK_CLOUDCERTPREP)
        self.assertEqual(progress.get_practice_font_scale(BANK_NATIVE), 1.2)
        self.assertEqual(progress.get_practice_font_scale(BANK_CLOUDCERTPREP), 0.9)


if __name__ == "__main__":
    unittest.main()