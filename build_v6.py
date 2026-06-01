#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_v6.py - 生成带图片展示的 GPT-Image-2 提示词搜索引擎
正确处理中文、JS转义、图片路径
"""

import json, os, base64

BASE = r'C:\Users\Administrator\WorkBuddy\2026-05-31-10-53-55\gpt-image-prompts'
DATA = os.path.join(BASE, 'data')
IMG_DIR = os.path.join(BASE, 'images')

# 读取数据
with open(os.path.join(DATA, 'cases-full.json'), 'r', encoding='utf-8') as f:
    cases_data = json.load(f)

with open(os.path.join(DATA, 'templates.json'), 'r', encoding='utf-8') as f:
    tpl_data = json.load(f)

cases = cases_data.get('cases', [])
templates = tpl_data if isinstance(tpl_data, list) else tpl_data.get('templates', [])

print(f'案例: {len(cases)}, 模板: {len(templates)}')

# 检查本地图片
have_imgs = set()
missing_404 = set()

if os.path.exists(IMG_DIR):
    for fname in os.listdir(IMG_DIR):
        if fname.startswith('case') and fname.endswith('.jpg') and not fname.endswith('.missing'):
            try:
                have_imgs.add(int(fname[4:-4]))  # case123.jpg -> 123
            except ValueError:
                pass
        elif fname.endswith('.jpg.missing'):
            try:
                # case123.jpg.missing -> 123
                num = fname[4:-11]
                missing_404.add(int(num))
            except (ValueError, IndexError):
                pass

print(f'本地有图: {len(have_imgs)}, 已知404: {len(missing_404)}')
print(f'404 ID: {sorted(missing_404)[:20]}')

# 处理案例数据
processed_cases = []
for c in cases:
    cid = c['id']
    processed_cases.append({
        'id': cid,
        'title': c.get('title', ''),
        'prompt': c.get('prompt', ''),
        'promptPreview': c.get('promptPreview', ''),
        'category': c.get('category', ''),
        'styles': c.get('styles', []),
        'scenes': c.get('scenes', []),
        'featured': c.get('featured', False),
        'githubUrl': c.get('githubUrl', ''),
        'hasImage': cid in have_imgs,
        'is404': cid in missing_404,
    })

# 分类统计
categories = sorted(set(c['category'] for c in processed_cases if c['category']))
all_styles = sorted(set(s for c in processed_cases for s in c['styles']))
all_scenes = sorted(set(s for c in processed_cases for s in c['scenes']))

print(f'分类: {len(categories)}, 风格: {len(all_styles)}, 场景: {len(all_scenes)}')

# ========== 生成占位 SVG data URI ==========
def make_placeholder_svg(cid, title):
    """生成包含案例编号的占位 SVG（data URI 格式）"""
    short = title[:18] + '..' if len(title) > 20 else title
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300">'
        '<rect width="400" height="300" fill="#1a1a2e"/>'
        f'<text x="200" y="120" text-anchor="middle" fill="#7c5cfc" font-size="42" font-weight="bold">#{cid}</text>'
        '<text x="200" y="165" text-anchor="middle" fill="#888" font-size="13">图片缺失 / 404</text>'
        f'<text x="200" y="200" text-anchor="middle" fill="#666" font-size="11">{short}</text>'
        '</svg>'
    )
    b64 = base64.b64encode(svg.encode('utf-8')).decode('ascii')
    return f'data:image/svg+xml;base64,{b64}'

# 为所有 404 的案例预生成占位图 data URI
placeholder_map = {}
for c in processed_cases:
    if not c['hasImage']:
        placeholder_map[c['id']] = make_placeholder_svg(c['id'], c['title'])

# ========== 序列化数据（嵌入 HTML）==========
def safe_js_str(s):
    """转义字符串用于 JS 字符串字面量（单引号包裹）"""
    if not s:
        return "'
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '')

def dict_to_js(obj, depth=0):
    """将 Python 对象转为 JS 字面量（处理中文）"""
    if isinstance(obj, str):
        return "'" + safe_js_str(obj) + "'"
    elif isinstance(obj, bool):
        return 'true' if obj else 'false'
    elif isinstance(obj, (int, float)):
        return str(obj)
    elif isinstance(obj, list):
        items = [dict_to_js(x, depth+1) for x in obj]
        return '[' + ','.join(items) + ']'
    elif isinstance(obj, dict):
        pairs = []
        for k, v in obj.items():
            pairs.append("'" + safe_js_str(str(k)) + "':" + dict_to_js(v, depth+1))
        return '{' + ','.join(pairs) + '}'
    elif obj is None:
        return 'null'
    else:
        return str(obj)

# 只嵌入有图/404 标记，不嵌入完整 prompt（太大）
# 用两个 JS 变量：CASES_META（元信息）和 PROMPTS（ID->prompt 映射）
cases_meta = []
for c in processed_cases:
    cases_meta.append({
        'id': c['id'],
        't': c['title'],
        'c': c['category'],
        's': c['styles'],
        'sc': c['scenes'],
        'f': c['featured'],
        'h': c['hasImage'],
        'i404': c['is404'],
    })

# prompts 单独存（ID->prompt）
prompt_map = {c['id']: c['prompt'] for c in processed_cases}
prompt_preview_map = {c['id']: c.get('promptPreview','') for c in processed_cases}

# 序列化为 JS
cases_meta_js = 'const CASES_META = ' + json.dumps(cases_meta, ensure_ascii=False) + ';\n'
prompt_map_js = 'const PROMPTS = ' + json.dumps(prompt_map, ensure_ascii=False) + ';\n'
preview_map_js = 'const PREVIEW = ' + json.dumps(prompt_preview_map, ensure_ascii=False) + ';\n'

# 模板数据
tpl_js = 'const TEMPLATES = ' + json.dumps(templates, ensure_ascii=False) + ';\n'

# 占位图映射（只存 404 的）
ph_map_js = 'const PLACEHOLDERS = ' + json.dumps(placeholder_map, ensure_ascii=False) + ';\n'

print(f'CASES_META: {len(cases_meta)} 条')
print(f'PROMPTS: {len(prompt_map)} 条')
print(f'PLACEHOLDERS: {len(placeholder_map)} 条')

# ========== 生成 HTML ==========
html_template = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GPT-Image-2 提示词搜索引擎 🔍</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f0f23;--bg2:#1a1a2e;--bg3:#25253e;
  --accent:#7c5cfc;--accent2:#a78bfa;--green:#34d399;
  --text:#e2e8f0;--text2:#94a3b8;--border:#2d2d4a;
  --radius:12px;
}
body{font-family:-apple-system,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}

/* Header */
.header{background:var(--bg2);border-bottom:1px solid var(--border);padding:12px 20px;display:flex;align-items:center;gap:12px;position:sticky;top:0;z-index:100;flex-wrap:wrap;}
.logo{font-size:18px;font-weight:800;background:linear-gradient(135deg,var(--accent),#f472b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;white-space:nowrap;}
.sb{flex:1;max-width:540px;position:relative;}
.sb-i{position:absolute;left:12px;top:50%;transform:translateY(-50%);color:var(--text2);font-size:13px;pointer-events:none;}
.sb input{width:100%;padding:8px 12px 8px 34px;background:var(--bg3);border:1px solid var(--border);border-radius:20px;color:var(--text);font-size:13px;outline:none;transition:all .2s;}
.sb input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(124,92,252,.15);}
.stats{font-size:11px;color:var(--text2);white-space:nowrap;}
.mt{display:flex;background:var(--bg3);border-radius:8px;padding:2px;gap:2px;}
.mt button{padding:5px 11px;border:none;border-radius:6px;background:transparent;color:var(--text2);font-size:12px;cursor:pointer;transition:all .2s;white-space:nowrap;}
.mt button.active{background:var(--accent);color:#fff;font-weight:600;}

/* Filters */
.filters{background:var(--bg2);border-bottom:1px solid var(--border);padding:8px 20px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;}
.fg{display:flex;align-items:center;gap:5px;}
.fg label{font-size:11px;color:var(--text2);white-space:nowrap;}
.fg select{padding:4px 20px 4px 8px;background:var(--bg3);border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:12px;cursor:pointer;appearance:none;-webkit-appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='8' height='5'%3E%3Cpath d='M0 0l4 5 4-5z' fill='%2394a3b8'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 6px center;}
.fg select:focus{outline:none;border-color:var(--accent);}
.chip{padding:3px 10px;border-radius:14px;border:1px solid var(--border);background:var(--bg3);color:var(--text2);font-size:11px;cursor:pointer;transition:all .2s;user-select:none;}
.chip.active{background:var(--accent);color:#fff;border-color:var(--accent);}

/* Grid */
.container{max-width:1440px;margin:0 auto;padding:20px;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:16px;}
.card{background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:all .25s;cursor:pointer;display:flex;flex-direction:column;}
.card:hover{border-color:var(--accent);transform:translateY(-3px);box-shadow:0 8px 28px rgba(124,92,252,.15);}
.ciw{width:100%;height:200px;overflow:hidden;background:var(--bg3);display:flex;align-items:center;justify-content:center;position:relative;}
.ciw img{width:100%;height:100%;object-fit:cover;display:block;}
.ciw .noimg{text-align:center;color:var(--text2);font-size:12px;padding:8px;}
.cb{padding:10px 12px 12px;flex:1;display:flex;flex-direction:column;}
.ct{font-size:12px;font-weight:600;margin-bottom:4px;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
.cm{display:flex;gap:3px;flex-wrap:wrap;margin-bottom:5px;}
.tag{padding:1px 5px;border-radius:4px;font-size:10px;line-height:1.7;}
.tag.cat{background:rgba(124,92,252,.15);color:var(--accent2);}
.tag.stl{background:rgba(52,211,153,.12);color:var(--green);}
.cp{font-size:11px;color:var(--text2);line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-bottom:6px;flex:1;}
.ca{display:flex;gap:5px;margin-top:auto;}
.btn-copy{flex:1;padding:4px 8px;border-radius:6px;border:1px solid var(--accent);background:transparent;color:var(--accent);font-size:10px;cursor:pointer;transition:all .2s;text-align:center;}
.btn-copy:hover{background:var(--accent);color:#fff;}
.btn-view{padding:4px 8px;border-radius:6px;border:1px solid var(--border);background:transparent;color:var(--text2);font-size:10px;cursor:pointer;transition:all .2s;}
.btn-view:hover{border-color:var(--accent);color:var(--accent);}

.empty{text-align:center;padding:60px 20px;color:var(--text2);display:none;}
.empty .ic{font-size:40px;margin-bottom:12px;}
.empty p{font-size:14px;}

/* Modal */
.mo{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.88);z-index:1000;overflow-y:auto;}
.mo.open{display:flex;align-items:flex-start;justify-content:center;padding:30px 16px;}
.modal{background:var(--bg2);border-radius:var(--radius);max-width:900px;width:100%;overflow:hidden;margin-bottom:30px;}
.miw{width:100%;max-height:460px;overflow:hidden;background:#000;display:flex;align-items:center;justify-content:center;}
.miw img{width:100%;height:auto;max-height:460px;object-fit:contain;display:block;}
.miw .noimg-m{color:var(--text2);padding:30px;text-align:center;font-size:13px;}
.mb{padding:18px 20px 20px;}
.mt2{font-size:17px;font-weight:700;margin-bottom:10px;line-height:1.4;}
.mm{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px;}
.mp{background:var(--bg3);border-radius:8px;padding:13px;font-size:12px;line-height:1.7;color:var(--text);white-space:pre-wrap;word-break:break-all;max-height:360px;overflow-y:auto;font-family:'Courier New',monospace;margin-bottom:12px;}
.ma{display:flex;gap:10px;}
.bp{padding:7px 16px;border-radius:8px;border:none;background:var(--accent);color:#fff;font-size:13px;font-weight:600;cursor:pointer;transition:all .2s;}
.bp:hover{opacity:.88;}
.bs{padding:7px 16px;border-radius:8px;border:1px solid var(--border);background:transparent;color:var(--text);font-size:13px;cursor:pointer;}

@media(max-width:768px){
  .header{padding:10px 12px;gap:8px;}
  .sb{max-width:100%;order:3;width:100%;}
  .grid{grid-template-columns:1fr;}
}
</style>
</head>
<body>

<div class="header">
  <div class="logo"> GPT-Image-2 提示词库</div>
  <div class="sb">
    <span class="sb-i">🔍</span>
    <input type="text" id="searchInput" placeholder="搜索提示词、标题、分类、风格..." oninput="onSearch(this.value)" />
  </div>
  <div class="stats" id="stats"></div>
  <div class="mt">
    <button id="btnCase" class="active" onclick="switchMode('case')">🖼️ 案例 (<span id="caseCnt">CASE_CNT</span>)</button>
    <button id="btnTpl" onclick="switchMode('tpl')">📋 模板 (<span id="tplCnt">TPL_CNT</span>)</button>
  </div>
</div>

<div class="filters">
  <div class="fg" id="fgCat">
    <label>分类：</label>
    <select id="catFilter" onchange="render()">
      <option value="">全部分类</option>
    </select>
  </div>
  <div class="fg" id="fgStyle" style="display:none">
    <label>风格：</label>
    <select id="styleFilter" onchange="render()">
      <option value="">全部风格</option>
    </select>
  </div>
  <div class="fg" id="fgScene" style="display:none">
    <label>场景：</label>
    <select id="sceneFilter" onchange="render()">
      <option value="">全部场景</option>
    </select>
  </div>
  <label class="chip" id="chipFeatured" onclick="toggleFeatured()">⭐ 精选</label>
</div>

<div class="container">
  <div class="grid" id="grid"></div>
  <div class="empty" id="emptyDiv">
    <div class="ic">😕</div>
    <p>没有找到匹配的结果，换个关键词试试？</p>
  </div>
</div>

<!-- Modal -->
<div class="mo" id="modal" onclick="closeModal(event)">
  <div class="modal" onclick="event.stopPropagation()">
    <div class="miw" id="modalImgWrap"></div>
    <div class="mb">
      <div class="mt2" id="modalTitle"></div>
      <div class="mm" id="modalMeta"></div>
      <div class="mp" id="modalPrompt"></div>
      <div class="ma">
        <button class="bp" onclick="doCopy()">📋 复制提示词</button>
        <button class="bs" onclick="closeModal()">关闭</button>
      </div>
    </div>
  </div>
</div>

<script>
/* === Embedded Data === */
DATA_PLACEHOLDER

/* === Init === */
function init() {
  // Categories
  const cats = [...new Set(CASES_META.map(c=>c.c))].sort();
  const cs = document.getElementById('catFilter');
  cats.forEach(c => { const o=document.createElement('option'); o.value=c; o.textContent=c; cs.appendChild(o); });
  // Styles
  const styles = [...new Set(CASES_META.flatMap(c=>(c.s||[])))].sort();
  const ss = document.getElementById('styleFilter');
  styles.forEach(s => { const o=document.createElement('option'); o.value=s; o.textContent=s; ss.appendChild(o); });
  document.getElementById('fgStyle').style.display = '';
  // Scenes
  const scenes = [...new Set(CASES_META.flatMap(c=>(c.sc||[])))].sort();
  const scs = document.getElementById('sceneFilter');
  scenes.forEach(s => { const o=document.createElement('option'); o.value=s; o.textContent=s; scs.appendChild(o); });
  document.getElementById('fgScene').style.display = '';
  render();
}

function escHtml(s) {
  if (!s) return '';
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function getImgSrc(item) {
  if (item.h) return 'images/case' + item.id + '.jpg';
  // Use pre-generated placeholder data URI
  if (PLACEHOLDERS[item.id]) return PLACEHOLDERS[item.id];
  // Fallback: simple inline SVG data URI
  return 'data:image/svg+xml,' + encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300">' +
    '<rect width="400" height="300" fill="%231a1a2e"/>' +
    '<text x="200" y="150" text-anchor="middle" fill="%237c5cfc" font-size="36">#' + item.id + '</text>' +
    '</svg>'
  );
}

/* === Render === */
function render() {
  const grid = document.getElementById('grid');
  const emptyDiv = document.getElementById('emptyDiv');
  const kw = (document.getElementById('searchInput').value||'').toLowerCase().trim();
  const cat = document.getElementById('catFilter').value;
  const style = document.getElementById('styleFilter').value;
  const scene = document.getElementById('sceneFilter').value;

  let list = (currentMode === 'case') ? CASES_META.slice() : TEMPLATES.slice();

  if (currentMode === 'case') {
    if (cat) list = list.filter(c => c.c === cat);
    if (style) list = list.filter(c => (c.s||[]).includes(style));
    if (scene) list = list.filter(c => (c.sc||[]).includes(scene));
    if (showFeatured) list = list.filter(c => c.f);
  }

  if (kw) {
    list = list.filter(item => {
      const text = [
        (item.t||''),
        (PROMPTS[item.id]||''),
        (item.c||''),
        (item.s||[]).join(' '),
        (item.sc||[]).join(' '),
        (item.name||''),
        (item.description||''),
      ].join(' ').toLowerCase();
      return text.includes(kw);
    });
  }

  const MAX = 200;
  const showing = list.slice(0, MAX);
  const trimmed = list.length > MAX;

  const total = currentMode === 'case' ? CASES_META.length : TEMPLATES.length;
  let statsTxt = '找到 ' + list.length + ' / ' + total + ' 条';
  if (trimmed) statsTxt += '（仅显示前' + MAX + '条，请缩小搜索范围）';
  document.getElementById('stats').textContent = statsTxt;

  if (showing.length === 0) {
    grid.innerHTML = '';
    emptyDiv.style.display = '';
    return;
  }
  emptyDiv.style.display = 'none';

  const parts = [];
  for (let i = 0; i < showing.length; i++) {
    const item = showing[i];
    if (currentMode === 'case') {
      const imgSrc = getImgSrc(item);
      const isDataUri = imgSrc.startsWith('data:');
      let imgHtml;
      if (isDataUri) {
        imgHtml = '<div class="noimg">图片缺失</div>';
      } else {
        imgHtml = '<img src="' + escHtml(imgSrc) + '" alt="' + escHtml(item.t) + '" loading="lazy" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'block\';" /><div class="noimg" style="display:none">图片加载失败</div>';
      }
      parts.push(
        '<div class="card" onclick="openCase(' + item.id + ')">' +
          '<div class="ciw">' + imgHtml + '</div>' +
          '<div class="cb">' +
            '<div class="ct">#' + item.id + ' ' + escHtml(item.t) + '</div>' +
            '<div class="cm">' +
              '<span class="tag cat">' + escHtml(item.c) + '</span>' +
              (item.s||[]).slice(0,2).map(s => '<span class="tag stl">' + escHtml(s) + '</span>').join('') +
            '</div>' +
            '<div class="cp">' + escHtml((PREVIEW[item.id]||PROMPTS[item.id]||'').substring(0,100)) + '</div>' +
            '<div class="ca">' +
              '<button class="btn-copy" onclick="event.stopPropagation();doCopyText(' + item.id + ')">📋 复制</button>' +
              '<button class="btn-view" onclick="event.stopPropagation();openCase(' + item.id + ')">查看</button>' +
            '</div>' +
          '</div>' +
        '</div>'
      );
    } else {
      const title = item.title || item.name || '模板';
      const tags = item.tags || item.category || [];
      parts.push(
        '<div class="card" onclick="openTpl(' + (item.id||0) + ')">' +
          '<div class="cb">' +
            '<div class="ct">📋 ' + escHtml(title) + '</div>' +
            '<div class="cm">' + tags.slice(0,3).map(t => '<span class="tag cat">' + escHtml(t) + '</span>').join('') + '</div>' +
            '<div class="cp">' + escHtml((item.description||(item.prompt||'').substring(0,100))) + '</div>' +
            '<div class="ca">' +
              '<button class="btn-copy" onclick="event.stopPropagation();doCopyTextTpl(' + (item.id||0) + ')">📋 复制</button>' +
              '<button class="btn-view" onclick="event.stopPropagation();openTpl(' + (item.id||0) + ')">查看</button>' +
            '</div>' +
          '</div>' +
        '</div>'
      );
    }
  }
  grid.innerHTML = parts.join('');
}

/* === Search === */
let searchTimer = null;
function onSearch(val) {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(render, 150);
}

/* === Mode === */
let currentMode = 'case';
let showFeatured = false;
function switchMode(mode) {
  currentMode = mode;
  document.getElementById('btnCase').classList.toggle('active', mode==='case');
  document.getElementById('btnTpl').classList.toggle('active', mode==='tpl');
  document.getElementById('fgCat').style.display = mode==='case' ? '' : 'none';
  document.getElementById('fgStyle').style.display = mode==='case' ? '' : 'none';
  document.getElementById('fgScene').style.display = mode==='case' ? '' : 'none';
  document.getElementById('chipFeatured').style.display = mode==='case' ? '' : 'none';
  if (mode === 'tpl') {
    document.getElementById('catFilter').value = '';
    document.getElementById('styleFilter').value = '';
    document.getElementById('sceneFilter').value = '';
    showFeatured = false;
    document.getElementById('chipFeatured').classList.remove('active');
  }
  render();
}
function toggleFeatured() {
  showFeatured = !showFeatured;
  document.getElementById('chipFeatured').classList.toggle('active', showFeatured);
  render();
}

/* === Modal === */
let currentPromptId = null;
function openCase(id) {
  const item = CASES_META.find(c => c.id === id);
  if (!item) return;
  currentPromptId = id;
  const wrap = document.getElementById('modalImgWrap');
  if (item.h) {
    wrap.innerHTML = '<img src="images/case' + id + '.jpg" alt="' + escHtml(item.t) + '" onerror="this.style.display=\'none\';this.parentNode.querySelector(\'.noimg-m\').style.display=\'block\';" /><div class="noimg-m" style="display:none"><div style="font-size:32px;color:#7c5cfc;margin-bottom:8px">#' + id + '</div><div>图片加载失败</div></div>';
  } else {
    wrap.innerHTML = '<div class="noimg-m"><div style="font-size:32px;color:#7c5cfc;margin-bottom:8px">#' + id + '</div><div>图片缺失（服务器 404）</</div><div style="font-size:11px;color:#666;margin-top:6px">' + escHtml(item.t) + '</div></div>';
  }
  document.getElementById('modalTitle').textContent = '#' + id + ' ' + (item.t || '');
  let metaHtml = '<span class="tag cat">' + escHtml(item.c) + '</span>';
  metaHtml += (item.s||[]).map(s => '<span class="tag stl">' + escHtml(s) + '</span>').join('');
  metaHtml += (item.sc||[]).map(s => '<span class="tag cat">' + escHtml(s) + '</span>').join('');
  if (item.f) metaHtml += '<span class="tag stl">⭐ 精选</span>';
  document.getElementById('modalMeta').innerHTML = metaHtml;
  document.getElementById('modalPrompt').textContent = PROMPTS[id] || '（无提示词）';
  document.getElementById('modal').classList.add('open');
}
function openTpl(id) {
  const item = TEMPLATES.find(t => (t.id||0) === id);
  if (!item) return;
  currentPromptId = null;
  const wrap = document.getElementById('modalImgWrap');
  wrap.innerHTML = '<div class="noimg-m"><div style="font-size:32px;margin-bottom:8px">📋</div><div>模板预览</div></div>';
  const title = item.title || item.name || '模板';
  document.getElementById('modalTitle').textContent = '📋 ' + title;
  const tags = item.tags || item.category || [];
  document.getElementById('modalMeta').innerHTML = tags.slice(0,5).map(t => '<span class="tag cat">' + escHtml(t) + '</span>').join('');
  document.getElementById('modalPrompt').textContent = item.prompt || item.template || '（无模板内容）';
  document.getElementById('modal').classList.add('open');
}
function closeModal(e) {
  if (e && e.target !== e.currentTarget) return;
  document.getElementById('modal').classList.remove('open');
}
function doCopy() {
  if (!currentPromptId) return;
  const text = PROMPTS[currentPromptId] || '';
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.querySelector('.bp');
    const orig = btn.textContent;
    btn.textContent = '✅ 已复制！';
    setTimeout(() => btn.textContent = orig, 1200);
  }).catch(() => alert('复制失败，请手动选中提示词后 Ctrl+C'));
}
function doCopyText(id) {
  const text = PROMPTS[id] || '';
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {
    event.target.textContent = '✅ 已复制！';
    setTimeout(() => event.target.textContent = '📋 复制', 1200);
  }).catch(() => alert('复制失败'));
}
function doCopyTextTpl(id) {
  const item = TEMPLATES.find(t => (t.id||0) === id);
  if (!item) return;
  const text = item.prompt || item.template || '';
  navigator.clipboard.writeText(text).then(() => {
    event.target.textContent = '✅ 已复制！';
    setTimeout(() => event.target.textContent = '📋 复制', 1200);
  }).catch(() => alert('复制失败'));
}

/* === Keyboard === */
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
  if (e.ctrlKey && e.key === 'f') { e.preventDefault(); document.getElementById('searchInput').focus(); }
});

init();
</script>
</body>
</html>"""

# 替换占位符
html = html_template
html = html.replace('CASE_CNT', str(len(processed_cases)))
html = html.replace('TPL_CNT', str(len(templates)))

# 构建 data 块
data_js = cases_meta_js + prompt_map_js + preview_map_js + tpl_js + ph_map_js
html = html.replace('/*=== Embedded Data === */\nDATA_PLACEHOLDER', data_js)

# 写入文件
out_path = os.path.join(BASE, 'search-engine.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

sz = os.path.getsize(out_path)
print(f'\n✅ 生成完成: {out_path}')
print(f'   文件大小: {sz/1024:.1f} KB')
print(f'   案例元信息: {len(cases_meta)} 条')
print(f'   提示词: {len(prompt_map)} 条')
print(f'   模板: {len(templates)} 条')
print(f'   占位图: {len(placeholder_map)} 条')
print(f'   有图: {sum(1 for c in processed_cases if c["hasImage"])}')
print(f'   404: {len(missing_404)}')
