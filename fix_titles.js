/**
 * 标题修复 v4 - 最终版
 * 1. 从 GitHub 原始数据恢复全部标题
 * 2. 对161条重复标题案例，精准提取 prompt 中的核心描述
 * 3. 确保同组内每条标题唯一
 */
const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, 'data', 'cases-full.json');
const htmlPath = path.join(__dirname, 'search-engine.html');
const origPath = path.join(__dirname, 'data', 'cases-orig.json');

// Load original titles
const origCases = JSON.parse(fs.readFileSync(origPath, 'utf8')).cases;
const origTitleMap = {};
origCases.forEach(c => { origTitleMap[c.id] = c.title; });
console.log(`原始数据: ${origCases.length} 条案例`);

// Load current data
const raw = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
const cases = raw.cases;

// Step 1: Restore ALL original titles
let restored = 0;
cases.forEach(c => {
  if (origTitleMap[c.id] && c.title !== origTitleMap[c.id]) {
    c.title = origTitleMap[c.id];
    restored++;
  }
});
console.log(`恢复了 ${restored} 个原始标题`);

// Step 2: Find duplicate titles
const titleMap = {};
cases.forEach(c => {
  if (!titleMap[c.title]) titleMap[c.title] = [];
  titleMap[c.title].push(c.id);
});
const dupeTitles = new Set(Object.keys(titleMap).filter(t => titleMap[t].length > 1));

// Step 3: Generate unique descriptive titles for each duplicate
function extractTitle(prompt) {
  if (!prompt) return null;
  let p = prompt.trim();

  // === Strategy 1: [中文]... format ===
  if (p.includes('[中文]')) {
    const cnMatch = p.match(/\[中文\][\.\s]*([^\[]+)/s);
    if (cnMatch) {
      let cn = cnMatch[1].replace(/\n/g, ' ').trim();
      cn = cn.replace(/\{argument[^}]*default="([^"]*)"[^}]*\}/g, '$1');
      cn = cn.replace(/\{[^}]*\}/g, '');
      cn = cn.replace(/\s+/g, ' ').trim();
      if (cn.length > 50) {
        const idx = cn.search(/[。，！？；:]/);
        if (idx > 5 && idx < 50) cn = cn.substring(0, idx);
        else cn = cn.substring(0, 47) + '…';
      }
      if (cn.length >= 4) return cn;
    }
  }

  // === Strategy 2: Chinese at start ===
  if (/^[\u4e00-\u9fff]/.test(p)) {
    let cn = p.replace(/\n/g, ' ').trim();
    cn = cn.replace(/\{argument[^}]*default="([^"]*)"[^}]*\}/g, '$1');
    cn = cn.replace(/\{[^}]*\}/g, '');
    cn = cn.replace(/\s+/g, ' ').trim();
    if (cn.length > 50) {
      const idx = cn.search(/[。，！？；:]/);
      if (idx > 5 && idx < 50) cn = cn.substring(0, idx);
      else cn = cn.substring(0, 47) + '…';
    }
    if (cn.length >= 4) return cn;
  }

  // === Strategy 3: JSON structured ===
  const jsonStart = p.indexOf('{');
  if (jsonStart >= 0 && jsonStart < 5) {
    const jsonStr = p.substring(jsonStart);
    try {
      const obj = JSON.parse(jsonStr);
      let parts = [];
      if (obj.type) parts.push(String(obj.type));
      if (obj.theme) {
        if (typeof obj.theme === 'string') parts.push(obj.theme);
      }
      if (obj.subject) {
        if (typeof obj.subject === 'string') parts.push(obj.subject.substring(0, 40));
        else if (obj.subject.description) parts.push(obj.subject.description.split(',')[0].substring(0, 40));
      }
      if (obj.title) parts.push(String(obj.title));
      if (obj.product) {
        if (typeof obj.product === 'string') parts.push(obj.product);
        else if (obj.product.label) parts.push(obj.product.label);
        else if (obj.product.type) parts.push(obj.product.type);
      }
      if (obj.character && obj.character.name) parts.push(obj.character.name);
      if (parts.length > 0) {
        let t = parts.join(' · ');
        t = t.replace(/\{argument[^}]*default="([^"]*)"[^}]*\}/g, '$1');
        t = t.replace(/\{[^}]*\}/g, '');
        if (t.length > 60) t = t.substring(0, 57) + '…';
        if (t.length >= 4) return t;
      }
    } catch(e) {
      // Regex fallback
      const typeMatch = jsonStr.match(/"type"\s*:\s*"([^"]+)"/);
      const themeMatch = jsonStr.match(/"theme"\s*:\s*"([^"]+)"/);
      const descMatch = jsonStr.match(/"description"\s*:\s*"([^"]+)"/);
      let parts = [];
      if (typeMatch) parts.push(typeMatch[1]);
      if (themeMatch) parts.push(themeMatch[1]);
      if (descMatch) parts.push(descMatch[1].substring(0, 40));
      if (parts.length > 0) {
        let t = parts.join(' · ');
        t = t.replace(/\{argument[^}]*default="([^"]*)"[^}]*\}/g, '$1');
        t = t.replace(/\{[^}]*\}/g, '');
        if (t.length > 60) t = t.substring(0, 57) + '…';
        if (t.length >= 4) return t;
      }
    }
  }

  // === Strategy 4: Natural language ===
  let nl = p;
  nl = nl.replace(/\{argument[^}]*default="([^"]*)"[^}]*\}/g, '$1');
  nl = nl.replace(/\{[^}]*\}/g, '');
  nl = nl.replace(/\b\d{3,4}\s*[x×]\s*\d{3,4}\b/g, '');
  nl = nl.replace(/^(Create|Generate|Design|Make|Draw|Produce|Render|Illustrate|Craft|Build|Using|Please)\s+(a|an|the|this|me)?\s*/i, '');
  nl = nl.replace(/^(A|An|The|This)\s+/i, '');
  nl = nl.replace(/\s+/g, ' ').trim();

  let first = nl.split(/[.\n;]/)[0].trim();
  if (first.length < 15) {
    first = nl.split(/[.\n;]/).slice(0, 2).join('. ').trim();
  }
  if (first.length > 55) first = first.substring(0, 52) + '…';
  if (first.length >= 4) return first;

  return null;
}

const titleUpdates = {};
const groupNewTitles = {}; // oldTitle -> [{id, newTitle}]

cases.forEach(c => {
  if (!dupeTitles.has(c.title)) return;
  const newTitle = extractTitle(c.prompt);
  if (newTitle && newTitle !== c.title) {
    if (!groupNewTitles[c.title]) groupNewTitles[c.title] = [];
    groupNewTitles[c.title].push({ id: c.id, newTitle });
  }
});

// Resolve conflicts: if multiple cases in same group get same title, add distinguishing suffix
Object.entries(groupNewTitles).forEach(([oldTitle, items]) => {
  // Group by new title to find conflicts
  const byNew = {};
  items.forEach(item => {
    if (!byNew[item.newTitle]) byNew[item.newTitle] = [];
    byNew[item.newTitle].push(item.id);
  });

  items.forEach(item => {
    let finalTitle = item.newTitle;
    const group = byNew[item.newTitle];
    if (group.length > 1) {
      // Add ID-based suffix to differentiate
      const idx = group.indexOf(item.id);
      finalTitle = finalTitle.length > 48 ? finalTitle.substring(0, 48) : finalTitle;
      finalTitle += ` #${idx + 1}`;
    }
    titleUpdates[item.id] = { old: oldTitle, new: finalTitle };
    const c = cases.find(x => x.id === item.id);
    if (c) c.title = finalTitle;
  });
});

// For cases where extractTitle returned null, keep original + add #N
titleMap && Object.entries(titleMap).filter(([t, ids]) => dupeTitles.has(t)).forEach(([oldTitle, ids]) => {
  ids.forEach((id, idx) => {
    if (!titleUpdates[id]) {
      const suffix = ` #${idx + 1}`;
      titleUpdates[id] = { old: oldTitle, new: oldTitle + suffix };
      const c = cases.find(x => x.id === id);
      if (c) c.title = oldTitle + suffix;
    }
  });
});

console.log(`\n更新了 ${Object.keys(titleUpdates).length} 个案例标题\n`);

// Show results grouped by original title
const byOld = {};
Object.entries(titleUpdates).forEach(([id, v]) => {
  if (!byOld[v.old]) byOld[v.old] = [];
  byOld[v.old].push({ id: parseInt(id), new: v.new });
});
Object.entries(byOld).sort((a,b) => b[1].length - a[1].length).forEach(([oldTitle, items]) => {
  console.log(`【${oldTitle}】(${items.length}条)`);
  items.forEach(item => console.log(`  ID ${item.id}: "${item.new}"`));
  console.log();
});

// Save cases-full.json
fs.writeFileSync(dataPath, JSON.stringify(raw, null, 2), 'utf8');
console.log('data/cases-full.json 已更新');

// Update search-engine.html
let html = fs.readFileSync(htmlPath, 'utf8');
const marker = '<script id="data-cases" type="application/json">';
const endMarker = '</script>';
const si = html.indexOf(marker);
if (si === -1) { console.error('No data-cases tag!'); process.exit(1); }
const ji = si + marker.length;
const je = html.indexOf(endMarker, ji);
const embedded = JSON.parse(html.substring(ji, je));
let eu = 0;
embedded.forEach(c => {
  if (titleUpdates[c.id]) { c.title = titleUpdates[c.id].new; eu++; }
});
console.log(`HTML中更新了 ${eu} 个案例标题`);
html = html.substring(0, ji) + JSON.stringify(embedded) + html.substring(je);
fs.writeFileSync(htmlPath, html, 'utf8');
console.log('search-engine.html 已更新');

// Save mapping
fs.writeFileSync(path.join(__dirname, 'data', 'title-updates.json'), JSON.stringify(titleUpdates, null, 2), 'utf8');
console.log('data/title-updates.json 已保存');
