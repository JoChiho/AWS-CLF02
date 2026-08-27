# -*- coding: utf-8 -*-
"""
策略与准则辨识题库（迁移 7 R / CAF / Well-Architected / 落地场景）。

进度与自建题库、CloudCertPrep、服务定义辨识隔离。
"""
from __future__ import annotations

from typing import Any

from data.concept_drill.questions import CONCEPT_DRILL_QUESTIONS

BANK_ID = "concept_drill"
SOURCE = "concept_drill"

DOMAINS = [
    "Cloud Concepts",
    "Security and Compliance",
    "Technology and Services",
    "Billing, Pricing, and Support",
]

SINGLE_CHOICE_QUESTIONS = CONCEPT_DRILL_QUESTIONS
MULTI_CHOICE_QUESTIONS: list[dict[str, Any]] = []
ALL_QUESTIONS = SINGLE_CHOICE_QUESTIONS
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
