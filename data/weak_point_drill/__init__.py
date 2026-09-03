# -*- coding: utf-8 -*-
"""
薄弱点突击题库。

针对错 ≥4 次且正确率 ≤25% 的考点重出新题。进度与其它题库隔离。
"""
from __future__ import annotations

from typing import Any

from data.weak_point_drill.questions import WEAK_POINT_QUESTIONS

BANK_ID = "weak_point_drill"
SOURCE = "weak_point_drill"

DOMAINS = [
    "Cloud Concepts",
    "Security and Compliance",
    "Technology and Services",
    "Billing, Pricing, and Support",
]

SINGLE_CHOICE_QUESTIONS = [q for q in WEAK_POINT_QUESTIONS if not q.get("is_multi")]
MULTI_CHOICE_QUESTIONS = [q for q in WEAK_POINT_QUESTIONS if q.get("is_multi")]
ALL_QUESTIONS = SINGLE_CHOICE_QUESTIONS + MULTI_CHOICE_QUESTIONS
QUESTION_BY_ID: dict[str, dict] = {q["id"]: q for q in ALL_QUESTIONS}


def get_questions_by_domain(domain: str) -> list[dict]:
    return [q for q in ALL_QUESTIONS if q.get("domain") == domain]


def get_all_domains() -> list[str]:
    return DOMAINS


def get_domain_question_count(domain: str) -> int:
    return len(get_questions_by_domain(domain))


def get_question_by_id(qid: str) -> dict | None:
    return QUESTION_BY_ID.get(qid)


def get_all_question_ids() -> list[str]:
    return [q["id"] for q in ALL_QUESTIONS]


def get_wrong_book_questions(wrong_ids: list[str]) -> list[dict]:
    result = []
    for qid in wrong_ids:
        q = QUESTION_BY_ID.get(qid)
        if q:
            result.append(q)
    return result


def shuffle_question_options(q: dict[str, Any]) -> dict[str, Any]:
    import data as _data

    return _data.shuffle_question_options(q)


def get_shuffled_questions(questions: list[dict]) -> list[dict]:
    import data as _data

    return _data.get_shuffled_questions(questions)


__all__ = [
    "BANK_ID",
    "SOURCE",
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
]
