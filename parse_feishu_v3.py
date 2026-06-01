#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析 GPT Image 2 100组Prompt合集.md
直接按行模式匹配，不依赖复杂正则
"""

import re, json, os

MD_PATH = r'C:\Users\Administrator\Downloads\GPT Image 2全球开放使用!100组Prompt合集.md'
OUT_JSON = r'C:\Users\Administrator\WorkBuddy\2026-05-31-10-53-55\gpt-image-prompts\data\feishu-100-cases.json'

with open(MD_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total lines: {len(lines)}')

results = []
current_cat = '未知'
current_entry = None
in_code = False
code_buffer = []
categories = []

def flush_code():
    global current_entry, code_buffer
    if current_entry and code_buffer:
        text = '\n'.join(code_buffer).strip()
        if len(text) > 10:
            current_entry['prompt'] = text
        code_buffer = []

def save_current():
    global current_entry
    flush_code()
    if current_entry:
        if current_entry['prompt'] or current_entry['image_urls']:
            results.append(current_entry)
        current_entry = None

i = 0
while i < len(lines):
    raw = lines[i]
    line = raw.strip()

    # 检测代码块开始/结束
    if line.startswith('```'):
        if not in_code:
            in_code = True
            code_buffer = []
        else:
            in_code = False
            flush_code()
        i += 1
        continue

    if in_code:
        code_buffer.append(raw.rstrip('\n').rstrip('\r'))
        i += 1
        continue

    # 主分类 ## 01-人像写真
    if line.startswith('##'):
        save_current()
        current_cat = line.lstrip('#').strip()
        if current_cat not in categories:
            categories.append(current_cat)
            print(f'  [分类] {current_cat}')
        i += 1
        continue

    # 条目标题：匹配 **1001.** 或 **1001.** 格式
    # 实际格式: ### **1001.** 标题
    if '**100' in line or ('100' in line and ('**' in line or '###' in line)):
        # 尝试提取编号
        # 匹配 **1001.** 或 **1001.**
        m = re.search(r'\*{0,2}(\d{4,5})\.{0,1}\*{0,2}', line)
        if m:
            num = int(m.group(1))
            # 提取标题：去掉 ### 和 ** 标记
            title = re.sub(r'^#{1,4}\s+', '', line)
            title = re.sub(r'[\*]{1,3}', '', title)
            title = re.sub(r'\(Vol[:\s]*[\d\.]+\)', '', title)
            title = title.strip()
            
            save_current()
            current_entry = {
                'id': num,
                'title': title,
                'category': current_cat,
                'prompt': '',
                'image_urls': [],
                'source': 'feishu-100'
            }
            print(f'  [条目] #{num} {title[:30]}')
        i += 1
        continue

    # 图片链接
    img_m = re.match(r'!\[Image\]\((.+?)\)', line)
    if img_m and current_entry:
        url = img_m.group(1).strip()
        current_entry['image_urls'].append(url)
        i += 1
        continue

    i += 1

save_current()

print(f'\n=== 解析完成 ===')
print(f'总条目数: {len(results)}')
print(f'分类数: {len(categories)}')

# 统计
cat_stats = {}
for r in results:
    cat = r['category']
    cat_stats[cat] = cat_stats.get(cat, 0) + 1
for cat, cnt in cat_stats.items():
    print(f'  {cat}: {cnt}')

has_prompt = sum(1 for r in results if r['prompt'])
has_image = sum(1 for r in results if r['image_urls'])
print(f'\n有提示词: {has_prompt}/{len(results)}')
print(f'有图片URL: {has_image}/{len(results)}')

# 样本
print('\n=== 前5条样本 ===')
for r in results[:5]:
    print(f"  #{r['id']} [{r['category'][:15]}] {r['title'][:35]}")
    print(f"    提示词: {(r['prompt'][:70] + '...') if r['prompt'] else '(无)'}")
    print(f"    图片数: {len(r['image_urls'])}")

# 保存
os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
with open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f'\n保存至: {OUT_JSON}')
print(f'文件大小: {os.path.getsize(OUT_JSON)/1024:.1f} KB')
