const fs = require('fs');
const md = fs.readFileSync('C:/Users/Administrator/Downloads/GPT Image 2全球开放使用!100组Prompt合集.md', 'utf8');

// Split into lines
const lines = md.split('\n');

// Section mapping: ## 01-xxx => {num: "01", name: "xxx"}
const sections = [];
// Cases: each with id, title, category, prompt, imageUrls
const cases = [];

let currentSection = '';
let currentCase = null;
let inCodeBlock = false;
let codeContent = '';

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];

  // Track code blocks
  if (line.startsWith('```')) {
    if (inCodeBlock) {
      // End of code block
      if (currentCase && codeContent.trim()) {
        currentCase.prompt = codeContent.trim();
      }
      inCodeBlock = false;
      codeContent = '';
    } else {
      inCodeBlock = true;
      codeContent = '';
    }
    continue;
  }

  if (inCodeBlock) {
    codeContent += line + '\n';
    continue;
  }

  // Section heading: ## 01\-人像写真  or ## **02.** 商业广告
  // The \- is literal backslash-dash in the markdown
  let sectionMatch = line.match(/^##\s+(?:\*\*)?(\d+)[\-\\.\s]+(?:\*\*)?\s*(.+)/);
  if (!sectionMatch) {
    sectionMatch = line.match(/^##\s+\*\*(\d+)\.\*\*\s*(.+)/);
  }
  if (sectionMatch) {
    currentSection = sectionMatch[2].replace(/\*+/g, '').replace(/\\\)/g, ')').replace(/\\\(/g, '(').trim();
    sections.push({ num: sectionMatch[1], name: currentSection });
    continue;
  }

  // Case heading: ### **1001.** 室内棚拍-烟雾缭绕(Vol:1)
  // Various formats:
  // ### **1001.** 室内棚拍-烟雾缭绕(Vol:1)
  // ### 1015.**俯视厨房女厨师**
  // ### 1017\.蜘蛛精
  // ### **1018\.绝美唐风凤冠佳人的微醺特写**
  // ### 1020\. 韩系女友私密白衬衫特写
  let caseMatch = line.match(/^###\s+(?:\*\*)?(\d{4})[\.\\]+(?:\*\*)?\s*(.+)/);
  if (!caseMatch) {
    caseMatch = line.match(/^###\s+\*\*(\d{4})[\.\\]+\*\*\s*(.+)/);
  }
  if (!caseMatch) {
    // Try: ### 1024\.签名照
    caseMatch = line.match(/^###\s+(\d{4})[\.\\]+\s*(.+)/);
  }
  if (caseMatch) {
    // Save previous case
    if (currentCase) {
      cases.push(currentCase);
    }
    const caseId = parseInt(caseMatch[1]);
    const caseTitle = caseMatch[2].replace(/\*+/g, '').replace(/\\\./g, '.').replace(/\-/g, '-').trim();
    currentCase = {
      id: caseId,
      title: caseTitle,
      category: currentSection,
      prompt: '',
      imageUrls: []
    };
    continue;
  }

  // Image URLs (feishu CDN)
  let imgMatch = line.match(/!\[Image\]\((https?:\/\/[^\)]+)\)/);
  if (imgMatch && currentCase) {
    currentCase.imageUrls.push(imgMatch[1]);
  }

  // Skip non-case lines (ad headings, empty headings, etc.)
  if (line.match(/^###\s*$/) || line.match(/^###\s+\[/) || line.match(/^###\s+告别/) || line.match(/^###\s+基础/) || line.match(/^###\s+七大/) || line.match(/^###\s+与/)) {
    continue;
  }
}

// Don't forget last case
if (currentCase) {
  cases.push(currentCase);
}

// Filter out cases without prompts
const validCases = cases.filter(c => c.prompt && c.prompt.length > 10);

console.log('Total cases parsed:', cases.length);
console.log('Cases with prompts:', validCases.length);
console.log('Sections:', sections.map(s => s.num + '-' + s.name).join(', '));

// Show category distribution
const catDist = {};
validCases.forEach(c => {
  catDist[c.category || '未知'] = (catDist[c.category || '未知'] || 0) + 1;
});
console.log('\nCategory distribution:');
Object.entries(catDist).forEach(([k, v]) => console.log('  ' + k + ': ' + v));

// Show cases without prompts
const noPrompt = cases.filter(c => !c.prompt || c.prompt.length <= 10);
if (noPrompt.length > 0) {
  console.log('\nCases WITHOUT prompts (' + noPrompt.length + '):');
  noPrompt.forEach(c => console.log('  ' + c.id + ': ' + c.title + ' (images: ' + c.imageUrls.length + ')'));
}

// Save valid cases as JSON
const output = validCases.map(c => ({
  id: c.id,
  title: c.title,
  category: c.category,
  prompt: c.prompt,
  imageCount: c.imageUrls.length,
  sourceLabel: '飞书100组Prompt合集',
  sourceUrl: ''
}));

fs.writeFileSync('C:/Users/Administrator/WorkBuddy/2026-05-31-10-53-55/gpt-image-prompts/data/feishu-100-cases.json', JSON.stringify(output, null, 2));
console.log('\nSaved to data/feishu-100-cases.json');
