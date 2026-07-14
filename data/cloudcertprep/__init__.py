# -*- coding: utf-8 -*-
"""
CloudCertPrep CLF-C02 题库数据层（独立板块，与自建 320 题完全隔离）。

推荐用法：
    from data.cloudcertprep import ALL_QUESTIONS, get_question_by_id
    from data.banks import BANK_CLOUDCERTPREP, get_bank
"""

from __future__ import annotations

import random
import re
from typing import Any

from .domains import DOMAINS, MOCK_EXAM_DOMAIN_WEIGHTS
from .multi_choice import MULTI_CHOICE_QUESTIONS
from .single_choice import SINGLE_CHOICE_QUESTIONS

BANK_ID = "cloudcertprep"
SOURCE = "cloudcertprep"

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


def _strip_option_letter(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"^[A-Ea-e][\.\)]\s*", "", text).strip()


def shuffle_question_options(q: dict[str, Any]) -> dict[str, Any]:
    original_options: list[str] = q.get("options", [])
    if not original_options:
        return {
            "shuffled_options": [],
            "display_to_original": {},
            "original_to_display": {},
            "display_correct_answers": q.get("correct_answers", []),
        }

    indexed = list(enumerate(original_options))
    random.shuffle(indexed)

    shuffled_display: list[str] = []
    display_to_original: dict[str, str] = {}
    original_to_display: dict[str, str] = {}

    for new_idx, (orig_idx, raw_text) in enumerate(indexed):
        new_letter = chr(ord("A") + new_idx)
        orig_letter = chr(ord("A") + orig_idx)
        clean_text = _strip_option_letter(raw_text)
        display_text = f"{new_letter}. {clean_text}"
        shuffled_display.append(display_text)
        display_to_original[new_letter] = orig_letter
        original_to_display[orig_letter] = new_letter

    orig_correct = q.get("correct_answers", [])
    display_correct = [original_to_display.get(c, c) for c in orig_correct]

    return {
        "shuffled_options": shuffled_display,
        "display_to_original": display_to_original,
        "original_to_display": original_to_display,
        "display_correct_answers": sorted(display_correct),
    }


def get_shuffled_questions(questions: list[dict]) -> list[dict]:
    if not questions:
        return []
    shuffled = questions.copy()
    random.shuffle(shuffled)
    return shuffled


__all__ = [
    "BANK_ID",
    "SOURCE",
    "SINGLE_CHOICE_QUESTIONS",
    "MULTI_CHOICE_QUESTIONS",
    "ALL_QUESTIONS",
    "DOMAINS",
    "MOCK_EXAM_DOMAIN_WEIGHTS",
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