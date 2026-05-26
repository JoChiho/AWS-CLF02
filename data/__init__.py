# -*- coding: utf-8 -*-
"""
AWS CLF-C02 题库数据层（Data Layer）

提供统一的题库访问接口，方便后续维护和扩展。

推荐用法：
    from data import ALL_QUESTIONS, SINGLE_CHOICE_QUESTIONS, MULTI_CHOICE_QUESTIONS
"""

from .single_choice import SINGLE_CHOICE_QUESTIONS
from .multi_choice import MULTI_CHOICE_QUESTIONS

# 合并后的完整题库（推荐在大多数场景下使用）
ALL_QUESTIONS = SINGLE_CHOICE_QUESTIONS + MULTI_CHOICE_QUESTIONS

__all__ = [
    "SINGLE_CHOICE_QUESTIONS",
    "MULTI_CHOICE_QUESTIONS",
    "ALL_QUESTIONS",
]