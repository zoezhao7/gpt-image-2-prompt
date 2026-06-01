#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析 GPT Image 2 100组Prompt合集.md
提取：编号、标题、分类、提示词文本、图片URL
"""

import re, json, os

MD_PATH = r'C:\Users\Administrator\Downloads\GPT Image 2全球开放使用!100组Prompt合集.md'
OUT_JSON = r'C:\Users\Administrator\WorkBuddy\2026-05-31-10-53-55\gpt-image-prompts\data\feishu-100-cases.json'

with open(MD_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
print(f'Total lines: {len(lines)}')

# 提取所有标题行（## 01-人像写真  / ### 1001.  ...）
# 先找主分类（## 开头）
categories = []
current_cat = '未知'
results = []
current_entry = None

i = 0
while i < len(lines):
    line = lines[i].strip()

    # 主分类 ## 01-人像写真
    if re.match(r'^##\s+\d+\\-', line):
        current_cat = re.sub(r'^##\s+', '', line).strip()
        print(f'  [分类] {current_cat}')
        i += 1
        continue

    # 条目 ### **1001.** 室内棚拍-烟雾缭绕(Vol:1)
    m = re.match(r'^###\s+\*{0,2}(\d{4,5})\.{0,1}\*{0,2}\s+(.+)', line)
    if not m:
        # 也支持没有 ### 只有 **1001.** 的行
        m2 = re.match(r'^\*{0,2}(\d{4,5})\.{0,1}\*{0,2}\s+(.+)', line)
        if m2:
            m = m2
    if m:
        num = m.group(1)
        title = m.group(2).strip().replace('*', '').replace('`', '').strip()
        # 保存上一个
        if current_entry:
            results.append(current_entry)
        current_entry = {
            'id': int(num),
            'title': title,
            'category': current_cat,
            'prompt': '',
            'image_urls': [],
            'source': 'feishu-100'
        }
        print(f'  [条目] #{num} {title}')
        i += 1
        continue

    # 代码块中的提示词
    if current_entry and line.startswith('```'):
        # 读取代码块内容
        lang = line[3:].strip()
        code_lines = []
        i += 1
        while i < len(lines) and not lines[i].strip().startswith('```'):
            code_lines.append(lines[i])
            i += 1
        prompt_text = '\n'.join(code_lines).strip()
        if prompt_text:
            current_entry['prompt'] = prompt_text
        i += 1  # skip closing ```
        continue

    # 图片链接 ![Image](url)
    img_m = re.match(r'!\[Image\]\((.+?)\)', line)
    if img_m and current_entry:
        url = img_m.group(1).strip()
        current_entry['image_urls'].append(url)
        i += 1
        continue

    i += 1

# 保存最后一个
if current_entry:
    results.append(current_entry)

print(f'\n=== 解析完成 ===')
print(f'总条目数: {len(results)}')

# 统计
cat_stats = {}
for r in results:
    cat = r['category']
    cat_stats[cat] = cat_stats.get(cat, 0) + 1
print(f'分类数: {len(cat_stats)}')
for cat, cnt in cat_stats.items():
    print(f'  {cat}: {cnt}')

# 检查提示词覆盖率
has_prompt = sum(1 for r in results if r['prompt'])
has_image = sum(1 for r in results if r['image_urls'])
print(f'有提示词: {has_prompt}/{len(results)}')
print(f'有图片URL: {has_image}/{len(results)}')

# 看看前几个条目的数据
print('\n=== 前3条样本 ===')
for r in results[:3]:
    print(f"  #{r['id']} [{r['category']}] {r['title'][:40]}")
    print(f"    提示词: {r['prompt'][:80]}...")
    print(f"    图片数: {len(r['image_urls'])}")
    if r['image_urls']:
        print(f"    图片URL: {r['image_urls'][0][:80]}...")

# 保存JSON
os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
with open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f'\n保存至: {OUT_JSON}')
print(f'文件大小: {os.path.getsize(OUT_JSON)/1024:.1f} KB')
