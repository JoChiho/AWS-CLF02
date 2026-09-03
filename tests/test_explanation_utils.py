# -*- coding: utf-8 -*-
"""解析结构化工具测试"""

import unittest

from data.explanation_utils import (
    rebuild_explanation_text,
    structure_wrong_option_analysis,
)
from gui.explanation_formatter import parse_explanation


CCP_SAMPLE = (
    "正确答案：\n\n"
    "「在美国区域部署EC2实例可以使计算资源在物理上更接近美国用户，从而以最小的额外成本直接减少网络延迟。」\n\n"
    "错误选项分析：\n\n"
    "应用基于延迟的 Route 53 路由策略会将用户引导至延迟最低的区域，但这只能优化路由，如果所有计算资源都保留在东京，那么这本身并不会减少延迟。"
    "注册新的美国域名会改变用户通过名称访问应用程序的方式，但不会使任何计算资源更靠近美国用户或减少网络延迟。"
    "在美国建设新的数据中心并实施混合模型会带来大量资本支出和运营复杂性，与最大限度降低成本的要求相矛盾。"
)

CCP_OPTIONS = [
    "A. 应用Route 53基于延迟的路由策略",
    "B. 注册新的美国域名，服务美国用户",
    "C. 在美国建设新数据中心并实施混合模式",
    "D. 在位于美国的区域部署新的 Amazon EC2 实例",
]


class TestExplanationUtils(unittest.TestCase):
    def test_structure_splits_by_wrong_option_count(self):
        blocks = structure_wrong_option_analysis(
            CCP_SAMPLE.split("错误选项分析：\n\n", 1)[1],
            CCP_OPTIONS,
            ["D"],
        )
        self.assertEqual(len(blocks), 3)
        self.assertTrue(all("是错误的" in b for b in blocks))
        self.assertTrue(blocks[0].startswith("「A."))

    def test_rebuild_explanation_produces_paragraphs(self):
        rebuilt = rebuild_explanation_text(CCP_SAMPLE, CCP_OPTIONS, ["D"])
        sec = parse_explanation(
            rebuilt, options=CCP_OPTIONS, correct_answers=["D"],
        )
        self.assertEqual(len(sec.wrong_options), 3)

    def test_parse_cloudcertprep_wall_of_text_at_runtime(self):
        sec = parse_explanation(
            CCP_SAMPLE, options=CCP_OPTIONS, correct_answers=["D"],
        )
        self.assertEqual(len(sec.wrong_options), 3)

    def test_does_not_zip_reasons_in_letter_order(self):
        wrong = (
            "在美国建设新的数据中心并实施混合模型会带来大量资本支出。"
            "应用基于延迟的 Route 53 路由策略只会优化路由。"
            "注册新的美国域名不会使计算资源更靠近用户。"
        )
        blocks = structure_wrong_option_analysis(
            wrong, CCP_OPTIONS, ["D"],
        )
        by_letter = {b[1]: b for b in blocks}
        self.assertIn("C", by_letter)
        self.assertIn("数据中心", by_letter["C"])
        self.assertIn("A", by_letter)
        self.assertIn("Route 53", by_letter["A"])
        self.assertNotIn("「D.", "\n".join(blocks))

    def test_never_marks_correct_letter_as_wrong(self):
        wrong = (
            "「D. 在位于美国的区域部署新的 Amazon EC2 实例」是错误的："
            "这其实是正确做法。"
            "「A. 应用Route 53基于延迟的路由策略」是错误的：只优化路由。"
        )
        blocks = structure_wrong_option_analysis(
            wrong, CCP_OPTIONS, ["D"],
        )
        joined = "\n".join(blocks)
        self.assertNotIn("「D.", joined)
        self.assertTrue(any(b.startswith("「A.") for b in blocks))

    def test_concatenated_reasons_follow_option_content(self):
        options = [
            "A. 用户根据许可按小时或按月支付软件费用",
            "B. AWS Marketplace 使用户能够通过一键式启动应用程序",
            "C. AWS Marketplace 数据加密由第三方供应商管理",
            "D. AWS Marketplace 无需升级到较新的软件版本",
            "E. 用户无需测试即可部署第三方软件",
        ]
        wrong = (
            "「C. AWS Marketplace 数据加密由第三方供应商管理」不是本题应选的项："
            "AWS Marketplace 数据加密不由第三方供应商代表客户进行管理。"
            "AWS Marketplace 并不能消除升级到较新软件版本的需要。"
            "用户无法在未经测试的情况下部署第三方 Marketplace 软件。"
        )
        blocks = structure_wrong_option_analysis(
            wrong, options, ["A", "B"],
            question="使用 AWS Marketplace 中的第三方软件有什么价值？",
        )
        joined = "\n".join(blocks)
        self.assertIn("「C.", joined)
        self.assertIn("「D.", joined)
        self.assertIn("「E.", joined)
        self.assertNotIn("「A.", joined)
        self.assertNotIn("「B.", joined)
        by_letter = {b[1]: b for b in blocks}
        self.assertIn("数据加密", by_letter["C"])
        self.assertIn("升级", by_letter["D"])
        self.assertIn("测试", by_letter["E"])

    def test_short_option_mention_does_not_steal_subject(self):
        options = [
            "A. 高可用性",
            "B. 共享安全模型",
            "C. 弹性",
            "D. 按量付费定价",
            "E. 可靠性",
        ]
        wrong = (
            "「A. 高可用性」是错误的：高可用通过冗余确保应用程序在发生故障时仍可访问，"
            "虽然它有助于提高可靠性，但不会直接降低成本。\n\n"
            "「E. 可靠性」是错误的：可靠性是指工作负载正确执行其预期功能的能力。"
        )
        blocks = structure_wrong_option_analysis(wrong, options, ["C", "D"])
        by_letter = {b[1]: b for b in blocks}
        self.assertIn("高可用", by_letter["A"])
        self.assertIn("预期功能", by_letter["E"])
        self.assertNotIn("该项不是本题的正确选择", by_letter["A"])

    def test_service_reason_not_assigned_to_mentioned_correct_service(self):
        options = [
            "A. Amazon EC2",
            "B. Amazon S3",
            "C. Amazon Elastic Block Store (Amazon EBS)",
            "D. Amazon Cognito",
            "E. AWS Lambda",
        ]
        wrong = (
            "「C. Amazon Elastic Block Store (Amazon EBS)」是错误的："
            "Amazon Elastic Block Store 是一种块存储服务，提供附加到 Amazon EC2 instances 的持久卷。"
        )
        blocks = structure_wrong_option_analysis(wrong, options, ["A", "E"])
        joined = "\n".join(blocks)
        self.assertIn("「C.", joined)
        self.assertNotIn("「A.", joined)
        self.assertIn("块存储", "\n".join(b for b in blocks if b.startswith("「C.")))

    def test_letterless_quotes_map_to_wrong_options(self):
        options = [
            "A. CloudFront 主要优化 HTTP/HTTPS 内容分发和边缘缓存",
            "B. Global Accelerator 使用 Anycast IP 加速 TCP/UDP 流量",
            "C. CloudFront vs Global Accelerator 完全相同，两者均只能加速 HTTPS 网站内容",
            "D. Global Accelerator 主要通过边缘缓存静态文件降低延迟，不提供 Anycast IP 功能",
        ]
        wrong = (
            "「两者完全相同且只能加速 HTTPS」是错误的：GA 支持 TCP/UDP。\n\n"
            "「GA 主要通过边缘缓存静态文件」是错误的：缓存是 CloudFront 核心能力。"
        )
        blocks = structure_wrong_option_analysis(wrong, options, ["A", "B"])
        letters = {b[1] for b in blocks}
        self.assertEqual(letters, {"C", "D"})
        by_letter = {b[1]: b for b in blocks}
        self.assertIn("TCP", by_letter["C"])
        self.assertIn("缓存", by_letter["D"])


if __name__ == "__main__":
    unittest.main()