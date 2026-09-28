const fs = require('fs');
const js = fs.readFileSync('E:/AIGC/课件/12小说/site/assets/tutorial.js','utf-8');
const m = js.match(/const SIDEBAR = (\[[\s\S]*?\n\]);/);
const SIDEBAR = eval('(' + m[1] + ')');
console.log('=== SIDEBAR 当前实际数据 ===');
SIDEBAR.slice(0, 9).forEach(g => {
  const lbl = g.title || g.label;
  console.log(`${g.code}: title="${g.title}" label="${g.label}"`);
  console.log(`  split(' · '): ${JSON.stringify(lbl.split(' · '))}`);
  console.log(`  split(' · ')[1]: "${lbl.split(' · ')[1]}"`);
  console.log(`  fallback: "${lbl.split(' · ')[1] || lbl}"`);
});
