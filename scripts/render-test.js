// 不依赖 jsdom,自己拼一个 DOM 模拟
const fs = require('fs');

// 读取 tutorial/index.html
const html = fs.readFileSync('E:/AIGC/课件/12小说/site/tutorial/index.html', 'utf-8');

// 读取 tutorial.js 提取 SIDEBAR 数据
const js = fs.readFileSync('E:/AIGC/课件/12小说/site/assets/tutorial.js', 'utf-8');
const m = js.match(/const SIDEBAR = (\[[\s\S]*?\n\]);/);
const SIDEBAR = eval('(' + m[1] + ')');

// 模拟 DOM
const mockPath = '/site/tutorial/index.html';
global.window = { location: { pathname: mockPath } };

// 复制关键函数
function groupCodeToDir(code) {
  const map = {A:'manju-basic',B:'novel-to-script',C:'character',D:'storyboard',E:'ai-image',F:'ai-video',G:'audio-edit',H:'publish',I:'appendix'};
  return map[code];
}

const currentId = null;
const currentGroup = null;
const depth = (mockPath.match(/\/site\/tutorial\/[^/]+\//)) ? '../../' : '../';
const segments = mockPath.split('/').filter(s => s);
const levelsToRoot = segments.length - 1;
const rootPrefix = '../'.repeat(levelsToRoot);

let html_output = '';
SIDEBAR.forEach(group => {
  const targetDir = groupCodeToDir(group.code || group.id);
  const groupLabel = group.title || group.label || (group.code || group.id);
  const groupCode = group.code || group.id;
  html_output += `<div class="group-title">${groupCode} · ${groupLabel.split(' · ')[1] || groupLabel}</div><ul>`;
  group.pages.forEach(p => {
    let href;
    if (p.external && p.href) {
      if (p.href.startsWith('../')) {
        href = rootPrefix + p.href.substring(3);
      } else if (currentGroup === group.code || currentGroup === null) {
        href = p.href;
      } else {
        href = '../' + p.href;
      }
    } else {
      href = (currentGroup === group.code)
        ? `${p.id}.html`
        : `../${group.code}-${targetDir}/${p.id}.html`;
    }
    html_output += `<li><a href="${href}">${p.id} ${p.title}</a></li>`;
  });
  html_output += '</ul>';
});

console.log('=== tutorial/index.html 下 sidebar 渲染输出 ===');
console.log(html_output);
