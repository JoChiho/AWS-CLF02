# -*- coding: utf-8 -*-
"""
分析题库中选项长度分布，专门检测「选项太短导致正确答案容易被猜出」的问题。
这是 CLF-C02 题库质量的关键审计项：干扰项（distractors）必须有足够长度和 plausible 细节，
否则考生无需理解内容，仅凭“最长/最详细的那个”就能选对。
"""
import sys
import io
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data.single_choice import SINGLE_CHOICE_QUESTIONS
from data.multi_choice import MULTI_CHOICE_QUESTIONS

def analyze():
    all_questions = SINGLE_CHOICE_QUESTIONS + MULTI_CHOICE_QUESTIONS

    issues = []  # 所有有问题的题目

    for q in all_questions:
        options = q.get("options", [])
        correct_set = set(q.get("correct_answers", []))
        qid = q.get("id", "")
        domain = q.get("domain", "")

        if len(options) < 2:
            continue

        # 构建选项详情
        option_details = []
        for i, opt in enumerate(options):
            letter = chr(ord("A") + i)
            is_corr = letter in correct_set
            option_details.append({
                "letter": letter,
                "text": opt,
                "len": len(opt),
                "is_correct": is_corr
            })

        distractors = [o for o in option_details if not o["is_correct"]]
        corrects = [o for o in option_details if o["is_correct"]]

        if not distractors or not corrects:
            continue

        d_lens = [d["len"] for d in distractors]
        c_lens = [c["len"] for c in corrects]

        avg_d = sum(d_lens) / len(d_lens)
        max_c = max(c_lens)
        min_d = min(d_lens)
        max_d = max(d_lens)
        avg_c = sum(c_lens) / len(c_lens)

        # 短干扰项统计（<15 字通常是泛泛而谈，缺乏具体细节）
        very_short_d = [d for d in distractors if d["len"] < 15]
        short_d_count = len(very_short_d)
        ultra_short_d = [d for d in distractors if d["len"] < 10]

        # 核心指标
        ratio_maxc_avgd = max_c / avg_d if avg_d > 0 else 1.0
        ratio_maxc_mind = max_c / min_d if min_d > 0 else 1.0
        length_std = statistics.stdev([o["len"] for o in option_details]) if len(option_details) > 1 else 0

        # 判定逻辑：专门针对「选项太短导致容易选出正确答案」
        severity = None
        reasons = []

        # 1. 正确答案显著长于平均干扰项（最常见问题）
        if ratio_maxc_avgd >= 2.0:
            severity = "high"
            reasons.append(f"正确答案最长且长度是平均干扰项的 {ratio_maxc_avgd:.1f}x")
        elif ratio_maxc_avgd >= 1.6:
            severity = "medium" if not severity else severity
            reasons.append(f"正确答案明显长于干扰项 (ratio={ratio_maxc_avgd:.1f})")

        # 2. 存在多个极短的干扰项（<15 字），而正确答案有实质内容（>25 字）
        if short_d_count >= 2 and max_c >= 25:
            if not severity or severity == "medium":
                severity = "high" if short_d_count >= 3 else "medium"
            reasons.append(f"存在 {short_d_count} 个极短干扰项(<15字)，正确答案详细({max_c}字)")

        # 3. 存在超短干扰项（<10字，几乎无信息量）
        if len(ultra_short_d) >= 1 and max_c >= 30:
            severity = "high" if not severity else "high"
            reasons.append(f"存在超短干扰项(<10字): {[u['letter'] for u in ultra_short_d]}")

        # 4. 长度方差极大（选项质量严重不均衡）
        if length_std >= 20 and max_c >= 35:
            if severity != "high":
                severity = "medium"
            reasons.append(f"选项长度标准差过大 (std={length_std:.0f})，质量严重不均")

        # 5. 最小干扰项远短于最长正确（极端个案）
        if ratio_maxc_mind >= 3.0 and max_c >= 30:
            severity = "high"
            reasons.append(f"最长正确答案是最短干扰项的 {ratio_maxc_mind:.1f}x")

        if severity:
            # 保存完整选项以便人工复核
            full_opts = [{"letter": o["letter"], "text": o["text"], "len": o["len"], "is_correct": o["is_correct"]} for o in option_details]
            issues.append({
                "id": qid,
                "domain": domain,
                "question": q.get("question", ""),
                "severity": severity,
                "reasons": reasons,
                "metrics": {
                    "max_correct_len": max_c,
                    "avg_distractor_len": round(avg_d, 1),
                    "min_distractor_len": min_d,
                    "ratio_maxc_avgd": round(ratio_maxc_avgd, 2),
                    "short_distractor_count": short_d_count,
                    "length_std": round(length_std, 1)
                },
                "options": full_opts,
                "correct_answers": list(correct_set)
            })

    # 排序：先 high 再 medium，按 ratio 降序
    issues.sort(key=lambda x: (0 if x["severity"]=="high" else 1, -x["metrics"]["ratio_maxc_avgd"]))

    high_count = sum(1 for x in issues if x["severity"] == "high")
    med_count = len(issues) - high_count

    # ========== 控制台输出 ==========
    print("=" * 70)
    print("AWS CLF-C02 题库「选项长度/细节不均衡」专项审计报告")
    print("=" * 70)
    print(f"总题目数: {len(all_questions)}")
    print(f"发现问题题目: {len(issues)} 道 (High: {high_count}, Medium: {med_count})\n")

    print("【High 严重度】需要优先重写干扰项的题目（强烈建议修改）：")
    print("-" * 70)
    for i, item in enumerate([x for x in issues if x["severity"]=="high"][:15], 1):
        m = item["metrics"]
        print(f"{i}. [{item['id']}] {item['domain']} | 严重度: HIGH")
        print(f"   问题原因: {'; '.join(item['reasons'])}")
        print(f"   指标: 最长正确={m['max_correct_len']}字 | 平均干扰={m['avg_distractor_len']}字 | ratio={m['ratio_maxc_avgd']} | 短干扰数={m['short_distractor_count']}")
        print(f"   题目: {item['question'][:70]}...")
        print()

    print("\n【Medium 关注度】建议改善的题目：")
    print("-" * 70)
    for i, item in enumerate([x for x in issues if x["severity"]=="medium"][:10], 1):
        m = item["metrics"]
        print(f"{i}. [{item['id']}] {item['domain']}")
        print(f"   原因: {'; '.join(item['reasons'])}")
        print(f"   ratio={m['ratio_maxc_avgd']} | 短干扰={m['short_distractor_count']}")
        print()

    # ========== 导出 JSON（完整数据，便于后续脚本处理） ==========
    with open(ROOT / "option_length_issues.json", "w", encoding="utf-8") as f:
        json.dump(issues, f, ensure_ascii=False, indent=2)

    # ========== 生成人类可读的详细 TXT 报告 ==========
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("AWS CLF-C02 题库「选项太短导致正确答案容易被猜出」完整审计报告")
    report_lines.append(f"生成时间: 2026-05 (重新全面扫描)")
    report_lines.append("=" * 80)
    report_lines.append(f"\n总题数: 245 (单选136 + 多选109)")
    report_lines.append(f"发现问题: {len(issues)} 道 (High 严重: {high_count}, Medium 需关注: {med_count})")
    report_lines.append("\n【判定标准】")
    report_lines.append("  - High: 正确答案长度 >= 平均干扰项 2.0x, 或存在3个以上<15字短干扰项且正确>25字, 或存在<10字超短干扰")
    report_lines.append("  - Medium: 1.6x <= ratio < 2.0x, 或2个短干扰项, 或长度标准差过大")
    report_lines.append("\n【核心问题本质】")
    report_lines.append("  干扰项（错误选项）写得太短、太泛、太没细节，导致考生即使不知道正确答案是哪个，也能通过“挑最长最详细的”蒙对。")
    report_lines.append("  这违反了良好 MCQ 的基本原则：所有选项在长度、具体程度、语法结构上应该尽量接近。")
    report_lines.append("\n" + "=" * 80)

    for idx, item in enumerate(issues, 1):
        m = item["metrics"]
        sev = item["severity"].upper()
        report_lines.append(f"\n{idx}. [{item['id']}] {item['domain']}  【{sev}】")
        report_lines.append(f"   问题: {'; '.join(item['reasons'])}")
        report_lines.append(f"   指标: 正确最长={m['max_correct_len']} | 干扰平均={m['avg_distractor_len']} | 最小干扰={m['min_distractor_len']} | ratio={m['ratio_maxc_avgd']} | 短干扰数={m['short_distractor_count']} | 长度std={m['length_std']}")
        report_lines.append(f"   题干: {item['question']}")
        report_lines.append("   选项:")
        for o in item["options"]:
            flag = "✓正确" if o["is_correct"] else "✗干扰"
            report_lines.append(f"     {o['letter']}. [{o['len']:3d}字] {flag}  {o['text']}")
        report_lines.append("")

    report_lines.append("\n" + "=" * 80)
    report_lines.append("【建议修复优先级】")
    report_lines.append("1. 所有 HIGH 题目必须重写至少2-3个干扰项，使其长度接近正确答案，并增加具体细节/场景/限制条件。")
    report_lines.append("2. Medium 题目建议在下一轮迭代中改善。")
    report_lines.append("3. 理想状态：单选题4个选项长度差异控制在±8字以内；多选题选项长度差异控制在±12字。")
    report_lines.append("4. 错误选项应使用『具体但错误』的表述，而非『泛泛而正确但不完整』或『过于简短』。")
    report_lines.append("=" * 80)

    with open(ROOT / "option_length_audit_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"\n已导出:")
    print(f"  - option_length_issues.json (完整结构化数据，{len(issues)} 条)")
    print(f"  - option_length_audit_report.txt (人类可读完整报告，含所有选项原文)")
    print(f"\n强烈建议：优先打开 option_length_audit_report.txt 查看 HIGH 严重题目并逐一修复。")

if __name__ == "__main__":
    analyze()
