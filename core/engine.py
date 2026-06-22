# -*- coding: utf-8 -*-
"""
Quiz 引擎模块（Quiz Engine）

包含：
- 运行一轮测试的核心逻辑
- 评分系统
- 错题收集与回顾
- CLI 持久化（与 GUI 共用 data/progress.py）
"""

import time
from typing import List, Dict, Any, Optional

from data import ALL_QUESTIONS, shuffle_question_options, get_shuffled_questions
from data.progress import record_session, update_question_stat
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


def persist_round_result(
    mode: str,
    questions: List[Dict[str, Any]],
    answers_by_index: Dict[int, List[str]],
    start_time: float,
) -> Dict[str, Any]:
    """
    将一轮练习结果写入 user_data.json（与 GUI finish_quiz 逻辑一致）。

    answers_by_index: 0-based 题目索引 -> 用户答案（原始字母列表）
    """
    correct_count = 0
    answered_count = 0

    for i, q in enumerate(questions):
        user = answers_by_index.get(i, [])
        if user:
            answered_count += 1
            if set(user) == set(q.get("correct_answers", [])):
                correct_count += 1

    duration = int(time.time() - start_time) if start_time else 0
    total = len(questions)

    try:
        record_session(mode, total, correct_count, duration, answered=answered_count)
        for i, q in enumerate(questions):
            user_ans = answers_by_index.get(i, [])
            if not user_ans:
                continue
            qid = q.get("id")
            if not qid:
                continue
            is_correct = set(user_ans) == set(q.get("correct_answers", []))
            update_question_stat(qid, is_correct, user_ans)
        saved = True
    except Exception as e:
        print(f"[进度保存警告] {e}")
        saved = False

    answered_for_rate = answered_count if answered_count > 0 else 1
    percentage = (correct_count / answered_for_rate) * 100 if answered_count > 0 else 0.0

    return {
        "correct_count": correct_count,
        "answered_count": answered_count,
        "total": total,
        "percentage": percentage,
        "duration": duration,
        "saved": saved,
    }


def run_single_round(
    question_list: Optional[List[Dict[str, Any]]] = None,
    mode: str = "cli:all",
) -> Dict[str, Any]:
    """
    运行一轮完整的测试，返回本轮统计结果。

    参数：
        question_list: 题目列表，默认 ALL_QUESTIONS
        mode: 持久化会话模式标识（如 cli:all / cli:single）

    返回字典包含：
        - score: 得分
        - total: 总题数
        - percentage: 正确率（基于已回答题目）
        - wrong_questions: 错题列表（用于回顾）
        - early_exit: 是否中途退出
        - answered_count: 实际作答数
        - saved: 是否成功持久化
    """
    quiz_questions = get_shuffled_questions(question_list or ALL_QUESTIONS)

    if not quiz_questions:
        print("题库为空，无法开始测试。")
        return {
            "score": 0,
            "total": 0,
            "percentage": 0,
            "wrong_questions": [],
            "early_exit": False,
            "answered_count": 0,
            "saved": False,
        }

    start_time = time.time()
    answers_by_index: Dict[int, List[str]] = {}
    score = 0
    wrong_questions = []
    total = len(quiz_questions)

    for i, q in enumerate(quiz_questions, 1):
        print("\n" + "=" * 70)
        print(_get_question_display(q, i, total))

        shuffle_info = shuffle_question_options(q)
        display_opts = shuffle_info["shuffled_options"]
        display_to_original = shuffle_info["display_to_original"]
        display_correct = shuffle_info["display_correct_answers"]

        for opt in display_opts:
            print(f"   {opt}")

        prompt = _get_input_prompt(q)

        while True:
            raw = input(prompt).strip()
            if is_quit_command(raw):
                print("\n⚠️  已中途退出本轮测试。")
                summary = persist_round_result(mode, quiz_questions, answers_by_index, start_time)
                if summary["saved"]:
                    print("✓ 进度已自动保存（历史记录 + 错题统计）")
                answered = summary["answered_count"]
                pct = summary["percentage"] if answered > 0 else 0.0
                return {
                    "score": summary["correct_count"],
                    "total": total,
                    "percentage": pct,
                    "wrong_questions": wrong_questions,
                    "early_exit": True,
                    "answered_count": answered,
                    "saved": summary["saved"],
                }

            display_answers = parse_user_answers(raw)
            user_answers = sorted(display_to_original.get(d, d) for d in display_answers)

            if display_answers or raw == "":
                break
            print("❗ 输入无效，请输入字母（如 A 或 A C）")

        idx = i - 1
        if user_answers:
            answers_by_index[idx] = user_answers

        correct = q.get("correct_answers", [])
        if user_answers == correct:
            print("✅ 正确！")
            score += 1
        else:
            user_display_str = "、".join(display_answers) if display_answers else "未作答"
            correct_display_str = "、".join(display_correct)
            print(f"❌ 错误！正确答案是：{correct_display_str}")
            print(f"   你输入的是：{user_display_str}")
            print(f"📝 解析：{q.get('explanation', '暂无解析')}")

            wrong_questions.append({
                "id": q.get("id"),
                "question": q["question"],
                "your_answer": user_display_str,
                "correct": correct_display_str,
                "explanation": q.get("explanation", ""),
            })

    summary = persist_round_result(mode, quiz_questions, answers_by_index, start_time)
    if summary["saved"]:
        print("✓ 进度已自动保存（历史记录 + 错题统计）")

    percentage = summary["percentage"]
    correct_count = summary["correct_count"]
    answered_count = summary["answered_count"]

    print("\n" + "=" * 70)
    print(f"🎯 本轮测试结束！得分：{correct_count}/{answered_count or total}")
    print(f"正确率：{percentage:.1f}%（基于已回答题目）")
    print(get_performance_message(percentage))

    return {
        "score": correct_count,
        "total": total,
        "percentage": percentage,
        "wrong_questions": wrong_questions,
        "early_exit": False,
        "answered_count": answered_count,
        "saved": summary["saved"],
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
        qid = wq.get("id")
        if qid:
            print(f"ID：{qid}")
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