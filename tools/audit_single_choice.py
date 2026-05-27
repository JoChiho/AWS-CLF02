# -*- coding: utf-8 -*-
"""Quick audit of single-choice explanation quality."""
from data.single_choice import SINGLE_CHOICE_QUESTIONS

lengths = []
weak = []
good = []

for q in SINGLE_CHOICE_QUESTIONS:
    exp = q.get("explanation", "")
    length = len(exp)
    lengths.append(length)
    
    # Simple heuristic for "weak" explanations
    has_wrong_analysis = any(kw in exp for kw in ["是错误的", "不是", "陷阱", "常见误区", "注意", "错误选项"])
    
    if length < 70 or not has_wrong_analysis:
        weak.append((q["id"], exp[:90]))
    else:
        good.append(q["id"])

print("=" * 70)
print("SINGLE-CHOICE EXPLANATION QUALITY AUDIT")
print("=" * 70)
print(f"Total questions: {len(SINGLE_CHOICE_QUESTIONS)}")
print(f"Average explanation length: {sum(lengths)/len(lengths):.0f} characters")
print(f"Weak / short explanations (need improvement): {len(weak)}")
print(f"Better explanations: {len(good)}")
print()

print("Sample of weak/short explanations:")
for qid, preview in weak[:8]:
    print(f"  {qid}: {preview}...")
    print()

print(f"\nIDs needing significant improvement: {[w[0] for w in weak]}")