const fs = require('fs');

const jsContent = fs.readFileSync('E:/AIGC/课件/12小说/site/assets/tutorial.js', 'utf-8');
const sidebarMatch = jsContent.match(/const SIDEBAR = (\[[\s\S]*?\n\]);/);
const sidebarData = eval('(' + sidebarMatch[1] + ')');

function testPath(mockPath) {
  const depth = (mockPath.match(/\/site\/tutorial\/[^/]+\//)) ? '../../' : '../';
  const segments = mockPath.split('/').filter(s => s);
  const levelsToRoot = segments.length - 1;
  const rootPrefix = '../'.repeat(levelsToRoot);
  const match = mockPath.match(/([A-I])-(\d+)\.html/);
  const currentGroup = match ? match[1] : null;
  console.log(`\n=== ${mockPath} (group=${currentGroup}) ===`);
  
  sidebarData.forEach(g => {
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
      href = (currentGroup === g.code)
        ? `${p.id}.html`
        : `../${g.code}-manju-basic/${p.id}.html`;
    }
    console.log(`  ${g.code} · ${p.id} → ${href}`);
  });
}

testPath('/site/tutorial/A-manju-basic/A-1.html');
testPath('/site/tutorial/index.html');
testPath('/site/tutorial/C-character/C-1.html');
