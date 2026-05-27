# -*- coding: utf-8 -*-
import json
from data.single_choice import SINGLE_CHOICE_QUESTIONS
from data.multi_choice import MULTI_CHOICE_QUESTIONS

modified_ids = ['S35','S56','S82','S05','S13','S15','S25','S128','S138']

all_questions = SINGLE_CHOICE_QUESTIONS + MULTI_CHOICE_QUESTIONS
modified_questions = [q for q in all_questions if q['id'] in modified_ids]

with open('modified_questions_current.json', 'w', encoding='utf-8') as f:
    json.dump(modified_questions, f, ensure_ascii=False, indent=2)

print(f"Saved current state of {len(modified_questions)} modified questions.")
for q in sorted(modified_questions, key=lambda x: x['id']):
    print(f"  {q['id']}")
