# -*- coding: utf-8 -*-
"""练习模式解析文本结构化解析与富文本渲染。"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExplanationSections:
    """将题库 explanation 字段拆成易读区块。"""

    opening: str = ""
    correct_items: list[str] = field(default_factory=list)
    wrong_options: list[str] = field(default_factory=list)
    key_points: list[str] = field(default_factory=list)


_SECTION_WRONG = re.compile(
    r"\n\n(?:其他选项分析|错误选项分析)[：:]\s*\n\n",
    re.MULTILINE,
)
_SECTION_KEY = re.compile(
    r"\n\n\*\*(?:重点考点|考试重点)[^*\n]*\*\*\s*\n",
    re.MULTILINE,
)
_SECTION_CORRECT_HEADER = re.compile(r"^正确答案[：:]\s*\n\n", re.MULTILINE)
_BULLET = re.compile(r"^[-•*]\s*", re.MULTILINE)
_MD_BOLD = re.compile(r"\*\*(.+?)\*\*")
_KEY_PREFIX = re.compile(r"^([^：:\n]+)([：:])(.*)$", re.DOTALL)


def _normalize_explanation_text(text: str) -> str:
    """统一换行，修复题库中偶发的字面量 \\n。"""
    raw = (text or "").replace("\\n", "\n").strip()
    return raw


def _split_blocks(paragraph: str) -> list[str]:
    return [block.strip() for block in re.split(r"\n\n+", paragraph.strip()) if block.strip()]


def _extract_correct_items(opening: str) -> tuple[list[str], str]:
    """从多选题「正确答案」区块拆出条目，返回 (条目列表, 剩余开场说明)。"""
    if not _SECTION_CORRECT_HEADER.match(opening):
        return [], opening

    body = _SECTION_CORRECT_HEADER.sub("", opening, count=1).strip()
    if not body:
        return [], ""

    lines = [line.strip() for line in body.splitlines() if line.strip()]
    if lines and all(
        line.startswith("「") and line.endswith("」") for line in lines
    ):
        return lines, ""

    blocks = _split_blocks(body)
    if not blocks:
        return [], ""

    if len(blocks) == 1 and "是正确的" in blocks[0]:
        return [], blocks[0]

    return blocks, ""


def parse_explanation(text: str) -> ExplanationSections:
    """把原始解析拆成：正确说明 / 错误选项 / 重点考点。"""
    raw = _normalize_explanation_text(text)
    if not raw:
        return ExplanationSections()

    head = raw
    key_part = ""

    key_split = _SECTION_KEY.split(raw, maxsplit=1)
    if len(key_split) == 2:
        head, key_part = key_split

    opening = head
    wrong_part = ""

    wrong_split = _SECTION_WRONG.split(head, maxsplit=1)
    if len(wrong_split) == 2:
        opening, wrong_part = wrong_split

    correct_items, opening = _extract_correct_items(opening.strip())

    return ExplanationSections(
        opening=opening.strip(),
        correct_items=correct_items,
        wrong_options=_split_blocks(wrong_part),
        key_points=[
            _BULLET.sub("", line).strip()
            for line in key_part.splitlines()
            if line.strip()
        ],
    )


def _insert(textbox: Any, content: str, tag: str) -> None:
    if not content:
        return
    textbox.insert("end", content, tag)


def _configure_tags(textbox: Any, scale: float = 1.0) -> None:
    """为底层 Tk Text 配置样式标签。"""
    body_size = max(13, int(14 * scale))
    title_size = max(14, int(15 * scale))
    small_size = max(12, int(13 * scale))

    textbox.tag_configure(
        "body",
        foreground="#e2e6ef",
        spacing1=3,
        spacing3=6,
        font=("Microsoft YaHei UI", body_size),
    )
    textbox.tag_configure(
        "quote_correct",
        foreground="#6ee7a0",
        font=("Microsoft YaHei UI", body_size, "bold"),
    )
    textbox.tag_configure(
        "section_title",
        foreground="#7ec8ff",
        font=("Microsoft YaHei UI", title_size, "bold"),
        spacing1=12,
        spacing3=8,
    )
    textbox.tag_configure(
        "section_divider",
        foreground="#3d4f6f",
        spacing1=14,
        spacing3=10,
        font=("Microsoft YaHei UI", max(11, int(12 * scale))),
    )
    textbox.tag_configure(
        "wrong_option",
        foreground="#f0c4c4",
        spacing1=6,
        spacing3=6,
        font=("Microsoft YaHei UI", body_size),
        lmargin1=12,
        lmargin2=12,
    )
    textbox.tag_configure(
        "quote_wrong",
        foreground="#ff8a8a",
        font=("Microsoft YaHei UI", body_size, "bold"),
    )
    textbox.tag_configure(
        "key_header",
        foreground="#ffd966",
        font=("Microsoft YaHei UI", title_size, "bold"),
        spacing1=12,
        spacing3=8,
    )
    textbox.tag_configure(
        "key_bullet",
        foreground="#d5dbe8",
        spacing1=3,
        spacing3=4,
        font=("Microsoft YaHei UI", body_size),
        lmargin1=20,
        lmargin2=32,
    )
    textbox.tag_configure(
        "key_keyword",
        foreground="#5eb8ff",
        font=("Microsoft YaHei UI", body_size, "bold"),
    )
    textbox.tag_raise("key_keyword")
    textbox.tag_configure(
        "muted",
        foreground="#9aa3b5",
        font=("Microsoft YaHei UI", small_size),
        spacing1=4,
        spacing3=4,
    )


def _insert_section_divider(textbox: Any) -> None:
    _insert(textbox, "────────────────────────────\n", "section_divider")


def render_explanation_body(
    ctk_textbox: Any,
    explanation: str,
    *,
    scale: float = 1.0,
) -> None:
    """
    将解析正文渲染到 CTkTextbox（仅内容区，不含正误状态行）。
    使用颜色与分段标题提升可读性。
    """
    inner = ctk_textbox._textbox
    inner.configure(state="normal")
    inner.delete("1.0", "end")
    _configure_tags(inner, scale)

    sections = parse_explanation(explanation)
    if not any([
        sections.opening,
        sections.correct_items,
        sections.wrong_options,
        sections.key_points,
    ]):
        _insert(inner, explanation or "暂无解析", "muted")
        inner.configure(state="disabled")
        return

    if sections.correct_items:
        _insert(inner, "正确答案\n", "section_title")
        for idx, item in enumerate(sections.correct_items):
            if idx > 0:
                _insert(inner, "\n", "body")
            _render_quoted_lines(inner, item, "quote_correct", "body")

    if sections.opening:
        if sections.correct_items:
            _insert(inner, "\n", "body")
        _render_opening(inner, sections.opening)

    if sections.wrong_options:
        _insert_section_divider(inner)
        _insert(inner, "错误选项分析\n", "section_title")
        for idx, block in enumerate(sections.wrong_options):
            if idx > 0:
                _insert(inner, "\n", "wrong_option")
            _render_wrong_block(inner, block)

    if sections.key_points:
        _insert_section_divider(inner)
        _insert(inner, "重点考点 / 关键词\n", "key_header")
        for point in sections.key_points:
            _render_key_point(inner, point)

    inner.configure(state="disabled")


def _render_inline_markdown(
    textbox: Any, text: str, *, keyword_tag: str, normal_tag: str,
) -> None:
    """将 **关键词** 渲染为加粗高亮，其余为普通正文。"""
    if not text:
        return
    parts = re.split(r"(\*\*.+?\*\*)", text)
    for part in parts:
        if not part:
            continue
        bold_match = _MD_BOLD.fullmatch(part)
        if bold_match:
            _insert(textbox, bold_match.group(1), keyword_tag)
        else:
            _insert(textbox, part, normal_tag)


def _render_key_point(textbox: Any, point: str) -> None:
    _insert(textbox, "• ", "key_bullet")
    if _MD_BOLD.search(point):
        _render_inline_markdown(
            textbox, point, keyword_tag="key_keyword", normal_tag="key_bullet",
        )
    else:
        prefix_match = _KEY_PREFIX.match(point)
        if prefix_match:
            prefix, separator, rest = prefix_match.groups()
            _insert(textbox, prefix.strip(), "key_keyword")
            _insert(textbox, separator + rest, "key_bullet")
        else:
            _insert(textbox, point, "key_keyword")
    _insert(textbox, "\n", "key_bullet")


def _render_quoted_lines(
    textbox: Any, text: str, quote_tag: str, body_tag: str,
) -> None:
    parts = re.split(r"(「[^」]+」)", text)
    for part in parts:
        if part.startswith("「") and part.endswith("」"):
            _insert(textbox, part, quote_tag)
        else:
            _insert(textbox, part, body_tag)


def _render_opening(textbox: Any, opening: str) -> None:
    """正确选项说明：高亮「」内引文。"""
    _render_quoted_lines(textbox, opening, "quote_correct", "body")
    _insert(textbox, "\n", "body")


def _render_wrong_block(textbox: Any, block: str) -> None:
    """错误选项段落：高亮选项引文。"""
    _render_quoted_lines(textbox, block, "quote_wrong", "wrong_option")