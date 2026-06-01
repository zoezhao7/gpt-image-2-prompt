const fs = require('fs');
const htmlPath = 'C:/Users/Administrator/WorkBuddy/2026-05-31-10-53-55/gpt-image-prompts/search-engine.html';

// Category mapping: feishu -> GitHub standard categories
const CAT_MAP = {
  '人像写真': 'Characters & People',
  '商业广告': 'Products & E-commerce',
  '海报主视觉': 'Posters & Typography',
  '百科信息图': 'Charts & Infographics',
  '角色卡设定': 'Characters & People',
  'UI界面与荧幕版型': 'UI & Interfaces',
  '产品摄影(更多相关内容收录在Vol:12)': 'Products & E-commerce',
  '场景摄影': 'Photography & Realism',
  '插画与艺术风格': 'Illustration & Art',
  '社群视觉与版型': 'Posters & Typography',
  '建筑与空间设计专辑': 'Architecture & Spaces'
};

// Style mapping based on category
const STYLE_MAP = {
  'Characters & People': ['Character'],
  'Products & E-commerce': ['Product'],
  'Posters & Typography': ['Poster'],
  'Charts & Infographics': ['Infographic'],
  'UI & Interfaces': ['UI'],
  'Photography & Realism': ['Photography', 'Realistic'],
  'Illustration & Art': ['Illustration'],
  'Architecture & Spaces': ['Architecture']
};

const feishuData = JSON.parse(fs.readFileSync('C:/Users/Administrator/WorkBuddy/2026-05-31-10-53-55/gpt-image-prompts/data/feishu-100-cases.json', 'utf8'));

// Convert to GitHub format
const converted = feishuData.map(c => {
  const cat = CAT_MAP[c.category] || 'Other Use Cases';
  const styles = STYLE_MAP[cat] || [];
  // Truncate prompt for preview
  const promptPreview = c.prompt.length > 120 ? c.prompt.substring(0, 120) + '...' : c.prompt;

  return {
    id: c.id,
    title: c.title.replace(/\\-/g, '-').replace(/\\\(/g, '(').replace(/\\\)/g, ')'),
    image: '',  // No local images yet (feishu CDN requires auth)
    imageAlt: c.title,
    sourceLabel: '飞书100组Prompt合集',
    sourceUrl: '',
    prompt: c.prompt,
    promptPreview: promptPreview,
    category: cat,
    styles: styles,
    scenes: [],
    featured: false,
    githubUrl: '',
    h: false,  // No local image
    nf: true,  // Mark as no image file
    feishu: true  // Flag to identify feishu source
  };
});

console.log('Converted feishu cases:', converted.length);

// Read current HTML
let html = fs.readFileSync(htmlPath, 'utf8');

// Find the embedded cases JSON
const startTag = '<script id="data-cases" type="application/json">';
const endTag = '</script>';
const startIdx = html.indexOf(startTag);
if (startIdx === -1) {
  console.error('Cannot find data-cases script tag!');
  process.exit(1);
}
const jsonStart = startIdx + startTag.length;
const jsonEnd = html.indexOf(endTag, jsonStart);
const existingJson = html.substring(jsonStart, jsonEnd);

let existingCases;
try {
  existingCases = JSON.parse(existingJson);
  console.log('Existing cases:', existingCases.length);
} catch(e) {
  console.error('Failed to parse existing JSON:', e.message);
  process.exit(1);
}

// Merge: append feishu cases (no duplicates by id)
const existingIds = new Set(existingCases.map(c => c.id));
const newCases = converted.filter(c => !existingIds.has(c.id));
console.log('New feishu cases to add:', newCases.length);

const merged = existingCases.concat(newCases);
console.log('Total merged cases:', merged.length);

// Write back
const mergedJson = JSON.stringify(merged);
const newHtml = html.substring(0, jsonStart) + mergedJson + html.substring(jsonEnd);

fs.writeFileSync(htmlPath, newHtml);
console.log('HTML updated successfully!');

// Also update ALL_CASES count reference in the text if any
console.log('Done! Total cases: ' + merged.length);
