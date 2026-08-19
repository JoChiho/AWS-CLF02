# -*- coding: utf-8 -*-
"""
CLF-C02 模拟考试抽题逻辑

按官方考试领域权重从题库随机抽题，默认 65 题 / 90 分钟 / 70% 及格。
"""

import random
from typing import Dict, List, Any

from data.banks import BANK_NATIVE, get_bank

MOCK_EXAM_QUESTION_COUNT = 65
MOCK_EXAM_DURATION_SEC = 90 * 60
MOCK_EXAM_PASS_PERCENT = 70.0

# CLF-C02 官方考试领域权重（%）
MOCK_EXAM_DOMAIN_WEIGHTS: Dict[str, int] = {
    "Cloud Concepts": 24,
    "Security and Compliance": 30,
    "Technology and Services": 34,
    "Billing, Pricing, and Support": 12,
}


def allocate_domain_counts(
    total: int = MOCK_EXAM_QUESTION_COUNT,
    weights: Dict[str, int] | None = None,
) -> Dict[str, int]:
    """
    按权重分配各领域题目数量（最大余数法），保证总和恰好等于 total。
    """
    weights = weights or MOCK_EXAM_DOMAIN_WEIGHTS
    domains = [d for d in weights]
    total_weight = sum(weights[d] for d in domains)

    exact = {d: total * weights[d] / total_weight for d in domains}
    counts = {d: int(exact[d]) for d in domains}
    remainder = total - sum(counts.values())

    if remainder > 0:
        by_fraction = sorted(domains, key=lambda d: exact[d] - counts[d], reverse=True)
        for i in range(remainder):
            counts[by_fraction[i]] += 1

    return counts


def select_mock_exam_questions(
    count: int = MOCK_EXAM_QUESTION_COUNT,
    weights: Dict[str, int] | None = None,
    bank_id: str = BANK_NATIVE,
) -> List[Dict[str, Any]]:
    """
    按领域权重随机抽题，最终顺序随机打乱。

    若某领域题库不足，先取尽该领域全部题目，再从其余未选中题目中补足。
    """
    bank = get_bank(bank_id)
    domains = bank.DOMAINS
    weights = weights or getattr(bank, "MOCK_EXAM_DOMAIN_WEIGHTS", MOCK_EXAM_DOMAIN_WEIGHTS)
    allocation = allocate_domain_counts(count, weights)
    selected: List[Dict[str, Any]] = []
    selected_ids: set[str] = set()

    for domain in domains:
        need = allocation.get(domain, 0)
        if need <= 0:
            continue

        pool = [
            q for q in bank.get_questions_by_domain(domain)
            if q["id"] not in selected_ids
        ]
        take = min(need, len(pool))
        if take > 0:
            picked = random.sample(pool, take)
            selected.extend(picked)
            selected_ids.update(q["id"] for q in picked)

    if len(selected) < count:
        remaining_pool = [
            q for q in bank.ALL_QUESTIONS if q["id"] not in selected_ids
        ]
        extra = min(count - len(selected), len(remaining_pool))
        if extra > 0:
            picked = random.sample(remaining_pool, extra)
            selected.extend(picked)
            selected_ids.update(q["id"] for q in picked)

    return bank.get_shuffled_questions(selected[:count])


def score_mock_exam(
    questions: List[Dict[str, Any]],
    answers_by_index: Dict[int, List[str]],
) -> Dict[str, Any]:
    """
    计算模拟考试成绩与领域分项统计。

    answers_by_index: 0-based 索引 -> 用户答案（原始字母）
    """
    total = len(questions)
    correct_count = 0
    answered_count = 0
    wrong_items: List[Dict[str, Any]] = []

    domain_keys = sorted({q.get("domain", "") for q in questions if q.get("domain")})
    domain_stats: Dict[str, Dict[str, int]] = {
        d: {"total": 0, "correct": 0, "answered": 0} for d in domain_keys
    }

    for i, q in enumerate(questions):
        domain = q.get("domain", "")
        if domain in domain_stats:
            domain_stats[domain]["total"] += 1

        user = answers_by_index.get(i, [])
        if user:
            answered_count += 1
            if domain in domain_stats:
                domain_stats[domain]["answered"] += 1

        is_correct = bool(user) and set(user) == set(q.get("correct_answers", []))
        if is_correct:
            correct_count += 1
            if domain in domain_stats:
                domain_stats[domain]["correct"] += 1
        elif user:
            wrong_items.append({
                "index": i + 1,
                "id": q.get("id"),
                "domain": domain,
                "question": q["question"],
                "options": q.get("options", []),
                "user_answer": user,
                "correct_answers": q.get("correct_answers", []),
                "explanation": q.get("explanation", ""),
            })

    # 未作答视为错误，计入错题（无 user_answer 展示为未作答）
    for i, q in enumerate(questions):
        if not answers_by_index.get(i):
            wrong_items.append({
                "index": i + 1,
                "id": q.get("id"),
                "domain": q.get("domain", ""),
                "question": q["question"],
                "options": q.get("options", []),
                "user_answer": [],
                "correct_answers": q.get("correct_answers", []),
                "explanation": q.get("explanation", ""),
                "unanswered": True,
            })

    wrong_items.sort(key=lambda x: x["index"])
    percentage = (correct_count / total * 100.0) if total > 0 else 0.0
    passed = percentage >= MOCK_EXAM_PASS_PERCENT

    return {
        "total": total,
        "correct_count": correct_count,
        "answered_count": answered_count,
        "percentage": round(percentage, 1),
        "passed": passed,
        "domain_stats": domain_stats,
        "wrong_items": wrong_items,
    }