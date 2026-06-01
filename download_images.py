#!/usr/bin/env python3
"""
批量下载 GPT-Image-2 案例效果图
URL规律: https://gpt-image2.canghe.ai/images/case{id}.jpg
支持断点续传、错误重试、进度显示
"""

import urllib.request
import json
import os
import time
import sys

OUT_DIR = r'C:\Users\Administrator\WorkBuddy\2026-05-31-10-53-55\gpt-image-prompts\images'
CASES_JSON = r'C:\Users\Administrator\WorkBuddy\2026-05-31-10-53-55\gpt-image-prompts\data\cases-full.json'
BASE_URL = 'https://gpt-image2.canghe.ai/images/case{}.jpg'

# 配置
MAX_RETRIES = 3
DELAY = 0.3  # 请求间隔(秒)
TIMEOUT = 15

def load_existing():
    """加载已下载的文件，返回 {id: filesize}"""
    existing = {}
    if not os.path.exists(OUT_DIR):
        return existing
    for fname in os.listdir(OUT_DIR):
        if fname.startswith('case') and fname.endswith('.jpg'):
            try:
                case_id = int(fname[4:-4])  # case123.jpg -> 123
                fpath = os.path.join(OUT_DIR, fname)
                existing[case_id] = os.path.getsize(fpath)
            except (ValueError, OSError):
                continue
    return existing

def download_case(case_id, retries=0):
    """下载单个案例图片，返回 (success, size_bytes)"""
    url = BASE_URL.format(case_id)
    fpath = os.path.join(OUT_DIR, f'case{case_id}.jpg')
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://gpt-image2.canghe.ai/',
            'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
        })
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = resp.read()
            with open(fpath, 'wb') as f:
                f.write(data)
            return True, len(data)
    except Exception as e:
        code = getattr(e, 'code', None)
        if code == 404:
            print(f'  [404] case{case_id} not found on server, skipping')
            # 创建一个占位符标记文件，避免反复重试
            with open(fpath + '.missing', 'w') as f:
                f.write('404')
            return False, 0
        if retries < MAX_RETRIES - 1:
            time.sleep(DELAY * 2)
            return download_case(case_id, retries + 1)
        else:
            print(f'  [ERR] case{case_id}: {e}')
            return False, 0

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # 加载案例ID列表
    with open(CASES_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    case_ids = [c['id'] for c in data.get('cases', [])]
    total = len(case_ids)
    
    # 加载已下载的
    existing = load_existing()
    missing_ids = [i for i in range(1, total + 1) if i not in existing]
    
    # 还要检查 .missing 标记文件（404的）
    missing_marked = set()
    for fname in os.listdir(OUT_DIR):
        if fname.endswith('.jpg.missing'):
            try:
                missing_marked.add(int(fname[4:-11]))
            except ValueError:
                pass
    
    to_download = [i for i in range(1, total + 1) 
                   if i not in existing and i not in missing_marked]
    
    print(f'=== GPT-Image-2 案例图片下载 ===')
    print(f'总计案例: {total}')
    print(f'已下载: {len(existing)}')
    print(f'需下载: {len(to_download)}')
    if missing_marked:
        print(f'已知404: {len(missing_marked)} (已标记，跳过)')
    print()
    
    if not to_download:
        print('全部已下载，无需操作！')
        return
    
    success = 0
    failed = 0
    total_size = 0
    t0 = time.time()
    
    for i, case_id in enumerate(to_download, 1):
        ok, size = download_case(case_id)
        if ok:
            success += 1
            total_size += size
        else:
            failed += 1
        
        # 进度显示
        if i % 20 == 0 or i == len(to_download):
            elapsed = time.time() - t0
            speed = total_size / 1024 / elapsed if elapsed > 0 else 0
            pct = i / len(to_download) * 100
            print(f'  [{i}/{len(to_download)} {pct:.0f}%] '
                  f'成功:{success} 失败:{failed} '
                  f'已下载:{total_size/1024/1024:.1f}MB 速度:{speed:.0f}KB/s')
        
        time.sleep(DELAY)
    
    elapsed = time.time() - t0
    print()
    print(f'=== 下载完成 ===')
    print(f'成功: {success}/{len(to_download)}')
    print(f'失败: {failed}')
    print(f'总大小: {total_size/1024/1024:.1f} MB')
    print(f'耗时: {elapsed:.0f}s')
    print(f'本地路径: {OUT_DIR}')

if __name__ == '__main__':
    main()
