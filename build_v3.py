#!/usr/bin/env python3
"""Build the complete GPT-Image-2 search engine HTML with ALL 481 cases + templates."""

import json
import os

# Load data
base = r'C:\Users\Administrator\WorkBuddy\2026-05-31-10-53-55\gpt-image-prompts'

with open(os.path.join(base, 'data', 'cases-full.json'), 'r', encoding='utf-8') as f:
    raw = json.load(f)

cases = raw['cases']
categories = raw['categories']
styles = raw['styles']
scenes = raw['scenes']

# Build templates from style-library.md (the 22 templates we already have)
templates = [
    {"id": "ui-screenshot-system", "name": "UI 截图系统", "category": "UI & Interfaces", "desc": "App 截图、仪表盘、社媒截图和直播界面"},
    {"id": "infographic-engine", "name": "信息图引擎", "category": "Charts & Infographics", "desc": "解释图、技术图解、时间线和知识卡片"},
    {"id": "scientific-scale-diagram", "name": "科学尺度缩放图", "category": "Charts & Infographics", "desc": "微观到宏观的尺度对比展示"},
    {"id": "poster-layout-system", "name": "海报排版系统", "category": "Posters & Typography", "desc": "活动海报、电影海报、封面和社媒传播视觉"},
    {"id": "sports-campaign-poster", "name": "运动商业Campaign", "category": "Posters & Typography", "desc": "运动品牌Campaign、运动员海报和运动产品视觉"},
    {"id": "conceptual-typography-poster", "name": "概念字体海报", "category": "Posters & Typography", "desc": "标题文字成为主视觉结构的海报"},
    {"id": "ink-double-exposure-poster", "name": "水墨双重曝光海报", "category": "Posters & Typography", "desc": "诗意人像海报、水墨氛围和文化主题视觉"},
    {"id": "nature-science-poster", "name": "自然科普海报", "category": "Posters & Typography", "desc": "自然主题的高级干净科普海报"},
    {"id": "product-commerce-visual", "name": "商品商业视觉", "category": "Products & E-commerce", "desc": "商品主图、包装视觉、详情页和销售卖点排版"},
    {"id": "personalized-beauty-report", "name": "个性化美妆报告", "category": "Products & E-commerce", "desc": "美妆推荐、肤质报告、导购助手和生活方式商品卡片"},
    {"id": "brand-identity-package", "name": "品牌身份包", "category": "Brand & Logos", "desc": "Logo系统、品牌板、VI套件和应用样机"},
    {"id": "brand-touchpoint-board", "name": "品牌触点视觉板", "category": "Brand & Logos", "desc": "多触点Campaign展示和品牌落地预览"},
    {"id": "architecture-space", "name": "建筑与空间", "category": "Architecture & Spaces", "desc": "室内、建筑表现、城市地图和空间规划"},
    {"id": "realistic-photography", "name": "写实摄影", "category": "Photography & Realism", "desc": "人像、街拍、商品摄影和电影感写实"},
    {"id": "street-accident-moment", "name": "街头意外瞬间", "category": "Photography & Realism", "desc": "街头抓拍、意外泼洒和手机纪实"},
    {"id": "illustration-art-style", "name": "插画与艺术风格", "category": "Illustration & Art", "desc": "动漫、水彩、水墨、装饰画和风格实验"},
    {"id": "character-design-sheet", "name": "角色设定表", "category": "Characters & People", "desc": "角色设定表、动作网格和一致性参考"},
    {"id": "3d-collectible-toy", "name": "3D收藏玩具", "category": "Characters & People", "desc": "高级收藏玩具、头像公仔和潮玩角色"},
    {"id": "scene-storytelling", "name": "场景叙事", "category": "Scenes & Storytelling", "desc": "分镜、世界观和情绪叙事画面"},
    {"id": "history-classical-themes", "name": "历史与古风题材", "category": "History & Classical Themes", "desc": "古风题材、长卷、朝代服饰和诗词视觉"},
    {"id": "document-publishing", "name": "文档与出版物", "category": "Documents & Publishing", "desc": "白皮书、手册、百科图鉴和报告页面"},
    {"id": "concept-product-breakdown", "name": "概念产品拆解", "category": "Other Use Cases", "desc": "实验型任务、研发视觉板和拆解图"},
]

print(f"Cases: {len(cases)}, Templates: {len(templates)}, Categories: {len(categories)}")

# Build search text for each case (for performance, pre-compute)
for c in cases:
    search_text = f"{c['title']} {c['category']} {' '.join(c.get('styles',[]))} {' '.join(c.get('scenes',[]))} {c.get('sourceLabel','')} {c.get('prompt','')[:200]}"
    c['_search'] = search_text.lower()

# Generate HTML
cases_json = json.dumps(cases, ensure_ascii=False)
templates_json = json.dumps(templates, ensure_ascii=False)
categories_json = json.dumps(categories, ensure_ascii=False)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GPT-Image-2 提示词搜索引擎 — 481条案例 + 22套模板</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f1117; color: #e1e4e8; }}
.header {{ background: linear-gradient(135deg, #1a1c2e 0%, #2a1a3e 50%, #1a1c2e 100%); padding: 20px 24px; border-bottom: 1px solid #2d3047; position: sticky; top: 0; z-index: 100; }}
.header h1 {{ font-size: 22px; background: linear-gradient(135deg, #a78bfa, #f472b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 4px; }}
.header .sub {{ font-size: 13px; color: #8b8fa3; }}
.search-bar {{ display: flex; gap: 8px; margin-top: 12px; flex-wrap: wrap; }}
.search-bar input {{ flex: 1; min-width: 200px; padding: 10px 16px; background: #1e2130; border: 1px solid #353a50; border-radius: 8px; color: #e1e4e8; font-size: 14px; outline: none; }}
.search-bar input:focus {{ border-color: #a78bfa; }}
.search-bar input::placeholder {{ color: #555; }}
.filter-group {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: 2px; }}
.filter-group select, .filter-group button {{ padding: 8px 12px; background: #1e2130; border: 1px solid #353a50; border-radius: 6px; color: #c9cdd4; font-size: 12px; cursor: pointer; }}
.filter-group select:focus, .filter-group button:hover {{ border-color: #a78bfa; }}
.filter-group button.active {{ background: #a78bfa22; border-color: #a78bfa; color: #a78bfa; }}
.stats {{ padding: 12px 24px; background: #141720; border-bottom: 1px solid #2d3047; font-size: 13px; color: #8b8fa3; display: flex; justify-content: space-between; align-items: center; }}
.stats .count {{ color: #a78bfa; font-weight: 600; }}
.mode-tabs {{ display: flex; gap: 4px; }}
.mode-tabs button {{ padding: 6px 14px; background: transparent; border: 1px solid #353a50; border-radius: 6px; color: #8b8fa3; font-size: 12px; cursor: pointer; }}
.mode-tabs button.active {{ background: #a78bfa22; border-color: #a78bfa; color: #a78bfa; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 12px; padding: 16px 24px; max-height: calc(100vh - 200px); overflow-y: auto; }}
.card {{ background: #1a1d2e; border: 1px solid #2d3047; border-radius: 10px; padding: 16px; transition: all 0.2s; display: flex; flex-direction: column; }}
.card:hover {{ border-color: #a78bfa44; transform: translateY(-1px); box-shadow: 0 4px 20px rgba(0,0,0,0.3); }}
.card .card-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }}
.card .case-id {{ font-size: 11px; color: #555; font-family: monospace; }}
.card .case-title {{ font-size: 14px; font-weight: 600; color: #e1e4e8; line-height: 1.4; flex: 1; margin-right: 8px; }}
.card .badges {{ display: flex; gap: 4px; flex-wrap: wrap; margin-bottom: 8px; }}
.card .badge {{ font-size: 10px; padding: 2px 8px; border-radius: 10px; white-space: nowrap; }}
.badge-cat {{ background: #a78bfa22; color: #a78bfa; }}
.badge-style {{ background: #f472b622; color: #f472b6; }}
.badge-scene {{ background: #34d39922; color: #34d399; }}
.card .source {{ font-size: 11px; color: #555; margin-bottom: 8px; }}
.card .source a {{ color: #a78bfa; text-decoration: none; }}
.card .prompt {{ background: #0f1117; border: 1px solid #2d3047; border-radius: 6px; padding: 10px; font-size: 12px; color: #8b8fa3; line-height: 1.5; max-height: 120px; overflow-y: auto; white-space: pre-wrap; word-break: break-all; flex: 1; }}
.card .card-footer {{ display: flex; gap: 8px; margin-top: 10px; }}
.card .btn {{ padding: 6px 14px; border-radius: 6px; font-size: 11px; cursor: pointer; border: none; transition: all 0.2s; }}
.btn-copy {{ background: #a78bfa22; color: #a78bfa; border: 1px solid #a78bfa44; }}
.btn-copy:hover {{ background: #a78bfa33; }}
.btn-view {{ background: #1e2130; color: #8b8fa3; border: 1px solid #353a50; }}
.btn-view:hover {{ background: #2d3047; }}
.btn-copied {{ background: #34d39922 !important; color: #34d399 !important; border-color: #34d39944 !important; }}
.empty {{ text-align: center; padding: 60px 20px; color: #555; font-size: 15px; grid-column: 1 / -1; }}
.empty .icon {{ font-size: 48px; margin-bottom: 12px; }}
.template-card {{ background: linear-gradient(135deg, #1a1c2e, #2a1a3e); border-color: #a78bfa33; }}
.template-card .card-header::before {{ content: "📋"; margin-right: 6px; }}
.loading {{ text-align: center; padding: 40px; color: #8b8fa3; }}

@media (max-width: 768px) {{
  .grid {{ grid-template-columns: 1fr; padding: 12px; }}
  .search-bar {{ flex-direction: column; }}
}}

/* Scrollbar */
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: #0f1117; }}
::-webkit-scrollbar-thumb {{ background: #353a50; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: #a78bfa44; }}
</style>
</head>
<body>
<div class="header">
  <h1>🐾 GPT-Image-2 提示词搜索引擎</h1>
  <div class="sub">基于 awesome-gpt-image-2 仓库 · 481条案例 · 13大分类 · 全部含完整提示词</div>
  <div class="search-bar">
    <input type="text" id="searchInput" placeholder="搜索提示词... 例如：海报 水墨、直播 截图、信息图 城市、Logo 品牌..." oninput="doSearch()">
  </div>
  <div class="filter-group">
    <select id="catFilter" onchange="doSearch()">
      <option value="">全部分类</option>
    </select>
    <select id="styleFilter" onchange="doSearch()">
      <option value="">全部风格</option>
    </select>
    <select id="sceneFilter" onchange="doSearch()">
      <option value="">全部场景</option>
    </select>
    <button id="featuredBtn" onclick="toggleFeatured()">⭐ 精选 (26)</button>
  </div>
</div>

<div class="stats">
  <div class="mode-tabs">
    <button class="active" id="tabCases" onclick="switchMode('cases')">📦 案例 <span class="count" id="caseCount">481</span></button>
    <button id="tabTemplates" onclick="switchMode('templates')">📋 模板 <span class="count">22</span></button>
  </div>
  <span id="resultInfo">显示 481 条</span>
</div>

<div class="grid" id="grid"></div>

<script>
const ALL_CASES = {cases_json};
const TEMPLATES = {templates_json};
const ALL_CATEGORIES = {categories_json};

let mode = 'cases';
let showFeatured = false;
let currentResults = [];

function init() {{
  // Populate filters
  const catSel = document.getElementById('catFilter');
  ALL_CATEGORIES.forEach(c => {{
    const opt = document.createElement('option');
    opt.value = c; opt.textContent = c;
    catSel.appendChild(opt);
  }});
  
  // Populate style filter
  const allStyles = [...new Set(ALL_CASES.flatMap(c => c.styles || []))].sort();
  const styleSel = document.getElementById('styleFilter');
  allStyles.forEach(s => {{
    const opt = document.createElement('option');
    opt.value = s; opt.textContent = s;
    styleSel.appendChild(opt);
  }});
  
  // Populate scene filter
  const allScenes = [...new Set(ALL_CASES.flatMap(c => c.scenes || []))].sort();
  const sceneSel = document.getElementById('sceneFilter');
  allScenes.forEach(s => {{
    const opt = document.createElement('option');
    opt.value = s; opt.textContent = s;
    sceneSel.appendChild(opt);
  }});
  
  doSearch();
}}

function switchMode(m) {{
  mode = m;
  document.getElementById('tabCases').classList.toggle('active', m === 'cases');
  document.getElementById('tabTemplates').classList.toggle('active', m === 'templates');
  doSearch();
}}

function toggleFeatured() {{
  showFeatured = !showFeatured;
  document.getElementById('featuredBtn').classList.toggle('active', showFeatured);
  doSearch();
}}

function doSearch() {{
  const query = document.getElementById('searchInput').value.toLowerCase().trim();
  const catFilter = document.getElementById('catFilter').value;
  const styleFilter = document.getElementById('styleFilter').value;
  const sceneFilter = document.getElementById('sceneFilter').value;
  
  if (mode === 'templates') {{
    let results = [...TEMPLATES];
    if (query) {{
      results = results.filter(t => 
        (t.name + ' ' + t.category + ' ' + t.desc).toLowerCase().includes(query)
      );
    }}
    if (catFilter) {{
      results = results.filter(t => t.category === catFilter);
    }}
    currentResults = results;
    renderTemplates(results);
    document.getElementById('resultInfo').textContent = `显示 ${{results.length}} 套模板`;
  }} else {{
    let results = ALL_CASES;
    if (query) {{
      results = results.filter(c => c._search.includes(query));
    }}
    if (catFilter) {{
      results = results.filter(c => c.category === catFilter);
    }}
    if (styleFilter) {{
      results = results.filter(c => (c.styles || []).includes(styleFilter));
    }}
    if (sceneFilter) {{
      results = results.filter(c => (c.scenes || []).includes(sceneFilter));
    }}
    if (showFeatured) {{
      results = results.filter(c => c.featured);
    }}
    currentResults = results;
    renderCases(results);
    document.getElementById('resultInfo').textContent = `显示 ${{results.length}} 条案例`;
  }}
  document.getElementById('caseCount').textContent = mode === 'cases' ? currentResults.length : '';
}}

function renderCases(cases) {{
  const grid = document.getElementById('grid');
  if (cases.length === 0) {{
    grid.innerHTML = '<div class="empty"><div class="icon">🔍</div>没有找到匹配的提示词<br>试试换一个关键词或分类筛选</div>';
    return;
  }}
  
  // Limit to 200 for performance, show first 200
  const display = cases.slice(0, 200);
  let html = '';
  for (const c of display) {{
    const badges = [];
    badges.push(`<span class="badge badge-cat">${{c.category}}</span>`);
    (c.styles || []).slice(0, 2).forEach(s => badges.push(`<span class="badge badge-style">${{s}}</span>`));
    (c.scenes || []).slice(0, 2).forEach(s => badges.push(`<span class="badge badge-scene">${{s}}</span>`));
    
    const promptPreview = (c.prompt || '').length > 300 
      ? c.prompt.substring(0, 300) + '...' 
      : (c.prompt || '');
    
    const featuredStar = c.featured ? ' ⭐' : '';
    
    html += `
    <div class="card" data-id="${{c.id}}">
      <div class="card-header">
        <span class="case-title">#${{c.id}}${{featuredStar}} ${{c.title}}</span>
      </div>
      <div class="badges">${{badges.join('')}}</div>
      <div class="source">来源: <a href="${{c.sourceUrl || '#'}}" target="_blank">${{c.sourceLabel || '未知'}}</a></div>
      <div class="prompt">${{escapeHtml(promptPreview)}}</div>
      <div class="card-footer">
        <button class="btn btn-copy" onclick="copyPrompt(${{c.id}}, this)">📋 复制提示词</button>
        ${{c.sourceUrl ? `<a href="${{c.sourceUrl}}" target="_blank"><button class="btn btn-view">🔗 查看原帖</button></a>` : ''}}
      </div>
    </div>`;
  }}
  
  if (cases.length > 200) {{
    html += `<div class="empty" style="padding:20px">📌 共 ${{cases.length}} 条结果，显示前 200 条。请使用更精确的搜索词或筛选条件缩小范围。</div>`;
  }}
  
  grid.innerHTML = html;
}}

function renderTemplates(templates) {{
  const grid = document.getElementById('grid');
  if (templates.length === 0) {{
    grid.innerHTML = '<div class="empty"><div class="icon">📋</div>没有找到匹配的模板</div>';
    return;
  }}
  
  let html = '';
  for (const t of templates) {{
    html += `
    <div class="card template-card">
      <div class="card-header">
        <span class="case-title">${{t.name}}</span>
      </div>
      <div class="badges">
        <span class="badge badge-cat">${{t.category}}</span>
      </div>
      <div style="font-size:13px;color:#8b8fa3;margin-bottom:8px;">${{t.desc}}</div>
      <div style="font-size:12px;color:#555;margin-bottom:8px;">模板ID: <code>${{t.id}}</code></div>
      <div class="card-footer">
        <span style="font-size:11px;color:#555;">💡 此模板需结合具体场景替换 [方括号] 变量使用</span>
      </div>
    </div>`;
  }}
  grid.innerHTML = html;
}}

function copyPrompt(id, btn) {{
  const c = ALL_CASES.find(x => x.id === id);
  if (!c || !c.prompt) return;
  
  navigator.clipboard.writeText(c.prompt).then(() => {{
    btn.textContent = '✅ 已复制!';
    btn.classList.add('btn-copied');
    setTimeout(() => {{
      btn.textContent = '📋 复制提示词';
      btn.classList.remove('btn-copied');
    }}, 1500);
  }}).catch(() => {{
    // Fallback
    const ta = document.createElement('textarea');
    ta.value = c.prompt;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    btn.textContent = '✅ 已复制!';
    btn.classList.add('btn-copied');
    setTimeout(() => {{
      btn.textContent = '📋 复制提示词';
      btn.classList.remove('btn-copied');
    }}, 1500);
  }});
}}

function escapeHtml(text) {{
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}}

init();
</script>
</body>
</html>'''

# Write output
out_path = os.path.join(base, 'search-engine.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)

size_mb = os.path.getsize(out_path) / (1024 * 1024)
print(f'Generated: {out_path} ({size_mb:.2f} MB)')
print(f'Cases: {len(cases)}, Templates: {len(templates)}, Total entries: {len(cases) + len(templates)}')
