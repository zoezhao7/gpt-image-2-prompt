#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build search-engine.html - Robust Version.
Data embedded in <script type="application/json"> tags.
JS reads via JSON.parse() -> zero escaping issues.
"""
import json, os

BASE = r'C:\Users\Administrator\WorkBuddy\2026-05-31-10-53-55\gpt-image-prompts'

with open(os.path.join(BASE, 'data', 'cases-full.json'), 'r', encoding='utf-8') as f:
    full = json.load(f)

cases = full.get('cases', [])
categories = full.get('categories', [])
styles_list = full.get('styles', [])
scenes_list = full.get('scenes', [])

# Mark which cases have local images
img_dir = os.path.join(BASE, 'images')
have_img = set()
nf_ids = set()
for fn in os.listdir(img_dir):
    if fn.startswith('case') and fn.endswith('.jpg') and 'missing' not in fn:
        try:
            have_img.add(int(fn[4:-4]))  # case123.jpg -> 123
        except:
            pass
    if fn.endswith('.jpg.missing'):
        try:
            nf_ids.add(int(fn.split('.')[0][4:]))  # case123.jpg.missing -> 123
        except:
            pass

for c in cases:
    cid = c['id']
    c['h'] = cid in have_img
    c['nf'] = cid in nf_ids

print(f'Total cases: {len(cases)}, Images: {len(have_img)}, 404s: {len(nf_ids)}')

# ---------- Templates (22) ----------
TEMPLATES = [
  {"id":1,"t":"信息图通用模板","c":"信息可视化","p":"Create a professional infographic with the following structure: Title section with clear hierarchy, 3-4 content sections with icons, data visualization elements, clean typography. Style: modern flat design, vibrant colors, white background. Topic: {{TOPIC}}"},
  {"id":2,"t":"海报设计模板","c":"Posters & Typography","p":"Design a movie-poster-style image with dramatic lighting, bold title typography at the top, central subject with rim lighting, atmospheric background. Theme: {{THEME}}, mood: {{MOOD}}"},
  {"id":3,"t":"产品摄影模板","c":"Product & E-commerce","p":"Product photography of {{PRODUCT}} on clean white background, soft studio lighting, sharp focus, high resolution, commercial quality, subtle shadow underneath"},
  {"id":4,"t":"UI界面设计模板","c":"UI & Interfaces","p":"Design a clean mobile app interface screen for {{APP_TYPE}}, iOS style, with navigation bar, content area, and tab bar. Use system fonts, proper padding, and realistic content placeholders"},
  {"id":5,"t":"Logo设计模板","c":"Branding & Logo","p":"Design a minimalist logo for brand '{{BRAND_NAME}}', in the style of {{STYLE}}, suitable for {{INDUSTRY}} industry. Vector style, clean lines, recognizable at small sizes"},
  {"id":6,"t":"插画风格模板","c":"Illustration & Art","p":"Create an illustration in {{STYLE}} style, depicting {{SUBJECT}}. Use vibrant colors, rich details, artistic composition, suitable for editorial use"},
  {"id":7,"t":"摄影写实模板","c":"Photography & Realism","p":"A photorealistic image of {{SUBJECT}}, shot on 35mm lens, shallow depth of field, natural lighting, high detail, 8K resolution, cinematic color grading"},
  {"id":8,"t":"角色设计模板","c":"Characters & Portraits","p":"Character design sheet for {{CHARACTER_DESC}}, showing front view, side view, and expression variants. Style: {{STYLE}}, consistent lighting, white background"},
  {"id":9,"t":"建筑空间模板","c":"Architecture & Spaces","p":"Architectural visualization of {{BUILDING_DESC}}, photorealistic rendering, golden hour lighting, dramatic shadows, professional architecture photography style"},
  {"id":10,"t":"文档出版模板","c":"Documents & Publications","p":"Design a document page layout for {{DOC_TYPE}}, with clean typography, proper margins, header/footer, and placeholder content. Professional and print-ready"},
  {"id":11,"t":"社交媒体模板","c":"Posters & Typography","p":"Create a social media post image for {{PLATFORM}}, with eye-catching visuals, bold text overlay '{{TEXT}}', vibrant gradient background, modern design"},
  {"id":12,"t":"食物摄影模板","c":"Photography & Realism","p":"Food photography of {{DISH}}, studio lighting, shallow depth of field, steam rising, vibrant colors, dark background for contrast, commercial quality"},
  {"id":13,"t":"科技感界面模板","c":"UI & Interfaces","p":"Futuristic tech interface HUD element, with data visualizations, glowing neon accents (cyan/magenta), dark background, sci-fi aesthetic inspired by MR movies"},
  {"id":14,"t":"水墨国风模板","c":"Illustration & Art","p":"Traditional Chinese ink wash painting style illustration of {{SUBJECT}}, with expressive brushstrokes, ink wash textures, elegant composition, minimal color palette with ink tones"},
  {"id":15,"t":"儿童插画模板","c":"Illustration & Art","p":"Children's book illustration style, depicting {{SCENE}}, with soft pastel colors, round friendly characters, warm lighting, whimsical details, suitable for ages 3-8"},
  {"id":16,"t":"复古海报模板","c":"Posters & Typography","p":"Vintage poster design in Art Deco style, for {{SUBJECT}}, with geometric patterns, bold typography, muted color palette, weathered texture, 1920s aesthetic"},
  {"id":17,"t":"科幻场景模板","c":"Scenes & Narratives","p":"Sci-fi concept art of {{SCENE}}, with futuristic architecture, atmospheric lighting, detailed environment, cinematic composition, inspired by MR concept artists"},
  {"id":18,"t":"品牌VI模板","c":"Branding & Logo","p":"Brand identity design system for {{BRAND}}, including logo, color palette, typography guide, and application examples on business card and stationery. Cohesive and professional"},
  {"id":19,"t":"数据图表模板","c":"Information Visualization","p":"Create a set of clean data charts: bar chart, line graph, and pie chart, showing {{DATA_DESC}}. Use consistent color scheme, clear labels, modern flat design style"},
  {"id":20,"t":"街头艺术模板","c":"Illustration & Art","p":"Street art / graffiti style mural of {{SUBJECT}}, with bold colors, spray paint textures, urban background, dynamic composition, Banksy-inspired stencil elements"},
  {"id":21,"t":"奇幻场景模板","c":"Scenes & Narratives","p":"Fantasy landscape concept art of {{SCENE}}, with dramatic lighting, epic scale, detailed environment, magical atmosphere, inspired by RPG game concept art"},
  {"id":22,"t":"历史古风模板","c":"Historical & Cultural","p":"Historical Chinese painting style depiction of {{SCENE}}, with traditional composition, period-accurate clothing and architecture, elegant brushwork, classical aesthetics"},
]

# ---------- JSON strings (safe for embedding in <script type="application/json">) ----------
cases_json   = json.dumps(cases,     ensure_ascii=False, separators=(',', ': '))
tpl_json      = json.dumps(TEMPLATES,  ensure_ascii=False, separators=(',', ': '))

# ---------- HTML construction ----------
# We write the file in parts to avoid Python string formatting issues with the large JSON blobs.

html_parts = []
add = html_parts.append

add('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GPT-Image-2 提示词搜索引擎</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f0f23;--bg2:#1a1a2e;--bg3:#25253e;
  --accent:#7c5cfc;--accent2:#a78bfa;--green:#34d399;
  --text:#e2e8f0;--text2:#94a3b8;--border:#2d2d4a;
  --radius:12px;
}
body{font-family:-apple-system,'Segoe UI',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}

.header{background:var(--bg2);border-bottom:1px solid var(--border);padding:12px 20px;display:flex;align-items:center;gap:12px;position:sticky;top:0;z-index:100;flex-wrap:wrap;}
.logo{font-size:18px;font-weight:800;background:linear-gradient(135deg,var(--accent),#f472b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;white-space:nowrap;}
.search-box{flex:1;max-width:540px;position:relative;}
.search-box .si{position:absolute;left:12px;top:50%;transform:translateY(-50%);color:var(--text2);font-size:13px;pointer-events:none;}
.search-box input{width:100%;padding:8px 12px 8px 34px;background:var(--bg3);border:1px solid var(--border);border-radius:20px;color:var(--text);font-size:13px;outline:none;transition:all .2s;}
.search-box input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(124,92,252,.15);}
.stats{font-size:11px;color:var(--text2);white-space:nowrap;}
.mode-toggle{display:flex;background:var(--bg3);border-radius:8px;padding:2px;gap:2px;}
.mode-toggle button{padding:5px 11px;border:none;border-radius:6px;background:transparent;color:var(--text2);font-size:12px;cursor:pointer;transition:all .2s;}
.mode-toggle button.active{background:var(--accent);color:#fff;font-weight:600;}

.filters{background:var(--bg2);border-bottom:1px solid var(--border);padding:8px 20px;display:flex;gap:10px;flex-wrap:wrap;align-items:center;}
.fg{display:flex;align-items:center;gap:5px;}
.fg label{font-size:11px;color:var(--text2);white-space:nowrap;}
.fg select{background:var(--bg3);color:var(--text);border:1px solid var(--border);border-radius:6px;padding:3px 6px;font-size:11px;}

.main{padding:20px;max-width:1400px;margin:0 auto;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;}
.card{background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;cursor:pointer;transition:all .25s;position:relative;}
.card:hover{transform:translateY(-4px);box-shadow:0 12px 40px rgba(0,0,0,.4);border-color:var(--accent);}
.card-img{width:100%;aspect-ratio:4/3;object-fit:cover;background:var(--bg3);display:block;}
.card-body{padding:12px;position:relative;}
.card-title{font-size:13px;font-weight:600;margin-bottom:6px;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
.card-meta{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:8px;}
.tag{font-size:10px;padding:2px 6px;border-radius:4px;background:rgba(124,92,252,.15);color:var(--accent2)}
.tag-cat{background:rgba(52,211,153,.12);color:var(--green);}
.card-actions{display:flex;gap:6px;}
.card-actions button{padding:4px 10px;border-radius:6px;border:none;font-size:11px;cursor:pointer;transition:all .2s;}
.btn-copy{background:var(--accent);color:#fff;}
.btn-copy:hover{background:#6b4ce0;}
.btn-view{background:var(--bg3);color:var(--text2);border:1px solid var(--border) !important;}
.btn-view:hover{border-color:var(--accent);color:var(--text);}
.prompt-preview{font-size:11px;color:var(--text2);line-height:1.5;margin-top:8px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;}

.pagination{display:flex;justify-content:center;gap:6px;margin-top:24px;flex-wrap:wrap;}
.pagination button{padding:6px 12px;border-radius:6px;border:1px solid var(--border);background:var(--bg2);color:var(--text2);font-size:12px;cursor:pointer;transition:all .2s;}
.pagination button:hover,.pagination button.active{background:var(--accent);color:#fff;border-color:var(--accent);}
.pagination button:disabled{opacity:.4;cursor:not-allowed;}

.modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.85);z-index:1000;display:flex;align-items:center;justify-content:center;padding:20px;}
.modal{background:var(--bg2);border:1px solid var(--border);border-radius:16px;max-width:720px;width:100%;max-height:85vh;overflow-y:auto;padding:24px;position:relative;}
.modal-close{position:absolute;top:12px;right:16px;background:none;border:none;color:var(--text2);font-size:22px;cursor:pointer;}
.modal-img{max-width:100%;border-radius:8px;margin-bottom:16px;}
.modal-title{font-size:18px;font-weight:700;margin-bottom:12px;}
.modal-prompt{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:14px;font-size:13px;line-height:1.7;white-space:pre-wrap;word-break:break-all;color:var(--text);margin-bottom:14px;max-height:50vh;overflow-y:auto;}
.modal-actions{display:flex;gap:8px;}
.modal-actions button{padding:7px 16px;border-radius:8px;border:none;font-size:13px;cursor:pointer;}
.btn-copy-lg{background:var(--accent);color:#fff;}
.btn-copy-lg:hover{background:#6b4ce0;}

.no-image{width:100%;aspect-ratio:4/3;background:var(--bg3);display:flex;align-items:center;justify-content:center;color:var(--text2);font-size:13px;}

@media(max-width:640px){
  .header{padding:10px 12px;gap:8px;}
  .search-box{max-width:100%;}
  .main{padding:12px;}
  .grid{grid-template-columns:1fr;}
}
</style>
</head>
<body>

<div class="header">
  <div class="logo">GPT-Image-2 提示词库</div>
  <div class="search-box">
    <span class="si">🔍</span>
    <input type="text" id="searchInput" placeholder="搜索提示词、分类、风格…（支持中英文）">
  </div>
  <div class="stats" id="stats">加载中…</div>
  <div class="mode-toggle">
    <button id="btnCase" class="active" onclick="switchMode('case')">🖼️ 案例 (''' + str(len(cases)) + ''')</button>
    <button id="btnTpl" onclick="switchMode('tpl')">📋 模板 (22)</button>
  </div>
</div>

<div class="filters">
  <div class="fg">
    <label>分类</label>
    <select id="catFilter"><option value="">全部</option></select>
  </div>
  <div class="fg" id="styleFilterWrap" style="display:none">
    <label>风格</label>
    <select id="styleFilter"><option value="">全部</option></select>
  </div>
  <div class="fg" id="sceneFilterWrap" style="display:none">
    <label>场景</label>
    <select id="sceneFilter"><option value="">全部</option></select>
  </div>
  <div class="fg">
    <label>精选</label>
    <select id="featuredFilter">
      <option value="">全部</option>
      <option value="true">⭐ 精选</option>
    </select>
  </div>
  <div class="fg" style="margin-left:auto">
    <label>每页</label>
    <select id="pageSizeSelect">
      <option value="20">20</option>
      <option value="50" selected>50</option>
      <option value="100">100</option>
    </select>
  </div>
</div>

<div class="main">
  <div class="grid" id="grid"></div>
  <div class="pagination" id="pagination"></div>
</div>

<!-- Modal -->
<div class="modal-overlay" id="modal" style="display:none" onclick="if(event.target===this)closeModal()">
  <div class="modal">
    <button class="modal-close" onclick="closeModal()">✕</button>
    <img class="modal-img" id="modalImg" src="" alt="">
    <div class="modal-title" id="modalTitle"></div>
    <div id="modalTags" style="display:flex;gap:5px;flex-wrap:wrap;margin-bottom:14px;"></div>
    <div class="modal-prompt" id="modalPrompt"></div>
    <div class="modal-actions">
      <button class="btn-copy-lg" id="modalCopyBtn">📋 复制提示词</button>
      <button class="btn-view" onclick="closeModal()">关闭</button>
    </div>
  </div>
</div>

<!-- Data embedded as application/json (never executed as JS) -->
<script id="data-cases" type="application/json">
''')

# Part 2: cases JSON
add(cases_json)
add('''
</script>
<script id="data-templates" type="application/json">
''')

# Part 3: templates JSON
add(tpl_json)
add('''
</script>

<script>
// ============ Load data from embedded JSON script tags ============
var ALL_CASES = [];
var ALL_TEMPLATES = ''' + tpl_json + ''';

(function(){
  try {
    var casesScript = document.getElementById('data-cases');
    ALL_CASES = JSON.parse(casesScript.textContent);
  } catch(e) {
    console.error('Failed to parse cases data:', e);
    ALL_CASES = [];
  }
})();

// ============ State ============
var currentMode = 'case';
var currentPage = 1;
var pageSize = 50;
var currentItem = null;

// ============ Init ============
function init(){
  populateCatFilter();
  bindEvents();
  doSearch();
}

function populateCatFilter(){
  var cats = {};
  ALL_CASES.forEach(function(c){ if(c.c) cats[c.c]=true; });
  var sel = document.getElementById('catFilter');
  Object.keys(cats).sort().forEach(function(c){
    var o = document.createElement('option');
    o.value = c; o.textContent = c;
    sel.appendChild(o);
  });
  // Also populate style and scene filters
  var styleSel = document.getElementById('styleFilter');
  var scenes = {};
  ALL_CASES.forEach(function(c){ (c.s||[]).forEach(function(s){ scenes[s]=true; }); });
  Object.keys(scenes).sort().forEach(function(s){
    var o = document.createElement('option'); o.value=s; o.textContent=s; styleSel.appendChild(o);
  });
  var sceneSel = document.getElementById('sceneFilter');
  ALL_CASES.forEach(function(c){ (c.sc||[]).forEach(function(s){ scenes[s]=true; }); });
  Object.keys(scenes).sort().forEach(function(s){
    var o = document.createElement('option'); o.value=s; o.textContent=s; sceneSel.appendChild(o);
  });
}

function bindEvents(){
  document.getElementById('searchInput').addEventListener('input', function(){
    currentPage = 1; doSearch();
  });
  document.getElementById('catFilter').addEventListener('change', function(){
    currentPage = 1; doSearch();
  });
  document.getElementById('styleFilter').addEventListener('change', function(){
    currentPage = 1; doSearch();
  });
  document.getElementById('sceneFilter').addEventListener('change', function(){
    currentPage = 1; doSearch();
  });
  document.getElementById('featuredFilter').addEventListener('change', function(){
    currentPage = 1; doSearch();
  });
  document.getElementById('pageSizeSelect').addEventListener('change', function(){
    pageSize = parseInt(this.value); currentPage = 1; doSearch();
  });
  document.addEventListener('keydown', function(e){
    if(e.key==='Escape') closeModal();
  });
}

// ============ Search ============
function doSearch(){
  var kw = document.getElementById('searchInput').value.trim().toLowerCase();
  var cat = document.getElementById('catFilter').value;
  var style = document.getElementById('styleFilter').value;
  var scene = document.getElementById('sceneFilter').value;
  var featured = document.getElementById('featuredFilter').value;

  var pool = currentMode==='case' ? ALL_CASES : ALL_TEMPLATES;

  var results = pool.filter(function(item){
    if(currentMode==='case'){
      if(cat && item.c !== cat) return false;
      if(style && !(item.s||[]).includes(style)) return false;
      if(scene && !(item.sc||[]).includes(scene)) return false;
      if(featured === 'true' && !item.f) return false;
    }
    if(!kw) return true;
    var hay = [item.t||'', item.p||'', item.c||'', (item.s||[]).join(' '), (item.sc||[]).join(' ')].join(' ').toLowerCase();
    return hay.indexOf(kw) !== -1;
  });

  if(currentMode==='case'){
    results.sort(function(a,b){
      if(a.f && !b.f) return -1;
      if(!a.f && b.f) return 1;
      return (a.id||0) - (b.id||0);
    });
  }

  renderResults(results);
}

// ============ Render ============
function renderResults(results){
  document.getElementById('stats').textContent =
    '找到 ' + results.length + ' 条' + (currentMode==='case' ? '（案例）' : '（模板）');

  var totalPages = Math.max(1, Math.ceil(results.length / pageSize));
  if(currentPage > totalPages) currentPage = totalPages;

  var start = (currentPage-1)*pageSize;
  var page = results.slice(start, start+pageSize);

  var grid = document.getElementById('grid');
  grid.innerHTML = '';

  if(page.length === 0){
    grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:60px;color:var(--text2)">暂无结果，换个关键词试试？</div>';
  } else {
    page.forEach(function(item){
      grid.appendChild(createCard(item));
    });
  }

  renderPagination(results.length, totalPages);
}

function createCard(item){
  var div = document.createElement('div');
  div.className = 'card';

  var id = item.id || 0;
  var title = item.t || item.title || 'Untitled';
  var prompt = item.p || '';
  var cat = item.c || '';
  var styles = item.s || [];
  var scenes = item.sc || [];
  var featured = !!item.f;
  var hasImage = item.h !== false;
  var nf = !!item.nf;

  var imgSrc = '';
  if(currentMode==='case' && !nf && hasImage){
    imgSrc = 'images/case' + id + '.jpg';
  }

  var imgHtml = '';
  if(imgSrc){
    imgHtml = '<img class="card-img" src="' + imgSrc + '" alt="' + escHtml(title) + '" loading="lazy" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'">' +
      '<div class="no-image" style="display:none">🖼️ 图片加载失败</div>';
  } else {
    imgHtml = '<div class="no-image">📄 暂无效果图</div>';
  }

  var tagsHtml = '';
  if(cat) tagsHtml += '<span class="tag tag-cat">' + escHtml(cat) + '</span>';
  if(featured) tagsHtml += '<span class="tag">⭐ 精选</span>';
  styles.slice(0,3).forEach(function(s){
    tagsHtml += '<span class="tag">' + escHtml(s) + '</span>';
  });

  var preview = prompt.substring(0, 120) + (prompt.length > 120 ? '…' : '');

  div.innerHTML =
    imgHtml +
    '<div class="card-body">' +
      '<div class="card-title">' + (featured?'⭐ ':'') + escHtml(title) + '</div>' +
      '<div class="card-meta">' + tagsHtml + '</div>' +
      '<div class="prompt-preview">' + escHtml(preview) + '</div>' +
      '<div class="card-actions">' +
        '<button class="btn-copy" onclick="event.stopPropagation();doCopy(event,\\'' + id + '\\',\\'' + currentMode + '\\')">📋 复制</button>' +
        '<button class="btn-view" onclick="event.stopPropagation();openModalById(\\'' + id + '\\',\\'' + currentMode + '\\')">查看</button>' +
      '</div>' +
    '</div>';

  div.addEventListener('click', function(){ openModalById(id, currentMode); });

  return div;
}

// ============ Copy ============
function doCopy(e, id, mode){
  e.stopPropagation();
  var item = findItem(id, mode);
  if(!item) return;
  var text = item.p || '';
  copyText(text);
}

function copyText(text){
  if(!text) return;
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(function(){
      showCopyOk();
    }).catch(function(){
      fallbackCopy(text);
    });
  } else {
    fallbackCopy(text);
  }
}

function fallbackCopy(text){
  var ta = document.createElement('textarea');
  ta.value = text;
  ta.style.cssText = 'position:fixed;left:-9999px;top:-9999px;opacity:0';
  document.body.appendChild(ta);
  ta.focus(); ta.select();
  try {
    document.execCommand('copy');
    showCopyOk();
  } catch(ex){
    alert('复制失败，请手动选中提示词后 Ctrl+C');
  }
  document.body.removeChild(ta);
}

function showCopyOk(){
  var btn = document.getElementById('modalCopyBtn');
  if(btn && document.getElementById('modal').style.display !== 'none'){
    var orig = btn.textContent;
    btn.textContent = '✅ 已复制！';
    setTimeout(function(){ btn.textContent = orig; }, 1200);
  }
}

// ============ Modal ============
function openModalById(id, mode){
  var item = findItem(id, mode);
  if(!item) return;
  currentItem = item;

  var title = item.t || item.title || 'Untitled';
  var prompt = item.p || '';
  var cat = item.c || '';
  var styles = item.s || [];
  var scenes = item.sc || [];
  var hasImage = item.h !== false;
  var nf = !!item.nf;

  document.getElementById('modalTitle').textContent = title;

  var imgEl = document.getElementById('modalImg');
  if(currentMode==='case' && !nf && hasImage){
    imgEl.src = 'images/case' + item.id + '.jpg';
    imgEl.style.display = 'block';
    imgEl.onerror = function(){ this.style.display='none'; };
  } else {
    imgEl.style.display = 'none';
  }

  var tagsHtml = '';
  if(cat) tagsHtml += '<span class="tag tag-cat">' + escHtml(cat) + '</span>';
  styles.forEach(function(s){
    tagsHtml += '<span class="tag">' + escHtml(s) + '</span>';
  });
  scenes.forEach(function(s){
    tagsHtml += '<span class="tag" style="background:rgba(244,114,182,.12);color:#f472b6">' + escHtml(s) + '</span>';
  });
  document.getElementById('modalTags').innerHTML = tagsHtml;

  document.getElementById('modalPrompt').textContent = prompt;
  document.getElementById('modalCopyBtn').onclick = function(){ copyText(prompt); };

  document.getElementById('modal').style.display = 'flex';
}

function closeModal(){
  document.getElementById('modal').style.display = 'none';
  currentItem = null;
}

// ============ Pagination ============
function renderPagination(total, totalPages){
  var pag = document.getElementById('pagination');
  pag.innerHTML = '';

  if(totalPages <= 1) return;

  var prev = document.createElement('button');
  prev.textContent = '‹ 上一页';
  prev.disabled = currentPage <= 1;
  prev.onclick = function(){ currentPage--; doSearch(); };
  pag.appendChild(prev);

  var startP = Math.max(1, currentPage - 2);
  var endP = Math.min(totalPages, currentPage + 2);
  for(var i=startP; i<=endP; i++){
    (function(p){
      var btn = document.createElement('button');
      btn.textContent = p;
      if(p === currentPage) btn.className = 'active';
      btn.onclick = function(){ currentPage = p; doSearch(); };
      pag.appendChild(btn);
    })(i);
  }

  var next = document.createElement('button');
  next.textContent = '下一页 ›';
  next.disabled = currentPage >= totalPages;
  next.onclick = function(){ currentPage++; doSearch(); };
  pag.appendChild(next);
}

// ============ Mode Switch ============
function switchMode(mode){
  currentMode = mode;
  currentPage = 1;
  document.getElementById('btnCase').classList.toggle('active', mode==='case');
  document.getElementById('btnTpl').classList.toggle('active', mode==='tpl');
  document.getElementById('styleFilterWrap').style.display = mode==='case' ? 'flex' : 'none';
  document.getElementById('sceneFilterWrap').style.display = mode==='case' ? 'flex' : 'none';
  doSearch();
}

// ============ Helpers ============
function findItem(id, mode){
  var pool = mode === 'case' ? ALL_CASES : ALL_TEMPLATES;
  for(var i=0; i<pool.length; i++){
    if(String(pool[i].id) === String(id)) return pool[i];
  }
  return null;
}

function escHtml(s){
  var d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

// ============ Start ============
init();
</script>
</body>
</html>''')

# ---------- Write to file ----------
out_path = os.path.join(BASE, 'search-engine.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(''.join(html_parts))

size_kb = os.path.getsize(out_path) / 1024
print(f'✅ Built: search-engine.html ({size_kb:.1f} KB)')
print(f'   Cases: {len(cases)}')
print(f'   Templates: {len(TEMPLATES)}')
print(f'   Images on disk: {len(have_img)}')
print(f'   404 marked: {len(nf_ids)}')
print(f'   Data: embedded in <script type=application/json> (works under file://)')
