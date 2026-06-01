#!/usr/bin/env python3
"""
build_v5.py - 生成带图片展示的 GPT-Image-2 提示词搜索引擎
- 读取 cases-full.json 和 templates.json
- 检查本地 images/ 目录，标记哪些有图、哪些 404
- 生成自包含 HTML（数据嵌入 JS，图片用相对路径）
- 支持：搜索、分类/风格/场景筛选、精选、模态框查看、一键复制
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
            try: have_imgs.add(int(fname[4:-4]))
            except: pass
        elif fname.endswith('.jpg.missing'):
            try: missing_404.add(int(fname[4:-11]))
            except: pass

print(f'本地有图: {len(have_imgs)}, 已知404: {len(missing_404)}')

# 处理案例数据
processed = []
for c in cases:
    cid = c['id']
    processed.append({
        'id': cid,
        'title': c.get('title',''),
        'prompt': c.get('prompt',''),
        'promptPreview': c.get('promptPreview',''),
        'category': c.get('category',''),
        'styles': c.get('styles',[]),
        'scenes': c.get('scenes',[]),
        'featured': c.get('featured', False),
        'githubUrl': c.get('githubUrl',''),
        'hasImage': cid in have_imgs,
        'is404': cid in missing_404,
    })

# 分类 / 风格 / 场景
categories = sorted(set(c['category'] for c in processed if c['category']))
all_styles = sorted(set(s for c in processed for s in c['styles']))
all_scenes = sorted(set(s for c in processed for s in c['scenes']))

print(f'分类: {len(categories)}, 风格: {len(all_styles)}, 场景: {len(all_scenes)}')

# 序列化（正确处理中文和引号）
tpl_json = json.dumps(templates, ensure_ascii=False, separators=(',',':'))
cases_json = json.dumps(processed, ensure_ascii=False, separators=(',',':'))

# ========== 生成 HTML ==========
html = '''<!DOCTYPE html>
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

.header{background:var(--bg2);border-bottom:1px solid var(--border);padding:14px 24px;display:flex;align-items:center;gap:14px;position:sticky;top:0;z-index:100;flex-wrap:wrap;}
.logo{font-size:20px;font-weight:800;background:linear-gradient(135deg,var(--accent),#f472b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.search-box{flex:1;max-width:560px;position:relative;}
.search-box .si{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--text2);font-size:13px;pointer-events:none;}
.search-box input{width:100%;padding:9px 14px 9px 36px;background:var(--bg3);border:1px solid var(--border);border-radius:22px;color:var(--text);font-size:14px;outline:none;transition:all .2s;}
.search-box input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(124,92,252,.15);}
.stats{font-size:12px;color:var(--text2);white-space:nowrap;}
.mode-toggle{display:flex;background:var(--bg3);border-radius:8px;padding:3px;gap:2px;}
.mode-toggle button{padding:5px 13px;border:none;border-radius:6px;background:transparent;color:var(--text2);font-size:13px;cursor:pointer;transition:all .2s;}
.mode-toggle button.active{background:var(--accent);color:#fff;font-weight:600;}

.filters{background:var(--bg2);border-bottom:1px solid var(--border);padding:10px 24px;display:flex;gap:12px;flex-wrap:wrap;align-items:center;}
.fg{display:flex;align-items:center;gap:6px;}
.fg label{font-size:12px;color:var(--text2);white-space:nowrap;}
.fg select{padding:4px 22px 4px 8px;background:var(--bg3);border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:12px;cursor:pointer;appearance:none;-webkit-appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='8' height='5'%3E%3Cpath d='M0 0l4 5 4-5z' fill='%2394a3b8'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 7px center;}
.fg select:focus{outline:none;border-color:var(--accent);}
.chip{padding:4px 11px;border-radius:14px;border:1px solid var(--border);background:var(--bg3);color:var(--text2);font-size:12px;cursor:pointer;transition:all .2s;user-select:none;}
.chip.active{background:var(--accent);color:#fff;border-color:var(--accent);}

.container{max-width:1440px;margin:0 auto;padding:24px;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px;}
.card{background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:all .25s;cursor:pointer;display:flex;flex-direction:column;}
.card:hover{border-color:var(--accent);transform:translateY(-3px);box-shadow:0 8px 30px rgba(124,92,252,.15);}
.card-img-wrap{width:100%;height:200px;overflow:hidden;background:var(--bg3);display:flex;align-items:center;justify-content:center;}
.card-img-wrap img{width:100%;height:100%;object-fit:cover;display:block;}
.card-img-wrap .noimg{text-align:center;color:var(--text2);font-size:13px;padding:10px;}
.card-body{padding:12px 14px 14px;flex:1;display:flex;flex-direction:column;}
.card-title{font-size:13px;font-weight:600;margin-bottom:5px;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
.card-meta{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:6px;}
.tag{padding:1px 6px;border-radius:4px;font-size:11px;line-height:1.8;}
.tag.cat{background:rgba(124,92,252,.15);color:var(--accent2);}
.tag.stl{background:rgba(52,211,153,.12);color:var(--green);}
.card-preview{font-size:11px;color:var(--text2);line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin-bottom:8px;flex:1;}
.card-actions{display:flex;gap:6px;margin-top:auto;}
.btn-copy{flex:1;padding:5px 10px;border-radius:6px;border:1px solid var(--accent);background:transparent;color:var(--accent);font-size:11px;cursor:pointer;transition:all .2s;text-align:center;}
.btn-copy:hover{background:var(--accent);color:#fff;}
.btn-view{padding:5px 10px;border-radius:6px;border:1px solid var(--border);background:transparent;color:var(--text2);font-size:11px;cursor:pointer;transition:all .2s;}
.btn-view:hover{border-color:var(--accent);color:var(--accent);}

.empty{text-align:center;padding:80px 20px;color:var(--text2);display:none;}
.empty .ic{font-size:48px;margin-bottom:14px;}
.empty p{font-size:15px;}

/* Modal */
.modal-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.88);z-index:1000;overflow-y:auto;}
.modal-overlay.open{display:flex;align-items:flex-start;justify-content:center;padding:40px 16px;}
.modal{background:var(--bg2);border-radius:var(--radius);max-width:920px;width:100%;overflow:hidden;margin-bottom:40px;}
.modal-img-wrap{width:100%;max-height:480px;overflow:hidden;background:#000;display:flex;align-items:center;justify-content:center;}
.modal-img-wrap img{width:100%;height:auto;max-height:480px;object-fit:contain;display:block;}
.modal-img-wrap .noimg-modal{color:var(--text2);padding:40px;text-align:center;}
.modal-body{padding:20px 24px 24px;}
.modal-title{font-size:18px;font-weight:700;margin-bottom:10px;line-height:1.4;}
.modal-meta{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px;}
.modal-prompt{background:var(--bg3);border-radius:8px;padding:14px;font-size:13px;line-height:1.7;color:var(--text);white-space:pre-wrap;word-break:break-all;max-height:380px;overflow-y:auto;margin-bottom:14px;font-family:'Courier New',monospace;}
.modal-actions{display:flex;gap:10px;}
.btn-primary{padding:8px 18px;border-radius:8px;border:none;background:var(--accent);color:#fff;font-size:13px;font-weight:600;cursor:pointer;transition:all .2s;}
.btn-primary:hover{opacity:.88;}
.btn-secondary{padding:8px 18px;border-radius:8px;border:1px solid var(--border);background:transparent;color:var(--text);font-size:13px;cursor:pointer;}

@media(max-width:768px){
  .header{padding:10px 14px;gap:8px;}
  .search-box{max-width:100%;order:3;width:100%;}
  .grid{grid-template-columns:1fr;}
}
</style>
</head>
<body>

<div class="header">
  <div class="logo">GPT-Image-2 提示词库</div>
  <div class="search-box">
    <span class="si">🔍</span>
    <input type="text" id="searchInput" placeholder="搜索提示词、标题、分类、风格..." oninput="onSearchInput(this.value)" />
  </div>
  <div class="stats" id="stats"></div>
  <div class="mode-toggle">
    <button id="btnCase" class="active" onclick="switchMode('case')">🖼️ 案例 (<span id="caseCount">''' + str(len(cases)) + r'''</span>)</button>
    <button id="btnTpl" onclick="switchMode('tpl')">📋 模板 (<span id="tplCount">''' + str(len(templates)) + r'''</span>)</button>
  </div>
</div>

<div class="filters">
  <div class="fg" id="fgCat">
    <label>分类：</label>
    <select id="catFilter" onchange="doRender()">
      <option value="">全部分类</option>
    </select>
  </div>
  <div class="fg" id="fgStyle" style="display:none">
    <label>风格：</label>
    <select id="styleFilter" onchange="doRender()">
      <option value="">全部风格</option>
    </select>
  </div>
  <div class="fg" id="fgScene" style="display:none">
    <label>场景：</label>
    <select id="sceneFilter" onchange="doRender()">
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
<div class="modal-overlay" id="modal" onclick="closeModal(event)">
  <div class="modal" onclick="event.stopPropagation()">
    <div class="modal-img-wrap" id="modalImgWrap"></div>
    <div class="modal-body">
      <div class="modal-title" id="modalTitle"></div>
      <div class="modal-meta" id="modalMeta"></div>
      <div class="modal-prompt" id="modalPrompt"></div>
      <div class="modal-actions">
        <button class="btn-primary" onclick="doCopy()">📋 复制提示词</button>
        <button class="btn-secondary" onclick="closeModal()">关闭</button>
      </div>
    </div>
  </div>
</div>

<script>
// ===== Embedded Data =====
const ALL_CASES = ''' + cases_json + r''';
const ALL_TPLS = ''' + tpl_json + r''';

let currentMode = 'case';
let showFeatured = false;
let currentPrompt = '';
let searchTimer = null;

// ===== Init =====
function init() {
  // Categories
  const cats = [...new Set(ALL_CASES.map(c=>c.category))].sort();
  const catSel = document.getElementById('catFilter');
  cats.forEach(c => { const o=document.createElement('option'); o.value=c; o.textContent=c; catSel.appendChild(o); });

  // Styles
  const styles = [...new Set(ALL_CASES.flatMap(c=>(c.styles||[])))].sort();
  const styleSel = document.getElementById('styleFilter');
  styles.forEach(s => { const o=document.createElement('option'); o.value=s; o.textContent=s; styleSel.appendChild(o); });
  document.getElementById('fgStyle').style.display = '';

  // Scenes
  const scenes = [...new Set(ALL_CASES.flatMap(c=>(c.scenes||[])))].sort();
  const sceneSel = document.getElementById('sceneFilter');
  scenes.forEach(s => { const o=document.createElement('option'); o.value=s; o.textContent=s; sceneSel.appendChild(o); });
  document.getElementById('fgScene').style.display = '';

  doRender();
}

// ===== Helpers =====
function escHtml(s) {
  if(!s) return '';
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function escJs(s) {
  if(!s) return '';
  return s.replace(/\\/g,'\\\\').replace(/`/g,'\\`').replace(/\${/g,'\\${');
}

function getImgHtml(item) {
  // item: {id, hasImage, is404, title}
  if (item.hasImage) {
    return '<img src="images/case' + item.id + '.jpg" alt="' + escHtml(item.title) + '" loading="lazy" onerror="this.style.display=\\'none\\';this.parentNode.querySelector(\\.noimg\\').style.display=\\'block\\';" /><div class="noimg" style="display:none">图片加载失败</div>';
  }
  // 404 or no image: SVG placeholder via data URI
  var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300">' +
    '<rect width="400" height="300" fill="%231a1a2e"/>' +
    '<text x="200" y="120" text-anchor="middle" fill="%237c5cfc" font-size="38" font-weight="bold">#' + item.id + '</text>' +
    '<text x="200" y="165" text-anchor="middle" fill="%23888" font-size="13">图片缺失 / 404</text>' +
      '<text x="200" y="195" text-anchor="middle" fill="%23666" font-size="11">' + escHtml((item.title||'').substring(0,24)) + '</text>' +
      '</svg>';
  var dataUri = 'data:image/svg+xml,' + encodeURIComponent(svg);
  return '<img src="' + dataUri + '" alt="' + escHtml(item.title) + '" />';
}

// ===== Render =====
function doRender() {
  var grid = document.getElementById('grid');
  var emptyDiv = document.getElementById('emptyDiv');
  var kw = (document.getElementById('searchInput').value||'').toLowerCase().trim();
  var cat = document.getElementById('catFilter').value;
  var style = document.getElementById('styleFilter').value;
  var scene = document.getElementById('sceneFilter').value;

  var list = currentMode === 'case' ? ALL_CASES.slice() : ALL_TPLS.slice();

  // Filters
  if (currentMode === 'case') {
    if (cat) list = list.filter(c => c.category === cat);
    if (style) list = list.filter(c => (c.styles||[]).includes(style));
    if (scene) list = list.filter(c => (c.scenes||[]).includes(scene));
    if (showFeatured) list = list.filter(c => c.featured);
  }

  // Search
  if (kw) {
    list = list.filter(function(item) {
      var text = [
        item.title||'',
        item.prompt||'',
        item.category||'',
        (item.styles||[]).join(' '),
        (item.scenes||[]).join(' '),
        (item.tags||[]).join(' '),
        (item.description||''),
        (item.name||''),
      ].join(' ').toLowerCase();
      return text.indexOf(kw) !== -1;
    });
  }

  // Limit
  var MAX = 200;
  var trimmed = list.length > MAX;
  var showing = list.slice(0, MAX);

  // Stats
  var total = currentMode === 'case' ? ALL_CASES.length : ALL_TPLS.length;
  var statsTxt = '找到 ' + list.length + ' / ' + total + ' 条';
  if (trimmed) statsTxt += '（仅显示前' + MAX + '条，请缩小搜索范围）';
  document.getElementById('stats').textContent = statsTxt;

  if (showing.length === 0) {
    grid.innerHTML = '';
    emptyDiv.style.display = '';
    return;
  }
  emptyDiv.style.display = 'none';

  // Build cards
  var htmlParts = [];
  for (var i = 0; i < showing.length; i++) {
    var item = showing[i];
    if (currentMode === 'case') {
      var card = '<div class="card" onclick="openCase(' + item.id + ')">' +
        '<div class="card-img-wrap">' + getImgHtml(item) + '</div>' +
        '<div class="card-body">' +
          '<div class="card-title">#' + item.id + ' ' + escHtml(item.title) + '</div>' +
          '<div class="card-meta">' +
            '<span class="tag cat">' + escHtml(item.category) + '</span>' +
            (item.styles||[]).slice(0,2).map(function(s){return '<span class="tag stl">' + escHtml(s) + '</span>';}).join('') +
          '</div>' +
          '<div class="card-preview">' + escHtml((item.promptPreview||item.prompt||'').substring(0,120)) + '</div>' +
          '<div class="card-actions">' +
            '<button class="btn-copy" onclick="event.stopPropagation();doCopyText(\'' + escJs(item.prompt) + '\')">📋 复制提示词</button>' +
            '<button class="btn-view" onclick="event.stopPropagation();openCase(' + item.id + ')">查看</button>' +
          '</div>' +
        '</div>' +
      '</div>';
      htmlParts.push(card);
    } else {
      var t = item;
      var title = t.title || t.name || '模板';
      var prompt = t.prompt || t.template || '';
      var tags = t.tags || t.category || [];
      if (typeof tags === 'string') tags = [tags];
      var desc = t.description || prompt.substring(0,100);
      var card = '<div class="card" onclick="openTpl(' + (t.id||0) + ')">' +
        '<div class="card-body">' +
          '<div class="card-title">📋 ' + escHtml(title) + '</div>' +
          '<div class="card-meta">' + tags.slice(0,3).map(function(tg){return '<span class="tag cat">' + escHtml(tg) + '</span>';}).join('') + '</div>' +
          '<div class="card-preview">' + escHtml(desc) + '</div>' +
          '<div class="card-actions">' +
            '<button class="btn-copy" onclick="event.stopPropagation();doCopyText(\'' + escJs(prompt) + '\')">📋 复制模板</button>' +
            '<button class="btn-view" onclick="event.stopPropagation();openTpl(' + (t.id||0) + ')">查看</button>' +
          '</div>' +
        '</div>' +
      '</div>';
      htmlParts.push(card);
    }
  }
  grid.innerHTML = htmlParts.join('');
}

// ===== Search (debounced) =====
function onSearchInput(val) {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(doRender, 180);
}

// ===== Mode =====
function switchMode(mode) {
  currentMode = mode;
  document.getElementById('btnCase').classList.toggle('active', mode==='case');
  document.getElementById('btnTpl').classList.toggle('active', mode==='tpl');
  document.getElementById('fgCat').style.display = mode==='case'?'':'none';
  document.getElementById('fgStyle').style.display = mode==='case'?'':'none';
  document.getElementById('fgScene').style.display = mode==='case'?'':'none';
  document.getElementById('chipFeatured').style.display = mode==='case'?'':'none';
  if (mode === 'tpl') {
    document.getElementById('catFilter').value = '';
    document.getElementById('styleFilter').value = '';
    document.getElementById('sceneFilter').value = '';
    showFeatured = false;
    document.getElementById('chipFeatured').classList.remove('active');
  }
  doRender();
}

// ===== Featured =====
function toggleFeatured() {
  showFeatured = !showFeatured;
  document.getElementById('chipFeatured').classList.toggle('active', showFeatured);
  doRender();
}

// ===== Modal =====
function openCase(id) {
  var item = ALL_CASES.find(function(c){return c.id===id;});
  if (!item) return;
  currentPrompt = item.prompt || '';
  // Image
  var wrap = document.getElementById('modalImgWrap');
  if (item.hasImage) {
    wrap.innerHTML = '<img src="images/case' + item.id + '.jpg" alt="' + escHtml(item.title) + '" onerror="this.style.display=\\'none\\';" />';
  } else {
    wrap.innerHTML = '<div class="noimg-modal"><div style="font-size:36px;color:#7c5cfc;margin-bottom:10px">#' + id + '</div><div>图片缺失（服务器 404）</div><div style="font-size:12px;color:#666;margin-top:8px">' + escHtml(item.title) + '</div></div>';
  }
  document.getElementById('modalTitle').textContent = '#' + id + ' ' + (item.title||'');
  var metaHtml = '<span class="tag cat">' + escHtml(item.category) + '</span>';
  metaHtml += (item.styles||[]).map(function(s){return '<span class="tag stl">' + escHtml(s) + '</span>';}).join('');
  metaHtml += (item.scenes||[]).map(function(s){return '<span class="tag cat">' + escHtml(s) + '</span>';}).join('');
  if (item.featured) metaHtml += '<span class="tag stl">⭐ 精选</span>';
  document.getElementById('modalMeta').innerHTML = metaHtml;
  document.getElementById('modalPrompt').textContent = item.prompt || '（无提示词）';
  document.getElementById('modal').classList.add('open');
}

function openTpl(id) {
  var item = ALL_TPLS.find(function(t){return (t.id||0)===id;});
  if (!item) return;
  currentPrompt = item.prompt || item.template || '';
  var wrap = document.getElementById('modalImgWrap');
  wrap.innerHTML = '<div class="noimg-modal"><div style="font-size:36px;margin-bottom:10px">📋</div><div>模板预览</div></div>';
  var title = item.title || item.name || '模板';
  document.getElementById('modalTitle').textContent = '📋 ' + title;
  var tags = item.tags || item.category || [];
  if (typeof tags === 'string') tags = [tags];
  document.getElementById('modalMeta').innerHTML = tags.slice(0,5).map(function(t){return '<span class="tag cat">' + escHtml(t) + '</span>';}).join('');
  document.getElementById('modalPrompt').textContent = item.prompt || item.template || '（无模板内容）';
  document.getElementById('modal').classList.add('open');
}

function closeModal(e) {
  if (e && e.target !== e.currentTarget) return;
  document.getElementById('modal').classList.remove('open');
}

function doCopy() {
  if (!currentPrompt) return;
  navigator.clipboard.writeText(currentPrompt).then(function(){
    var btn = document.querySelector('.btn-primary');
    var orig = btn.textContent;
    btn.textContent = '✅ 已复制！';
    setTimeout(function(){btn.textContent=orig;},1500);
  }).catch(function(){alert('复制失败，请手动选中提示词后 Ctrl+C');});
}

function doCopyText(text) {
  navigator.clipboard.writeText(text).then(function(){
    event.target.textContent = '✅ 已复制！';
    var btn = event.target;
    setTimeout(function(){btn.textContent='📋 复制提示词';},1500);
  }).catch(function(){alert('复制失败');});
}

// ===== Keyboard =====
document.addEventListener('keydown', function(e){
  if (e.key==='Escape') closeModal();
  if (e.ctrlKey && e.key==='f') { e.preventDefault(); document.getElementById('searchInput').focus(); }
});

init();
</script>
</body>
</html>'''

out_path = os.path.join(BASE, 'search-engine.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

sz = os.path.getsize(out_path)
print(f'\n✅ 生成完成: {out_path}')
print(f'   文件大小: {sz/1024:.1f} KB')
print(f'   案例数: {len(processed)}')
print(f'   模板数: {len(templates)}')
print(f'   有图: {sum(1 for c in processed if c["hasImage"])}')
print(f'   404: {len(missing_404)}')
