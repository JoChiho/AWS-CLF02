# -*- coding: utf-8 -*-
"""
全面审计题库分类和领域正确性
输出到控制台 + 保存到 JSON 文件
"""
import sys
import io
from data.single_choice import SINGLE_CHOICE_QUESTIONS as SINGLE
from data.multi_choice import MULTI_CHOICE_QUESTIONS as MULTI
from collections import Counter
import json

# 强制 stdout 使用 utf-8（Windows cp932 会乱码）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OFFICIAL_DOMAINS = {
    "Cloud Concepts",
    "Security and Compliance",
    "Technology and Services",
    "Billing, Pricing, and Support"
}

def audit():
    results = []

    def log(msg):
        print(msg)
        results.append(msg)

    log("=" * 80)
    log("AWS CLF-C02 题库全面审计报告")
    log("=" * 80)

    log(f"\n当前统计:")
    log(f"  SINGLE_CHOICE_QUESTIONS: {len(SINGLE)} 题")
    log(f"  MULTI_CHOICE_QUESTIONS:  {len(MULTI)} 题")
    log(f"  总计: {len(SINGLE) + len(MULTI)} 题")

    # 1. 单选/多选分类错误
    log("\n" + "=" * 80)
    log("【1. 单选/多选分类错误】")
    log("=" * 80)

    should_be_multi = [q for q in SINGLE if len(q.get("correct_answers", [])) > 1]
    log(f"\n放在 SINGLE 文件里，但实际是多选题 (correct_answers > 1): {len(should_be_multi)} 道")
    for q in should_be_multi:
        log(f"  {q['id']}: {q['correct_answers']} | {q['question'][:65]}...")

    should_be_single = [q for q in MULTI if len(q.get("correct_answers", [])) < 2]
    log(f"\n放在 MULTI 文件里，但实际是单选题 (correct_answers < 2): {len(should_be_single)} 道")
    for q in should_be_single:
        log(f"  {q['id']}: {q['correct_answers']} | {q['question'][:65]}...")

    # 2. 领域审计
    log("\n" + "=" * 80)
    log("【2. 考点领域（Domain）审计】")
    log("=" * 80)

    domain_count = Counter()
    invalid_domain_questions = []

    for q in SINGLE + MULTI:
        d = q.get("domain")
        domain_count[d] += 1
        if d not in OFFICIAL_DOMAINS:
            invalid_domain_questions.append(q)

    log("\n当前题库使用的领域分布：")
    for domain, count in sorted(domain_count.items(), key=lambda x: -x[1]):
        status = "✓ 官方" if domain in OFFICIAL_DOMAINS else "✗ 非官方/缺失"
        log(f"  {count:3d} 题 | {domain or 'MISSING'}  {status}")

    log(f"\n非官方或缺失领域的题目: {len(invalid_domain_questions)} 道")
    for q in invalid_domain_questions:
        log(f"  {q['id']}: domain=\"{q.get('domain')}\" | {q['question'][:60]}...")

    # 3. ID 重复
    log("\n" + "=" * 80)
    log("【3. ID 重复检查】")
    log("=" * 80)
    all_ids = [q["id"] for q in SINGLE + MULTI]
    dups = [k for k, v in Counter(all_ids).items() if v > 1]
    log(f"重复 ID: {dups if dups else '无'}")

    # 4. 汇总
    log("\n" + "=" * 80)
    log("【修复建议】")
    log("=" * 80)

    move_to_multi = [q["id"] for q in should_be_multi]
    move_to_single = [q["id"] for q in should_be_single]

    log(f"\n需要从 SINGLE 移到 MULTI 的题目 ({len(move_to_multi)} 道): {move_to_multi}")
    log(f"需要从 MULTI 移到 SINGLE 的题目 ({len(move_to_single)} 道): {move_to_single}")

    fix_domain_list = []
    for q in invalid_domain_questions:
        fix_domain_list.append({
            "id": q["id"],
            "current_domain": q.get("domain"),
            "question_preview": q["question"][:70]
        })

    log(f"\n需要修正 domain 的题目: {len(fix_domain_list)} 道")

    # 导出 JSON
    issues = {
        "move_single_to_multi_ids": move_to_multi,
        "move_multi_to_single_ids": move_to_single,
        "fix_domain_questions": fix_domain_list,
        "official_domains": list(OFFICIAL_DOMAINS)
    }
    with open("question_bank_audit_issues.json", "w", encoding="utf-8") as f:
        json.dump(issues, f, ensure_ascii=False, indent=2)

    log("\n详细问题已导出到: question_bank_audit_issues.json")
    return issues

if __name__ == "__main__":
    audit()
