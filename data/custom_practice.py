# -*- coding: utf-8 -*-
"""自定义练习：按题量、范围与筛选条件随机抽题。"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from data.progress import get_all_question_stats

FILTER_ALL = "all"
FILTER_NEVER = "never"
FILTER_LOW_ACCURACY = "low_accuracy"

SCOPE_ALL = "all"
SCOPE_SINGLE = "single"
SCOPE_MULTI = "multi"


@dataclass
class CustomPracticeResult:
    questions: List[Dict[str, Any]]
    requested_count: int
    pool_size: int
    actual_count: int
    mode: str


def _question_accuracy(
    qid: str, stats: Dict[str, Dict[str, Any]],
) -> Optional[float]:
    raw = stats.get(qid)
    if not raw:
        return None
    correct = int(raw.get("correct_count", 0))
    wrong = int(raw.get("wrong_count", 0))
    total = correct + wrong
    if total <= 0:
        return None
    return correct / total * 100.0


def _attempt_count(qid: str, stats: Dict[str, Dict[str, Any]]) -> int:
    raw = stats.get(qid)
    if not raw:
        return 0
    return int(raw.get("correct_count", 0)) + int(raw.get("wrong_count", 0))


def get_practice_pool(
    *,
    scope: str = SCOPE_ALL,
    filter_mode: str = FILTER_ALL,
    accuracy_threshold: float = 70.0,
    stats: Optional[Dict[str, Dict[str, Any]]] = None,
    bank_id: str = "native",
) -> List[Dict[str, Any]]:
    """返回符合范围与筛选条件的题目池（不打乱、不截断）。"""
    from data.banks import get_bank

    bank = get_bank(bank_id)

    if scope == SCOPE_SINGLE:
        pool = list(bank.SINGLE_CHOICE_QUESTIONS)
    elif scope == SCOPE_MULTI:
        pool = list(bank.MULTI_CHOICE_QUESTIONS)
    elif scope.startswith("domain:"):
        domain = scope.split(":", 1)[1]
        pool = list(bank.get_questions_by_domain(domain))
    else:
        pool = list(bank.ALL_QUESTIONS)

    stats = stats if stats is not None else get_all_question_stats(bank_id=bank_id)

    if filter_mode == FILTER_NEVER:
        pool = [q for q in pool if _attempt_count(q["id"], stats) == 0]
    elif filter_mode == FILTER_LOW_ACCURACY:
        filtered: List[Dict[str, Any]] = []
        for q in pool:
            acc = _question_accuracy(q["id"], stats)
            if acc is not None and acc < accuracy_threshold:
                filtered.append(q)
        pool = filtered

    return pool


def build_custom_practice_mode(
    *,
    count: int,
    scope: str,
    filter_mode: str,
    accuracy_threshold: float = 70.0,
) -> str:
    parts = [
        f"custom:n={count}",
        f"scope={scope}",
        f"filter={filter_mode}",
    ]
    if filter_mode == FILTER_LOW_ACCURACY:
        parts.append(f"thr={int(accuracy_threshold)}")
    return ";".join(parts)


def select_custom_practice_questions(
    *,
    count: int,
    scope: str = SCOPE_ALL,
    filter_mode: str = FILTER_ALL,
    accuracy_threshold: float = 70.0,
    bank_id: str = "native",
) -> CustomPracticeResult:
    """从符合条件的题目池中随机抽取至多 count 道题。"""
    pool = get_practice_pool(
        scope=scope,
        filter_mode=filter_mode,
        accuracy_threshold=accuracy_threshold,
        bank_id=bank_id,
    )
    pool_size = len(pool)
    actual_count = min(max(0, count), pool_size)
    selected = random.sample(pool, actual_count) if actual_count > 0 else []

    mode = build_custom_practice_mode(
        count=count,
        scope=scope,
        filter_mode=filter_mode,
        accuracy_threshold=accuracy_threshold,
    )
    return CustomPracticeResult(
        questions=selected,
        requested_count=count,
        pool_size=pool_size,
        actual_count=actual_count,
        mode=mode,
    )