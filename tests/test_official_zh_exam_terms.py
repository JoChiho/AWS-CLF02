# -*- coding: utf-8 -*-
"""官方 CLF-C02 简体中文考试术语映射测试"""

import unittest

from data.official_zh_exam_terms import (
    apply_official_zh_exam_terms,
    is_official_zh_exam_term,
)
from data.aws_english_terms import restore_option, should_force_english_option


class TestOfficialZhExamTerms(unittest.TestCase):
    def test_purchase_options(self):
        self.assertEqual(
            apply_official_zh_exam_terms("Spot Instances", whole_option=True),
            "竞价型实例",
        )
        self.assertEqual(
            apply_official_zh_exam_terms("On-Demand Instances", whole_option=True),
            "按需型实例",
        )
        self.assertEqual(
            apply_official_zh_exam_terms("Reserved Instances", whole_option=True),
            "预留实例",
        )
        self.assertEqual(
            apply_official_zh_exam_terms("Dedicated Hosts", whole_option=True),
            "专属主机",
        )
        self.assertEqual(
            apply_official_zh_exam_terms("Savings Plans", whole_option=True),
            "AWS 节省计划",
        )

    def test_infrastructure_terms(self):
        self.assertEqual(
            apply_official_zh_exam_terms("Availability Zones", whole_option=True),
            "可用区",
        )
        text = apply_official_zh_exam_terms("跨多个 Availability Zones 部署")
        self.assertIn("可用区", text)
        self.assertNotIn("Availability Zones", text)

    def test_service_brands_stay_english(self):
        self.assertFalse(is_official_zh_exam_term("Amazon S3"))
        self.assertFalse(is_official_zh_exam_term("AWS Lambda"))
        self.assertTrue(should_force_english_option("Amazon S3"))
        self.assertEqual(restore_option("C. Amazon S3"), "C. Amazon S3")

    def test_console_and_quotas(self):
        self.assertEqual(
            apply_official_zh_exam_terms("AWS Management Console"),
            "AWS 管理控制台",
        )
        self.assertEqual(
            apply_official_zh_exam_terms("Service Quotas", whole_option=True),
            "服务配额",
        )

    def test_shared_responsibility(self):
        self.assertIn(
            "责任共担模式",
            apply_official_zh_exam_terms("根据 AWS Shared Responsibility Model"),
        )

    def test_mixed_distractor_stays_english(self):
        self.assertTrue(should_force_english_option("Mixed"))
        self.assertEqual(restore_option("B. Mixed"), "B. Mixed")
