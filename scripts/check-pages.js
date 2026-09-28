const fs = require('fs');
const js = fs.readFileSync('E:/AIGC/课件/12小说/site/assets/tutorial.js','utf-8');
const m = js.match(/const SIDEBAR = (\[[\s\S]*?\n\]);/);
const SIDEBAR = eval('(' + m[1] + ')');
SIDEBAR.forEach(g => {
  console.log(`  ${g.code || g.id}: ${g.pages ? g.pages.length : 0} 页 · title=${g.title || g.label}`);
});
