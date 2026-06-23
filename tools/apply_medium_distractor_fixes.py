# -*- coding: utf-8 -*-
"""
将 tools/medium_distractor_fixes.json 中的干扰项修复应用到题库源文件。

规则：
- 正确选项文本不得改动（脚本会校验）
- 仅更新 options 与 explanation
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from data.single_choice import SINGLE_CHOICE_QUESTIONS
from data.multi_choice import MULTI_CHOICE_QUESTIONS

FIXES_PATH = ROOT / "tools" / "medium_distractor_fixes.json"
SINGLE_PATH = ROOT / "data" / "single_choice.py"
MULTI_PATH = ROOT / "data" / "multi_choice.py"

SINGLE_HEADER = '''# -*- coding: utf-8 -*-
"""Single Choice Questions

Stable IDs: S01 ~ Sxxx (used for progress tracking & wrong book)"""

SINGLE_CHOICE_QUESTIONS = [
'''

MULTI_HEADER = '''# -*- coding: utf-8 -*-
"""Multi Choice Questions

Stable IDs: M01 ~ Mxxx (used for progress tracking & wrong book)"""

MULTI_CHOICE_QUESTIONS = [
'''


def _validate_fix(q: dict, fix: dict) -> None:
    qid = q["id"]
    old_opts = q["options"]
    new_opts = fix["options"]
    correct = set(q["correct_answers"])

    if len(old_opts) != len(new_opts):
        raise ValueError(f"{qid}: option count mismatch {len(old_opts)} vs {len(new_opts)}")

    for i, (old, new) in enumerate(zip(old_opts, new_opts)):
        letter = chr(ord("A") + i)
        if letter in correct and old != new:
            raise ValueError(f"{qid}: correct option {letter} changed\n  old: {old}\n  new: {new}")


def _format_question(q: dict) -> str:
    lines = [
        "    {",
        f'        "id": {json.dumps(q["id"], ensure_ascii=False)},',
        f'        "question": {json.dumps(q["question"], ensure_ascii=False)},',
        '        "options": [',
    ]
    for opt in q["options"]:
        lines.append(f"            {json.dumps(opt, ensure_ascii=False)},")
    lines.append("        ],")
    lines.append('        "correct_answers": [')
    for letter in q["correct_answers"]:
        lines.append(f"            {json.dumps(letter, ensure_ascii=False)},")
    lines.append("        ],")
    lines.append(f'        "explanation": {json.dumps(q["explanation"], ensure_ascii=False)},')
    lines.append(f'        "domain": {json.dumps(q["domain"], ensure_ascii=False)},')
    lines.append("    },")
    return "\n".join(lines)


def _write_bank(path: Path, header: str, questions: list[dict]) -> None:
    body = "\n".join(_format_question(q) for q in questions)
    path.write_text(f"{header}{body}\n]\n", encoding="utf-8")


def _apply_fixes(questions: list[dict], fixes: dict) -> int:
    by_id = {q["id"]: q for q in questions}
    applied = 0
    for qid, fix in fixes.items():
        if qid not in by_id:
            continue
        q = by_id[qid]
        _validate_fix(q, fix)
        q["options"] = list(fix["options"])
        q["explanation"] = fix["explanation"]
        applied += 1
    return applied


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply medium distractor fixes to question bank")
    parser.add_argument("--dry-run", action="store_true", help="Validate only, do not write files")
    args = parser.parse_args()

    fixes = json.loads(FIXES_PATH.read_text(encoding="utf-8"))
    single = copy.deepcopy(SINGLE_CHOICE_QUESTIONS)
    multi = copy.deepcopy(MULTI_CHOICE_QUESTIONS)
    all_q = single + multi
    by_id = {q["id"]: q for q in all_q}

    missing = [qid for qid in fixes if qid not in by_id]
    if missing:
        raise SystemExit(f"Unknown question IDs in fixes: {missing}")

    for qid, fix in fixes.items():
        _validate_fix(by_id[qid], fix)

    print(f"Validated {len(fixes)} fixes")

    if args.dry_run:
        print("Dry run — no files written.")
        return

    s_count = _apply_fixes(single, fixes)
    m_count = _apply_fixes(multi, fixes)
    _write_bank(SINGLE_PATH, SINGLE_HEADER, single)
    _write_bank(MULTI_PATH, MULTI_HEADER, multi)
    print(f"Applied {s_count} single-choice + {m_count} multi-choice fixes")
    print(f"Rewrote {SINGLE_PATH.name} and {MULTI_PATH.name}")


if __name__ == "__main__":
    main()