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


if __name__ == "__main__":
    unittest.main()