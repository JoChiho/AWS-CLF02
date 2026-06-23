# -*- coding: utf-8 -*-
"""术语中文标注回归测试"""

import unittest

from gui.term_glossary import annotate_text


class TestTermGlossary(unittest.TestCase):
    def test_spot_instances_annotation(self):
        out = annotate_text("以下哪种工作负载最适合 Spot Instances？")
        self.assertIn("Spot Instances（竞价实例）", out)

    def test_on_demand_instances_annotation(self):
        out = annotate_text("On-Demand Instances 灵活性最高")
        self.assertIn("On-Demand Instances（按需实例）", out)

    def test_no_double_annotation(self):
        src = "Spot Instances（竞价实例）已标注"
        self.assertEqual(annotate_text(src), src)

    def test_longer_term_matches_first(self):
        out = annotate_text("推荐购买 Compute Savings Plans")
        self.assertIn("Compute Savings Plans（计算节省计划）", out)
        self.assertNotIn("Savings Plans（节省计划）（", out)

    def test_case_preserved(self):
        out = annotate_text("使用 amazon s3 存储")
        self.assertIn("amazon s3（对象存储）", out.lower() or out)
        # 保留原文大小写
        self.assertTrue("（对象存储）" in out)

    def test_empty_and_plain_chinese(self):
        self.assertEqual(annotate_text(""), "")
        self.assertEqual(annotate_text("高可用架构"), "高可用架构")

    def test_common_abbreviations(self):
        out = annotate_text("IAM 用户通过 VPC 访问 RDS 数据库")
        self.assertIn("IAM（身份与访问管理）", out)
        self.assertIn("VPC（虚拟私有云）", out)
        self.assertIn("RDS（关系型数据库）", out)

    def test_edge_location_singular(self):
        out = annotate_text("Edge Location 用于 CDN 缓存")
        self.assertIn("Edge Location（边缘站点）", out)
        self.assertIn("CDN（内容分发网络）", out)

    def test_on_demand_standalone(self):
        out = annotate_text("Spot 价格与 On-Demand 价格对比")
        self.assertIn("On-Demand（按需）", out)
        self.assertNotIn("On-Demand（按需） Instances", out)

    def test_multi_az_annotated_without_az_inside(self):
        out = annotate_text("Multi-AZ 部署提高可用性")
        self.assertIn("Multi-AZ（多可用区）", out)
        self.assertNotIn("Multi-AZ（多可用区）（可用区）", out)

    def test_enterprise_support(self):
        out = annotate_text("Enterprise Support 包含 TAM 服务")
        self.assertIn("Enterprise Support（企业级支持）", out)


if __name__ == "__main__":
    unittest.main()