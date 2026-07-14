#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量重排 CloudCertPrep 题库「错误选项分析」分段格式（无需重新翻译）。

用法：
    python tools/reformat_cloudcertprep_explanations.py
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.explanation_utils import rebuild_explanation_text  # noqa: E402
from tools.import_cloudcertprep import write_question_file  # noqa: E402


def main() -> None:
    import data.cloudcertprep.single_choice as sc_mod
    import data.cloudcertprep.multi_choice as mc_mod

    importlib.reload(sc_mod)
    importlib.reload(mc_mod)

    singles = list(sc_mod.SINGLE_CHOICE_QUESTIONS)
    multis = list(mc_mod.MULTI_CHOICE_QUESTIONS)
    changed = 0

    for bucket in (singles, multis):
        for q in bucket:
            old = q.get("explanation", "")
            new = rebuild_explanation_text(
                old,
                q.get("options", []),
                q.get("correct_answers", []),
            )
            if new != old:
                q["explanation"] = new
                changed += 1

    out_single = ROOT / "data" / "cloudcertprep" / "single_choice.py"
    out_multi = ROOT / "data" / "cloudcertprep" / "multi_choice.py"

    write_question_file(
        out_single,
        "SINGLE_CHOICE_QUESTIONS",
        singles,
        title="CloudCertPrep CLF-C02 单选题库（自动生成，请勿手改）",
    )
    write_question_file(
        out_multi,
        "MULTI_CHOICE_QUESTIONS",
        multis,
        title="CloudCertPrep CLF-C02 多选题库（自动生成，请勿手改）",
    )

    print(f"完成：共 {len(singles) + len(multis)} 题，更新 {changed} 道解析格式。")


if __name__ == "__main__":
    main()