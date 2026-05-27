# -*- coding: utf-8 -*-
import json

with open('option_length_issues.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"当前剩余需要处理的严重题目数量: {len(data)}")
print("\nTop 12 最严重的（按正确答案比干扰项长多少排序）：\n")
for i, item in enumerate(data[:12], 1):
    print(f"{i}. {item['id']} - 比例 {item['ratio']}x - 领域: {item['domain']}")
    print(f"   题目: {item['question']}")
    print(f"   最长选项长度: {item['longest_len']} | 平均干扰项: {item['avg_distractor_len']}")
    print()
