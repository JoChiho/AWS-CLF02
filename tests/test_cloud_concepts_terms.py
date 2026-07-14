# -*- coding: utf-8 -*-
"""Cloud Concepts 术语统一测试"""

import unittest

from data.banks import BANK_CLOUDCERTPREP, get_bank
from data.cloud_concepts_terms import (
    normalize_cloud_concepts_text,
    should_force_cloud_concepts_english,
)


class TestCloudConceptsTerms(unittest.TestCase):
    def test_caf_perspectives_force_english(self):
        for term in ("Business", "People", "Governance", "Platform", "Security", "Operations"):
            self.assertTrue(should_force_cloud_concepts_english(term))

    def test_unify_people_and_business_in_explanation(self):
        text = normalize_cloud_concepts_text(
            "「C. 人们」是错误的：人员视角侧重于组织准备情况。"
            "「A. 商业」是错误的：业务角度侧重于业务成果。",
            in_caf_context=True,
        )
        self.assertIn("People", text)
        self.assertNotIn("人们", text)
        self.assertIn("Business", text)
        self.assertIn("业务视角", text)

    def test_caf_multi_question_options(self):
        bank = get_bank(BANK_CLOUDCERTPREP)
        q = next(x for x in bank.ALL_QUESTIONS if x.get("source_id") == "q1060")
        bodies = [o.split(". ", 1)[1] for o in q["options"]]
        self.assertEqual(
            bodies,
            ["Governance", "Financial", "People", "Infrastructure", "Agility"],
        )
        self.assertIn("人员", q["explanation"])
        self.assertNotIn("人们", q["explanation"])


if __name__ == "__main__":
    unittest.main()