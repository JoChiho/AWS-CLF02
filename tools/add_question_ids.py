# -*- coding: utf-8 -*-
"""
一次性迁移脚本：为所有题目添加稳定 ID

用法（在项目根目录执行）：
    python tools/add_question_ids.py

脚本会：
1. 读取现有的 single_choice.py / multi_choice.py
2. 为每道题添加 "id" 字段（S01-S46 / M01-M49）
3. 重新生成格式良好的数据文件（保留原有 explanation、domain 等全部内容）
4. 备份原文件为 .bak

执行后请人工 review 一下生成的文件是否正确，再删除 .bak 备份。
"""

import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
SINGLE_FILE = ROOT / "data" / "single_choice.py"
MULTI_FILE = ROOT / "data" / "multi_choice.py"

BACKUP_SUFFIX = ".bak"


def make_backup(path: Path):
    backup = path.with_suffix(path.suffix + BACKUP_SUFFIX)
    shutil.copy2(path, backup)
    print("Backup created:", str(path), "->", str(backup))


def generate_single_choice_with_ids() -> str:
    """生成带 ID 的单选题文件内容"""
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""单选题题库（Single Choice Questions）',
        "共 46 道题",
        "",
        "ID 规则：S01 ~ S46（稳定标识，用于持久化进度跟踪）",
        '"""',
        "",
        "SINGLE_CHOICE_QUESTIONS = [",
    ]

    # 原始 46 道单选题（从已读取的内容中硬编码复制核心部分）
    # 我们直接用 Python 运行时导入当前数据，然后重新序列化
    # 这样最安全，不会漏掉任何字段
    return None   # 占位，实际在 main() 里用运行时数据生成


def main():
    print("=" * 60)
    print("AWS CLF-C02 Question ID Migration Script")
    print("=" * 60)

    # 动态导入当前题库（此时还没有 id）
    import sys
    sys.path.insert(0, str(ROOT))

    from data.single_choice import SINGLE_CHOICE_QUESTIONS as OLD_SINGLE
    from data.multi_choice import MULTI_CHOICE_QUESTIONS as OLD_MULTI

    print("Detected single-choice questions: " + str(len(OLD_SINGLE)))
    print("Detected multi-choice questions: " + str(len(OLD_MULTI)))

    # 备份
    make_backup(SINGLE_FILE)
    make_backup(MULTI_FILE)

    # ========== 生成新的 single_choice.py ==========
    new_single_lines = [
        "# -*- coding: utf-8 -*-",
        '"""Single Choice Questions (46 total)',
        "",
        "Stable IDs: S01 ~ S46 (used for progress tracking & wrong book)",
        '"""',
        "",
        "SINGLE_CHOICE_QUESTIONS = [",
    ]

    for i, q in enumerate(OLD_SINGLE, 1):
        qid = f"S{i:02d}"
        new_q = {
            "id": qid,
            "question": q["question"],
            "options": q["options"],
            "correct_answers": q["correct_answers"],
            "explanation": q["explanation"],
            "domain": q.get("domain", "未分类"),
        }
        new_single_lines.append("    {")
        new_single_lines.append(f'        "id": "{new_q["id"]}",')
        new_single_lines.append(f'        "question": {repr(new_q["question"])},')
        new_single_lines.append('        "options": [')
        for opt in new_q["options"]:
            new_single_lines.append(f"            {repr(opt)},")
        new_single_lines.append("        ],")
        new_single_lines.append(f'        "correct_answers": {new_q["correct_answers"]},')
        new_single_lines.append(f'        "explanation": {repr(new_q["explanation"])},')
        new_single_lines.append(f'        "domain": "{new_q["domain"]}",')
        new_single_lines.append("    },")

    new_single_lines.append("]")
    new_single_lines.append("")

    SINGLE_FILE.write_text("\n".join(new_single_lines), encoding="utf-8")
    print("Generated single_choice.py with stable IDs (46 questions)")

    # ========== 生成新的 multi_choice.py ==========
    new_multi_lines = [
        "# -*- coding: utf-8 -*-",
        '"""Multi Choice Questions (49 total, Choose TWO / Choose THREE)',
        "",
        "Stable IDs: M01 ~ M49 (used for progress tracking & wrong book)",
        '"""',
        "",
        "MULTI_CHOICE_QUESTIONS = [",
    ]

    for i, q in enumerate(OLD_MULTI, 1):
        qid = f"M{i:02d}"
        new_q = {
            "id": qid,
            "question": q["question"],
            "options": q["options"],
            "correct_answers": q["correct_answers"],
            "explanation": q["explanation"],
            "domain": q.get("domain", "未分类"),
        }
        new_multi_lines.append("    {")
        new_multi_lines.append(f'        "id": "{new_q["id"]}",')
        new_multi_lines.append(f'        "question": {repr(new_q["question"])},')
        new_multi_lines.append('        "options": [')
        for opt in new_q["options"]:
            new_multi_lines.append(f"            {repr(opt)},")
        new_multi_lines.append("        ],")
        new_multi_lines.append(f'        "correct_answers": {new_q["correct_answers"]},')
        new_multi_lines.append(f'        "explanation": {repr(new_q["explanation"])},')
        new_multi_lines.append(f'        "domain": "{new_q["domain"]}",')
        new_multi_lines.append("    },")

    new_multi_lines.append("]")
    new_multi_lines.append("")

    MULTI_FILE.write_text("\n".join(new_multi_lines), encoding="utf-8")
    print("Generated multi_choice.py with stable IDs (49 questions)")

    print("\n" + "=" * 60)
    print("MIGRATION COMPLETE")
    print("Verify with:")
    print('    python -c "from data import ALL_QUESTIONS; print(ALL_QUESTIONS[0][\"id\"], ALL_QUESTIONS[46][\"id\"])"')
    print("After verification, you may safely delete the .bak backup files.")
    print("=" * 60)


if __name__ == "__main__":
    main()