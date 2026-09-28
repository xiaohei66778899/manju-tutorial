const fs = require('fs');
const jsContent = fs.readFileSync('E:/AIGC/课件/12小说/site/assets/tutorial.js', 'utf-8');
const sidebarMatch = jsContent.match(/const SIDEBAR = (\[[\s\S]*?\n\]);/);
const sidebarData = eval('(' + sidebarMatch[1] + ')');

// 用真实 groupCodeToDir
function groupCodeToDir(code) {
  const map = {
    A: 'manju-basic', B: 'novel-to-script', C: 'character', D: 'storyboard',
    E: 'ai-image', F: 'ai-video', G: 'audio-edit', H: 'publish', I: 'appendix'
  };
  return map[code];
}

const segments = '/site/tutorial/A-manju-basic/A-1.html'.split('/').filter(s => s);
const levelsToRoot = segments.length - 1;
const rootPrefix = '../'.repeat(levelsToRoot);
const currentGroup = 'A';
console.log('A-1.html 下 sidebar 各组 href:');
sidebarData.forEach(g => {
  if (!g.pages || g.pages.length === 0) return;
  console.log(`  ${g.code}: ${JSON.stringify(g.pages.map(p => {
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
      const targetDir = groupCodeToDir(g.code);
      href = (currentGroup === g.code) ? `${p.id}.html` : `../${g.code}-${targetDir}/${p.id}.html`;
    }
    return `${p.id} -> ${href}`;
  }))}`);
});
