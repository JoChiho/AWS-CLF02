#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将 CloudCertPrep 题库中的官方中文考试术语写成考试指南用词。"""
from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.aws_english_terms import restore_question_fields  # noqa: E402
from tools.import_cloudcertprep import write_question_file  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="套用官方中文考试术语")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    sc_mod = importlib.import_module("data.cloudcertprep.single_choice")
    mc_mod = importlib.import_module("data.cloudcertprep.multi_choice")
    singles = list(sc_mod.SINGLE_CHOICE_QUESTIONS)
    multis = list(mc_mod.MULTI_CHOICE_QUESTIONS)

    changed = 0
    samples: list[tuple[str, str, str]] = []
    for bucket in (singles, multis):
        for q in bucket:
            old_q = q.get("question", "")
            old_opts = list(q.get("options", []))
            old_exp = q.get("explanation", "")
            restore_question_fields(q)
            if (
                q.get("question") != old_q
                or q.get("options") != old_opts
                or q.get("explanation") != old_exp
            ):
                changed += 1
                if len(samples) < 8:
                    diff_opt = next(
                        (f"{a} -> {b}" for a, b in zip(old_opts, q["options"]) if a != b),
                        "",
                    )
                    samples.append((q["id"], old_q[:60], diff_opt[:80]))

    total = len(singles) + len(multis)
    print(f"共 {total} 题，更新 {changed} 题")
    for qid, stem, opt in samples:
        print(f"  {qid}: {stem}")
        if opt:
            print(f"       {opt}")

    if args.dry_run:
        return

    write_question_file(
        ROOT / "data" / "cloudcertprep" / "single_choice.py",
        "SINGLE_CHOICE_QUESTIONS",
        singles,
        title="CloudCertPrep CLF-C02 单选题库（自动生成，请勿手改）",
    )
    write_question_file(
        ROOT / "data" / "cloudcertprep" / "multi_choice.py",
        "MULTI_CHOICE_QUESTIONS",
        multis,
        title="CloudCertPrep CLF-C02 多选题库（自动生成，请勿手改）",
    )
    print("已写入 data/cloudcertprep/single_choice.py、multi_choice.py")


if __name__ == "__main__":
    main()
