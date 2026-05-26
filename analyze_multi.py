from data.multi_choice import MULTI_CHOICE_QUESTIONS
import json

print("=== Multi Choice Bank Analysis ===\n")

# Find questions mentioning "three items"
print("=== Questions mentioning three items ===")
three_item_qs = []
for i, q in enumerate(MULTI_CHOICE_QUESTIONS):
    qtext = q.get('question', '')
    if '三项' in qtext or '选择三' in qtext:
        three_item_qs.append(i)
        correct = q.get('correct_answers', [])
        print(f"Index: {i}")
        print(f"Correct count: {len(correct)}")
        print(f"Correct: {correct}")
        print("---")

print(f"\nTotal questions mentioning three items: {len(three_item_qs)}")

# Find questions where explanation suggests more correct answers than listed
print("\n=== Potential mismatch (explanation suggests 3+ but data has fewer) ===")
mismatches = []
for i, q in enumerate(MULTI_CHOICE_QUESTIONS):
    correct = q.get('correct_answers', [])
    expl = q.get('explanation', '')
    
    # Count distinct letters mentioned as correct in explanation
    mentioned_letters = set()
    for letter in 'ABCDE':
        if letter in expl:
            # Very rough heuristic
            if any(phrase in expl for phrase in [f'{letter}、', f'{letter}正确', f'{letter}都']):
                mentioned_letters.add(letter)
    
    if len(mentioned_letters) >= 3 and len(correct) < 3:
        mismatches.append({
            'index': i,
            'question': q.get('question', '')[:120],
            'current_correct': correct,
            'explanation': expl[:300]
        })

print(f"Found {len(mismatches)} potential data issues")

with open('multi_choice_data_issues.json', 'w', encoding='utf-8') as f:
    json.dump(mismatches, f, ensure_ascii=False, indent=2)

print("Saved detailed issues to multi_choice_data_issues.json")

# Also save full summary
summary = []
for i, q in enumerate(MULTI_CHOICE_QUESTIONS):
    summary.append({
        'index': i,
        'correct_count': len(q.get('correct_answers', [])),
        'has_three_in_question': '三项' in q.get('question', '')
    })

with open('multi_choice_full_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print("Saved summary to multi_choice_full_summary.json")