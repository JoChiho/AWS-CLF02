# -*- coding: utf-8 -*-
"""
AWS CLF-C02 题库数据层（Data Layer）

提供统一的题库访问接口，方便后续维护和扩展。

推荐用法：
    from data import ALL_QUESTIONS, SINGLE_CHOICE_QUESTIONS, MULTI_CHOICE_QUESTIONS
    from data import get_questions_by_domain, get_all_domains
    from data import QUESTION_BY_ID, get_question_by_id, get_all_question_ids
    from data import shuffle_question_options, get_shuffled_questions
"""

import random
import re
from typing import Dict, Any, List

from .single_choice import SINGLE_CHOICE_QUESTIONS
from .multi_choice import MULTI_CHOICE_QUESTIONS

# 合并后的完整题库（推荐在大多数场景下使用）
ALL_QUESTIONS = SINGLE_CHOICE_QUESTIONS + MULTI_CHOICE_QUESTIONS

# 官方 CLF-C02 考试四大领域（按考试顺序排序）
DOMAINS = [
    "Cloud Concepts",
    "Security and Compliance",
    "Technology and Services",
    "Billing, Pricing, and Support",
]

# 稳定 ID 到完整题目对象的映射（用于持久化进度、错题本等）
# 在所有题目被加载后立即构建
QUESTION_BY_ID: dict[str, dict] = {q["id"]: q for q in ALL_QUESTIONS}


def get_questions_by_domain(domain: str):
    """根据领域名称返回该领域下的所有题目（单选 + 多选混合）"""
    return [q for q in ALL_QUESTIONS if q.get("domain") == domain]


def get_all_domains():
    """返回当前题库中实际存在的领域列表"""
    return DOMAINS


def get_domain_question_count(domain: str) -> int:
    """返回某个领域的题目数量"""
    return len(get_questions_by_domain(domain))


def get_question_by_id(qid: str):
    """通过稳定 ID 获取完整题目对象（不存在时返回 None）"""
    return QUESTION_BY_ID.get(qid)


def get_all_question_ids() -> list[str]:
    """返回当前题库中所有题目的稳定 ID 列表（顺序与 ALL_QUESTIONS 一致）"""
    return [q["id"] for q in ALL_QUESTIONS]


def get_wrong_book_questions(wrong_ids: list[str]) -> list[dict]:
    """
    根据错题 ID 列表返回对应的题目对象列表（保持传入顺序）。
    用于“错题本练习”入口。
    """
    result = []
    for qid in wrong_ids:
        q = QUESTION_BY_ID.get(qid)
        if q:
            result.append(q)
    return result


# ============================================================
# 题目顺序 + 选项打乱工具（供 GUI 与 CLI 使用）
# ============================================================

def _strip_option_letter(text: str) -> str:
    """去除选项开头的 A. / B. / A) / a. 等前缀"""
    if not text:
        return ""
    # 匹配 "A. "、"B) "、"C " 等常见形式（支持中英文大小写）
    return re.sub(r'^[A-Ea-e][\.\)]\s*', '', text).strip()


def shuffle_question_options(q: Dict[str, Any]) -> Dict[str, Any]:
    """
    为单道题目生成选项打乱视图（会话内稳定）。

    返回结构：
        {
            "shuffled_options": ["A. 新文本1", "B. 新文本2", ...],  # 已重新编号的干净选项
            "display_to_original": {"A": "C", "B": "A", ...},       # 用户看到的字母 -> 原始字母
            "original_to_display": {"C": "A", "A": "B", ...},
            "display_correct_answers": ["B", "D"],                  # 正确答案在显示字母下的形式
        }
    """
    original_options: List[str] = q.get("options", [])
    if not original_options:
        return {
            "shuffled_options": [],
            "display_to_original": {},
            "original_to_display": {},
            "display_correct_answers": q.get("correct_answers", []),
        }

    # 带原始索引的列表
    indexed = list(enumerate(original_options))
    random.shuffle(indexed)

    shuffled_display: List[str] = []
    display_to_original: Dict[str, str] = {}
    original_to_display: Dict[str, str] = {}

    for new_idx, (orig_idx, raw_text) in enumerate(indexed):
        new_letter = chr(ord("A") + new_idx)
        orig_letter = chr(ord("A") + orig_idx)

        clean_text = _strip_option_letter(raw_text)
        display_text = f"{new_letter}. {clean_text}"

        shuffled_display.append(display_text)
        display_to_original[new_letter] = orig_letter
        original_to_display[orig_letter] = new_letter

    # 计算打乱后的正确答案字母
    orig_correct = q.get("correct_answers", [])
    display_correct = [original_to_display.get(c, c) for c in orig_correct]

    return {
        "shuffled_options": shuffled_display,
        "display_to_original": display_to_original,
        "original_to_display": original_to_display,
        "display_correct_answers": sorted(display_correct),  # 保持多选时字母有序，方便显示
    }


def get_shuffled_questions(questions: list[dict]) -> list[dict]:
    """
    返回题库列表的随机打乱副本。
    每次调用都会产生新的随机顺序，不会修改原始题库数据。
    """
    if not questions:
        return []
    shuffled = questions.copy()
    random.shuffle(shuffled)
    return shuffled


# 便捷包装（可选使用）
def get_shuffled_single_choice_questions() -> list[dict]:
    """返回打乱后的单选题题库（141题）"""
    return get_shuffled_questions(SINGLE_CHOICE_QUESTIONS)


def get_shuffled_multi_choice_questions() -> list[dict]:
    """返回打乱后的多选题题库（104题）"""
    return get_shuffled_questions(MULTI_CHOICE_QUESTIONS)


def get_shuffled_all_questions() -> list[dict]:
    """返回打乱后的完整题库（245题）"""
    return get_shuffled_questions(ALL_QUESTIONS)


__all__ = [
    "SINGLE_CHOICE_QUESTIONS",
    "MULTI_CHOICE_QUESTIONS",
    "ALL_QUESTIONS",
    "DOMAINS",
    "QUESTION_BY_ID",
    "get_questions_by_domain",
    "get_all_domains",
    "get_domain_question_count",
    "get_question_by_id",
    "get_all_question_ids",
    "get_wrong_book_questions",
    "shuffle_question_options",
    "get_shuffled_questions",
    "get_shuffled_single_choice_questions",
    "get_shuffled_multi_choice_questions",
    "get_shuffled_all_questions",
]