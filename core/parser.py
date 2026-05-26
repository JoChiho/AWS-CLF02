# -*- coding: utf-8 -*-
"""
输入格式解析模块（Input Parser）

负责处理用户在命令行输入的答案，支持单选和多选的多种输入格式。
"""

import re
from typing import List


def parse_user_answers(raw_input: str) -> List[str]:
    """
    将用户输入的答案字符串解析为标准化的字母列表。

    支持的输入格式示例：
        - 单选: "A", "b", " c "
        - 多选: "A C", "a,c", "B D E", "ac", "A,C,D"

    返回值：
        去重后按字母顺序排序的大写列表，例如：["A", "C"] 或 ["B"]
    """
    if not raw_input or not isinstance(raw_input, str):
        return []

    # 提取所有英文字母（忽略大小写、空格、逗号、分号等）
    letters = re.findall(r'[A-Za-z]', raw_input)

    # 转为大写、去重、排序
    normalized = sorted(set(letter.upper() for letter in letters))

    # 只保留 A-D（未来可扩展到更多选项）
    valid_letters = [l for l in normalized if l in "ABCD"]

    return valid_letters


def is_quit_command(raw_input: str) -> bool:
    """判断用户是否输入退出指令"""
    if not raw_input:
        return False
    return raw_input.strip().lower() in ("q", "quit", "exit", "退出")


# 便捷测试入口
if __name__ == "__main__":
    test_cases = [
        "A",
        " b ",
        "A C",
        "a,c,d",
        "B D E",
        "ac",
        "Q",
        "quit",
        "",
        "   ",
    ]
    for case in test_cases:
        parsed = parse_user_answers(case)
        is_quit = is_quit_command(case)
        print(f"Input: {repr(case):12} -> {parsed} | Quit: {is_quit}")