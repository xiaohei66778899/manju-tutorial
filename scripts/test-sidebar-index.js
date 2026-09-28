const fs = require('fs');
const js = fs.readFileSync('E:/AIGC/课件/12小说/site/assets/tutorial.js','utf-8');
const sidebarMatch = js.match(/const SIDEBAR = (\[[\s\S]*?\n\]);/);
const SIDEBAR = eval('(' + sidebarMatch[1] + ')');
const DONE_PAGES = new Set();  // 简化

function groupCodeToDir(code) {
  const map = {A:'manju-basic',B:'novel-to-script',C:'character',D:'storyboard',E:'ai-image',F:'ai-video',G:'audio-edit',H:'publish',I:'appendix'};
  return map[code];
}

// 模拟 tutorial/index.html
const mockPath = '/site/tutorial/index.html';
const currentId = null;
const currentGroup = null;
const segments = mockPath.split('/').filter(s => s);
const levelsToRoot = segments.length - 1;
const rootPrefix = '../'.repeat(levelsToRoot);
console.log(`=== ${mockPath} (currentGroup=${currentGroup}) ===`);
console.log(`levelsToRoot=${levelsToRoot}, rootPrefix="${rootPrefix}"`);
SIDEBAR.forEach(g => {
  if (!g.pages || g.pages.length === 0) return;
  const p = g.pages[0];
  let href;
  if (p.external && p.href) {
    if (p.href.startsWith('../')) {
      href = rootPrefix + p.href.substring(3);
    } else if (currentGroup === g.code || currentGroup === null) {
      href = p.href;
    } else {
      href = '../' + p.href;
    }
  } else {
    href = (currentGroup === g.code) ? `${p.id}.html` : `../${g.code}-${groupCodeToDir(g.code)}/${p.id}.html`;
  }
  console.log(`  ${g.code || g.id}: ${p.id} → ${href}`);
});
