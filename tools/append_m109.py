# -*- coding: utf-8 -*-
import json

with open('data/multi_choice.py', 'r', encoding='utf-8') as f:
    content = f.read()

s102 = json.load(open('s102_as_m109.json', encoding='utf-8'))

def fmt(q):
    lines = ['    {']
    for k in ['id','question','options','correct_answers','explanation','domain']:
        v = q[k]
        if isinstance(v, str):
            esc = v.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            lines.append(f'        "{k}": "{esc}",')
        else:
            lines.append(f'        "{k}": [')
            for item in v:
                esc = item.replace('\\', '\\\\').replace('"', '\\"')
                lines.append(f'            "{esc}",')
            lines.append('        ],')
    lines.append('    },')
    return '\n'.join(lines)

new_block = '\n' + fmt(s102) + '\n'

if content.rstrip().endswith(']'):
    new_content = content.rstrip()[:-1].rstrip() + new_block + ']\n'
else:
    print('格式异常')
    exit(1)

with open('data/multi_choice.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('M109 已成功加入 multi_choice.py')
