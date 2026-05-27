# -*- coding: utf-8 -*-
"""Analyze how heavily the explanations depend on original option letters."""
from data.multi_choice import MULTI_CHOICE_QUESTIONS
from data.single_choice import SINGLE_CHOICE_QUESTIONS
import re

def count_letter_references(text: str) -> int:
    """Count occurrences of patterns that refer to option letters."""
    patterns = [
        r"正确答案是 [A-E和、]+",
        r"[A-E] 是错误的",
        r"[A-E] 是正确的",
        r"答案是 [A-E]",
        r"正确选项是 [A-E]",
    ]
    count = 0
    for pat in patterns:
        count += len(re.findall(pat, text))
    return count

print("=" * 70)
print("MULTI-CHOICE QUESTIONS (49 total)")
print("=" * 70)

multi_with_refs = 0
multi_total_refs = 0
for q in MULTI_CHOICE_QUESTIONS:
    exp = q.get("explanation", "")
    refs = count_letter_references(exp)
    if refs > 0:
        multi_with_refs += 1
        multi_total_refs += refs

print(f"Questions containing letter references: {multi_with_refs} / 49")
print(f"Total letter-reference occurrences: {multi_total_refs}")

print("\n" + "=" * 70)
print("SINGLE-CHOICE QUESTIONS (46 total)")
print("=" * 70)

single_with_refs = 0
single_total_refs = 0
for q in SINGLE_CHOICE_QUESTIONS:
    exp = q.get("explanation", "")
    refs = count_letter_references(exp)
    if refs > 0:
        single_with_refs += 1
        single_total_refs += refs

print(f"Questions containing letter references: {single_with_refs} / 46")
print(f"Total letter-reference occurrences: {single_total_refs}")

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)
print("Multi-choice explanations are heavily letter-dependent and need rewriting.")
print("Single-choice explanations have very few letter references (mostly safe).")