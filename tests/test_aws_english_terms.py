# -*- coding: utf-8 -*-
"""AWS 英文术语还原测试"""

import re
import unittest

from data.aws_english_terms import (
    _build_glossary_service_reverse,
    is_english_keyword_only_option,
    option_body_needs_chinese_restore,
    restore_aws_english_terms,
    restore_option,
    restore_question_fields,
    should_force_english_option,
)
from data.banks import BANK_CLOUDCERTPREP, get_bank


class TestAwsEnglishTermsRestore(unittest.TestCase):
    def test_restore_option_embeds_service_name_in_chinese(self):
        self.assertEqual(
            restore_option("B. 通过使用弹性负载均衡器自动扩展您的 AWS 资源"),
            "B. 通过使用 Elastic Load Balancer 自动扩展您的 AWS 资源",
        )
        self.assertEqual(
            restore_option("C. Amazon简单存储服务"),
            "C. Amazon S3",
        )
        self.assertEqual(
            restore_option("D. AWS 弹性豆茎"),
            "D. AWS Elastic Beanstalk",
        )

    def test_pure_service_name_option_stays_english(self):
        self.assertEqual(
            restore_option("C. Elastic Load Balancing"),
            "C. Elastic Load Balancing",
        )
        self.assertEqual(
            restore_option("A. Multi-Factor Authentication"),
            "A. Multi-Factor Authentication",
        )

    def test_semantic_option_needs_chinese_restore(self):
        self.assertTrue(option_body_needs_chinese_restore("implement elasticity"))
        self.assertTrue(
            option_body_needs_chinese_restore(
                "AWS allows you to host your applications in multiple regions",
            ),
        )
        self.assertFalse(option_body_needs_chinese_restore("Elastic Load Balancing"))
        self.assertFalse(option_body_needs_chinese_restore("Amazon S3"))

    def test_restore_mistranslated_amazon_service(self):
        text = "Amazon精确定位是一项客户参与服务"
        restored = restore_aws_english_terms(text)
        self.assertIn("Amazon Pinpoint", restored)
        self.assertNotIn("精确定位", restored)

    def test_restore_explanation_serverless(self):
        text = "Amazon Athena 是一种无服务器查询服务"
        restored = restore_aws_english_terms(text)
        self.assertIn("Serverless interactive query service", restored)
        self.assertNotIn("无服务器查询服务", restored)

    def test_generic_nosql_not_replaced_with_dynamodb(self):
        text = "哪项 AWS 服务是托管 NoSQL 数据库？"
        restored = restore_aws_english_terms(text)
        self.assertIn("NoSQL 数据库", restored)
        self.assertNotIn("Amazon DynamoDB", restored)

    def test_glossary_reverse_skips_generic_concepts(self):
        reverse = dict(_build_glossary_service_reverse())
        self.assertNotIn("NoSQL 数据库", reverse)
        self.assertNotIn("数据仓库", reverse)
        self.assertNotIn("对象存储", reverse)

    def test_deployment_model_and_service_quotas(self):
        self.assertTrue(should_force_english_option("Hybrid"))
        self.assertTrue(should_force_english_option("Mixed"))
        self.assertTrue(should_force_english_option("On-premises"))
        self.assertTrue(should_force_english_option("Service Quotas"))
        self.assertEqual(restore_option("C. 杂交种"), "C. Hybrid")
        self.assertEqual(restore_option("C. 服务配额"), "C. Service Quotas")
        self.assertEqual(
            restore_aws_english_terms("六个 EC2 实例上运行"),
            "六个 Amazon EC2 instances 上运行",
        )

    def test_hybrid_mixed_explanation_not_confused(self):
        expl = restore_aws_english_terms(
            "「B. 混合」是错误的：混合不是公认的云计算部署模型，"
            "并且不会与本地、混合和云一起出现在 AWS 框架中。"
        )
        self.assertIn("Mixed", expl)
        self.assertNotIn("「B. 混合」", expl)

    def test_restore_question_fields_keeps_chinese_semantics(self):
        q = {
            "question": "使用弹性负载均衡器分发流量",
            "options": [
                "A. 实施弹性",
                "B. 通过使用 Elastic Load Balancing 扩展资源",
            ],
            "explanation": "AWS 法门适用于容器",
        }
        restore_question_fields(q)
        self.assertIn("Elastic Load Balancer", q["question"])
        self.assertEqual(q["options"][0], "A. 实施弹性")
        self.assertIn("Elastic Load Balancing", q["options"][1])
        self.assertIn("AWS Fargate", q["explanation"])


class TestCloudCertPrepEnglishTermsInBank(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bank = get_bank(BANK_CLOUDCERTPREP)
        if len(cls.bank.ALL_QUESTIONS) < 1000:
            raise unittest.SkipTest("请先运行 fix_cloudcertprep_english_terms.py")

    def test_no_common_mistranslations_in_options(self):
        bad_fragments = [
            "弹性负载均衡",
            "Amazon简单存储服务",
            "AWS 弹性豆茎",
            "Amazon精确定位",
            "AWS 法门",
            "多重身份验证",
            "杂交种",
            "服务配额",
        ]
        hits = []
        for q in self.bank.ALL_QUESTIONS:
            for opt in q.get("options", []):
                for frag in bad_fragments:
                    if frag in opt:
                        hits.append((q["id"], opt, frag))
        self.assertEqual(hits[:10], [], f"选项仍含误译术语: {hits[:5]}")

    def test_semantic_options_should_be_chinese(self):
        bad = []
        for q in self.bank.ALL_QUESTIONS:
            for opt in q.get("options", []):
                body = opt.split(". ", 1)[-1] if ". " in opt else opt
                if option_body_needs_chinese_restore(body):
                    bad.append((q["id"], opt[:70]))
        self.assertEqual(bad, [], f"语意选项仍为整段英文: {bad[:5]}")

    def test_hybrid_deployment_question_options(self):
        bank = get_bank(BANK_CLOUDCERTPREP)
        q = next(x for x in bank.ALL_QUESTIONS if x.get("source_id") == "q406")
        bodies = [o.split(". ", 1)[1] for o in q["options"]]
        self.assertEqual(
            bodies,
            ["On-premises", "Mixed", "Hybrid", "Cloud"],
        )
        self.assertIn("Mixed", q["explanation"])
        self.assertIn("Hybrid", q["explanation"])

    def test_no_glossary_polluted_service_questions(self):
        polluted = []
        for q in self.bank.ALL_QUESTIONS:
            zh = q.get("question", "")
            en = (q.get("question_en") or "").lower()
            if "nosql database" in en and "Amazon DynamoDB" in zh:
                polluted.append((q["id"], zh))
            if "data warehouse" in en and re.search(
                r"Amazon Redshift(?! 是)", zh
            ):
                polluted.append((q["id"], zh))
        self.assertEqual(polluted, [], f"题干将通用概念误替换成服务名: {polluted[:5]}")

    def test_q086_managed_nosql_question(self):
        q = next(x for x in self.bank.ALL_QUESTIONS if x.get("source_id") == "q086")
        self.assertIn("NoSQL 数据库", q["question"])
        self.assertNotIn("是托管 Amazon DynamoDB", q["question"])

    def test_q461_migrate_databases_not_dms_in_stem(self):
        q = next(x for x in self.bank.ALL_QUESTIONS if x.get("source_id") == "q461")
        self.assertIn("数据库迁移", q["question"])
        self.assertNotRegex(q["question"], r"本地\s*DMS")
        self.assertEqual(q["correct_answers"], ["A"])

    def test_no_correct_answer_verbatim_in_question_stem(self):
        leaked = []
        for q in self.bank.ALL_QUESTIONS:
            zh = q.get("question", "")
            opts = {
                o.split(". ", 1)[0]: o.split(". ", 1)[1].strip()
                for o in q.get("options", [])
                if ". " in o
            }
            for letter in q.get("correct_answers", []):
                body = opts.get(letter, "")
                if len(body) >= 8 and body in zh:
                    leaked.append((q["id"], body[:60]))
        self.assertEqual(leaked, [], f"正确选项全文出现在题干: {leaked[:5]}")

    def test_audit_no_critical_translation_issues(self):
        from tools.audit_cloudcertprep_translations import (
            audit_questions,
            count_critical_issues,
        )

        report = audit_questions(fetch_source=True)
        critical = count_critical_issues(report)
        self.assertEqual(
            critical,
            0,
            f"题干翻译审计失败: {report['answer_in_stem'][:3]} "
            f"{report['glossary_pollution'][:3]}",
        )


if __name__ == "__main__":
    unittest.main()