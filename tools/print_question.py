#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick helper: print full question by ID (single or multi).
Usage:
  python tools/print_question.py S24
  python tools/print_question.py M70
"""
import sys
import json
from data.single_choice import SINGLE_CHOICE_QUESTIONS
from data.multi_choice import MULTI_CHOICE_QUESTIONS

ALL = {q["id"]: q for q in SINGLE_CHOICE_QUESTIONS}
ALL.update({q["id"]: q for q in MULTI_CHOICE_QUESTIONS})

def print_question(qid):
    q = ALL.get(qid)
    if not q:
        print(f"Question {qid} not found!")
        return
    print("=" * 70)
    print(f"[{q['id']}] {q.get('domain','')}  |  {'单选' if len(q.get('correct_answers',[]))==1 else '多选'}")
    print(f"题干: {q['question']}")
    print("选项:")
    for i, opt in enumerate(q["options"]):
        letter = chr(ord("A") + i)
        mark = "✓" if letter in q.get("correct_answers", []) else "✗"
        print(f"  {letter}. {mark}  {opt}")
    print("\n解析 (前300字预览):")
    exp = q.get("explanation", "")
    print(exp[:300] + ("..." if len(exp) > 300 else ""))
    print("=" * 70)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print_question(sys.argv[1].upper())
    else:
        print("Usage: python tools/print_question.py S24")
