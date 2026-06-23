# -*- coding: utf-8 -*-
"""解析格式化模块测试"""

import unittest

from data.multi_choice import MULTI_CHOICE_QUESTIONS
from data.single_choice import SINGLE_CHOICE_QUESTIONS
import tkinter as tk

from gui.explanation_formatter import (
    _MD_BOLD,
    _configure_tags,
    _render_key_point,
    parse_explanation,
    render_explanation_body,
)


SAMPLE_SINGLE = (
    "「缓存内容以降低全球用户延迟」是正确的，因为 Edge Location 是 CDN 节点。\n\n"
    "其他选项分析：\n\n"
    "「提供跨 Region 的高可用性」是错误的：跨 Region 高可用依靠 Route 53。\n\n"
    "「托管关系型数据库」是错误的：这是 RDS 的职责。\n\n"
    "**重点考点 / 关键词补充：**\n"
    "- Edge Location ≠ Availability Zone\n"
    "- 主要服务：CloudFront"
)

SAMPLE_MULTI = (
    "正确答案：\n\n"
    "「责任边界取决于使用的服务类型（IaaS/PaaS/SaaS）」\n"
    "「对于托管服务，AWS 承担更多运营责任」\n\n"
    "错误选项分析：\n\n"
    "「无论使用 EC2、Lambda 还是 SaaS…」是错误的：责任是共享的。\n\n"
    "「AWS 始终负责为客户数据生成…」是错误的：客户负责 CMK。\n\n"
    "**重点考点 / 关键词补充：**\n"
    "- **Shared Responsibility Model**：AWS 负责云的安全\n"
    "- **IaaS / PaaS / SaaS 责任边界**：IaaS 客户管最多"
)


class TestExplanationFormatter(unittest.TestCase):
    def test_parse_single_choice_sections(self):
        sec = parse_explanation(SAMPLE_SINGLE)
        self.assertIn("是正确的", sec.opening)
        self.assertEqual(len(sec.wrong_options), 2)
        self.assertEqual(len(sec.key_points), 2)
        self.assertEqual(sec.correct_items, [])

    def test_parse_multi_choice_sections(self):
        sec = parse_explanation(SAMPLE_MULTI)
        self.assertEqual(len(sec.correct_items), 2)
        self.assertEqual(len(sec.wrong_options), 2)
        self.assertEqual(len(sec.key_points), 2)
        self.assertEqual(sec.opening, "")

    def test_parse_escaped_newlines(self):
        escaped = SAMPLE_SINGLE.replace("\n", "\\n")
        sec = parse_explanation(escaped)
        self.assertEqual(len(sec.wrong_options), 2)
        self.assertEqual(len(sec.key_points), 2)

    def test_parse_empty(self):
        sec = parse_explanation("")
        self.assertEqual(sec.opening, "")
        self.assertEqual(sec.wrong_options, [])
        self.assertEqual(sec.key_points, [])

    def test_parse_plain_text_fallback(self):
        sec = parse_explanation("这是一段没有分节的普通解析。")
        self.assertEqual(sec.opening, "这是一段没有分节的普通解析。")

    def test_key_points_keep_markdown_bold(self):
        sec = parse_explanation(SAMPLE_MULTI)
        self.assertTrue(
            any("Shared Responsibility Model" in p for p in sec.key_points),
        )
        self.assertTrue(
            any(_MD_BOLD.search(p) for p in sec.key_points),
        )

    def test_key_point_colon_prefix_gets_keyword_tag(self):
        root = tk.Tk()
        root.withdraw()
        textbox = tk.Text(root)
        _configure_tags(textbox, 1.0)
        _render_key_point(
            textbox,
            "水平扩展（Scale Out）：增加实例数量",
        )
        idx = textbox.get("1.0", "end").find("水平扩展")
        self.assertGreaterEqual(idx, 0)
        self.assertIn("key_keyword", textbox.tag_names(f"1.{idx}"))
        root.destroy()

    def test_key_point_markdown_bold_gets_keyword_tag(self):
        root = tk.Tk()
        root.withdraw()
        textbox = tk.Text(root)
        _configure_tags(textbox, 1.0)
        _render_key_point(
            textbox,
            "**Shared Responsibility Model（责任共担模型）**：AWS 负责云的安全",
        )
        content = textbox.get("1.0", "end")
        self.assertNotIn("**", content)
        idx = content.find("Shared Responsibility Model")
        self.assertGreaterEqual(idx, 0)
        self.assertIn("key_keyword", textbox.tag_names(f"1.{idx}"))
        root.destroy()

    def test_render_explanation_body_highlights_key_points(self):
        try:
            import customtkinter as ctk
        except ImportError:
            self.skipTest("customtkinter not installed")

        try:
            root = ctk.CTk()
        except tk.TclError:
            self.skipTest("Tk not available in test environment")

        root.withdraw()
        textbox = ctk.CTkTextbox(root, font=ctk.CTkFont(size=14), text_color="#e2e6ef")
        render_explanation_body(textbox, SAMPLE_MULTI, scale=1.0)
        inner = textbox._textbox
        ranges = inner.tag_ranges("key_keyword")
        self.assertGreaterEqual(len(ranges), 2)
        highlighted = inner.get(str(ranges[0]), str(ranges[1]))
        self.assertIn("Shared Responsibility Model", highlighted)
        root.destroy()

    def test_bank_coverage(self):
        """题库中带分段标记的解析应能正确拆分错误项与重点。"""
        failures = []
        for q in SINGLE_CHOICE_QUESTIONS + MULTI_CHOICE_QUESTIONS:
            exp = q.get("explanation", "")
            if "其他选项分析" not in exp and "错误选项分析" not in exp:
                continue
            sec = parse_explanation(exp)
            if not sec.wrong_options:
                failures.append(q["id"])
            if "重点考点" in exp and not sec.key_points:
                failures.append(f"{q['id']}:key")
        self.assertEqual(failures, [], f"parse failures: {failures[:10]}")


if __name__ == "__main__":
    unittest.main()