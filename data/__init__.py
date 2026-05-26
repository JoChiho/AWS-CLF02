# -*- coding: utf-8 -*-
"""
AWS CLF-C02 题库数据层（Data Layer）

提供统一的题库访问接口，方便后续维护和扩展。

推荐用法：
    from data import ALL_QUESTIONS, SINGLE_CHOICE_QUESTIONS, MULTI_CHOICE_QUESTIONS
    from data import get_questions_by_domain, get_all_domains
"""

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


def get_questions_by_domain(domain: str):
    """根据领域名称返回该领域下的所有题目（单选 + 多选混合）"""
    return [q for q in ALL_QUESTIONS if q.get("domain") == domain]


def get_all_domains():
    """返回当前题库中实际存在的领域列表"""
    return DOMAINS


def get_domain_question_count(domain: str) -> int:
    """返回某个领域的题目数量"""
    return len(get_questions_by_domain(domain))


__all__ = [
    "SINGLE_CHOICE_QUESTIONS",
    "MULTI_CHOICE_QUESTIONS",
    "ALL_QUESTIONS",
    "DOMAINS",
    "get_questions_by_domain",
    "get_all_domains",
    "get_domain_question_count",
]