# -*- coding: utf-8 -*-
"""
题库解析内容质量检查工具

用途：
- 检测多选题解析中是否仍然存在对原始选项字母（A-E）的依赖
- 防止未来新增或修改题目时重新引入字母依赖问题
- 支持长期维护

运行方式：
    python tools/check_explanations.py

如果检测到问题，会输出具体题目 ID 和问题片段，并以非零状态退出（适合 CI）。
"""

import re
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.multi_choice import MULTI_CHOICE_QUESTIONS
from data.single_choice import SINGLE_CHOICE_QUESTIONS


# 需要检测的字母依赖模式
LETTER_DEPENDENT_PATTERNS = [
    r"正确答案是 [A-E和、]+",           # "正确答案是 B 和 D"
    r"[A-E] 是错误的",                  # "A 是错误的"
    r"[A-E] 是正确的",                  # "B 是正确的"
    r"答案是 [A-E]",                    # "答案是 A"
    r"正确选项是 [A-E]",                # "正确选项是 B、C"
    r"正确答案 [A-E]、[A-E]",           # 一些简写形式
]


def find_letter_issues(text: str):
    """返回文本中所有匹配的字母依赖片段"""
    issues = []
    for pattern in LETTER_DEPENDENT_PATTERNS:
        matches = re.findall(pattern, text)
        issues.extend(matches)
    return issues


def check_questions(questions, question_type: str):
    """检查一组题目"""
    problems = []
    for q in questions:
        exp = q.get("explanation", "")
        issues = find_letter_issues(exp)
        if issues:
            problems.append({
                "id": q["id"],
                "issues": issues,
                "preview": exp[:150].replace("\n", " ")
            })
    return problems


def main():
    # Windows 控制台 UTF-8 兼容处理（必须在任何 print 之前）
    import sys
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 70)
    print("AWS CLF-C02 题库解析质量检查")
    print("=" * 70)

    # 检查多选题（重点）
    multi_problems = check_questions(MULTI_CHOICE_QUESTIONS, "multi")
    # 检查单选题（应该已经干净）
    single_problems = check_questions(SINGLE_CHOICE_QUESTIONS, "single")

    total_issues = len(multi_problems) + len(single_problems)

    if total_issues == 0:
        print("\n✅ 通过检查！所有解析内容均不依赖选项字母。")
        print("   打乱选项后用户阅读体验良好。")
        return 0

    print(f"\n❌ 发现 {total_issues} 道题目存在字母依赖问题：\n")

    if multi_problems:
        print(f"多选题（{len(multi_problems)} 道）：")
        for p in multi_problems:
            print(f"  - {p['id']}")
            print(f"    问题片段: {p['issues']}")
            print(f"    内容预览: {p['preview']}...\n")

    if single_problems:
        print(f"单选题（{len(single_problems)} 道）：")
        for p in single_problems:
            print(f"  - {p['id']}: {p['issues']}")

    print("-" * 70)
    print("建议：")
    print("  请将解析中的「A 是错误的」「正确答案是 B 和 D」等表述，")
    print("  改为直接引用选项完整文字，例如：")
    print('    「客户始终对所有安全负责」是错误的：...')
    print('    正确答案：')
    print('    「责任边界取决于使用的服务类型（IaaS/PaaS/SaaS）」')
    print('    「对于托管服务，AWS 承担更多运营责任」')
    print("-" * 70)

    return 1


if __name__ == "__main__":
    sys.exit(main())