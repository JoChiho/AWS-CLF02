# -*- coding: utf-8 -*-
"""题库注册表：自建题库与 CloudCertPrep 独立板块。"""

from __future__ import annotations

from typing import Any, Protocol

BANK_NATIVE = "native"
BANK_CLOUDCERTPREP = "cloudcertprep"
BANK_KEYWORD_DRILL = "keyword_drill"
BANK_CONCEPT_DRILL = "concept_drill"

BANK_LABELS = {
    BANK_NATIVE: "自建题库（320 题）",
    BANK_CLOUDCERTPREP: "CloudCertPrep 题库",
    BANK_KEYWORD_DRILL: "服务定义辨识",
    BANK_CONCEPT_DRILL: "策略与准则辨识",
}


class QuestionBank(Protocol):
    BANK_ID: str
    SINGLE_CHOICE_QUESTIONS: list[dict[str, Any]]
    MULTI_CHOICE_QUESTIONS: list[dict[str, Any]]
    ALL_QUESTIONS: list[dict[str, Any]]
    DOMAINS: list[str]
    QUESTION_BY_ID: dict[str, dict[str, Any]]

    def get_questions_by_domain(self, domain: str) -> list[dict[str, Any]]: ...
    def get_question_by_id(self, qid: str) -> dict[str, Any] | None: ...
    def get_wrong_book_questions(self, wrong_ids: list[str]) -> list[dict[str, Any]]: ...


def get_bank(bank_id: str = BANK_NATIVE) -> Any:
    """按 bank_id 返回对应题库模块（API 与 data 包一致）。"""
    if bank_id == BANK_CLOUDCERTPREP:
        from data import cloudcertprep

        return cloudcertprep
    if bank_id == BANK_KEYWORD_DRILL:
        from data import keyword_drill

        return keyword_drill
    if bank_id == BANK_CONCEPT_DRILL:
        from data import concept_drill

        return concept_drill
    import data

    return data


def get_bank_label(bank_id: str) -> str:
    return BANK_LABELS.get(bank_id, bank_id)