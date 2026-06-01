#!/usr/bin/env python3
"""
生成带图片展示的 GPT-Image-2 提示词搜索引擎 HTML
- 嵌入全部 481 条案例 + 22 套模板数据
- 支持图片展示（本地 images/ 目录）
- 搜索、分类筛选、模板/案例切换、一键复制
- 纯单文件，双击即用
"""

import json
import os

# === 读取数据 ===
BASE_DIR = r'C:\Users\Administrator\WorkBuddy\2026-05-31-10-53-55\gpt-image-prompts'
DATA_DIR = os.path.join(BASE_DIR, 'data')
IMG_DIR = os.path.join(BASE_DIR, 'images')

with open(os.path.join(DATA_DIR, 'cases-full.json'), 'r', encoding='utf-8') as f:
    cases_data = json.load(f)

with open(os.path.join(DATA_DIR, 'templates.json'), 'r', encoding='utf-8') as f:
    tpl_data = json.load(f)

cases = cases_data.get('cases', [])
templates = tpl_data if isinstance(tpl_data, list) else tpl_data.get('templates', [])

print(f'案例: {len(cases)}, 模板: {len(templates)}')

# === 检查本地图片 ===
HAVE_IMGS = set()
MISSING_404 = set()
if os.path.exists(IMG_DIR):
    for fname in os.listdir(IMG_DIR):
        if fname.startswith('case') and fname.endswith('.jpg') and not fname.endswith('.missing'):
            try:
                HAVE_IMGS.add(int(fname[4:-4]))
            except ValueError:
                pass
        elif fname.endswith('.jpg.missing'):
            try:
                MISSING_404.add(int(fname[4:-11]))
            except ValueError:
                pass

print(f'本地图片: {len(HAVE_IMGS)}, 已知404: {len(MISSING_404)}')

# === 生成占位 SVG (data URI) ===
def placeholder_svg(case_id, alt_text):
    """生成一个包含案例编号的占位 SVG data URI"""
    text = f"#{case_id}\n图片缺失"
    # 简化 alt
    short_alt = alt_text[:20] + '..' if len(alt_text) > 22 else alt_text
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300">
<rect width="400" height="300" fill="#1a1a2e"/>
<text x="200" y="120" text-anchor="middle" fill="#7c5cfc" font-size="48" font-weight="bold">#{case_id}</text>
<text x="200" y="170" text-anchor="middle" fill="#888" font-size="14">图片缺失 / 404</text>
<text x="200" y="200" text-anchor="middle" fill="#666" font-size="12">{short_alt}</text>
</svg>'''.replace('\n', ' ').replace('  ', ' ')
    import base64
    b64 = base64.b64encode(svg.encode('utf-8')).decode('ascii')
    return f'data:image/svg+xml;base64,{b64}'

# === 预处理案例数据（添加图片状态） ===
processed_cases = []
for c in cases:
    cid = c['id']
    has_img = cid in HAVE_IMGS
    is_404 = cid in MISSING_404
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
        'hasImage': has_img,
        'is404': is_404,
    })

# === 生成 HTML ===
def esc_js(s):
    """转义字符串用于 JS"""
    if not s:
        return ''
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n').replace('\r', '')

tpl_json_str = json.dumps(templates, ensure_ascii=False, default=str)
cases_json_str = json.dumps(processed_cases, ensure_ascii=False, default=str)

html = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GPT-Image-2 提示词搜索引擎 🔍</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #0f0f23; --bg2: #1a1a2e; --bg3: #25253e;
  --accent: #7c5cfc; --accent2: #a78bfa; --green: #34d399;
  --text: #e2e8f0; --text2: #94a3b8; --border: #2d2d4a;
  --radius: 12px;
}
body { font-family: -apple-system, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }

/* === Header === */
.header { background: var(--bg2); border-bottom: 1px solid var(--border); padding: 16px 24px; display: flex; align-items: center; gap: 16px; position: sticky; top: 0; z-index: 100; }
.logo { font-size: 22px; font-weight: 800; background: linear-gradient(135deg, var(--accent), #f472b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.search-box { flex: 1; max-width: 600px; position: relative; }
.search-box input { width: 100%; padding: 10px 16px 10px 40px; background: var(--bg3); border: 1px solid var(--border); border-radius: 24px; color: var(--text); font-size: 14px; outline: none; transition: all .2s; }
.search-box input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(124,92,252,.15); }
.search-box .icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text2); font-size: 14px; }
.stats { font-size: 12px; color: var(--text2); white-space: nowrap; }

/* === Mode Toggle === */
.mode-toggle { display: flex; background: var(--bg3); border-radius: 8px; padding: 3px; gap: 2px; }
.mode-toggle button { padding: 6px 14px; border: none; border-radius: 6px; background: transparent; color: var(--text2); font-size: 13px; cursor: pointer; transition: all .2s; }
.mode-toggle button.active { background: var(--accent); color: #fff; font-weight: 600; }

/* === Filters === */
.filters { background: var(--bg2); border-bottom: 1px solid var(--border); padding: 12px 24px; display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
.filter-group { display: flex; align-items: center; gap: 6px; }
.filter-group label { font-size: 12px; color: var(--text2); white-space: nowrap; }
.filter-group select { padding: 5px 24px 5px 10px; background: var(--bg3); border: 1px solid var(--border); border-radius: 6px; color: var(--text); font-size: 13px; cursor: pointer; appearance: none; -webkit-appearance: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%2394a3b8'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 8px center; }
.filter-group select:focus { outline: none; border-color: var(--accent); }
.chip { padding: 4px 12px; border-radius: 14px; border: 1px solid var(--border); background: var(--bg3); color: var(--text2); font-size: 12px; cursor: pointer; transition: all .2s; }
.chip.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.chip:hover { border-color: var(--accent); }

/* === Cards Grid === */
.container { max-width: 1400px; margin: 0 auto; padding: 24px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }
.card { background: var(--bg2); border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; transition: all .25s; cursor: pointer; }
.card:hover { border-color: var(--accent); transform: translateY(-2px); box-shadow: 0 8px 32px rgba(124,92,252,.15); }
.card-img { width: 100%; height: 220px; object-fit: cover; background: var(--bg3); display: block; }
.card-body { padding: 14px; }
.card-title { font-size: 14px; font-weight: 600; margin-bottom: 6px; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.card-meta { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 8px; }
.tag { padding: 2px 8px; border-radius: 4px; font-size: 11px; background: rgba(124,92,252,.15); color: var(--accent2); }
.tag.style { background: rgba(52,211,153,.12); color: var(--green); }
.card-prompt { font-size: 12px; color: var(--text2); line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: 10px; }
.card-actions { display: flex; gap: 8px; }
.btn-copy { flex: 1; padding: 6px 12px; border-radius: 6px; border: 1px solid var(--accent); background: transparent; color: var(--accent); font-size: 12px; cursor: pointer; transition: all .2s; text-align: center; }
.btn-copy:hover { background: var(--accent); color: #fff; }
.btn-expand { padding: 6px 12px; border-radius: 6px; border: 1px solid var(--border); background: transparent; color: var(--text2); font-size: 12px; cursor: pointer; transition: all .2s; }
.btn-expand:hover { border-color: var(--accent); color: var(--accent); }
.no-image { width: 100%; height: 220px; background: var(--bg3); display: flex; align-items: center; justify-content: center; color: var(--text2); font-size: 14px; }

/* === Modal === */
.modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,.85); z-index: 1000; overflow-y: auto; }
.modal-overlay.open { display: flex; align-items: flex-start; justify-content: center; padding: 40px 20px; }
.modal { background: var(--bg2); border-radius: var(--radius); max-width: 900px; width: 100%; overflow: hidden; }
.modal-img { width: 100%; max-height: 500px; object-fit: contain; background: #000; }
.modal-body { padding: 24px; }
.modal-title { font-size: 20px; font-weight: 700; margin-bottom: 12px; }
.modal-meta { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.modal-prompt { background: var(--bg3); border-radius: 8px; padding: 16px; font-size: 13px; line-height: 1.7; color: var(--text); white-space: pre-wrap; word-break: break-all; max-height: 400px; overflow-y: auto; margin-bottom: 16px; }
.modal-actions { display: flex; gap: 12px; }
.btn-primary { padding: 8px 20px; border-radius: 8px; border: none; background: var(--accent); color: #fff; font-size: 14px; font-weight: 600; cursor: pointer; }
.btn-secondary { padding: 8px 20px; border-radius: 8px; border: 1px solid var(--border); background: transparent; color: var(--text); font-size: 14px; cursor: pointer; }

/* === Empty === */
.empty { text-align: center; padding: 80px 20px; color: var(--text2); }
.empty .icon { font-size: 48px; margin-bottom: 16px; }
.empty p { font-size: 16px; }

/* === Responsive === */
@media (max-width: 768px) {
  .header { flex-wrap: wrap; }
  .search-box { order: 3; max-width: 100%; }
  .grid { grid-template-columns: 1fr; }
}
</style>
</head>
<body>

<div class="header">
  <div class="logo">GPT-Image-2 提示词库</div>
  <div class="search-box">
    <span class="icon">🔍</span>
    <input type="text" id="searchInput" placeholder="搜索提示词、标题、分类、风格...（支持中英文）" oninput="onSearch(this.value)" />
  </div>
  <div class="stats" id="stats"></div>
  <div class="mode-toggle">
    <button id="btnModeCase" class="active" onclick="switchMode('case')">📷 案例 (481)</button>
    <button id="btnModeTpl" onclick="switchMode('tpl')">📋 模板 (22)</button>
  </div>
</div>

<div class="filters">
  <div class="filter-group">
    <label>分类：</label>
    <select id="catFilter" onchange="render()">
      <option value="">全部分类</option>
    </select>
  </div>
  <div class="filter-group" id="styleFilterWrap" style="display:none">
    <label>风格：</label>
    <select id="styleFilter" onchange="render()">
      <option value="">全部风格</option>
    </select>
  </div>
  <div class="filter-group" id="sceneFilterWrap" style="display:none">
    <label>场景：</label>
    <select id="sceneFilter" onchange="render()">
      <option value="">全部场景</option>
    </select>
  </div>
  <label class="chip" id="chipFeatured" onclick="toggleFeatured()">⭐ 精选案例</label>
</div>

<div class="container">
  <div class="grid" id="grid"></div>
  <div class="empty" id="empty" style="display:none">
    <div class="icon">😕</div>
    <p>没有找到匹配的结果，换个关键词试试？</p>
  </div>
</div>

<!-- Modal -->
<div class="modal-overlay" id="modal" onclick="closeModal(event)">
  <div class="modal" onclick="event.stopPropagation()">
    <img class="modal-img" id="modalImg" />
    <div class="modal-body">
      <div class="modal-title" id="modalTitle"></div>
      <div class="modal-meta" id="modalMeta"></div>
      <div class="modal-prompt" id="modalPrompt"></div>
      <div class="modal-actions">
        <button class="btn-primary" onclick="copyPrompt()">📋 复制提示词</button>
        <button class="btn-secondary" onclick="closeModal()">关闭</button>
      </div>
    </div>
  </div>
</div>

<script>
// === Embedded Data ===
const ALL_TEMPLATES = """ + tpl_json_str + r""";
const ALL_CASES = """ + cases_json_str + r""";

let currentMode = 'case';
let showFeaturedOnly = false;
let currentPrompt = '';

// === Init ===
function init() {
  // Populate category filter
  const cats = [...new Set(ALL_CASES.map(c => c.category))].sort();
  const catSel = document.getElementById('catFilter');
  cats.forEach(c => {
    const opt = document.createElement('option');
    opt.value = c; opt.textContent = c;
    catSel.appendChild(opt);
  });
  
  // Populate style filter
  const styles = [...new Set(ALL_CASES.flatMap(c => c.styles || []))].sort();
  const styleSel = document.getElementById('styleFilter');
  styles.forEach(s => {
    const opt = document.createElement('option');
    opt.value = s; opt.textContent = s;
    styleSel.appendChild(opt);
  });
  document.getElementById('styleFilterWrap').style.display = '';
  
  // Populate scene filter
  const scenes = [...new Set(ALL_CASES.flatMap(c => c.scenes || []))].sort();
  const sceneSel = document.getElementById('sceneFilter');
  scenes.forEach(s => {
    const opt = document.createElement('option');
    opt.value = s; opt.textContent = s;
    sceneSel.appendChild(opt);
  });
  document.getElementById('sceneFilterWrap').style.display = '';
  
  render();
}

// === Image Path Helper ===
function getImgSrc(item) {
  // item = case object with hasImage, is404, id
  if (item.hasImage) {
    return 'images/case' + item.id + '.jpg';
  }
  // 404 or missing: return a data URI placeholder
  return genPlaceholder(item.id, item.title);
}

function genPlaceholder(id, title) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300">
    <rect width="400" height="300" fill="%231a1a2e"/>
    <text x="200" y="120" text-anchor="middle" fill="%237c5cfc" font-size="42" font-weight="bold">#${id}</text>
    <text x="200" y="165" text-anchor="middle" fill="%23888" font-size="13">图片缺失 / 404</text>
    <text x="200" y="195" text-anchor="middle" fill="%23666" font-size="11">${escAttr(title)}</text>
  </svg>`;
  return 'data:image/svg+xml,' + encodeURIComponent(svg);
}

function escAttr(s) {
  return (s||'').replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// === Render ===
function render() {
  const grid = document.getElementById('grid');
  const empty = document.getElementById('empty');
  const kw = (document.getElementById('searchInput').value || '').toLowerCase().trim();
  const cat = document.getElementById('catFilter').value;
  const style = document.getElementById('styleFilter').value;
  const scene = document.getElementById('sceneFilter').value;
  
  let list = currentMode === 'case' ? [...ALL_CASES] : [...ALL_TEMPLATES];
  
  // Filter
  if (currentMode === 'case') {
    if (cat) list = list.filter(c => c.category === cat);
    if (style) list = list.filter(c => (c.styles||[]).includes(style));
    if (scene) list = list.filter(c => (c.scenes||[]).includes(scene));
    if (showFeaturedOnly) list = list.filter(c => c.featured);
  }
  
  // Search
  if (kw) {
    list = list.filter(item => {
      const text = [
        item.title || '',
        item.prompt || '',
        item.category || '',
        (item.styles||[]).join(' '),
        (item.scenes||[]).join(' '),
        (item.tags||[]).join(' '),
        item.description || '',
      ].join(' ').toLowerCase();
      return text.includes(kw);
    });
  }
  
  // Limit for performance
  const MAX = 200;
  const showing = list.slice(0, MAX);
  const trimmed = list.length > MAX;
  
  // Stats
  const total = currentMode === 'case' ? ALL_CASES.length : ALL_TEMPLATES.length;
  document.getElementById('stats').textContent = 
    `找到 ${list.length} / ${total} 条` + (trimmed ? '（仅显示前' + MAX + '条，请缩小搜索范围）' : '');
  
  if (showing.length === 0) {
    grid.innerHTML = '';
    empty.style.display = '';
    return;
  }
  empty.style.display = 'none';
  
  // Render cards
  grid.innerHTML = showing.map(item => {
    if (currentMode === 'case') {
      const imgSrc = getImgSrc(item);
      const imgHtml = item.hasImage 
        ? `<img class="card-img" src="${imgSrc}" alt="${escAttr(item.title)}" loading="lazy" />`
        : `<div class="no-image"><div style="text-align:center"><div style="font-size:32px;color:#7c5cfc;margin-bottom:8px">#${item.id}</div><div>图片缺失</div></div></div>`;
      
      return `<div class="card" onclick="openCase(${item.id})">
        ${imgHtml}
        <div class="card-body">
          <div class="card-title">#${item.id} ${escHtml(item.title)}</div>
          <div class="card-meta">
            <span class="tag">${escHtml(item.category)}</span>
            ${(item.styles||[]).slice(0,2).map(s => '<span class="tag style">'+escHtml(s)+'</span>').join('')}
          </div>
          <div class="card-prompt">${(item.promptPreview||item.prompt||'').substring(0,120)}</div>
          <div class="card-actions">
            <button class="btn-copy" onclick="event.stopPropagation();copyText(\`${escJs(item.prompt)}\`)">📋 复制提示词</button>
          </div>
        </div>
      </div>`;
    } else {
      // Template card
      return `<div class="card" onclick="openTemplate(${item.id||0})">
        <div class="card-body">
          <div class="card-title">📋 ${escHtml(item.title||item.name||'模板')}</div>
          <div class="card-meta">
            ${(item.tags||item.category||[]).slice(0,3).map(t => '<span class="tag">'+escHtml(t)+'</span>').join('')}
          </div>
          <div class="card-prompt">${(item.description||item.prompt||'').substring(0,150)}</div>
          <div class="card-actions">
            <button class="btn-copy" onclick="event.stopPropagation();copyText(\`${escJs(item.prompt||item.template||'')}\`)">📋 复制模板</button>
          </div>
        </div>
      </div>`;
    }
  }).join('');
}

// === Search (debounced) ===
let searchTimer;
function onSearch(val) {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(render, 200);
}

// === Mode Switch ===
function switchMode(mode) {
  currentMode = mode;
  document.getElementById('btnModeCase').classList.toggle('active', mode === 'case');
  document.getElementById('btnModeTpl').classList.toggle('active', mode === 'tpl');
  document.getElementById('catFilter').disabled = (mode === 'tpl');
  document.getElementById('styleFilter').disabled = (mode === 'tpl');
  document.getElementById('sceneFilter').disabled = (mode === 'tpl');
  document.getElementById('chipFeatured').style.display = mode === 'case' ? '' : 'none';
  render();
}

// === Featured Toggle ===
function toggleFeatured() {
  showFeaturedOnly = !showFeaturedOnly;
  document.getElementById('chipFeatured').classList.toggle('active', showFeaturedOnly);
  render();
}

// === Modal ===
function openCase(id) {
  const item = ALL_CASES.find(c => c.id === id);
  if (!item) return;
  currentPrompt = item.prompt || '';
  document.getElementById('modalImg').src = getImgSrc(item);
  document.getElementById('modalTitle').textContent = '#' + item.id + ' ' + (item.title || '');
  document.getElementById('modalMeta').innerHTML = 
    `<span class="tag">${escHtml(item.category)}</span>` +
    (item.styles||[]).map(s => '<span class="tag style">'+escHtml(s)+'</span>').join('') +
    (item.scenes||[]).map(s => '<span class="tag">'+escHtml(s)+'</span>').join('');
  document.getElementById('modalPrompt').textContent = item.prompt || '（无提示词）';
  document.getElementById('modal').classList.add('open');
}

function openTemplate(id) {
  const item = ALL_TEMPLATES.find(t => (t.id||0) === id);
  if (!item) return;
  currentPrompt = item.prompt || item.template || '';
  document.getElementById('modalImg').src = 'data:image/svg+xml,' + encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300"><rect width="400" height="300" fill="%231a1a2e"/><text x="200" y="150" text-anchor="middle" fill="%237c5cfc" font-size="24">📋 模板</text></svg>'
  );
  document.getElementById('modalTitle').textContent = '📋 ' + (item.title || item.name || '模板');
  document.getElementById('modalMeta').innerHTML = (item.tags||item.category||[]).map(t => '<span class="tag">'+escHtml(t)+'</span>').join('');
  document.getElementById('modalPrompt').textContent = item.prompt || item.template || '（无模板内容）';
  document.getElementById('modal').classList.add('open');
}

function closeModal(e) {
  if (e && e.target !== e.currentTarget) return;
  document.getElementById('modal').classList.remove('open');
}

function copyPrompt() {
  if (!currentPrompt) return;
  navigator.clipboard.writeText(currentPrompt).then(() => {
    const btn = document.querySelector('.btn-primary');
    const orig = btn.textContent;
    btn.textContent = '✅ 已复制！';
    setTimeout(() => btn.textContent = orig, 1500);
  });
}

function copyText(text) {
  navigator.clipboard.writeText(text).then(() => {
    event.target.textContent = '✅ 已复制！';
    setTimeout(() => event.target.textContent = '📋 复制提示词', 1500);
  });
}

// === Helpers ===
function escHtml(s) {
  if (!s) return '';
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function escJs(s) {
  if (!s) return '';
  return s.replace(/\\/g,'\\\\').replace(/`/g,'\\`').replace(/\${/g,'\\${');
}

// === Keyboard ===
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
  if (e.ctrlKey && e.key === 'f') { e.preventDefault(); document.getElementById('searchInput').focus(); }
});

init();
</script>
</body>
</html>
"""