# -*- coding: utf-8 -*-
"""
一键修复题库分类错误：
- 把 SINGLE 中实际是多选的 5 道题移到 MULTI
- 分配新的 M105~M109 ID
- 保持 domain 等其他字段不变
- 写回两个数据文件
"""
import sys
import io
import re
from data.single_choice import SINGLE_CHOICE_QUESTIONS as SINGLE
from data.multi_choice import MULTI_CHOICE_QUESTIONS as MULTI

# 强制 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 要移动的原 ID
# 脚本会自动检测 SINGLE 中 correct_answers > 1 的题目并移动
# 新 ID 从当前 MULTI 最大 ID +1 开始分配

def format_question(q, indent=4):
    """把一个题目 dict 格式化为 Python 列表项的字符串"""
    lines = []
    sp = " " * indent
    lines.append(sp + "{")

    for key in ["id", "question", "options", "correct_answers", "explanation", "domain"]:
        val = q[key]
        if key in ("id", "question", "explanation", "domain"):
            # 字符串，注意内部引号和换行
            escaped = val.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
            lines.append(f'{sp}    "{key}": "{escaped}",')
        elif key in ("options", "correct_answers"):
            lines.append(f'{sp}    "{key}": [')
            for item in val:
                escaped_item = item.replace("\\", "\\\\").replace('"', '\\"')
                lines.append(f'{sp}        "{escaped_item}",')
            lines.append(f'{sp}    ],')
    lines.append(sp + "},")
    return "\n".join(lines)


def get_next_m_id(current_multi):
    """根据当前 MULTI 列表计算下一个可用的 M ID"""
    max_num = 0
    for q in current_multi:
        m = re.match(r"M(\d+)", q["id"])
        if m:
            max_num = max(max_num, int(m.group(1)))
    return max_num + 1


def main():
    print("开始自动修复题库分类...")

    # 1. 自动检测 SINGLE 中所有实际是多选的题目
    to_move = [q for q in SINGLE if len(q.get("correct_answers", [])) > 1]
    to_move.sort(key=lambda x: x["id"])

    if not to_move:
        print("没有检测到需要移动的题目，当前分类已是干净状态。")
        return

    print(f"检测到 {len(to_move)} 道放在 SINGLE 里但实际是多选的题目: {[q['id'] for q in to_move]}")

    # 2. 为它们分配连续的新 M ID
    next_id = get_next_m_id(MULTI)
    corrected = []
    for q in to_move:
        new_q = q.copy()
        new_q["id"] = f"M{next_id:03d}"
        corrected.append(new_q)
        print(f"  {q['id']} -> {new_q['id']}")
        next_id += 1

    # 3. 构建新列表
    to_move_ids = {q["id"] for q in to_move}
    new_single = [q for q in SINGLE if q["id"] not in to_move_ids]
    new_multi = MULTI + corrected

    print(f"\n新的 SINGLE 列表长度: {len(new_single)} (原 {len(SINGLE)})")
    print(f"新的 MULTI 列表长度: {len(new_multi)} (原 {len(MULTI)})")

    # 4. 写回 single_choice.py
    header = '''# -*- coding: utf-8 -*-
"""Single Choice Questions

Stable IDs: S01 ~ Sxxx (used for progress tracking & wrong book)"""

SINGLE_CHOICE_QUESTIONS = [
'''

    with open("data/single_choice.py", "w", encoding="utf-8") as f:
        f.write(header)
        for q in new_single:
            f.write(format_question(q, indent=4))
            f.write("\n")
        f.write("]\n")
    print("✓ 已写回 data/single_choice.py")

    # 5. 写回 multi_choice.py
    multi_header = '''# -*- coding: utf-8 -*-
"""Multi Choice Questions

Stable IDs: M01 ~ Mxxx (used for progress tracking & wrong book)"""

MULTI_CHOICE_QUESTIONS = [
'''

    with open("data/multi_choice.py", "w", encoding="utf-8") as f:
        f.write(multi_header)
        for q in new_multi:
            f.write(format_question(q, indent=4))
            f.write("\n")
        f.write("]\n")
    print("✓ 已写回 data/multi_choice.py")

    print("\n修复完成！建议立即运行 audit_question_bank.py 再次确认。")

if __name__ == "__main__":
    main()
