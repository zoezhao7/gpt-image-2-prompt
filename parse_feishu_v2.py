#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析 GPT Image 2 100组Prompt合集.md
飞书图片需要鉴权，无法直接下载，先提取文本和URL，标记需要手动处理的图片
"""

import re, json, os

MD_PATH = r'C:\Users\Administrator\Downloads\GPT Image 2全球开放使用!100组Prompt合集.md'
OUT_JSON = r'C:\Users\Administrator\WorkBuddy\2026-05-31-10-53-55\gpt-image-prompts\data\feishu-100-cases.json'

with open(MD_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total lines: {len(lines)}')

# 数据结构
categories = []   # 主分类列表
results = []      # 所有条目
current_cat = '未知'
current_entry = None
in_code_block = False
code_lang = ''
code_buffer = []

def save_entry():
    global current_entry
    if current_entry:
        if current_entry['prompt'] or current_entry['image_urls']:
            results.append(current_entry)
        current_entry = None

i = 0
while i < len(lines):
    raw = lines[i]
    line = raw.strip()

    # 代码块边界检测
    if line.startswith('```'):
        if not in_code_block:
            in_code_block = True
            code_lang = line[3:].strip()
            code_buffer = []
            i += 1
            continue
        else:
            # 结束代码块
            in_code_block = False
            if current_entry and code_buffer:
                prompt_text = '\n'.join(code_buffer).strip()
                if prompt_text and len(prompt_text) > 20:
                    current_entry['prompt'] = prompt_text
            code_buffer = []
            i += 1
            continue

    if in_code_block:
        code_buffer.append(raw.rstrip('\n').rstrip('\r'))
        i += 1
        continue

    # 主分类 ## 01-人像写真
    if re.match(r'^##\s+', line):
        save_entry()
        current_cat = re.sub(r'^##\s+', '', line).strip()
        if current_cat not in categories:
            categories.append(current_cat)
            print(f'  [分类] {current_cat}')
        i += 1
        continue

    # 条目标题（多种格式）
    # 格式1: ### **1001.** 室内棚拍...
    # 格式2: ### **1001.** 室内棚拍...（无Vol标记）
    # 格式3: ### 1001. 室内棚拍...
    entry_patterns = [
        r'^\*{0,2}(\d{4,5})\.{0,1}\*{0,2}\s+(.+)',   # ### 之后 **1001.** 标题
    ]
    # 直接尝试提取数字开头的标题行
    cleaned = re.sub(r'^\#{1,4}\s+', '', line)  # 去掉 ### 等
    cleaned = re.sub(r'[\*]{1,2}', '', cleaned)           # 去掉粗体标记
    m = re.match(r'^(\d{4,5})\.?\s+(.+)', cleaned)
    if m:
        save_entry()
        num = int(m.group(1))
        title = m.group(2).strip()
        # 去掉末尾的 (Vol:...) 等标记
        title = re.sub(r'\(Vol[:\s]*[\d\.]+\)', '', title).strip()
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

    # 图片链接 ![Image](url)
    img_m = re.match(r'!\[Image\]\((.+?)\)', line)
    if img_m and current_entry:
        url = img_m.group(1).strip()
        current_entry['image_urls'].append(url)
        i += 1
        continue

    i += 1

save_entry()

print(f'\n=== 解析完成 ===')
print(f'总条目数: {len(results)}')
print(f'分类数: {len(categories)}')
for c in categories:
    cnt = sum(1 for r in results if r['category'] == c)
    print(f'  {c}: {cnt}')

has_prompt = sum(1 for r in results if r['prompt'])
has_image = sum(1 for r in results if r['image_urls'])
print(f'\n有提示词: {has_prompt}/{len(results)}')
print(f'有图片URL: {has_image}/{len(results)}')

# 查看前几条
print('\n=== 前5条样本 ===')
for r in results[:5]:
    print(f"  #{r['id']} [{r['category']}] {r['title'][:40]}")
    print(f"    提示词: {r['prompt'][:80] if r['prompt'] else '(无)'}")
    print(f"    图片数: {len(r['image_urls'])}")
    if r['image_urls']:
        print(f"    图片URL示例: {r['image_urls'][0][:80]}...")

# 保存JSON
os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
with open(OUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f'\n保存至: {OUT_JSON}')
print(f'文件大小: {os.path.getsize(OUT_JSON)/1024:.1f} KB')
