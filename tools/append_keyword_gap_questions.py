# -*- coding: utf-8 -*-
"""将 keyword_gap_questions.py 中的补题追加到题库。"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from data.single_choice import SINGLE_CHOICE_QUESTIONS
from data.multi_choice import MULTI_CHOICE_QUESTIONS
from tools.keyword_gap_questions import NEW_SINGLE, NEW_MULTI

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


def main() -> None:
    existing_ids = {q["id"] for q in SINGLE_CHOICE_QUESTIONS + MULTI_CHOICE_QUESTIONS}
    for q in NEW_SINGLE + NEW_MULTI:
        if q["id"] in existing_ids:
            raise SystemExit(f"Duplicate ID: {q['id']}")

    single = copy.deepcopy(SINGLE_CHOICE_QUESTIONS) + NEW_SINGLE
    multi = copy.deepcopy(MULTI_CHOICE_QUESTIONS) + NEW_MULTI
    _write_bank(SINGLE_PATH, SINGLE_HEADER, single)
    _write_bank(MULTI_PATH, MULTI_HEADER, multi)
    print(f"Added {len(NEW_SINGLE)} single + {len(NEW_MULTI)} multi = {len(NEW_SINGLE)+len(NEW_MULTI)} questions")
    print(f"New totals: {len(single)} single, {len(multi)} multi, {len(single)+len(multi)} total")


if __name__ == "__main__":
    main()