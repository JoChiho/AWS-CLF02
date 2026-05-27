# -*- coding: utf-8 -*-
"""
Quiz 引擎模块（Quiz Engine）

包含：
- 运行一轮测试的核心逻辑
- 评分系统
- 错题收集与回顾
- 与解析器、数据层的解耦
"""

from typing import List, Dict, Any

from data import ALL_QUESTIONS, shuffle_question_options, get_shuffled_questions
from core.parser import parse_user_answers, is_quit_command


def _get_question_display(q: Dict[str, Any], index: int, total: int) -> str:
    """生成题目显示文本"""
    is_multi = len(q.get("correct_answers", [])) > 1
    hint = "（多选题）" if is_multi else ""
    domain = q.get("domain", "未分类")
    return f"【第 {index}/{total} 题】{q['question']} {hint}\n   领域：{domain}"


def _get_input_prompt(q: Dict[str, Any]) -> str:
    """根据题目类型返回不同的输入提示"""
    is_multi = len(q.get("correct_answers", [])) > 1
    if is_multi:
        return "\n请输入所有正确答案的字母（用空格或逗号分隔，例如：A C 或 B,D），输入 q 退出："
    else:
        return "\n你的答案（A/B/C/D），输入 q 退出："


def run_single_round() -> Dict[str, Any]:
    """
    运行一轮完整的测试，返回本轮统计结果。

    返回字典包含：
        - score: 得分
        - total: 总题数
        - percentage: 正确率
        - wrong_questions: 错题列表（用于回顾）
    """
    if not ALL_QUESTIONS:
        print("题库为空，无法开始测试。")
        return {"score": 0, "total": 0, "percentage": 0, "wrong_questions": []}

    # 随机打乱题目出题顺序（使用集中化工具）
    quiz_questions = get_shuffled_questions(ALL_QUESTIONS)

    score = 0
    wrong_questions = []

    total = len(quiz_questions)

    for i, q in enumerate(quiz_questions, 1):
        print("\n" + "=" * 70)
        print(_get_question_display(q, i, total))

        # 获取打乱后的选项视图
        shuffle_info = shuffle_question_options(q)
        display_opts = shuffle_info["shuffled_options"]
        display_to_original = shuffle_info["display_to_original"]
        original_to_display = shuffle_info["original_to_display"]
        display_correct = shuffle_info["display_correct_answers"]

        for opt in display_opts:
            print(f"   {opt}")

        prompt = _get_input_prompt(q)

        while True:
            raw = input(prompt).strip()
            if is_quit_command(raw):
                print("\n⚠️  已中途退出本轮测试。")
                return {
                    "score": score,
                    "total": total,
                    "percentage": (score / total * 100) if total > 0 else 0,
                    "wrong_questions": wrong_questions,
                    "early_exit": True
                }

            # 用户输入的是「显示字母」，先解析再转回原始字母用于比较
            display_answers = parse_user_answers(raw)
            user_answers = sorted(display_to_original.get(d, d) for d in display_answers)

            if display_answers or raw == "":  # 允许空输入（后续会判错）
                break
            print("❗ 输入无效，请输入字母（如 A 或 A C）")

        correct = q.get("correct_answers", [])
        if user_answers == correct:
            print("✅ 正确！")
            score += 1
        else:
            # 给用户展示时使用「显示字母」（更友好）
            user_display_str = "、".join(display_answers) if display_answers else "未作答"
            correct_display_str = "、".join(display_correct)
            print(f"❌ 错误！正确答案是：{correct_display_str}")
            print(f"   你输入的是：{user_display_str}")
            print(f"📝 解析：{q.get('explanation', '暂无解析')}")

            wrong_questions.append({
                "question": q["question"],
                "your_answer": user_display_str,
                "correct": correct_display_str,
                "explanation": q.get("explanation", "")
            })

    # 本轮结束统计
    percentage = (score / total * 100) if total > 0 else 0

    print("\n" + "=" * 70)
    print(f"🎯 本轮测试结束！得分：{score}/{total}")
    print(f"正确率：{percentage:.1f}%")

    if percentage >= 85:
        print("🎉 非常优秀！这个水平已经非常接近或超过 CLF-C02 真实考试要求！")
    elif percentage >= 75:
        print("👍 很好！继续保持，很有希望一次通过考试！")
    elif percentage >= 65:
        print("📈 及格边缘，再针对性复习薄弱领域即可。")
    else:
        print("💪 继续努力！重点看错题解析和官方 Exam Guide。")

    return {
        "score": score,
        "total": total,
        "percentage": percentage,
        "wrong_questions": wrong_questions,
        "early_exit": False
    }


def review_wrong_questions(wrong_questions: List[Dict]):
    """展示错题回顾"""
    if not wrong_questions:
        print("本轮没有错题，表现很好！")
        return

    print(f"\n本次共答错 {len(wrong_questions)} 题。")
    choice = input("是否查看本次所有错题及详细解析？(y/n)：").strip().lower()
    if choice != "y":
        return

    for idx, wq in enumerate(wrong_questions, 1):
        print(f"\n--- 错题 {idx} ---")
        print(f"题目：{wq['question']}")
        print(f"你的答案：{wq['your_answer']}   |   正确答案：{wq['correct']}")
        print(f"解析：{wq['explanation']}")


def get_performance_message(percentage: float) -> str:
    """根据正确率返回建议文案"""
    if percentage >= 85:
        return "🎉 太棒了！可以考虑预约考试了！"
    elif percentage >= 75:
        return "👍 继续保持，再刷几轮会更稳！"
    elif percentage >= 65:
        return "📈 及格线附近，重点攻克错题领域。"
    else:
        return "💪 多做几轮 + 重点看解析，进步会非常明显。"